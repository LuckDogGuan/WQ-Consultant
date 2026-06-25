import os
import sys
import json
import time
import pickle
import logging
import argparse
import traceback
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Optional, Tuple, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BRAIN_API_URL = os.environ.get("BRAIN_API_URL", "https://api.worldquantbrain.com")

def sign_in():
    """
    Authenticate with WQ Brain API.
    Loads credentials dynamically from user_config.json or user_info.txt.
    """
    username, password = None, None
    config_file = r"D:\SoftWare\AiWorkFlow\user_config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            credentials = config_data.get("credentials", {})
            username = credentials.get("email")
            password = credentials.get("password")
            if username and password:
                logger.info(f"Loaded credentials from {config_file}")
        except Exception as e:
            logger.error(f"Error loading credentials from user_config.json: {e}")

    if not username or not password:
        txt_file = 'user_info.txt'
        try:
            with open(txt_file, 'r') as f:
                data = f.read().strip().split('\n')
                data = {line.split(': ')[0]: line.split(': ')[1] for line in data}
            username = data['username'].strip("'\" ")
            password = data['password'].strip("'\" ")
            logger.info(f"Loaded credentials from {txt_file}")
        except FileNotFoundError:
            logger.error(f"Credentials not found. Please setup {config_file} or create {txt_file}.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading credentials from user_info.txt: {e}")
            sys.exit(1)

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    s = requests.Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.auth = (username, password)
    
    max_try = 3
    retry = 0
    while retry < max_try:
        try:
            response = s.post(f'{BRAIN_API_URL}/authentication')
            if response.status_code in [200, 201]:
                logger.info("Login successful")
                return s
        except Exception as e:
            logger.error(f"Login failed: {e}")
            time.sleep(5)
        retry += 1
    return None

