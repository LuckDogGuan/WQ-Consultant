# Osmosis 给你100000美金，每个alpha买多少？分享4种给自己alpha池打分的方案-打完就飙升经验分享

- **链接**: [Commented] Osmosis 给你100000美金每个alpha买多少分享4种给自己alpha池打分的方案-打完就飙升经验分享.md
- **作者**: CC21336
- **发布时间/热度**: 6个月前, 得票: 32

## 帖子正文

今天看了课代表@ **XX42289**  分享的《CA 降维 + 多指标聚类数评判 Osmosis 点数分配工具》，也看了@ [JR23144](/hc/zh-cn/profiles/28844048981143-JR23144) 【贺六浑】-【工具配置】OC2025 一键清空分数脚本，写的两篇帖子都非常实用。拜读两位大佬的帖子后，也准备给自己的alpha写个打分策略。

Osmosis 比赛，包括USA, EUR, ASI, GLB, IND共5个地区，每个Region总分100000分，你首先需要挑选独特的，优异的alpha建立一个池子，池中至少包含10个alpha，再对池中alpha采用一定的策略，对每个alpha进行分数分配。也可以理解为100000美金，你打算对自己的池中alpha每个买多少？注意总额度不能超过100000美金，如果超过总额则可能面临比赛资格被取消。

下面是我的4种打分分配方案，给大家下注提供一个参考，抛砖引玉。该思路基于多维度指标进行综合评价，基于7个关键指标（fitness、returns、margin、sharpe、drawdown、turnover、多空平衡）计算综合得分,将100,000总分分配给每个Alpha。

Alpha分配分数（总分为100000）。

对每个Alpha计算综合得分，考虑以下指标：

指标优劣：fitness（越大越好） returns（越大越好） margin（越大越好） sharpe（越大越好） drawdown（越小越好） turnover（理想区间8%-20%） 多空平衡（longCount和shortCount越接近越好）

四种分配方法，概括如下：

① Softmax分配法：

基于综合得分的指数概率分布，高分Alpha获得指数级更多分数，适合突出表现优异的Alpha。

② Rank分配法：

基于排名进行指数衰减分配，保证每个Alpha都有基础分数，公平性强，适合追求稳健和公平性的场景。

③ Cluster加权法：

先聚类再分配，确保不同类型Alpha都能获得分数，鼓励策略多样性，适合希望覆盖多种策略的场景。

④ Weighted混合法：

多种方法的加权组合，灵活平衡各方法优点，适合需要综合考量多种因素的场景。

我打完分即刻223飙升第2，相信大佬们的alpha池更好更优异，赶紧试一试吧。

![图片](images/img_ef6362229e.png)

预祝大家买入大赚，榜上有名。

代码如下：

