# 我的Alpha“综合得分”排序函数迭代之路：从算术平均到几何平均经验分享

- **链接**: [Commented] 我的Alpha综合得分排序函数迭代之路从算术平均到几何平均经验分享.md
- **作者**: QL33636
- **发布时间/热度**: 8个月前, 得票: 10

## 帖子正文

**缘起：一个提高Alpha提交效率的想法**

大家好！最近在社区拜读了关于alpha综合得分排序的 [文章](/hc/zh-cn/community/posts/34405014378135) ，深受启发。这篇文章提出，在提交alpha之前，通过一个综合得分函数对它们进行预筛选，可以极大地提升我们的研究效率和最终的Value Factor。

基于这个核心思想，我开始着手构建自己的综合得分函数。在这个过程中，我进行了一些迭代。本文就是对我整个思考过程的记录与分享，希望能抛砖引玉，与大家共同探讨如何更科学地评价alpha。

**V1.0：算术平均的探索——合并与增补**

在阅读原文后，我很快实现了我的第一个版本。相较于原文，我主要做了以下调整：

1.  **聚焦核心指标 `fitness`** ：我将原文中的`sharpe`、`returns`、`turnover`等指标统一归入`fitness`。我的理由是，`fitness`的计算本身就已经综合了夏普率、收益率和换手率等信息。单独再将这些指标加入综合分，本质上只是改变了它们的权重，相当于引入了一个自定义的、等权相加的`my_fitness`指标。我认为这种做法虽然直观，但可能不够科学。相比之下，`fitness`是平台经过行业验证的综合性指标，专注于它能让我们的评价体系更简洁、更聚焦于alpha的综合表现。

2.   **引入关键维度 `correlation`** ：在`Kunqi`老师的启发下，我将`correlation`（与已提交alpha的相关性）纳入了评分体系。相关性的重要性不言而喻，一个真正优秀的alpha不仅要有出色的自身表现，还必须为我们的投资组合带来多样性。因此，将它作为评价维度之一是必不可少的。

3.   **增加其他有效信息** ：既然`correlation`都已加入，我还想到了其他几个可以反映alpha稳健性的指标，包括`sub_universe_sharpe_ratio`（子区域夏普与总夏-普的比率）、`two_year_sharpe`（两年夏普）和`drawdown`（最大回撤）。

于是，我的第一版alpha综合得分排序函数诞生了，它采用 **算术平均** 的思路，对归一化后的各项指标得分进行线性加总。

> # --- V1.0 代码 ---
> def sorted_alpha_by_composite_score(alphas):
> """
> 根据综合得分对数组进行降序排序
> Args:
> alphas: 输入的alpha数组，每个元素应包含'is'键及其相关指标
> Returns:
> 排序后的alpha数组
> """
> if len(alphas) <= 1:
> return alphas
> print("📊 正在计算alpha综合得分并进行排序...")
> alpha_metrics = {}
> for alpha in alphas:
> in_sample = alpha['is']
> # 提取基础指标
> metrics = {
> 'fitness': in_sample['fitness'],
> 'margin': in_sample['margin'],
> 'drawdown': in_sample['drawdown'],
> 'correlation': get_submitted_correlation(alpha)
> }
> # 从checks中提取额外指标
> checks_dict = {check['name']: check.get('value') for check in in_sample['checks']}
> metrics['sub_universe_sharpe_ratio'] = checks_dict.get('LOW_SUB_UNIVERSE_SHARPE', 0.0) / in_sample['sharpe']
> metrics['two_year_sharpe'] = checks_dict.get('LOW_2Y_SHARPE', 0.0)
> alpha_metrics[alpha['id']] = metrics
> # 获取各项指标的最值用于归一化
> metric_names = list(next(iter(alpha_metrics.values())).keys())
> metric_ranges = {}
> for metric_name in metric_names:
> values = [metrics[metric_name] for metrics in alpha_metrics.values()]
> metric_ranges[metric_name] = {
> 'min': min(values),
> 'max': max(values)
> }
> # 打印指标范围
> print("📈 指标范围:")
> for metric_name, range_vals in metric_ranges.items():
> print(f"   {metric_name}: [{range_vals['min']:.4f}, {range_vals['max']:.4f}]")
> def calculate_composite_score(alpha):
> """
> 计算alpha的综合得分
> Args:
> alpha: 单个alpha对象，应包含'is'键及其相关指标
> Returns:
> 综合得分
> """
> current_metrics = alpha_metrics[alpha['id']]
> score = 0.0
> # 计算归一化得分
> for metric_name, value in current_metrics.items():
> min_val = metric_ranges[metric_name]['min']
> max_val = metric_ranges[metric_name]['max']
> # 特殊处理：drawdown和correlation是负向指标
> if metric_name in ['drawdown', 'correlation']:
> # 负向指标，最大值变最小值
> normalized = (max_val - value) / (max_val - min_val) if max_val != min_val else 0.0
> else:
> # 正向指标
> normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.0
> score += normalized
> return score
> # 执行排序
> sorted_alphas = sorted(alphas, key=calculate_composite_score, reverse=True)
> print(f"✅ 排序完成！共处理 {len(sorted_alphas)} 个alpha因子")
> print(f"🏆 最高综合得分: {calculate_composite_score(sorted_alphas[0]):.4f}")
> print(f"🏁 最低综合得分: {calculate_composite_score(sorted_alphas[-1]):.4f}")
> return sorted_alphas

