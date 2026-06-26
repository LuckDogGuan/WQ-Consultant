# 【基于相关性剪枝】完整代码代码优化

- **链接**: [Commented] 【基于相关性剪枝】完整代码代码优化.md
- **作者**: JG21054
- **发布时间/热度**: 11个月前, 得票: 62

## 帖子正文

首先感谢  [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256)  和   [HQ17963](/hc/en-us/profiles/27241930042903-HQ17963)  以及  [EC12049](/hc/zh-cn/profiles/28832539069463-EC12049)  三位大佬的源码，思路和分享。具体的文章就不放链接了，有需要的可以去他们的社区主页看看，可以收获到很多。

> 该剪枝方法基于如若一阶段存在较高相关性的alpha,那么在经过二阶段的变换之后其依旧存在高相关性的假设

除了对一阶段剪枝外，我之前还使用这个相关性剪枝去筛选过alpha，对同一数据集，用二阶段跑出的，检测出可提交的alpha进行再一次筛选。筛选出来的alpha都可以提交，提交一个不会影响其余alpha的提交。不过我没有测试是否存在可提交的alpha被遗漏。大概判断一下有多少个可提交的alpha也是很不错的，毕竟原理上只会比这个数量更多，甚至还可以再交PPA如果质量不错的话。

目前我测试剪枝最多的alpha数量在1500左右都挺快的，更多数量应该也可以，只是到后面获取PNL的速度会慢一些。只是几百个的话速度还是很快的，几分钟就可以有结果。

下面是完整代码：

- 首先是登陆函数，也可以替换成自己的登录函数。
- 最后主函数中传入alpha id，我是把数据储存到了文件里做了个排序，也可以直接传入一批id的变量，比如直接把get函数获取的alpha信息的id提取出来传入也行。由于每个人处理数据方式不同，可以结合自己的进行一下修改。

