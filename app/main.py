from __future__ import annotations
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

import logging
import math
import time as perf_time
from pathlib import Path
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any

from .paths import APP_ROOT, LOG_DIR
from .storage import (
    init_db,
    get_settings,
    update_settings,
    create_job,
    list_jobs,
    list_job_events,
    list_rows,
    get_setting,
    update_job,
    delete_job,
    utc_now,
    connect,
    upsert_alpha
)
from .auth import (
    get_current_admin,
    hash_password,
    verify_password,
    sign_cookie,
    get_secret_key,
    auto_import_credentials,
    handle_env_password_override
)
from .job_runner import JobRunner
from .services.wq_client import test_wq_credentials
from .services.catalog_service import (
    ensure_catalog_data,
    check_cache_expired,
    load_datasets_from_cache,
    load_fields_from_cache,
    get_cached_scopes,
    get_all_day1_scopes,
    REGION_DISPLAY_NAMES
)
from .services.dashboard_metrics import get_dashboard_metrics
from .services.alpha_rating import build_alpha_rating, select_checks_payload

logger = logging.getLogger(__name__)

app = FastAPI(title="WorldQuant Consultant GUI", version="v0.1")


def api_slow_threshold_ms() -> float:
    try:
        return max(0.0, float(get_setting("api_slow_threshold_ms", "1500")))
    except Exception:
        return 1500.0


@app.middleware("http")
async def api_latency_middleware(request: Request, call_next):
    if not request.url.path.startswith("/api/"):
        return await call_next(request)

    started = perf_time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_time.perf_counter() - started) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"

    threshold_ms = api_slow_threshold_ms()
    if threshold_ms and elapsed_ms >= threshold_ms:
        payload = {
            "path": request.url.path,
            "method": request.method,
            "elapsed_ms": round(elapsed_ms, 2),
            "threshold_ms": threshold_ms,
        }
        logger.warning(
            "Slow API request: %s %s took %.2fms",
            request.method,
            request.url.path,
            elapsed_ms,
        )
        try:
            from .storage import add_error

            add_error("api_slow", f"{request.method} {request.url.path} took {elapsed_ms:.2f}ms", payload)
        except Exception:
            logger.debug("Failed to persist slow API record.", exc_info=True)

    return response

import json
# 挂载静态资源和模板
app.mount("/static", StaticFiles(directory=str(APP_ROOT / "app" / "static")), name="static")
def inject_global_settings(request: Request):
    try:
        from .storage import get_setting
        return {
            "need_confirm_on_modify": get_setting("need_confirm_on_modify", "0")
        }
    except Exception:
        return {
            "need_confirm_on_modify": "0"
        }

templates = Jinja2Templates(
    directory=str(APP_ROOT / "app" / "templates"),
    context_processors=[inject_global_settings]
)
templates.env.filters["json_loads"] = json.loads

def format_datetime(value: str) -> str:
    if not value:
        return ""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(value)
        return dt.strftime("%m-%d %H:%M:%S")
    except Exception:
        return value

templates.env.filters["format_datetime"] = format_datetime


from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse
import traceback

@app.exception_handler(Exception)
def debug_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception during request to {request.url.path}:")
    is_api = request.url.path.startswith("/api/") or "application/json" in request.headers.get("Accept", "")
    if is_api:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(exc), "traceback": traceback.format_exc()}
        )
    else:
        err_msg = f"""
        <html>
            <head><title>500 Internal Server Error</title></head>
            <body style="font-family: sans-serif; padding: 20px; background: #f8f9fa;">
                <h2 style="color: #dc3545;">500 Internal Server Error</h2>
                <p><strong>Path:</strong> {request.url.path}</p>
                <p><strong>Error:</strong> {exc}</p>
                <pre style="background: #e9ecef; padding: 15px; border-radius: 5px; overflow-x: auto;">{traceback.format_exc()}</pre>
            </body>
        </html>
        """
        return HTMLResponse(status_code=500, content=err_msg)


@app.get("/api/optimization/plans")
def get_optimization_plans(limit: int = 200, admin: str = Depends(get_current_admin)):
    from .services.optimization_planner import list_optimization_plans

    plans = list_optimization_plans(limit=limit)
    items = [plan.to_dict() for plan in plans]
    return {
        "items": items,
        "total": len(items),
        "optimizable": sum(1 for item in items if item["should_optimize"]),
        "skipped": sum(1 for item in items if not item["should_optimize"]),
    }


@app.post("/api/expressions/validate")
async def post_validate_expression(request: Request, admin: str = Depends(get_current_admin)):
    from .services.expression_validator import validate_expression

    try:
        payload = await request.json()
    except Exception:
        payload = {}
    expression = str(payload.get("expression") or "")
    return validate_expression(expression).to_dict()


@app.get("/api/optimization/variants/{alpha_id}")
def get_optimization_variants(alpha_id: str, max_variants: int = 30, admin: str = Depends(get_current_admin)):
    from .services.alpha_enhancement import generate_variants_for_alpha_id

    plan, variants = generate_variants_for_alpha_id(alpha_id, max_variants=max_variants)
    if plan is None:
        raise HTTPException(status_code=404, detail="Alpha not found.")
    return {
        "plan": plan.to_dict(),
        "items": [variant.to_dict() for variant in variants],
        "total": len(variants),
    }


