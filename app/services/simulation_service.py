from __future__ import annotations

import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd
import requests
import threading
from typing import Any

from ..paths import CATALOG_DIR, LOG_DIR
from ..storage import get_setting, update_job, add_job_event, upsert_alpha
from ..job_runner import JobRunner, redirected_stdout, redirected_stderr
from .wq_client import login_with_credentials, get_current_daily_limit_count
from .catalog_service import load_fields_from_cache, run_catalog_refresh

logger = logging.getLogger(__name__)

def _init_job_log_thread(log_file):
    try:
        redirected_stdout.local.file = log_file
        redirected_stderr.local.file = log_file
    except Exception:
        pass


def is_in_blocked_window(start_str: str, end_str: str) -> bool:
    """检查当前是否处于中国时间禁用段"""
    if not start_str or not end_str or (start_str == "00:00" and end_str == "00:00"):
        return False
    try:
        sh_tz = ZoneInfo("Asia/Shanghai")
        now_sh = datetime.now(sh_tz)
        now_time = now_sh.strftime("%H:%M")
        
        if start_str <= end_str:
            return start_str <= now_time <= end_str
        else:  # 跨子夜情况
            return now_time >= start_str or now_time <= end_str
    except Exception as e:
        logger.error(f"Error checking blocked window: {e}")
        return False


def check_limits_and_wait(job_id: int, s: requests.Session) -> None:
    """限额与时间窗口循环拦截器。达到限制时会使 Job 进入挂起等待状态。"""
    runner = JobRunner()
    
    while True:
        runner.check_paused(job_id)
        
        blocked_start = get_setting("blocked_start_cn", "00:00")
        blocked_end = get_setting("blocked_end_cn", "00:00")
        if is_in_blocked_window(blocked_start, blocked_end):
            msg = f"Inside blocked time window ({blocked_start} - {blocked_end} CN). Waiting..."
            update_job(job_id, status="waiting_time_window", message=msg)
            print(f"[Limit Check] {msg}", flush=True)
            # 循环检查，每 10 秒唤醒一次以支持暂停响应
            time.sleep(10)
            continue
            
        daily_limit = int(get_setting("backtest_daily_limit", "4500"))
        daily_count = get_current_daily_limit_count(s)
        if daily_count >= daily_limit:
            poll_minutes = float(get_setting("poll_minutes", "20"))
            
            # 刷新观察窗口：12:00-14:00 缩短为 5 分钟
            sh_tz = ZoneInfo("Asia/Shanghai")
            now_sh = datetime.now(sh_tz)
            now_time = now_sh.strftime("%H:%M")
            is_refresh_window = "12:00" <= now_time <= "14:00"
            sleep_seconds = 300 if is_refresh_window else int(poll_minutes * 60)
            
            msg = f"Daily limit reached ({daily_count}/{daily_limit}). Waiting {sleep_seconds // 60}m for reset..."
            update_job(job_id, status="waiting_limit", message=msg)
            print(f"[Limit Check] {msg}", flush=True)
            
            slept = 0
            while slept < sleep_seconds:
                runner.check_paused(job_id)
                time.sleep(10)
                slept += 10
            continue
            
        # 通过校验，恢复 running 状态并继续
        update_job(job_id, status="running")
        break


def handle_reconnect(job_id: int, reconnect_count: int) -> requests.Session:
    """网络断开或 session 失效时的自动重连状态机"""
    from ..job_runner import JobRunner
    runner = JobRunner()
    
    short_sleep = int(get_setting("reconnect_short_sleep_seconds", "300"))
    long_sleep = int(get_setting("reconnect_long_sleep_seconds", "3600"))
    
    wait_time = short_sleep if reconnect_count < 2 else long_sleep
    msg = f"Connection issues. Reconnecting in {wait_time} seconds (attempt {reconnect_count + 1})..."
    update_job(job_id, status="reconnecting", message=msg)
    add_job_event(job_id, "warning", f"Connection error. Sleep {wait_time}s before reconnect.")
    
    slept = 0
    while slept < wait_time:
        runner.check_paused(job_id)
        time.sleep(5)
        slept += 5
        
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    
    try:
        s = login_with_credentials(username, password)
        add_job_event(job_id, "info", "Reconnection successful.")
        update_job(job_id, status="running")
        return s
    except Exception as e:
        logger.error(f"Reconnection login failed: {e}")
        raise


