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
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(ZoneInfo("Asia/Shanghai")).strftime("%m-%d %H:%M:%S")
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


@app.get("/template-iteration", response_class=HTMLResponse)
def get_template_iteration_page(request: Request, admin: str = Depends(get_current_admin)):
    return templates.TemplateResponse(request, "template_iteration.html", {"success": None})


@app.post("/api/template-iteration/preview")
async def post_template_iteration_preview(request: Request, admin: str = Depends(get_current_admin)):
    from .services.template_iteration import dedupe_candidates, expand_template_candidates, normalize_template_iteration_options

    try:
        payload = await request.json()
    except Exception:
        payload = {}
    options = normalize_template_iteration_options(payload)
    fields = list(payload.get("fields") or [])
    if not fields:
        fields = _load_template_iteration_fields(options.regions, str(payload.get("universe") or "TOP3000"), int(payload.get("delay") or 1))
    return dedupe_candidates(expand_template_candidates(
        payload.get("templates") or "",
        fields,
        options,
    )).to_dict()


@app.post("/api/jobs/template_iteration")
async def post_template_iteration_job(request: Request, admin: str = Depends(get_current_admin)):
    from .services.template_iteration import create_template_iteration_job_params

    try:
        payload = await request.json()
        params = create_template_iteration_job_params(payload.get("candidates") or [], payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid template iteration payload: {exc}") from exc

    params["custom_alphas"] = [item["expression"] for item in params["candidates"]]
    title = f"模板迭代回测 ({len(params['custom_alphas'])} 个候选)"
    job_id = create_job("template_iteration", title, params)
    JobRunner().start_job(job_id, "template_iteration", params)
    return {"status": "ok", "job_id": job_id}


def _load_template_iteration_fields(regions: list[str], universe: str, delay: int) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    for region in regions:
        for dataset in load_datasets_from_cache(region, universe, delay)[:10]:
            dataset_id = str(dataset.get("id") or dataset.get("dataset_id") or "")
            if not dataset_id:
                continue
            for field in load_fields_from_cache(region, universe, delay, dataset_id):
                item = dict(field)
                item.setdefault("region", region)
                item.setdefault("dataset", dataset_id)
                fields.append(item)
    return fields


@app.get("/api/catalog/datasets")
def get_catalog_datasets(region: str = "USA", universe: str = "TOP3000", delay: int = 1, admin: str = Depends(get_current_admin)):
    from .services.catalog_service import load_datasets_from_cache
    datasets = load_datasets_from_cache(region, universe, delay)
    return {"datasets": datasets}


@app.get("/api/catalog/fields")
def get_catalog_fields(region: str = "USA", universe: str = "TOP3000", delay: int = 1, dataset_id: str = "", admin: str = Depends(get_current_admin)):
    from .services.catalog_service import load_fields_from_cache
    fields = load_fields_from_cache(region, universe, delay, dataset_id)
    return {"fields": fields}


@app.get("/api/catalog/search-fields")
def get_catalog_search_fields(region: str = "USA", universe: str = "TOP3000", delay: int = 1, query: str = "", admin: str = Depends(get_current_admin)):
    from .services.catalog_service import load_datasets_from_cache, load_fields_from_cache
    query_lower = query.lower().strip()
    if not query_lower:
        return {"fields": []}
    
    datasets = load_datasets_from_cache(region, universe, delay)
    matched_fields = []
    for ds in datasets[:15]:
        ds_id = ds.get("id") or ds.get("dataset_id") or ""
        if not ds_id:
            continue
        fields = load_fields_from_cache(region, universe, delay, ds_id)
        for field in fields:
            f_id = str(field.get("id") or field.get("field_id") or "").lower()
            f_desc = str(field.get("description") or "").lower()
            if query_lower in f_id or query_lower in f_desc:
                item = dict(field)
                item["dataset"] = ds_id
                item["region"] = region
                matched_fields.append(item)
                if len(matched_fields) >= 100:
                    break
        if len(matched_fields) >= 100:
            break
            
    return {"fields": matched_fields}


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
    limit: int | None = None,
    admin: str = Depends(get_current_admin),
):
    from .services.optimization_planner import build_optimization_plan

    page_size = 11
    success_map = {
        "optimization_job_started": "优化任务已启动，可以在下方查看进度。",
        "optimization_schedule_saved": "优化定时设置已保存。",
    }
    success_msg = success_map.get(request.query_params.get("success") or "")
    settings = get_settings()
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'optimization_run' ORDER BY id DESC LIMIT 5").fetchall()
    query_limit = max(1, min(int(limit or settings.get("optimization_scan_limit") or 200), 5000))
    plan_where = ["a.is_garbage = 0", "a.alpha_type IN ('S', 'A', 'B', 'C')"]
    plan_params: list[Any] = []
    if level_filter:
        plan_where.append("a.alpha_type = ?")
        plan_params.append(level_filter)
    if status_filter == "corr_fail":
        plan_where.append("a.status = 'CORR_FAIL'")
    plan_where_sql = " AND ".join(plan_where)
    with connect() as conn:
        rows = conn.execute(
            f"""
            SELECT
                a.alpha_id,
                a.name,
                a.alpha_type,
                a.sharpe,
                a.fitness,
                a.margin,
                a.prod_corr,
                a.ppa_corr,
                a.status,
                a.payload,
                a.updated_at,
                c.result AS check_result,
                c.message AS check_message,
                c.payload AS check_payload
            FROM alpha_records a
            LEFT JOIN (
                SELECT c1.*
                FROM check_results c1
                INNER JOIN (
                    SELECT alpha_id, MAX(id) AS max_id
                    FROM check_results
                    GROUP BY alpha_id
                ) latest ON latest.max_id = c1.id
            ) c ON c.alpha_id = a.alpha_id
            WHERE {plan_where_sql}
            ORDER BY a.updated_at DESC
            LIMIT ?
            """,
            tuple(plan_params) + (query_limit,),
        ).fetchall()

    plans = []
    for row in rows:
        row_dict = dict(row)
        plan_dict = build_optimization_plan(
            row_dict,
            check_payload=row_dict.get("check_payload"),
            check_message=row_dict.get("check_message") or "",
            check_result=row_dict.get("check_result") or "",
        )
        plan = plan_dict.to_dict()
        plan["prod_corr"] = row_dict.get("prod_corr")
        plan["ppa_corr"] = row_dict.get("ppa_corr")
        plans.append(plan)
    # 彻底过滤掉负夏普/厂字等垃圾/高危因子，不展示在优化页面上
    plans = [plan for plan in plans if plan.get("skip_reason") != "high_risk_garbage_alpha"]
    if status_filter == "optimizable":
        plans = [plan for plan in plans if plan["should_optimize"]]
    elif status_filter == "skipped":
        plans = [plan for plan in plans if not plan["should_optimize"]]
    elif status_filter == "corr_fail":
        plans = [plan for plan in plans if plan["strategy"] == "decorrelate" or any("CORRELATION" in str(chk.get("name")).upper() for chk in plan.get("failed_checks", []))]
    elif status_filter == "other_opt":
        plans = [plan for plan in plans if plan["should_optimize"] and plan["strategy"] != "decorrelate" and not any("CORRELATION" in str(chk.get("name")).upper() for chk in plan.get("failed_checks", []))]

    if strategy_filter:
        plans = [plan for plan in plans if plan["strategy"] == strategy_filter]

    # 优先显示可优化因子，并按照确定性得分从高到低排序
    plans.sort(key=lambda p: (1 if p.get("should_optimize") else 0, p.get("confidence_score") or 0.0), reverse=True)

    class_a_count = sum(1 for plan in plans if plan.get("alpha_class") == "Class A" and plan.get("should_optimize"))
    class_b_count = sum(1 for plan in plans if plan.get("alpha_class") == "Class B" and plan.get("should_optimize"))
    class_c_count = sum(1 for plan in plans if plan.get("alpha_class") == "Class C" and plan.get("should_optimize"))

    # 查询最近被救活/优化成功的因子数据
    with connect() as conn:
        result_rows = conn.execute(
            """
            SELECT
                a.alpha_id,
                a.name,
                a.alpha_type,
                a.sharpe,
                a.fitness,
                a.margin,
                a.prod_corr,
                a.status,
                a.payload,
                a.created_at,
                c.result AS check_result
            FROM alpha_records a
            LEFT JOIN (
                SELECT c1.alpha_id, c1.result
                FROM check_results c1
                INNER JOIN (
                    SELECT alpha_id, MAX(id) AS max_id
                    FROM check_results
                    GROUP BY alpha_id
                ) latest ON latest.max_id = c1.id
            ) c ON c.alpha_id = a.alpha_id
            WHERE a.is_garbage = 0
              AND (a.status IN ('RENAMED', 'CHECKED_PASS', 'SUBMITTED', 'OS') OR a.name LIKE 'S_%')
            ORDER BY a.created_at DESC
            LIMIT 10
            """
        ).fetchall()

    recent_results = []
    for r in result_rows:
        r_dict = dict(r)
        expr = ""
        try:
            payload_data = json.loads(r_dict.get("payload") or "{}")
            expr = payload_data.get("expression") or payload_data.get("regular", {}).get("code") or ""
        except Exception:
            pass
        r_dict["expression"] = expr
        recent_results.append(r_dict)

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
            "class_a_count": class_a_count,
            "class_b_count": class_b_count,
            "class_c_count": class_c_count,
            "recent_results": recent_results,
            "limit": query_limit,
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