```
import pandas as pdimport numpy as npfrom concurrent.futures import ThreadPoolExecutor, as_completedfrom collections import defaultdictimport requestsimport pickleimport timeimport loggingdef sign_in(username, password):    s = requests.Session()    s.auth = (username, password)    try:        response = s.post('https://api.worldquantbrain.com/authentication')        response.raise_for_status()        logging.info("Successfully signed in")        return s    except requests.exceptions.RequestException as e:        logging.error(f"Login failed: {e}")        return None        # 使用示例username = ""password = ""sess= sign_in(username, password)def wait_get(url: str, max_retries: int = 10) -> requests.Response:    retries = 0    while retries < max_retries:        while True:            simulation_progress = sess.get(url)            if simulation_progress.headers.get("Retry-After", 0) == 0:                break            time.sleep(float(simulation_progress.headers["Retry-After"]))        if simulation_progress.status_code < 400:            break        else:            time.sleep(2 ** retries)            retries += 1    return simulation_progress# --------------------------# 配置项（可根据实际情况修改）# --------------------------API_BASE_URL = "https://api.worldquantbrain.com/alphas"  # API基础地址REGION_DEFAULT = "ASI"  # 默认区域（若alpha无region信息时使用）CORRELATION_THRESHOLD = 0.8  # 相关性阈值（高于此值视为高相关）TIME_WINDOW_YEARS = 4  # 计算相关性的时间窗口（最近N年）VERBOSE = True  # 是否打印过程信息def _get_alpha_pnl(alpha_id: str) -> pd.DataFrame:    """获取单个alpha的PnL数据，返回包含日期和PnL的DataFrame"""    url = f"{API_BASE_URL}/{alpha_id}/recordsets/pnl"    pnl_data = wait_get(url).json()        # 解析数据为DataFrame    columns = [item['name'] for item in pnl_data['schema']['properties']]    df = pd.DataFrame(pnl_data['records'], columns=columns)        # 重命名并保留必要列    df = df.rename(columns={'date': 'Date', 'pnl': alpha_id})    return df[['Date', alpha_id]].set_index('Date')  # 以日期为索引def get_batch_pnl(alpha_ids: list[str]) -> pd.DataFrame:    if not alpha_ids:        raise ValueError("输入的alpha_id列表不能为空")        total = len(alpha_ids)    pnl_dfs = []    completed = 0  # 已完成获取的数量        with ThreadPoolExecutor(max_workers=10) as executor:        # 提交所有任务并关联alpha_id        futures = {executor.submit(_get_alpha_pnl, aid): aid for aid in alpha_ids}                # 遍历已完成的任务，实时跟踪进度        for future in as_completed(futures):            alpha_id = futures[future]            try:                # 获取单个alpha的PnL结果                pnl_df = future.result()                pnl_dfs.append(pnl_df)                completed += 1                # 打印进度（每完成一个就更新）                if VERBOSE:                    print(f"已获取 {completed}/{total} 个alpha的PnL数据（当前：{alpha_id}）")            except Exception as e:                print(f"获取alpha {alpha_id} 的PnL失败：{str(e)}")        if not pnl_dfs:        raise ValueError("所有alpha的PnL数据获取失败")        # 合并数据    combined_pnl = pd.concat(pnl_dfs, axis=1)    combined_pnl.index = pd.to_datetime(combined_pnl.index)    combined_pnl.sort_index(inplace=True)    return combined_pnldef pnl_to_returns(pnl_df: pd.DataFrame) -> pd.DataFrame:    """将PnL数据转换为收益率（参考calc_self_corr逻辑）"""    # 填充缺失值后计算差分（当前PnL - 前一日PnL）    return pnl_df.ffill().diff()# --------------------------# 核心筛选函数（低相关性筛选）# --------------------------def filter_low_correlation_alphas(alpha_ids: list[str]) -> list[str]:    """    传入一批alpha_id，返回筛选后的低相关性alpha列表        流程：    1. 批量获取所有alpha的PnL数据    2. 将PnL转换为收益率    3. 迭代筛选低相关性alpha（核心逻辑）        迭代筛选原理：    - 每次从剩余列表选第一个alpha，加入结果集    - 剔除剩余列表中与该alpha相关性>阈值的所有alpha    - 移除该alpha本身，继续处理剩余列表，直到为空    """    if VERBOSE:        print(f"开始处理{len(alpha_ids)}个alpha...")        # 步骤1：获取批量PnL数据    if VERBOSE:        print("正在获取PnL数据...")    alpha_pnl = get_batch_pnl(alpha_ids)        # 步骤2：转换为收益率    if VERBOSE:        print("将PnL转换为收益率...")    alpha_returns = pnl_to_returns(alpha_pnl)        # 步骤3：限制时间窗口（仅保留最近N年数据）    cutoff_date = alpha_returns.index.max() - pd.DateOffset(years=TIME_WINDOW_YEARS)    alpha_returns = alpha_returns[alpha_returns.index > cutoff_date]    if VERBOSE:        print(f"使用最近{TIME_WINDOW_YEARS}年数据进行筛选，有效日期范围：{alpha_returns.index.min()}至{alpha_returns.index.max()}")        # 步骤4：迭代筛选低相关性alpha    remaining = list(alpha_returns.columns)  # 剩余未处理的alpha    selected = []  # 已选中的低相关性alpha    removal_info = []  # 记录剔除信息        while remaining:        if VERBOSE:            print(f"\n剩余待处理alpha数量：{len(remaining)}")                # 选择当前列表中的第一个alpha        current = remaining[0]        selected.append(current)        if VERBOSE:            print(f"选中alpha：{current}")                # 从剩余列表中移除当前alpha        remaining.remove(current)        if not remaining:            break  # 若已无剩余，结束循环                # 计算当前alpha与剩余alpha的相关性        current_rets = alpha_returns[current]        correlations = alpha_returns[remaining].corrwith(current_rets)                # 筛选出高相关的alpha（修复后）        high_corr = []        for alpha in remaining:            # 1. 获取相关性结果（可能是Series或标量）            corr_result = correlations.get(alpha)                        # 2. 处理可能的Series类型，提取标量值            if isinstance(corr_result, pd.Series):                # 如果是Series，取第一个元素（默认单值场景）                if not corr_result.empty:                    corr_value = corr_result.iloc[0]  # 强制取标量                else:                    corr_value = -float('inf')  # 空值视为低相关            else:                corr_value = corr_result  # 直接使用标量                        # 3. 确保是数值类型后再比较            if isinstance(corr_value, (int, float)) and corr_value > CORRELATION_THRESHOLD:                high_corr.append(alpha)                # 记录剔除信息        for alpha in high_corr:            removal_info.append({                "选中alpha": current,                "被剔除alpha": alpha,                "相关系数": round(correlations[alpha], 4)            })                # 从剩余列表中移除高相关alpha        remaining = [a for a in remaining if a not in high_corr]        if VERBOSE and high_corr:            print(f"已剔除与{current}高相关的alpha数量：{len(high_corr)}")        # 输出筛选结果    if VERBOSE:        print("\n" + "="*50)        print(f"筛选完成！原始数量：{len(alpha_ids)}，保留数量：{len(selected)}，剔除数量：{len(alpha_ids)-len(selected)}")        print("保留的低相关性alpha列表：", selected)        return selected    # --------------------------# 使用示例# --------------------------if __name__ == "__main__":     # 读取 CSV 文件    csv_file_path = 'first_7.15 USA-mocr.csv'  # 请替换为实际的 CSV 文件路径    df = pd.read_csv(csv_file_path)        # 只提取第一列的alpha_id    alpha_ids = df['alpha_id'].tolist()        # 调用筛选函数    low_corr_alphas = filter_low_correlation_alphas(alpha_ids)
```

