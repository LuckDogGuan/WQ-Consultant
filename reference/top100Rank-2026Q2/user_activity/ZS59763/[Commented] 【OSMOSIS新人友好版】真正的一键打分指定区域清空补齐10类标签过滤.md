# 【OSMOSIS新人友好版】真正的一键打分：指定区域清空+补齐10类+标签过滤

- **链接**: [Commented] 【OSMOSIS新人友好版】真正的一键打分指定区域清空补齐10类标签过滤.md
- **作者**: BQ64903
- **发布时间/热度**: 2个月前, 得票: 22

## 帖子正文

前几天看到  **[XX42289](/hc/en-us/profiles/14187300941847-XX42289)**   [【课代表】【轻松点击即可完成参赛】CA 降维 + 多指标聚类数评判 + KMeans / 层次 / DBSCAN 聚类的 Osmosis 点数分配工具 – WorldQuant BRAIN](../MZ45384/[Commented] 【课代表】【轻松点击即可完成参赛】CA 降维  多指标聚类数评判  KMeans  层次  DBSCAN 聚类的 Osmosis 点数分配工具经验分享.md) 和 [JR23144](/hc/en-us/profiles/28844048981143-JR23144)  [【贺六浑】-【工具配置】OC2025 一键清空分数脚本 – WorldQuant BRAIN](../JR23144/【贺六浑】-【工具配置】OC2025 一键清空分数脚本经验分享.md) 的文章。发现一些细节不足：

1. 清除分数会将所有区域清除，且不包含super alpha
2. 分配分数时四舍五入的偏差并没有通过API更新
3. 分类结果可能小于10类，不满足打分标准

所以在此做了略微改进，主要在于：

1. 给指定区域打分前先清空该区域所有分数（包括super alpha）
2. 通过API更新四舍五入的偏差
3. 不足十类的，给其他alpha赋值1，强行满足要求
4. 支持通过颜色/tag筛选要打分的alpha（这样可以把AI提交的烂alpha排除出去）

