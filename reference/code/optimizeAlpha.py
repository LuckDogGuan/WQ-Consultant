import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
import sys
import time
from machine_lib import * 
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.exceptions import RequestException, ConnectionError
import json
import argparse
import queue
import random
import self_corr_checkV3 as scV3  # 添加导入self_corr_checkV3模块
from diggingStep import *
from collections import defaultdict
from machine_lib import basic_ops, getHashSeed, first_order_factory, ts_ops
from datetime import datetime  # re-import after star imports to restore class (diggingStep exports module)

# 全局卡槽大小覆盖（None = 自动；由 --batch-size 命令行参数设置）
_BATCH_SIZE_OVERRIDE = None

class SessionManager:
    def __init__(self, session, start_time, expiry_time):
        self.session = session
        self.start_time = start_time
        self.expiry_time = expiry_time
        self.lock = threading.Lock()  # 添加线程锁保护session刷新

    def refresh_session(self):
        with self.lock:  # 使用线程锁保护session刷新过程
            print("Session expired, logging in again...")
            if self.session:
                self.session.close()
            self.session = login()  # 使用同步login函数
            self.start_time = time.time()

def locate_details(s, alpha_id):
    while True:
        alpha = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id)
        if "retry-after" in alpha.headers:
            time.sleep(float(alpha.headers["Retry-After"]))
        else:
            break
    string = alpha.content.decode('utf-8')
    metrics = json.loads(string)

    # 使用 get 方法安全获取数据
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
    maxTrade = settings.get("maxTrade", 0)
    
    # 安全获取 pyramids 数据
    matches_pyramid = next((check for check in is_data.get('checks', []) if check.get('name') == 'MATCHES_PYRAMID'), None)
    pyramids = [p.get('name', '') for p in matches_pyramid.get('pyramids', [])] if matches_pyramid else []

    # 查找 LOW_ROBUST_UNIVERSE_SHARPE
    robust_sharpe = 0.0
    robust_sharpe_check = next((check for check in is_data.get('checks', []) if check.get('name') == 'LOW_ROBUST_UNIVERSE_SHARPE'), None)
    if robust_sharpe_check:
        robust_sharpe = robust_sharpe_check.get('value', 0.0)
    
    triple = [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]
    return triple


def get_pnl(s, alpha_id):
    """
    Fetches the profit and loss (PnL) data for a given alpha ID by making requests to an API endpoint.
    The function handles retry logic for requests when a 'Retry-After' header
    is present in the response from the server.

    Parameters:
        s: requests.Session
            The session object used to make requests to the API.
        alpha_id: str
            The unique identifier of the alpha whose PnL data is to be fetched.

    Returns:
        requests.Response
            The API response containing PnL data.

    Raises:
        No explicit exceptions are raised within the function, but exceptions
        related to HTTP requests (such as connection errors) may occur.

    """
    while True:
        pnl = s.get('https://api.worldquantbrain.com/alphas/' + alpha_id + '/recordsets/pnl')
        if pnl.headers.get('Retry-After', 0) == 0:
             break
        time.sleep(float(pnl.headers['Retry-After']))
    return pnl

    return pnl

import re

def first_self_factory(fields):
    alpha_set = []
    for field in fields:
        alpha1 = f"ts_zscore(group_rank({field}, sector), 120)"
        alpha2 = f"ts_zscore(group_rank({field}, sector), 22)"
        alpha_set += [alpha1, alpha2]
    return alpha_set

def eventDriven(field):
    gp = "group_cartesian_product(country, industry)"
    exprs = []
    days = [5, 22, 66, 120, 240]
    for op in group_ops:
        if op == "group_backfill":
            for day in [22, 66]:
                expr = f"{op}({field}, {gp}, {day}, std=4.0)"
                for ts_op in ts_ops:
                    for ts_day in days:
                        exprs.append(f"{ts_op}({expr}, {ts_day})")
            continue

        expr = f"{op}({field},{gp})"
        for ts_op in ts_ops:
            for day in days:
                exprs.append(f"{ts_op}({expr},{day})")

    return exprs


def template_factory(field, region=None):
    output = []

    output.append(f"""divide(rank({field}), rank(returns))""")
    output.append(f"""signed_power({field}, 0.5)""")
    output.append(f"""signed_power({field}, 2)""")
    output.append(f"""hump(zscore({field}), hump=0.01)""")
    output.append(f"""last_diff_value({field}, 22)""")

    output.append(f"""
    my_group = market;
    my_group2 = bucket(rank(cap),range='0,1,0.1');
    alpha=rank(group_rank(ts_decay_linear(volume/ts_sum(volume,252),10),my_group)*group_rank(ts_rank({field}, 22),my_group)*group_rank(-ts_delta(close,5),my_group));
    trade_when(volume>adv20,group_neutralize(alpha,my_group2),-1)
    """)

    output.append(f"""ts_regression(ts_zscore(ts_mean({field}, 252),500), ts_zscore(ts_std_dev({field}, 252),500),500)""")
    output.append(f"""ts_regression(ts_zscore({field}, 500), step(500), 500)""")
    output.append(f"""1 / ts_std_dev(ts_regression(ts_zscore(ts_mean({field}, 252),500), ts_zscore(ts_std_dev({field}, 252),500),500), 500)""")
    output.append(f"""
    residual = ts_regression(ts_zscore(ts_mean({field}, 252),500), ts_zscore(ts_std_dev({field}, 252), 500), 500);
    residual/ts_std_dev(residual, 500)
    """)

    return output


def trade_when_factory(op, field, region, delay=1):
    output = []
    open_events = ["ts_arg_max(volume, 5) == 0", "ts_corr(close, volume, 20) < 0",
                   "ts_corr(close, volume, 5) < 0", "ts_mean(volume,10)>ts_mean(volume,60)",
                   "group_rank(ts_std_dev(returns,60), sector) > 0.7", "ts_zscore(returns,60) > 2",
                   "ts_arg_min(volume, 5) > 3",
                   "ts_std_dev(returns, 5) > ts_std_dev(returns, 20)",
                   "ts_arg_max(close, 5) == 0", "ts_arg_max(close, 20) == 0",
                   "ts_corr(close, volume, 5) > 0", "ts_corr(close, volume, 5) > 0.3",
                   "ts_corr(close, volume, 5) > 0.5",
                   "ts_corr(close, volume, 20) > 0", "ts_corr(close, volume, 20) > 0.3",
                   "ts_corr(close, volume, 20) > 0.5", "ts_corr(vwap, volume, 20) > 0.5",
                   "ts_corr(vwap, volume, 20) > 0.3",
                   "ts_regression(returns, ts_step(20), 20, lag = 0, rettype = 2) > 0",
                   "ts_regression(returns, ts_step(5), 5, lag = 0, rettype = 2) > 0"]
    if delay == 1:
        exit_events = ["abs(returns) > 0.1", "-1"]
    else:
        exit_events = ["abs(returns) > 0.1", "-1"]

    usa_events = ["rank(rp_css_business) > 0.8", "ts_rank(rp_css_business, 22) > 0.8",
                  "rank(vec_avg(nws5_close_vol)) > 0.8", "rank(vec_avg(nws48_ssc)) > 0.8",
                  "ts_rank(vec_avg(nws48_ssc),22) > 0.8", "rank(vec_avg(mws50_ssc)) > 0.8",
                  "ts_rank(vec_avg(mws50_ssc),22) > 0.8",
                  "ts_rank(vec_sum(scl12_alltype_buzzvec),22) > 0.9", "pcr_oi_270 < 1", "pcr_oi_270 > 1"]

    eur_events = ["sharesout > ts_mean(sharesout, 20)",
                  "and(rp_css_insider > 0, rp_ess_insider > 0)",
                  "eps_12m > anl69_analyst_best_eeps_cur_yr",
                  "pv87_sentiment_mean > ts_mean(pv87_sentiment_mean, 20) + 2 * ts_std_dev(pv87_sentiment_mean, 20)",
                  "ts_delta(anl46_sentiment, 1) > 0.05",
                  "vec_avg(mws81_sentiment) > ts_mean(vec_avg(mws81_sentiment), 20)",
                  "rank(rp_css_business) > 0.8", "ts_rank(rp_css_business, 22) > 0.8",
                  "rank(vec_avg(nws3_scores_posnormscr)) > 0.8",
                  "ts_rank(vec_avg(nws3_scores_posnormscr),22) > 0.8"]

    if region == 'EUR':
        open_events.extend(eur_events)
    elif region == 'USA':
        open_events.extend(usa_events)

    for oe in open_events:
        for ee in exit_events:
            alpha = "%s(%s, %s, %s)" % (op, oe, field, ee)
            output.append(alpha)
    return output


def trade_act_factory(op, field, region):
    eur_conditions = [
        {"field": "rsk62_risk_growth",
         "condition": "ts_zscore(rsk62_risk_growth, 60) > 1.5",
         "exit": "ts_delta(rsk62_risk_growth, 5) < 0"},
        {"field": "rsk62_risk_logadv20",
         "condition": "rsk62_risk_logadv20 > ts_quantile(rsk62_risk_logadv20,20)",
         "exit": "volume < ts_mean(volume, 5)"},
        {"field": "rsk62_risk_logcap",
         "condition": "rsk62_risk_logcap < ts_quantile(rsk62_risk_logcap,252)",
         "exit": "rsk62_risk_logcap > ts_mean(rsk62_risk_logcap, 60)"},
        {"field": "rsk62_risk_mtl",
         "condition": "ts_corr(returns, rsk62_risk_mtl, 10) > 0.7",
         "exit": "ts_delta(rsk62_risk_mtl, 5) < -ts_std_dev(rsk62_risk_mtl, 20)"},
        {"field": "rsk62_risk_mts",
         "condition": "rsk62_risk_mts < ts_quantile(rsk62_risk_mts, 20)",
         "exit": "rsk62_risk_mts > ts_median(rsk62_risk_mts, 60)"},
        {"field": "rsk62_risk_qe2d",
         "condition": "ts_delta(rsk62_risk_qe2d, 5) > ts_std_dev(rsk62_risk_qe2d, 60)",
         "exit": "debt/equity > 1.5"},
        {"field": "rsk62_risk_volatility",
         "condition": "rsk62_risk_volatility < ts_quantile(rsk62_risk_volatility,60)",
         "exit": "rsk62_risk_volatility > ts_quantile(rsk62_risk_volatility,20)"},
        {"condition": "sharesout > ts_mean(sharesout, 20)",
         "exit": "sharesout < ts_mean(sharesout, 10)"},
        {"condition": "and(rp_css_insider > 0, rp_ess_insider > 0)",
         "exit": "or(rp_css_insider < 0, rp_ess_insider < 0)"},
        {"condition": "eps_12m > anl69_analyst_best_eeps_cur_yr",
         "exit": "eps_12m < ts_mean(anl69_analyst_best_eeps_cur_yr, 10)"},
        {"condition": "eps_12m > anl69_analyst_best_eeps_cur_yr",
         "exit": "ts_delta(anl46_sentiment, 3) < -0.03"},
        {"condition": "pv87_sentiment_mean > ts_mean(pv87_sentiment_mean, 20) + 2 * ts_std_dev(pv87_sentiment_mean, 20)",
         "exit": "pv87_sentiment_mean < ts_median(pv87_sentiment_mean, 20)"},
        {"condition": "ts_delta(anl46_sentiment, 1) > 0.05",
         "exit": "ts_delta(anl46_sentiment, 3) < 0"},
        {"condition": "vec_avg(mws81_sentiment) > ts_mean(vec_avg(mws81_sentiment), 20)",
         "exit": "vec_avg(mws81_sentiment) < ts_mean(vec_avg(mws81_sentiment), 20)"},
        {"condition": "vec_avg(mws81_sentiment) > ts_mean(vec_avg(mws81_sentiment), 20)",
         "exit": "ts_corr(mws81_sentiment, returns, 5) < 0"},
        {"condition": "or(rank(vec_avg(nws3_scores_posnormscr)) > 0.8, ts_rank(vec_avg(nws3_scores_posnormscr), 22) > 0.8)",
         "exit": "ts_delta(vec_avg(nws3_scores_posnormscr), 3) < -0.1"},
    ]
    output = []
    if region == 'EUR':
        for item in eur_conditions:
            open_event = item['condition']
            exit_event = item['exit']
            alpha = "%s(%s, %s, %s)" % (op, open_event, field, exit_event)
            output.append(alpha)
    return output