@app.get("/optimization", response_class=HTMLResponse)
def get_optimization_page(
    request: Request,
    page: int = 1,
    status_filter: str = "",
    level_filter: str = "",
    strategy_filter: str = "",
    limit: int = 500,
    admin: str = Depends(get_current_admin),
):
    from .services.optimization_planner import list_optimization_plans

    page_size = 11
    success_map = {
        "optimization_job_started": "优化任务已启动，可以在下方查看进度。",
        "optimization_schedule_saved": "优化定时设置已保存。",
    }
    success_msg = success_map.get(request.query_params.get("success") or "")
    settings = get_settings()
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'optimization_run' ORDER BY id DESC LIMIT 5").fetchall()
    plans = [plan.to_dict() for plan in list_optimization_plans(limit=limit)]
    if status_filter == "optimizable":
        plans = [plan for plan in plans if plan["should_optimize"]]
    elif status_filter == "skipped":
        plans = [plan for plan in plans if not plan["should_optimize"]]

    if level_filter:
        plans = [plan for plan in plans if plan["level"] == level_filter]
    if strategy_filter:
        plans = [plan for plan in plans if plan["strategy"] == strategy_filter]

    total = len(plans)
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size
    page_items = plans[offset:offset + page_size]
    strategies = sorted({plan["strategy"] for plan in plans if plan["strategy"]})

    return templates.TemplateResponse(
        request,
        "optimization.html",
        {
            "plans": page_items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "status_filter": status_filter,
            "level_filter": level_filter,
            "strategy_filter": strategy_filter,
            "strategies": strategies,
            "optimizable": sum(1 for plan in plans if plan["should_optimize"]),
            "skipped": sum(1 for plan in plans if not plan["should_optimize"]),
            "limit": limit,
            "settings": settings,
            "jobs": jobs,
            "success": success_msg,
        },
    )


@app.get("/optimization/{alpha_id}/variants", response_class=HTMLResponse)
def get_optimization_variants_page(
    request: Request,
    alpha_id: str,
    max_variants: int = 30,
    admin: str = Depends(get_current_admin),
):
    from .services.alpha_enhancement import generate_variants_for_alpha_id

    plan, variants = generate_variants_for_alpha_id(alpha_id, max_variants=max_variants)
    if plan is None:
        raise HTTPException(status_code=404, detail="Alpha not found.")
    return templates.TemplateResponse(
        request,
        "optimization_variants.html",
        {
            "plan": plan.to_dict(),
            "variants": [variant.to_dict() for variant in variants],
            "total": len(variants),
            "max_variants": max_variants,
        },
    )


@app.on_event("startup")
def on_startup():
    """Web 服务启动时初始化配置与数据克隆"""
    init_db()
    JobRunner().init_runner()
    auto_import_credentials()
    handle_env_password_override()
    ensure_catalog_data()
    
    # 启动网络监视器服务
    from .services.network_monitor import NetworkMonitor
    NetworkMonitor().start()
    
    # 启动定时任务调度服务
    from .services.scheduler_service import SchedulerService
    SchedulerService().start()
    
    logger.info("WorldQuant Consultant GUI startup checklist complete.")


@app.on_event("shutdown")
def on_shutdown():
    """Web 服务关闭时释放资源"""
    try:
        from .services.network_monitor import NetworkMonitor
        NetworkMonitor().stop()
    except Exception as e:
        logger.error(f"Error during shutdown network monitor: {e}")
        
    try:
        from .services.scheduler_service import SchedulerService
        SchedulerService().stop()
    except Exception as e:
        logger.error(f"Error during shutdown scheduler: {e}")
        
    logger.info("WorldQuant Consultant GUI shutdown complete.")


# ==========================================
# 登录认证路由
# ==========================================

@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@app.post("/login")
def post_login(request: Request, password: str = Form(...)):
    db_password = get_setting("admin_password")
    
    if verify_password(password, db_password):
        secret = get_secret_key()
        signed_val = sign_cookie("admin", secret)
        is_secure = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="admin_session",
            value=signed_val,
            httponly=True,
            samesite="lax",
            secure=is_secure
        )
        return response
    
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": "管理员密码不正确。"}
    )


@app.get("/logout")
def get_logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("admin_session")
    return response


# ==========================================
# 核心视图路由（使用 get_current_admin 依赖保护）
# ==========================================

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request, admin: str = Depends(get_current_admin)):
    # 读取仪表盘数据统计
    jobs = list_jobs(limit=10)
    
    # 统计数据
    region = get_setting("region", "USA")
    universe = get_setting("universe", "TOP3000")
    delay = int(get_setting("delay", "1"))
    
    expired, refresh_str = check_cache_expired(region, universe, delay)
    datasets = load_datasets_from_cache(region, universe, delay)
    
    counts = get_dashboard_metrics()

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "jobs": jobs,
            "counts": counts,
            "cache_expired": expired,
            "cache_last_refresh": refresh_str,
            "cache_dataset_count": len(datasets),
            "region": region,
            "universe": universe,
            "delay": delay
        }
    )


@app.get("/flow", response_class=HTMLResponse)
def get_flow_page(request: Request, admin: str = Depends(get_current_admin)):
    return templates.TemplateResponse(request, "flow.html", {})


@app.get("/settings", response_class=HTMLResponse)
def get_settings_page(request: Request, admin: str = Depends(get_current_admin)):
    settings = get_settings()
    cached_scopes = get_cached_scopes()
    day1_scopes = get_all_day1_scopes()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    return templates.TemplateResponse(
        request, 
        "settings.html", 
        {
            "settings": settings, 
            "success": success_msg, 
            "cached_scopes": cached_scopes,
            "day1_scopes": day1_scopes,
            "region_names": REGION_DISPLAY_NAMES
        }
    )