def migrate_alpha_types():
    """将老数据库中的 alpha_type (PPA, RA, ATOM) 统一升级为规范的五档评级 S/A/B/C/D"""
    logger.info("Starting database migration to unify alpha grades...")
    try:
        from .services.alpha_rating import build_alpha_rating
        from .storage import connect
        
        with connect() as conn:
            rows = conn.execute("SELECT * FROM alpha_records").fetchall()
            
            # 批量载入所有的最新 check_results，避免循环中重复查询
            latest_checks = {}
            for chk in conn.execute(
                """
                SELECT c1.alpha_id, c1.result 
                FROM check_results c1
                INNER JOIN (
                    SELECT alpha_id, MAX(id) AS max_id
                    FROM check_results
                    GROUP BY alpha_id
                ) latest ON latest.max_id = c1.id
                """
            ).fetchall():
                latest_checks[chk["alpha_id"]] = {"result": chk["result"]}
                
            updated_count = 0
            for r in rows:
                row_dict = dict(r)
                alpha_id = row_dict["alpha_id"]
                current_type = row_dict.get("alpha_type") or ""
                
                # 如果已经是五档分类之一，并且不是空的，就跳过
                if current_type in {"S", "A", "B", "C", "D"}:
                    continue
                    
                latest_check = latest_checks.get(alpha_id)
                rating = build_alpha_rating(row_dict, latest_check)
                grade = rating.get("grade", "C")
                
                conn.execute(
                    "UPDATE alpha_records SET alpha_type = ?, updated_at = datetime('now') WHERE alpha_id = ?",
                    (grade, alpha_id)
                )
                updated_count += 1
                
        logger.info(f"Database rating unification complete. Migrated {updated_count} alpha records.")
    except Exception as e:
        logger.error(f"Failed to migrate alpha rating types: {e}")


