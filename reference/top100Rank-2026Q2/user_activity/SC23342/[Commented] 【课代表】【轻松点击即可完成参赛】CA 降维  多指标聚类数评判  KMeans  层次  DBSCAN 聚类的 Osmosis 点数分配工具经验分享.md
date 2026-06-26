# 【课代表】【轻松点击即可完成参赛】CA 降维 + 多指标聚类数评判 + KMeans / 层次 / DBSCAN 聚类的 Osmosis 点数分配工具经验分享

- **链接**: [Commented] 【课代表】【轻松点击即可完成参赛】CA 降维  多指标聚类数评判  KMeans  层次  DBSCAN 聚类的 Osmosis 点数分配工具经验分享.md
- **作者**: XX42289
- **发布时间/热度**: 6个月前, 得票: 138

## 帖子正文

# 特此感谢 [BJ65592](/hc/en-us/profiles/34337104554903-BJ65592) 的付出。

```
import urllib.parseimport loggingimport numpy as npimport pandas as pdfrom datetime import datetimefrom sklearn.preprocessing import StandardScaler, RobustScalerfrom sklearn.cluster import KMeans, DBSCAN, AgglomerativeClusteringfrom sklearn.metrics import silhouette_score, calinski_harabasz_scorefrom sklearn.decomposition import PCA# 假设该库返回requests.Session对象from machine_lib import login  def get_history_alpha_ids(s, region, start_date, limit=50, offset=0):    """    从接口分页获取指定地区、指定日期后的alpha数据    :param s: requests.Session对象，已完成登录的会话    :param region: 地区大写：USA, EUR ... ...    :param start_date: 过滤日期，获取该日期之后的因子    :param limit: 每页获取的数量    :param offset: 分页偏移量    :return: 包含alpha的id和各类is指标的列表    """    alphas_data = []    # 对日期字符串进行URL编码，避免特殊字符影响请求    start_date_str = urllib.parse.quote(start_date.astimezone().isoformat(timespec='seconds'))    # 分页获取数据    while True:        url = (            f"https://api.worldquantbrain.com/users/self/alphas?"            f"limit={limit}&offset={offset}"            f"&dateCreated%3E={start_date_str}"            f"&settings.region={region}"            f"&status!=UNSUBMITTED%1FIS-FAIL"            f"&hidden=false"            f"&order=-dateSubmitted"        )        try:            resp = s.get(url)            if resp.status_code != 200:                print(f"请求出错，状态码：{resp.status_code}")                break            data = resp.json()            results = data.get("results", [])            alphas_data.extend(results)            # 判断是否获取完所有数据，是则退出循环            if offset + len(results) >= data.get("count", 0) or len(results) < limit:                break            offset += limit        except Exception as e:            print(f"数据获取异常，异常信息：{e}")            break    # 提取需要的指标数据    alpha_metrics = []    for item in alphas_data:        # 检查is中的关键指标是否存在，避免键缺失报错        is_data = item.get('is', {})        metrics = {            'id': item['id'],            'fitness': is_data.get('fitness', 0.0),            'longCount': is_data.get('longCount', 0.0),            'shortCount': is_data.get('shortCount', 0.0),            'turnover': is_data.get('turnover', 0.0),            'returns': is_data.get('returns', 0.0),            'drawdown': is_data.get('drawdown', 0.0),            'margin': is_data.get('margin', 0.0),            'sharpe': is_data.get('sharpe', 0.0)        }        alpha_metrics.append(metrics)    if not alpha_metrics:        print("错误：没有获取到有效的alpha数据")        return []    return alpha_metricsdef determine_clusters_multi_criteria(X, min_clusters=5, max_clusters=50):    """    多指标确定聚类数（结合轮廓系数、CH指数，同时限制聚类数范围）    :param X: 标准化后的特征数据    :param min_clusters: 最小聚类数（避免过少）    :param max_clusters: 最大聚类数（避免过多）    :return: 最终聚类数量    """    if len(X) <= min_clusters:        return len(X)  # 样本数少于最小聚类数时，取样本数    # 限制聚类数范围：2 ~ 样本数（但不超过max_clusters，不低于min_clusters）    cluster_range = range(max(2, min_clusters), min(max_clusters + 1, len(X)))    scores = []    for k in cluster_range:        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')        labels = kmeans.fit_predict(X)        # 轮廓系数：衡量聚类紧密度和分离度，越接近1越好        sil_score = silhouette_score(X, labels)        # CH指数：数值越大表示聚类效果越好（类内紧密，类间分离）        ch_score = calinski_harabasz_score(X, labels)        # 综合得分（归一化后加权，可调整权重）        scores.append({            'k': k,            'sil': sil_score,            'ch': ch_score,            # 权重可调整，平衡轮廓系数和CH指数的影响            'composite': 0.4 * sil_score + 0.6 * (ch_score / 100000)        })    # 转换为DataFrame方便排序    score_df = pd.DataFrame(scores)    # 按综合得分降序排序，取第一个作为最佳聚类数    best_k = score_df.sort_values('composite', ascending=False)['k'].iloc[0]    # 兜底：确保聚类数在合理范围    best_k = max(min_clusters, min(best_k, max_clusters))    return best_kdef cluster_alphas_improved(alpha_metrics, use_pca=True, cluster_algorithm='kmeans'):    """    改进的聚类逻辑：支持PCA降维、多种聚类算法、多指标确定聚类数    :param alpha_metrics: alpha的指标数据    :param use_pca: 是否使用PCA降维（处理特征冗余）    :param cluster_algorithm: 聚类算法（kmeans/agglomerative/dbscan）    :return: 选中的alpha列表（每个聚类fitness最大）    """    # 转换为DataFrame方便处理    df = pd.DataFrame(alpha_metrics)    # 定义用于聚类的特征列    feature_cols = ['longCount', 'shortCount', 'turnover', 'returns', 'drawdown', 'margin', 'sharpe']    # 提取特征数据，处理缺失值（填充0）    X = df[feature_cols].fillna(0).values    # 改进1：使用RobustScaler标准化（抗异常值，比StandardScaler更适合金融数据）    scaler = RobustScaler()  # 替代StandardScaler，对异常值不敏感    X_scaled = scaler.fit_transform(X)    # 改进2：PCA降维（处理特征冗余，减少噪声）    if use_pca and len(feature_cols) > 2:        # 保留95%的方差，自动确定降维后的维度        pca = PCA(n_components=0.95, random_state=42)        X_processed = pca.fit_transform(X_scaled)        print(f"PCA降维后，特征维度从{len(feature_cols)}变为{X_processed.shape[1]}")    else:        X_processed = X_scaled    # 改进3：多指标确定聚类数（避免聚类数过少）    best_k = determine_clusters_multi_criteria(X_processed, min_clusters=5, max_clusters=50)    print(f"改进后确定的最佳聚类数量：{best_k}")    # 改进4：支持多种聚类算法（KMeans/层次聚类/DBSCAN）    if cluster_algorithm == 'kmeans':        # KMeans：适合球形分布，速度快        cluster_model = KMeans(n_clusters=best_k, random_state=42, n_init='auto')        df['cluster'] = cluster_model.fit_predict(X_processed)    elif cluster_algorithm == 'agglomerative':        # 层次聚类：不假设球形分布，更灵活        cluster_model = AgglomerativeClustering(n_clusters=best_k)        df['cluster'] = cluster_model.fit_predict(X_processed)    elif cluster_algorithm == 'dbscan':        # DBSCAN：无需指定聚类数，自动识别密度聚类（适合非球形分布）        # eps和min_samples可调整：eps越大，聚类数越少；min_samples越大，聚类数越多        cluster_model = DBSCAN(eps=0.5, min_samples=5)        df['cluster'] = cluster_model.fit_predict(X_processed)        # DBSCAN的-1表示噪声点，单独处理为一个聚类        noise_cluster = df['cluster'].max() + 1        df.loc[df['cluster'] == -1, 'cluster'] = noise_cluster        best_k = len(df['cluster'].unique())        print(f"DBSCAN聚类后实际聚类数量：{best_k}")    # 每个聚类中选择fitness最大的alpha    selected_alphas = []    for cluster in df['cluster'].unique():        cluster_df = df[df['cluster'] == cluster]        # 取fitness最大的行        best_alpha = cluster_df.loc[cluster_df['fitness'].idxmax()]        selected_alphas.append(best_alpha.to_dict())    return selected_alphasif __name__ == '__main__':    # 配置参数：顾问相关日期、分页参数    advisor_date = datetime(2020, 1, 1)  # 成为顾问的日期，用于过滤该日期之后的因子    page_limit = 100  # 每页获取的alpha数量    page_offset = 0   # 分页起始偏移量    target_region = "EUR"  # 目标地区    # 初始化登录会话    session = login()    logging.info("登录成功，开始获取alpha数据")    # 获取alpha的指标数据    alpha_metrics_list = get_history_alpha_ids(        s=session,        region=target_region,        start_date=advisor_date,        limit=page_limit,        offset=page_offset    )    # 校验数据是否有效    if not alpha_metrics_list:        print("程序终止：未获取到有效alpha数据")        exit(1)    # 执行聚类并选择每个类别中fitness最大的alpha    selected_alpha_list = cluster_alphas_improved(        alpha_metrics=alpha_metrics_list,        use_pca=True,        cluster_algorithm='kmeans'    )    # 校验聚类结果    if not selected_alpha_list:        print("程序终止：聚类后未选中任何alpha")        exit(1)    # 计算平均权重并分配分数（总分为100000）    total_selected = len(selected_alpha_list)    per_alpha_weight = 1.0 / total_selected if total_selected > 0 else 0.0    total_allocated_score = 0    # 遍历选中的alpha，输出信息并计算分数    for alpha_info in selected_alpha_list:        alpha_score = int(per_alpha_weight * 100000)        print(            f"Alpha ID：{alpha_info['id']} | "            f"Fitness值：{alpha_info['fitness']} | "            f"所属聚类：{alpha_info['cluster']} | "            f"分配分数：{alpha_score}"        )        # 如需调用接口更新分数，取消以下注释        update_url = f"https://api.worldquantbrain.com/alphas/{alpha_info['id']}"        session.patch(update_url, json={"osmosisPoints": alpha_score})        total_allocated_score += alpha_score    # 处理四舍五入导致的分数偏差    score_deviation = 100000 - total_allocated_score    if score_deviation != 0:        print(f"\n因四舍五入产生分数偏差：{score_deviation}分，已将偏差分加到第一个Alpha上")        # 修正第一个Alpha的分数        first_alpha_score = int(per_alpha_weight * 100000) + score_deviation        print(f"第一个Alpha {selected_alpha_list[0]['id']} 的最终分数：{first_alpha_score}")        total_allocated_score = 100000    # 输出最终分配结果    print(f"\n分数分配完成：总分配分数 {total_allocated_score} 分，无分数损耗")
```