NEUT_DICTS = {
    'USA': ['REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'GLB': ['REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'FAST'],
    'EUR': ['REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'ASI': ['REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'CHN': ['REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'FAST', 'SLOW_AND_FAST'],
    'KOR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'TWN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'HKG': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'AMR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'COUNTRY'],
    'IND': ['REVERSION_AND_MOMENTUM', 'CROWDING', 'FAST', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],
    'JPN': ['REVERSION_AND_MOMENTUM', 'CROWDING', 'FAST', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST'],
}

def modify_alpha_expression(original_exp, modification_type, value):
    """
    根据指定的修改类型和值，智能地修改Alpha表达式字符串。
    """
    modified_exp = original_exp

    if modification_type == "time_backfill_ts":
        # 查找 ts_backfill(X, N) 并修改 N
        # 匹配 ts_backfill( 任意非逗号字符 , 任意数字 )
        match = re.search(r"ts_backfill\(([^,]+),\s*(\d+)\)", original_exp)
        if match:
            # 替换捕获组2（数字）为新的值
            modified_exp = re.sub(r"ts_backfill\(([^,]+),\s*(\d+)\)", fr"ts_backfill(\1, {value})", original_exp, 1)
        else:
            # 如果没有找到 ts_backfill，则尝试添加
            modified_exp = f"ts_backfill({original_exp}, {value})"
            
    elif modification_type == "time_backfill_group":
        # 查找 group_backfill(X, Y, N) 并修改 N
        # 匹配 group_backfill( 任意非逗号字符 , 任意非逗号字符 , 任意数字 )
        match = re.search(r"group_backfill\(([^,]+),\s*([^,]+),\s*(\d+)\)", original_exp)
        if match:
            # 替换捕获组3（数字）为新的值
            modified_exp = re.sub(r"group_backfill\(([^,]+),\s*([^,]+),\s*(\d+)\)", fr"group_backfill(\1, \2, {value})", original_exp, 1)
        else:
            # 如果没有找到 group_backfill，则尝试添加
            # 假设 group_backfill 需要一个 group 参数，这里默认使用 'sector'
            modified_exp = f"group_backfill({original_exp}, sector, {value})"

    elif modification_type == "add_winsorize":
        # 将 original_exp 用 winsorize(original_exp, std=value) 包装
        modified_exp = f"winsorize({original_exp}, std={value})"

    elif modification_type == "add_signed_power":
        # 将 original_exp 用 signed_power(original_exp, value) 包装
        modified_exp = f"signed_power({original_exp}, {value})"

    elif modification_type == "add_group_zscore":
        # 将 original_exp 用 group_zscore(original_exp, value) 包装
        # value 预期为 'sector' 或 'industry'
        modified_exp = f"group_zscore({original_exp}, {value})"

    elif modification_type == "winsorize_std":
        # 查找 winsorize(X, std=N) 并修改 N
        match = re.search(r"winsorize\(([^,]+),\s*std=(\d+)\)", original_exp)
        if match:
            modified_exp = re.sub(r"winsorize\(([^,]+),\s*std=(\d+)\)", fr"winsorize(\1, std={value})", original_exp, 1)
        # 如果没有找到 winsorize，则不进行修改，或者可以考虑添加，但这里选择不修改
        
    else:
        print(f"未知修改类型: {modification_type}")

    return modified_exp

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def saveResults(details, alpha_list):
    import copy  # 确保 copy 模块可用

    # 获取OS alphas数据用于计算自相关性（预加载，提高性能）
    os_alpha_ids_sc, os_alpha_rets_sc = scV3.load_data("SelfCorr")
    os_alpha_ids_ppac, os_alpha_rets_ppac = scV3.load_data("PPAC")

    # 调试信息：检查两个池子的数据是否不同
    print(f"\n=== 数据加载调试信息 ===")
    print(f"SelfCorr 池子 alpha 总数: {sum(len(v) for v in os_alpha_ids_sc.values())}")
    print(f"PPAC 池子 alpha 总数: {sum(len(v) for v in os_alpha_ids_ppac.values())}")
    print(f"SelfCorr 池子包含的区域: {list(os_alpha_ids_sc.keys())}")
    print(f"PPAC 池子包含的区域: {list(os_alpha_ids_ppac.keys())}")

    # 检查是否有重叠
    all_sc_ids = set([aid for aids in os_alpha_ids_sc.values() for aid in aids])
    all_ppac_ids = set([aid for aids in os_alpha_ids_ppac.values() for aid in aids])
    overlap = all_sc_ids & all_ppac_ids
    print(f"两个池子重叠的 alpha 数量: {len(overlap)}")
    print(f"SelfCorr 独有: {len(all_sc_ids - all_ppac_ids)}")
    print(f"PPAC 独有: {len(all_ppac_ids - all_sc_ids)}")
    print(f"========================\n")

    # 定义处理单个alpha的辅助函数
    def process_single_alpha(alpha):
        try:
            # 判断输入是details列表还是单个alpha_id
            if isinstance(alpha, list):
                # 处理初始details
                [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids_list, robust_sharpe] = alpha
            else:
                # 处理普通alpha_id
                tem = locate_details(s, alpha)
                [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids_list, robust_sharpe] = tem

            
            # 转换turnover和margin数值
            turnover = float(turnover) * 100  # 乘以100
            margin = float(margin) * 10000    # 乘以10000

            # 获取alpha详细信息
            alpha_detail = get_alpha_byid(s, alpha_id)
            
            # 提取result结果
            checks = alpha_detail.get('is', {}).get('checks', [])
            checks_df = pd.DataFrame(checks)
            # 检查是否通过了最基础的项目
            if (any(checks_df["result"] == "FAIL") or any(checks_df["result"] == "ERROR")):
                # 最基础的项目不通过
                result = 'Fail'
            else:
                result = 'Pass'
            
            if "Weight is too strongly" in str(checks):
                result = 'Fail'
            
            # 新增：计算glb_low值
            glb_low_values = []
            for check_name in ['LOW_GLB_AMER_SHARPE', 'LOW_GLB_EMEA_SHARPE', 'LOW_GLB_APAC_SHARPE']:
                check = next((c for c in checks if c.get('name') == check_name), None)
                value = str(check.get('value', '0') if check else '0')
                glb_low_values.append(value)
            glb_low = '|'.join(glb_low_values)
            
            # 新增：计算警告数量
            warning_count = sum(1 for check in checks if check.get('result') == 'WARNING')
            print(f"Debug: Calculated warning_count for {alpha_id}: {warning_count}")

            # 获取2-year Sharpe
            two_year_sharpe = 0.0
            two_year_sharpe_check = next((check for check in checks if check.get('name') == 'LOW_2Y_SHARPE'), None)
            if two_year_sharpe_check:
                two_year_sharpe = two_year_sharpe_check.get('value', 0.0)

            # 提取opCount
            opCount = alpha_detail['regular']['operatorCount']
            
            # 判断是否属于power pool
            power_pool_check = next((check for check in alpha_detail['is']['checks'] if check.get('name') == 'POWER_POOL_CORRELATION'), None)
            powerpool = 'Y' if power_pool_check is not None else 'N'
            
            # 计算sc - 使用深拷贝避免数据污染
            try:
                sorr = scV3.calc_self_corr(s, alpha_id=alpha_id,
                                          os_alpha_rets=os_alpha_rets_sc.copy(),  # DataFrame.copy()
                                          os_alpha_ids=copy.deepcopy(os_alpha_ids_sc))  # 深拷贝 dict
                sc = f"{sorr:.2f}" if sorr is not None else "0.00"
            except Exception as e:
                print(f"计算sc失败 {alpha_id}: {e}")
                sc = 0.00

            # 计算pa_sc - 使用深拷贝避免数据污染
            try:
                if powerpool == 'Y':
                    pa_sc_value = scV3.calc_self_corr(s, alpha_id=alpha_id,
                                                     os_alpha_rets=os_alpha_rets_ppac.copy(),  # DataFrame.copy()
                                                     os_alpha_ids=copy.deepcopy(os_alpha_ids_ppac))  # 深拷贝 dict
                    pa_sc = round(float(pa_sc_value), 2) if pa_sc_value is not None else 0.00
                else:
                    pa_sc = 0.00
            except Exception as e:
                print(f"计算pa_sc失败 {alpha_id}: {e}")
                pa_sc = 0.00
            
            # 处理pyramids为字符串
            pyramids_str = ' '.join(pyramids_list) if isinstance(pyramids_list, list) else ''
            
            # 获取returns
            try:
                json_data = get_pnl(s, alpha_id).json()['records']
                df_returns = pd.DataFrame(json_data)
                if not df_returns.empty:
                    # 计算总收益率
                    last_value = float(df_returns.iloc[-1, 1])
                    first_value = float(df_returns.iloc[0, 1])
                    total_return = last_value - first_value
                    returns = f"{total_return:.4f}"
                else:
                    returns = "0.0000"
            except Exception as e:
                print(f"获取alpha_id {alpha_id} 的returns数据失败: {str(e)}")
                returns = "0.0000"
            
            return [alpha_id, neutralization, sc, opCount, powerpool, pa_sc, pyramids_str, decay, robust_sharpe, sharpe, fitness, turnover, margin, returns, result, glb_low, warning_count, two_year_sharpe]
        except Exception as e:
            print(f"处理alpha时出错: {str(e)}")
            return None
    
    # Define columns once
    columns = ['alpha_id', 'neutralization', 'sc', 'opCount', 'powerpool', 'pa_sc', 'pyramids', 'decay', 'robust_sharpe', 'sharpe', 'fitness', 'turnover', 'margin', 'returns', 'result', 'glb_low', 'warning_count', '2_year_sharpe']
    all_rows = []

    # Process initial alpha
    initial_result = process_single_alpha(details)
    if initial_result is not None:
        all_rows.append(list(initial_result) + [True])

    # 过滤掉alpha_list中的None值、字符串"None"以及已经作为初始details处理过的alpha_id
    original_alpha_id_from_details = details[0]
    filtered_alpha_list = [alpha for alpha in alpha_list if alpha is not None and alpha != "None" and alpha != original_alpha_id_from_details]

    # 使用线程池处理过滤后的alpha列表
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_single_alpha, filtered_alpha_list))

    # 过滤掉None结果并收集所有有效行
    valid_results = [res for res in results if res is not None]
    for res in valid_results:
        if len(res) == 18:
            all_rows.append(list(res) + [False])
        else:
            print(f"警告: 结果长度不匹配，跳过: {res}")

    # Create DataFrame from collected rows
    if all_rows:
        df_list = pd.DataFrame(all_rows, columns=columns + ['is_original'])
    else:
        # If no valid results, create an empty DataFrame with all columns
        df_list = pd.DataFrame(columns=columns + ['is_original'])

    # 去重
    df_list = df_list.drop_duplicates(subset='alpha_id', keep='last')

    # 确保原始alpha在第一行
    if not df_list.empty and 'is_original' in df_list.columns:
        # 检查是否有标记为原始alpha的行
        original_alpha_mask = df_list['is_original']
        if original_alpha_mask.any():
            # 提取原始alpha行
            original_alpha = df_list[original_alpha_mask].copy()
            # 提取剩余行并排序
            sorted_rest = df_list[~original_alpha_mask].sort_values(by=["neutralization", "sc"], ascending=[True, True])
            # 合并原始行和排序后的其余行
            df_list = pd.concat([original_alpha, sorted_rest], ignore_index=True)
        else:
            # 如果没有标记为原始alpha的行，查找并设置原始alpha
            # 假设details[0]是原始alpha_id
            original_alpha_id = details[0]
            original_alpha_mask = df_list['alpha_id'] == original_alpha_id
            if original_alpha_mask.any():
                # 提取原始alpha行
                original_alpha = df_list[original_alpha_mask].copy()
                # 提取剩余行并排序
                sorted_rest = df_list[~original_alpha_mask].sort_values(by=["neutralization", "sc"], ascending=[True, True])
                # 合并原始行和排序后的其余行
                df_list = pd.concat([original_alpha, sorted_rest], ignore_index=True)
            else:
                # 如果找不到原始alpha，按照原来的逻辑处理
                original_alpha = df_list.iloc[[0]].copy()
                sorted_rest = df_list.iloc[1:].sort_values(by=["neutralization", "sc"], ascending=[True, True])
                df_list = pd.concat([original_alpha, sorted_rest], ignore_index=True)
        df_list = df_list.drop(columns=['is_original'], errors='ignore')
        
    os.makedirs("optimize", exist_ok=True)
    # 保存去重后的df_list到optimize目录下的CSV文件
    save_path = os.path.join("optimize", f"{details[0]}.csv")
    df_list.to_csv(save_path, index=False)
    print(f"已保存去重后的alpha列表到：{save_path}")
    
    df1 = pd.DataFrame()
    
    # 定义获取单个alpha_id的PnL数据的辅助函数
    def fetch_pnl_data(alpha_id):
        try:
            print(alpha_id)
            json_data = get_pnl(s, alpha_id).json()['records']
            df = pd.DataFrame(json_data)
            df = df.iloc[:,0:2]
            df.columns = ['date', alpha_id]
            df.set_index('date', inplace=True)
            return df
        except Exception as e:
            print(f"获取alpha_id {alpha_id} 的PnL数据失败: {str(e)}")
            return None
    
    # 使用线程池获取PnL数据
    with ThreadPoolExecutor(max_workers=10) as executor:
        pnl_results = list(executor.map(fetch_pnl_data, df_list['alpha_id'].unique()))
    
    # 合并PnL数据
    for df in pnl_results:
        if df is not None:
            df1 = pd.merge(df1, df, left_index=True, right_index=True, how='outer')
    
    df1.index = pd.to_datetime(df1.index)
    # 使用neutralization和sc进行双重排序，先按neutralization升序，再按sc升序
    df_sorted = df_list.sort_values(by=["neutralization", "sc"], ascending=[True, True])
    # 保持原有的索引设置
    df_sorted.set_index(["sc", "opCount"])
    return df1
    
def drawResults(details, alpha_list):
    # 调用saveResults获取准备好的数据
    df1 = saveResults(details, alpha_list)
    return
    
    # 设置matplotlib
    plt.rcParams['font.sans-serif'] = ["Microsoft YaHei", "Arial Unicode MS"]  # 兼容win和mac的字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    # 绘制所有列（自动分配颜色和标签）
    # 修改图表初始化参数
    ax = df1.plot(
    figsize=(20, 12),  # 增大图表尺寸
    linewidth=1,       # 减小线条宽度
    title='多时间序列对比',
    grid=True,
    alpha=0.6,         # 降低透明度
    fontsize=10        # 减小字体大小
    )
    # 添加图例和标签
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('数值', fontsize=12)
    ax.legend(loc='upper right', frameon=True)  # 调整图例位置避免重叠

    # 在每条线末尾添加alpha_id标注
    lines = ax.get_lines()
    y_offset = 0  # 垂直偏移量初始值
    offset_step = 15  # 每条线的垂直偏移步长
    max_offset = 100  # 最大偏移量，防止超出图表范围
    
    for i, (line, alpha_id) in enumerate(zip(lines, df1.columns)):
        x_data, y_data = line.get_data()
        if len(x_data) > 0:  # 确保有数据点
            last_x = x_data[-1]
            last_y = y_data[-1]
            
            # 计算垂直偏移，循环使用偏移量防止重叠
            current_offset = (y_offset % max_offset) - (max_offset / 2)
            y_offset += offset_step
            
            ax.annotate(
                alpha_id,
                xy=(last_x, last_y),
                xytext=(5, current_offset),  # 水平和垂直偏移
                textcoords='offset points',
                fontsize=9,
                color=line.get_color(),
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='gray', alpha=0.7),  # 添加背景框
                rotation=30,  # 轻微旋转标签
                va='center'
            )

    plt.xticks(rotation=45)
    plt.tight_layout()
   
    save_dir = "optimize" # 修改保存目录为records
    os.makedirs(save_dir, exist_ok=True)  # exist_ok=True避免目录已存在时报错

    # 保存图片到指定路径（使用alpha_id命名）
    save_path = os.path.join(save_dir, f"{details[0]}.png") # 修改保存目录为records
    plt.savefig(
        save_path,
        dpi=300,  # 设置图片分辨率（可选，提高清晰度）
        bbox_inches='tight'  # 自动调整布局避免标签截断（可选）
    )
    print(f"图表已保存至：{save_path}")

    # 关闭图表释放内存（重要！避免内存泄漏）
    plt.close()