```
# # 清空# In[1]:# -*- coding: utf-8 -*-import urllib.parseimport loggingimport numpy as npimport pandas as pdfrom sklearn.preprocessing import StandardScaler, RobustScalerfrom sklearn.cluster import KMeans, DBSCAN, AgglomerativeClusteringfrom sklearn.metrics import silhouette_score, calinski_harabasz_scorefrom sklearn.decomposition import PCA# 假设该库返回requests.Session对象#from machine_lib import login  from ace_lib import (    start_session )import timefrom datetime import datetime, timedelta#from machine_lib import *  # 假设 login() 在这里from concurrent.futures import ThreadPoolExecutorimport json# In[2]:# ===================================================================# PART 1: 配置与函数定义# ===================================================================#  并发清除操作的线程数MAX_WORKERS = 10def up_alpha_properties_to_clear(s, alpha_id: str, old_osmosisPoints: str):    """    一个专门用于清除 Alpha 分数的函数。    它通过将 'osmosisPoints' 字段设置为 null 来实现。    """    params = {"osmosisPoints": None}  # 在 requests 中, None 会被序列化为 JSON null    response = s.patch(        f"https://api.worldquantbrain.com/alphas/{alpha_id}", json=params    )    if response.status_code == 200:        print(f"成功清除 Alpha {alpha_id} 的分数 (原分数: {old_osmosisPoints})。")        return "SUCCESS"    else:        print(f"清除 Alpha {alpha_id} 分数失败，状态码: {response.status_code}, 信息: {response.text}")        return "FAILED"def get_colored_alphas_in_date_range(s, start_date, end_date, region, alpha_num_limit=1000):    """    获取在指定日期范围内，所有设置了分数的Alpha。    """    colored_alphas = []    print(f"开始查找从 {start_date} 到 {end_date} 所有已设置分数的常规 Alpha...")    for i in range(0, alpha_num_limit, 100):        print(f"正在扫描第 {i} 到 {i + 100} 个 alpha...")        # 【重要】在 URL 中加入了 dateSubmitted 过滤器        url_e = (            f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}"            f"&status!=UNSUBMITTED&status!=IS_FAIL&hidden=false"            f"&dateSubmitted>={start_date}T00:00:00-04:00"            f"&dateSubmitted<{end_date}T00:00:00-04:00"            f"&settings.region={region}"          )        try:            response = s.get(url_e)            response.raise_for_status()            alpha_list = response.json().get("results", [])            if not alpha_list:                print("已扫描完所有符合条件的 Alpha。")                break            # 在客户端筛选出有分数的 Alpha            for alpha in alpha_list:                if alpha.get("osmosisPoints") is not None:                    record = {                        "id": alpha["id"],                        "osmosisPoints": alpha["osmosisPoints"]                    }                    colored_alphas.append(record)        except Exception as e:            print(f"获取alpha时发生异常: {e}")            resp = s.get('https://api.worldquantbrain.com/users/self')            if resp.status_code != 200:                print(f"用户会话可能已过期，状态码: {resp.status_code}")            break    print(f"\n查找完毕！共找到 {len(colored_alphas)} 个在指定日期内需要清除分数的 Alpha。")    return colored_alphas# In[3]:def get_history_alpha_ids(s, region, start_date, limit=50, offset=0, exclude_tags=None, exclude_color=None):    """    从接口分页获取指定地区、指定日期后的alpha数据    :param s: requests.Session对象，已完成登录的会话    :param region: 地区大写：USA, EUR ... ...    :param start_date: 过滤日期，获取该日期之后的因子    :param limit: 每页获取的数量    :param offset: 分页偏移量    :return: 包含alpha的id和各类is指标的列表    """    alphas_data = []    # 对日期字符串进行URL编码，避免特殊字符影响请求    start_date_str = urllib.parse.quote(start_date.astimezone().isoformat(timespec='seconds'))    # 分页获取数据    #去掉color为红的    while True:        url = (            f"https://api.worldquantbrain.com/users/self/alphas?"            f"limit={limit}&offset={offset}"            f"&dateCreated%3E={start_date_str}"            f"&settings.region={region}"            f"&status!=UNSUBMITTED%1FIS-FAIL"            f"&hidden=false"            f"&order=-dateSubmitted"            f"&color!={exclude_color}"            f"&tag!={exclude_tags}"        )        try:            resp = s.get(url)            if resp.status_code != 200:                print(f"请求出错，状态码：{resp.status_code}")                break            data = resp.json()            results = data.get("results", [])            alphas_data.extend(results)            # 判断是否获取完所有数据，是则退出循环            if offset + len(results) >= data.get("count", 0) or len(results) < limit:                break            offset += limit        except Exception as e:            print(f"数据获取异常，异常信息：{e}")            break    # 提取需要的指标数据    alpha_metrics = []    for item in alphas_data:        # 检查is中的关键指标是否存在，避免键缺失报错        is_data = item.get('is', {})        metrics = {            'id': item['id'],            'fitness': is_data.get('fitness', 0.0),            'longCount': is_data.get('longCount', 0.0),            'shortCount': is_data.get('shortCount', 0.0),            'turnover': is_data.get('turnover', 0.0),            'returns': is_data.get('returns', 0.0),            'drawdown': is_data.get('drawdown', 0.0),            'margin': is_data.get('margin', 0.0),            'sharpe': is_data.get('sharpe', 0.0)        }        alpha_metrics.append(metrics)    if not alpha_metrics:        print("错误：没有获取到有效的alpha数据")        return []    return alpha_metricsdef determine_clusters_multi_criteria(X, min_clusters=5, max_clusters=50):    """    多指标确定聚类数（结合轮廓系数、CH指数，同时限制聚类数范围）    :param X: 标准化后的特征数据    :param min_clusters: 最小聚类数（避免过少）    :param max_clusters: 最大聚类数（避免过多）    :return: 最终聚类数量    """    if len(X) <= min_clusters:        return len(X)  # 样本数少于最小聚类数时，取样本数    # 限制聚类数范围：2 ~ 样本数（但不超过max_clusters，不低于min_clusters）    cluster_range = range(max(2, min_clusters), min(max_clusters + 1, len(X)))    scores = []    for k in cluster_range:        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')        labels = kmeans.fit_predict(X)        # 轮廓系数：衡量聚类紧密度和分离度，越接近1越好        sil_score = silhouette_score(X, labels)        # CH指数：数值越大表示聚类效果越好（类内紧密，类间分离）        ch_score = calinski_harabasz_score(X, labels)        # 综合得分（归一化后加权，可调整权重）        scores.append({            'k': k,            'sil': sil_score,            'ch': ch_score,            # 权重可调整，平衡轮廓系数和CH指数的影响            'composite': 0.4 * sil_score + 0.6 * (ch_score / 100000)        })    # 转换为DataFrame方便排序    score_df = pd.DataFrame(scores)    # 按综合得分降序排序，取第一个作为最佳聚类数    best_k = score_df.sort_values('composite', ascending=False)['k'].iloc[0]    # 兜底：确保聚类数在合理范围    best_k = max(min_clusters, min(best_k, max_clusters))    return best_kdef cluster_alphas_improved(alpha_metrics, use_pca=True, cluster_algorithm='kmeans'):    """    改进的聚类逻辑：支持PCA降维、多种聚类算法、多指标确定聚类数    :param alpha_metrics: alpha的指标数据    :param use_pca: 是否使用PCA降维（处理特征冗余）    :param cluster_algorithm: 聚类算法（kmeans/agglomerative/dbscan）    :return: 选中的alpha列表（每个聚类fitness最大）    """    # 转换为DataFrame方便处理    df = pd.DataFrame(alpha_metrics)    # 定义用于聚类的特征列    feature_cols = ['longCount', 'shortCount', 'turnover', 'returns', 'drawdown', 'margin', 'sharpe']    # 提取特征数据，处理缺失值（填充0）    X = df[feature_cols].fillna(0).values    # 改进1：使用RobustScaler标准化（抗异常值，比StandardScaler更适合金融数据）    scaler = RobustScaler()  # 替代StandardScaler，对异常值不敏感    X_scaled = scaler.fit_transform(X)    # 改进2：PCA降维（处理特征冗余，减少噪声）    if use_pca and len(feature_cols) > 2:        # 保留95%的方差，自动确定降维后的维度        pca = PCA(n_components=0.95, random_state=42)        X_processed = pca.fit_transform(X_scaled)        print(f"PCA降维后，特征维度从{len(feature_cols)}变为{X_processed.shape[1]}")    else:        X_processed = X_scaled    # 改进3：多指标确定聚类数（避免聚类数过少）    best_k = determine_clusters_multi_criteria(X_processed, min_clusters=5, max_clusters=50)    print(f"改进后确定的最佳聚类数量：{best_k}")    # 改进4：支持多种聚类算法（KMeans/层次聚类/DBSCAN）    if cluster_algorithm == 'kmeans':        # KMeans：适合球形分布，速度快        cluster_model = KMeans(n_clusters=best_k, random_state=42, n_init='auto')        df['cluster'] = cluster_model.fit_predict(X_processed)    elif cluster_algorithm == 'agglomerative':        # 层次聚类：不假设球形分布，更灵活        cluster_model = AgglomerativeClustering(n_clusters=best_k)        df['cluster'] = cluster_model.fit_predict(X_processed)    elif cluster_algorithm == 'dbscan':        # DBSCAN：无需指定聚类数，自动识别密度聚类（适合非球形分布）        # eps和min_samples可调整：eps越大，聚类数越少；min_samples越大，聚类数越多        cluster_model = DBSCAN(eps=0.5, min_samples=5)        df['cluster'] = cluster_model.fit_predict(X_processed)        # DBSCAN的-1表示噪声点，单独处理为一个聚类        noise_cluster = df['cluster'].max() + 1        df.loc[df['cluster'] == -1, 'cluster'] = noise_cluster        best_k = len(df['cluster'].unique())        print(f"DBSCAN聚类后实际聚类数量：{best_k}")    # 每个聚类中选择fitness最大的alpha    selected_alphas = []    for cluster in df['cluster'].unique():        cluster_df = df[df['cluster'] == cluster]        # 取fitness最大的行        best_alpha = cluster_df.loc[cluster_df['fitness'].idxmax()]        selected_alphas.append(best_alpha.to_dict())    return selected_alphas# In[4]:# ===================================================================# PART 3: 主逻辑 (先清除该地区，再赋值)# ===================================================================if __name__ == '__main__':    # 1. 基础配置    target_region = "USA"     advisor_date_obj = datetime(2025, 12, 10)    advisor_date_str = advisor_date_obj.strftime("%Y-%m-%d")    page_limit = 100  # 每页获取的alpha数量    page_offset = 0   # 分页起始偏移量    session = start_session()    # --- A. 清除该地区既有分数 ---    # 计算日期范围 (参考你清除脚本的逻辑)    begin_date = advisor_date_str    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")    print(f"正在清除地区 {target_region} 在 {begin_date} 之后的既有分数...")    alphas_to_clear = get_colored_alphas_in_date_range(session, begin_date, end_date, target_region)    if alphas_to_clear:        with ThreadPoolExecutor(max_workers=10) as executor:            for alpha_data in alphas_to_clear:                executor.submit(up_alpha_properties_to_clear, session, alpha_data["id"], alpha_data["osmosisPoints"])    else:        print("未找到需要清除分数的 Alpha。")    # 获取alpha的指标数据    alpha_metrics_list = get_history_alpha_ids(        s=session,        region=target_region,        start_date=advisor_date_obj,        limit=page_limit,        offset=page_offset,        #exclude_tags=["TEST"],         exclude_color='RED'    )    # 校验数据是否有效    if not alpha_metrics_list:        print("程序终止：未获取到有效alpha数据")        exit(1)    # 执行聚类并选择每个类别中fitness最大的alpha    selected_alpha_list = cluster_alphas_improved(        alpha_metrics=alpha_metrics_list,        use_pca=True,        cluster_algorithm='kmeans'    )    # 校验聚类结果    if not selected_alpha_list:        print("程序终止：聚类后未选中任何alpha")        exit(1)# In[5]:# --- 1. 获取聚类领头羊 ---# selected_alpha_list 已经是每个聚类里 fitness 最大的一个selected_ids = {a['id'] for a in selected_alpha_list}# --- 2. 补齐逻辑：如果不足 10 类，从备选池里抓取 ---target_count = 10current_count = len(selected_alpha_list)if current_count < target_count:    # 找出那些没被选中的因子    remaining_alphas = [a for a in alpha_metrics_list if a['id'] not in selected_ids]    # 按 Fitness 排序，选出表现较好的作为凑数因子    remaining_alphas.sort(key=lambda x: x['fitness'], reverse=True)    # 计算需要补多少个    needed = target_count - current_count    # 注意：补齐数量不能超过备选池总数    fillers = remaining_alphas[:needed]    for f in fillers:        f['cluster'] = 'filler'  # 标记为凑数        selected_alpha_list.append(f)# 更新当前最终选中的数量final_selected_count = len(selected_alpha_list)print(f"最终入选因子数：{final_selected_count} (其中聚类领头羊：{current_count}，凑数因子：{final_selected_count - current_count})")# --- 3. 分数分配逻辑 ---# 分成两拨处理：核心因子 vs 凑数因子leaders = [a for a in selected_alpha_list if a['cluster'] != 'filler']fillers = [a for a in selected_alpha_list if a['cluster'] == 'filler']# 凑数因子总分 = 数量 * 1分filler_total_points = len(fillers)# 核心因子总分 = 100,000 - 凑数分leader_pool_points = 100000 - filler_total_points# 核心因子基础分（平分池子）leader_base_score = leader_pool_points // len(leaders)leader_remainder = leader_pool_points % len(leaders)# --- 4. 执行 API 更新 ---total_check = 0for i, alpha_info in enumerate(selected_alpha_list):    alpha_id = alpha_info['id']    # 判断分数    if alpha_info['cluster'] == 'filler':        final_score = 1    else:        # 如果是核心因子中的第一个，拿走余数        if alpha_id == leaders[0]['id']:            final_score = leader_base_score + leader_remainder        else:            final_score = leader_base_score    print(f"Alpha {alpha_id} | Fitness值：{alpha_info['fitness']} | 类型: {alpha_info['cluster']} | 分配分数: {final_score}")    # 执行更新    update_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"    session.patch(update_url, json={"osmosisPoints": final_score}) # 确认无误后再取消注释    total_check += final_scoreprint(f"\n分配总计：{total_check} 分 (目标 100,000)")
```