**V2.0：引入几何平均，追求均衡**

V1.0版本使用了一段时间后，我发现了一个潜在问题： **“偏科”现象** 。由于采用线性加权，某些alpha可能仅因某一项指标表现极其出色，即便其他指标很差，依然能获得很高的总分。

同时，我也在反思，像`sub_universe_sharpe`和`drawdown`这类指标，平台的初衷更多是将其作为 **风险控制** 或 **约束性指标** ，而非“越高越好”的正向评价指标。将它们直接纳入加权求和，可能会误导我们的判断。

为了解决“偏科”问题，并让评分体系更聚焦于alpha的均衡发展，我受到了AI的启发，决定采用 **几何平均** 来代替算术平均。

几何平均的优势在于，它要求各项指标均衡发展。如果任何一个归一化后的指标得分为0，那么最终的综合得分也将为0。这能有效惩罚那些“偏科”的alpha，确保我们选出的是真正 **全面发展** 的优质alpha。

在V2.0版本中，我精简了评分指标，只保留了最核心的几项：
*   **正向指标**：`fitness`, `margin`, `two_year_sharpe`
*   **风险控制指标**：`correlation`

> # --- V2.0 代码 ---
> def sorted_alpha_by_composite_score(alphas):
> """
> 根据综合得分对数组进行降序排序
> 评分指标选择原则：
> 1. 正向指标：fitness、margin、two_year_sharpe
> 2. 风险控制指标：correlation
> 使用几何平均数计算综合得分，以避免"偏科"现象，确保各项指标均衡发展。
> Args:
> alphas: 输入的alpha数组，每个元素应包含'is'键及其相关指标
> Returns:
> 排序后的alpha数组
> """
> if len(alphas) <= 1:
> return alphas
> print("📊 正在计算alpha综合得分并进行排序...")
> alpha_metrics = {}
> for alpha in alphas:
> in_sample = alpha['is']
> checks_map = {check['name']: check for check in in_sample['checks']}
> alpha_metrics[alpha['id']] = {
> 'fitness': in_sample['fitness'],
> 'margin': in_sample['margin'],
> 'correlation': get_submitted_correlation(alpha),
> 'two_year_sharpe': checks_map.get('LOW_2Y_SHARPE', {}).get('value', 0),
> }
> metric_ranges = {}
> metric_names = list(alpha_metrics.values())[0].keys()
> for metric_name in metric_names:
> values = [metrics[metric_name] for metrics in alpha_metrics.values()]
> metric_ranges[metric_name] = [min(values), max(values)]
> # 打印指标范围
> print("📈 指标范围:")
> for metric_name, range_vals in metric_ranges.items():
> print(f"   {metric_name}: [{range_vals[0]:.4f}, {range_vals[1]:.4f}]")
> def calculate_composite_score(alpha_id):
> """
> 计算alpha的综合得分
> 使用几何平均数而非算术平均数，避免单项指标过高掩盖其他指标不足的问题。
> 如果任何一个指标得分为0，则总分为0，防止"偏科"alpha获得高排名。
> Args:
> alpha_id: alpha的ID
> Returns:
> 综合得分
> """
> current_metrics = alpha_metrics[alpha_id]
> normalized_values = []
> # 计算归一化得分
> for m_name, value in current_metrics.items():
> min_val, max_val = metric_ranges[m_name]
> # 特殊处理：correlation是负向指标
> if m_name in ['correlation']:
> # 负向指标，最大值变最小值
> normalized = (max_val - value) / (max_val - min_val) if max_val != min_val else 0.0
> else:
> # 正向指标
> normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.0
> normalized_values.append(normalized)
> # 使用几何平均数计算综合得分
> if not normalized_values:
> return 0.0
> product = 1.0
> for value in normalized_values:
> product *= value
> return product ** (1.0 / len(normalized_values))
> # 执行排序
> sorted_alphas = sorted(alphas, key=lambda a: calculate_composite_score(a['id']), reverse=True)
> print(f"✅ 排序完成！共处理 {len(sorted_alphas)} 个alpha因子")
> print(f"🏆 最高综合得分: {calculate_composite_score(sorted_alphas[0]['id']):.4f}")
> print(f"🏁 最低综合得分: {calculate_composite_score(sorted_alphas[-1]['id']):.4f}")
> return sorted_alphas