@app.post("/settings", response_class=HTMLResponse)
def post_settings_page(
    request: Request,
    admin: str = Depends(get_current_admin),
    admin_password: str = Form(None),
    wq_username: str = Form(None),
    wq_password: str = Form(None),
    region: str = Form("USA"),
    universe: str = Form("TOP3000"),
    delay: str = Form("1"),
    backtest_children: str = Form("5"),
    backtest_threads: str = Form("8"),
    fo_backtest_children: str = Form("6"),
    fo_backtest_threads: str = Form("10"),
    so_backtest_children: str = Form("5"),
    so_backtest_threads: str = Form("8"),
    th_backtest_children: str = Form("5"),
    th_backtest_threads: str = Form("8"),
    alpha_date_timezone: str = Form("Asia/Shanghai"),
    alpha_fetch_limit_multiplier: str = Form("3"),
    daily_alpha_count_usage: str = Form("track"),
    daily_alpha_count_status: str = Form("UNSUBMITTED%1FIS_FAIL"),
    backtest_daily_limit: str = Form("4500"),
    check_daily_limit: str = Form("4500"),
    check_threads: str = Form("3"),
    poll_minutes: str = Form("20"),
    blocked_start_cn: str = Form("00:00"),
    blocked_end_cn: str = Form("00:00"),
    auto_rename: str = Form("0"),
    corr_lookback_days: str = Form("14"),
    corr_fetch_limit: str = Form(""),
    corr_workers: str = Form("5"),
    submit_lookback_days: str = Form("30"),
    submit_sharpe: str = Form("1.58"),
    submit_fitness: str = Form("1.0"),
    submit_alpha_num: str = Form("200"),
    fo_track_lookback_days: str = Form("90"),
    fo_track_sharpe: str = Form("1.0"),
    fo_track_fitness: str = Form("0.7"),
    fo_track_alpha_num: str = Form("100"),
    so_track_lookback_days: str = Form("90"),
    so_track_sharpe: str = Form("1.3"),
    so_track_fitness: str = Form("0.8"),
    so_track_alpha_num: str = Form("100"),
    prune_keep_num: str = Form("5"),
    prune_prefix_min_share: str = Form("0.6"),
    track_fallback_keep_num: str = Form("50"),
    group_ops: str = Form("group_neutralize,group_rank,group_zscore"),
    reconnect_short_sleep_seconds: str = Form("300"),
    reconnect_long_sleep_seconds: str = Form("600"),
    need_confirm_on_modify: str = Form("0")
):
    updates = {
        "region": region,
        "universe": universe,
        "delay": delay,
        "backtest_children": backtest_children,
        "backtest_threads": backtest_threads,
        "fo_backtest_children": fo_backtest_children,
        "fo_backtest_threads": fo_backtest_threads,
        "so_backtest_children": so_backtest_children,
        "so_backtest_threads": so_backtest_threads,
        "th_backtest_children": th_backtest_children,
        "th_backtest_threads": th_backtest_threads,
        "alpha_date_timezone": alpha_date_timezone,
        "alpha_fetch_limit_multiplier": alpha_fetch_limit_multiplier,
        "daily_alpha_count_usage": daily_alpha_count_usage,
        "daily_alpha_count_status": daily_alpha_count_status,
        "backtest_daily_limit": backtest_daily_limit,
        "check_daily_limit": check_daily_limit,
        "check_threads": check_threads,
        "poll_minutes": poll_minutes,
        "blocked_start_cn": blocked_start_cn,
        "blocked_end_cn": blocked_end_cn,
        "auto_rename": auto_rename,
        "corr_lookback_days": corr_lookback_days,
        "corr_fetch_limit": corr_fetch_limit,
        "corr_workers": corr_workers,
        "submit_lookback_days": submit_lookback_days,
        "submit_sharpe": submit_sharpe,
        "submit_fitness": submit_fitness,
        "submit_alpha_num": submit_alpha_num,
        "fo_track_lookback_days": fo_track_lookback_days,
        "fo_track_sharpe": fo_track_sharpe,
        "fo_track_fitness": fo_track_fitness,
        "fo_track_alpha_num": fo_track_alpha_num,
        "so_track_lookback_days": so_track_lookback_days,
        "so_track_sharpe": so_track_sharpe,
        "so_track_fitness": so_track_fitness,
        "so_track_alpha_num": so_track_alpha_num,
        "prune_keep_num": prune_keep_num,
        "prune_prefix_min_share": prune_prefix_min_share,
        "track_fallback_keep_num": track_fallback_keep_num,
        "group_ops": group_ops,
        "reconnect_short_sleep_seconds": reconnect_short_sleep_seconds,
        "reconnect_long_sleep_seconds": reconnect_long_sleep_seconds,
        "need_confirm_on_modify": need_confirm_on_modify
    }
    
    # 修改管理员密码（加盐哈希）
    if admin_password and admin_password.strip():
        updates["admin_password"] = hash_password(admin_password.strip())
        
    # 修改 WQ 用户名
    if wq_username is not None:
        updates["wq_username"] = wq_username.strip()
        
    # 修改 WQ 密码（非空时覆盖）
    if wq_password and wq_password.strip():
        updates["wq_password"] = wq_password.strip()

    update_settings(updates)
    
    settings = get_settings()
    cached_scopes = get_cached_scopes()
    day1_scopes = get_all_day1_scopes()
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse({"status": "ok", "message": "配置已成功保存。"})
    return templates.TemplateResponse(
        request, 
        "settings.html", 
        {
            "settings": settings, 
            "success": "配置已成功保存。", 
            "cached_scopes": cached_scopes,
            "day1_scopes": day1_scopes,
            "region_names": REGION_DISPLAY_NAMES
        }
    )
 
 
@app.post("/api/settings/update")
async def api_update_settings(request: Request, admin: str = Depends(get_current_admin)):
    form_data = await request.form()
    updates = {}
    for key, value in form_data.items():
        if key == "admin_password":
            if value.strip():
                updates[key] = hash_password(value.strip())
        elif key == "wq_password":
            if value.strip():
                updates[key] = value.strip()
        else:
            updates[key] = value
            
    if updates:
        update_settings(updates)
        
    referer = request.headers.get("referer", "/settings")
    if "?" in referer:
        if "success=1" not in referer:
            redirect_url = referer + "&success=1"
        else:
            redirect_url = referer
    else:
        redirect_url = referer + "?success=1"
        
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/catalog", response_class=HTMLResponse)
def get_catalog(
    request: Request,
    region: str = None,
    universe: str = None,
    delay: int = None,
    admin: str = Depends(get_current_admin)
):
    default_region = get_setting("region", "USA")
    default_universe = get_setting("universe", "TOP3000")
    default_delay = int(get_setting("delay", "1"))
    
    region = region or default_region
    universe = universe or default_universe
    delay = delay if delay is not None else default_delay
    
    datasets = load_datasets_from_cache(region, universe, delay)
    expired, refresh_str = check_cache_expired(region, universe, delay)
    cached_scopes = get_cached_scopes()
    day1_scopes = get_all_day1_scopes()
    settings = get_settings()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    
    return templates.TemplateResponse(
        request,
        "catalog.html",
        {
            "datasets": datasets,
            "cache_expired": expired,
            "cache_last_refresh": refresh_str,
            "region": region,
            "universe": universe,
            "delay": delay,
            "default_region": default_region,
            "default_universe": default_universe,
            "default_delay": default_delay,
            "cached_scopes": cached_scopes,
            "day1_scopes": day1_scopes,
            "region_names": REGION_DISPLAY_NAMES,
            "settings": settings,
            "success": success_msg
        }
    )