---

## 讨论与评论 (36)

### 评论 #1 (作者: XX42289, 时间: 6个月前)

运行之前请配置

```
    advisor_date = datetime(2020, 1, 1)  # 成为顾问的日期，用于过滤该日期之后的因子    target_region = "EUR"  # 目标地区
```

要每个地区分别去分配才行，可以让ai修改算法。

---

### 评论 #2 (作者: RM49262, 时间: 6个月前)

=====================================评论区=========================================

感谢课代表，这下真做到一键参赛了哈哈

===================================================================================

---

### 评论 #3 (作者: ZY88181, 时间: 6个月前)

看着很有帮助的样子，下载了，学习一下，看看能不能在比赛中调用。

---

### 评论 #4 (作者: GZ60647, 时间: 6个月前)

是不是应该过滤掉SA

---

### 评论 #5 (作者: ZY88181, 时间: 6个月前)

代码可以用，但是这个Osmosis point没法设置在super alpha里 ，请问怎么设置？

![图片](images/img_42d9581482.png)

---

### 评论 #6 (作者: HZ49684, 时间: 6个月前)

真是省时省力的神器，感谢课代表！！！
提升大家安装依赖的

```
pip install numpy pandas scikit-learn requests
```

可以安装运行环境

---

### 评论 #7 (作者: XG43628, 时间: 6个月前)

