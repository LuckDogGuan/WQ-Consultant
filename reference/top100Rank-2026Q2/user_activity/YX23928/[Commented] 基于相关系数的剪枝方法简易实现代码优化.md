# 基于相关系数的剪枝方法简易实现代码优化

- **链接**: [Commented] 基于相关系数的剪枝方法简易实现代码优化.md
- **作者**: EC12049
- **发布时间/热度**: 1年前, 得票: 23

## 帖子正文

感谢 [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256) 以及  [HQ17963](/hc/en-us/profiles/27241930042903-HQ17963)  两位大佬的源码和思路

- 该剪枝方法基于如若一阶段存在较高相关性的alpha,那么在经过二阶段的变换之后其依旧存在高相关性的假设

```
def filter_correlated_alphas(    alpha_returns: pd.DataFrame, threshold: float = 0.8, verbose: bool = True) -> list[str]:    """    迭代筛选相关性低的alpha策略    原理：每次选择一个alpha，剔除与其高度相关的策略，然后移除该alpha本身    并继续处理下一个，直到列表为空    Args:        alpha_returns: 包含所有alpha收益率的DataFrame        threshold: 相关系数阈值，默认0.8        verbose: 是否打印详细信息    Returns:        list: 保留的alpha策略列表 (相互低相关)    """    # 复制所有alpha ID列表，避免修改原始数据    remaining_alphas = list(alpha_returns.columns)    selected_alphas = []    # 记录被剔除的alpha及原因    removal_info = []    # 当还有alpha未处理时继续循环    while remaining_alphas:        if verbose:            print(f"剩余alpha数量: {len(remaining_alphas)}")        # 选取当前列表中的第一个alpha        current_alpha = remaining_alphas[0]        selected_alphas.append(current_alpha)        if verbose:            print(f"选择alpha: {current_alpha}")        # 从剩余列表中移除当前alpha        remaining_alphas.remove(current_alpha)        # 如果没有剩余alpha，跳出循环        if not remaining_alphas:            break        # 计算当前alpha与所有剩余alpha的相关系数        correlations = {}        for other_alpha in remaining_alphas:            correlations[other_alpha] = alpha_returns[current_alpha].corr(                alpha_returns[other_alpha]            )        # 转换为Series并找出高度相关的alpha        corr_series = pd.Series(correlations)        high_corr_alphas = corr_series[corr_series > threshold].index.tolist()        # 记录哪些alpha被剔除以及原因        for alpha in high_corr_alphas:            removal_info.append(                {                    "reference_alpha": current_alpha,                    "removed_alpha": alpha,                    "correlation": corr_series[alpha],                }            )        # 从剩余列表中移除高度相关的alpha        remaining_alphas = [a for a in remaining_alphas if a not in high_corr_alphas]        if verbose and high_corr_alphas:            print(f"  移除了 {len(high_corr_alphas)} 个高相关alpha")    # 创建并保存剔除记录    if removal_info:        removal_df = pd.DataFrame(removal_info)        removal_df.to_csv("alpha_removal_records.csv", index=False)    # 打印结果统计    print("\n筛选结果:")    print(f"原始alpha数量: {len(alpha_returns.columns)}")    print(f"保留alpha数量: {len(selected_alphas)}")    print(f"剔除alpha数量: {len(alpha_returns.columns) - len(selected_alphas)}")    return selected_alphas
```

- 运行过程

![图片](images/img_4197b59eef.png)

---

## 讨论与评论 (11)

### 评论 #1 (作者: YX23928, 时间: 1年前)

感谢分享，请问一次大概能计算多少个alpha的相关性？

---

### 评论 #2 (作者: YZ70114, 时间: 1年前)

你好，麻烦问下这里的逻辑alpha_returns 参数是指池子里的PnL 数据吗？然后计算相似度不断排除，只留最后各自独特的alpha 再加工？

---

### 评论 #3 (作者: TL53163, 时间: 1年前)

您好，请问两两之间的相关系数是依据什么计算的？在“ [本地0误差计算自相关性](../KZ79256/本地0误差计算自相关性【即插即用版】代码优化.md) ”的文章中是需要查询Alpha的pnl数据来计算相关性的

---

### 评论 #4 (作者: EC12049, 时间: 1年前)

[TL53163 你好:](/hc/en-us/profiles/28917088671639-Tenglong-Li-TL53163)

在文章“ [本地0误差计算自相关性](../KZ79256/本地0误差计算自相关性【即插即用版】代码优化.md) ”的相关性计算是基于两个因子 **最近四年** 的每日盈亏数据的Pearson相关系数计算,其中每日盈亏数据即当前pnl减去前一日pnl----这在 [本地0误差计算自相关性](../KZ79256/本地0误差计算自相关性【即插即用版】代码优化.md) 的源码中有所体现

---

### 评论 #5 (作者: EC12049, 时间: 1年前)

[YX23928](/hc/en-us/profiles/27479819504663-YX23928) 你好:

目前来看没有限制,因为计算过程是在本地完成.

---

### 评论 #6 (作者: EC12049, 时间: 1年前)

[YZ70114](/hc/en-us/profiles/26918538763927-YZ70114)  你好:

这里Returns指的是因子回测期间每日的盈亏,即当日pnl减去前一日pnl

---

### 评论 #7 (作者: LR93609, 时间: 1年前)

感谢分享：有一个小问题

请问，第一个Alpha是基于什么排序？排序逻辑是什么

这里只看到你提取一个Alpha数据之后，就开始裁剪了。

---

### 评论 #8 (作者: EC12049, 时间: 1年前)

[lengrufeng(LR93609)](/hc/en-us/profiles/30244554462231-lengrufeng-LR93609)  这里的因子排序取决于使用者

文章 [从Gold跃升到GrandMaster——选好模板和相关性剪枝可能是关键](../AY17279/[Commented] 从Gold跃升到GrandMaster选好模板和相关性剪枝可能是关键论坛精选.md) 有所提及 ![图片](images/img_2bf48f5959.png)

---

### 评论 #9 (作者: ZH39644, 时间: 1年前)

感谢大佬分享，正好需要！

---

### 评论 #10 (作者: JM89654, 时间: 1年前)

请教一下，这个入参 alpha_returns 该怎么传，有点懵。

---

### 评论 #11 (作者: ZX59531, 时间: 1年前)

请问alpha_returns怎么得到？

---