@app.get("/backtest", response_class=HTMLResponse)
def get_backtest(request: Request, admin: str = Depends(get_current_admin)):
    # 查询最近运行的回测 Job
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'backtest' ORDER BY id DESC LIMIT 5").fetchall()
    settings = get_settings()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    return templates.TemplateResponse(request, "backtest.html", {"jobs": jobs, "settings": settings, "success": success_msg})


@app.get("/correlation", response_class=HTMLResponse)
def get_correlation(
    request: Request,
    page: int = 1,
    date_filter: str = "",
    admin: str = Depends(get_current_admin)
):
    page_size = 12
    offset = (page - 1) * page_size
    
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'correlation' ORDER BY id DESC LIMIT 5").fetchall()
        # 加载待改名候选 (PPA/RA/ATOM)
        where_clause = "alpha_type IN ('PPA', 'RA', 'ATOM')"
        params = []
        if date_filter:
            local_tz = datetime.now().astimezone().tzinfo
            now_local = datetime.now(local_tz)
            today_start_local = datetime.combine(now_local.date(), time.min).replace(tzinfo=local_tz)
            
            if date_filter == "today":
                start_utc = today_start_local.astimezone(timezone.utc)
                where_clause += " AND created_at >= ?"
                params.append(start_utc.isoformat())
            elif date_filter == "yesterday":
                start_utc = (today_start_local - timedelta(days=1)).astimezone(timezone.utc)
                end_utc = today_start_local.astimezone(timezone.utc) - timedelta(seconds=1)
                where_clause += " AND created_at >= ? AND created_at <= ?"
                params.extend([start_utc.isoformat(), end_utc.isoformat()])
            elif date_filter == "3days":
                start_utc = (today_start_local - timedelta(days=2)).astimezone(timezone.utc)
                where_clause += " AND created_at >= ?"
                params.append(start_utc.isoformat())
            elif date_filter == "7days":
                start_utc = (today_start_local - timedelta(days=6)).astimezone(timezone.utc)
                where_clause += " AND created_at >= ?"
                params.append(start_utc.isoformat())
                
        alphas_all = conn.execute(
            f"""
            SELECT * FROM alpha_records 
            WHERE {where_clause} 
            ORDER BY created_at DESC
            """,
            params
        ).fetchall()
        
        total = len(alphas_all)
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        alphas = alphas_all[offset:offset+page_size]
        
    settings = get_settings()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    return templates.TemplateResponse(
        request,
        "correlation.html",
        {
            "jobs": jobs,
            "alphas": alphas,
            "settings": settings,
            "success": success_msg,
            "page": page,
            "total_pages": total_pages,
            "date_filter": date_filter,
            "total": total
        }
    )


@app.get("/check", response_class=HTMLResponse)
def get_check(
    request: Request,
    page: int = 1,
    type_filter: str = "",
    level_filter: str = "",
    date_filter: str = "",
    admin: str = Depends(get_current_admin)
):
    page_size = 11
    offset = (page - 1) * page_size
    
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'check_submission' ORDER BY id DESC LIMIT 5").fetchall()
        
        where_clause = "1=1"
        params = []
        if type_filter:
            if type_filter == "PASS":
                where_clause += " AND c.result = 'PASS'"
            else:
                where_clause += " AND a.alpha_type = ?"
                params.append(type_filter)
                
        if date_filter:
            local_tz = datetime.now().astimezone().tzinfo
            now_local = datetime.now(local_tz)
            today_start_local = datetime.combine(now_local.date(), time.min).replace(tzinfo=local_tz)
            
            if date_filter == "today":
                start_utc = today_start_local.astimezone(timezone.utc)
                where_clause += " AND c.created_at >= ?"
                params.append(start_utc.isoformat())
            elif date_filter == "yesterday":
                start_utc = (today_start_local - timedelta(days=1)).astimezone(timezone.utc)
                end_utc = today_start_local.astimezone(timezone.utc) - timedelta(seconds=1)
                where_clause += " AND c.created_at >= ? AND c.created_at <= ?"
                params.extend([start_utc.isoformat(), end_utc.isoformat()])
            elif date_filter == "3days":
                start_utc = (today_start_local - timedelta(days=2)).astimezone(timezone.utc)
                where_clause += " AND c.created_at >= ?"
                params.append(start_utc.isoformat())
            elif date_filter == "7days":
                start_utc = (today_start_local - timedelta(days=6)).astimezone(timezone.utc)
                where_clause += " AND c.created_at >= ?"
                params.append(start_utc.isoformat())

        db_results = conn.execute(
            f"""
            SELECT
                c.id, c.alpha_id, c.result, c.prod_corr, c.source, c.message, c.created_at,
                c.payload AS check_payload,
                a.sharpe, a.fitness, a.alpha_type, a.margin, a.returns, a.drawdown,
                a.payload AS alpha_payload
            FROM check_results c 
            LEFT JOIN alpha_records a ON c.alpha_id = a.alpha_id 
            WHERE {where_clause}
            ORDER BY c.created_at DESC 
            """,
            params
        ).fetchall()
        
        all_results = []
        for r in db_results:
            row_dict = dict(r)
            row_dict["payload"] = row_dict.get("alpha_payload")
            rating = build_alpha_rating(row_dict, {"result": row_dict.get("result"), "payload": row_dict.get("check_payload")})
            row_dict.update(rating)

            if level_filter and row_dict["submission_class"] != level_filter:
                continue
            all_results.append(row_dict)
            
        total = len(all_results)
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        results = all_results[offset:offset+page_size]
        
    settings = get_settings()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    
    return templates.TemplateResponse(
        request, 
        "check.html", 
        {
            "jobs": jobs, 
            "results": results,
            "settings": settings,
            "success": success_msg,
            "page": page,
            "total_pages": total_pages,
            "type_filter": type_filter,
            "level_filter": level_filter,
            "date_filter": date_filter,
            "total": total
        }
    )