```
# Import Libraryfromalphalib.machine_libimport*import urllib.parseimport loggingimport numpy as npimport pandas as pdfrom datetime import datetimefrom scipy.stats import rankdatafrom sklearn.preprocessing import RobustScalerfrom sklearn.cluster import KMeansfrom sklearn.decomposition import PCAdef get_history_alpha_ids(s, region, start_date, limit=50, offset=0):    """    从接口分页获取指定地区、指定日期后的alpha数据    """    alphas_data = []    start_date_str = urllib.parse.quote(start_date.astimezone().isoformat(timespec='seconds'))    while True:        url = (            f"https://api.worldquantbrain.com/users/self/alphas?"            f"limit={limit}&offset={offset}"            f"&dateCreated%3E={start_date_str}"            f"&settings.region={region}"            f"&status!=UNSUBMITTED%1FIS-FAIL"            f"&hidden=false"            f"&type!=SUPER"            f"&order=-dateSubmitted"        )        try:            resp = s.get(url)            if resp.status_code != 200:                logging.error(f"请求出错，状态码：{resp.status_code}")                break            data = resp.json()            results = data.get("results", [])            alphas_data.extend(results)            if offset + len(results) >= data.get("count", 0) or len(results) < limit:                break            offset += limit        except Exception as e:            logging.error(f"数据获取异常: {e}")            break    if not alphas_data:        logging.warning("没有获取到alpha数据")        return []    # 提取需要的指标数据    alpha_metrics = []    for item in alphas_data:        is_data = item.get('is', {})        metrics = {            'id': item['id'],            'fitness': is_data.get('fitness', 0.0),            'longCount': is_data.get('longCount', 0.0),            'shortCount': is_data.get('shortCount', 0.0),            'turnover': is_data.get('turnover', 0.0),            'returns': is_data.get('returns', 0.0),            'drawdown': is_data.get('drawdown', 0.0),            'margin': is_data.get('margin', 0.0),            'sharpe': is_data.get('sharpe', 0.0)        }        alpha_metrics.append(metrics)    return alpha_metricsdef calculate_turnover_score(turnover):    """    计算turnover得分，理想区间为8-20%    """    if pd.isna(turnover):        return 0.5       ideal_center = 14.0    ideal_min = 8.0    ideal_max = 20.0       if ideal_min <= turnover <= ideal_max:        distance = abs(turnover - ideal_center) / (ideal_max - ideal_min)        score = 1.0 - distance    elif turnover < ideal_min:        score = max(0, turnover / ideal_min)    else:        # 防止除零错误        score = max(0, 1.0 - (turnover - ideal_max) / (4 * ideal_max)) if ideal_max > 0 else 0       return max(0, min(1, score))def calculate_balance_score(long_count, short_count):    """    计算多空平衡得分    """    if pd.isna(long_count) or pd.isna(short_count):        return 0.5       if long_count == 0 and short_count == 0:        return 0.0       if long_count == 0 or short_count == 0:        return 0.2       ratio = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) > 0 else 0    balance_score = ratio ** 0.5 if ratio >= 0 else 0       return min(1, max(0, balance_score))def calculate_alpha_scores(alpha_metrics, weights=None):    """    为每个alpha计算综合得分    """    if not alpha_metrics:        logging.warning("没有alpha数据用于计算得分")        return pd.DataFrame()       df = pd.DataFrame(alpha_metrics)       # 检查必要的列是否存在    required_columns = ['fitness', 'returns', 'margin', 'sharpe', 'drawdown', 'turnover', 'longCount', 'shortCount']    missing_columns = [col for col in required_columns if col not in df.columns]    if missing_columns:        logging.warning(f"缺失列: {missing_columns}，使用默认值填充")        for col in missing_columns:            df[col] = 0.0       # 默认权重配置    if weights is None:        weights = {            'fitness': 0.25,            'returns': 0.20,            'margin': 0.15,            'sharpe': 0.20,            'drawdown': 0.10,            'turnover': 0.05,            'balance': 0.05,        }       # 归一化越大越好的指标    for col in ['fitness', 'returns', 'margin', 'sharpe']:        if len(df) > 1 and df[col].nunique() > 1:            df[f'{col}_score'] = rankdata(df[col].fillna(0)) / len(df)        else:            df[f'{col}_score'] = 0.5       # 处理drawdown(越小越好)    if 'drawdown' in df.columns and len(df) > 1 and df['drawdown'].nunique() > 1:        neg_drawdown = -df['drawdown'].fillna(df['drawdown'].max() if df['drawdown'].max() > 0 else 1)        df['drawdown_score'] = rankdata(neg_drawdown) / len(df)    else:        df['drawdown_score'] = 0.5       # 处理turnover    df['turnover_score'] = df['turnover'].apply(lambda x: calculate_turnover_score(x))       # 计算多空平衡得分    df['balance_score'] = df.apply(lambda row: calculate_balance_score(row['longCount'], row['shortCount']), axis=1)       # 计算综合得分    df['composite_score'] = (        weights['fitness'] * df['fitness_score'] +        weights['returns'] * df['returns_score'] +        weights['margin'] * df['margin_score'] +        weights['sharpe'] * df['sharpe_score'] +        weights['drawdown'] * df['drawdown_score'] +        weights['turnover'] * df['turnover_score'] +        weights['balance'] * df['balance_score']    )       # 归一化到[0,1]    if len(df) > 1 and df['composite_score'].nunique() > 1:        score_min = df['composite_score'].min()        score_max = df['composite_score'].max()        if score_max > score_min:            df['composite_score'] = (df['composite_score'] - score_min) / (score_max - score_min)        else:            df['composite_score'] = 0.5    else:        df['composite_score'] = 0.5       return dfdef assign_scores_with_softmax(df, total_score=100000, temperature=0.1):    """    使用softmax函数分配分数    """    if len(df) == 0:        return df       # 防止温度参数为0    temperature = max(temperature, 1e-10)       # 使用softmax计算概率分布    scores = df['composite_score'].values    exp_scores = np.exp(scores / temperature)    probabilities = exp_scores / exp_scores.sum()       # 分配分数    df['assigned_score'] = np.floor(probabilities * total_score).astype(int)       # 处理四舍五入偏差    score_diff = total_score - df['assigned_score'].sum()    if score_diff > 0:        top_indices = df.nlargest(min(score_diff, len(df)), 'composite_score').index        df.loc[top_indices, 'assigned_score'] += 1    elif score_diff < 0:        bottom_indices = df.nsmallest(min(abs(score_diff), len(df)), 'composite_score').index        for idx in bottom_indices:            if df.at[idx, 'assigned_score'] > 1:                df.at[idx, 'assigned_score'] -= 1                score_diff += 1                if score_diff == 0:                    break       return dfdef assign_scores_with_rank_based(df, total_score=100000, min_score=100):    """    基于排名的分数分配方法    """    if len(df) == 0:        return df       n = len(df)    min_score = max(1, min_score)  # 确保最小分数为正       # 计算基础分配    base_allocation = min_score * n    if base_allocation > total_score:        # 如果基础分数总和超过总分，按比例缩减        scale_factor = total_score / base_allocation        df['assigned_score'] = (min_score * scale_factor).astype(int)        return df       # 分配剩余分数    remaining_score = total_score - base_allocation    ranks = rankdata(df['composite_score'])       # 使用指数权重    weights = np.exp(ranks / n)    normalized_weights = weights / weights.sum()    bonus_scores = np.floor(normalized_weights * remaining_score).astype(int)       # 分配分数    df['assigned_score'] = min_score + bonus_scores       # 调整总分    score_diff = total_score - df['assigned_score'].sum()    if score_diff != 0:        # 将偏差加到最高得分的alpha        top_idx = df['composite_score'].idxmax()        df.at[top_idx, 'assigned_score'] += score_diff       return dfdef assign_scores_with_cluster_weighting(df, use_pca=True, total_score=100000):    """    结合聚类和综合得分的分数分配方法    """    if len(df) < 2:        df['assigned_score'] = total_score        return df       # 检查聚类特征列    feature_cols = ['returns', 'margin', 'sharpe', 'drawdown', 'turnover']    available_features = [col for col in feature_cols if col in df.columns]       if len(available_features) < 2:        logging.warning("聚类特征不足，使用softmax方法")        return assign_scores_with_softmax(df, total_score)       # 准备特征数据    X = df[available_features].fillna(0).values       try:        scaler = RobustScaler()        X_scaled = scaler.fit_transform(X)               if use_pca and len(available_features) > 2:            pca = PCA(n_components=min(0.95, len(available_features)), random_state=42)            X_processed = pca.fit_transform(X_scaled)        else:            X_processed = X_scaled               # 确定聚类数        n_samples = len(df)        n_clusters = min(20, max(2, n_samples // 5))  # 每5个样本一个聚类        n_clusters = min(n_clusters, n_samples)               if n_clusters < 2:            df['cluster'] = 0        else:            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)            df['cluster'] = kmeans.fit_predict(X_processed)       except Exception as e:        logging.warning(f"聚类失败: {e}，使用softmax方法")        return assign_scores_with_softmax(df, total_score)       # 为每个聚类分配基础分数    cluster_sizes = df['cluster'].value_counts()    cluster_base_scores = (cluster_sizes / len(df) * total_score * 0.3).astype(int)       # 在每个聚类内分配分数    df['assigned_score'] = 0       for cluster_id, size in cluster_sizes.items():        cluster_mask = df['cluster'] == cluster_id        cluster_df = df[cluster_mask].copy()               if len(cluster_df) == 0:            continue                   # 聚类基础分数        base_for_cluster = cluster_base_scores.get(cluster_id, 0)               if base_for_cluster > 0:            # 在聚类内按综合得分分配基础分数            cluster_scores = cluster_df['composite_score'].values            if cluster_scores.sum() > 0:                base_weights = cluster_scores / cluster_scores.sum()            else:                base_weights = np.ones(len(cluster_df)) / len(cluster_df)                       base_allocations = np.floor(base_weights * base_for_cluster).astype(int)                       # 处理余数            remainder = base_for_cluster - base_allocations.sum()            if remainder > 0:                top_indices = cluster_df.nlargest(remainder, 'composite_score').index                base_allocations[cluster_df.index.isin(top_indices)] += 1                       cluster_df['assigned_score'] = base_allocations               # 更新主DataFrame        df.loc[cluster_mask, 'assigned_score'] = cluster_df['assigned_score'].values       # 按综合得分分配剩余分数    total_assigned = df['assigned_score'].sum()    remaining_total = total_score - total_assigned       if remaining_total > 0:        scores = df['composite_score'].values        if scores.sum() > 0:            weights = scores / scores.sum()        else:            weights = np.ones(len(df)) / len(df)               bonus_allocations = np.floor(weights * remaining_total).astype(int)        df['assigned_score'] += bonus_allocations               # 处理余数        total_assigned = df['assigned_score'].sum()        remaining_total = total_score - total_assigned        if remaining_total > 0:            top_indices = df.nlargest(remaining_total, 'composite_score').index            df.loc[top_indices, 'assigned_score'] += 1       return dfdef assign_scores_weighted_combination(df, total_score=100000,                                       weights=None, cluster_weight=0.3,                                       softmax_temp=0.1, min_base_score=50):    """    加权组合分配方法    """    if len(df) == 0:        return df       if weights is None:        weights = {'softmax': 0.4, 'rank': 0.3, 'cluster': 0.3}       # 计算各种方法的分数    df_softmax = assign_scores_with_softmax(df.copy(), total_score, softmax_temp)    df_rank = assign_scores_with_rank_based(df.copy(), total_score, min_base_score)       # 计算加权分数    weighted_scores = (        weights['softmax'] * df_softmax['assigned_score'] +        weights['rank'] * df_rank['assigned_score']    )       # 添加聚类调整    if cluster_weight > 0 and len(df) > 1:        try:            feature_cols = ['returns', 'margin', 'sharpe', 'drawdown', 'turnover']            available_features = [col for col in feature_cols if col in df.columns]                       if len(available_features) >= 2:                X = df[available_features].fillna(0).values                scaler = RobustScaler()                X_scaled = scaler.fit_transform(X)                               n_clusters = min(20, max(2, len(df) // 5))                if n_clusters > 1:                    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)                    clusters = kmeans.fit_predict(X_scaled)                                       # 计算聚类调整因子                    for i in range(n_clusters):                        cluster_mask = clusters == i                        cluster_size = np.sum(cluster_mask)                        if cluster_size > 0:                            cluster_factor = 1.0 / np.sqrt(cluster_size)                            weighted_scores[cluster_mask] *= (1 + cluster_weight * cluster_factor)        except Exception as e:            logging.warning(f"聚类调整失败: {e}")       # 归一化到总分    total_weighted = weighted_scores.sum()    if total_weighted > 0:        df['assigned_score'] = (weighted_scores / total_weighted * total_score).astype(int)    else:        df['assigned_score'] = (total_score // len(df))       # 调整总分    total_assigned = df['assigned_score'].sum()    diff = total_score - total_assigned       if diff != 0:        sorted_indices = df.sort_values('composite_score', ascending=False).index        adjust_count = min(abs(diff), len(df))               for i in range(adjust_count):            idx = sorted_indices[i]            if diff > 0:                df.at[idx, 'assigned_score'] += 1            else:                df.at[idx, 'assigned_score'] = max(1, df.at[idx, 'assigned_score'] - 1)       return dfdef assign_scores_hybrid(df, method='softmax', total_score=100000, **kwargs):    """    混合分配方法    """    if method == 'softmax':        temperature = kwargs.get('temperature', 0.1)        return assign_scores_with_softmax(df, total_score, temperature)       elif method == 'rank':        min_score = kwargs.get('min_score', 100)        return assign_scores_with_rank_based(df, total_score, min_score)       elif method == 'cluster':        use_pca = kwargs.get('use_pca', True)        return assign_scores_with_cluster_weighting(df, use_pca, total_score)       elif method == 'weighted':        return assign_scores_weighted_combination(df, total_score, **kwargs)       else:        raise ValueError(f"未知的分配方法: {method}")'''四种分配方法，概括如下：Softmax分配法：基于综合得分的指数概率分布，高分Alpha获得指数级更多分数，适合突出表现优异的Alpha。Rank分配法：基于排名进行指数衰减分配，保证每个Alpha都有基础分数，公平性强，适合追求稳健和公平性的场景。Cluster加权法：先聚类再分配，确保不同类型Alpha都能获得分数，鼓励策略多样性，适合希望覆盖多种策略的场景。Weighted混合法：多种方法的加权组合，灵活平衡各方法优点，适合需要综合考量多种因素的场景。'''def main():    """主函数"""    # 配置参数,成为正式顾问的日期    advisor_date = datetime(2025, 3, 11)    page_limit = 100    page_offset = 0    target_region = "GLB"  # USA, EUR, ASI, GLB, IND    # 分配方法配置    ALLOCATION_METHOD = 'weighted'  # softmax, rank, cluster, weighted    # 总分(资金总额度)    TOTAL_SCORE = 100000       # 方法参数配置    METHOD_CONFIG = {        'softmax': {'temperature': 0.1},        'rank': {'min_score': 100},        'cluster': {'use_pca': True},        'weighted': {            'weights': {'softmax': 0.4, 'rank': 0.3, 'cluster': 0.3},            'cluster_weight': 0.3        }    }       # 初始化登录会话    try:        session = login()        logging.info("登录成功，开始获取alpha数据")    except Exception as e:        logging.error(f"登录失败: {e}")        return       '''    注意：    这里是获取成为顾问后所配置target_region中所有alpha数据    后续你需要根据自己的理解需求建立自己独特优异的分配池进行打分    '''    #获取成为顾问后所配置地区所有alpha数据    alpha_metrics_list = get_history_alpha_ids(        s=session,        region=target_region,        start_date=advisor_date,        limit=page_limit,        offset=page_offset    )    if not alpha_metrics_list:        logging.error("未获取到有效alpha数据")        return       print(f"共获取到 {len(alpha_metrics_list)} 个alpha")       # 计算综合得分    df_scores = calculate_alpha_scores(alpha_metrics_list)    if df_scores.empty:        logging.error("无法计算alpha综合得分")        return       # 分配分数    print(f"\n使用 {ALLOCATION_METHOD} 方法进行分数分配...")    try:        df_with_scores = assign_scores_hybrid(            df_scores,            method=ALLOCATION_METHOD,            total_score=TOTAL_SCORE,            **METHOD_CONFIG.get(ALLOCATION_METHOD, {})        )    except Exception as e:        logging.error(f"分数分配失败: {e}")        return       # 输出结果    print(f"\n{'='*60}")    print(f"最终分配结果（使用{ALLOCATION_METHOD}方法）")    print(f"{'='*60}")       total_assigned = 0    successful_updates = 0    failed_updates = 0       # 按分配分数排序    df_with_scores = df_with_scores.sort_values('assigned_score', ascending=False)       # 输出每个Alpha的分配结果    for idx, alpha in df_with_scores.iterrows():        print(f"Alpha ID: {alpha['id']}")        print(f"  综合得分: {alpha['composite_score']:.4f} (排名: {idx+1}/{len(df_with_scores)})")        print(f"  分配分数: {alpha['assigned_score']}")               # 调用API更新分数        update_url = f"https://api.worldquantbrain.com/alphas/{alpha['id']}"        try:            response = session.patch(update_url, json={"osmosisPoints": int(alpha['assigned_score'])})            if response.status_code == 200:                successful_updates += 1                print(f"  ✓ 分数更新成功")            else:                failed_updates += 1                print(f"  ✗ 分数更新失败: {response.status_code}")        except Exception as e:            failed_updates += 1            print(f"  ✗ 更新异常: {str(e)}")               total_assigned += alpha['assigned_score']       # 统计信息    print(f"\n{'='*60}")    print("分配统计")    print(f"{'='*60}")    print(f"总alpha数量: {len(df_with_scores)}")    print(f"总分配分数: {total_assigned}")    print(f"平均分数: {total_assigned/len(df_with_scores):.0f}")    print(f"最高分数: {df_with_scores['assigned_score'].max()}")    print(f"最低分数: {df_with_scores['assigned_score'].min()}")    print(f"中位数分数: {df_with_scores['assigned_score'].median():.0f}")    print(f"分数标准差: {df_with_scores['assigned_score'].std():.0f}")       if df_with_scores['assigned_score'].mean() > 0:        cv = df_with_scores['assigned_score'].std() / df_with_scores['assigned_score'].mean()        print(f"变异系数: {cv:.3f}")       print(f"API更新成功: {successful_updates} 个")    print(f"API更新失败: {failed_updates} 个")       # 分数分布    print(f"\n{'='*60}")    print("分数分布")    print(f"{'='*60}")       score_bins = [0, 1000, 2000, 3000, 5000, 10000, float('inf')]    bin_labels = ['<1000', '1000-2000', '2000-3000', '3000-5000', '5000-10000', '>10000']       df_with_scores['score_bin'] = pd.cut(df_with_scores['assigned_score'], bins=score_bins, labels=bin_labels)    bin_counts = df_with_scores['score_bin'].value_counts().sort_index()       for bin_label, count in bin_counts.items():        percentage = count/len(df_with_scores)*100        bar_length = int(percentage/2)        bar = '█' * bar_length if bar_length > 0 else ''        print(f"{bin_label}: {count:3d}个alpha ({percentage:5.1f}%) {bar}")if __name__ == '__main__':    # 配置日志    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')       # 运行主函数    main()
```

