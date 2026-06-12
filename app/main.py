from __future__ import annotations

import logging
import math
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
    connect
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

logger = logging.getLogger(__name__)

app = FastAPI(title="WorldQuant Consultant GUI", version="v0.1")

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
    
    counts = {}
    with connect() as conn:
        counts["alpha_records"] = conn.execute("SELECT COUNT(*) FROM alpha_records").fetchone()[0]
        counts["check_results"] = conn.execute("SELECT COUNT(*) FROM check_results").fetchone()[0]
        counts["errors"] = conn.execute("SELECT COUNT(*) FROM errors").fetchone()[0]
        counts["ppa_count"] = conn.execute("SELECT COUNT(*) FROM alpha_records WHERE alpha_type = 'PPA'").fetchone()[0]
        counts["ra_count"] = conn.execute("SELECT COUNT(*) FROM alpha_records WHERE alpha_type = 'RA'").fetchone()[0]
        counts["atom_count"] = conn.execute("SELECT COUNT(*) FROM alpha_records WHERE alpha_type = 'ATOM'").fetchone()[0]

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
    reconnect_long_sleep_seconds: str = Form("3600"),
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
def get_correlation(request: Request, admin: str = Depends(get_current_admin)):
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'correlation' ORDER BY id DESC LIMIT 5").fetchall()
        # 加载待改名候选 (PPA/RA/ATOM)
        alphas = conn.execute(
            """
            SELECT * FROM alpha_records 
            WHERE alpha_type IN ('PPA', 'RA', 'ATOM') 
            ORDER BY created_at DESC
            """
        ).fetchall()
    settings = get_settings()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    return templates.TemplateResponse(request, "correlation.html", {"jobs": jobs, "alphas": alphas, "settings": settings, "success": success_msg})


@app.get("/check", response_class=HTMLResponse)
def get_check(
    request: Request,
    page: int = 1,
    type_filter: str = "",
    level_filter: str = "",
    admin: str = Depends(get_current_admin)
):
    page_size = 50
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
                
        if level_filter:
            if level_filter == "premium":
                where_clause += " AND a.fitness >= 2.5 AND CAST(json_extract(a.payload, '$.is.margin') AS REAL) >= 0.0030"
            elif level_filter == "standard":
                where_clause += " AND a.fitness >= 1.5 AND CAST(json_extract(a.payload, '$.is.margin') AS REAL) >= 0.0010 AND NOT (a.fitness >= 2.5 AND CAST(json_extract(a.payload, '$.is.margin') AS REAL) >= 0.0030)"
            elif level_filter == "marginal":
                where_clause += " AND a.fitness >= 1.0 AND CAST(json_extract(a.payload, '$.is.margin') AS REAL) >= 0.0005 AND NOT (a.fitness >= 1.5 AND CAST(json_extract(a.payload, '$.is.margin') AS REAL) >= 0.0010)"
            elif level_filter == "substandard":
                where_clause += " AND (a.fitness < 1.0 OR CAST(json_extract(a.payload, '$.is.margin') AS REAL) < 0.0005 OR a.fitness IS NULL OR json_extract(a.payload, '$.is.margin') IS NULL)"
            
        total = conn.execute(
            f"""
            SELECT COUNT(*) 
            FROM check_results c
            LEFT JOIN alpha_records a ON c.alpha_id = a.alpha_id
            WHERE {where_clause}
            """,
            params
        ).fetchone()[0]
        
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        
        db_results = conn.execute(
            f"""
            SELECT c.*, a.sharpe, a.fitness, a.alpha_type, a.payload 
            FROM check_results c 
            LEFT JOIN alpha_records a ON c.alpha_id = a.alpha_id 
            WHERE {where_clause}
            ORDER BY c.created_at DESC 
            LIMIT ? OFFSET ?
            """,
            params + [page_size, offset]
        ).fetchall()
        
        results = []
        for r in db_results:
            row_dict = dict(r)
            payload = {}
            if row_dict.get("payload"):
                try:
                    payload = json.loads(row_dict["payload"]) if isinstance(row_dict["payload"], str) else row_dict["payload"]
                except Exception:
                    pass
            is_metrics = payload.get("is", {})
            row_dict["margin"] = is_metrics.get("margin")
            row_dict["returns"] = is_metrics.get("returns")
            row_dict["drawdown"] = is_metrics.get("drawdown")
            
            fit = row_dict["fitness"] if row_dict["fitness"] is not None else 0.0
            margin = row_dict["margin"] if row_dict["margin"] is not None else 0.0
            
            if fit >= 2.5 and margin >= 0.0030:
                row_dict["alpha_level"] = "优质因子"
                row_dict["level_class"] = "premium"
            elif fit >= 1.5 and margin >= 0.0010:
                row_dict["alpha_level"] = "一般因子"
                row_dict["level_class"] = "standard"
            elif fit >= 1.0 and margin >= 0.0005:
                row_dict["alpha_level"] = "边际因子"
                row_dict["level_class"] = "marginal"
            else:
                row_dict["alpha_level"] = "不合格因子"
                row_dict["level_class"] = "substandard"
            results.append(row_dict)
        
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
            "total": total
        }
    )