@app.on_event("startup")
def on_startup():
    """Web 服务启动时初始化配置与数据克隆"""
    init_db()
    JobRunner().init_runner()
    auto_import_credentials()
    handle_env_password_override()
    ensure_catalog_data()
    
    # 统一规范因子评级归档
    migrate_alpha_types()
    
    # 启动网络监视器服务
    from .services.network_monitor import NetworkMonitor
    NetworkMonitor().start()
    
    # 启动定时任务调度服务
    from .services.scheduler_service import SchedulerService
    SchedulerService().start()
    
    # 启动后台自动巡检核查服务
    from .services.background_inspector import BackgroundInspector
    BackgroundInspector().start()
    
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
        
    try:
        from .services.background_inspector import BackgroundInspector
        BackgroundInspector().stop()
    except Exception as e:
        logger.error(f"Error during shutdown background inspector: {e}")
        
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
    corr_fetch_limit: str = Form("4000"),
    corr_workers: str = Form("5"),
    wq_sync_limit: str = Form("500"),
    submit_lookback_days: str = Form("30"),
    submit_sharpe: str = Form("1.58"),
    submit_fitness: str = Form("1.0"),
    submit_alpha_num: str = Form("200"),
    optimization_scan_limit: str = Form("200"),
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
        "wq_sync_limit": wq_sync_limit,
        "submit_lookback_days": submit_lookback_days,
        "submit_sharpe": submit_sharpe,
        "submit_fitness": submit_fitness,
        "submit_alpha_num": submit_alpha_num,
        "optimization_scan_limit": optimization_scan_limit,
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



@app.get("/backtest", response_class=HTMLResponse)
def get_backtest(request: Request, admin: str = Depends(get_current_admin)):
    # 查询最近运行的回测 Job
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs WHERE kind = 'backtest' ORDER BY id DESC LIMIT 5").fetchall()
    settings = get_settings()
    success_msg = "配置已成功保存。" if request.query_params.get("success") == "1" else None
    return templates.TemplateResponse(
        request,
        "backtest.html",
        {"jobs": jobs, "settings": settings, "success": success_msg, "backtest_regions": _backtest_regions_from_catalog()},
    )


def _backtest_regions_from_catalog() -> list[str]:
    cached = get_cached_scopes()
    regions = [region for region in ("USA", "ASI", "EUR") if region in cached]
    if regions:
        return regions
    selected = str(get_setting("region", "USA") or "USA").upper()
    return [selected] if selected in {"USA", "ASI", "EUR"} else ["USA"]