def save_obj(obj: object, name: str) -> None:
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name: str) -> object:
    try:
        with open(name + '.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Failed to load object {name}: {e}")
        return None

def get_submit_alphas(session, start_date: str, end_date: str, sharpe_th: float, 
                      fitness_th: float, region: str, alpha_num: int) -> List[Dict]:
    """
    Get unsubmitted SuperAlphas that meet the criteria.
    """
    output = []
    count = 0
    # Pagination loop
    for i in range(0, alpha_num, 100):
        logger.info(f"Processing offset: {i}")
        # Format dates assuming year is 2026 as per WQ Brain forum context or local year
        curr_year = datetime.now().year
        base_url = f"{BRAIN_API_URL}/users/self/alphas?limit=100&offset={i}&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E={curr_year}-{start_date}T00:00:00-05:00&dateCreated%3C={curr_year}-{end_date}T00:00:00-05:00&is.fitness%3E={fitness_th}&is.sharpe%3E={sharpe_th}&settings.region={region}&order=-is.sharpe&hidden=false&type=SUPER"
        
        try:
            response = session.get(base_url)
            if response.status_code == 200:
                alpha_list = response.json().get("results", [])
                if not alpha_list:
                    break
                for alpha in alpha_list:
                    alpha_id = alpha.get("id")
                    name = alpha.get("name")
                    dateCreated = alpha.get("dateCreated")
                    sharpe = alpha.get("is", {}).get("sharpe")
                    fitness = alpha.get("is", {}).get("fitness")
                    turnover = alpha.get("is", {}).get("turnover")
                    margin = alpha.get("is", {}).get("margin")
                    longCount = alpha.get("is", {}).get("longCount")
                    shortCount = alpha.get("is", {}).get("shortCount")
                    decay = alpha.get("settings", {}).get("decay")
                    alpha_type = alpha.get("type", "REGULAR")
                    neutralization = alpha.get("settings", {}).get("neutralization", "NONE")
                    
                    neutralization_map = {
                        "SUBINDUSTRY": "Subindustry",
                        "STATISTICAL": "Statistical",
                        "SLOW": "Slow Factors",
                        "SLOW_AND_FAST": "Slow + Fast Factors",
                        "SECTOR": "Sector",
                        "NONE": "None",
                        "MARKET": "Market",
                        "INDUSTRY": "Industry",
                        "FAST": "Fast Factors",
                        "CROWDING": "Crowding Factors",
                        "COUNTRY": "Country/Region",
                        "SUPER_NEUTRAL": "Super Alpha Neutralization"
                    }
                    neutralization_name = neutralization_map.get(neutralization, neutralization)
                    count += 1
                    
                    # Verify checks
                    checks = alpha.get("is", {}).get("checks", [])
                    checks_df = pd.DataFrame(checks)
                    check_status = "Check FAIL"
                    if not checks_df.empty and "result" in checks_df.columns:
                        if not any(checks_df["result"].eq("FAIL")) and ((longCount or 0) + (shortCount or 0) > 100):
                            check_status = "Check OK"
                    
                    rec = {
                        "alpha_id": alpha_id,
                        "alpha_type": alpha_type,
                        "check_status": check_status,
                        "sharpe": sharpe,
                        "turnover": f"{turnover:.2%}" if turnover is not None else None,
                        "fitness": fitness,
                        "margin": f"{margin * 10000:.2f}‱" if margin is not None else None,
                        "longCount": longCount,
                        "shortCount": shortCount,
                        "dateCreated": dateCreated,
                        "decay": decay,
                        "neutralization": neutralization,
                        "neutralization_name": neutralization_name
                    }
                    if check_status == "Check OK":
                        output.append(rec)
            else:
                logger.error(f"Request failed, status code: {response.status_code}")
                logger.error(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Error handling offset {i}: {e}")
            
    logger.info(f"Total processed SuperAlphas: {count}")
    logger.info(f"Matching condition SuperAlphas: {len(output)}")
    return output

def wait_get(session, url: str, max_retries: int = 10) -> Optional[requests.Response]:
    retries = 0
    while retries < max_retries:
        try:
            response = session.get(url)
            if response.status_code == 429 or "Retry-After" in response.headers:
                retry_after = float(response.headers.get("Retry-After", 5))
                time.sleep(retry_after)
                continue
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            time.sleep(2 ** retries)
            retries += 1
    return None

def _get_alpha_pnl(session, alpha_id: str) -> pd.DataFrame:
    """Get PnL data for a specific Alpha ID"""
    pnl = wait_get(session, f"{BRAIN_API_URL}/alphas/{alpha_id}/recordsets/pnl")
    if pnl is None or pnl.status_code != 200:
        return pd.DataFrame()
    try:
        pnl_data = pnl.json()
        df = pd.DataFrame(pnl_data['records'],
                          columns=[item['name'] for item in pnl_data['schema']['properties']])
        df = df.rename(columns={'date': 'Date', 'pnl': alpha_id})
        return df[['Date', alpha_id]]
    except Exception as e:
        logger.error(f"Error parsing PnL data for {alpha_id}: {e}")
        return pd.DataFrame()

def get_alpha_pnls(session, alphas: List[Dict], alpha_pnls: Optional[pd.DataFrame] = None,
                   alpha_ids: Optional[Dict[str, List[str]]] = None) -> Tuple[Dict[str, List[str]], pd.DataFrame]:
    """Get PnL data for multiple alphas"""
    if alpha_ids is None:
        alpha_ids = defaultdict(list)
    if alpha_pnls is None:
        alpha_pnls = pd.DataFrame()
        
    new_alphas = [item for item in alphas if item['id'] not in alpha_pnls.columns]
    if not new_alphas:
        return alpha_ids, alpha_pnls
        
    for item_alpha in new_alphas:
        region = item_alpha.get('settings', {}).get('region', 'GLOBAL')
        alpha_ids[region].append(item_alpha['id'])
        
    def fetch_pnl(alpha_id):
        return _get_alpha_pnl(session, alpha_id).set_index('Date')
        
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_pnl, [item['id'] for item in new_alphas]))
        
    valid_results = [df for df in results if not df.empty]
    if valid_results:
        for df in valid_results:
            df.columns = df.columns.astype(str)
        alpha_pnls = pd.concat([alpha_pnls] + valid_results, axis=1)
        alpha_pnls.sort_index(inplace=True)
        
    return alpha_ids, alpha_pnls