**总结与展望：综合得分函数是Alpha的Alpha**

在我看来，构建综合得分排序函数的过程，本身就像是在开发一个 **“Alpha的Alpha”** 。

WorldQuant BRAIN平台的核心思想就是用数据说话：Alpha是预测股市表现的信号，Genius计划是预测顾问表现的信号，而我们的综合得分函数，则是预测Alpha表现的信号。

我们用来评价alpha的`sharpe`、`fitness`、`drawdown`等是数据字段，而我们回测出的每一个alpha，都是一个样本。一个好的综合得分排序函数，应该能帮助我们从大量样本中，稳定地筛选出那些最有可能提高我们最终Value Factor的alpha。

从这个角度看，综合分的计算方法远不止一种。对于解决偏科的问题，除了AI给出的几何平均的方法，我原先想到的是采用非线性衰减的方法（具体做法是对每个归一化后的指标值开平方根）。当我们拥有足够大的测试样本时，或许就能找到那个表现极佳的“最优”综合得分函数。

在此，我将我的思考过程分享出来，非常欢迎大家集思广益，提出宝贵的意见，共同打磨这个能提升我们研究效率的利器！

---

## 讨论与评论 (7)

### 评论 #1 (作者: HJ31437, 时间: 7个月前)

```
get_submitted_correlation大佬求 这个方法是哪里来源
```

---

### 评论 #2 (作者: CJ35087, 时间: 7个月前)

感谢楼主的分享。本人刚刚成为顾问不久，还是有很多东西要学。楼主的文章，让我受益良多，在代码习惯上，还是要向楼主多多学习!

---

### 评论 #3 (作者: KZ79256, 时间: 7个月前)

[https://support.worldquantbrain.com/hc/zh-cn/community/posts/20852222347159-%E8%8B%B1%E6%89%8D%E5%80%99%E9%80%89%E4%BA%BA%E8%AE%A1%E5%88%92%E5%AE%9E%E8%AE%AD%E8%80%83%E6%A0%B8-Case5-202403%E6%9C%9F%E4%BD%9C%E4%B8%9A%E6%8F%90%E4%BA%A4%E5%A4%84](https://support.worldquantbrain.com/hc/zh-cn/community/posts/20852222347159-%E8%8B%B1%E6%89%8D%E5%80%99%E9%80%89%E4%BA%BA%E8%AE%A1%E5%88%92%E5%AE%9E%E8%AE%AD%E8%80%83%E6%A0%B8-Case5-202403%E6%9C%9F%E4%BD%9C%E4%B8%9A%E6%8F%90%E4%BA%A4%E5%A4%84) 

古早有一个课的作业就是开发相应的评价函数, 博主也可以看看, 连接在上面

---

### 评论 #4 (作者: JW44543, 时间: 7个月前)

感谢大佬分享，对我帮助很大，祝大佬早日GM！

---

### 评论 #5 (作者: ZT38415, 时间: 7个月前)

非常有意思的思路，给两个小小的建议，最后一部分会冗余计算calculate_composite_score，可以改成

# 先计算每个 alpha 的综合得分并缓存
scored_alphas = [
    {**a, "score": calculate_composite_score(a['id'])}
    for a in alphas
]

# 按缓存的分数排序
sorted_alphas = sorted(scored_alphas, key=lambda a: a["score"], reverse=True)

print(f"✅ 排序完成！共处理 {len(sorted_alphas)} 个 alpha 因子")
print(f"🏆 最高综合得分: {sorted_alphas[0]['score']:.4f}")
print(f"🏁 最低综合得分: {sorted_alphas[-1]['score']:.4f}")

另外一些计算也可以并行加速，提升效率。

---

### 评论 #6 (作者: ZX72144, 时间: 7个月前)

这个因子得分是提交之前算的，还是提交之后算的，因为我发现你获取correlation的函数名是提交过的（get_submitted_correlation）

---

### 评论 #7 (作者: QL33636, 时间: 7个月前)

[HJ31437](/hc/zh-cn/profiles/32117943797655-HJ31437)

[ZX72144](/hc/zh-cn/profiles/30331013399575-ZX72144)

这个 `get_submitted_correlation` 是计算一个alpha和自己提交的所有同region的alpha的最大相关性（算上自己提交的所有Power Pool Alpha和Regular Alpha的自相关性），可以参考 [该文章](../LW67640/[Commented] self corr计算的代码优化.md) 实现，我的 `get_submitted_correlation` 因为涉及到一些其他本地代码依赖就没贴上了；主要是计算综合分的思路，即使没有 `get_submitted_correlation` 也就是相当于少一个衡量alpha好坏的指标。

---

