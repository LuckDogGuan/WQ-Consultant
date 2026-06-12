from __future__ import annotations

import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from typing import Any

from ..paths import CATALOG_DIR, CORRELATION_DIR, PROJECT_ROOT
from ..storage import get_setting, update_job, add_job_event
from .wq_client import login_with_credentials

logger = logging.getLogger(__name__)


def ensure_catalog_data() -> None:
    """如果 GUI 本地缓存为空，自动复制外界的 data_catalog 快照以实现数据隔离运行"""
    # 1. 复制 EQUITY 目录
    target_equity = CATALOG_DIR / "EQUITY"
    source_equity = PROJECT_ROOT / "data_catalog" / "EQUITY"
    if not target_equity.exists() or not any(target_equity.iterdir()):
        if source_equity.exists() and any(source_equity.iterdir()):
            logger.info(f"Cloning data catalog snapshot from {source_equity} to {target_equity}...")
            shutil.copytree(source_equity, target_equity, dirs_exist_ok=True)
            logger.info("Data catalog snapshot cloned successfully.")
        else:
            logger.warning("No external data catalog EQUITY snapshot found to copy.")

    # 2. 复制 correlation_data (.pickle 文件)
    source_corr = PROJECT_ROOT / "data_catalog" / "correlation_data"
    if not CORRELATION_DIR.exists() or not any(CORRELATION_DIR.iterdir()):
        if source_corr.exists() and any(source_corr.iterdir()):
            logger.info(f"Cloning correlation data snapshot from {source_corr} to {CORRELATION_DIR}...")
            CORRELATION_DIR.mkdir(parents=True, exist_ok=True)
            copied_count = 0
            for f in source_corr.glob("*.pickle"):
                shutil.copy2(f, CORRELATION_DIR / f.name)
                copied_count += 1
            logger.info(f"Copied {copied_count} correlation pickle files.")
        else:
            logger.warning("No external correlation data snapshot found to copy.")


def get_scope_path(region: str, universe: str, delay: int, instrument_type: str = "EQUITY") -> Path:
    """获取指定 Scope 的绝对路径"""
    return CATALOG_DIR / instrument_type / region / universe / f"delay_{delay}"


def check_cache_expired(region: str, universe: str, delay: int, instrument_type: str = "EQUITY") -> tuple[bool, str]:
    """检查缓存是否超过 7 天。返回 (is_expired, last_refresh_str)"""
    scope_path = get_scope_path(region, universe, delay, instrument_type)
    manifest_path = scope_path / "catalog_manifest.json"
    if not manifest_path.exists():
        return True, "无缓存"
    
    import json
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        last_refresh_str = manifest.get("last_refresh_at")
        if not last_refresh_str:
            return True, "未记录刷新时间"
        
        last_refresh = datetime.fromisoformat(last_refresh_str)
        now = datetime.now(timezone.utc)
        delta = now - last_refresh
        return delta.days >= 7, last_refresh.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"Failed to parse manifest: {e}")
        return True, "解析错误"


def load_datasets_from_cache(region: str, universe: str, delay: int, instrument_type: str = "EQUITY") -> list[dict[str, Any]]:
    """从本地缓存加载 datasets 列表"""
    scope_path = get_scope_path(region, universe, delay, instrument_type)
    datasets_excel = scope_path / "datasets.xlsx"
    if not datasets_excel.exists():
        return []
    
    try:
        df = pd.read_excel(datasets_excel, sheet_name="datasets")
        # 填充 NaN 为空字符串
        df = df.fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load datasets from cache: {e}")
        return []


def load_fields_from_cache(region: str, universe: str, delay: int, dataset_id: str, instrument_type: str = "EQUITY") -> list[dict[str, Any]]:
    """从本地缓存加载指定 dataset_id 的字段列表"""
    scope_path = get_scope_path(region, universe, delay, instrument_type)
    dataset_excel = scope_path / "by_dataset" / f"{dataset_id}.xlsx"
    if not dataset_excel.exists():
        return []
    
    try:
        df = pd.read_excel(dataset_excel, sheet_name="datafields")
        df = df.fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load fields for {dataset_id}: {e}")
        return []