效果图：

![图片](images/img_be435d96f8.png)

![图片](images/img_6706778e59.png)

---

## 讨论与评论 (11)

### 评论 #1 (作者: SZ83096, 时间: 11个月前)

大佬，你这里是根据第一个alpha来判断后续其他alpha于它的相关性 ，选择是保留还是剔除的吗？那么这种方法选出来选择保存的alpha,是否会很依赖于与第一个alpha的相关性？导致更优秀的alpha由于与第一个alpha的相关性而剔除？

================================================================================

---

### 评论 #2 (作者: JX28185, 时间: 11个月前)

感谢分享完整代码

---

### 评论 #3 (作者: JG21054, 时间: 11个月前)

[SZ83096](/hc/en-us/profiles/29001331587351-SZ83096)

每次剪枝前，我会先对这批alpha根据不同指标计算一个综合评分，单从指标计算出的得分来看，可以认为排在前面的就是比较好的alpha，之后剪枝时它优先选择的就是较好的alpha。

> 导致更优秀的alpha由于与第一个alpha的相关性而剔除？

关于这个问题，我认为会出现有些指标差不多，但在某方面比较好的alpha由于相关性被剔除。不过这应该是剪枝都会存在的问题。

---

### 评论 #4 (作者: BW14163, 时间: 11个月前)

非常感谢，改天就跑跑看效果。

---

### 评论 #5 (作者: DS48533, 时间: 11个月前)

[SZ83096](/hc/zh-cn/profiles/29001331587351-SZ83096) 
您好，我是刚从IQC出来的，我也想过您提到的这个点，所以我做了一点创新，不会直接剪枝，而是先把alpha分组保存，就按照相关性，把彼此相关性高的放在同一个文件夹。

都分好文件夹后，设置一个指标，如(fitness * 2) + (sharpe * 1) - operator_count/4 - failed_checks_percentage/10

按照指标，从每个文件夹中挑选出来最优秀的，进行提交/遍历设置/二阶等操作

如果某个文件夹提交了因子了，就删除这个文件夹。

后续如果对于因子优秀与否的判断有了改变，可以修改评价指标的表达式，然后可以很方便的得到新的判据下的好Alphas

---

### 评论 #6 (作者: JL66317, 时间: 10个月前)

感谢大佬分享

---

### 评论 #7 (作者: DZ31817, 时间: 9个月前)

20250929

------------------------------------------------------------------------------------------

感谢分享，关于评论区SZ83096的问题，我的解决方案是多通道剪枝，即按sharpe、fitness、return等指标分别排序后分别进行剪枝，从而增加多样性。实际使用下来效果跟只按sharpe排序的结果差不多。

---

### 评论 #8 (作者: SL95036, 时间: 8个月前)

感谢分享

---

### 评论 #9 (作者: SZ83387, 时间: 8个月前)

[DS48533](/hc/zh-cn/profiles/29332844557207-DS48533)

大佬这个剪枝的指标是从实践中的出来的吗，有什么依据吗

---

### 评论 #10 (作者: PY58917, 时间: 8个月前)

谢谢老板的帖子，我之前已经用于本地ppa和ra的检查了，只不过老板，这个帖子的可以用于sa的二次筛选吗？

**#========= WORLDQUANT BRAIN CONSULTANT ========== #
#========= 希望大家都可以解决Alpha挖掘中的探索、语义理解和多样性这三大核心问题========== #
#=========知过必改，得能莫忘 ========== #**

**#=========希望大家找到属于自己的圣杯========== #**

**#========= 2025年10月22日中午 ========== #**

---

### 评论 #11 (作者: JG21054, 时间: 8个月前)

[PY58917](/hc/en-us/profiles/30360901528087-PY58917)

这个剪枝也可以用于sa的二次筛选，不过这个阈值应该只能保证它们之间的相关性小于0.7。如果你希望交Prod Correlation小于0.5这一类的sa的话可能需要再找到一个合适的阈值，确保获得的低相关性列表中不会因为交了其中一个alpha导致另一个alpha的Prod Correlation提升到了0.6的这种情况。

---