---

## 讨论与评论 (21)

### 评论 #1 (作者: QX52484, 时间: 2个月前)

======================================================================
这段代码分配的效果怎么样呢?另外我看了一下好像只是简单按指标聚类了,没有对指标评分的代码,感觉有几率会产出高回撤的alpha聚类,这是你计划中的多样性的一部分吗?
======================================================================
sharpe is ts_delta and ts_delta but returns ts_delay and ts_delay.

---

### 评论 #2 (作者: FF45555, 时间: 2个月前)

感谢大佬的改良和分享，刚刚使用了一下，提示缺少 sklearn 库，需要安装，给同样没有安装的小伙伴提供一下安装命令：pip install scikit-learn

安装后再使用，就不会报错了。

====================================================================================== # Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100% # sys.setrecursionlimit(α∞) # PnL = ∑(Robustness * Creativity) #无限探索、鲁棒性优先，创新性增值 #Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。

---

### 评论 #3 (作者: FF65210, 时间: 2个月前)

感谢课代表的代码，对os分配没把握，这下可以用课代表的代码试试了。

**===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================**

---

### 评论 #4 (作者: RM49262, 时间: 2个月前)

=====================================评论区====================================

感谢大佬分享

这套方案非常靠谱了  这就用起来

=============================================================================

---

### 评论 #5 (作者: DL61056, 时间: 2个月前)