@app.get("/alphas", response_class=HTMLResponse)
def get_alphas(
    request: Request,
    page: int = 1,
    type_filter: str = "",
    level_filter: str = "",
    date_filter: str = "",
    show_hidden: str = "0",
    admin: str = Depends(get_current_admin)
):
    page_size = 12
    page = max(1, int(page))
    offset = (page - 1) * page_size
    where = "1=1"
    params = []
    if show_hidden != "1":
        where += " AND a.is_garbage = 0"
        
    if type_filter:
        where += " AND a.alpha_type = ?"
        params.append(type_filter)

    if level_filter:
        if level_filter == "premium":
            where += " AND a.alpha_type = 'S' AND a.sharpe >= 1.70 AND a.fitness >= 1.50 AND a.margin >= 0.0015 AND COALESCE(a.prod_corr, 0) <= 0.35"
        elif level_filter == "standard":
            where += " AND a.alpha_type = 'S' AND a.sharpe >= 1.58 AND a.fitness >= 1.20 AND a.margin >= 0.0012 AND COALESCE(a.prod_corr, 0) <= 0.45"
            where += " AND NOT (a.sharpe >= 1.70 AND a.fitness >= 1.50 AND a.margin >= 0.0015 AND COALESCE(a.prod_corr, 0) <= 0.35)"
        elif level_filter == "marginal":
            where += " AND a.alpha_type = 'S'"
            where += " AND NOT (a.sharpe >= 1.58 AND a.fitness >= 1.20 AND a.margin >= 0.0012 AND COALESCE(a.prod_corr, 0) <= 0.45)"
        elif level_filter == "substandard":
            where += " AND a.alpha_type != 'S'"
        
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
        total = conn.execute(
            f"SELECT COUNT(*) AS n FROM alpha_records a {where_sql}",
            tuple(params),
        ).fetchone()["n"]
        rows = conn.execute(
            f"SELECT a.* FROM alpha_records a {where_sql} ORDER BY a.created_at DESC LIMIT ? OFFSET ?",
            tuple(params) + (page_size, offset)
        ).fetchall()
        alpha_ids = [row["alpha_id"] for row in rows]
        latest_checks = {}
        if alpha_ids:
            placeholders = ",".join("?" for _ in alpha_ids)
            check_rows = conn.execute(
                f"""
                SELECT c1.alpha_id, c1.result, c1.payload
                FROM check_results c1
                INNER JOIN (
                    SELECT alpha_id, MAX(id) AS max_id
                    FROM check_results
                    WHERE alpha_id IN ({placeholders})
                    GROUP BY alpha_id
                ) latest ON latest.max_id = c1.id
                """,
                tuple(alpha_ids),
            ).fetchall()
            latest_checks = {row["alpha_id"]: row for row in check_rows}
        
    from .services.optimization_planner import is_high_risk_garbage_alpha
    alphas = []
    for r in rows:
        row_dict = dict(r)
        latest_check = latest_checks.get(row_dict["alpha_id"])
        rating = build_alpha_rating(
            row_dict,
            {"result": latest_check["result"], "payload": latest_check["payload"]} if latest_check else None,
        )
        row_dict.update(rating)

        # 垃圾/高危因子状态已在数据库 is_garbage 字段中维护，此处仅做读取展示即可，不再执行 python 内存过滤以防止破坏分页行数
        is_garbage = (row_dict.get("is_garbage") == 1)
        row_dict["is_garbage"] = is_garbage
        alphas.append(row_dict)
        
    total_pages = math.ceil(total / page_size) if total > 0 else 1
        
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
            "show_hidden": show_hidden,
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


@app.post("/api/alphas/{alpha_id}/remote_validate")
def remote_validate_alpha(
    alpha_id: str,
    check_pnl: bool = False,
    admin: str = Depends(get_current_admin),
):
    """
    远端二次验证 (A / S 级触发)：
    - 拉取 WQ yearly-stats → 厂字 / OS 崩塌检测
    - 可选拉取 PNL → 末端平坦检测
    - 若 grade_adjustment == 'D' → 本地标记 is_garbage + WQ 平台 DELETE
    """
    from .services.alpha_remote_validator import run_remote_validation
    from .services.wq_client import login_with_credentials, retire_wq_alpha

    with connect() as conn:
        alpha = conn.execute(
            "SELECT alpha_id, sharpe, fitness, grade, is_garbage FROM alpha_records WHERE alpha_id = ?",
            (alpha_id,),
        ).fetchone()
    if not alpha:
        raise HTTPException(status_code=404, detail="Alpha not found in database.")

    settings = get_settings()
    username = settings.get("wq_username", "")
    password = settings.get("wq_password", "")
    if not username or not password:
        raise HTTPException(status_code=400, detail="WQ credentials not set in settings.")

    try:
        s = login_with_credentials(username.strip(), password.strip())
        is_sharpe = float(alpha["sharpe"] or 0)
        is_fitness = float(alpha["fitness"] or 0)

        result = run_remote_validation(
            session=s,
            alpha_id=alpha_id,
            is_sharpe=is_sharpe,
            is_fitness=is_fitness,
            check_pnl=check_pnl,
        )

        # 若判定为 D 级垃圾因子 → 本地隐藏 + 平台退休
        if result.get("grade_adjustment") == "D":
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET is_garbage = 1, skip_reason = ? WHERE alpha_id = ?",
                    (
                        "DEAD_ALPHA_RISK|" + "|".join(result.get("issues", [])),
                        alpha_id,
                    ),
                )
            # 尝试远端退休（DELETE simulation）
            try:
                retired = retire_wq_alpha(s, alpha_id)
                result["wq_retired"] = retired
            except Exception as ex:
                logger.warning(f"[RemoteValidate] WQ retire failed for {alpha_id}: {ex}")
                result["wq_retired"] = False
        else:
            # 若通过，更新本地 grade_note 字段（备注远端验证结果）
            note = "remote_verified" if result.get("grade_adjustment") == "keep" else "os_decay_warning"
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET remote_validation_note = ? WHERE alpha_id = ?",
                    (note, alpha_id),
                )

        s.close()
        return {"status": "ok", "alpha_id": alpha_id, **result}

    except Exception as e:
        logger.error(f"[RemoteValidate] Failed for {alpha_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs", response_class=HTMLResponse)