# 帮助函数：将alpha列表分割为多个批次，每批次最多包含batch_size个alpha
def to_multi_alphas(alpha_list, batch_size=10):
    return [alpha_list[i:i + batch_size] for i in range(0, len(alpha_list), batch_size)]

def simulate_multis(session_manager, alphas, name, tags):
    """
    模拟多个alpha表达式对应的某个地区的信息
    """
    if session_manager.session is None:
        session_manager.refresh_session()
    if time.time() - session_manager.start_time > session_manager.expiry_time:
        session_manager.refresh_session()

    result_ids = []  # 用于存储alpha_id结果
    
    if len(alphas) >1:
        while True:
            try:
                resp = session_manager.session.post('https://api.worldquantbrain.com/simulations',
                                                    json=alphas)
                simulation_progress_url = resp.headers.get('Location', 0)
                if simulation_progress_url == 0:
                    json_data = resp.json()
                    print(json_data)
                    detail = ""
                    if isinstance(json_data, list):
                        if json_data and isinstance(json_data[0], dict):
                            detail = json_data[0].get("detail", "")
                        else:
                            detail = str(json_data)
                    elif isinstance(json_data, dict):
                        detail = json_data.get("detail", "")

                    if isinstance(detail, str) and 'SIMULATION_LIMIT_EXCEEDED' in detail:
                        print("Limited by the number of simulations allowed per time")
                        time.sleep(1)
                    else:
                        print("detail:", detail)
                        print("json_data:", json_data)
                        print("Alpha expression is duplicated or invalid.")
                        time.sleep(1)
                        return result_ids
                else:
                    print('simulation_progress_url:', simulation_progress_url)
                    break
            except KeyError:
                print("Location key error during simulation request")
                time.sleep(60)
            except Exception as e:
                print("An error occurred1:", str(e))
                time.sleep(60)
        # 检查进度阶段超时控制（15分钟）
        get_start_time = time.time()
        while True:
            if time.time() - get_start_time > 1200:
                print(f"模拟进度检查超时(20分钟), alpha: {alphas}, progress_url: {simulation_progress_url}")
                return result_ids
            try:
                resps = session_manager.session.get(simulation_progress_url)
                json_data = resps.json()
                # 提前初始化children变量，确保所有路径都能访问
                children = json_data.get("children", [])
                # 获取响应头
                headers = resps.headers
                retry_after = float(headers.get('Retry-After', 0))
                status = json_data.get("status", "")
                if retry_after > 0:
                    # 模拟仍在运行，等待后继续轮询
                    print(f"模拟进行中，等待 {retry_after}s ... ({int(time.time() - get_start_time)}s elapsed)", flush=True)
                    time.sleep(retry_after)
                else:
                    # retry_after == 0 表示模拟已结束
                    if status == 'ERROR':
                        print(f"Error in simulation: {simulation_progress_url}")
                    elif status != "COMPLETE":
                        print(f"Simulation not complete (status={status}): {simulation_progress_url}")
                    else:
                        print(f"Simulation completed: {simulation_progress_url}")
                    break
            except Exception as e:
                print(f"Progress check error: %s", str(e))
                time.sleep(30) 
        
        # 将for循环移到while循环之外
        for alpha, child in zip(alphas, children):
            try:
                child_str = str(child) # 新增：确保child是字符串
                child_progress = session_manager.session.get(brain_api_url + "/simulations/" + child_str)
                json_data = child_progress.json()
                alpha_id = json_data["alpha"]
                print("set_alpha_properties alpha_id: %s"%alpha_id)
                set_alpha_properties(session_manager.session,
                                    alpha_id,
                                    name="%s" % name,
                                    color=None,
                                    tags=tags)
                # 使用原始alpha数据生成唯一ID
                settings_str = json.dumps(alpha['settings'], sort_keys=True)  # 使用原始配置
                regular_str = alpha['regular']  # 使用原始配置
                unique_id = f"{regular_str}|{settings_str}"
                # 确保optimize目录存在
                os.makedirs('optimize', exist_ok=True)
                result_file_path = f'optimize/{name}_simulated_alpha_expression.txt'
                with open(result_file_path, mode='a') as f:
                    f.write(f"{alpha_id}|{unique_id}\n")
                # 将alpha_id添加到结果列表
                result_ids.append(alpha_id)
            except KeyError:
                print("Failed to retrieve alpha ID for: %s" % (brain_api_url + "/simulations/" + child))
                try:
                    # 关联原始alpha信息并获取错误状态和消息
                    settings_str = json.dumps(alpha['settings'], sort_keys=True)  # 使用原始配置
                    regular_str = alpha['regular']  # 使用原始配置
                    unique_id = f"{regular_str}|{settings_str}"
                    status = json_data.get("status")
                    if status == "ERROR":
                        error_msg = json_data.get("message", "No error message available")
                        error_str = f"ERROR_{error_msg}"
                        print("write error msg to file")
                        # 确保optimize目录存在
                        os.makedirs('optimize', exist_ok=True)
                        result_file_path = f'optimize/{name}_simulated_alpha_expression.txt'
                        with open(result_file_path, mode='a') as f:
                            f.write(f"{error_str}|{unique_id}\n")
                except Exception as e:
                    print("get error status :",str(e))  
            except Exception as e:
                print("An error occurred while setting alpha properties:" + str(e))
        return result_ids  # 将return移至for循环外部
    else:
        result_ids = []
        simulation_data = alphas[0]
        while True:
            try:
                resp = session_manager.session.post('https://api.worldquantbrain.com/simulations',
                                                    json=simulation_data)
                simulation_progress_url = resp.headers.get('Location', 0)
                if simulation_progress_url == 0:
                    json_data = resp.json()
                    if isinstance(json_data, list):
                        print(json_data)
                        detail = json_data[0].get("detail", 0) if json_data else 0
                    else:
                        detail = json_data.get("detail", 0)
                    if 'SIMULATION_LIMIT_EXCEEDED' in detail:
                        print("Limited by the number of simulations allowed per time")
                        time.sleep(1)
                    else:
                        print("detail:", detail)
                        print("json_data:", json_data)
                        print("Alpha expression is duplicated")
                        time.sleep(1)
                        return result_ids
                else:
                    print('simulation_progress_url:', simulation_progress_url)
                    break
            except KeyError:
                print("Location key error during simulation request")
                time.sleep(60)
            except Exception as e:
                print("An error occurred2:", str(e))
                time.sleep(60)

        # 检查进度阶段超时控制（5分钟）
        get_start_time = time.time()
        while True:
            if time.time() - get_start_time > 1200:
                print(f"模拟进度检查超时（20分钟），alpha: {alpha}, progress_url: {simulation_progress_url}")
                return result_ids
            try:
                resp = session_manager.session.get(simulation_progress_url)
                json_data = resp.json()
                # 获取响应头
                headers = resp.headers
                retry_after = headers.get('Retry-After', 0)
                if retry_after == 0:
                    print("response done: %s" % json_data)
                    break
                time.sleep(float(retry_after))
            except Exception as e:
                print("Error while checking progress:", str(e))
                time.sleep(60)

        print("%s done simulating, getting alpha details" % (simulation_progress_url))
        try:
            alpha_id = json_data.get("alpha")
            alpha = json_data.get("regular")
            print("set_alpha_properties alpha_id: %s"%alpha_id)
            # 假设 async_set_alpha_properties 有对应的同步版本
            set_alpha_properties(session_manager.session,
                                alpha_id,
                                name="%s" % name,
                                color=None,
                                tags=tags)

            
            settings_str = json.dumps(simulation_data['settings'], sort_keys=True)  # 改为使用原始配置
            regular_str = simulation_data['regular']  # 改为使用原始配置
            unique_id = f"{regular_str}|{settings_str}"
            # 确保optimize目录存在
            os.makedirs('optimize', exist_ok=True)
            result_file_path = f'optimize/{name}_simulated_alpha_expression.txt'
            with open(result_file_path, mode='a') as f:
                f.write(f"{alpha_id}|{unique_id}\n")
            result_ids.append(alpha_id)

        except KeyError:
            print("Failed to retrieve alpha ID for: %s" % simulation_progress_url)
            try:
                # 关联原始alpha信息并获取错误状态和消息
                settings_str = json.dumps(simulation_data['settings'], sort_keys=True)  # 使用原始配置
                regular_str = simulation_data['regular']  # 使用原始配置
                unique_id = f"{regular_str}|{settings_str}"
                status = json_data.get("status")
                if status == "ERROR":
                    error_msg = json_data.get("message", "No error message available")
                    error_str = f"ERROR_{error_msg}"
                    print("write error msg to file")
                    # 确保optimize目录存在
                    os.makedirs('optimize', exist_ok=True)
                    result_file_path = f'optimize/{name}_simulated_alpha_expression.txt'
                    with open(result_file_path, mode='a') as f:
                        f.write(f"{error_str}|{unique_id}\n")
            except Exception as e:
                print("get error status :",str(e))
        except Exception as e:
            print("An error occurred while setting alpha properties:", str(e))

        return result_ids  # 返回收集的alpha_id列表，每个ID出现两次