@app.get("/alphas", response_class=HTMLResponse)
def get_alphas(
    request: Request,
    page: int = 1,
    type_filter: str = "",
    level_filter: str = "",
    date_filter: str = "",
    admin: str = Depends(get_current_admin)
):
    page_size = 12
    where = "1=1"
    params = []
    if type_filter:
        where += " AND a.alpha_type = ?"
        params.append(type_filter)
        
    if date_filter:
        local_tz = datetime.now().astimezone().tzinfo
        now_local = datetime.now(local_tz)
        today_start_local = datetime.combine(now_local.date(), time.min).replace(tzinfo=local_tz)
        
        if date_filter == "today":
            start_utc = today_start_local.astimezone(timezone.utc)
            where += " AND a.created_at >= ?"
            params.append(start_utc.isoformat())
        elif date_filter == "yesterday":
            start_utc = (today_start_local - timedelta(days=1)).astimezone(timezone.utc)
            end_utc = today_start_local.astimezone(timezone.utc) - timedelta(seconds=1)
            where += " AND a.created_at >= ? AND a.created_at <= ?"
            params.extend([start_utc.isoformat(), end_utc.isoformat()])
        elif date_filter == "3days":
            start_utc = (today_start_local - timedelta(days=2)).astimezone(timezone.utc)
            where += " AND a.created_at >= ?"
            params.append(start_utc.isoformat())
        elif date_filter == "7days":
            start_utc = (today_start_local - timedelta(days=6)).astimezone(timezone.utc)
            where += " AND a.created_at >= ?"
            params.append(start_utc.isoformat())

    where_sql = f" WHERE {where}" if where else ""
    with connect() as conn:
        rows = conn.execute(
            f"""
            SELECT
                a.*,
                c.result AS latest_check_result,
                c.payload AS latest_check_payload
            FROM alpha_records a
            LEFT JOIN (
                SELECT cr.*
                FROM check_results cr
                INNER JOIN (
                    SELECT alpha_id, MAX(id) AS max_id
                    FROM check_results
                    GROUP BY alpha_id
                ) latest ON latest.max_id = cr.id
            ) c ON c.alpha_id = a.alpha_id
            {where_sql}
            ORDER BY a.created_at DESC
            """,
            tuple(params)
        ).fetchall()
        
    alphas_all = []
    for r in rows:
        row_dict = dict(r)
        rating = build_alpha_rating(
            row_dict,
            {"result": row_dict.get("latest_check_result"), "payload": row_dict.get("latest_check_payload")},
        )
        row_dict.update(rating)

        if level_filter and row_dict["submission_class"] != level_filter:
            continue
        alphas_all.append(row_dict)
        
    total = len(alphas_all)
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    offset = (page - 1) * page_size
    alphas = alphas_all[offset:offset+page_size]
        
    return templates.TemplateResponse(
        request,
        "alphas.html",
        {
            "alphas": alphas,
            "page": page,
            "total_pages": total_pages,
            "type_filter": type_filter,
            "level_filter": level_filter,
            "date_filter": date_filter,
            "total": total
        }
    )


