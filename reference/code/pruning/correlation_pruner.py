import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any, Union

logger = logging.getLogger(__name__)

def calculate_correlation_matrix(pnl_dfs: List[pd.DataFrame], lookback_years: float = 4.0) -> pd.DataFrame:
    """
    根据传入的多个 Alpha PnL DataFrames，计算两两之间的时序日收益率相关性矩阵。
    每个 PnL DataFrame 应当包含 'Date'（作为索引或列）以及以 Alpha ID 为名的 PnL 累计值列。
    """
    if len(pnl_dfs) < 2:
        raise ValueError("计算相关性矩阵至少需要 2 个 Alpha 的 PnL 数据")

    # 规范化并以 Date 作为索引合并
    processed_dfs = []
    for df in pnl_dfs:
        df_copy = df.copy()
        if 'Date' in df_copy.columns:
            df_copy = df_copy.set_index('Date')
        # 确保索引是 DatetimeIndex
        df_copy.index = pd.to_datetime(df_copy.index)
        processed_dfs.append(df_copy)

    # 按照 Date 的 inner join 合并所有 PnL (仅保留共有日期)
    combined_pnl = pd.concat(processed_dfs, axis=1, join='inner')
    if combined_pnl.empty or len(combined_pnl) < 2:
        raise ValueError("所有 Alpha 之间没有足够的共有交易日期，无法计算相关性")

    # 筛选指定时间窗口内的数据
    max_date = combined_pnl.index.max()
    cutoff_date = max_date - pd.DateOffset(years=lookback_years)
    combined_pnl = combined_pnl[combined_pnl.index > cutoff_date]

    # 计算日收益率 (rets = pnl_t - pnl_{t-1})
    combined_rets = combined_pnl - combined_pnl.ffill().shift(1)
    combined_rets = combined_rets.dropna()

    if len(combined_rets) < 2:
        raise ValueError(f"在过去 {lookback_years} 年的共有时间窗口内数据点不足，无法计算")

    # 计算皮尔逊相关性矩阵
    return combined_rets.corr()

def prune_by_correlation(correlation_matrix: pd.DataFrame, 
                         alphas: Union[pd.DataFrame, List[Dict[str, Any]]], 
                         corr_threshold: float = 0.7,
                         sharpe_col: str = "sharpe",
                         fitness_col: str = "fitness",
                         margin_col: str = "margin") -> List[str]:
    """
    结合自相关性矩阵对 Alpha 进行贪心剪枝。
    
    算法流程：
    1. 计算每个 Alpha 的综合得分 (0.5 * fitness + 0.5 * margin)；如果 margin 缺失或不存在，则以 fitness 替代；如果 fitness 缺失则以 sharpe 替代。
    2. 将 Alpha 按综合得分从高到低排序。
    3. 依次遍历 Alpha：如果它与任何已经入选的 Alpha 的相关系数 >= corr_threshold，则剔除；否则，将其加入入选列表。
    
    参数:
        correlation_matrix: pd.DataFrame，行/列均为 Alpha ID 的对称相关性矩阵
        alphas: pd.DataFrame 或包含字典的列表，每个元素含有 alpha_id / sharpe / fitness / margin 等指标
        corr_threshold: 最大允许的相关性阈值，默认 0.7
        
    返回:
        List[str]: 筛选后保留的 Alpha ID 列表
    """
    if correlation_matrix.empty:
        return []

    # 转换输入格式为统一的 dict list
    alpha_records = []
    if isinstance(alphas, pd.DataFrame):
        alpha_records = alphas.to_dict(orient="records")
    else:
        alpha_records = [dict(a) for a in alphas]

    if not alpha_records:
        return []

    # 提取得分并进行降序排序
    scored_alphas = []
    for a in alpha_records:
        alpha_id = a.get("alpha_id") or a.get("id")
        if not alpha_id or alpha_id not in correlation_matrix.index:
            continue
            
        sharpe = float(a.get(sharpe_col) or 0.0)
        fitness = float(a.get(fitness_col) or 0.0)
        
        # 兼容处理 margin 格式 (支持百分比/万分比字符串或浮点数)
        margin_val = a.get(margin_col)
        margin = 0.0
        if margin_val is not None:
            try:
                if isinstance(margin_val, str):
                    cleaned_margin = margin_val.replace('ⱱ', '').replace('%', '').strip()
                    margin = float(cleaned_margin)
                else:
                    margin = float(margin_val)
            except ValueError:
                margin = 0.0

        # 综合评分逻辑：默认以 (fitness + margin) 进行得分衡量，如果没有则回退
        if fitness > 0 and margin > 0:
            score = 0.5 * fitness + 0.5 * margin
        elif fitness > 0:
            score = fitness
        else:
            score = abs(sharpe)

        scored_alphas.append({
            "id": alpha_id,
            "score": score,
            "sharpe": sharpe
        })

    # 按照综合得分降序排列
    scored_alphas.sort(key=lambda x: x["score"], reverse=True)

    selected_ids = []
    for item in scored_alphas:
        aid = item["id"]
        conflict = False
        for selected_id in selected_ids:
            # 查找相关系数值
            corr = correlation_matrix.loc[aid, selected_id]
            if pd.isna(corr):
                corr = 0.0
                
            if abs(corr) >= corr_threshold:
                conflict = True
                break
                
        if not conflict:
            selected_ids.append(aid)

    return selected_ids