感谢大佬真及时，我刚写了个清除分数的脚本，还没来得及写分配策略就在论坛看到帖子了，省事了。

---

### 评论 #6 (作者: CZ78575, 时间: 2个月前)

==================================================================================

直接99991+9*1，梭哈也是一门艺术

----------    好东西，快把这个代码给我啊==================================================================================

---

### 评论 #7 (作者: JL52079, 时间: 2个月前)

感谢大佬的代码分享，效率简直飙升！

---

### 评论 #8 (作者: CH62432, 时间: 2个月前)

感谢大佬分享!

基于对alpha池子不够自信,目前还是手选的alpha进行打分,先看看效果 后期可以尝试一下大佬的代码!

==================================================================================

“牛市在悲观中诞生，在怀疑中成长，在乐观中成熟，在狂热中死亡。”
 *(Bull markets are born on pessimism, grow on skepticism, mature on optimism, and die on euphoria.)*

*==================================================================================*

---

### 评论 #9 (作者: ZS59763, 时间: 2个月前)

很好用，很赞

后续的改进思路：对ra和sa的赋分有个上限，比如设置一下，sa给三万分，或者几万分，就可以自动区分开了

=========================================================================

告诉你个秘密，其实我是游戏王

=========================================================================

---

### 评论 #10 (作者: XG41865, 时间: 2个月前)

