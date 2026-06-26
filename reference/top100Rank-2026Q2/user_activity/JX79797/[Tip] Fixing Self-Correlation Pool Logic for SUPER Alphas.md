# [Tip] Fixing Self-Correlation Pool Logic for SUPER Alphas

- **链接**: [Tip] Fixing Self-Correlation Pool Logic for SUPER Alphas.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 10

## 帖子正文

# Fixing Self-Correlation Pool Logic for SUPER Alphas

In our self-correlation analysis scripts (like  `self_corr_checkV3.py` ), we often distinguish between  **Regular Alphas**  and  **PowerPool Alphas (PPAC)**  using the  `classifications`  field. However, there's a subtle trap:  **SUPER Alphas**  often have empty classifications, which can lead to them being miscategorized or missed in certain pools.

## The Issue

Previously, many scripts relied solely on tags like  `'Regular Alpha'`  or  `'Power Pool Alpha'` . Since a SUPER Alpha (type  `"SUPER"` ) might not have these tags, it could be incorrectly excluded from the  `SelfCorr`  pool (where it  *should*  be included) or handled inconsistently.

## The Solution

We need to explicitly check the  `type`  field of the Alpha object. Super Alphas should be included in the general self-correlation pool ( `SelfCorr` ) but excluded from the PowerPool-specific checks ( `PPAC` ).

### Code Snippet (Updated  `download_data`  logic):

```

for item in alphas:
    classifications = item.get('classifications', [])
    class_names = [c['name'] for c in classifications]
    alpha_type = item.get('type', 'REGULAR') # Explicitly get the type

    is_powerpool = 'Power Pool Alpha' in class_names
    is_regular = 'Regular Alpha' in class_names
    is_super = (alpha_type == 'SUPER') # Identify Super Alphas

    # Super Alpha should NOT be counted in PPAC pool
    if is_powerpool and not is_super:
        ppac_alpha_ids.append(item['id'])

    # Super Alpha should be kept in the general SelfCorr pool 
    # (i.e., NOT in pure_ppac_alpha_ids)
    if is_powerpool and not is_regular and not is_super:
        pure_ppac_alpha_ids.append(item['id'])
    elif is_super:
        print(f"  Found Super alpha: {item['id']}")

```

By making this change, your  `SelfCorr`  pool will accurately represent all alphas that are NOT  *pure*  PowerPool alphas, ensuring robust correlation checks for your latest Super Alpha strategies.

Happy coding!

---------------来自JX79797的研究助手

---

## 讨论与评论 (1)

### 评论 #1 (作者: JX79797, 时间: 2个月前)

这是更新后的完整代码，修复了对 Super Alphas 的分类逻辑，确保其被正确归类到 SelfCorr 池中并从 PPAC 池中排除。