---

## 讨论与评论 (27)

### 评论 #1 (作者: LG87838, 时间: 6个月前)

感谢分享，有没有像我这样1个alpha也没有分配的？

一点小建议：我这个月vf更新后下降的比较厉害，这个vf周期的alpha需要认真挑选，或者放弃掉。

--------------------------------------------------------------------------------------------------------

慢慢来，相信时间的力量。

--------------------------------------------------------------------------------------------------------

---

### 评论 #2 (作者: ZZ12657, 时间: 6个月前)

很有帮助

---

### 评论 #3 (作者: CC21336, 时间: 6个月前)

目前这个打分方案还有继续改进的地方：

①如果你的池子中有某个alpha不具备打分资格，那么100000美金可能无法完全分配完，所以打分前最好先确认所有被打分的alpha具备打分资格；

②此外该打分只考虑了平均fitness、returns、margin、sharpe、drawdown、turnover、多空平衡，没有具体考虑近2-3年是否赚钱亏钱，如果近2-3年衰减严重出现亏钱，则需降低分数(下注金额)

---

### 评论 #4 (作者: MZ45384, 时间: 6个月前)

感谢大佬的帖子，分配方法很全面，之前用课代表的代码分配分数的时候有几个inactive的alpha分配失败了，但没找出来具体是哪几个，这次用大佬的代码找出来隐藏了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