def simulate_multiple_alphas_with_retry(alpha_list, name="optimize_alpha", n_jobs=8, max_retries=5, is_neut=False):
    """
    包装simulate_multiple_alphas函数，使用队列方式提供自动重试功能
    当结果列表长度等于初始alpha_list长度或重试次数达到上限时退出
    固定批次大小为6个一组
    """
    original_alpha_count = len(alpha_list)
    all_results = []
    retries = 0
    # 创建用于存储结果的文件路径
    result_file_path = f'optimize/{name}_simulated_alpha_expression.txt'
    os.makedirs('optimize', exist_ok=True)
    
    while retries < max_retries:
        # 从文件中读取已完成的alpha表达式
        completed_alphas = set()
        try:
            with open(result_file_path, mode='r') as f:
                for line in f:
                    completed_alphas.add(line.strip())
            print(f"从文件中读取到{len(completed_alphas)}个已完成的alpha")
        except FileNotFoundError:
            print(f"文件{result_file_path}不存在，创建新文件")
        
        # 过滤出尚未完成的alpha
        remaining_alphas = []
        for alpha in alpha_list:
            # 生成唯一标识
            settings_str = json.dumps(alpha['settings'], sort_keys=True)
            regular_str = alpha['regular']
            unique_id = f"{regular_str}|{settings_str}"
            
            # 检查是否已完成
            if not any(unique_id in line for line in completed_alphas):
                remaining_alphas.append((alpha, unique_id))
            
            # 收集已完成的结果
            for line in completed_alphas:
                if "|" in line and unique_id in line:
                    alpha_id = line.split("|")[0]
                    if "ERROR" not in alpha_id and alpha_id not in all_results:
                        all_results.append(alpha_id)
        
        # 如果所有alpha都已完成，提前退出
        if len(remaining_alphas)==0:
            print(f"所有{original_alpha_count}个alpha已完成，无需继续重试")
            return all_results
        
        # 如果达到最大重试次数，退出
        if retries >= max_retries:
            print(f"已达到最大重试次数 {max_retries}，停止重试")
            break
        
        # 如果所有alpha都已完成，提前退出
        if len(remaining_alphas) == 0:
            print(f"所有{original_alpha_count}个alpha已完成，无需继续重试")
            return all_results
        
        # 如果达到最大重试次数，退出
        if retries >= max_retries:
            print(f"已达到最大重试次数 {max_retries}，停止重试")
            break
        
        print(f"第 {retries + 1} 次尝试，开始处理{len(remaining_alphas)}/{original_alpha_count}个未完成的alpha")
        
        # 创建线程安全的任务队列
        task_queue = queue.Queue()
        # 将所有任务添加到队列
        for alpha, unique_id in remaining_alphas:
            task_queue.put((alpha, unique_id))
        
        # 登录并创建会话管理器
        session = login()
        session_start_time = time.time()
        session_expiry_time = 3 * 60 * 60  # 3小时
        session_manager = SessionManager(session, session_start_time, session_expiry_time)
        
        if _BATCH_SIZE_OVERRIDE is not None:
            BATCH_SIZE = max(1, min(_BATCH_SIZE_OVERRIDE, len(remaining_alphas)))
        else:
            BATCH_SIZE = min(8, len(remaining_alphas)) - retries
            BATCH_SIZE = max(1, BATCH_SIZE) # 确保 BATCH_SIZE 至少为 1

            alpha_for_region_check = remaining_alphas[0][0] # 确保 remaining_alphas 已经检查不为空
            if alpha_for_region_check.get('settings').get('region') == "GLB":
                n_jobs = 3
                BATCH_SIZE = min(6, len(remaining_alphas)) - retries
                BATCH_SIZE = max(1, BATCH_SIZE) # 确保 GLB 区域的 BATCH_SIZE 也至少为 1
                if len(remaining_alphas) < 10 and BATCH_SIZE > 3:
                    BATCH_SIZE = 3
        if is_neut:
            BATCH_SIZE = 1
        # 添加批次计数器
        total_batches = (len(remaining_alphas) + BATCH_SIZE - 1) // BATCH_SIZE
        completed_batches = 0
        processed_tasks = 0 
        batch_lock = threading.Lock()  # 用于保护批次计数器的锁

        # 工作线程函数
        def worker(worker_id):
            nonlocal completed_batches, total_batches, processed_tasks
            while not task_queue.empty():
                try:
                    batch = []
                    for _ in range(BATCH_SIZE):
                        try:
                            item = task_queue.get(timeout=1)
                            batch.append(item)
                        except queue.Empty:
                            break
        
                    if not batch:
                        break  # 队列为空，退出循环
        
                    # 处理批次任务
                    alphas = [item[0] for item in batch]
                    unique_ids = [item[1] for item in batch]
            
                    # 调用模拟函数
                    print(f"[worker-{worker_id}] 开始提交批次 {len(alphas)} 个alpha", flush=True)
                    result_ids = simulate_multis(session_manager, alphas, name, [name])
            
                    # 记录结果
                    if result_ids:
                        for i, alpha_id in enumerate(result_ids):
                            if i < len(unique_ids):
                                unique_id = unique_ids[i]
                                if alpha_id and "ERROR" not in alpha_id:
                                    with open(result_file_path, mode='a') as f:
                                        f.write(f"{alpha_id}|{unique_id}\n")
                                    if alpha_id not in all_results:
                                        all_results.append(alpha_id)
        
                    # 更新批次计数器并打印进度
                    with batch_lock:
                        completed_batches += 1
                        processed_tasks += len(batch)
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[{current_time}] 完成批次 {completed_batches}/{total_batches}，累计处理了 {processed_tasks}/{len(remaining_alphas)} 个任务")
                except Exception as e:
                    print(f"批次任务失败：错误={type(e).__name__}-{str(e)}")
                finally:
                    # 标记批次中所有任务为完成
                    if 'batch' in locals():
                        for _ in batch:
                            task_queue.task_done()
        
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            # 提交工作线程
            futures = [executor.submit(worker, i) for i in range(n_jobs)]
        
            # 等待所有任务完成
            task_queue.join()
        
            # 检查是否有未完成的future
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"线程执行异常: {str(e)}")
        
        # 关闭会话
        try:
            if session_manager.session:
                session_manager.session.close()
        except Exception as e:
            print(f"关闭会话失败: {str(e)}")
        
        retries += 1
        
        print(f"第 {retries} 次尝试完成，当前成功获取{len(all_results)}/{original_alpha_count}个alpha结果")
    
    print(f"完成处理，成功获取{len(all_results)}/{original_alpha_count}个alpha结果")
    return all_results

def simulate_multiple_alphas(alpha_list, name = "optimize_alpha", n_jobs=3):
    tags=[name]
    session = login()  # 使用同步登录
    session_start_time = time.time()
    session_expiry_time = 3 * 60 * 60  # 3小时
    session_manager = SessionManager(session, session_start_time, session_expiry_time)

    chunk_size = (len(alpha_list) + n_jobs - 1) // n_jobs
    task_chunks = [alpha_list[i:i + chunk_size] for i in range(0, len(alpha_list), chunk_size)]
    total_tasks = len(alpha_list)
    start_time = time.time()
    completed_count = 0
    count_lock = threading.Lock()
    all_results = []

    def wrap_task(session_manager, alphas, name, tags):
        nonlocal completed_count
        try:
            # 调用同步函数，接收返回的列表
            result_list = simulate_multis(session_manager, alphas, name, tags)
            with count_lock:  # 使用锁保护共享数据
                return result_list
        except Exception as e:
            print(f"任务失败：alpha={alphas}, 错误={type(e).__name__}-{str(e)}")  # 记录具体错误
            return []
        finally:
            with count_lock:
                completed_count += len(alphas)
                elapsed_time = time.time() - start_time
                average_time = elapsed_time / completed_count if completed_count > 0 else 0
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] 完成了总数 {total_tasks} 中的第 {completed_count} 个任务，平均耗时: {average_time:.2f} 秒")

    # 使用线程池执行任务
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for task_chunk in task_chunks:
            # 获取当前 chunk 对应的 session_manager
            current_session_manager = session_manager
            multi_alphas = to_multi_alphas(task_chunk, 6) 
            for alphas in multi_alphas:
                # 将任务与当前的 session_manager 关联
                future = executor.submit(wrap_task, current_session_manager, alphas, name, tags)
                futures.append(future)
        
        # 使用as_completed可以在任务完成时立即获取结果
        for future in concurrent.futures.as_completed(futures, timeout=6*60*60):
            result = future.result()
            if result:
                all_results.extend(result)
        return all_results