课代表还是牛啊！同时还有  [BJ65592](/hc/en-us/profiles/34337104554903-BJ65592) ，感谢两位大佬的分享与贡献。本来就对于新比赛一知半解，对自己的alpha也不是很有信心，现在有了工具解决问题太好了！

================================================================================

知难上，戒骄狂，常自省，穷途明 ================================================================================

---

### 评论 #8 (作者: JX39934, 时间: 6个月前)

谢谢课代表的分享，顺便我提一下不足之处，一个是要把SA给筛出去，还有就是原本的脚本没有把其他加了分的因子给清除掉，然后就是如果聚类不够10个，也没有补够10个

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #9 (作者: SY43349, 时间: 6个月前)

之前也想到这个、印象中之前是用来做super alpha的。太合适了，感谢佬的分享。

_______________________________________________________________

跑了一下、发现superalpha没有默认过滤，大家调整一下  get_history_alpha_ids 函数的，加入 &type=REGULAR 即可，也可以直接替换为下面的url：

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&dateCreated%3E={start_date_str}"

f"&settings.region={region}"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&type=REGULAR"

f"&hidden=false"

f"&order=-dateSubmitted"

)

---

### 评论 #10 (作者: DX67257, 时间: 6个月前)

感谢大佬分享

---

### 评论 #11 (作者: YQ84572, 时间: 6个月前)