### 评论 #5 (作者: LD27384, 时间: 6个月前)

----------------------------------------------------------------------------------------------------------------------------------------------------

感谢您的分享，我在使用时发现代码未过滤 DECOMMISSIONED 的alpha，只需在URL拼接时加入过滤条件即可。

----------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #6 (作者: XX81632, 时间: 6个月前)

感谢大佬的分享，尤其是四种分配方式，让我学到了更多的知识，祝大佬蒸蒸日上！

---

### 评论 #7 (作者: DX67257, 时间: 6个月前)

感谢大佬分享

---

### 评论 #8 (作者: CL86067, 时间: 6个月前)

太棒了，感谢大佬的分享，太有用了，而且一下多种分配方式给我蛮多启发的，打分这种办法真的很有想法，根据不同打分策略可以有不同的分配方案。

再次感谢，祝大佬vf常驻0.98+，genius直升Gm！

——行动才是解决一切问题的答案，加油，run起来

---

### 评论 #9 (作者: QX52484, 时间: 6个月前)

======================================================================

感谢大佬 祝大佬比赛取得佳绩

sharpe is ts_delta and ts_delta but returns ts_delay and ts_delay
======================================================================

---

### 评论 #10 (作者: ZZ10277, 时间: 6个月前)

感谢分享，我开始的时候每个区就选了10个，完后按照表现进行了rank，这样分完几个区后发现排到100多名了。