def runStable(s, details, show=True):
    alpha_list=[]
    [alpha_id, sharpe, turnover, fitness, margin, exp, region,  universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]=details
    # 判断是否包含/PV、/ANALYST、/FUNDAMENTAL中的任意一个
    neutralizations = NEUT_DICTS[region]
    print(neutralizations)
    neut_list = [
        {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neut,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': exp
        }
        for neut in neutralizations
    ]
    neut_results = simulate_multiple_alphas_with_retry(neut_list, name=f"optimize_alpha")
    print(f"neut_results: {neut_results}")
    detailed_results = []
    for alpha_id in neut_results:
        if alpha_id == "None":
            continue
        # 从next_ids_details获取详情，包含fitness等指标
        [alpha_id, sharpe, turnover, fitness, margin, exp, region,  universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]=locate_details(s, alpha_id)
        detailed_results.append({
            'alpha_id': alpha_id,
            'sharpe': sharpe,
            'fitness': fitness,
            'neutralization': neutralization
        })
    # 按fitness降序排序，取前三名结果
    length = min(5, int(len(detailed_results)))
    if region == "GLB":
        length = min(4, int(len(detailed_results)))
    sorted_results = sorted(detailed_results, key=lambda x: x['fitness'], reverse=True)[:length]
    neutralization_list = [item['neutralization'] for item in sorted_results]

    has_any_target = any(('/PV' in p or '/ANALYST' in p or '/FUNDAMENTAL' in p) for p in pyramids)
    if has_any_target:
        decaylists=[0,1,3,6,20,30,60,120,240]
    else:
        decaylists=[0,1,3,6,20,30,60]
    alpha_list.extend(
        {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay_tem,
                'neutralization': neut,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': exp
        }
        for decay_tem in decaylists
        for neut in neutralization_list
        )
    print(f"👨‍💻 共生成了 {len(alpha_list)} 因子表达式.")
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"machine_optimize_alpha")
    if show:
        print(f"模拟结果列表：{simulation_results[:100]}") # 限制最多显示100个结果
        drawResults(details, simulation_results)

def runPower(details):
    alpha_list=[]
    [alpha_id, sharpe, turnover, fitness, margin, exp, region,  universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]=details
    powers=[0.2,0.5,0.8,1.2,1.5,2]
    for power in powers:
        new_expr = f"signed_power({exp}, {power})"
        # 将新生成的alpha项添加到扩展列表
        alpha_list.append({
        'type': 'REGULAR',
        'settings': {
            'instrumentType': 'EQUITY',
            'region': region,
            'universe': universe,
            'delay': delay,
            'decay': decay,
            'neutralization': neutralization,
            'truncation': truncation,
            'pasteurization': 'ON',
            'unitHandling': 'VERIFY',
            'nanHandling': 'ON',
            'language': 'FASTEXPR',
            'visualization': False,
            'testPeriod': "P0Y",
            'maxTrade': maxTrade
        },
        'regular': new_expr
    })

    tvrs=["target_tvr=0.2","target_tvr=0.3","target_tvr=0.5","target_tvr=1"]
    for tvr in tvrs:
        new_expr = f"ts_target_tvr_decay({exp}, lambda_min=0, lambda_max=5, {tvr})"
        # 将新生成的alpha项添加到扩展列表
        alpha_list.append({
        'type': 'REGULAR',
        'settings': {
            'instrumentType': 'EQUITY',
            'region': region,
            'universe': universe,
            'delay': delay,
            'decay': decay,
            'neutralization': neutralization,
            'truncation': truncation,
            'pasteurization': 'ON',
            'unitHandling': 'VERIFY',
            'nanHandling': 'ON',
            'language': 'FASTEXPR',
            'visualization': False,
            'testPeriod': "P0Y",
            'maxTrade': maxTrade
        },
        'regular': new_expr
    })


    print(f"👨‍💻 共生成了 {len(alpha_list)} 因子表达式.")
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"optimize_alpha")
    print(f"模拟结果列表：{simulation_results}")
    drawResults(details, simulation_results)

def runTemplate(details):
    alpha_list = []
    [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
    
    template_expressions = template_factory(exp, region)
    event_expressions = eventDriven(exp)
    template_expressions.extend(event_expressions)
    
    # 为每个模板表达式创建alpha配置
    for template_expr in template_expressions:
        alpha_list.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': template_expr
        })
    
    print(f"👨‍💻 共生成了 {len(alpha_list)} 因子表达式.")
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"template_alpha")
    print(f"模拟结果列表：{simulation_results[:100]}") # 限制最多显示100个结果
    saveResults(details, simulation_results)

def runTrade(details):
    """
    实现基于trade_when和trade_act策略的alpha回测
    
    Parameters:
        details: list
            包含alpha详细信息的列表
    """
    [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
    print(f"🚀 开始Trade策略回测: {alpha_id} - {exp}")
    print(f"📊 配置: region={region}, universe={universe}, delay={delay}, neutralization={neutralization}, decay={decay}, truncation={truncation}")
    
    alpha_list = []
    
    # 生成交易策略表达式
    trade_when_expressions = trade_when_factory("trade_when", exp, region, delay)
    trade_act_expressions = trade_act_factory("trade_when", exp, region)
    
    # 合并所有交易策略表达式
    trade_expressions = []
    trade_expressions.extend(trade_when_expressions)
    trade_expressions.extend(trade_act_expressions)
    
    print(f"👨‍💻 共生成了 {len(trade_expressions)} 个交易策略表达式")
    
    # 为每个交易策略表达式创建alpha配置
    for trade_expr in trade_expressions:
        alpha_list.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': trade_expr
        })
    
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"trade_alpha")
    print(f"模拟结果列表：{simulation_results[:100]}") # 限制最多显示100个结果
    
    # 保存结果
    saveResults(details, simulation_results)

FIELDS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'fields')

DATASET_CATEGORY_LIST = ['pv', 'fundamental', 'analyst', 'socialmedia', 'news', 'option', 'model', 'shortinterest', 'institutions', 'other', 'sentiment', 'insiders', 'earnings', 'macro', 'imbalance', 'risk']
_DATASET_CATEGORY_TO_IDS_MAP = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
_ALL_GROUP_FIELDS_CACHE = {}
_INITIALIZED = False

def _download_group_fields(s, region, delay, universe, instrument_type='EQUITY'):
    """下载并保存 group 字段 CSV，供 group_single 模式使用"""
    fields_dir = os.path.join(os.path.dirname(__file__), 'data', 'fields')
    os.makedirs(fields_dir, exist_ok=True)
    group_csv = os.path.join(fields_dir, f'{instrument_type}_{region}_{delay}_{universe}_group.csv')

    print(f"[group_single] 未找到 group 字段文件，开始下载 ({region}/{universe}/delay={delay})...")
    datasetlist = get_datasets(s, instrument_type, region, delay, universe)['id'].tolist()
    group_rows = []
    for dataset_id in datasetlist:
        try:
            df = get_datafields(s, dataset_id=dataset_id, region=region, delay=delay, universe=universe)
            group_data = datafields_tolist(dataset_id, df, isGroup=True)
            group_rows.extend(group_data)
            print(f"  {dataset_id}: {len(group_data)} group 字段")
        except Exception as e:
            print(f"  {dataset_id} 下载失败: {e}")

    if group_rows:
        import pandas as _pd
        df_group = _pd.DataFrame(group_rows, columns=['dataset', 'name', 'description', 'type'])
        df_group[['name', 'dataset']].to_csv(group_csv, index=False)
        print(f"[group_single] 已保存 {len(df_group)} 条 group 字段到 {group_csv}")
    else:
        print("[group_single] 警告：未获取到任何 group 字段")

    # 重置缓存，使 _initialize_group_data 重新加载
    global _INITIALIZED
    _INITIALIZED = False