def save_children_alphas(s: requests.Session, progress_url: str, region: str, universe: str, source: str) -> None:
    """提取 multi-simulation 的子任务 Alpha ID，并录入本地数据库"""
    try:
        resp = s.get(progress_url, timeout=30)
        if resp.status_code != 200:
            return
        
        data = resp.json()
        children = data.get("children", [])
        for child_id in children:
            child_resp = s.get(f"https://api.worldquantbrain.com/simulations/{child_id}", timeout=30)
            if child_resp.status_code == 200:
                child_data = child_resp.json()
                alpha_id = child_data.get("alpha")
                if alpha_id:
                    metrics = child_data.get("is", {})
                    record = {
                        "alpha_id": alpha_id,
                        "alpha_type": "",
                        "name": "",
                        "region": region,
                        "universe": universe,
                        "sharpe": metrics.get("sharpe"),
                        "fitness": metrics.get("fitness"),
                        "status": "UNSUBMITTED",
                        "source": source,
                        "payload": child_data
                    }
                    upsert_alpha(record)
    except Exception as e:
        logger.error(f"Failed to fetch child alpha details for {progress_url}: {e}")


def run_simulation_pool_with_control(
    job_id: int,
    alpha_pools: list[Any],
    neut: str,
    region: str,
    universe: str,
    log_path: Path,
) -> None:
    """定制的多线程 Simulation 执行器，支持限额限时拦截、优雅暂停、自动重连以及入库"""
    from consultant_core.machine_lib import (
        next_simulation_start,
        generate_sim_data,
        write_simulation_log,
        _response_content_text
    )
    import concurrent.futures
    
    runner = JobRunner()
    
    # 1. 检查断点
    start_index = next_simulation_start(str(log_path))
    if start_index == 0:
        write_simulation_log(
            str(log_path),
            {
                "event": "simulation_run_start",
                "start": 0,
                "pool_count": len(alpha_pools),
                "neutralization": neut,
                "region": region,
                "universe": universe,
            },
        )
        
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    s = login_with_credentials(username, password)
    
    session_container = {"session": s}
    session_lock = threading.Lock()
    limit_lock = threading.Lock()
    status_lock = threading.Lock()
    reconnect_count = 0
    
    total_pools = len(alpha_pools)
    
    try:
        for x, pool in enumerate(alpha_pools):
            if x < start_index:
                continue
                
            runner.check_paused(job_id)
            
            # 更新 Job 进度
            pct = int((x / total_pools) * 100) if total_pools > 0 else 0
            update_job(job_id, progress_current=x+1, progress_total=total_pools, message=f"Processing pool {x+1}/{total_pools}...")
            
            pool_failed = [False]
            write_simulation_log(str(log_path), {"event": "pool_start", "pool_index": x, "task_count": len(pool)})
            print(f"\n==================================================", flush=True)
            print(f"[Pool {x+1} / {total_pools}] Starting concurrency stage with {len(pool)} concurrent multi-simulation slots...", flush=True)
            print(f"==================================================", flush=True)
            
            def run_single_task(y, task):
                nonlocal reconnect_count
                runner.check_paused(job_id)
                
                print(f"[Pool {x+1}] [Slot {y+1}] Starting simulation of {len(task)} alphas...", flush=True)
                for idx, t_item in enumerate(task):
                    expr = t_item[0] if isinstance(t_item, tuple) else t_item
                    decay = t_item[1] if isinstance(t_item, tuple) and len(t_item) > 1 else 0
                    print(f"  - Alpha {idx+1}: {expr} (decay={decay})", flush=True)
                
                # A. 额度和时间窗口检查
                with limit_lock:
                    with session_lock:
                        cur_sess = session_container["session"]
                    check_limits_and_wait(job_id, cur_sess)
                    
                sim_data = generate_sim_data(task, region, universe, neut)
                write_simulation_log(
                    str(log_path),
                    {
                        "event": "task_post_start",
                        "pool_index": x,
                        "task_index": y,
                        "alpha_count": len(task),
                    },
                )
                
                progress_url = None
                attempts = 0
                max_post_retries = 3
                while attempts < max_post_retries:
                    runner.check_paused(job_id)
                    with session_lock:
                        thread_session = session_container["session"]
                        
                    try:
                        print(f"[Pool {x+1}] [Slot {y+1}] Sending POST request to WorldQuant Brain (Attempt {attempts+1}/{max_post_retries})...", flush=True)
                        simulation_response = thread_session.post('https://api.worldquantbrain.com/simulations', json=sim_data, timeout=60)
                        
                        if simulation_response.status_code == 429:
                            retry_after = int(simulation_response.headers.get("Retry-After", 5))
                            logger.info(f"Rate limited (429). Sleeping for {retry_after}s...")
                            print(f"[Pool {x+1}] [Slot {y+1}] Rate limited (429). Sleeping for {retry_after}s before retry...", flush=True)
                            time.sleep(retry_after)
                            continue
                            
                        if simulation_response.status_code == 401:
                            raise ConnectionResetError("Unauthorized token.")
                            
                        progress_url = simulation_response.headers['Location']
                        print(f"[Pool {x+1}] [Slot {y+1}] POST successful. Progress URL: {progress_url}", flush=True)
                        write_simulation_log(
                            str(log_path),
                            {
                                "event": "task_post_submitted",
                                "pool_index": x,
                                "task_index": y,
                                "progress_url": progress_url,
                            },
                        )
                        break
                        
                    except Exception as exc:
                        attempts += 1
                        logger.warning(f"Error POSTing simulation: {exc}. Attempt {attempts}/{max_post_retries}")
                        print(f"[Pool {x+1}] [Slot {y+1}] Error POSTing simulation: {exc}. Attempt {attempts}/{max_post_retries}", flush=True)
                        if attempts >= max_post_retries:
                            with status_lock:
                                pool_failed[0] = True
                            content = _response_content_text(simulation_response) if simulation_response else str(exc)
                            write_simulation_log(
                                str(log_path),
                                {
                                    "event": "task_post_error",
                                    "pool_index": x,
                                    "task_index": y,
                                    "status_code": getattr(simulation_response, "status_code", None),
                                    "message": content,
                                    "exception": repr(exc),
                                },
                            )
                            print(f"[Pool {x+1}] [Slot {y+1}] Location key error or post failure: {content}", flush=True)
                            
                            if isinstance(exc, (requests.exceptions.RequestException, OSError, ConnectionResetError)):
                                with session_lock:
                                    if session_container["session"] == thread_session:
                                        session_container["session"] = handle_reconnect(job_id, reconnect_count)
                                        reconnect_count += 1
                            else:
                                time.sleep(60)
                            break
                        else:
                            time.sleep(5)
                            
                if not progress_url:
                    print(f"[Pool {x+1}] [Slot {y+1}] Failed to submit task. Skipping polling.", flush=True)
                    return
                    
                # B. 轮询并提取结果
                try:
                    simulation_progress = None
                    print(f"[Pool {x+1}] [Slot {y+1}] Starting polling loop for WQ Brain simulation...", flush=True)
                    while True:
                        runner.check_paused(job_id)
                        with session_lock:
                            thread_session = session_container["session"]
                            
                        try:
                            simulation_progress = thread_session.get(progress_url, timeout=30)
                        except (requests.exceptions.RequestException, OSError) as exc:
                            print(f"[Pool {x+1}] [Slot {y+1}] Connection issues while polling: {exc}. Reconnecting...", flush=True)
                            with session_lock:
                                if session_container["session"] == thread_session:
                                    session_container["session"] = handle_reconnect(job_id, reconnect_count)
                                    reconnect_count += 1
                            continue
                            
                        if simulation_progress.status_code == 401:
                            print(f"[Pool {x+1}] [Slot {y+1}] Token expired while polling. Reconnecting...", flush=True)
                            with session_lock:
                                if session_container["session"] == thread_session:
                                    session_container["session"] = handle_reconnect(job_id, reconnect_count)
                                    reconnect_count += 1
                            continue
                            
                        retry_after = float(simulation_progress.headers.get("Retry-After", 0))
                        if retry_after == 0:
                            break
                        print(f"[Pool {x+1}] [Slot {y+1}] Simulation in progress. Checking again in {retry_after}s...", flush=True)
                        time.sleep(retry_after)
                        
                    status_str = simulation_progress.json().get("status", "")
                    if status_str != "COMPLETE":
                        with status_lock:
                            pool_failed[0] = True
                        write_simulation_log(
                            str(log_path),
                            {
                                "event": "simulation_not_complete",
                                "pool_index": x,
                                "task_index": y,
                                "progress_url": progress_url,
                                "status": status_str,
                            },
                        )
                        print(f"[Pool {x+1}] [Slot {y+1}] Simulation not complete. WQ status: {status_str}", flush=True)
                    else:
                        print(f"[Pool {x+1}] [Slot {y+1}] Simulation COMPLETE. Saving child alphas to local database...", flush=True)
                        write_simulation_log(
                            str(log_path),
                            {
                                "event": "simulation_complete",
                                "pool_index": x,
                                "task_index": y,
                                "progress_url": progress_url,
                            },
                        )
                        with session_lock:
                            current_s = session_container["session"]
                        save_children_alphas(current_s, progress_url, region, universe, f"job_{job_id}")
                        print(f"[Pool {x+1}] [Slot {y+1}] Alphas saved successfully.", flush=True)
                        
                except Exception as e:
                    with status_lock:
                        pool_failed[0] = True
                    write_simulation_log(
                        str(log_path),
                        {
                            "event": "simulation_poll_error",
                            "pool_index": x,
                            "task_index": y,
                            "progress_url": progress_url,
                            "exception": repr(e),
                        },
                    )
                    print(f"[Pool {x+1}] [Slot {y+1}] Poll error occurred: {e}", flush=True)
            
            # 获取当前主线程的日志文件对象，用于在子线程中做输出重定向
            log_file = getattr(redirected_stdout.local, "file", None)
            
            # 使用 ThreadPoolExecutor 并发处理当前 pool 的所有任务
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(pool),
                initializer=_init_job_log_thread,
                initargs=(log_file,)
            ) as executor:
                # 提交所有任务
                futures = [executor.submit(run_single_task, y, task) for y, task in enumerate(pool)]
                # 等待所有任务完成
                concurrent.futures.wait(futures)
                
            print(f"[Pool {x+1} / {total_pools}] Concurrency stage done.", flush=True)
            
            if not pool_failed[0]:
                write_simulation_log(str(log_path), {"event": "pool_complete", "pool_index": x})
                
        write_simulation_log(str(log_path), {"event": "simulation_run_complete"})
        
    finally:
        with session_lock:
            session_container["session"].close()


