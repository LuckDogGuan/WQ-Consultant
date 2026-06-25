from __future__ import annotations

import logging
import pickle
import os
import time
import concurrent.futures
from datetime import datetime, timedelta
import pandas as pd
from typing import Any

from ..paths import CORRELATION_DIR
from ..storage import get_setting, update_job, add_job_event, upsert_alpha, connect
from ..job_runner import JobRunner
from .wq_client import login_with_credentials

logger = logging.getLogger(__name__)


def save_obj(obj: Any, name: str) -> None:
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name: str) -> Any:
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)


def wait_get(sess: Any, url: str, max_retries: int = 10) -> Any:
    retries = 0
    while retries < max_retries:
        while True:
            try:
                res = sess.get(url, timeout=30)
            except Exception as e:
                logger.error(f"Request failed: {url} -> {e}")
                time.sleep(2 ** retries)
                break
            
            retry_after = res.headers.get("Retry-After", 0)
            if retry_after == 0 or retry_after is None:
                if res.status_code < 400:
                    return res
                break
            time.sleep(float(retry_after))
        retries += 1
        time.sleep(2 ** retries)
    return None


def get_alpha_pnl(sess: Any, alpha_id: str) -> pd.DataFrame:
    resp = wait_get(sess, f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl")
    if not resp:
        return pd.DataFrame()
    pnl = resp.json()
    if 'records' not in pnl or 'schema' not in pnl:
        return pd.DataFrame()
    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])
    if 'date' in df.columns and 'pnl' in df.columns:
        df = df.rename(columns={'date': 'Date', 'pnl': alpha_id})
        df = df[['Date', alpha_id]]
    return df


def get_os_alphas(sess: Any, limit: int = 100, get_first: bool = False) -> list[dict[str, Any]]:
    fetched_alphas = []
    offset = 0
    total_alphas = 100
    while len(fetched_alphas) < total_alphas:
        logger.info(f"Fetching OS alphas from offset {offset} to {offset + limit}...")
        url = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}&order=-dateSubmitted"
        res = wait_get(sess, url)
        if not res:
            break
        res_json = res.json()
        if offset == 0:
            total_alphas = res_json.get('count', 100)
        alphas = res_json.get("results", [])
        fetched_alphas.extend(alphas)
        if len(alphas) < limit:
            break
        offset += limit
        if get_first:
            break
    return fetched_alphas[:total_alphas]