def _initialize_group_data():
    global _INITIALIZED, _DATASET_CATEGORY_TO_IDS_MAP, _ALL_GROUP_FIELDS_CACHE
    if _INITIALIZED:
        return
    datasets_dir = os.path.join(os.path.dirname(__file__), 'data', 'datasets')
    if os.path.exists(datasets_dir):
        for filename in os.listdir(datasets_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(datasets_dir, filename)
                try:
                    df = pd.read_csv(filepath)
                    for _, row in df.iterrows():
                        if 'id' in row and 'category' in row and 'region' in row and 'delay' in row:
                            dataset_id = row['id']
                            category_json = row['category']
                            region = row['region']
                            delay = int(row['delay'])
                            category_data = json.loads(category_json.replace("'", '"'))
                            category_name = category_data.get('id', '').lower()
                            if category_name in DATASET_CATEGORY_LIST:
                                _DATASET_CATEGORY_TO_IDS_MAP[category_name][region][delay].append(dataset_id)
                except Exception as e:
                    print(f"Error processing dataset file '{filepath}': {e}")
    fields_dir = os.path.join(os.path.dirname(__file__), 'data', 'fields')
    if os.path.exists(fields_dir):
        for root, _, files in os.walk(fields_dir):
            for filename in files:
                if filename.endswith('_group.csv'):
                    filepath = os.path.join(root, filename)
                    try:
                        parts = filename.replace('_group.csv', '').split('_')
                        if len(parts) >= 4:
                            current_region = parts[1]
                            current_delay = int(parts[2])
                            current_universe = '_'.join(parts[3:])
                            df_groups = pd.read_csv(filepath)
                            group_data = []
                            if 'name' in df_groups.columns and 'dataset' in df_groups.columns:
                                for _, row in df_groups.iterrows():
                                    group_data.append((row['name'], row['dataset']))
                            _ALL_GROUP_FIELDS_CACHE[(current_region, current_delay, current_universe)] = group_data
                    except Exception as e:
                        print(f"Error processing group field file '{filepath}': {e}")
    _INITIALIZED = True

def get_category_specific_groups(expr, region, universe, delay, instrumentType, category_filter):
    _initialize_group_data()
    selected_groups = []
    if category_filter:
        lower_category_filter = category_filter.lower()
        dataset_ids_for_category = _DATASET_CATEGORY_TO_IDS_MAP.get(lower_category_filter, {}).get(region, {}).get(delay, [])
        if not dataset_ids_for_category:
            print(f"Warning: No dataset IDs found for category '{lower_category_filter}' in region '{region}' delay '{delay}'.")
            return []
        all_groups_for_config = _ALL_GROUP_FIELDS_CACHE.get((region, delay, universe), [])
        if not all_groups_for_config:
            print(f"Warning: No group fields found for config ({region}, {delay}, {universe}).")
            return []
        for group_expr, dataset_id in all_groups_for_config:
            if dataset_id in dataset_ids_for_category:
                selected_groups.append(group_expr)
        if len(selected_groups) > 100:
            seed = getHashSeed(expr)
            rng = random.Random(seed)
            selected_groups = rng.sample(selected_groups, k=100)
    return sorted(list(set(selected_groups)))

def get_groups_region(expr, region, universe, delay, instrumentType, category_filter=None):
    group_path = f"{FIELDS_PATH}/{instrumentType}_{region}_{delay}_{universe}_group.csv"
    eur_groups = ["bucket(group_rank(io_fund_pct,subindustry), range='0,1,0.1')","bucket(group_rank(io_inst_pct,subindustry), range='0,1,0.1')","bucket(group_rank(io_fund_holding,subindustry), range='0.1,1,0.1')",
    "bucket(group_rank(io_inst_holding,industry), range='0.1,1,0.1')","bucket(group_rank(io_fund_mv,industry), range='0.1,1,0.1')","bucket(group_rank(io_inst_mv,industry), range='0.1,1,0.1')",
    "bucket(group_rank(io_fund_prev_holding,sector), range='0.1,1,0.1')","bucket(group_rank(io_inst_prev_mv,industry), range='0.1,1,0.1')","bucket(group_rank(io_fund_number,sector), range='0.1,1,0.1')",
    "bucket(group_rank(io_inst_number,sector), range='0.1,1,0.1')","bucket(ts_zscore(snt_value,20), range='0,1,0.1')",
    "bucket(group_rank(scl12_buzz, subindustry), range='0,1,0.2')","bucket(ts_mean(snt_value,20), range='0,1,0.2')",
    "bucket(group_rank(rp_css_assets, subindustry), range='0,1,0.1')","bucket(ts_zscore(rp_ess_earnings,20), range='0.1,0.9,0.1')","bucket(group_rank(rp_css_earnings, subindustry), range='0,1,0.1')",
    "bucket(ts_zscore(rp_ess_mna, 20), range='0.1,0.9,0.1')","bucket(rank(ts_delta(vec_avg(nws18_ghc_lna), 5)), range='0.3,0.7,0.1')"]
    eur_groups_2 = [
        "bucket(rank(vec_avg(insd12_mktprice)), range='0,1,0.1')",
        "bucket(rank(vec_avg(insd12_percent)), range='0,1,0.1')",
        "bucket(rank(vec_avg(insd12_positionchangetransactionamount)), range='0,1,0.1')",
        "bucket(rank(vec_avg(insd12_sharesheld)), range='0,1,0.1')",
        "bucket(rank(vec_avg(insd12_transactioncode)), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_mktprice), sector), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_percent), sector), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_positionchangetransactionamount), sector), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_sharesheld), sector), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_transactioncode), sector), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_mktprice), subindustry), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_percent), subindustry), range='0,1,0.1')",
        "bucket(group_rank(vec_avg(insd12_positionchangetransactionamount), subindustry), range='0,1,0.1')",
    ]
    usa_groups = ["bucket(group_rank(io_fund_pct,subindustry), range='0,1,0.1')","bucket(group_rank(io_inst_pct,subindustry), range='0,1,0.1')","bucket(group_rank(io_fund_holding,subindustry), range='0.1,1,0.1')",
    "bucket(group_rank(io_inst_holding,industry), range='0.1,1,0.1')","bucket(group_rank(io_fund_mv,industry), range='0.1,1,0.1')","bucket(group_rank(io_inst_mv,industry), range='0.1,1,0.1')",
    "bucket(group_rank(io_fund_prev_holding,sector), range='0.1,1,0.1')","bucket(group_rank(io_inst_prev_mv,industry), range='0.1,1,0.1')","bucket(group_rank(io_fund_number,sector), range='0.1,1,0.1')",
    "bucket(group_rank(io_inst_number,sector), range='0.1,1,0.1')","bucket(ts_zscore(snt_value,20), range='0,1,0.1')",
    "bucket(group_rank(scl12_buzz, subindustry), range='0,1,0.2')","bucket(ts_mean(snt_value,20), range='0,1,0.2')",
    "bucket(group_rank(rp_css_assets, subindustry), range='0,1,0.1')","bucket(ts_zscore(rp_ess_earnings,20), range='0.1,0.9,0.1')","bucket(group_rank(rp_css_earnings, subindustry), range='0,1,0.1')",
    "bucket(ts_zscore(rp_ess_mna, 20), range='0.1,0.9,0.1')","bucket(rank(ts_delta(vec_avg(nws18_ghc_lna), 5)), range='0.3,0.7,0.1')"]
    usa_groups_2 = ["bucket(rank(imb5_mktcap), range='0.05,1,0.05')",
                    "bucket(group_rank(imb5_mktcap, subindustry), range='0.05,1,0.05')",
                    "bucket(group_rank(imb5_mktcap, industry), range='0.05,1,0.05')",
                    "bucket(group_rank(imb5_mktcap, sector), range='0.05,1,0.05')",
                    "bucket(rank(imb5_score), range='0.05,1,0.05')",
                    "bucket(group_rank(imb5_score, subindustry), range='0.05,1,0.05')",
                    "bucket(group_rank(imb5_score, industry), range='0.05,1,0.05')",
                    "bucket(group_rank(imb5_score, sector), range='0.05,1,0.05')",
                    "bucket(rank(insd3_mun_qca), range='0.05,1,0.05')"]
    usa0_groups = [
    "bucket(rank(vec_avg(ern6_actual_eps_67)), range='0,1,0.1')",
    "bucket(rank(vec_avg(ern6_estimated_eps_68)), range='0,1,0.1')",
    "bucket(group_rank(vec_avg(ern6_actual_eps_67), subindustry), range='0,1,0.1')",
    "bucket(group_rank(vec_avg(ern6_actual_eps_67), sta1_allc10), range='0,1,0.1')",
    "bucket(group_rank(vec_avg(ern6_estimated_eps_68), subindustry), range='0,1,0.1')",
    "bucket(group_rank(vec_avg(ern6_estimated_eps_68), sta1_allc10), range='0,1,0.1')",
    ]
    asi_groups = ["bucket(group_rank(inst14_shortnego, subindustry), range='0.7,1,0.1')","bucket(group_rank(inst14_longnego, subindustry), range='0.7,1,0.1')","bucket(group_rank(inst14_shortnego/inst14_shorttotal, subindustry), range='0,0.3,0.05')","bucket(ts_rank(inst14_longtotal / inst14_shorttotal, 10), range='0.8,1,0.05')",
    "bucket(group_rank(rp_css_assets, subindustry), range='0,1,0.1')","bucket(ts_zscore(rp_ess_earnings,20), range='0.1,0.9,0.1')","bucket(group_rank(rp_css_earnings, subindustry), range='0,1,0.1')",
    "bucket(ts_zscore(rp_ess_mna, 20), range='0.1,0.9,0.1')","bucket(rank(ts_delta(vec_avg(nws18_ghc_lna), 5)), range='0.3,0.7,0.1')","bucket(group_rank(rp_css_earnings, subindustry), range='0.7,1,0.1')"]
    glb_groups = ["bucket(group_rank(ts_mean(vec_avg(nws20_qmb), 3), subindustry), range='0,1,0.1')","bucket(rank(ts_backfill(fnd17_ttmebitd, 252)), range='0.1, 1, 0.1')", "bucket(rank(ts_backfill(fnd17_ttmdebteps, 252)), range='0.1, 1, 0.1')", "bucket(rank(ts_backfill(mdl110_analyst_sentiment, 66)), range='0.1, 1, 0.1')"]
    amr_group1 = ["bucket(rank(imb5_mktcap), range='0.05,1,0.05')",
    "bucket(group_rank(imb5_mktcap, subindustry), range='0.05,1,0.05')",
    "bucket(group_rank(imb5_mktcap, industry), range='0.05,1,0.05')",
    "bucket(group_rank(imb5_mktcap, sector), range='0.05,1,0.05')",
    "bucket(rank(imb5_score), range='0.05,1,0.05')",
    "bucket(group_rank(imb5_score, subindustry), range='0.05,1,0.05')",
    "bucket(group_rank(imb5_score, industry), range='0.05,1,0.05')",
    "bucket(group_rank(imb5_score, sector), range='0.05,1,0.05')"]
    jpn_group = ["bucket(rank(mcr63_weight), range='0,1,0.1')", "bucket(rank(mcr63_membership), range='0,1,0.1')"]
    ind_group1 = ["bucket(rank(vec_avg(ern11_composite_sentiment_score)), range='0,1,0.05')",
    "bucket(group_rank(vec_avg(ern11_composite_sentiment_score), industry), range='0,1,0.05')",
    "bucket(group_rank(vec_avg(ern11_composite_sentiment_score), subindustry), range='0,1,0.05')"]

    all_collected_groups = []
    if int(delay) == 1:
        if region == 'EUR':
            all_collected_groups.extend(eur_groups)
            all_collected_groups.extend(eur_groups_2)
        elif region == 'USA':
            all_collected_groups.extend(usa_groups)
            all_collected_groups.extend(usa_groups_2)
        elif region == 'ASI':
            all_collected_groups.extend(asi_groups)
        elif region == 'GLB':
            all_collected_groups.extend(glb_groups)
        elif region == 'AMR':
            all_collected_groups.extend(amr_group1)
        elif region == 'IND':
            all_collected_groups.extend(ind_group1)
        elif region == 'JPN':
            all_collected_groups.extend(jpn_group)
    else:
        if region == 'USA':
            all_collected_groups.extend(usa0_groups)

    final_groups = []
    if category_filter:
        lower_category_filter = category_filter.lower()
        for group_expr in all_collected_groups:
            if lower_category_filter in group_expr.lower():
                final_groups.append(group_expr)
        if len(final_groups) > 100:
            seed = getHashSeed(expr)
            rng = random.Random(seed)
            final_groups = rng.sample(final_groups, k=100)
        if not final_groups:
            final_groups = all_collected_groups
    else:
        final_groups = all_collected_groups

    if os.path.exists(group_path):
        df = pd.read_csv(group_path)
        seed = getHashSeed(expr)
        df = df.sort_values(by='dataset')
        dataset_groups = df.groupby('dataset')
        for dataset_name, group in dataset_groups:
            seed = getHashSeed(expr)
            sample_size = min(5, len(group))
            selected = group['name'].sample(n=sample_size, random_state=seed).tolist()
            selected = [name for name in selected if not name.startswith('pv64')]
            final_groups.extend(selected)

    return sorted(list(set(final_groups)))

def runGroup(details):
    """
    实现基于分组策略的alpha回测

    Parameters:
        details: list
            包含alpha详细信息的列表
    """
    [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
    print(f"🚀 开始Group策略回测: {alpha_id} - {exp}")
    print(f"📊 配置: region={region}, universe={universe}, delay={delay}, neutralization={neutralization}, decay={decay}, truncation={truncation}")
    
    alpha_list = []    
    groups_region = get_groups_region(exp,region,universe,delay,"EQUITY")
    raw_alphas = list(get_group_second_order_factory([exp], group_ops, groups_region))
    seed = getHashSeed(exp)
    rng = random.Random(seed)
    unique_alphas = list(dict.fromkeys(raw_alphas))

    # 按自然顺序排序（如元素是字符串则按字母序，数值按大小）
    sorted_alphas = sorted(unique_alphas) # 对过滤后的列表进行排序
    run_alphas = rng.sample(sorted_alphas, k=max(1, min(120, len(sorted_alphas))))

    print(f"🔨 生成 {len(run_alphas)} 个分组表达式")
    
    # 4. 为每个分组策略表达式创建alpha配置
    for group_expr in run_alphas:
        alpha_list.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': group_expr
        })
    
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"group_alpha")
    print(f"模拟结果列表：{simulation_results[:100]}") # 限制最多显示100个结果
    
    # 保存结果
    saveResults(details, simulation_results)

