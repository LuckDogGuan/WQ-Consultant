from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .paths import DB_PATH, ensure_dirs


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@contextmanager
def connect():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                status TEXT NOT NULL,
                title TEXT NOT NULL,
                params TEXT NOT NULL,
                progress_current INTEGER NOT NULL DEFAULT 0,
                progress_total INTEGER NOT NULL DEFAULT 0,
                message TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS job_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                payload TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alpha_records (
                alpha_id TEXT PRIMARY KEY,
                alpha_type TEXT NOT NULL DEFAULT '',
                name TEXT NOT NULL DEFAULT '',
                region TEXT NOT NULL DEFAULT '',
                universe TEXT NOT NULL DEFAULT '',
                sharpe REAL,
                fitness REAL,
                prod_corr REAL,
                ppa_corr REAL,
                margin REAL,
                returns REAL,
                drawdown REAL,
                status TEXT NOT NULL DEFAULT '',
                source TEXT NOT NULL DEFAULT '',
                platform_url TEXT NOT NULL DEFAULT '',
                payload TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS check_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alpha_id TEXT NOT NULL,
                result TEXT NOT NULL,
                prod_corr REAL,
                source TEXT NOT NULL DEFAULT '',
                message TEXT NOT NULL DEFAULT '',
                payload TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area TEXT NOT NULL,
                message TEXT NOT NULL,
                payload TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );
            """
        )
        
        # Schema migration: check and add margin, returns, drawdown if they do not exist
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(alpha_records)")
        existing_cols = {col[1] for col in cursor.fetchall()}
        for col_name, col_type in [("margin", "REAL"), ("returns", "REAL"), ("drawdown", "REAL")]:
            if col_name not in existing_cols:
                try:
                    conn.execute(f"ALTER TABLE alpha_records ADD COLUMN {col_name} {col_type}")
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(f"Failed to add column {col_name} to alpha_records: {e}")
                    
        seed_defaults(conn)


DEFAULT_SETTINGS = {
    "admin_password": "admin",
    "wq_username": "",
    "wq_password": "",
    "region": "USA",
    "universe": "TOP3000",
    "delay": "1",
    "instrument_type": "EQUITY",
    "backtest_children": "5",
    "backtest_threads": "8",
    "fo_backtest_children": "6",
    "fo_backtest_threads": "10",
    "so_backtest_children": "5",
    "so_backtest_threads": "8",
    "th_backtest_children": "5",
    "th_backtest_threads": "8",
    "alpha_date_timezone": "Asia/Shanghai",
    "alpha_fetch_limit_multiplier": "3",
    "daily_alpha_count_usage": "track",
    "daily_alpha_count_status": "UNSUBMITTED%1FIS_FAIL",
    "backtest_max_jobs": "3",
    "backtest_daily_limit": "4500",
    "check_daily_limit": "4500",
    "check_threads": "3",
    "poll_minutes": "20",
    "blocked_start_cn": "00:00",
    "blocked_end_cn": "00:00",
    "auto_rename": "1",
    "weekly_catalog_refresh": "1",
    # 相关性检测与 check_submission 相关参数
    "corr_threshold_sharpe": "1.0",
    "corr_threshold_fitness": "0.7",
    "corr_lookback_days": "14",
    "corr_fetch_limit": "",
    "corr_workers": "5",
    "submit_lookback_days": "30",
    "submit_sharpe": "1.58",
    "submit_fitness": "1.0",
    "submit_alpha_num": "200",
    "submit_daily_regular_limit": "4",
    "submit_daily_super_limit": "1",
    # 提交检查配置过滤与定时任务调度
    "check_lookback_days": "60",
    "check_max_candidates": "4000",
    "check_schedule_enabled": "0",
    "check_schedule_hour": "0",
    "check_schedule_interval_hours": "24",
    "check_schedule_last_run": "",
    # 相关性检测定时任务调度
    "corr_schedule_enabled": "0",
    "corr_schedule_hour": "11",
    "corr_schedule_lookback_days": "7",
    "corr_schedule_max_candidates": "4000",
    "corr_schedule_last_run": "",
    # 跟踪过滤相关参数
    "fo_track_lookback_days": "90",
    "fo_track_sharpe": "1.0",
    "fo_track_fitness": "0.7",
    "fo_track_alpha_num": "100",
    "so_track_lookback_days": "90",
    "so_track_sharpe": "1.3",
    "so_track_fitness": "0.8",
    "so_track_alpha_num": "100",
    "prune_keep_num": "5",
    "prune_prefix_min_share": "0.6",
    "track_fallback_keep_num": "50",
    "group_ops": "group_neutralize,group_rank,group_zscore",
    # 重新连接参数
    "reconnect_short_sleep_seconds": "300",
    "reconnect_long_sleep_seconds": "600",
    # 修改属性二次确认选项
    "need_confirm_on_modify": "0",
    # API 延时判断。超过该毫秒阈值会写入慢请求日志；设为 0 可关闭慢请求记录。
    "api_slow_threshold_ms": "1500",
    "optimization_source_mode": "recent",
    "optimization_recent_days": "14",
    "optimization_candidate_limit": "20",
    "optimization_children_per_request": "1",
    "optimization_schedule_enabled": "0",
    "optimization_schedule_hour": "1",
    "optimization_schedule_last_run": "",
    "submitted_cleanup_schedule_enabled": "1",
    "submitted_cleanup_schedule_hour": "0",
    "submitted_cleanup_schedule_last_run": "",
    "daily_inspection_schedule_enabled": "1",
    "daily_inspection_schedule_hour": "9",
    "daily_inspection_schedule_last_run": "",
    "daily_inspection_lookback_days": "7",
    "daily_inspection_max_candidates": "4000",
    "daily_inspection_auto_submit": "0",
    # 各阶段穿插相关性检查（只使用 Prod 相关性，不使用 PPA）
    # 一阶 FO 结束后检查
    "fo_corr_enable": "1",          # 默认开启
    "fo_corr_sharpe_th": "1.0",     # Sharpe 过滤阈值
    "fo_max_prod_corr": "0.7",      # Prod 最大相关性上限
    # 二阶 SO 结束后检查
    "so_corr_enable": "0",          # 默认关闭
    "so_corr_sharpe_th": "1.2",
    "so_max_prod_corr": "0.7",
    # 三阶 TH 结束后检查
    "th_corr_enable": "0",          # 默认关闭
    "th_corr_sharpe_th": "1.3",
    "th_max_prod_corr": "0.7",
    # 一阶 FO 结束后：自动过滤负夏普垃圾因子（厂字因子最直接识别指标）
    "fo_filter_negative_sharpe": "1",   # 默认开启，直接从数据库删除不展示
}


def seed_defaults(conn: sqlite3.Connection) -> None:
    now = utc_now()
    for key, value in DEFAULT_SETTINGS.items():
        conn.execute(
            "INSERT OR IGNORE INTO settings(key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, now),
        )


def get_setting(key: str, default: str = "") -> str:
    with connect() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default


def get_settings() -> dict[str, str]:
    with connect() as conn:
        return {row["key"]: row["value"] for row in conn.execute("SELECT key, value FROM settings")}


def update_settings(values: dict[str, Any]) -> None:
    now = utc_now()
    with connect() as conn:
        for key, value in values.items():
            conn.execute(
                """
                INSERT INTO settings(key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
                """,
                (key, str(value), now),
            )


def create_job(kind: str, title: str, params: dict[str, Any]) -> int:
    now = utc_now()
    with connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO jobs(kind, status, title, params, created_at, updated_at)
            VALUES (?, 'queued', ?, ?, ?, ?)
            """,
            (kind, title, json.dumps(params, ensure_ascii=False), now, now),
        )
        return int(cur.lastrowid)