@app.get("/alphas/{alpha_id}", response_class=HTMLResponse)
def get_alpha_detail_page(request: Request, alpha_id: str, admin: str = Depends(get_current_admin)):
    import pandas as pd
    
    with connect() as conn:
        alpha = conn.execute("SELECT * FROM alpha_records WHERE alpha_id = ?", (alpha_id,)).fetchone()
        check_history = conn.execute("SELECT * FROM check_results WHERE alpha_id = ? ORDER BY created_at DESC", (alpha_id,)).fetchall()
        latest_check = check_history[0] if check_history else None
        
    payload_data = {}
    if alpha and alpha["payload"]:
        try:
            payload_data = json.loads(alpha["payload"]) if isinstance(alpha["payload"], str) else alpha["payload"]
        except Exception:
            pass
            
    # Check if we lack crucial info
    should_fetch_online = False
    if not alpha:
        should_fetch_online = True
    else:
        if not alpha["region"] or not alpha["universe"]:
            should_fetch_online = True
            
    if should_fetch_online:
        settings = get_settings()
        username = settings.get("wq_username")
        password = settings.get("wq_password")
        if username and password:
            try:
                from .services.wq_client import login_with_credentials
                from consultant_core.machine_lib import get_alpha_detail, get_alpha_recordsets
                logger.info(f"Fetching alpha {alpha_id} details online...")
                s = login_with_credentials(username.strip(), password.strip())
                detail = get_alpha_detail(alpha_id, session=s)
                if detail:
                    recordsets_results = []
                    try:
                        recordsets_list = get_alpha_recordsets(alpha_id, session=s)
                        recordsets_results = recordsets_list.get("results", [])
                    except Exception as e:
                        logger.error(f"Failed to fetch recordsets listing for alpha {alpha_id}: {e}")
                        
                    detail["recordsets_list"] = recordsets_results
                    
                    is_metrics = detail.get("is", {})
                    settings_dict = detail.get("settings", {})
                    
                    upsert_alpha({
                        "alpha_id": alpha_id,
                        "alpha_type": "",
                        "name": detail.get("name") or "",
                        "region": settings_dict.get("region") or "",
                        "universe": settings_dict.get("universe") or "",
                        "sharpe": is_metrics.get("sharpe"),
                        "fitness": is_metrics.get("fitness"),
                        "margin": is_metrics.get("margin"),
                        "returns": is_metrics.get("returns"),
                        "drawdown": is_metrics.get("drawdown"),
                        "status": detail.get("status") or "",
                        "payload": detail
                    })
                    
                    with connect() as conn:
                        alpha = conn.execute("SELECT * FROM alpha_records WHERE alpha_id = ?", (alpha_id,)).fetchone()
                        payload_data = detail
                s.close()
            except Exception as e:
                logger.error(f"Failed to fetch alpha {alpha_id} detail online: {e}")
                
    if not alpha:
        raise HTTPException(status_code=404, detail=f"Alpha {alpha_id} not found in database and could not be fetched from WorldQuant Brain.")
        
    alpha_dict = dict(alpha)
    payload = payload_data
    
    # Try parsing expression and decay
    raw_payload = payload
    if "raw_payload" in payload:
        raw_payload = payload["raw_payload"] or {}
        
    expression = raw_payload.get("expression") or raw_payload.get("regular", {}).get("code") if isinstance(raw_payload.get("regular"), dict) else raw_payload.get("regular")
    decay = raw_payload.get("decay") or raw_payload.get("settings", {}).get("decay")
    neutralization = raw_payload.get("neutralization") or raw_payload.get("settings", {}).get("neutralization")
    
    # Format fixed rating badges from one shared source.
    rating = build_alpha_rating(alpha_dict, dict(latest_check) if latest_check else None)
    alpha_dict.update(rating)
    
    # Categorize failed, warning, and passed checks
    latest_check_payload = latest_check["payload"] if latest_check and "payload" in latest_check.keys() else None
    checks_payload = select_checks_payload(payload, latest_check_payload)
    checks = checks_payload.get("is", {}).get("checks", []) if isinstance(checks_payload, dict) else []
    failed_checks = []
    warning_checks = []
    passed_checks = []
    
    def get_check_message(ch: dict) -> str:
        for key in ["message", "description", "display", "name"]:
            val = ch.get(key)
            if val:
                return str(val)
        parts = []
        for key in ["value", "limit", "cutoff", "result"]:
            if key in ch:
                parts.append(f"{key}={ch.get(key)}")
        return ", ".join(parts)
        
    if isinstance(checks, list):
        for check in checks:
            result = str(check.get("result") or check.get("status") or "").upper()
            name = str(check.get("name") or check.get("check") or "Unknown Check")
            ch_dict = {
                "name": name,
                "result": result or "ATTENTION",
                "message": get_check_message(check)
            }
            if result in {"FAIL", "FAILED", "ERROR"}:
                failed_checks.append(ch_dict)
            elif result in {"WARNING", "WARN"}:
                warning_checks.append(ch_dict)
            else:
                passed_checks.append(ch_dict)
                
    # Extracted stats and charts
    recordsets_data = payload.get("recordsets_data", {}) if isinstance(payload, dict) else {}
    recordsets_list = payload.get("recordsets_list", []) if isinstance(payload, dict) else []
    
    charts_svg = {}
    yearly_stats_cols = []
    yearly_stats_rows = []
    
    if recordsets_data:
        try:
            from consultant_core.alpha_report import render_line_chart
            series_frames = {}
            for name, records in recordsets_data.items():
                if records:
                    df = pd.DataFrame(records)
                    if "date" in df.columns:
                        df["date"] = pd.to_datetime(df["date"], errors="coerce")
                    series_frames[name] = df
            
            chart_specs = [
                ("pnl", ["pnl", "risk-neutralized-pnl", "investability-constrained-pnl"]),
                ("daily-pnl", ["pnl"]),
                ("sharpe", ["sharpe"]),
                ("turnover", ["turnover"]),
            ]
            for name, preferred_cols in chart_specs:
                df = series_frames.get(name)
                if df is not None and not df.empty:
                    y_cols = [col for col in preferred_cols if col in df.columns]
                    charts_svg[name] = render_line_chart(df, title=name, y_cols=y_cols)
                    
            if "yearly-stats" in recordsets_data:
                ys_records = recordsets_data["yearly-stats"]
                if ys_records:
                    df_ys = pd.DataFrame(ys_records)
                    columns = [col for col in ["year", "sharpe", "turnover", "fitness", "returns", "drawdown", "margin", "longCount", "shortCount"] if col in df_ys.columns]
                    yearly_stats_cols = columns
                    yearly_stats_rows = df_ys[columns].to_dict(orient="records")
        except Exception as e:
            logger.error(f"Failed to generate custom elements for alpha page {alpha_id}: {e}")
            
    from consultant_core.alpha_report import METRIC_FORMATS, format_value
    
    def render_metric(val: Any, key: str) -> str:
        style = METRIC_FORMATS.get(key, "auto")
        return format_value(val, style)
        
    return templates.TemplateResponse(
        request,
        "alpha_detail.html",
        {
            "alpha": alpha_dict,
            "expression": expression or "N/A",
            "decay": decay if decay is not None else "N/A",
            "neutralization": neutralization or "N/A",
            "check_history": [dict(h) for h in check_history],
            "raw_payload_str": json.dumps(payload, indent=2, ensure_ascii=False),
            "failed_checks": failed_checks,
            "warning_checks": warning_checks,
            "passed_checks": passed_checks,
            "recordsets_list": recordsets_list,
            "charts_svg": charts_svg,
            "yearly_stats_cols": yearly_stats_cols,
            "yearly_stats_rows": yearly_stats_rows,
            "render_metric": render_metric,
            "has_recordsets_loaded": bool(recordsets_data)
        }
    )


