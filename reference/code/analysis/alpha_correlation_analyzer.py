import sys
import os
import time
import json
import pickle
import logging
import pandas as pd
import numpy as np
from pathlib import Path
import concurrent.futures
from collections import defaultdict
from datetime import datetime, timedelta

# Add consultant_core to sys.path
cwd = Path(__file__).resolve().parent
project_root = cwd.parent
sys.path.insert(0, str(project_root / "src"))

from consultant_core.machine_lib import login, get_alphas_full, set_alpha_properties

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    data_path = project_root / 'data_catalog' / 'correlation_data'

Config.data_path.mkdir(exist_ok=True, parents=True)

def wait_get(sess, url: str, max_retries: int = 10):
    retries = 0
    while retries < max_retries:
        while True:
            try:
                simulation_progress = sess.get(url, timeout=30)
            except Exception as e:
                logging.error(f"Request failed: {url} -> {e}")
                time.sleep(2 ** retries)
                break # Break inner loop to retry
            
            retry_after = simulation_progress.headers.get("Retry-After", 0)
            if retry_after == 0 or retry_after is None:
                if simulation_progress.status_code < 400:
                    return simulation_progress
                break
            time.sleep(float(retry_after))
        retries += 1
        time.sleep(2 ** retries)
    return None

def _get_alpha_pnl(sess, alpha_id: str) -> pd.DataFrame:
    resp = wait_get(sess, f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl")
    if not resp: return pd.DataFrame()
    pnl = resp.json()
    if 'records' not in pnl or 'schema' not in pnl:
        return pd.DataFrame()
    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])
    if 'date' in df.columns and 'pnl' in df.columns:
        df = df.rename(columns={'date': 'Date', 'pnl': alpha_id})
        df = df[['Date', alpha_id]]
    return df

def get_alpha_pnls(sess, alphas: list, alpha_pnls=None, alpha_ids=None):
    if alpha_ids is None:
        alpha_ids = defaultdict(list)
    if alpha_pnls is None:
        alpha_pnls = pd.DataFrame()
    
    new_alphas = [item for item in alphas if item['id'] not in alpha_pnls.columns]
    if not new_alphas:
        return alpha_ids, alpha_pnls
    
    for item_alpha in new_alphas:
        region = item_alpha.get('settings', {}).get('region', 'USA')
        alpha_ids[region].append(item_alpha['id'])
        
    def fetch_pnl_func(alpha_id):
        df = _get_alpha_pnl(sess, alpha_id)
        if not df.empty:
            return df.set_index('Date')
        return pd.DataFrame()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_pnl_func, [item['id'] for item in new_alphas]))
    
    valid_results = [res for res in results if not res.empty]
    if valid_results:
        alpha_pnls = pd.concat([alpha_pnls] + valid_results, axis=1)
        alpha_pnls.sort_index(inplace=True)
        
    return alpha_ids, alpha_pnls

def get_os_alphas(sess, limit: int = 100, get_first: bool = False):
    fetched_alphas = []
    offset = 0
    total_alphas = 100
    while len(fetched_alphas) < total_alphas:
        logging.info(f"Fetching OS alphas from offset {offset} to {offset + limit}")
        url = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}&order=-dateSubmitted"
        res = wait_get(sess, url)
        if not res: break
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

def save_obj(obj, name):
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)