def update_job(job_id: int, **fields: Any) -> None:
    if not fields:
        return
    fields["updated_at"] = utc_now()
    keys = list(fields)
    sql = ", ".join(f"{key} = ?" for key in keys)
    values = [fields[key] for key in keys]
    values.append(job_id)
    with connect() as conn:
        conn.execute(f"UPDATE jobs SET {sql} WHERE id = ?", values)


def add_job_event(job_id: int, level: str, message: str, payload: dict[str, Any] | None = None) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO job_events(job_id, level, message, payload, created_at) VALUES (?, ?, ?, ?, ?)",
            (job_id, level, message, json.dumps(payload or {}, ensure_ascii=False), utc_now()),
        )


def add_error(area: str, message: str, payload: dict[str, Any] | None = None) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO errors(area, message, payload, created_at) VALUES (?, ?, ?, ?)",
            (area, message, json.dumps(payload or {}, ensure_ascii=False), utc_now()),
        )


def upsert_alpha(record: dict[str, Any]) -> None:
    alpha_id = record["alpha_id"]
    now = utc_now()
    payload = json.dumps(record.get("payload", {}), ensure_ascii=False)
    
    def clean_str(v, default=""):
        if v is None or v != v:
            return default
        return str(v)
        
    def clean_float(v):
        if v is None or v != v:
            return None
        try:
            return float(v)
        except Exception:
            return None

    with connect() as conn:
        conn.execute(
            """
            INSERT INTO alpha_records(
                alpha_id, alpha_type, name, region, universe, sharpe, fitness,
                prod_corr, ppa_corr, margin, returns, drawdown, status, source, platform_url, payload, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(alpha_id) DO UPDATE SET
                alpha_type = CASE WHEN excluded.alpha_type = '' THEN alpha_records.alpha_type ELSE excluded.alpha_type END,
                name = CASE WHEN excluded.name = '' THEN alpha_records.name ELSE excluded.name END,
                region = excluded.region,
                universe = excluded.universe,
                sharpe = excluded.sharpe,
                fitness = excluded.fitness,
                prod_corr = excluded.prod_corr,
                ppa_corr = excluded.ppa_corr,
                margin = excluded.margin,
                returns = excluded.returns,
                drawdown = excluded.drawdown,
                status = excluded.status,
                source = excluded.source,
                platform_url = excluded.platform_url,
                payload = excluded.payload,
                updated_at = excluded.updated_at
            """,
            (
                alpha_id,
                clean_str(record.get("alpha_type")),
                clean_str(record.get("name")),
                clean_str(record.get("region")),
                clean_str(record.get("universe")),
                clean_float(record.get("sharpe")),
                clean_float(record.get("fitness")),
                clean_float(record.get("prod_corr")),
                clean_float(record.get("ppa_corr")),
                clean_float(record.get("margin")),
                clean_float(record.get("returns")),
                clean_float(record.get("drawdown")),
                clean_str(record.get("status")),
                clean_str(record.get("source")),
                clean_str(record.get("platform_url") or f"https://platform.worldquantbrain.com/alpha/{alpha_id}"),
                payload,
                now,
                now,
            ),
        )