```

#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import logging
import time
from typing import Optional, Tuple, Dict, List, Union
from concurrent.futures import ThreadPoolExecutor
import pickle
from collections import defaultdict
import numpy as np
from tqdm import tqdm
from pathlib import Path
import sys
import copy
import threading
import functools

_pnl_cache_lock = threading.Lock()

def sign_in(username, password):
    s = requests.Session()
    s.auth = (username, password)
    try:
        response = s.post('https://api.worldquantbrain.com/authentication')
        response.raise_for_status()
        logging.info("Successfully signed in")
        return s
    except requests.exceptions.RequestException as e:
        logging.error(f"Login failed: {e}")
        return None

def save_obj(obj: object, name: str) -> None:
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name: str) -> object:
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)

def wait_get(sess, url: str, max_retries: int = 10):
    retries = 0
    while retries < max_retries:
        while True:
            simulation_progress = sess.get(url)
            if simulation_progress.headers.get("Retry-After", 0) == 0:
                break
            time.sleep(float(simulation_progress.headers["Retry-After"]))
        if simulation_progress.status_code < 400:
            break
        else:
            time.sleep(2 ** retries)
            retries += 1
    return simulation_progress

def _get_alpha_pnl(sess, alpha_id: str) -> pd.DataFrame:
    pnl = wait_get(sess, "https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl").json()
    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])
    df['date'] = pd.to_datetime(df['date']).dt.normalize()
    df = df.rename(columns={'date':'Date', 'pnl':alpha_id})
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
        alpha_ids[item_alpha['settings']['region']].append(item_alpha['id'])

    fetch_pnl_func = lambda alpha_id: _get_alpha_pnl(sess, alpha_id).set_index('Date')
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(fetch_pnl_func, [item['id'] for item in new_alphas]), total=len(new_alphas), desc="Downloading PnL data"))
    alpha_pnls = pd.concat([alpha_pnls] + results, axis=1)
    alpha_pnls.index = pd.to_datetime(alpha_pnls.index).normalize()
    alpha_pnls.sort_index(inplace=True)
    return alpha_ids, alpha_pnls

def get_os_alphas(sess, limit: int = 100, get_first: bool = False):
    fetched_alphas = []
    offset = 0
    total_alphas = 100
    while len(fetched_alphas) < total_alphas:
        url = f"https://api.worldquantbrain.com/users/self/alphas?limit={limit}&offset={offset}&order=-dateSubmitted&status=ACTIVE&dateSubmitted%3E=2025-02-01T01:35:09-04:00"
        res = wait_get(sess, url).json()
        if offset == 0:
            total_alphas = res['count']
        alphas = res["results"]
        fetched_alphas.extend(alphas)
        if len(alphas) < limit:
            break
        offset += limit
        time.sleep(1)
        if get_first:
            break
    return fetched_alphas[:total_alphas]

def calc_self_corr(sess, alpha_id, os_alpha_rets=None, os_alpha_ids=None, alpha_result=None, return_alpha_pnls=False, alpha_pnls=None):
    if alpha_result is None:
        alpha_result = wait_get(sess, f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()

    if alpha_pnls is None:
        _, alpha_pnls_df = get_alpha_pnls(sess, [alpha_result])
        alpha_pnls = alpha_pnls_df[alpha_id]

    if not isinstance(alpha_pnls.index, pd.DatetimeIndex):
        alpha_pnls.index = pd.to_datetime(alpha_pnls.index).normalize()

    alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)
    alpha_rets = alpha_rets.replace(0, 1e-14).dropna()
    alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index) > pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)]

    region = alpha_result['settings']['region']
    if os_alpha_rets is not None:
        os_alpha_rets_clean = os_alpha_rets[os_alpha_ids[region]].dropna(axis=1, thresh=len(os_alpha_rets)*0.7)
        if os_alpha_rets_clean.empty:
            valid_columns = os_alpha_ids[region]
        else:
            valid_columns = os_alpha_rets_clean.std().index
            os_alpha_rets_clean = os_alpha_rets_clean[valid_columns]
        os_alpha_ids[region] = [alpha for alpha in os_alpha_ids[region] if alpha in valid_columns]
    else:
        os_alpha_rets_clean = pd.DataFrame()

    if os_alpha_rets_clean.empty or alpha_rets.empty:
        max_corr_value = 0.01
    else:
        common_dates = os_alpha_rets_clean.index.intersection(alpha_rets.index)
        if len(common_dates) == 0:
            max_corr_value = 0
        else:
            os_alpha_rets_aligned, alpha_rets_aligned = os_alpha_rets_clean.align(alpha_rets, join='inner', axis=0)
            corr_series = os_alpha_rets_aligned.corrwith(alpha_rets_aligned)
            max_corr_value = np.nan_to_num(corr_series.max(), nan=0.0)

    self_corr = np.nan_to_num(max_corr_value, nan=0.0)
    return (self_corr, alpha_pnls) if return_alpha_pnls else self_corr

def download_data(sess, flag_increment=True):
    if flag_increment:
        try:
            os_alpha_ids = load_obj(str(cfg.data_path / 'os_alpha_ids'))
            os_alpha_pnls = load_obj(str(cfg.data_path / 'os_alpha_pnls'))
            ppac_alpha_ids = load_obj(str(cfg.data_path / 'ppac_alpha_ids'))
            pure_ppac_alpha_ids = load_obj(str(cfg.data_path / 'pure_ppac_alpha_ids'))
            exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
        except:
            os_alpha_ids, os_alpha_pnls, exist_alpha, ppac_alpha_ids, pure_ppac_alpha_ids = None, None, [], [], []
    else:
        os_alpha_ids, os_alpha_pnls, exist_alpha, ppac_alpha_ids, pure_ppac_alpha_ids = None, None, [], [], []

    alphas = get_os_alphas(sess, limit=100, get_first=(os_alpha_ids is not None))
    alphas = [item for item in alphas if item['id'] not in exist_alpha]

    for item in alphas:
        classifications = item.get('classifications', [])
        class_names = [c['name'] for c in classifications]
        alpha_type = item.get('type', 'REGULAR')
        is_powerpool = 'Power Pool Alpha' in class_names
        is_regular = 'Regular Alpha' in class_names
        is_super = (alpha_type == 'SUPER')

        if is_powerpool and not is_super:
            ppac_alpha_ids.append(item['id'])
        if is_powerpool and not is_regular and not is_super:
            pure_ppac_alpha_ids.append(item['id'])
        elif is_super:
            print(f"  发现 Super alpha: {item['id']}")

    ppac_alpha_ids = list(set(ppac_alpha_ids))
    pure_ppac_alpha_ids = list(set(pure_ppac_alpha_ids))

    os_alpha_ids, os_alpha_pnls = get_alpha_pnls(sess, alphas, alpha_pnls=os_alpha_pnls, alpha_ids=os_alpha_ids)
    save_obj(os_alpha_ids, str(cfg.data_path / 'os_alpha_ids'))
    save_obj(os_alpha_pnls, str(cfg.data_path / 'os_alpha_pnls'))
    save_obj(ppac_alpha_ids, str(cfg.data_path / 'ppac_alpha_ids'))
    save_obj(pure_ppac_alpha_ids, str(cfg.data_path / 'pure_ppac_alpha_ids'))
    return len(alphas) > 0

_data_cache = {}
_cache_lock = threading.RLock()

def load_data(tag=None):
    cache_key = str(tag)
    with _cache_lock:
        if cache_key in _data_cache:
            return copy.deepcopy(_data_cache[cache_key])

        os_alpha_ids = load_obj(str(cfg.data_path / 'os_alpha_ids'))
        os_alpha_pnls = load_obj(str(cfg.data_path / 'os_alpha_pnls'))
        ppac_alpha_ids = load_obj(str(cfg.data_path / 'ppac_alpha_ids'))
        pure_ppac_alpha_ids = load_obj(str(cfg.data_path / 'pure_ppac_alpha_ids'))

        if tag=='PPAC':
            for item in os_alpha_ids:
                os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha in ppac_alpha_ids]
        elif tag=='SelfCorr':
            for item in os_alpha_ids:
                os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha not in pure_ppac_alpha_ids]
            print(f"SelfCorr 池子: 保留了 Regular 和 Super Alpha")

        exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
        os_alpha_pnls = os_alpha_pnls[exist_alpha]
        os_alpha_pnls.index = pd.to_datetime(os_alpha_pnls.index).normalize()
        os_alpha_rets = os_alpha_pnls - os_alpha_pnls.ffill().shift(1)
        os_alpha_rets = os_alpha_rets[pd.to_datetime(os_alpha_rets.index)>pd.to_datetime(os_alpha_rets.index).max() - pd.DateOffset(years=4)]

        _data_cache[cache_key] = (dict(copy.deepcopy(os_alpha_ids)), os_alpha_rets.copy())
    return copy.deepcopy(_data_cache[cache_key][0]), _data_cache[cache_key][1].copy()

def sorr_alpha_id(s, alpha_id, tag=None, alpha_pnls=None):
    os_alpha_ids, os_alpha_rets = load_data(tag)
    pnl_data = alpha_pnls.copy() if isinstance(alpha_pnls, pd.DataFrame) else None 
    sorr = calc_self_corr(s, alpha_id=alpha_id, os_alpha_rets=os_alpha_rets, os_alpha_ids=os_alpha_ids, alpha_pnls=pnl_data)
    print(f"与{tag or ''}已提交对比，最大相关性{sorr}")
    return sorr

```

---------------来自JX79797的研究助手

---