------------------------------------------------------------------------------------------

回测是历史的答案，实盘是未来的考题。

------------------------------------------------------------------------------------------

---

### 评论 #11 (作者: SJ65808, 时间: 6个月前)

很不错的分配方案，解释性很强

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #12 (作者: YH87796, 时间: 6个月前)

感谢分享！跟着大佬的思路自己做了一下，果然有了一些新思路！

---

### 评论 #13 (作者: QX52484, 时间: 6个月前)

while True:

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&dateCreated%3E={start_date_str}"

f"&settings.region={region}"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&hidden=false"

f"&type!=SUPER"

f"&order=-dateSubmitted"

f"&settings.delay=1"

)

使用过程中发现会把d0加上 d0不参赛会设置出错 .感觉需要加上一个f"&settings.delay=1"

---

### 评论 #14 (作者: LJ85703, 时间: 6个月前)

用了你的模板，直接干到前20了

---

### 评论 #15 (作者: YQ84572, 时间: 6个月前)

非常好用啊，用完直接干到60名，可惜不能再往前一步了，4钟方法都用尽了，因子池质量还是差了点看来，佬的工具还是十分nice的，在尝试看看能不能根据自己因子的特性进一步微调一下分配机制来冲进前五十。感谢佬的分享

---

### 评论 #16 (作者: MY49971, 时间: 6个月前)