def get_os_alphas(session, limit: int = 100, get_first: bool = False) -> List[Dict]:
    """Get alphas in the Out-of-Sample (OS) stage"""
    fetched_alphas = []
    offset = 0
    total_alphas = 100
    while len(fetched_alphas) < total_alphas:
        url = f"{BRAIN_API_URL}/users/self/alphas?stage=OS&limit={limit}&offset={offset}&order=-dateSubmitted"
        res = wait_get(session, url)
        if res is None or res.status_code != 200:
            break
        try:
            res_data = res.json()
            if offset == 0:
                total_alphas = res_data.get('count', 100)
            alphas = res_data.get("results", [])
            fetched_alphas.extend(alphas)
            if len(alphas) < limit or get_first:
                break
            offset += limit
        except Exception as e:
            logger.error(f"Error parsing OS Alpha data: {e}")
            break
    return fetched_alphas[:total_alphas]

def download_data(session, data_path: Path, flag_increment: bool = True) -> Tuple[
    Optional[Dict], Optional[pd.DataFrame]]:
    """Download and cache base OS data"""
    os_alpha_ids = None
    os_alpha_pnls = None
    exist_alpha = []
    
    if flag_increment:
        try:
            os_alpha_ids = load_obj(str(data_path / 'os_alpha_ids'))
            os_alpha_pnls = load_obj(str(data_path / 'os_alpha_pnls'))
            if os_alpha_ids is not None:
                exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
        except Exception as e:
            logger.error(f"Error loading cached data: {e}")
            
    if os_alpha_ids is None:
        alphas = get_os_alphas(session, limit=100, get_first=False)
    else:
        alphas = get_os_alphas(session, limit=30, get_first=True)
        
    alphas = [item for item in alphas if item['id'] not in exist_alpha]
    os_alpha_ids, os_alpha_pnls = get_alpha_pnls(session, alphas,
                                                 alpha_pnls=os_alpha_pnls,
                                                 alpha_ids=os_alpha_ids)
    if os_alpha_ids:
        save_obj(os_alpha_ids, str(data_path / 'os_alpha_ids'))
    if os_alpha_pnls is not None and not os_alpha_pnls.empty:
        save_obj(os_alpha_pnls, str(data_path / 'os_alpha_pnls'))
        
    logger.info(f"New OS alphas downloaded: {len(alphas)}, Current total OS alphas cached: {os_alpha_pnls.shape[1] if os_alpha_pnls is not None else 0}")
    return os_alpha_ids, os_alpha_pnls

def load_data(session, data_path: Path) -> Tuple[Optional[Dict], Optional[pd.DataFrame]]:
    """Load cached OS PnL data and compute returns"""
    try:
        os_alpha_ids = load_obj(str(data_path / 'os_alpha_ids'))
        os_alpha_pnls = load_obj(str(data_path / 'os_alpha_pnls'))
    except Exception as e:
        logger.error(f"Error loading OS data: {e}")
        return None, None
        
    if os_alpha_ids is None or os_alpha_pnls is None:
        return None, None
        
    exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
    # Filter only existing column indices in case of discrepancy
    common_alphas = [a for a in exist_alpha if a in os_alpha_pnls.columns]
    os_alpha_pnls = os_alpha_pnls[common_alphas]
    
    # Calculate returns
    os_alpha_rets = os_alpha_pnls - os_alpha_pnls.ffill().shift(1)
    
    # Keep only the last 4 years of data
    if not os_alpha_rets.empty:
        cutoff_date = pd.to_datetime(os_alpha_rets.index).max() - pd.DateOffset(years=4)
        os_alpha_rets = os_alpha_rets[pd.to_datetime(os_alpha_rets.index) > cutoff_date]
        
    return os_alpha_ids, os_alpha_rets

