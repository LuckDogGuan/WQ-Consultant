#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WorldQuant Consultant GUI - 部署环境检测脚本
"""
import os
import sys
import json
import sqlite3
import urllib.request
import time
from pathlib import Path

# 定义颜色
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def log_ok(msg: str):
    print(f"[{GREEN}OK{RESET}] {msg}")

def log_warn(msg: str):
    print(f"[{YELLOW}WARN{RESET}] {msg}")

def log_err(msg: str):
    print(f"[{RED}ERROR{RESET}] {msg}")

def main():
    # 强制设置 sys.stdout 编码为 utf-8，解决 Windows 控制台输出中文乱码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    print("=" * 60)
    print("       WorldQuant Consultant GUI 部署环境检测")
    print("=" * 60)
    
    # 1. 检测 Python 版本
    py_ver = sys.version_info
    py_ver_str = f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"
    if py_ver.major == 3 and py_ver.minor >= 8:
        log_ok(f"Python 版本: {py_ver_str} (符合要求 >= 3.8)")
    else:
        log_err(f"Python 版本: {py_ver_str} (不符合要求，建议使用 >= 3.8)")

    # 2. 检测依赖包
    req_packages = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "jinja2": "jinja2",
        "multipart": "python-multipart",
        "pandas": "pandas",
        "requests": "requests",
        "openpyxl": "openpyxl"
    }
    missing_packages = []
    for pkg_import, pkg_name in req_packages.items():
        try:
            __import__(pkg_import)
            log_ok(f"依赖项导入成功: {pkg_name}")
        except ImportError:
            missing_packages.append(pkg_name)
            log_err(f"缺失依赖项: {pkg_name}")
            
    if missing_packages:
        print(f"\n{YELLOW}请先运行以下命令安装缺失的依赖库：{RESET}")
        print("pip install -r requirements.txt\n")

    # 3. 路径及写权限检测
    gui_dir = Path(__file__).resolve().parent
    data_dir = gui_dir / "data"
    logs_dir = gui_dir / "logs"
    
    # 检测 data 目录
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        test_file = data_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        log_ok(f"数据目录读写权限正常: {data_dir}")
    except Exception as e:
        log_err(f"数据目录无写权限: {data_dir} (错误: {e})")

    # 检测 logs 目录
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
        test_file = logs_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        log_ok(f"日志目录读写权限正常: {logs_dir}")
    except Exception as e:
        log_err(f"日志目录无写权限: {logs_dir} (错误: {e})")

    # 4. WQ Brain API 网络检测
    api_url = "https://api.worldquantbrain.com"
    print(f"\n正在检测连接 WQ Brain API ({api_url})...")
    start_time = time.time()
    try:
        # 3 秒超时
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.0) as response:
            pass
        latency = (time.time() - start_time) * 1000
        log_ok(f"成功连接至 WQ Brain API (延迟: {latency:.1f}ms)")
    except urllib.error.HTTPError:
        # HTTPError 说明网络完全连通且收到服务器响应（通常是 401，因为没带身份令牌）
        latency = (time.time() - start_time) * 1000
        log_ok(f"成功连通 WQ Brain API (收到响应且延迟: {latency:.1f}ms)")
    except Exception as e:
        log_err(f"无法访问 WQ Brain API! 错误: {e}")
        log_warn("如果在内网或服务器上运行，请配置 http_proxy/https_proxy 环境变量。")

    # 5. 凭证(Credentials)检测
    print("\n正在检测 WQ Brain 凭据配置...")
    cred_file = gui_dir.parent / "credentials.json"
    db_file = data_dir / "gui.db"
    
    cred_found = False
    cred_username = ""
    
    # 优先检测本地 credentials.json
    if cred_file.exists():
        try:
            with open(cred_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                email = data.get("email") or data.get("username")
                pwd = data.get("password")
                if email and pwd:
                    cred_found = True
                    cred_username = email
                    log_ok(f"在 {cred_file.name} 中找到凭证, 账号: {email[:3]}***{email[email.find('@'):] if '@' in email else ''}")
        except Exception as e:
            log_warn(f"解析 credentials.json 失败: {e}")

    # 检测数据库中的配置
    if not cred_found and db_file.exists():
        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
            row_user = conn.execute("SELECT value FROM settings WHERE key = 'wq_username'").fetchone()
            row_pwd = conn.execute("SELECT value FROM settings WHERE key = 'wq_password'").fetchone()
            conn.close()
            if row_user and row_pwd and row_user["value"] and row_pwd["value"]:
                cred_found = True
                user = row_user["value"]
                cred_username = user
                log_ok(f"在本地 SQLite 数据库中找到凭证, 账号: {user[:3]}***{user[user.find('@'):] if '@' in user else ''}")
        except Exception:
            pass

    if not cred_found:
        log_warn("未检测到 WQ 凭证配置！系统将运行在未登录状态。请在 UI 界面登录后，至“系统设置”页面填写 WorldQuant 账号与密码。")

    # 6. 安全与配置环境变量检测
    print("\n正在检测环境变量配置...")
    admin_pwd_env = os.environ.get("WQ_GUI_ADMIN_PASSWORD")
    if admin_pwd_env:
        log_ok("环境变量 WQ_GUI_ADMIN_PASSWORD 已配置 (将覆盖默认初始密码 admin)")
    else:
        log_warn("未设置环境变量 WQ_GUI_ADMIN_PASSWORD。初始默认登录密码为 admin，建议在服务器部署时设置该环境变量以提升安全性。")

    proxy_http = os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY")
    proxy_https = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    if proxy_http or proxy_https:
        log_ok(f"已检测到代理配置: HTTP={proxy_http}, HTTPS={proxy_https}")
    else:
        log_warn("未检测到代理环境变量 (如需要请配置 http_proxy/https_proxy)")

    print("=" * 60)
    print("                     部署建议与注意事项")
    print("=" * 60)
    print("1. 【安全第一】:")
    print("   * 生产环境部署必须修改默认管理员密码 (密码初始为 admin)，或者通过环境变量 `WQ_GUI_ADMIN_PASSWORD` 注入。")
    print("   * 请勿将 credentials.json 或 gui/data/gui.db 提交到公开 Git 仓库中。")
    print("2. 【反向代理与 HTTPS】:")
    print("   * 强烈建议在服务器上使用 Nginx 或 Apache 作为反向代理，并配置 SSL/TLS (HTTPS) 提供外网访问。")
    print("   * 本程序已配置为：在 HTTPS 协议下自动将 admin_session Cookie 的 Secure 属性设为 True，防止会话劫持。")
    print("3. 【进程守候】:")
    print("   * 在服务器后台运行，建议使用 Systemd、PM2 或 Docker 容器管理该 GUI 服务进程。")
    print("   * 命令行启动范例: python run_gui.py --host 0.0.0.0 --port 8765 --no-browser")
    print("=" * 60)

if __name__ == "__main__":
    main()