@app.get("/alphas", response_class=HTMLResponse)
def get_alphas(
    request: Request,
    page: int = 1,
    type_filter: str = "",
    level_filter: str = "",
    admin: str = Depends(get_current_admin)
):
    page_size = 50
    where = "1=1"
    params = []
    if type_filter:
        where += " AND alpha_type = ?"
        params.append(type_filter)
        
    if level_filter:
        if level_filter == "premium":
            where += " AND fitness >= 2.5 AND CAST(json_extract(payload, '$.is.margin') AS REAL) >= 0.0030"
        elif level_filter == "standard":
            where += " AND fitness >= 1.5 AND CAST(json_extract(payload, '$.is.margin') AS REAL) >= 0.0010 AND NOT (fitness >= 2.5 AND CAST(json_extract(payload, '$.is.margin') AS REAL) >= 0.0030)"
        elif level_filter == "marginal":
            where += " AND fitness >= 1.0 AND CAST(json_extract(payload, '$.is.margin') AS REAL) >= 0.0005 AND NOT (fitness >= 1.5 AND CAST(json_extract(payload, '$.is.margin') AS REAL) >= 0.0010)"
        elif level_filter == "substandard":
            where += " AND (fitness < 1.0 OR CAST(json_extract(payload, '$.is.margin') AS REAL) < 0.0005 OR fitness IS NULL OR json_extract(payload, '$.is.margin') IS NULL)"
        
    rows, total = list_rows("alpha_records", page=page, page_size=page_size, where=where, params=params, order_by="created_at DESC")
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    alphas = []
    for r in rows:
        row_dict = dict(r)
        payload = {}
        if row_dict.get("payload"):
            try:
                payload = json.loads(row_dict["payload"]) if isinstance(row_dict["payload"], str) else row_dict["payload"]
            except Exception:
                pass
        is_metrics = payload.get("is", {})
        row_dict["margin"] = is_metrics.get("margin")
        row_dict["returns"] = is_metrics.get("returns")
        row_dict["drawdown"] = is_metrics.get("drawdown")
        
        fit = row_dict["fitness"] if row_dict["fitness"] is not None else 0.0
        margin = row_dict["margin"] if row_dict["margin"] is not None else 0.0
        
        if fit >= 2.5 and margin >= 0.0030:
            row_dict["alpha_level"] = "优质因子"
            row_dict["level_class"] = "premium"
        elif fit >= 1.5 and margin >= 0.0010:
            row_dict["alpha_level"] = "一般因子"
            row_dict["level_class"] = "standard"
        elif fit >= 1.0 and margin >= 0.0005:
            row_dict["alpha_level"] = "边际因子"
            row_dict["level_class"] = "marginal"
        else:
            row_dict["alpha_level"] = "不合格因子"
            row_dict["level_class"] = "substandard"
        alphas.append(row_dict)
        
    return templates.TemplateResponse(
        request,
        "alphas.html",
        {
            "alphas": alphas,
            "page": page,
            "total_pages": total_pages,
            "type_filter": type_filter,
            "level_filter": level_filter,
            "total": total
        }
    )


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