def calc_self_corr(session, alpha_id: str, os_alpha_rets: pd.DataFrame,
                   os_alpha_ids: Dict[str, List[str]], alpha_result: Optional[Dict] = None) -> float:
    """Calculate maximum correlation with current OS alphas in the same region"""
    if alpha_result is None:
        alpha_result_res = wait_get(session, f"{BRAIN_API_URL}/alphas/{alpha_id}")
        if alpha_result_res is None or alpha_result_res.status_code != 200:
            return 1.0  # Fallback to high correlation
        try:
            alpha_result = alpha_result_res.json()
        except Exception as e:
            logger.error(f"Error parsing alpha details: {e}")
            return 1.0
            
    alpha_pnl = _get_alpha_pnl(session, alpha_id)
    if alpha_pnl.empty:
        return 1.0
        
    try:
        alpha_pnl = alpha_pnl.set_index('Date')[alpha_id]
        alpha_rets = alpha_pnl - alpha_pnl.ffill().shift(1)
        
        # Keep only the last 4 years
        cutoff_date = pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)
        if not alpha_rets.empty:
            alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index) > cutoff_date]
            
        region = alpha_result.get('settings', {}).get('region', 'GLOBAL')
        region_os_alphas = os_alpha_ids.get(region, [])
        if not region_os_alphas:
            logger.warning(f"No OS alphas found for region {region}")
            return 1.0
            
        available_alphas = [a for a in region_os_alphas if a in os_alpha_rets.columns]
        if not available_alphas:
            logger.warning(f"No matching OS alpha return columns found for region {region}")
            return 1.0
            
        corr_values = os_alpha_rets[available_alphas].corrwith(alpha_rets)
        if corr_values.empty:
            return 1.0
            
        max_corr = corr_values.max()
        return 1.0 if np.isnan(max_corr) else max_corr
    except Exception as e:
        logger.error(f"Error calculating self-correlation for {alpha_id}: {e}")
        return 1.0

def calculate_self_correlation(session, data_path: Path, alpha_df: pd.DataFrame, 
                               max_workers: int = 3, threshold: float = 0.3) -> pd.DataFrame:
    """Calculate self-correlation for a dataframe of alphas"""
    logger.info("Downloading OS baseline data...")
    download_data(session, data_path, flag_increment=True)
    
    logger.info("Loading OS baseline data...")
    os_alpha_ids, os_alpha_rets = load_data(session, data_path)
    
    if os_alpha_ids is None or os_alpha_rets is None or os_alpha_rets.empty:
        logger.warning("Could not load baseline data, skipping self-correlation calculation.")
        alpha_df['self_correlation'] = 1.0
        alpha_df['low_self_corr'] = False
        return alpha_df
        
    logger.info(f"Calculating self-correlation for {len(alpha_df)} alphas...")
    self_corr_results = []
    
    def process_alpha(row):
        alpha_id = row['alpha_id']
        try:
            corr_value = calc_self_corr(
                session=session,
                alpha_id=alpha_id,
                os_alpha_rets=os_alpha_rets,
                os_alpha_ids=os_alpha_ids
            )
            return {
                "alpha_id": alpha_id,
                "self_correlation": corr_value
            }
        except Exception as e:
            logger.error(f"Failed self-correlation for {alpha_id}: {e}")
            return {
                "alpha_id": alpha_id,
                "self_correlation": 1.0
            }
            
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_alpha, row) for _, row in alpha_df.iterrows()]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Calculating self-correlation"):
            self_corr_results.append(future.result())
            
    self_corr_df = pd.DataFrame(self_corr_results)
    result_df = alpha_df.merge(self_corr_df, on='alpha_id', how='left')
    result_df['low_self_corr'] = result_df['self_correlation'] < threshold
    return result_df