def get_logs(request: Request, admin: str = Depends(get_current_admin)):
    # 读取系统错误
    with connect() as conn:
        errors = conn.execute("SELECT * FROM errors ORDER BY id DESC LIMIT 20").fetchall()
    return templates.TemplateResponse(request, "logs.html", {"errors": errors})


def get_csv_data(file_path: Path) -> list[dict[str, Any]]:
    if not file_path.exists():
        return []
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        df = df.fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to read CSV {file_path}: {e}")
        return []



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
async def post_backtest_run(
    request: Request,
    admin: str = Depends(get_current_admin)
):
    from .services.job_params import normalize_backtest_params

    form_data = await request.form()
    save_only = form_data.get("save_only") == "true" or form_data.get("save_only") == "on"

    settings_keys = [
        "fo_filter_negative_sharpe", "so_filter_negative_sharpe", "fo_corr_enable", "fo_corr_sharpe_th", "fo_max_prod_corr",
        "so_corr_enable", "so_corr_sharpe_th", "so_max_prod_corr",
        "fo_track_lookback_days", "fo_track_sharpe", "fo_track_fitness", "fo_track_alpha_num",
        "th_corr_enable", "th_corr_sharpe_th", "th_max_prod_corr",
        "so_track_lookback_days", "so_track_sharpe", "so_track_fitness", "so_track_alpha_num",
        "prune_keep_num", "prune_prefix_min_share", "track_fallback_keep_num", "group_ops",
        "fo_backtest_children", "fo_backtest_threads",
        "so_backtest_children", "so_backtest_threads",
        "th_backtest_children", "th_backtest_threads",
        "alpha_fetch_limit_multiplier", "alpha_date_timezone",
        "advisor_level", "self_corr_safe", "self_corr_hard", "prod_corr_good", "prod_corr_hard",
        "turnover_warn", "turnover_hard", "operator_count_max", "hide_grade_d_local", "retire_grade_d_remote",
    ]
    updates = {}
    for key in settings_keys:
        val = form_data.get(key)
        if val is not None:
            if val in ("true", "on"):
                updates[key] = "1"
            elif val in ("false", "off"):
                updates[key] = "0"
            else:
                updates[key] = str(val)
        else:
            if "enable" in key or "filter" in key:
                updates[key] = "0"
    if updates:
        update_settings(updates)

    if save_only:
        return RedirectResponse(url="/backtest?success=1", status_code=status.HTTP_303_SEE_OTHER)

    dataset_ids = form_data.get("dataset_ids", "")
    run_fo = form_data.get("run_fo") == "true" or form_data.get("run_fo") == "on"
    run_so = form_data.get("run_so") == "true" or form_data.get("run_so") == "on"
    run_th = form_data.get("run_th") == "true" or form_data.get("run_th") == "on"

    ids_list = [i.strip() for i in dataset_ids.split("\n") if i.strip()]
    if not ids_list:
        raise HTTPException(status_code=400, detail="数据集 ID 列表不能为空。")

    raw_backtest_params = dict(form_data)
    raw_backtest_params.update({
        "dataset_ids": ids_list,
        "regions": _backtest_regions_from_catalog(),
        "run_fo": run_fo,
        "run_so": run_so,
        "run_th": run_th,
    })
    params = normalize_backtest_params(raw_backtest_params)
    if not params["allowed_dataset_ids"]:
        raise HTTPException(status_code=400, detail="当前顾问等级没有可运行的数据集。")
    params["dataset_ids"] = params["allowed_dataset_ids"]

    title_regions = "/".join(params.get("regions") or [])
    job_id = create_job("backtest", f"王哥严格版回测 ({title_regions}，共 {len(params['dataset_ids'])} 个数据集)", params)
    JobRunner().start_job(job_id, "backtest", params)
    return RedirectResponse(url="/backtest", status_code=status.HTTP_303_SEE_OTHER)