def download_data(sess, flag_increment=True):
    try:
        if flag_increment:
            os_alpha_ids = load_obj(str(Config.data_path / 'os_alpha_ids'))
            os_alpha_pnls = load_obj(str(Config.data_path / 'os_alpha_pnls'))
            ppac_alpha_ids = load_obj(str(Config.data_path / 'ppac_alpha_ids'))
            exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
        else:
            raise FileNotFoundError
    except Exception as e:
        logging.info("Existing data not found or full download requested. Starting fresh.")
        os_alpha_ids = None
        os_alpha_pnls = None
        exist_alpha = []
        ppac_alpha_ids = []
        
    if os_alpha_ids is None:
        alphas = get_os_alphas(sess, limit=100, get_first=False)
    else:
        alphas = get_os_alphas(sess, limit=30, get_first=True)
    
    alphas = [item for item in alphas if item['id'] not in exist_alpha]
    if alphas:
        ppac_alpha_ids += [
            item['id'] for item in alphas 
            if any(c.get('name') == 'Power Pool Alpha' for c in item.get('classifications', []))
        ]
                
        os_alpha_ids, os_alpha_pnls = get_alpha_pnls(sess, alphas, alpha_pnls=os_alpha_pnls, alpha_ids=os_alpha_ids)
        save_obj(os_alpha_ids, str(Config.data_path / 'os_alpha_ids'))
        save_obj(os_alpha_pnls, str(Config.data_path / 'os_alpha_pnls'))
        save_obj(ppac_alpha_ids, str(Config.data_path / 'ppac_alpha_ids'))
        
    logging.info(f'Downloaded {len(alphas)} new alphas. Total: {os_alpha_pnls.shape[1] if os_alpha_pnls is not None else 0}')

def load_data(tag=None):
    os_alpha_ids = load_obj(str(Config.data_path / 'os_alpha_ids'))
    os_alpha_pnls = load_obj(str(Config.data_path / 'os_alpha_pnls'))
    ppac_alpha_ids = load_obj(str(Config.data_path / 'ppac_alpha_ids'))
    
    import copy
    filtered_ids = copy.deepcopy(os_alpha_ids)
    
    if tag == 'PPAC':
        for item in filtered_ids:
            filtered_ids[item] = [alpha for alpha in filtered_ids[item] if alpha in ppac_alpha_ids]
    elif tag == 'SelfCorr':
        for item in filtered_ids:
            filtered_ids[item] = [alpha for alpha in filtered_ids[item] if alpha not in ppac_alpha_ids]
            
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
            os_alpha_rets = os_alpha_rets[os_alpha_rets.index > max_date - pd.DateOffset(years=4)]
            
    return filtered_ids, os_alpha_rets

def calc_self_corr_local(alpha_rets_series: pd.Series, os_alpha_rets: pd.DataFrame, os_alpha_ids: dict, region: str) -> float:
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