def derive_prune_prefix(fields: list[dict[str, Any]]) -> str | None:
    """自动推导字段前缀（例如 mcr38, anl4 等）。
    前缀最多次数占比 >= PRUNE_PREFIX_MIN_SHARE（默认 60%）时生效。
    """
    prefixes = []
    for f in fields:
        field_id = f.get("id")
        if field_id and "_" in field_id:
            prefixes.append(field_id.split("_")[0])
    if not prefixes:
        return None
        
    counter = Counter(prefixes)
    most_common, count = counter.most_common(1)[0]
    share = count / len(fields)
    min_share = float(get_setting("prune_prefix_min_share", "0.6"))
    if share >= min_share:
        return most_common
    return None


def run_backtest_job(job_id: int, params: dict[str, Any]) -> None:
    """后台任务主入口：三阶段回测业务控制层"""
    from consultant_core import machine_lib
    from consultant_core.machine_lib import (
        process_datafields,
        recommended_neutralization_table,
        split_processed_datafields_by_neutralization,
        first_order_factory,
        load_task_pool,
        get_recent_alphas,
        prune,
        get_group_second_order_factory,
        trade_when_factory,
        load_webdatascope_info
    )
    
    # 动态修补 machine_lib 内部的 login 函数，使其读写 SQLite 配置
    def custom_login():
        username = get_setting("wq_username")
        password = get_setting("wq_password")
        return login_with_credentials(username, password)
        
    machine_lib.login = custom_login
    
    # 获取任务配置参数
    dataset_ids = params.get("dataset_ids", [])
    run_fo = params.get("run_fo", True)
    run_so = params.get("run_so", True)
    run_th = params.get("run_th", True)
    
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    
    region = get_setting("region", "USA")
    universe = get_setting("universe", "TOP3000")
    delay = int(get_setting("delay", "1"))
    instrument_type = get_setting("instrument_type", "EQUITY")
    
    fo_children = int(get_setting("fo_backtest_children") or get_setting("backtest_children", "6"))
    fo_threads = int(get_setting("fo_backtest_threads") or get_setting("backtest_threads", "10"))
    so_children = int(get_setting("so_backtest_children") or get_setting("backtest_children", "5"))
    so_threads = int(get_setting("so_backtest_threads") or get_setting("backtest_threads", "8"))
    th_children = int(get_setting("th_backtest_children") or get_setting("backtest_children", "5"))
    th_threads = int(get_setting("th_backtest_threads") or get_setting("backtest_threads", "8"))
    
    timezone_name = get_setting("alpha_date_timezone", "Asia/Shanghai")
    fetch_limit_multiplier = int(get_setting("alpha_fetch_limit_multiplier", "3"))
    
    # 校验数据集
    if not dataset_ids:
        raise ValueError("No dataset_ids provided.")
        
    total_datasets = len(dataset_ids)
    
    for idx, dataset_id in enumerate(dataset_ids):
        msg = f"Starting backtest for dataset {dataset_id} ({idx+1}/{total_datasets})..."
        logger.info(msg)
        update_job(job_id, message=msg)
        
        # 1. 获取本地字段缓存
        fields = load_fields_from_cache(region, universe, delay, dataset_id, instrument_type)
        if not fields:
            # 尝试远程下载刷新
            try:
                msg = f"Fields cache not found for {dataset_id}. Triggering refresh..."
                logger.info(msg)
                update_job(job_id, message=msg)
                # 模拟执行 catalog 刷新逻辑
                run_catalog_refresh(job_id)
                fields = load_fields_from_cache(region, universe, delay, dataset_id, instrument_type)
            except Exception as e:
                logger.error(f"Catalog refresh failed: {e}")
                
        if not fields:
            err = f"Dataset {dataset_id} fields cache is missing. Skipping this dataset."
            logger.error(err)
            add_job_event(job_id, "error", err)
            continue
            
        df_fields = pd.DataFrame(fields)
        
        # ==========================================
        # 阶段一：一阶 FO
        # ==========================================
        if run_fo:
            logger.info(f"[{dataset_id}] Starting FO Stage...")
            update_job(job_id, message=f"[{dataset_id}] Running FO Stage...")
            
            # 使用 machine_lib 清洗字段
            processed_fields = process_datafields(df_fields)
            
            # 推荐 Neutralization 评分
            try:
                webdatascope_info = load_webdatascope_info()
            except Exception as e:
                logger.error(f"Failed to load webdatascope info: {e}")
                webdatascope_info = {}
            recs = recommended_neutralization_table(
                df_fields,
                webdatascope_info,
                dataset_id,
                region=region,
                universe=universe,
                delay=delay
            )
                
            groups = split_processed_datafields_by_neutralization(df_fields, recs)
            
            # 逐个 neutralization 分组执行
            for neut_name, neut_fields in groups.items():
                logger.info(f"[{dataset_id}] Neutralization group: {neut_name} ({len(neut_fields)} fields)")
                
                # 生成一阶表达式
                fo_alphas = first_order_factory(neut_fields, machine_lib.ts_ops)
                # 转换为 (alpha, decay) 列表，一阶默认 decay=0
                fo_tuples = [(alpha, 0) for alpha in fo_alphas]
                
                # 构建 Pool
                fo_pools = load_task_pool(fo_tuples, fo_children, fo_threads)
                
                # 设定日志断点文件
                fo_log_path = LOG_DIR / f"fo_progress_{job_id}_{dataset_id}_{neut_name}.jsonl"
                
                run_simulation_pool_with_control(
                    job_id=job_id,
                    alpha_pools=fo_pools,
                    neut=neut_name,
                    region=region,
                    universe=universe,
                    log_path=fo_log_path
                )
                
        # ==========================================
        # 阶段二：二阶 SO
        # ==========================================
        if run_so:
            logger.info(f"[{dataset_id}] Starting SO Stage...")
            update_job(job_id, message=f"[{dataset_id}] Running SO Stage...")
            
            # 获取 SO 参数
            fo_track_lookback = int(get_setting("fo_track_lookback_days", "90"))
            fo_track_sharpe = float(get_setting("fo_track_sharpe", "1.0"))
            fo_track_fitness = float(get_setting("fo_track_fitness", "0.7"))
            fo_track_num = int(get_setting("fo_track_alpha_num", "100"))
            
            # 拉取一阶追踪候选
            session = login_with_credentials(username, password)
            try:
                fo_tracker = get_recent_alphas(
                    lookback_days=fo_track_lookback,
                    sharpe_th=fo_track_sharpe,
                    fitness_th=fo_track_fitness,
                    region=region,
                    universe=universe,
                    alpha_num=fo_track_num,
                    usage="track",
                    timezone_name=timezone_name,
                    fetch_limit_multiplier=fetch_limit_multiplier,
                    session=session,
                    verbose=True
                )
            finally:
                session.close()
                
            if not fo_tracker:
                logger.info(f"[{dataset_id}] No eligible FO tracker candidates. Skipping SO Stage.")
                add_job_event(job_id, "warning", f"[{dataset_id}] No FO tracker candidates. Skipping SO.")
            else:
                # 剪枝与 Fallback 策略
                prefix = derive_prune_prefix(fields)
                keep_num = int(get_setting("prune_keep_num", "5"))
                
                pruned_candidates = []
                if prefix:
                    try:
                        pruned_candidates = prune(fo_tracker, prefix, keep_num)
                        logger.info(f"[{dataset_id}] Pruned using prefix '{prefix}' -> {len(pruned_candidates)} left.")
                    except Exception as e:
                        logger.warning(f"Prune failed: {e}. Fallback to sorting.")
                        
                if not pruned_candidates:
                    fallback_keep = int(get_setting("track_fallback_keep_num", "50"))
                    # 已经默认按 Sharpe 排序，截取前 N 项并组合
                    pruned_candidates = [[rec[1], rec[-1]] for rec in fo_tracker[:fallback_keep]]
                    logger.info(f"[{dataset_id}] Prune failed/skipped. Used global fallback selection: {len(pruned_candidates)} candidates.")
                    
                # 生成二阶算子表达式
                group_ops = get_setting("group_ops", "group_neutralize,group_rank,group_zscore").split(",")
                # pruned_candidates 是 [[expr, decay]] 结构。需要只传递其中的 expr 列表
                expr_list = [c[0] for c in pruned_candidates]
                so_alphas = get_group_second_order_factory(expr_list, group_ops, region)
                
                # 默认二阶 decay 继承一阶
                so_tuples = []
                # 建立字典映射以便寻找原始 decay
                decay_map = {c[0]: c[1] for c in pruned_candidates}
                for so_alpha in so_alphas:
                    # 匹配原字段的 decay
                    decay = 0
                    for k, v in decay_map.items():
                        if k in so_alpha:
                            decay = v
                            break
                    so_tuples.append((so_alpha, decay))
                    
                so_pools = load_task_pool(so_tuples, so_children, so_threads)
                so_log_path = LOG_DIR / f"so_progress_{job_id}_{dataset_id}.jsonl"
                
                # 二阶的 neutralization 使用默认
                run_simulation_pool_with_control(
                    job_id=job_id,
                    alpha_pools=so_pools,
                    neut="INDUSTRY", # SO 默认 neut 级别
                    region=region,
                    universe=universe,
                    log_path=so_log_path
                )
                
        # ==========================================
        # 阶段三：三阶 TH
        # ==========================================
        if run_th:
            logger.info(f"[{dataset_id}] Starting TH Stage...")
            update_job(job_id, message=f"[{dataset_id}] Running TH Stage...")
            
            # 获取 TH 参数
            so_track_lookback = int(get_setting("so_track_lookback_days", "90"))
            so_track_sharpe = float(get_setting("so_track_sharpe", "1.3"))
            so_track_fitness = float(get_setting("so_track_fitness", "0.8"))
            so_track_num = int(get_setting("so_track_alpha_num", "100"))
            
            # 拉取二阶追踪候选
            session = login_with_credentials(username, password)
            try:
                so_tracker = get_recent_alphas(
                    lookback_days=so_track_lookback,
                    sharpe_th=so_track_sharpe,
                    fitness_th=so_track_fitness,
                    region=region,
                    universe=universe,
                    alpha_num=so_track_num,
                    usage="track",
                    timezone_name=timezone_name,
                    fetch_limit_multiplier=fetch_limit_multiplier,
                    session=session,
                    verbose=True
                )
            finally:
                session.close()
                
            if not so_tracker:
                logger.info(f"[{dataset_id}] No eligible SO tracker candidates. Skipping TH Stage.")
                add_job_event(job_id, "warning", f"[{dataset_id}] No SO tracker candidates. Skipping TH.")
            else:
                prefix = derive_prune_prefix(fields)
                keep_num = int(get_setting("prune_keep_num", "5"))
                
                pruned_candidates = []
                if prefix:
                    try:
                        pruned_candidates = prune(so_tracker, prefix, keep_num)
                        logger.info(f"[{dataset_id}] Pruned using prefix '{prefix}' -> {len(pruned_candidates)} left.")
                    except Exception as e:
                        logger.warning(f"Prune failed: {e}. Fallback to sorting.")
                        
                if not pruned_candidates:
                    fallback_keep = int(get_setting("track_fallback_keep_num", "50"))
                    pruned_candidates = [[rec[1], rec[-1]] for rec in so_tracker[:fallback_keep]]
                    logger.info(f"[{dataset_id}] Prune failed/skipped. Used global fallback selection: {len(pruned_candidates)} candidates.")
                    
                # 生成三阶交易控制表达式
                th_alphas = []
                decay_map = {c[0]: c[1] for c in pruned_candidates}
                for c in pruned_candidates:
                    th_alphas += trade_when_factory("trade_when", c[0], region)
                    
                th_tuples = []
                for th_alpha in th_alphas:
                    decay = 0
                    for k, v in decay_map.items():
                        if k in th_alpha:
                            decay = v
                            break
                    th_tuples.append((th_alpha, decay))
                    
                th_pools = load_task_pool(th_tuples, th_children, th_threads)
                th_log_path = LOG_DIR / f"th_progress_{job_id}_{dataset_id}.jsonl"
                
                run_simulation_pool_with_control(
                    job_id=job_id,
                    alpha_pools=th_pools,
                    neut="INDUSTRY",
                    region=region,
                    universe=universe,
                    log_path=th_log_path
                )
                
        # 单个数据集成功结束
        add_job_event(job_id, "info", f"Dataset {dataset_id} completed through all requested stages.")