@app.post("/api/jobs/submit")
def post_alpha_submit_run(
    request: Request,
    source_mode: str = Form("local_pass"),
    manual_ids: str = Form(""),
    limit: int = Form(200),
    dry_run: str = Form("0"),
    admin: str = Depends(get_current_admin),
):
    from .services.submit_service import parse_alpha_ids

    ids_list = parse_alpha_ids(manual_ids)
    params = {
        "source_mode": source_mode,
        "manual_ids": ids_list,
        "limit": limit,
        "dry_run": dry_run == "1",
        "max_cycles": 1,
    }
    title = f"提交因子 ({source_mode}, 上限 {limit}, 手动 {len(ids_list)} 个)"
    job_id = create_job("alpha_submit", title, params)
    JobRunner().start_job(job_id, "alpha_submit", params)
    
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse({"status": "ok", "job_id": job_id})
    return RedirectResponse(url="/alphas", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/api/jobs/optimization")
def post_optimization_run(
    action: str = Form("run"),
    source_mode: str = Form("recent"),
    recent_days: int = Form(14),
    candidate_limit: int = Form(20),
    level_filter: str = Form("C"),
    start_date: str = Form(""),
    end_date: str = Form(""),
    alpha_ids: str = Form(""),
    children_per_request: int = Form(1),
    backtest_threads: int = Form(10),
    schedule_enabled: str = Form("0"),
    schedule_hour: int = Form(1),
    group_neutralization: list[str] = Form(default=["subindustry"]),
    trade_std_window: int = Form(5),
    trade_std_threshold: float = Form(0.01),
    decay_windows: str = Form("5,10,20"),
    max_variants: int = Form(10),
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
            "optimization_level_filter": level_filter,
            "optimization_children_per_request": children_per_request,
            "optimization_backtest_threads": backtest_threads,
            "optimization_schedule_enabled": schedule_enabled_value,
            "optimization_schedule_hour": schedule_hour,
            "optimization_group_neutralization": ",".join(group_neutralization),
            "optimization_trade_std_window": str(trade_std_window),
            "optimization_trade_std_threshold": str(trade_std_threshold),
            "optimization_decay_windows": decay_windows,
            "optimization_max_variants": str(max_variants),
        }
    )

    params = normalize_optimization_params({
        "source_mode": source_mode,
        "recent_days": recent_days,
        "candidate_limit": candidate_limit,
        "level_filter": level_filter,
        "start_date": start_date,
        "end_date": end_date,
        "alpha_ids": "\n".join(parse_alpha_ids(alpha_ids)),
        "children_per_request": children_per_request,
        "backtest_threads": backtest_threads,
        "group_neutralization": group_neutralization,
        "trade_std_window": trade_std_window,
        "trade_std_threshold": trade_std_threshold,
        "decay_windows": decay_windows,
        "max_variants": max_variants,
    })
    if action == "save_schedule":
        return RedirectResponse(url="/optimization?success=optimization_schedule_saved", status_code=status.HTTP_303_SEE_OTHER)

    source_label = {
        "manual": f"手动 {len(parse_alpha_ids(alpha_ids))} 个",
        "range": f"{start_date or '起始'} 至 {end_date or '现在'}",
        "recent": f"最近 {recent_days} 天",
    }.get(source_mode, source_mode)
    job_id = create_job("optimization_run", f"Alpha 优化运行 ({source_label}，等级 {level_filter}及以上，最多 {candidate_limit} 个)", params)
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
        "message": "网络连接正常" if monitor.is_connected else "网络连接已断开 (5分钟重连中...)"
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


@app.get("/api/jobs/{job_id}/summary")
def get_job_summary_json(job_id: int, admin: str = Depends(get_current_admin)):
    with connect() as conn:
        job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found.")
        rows = conn.execute(
            """
            SELECT alpha_type, status, is_garbage
            FROM alpha_records
            WHERE source = ? OR source LIKE ?
            """,
            (f"job_{job_id}", f"%job_{job_id}%"),
        ).fetchall()

    grade_counts = {grade: 0 for grade in ("S", "A", "B", "C", "D")}
    passed = 0
    hidden = 0
    for row in rows:
        grade = row["alpha_type"] or ""
        if grade in grade_counts:
            grade_counts[grade] += 1
        if grade in {"S", "A", "B"} or row["status"] == "CHECKED_PASS":
            passed += 1
        if grade == "D" or int(row["is_garbage"] or 0):
            hidden += 1

    try:
        started = datetime.fromisoformat(str(job["created_at"]).replace("Z", "+00:00"))
        ended = datetime.fromisoformat(str(job["updated_at"]).replace("Z", "+00:00"))
        duration_seconds = max(0, int((ended - started).total_seconds()))
    except Exception:
        duration_seconds = 0
    minutes = max(duration_seconds / 60, 1 / 60)
    total = len(rows)
    return {
        "job_id": job_id,
        "status": job["status"],
        "total": total,
        "passed": passed,
        "hidden": hidden,
        "grade_counts": grade_counts,
        "duration_seconds": duration_seconds,
        "alphas_per_minute": round(total / minutes, 2),
    }


