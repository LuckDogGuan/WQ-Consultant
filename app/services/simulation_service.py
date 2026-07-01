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
from ..storage import get_setting, update_job, add_job_event, upsert_alpha, connect
from ..job_runner import JobRunner, redirected_stdout, redirected_stderr
from .wq_client import WQRateLimitError, login_with_credentials, get_current_daily_limit_count
from .catalog_service import load_fields_from_cache, run_catalog_refresh
from .wq_retry_policy import classify_post_exception, next_wait_seconds, should_retry_without_skipping
from .correlation_service import run_inline_correlation_check


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


_daily_alpha_count_cache: int | None = None
_daily_alpha_count_time: float = 0.0
_daily_alpha_count_lock = threading.Lock()


def get_cached_daily_limit_count(s: requests.Session) -> int:
    global _daily_alpha_count_cache, _daily_alpha_count_time
    with _daily_alpha_count_lock:
        now = time.time()
        # 缓存过期时间为 5 分钟 (300 秒)
        if _daily_alpha_count_cache is None or now - _daily_alpha_count_time > 300:
            _daily_alpha_count_cache = get_current_daily_limit_count(s)
            _daily_alpha_count_time = now
        return _daily_alpha_count_cache


def increment_cached_daily_limit_count(n: int) -> None:
    global _daily_alpha_count_cache
    with _daily_alpha_count_lock:
        if _daily_alpha_count_cache is not None:
            _daily_alpha_count_cache += n


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
        daily_count = get_cached_daily_limit_count(s)
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
            
            global _daily_alpha_count_cache
            with _daily_alpha_count_lock:
                _daily_alpha_count_cache = None
            continue
            
        # 通过校验，恢复 running 状态并继续
        update_job(job_id, status="running")
        break


def handle_reconnect(job_id: int, reconnect_count: int) -> requests.Session:
    """网络断开或 session 失效时的自动重连状态机"""
    from ..job_runner import JobRunner
    runner = JobRunner()
    
    short_sleep = int(get_setting("reconnect_short_sleep_seconds", "300"))
    long_sleep = int(get_setting("reconnect_long_sleep_seconds", "300"))
    
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
    
    s = login_with_rate_limit_wait(job_id, username, password, context="reconnect")
    add_job_event(job_id, "info", "Reconnection successful.")
    update_job(job_id, status="running")
    return s


def login_with_rate_limit_wait(job_id: int, username: str, password: str, context: str = "login") -> requests.Session:
    runner = JobRunner()
    rate_limit_failures = 0
    while True:
        runner.check_paused(job_id)
        try:
            session = login_with_credentials(username, password)
            if rate_limit_failures:
                add_job_event(job_id, "info", f"WQ login recovered after {rate_limit_failures} rate-limit response(s).")
            return session
        except WQRateLimitError as exc:
            rate_limit_failures += 1
            wait_seconds = configured_rate_limit_wait_seconds(rate_limit_failures)
            msg = (
                f"WQ login rate limited (429) during {context}. "
                f"Waiting {wait_seconds}s before retry; consecutive 429 count {rate_limit_failures}."
            )
            logger.info(msg)
            update_job(job_id, status="waiting_limit", message=msg)
            add_job_event(job_id, "warning", msg, {"error": str(exc), "rate_limit_failures": rate_limit_failures})
            sleep_with_pause_checks(job_id, wait_seconds)


def save_children_alphas(s: requests.Session, progress_url: str, region: str, universe: str, source: str) -> list[str]:
    """提取 multi-simulation 的子任务 Alpha ID，并录入本地数据库，返回保存成功的 ID 列表"""
    saved_ids = []
    try:
        resp = s.get(progress_url, timeout=30)
        if resp.status_code != 200:
            return []
        
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
                        "margin": metrics.get("margin"),
                        "returns": metrics.get("returns"),
                        "drawdown": metrics.get("drawdown"),
                        "status": "UNSUBMITTED",
                        "source": source,
                        "payload": child_data
                    }
                    upsert_alpha(record)
                    saved_ids.append(alpha_id)
                    
                    # 因子评级诊断：若为 Grade D，触发 WQ 平台上的模拟退休/隐藏
                    try:
                        from .template_iteration import grade_candidate_result
                        grading = grade_candidate_result({
                            "sharpe": metrics.get("sharpe"),
                            "fitness": metrics.get("fitness"),
                            "margin": metrics.get("margin"),
                            "turnover": metrics.get("turnover"),
                            "self_corr": 0.0,
                            "prod_corr": 0.0,
                            "failed_checks": 0,
                        })
                        if grading.get("grade") == "D":
                            from .wq_client import retire_wq_alpha
                            retire_wq_alpha(s, alpha_id)
                    except Exception as ge:
                        logger.error(f"Error grading and retiring child alpha {alpha_id}: {ge}")
    except Exception as e:
        logger.error(f"Failed to fetch child alpha details for {progress_url}: {e}")
    return saved_ids