def download_correlation_data(sess: Any, flag_increment: bool = True) -> None:
    """拉取并更新本地 OS Alphas 的 PnL 缓存数据"""
    ids_path = str(CORRELATION_DIR / 'os_alpha_ids')
    pnls_path = str(CORRELATION_DIR / 'os_alpha_pnls')
    ppac_path = str(CORRELATION_DIR / 'ppac_alpha_ids')
    
    try:
        if flag_increment:
            os_alpha_ids = load_obj(ids_path)
            os_alpha_pnls = load_obj(pnls_path)
            ppac_alpha_ids = load_obj(ppac_path)
            exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
        else:
            raise FileNotFoundError
    except Exception:
        logger.info("Existing correlation cache not found. Performing full cache refresh.")
        os_alpha_ids = {}
        os_alpha_pnls = pd.DataFrame()
        exist_alpha = []
        ppac_alpha_ids = []
        
    if not os_alpha_ids:
        alphas = get_os_alphas(sess, limit=100, get_first=False)
    else:
        # 增量模式：拉取最近 30 条以追加新 OS alpha
        alphas = get_os_alphas(sess, limit=30, get_first=True)
        
    new_alphas = [item for item in alphas if item['id'] not in exist_alpha]
    if new_alphas:
        # 记录 Power Pool Alpha 标签
        ppac_alpha_ids += [
            item['id'] for item in new_alphas 
            if any(c.get('name') == 'Power Pool Alpha' for c in item.get('classifications', []))
        ]
        
        # 分组拉取 PnL
        from collections import defaultdict
        alpha_ids_grouped = defaultdict(list, os_alpha_ids)
        
        for item_alpha in new_alphas:
            region = item_alpha.get('settings', {}).get('region', 'USA')
            alpha_ids_grouped[region].append(item_alpha['id'])
            
        def fetch_pnl_func(alpha_id):
            df = get_alpha_pnl(sess, alpha_id)
            if not df.empty:
                return df.set_index('Date')
            return pd.DataFrame()
            
        workers = int(get_setting("corr_workers", "5"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(fetch_pnl_func, [item['id'] for item in new_alphas]))
            
        valid_results = [res for res in results if not res.empty]
        if valid_results:
            os_alpha_pnls = pd.concat([os_alpha_pnls] + valid_results, axis=1)
            os_alpha_pnls.sort_index(inplace=True)
            
        save_obj(dict(alpha_ids_grouped), ids_path)
        save_obj(os_alpha_pnls, pnls_path)
        save_obj(ppac_alpha_ids, ppac_path)
        
    logger.info(f"Downloaded {len(new_alphas)} new alphas. Total cached: {os_alpha_pnls.shape[1] if os_alpha_pnls is not None else 0}")


def load_correlation_data(tag: str | None = None) -> tuple[dict[str, list[str]], pd.DataFrame]:
    """载入本地 PnL 缓存，并转换计算回报率"""
    ids_path = str(CORRELATION_DIR / 'os_alpha_ids')
    pnls_path = str(CORRELATION_DIR / 'os_alpha_pnls')
    ppac_path = str(CORRELATION_DIR / 'ppac_alpha_ids')
    
    if not os.path.exists(ids_path + '.pickle') or not os.path.exists(pnls_path + '.pickle'):
        return {}, pd.DataFrame()
        
    os_alpha_ids = load_obj(ids_path)
    os_alpha_pnls = load_obj(pnls_path)
    ppac_alpha_ids = load_obj(ppac_path) if os.path.exists(ppac_path + '.pickle') else []
    
    import copy
    filtered_ids = copy.deepcopy(os_alpha_ids)
    
    if tag == 'PPAC':
        for r in filtered_ids:
            filtered_ids[r] = [alpha for alpha in filtered_ids[r] if alpha in ppac_alpha_ids]
    elif tag == 'SelfCorr':
        for r in filtered_ids:
            filtered_ids[r] = [alpha for alpha in filtered_ids[r] if alpha not in ppac_alpha_ids]
            
    exist_alpha = [alpha for ids in filtered_ids.values() for alpha in ids]
    valid_alphas = [a for a in exist_alpha if a in os_alpha_pnls.columns]
    
    if not valid_alphas:
        return filtered_ids, pd.DataFrame()
        
    filtered_pnls = os_alpha_pnls[valid_alphas]
    os_alpha_rets = filtered_pnls - filtered_pnls.ffill().shift(1)
    if not os_alpha_rets.empty and not os_alpha_rets.index.empty:
        os_alpha_rets.index = pd.to_datetime(os_alpha_rets.index)
        max_date = os_alpha_rets.index.max()
        if pd.notna(max_date):
            # 仅截取近 4 年数据以提高运算效率
            os_alpha_rets = os_alpha_rets[os_alpha_rets.index > max_date - pd.DateOffset(years=4)]
            
    return filtered_ids, os_alpha_rets


def calc_self_corr_local(alpha_rets_series: pd.Series, os_alpha_rets: pd.DataFrame, os_alpha_ids: dict[str, list[str]], region: str) -> float:
    """计算单个 alpha 与本地缓存库的最大相关性"""
    if os_alpha_rets.empty or alpha_rets_series.empty:
        return 0.0
        
    alpha_id = alpha_rets_series.name
    alpha_rets_series.index = pd.to_datetime(alpha_rets_series.index)
    max_date = alpha_rets_series.index.max()
    if pd.notna(max_date):
        alpha_rets_series = alpha_rets_series[alpha_rets_series.index > max_date - pd.DateOffset(years=4)]
        
    region_alphas = os_alpha_ids.get(region, [])
    valid_region_alphas = [a for a in region_alphas if a in os_alpha_rets.columns and a != alpha_id]
    
    if not valid_region_alphas:
        return 0.0
        
    corrs = os_alpha_rets[valid_region_alphas].corrwith(alpha_rets_series)
    self_corr = corrs.max()
    return float(self_corr) if pd.notna(self_corr) else 0.0


def run_correlation_job(job_id: int, params: dict[str, Any]) -> None:
    """JobRunner 调用的相关性诊断后台线程"""
    from consultant_core.machine_lib import get_alphas_full
    
    runner = JobRunner()
    
    # 读取凭据并登录
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    if not username or not password:
        raise ValueError("Missing WorldQuant credentials in Settings.")
        
    update_job(job_id, message="Logging in to WorldQuant Brain...")
    session = login_with_credentials(username, password)
    
    try:
        # 1. 增量更新本地 PnL 缓存
        update_job(job_id, message="Updating local OS alphas cache...")
        add_job_event(job_id, "info", "Downloading new OS alpha returns to cache...")
        download_correlation_data(session, flag_increment=True)
        
        runner.check_paused(job_id)
        
        # 2. 载入缓存
        update_job(job_id, message="Loading cached PnL returns...")
        ppa_ids, ppa_rets = load_correlation_data(tag='PPAC')
        all_ids, all_rets = load_correlation_data(tag=None)
        
        # 3. 拉取最近 unsubmitted 的 alphas
        lookback = int(params.get("lookback_days") or get_setting("corr_lookback_days", "14"))
        limit = params.get("limit") or get_setting("corr_fetch_limit", "")
        limit_val = int(limit) if limit and str(limit).isdigit() else None
        
        region = get_setting("region", "USA")
        universe = get_setting("universe", "TOP3000")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback)
        
        msg = f"Fetching unsubmitted alphas for {region} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})..."
        logger.info(msg)
        update_job(job_id, message=msg)
        
        alphas_df = get_alphas_full(
            start_date=start_date,
            end_date=end_date,
            sharpe_th=-10.0,  # 允许拉取低分进行本地筛选
            region=region,
            usage="submit",
            session=session,
            order="-dateCreated",
            limit=limit_val
        )
        
        if alphas_df.empty:
            msg = "No unsubmitted alphas found in the lookback window."
            logger.info(msg)
            update_job(job_id, message=msg)
            add_job_event(job_id, "info", msg)
            return
            
        total_fetched = len(alphas_df)
        
        # 进行 Pandas 初筛：
        # - Sharpe >= corr_threshold_sharpe 且 Fitness >= corr_threshold_fitness
        # - IS_FAIL / ERROR 只有在 Sharpe > 2.0 时保留
        corr_sharpe_th = float(get_setting("corr_threshold_sharpe", "1.0"))
        corr_fitness_th = float(get_setting("corr_threshold_fitness", "0.7"))
        
        valid_metrics = (alphas_df['sharpe'] >= corr_sharpe_th) & (alphas_df['fitness'] >= corr_fitness_th)
        is_fail = alphas_df['status'].isin(['IS_FAIL', 'ERROR'])
        valid_status = ~(is_fail & (alphas_df['sharpe'] <= 2.0))
        
        alphas_filtered = alphas_df[valid_metrics & valid_status]
        eligible_alphas = alphas_filtered.to_dict('records')
        
        # 增量断点恢复：过滤在这个 Job 中已经跑完并入库的项目
        with connect() as conn:
            finished_ids = {
                row["alpha_id"] 
                for row in conn.execute(
                    "SELECT alpha_id FROM alpha_records WHERE source = ?", 
                    (f"corr_check_{job_id}",)
                ).fetchall()
            }
        
        eligible_alphas = [a for a in eligible_alphas if a['alpha_id'] not in finished_ids]
        total_eligible = len(eligible_alphas) + len(finished_ids)
        completed = len(finished_ids)
        
        msg = f"Filtered {total_fetched} alphas down to {total_eligible} eligible candidates. (Already finished: {len(finished_ids)})"
        logger.info(msg)
        update_job(job_id, message=msg)
        add_job_event(job_id, "info", msg)
        
        if len(eligible_alphas) == 0:
            update_job(job_id, progress_current=total_eligible, progress_total=total_eligible, message="All candidates already analyzed.")
            return
            
        results = []
        
        # 4. 并发计算相关性与 L2Y Sharpe
        def analyze_single_alpha(row):
            alpha_id = row['alpha_id']
            row_region = row['region']
            sharpe = float(row['sharpe'])
            fitness = float(row['fitness'])
            is_ladder_pass = row['status'] not in ['IS_FAIL', 'ERROR']
            
            # 4.1 获取 PnL
            target_pnl_df = get_alpha_pnl(session, alpha_id)
            if target_pnl_df.empty or alpha_id not in target_pnl_df.columns:
                return None
                
            target_pnl_series = target_pnl_df.set_index('Date')[alpha_id]
            alpha_rets_series = target_pnl_series - target_pnl_series.ffill().shift(1)
            
            ppa_corr = calc_self_corr_local(alpha_rets_series, ppa_rets, ppa_ids, row_region)
            prod_corr = calc_self_corr_local(alpha_rets_series, all_rets, all_ids, row_region)
            
            # 4.2 计算 L2Y Sharpe
            l2y_sharpe = sharpe
            stats_resp = session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats", timeout=30)
            if stats_resp.status_code == 200 and stats_resp.text.strip():
                try:
                    stats_json = stats_resp.json()
                    stats = stats_json.get('records', [])
                    schema = stats_json.get('schema', {}).get('properties', [])
                    cols = [p['name'] for p in schema]
                    if stats and 'year' in cols and 'sharpe' in cols:
                        stats_df = pd.DataFrame(stats, columns=cols)
                        stats_df['year'] = pd.to_numeric(stats_df['year'])
                        stats_df['sharpe'] = pd.to_numeric(stats_df['sharpe'])
                        stats_df = stats_df.sort_values('year', ascending=False)
                        recent_2_years = stats_df.head(2)
                        l2y_sharpe = float(recent_2_years['sharpe'].mean())
                except Exception:
                    pass
            
            # 4.3 评定逻辑并生成推荐命名：类型_相关性_拟合度
            alpha_type = None
            target_name = None
            
            # 先判断 sharpe < corr_sharpe_th 或者是任何 correlation > 0.7 的，直接设为 anonymous
            if sharpe < corr_sharpe_th or prod_corr > 0.7 or ppa_corr > 0.7:
                alpha_type = "SKIP"
                target_name = "anonymous"
            else:
                # 获取 IS checks 异常数
                error_count = 0
                try:
                    check_resp = session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/check", timeout=30)
                    if check_resp.status_code == 200:
                        check_data = check_resp.json()
                        checks = check_data.get("is", {}).get("checks", [])
                        for chk in checks:
                            chk_res = str(chk.get("result") or "").upper()
                            if chk_res in {"FAIL", "FAILED", "ERROR"}:
                                error_count += 1
                except Exception as e:
                    logger.error(f"Failed to fetch checks for correlation analysis of {alpha_id}: {e}")
                    
                # 判定后续类型
                submit_sharpe_th = float(get_setting("submit_sharpe", "1.58"))
                if sharpe >= corr_sharpe_th and ppa_corr < 0.5:
                    if error_count > 0:
                        alpha_type = "SKIP"
                        target_name = "anonymous"
                    else:
                        alpha_type = "PPA"
                        target_name = f"PPA_{ppa_corr:.2f}_{fitness:.2f}"
                elif l2y_sharpe > 2.38 and prod_corr < 0.7:
                    if error_count < 2:
                        alpha_type = "ATOM"
                        target_name = f"ATOM_{prod_corr:.2f}_{fitness:.2f}_err{error_count}"
                    else:
                        alpha_type = "SKIP"
                        target_name = "anonymous"
                elif sharpe > submit_sharpe_th and prod_corr < 0.7 and is_ladder_pass:
                    if error_count > 0:
                        alpha_type = "SKIP"
                        target_name = "anonymous"
                    else:
                        alpha_type = "RA"
                        target_name = f"RA_{prod_corr:.2f}_{fitness:.2f}"
                else:
                    alpha_type = "SKIP"
                    target_name = "anonymous"
                
            return {
                'alpha_id': alpha_id,
                'name': row.get('name', ''),
                'region': row_region,
                'universe': row.get('universe', universe),
                'sharpe': sharpe,
                'fitness': fitness,
                'margin': row.get('margin'),
                'returns': row.get('returns'),
                'drawdown': row.get('drawdown'),
                'ppa_corr': ppa_corr,
                'prod_corr': prod_corr,
                'alpha_type': alpha_type or "SKIP",
                'target_name': target_name or "anonymous",
                'status': row.get('status', ''),
                'payload': row
            }

        workers = int(get_setting("corr_workers", "5"))
        
        auto_rename_enabled = params.get("auto_rename")
        if auto_rename_enabled is None:
            auto_rename_enabled = get_setting("auto_rename", "1") == "1"
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(analyze_single_alpha, row): row for row in eligible_alphas}
            for future in concurrent.futures.as_completed(futures):
                runner.check_paused(job_id)
                completed += 1
                row = futures[future]
                alpha_id = row['alpha_id']
                try:
                    res = future.result()
                    if res:
                        pct = int((completed / total_eligible) * 100)
                        msg = f"[{completed}/{total_eligible}] {alpha_id} | Sharpe: {res['sharpe']:.2f}, PPA: {res['ppa_corr']:.2f}, Prod: {res['prod_corr']:.2f} -> {res['alpha_type']}"
                        logger.info(msg)
                        
                        db_status = res["status"]
                        if auto_rename_enabled and res["target_name"] and res["alpha_type"] != "SKIP" and db_status != 'RENAMED':
                            try:
                                logger.info(f"Auto-renaming remote alpha {alpha_id} to '{res['target_name']}'...")
                                from consultant_core.machine_lib import set_alpha_properties
                                set_alpha_properties(session, alpha_id, name=res["target_name"])
                                db_status = 'RENAMED'
                                msg += " (Auto Renamed)"
                            except Exception as re_err:
                                logger.error(f"Auto-rename failed for {alpha_id}: {re_err}")
                        
                        update_job(job_id, progress_current=completed, progress_total=total_eligible, message=msg)
                        
                        # 入库
                        upsert_alpha({
                            "alpha_id": res["alpha_id"],
                            "alpha_type": res["alpha_type"],
                            "name": res["target_name"] if db_status == 'RENAMED' else res["name"],
                            "region": res["region"],
                            "universe": res["universe"],
                            "sharpe": res["sharpe"],
                            "fitness": res["fitness"],
                            "prod_corr": res["prod_corr"],
                            "ppa_corr": res["ppa_corr"],
                            "margin": res.get("margin"),
                            "returns": res.get("returns"),
                            "drawdown": res.get("drawdown"),
                            "status": db_status,
                            "source": f"corr_check_{job_id}",
                            "payload": {
                                "target_name": res["target_name"],
                                "raw_payload": res["payload"]
                            }
                        })
                        
                        if res["target_name"]:
                            results.append(res)
                            
                except Exception as e:
                    logger.error(f"Error checking alpha {alpha_id}: {e}")
                    
        # 结束处理
        msg = f"Correlation analysis completed. Found {len(results)} qualifying candidates (PPA/RA/ATOM)."
        update_job(job_id, message=msg, progress_current=100, progress_total=100)
        add_job_event(job_id, "info", msg, {"qualifying_count": len(results)})
        
    finally:
        session.close()
        try:
            import gc
            # 必须使用 globals() 或 locals() 检查
            locs = locals()
            if 'ppa_rets' in locs:
                del ppa_rets
            if 'all_rets' in locs:
                del all_rets
            if 'ppa_ids' in locs:
                del ppa_ids
            if 'all_ids' in locs:
                del all_ids
            gc.collect()
            logger.info("Memory cleaned up after correlation job.")
        except Exception as e:
            logger.error(f"Failed to clean up memory in correlation job: {e}")