这个排名是怎么来的，不是说到周三才确定吗

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #17 (作者: ZY88181, 时间: 6个月前)

代码去掉

```
alphalib
```

后正常运行了， usa的分配比较分散，不知道比赛分数会不会上升，感谢分享！

============================================================
分数分布
============================================================
<1000: 185个alpha ( 86.9%) ███████████████████████████████████████████
1000-2000:  23个alpha ( 10.8%) █████
2000-3000:   2个alpha (  0.9%)
3000-5000:   3个alpha (  1.4%)
5000-10000:   0个alpha (  0.0%)
>10000:   0个alpha (  0.0%)

---

### 评论 #18 (作者: FD69320, 时间: 6个月前)

感谢大佬分享，手动点赞

==================================================================================

WorldQuant is anyone‘s legend

---

### 评论 #19 (作者: GC81559, 时间: 6个月前)

四种分配方式很有用，感谢大佬分享，学习到了

---

### 评论 #20 (作者: ZV96737, 时间: 6个月前)

非常有用的方法，使我快速分配了分数，但是注意到在使用过程中有的alpha会分配错误，主要是以下几个原因引起的，大家可以针对性看一下

1. 成为顾问之前提交的没有报酬的alpha，解决这个问题只需改动main中的adversor_date
2. d0alpha,这一点楼上已经给出解决方案了
3. 近期oth455数据集下架导致一部分已经提交的alpha状态变成DECOMMISSIONED了，，要解决这一点非常简单也像上一条一样修改一下url就可以了