@app.post("/api/alphas/{alpha_id}/fetch_recordsets")
def fetch_alpha_recordsets_endpoint(alpha_id: str, admin: str = Depends(get_current_admin)):
    import pandas as pd
    import time
    
    with connect() as conn:
        alpha = conn.execute("SELECT * FROM alpha_records WHERE alpha_id = ?", (alpha_id,)).fetchone()
    if not alpha:
        raise HTTPException(status_code=404, detail="Alpha not found in database.")
        
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="WorldQuant username and password are not set in settings.")
        
    try:
        from .services.wq_client import login_with_credentials
        from consultant_core.machine_lib import get_alpha_detail, get_alpha_recordsets, get_alpha_recordset
        
        logger.info(f"Asynchronously fetching recordsets and updating metadata for alpha {alpha_id} online...")
        s = login_with_credentials(username.strip(), password.strip())
        
        # 1. Fetch latest metadata detail from WorldQuant Brain
        detail = get_alpha_detail(alpha_id, session=s)
        if not detail:
            detail = {}
            if alpha["payload"]:
                try:
                    detail = json.loads(alpha["payload"]) if isinstance(alpha["payload"], str) else alpha["payload"]
                except Exception:
                    pass
        else:
            # Merge with existing payload to preserve any local renames or extra fields
            existing_payload = {}
            if alpha["payload"]:
                try:
                    existing_payload = json.loads(alpha["payload"]) if isinstance(alpha["payload"], str) else alpha["payload"]
                except Exception:
                    pass
            for k, v in existing_payload.items():
                if k not in detail:
                    detail[k] = v
                    
        # 2. Fetch available recordsets list
        recordsets_list = get_alpha_recordsets(alpha_id, session=s)
        recordsets_results = recordsets_list.get("results", [])
        available_recordsets = {item.get("name") for item in recordsets_results if item.get("name")}
        
        # 3. Fetch detailed recordsets data
        recordsets_data = {}
        DESIRED_RECORDSETS = ["pnl", "daily-pnl", "sharpe", "turnover", "yearly-stats"]
        for name in DESIRED_RECORDSETS:
            if name in available_recordsets:
                try:
                    df = get_alpha_recordset(alpha_id, name, session=s)
                    if not df.empty:
                        records = []
                        for _, row in df.iterrows():
                            row_dict = dict(row)
                            for k, v in row_dict.items():
                                if hasattr(v, "isoformat"):
                                    row_dict[k] = v.isoformat()
                                elif pd.isna(v):
                                    row_dict[k] = None
                            records.append(row_dict)
                        recordsets_data[name] = records
                except Exception as e:
                    logger.error(f"Failed to fetch recordset {name} for alpha {alpha_id}: {e}")
                time.sleep(0.5)
                
        detail["recordsets_data"] = recordsets_data
        detail["recordsets_list"] = recordsets_results
        
        is_metrics = detail.get("is", {})
        settings_dict = detail.get("settings", {})
        
        # 4. Save updated metadata and recordsets to DB
        upsert_alpha({
            "alpha_id": alpha_id,
            "alpha_type": alpha["alpha_type"],
            "name": detail.get("name") or alpha["name"] or "",
            "region": settings_dict.get("region") or alpha["region"] or "",
            "universe": settings_dict.get("universe") or alpha["universe"] or "",
            "sharpe": is_metrics.get("sharpe") if is_metrics.get("sharpe") is not None else alpha["sharpe"],
            "fitness": is_metrics.get("fitness") if is_metrics.get("fitness") is not None else alpha["fitness"],
            "margin": is_metrics.get("margin") if is_metrics.get("margin") is not None else alpha["margin"],
            "returns": is_metrics.get("returns") if is_metrics.get("returns") is not None else alpha["returns"],
            "drawdown": is_metrics.get("drawdown") if is_metrics.get("drawdown") is not None else alpha["drawdown"],
            "status": detail.get("status") or alpha["status"] or "",
            "payload": detail
        })
        s.close()
        return {"status": "ok", "message": "Recordsets and metadata updated successfully."}
    except Exception as e:
        logger.error(f"Failed to fetch recordsets for {alpha_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs", response_class=HTMLResponse)
def get_logs(request: Request, admin: str = Depends(get_current_admin)):
    # 读取系统错误
    with connect() as conn:
        errors = conn.execute("SELECT * FROM errors ORDER BY id DESC LIMIT 20").fetchall()
    return templates.TemplateResponse(request, "logs.html", {"errors": errors})


# ==========================================
# 后台任务 API 控制路由
# ==========================================

@app.post("/api/jobs/catalog_refresh")
def post_catalog_refresh(
    region: str = Form(None),
    universe: str = Form(None),
    delay: int = Form(None),
    admin: str = Depends(get_current_admin)
):
    params = {}
    if region:
        params["region"] = region
    if universe:
        params["universe"] = universe
    if delay is not None:
        params["delay"] = delay
        
    title = f"更新数据目录缓存 ({region or '默认'}/{universe or '默认'}/delay={delay or '默认'})"
    job_id = create_job("catalog_refresh", title, params)
    JobRunner().start_job(job_id, "catalog_refresh", params)
    return {"status": "ok", "job_id": job_id}