def add_check_result(alpha_id: str, result: str, prod_corr: float | None, message: str, source: str = "", payload: dict[str, Any] | None = None) -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO check_results(alpha_id, result, prod_corr, source, message, payload, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (alpha_id, result, prod_corr, source, message, json.dumps(payload or {}, ensure_ascii=False), utc_now()),
        )


def list_rows(table: str, page: int = 1, page_size: int = 50, where: str = "", params: Iterable[Any] = (), order_by: str = "id DESC") -> tuple[list[sqlite3.Row], int]:
    page = max(1, int(page))
    page_size = max(1, min(200, int(page_size)))
    offset = (page - 1) * page_size
    where_sql = f" WHERE {where}" if where else ""
    with connect() as conn:
        total = conn.execute(f"SELECT COUNT(*) AS n FROM {table}{where_sql}", tuple(params)).fetchone()["n"]
        rows = conn.execute(
            f"SELECT * FROM {table}{where_sql} ORDER BY {order_by} LIMIT ? OFFSET ?",
            tuple(params) + (page_size, offset),
        ).fetchall()
        return rows, int(total)


def list_jobs(limit: int = 20) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()


def delete_job(job_id: int) -> None:
    from .job_runner import JobRunner
    runner = JobRunner()
    # 如果任务在运行，请求暂停
    if job_id in runner.active_jobs:
        runner.pause_job(job_id)
        
    with connect() as conn:
        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.execute("DELETE FROM job_events WHERE job_id = ?", (job_id,))


def list_job_events(job_id: int, limit: int = 200) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM job_events WHERE job_id = ? ORDER BY id DESC LIMIT ?",
            (job_id, limit),
        ).fetchall()


def read_log_tail(path: Path, max_lines: int = 200) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-max_lines:]