def run_simulation_pool_with_control(
    job_id: int,
    alpha_pools: list[Any],
    neut: str,
    region: str,
    universe: str,
    log_path: Path,
    progress_context: dict[str, Any] | None = None,
) -> list[str]:
    """定制的回测执行器，支持限额限时拦截、优雅暂停、自动重连以及入库。
    采用单线程顺序发送与轮询机制，利用 WQ 服务端异步并发，彻底避免客户端并发导致的 429 报错与锁死。
    """
    from consultant_core.machine_lib import (
        next_simulation_start,
        generate_sim_data,
        write_simulation_log,
        _response_content_text
    )
    
    runner = JobRunner()
    all_saved_ids = []
    
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
    s = login_with_rate_limit_wait(job_id, username, password, context="simulation pool startup")
    
    reconnect_count = 0
    total_pools = len(alpha_pools)
    emitted_progress_milestones: set[int] = set()
    
    try:
        print(f"\n==================================================", flush=True)
        print(f"Starting sequential simulation batch execution...", flush=True)
        print(f"Total pools to process: {total_pools - start_index} (Pools {start_index+1} to {total_pools})", flush=True)
        print(f"==================================================\n", flush=True)

        if progress_context:
            started_msg = format_backtest_stage_detail_message(
                dataset_id=str(progress_context["dataset_id"]),
                stage_name=str(progress_context["stage_name"]),
                stage_index=int(progress_context["stage_index"]),
                stages_per_dataset=int(progress_context["stages_per_dataset"]),
                completed_pools=start_index,
                total_pools=total_pools,
                group_label=progress_context.get("group_label"),
            )
        else:
            started_msg = f"Stage pool progress: {start_index}/{total_pools}."
        progress_current, progress_total = stage_detail_progress_values(start_index, total_pools)
        update_job(
            job_id,
            progress_current=progress_current,
            progress_total=progress_total,
            message=started_msg,
        )
        add_job_event(job_id, "info", started_msg)

        # 顺序执行每一个大 Pool
        for x in range(start_index, total_pools):
            runner.check_paused(job_id)
            pool = alpha_pools[x]
            write_simulation_log(str(log_path), {"event": "pool_start", "pool_index": x, "task_count": len(pool)})
            
            progress_urls = []
            pool_failed_flag = False
            
            # 阶段 A：顺序发送当前 Pool 内的所有回测任务 (POST)
            for y, task in enumerate(pool):
                runner.check_paused(job_id)
                
                print(f"[Pool {x+1}] [Slot {y+1}] Starting simulation of {len(task)} alphas...", flush=True)
                for idx, t_item in enumerate(task):
                    expr = t_item[0] if isinstance(t_item, tuple) else t_item
                    decay = t_item[1] if isinstance(t_item, tuple) and len(t_item) > 1 else 0
                    print(f"  - Alpha {idx+1}: {expr} (decay={decay})", flush=True)
                
                # 限额限时校验
                check_limits_and_wait(job_id, s)
                
                sim_data = generate_sim_data(task, region, universe, neut)
                post_payload = normalize_simulation_post_payload(sim_data)
                payload_shape = "single" if isinstance(sim_data, list) and len(sim_data) == 1 else "multi"
                write_simulation_log(
                    str(log_path),
                    {
                        "event": "task_post_start",
                        "pool_index": x,
                        "task_index": y,
                        "alpha_count": len(task),
                        "payload_shape": payload_shape,
                    },
                )
                
                progress_url = None
                attempts = 0
                max_post_retries = 3
                rate_limit_failures = 0
                network_failures = 0
                while attempts < max_post_retries:
                    runner.check_paused(job_id)
                    try:
                        print(f"[Pool {x+1}] [Slot {y+1}] Sending POST request to WorldQuant Brain (Attempt {attempts+1}/{max_post_retries})...", flush=True)
                        simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=post_payload, timeout=60)
                        
                        if simulation_response.status_code == 429:
                            rate_limit_failures += 1
                            retry_after = configured_rate_limit_wait_seconds(rate_limit_failures)
                            msg = (
                                f"Rate limited by WQ (429). Waiting {retry_after}s before retry; "
                                f"consecutive 429 count {rate_limit_failures}."
                            )
                            logger.info(msg)
                            update_job(job_id, status="waiting_limit", message=msg)
                            print(f"[Pool {x+1}] [Slot {y+1}] {msg}", flush=True)
                            sleep_with_pause_checks(job_id, retry_after)
                            continue
                            
                        if simulation_response.status_code == 401:
                            raise ConnectionResetError("Unauthorized token.")
                            
                        progress_url = simulation_response.headers.get("Location")
                        if not progress_url:
                            raise RuntimeError(describe_missing_location_response(simulation_response))
                        rate_limit_failures = 0
                        network_failures = 0
                        print(f"[Pool {x+1}] [Slot {y+1}] POST successful. Progress URL: {progress_url}", flush=True)
                        
                        # 成功 POST 后，累加缓存中的每日额度值
                        increment_cached_daily_limit_count(len(task))
                        
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
                        network_failures += 1
                        decision = classify_post_exception(
                            exc,
                            failure_count=network_failures,
                            short_wait_seconds=int(get_setting("reconnect_short_sleep_seconds", "300") or "300"),
                            long_wait_seconds=int(get_setting("reconnect_long_sleep_seconds", "300") or "300"),
                        )
                        if should_retry_without_skipping(decision):
                            msg = (
                                f"Network error during WQ submit. Waiting {decision.wait_seconds}s before retry; "
                                f"consecutive network failure count {network_failures}."
                            )
                            logger.warning(f"{msg} Error: {exc}")
                            update_job(job_id, status="reconnecting", message=msg)
                            add_job_event(
                                job_id,
                                "warning",
                                msg,
                                {"reason": decision.reason, "exception": repr(exc), "pool_index": x, "task_index": y},
                            )
                            print(f"[Pool {x+1}] [Slot {y+1}] {msg}", flush=True)
                            sleep_with_pause_checks(job_id, decision.wait_seconds)
                            try:
                                s.close()
                            except Exception:
                                pass
                            s = login_with_rate_limit_wait(
                                job_id,
                                username,
                                password,
                                context="simulation post network recovery",
                            )
                            continue

                        attempts += 1
                        logger.warning(f"Error POSTing simulation: {exc}. Attempt {attempts}/{max_post_retries}")
                        print(f"[Pool {x+1}] [Slot {y+1}] Error POSTing simulation: {exc}. Attempt {attempts}/{max_post_retries}", flush=True)
                        if attempts >= max_post_retries:
                            pool_failed_flag = True
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
                                s = handle_reconnect(job_id, reconnect_count)
                                reconnect_count += 1
                            else:
                                time.sleep(60)
                            break
                        else:
                            time.sleep(5)
                            
                if progress_url:
                    progress_urls.append((y, progress_url))
                    # 在发送成功后，如果不是当前 Pool 的最后一个任务，加入动态延迟以平滑请求，防止 WQ 触发 429 限流
                    if y < len(pool) - 1:
                        # 动态计算延迟：基础 1.0 秒，每多一个子回测(槽/slot)增加 0.15 秒
                        post_delay = max(1.0, len(task) * 0.15)
                        print(f"Pacing POST requests: sleeping {post_delay:.1f}s to prevent rate limits...", flush=True)
                        sleep_with_pause_checks(job_id, int(round(post_delay)))
                else:
                    print(f"[Pool {x+1}] [Slot {y+1}] Failed to submit task. Skipping polling.", flush=True)
            
            # 阶段 B：顺序轮询检查当前 Pool 内所有任务的状态 (GET)
            for y, progress_url in progress_urls:
                try:
                    simulation_progress = None
                    print(f"[Pool {x+1}] [Slot {y+1}] Starting polling loop for WQ Brain simulation...", flush=True)
                    while True:
                        runner.check_paused(job_id)
                        try:
                            simulation_progress = s.get(progress_url, timeout=30)
                        except (requests.exceptions.RequestException, OSError) as exc:
                            print(f"[Pool {x+1}] [Slot {y+1}] Connection issues while polling: {exc}. Reconnecting...", flush=True)
                            s = handle_reconnect(job_id, reconnect_count)
                            reconnect_count += 1
                            continue
                            
                        if simulation_progress.status_code == 401:
                            print(f"[Pool {x+1}] [Slot {y+1}] Token expired while polling. Reconnecting...", flush=True)
                            s = handle_reconnect(job_id, reconnect_count)
                            reconnect_count += 1
                            continue
                            
                        if simulation_progress.status_code == 429:
                            retry_after = int(simulation_progress.headers.get("Retry-After", 5))
                            sleep_time = min(60, retry_after)
                            print(f"[Pool {x+1}] [Slot {y+1}] Polling rate limited (429). Sleeping for {sleep_time}s...", flush=True)
                            sleep_with_pause_checks(job_id, sleep_time)
                            continue
                            
                        retry_after = float(simulation_progress.headers.get("Retry-After", 0))
                        if retry_after == 0:
                            break
                        sleep_time = max(20.0, retry_after)
                        print(f"[Pool {x+1}] [Slot {y+1}] Simulation in progress. Checking again in {sleep_time}s...", flush=True)
                        time.sleep(sleep_time)
                        
                    status_str = simulation_progress.json().get("status", "")
                    if status_str != "COMPLETE":
                        pool_failed_flag = True
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
                        child_ids = save_children_alphas(s, progress_url, region, universe, f"job_{job_id}")
                        all_saved_ids.extend(child_ids)
                        print(f"[Pool {x+1}] [Slot {y+1}] Alphas saved successfully.", flush=True)
                        
                except Exception as e:
                    pool_failed_flag = True
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
                    
            if not pool_failed_flag:
                write_simulation_log(str(log_path), {"event": "pool_complete", "pool_index": x})
                print(f"\n[Pool {x+1} / {total_pools}] Pool completed successfully.", flush=True)
            else:
                print(f"\n[Pool {x+1} / {total_pools}] Pool failed.", flush=True)
                
            # 更新整体 Job 进度
            completed_pools = x + 1
            if progress_context:
                msg = format_backtest_stage_detail_message(
                    dataset_id=str(progress_context["dataset_id"]),
                    stage_name=str(progress_context["stage_name"]),
                    stage_index=int(progress_context["stage_index"]),
                    stages_per_dataset=int(progress_context["stages_per_dataset"]),
                    completed_pools=completed_pools,
                    total_pools=total_pools,
                    group_label=progress_context.get("group_label"),
                )
            else:
                msg = f"Stage pool progress: {completed_pools}/{total_pools}."
            progress_current, progress_total = stage_detail_progress_values(
                completed_pools,
                total_pools,
            )
            update_job(
                job_id,
                progress_current=progress_current,
                progress_total=progress_total,
                message=msg,
            )
            if should_emit_stage_progress_event(
                completed_pools,
                total_pools,
                emitted_progress_milestones,
            ):
                add_job_event(job_id, "info", msg)

        write_simulation_log(str(log_path), {"event": "simulation_run_complete"})
        return all_saved_ids
        
    finally:
        try:
            s.close()
        except Exception:
            pass