感谢课代表与  [BJ65592](/hc/en-us/profiles/34337104554903-BJ65592) ，感谢两位大佬的分享与贡献。直接做到一键参赛了这是，比赛刚出来大佬们的速度就是快代码都已经搞定了================================================================================

评论区 ================================================================================

---

### 评论 #12 (作者: DL61056, 时间: 6个月前)

while True:

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&dateCreated%3E={start_date_str}"

f"&settings.region={region}"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&hidden=false"

f"&order=-dateSubmitted"

f"&type=REGULAR"  # 添加过滤条件，只获取Regular Alpha

)
感谢大佬分享，这里可以加个条件，只处理ra

---

### 评论 #13 (作者: ML34246, 时间: 6个月前)

@ [GZ60647](/hc/en-us/profiles/33063386613655-GZ60647)  把分页获取数据那段换成这个就只有regular了

```
# 分页获取数据whileTrue:    url = (        f"https://api.worldquantbrain.com/users/self/alphas?"        f"limit={limit}&offset={offset}"        f"&dateCreated%3E={start_date_str}"        f"&settings.region={region}"        f"&status!=UNSUBMITTED%1FIS-FAIL"        f"&hidden=false"        f"&type=REGULAR"        f"&order=-dateSubmitted")
```

---

### 评论 #14 (作者: CH62432, 时间: 6个月前)

感谢课代表的分享.

用之前可以添加一些准备事项 , 例如维护一个需要定点排除的id列表不参与运算 , 添加最少500天有收益的限制(排除一些曾经犯过的错) , 也可以添加近三年斜率放缓就排除的逻辑

----------------------------------------Where there is a will, there is a way.------------------------------------------

---

### 评论 #15 (作者: XX81632, 时间: 6个月前)

大佬牛的程度是无法想象的

---

### 评论 #16 (作者: XX81632, 时间: 6个月前)

关于会选到super alpha的问题在这块代码里加个f"&type=REGULAR"就可以了

```
# 分页获取数据while True:    url = (        f"https://api.worldquantbrain.com/users/self/alphas?"        f"limit={limit}&offset={offset}"        f"&dateCreated%3E={start_date_str}"        f"&settings.region={region}"        f"&type=REGULAR"        f"&status!=UNSUBMITTED%1FIS-FAIL"        f"&hidden=false"        f"&order=-dateSubmitted"    )
```

---

### 评论 #17 (作者: SC77987, 时间: 6个月前)

谢谢课代表分享 看到比赛要求好像需要过滤掉SA 代码可以修改如下：

```
# 分页获取数据whileTrue:url= (f"https://api.worldquantbrain.com/users/self/alphas?"f"limit={limit}&offset={offset}"f"&dateCreated%3E={start_date_str}"f"&settings.region={region}"f"&status!=UNSUBMITTED%1FIS-FAIL"f"&hidden=false"f"&type=REGULAR&type!=SUPER"f"&order=-dateSubmitted")
```

---

### 评论 #18 (作者: OY62064, 时间: 6个月前)

感谢大佬的分享，真是一个不错的工具，效率拉满！

---

### 评论 #19 (作者: XC66172, 时间: 6个月前)

谢谢课代表分享~~ 正准备看一下这个比赛，没想到代码就已经有了。这个立马试用一下。也问一下CHATGPT代码具体含义。

======================================

FIGHTING LABUBU!!

======================================

---

### 评论 #20 (作者: WW37372, 时间: 6个月前)

感谢大佬分享

---

### 评论 #21 (作者: MZ45384, 时间: 6个月前)

记得加上 f"&type!=SUPER"，把super alpha去掉，这样才完整。感谢课代表如此优秀的机器学习工具。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值
======================================================================================

---

### 评论 #22 (作者: SC23342, 时间: 6个月前)