def runGroupSingle(details, category_name=None):
    """
    实现基于分组策略的alpha回测 (group_single模式)
    
    Parameters:
        details: list
            包含alpha详细信息的列表
    """
    [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
    print(f"🚀 开始Group Single策略回测: {alpha_id} - {exp}")
    print(f"📊 配置: region={region}, universe={universe}, delay={delay}, neutralization={neutralization}, decay={decay}, truncation={truncation}")

    # 若 group 字段文件不存在，自动下载
    _fields_dir = os.path.join(os.path.dirname(__file__), 'data', 'fields')
    _group_csv = os.path.join(_fields_dir, f'EQUITY_{region}_{delay}_{universe}_group.csv')
    if not os.path.exists(_group_csv):
        _s = login()
        _download_group_fields(_s, region, delay, universe)

    alpha_list = []

    # Pass category_name to get_groups_region

    groups_region = [] # Initialize groups_region
    if category_name == "god":
        # In 'god' mode, directly use the exempted grouping fields as the basis for groups.
        # This bypasses the problematic get_groups_region/get_category_specific_groups functions
        # which were expecting string category names but received lists or inappropriate strings.
        groups_region = ['exchange', 'currency', 'subindustry', 'industry', 'sector', 'market', 'country']
    elif category_name is None:
        groups_region = get_groups_region(exp, region, universe, delay, "EQUITY", category_filter=category_name)
    else: # category_name is a specific category string
        groups_region = get_category_specific_groups(exp, region, universe, delay, "EQUITY", category_name)
        
    raw_alphas = list(get_group_second_order_factory([exp], group_ops, groups_region, isCustom=True))
    print(f"🔍 groups_region={len(groups_region)}, raw_alphas={len(raw_alphas)}")
    seed = getHashSeed(exp)
    rng = random.Random(seed)
    unique_alphas = list(dict.fromkeys(raw_alphas))

    # 过滤：只保留 exp 恰好出现一次的表达式（单group字段，不多重嵌套）
    unique_alphas = [a for a in unique_alphas if a.count(exp) == 1]
    print(f"🔍 单group字段过滤后: {len(unique_alphas)}")

    # 按自然顺序排序
    sorted_alphas = sorted(unique_alphas)
    if not sorted_alphas:
        print("⚠️ 过滤后无可用分组表达式，跳过本次优化")
        return
    run_alphas = rng.sample(sorted_alphas, k=min(100, len(sorted_alphas))) # 从过滤后的列表中采样

    print(f"🔨 生成 {len(run_alphas)} 个分组表达式")
    
    # 4. 为每个分组策略表达式创建alpha配置
    for group_expr in run_alphas:
        alpha_list.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': group_expr
        })
    
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"group_single_alpha")
    print(f"模拟结果列表：{simulation_results[:100]}") # 限制最多显示100个结果
    
    # 保存结果
    saveResults(details, simulation_results)

def runRuntime(details):
    """
    参考diggingStep model=='time'的alpha列表生成模式实现runtime方法
    
    Parameters:
        details: list
            包含alpha详细信息的列表（格式与runGroup等方法一致）
    """
    [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
    print(f"🚀 开始Runtime策略回测: {alpha_id} - {exp}")
    print(f"📊 配置: region={region}, universe={universe}, delay={delay}, neutralization={neutralization}")

    alpha_list = []
    rng = random.Random(getHashSeed(exp))  # 使用与diggingStep相同的哈希种子生成随机数

    # 生成一阶时间序列alpha表达式（模拟diggingStep的first_order_factory逻辑）
    first_order_alphas = list(first_order_factory([exp], ts_ops + basic_ops))  # 假设ts_ops和basic_ops已在当前作用域可用

    # 去重（保留首次出现顺序）
    unique_first_order_alphas = list(dict.fromkeys(first_order_alphas))

    # 添加来自first_self_factory的表达式（假设first_self_factory已定义）
    self_alphas = list(first_self_factory([exp]))

    # 合并所有待模拟的alpha表达式
    all_alphas = unique_first_order_alphas + self_alphas

    print(f"⏳ 生成{len(all_alphas)}个runtime模式alpha表达式")

    # 创建alpha配置列表（与现有方法格式一致）
    for alpha_expr in all_alphas:
        alpha_list.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': alpha_expr
        })

    # 执行模拟（复用现有异步函数）
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"runtime_alpha")
    print(f"✅ 模拟完成，前100个结果：{simulation_results[:100]}")

    # 保存结果（复用现有保存逻辑）
    saveResults(details, simulation_results)

def runRobustSharpe(s, details, show=True):
    # 1. 获取原始Alpha信息
    # [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]
    original_alpha_id, original_sharpe, _, _, _, original_exp, region, universe, original_neutralization, original_decay, delay, original_truncation, maxTrade, _, original_robust_sharpe = details

    print(f"🚀 开始Robust Sharpe优化: {original_alpha_id} - {original_exp}")
    print(f"📊 原始配置: region={region}, universe={universe}, delay={delay}, neutralization={original_neutralization}, decay={original_decay}, truncation={original_truncation}, robust_sharpe={original_robust_sharpe:.2f}, sharpe={original_sharpe:.2f}")

    # 存储所有中间结果，方便调试和最终筛选
    all_results = []

    # --- 阶段1: 中性化方法遍历与初步筛选 ---
    print("\n--- 阶段1: 中性化方法遍历 ---")
    neutralizations = NEUT_DICTS[region] # 获取该地区支持的中性化列表
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

    print(f"👨‍💻 生成了 {len(neut_alpha_configs)} 个中性化配置进行模拟.")
    neut_result_ids = simulate_multiple_alphas_with_retry(neut_alpha_configs, name=f"robust_sharpe_optimized")

    detailed_neut_results = []
    for alpha_id in neut_result_ids:
        if alpha_id == "None":
            continue
        # [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]
        current_details = locate_details(s, alpha_id)
        current_sharpe = current_details[1]
        current_robust_sharpe = current_details[-1]
        current_neutralization = current_details[8]

        if current_sharpe > 0.9:
            detailed_neut_results.append({
                'alpha_id': alpha_id,
                'sharpe': current_sharpe,
                'robust_sharpe': current_robust_sharpe,
                'neutralization': current_neutralization,
                'decay': original_decay,
                'truncation': original_truncation,
                'exp': original_exp # 记录当前使用的表达式
            })
    
    # 严格选择前两个最佳中性化配置
    detailed_neut_results.sort(key=lambda x: x['robust_sharpe'], reverse=True)
    best_neut_configs = detailed_neut_results[:2]
    print(f"✅ 筛选出 {len(best_neut_configs)} 个最佳中性化配置.")
    for cfg in best_neut_configs:
        print(f"   - AlphaId:{cfg['alpha_id']} Neut: {cfg['neutralization']}, Robust Sharpe: {cfg['robust_sharpe']:.2f}, Sharpe: {cfg['sharpe']:.2f}")

    # --- 阶段2: Decay/Truncation参数遍历与进一步筛选 ---
    print("\n--- 阶段2: Decay/Truncation参数遍历 ---")
    best_base_configs = [] # 存储最终选出的最佳中性化、decay、truncation组合

    decay_options = [original_decay, 10, 30, 60] # 示例值，可调整
    truncation_options = [original_truncation, 0.01, 0.03, 0.05] # 示例值，可调整

    for neut_cfg in best_neut_configs:
        current_neutralization = neut_cfg['neutralization']
        decay_trunc_alpha_configs = []
        for decay_val in decay_options:
            for trunc_val in truncation_options:
                config = {
                    'type': 'REGULAR',
                    'settings': {
                        'instrumentType': 'EQUITY',
                        'region': region,
                        'universe': universe,
                        'delay': delay,
                        'decay': decay_val,
                        'neutralization': current_neutralization,
                        'truncation': trunc_val,
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
                decay_trunc_alpha_configs.append(config)
        
        print(f"👨‍💻 为中性化 {current_neutralization} 生成了 {len(decay_trunc_alpha_configs)} 个Decay/Truncation配置进行模拟.")
        decay_trunc_result_ids = simulate_multiple_alphas_with_retry(decay_trunc_alpha_configs, name=f"robust_sharpe_optimized")

        detailed_decay_trunc_results = []
        for alpha_id in decay_trunc_result_ids:
            if alpha_id == "None":
                continue
            current_details = locate_details(s, alpha_id)
            current_sharpe = current_details[1]
            current_robust_sharpe = current_details[-1]
            current_decay = current_details[9]
            current_truncation = current_details[11]

            if current_sharpe > 1.0: # 进一步筛选：alpha sharpe > 1.0
                detailed_decay_trunc_results.append({
                    'alpha_id': alpha_id,
                    'sharpe': current_sharpe,
                    'robust_sharpe': current_robust_sharpe,
                    'neutralization': current_neutralization,
                    'decay': current_decay,
                    'truncation': current_truncation,
                    'exp': original_exp
                })
        
        # 严格选择前两个最佳Decay/Truncation组合
        detailed_decay_trunc_results.sort(key=lambda x: x['robust_sharpe'], reverse=True)
        best_base_configs.extend(detailed_decay_trunc_results[:2])
    
    print(f"✅ 筛选出 {len(best_base_configs)} 个最佳基础配置 (中性化+Decay+Truncation).")
    for cfg in best_base_configs:
        print(f"   - AlphaId:{cfg['alpha_id']} Neut: {cfg['neutralization']}, Decay: {cfg['decay']:.2f}, Trunc: {cfg['truncation']:.2f}, Robust Sharpe: {cfg['robust_sharpe']:.2f}, Sharpe: {cfg['sharpe']:.2f}")
    # 筛选出robust sharpe最好的一个配置
    best_base_configs.sort(key=lambda x: x['robust_sharpe'], reverse=True)
    best_base_configs = best_base_configs[:1]  # 只保留最佳的一个
    # --- 阶段3: 生成优化后的Alpha表达式变体 ---
    print("\n--- 阶段3: 生成优化后的Alpha表达式变体 ---")
    optimized_alpha_variants = []

    # 定义表达式修改的选项
    expression_modifications = [
        ("time_backfill_ts", 75), ("time_backfill_ts", 90),
        ("time_backfill_group", 180), ("time_backfill_group", 275),
        ("add_winsorize", 3),
        ("add_signed_power", 0.5),("add_signed_power", 1.5),("add_signed_power", 2),
        ("add_group_zscore", "sector"), # Assuming 'sector' as default group for zscore
        ("winsorize_std", 3), ("winsorize_std", 5) # Assuming original_std for winsorize was 4, offering alternatives
    ]

    for base_cfg in best_base_configs:
        current_exp = base_cfg['exp']
        current_neutralization = base_cfg['neutralization']
        current_decay = base_cfg['decay']
        current_truncation = base_cfg['truncation']

        # 原始表达式作为基准变体
        optimized_alpha_variants.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': current_decay,
                'neutralization': current_neutralization,
                'truncation': current_truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': current_exp
            # 'original_alpha_id': original_alpha_id # REMOVE THIS LINE
        })

        for mod_type, mod_val in expression_modifications:
            modified_exp = modify_alpha_expression(current_exp, mod_type, mod_val)
            if modified_exp != current_exp: # 确保表达式确实被修改了
                optimized_alpha_variants.append({
                    'type': 'REGULAR',
                    'settings': {
                        'instrumentType': 'EQUITY',
                        'region': region,
                        'universe': universe,
                        'delay': delay,
                        'decay': current_decay,
                        'neutralization': current_neutralization,
                        'truncation': current_truncation,
                        'pasteurization': 'ON',
                        'unitHandling': 'VERIFY',
                        'nanHandling': 'ON',
                        'language': 'FASTEXPR',
                        'visualization': False,
                        'testPeriod': "P0Y",
                        'maxTrade': maxTrade
                    },
                    'regular': modified_exp
                    # 'original_alpha_id': original_alpha_id # REMOVE THIS LINE
                })
    
    print(f"👨‍💻 生成了 {len(optimized_alpha_variants)} 个优化后的Alpha表达式变体进行模拟.")
    optimized_result_ids = simulate_multiple_alphas_with_retry(optimized_alpha_variants, name=f"robust_sharpe_optimized")

    # --- 阶段4: 验证与结果返回 ---
    print("\n--- 阶段4: 验证与结果返回 ---")
    all_final_stage_alphas = [] # New list to store all results
    satisfied_count = 0

    for alpha_id in optimized_result_ids:
        if alpha_id == "None":
            continue
        
        current_details = locate_details(s, alpha_id)
        current_sharpe = current_details[1]
        current_robust_sharpe = current_details[-1]
        current_exp = current_details[5]
        current_neutralization = current_details[8]
        current_decay = current_details[9]
        current_truncation = current_details[11]

        # Get basecheck result (Pass/Fail)
        alpha_detail = get_alpha_byid(s, alpha_id) # get_alpha_byid is imported from machine_lib
        result_basecheck = 'Pass'
        if alpha_detail:
            checks = alpha_detail['is']['checks']
            # Check if any basic checks fail or error
            if any(check.get("result") == "FAIL" or check.get("result") == "ERROR" for check in checks):
                result_basecheck = 'Fail'
            # Additional check for "Weight is too strongly"
            if "Weight is too strongly" in str(checks):
                result_basecheck = 'Fail'

        is_satisfied = (current_robust_sharpe >= 1.0 and current_sharpe > 1.2)
        if is_satisfied:
            satisfied_count += 1

        all_final_stage_alphas.append({
            'alpha_id': alpha_id,
            'optimized_expression': current_exp,
            'neutralization': current_neutralization,
            'decay': current_decay,
            'truncation': current_truncation,
            'robust_sharpe': current_robust_sharpe,
            'sharpe': current_sharpe,
            'basecheck_result': result_basecheck, # Add basecheck result
            'is_satisfied': is_satisfied # Add satisfaction flag
        })
    
    print(f"🎉 成功优化出 {satisfied_count} 个Alpha满足条件.")
    print(f"总共处理了 {len(all_final_stage_alphas)} 个最终阶段的Alpha。")

    if all_final_stage_alphas:
        # Print details for satisfied alphas
        print("\n--- 满足条件的优化Alpha详情 ---")
        for alpha in all_final_stage_alphas:
            if alpha['is_satisfied']:
                print(f"   - Alpha ID: {alpha['alpha_id']}, Robust Sharpe: {alpha['robust_sharpe']:.2f}, Sharpe: {alpha['sharpe']:.2f}")
                print(f"     Expression: {alpha['optimized_expression']}")
                print(f"     Settings: Neut={alpha['neutralization']}, Decay={alpha['decay']:.2f}, Trunc={alpha['truncation']:.2f}")
                print(f"     Basecheck: {alpha['basecheck_result']}")
        
        # Save all results to CSV
        df_results = pd.DataFrame(all_final_stage_alphas)
        save_path = os.path.join("optimize", f"{original_alpha_id}_robust_sharpe_all_results.csv")
        df_results.to_csv(save_path, index=False)
        print(f"\n所有最终阶段的优化结果已保存至：{save_path}")
    else:
        print("未能找到任何最终阶段的优化Alpha。")

    return all_final_stage_alphas # Return all results