def run_catalog_refresh(job_id: int) -> None:
    """JobRunner 调用的后台任务：刷新数据目录"""
    # 1. 确保目录环境存在
    ensure_catalog_data()
    
    # 2. 读取配置参数
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    
    import json
    from ..storage import connect
    with connect() as conn:
        row = conn.execute("SELECT params FROM jobs WHERE id = ?", (job_id,)).fetchone()
        job_params = json.loads(row["params"]) if (row and row["params"]) else {}
        
    region = job_params.get("region") or get_setting("region", "USA")
    universe = job_params.get("universe") or get_setting("universe", "TOP3000")
    delay = job_params.get("delay") or get_setting("delay", "1")
    delay = int(delay)
    instrument_type = get_setting("instrument_type", "EQUITY")
    
    if not username or not password:
        raise ValueError("Missing WorldQuant credentials in Settings.")
        
    update_job(job_id, message="Logging in to WorldQuant Brain...")
    session = login_with_credentials(username, password)
    
    try:
        update_job(job_id, message=f"Refreshing catalog for {region}/{universe} (delay={delay})...")
        add_job_event(job_id, "info", f"Starting remote catalog refresh for {region}/{universe}.")
        
        # 动态加载 machine_lib 的 refresh_catalog 并执行
        from consultant_core.catalog_cache import refresh_catalog
        
        res = refresh_catalog(
            session=session,
            output_root=CATALOG_DIR,
            instrument_type=instrument_type,
            region=region,
            universe=universe,
            delay=delay,
            force=True  # 页面触发属于用户明确命令，强制刷新
        )
        
        refreshed_ids = res.get("refreshed_dataset_ids", [])
        field_count = res.get("datafield_count", 0)
        
        msg = f"Catalog refreshed successfully. Refreshed {len(refreshed_ids)} datasets, total {field_count} fields."
        logger.info(msg)
        update_job(
            job_id,
            progress_current=100,
            progress_total=100,
            message=msg
        )
        add_job_event(job_id, "info", msg, {"refreshed_datasets": refreshed_ids, "field_count": field_count})
        
    finally:
        session.close()
        logger.info("WorldQuant session closed in catalog refresh job.")


def get_cached_scopes() -> dict[str, dict[str, list[int]]]:
    """扫描本地缓存目录并返回已缓存的地区、股票池和延时映射结构"""
    root = CATALOG_DIR / "EQUITY"
    mapping = {}
    if not root.exists():
        return mapping
    for r in root.iterdir():
        if r.is_dir() and r.name != 'correlation_data':
            universes = {}
            for u in r.iterdir():
                if u.is_dir():
                    # 寻找形如 delay_1, delay_2 的文件夹
                    delays = []
                    for d in u.iterdir():
                        if d.is_dir() and d.name.startswith("delay_"):
                            try:
                                delays.append(int(d.name.split("_")[-1]))
                            except ValueError:
                                pass
                    if delays:
                        universes[u.name] = sorted(delays)
            if universes:
                mapping[r.name] = universes
    return mapping


REGION_DISPLAY_NAMES = {
    "USA": "USA (美国)",
    "CHN": "CHN (中国)",
    "HKG": "HKG (中国香港)",
    "TWN": "TWN (中国台湾)",
    "JPN": "JPN (日本)",
    "KOR": "KOR (韩国)",
    "EUR": "EUR (欧洲)",
    "ASI": "ASI (亚洲)",
    "GLB": "GLB (全球)",
    "IND": "IND (印度)",
    "MEA": "MEA (中东非洲)"
}


def get_all_day1_scopes() -> dict[str, Any]:
    """读取 day1_scope_index.xlsx 获取所有可用的地区、股票池与延迟的对应关系"""
    excel_path = CATALOG_DIR / "EQUITY" / "day1_scope_index.xlsx"
    if not excel_path.exists():
        excel_path = PROJECT_ROOT / "data_catalog" / "EQUITY" / "day1_scope_index.xlsx"
    
    fallback_scopes = {
        "USA": ["TOP3000", "TOP2000", "TOP1000", "TOP500"],
        "CHN": ["TOP3000", "TOP2000", "TOP1000", "TOP500"],
        "EUR": ["TOP1200"],
        "JPN": ["TOP1600"],
        "GLB": ["TOP3000", "MINVOL1M"],
        "KOR": ["TOP600"],
        "ASI": ["MINVOL1M", "ILLIQUID_MINVOL1M"],
        "HKG": ["TOP1000", "TOP500"],
        "TWN": ["TOP1000", "TOP500"],
        "IND": ["TOP3000", "TOP2000", "TOP1000"],
        "MEA": ["TOP3000", "TOP2000"]
    }
    fallback_delays = {
        "USA": ["1", "0"],
        "CHN": ["1", "0"]
    }
    
    if not excel_path.exists():
        logger.warning(f"day1_scope_index.xlsx not found, using hardcoded fallback.")
        return {"scopes": fallback_scopes, "delays": fallback_delays}
        
    try:
        df = pd.read_excel(excel_path)
        # 筛选有效且数据集大于0的组合
        valid = df[(df["available"] == True) & (df["dataset_count"] > 0)]
        
        scopes = {}
        delays = {}
        for region, group in valid.groupby("region"):
            # 保证唯一排序
            scopes[region] = sorted(list(group["universe"].unique()))
            delays[region] = sorted([str(int(d)) for d in group["delay"].unique()])
            
        return {"scopes": scopes, "delays": delays}
    except Exception as e:
        logger.error(f"Error reading day1_scope_index.xlsx: {e}, using fallback.")
        return {"scopes": fallback_scopes, "delays": fallback_delays}