def rename_alpha_remote(alpha_id: str, target_name: str) -> None:
    """远程调用 WorldQuant Brain API 对 Alpha 进行重命名修改"""
    from consultant_core.machine_lib import set_alpha_properties
    
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    if not username or not password:
        raise ValueError("Missing WorldQuant credentials in Settings.")
        
    s = login_with_credentials(username, password)
    try:
        logger.info(f"Renaming remote alpha {alpha_id} to '{target_name}'...")
        set_alpha_properties(s, alpha_id, name=target_name)
        logger.info("Remote rename succeeded.")
        
        # 更新本地数据库状态
        with connect() as conn:
            conn.execute(
                "UPDATE alpha_records SET name = ?, status = 'RENAMED', updated_at = datetime('now') WHERE alpha_id = ?",
                (target_name, alpha_id)
            )
    finally:
        s.close()


def run_inline_correlation_check(
    session: Any,
    alpha_ids: list[str],
    job_id: int,
    stage: str = "FO",
) -> None:
    """在回测任务中穿插调用的本地相关性检测与类型评估逻辑（仅 Prod 相关性，无 PPA）。

    Args:
        session:    已登录的 WQ 会话
        alpha_ids:  待检测的 Alpha ID 列表
        job_id:     当前 Job ID（用于写入事件日志）
        stage:      当前所处阶段 ("FO" | "SO" | "TH")，用于读取对应的阈值配置
    """
    if not alpha_ids:
        return

    stage_prefix = stage.lower()
    logger.info(f"[{stage}] Running inline correlation check for {len(alpha_ids)} alphas...")

    # 更新本地相关性数据缓存
    try:
        download_correlation_data(session, flag_increment=True)
    except Exception as e:
        logger.error(f"[{stage}] Failed to update correlation cache: {e}")

    # 只加载 Prod 相关性矩阵（不再使用 PPA）
    all_ids, all_rets = load_correlation_data(tag=None)

    region = get_setting("region", "USA")
    # 读取该阶段对应的配置阈值
    corr_sharpe_th = float(get_setting(f"{stage_prefix}_corr_sharpe_th", "1.0"))
    max_prod_corr  = float(get_setting(f"{stage_prefix}_max_prod_corr",  "0.7"))

    skipped_count = 0
    passed_count  = 0

    for aid in alpha_ids:
        try:
            target_pnl_df = get_alpha_pnl(session, aid)
            if target_pnl_df.empty or aid not in target_pnl_df.columns:
                continue

            target_pnl_series = target_pnl_df.set_index('Date')[aid]
            alpha_rets_series  = target_pnl_series - target_pnl_series.ffill().shift(1)
            prod_corr = calc_self_corr_local(alpha_rets_series, all_rets, all_ids, region)

            # 从数据库读取 Sharpe / Fitness
            with connect() as conn:
                row = conn.execute(
                    "SELECT sharpe, fitness FROM alpha_records WHERE alpha_id = ?", (aid,)
                ).fetchone()

            if row:
                sharpe  = float(row["sharpe"]  or 0)
                fitness = float(row["fitness"] or 0)

                # 分类判定：prod_corr 超限 或 sharpe 不达标 → SKIP；否则 → RA
                if sharpe < corr_sharpe_th or prod_corr > max_prod_corr:
                    alpha_type  = "SKIP"
                    target_name = "anonymous"
                    skipped_count += 1
                else:
                    alpha_type  = "RA"
                    target_name = f"RA_{prod_corr:.2f}_{fitness:.2f}"
                    passed_count += 1

                with connect() as conn:
                    conn.execute(
                        """
                        UPDATE alpha_records
                        SET prod_corr = ?, alpha_type = ?, name = ?, updated_at = datetime('now')
                        WHERE alpha_id = ?
                        """,
                        (prod_corr, alpha_type, target_name, aid)
                    )
            else:
                # 仅更新相关性字段，不修改 alpha_type
                alpha_type = "N/A"
                with connect() as conn:
                    conn.execute(
                        "UPDATE alpha_records SET prod_corr = ?, updated_at = datetime('now') WHERE alpha_id = ?",
                        (prod_corr, aid)
                    )

            logger.info(f"[{stage}] Inline Corr {aid}: Prod={prod_corr:.4f}, type={alpha_type}")

        except Exception as ex:
            logger.error(f"[{stage}] Failed to check inline correlation for {aid}: {ex}")

    add_job_event(
        job_id, "info",
        f"[{stage}] Inline correlation done: {passed_count} passed (RA), {skipped_count} skipped (SKIP)."
    )