def set_alpha_properties(session, alpha_id: str, name: Optional[str] = None, color: Optional[str] = None) -> None:
    """Set alpha tags and properties on WQ Brain"""
    params = {}
    if name:
        params["name"] = name
    if color:
        params["color"] = color
    if not params:
        return
    try:
        response = session.patch(f"{BRAIN_API_URL}/alphas/{alpha_id}", json=params)
        if response.status_code == 200:
            logger.info(f"Successfully updated alpha {alpha_id}")
        else:
            logger.error(f"Failed to update alpha {alpha_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception updating alpha {alpha_id}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download and calculate self-correlation for WQ Brain SuperAlphas.")
    parser.add_argument("--start_date", type=str, default="01-30", help="Start date (MM-DD format).")
    parser.add_argument("--end_date", type=str, default="02-01", help="End date (MM-DD format).")
    parser.add_argument("--sharpe_th", type=float, default=5.0, help="Sharpe threshold.")
    parser.add_argument("--fitness_th", type=float, default=5.0, help="Fitness threshold.")
    parser.add_argument("--region", type=str, default="IND", help="Region (e.g. USA, EUR, IND, CHN).")
    parser.add_argument("--alpha_num", type=int, default=2000, help="Max alphas to process.")
    parser.add_argument("--corr_threshold", type=float, default=0.3, help="Self-correlation threshold.")
    parser.add_argument("--max_workers", type=int, default=3, help="Concurrent workers for correlation.")
    parser.add_argument("--data_path", type=str, default=".", help="Directory to cache OS data.")
    
    args = parser.parse_args()
    
    session = sign_in()
    if not session:
        logger.error("Authentication failed.")
        sys.exit(1)
        
    data_path = Path(args.data_path)
    data_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Querying SuperAlphas from {args.start_date} to {args.end_date} for region {args.region}...")
    alpha_data = get_submit_alphas(
        session=session,
        start_date=args.start_date,
        end_date=args.end_date,
        sharpe_th=args.sharpe_th,
        fitness_th=args.fitness_th,
        region=args.region,
        alpha_num=args.alpha_num
    )
    
    if not alpha_data:
        logger.info("No matching SuperAlphas found.")
        return
        
    alpha_df = pd.DataFrame(alpha_data)
    result_df = calculate_self_correlation(
        session=session,
        data_path=data_path,
        alpha_df=alpha_df,
        max_workers=args.max_workers,
        threshold=args.corr_threshold
    )
    
    # Mark/label low self correlation alphas
    low_corr_df = result_df[result_df['low_self_corr']]
    logger.info(f"Found {len(low_corr_df)} low self-correlation alphas (< {args.corr_threshold})")
    
    for _, row in low_corr_df.iterrows():
        alpha_id = row['alpha_id']
        corr_val = row['self_correlation']
        new_name = f"LOW_CORR_{corr_val:.4f}"
        set_alpha_properties(session, alpha_id, name=new_name, color="GREEN")
        
    # Output results
    output_file = data_path / f"Superalpha_results_{args.start_date}_{args.region}.xlsx"
    result_df = result_df.sort_values(by='self_correlation', ascending=True)
    
    if not result_df.empty:
        result_df['rank'] = result_df['self_correlation'].rank(method='min')
        
    output_columns = [
        "rank", "alpha_id", "alpha_type", "check_status", "sharpe", "turnover",
        "fitness", "margin", "dateCreated", "longCount", "shortCount", "decay",
        "neutralization_name", "self_correlation", "low_self_corr"
    ]
    available_cols = [c for c in output_columns if c in result_df.columns]
    result_df = result_df[available_cols]
    
    result_df.to_excel(output_file, sheet_name='Low Correlation SuperAlphas', index=False)
    logger.info(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()