@app.post("/api/jobs/backtest")
def post_backtest_run(
    dataset_ids: str = Form(...),
    run_fo: bool = Form(True),
    run_so: bool = Form(True),
    run_th: bool = Form(True),
    admin: str = Depends(get_current_admin)
):
    ids_list = [i.strip() for i in dataset_ids.split("\n") if i.strip()]
    if not ids_list:
        raise HTTPException(status_code=400, detail="数据集 ID 列表不能为空。")
        
    params = {
        "dataset_ids": ids_list,
        "run_fo": run_fo,
        "run_so": run_so,
        "run_th": run_th
    }
    
    job_id = create_job("backtest", f"回测三阶段任务 (共 {len(ids_list)} 个数据集)", params)
    JobRunner().start_job(job_id, "backtest", params)
    return RedirectResponse(url="/backtest", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/api/jobs/correlation")
def post_correlation_run(auto_rename: str = Form("0"), admin: str = Depends(get_current_admin)):
    params = {"auto_rename": auto_rename == "1"}
    job_id = create_job("correlation", "相关性检测及改名评定", params)
    JobRunner().start_job(job_id, "correlation", params)
    return RedirectResponse(url="/correlation", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/api/jobs/check")
def post_check_run(manual_ids: str = Form(""), admin: str = Depends(get_current_admin)):
    ids_list = [i.strip() for i in manual_ids.split("\n") if i.strip()]
    params = {"manual_ids": ids_list}
    job_id = create_job("check_submission", f"三线程 check_submission 检查 (手动追加 {len(ids_list)} 个)", params)
    JobRunner().start_job(job_id, "check_submission", params)
    return RedirectResponse(url="/check", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/api/jobs/optimization")
def post_optimization_run(
    action: str = Form("run"),
    source_mode: str = Form("recent"),
    recent_days: int = Form(14),
    candidate_limit: int = Form(20),
    start_date: str = Form(""),
    end_date: str = Form(""),
    alpha_ids: str = Form(""),
    children_per_request: int = Form(1),
    schedule_enabled: str = Form("0"),
    schedule_hour: int = Form(1),
    admin: str = Depends(get_current_admin),
):
    from .services.optimization_run_service import parse_alpha_ids
    from .services.job_params import normalize_optimization_params

    schedule_enabled_value = "1" if schedule_enabled == "1" else "0"
    update_settings(
        {
            "optimization_source_mode": source_mode,
            "optimization_recent_days": recent_days,
            "optimization_candidate_limit": candidate_limit,
            "optimization_children_per_request": children_per_request,
            "optimization_schedule_enabled": schedule_enabled_value,
            "optimization_schedule_hour": schedule_hour,
        }
    )

    params = normalize_optimization_params({
        "source_mode": source_mode,
        "recent_days": recent_days,
        "candidate_limit": candidate_limit,
        "start_date": start_date,
        "end_date": end_date,
        "alpha_ids": "\n".join(parse_alpha_ids(alpha_ids)),
        "children_per_request": children_per_request,
    })
    if action == "save_schedule":
        return RedirectResponse(url="/optimization?success=optimization_schedule_saved", status_code=status.HTTP_303_SEE_OTHER)

    source_label = {
        "manual": f"手动 {len(parse_alpha_ids(alpha_ids))} 个",
        "range": f"{start_date or '起始'} 至 {end_date or '现在'}",
        "recent": f"最近 {recent_days} 天",
    }.get(source_mode, source_mode)
    job_id = create_job("optimization_run", f"Alpha 优化运行 ({source_label}，最多 {candidate_limit} 个)", params)
    JobRunner().start_job(job_id, "optimization_run", params)
    return RedirectResponse(url="/optimization?success=optimization_job_started", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/api/jobs/{job_id}/pause")
def post_job_pause(job_id: int, admin: str = Depends(get_current_admin)):
    JobRunner().pause_job(job_id)
    return {"status": "ok"}


@app.post("/api/jobs/{job_id}/resume")
def post_job_resume(job_id: int, admin: str = Depends(get_current_admin)):
    # 获取任务参数重新启动
    with connect() as conn:
        row = conn.execute("SELECT kind, params FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        
        import json
        params = json.loads(row["params"])
        kind = row["kind"]
        
    JobRunner().start_job(job_id, kind, params)
    return {"status": "ok"}


@app.delete("/api/jobs/{job_id}")
@app.post("/api/jobs/{job_id}/delete")
def api_delete_job(job_id: int, admin: str = Depends(get_current_admin)):
    delete_job(job_id)
    return {"status": "ok", "message": f"任务 #{job_id} 已成功删除"}


@app.post("/api/jobs/{job_id}/modify")
def api_modify_job(job_id: int, params_json: str = Form(...), admin: str = Depends(get_current_admin)):
    import json
    try:
        new_params = json.loads(params_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"解析 JSON 参数失败: {e}")
        
    with connect() as conn:
        row = conn.execute("SELECT kind, title FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        
        kind = row["kind"]
        title = row["title"]
        
        new_title = title
        if kind == "catalog_refresh":
            r = new_params.get("region") or "默认"
            u = new_params.get("universe") or "默认"
            d = new_params.get("delay") or "默认"
            new_title = f"数据目录刷新 ({r}/{u}/delay={d})"
            
        conn.execute(
            "UPDATE jobs SET params = ?, title = ?, updated_at = ? WHERE id = ?",
            (json.dumps(new_params, ensure_ascii=False), new_title, utc_now(), job_id)
        )
    return {"status": "ok", "message": f"任务 #{job_id} 参数已成功修改"}


@app.post("/api/alphas/{alpha_id}/rename")
def post_alpha_rename(alpha_id: str, target_name: str = Form(...), admin: str = Depends(get_current_admin)):
    """用户确认对 Alpha 进行远程改名"""
    from .services.correlation_service import rename_alpha_remote
    try:
        rename_alpha_remote(alpha_id, target_name)
        return RedirectResponse(url="/correlation", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"远程改名失败: {e}")


@app.post("/api/import_credentials")
def post_import_credentials(admin: str = Depends(get_current_admin)):
    """触发凭据导入"""
    auto_import_credentials()
    return {"status": "ok"}


@app.post("/api/settings/test_credentials")
def post_test_credentials(
    wq_username: str = Form(...),
    wq_password: str = Form(...),
    admin: str = Depends(get_current_admin)
):
    """测试输入的 WorldQuant 凭据是否能成功登录"""
    from .services.wq_client import login_with_credentials
    try:
        session = login_with_credentials(wq_username.strip(), wq_password.strip())
        session.close()
        return {"status": "ok", "message": "测试登录成功，凭据正确！"}
    except Exception as e:
        return {"status": "error", "message": f"{str(e)}"}


# ==========================================
# 数据查询与实时日志 Tail API
# ==========================================

@app.get("/api/network_status")
def get_network_status(admin: str = Depends(get_current_admin)):
    from .services.network_monitor import NetworkMonitor
    monitor = NetworkMonitor()
    return {
        "connected": monitor.is_connected,
        "message": "网络连接正常" if monitor.is_connected else "网络连接已断开 (10分钟重连中...)"
    }


@app.get("/api/jobs")
def get_jobs_json(admin: str = Depends(get_current_admin)):
    jobs = list_jobs(limit=10)
    return [
        {
            "id": j["id"],
            "kind": j["kind"],
            "status": j["status"],
            "title": j["title"],
            "progress_current": j["progress_current"],
            "progress_total": j["progress_total"],
            "message": j["message"],
            "params": j["params"]
        } for j in jobs
    ]



@app.get("/api/jobs/{job_id}/events")
def get_job_events_json(job_id: int, admin: str = Depends(get_current_admin)):
    events = list_job_events(job_id, limit=50)
    return [{"id": e["id"], "level": e["level"], "message": e["message"], "payload": e["payload"], "created_at": e["created_at"]} for e in events]


@app.get("/api/jobs/{job_id}/log_tail")
def get_job_log_tail_json(job_id: int, max_lines: int = 100, admin: str = Depends(get_current_admin)):
    from .storage import read_log_tail
    path = LOG_DIR / f"job_{job_id}.log"
    lines = read_log_tail(path, max_lines=max_lines)
    return {"lines": lines}


@app.get("/api/gui_log_tail")
def get_gui_log_tail_json(max_lines: int = 100, admin: str = Depends(get_current_admin)):
    from .storage import read_log_tail
    path = LOG_DIR / "gui.log"
    lines = read_log_tail(path, max_lines=max_lines)
    return {"lines": lines}
