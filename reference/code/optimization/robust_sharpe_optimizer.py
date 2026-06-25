import sys
import time
from datetime import datetime
import pandas as pd
import os
import threading
import concurrent.futures
import requests
from requests.exceptions import RequestException
import json
import argparse
import queue
import re

brain_api_url = os.environ.get("BRAIN_API_URL", "https://api.worldquantbrain.com")

UNIVERSE_DICTS = {
    "USA": ["TOP3000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500"],
    "GLB": ["TOP3000", "MINVOL1M","TOPDIV3000"],
    "EUR": ["TOP2500", "TOP1200", "TOP800", "TOP400", "ILLIQUID_MINVOL1M"],
    "ASI": ["MINVOL1M", "ILLIQUID_MINVOL1M"],
    "CHN": ["TOP2000U"],
    "AMR": ["TOP600"],
    "IND": ["TOP500"]
}

NEUT_DICTS = {
    'USA': ['REVERSION_AND_MOMENTUM','STATISTICAL','CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'GLB': ['REVERSION_AND_MOMENTUM','STATISTICAL','CROWDING', 'FAST'],
    'EUR': ['REVERSION_AND_MOMENTUM','STATISTICAL','CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'ASI': ['REVERSION_AND_MOMENTUM','STATISTICAL','CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'CHN': ['REVERSION_AND_MOMENTUM','STATISTICAL','CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'KOR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'TWN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'HKG': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'JPN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'AMR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'COUNTRY'],
    'IND': ['REVERSION_AND_MOMENTUM','CROWDING', 'FAST', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY']
}

file_lock = threading.Lock()

def login():
    username, password = None, None
    
    # Try user_config.json first
    from pathlib import Path
    possible_paths = [
        Path("user_config.json"),
        Path("../user_config.json"),
        Path("../../user_config.json"),
        Path(os.path.expanduser("~")) / ".config" / "AiWorkFlow" / "user_config.json",
        Path("D:/SoftWare/AiWorkFlow/user_config.json")
    ]
    config_file = r"D:\SoftWare\AiWorkFlow\user_config.json"
    for p in possible_paths:
        if p.exists():
            config_file = str(p)
            break

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            credentials = config_data.get("credentials", {})
            username = credentials.get("email")
            password = credentials.get("password")
            if username and password:
                print(f"Loaded credentials from {config_file}")
        except Exception as e:
            print(f"Error loading credentials from user_config.json: {e}")

    # Fallback to user_info.txt
    if not username or not password:
        txt_file = 'user_info.txt'
        try:
            with open(txt_file, 'r') as f:
                data = f.read().strip().split('\n')
                data = {line.split(': ')[0]: line.split(': ')[1] for line in data}
            username = data['username'].strip("'\" ")
            password = data['password'].strip("'\" ")
            print(f"Loaded credentials from {txt_file}")
        except FileNotFoundError:
            print(f"Error: Credentials not found. Please setup {config_file} or create user_info.txt.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading user info from user_info.txt: {e}")
            sys.exit(1)

    s = requests.Session()
    s.auth = (username, password)
    try:
        response = s.post(f'{brain_api_url}/authentication')
        response.raise_for_status()
        print("Authentication successful.")
    except RequestException as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)
    return s

def set_alpha_properties(s, alpha_id, name: str = None, color: str = None, 
                         selection_desc: str = None, combo_desc: str = None, tags: list = None):
    if alpha_id is None:
        print("Alpha ID 为空，无法更新属性。")
        return False
        
    max_retries = 3
    params = {"category": None, "regular": {"description": None}}
    if color:
        params["color"] = color
    if name:
        params["name"] = name
    if tags:
        params["tags"] = tags
    if combo_desc:
        params["combo"] = {"description": combo_desc}
    if selection_desc:
        params["selection"] = {"description": selection_desc}
        
    for retry in range(max_retries):
        try:
            response = s.patch(f"{brain_api_url}/alphas/{alpha_id}", json=params)
            if 200 <= response.status_code < 300:
                print(f"成功设置 alpha_id: {alpha_id}, 标签: {tags if tags else '无'}（尝试 {retry + 1}/{max_retries}）")
                return response
            elif response.status_code == 429:
                print("429 Too Many Requests. Waiting before retry...")
                time.sleep(5)
        except Exception as e:
            print(f"请求异常: {e}，alpha_id: {alpha_id}（尝试 {retry + 1}/{max_retries}）")
        time.sleep(1)
    return None

def get_alpha_byid(s, alpha_id):
    request_timeout = 60
    while True:
        try:
            alpha = s.get(f"{brain_api_url}/alphas/{alpha_id}", timeout=request_timeout)
            if "retry-after" in alpha.headers:
                time.sleep(float(alpha.headers["Retry-After"]))
            else:
                alpha.raise_for_status()
                break
        except requests.exceptions.RequestException as e:
            print(f"请求 alpha_id={alpha_id} 接口错误: {e}. 重试...")
            time.sleep(5)
    return json.loads(alpha.content.decode('utf-8'))

def locate_details(s, alpha_id):
    metrics = get_alpha_byid(s, alpha_id)
    is_data = metrics.get("is", {})
    sharpe = is_data.get("sharpe", 0.0)
    fitness = is_data.get("fitness", 0.0)
    turnover = is_data.get("turnover", 0.0)
    margin = is_data.get("margin", 0.0)
    settings = metrics.get("settings", {})
    decay = settings.get("decay", 0)
    delay = settings.get("delay", 0)
    exp = metrics.get('regular', {}).get('code', "")
    universe = settings.get("universe", "")
    truncation = settings.get("truncation", 0)
    neutralization = settings.get("neutralization", "")
    region = settings.get("region", "")
    maxTrade = settings.get("maxTrade", "OFF")

    matches_pyramid = next((check for check in is_data.get('checks', []) if check.get('name') == 'MATCHES_PYRAMID'), None)
    pyramids = [p.get('name', '') for p in matches_pyramid.get('pyramids', [])] if matches_pyramid else []

    robust_sharpe = 0.0
    robust_sharpe_check = next((check for check in is_data.get('checks', []) if check.get('name') == 'LOW_ROBUST_UNIVERSE_SHARPE'), None)
    if robust_sharpe_check:
        robust_sharpe = robust_sharpe_check.get('value', 0.0)
        
    return [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]

def modify_alpha_expression(original_exp, modification_type, value):
    modified_exp = original_exp
    if modification_type == "time_backfill_ts":
        match = re.search(r"ts_backfill\(([^,]+),\s*(\d+)\)", original_exp)
        if match:
            modified_exp = re.sub(r"ts_backfill\(([^,]+),\s*(\d+)\)", fr"ts_backfill(\1, {value})", original_exp, 1)
        else:
            modified_exp = f"ts_backfill({original_exp}, {value})"
    elif modification_type == "time_backfill_group":
        match = re.search(r"group_backfill\(([^,]+),\s*([^,]+),\s*(\d+)\)", original_exp)
        if match:
            modified_exp = re.sub(r"group_backfill\(([^,]+),\s*([^,]+),\s*(\d+)\)", fr"group_backfill(\1, \2, {value})", original_exp, 1)
        else:
            modified_exp = f"group_backfill({original_exp}, sector, {value})"
    elif modification_type == "add_winsorize":
        modified_exp = f"winsorize({original_exp}, std={value})"
    elif modification_type == "add_signed_power":
        modified_exp = f"signed_power({original_exp}, {value})"
    elif modification_type == "add_group_zscore":
        modified_exp = f"group_zscore({original_exp}, {value})"
    elif modification_type == "winsorize_std":
        match = re.search(r"winsorize\(([^,]+),\s*std=(\d+)\)", original_exp)
        if match:
            modified_exp = re.sub(r"winsorize\(([^,]+),\s*std=(\d+)\)", fr"winsorize(\1, std={value})", original_exp, 1)
    return modified_exp

class SessionManager:
    def __init__(self, session, start_time, expiry_time):
        self.session = session
        self.start_time = start_time
        self.expiry_time = expiry_time
        self.lock = threading.Lock()
        self.needupdate = False
        
    def refresh_session(self):
        with self.lock:
            print("Session expired, logging in again...")
            if self.session:
                self.session.close()
            self.session = login()
            self.start_time = time.time()
            self.needupdate = False

def simulate_multis(session_manager, alphas, name, tags):
    if session_manager.session is None:
        session_manager.refresh_session()
    if time.time() - session_manager.start_time > session_manager.expiry_time:
        session_manager.refresh_session()
        
    result_ids = []
    
    # Use multi simulations post
    while True:
        try:
            resp = session_manager.session.post(f'{brain_api_url}/simulations', json=alphas)
            simulation_progress_url = resp.headers.get('Location', 0)
            if simulation_progress_url == 0:
                json_data = resp.json()
                detail = json_data[0].get("detail", "") if isinstance(json_data, list) else json_data.get("detail", "")
                if 'SIMULATION_LIMIT_EXCEEDED' in detail:
                    print("Simulation limit exceeded, waiting 1s...")
                    time.sleep(1)
                else:
                    print("Simulation failed:", detail)
                    return result_ids
            else:
                break
        except Exception as e:
            print(f"Exception during post simulation: {e}")
            time.sleep(10)

    # Monitor progress
    get_start_time = time.time()
    while True:
        if time.time() - get_start_time > 1200:
            print("Simulation check timeout (20 mins).")
            return result_ids
        try:
            resps = session_manager.session.get(simulation_progress_url)
            json_data = resps.json()
            children = json_data.get("children", [])
            retry_after = float(resps.headers.get('Retry-After', 0))
            if retry_after == 0:
                break
            time.sleep(retry_after)
        except Exception as e:
            print(f"Progress check error: {e}")
            time.sleep(10)

    # Set attributes and tags
    for alpha, child in zip(alphas, children):
        try:
            child_progress = session_manager.session.get(f"{brain_api_url}/simulations/{child}")
            child_data = child_progress.json()
            alpha_id = child_data.get("alpha")
            if alpha_id:
                set_alpha_properties(session_manager.session, alpha_id, name=name, tags=tags)
                result_ids.append(alpha_id)
        except Exception as e:
            print(f"Failed to set alpha properties for child {child}: {e}")
            
    return result_ids

def simulate_multiple_alphas_with_retry(alpha_list, name="optimize_alpha", n_jobs=4, max_retries=3):
    original_alpha_count = len(alpha_list)
    all_results = []
    retries = 0
    
    # Simple single-threaded loop to avoid complex queue lock errors during tests
    session = login()
    session_manager = SessionManager(session, time.time(), 3 * 3600)
    
    # Process in batches of 4
    batch_size = 4
    for i in range(0, len(alpha_list), batch_size):
        batch = alpha_list[i:i+batch_size]
        print(f"Simulating batch {i//batch_size + 1} of {((len(alpha_list)-1)//batch_size)+1}...")
        result_ids = simulate_multis(session_manager, batch, name, [name])
        all_results.extend(result_ids)
        
    if session_manager.session:
        session_manager.session.close()
        
    return all_results

def runRobustSharpe(s, details):
    original_alpha_id, original_sharpe, _, _, _, original_exp, region, universe, original_neutralization, original_decay, delay, original_truncation, maxTrade, _, original_robust_sharpe = details
    print(f"🚀 开始Robust Sharpe优化: {original_alpha_id} - {original_exp}")
    
    neutralizations = NEUT_DICTS.get(region, ["MARKET", "SECTOR"])
    neut_alpha_configs = []
    for neut in neutralizations:
        config = {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': original_decay,
                'neutralization': neut,
                'truncation': original_truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': original_exp
        }
        neut_alpha_configs.append(config)
        
    print(f"👨‍💻 阶段一: 对 {len(neut_alpha_configs)} 个中性化配置进行模拟...")
    neut_result_ids = simulate_multiple_alphas_with_retry(neut_alpha_configs, name="robust_sharpe_opt")
    
    detailed_neut_results = []
    for alpha_id in neut_result_ids:
        try:
            curr_details = locate_details(s, alpha_id)
            curr_sharpe = curr_details[1]
            curr_robust = curr_details[-1]
            curr_neut = curr_details[8]
            if curr_sharpe > 1.0:
                detailed_neut_results.append({
                    'alpha_id': alpha_id,
                    'sharpe': curr_sharpe,
                    'robust_sharpe': curr_robust,
                    'neutralization': curr_neut
                })
        except Exception as e:
            print(f"Error fetching details for {alpha_id}: {e}")
            
    detailed_neut_results.sort(key=lambda x: x['robust_sharpe'], reverse=True)
    best_neut_configs = detailed_neut_results[:2]
    
    if not best_neut_configs:
        print("未选出合适的最佳中性化配置，使用默认配置。")
        best_neut_configs = [{'neutralization': original_neutralization, 'robust_sharpe': original_robust_sharpe, 'sharpe': original_sharpe}]

    print(f"✅ 选出最佳中性化配置: {[c['neutralization'] for c in best_neut_configs]}")
    
    # Decay/Truncation optimization
    print("\n--- 阶段二: Decay/Truncation 参数探索 ---")
    decay_options = [original_decay, 10, 30]
    truncation_options = [original_truncation, 0.05]
    
    dt_configs = []
    for neut_cfg in best_neut_configs:
        for d_val in decay_options:
            for t_val in truncation_options:
                config = {
                    'type': 'REGULAR',
                    'settings': {
                        'instrumentType': 'EQUITY',
                        'region': region,
                        'universe': universe,
                        'delay': delay,
                        'decay': d_val,
                        'neutralization': neut_cfg['neutralization'],
                        'truncation': t_val,
                        'pasteurization': 'ON',
                        'unitHandling': 'VERIFY',
                        'nanHandling': 'ON',
                        'language': 'FASTEXPR',
                        'visualization': False,
                        'testPeriod': "P0Y",
                        'maxTrade': maxTrade
                    },
                    'regular': original_exp
                }
                dt_configs.append(config)
                
    print(f"模拟 {len(dt_configs)} 个 Decay/Truncation 组合...")
    dt_result_ids = simulate_multiple_alphas_with_retry(dt_configs, name="robust_sharpe_opt")
    
    detailed_dt_results = []
    for alpha_id in dt_result_ids:
        try:
            curr_details = locate_details(s, alpha_id)
            detailed_dt_results.append({
                'alpha_id': alpha_id,
                'sharpe': curr_details[1],
                'robust_sharpe': curr_details[-1],
                'neutralization': curr_details[8],
                'decay': curr_details[9],
                'truncation': curr_details[11]
            })
        except Exception as e:
            print(f"Error fetching details for {alpha_id}: {e}")
            
    detailed_dt_results.sort(key=lambda x: x['robust_sharpe'], reverse=True)
    best_base_configs = detailed_dt_results[:2]
    
    # Expression mutation
    print("\n--- 阶段三: 表达式变体生成与模拟 ---")
    expression_modifications = [
        ("time_backfill_ts", 90),
        ("add_winsorize", 3),
        ("add_signed_power", 0.5),
        ("add_group_zscore", "sector")
    ]
    
    variant_configs = []
    for base_cfg in best_base_configs:
        for mod_type, mod_val in expression_modifications:
            mod_exp = modify_alpha_expression(original_exp, mod_type, mod_val)
            if mod_exp != original_exp:
                config = {
                    'type': 'REGULAR',
                    'settings': {
                        'instrumentType': 'EQUITY',
                        'region': region,
                        'universe': universe,
                        'delay': delay,
                        'decay': base_cfg['decay'],
                        'neutralization': base_cfg['neutralization'],
                        'truncation': base_cfg['truncation'],
                        'pasteurization': 'ON',
                        'unitHandling': 'VERIFY',
                        'nanHandling': 'ON',
                        'language': 'FASTEXPR',
                        'visualization': False,
                        'testPeriod': "P0Y",
                        'maxTrade': maxTrade
                    },
                    'regular': mod_exp
                }
                variant_configs.append(config)
                
    print(f"模拟 {len(variant_configs)} 个表达式变体...")
    variant_result_ids = simulate_multiple_alphas_with_retry(variant_configs, name="robust_sharpe_opt")
    
    # Gather final results
    final_alphas = []
    for alpha_id in variant_result_ids:
        try:
            curr_details = locate_details(s, alpha_id)
            final_alphas.append({
                'alpha_id': alpha_id,
                'expression': curr_details[5],
                'neutralization': curr_details[8],
                'decay': curr_details[9],
                'truncation': curr_details[11],
                'robust_sharpe': curr_details[-1],
                'sharpe': curr_details[1]
            })
        except Exception as e:
            print(f"Error fetching details for {alpha_id}: {e}")
            
    df = pd.DataFrame(final_alphas)
    os.makedirs("optimize", exist_ok=True)
    csv_path = f"optimize/{original_alpha_id}_robust_sharpe_all_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"🎉 优化完成！结果保存至: {csv_path}")

def main():
    parser = argparse.ArgumentParser(description='Optimize Alpha expressions for Robust Sharpe.')
    parser.add_argument('alpha_id', help='The Alpha ID to optimize.')
    args = parser.parse_args()
    
    s = login()
    details = locate_details(s, args.alpha_id)
    runRobustSharpe(s, details)

if __name__ == '__main__':
    main()