def derive_prune_prefix(fields: list[dict[str, Any]], params: dict[str, Any] | None = None) -> str | None:
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
    if params is not None:
        min_share = get_float_param(params, "prune_prefix_min_share", 0.6)
    else:
        min_share = float(get_setting("prune_prefix_min_share", "0.6"))
    if share >= min_share:
        return most_common
    return None


def is_simulation_stage_complete(log_path: Path) -> bool:
    """读取日志文件，判定这一阶段是否已经完整跑完"""
    if not log_path.exists():
        return False
    try:
        import json
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if data.get("event") == "simulation_run_complete":
                        return True
                except Exception:
                    pass
    except Exception:
        pass
    return False


def build_backtest_stage_plan(
    dataset_ids: list[str],
    run_fo: bool,
    run_so: bool,
    run_th: bool,
) -> list[tuple[str, str, int, int, int, int, int, int]]:
    """Build coarse backtest progress units: one enabled stage per dataset."""
    enabled_stages: list[str] = []
    if run_fo:
        enabled_stages.append("FO")
    if run_so:
        enabled_stages.append("SO")
    if run_th:
        enabled_stages.append("TH")

    total_datasets = len(dataset_ids)
    stages_per_dataset = len(enabled_stages)
    total_stages = total_datasets * stages_per_dataset
    plan: list[tuple[str, str, int, int, int, int, int, int]] = []
    stage_current = 0
    for dataset_index, dataset_id in enumerate(dataset_ids, start=1):
        for stage_index, stage_name in enumerate(enabled_stages, start=1):
            stage_current += 1
            plan.append(
                (
                    dataset_id,
                    stage_name,
                    dataset_index,
                    total_datasets,
                    stage_index,
                    stages_per_dataset,
                    stage_current,
                    total_stages,
                )
            )
    return plan