@app.get("/api/gui_log_tail")
def get_gui_log_tail_json(max_lines: int = 100, admin: str = Depends(get_current_admin)):
    from .storage import read_log_tail
    path = LOG_DIR / "gui.log"
    lines = read_log_tail(path, max_lines=max_lines)
    return {"lines": lines}


@app.post("/api/logs/export")
def export_logs(
    log_type: str = Form(...),
    job_id: str = Form(None),
    start_time: str = Form(None),
    end_time: str = Form(None),
    admin: str = Depends(get_current_admin)
):
    from fastapi.responses import StreamingResponse
    from datetime import datetime
    from .services.log_service import filter_gui_log, get_job_log_path

    if log_type == "job":
        if not job_id:
            raise HTTPException(status_code=400, detail="Job ID is required for job log export.")
        log_file = get_job_log_path(job_id)
        if not log_file.exists():
            raise HTTPException(status_code=404, detail=f"Log file job_{job_id}.log not found.")
        
        filename = f"job_{job_id}_export.log"
        
        def iter_job_log():
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    yield line

        return StreamingResponse(
            iter_job_log(),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    elif log_type == "gui":
        now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"gui_export_{now_str}.log"

        def iter_filtered_gui_log():
            for line in filter_gui_log(start_time=start_time, end_time=end_time):
                yield line

        return StreamingResponse(
            iter_filtered_gui_log(),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid log_type.")


@app.get("/api/jobs/{job_id}/alphas")
def get_job_alphas_json(job_id: int, admin: str = Depends(get_current_admin)):
    """获取指定 Job 产生的所有子 Alpha 记录"""
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT 
                a.alpha_id, a.name, a.region, a.universe, a.sharpe, a.fitness, a.margin, a.returns, a.drawdown,
                a.prod_corr, a.ppa_corr, a.status, a.alpha_type
            FROM alpha_records a
            WHERE a.source = ? OR a.source LIKE ?
            ORDER BY a.created_at DESC
            """,
            (f"job_{job_id}", f"%job_{job_id}%")
        ).fetchall()
    return [dict(r) for r in rows]


@app.get("/api/alphas/{alpha_id}/pnl_chart")
def get_alpha_pnl_chart(alpha_id: str, admin: str = Depends(get_current_admin)):
    """懒加载获取指定因子的 PnL 图表 SVG"""
    import pandas as pd
    
    with connect() as conn:
        row = conn.execute("SELECT payload FROM alpha_records WHERE alpha_id = ?", (alpha_id,)).fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Alpha not found.")
        
    payload = {}
    if row["payload"]:
        try:
            payload = json.loads(row["payload"]) if isinstance(row["payload"], str) else row["payload"]
        except Exception:
            pass
            
    recordsets_data = payload.get("recordsets_data", {}) if isinstance(payload, dict) else {}
    pnl_records = recordsets_data.get("pnl", []) if isinstance(recordsets_data, dict) else []
    
    if not pnl_records:
        settings = get_settings()
        username = settings.get("wq_username")
        password = settings.get("wq_password")
        if not username or not password:
            return {"status": "error", "message": "请先在设置中配置 WQ 账号和密码。"}
            
        try:
            from .services.wq_client import login_with_credentials
            from consultant_core.machine_lib import get_alpha_recordset
            s = login_with_credentials(username.strip(), password.strip())
            df = get_alpha_recordset(alpha_id, "pnl", session=s)
            s.close()
            
            if not df.empty:
                records = []
                for _, r in df.iterrows():
                    row_dict = dict(r)
                    for k, v in row_dict.items():
                        if hasattr(v, "isoformat"):
                            row_dict[k] = v.isoformat()
                        elif pd.isna(v):
                            row_dict[k] = None
                    records.append(row_dict)
                
                # 写入 payload 缓存
                if not isinstance(payload, dict):
                    payload = {}
                if "recordsets_data" not in payload:
                    payload["recordsets_data"] = {}
                payload["recordsets_data"]["pnl"] = records
                
                with connect() as conn:
                    conn.execute(
                        "UPDATE alpha_records SET payload = ?, updated_at = datetime('now') WHERE alpha_id = ?",
                        (json.dumps(payload, ensure_ascii=False), alpha_id)
                    )
                pnl_records = records
        except Exception as e:
            logger.error(f"Failed to fetch pnl chart online: {e}")
            return {"status": "error", "message": f"在线拉取 PnL 失败: {e}"}
            
    if pnl_records:
        try:
            from consultant_core.alpha_report import render_line_chart
            df_pnl = pd.DataFrame(pnl_records)
            if "date" in df_pnl.columns:
                df_pnl["date"] = pd.to_datetime(df_pnl["date"], errors="coerce")
            df_pnl = df_pnl.rename(columns={'date': 'Date', 'pnl': alpha_id})
            chart_svg = render_line_chart(df_pnl, title="PnL 累计收益曲线", y_cols=[alpha_id])
            
            # 格式化一下 SVG 类名以便暗黑模式样式统一
            chart_svg = chart_svg.replace('<svg class="wqb-chart"', '<svg class="wqb-chart" style="width: 100% !important; height: auto !important; max-height: 280px;"')
            if 'class="wqb-chart"' not in chart_svg:
                chart_svg = chart_svg.replace('<svg ', '<svg class="wqb-chart" style="width: 100% !important; height: auto !important; max-height: 280px;" ')
            return {"status": "ok", "svg": chart_svg}
        except Exception as e:
            return {"status": "error", "message": f"图表渲染失败: {e}"}
            
    return {"status": "empty", "message": "该因子暂无可用的 PnL 数据。"}


@app.post("/api/alphas/sync")
def sync_alphas_from_wq(admin: str = Depends(get_current_admin)):
    """从 WQ 平台拉取最近 30 天所有已回测因子记录同步至本地数据库（后台任务化）"""
    from app.storage import create_job
    from app.job_runner import JobRunner
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="请先在设置中配置 WQ 账号和密码。")
        
    try:
        # 创建同步任务，默认回看最近 30 天
        job_id = create_job(
            kind="sync_alphas",
            title="同步云端因子 (最近 30 天)",
            params={"lookback_days": 30}
        )
        
        # 启动任务
        JobRunner().start_job(job_id, "sync_alphas", {"lookback_days": 30})
        
        return {
            "status": "ok", 
            "message": f"云端因子同步任务已成功启动，已加入后台队列。Job ID: #{job_id}",
            "job_id": job_id
        }
        
    except Exception as e:
        logger.error(f"Failed to start sync alphas job: {e}")
        raise HTTPException(status_code=500, detail=f"启动同步任务失败: {e}")


@app.post("/api/alphas/sync_local")
def sync_local_alphas_endpoint(admin: str = Depends(get_current_admin)):
    """计算本地所有非垃圾且已提交因子的自相关性 (后台任务)"""
    from app.storage import create_job
    from app.job_runner import JobRunner
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="请先在设置中配置 WQ 账号和密码。")
        
    try:
        job_id = create_job(
            kind="sync_local_alphas",
            title="同步本地因子 (自相关计算)",
            params={}
        )
        JobRunner().start_job(job_id, "sync_local_alphas", {})
        return {
            "status": "ok",
            "message": f"本地因子自相关同步任务已成功启动，已加入后台队列。Job ID: #{job_id}",
            "job_id": job_id
        }
    except Exception as e:
        logger.error(f"Failed to start sync local alphas job: {e}")
        raise HTTPException(status_code=500, detail=f"启动同步任务失败: {e}")


@app.post("/api/alphas/retire")
def post_retire_alpha(alpha_id: str = Form(...), admin: str = Depends(get_current_admin)):
    from .services.wq_client import login_with_credentials, retire_wq_alpha
    from .services.sync_service import load_credentials
    from .storage import connect
    import requests
    
    logger.info(f"Manual retire request received for {alpha_id}")
    try:
        creds = load_credentials()
        with requests.Session() as s:
            login_with_credentials(s, creds)
            retire_wq_alpha(s, alpha_id)
            
        with connect() as conn:
            conn.execute(
                "UPDATE alpha_records SET is_garbage = 1, alpha_type = 'D', updated_at = datetime('now') WHERE alpha_id = ?",
                (alpha_id,)
            )
        return {"status": "ok", "message": f"Successfully retired and marked {alpha_id} as garbage."}
    except Exception as e:
        logger.error(f"Failed manual retire for {alpha_id}: {e}")
        # Even if WQ retire fails (e.g. 404), we still want to mark it as garbage locally so it is removed from UI
        try:
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET is_garbage = 1, alpha_type = 'D', updated_at = datetime('now') WHERE alpha_id = ?",
                    (alpha_id,)
                )
            return {"status": "ok", "message": f"Failed WQ retire but successfully marked as garbage locally: {e}"}
        except Exception as db_err:
            raise HTTPException(status_code=500, detail=str(db_err))


@app.post("/api/alphas/{alpha_id}/local_correlation_check")
def local_correlation_check_endpoint(alpha_id: str, admin: str = Depends(get_current_admin)):
    """对单个因子触发本地自相关性计算与更新/重命名"""
    from app.services.background_inspector import BackgroundInspector
    from app.services.wq_client import login_with_credentials
    
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
        s = login_with_credentials(username.strip(), password.strip())
        inspector = BackgroundInspector()
        inspector._run_autocorrelation(s, alpha_id, dict(alpha))
        s.close()
        return {"status": "ok", "message": "本地自相关性检查和重命名计算完成。"}
    except Exception as e:
        logger.error(f"Failed to perform local correlation check for {alpha_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