不区分d1/d0，改造如下：

```
def get_colored_alphas_in_date_range(s, start_date, end_date, region, delay, alpha_num_limit=1000):      #  省略其它代码    url_e = (        f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}&stage=OS"       f"&dateSubmitted>={start_date}T00:00:00-04:00"       f"&dateSubmitted<{end_date}T00:00:00-04:00"       f"&settings.region={region}"       f"&settings.delay={delay}"    )def get_history_alpha_ids(s, region, delay, start_date, end_date,limit=50, offset=0, exclude_tags=None, exclude_color=None):   # 省略其它代码  
```

```
  url = (      f"https://api.worldquantbrain.com/users/self/alphas?limit={limit}&offset={offset}&stage=OS"         f"&dateSubmitted>={start_date}T00:00:00-04:00"       f"&dateSubmitted<{end_date}T00:00:00-04:00"       f"&settings.region={region}"       f"&settings.delay={delay}"       f"&hidden=false&order=-dateSubmitted"&color!={exclude_color}&tag!={exclude_tags}"  )# 命令入参支持if __name__ == '__main__':     # 1. 基础配置    # 配置命令行参数    parser = argparse.ArgumentParser(description='WorldQuant Brain Osmosis Points Allocator')    parser.add_argument('-r', '--region', type=str, required=True,  help='目标地区 (如: USA, EUR, ASI, IND, GLB)')    parser.add_argument('-n', '--count', type=int, default=50, help='目标选中的因子数量 (默认: 50)')    parser.add_argument('-d', '--delay', type=int, default=1, help='目标延迟天数 (默认: 1)')    parser.add_argument('-s', '--start', type=str, default='2025-05-14', help='开始日期 (默认: 2025-05-14)')        args = parser.parse_args()    target_region = args.region    # target_selected_alphas = args.count    target_delay = args.delay    target_start_date = args.start     print(f"目标地区: {target_region}, 目标延迟天数: {target_delay}, 开始日期: {target_start_date}")     advisor_date_obj = datetime.strptime(target_start_date, "%Y-%m-%d")  # 验证日期格式     advisor_date_str = advisor_date_obj.strftime("%Y-%m-%d")    page_limit = 100  # 每页获取的alpha数量    page_offset = 0   # 分页起始偏移量        session = login(os.environ.get('BRAIN_EMAIL'), os.environ.get('BRAIN_PASSWORD'))    # --- A. 清除该地区既有分数 ---    # 计算日期范围 (参考你清除脚本的逻辑)    begin_date = advisor_date_str    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")    print(f"正在清除地区 {target_region} 在 {begin_date} 之后的既有分数...")    alphas_to_clear = get_colored_alphas_in_date_range(session, begin_date, end_date, target_region, target_delay)    if alphas_to_clear:        with ThreadPoolExecutor(max_workers=10) as executor:            for alpha_data in alphas_to_clear:                executor.submit(up_alpha_properties_to_clear, session, alpha_data["id"], alpha_data["osmosisPoints"])    else:        print("未找到需要清除分数的 Alpha。")    # 获取alpha的指标数据    alpha_metrics_list = get_history_alpha_ids(        s=session,        region=target_region,        delay=target_delay,        start_date=begin_date,        end_date=end_date,        limit=page_limit,        offset=page_offset,        #exclude_tags=["TEST"],         exclude_color='RED'    )# 省略其它代码
```

