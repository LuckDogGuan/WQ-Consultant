from __future__ import annotations

import logging
import requests
from typing import Any

from consultant_core.machine_lib import get_daily_alpha_count

logger = logging.getLogger(__name__)


def login_with_credentials(username: str, password: str) -> requests.Session:
    """使用指定的账号密码登录 WorldQuant Brain"""
    if not username or not password:
        raise RuntimeError("Missing WorldQuant Brain credentials")
    
    s = requests.Session()
    s.trust_env = False
    s.auth = (username, password)
    
    url = "https://api.worldquantbrain.com/authentication"
    logger.info("Attempting to login to WorldQuant Brain...")
    
    response = s.post(url, timeout=60)
    if response.status_code not in (requests.codes.created, requests.codes.ok):
        try:
            error_data = response.json()
            msg = error_data.get("message", response.text)
        except Exception:
            msg = response.text
        raise RuntimeError(f"WorldQuant Brain login failed (status={response.status_code}): {msg}")
    
    logger.info("WorldQuant Brain login successful.")
    return s


def test_wq_credentials(username: str, password: str) -> bool:
    """测试账号密码是否能成功登录"""
    try:
        session = login_with_credentials(username, password)
        session.close()
        return True
    except Exception as e:
        logger.warning(f"WQ credentials test failed: {e}")
        return False


def get_current_daily_limit_count(session: requests.Session) -> int:
    """获取当天已生成的 Alpha 数量（用于回测额度限制参考）"""
    # 默认使用 usage="track" 统计已提交至系统的 Alpha
    try:
        count = get_daily_alpha_count(session=session, usage="track")
        logger.info(f"Retrieved current daily alpha count: {count}")
        return count
    except Exception as e:
        logger.error(f"Failed to fetch daily alpha count: {e}")
        raise
