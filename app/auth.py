from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from pathlib import Path
from fastapi import Request, HTTPException, status

from .paths import PROJECT_ROOT
from .storage import get_setting, update_settings


def hash_password(password: str) -> str:
    """对密码进行加盐 SHA256 哈希"""
    salt = os.urandom(16).hex()
    pbkdf2_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{pbkdf2_hash.hex()}"


def verify_password(password: str, hashed_value: str) -> bool:
    """验证密码是否匹配"""
    if not hashed_value:
        return False
    # 初始默认明文密码兼容
    if hashed_value == "admin" and password == "admin":
        return True
    if ":" not in hashed_value:
        # 兼容不带盐的纯 sha256 哈希
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_value
    
    salt, hash_hex = hashed_value.split(":", 1)
    pbkdf2_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return hmac.compare_digest(pbkdf2_hash.hex(), hash_hex)


def get_secret_key() -> str:
    """获取 Cookie 签名密钥，不存在则生成"""
    key = get_setting("secret_key")
    if not key:
        key = os.urandom(32).hex()
        update_settings({"secret_key": key})
    return key


def sign_cookie(data: str, secret: str) -> str:
    """对 Cookie 进行签名"""
    sig = hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
    sig_str = base64.urlsafe_b64encode(sig).decode('utf-8').rstrip('=')
    return f"{data}.{sig_str}"


def verify_cookie(cookie_value: str, secret: str) -> str | None:
    """验证 Cookie 签名，失败返回 None"""
    if not cookie_value or "." not in cookie_value:
        return None
    try:
        parts = cookie_value.split(".", 1)
        data, sig_str = parts[0], parts[1]
        expected_sig = hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
        expected_sig_str = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')
        # 对齐 '=' 填充以确保 urlsafe_b64encode 一致性
        if hmac.compare_digest(sig_str, expected_sig_str):
            return data
    except Exception:
        pass
    return None


def auto_import_credentials() -> None:
    """从本地 credentials.json 自动导入 WorldQuant 凭据（若 SQLite 中为空）"""
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    if not username or not password:
        cred_path = PROJECT_ROOT / "credentials.json"
        if cred_path.exists():
            try:
                with cred_path.open("r", encoding="utf-8") as f:
                    cred = json.load(f)
                user = cred.get("email") or cred.get("username")
                pwd = cred.get("password")
                if user and pwd:
                    update_settings({
                        "wq_username": user,
                        "wq_password": pwd
                    })
            except Exception:
                pass


def handle_env_password_override() -> None:
    """使用环境变量 WQ_GUI_ADMIN_PASSWORD 覆盖初始默认密码"""
    env_pwd = os.environ.get("WQ_GUI_ADMIN_PASSWORD")
    if env_pwd:
        current_pwd = get_setting("admin_password")
        # 仅当当前密码是默认的 "admin" 时允许覆盖
        if current_pwd == "admin":
            update_settings({"admin_password": hash_password(env_pwd)})


def get_current_admin(request: Request) -> str:
    """FastAPI 路由依赖：验证管理员登录状态"""
    secret = get_secret_key()
    cookie_val = request.cookies.get("admin_session")
    
    admin_user = verify_cookie(cookie_val, secret) if cookie_val else None
    if not admin_user:
        # 判断请求类型，API 请求返回 401，页面请求重定向到 /login
        path = request.url.path
        is_api = path.startswith("/api/") or "application/json" in request.headers.get("Accept", "")
        if is_api:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                headers={"Location": "/login"},
                detail="Redirecting to login"
            )
    return admin_user
