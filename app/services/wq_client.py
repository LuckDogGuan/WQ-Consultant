from __future__ import annotations

import logging
import requests
from typing import Any

from consultant_core.machine_lib import get_daily_alpha_count

logger = logging.getLogger(__name__)


class WQRateLimitError(RuntimeError):
    pass


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
        if response.status_code == 429:
            raise WQRateLimitError(f"WorldQuant Brain login rate limited (status=429): {msg}")
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
    from ..storage import get_setting
    try:
        limit = int(get_setting("backtest_daily_limit", "4500"))
        usage = get_setting("daily_alpha_count_usage", "track")
        timezone_name = get_setting("alpha_date_timezone", "Asia/Shanghai")
        status = get_setting("daily_alpha_count_status", "UNSUBMITTED%1FIS_FAIL")
        
        count = get_daily_alpha_count(
            alpha_num=limit,
            usage=usage,
            timezone_name=timezone_name,
            status=status,
            session=session
        )
        logger.info(f"Retrieved current daily alpha count: {count}")
        return count
    except Exception as e:
        logger.error(f"Failed to fetch daily alpha count: {e}")
        raise


def retire_wq_alpha(session: requests.Session, alpha_id: str) -> bool:
    """DELETE the simulation/alpha on the WQ platform to hide/retire it."""
    url = f"https://api.worldquantbrain.com/simulations/{alpha_id}"
    try:
        resp = session.delete(url, timeout=30)
        logger.info(f"Retire simulation {alpha_id} on WQ platform: status={resp.status_code}")
        return resp.status_code in (200, 204, 404)  # 200/204 means deleted, 404 means already gone
    except Exception as e:
        logger.error(f"Failed to retire simulation {alpha_id} on WQ: {e}")
        return False