使用方法：

python osmosis.py -r USA -d 1 -start 2026-01-01

---

### 评论 #11 (作者: MZ45384, 时间: 2个月前)

感谢大佬的代码分享。这周就试验一下。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #12 (作者: QL88701, 时间: 2个月前)

正好想更换os分配策略！感谢楼主！

===================================================

每日谨记：提交因子不能抱侥幸心理！！坚持一定会有结果！！

守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”
无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。===================================================

---

### 评论 #13 (作者: CZ39633, 时间: 2个月前)

====================================================================================                        感谢大佬的os代码一键配置分享 。太实用了                                                                   ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #14 (作者: BZ55699, 时间: 2个月前)

感谢大佬对代码的改良，一起加油。

---

### 评论 #15 (作者: ZC54526, 时间: 2个月前)

感谢大佬分享，用起来了

---

### 评论 #16 (作者: BQ64903, 时间: 2个月前)

[XG41865](/hc/en-us/profiles/30813446988823-XG41865)  感谢补充！

---

### 评论 #17 (作者: BQ64903, 时间: 2个月前)

[ZS59763](/hc/en-us/profiles/26858512793111-ZS59763)  多亏了游戏王的指点，这篇帖子才得以问世啊！

---

### 评论 #18 (作者: BQ64903, 时间: 2个月前)

[QX52484](/hc/en-us/profiles/28901412334615-QX52484)  一般差的alpha我都手动标红了，所以没有考虑到这方面。后续可能会加入这方面的功能

---

### 评论 #19 (作者: LR23136, 时间: 2个月前)

请问ace_lib库在哪里获取？

---

### 评论 #20 (作者: BQ64903, 时间: 2个月前)

[LR23136](/hc/en-us/profiles/28828952945815-LR23136)  Learn-Documentation-BRAIN API

---

### 评论 #21 (作者: BW14163, 时间: 1个月前)

感谢分享，回头和自己目前使用的代码比对一下，看看有没有可以优化的地方

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