def format_backtest_progress_message(
    dataset_id: str,
    stage_name: str,
    dataset_index: int,
    total_datasets: int,
    stage_index: int,
    stages_per_dataset: int,
    stage_current: int,
    stage_total: int,
    action: str,
) -> str:
    action_label = {
        "started": "已开始",
        "completed": "已完成",
        "skipped": "已跳过",
    }.get(action, action)
    return (
        f"[{dataset_id}] {stage_name} {action_label}。"
        f"数据集 {dataset_index}/{total_datasets}，"
        f"当前阶段 {stage_index}/{stages_per_dataset}，"
        f"总进度 {stage_current}/{stage_total}。"
    )


def format_backtest_stage_detail_message(
    dataset_id: str,
    stage_name: str,
    stage_index: int,
    stages_per_dataset: int,
    completed_pools: int,
    total_pools: int,
    group_label: str | None = None,
) -> str:
    group_text = f"{group_label}，" if group_label else ""
    return (
        f"[{dataset_id}] {stage_name} 小阶段进度："
        f"{group_text}Pool {completed_pools}/{total_pools}，"
        f"当前阶段 {stage_index}/{stages_per_dataset}。"
    )


def describe_missing_location_response(response: Any) -> str:
    status_code = getattr(response, "status_code", None)
    headers = getattr(response, "headers", {}) or {}
    retry_after = headers.get("Retry-After") if hasattr(headers, "get") else None
    body = _short_response_text(response)
    parts = [f"WQ simulation response missing Location header (status={status_code})"]
    if retry_after:
        parts.append(f"Retry-After={retry_after}")
    if body:
        parts.append(f"body={body}")
    return "; ".join(parts)


def normalize_simulation_post_payload(sim_data: Any) -> Any:
    """WorldQuant expects one simulation as an object and multi-simulation as an array."""
    if isinstance(sim_data, list) and len(sim_data) == 1:
        return sim_data[0]
    return sim_data


def rate_limit_retry_seconds(
    failure_count: int,
    short_seconds: int = 30,
    long_seconds: int = 300,
    cycle_size: int = 5,
) -> int:
    return next_wait_seconds(
        failure_count,
        short_seconds=short_seconds,
        long_seconds=long_seconds,
        cycle_size=cycle_size,
    )


def configured_rate_limit_wait_seconds(failure_count: int) -> int:
    long_wait = int(get_setting("reconnect_long_sleep_seconds", "300") or "300")
    return rate_limit_retry_seconds(failure_count, short_seconds=30, long_seconds=long_wait)


def sleep_with_pause_checks(job_id: int, seconds: int) -> None:
    runner = JobRunner()
    remaining = max(0, int(seconds))
    while remaining > 0:
        runner.check_paused(job_id)
        chunk = min(5, remaining)
        time.sleep(chunk)
        remaining -= chunk


def _short_response_text(response: Any, limit: int = 500) -> str:
    text = getattr(response, "text", "")
    if not text:
        try:
            text = response.content.decode("utf-8", errors="replace")
        except Exception:
            text = ""
    text = str(text).replace("\r", " ").replace("\n", " ").strip()
    return text[:limit]


def stage_detail_progress_values(completed_pools: int, total_pools: int) -> tuple[int, int]:
    if total_pools <= 0:
        return 0, 0
    completed = max(0, min(completed_pools, total_pools))
    return completed, total_pools


def should_emit_stage_progress_event(
    completed_pools: int,
    total_pools: int,
    emitted_milestones: set[int],
) -> bool:
    if total_pools <= 0:
        return False
    if completed_pools >= total_pools and 100 not in emitted_milestones:
        emitted_milestones.add(100)
        return True

    percent = int(completed_pools * 100 / total_pools)
    for milestone in (25, 50, 75):
        if percent >= milestone and milestone not in emitted_milestones:
            emitted_milestones.add(milestone)
            return True
    return False


def get_bool_param(params: dict[str, Any], key: str, default_val: bool) -> bool:
    val = params.get(key)
    if val is not None:
        if isinstance(val, bool):
            return val
        return str(val).lower() in ("true", "1", "yes")
    return get_setting(key, "1" if default_val else "0") == "1"