def runBasic(details):
    """
    实现基于basic模式的alpha回测
    
    Parameters:
        details: list
            包含alpha详细信息的列表
    """
    [alpha_id, sharpe, turnover, fitness, margin, exp, region, universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
    print(f"🚀 开始Basic策略回测: {alpha_id} - {exp}")
    print(f"📊 配置: region={region}, universe={universe}, delay={delay}, neutralization={neutralization}, decay={decay}, truncation={truncation}")
    
    alpha_list = []
    
    # 1. 生成一阶basic操作符包裹的表达式
    one_layer_alphas = []
    for op1 in basic_ops:
        if f"{op1}(" in exp:
            continue
        one_layer_alphas.append(f"{op1}({exp})")

    # 2. 生成ts_ops包裹的表达式（窗口=5）
    ts_layer_alphas = []
    for ts_op in ts_ops:
        if f"{ts_op}(" in exp:
            continue
        ts_layer_alphas.append(f"{ts_op}({exp}, 5)")

    # 合并所有待模拟的alpha表达式
    all_raw_expressions = [exp] + one_layer_alphas + ts_layer_alphas

    # 去重
    unique_expressions = list(dict.fromkeys(all_raw_expressions))

    # 全部遍历，不抽样
    run_alphas = unique_expressions

    print(f"🔨 生成 {len(run_alphas)} 个Basic模式表达式 (basic_ops:{len(one_layer_alphas)} + ts_ops:{len(ts_layer_alphas)} + 原始:1)")
    
    # 4. 为每个表达式创建alpha配置
    for basic_expr in run_alphas:
        alpha_list.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': basic_expr
        })
    
    # 调用异步函数获取返回列表
    simulation_results = simulate_multiple_alphas_with_retry(alpha_list, name=f"basic_alpha")
    print(f"模拟结果列表：{simulation_results[:100]}") # 限制最多显示100个结果
    
    # 保存结果
    saveResults(details, simulation_results)

def run_rerun_mode(file_path, tag, new_universe=None, new_neutralization=None, min_margin=None):
    """
    读取文件中的alpha_id列表，获取其设置并重新回测，然后打上新标签。
    """
    try:
        # 假设文件每行一个alpha_id，或者是单列的CSV
        df = pd.read_csv(file_path)
        # 如果存在 'sharpe' 列，则按其值从大到小排序
        if 'sharpe' in df.columns:
            df = df.sort_values(by='sharpe', ascending=False)
            print("文件已按 'sharpe' 列从大到小排序。")
        # 按 margin 过滤
        if min_margin is not None and 'margin' in df.columns:
            before = len(df)
            df = df[df['margin'] > min_margin]
            print(f"按 margin > {min_margin} 过滤：{before} -> {len(df)} 条记录。")
        # 按 expression 去重（保留第一个，即 sharpe 最高的）
        if 'expression' in df.columns:
            before = len(df)
            df = df.drop_duplicates(subset='expression', keep='first')
            print(f"按 expression 去重：{before} -> {len(df)} 条记录。")
        alpha_ids = df['alpha_id'].tolist()
    except Exception as e:
        print(f"读取文件 {file_path} 失败: {e}")
        return

    print(f"从 {file_path} 读取到 {len(alpha_ids)} 个alpha_id。")

    s = login()
    alpha_configs = []

    print("正在获取alpha详情...")
    # 使用线程池并行获取详情以加快速度
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        details_list = list(executor.map(lambda alpha_id: locate_details(s, alpha_id), alpha_ids))

    for details in details_list:
        if not details:
            print("获取alpha详情失败，跳过。")
            continue
        
        [alpha_id, sharpe, turnover, fitness, margin, exp, region,  original_universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe] = details
        
        if not exp or not region or not original_universe or neutralization == "":
             print(f"Skipping alpha {alpha_id} due to missing required settings. Full details: {details}")
             continue

        # 决定使用的universe
        final_universe = new_universe if new_universe is not None else original_universe
        if new_universe is not None:
            print(f"Alpha {alpha_id}: 使用新的universe '{new_universe}' (原为 '{original_universe}')")

        # 决定使用的neutralization
        final_neutralization = new_neutralization if new_neutralization is not None else neutralization
        if new_neutralization is not None:
            print(f"Alpha {alpha_id}: 使用新的neutralization '{new_neutralization}' (原为 '{neutralization}')")

        config = {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': final_universe,
                'delay': delay,
                'decay': decay,
                'neutralization': final_neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': "P0Y",
                'maxTrade': maxTrade
            },
            'regular': exp
        }
        alpha_configs.append(config)
    
    if not alpha_configs:
        print("没有可用于回测的alpha配置。")
        return

    print(f"👨‍💻 共生成了 {len(alpha_configs)} 个回测任务，使用标签 '{tag}'。")
    # `name` 参数在 `simulate_multiple_alphas_with_retry` 中被用作标签和结果文件名
    simulation_results = simulate_multiple_alphas_with_retry(alpha_configs, name=tag, is_neut=False)

    print("\n回测完成。生成的新alpha ID:")
    if simulation_results:
        for new_alpha_id in simulation_results:
            print(new_alpha_id)
    else:
        print("没有生成新的alpha ID。")

def doMain(alpha_id, model = "stable", category_name=None):
    s=login()
    details = locate_details(s, alpha_id)
    [alpha_id, sharpe, turnover, fitness, margin, exp, region,  universe, neutralization, decay, delay, truncation, maxTrade, pyramids, robust_sharpe]=details
    # 判断是否包含/PV、/ANALYST、/FUNDAMENTAL中的任意一个
    has_any_target = any(('/PV' in p or '/ANALYST' in p or '/FUNDAMENTAL' in p) for p in pyramids)

    alpha_list=[]
    if model == "stable":
        runStable(s, details)
    elif model == "power":
        runPower(details)
    elif model == "template":
        runTemplate(details)
    elif model == "trade":
        runTrade(details)
    elif model == "group":
        runGroup(details)
    elif model == "group_single" or model == "group_sing":  # 支持简写
        runGroupSingle(details, category_name)
    elif model == "time":
        runRuntime(details)
    elif model == "basic":
        runBasic(details)
    elif model == "robust_sharpe":
        runRobustSharpe(s, details)
    else:
        print(f"❌ 未知的模型类型: '{model}'")
        print("支持的模型类型: stable, power, template, trade, group, group_single (或 group_sing), time, basic, robust_sharpe")
if __name__ == '__main__':
    # 传统方式
    # python optimizeAlpha.py alpha_id [model]

    # 新的方式
    # python optimizeAlpha.py -f path/to/alpha_list.csv -t my_tag -m rerun
    # 解析命令行参数

    parser = argparse.ArgumentParser(description='优化Alpha表达式')
    parser.add_argument('alpha_id', nargs='?', help='Alpha ID')
    parser.add_argument('model', nargs='?', default='stable', help='模型类型：stable, power, template, trade, group, group_single, time, basic, robust_sharpe')
    parser.add_argument('-f', '--file', help='包含alpha ID列表的文件路径')
    parser.add_argument('-t', '--tag', help='应用于alpha的标签')
    parser.add_argument('-m', '--mode', help='执行模式，例如 "rerun"')
    parser.add_argument('-u', '--universe', help='指定一个新的universe来覆盖原始设置')
    parser.add_argument('-n', '--neutralization', help='指定一个新的neutralization来覆盖原始设置')
    parser.add_argument('-c', '--category', help='指定group_single模式下的category名称，用于筛选group类型字段')
    parser.add_argument('-o', '--min-margin', type=float, default=None, help='筛选margin大于该值的alpha（浮点数），不指定则处理全部')
    parser.add_argument('-b', '--batch-size', type=int, default=None, help='单卡槽提交alpha数量（默认自动；1-10）')

    args = parser.parse_args()

    if args.batch_size is not None:
        _BATCH_SIZE_OVERRIDE = max(1, min(args.batch_size, 10))

    # 根据参数决定执行路径
    if args.mode == 'rerun' and args.file and args.tag:
        run_rerun_mode(args.file, args.tag, new_universe=args.universe, new_neutralization=args.neutralization, min_margin=args.min_margin)
    elif args.file and args.tag:
        # 使用文件路径和标签执行新方法
        #run_from_file(args.file, args.tag)
        print(f"使用run_simulation_from_json.py")
    elif args.alpha_id:
        # 使用传统方式执行
        doMain(args.alpha_id, args.model, args.category)
    else:
        print("用法错误: 请提供 alpha_id，或使用 -m rerun -f <file> -t <tag>。")