感谢课代表，太爱这种可以直接使用的工具代码啦！不过好像直接运行的话基本选不到十个以上，得修改一下选取方法才行

=================================赛博炼丹，其乐无穷===================================

---

### 评论 #23 (作者: LY15192, 时间: 6个月前)

感谢老师的分享

---

### 评论 #24 (作者: AL13375, 时间: 6个月前)

感谢课代表的无私分享，这个代码太好用了！

已经用上了，比我想象中牛逼！

祝课代表vf早日回升到0.99！

================大角羊================

---

### 评论 #25 (作者: PP26750, 时间: 6个月前)

感谢课代表的无私分享！这个工具直接把 Osmosis 点数分配的门槛拉满了，原本还在纠结怎么选 alpha、怎么分分数，现在一键运行就能搞定，效率直接翻倍，对我们这种想快速参赛又追求分散化的选手太友好了～

====================================================================
活到老学到老
====================================================================

---

### 评论 #26 (作者: PS55811, 时间: 6个月前)

感谢大佬的代码分享，我认为可以进一步问AI优化代码，增加一项功能：允许手动剔除某些不想要分配分数的Alpha因子，并将它们原有的分数重新分配给筛选出来的其他因子

---

### 评论 #27 (作者: CY96125, 时间: 6个月前)

谢谢课代表的分享，代码需要结合分数进行优化

---

### 评论 #28 (作者: FF65210, 时间: 6个月前)

感谢大佬付出，新人确实也能轻松参赛了

---

### 评论 #29 (作者: QW53070, 时间: 6个月前)

谢谢课代表的分享，一键参加比赛

=============================================================================

Osmosis Competition 2025

=============================================================================

---

### 评论 #30 (作者: JX14975, 时间: 5个月前)

课代表可以提示一下因四舍五入产生分数偏差分在代码里是没有分配的（虽然print'已经分配'），需要手动分配，如果忽略这一点可能会导致分数并非恰好100000从而没有成绩。

---

### 评论 #31 (作者: SP74109, 时间: 5个月前)

============================================================
非常感谢课代表的分享，另外提示大家使用这段代码的时候要把SA挑出去，规则上无法对SA分配点数；建议大家可以多尝试几个聚类方法和不同的参数，可能会有惊喜
============================================================
于像素微观处解析视界，在市场波动中量化真知。

---

### 评论 #32 (作者: ZC26080, 时间: 5个月前)

感谢课代表分享，有个小问题：

如果可以根据alpha的质量，分配不同的分数，而不是直接平均分，似乎是一个更好的选择？

================================================================================

知难上，戒骄狂，常自省，穷途明 ================================================================================

---

### 评论 #33 (作者: JL66317, 时间: 4个月前)

=====================================评论区=========================================

感谢课代表，这下真做到一键参赛了哈哈

===================================================================================

---

### 评论 #34 (作者: RX41832, 时间: 3个月前)

感谢大佬的分享，学习到了很多

依旧有几个问题想要请教：

1. 代码最底层的思想是将alpha 通过各个指标分成几个组，找组里最具有代表性的一个alpha赋予分数point。这样做可以使point收益最大化吗？还是可以视为最优解之一？
2. 我们可以根据不同的地区分配相应的点数？但是一次只能分配一个区，所以每个区域的总点数需要我们自己判断？

---

### 评论 #35 (作者: YH55729, 时间: 3个月前)

感谢课代表，准备拿点渗透分了

===================================================================================

---

### 评论 #36 (作者: BQ64903, 时间: 2个月前)

处理四舍五入时要调用API覆盖之前的分数，课代表可能忘了加入：

```
    # 处理四舍五入导致的分数偏差    score_deviation = 100000 - total_allocated_score    if score_deviation != 0:        print(f"\n因四舍五入产生分数偏差：{score_deviation}分，已将偏差分加到第一个Alpha上")                # 修正第一个Alpha的分数        first_alpha_id = selected_alpha_list[0]['id']        first_alpha_score = int(per_alpha_weight * 100000) + score_deviation                # 调用 API 覆盖之前的旧分数        update_url = f"https://api.worldquantbrain.com/alphas/{first_alpha_id}"        session.patch(update_url, json={"osmosisPoints": first_alpha_score})                print(f"第一个Alpha {first_alpha_id} 的最终分数已更新为：{first_alpha_score}")        total_allocated_score = 100000
```

---