其他情况我也没有遇到，希望大家可以一起补充，结合选取active与d1设置的url如下

```
url = (    f"https://api.worldquantbrain.com/users/self/alphas?"    f"limit={limit}&offset={offset}&status=ACTIVE"    f"&dateCreated%3E={start_date_str}"    f"&settings.region={region}"    f"&status!=UNSUBMITTED%1FIS-FAIL"    f"&hidden=false"    f"&type!=SUPER"    f"&order=-dateSubmitted"    f"&settings.delay=1")
```

---

### 评论 #21 (作者: HZ10678, 时间: 6个月前)

感谢大佬分享~

为了过滤delay=0的alpha，可以把settings.delay设置为1，代码如下：

while True:

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&dateCreated%3E={start_date_str}"

f"&settings.region={region}"

f"&settings.delay=1"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&hidden=false"

f"&type!=SUPER"

f"&order=-dateSubmitted"

)

---

### 评论 #22 (作者: JX39934, 时间: 6个月前)

感谢大佬的分享，但是我觉得这样打分会不会有一些情况没有顾及到，比如有的因子可能平均IS表现很好，然后获得了比较大的打分权重，但是21 22年表现不好，或者说是下降趋势，这种会不会亏钱的可能性也很大呢，感觉打分脚本应该把这一块考虑进去

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #23 (作者: SJ65808, 时间: 5个月前)

四种分配方案哪种更好大佬有有测试吗？

==================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #24 (作者: OY62064, 时间: 5个月前)

感谢大佬的分享，先试试看~

---

### 评论 #25 (作者: LL81909, 时间: 5个月前)

厉害，代码即插即用！

---

### 评论 #26 (作者: ZY27848, 时间: 3个月前)

请问大佬，运行提供的代码，收到提示：2026-03-08 13:58:12,373 - INFO - 登录成功，开始获取alpha数据
2026-03-08 13:58:12,764 - WARNING - 没有获取到alpha数据
2026-03-08 13:58:12,764 - ERROR - 未获取到有效alpha数据，是什么原因？

---

### 评论 #27 (作者: ZY27848, 时间: 3个月前)

找到原因了，没填Data

---