def process_unsubmitted_alphas(sess, limit=None):
    logging.info("Updating local OS alphas cache...")
    download_data(sess, flag_increment=True)
    
    logging.info("Loading cached PnL returns...")
    ppa_ids, ppa_rets = load_data(tag='PPAC')
    all_ids, all_rets = load_data(tag=None)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=4)
    
    logging.info(f"Fetching unsubmitted alphas (from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})...")
    alphas_df = get_alphas_full(
        start_date=start_date,
        end_date=end_date,
        sharpe_th=-10.0, # Fetch everything initially to do strict filtering in-memory
        region="USA", 
        usage="submit", 
        session=sess, 
        order="-dateCreated",
        limit=limit
    )
    
    if alphas_df.empty:
        logging.info("No unsubmitted alphas found.")
        return
        
    # Pandas pre-filtering
    total_fetched = len(alphas_df)
    
    # 1. sharpe >= 1 and fitness >= 0.7
    valid_metrics = (alphas_df['sharpe'] >= 1.0) & (alphas_df['fitness'] >= 0.7)
    
    # 2. Drop IS_FAIL unless sharpe > 2.0
    is_fail = alphas_df['status'].isin(['IS_FAIL', 'ERROR'])
    valid_status = ~(is_fail & (alphas_df['sharpe'] <= 2.0))
    
    alphas_df = alphas_df[valid_metrics & valid_status]
    eligible_alphas = alphas_df.to_dict('records')
    total_eligible = len(eligible_alphas)
    
    logging.info(f"Filtered {total_fetched} alphas down to {total_eligible} eligible alphas.")
    if total_eligible == 0:
        return
        
    def analyze_single_alpha(row):
        alpha_id = row['alpha_id']
        region = row['region']
        sharpe = float(row['sharpe'])
        
        # We assume IS_LADDER is passed if status is UNSUBMITTED or if it was kept as a high Sharpe exception
        is_ladder_pass = row['status'] not in ['IS_FAIL', 'ERROR']
        
        # 1. Fetch PnL for correlation
        target_pnl_df = _get_alpha_pnl(sess, alpha_id)
        if target_pnl_df.empty or alpha_id not in target_pnl_df.columns:
            return None # Failed to get PnL
            
        target_pnl_series = target_pnl_df.set_index('Date')[alpha_id]
        alpha_rets_series = target_pnl_series - target_pnl_series.ffill().shift(1)
        
        ppa_corr = calc_self_corr_local(alpha_rets_series, ppa_rets, ppa_ids, region)
        prod_corr = calc_self_corr_local(alpha_rets_series, all_rets, all_ids, region)
        
        # 2. Fetch yearly-stats to calculate L2Y Sharpe
        l2y_sharpe = sharpe
        stats_resp = sess.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats")
        if stats_resp.status_code == 200 and stats_resp.text.strip():
            stats = stats_resp.json().get('records', [])
            schema = stats_resp.json().get('schema', {}).get('properties', [])
            cols = [p['name'] for p in schema]
            if stats and 'year' in cols and 'sharpe' in cols:
                stats_df = pd.DataFrame(stats, columns=cols)
                stats_df['year'] = pd.to_numeric(stats_df['year'])
                stats_df['sharpe'] = pd.to_numeric(stats_df['sharpe'])
                stats_df = stats_df.sort_values('year', ascending=False)
                recent_2_years = stats_df.head(2)
                l2y_sharpe = float(recent_2_years['sharpe'].mean())
        
        alpha_type = None
        target_name = None
        
        if sharpe > 1.0 and ppa_corr < 0.5:
            alpha_type = "PPA"
            target_name = f"PPA_{ppa_corr:.2f}"
        elif l2y_sharpe > 2.38 and prod_corr < 0.7:
            alpha_type = "ATOM"
            target_name = f"ATOM_{prod_corr:.2f}"
        elif sharpe > 1.58 and prod_corr < 0.7 and is_ladder_pass:
            alpha_type = "RA"
            target_name = f"RA_{prod_corr:.2f}"
            
        return {
            'alpha_id': alpha_id,
            'sharpe': sharpe,
            'l2y_sharpe': l2y_sharpe,
            'ppa_corr': ppa_corr,
            'prod_corr': prod_corr,
            'alpha_type': alpha_type,
            'target_name': target_name
        }

    logging.info("Starting multi-threaded analysis...")
    results_to_submit = []
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(analyze_single_alpha, row): row for row in eligible_alphas}
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            row = futures[future]
            alpha_id = row['alpha_id']
            try:
                res = future.result()
                if res:
                    logging.info(f"[{completed}/{total_eligible}] {alpha_id} | Sharpe: {res['sharpe']:.2f}, L2Y: {res['l2y_sharpe']:.2f}, PPA: {res['ppa_corr']:.4f}, Prod: {res['prod_corr']:.4f} -> {res['target_name'] or 'SKIP'}")
                    if res['target_name']:
                        results_to_submit.append(res)
                else:
                    logging.info(f"[{completed}/{total_eligible}] {alpha_id} | Failed to retrieve PnL or analyze.")
            except Exception as e:
                logging.error(f"[{completed}/{total_eligible}] {alpha_id} | Exception during analysis: {e}")

    if results_to_submit:
        logging.info(f"Found {len(results_to_submit)} alphas to submit. Submitting sequentially...")
        for res in results_to_submit:
            logging.info(f"Renaming {res['alpha_id']} to {res['target_name']}")
            set_alpha_properties(sess, res['alpha_id'], name=res['target_name'])
        logging.info("Done submitting all alphas.")
    else:
        logging.info("No alphas qualified for renaming.")

if __name__ == "__main__":
    sess = login()
    process_unsubmitted_alphas(sess, limit=None)