def get_int_param(params: dict[str, Any], key: str, default_val: int) -> int:
    val = params.get(key)
    if val is not None:
        try:
            return int(val)
        except ValueError:
            pass
    return int(get_setting(key, str(default_val)))


def get_float_param(params: dict[str, Any], key: str, default_val: float) -> float:
    val = params.get(key)
    if val is not None:
        try:
            return float(val)
        except ValueError:
            pass
    return float(get_setting(key, str(default_val)))


def get_str_param(params: dict[str, Any], key: str, default_val: str) -> str:
    val = params.get(key)
    if val is not None:
        return str(val)
    return get_setting(key, default_val)




def stage_pool_settings(
    params: dict[str, Any],
    region: str,
    stage: str,
    default_children: int,
    default_threads: int,
) -> tuple[int, int]:
    config = params.get("region_stage_config") if isinstance(params, dict) else None
    if not isinstance(config, dict):
        return default_children, default_threads
    region_config = config.get(str(region or "").upper())
    if not isinstance(region_config, dict):
        return default_children, default_threads
    stage_config = region_config.get(str(stage or "").upper())
    if not isinstance(stage_config, dict):
        return default_children, default_threads
    children = stage_config.get("children", default_children)
    threads = stage_config.get("threads", default_threads)
    try:
        children = int(children)
    except Exception:
        children = default_children
    try:
        threads = int(threads)
    except Exception:
        threads = default_threads
    return max(1, children), max(1, threads)
def run_backtest_job(job_id: int, params: dict[str, Any]) -> None:
    """后台任务主入口：三阶段回测业务控制层"""
    from .check_service import run_inline_checks
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
        return login_with_rate_limit_wait(job_id, username, password, context="machine_lib login")
        
    machine_lib.login = custom_login
    
    # 获取任务配置参数
    dataset_ids = params.get("dataset_ids", [])
    run_fo = params.get("run_fo", True)
    run_so = params.get("run_so", True)
    run_th = params.get("run_th", True)
    
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    
    base_region = get_setting("region", "USA")
    regions = params.get("regions") or [base_region]
    regions = [str(item).upper() for item in regions if str(item).upper() in {"USA", "ASI", "EUR"}] or [base_region]
    region = regions[0]
    universe = get_setting("universe", "TOP3000")
    delay = int(get_setting("delay", "1"))
    instrument_type = get_setting("instrument_type", "EQUITY")
    
    custom_alphas = params.get("custom_alphas")
    if custom_alphas:
        logger.info(f"Starting custom backtest job for {len(custom_alphas)} alphas...")
        update_job(job_id, message=f"Starting custom alpha simulation for {len(custom_alphas)} candidates...")
        
        fo_tuples = []
        for item in custom_alphas:
            if isinstance(item, (tuple, list)):
                fo_tuples.append((item[0], item[1]))
            else:
                fo_tuples.append((item, 0))
                
        default_fo_children = int(get_setting("fo_backtest_children") or get_setting("backtest_children", "6"))
        default_fo_threads = int(get_setting("fo_backtest_threads") or get_setting("backtest_threads", "10"))
        fo_children, fo_threads = stage_pool_settings(params, region, "FO", default_fo_children, default_fo_threads)
        custom_pools = load_task_pool(fo_tuples, fo_children, fo_threads)
        
        custom_log_path = LOG_DIR / f"custom_progress_{job_id}.jsonl"
        saved_ids = run_simulation_pool_with_control(
            job_id=job_id,
            alpha_pools=custom_pools,
            neut=params.get("neutralization") or "INDUSTRY",
            region=region,
            universe=universe,
            log_path=custom_log_path,
        )
        
        if saved_ids:
            msg = f"Custom simulation completed. Running inline correlation and checks for {len(saved_ids)} saved alphas..."
            logger.info(msg)
            update_job(job_id, message=msg)
            
            session = login_with_rate_limit_wait(job_id, username, password, context="Custom Alphas Checks")
            try:
                run_inline_correlation_check(session, saved_ids, job_id)
                run_inline_checks(session, saved_ids)
            finally:
                session.close()
                
            add_job_event(job_id, "info", f"Custom backtest successfully finished. {len(saved_ids)} alphas evaluated.")
        else:
            add_job_event(job_id, "warning", "Custom simulation yielded no saved alphas.")
        return

    default_fo_children = int(get_setting("fo_backtest_children") or get_setting("backtest_children", "6"))
    default_fo_threads = int(get_setting("fo_backtest_threads") or get_setting("backtest_threads", "10"))
    default_so_children = int(get_setting("so_backtest_children") or get_setting("backtest_children", "5"))
    default_so_threads = int(get_setting("so_backtest_threads") or get_setting("backtest_threads", "8"))
    default_th_children = int(get_setting("th_backtest_children") or get_setting("backtest_children", "5"))
    default_th_threads = int(get_setting("th_backtest_threads") or get_setting("backtest_threads", "8"))
    
    timezone_name = get_setting("alpha_date_timezone", "Asia/Shanghai")
    fetch_limit_multiplier = int(get_setting("alpha_fetch_limit_multiplier", "3"))
    
    # 校验数据集
    if not dataset_ids:
        raise ValueError("No dataset_ids provided.")
        
    work_items = [(region_name, dataset_id) for region_name in regions for dataset_id in dataset_ids]
    dataset_labels = [f"{region_name}:{dataset_id}" if len(regions) > 1 else dataset_id for region_name, dataset_id in work_items]
    total_datasets = len(work_items)
    stage_plan = build_backtest_stage_plan(dataset_labels, run_fo, run_so, run_th)
    total_stages = len(stage_plan)
    stage_lookup = {
        (dataset_index, stage_name): (
            dataset_id,
            stage_name,
            dataset_index,
            total_dataset_count,
            stage_index,
            stages_per_dataset,
            stage_current,
            stage_total,
        )
        for (
            dataset_id,
            stage_name,
            dataset_index,
            total_dataset_count,
            stage_index,
            stages_per_dataset,
            stage_current,
            stage_total,
        ) in stage_plan
    }

    update_job(
        job_id,
        progress_current=0,
        progress_total=0,
        message=f"Backtest queue ready. Total stages: 0/{total_stages}.",
    )
    add_job_event(job_id, "info", f"Backtest queue ready. Total stages: 0/{total_stages}.")

    def mark_stage(stage_name: str, dataset_index: int, action: str) -> None:
        plan_item = stage_lookup.get((dataset_index, stage_name))
        if not plan_item:
            return
        (
            dataset_id,
            stage_name,
            dataset_index,
            total_dataset_count,
            stage_index,
            stages_per_dataset,
            stage_current,
            stage_total,
        ) = plan_item
        progress_current = stage_current if action in {"completed", "skipped"} else stage_current - 1
        msg = format_backtest_progress_message(
            dataset_id=dataset_id,
            stage_name=stage_name,
            dataset_index=dataset_index,
            total_datasets=total_dataset_count,
            stage_index=stage_index,
            stages_per_dataset=stages_per_dataset,
            stage_current=progress_current,
            stage_total=stage_total,
            action=action,
        )
        logger.info(msg)
        if action in {"started", "skipped"}:
            update_job(job_id, progress_current=0, progress_total=0, message=msg)
        else:
            update_job(job_id, message=msg)
        add_job_event(job_id, "info", msg)

    def stage_progress_context(
        stage_name: str,
        dataset_index: int,
        group_label: str | None = None,
    ) -> dict[str, Any] | None:
        plan_item = stage_lookup.get((dataset_index, stage_name))
        if not plan_item:
            return None
        (
            dataset_id,
            stage_name,
            _dataset_index,
            _total_dataset_count,
            stage_index,
            stages_per_dataset,
            _stage_current,
            _stage_total,
        ) = plan_item
        return {
            "dataset_id": dataset_id,
            "stage_name": stage_name,
            "stage_index": stage_index,
            "stages_per_dataset": stages_per_dataset,
            "group_label": group_label,
        }
    
    for idx, (region, dataset_id) in enumerate(work_items):
        dataset_label = dataset_labels[idx]
        fo_children, fo_threads = stage_pool_settings(params, region, "FO", default_fo_children, default_fo_threads)
        so_children, so_threads = stage_pool_settings(params, region, "SO", default_so_children, default_so_threads)
        th_children, th_threads = stage_pool_settings(params, region, "TH", default_th_children, default_th_threads)
        msg = f"Starting backtest for dataset {dataset_label} ({idx+1}/{total_datasets})..."
        logger.info(msg)
        update_job(job_id, message=msg)
        add_job_event(job_id, "info", msg)
        
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
            for stage_name in ("FO", "SO", "TH"):
                if (idx + 1, stage_name) in stage_lookup:
                    mark_stage(stage_name, idx + 1, "skipped")
            continue
            
        df_fields = pd.DataFrame(fields)
        
        # ==========================================
        # 阶段一：一阶 FO
        # ==========================================
        if run_fo:
            logger.info(f"[{dataset_id}] Starting FO Stage...")
            mark_stage("FO", idx + 1, "started")
            
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
            group_items = list(groups.items())
            
            # 逐个 neutralization 分组执行
            for group_index, (neut_name, neut_fields) in enumerate(group_items, start=1):
                # 设定日志断点文件
                fo_log_path = LOG_DIR / f"fo_progress_{job_id}_{dataset_id}_{neut_name}.jsonl"
                if is_simulation_stage_complete(fo_log_path):
                    logger.info(f"[{dataset_id}] FO Stage for group {neut_name} already completed. Skipping.")
                    continue
                
                logger.info(f"[{dataset_id}] Neutralization group: {neut_name} ({len(neut_fields)} fields)")
                
                # 生成一阶表达式
                fo_alphas = first_order_factory(neut_fields, machine_lib.ts_ops)
                # 转换为 (alpha, decay) 列表，一阶默认 decay=0
                fo_tuples = [(alpha, 0) for alpha in fo_alphas]
                
                # 构建 Pool
                fo_pools = load_task_pool(fo_tuples, fo_children, fo_threads)
                
                saved_ids = run_simulation_pool_with_control(
                    job_id=job_id,
                    alpha_pools=fo_pools,
                    neut=neut_name,
                    region=region,
                    universe=universe,
                    log_path=fo_log_path,
                    progress_context=stage_progress_context(
                        "FO",
                        idx + 1,
                        group_label=f"分组 {group_index}/{len(group_items)}: {neut_name}",
                    ),
                )
                if saved_ids:
                    # ── 负夏普垃圾因子过滤（厂字识别）──
                    if get_bool_param(params, "fo_filter_negative_sharpe", True):
                        neg_ids = []
                        placeholders_ns = ",".join(["?"] * len(saved_ids))
                        with connect() as conn:
                            ns_rows = conn.execute(
                                f"SELECT alpha_id, sharpe FROM alpha_records WHERE alpha_id IN ({placeholders_ns})",
                                saved_ids
                            ).fetchall()
                        for ns_row in ns_rows:
                            if ns_row["sharpe"] is not None and float(ns_row["sharpe"]) < 0:
                                neg_ids.append(ns_row["alpha_id"])
                        if neg_ids:
                            neg_ph = ",".join(["?"] * len(neg_ids))
                            with connect() as conn:
                                conn.execute(f"DELETE FROM alpha_records WHERE alpha_id IN ({neg_ph})", neg_ids)
                            add_job_event(job_id, "info",
                                f"[{dataset_id}] FO: Removed {len(neg_ids)} negative-sharpe garbage alphas (厂字过滤).")
                            saved_ids = [aid for aid in saved_ids if aid not in neg_ids]

                    # ── FO 穿插相关性检查（可配置开关）──
                    if saved_ids and get_bool_param(params, "fo_corr_enable", True):
                        msg = f"[{dataset_id}] FO Group {neut_name}: Running inline correlation checks for {len(saved_ids)} alphas..."
                        logger.info(msg)
                        update_job(job_id, message=msg)
                        add_job_event(job_id, "info", msg)

                        session = login_with_rate_limit_wait(job_id, username, password, context="FO Inline Correlation")
                        try:
                            run_inline_correlation_check(session, saved_ids, job_id, stage="FO")
                        finally:
                            session.close()
            mark_stage("FO", idx + 1, "completed")
                
        # ==========================================
        # 阶段二：二阶 SO
        # ==========================================
        if run_so:
            so_log_path = LOG_DIR / f"so_progress_{job_id}_{dataset_id}.jsonl"
            if is_simulation_stage_complete(so_log_path):
                logger.info(f"[{dataset_id}] SO Stage already completed. Skipping.")
                mark_stage("SO", idx + 1, "completed")
            else:
                logger.info(f"[{dataset_id}] Starting SO Stage...")
                mark_stage("SO", idx + 1, "started")
                
                # 获取 SO 参数
                fo_track_lookback = get_int_param(params, "fo_track_lookback_days", 90)
                fo_track_sharpe = get_float_param(params, "fo_track_sharpe", 1.0)
                fo_track_fitness = get_float_param(params, "fo_track_fitness", 0.7)
                fo_track_num = get_int_param(params, "fo_track_alpha_num", 100)
                
                # 拉取一阶追踪候选
                session = login_with_rate_limit_wait(job_id, username, password, context="FO tracker")
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
                    
                if fo_tracker:
                    alpha_ids = [rec[0] for rec in fo_tracker]
                    placeholders = ",".join(["?"] * len(alpha_ids))
                    with connect() as conn:
                        rows = conn.execute(
                            f"SELECT alpha_id, alpha_type, status FROM alpha_records WHERE alpha_id IN ({placeholders})",
                            alpha_ids
                        ).fetchall()
                    db_map = {r["alpha_id"]: r for r in rows}
                    
                    filtered_fo_tracker = []
                    for rec in fo_tracker:
                        aid = rec[0]
                        if aid in db_map:
                            alpha_type = db_map[aid]["alpha_type"]
                            status = db_map[aid]["status"]
                            if alpha_type == 'SKIP':
                                logger.info(f"[{dataset_id}] Filtering out FO candidate {aid}: alpha_type is SKIP (correlation conflict/厂字)")
                                continue
                            if status and ("FAIL" in status.upper() or "ERROR" in status.upper()):
                                logger.info(f"[{dataset_id}] Filtering out FO candidate {aid}: status is {status} (bad curve/checks failed)")
                                continue
                        filtered_fo_tracker.append(rec)
                    
                    original_len = len(fo_tracker)
                    fo_tracker = filtered_fo_tracker
                    logger.info(f"[{dataset_id}] Filtered FO tracker candidates: {original_len} -> {len(fo_tracker)}")
                    
                if not fo_tracker:
                    logger.info(f"[{dataset_id}] No eligible FO tracker candidates. Skipping SO Stage.")
                    add_job_event(job_id, "warning", f"[{dataset_id}] No FO tracker candidates. Skipping SO.")
                    mark_stage("SO", idx + 1, "skipped")
                else:
                    # 剪枝与 Fallback 策略
                    prefix = derive_prune_prefix(fields, params)
                    keep_num = get_int_param(params, "prune_keep_num", 5)
                    
                    pruned_candidates = []
                    if prefix:
                        try:
                            pruned_candidates = prune(fo_tracker, prefix, keep_num)
                            logger.info(f"[{dataset_id}] Pruned using prefix '{prefix}' -> {len(pruned_candidates)} left.")
                        except Exception as e:
                            logger.warning(f"Prune failed: {e}. Fallback to sorting.")
                            
                    if not pruned_candidates:
                        fallback_keep = get_int_param(params, "track_fallback_keep_num", 50)
                        # 已经默认按 Sharpe 排序，截取前 N 项并组合
                        pruned_candidates = [[rec[1], rec[-1]] for rec in fo_tracker[:fallback_keep]]
                        logger.info(f"[{dataset_id}] Prune failed/skipped. Used global fallback selection: {len(pruned_candidates)} candidates.")
                        
                    # 生成二阶算子表达式
                    group_ops = get_str_param(params, "group_ops", "group_neutralize,group_rank,group_zscore").split(",")
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

                    # 二阶的 neutralization 使用默认
                    so_saved_ids = run_simulation_pool_with_control(
                        job_id=job_id,
                        alpha_pools=so_pools,
                        neut="INDUSTRY",
                        region=region,
                        universe=universe,
                        log_path=so_log_path,
                        progress_context=stage_progress_context("SO", idx + 1),
                    )

                    # ── SO 负夏普垃圾因子过滤（厂字识别）──
                    if so_saved_ids and get_bool_param(params, "so_filter_negative_sharpe", True):
                        neg_ids = []
                        placeholders_ns = ",".join(["?"] * len(so_saved_ids))
                        with connect() as conn:
                            ns_rows = conn.execute(
                                f"SELECT alpha_id, sharpe FROM alpha_records WHERE alpha_id IN ({placeholders_ns})",
                                so_saved_ids
                            ).fetchall()
                        for ns_row in ns_rows:
                            if ns_row["sharpe"] is not None and float(ns_row["sharpe"]) < 0:
                                neg_ids.append(ns_row["alpha_id"])
                        if neg_ids:
                            neg_ph = ",".join(["?"] * len(neg_ids))
                            with connect() as conn:
                                conn.execute(f"DELETE FROM alpha_records WHERE alpha_id IN ({neg_ph})", neg_ids)
                            add_job_event(job_id, "info",
                                f"[{dataset_id}] SO: Removed {len(neg_ids)} negative-sharpe garbage alphas (厂字过滤).")
                            so_saved_ids = [aid for aid in so_saved_ids if aid not in neg_ids]

                    # ── SO 穿插相关性检查（可配置开关）──
                    if so_saved_ids and get_bool_param(params, "so_corr_enable", False):
                        msg = f"[{dataset_id}] SO: Running inline correlation checks for {len(so_saved_ids)} alphas..."
                        logger.info(msg)
                        update_job(job_id, message=msg)
                        add_job_event(job_id, "info", msg)

                        session = login_with_rate_limit_wait(job_id, username, password, context="SO Inline Correlation")
                        try:
                            run_inline_correlation_check(session, so_saved_ids, job_id, stage="SO")
                        finally:
                            session.close()

                    mark_stage("SO", idx + 1, "completed")
                
        # ==========================================
        # 阶段三：三阶 TH
        # ==========================================
        if run_th:
            th_log_path = LOG_DIR / f"th_progress_{job_id}_{dataset_id}.jsonl"
            if is_simulation_stage_complete(th_log_path):
                logger.info(f"[{dataset_id}] TH Stage already completed. Skipping.")
                mark_stage("TH", idx + 1, "completed")
            else:
                logger.info(f"[{dataset_id}] Starting TH Stage...")
                mark_stage("TH", idx + 1, "started")
                
                # 获取 TH 参数
                so_track_lookback = get_int_param(params, "so_track_lookback_days", 90)
                so_track_sharpe = get_float_param(params, "so_track_sharpe", 1.3)
                so_track_fitness = get_float_param(params, "so_track_fitness", 0.8)
                so_track_num = get_int_param(params, "so_track_alpha_num", 100)
                
                # 拉取二阶追踪候选
                session = login_with_rate_limit_wait(job_id, username, password, context="SO tracker")
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
                    
                if so_tracker:
                    alpha_ids = [rec[0] for rec in so_tracker]
                    placeholders = ",".join(["?"] * len(alpha_ids))
                    with connect() as conn:
                        rows = conn.execute(
                            f"SELECT alpha_id, alpha_type, status FROM alpha_records WHERE alpha_id IN ({placeholders})",
                            alpha_ids
                        ).fetchall()
                    db_map = {r["alpha_id"]: r for r in rows}
                    
                    filtered_so_tracker = []
                    for rec in so_tracker:
                        aid = rec[0]
                        if aid in db_map:
                            alpha_type = db_map[aid]["alpha_type"]
                            status = db_map[aid]["status"]
                            if alpha_type == 'SKIP':
                                logger.info(f"[{dataset_id}] Filtering out SO candidate {aid}: alpha_type is SKIP (correlation conflict/厂字)")
                                continue
                            if status and ("FAIL" in status.upper() or "ERROR" in status.upper()):
                                logger.info(f"[{dataset_id}] Filtering out SO candidate {aid}: status is {status} (bad curve/checks failed)")
                                continue
                        filtered_so_tracker.append(rec)
                    
                    original_len = len(so_tracker)
                    so_tracker = filtered_so_tracker
                    logger.info(f"[{dataset_id}] Filtered SO tracker candidates: {original_len} -> {len(so_tracker)}")
                    
                if not so_tracker:
                    logger.info(f"[{dataset_id}] No eligible SO tracker candidates. Skipping TH Stage.")
                    add_job_event(job_id, "warning", f"[{dataset_id}] No SO tracker candidates. Skipping TH.")
                    mark_stage("TH", idx + 1, "skipped")
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
                    
                    saved_ids = run_simulation_pool_with_control(
                        job_id=job_id,
                        alpha_pools=th_pools,
                        neut="INDUSTRY",
                        region=region,
                        universe=universe,
                        log_path=th_log_path,
                        progress_context=stage_progress_context("TH", idx + 1),
                    )
                    if saved_ids:
                        msg = f"[{dataset_id}] TH: Running inline checks for {len(saved_ids)} new alphas..."
                        logger.info(msg)
                        update_job(job_id, message=msg)
                        add_job_event(job_id, "info", msg)

                        session = login_with_rate_limit_wait(job_id, username, password, context="TH Inline Checks")
                        try:
                            # ── TH 穿插相关性检查（可配置开关）──
                            if get_setting("th_corr_enable", "0") == "1":
                                run_inline_correlation_check(session, saved_ids, job_id, stage="TH")
                            run_inline_checks(session, saved_ids)
                        finally:
                            session.close()
                    mark_stage("TH", idx + 1, "completed")
                
        # 单个数据集成功结束
        add_job_event(job_id, "info", f"Dataset {dataset_id} completed through all requested stages.")
