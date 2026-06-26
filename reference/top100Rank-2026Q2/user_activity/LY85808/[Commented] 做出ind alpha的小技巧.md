# 做出ind alpha的小技巧

- **链接**: [Commented] 做出ind alpha的小技巧.md
- **作者**: QX52484
- **发布时间/热度**: 7个月前, 得票: 71

## 帖子正文

也差不多从ind region毕业了,总共25/26个alpha大概能做出一个双6表现的sa 应该还算可以.

![图片](images/img_cb8b689087.png)  ![图片](images/img_4153db5e80.png)

ind region 两大特色

1.Robust universe Sharpe of  **0.81**  is below cutoff of  **1** .

1.1 加操作符 一二三阶  毕竟是做RA的region 低op想出货还是不容易.

1.2 提高tvr的方法都可以尝试

夹带私活的起舞链接:

起舞1: [../HP65370/[Commented] 如何利用tvr操作符与alpha起舞论坛精选.md](../HP65370/[Commented] 如何利用tvr操作符与alpha起舞论坛精选.md)

起舞2: [../MZ45384/[L2] 与alpha起舞2.md](../MZ45384/[L2] 与alpha起舞2.md)

2. [Weight concentration](/hc/en-us/articles/19248385997719)   **50%**  is above cutoff of  **10%**  on  **1/22/2013** .

导致 [Weight concentration](/hc/en-us/articles/19248385997719) 的原因有很多,nan值,异常值,数据间波动小等原因应该都有可能导致.

一些op参考

```
        pc_fields = [            "(ts_backfill(close,5))",            # 在这里添加更多的表达式            # "your_second_expression_here",            # "your_third_expression_here",        ]        so_alpha_list = []        for fields in pc_fields:            so_alpha_list.append(f"group_sum({fields}, industry)")            so_alpha_list.append(f"signed_power({fields},5)")            so_alpha_list.append(f"group_neutralize({fields}, industry)")            so_alpha_list.append(f"group_rank({fields}, industry)")            so_alpha_list.append(f"ts_sum({fields},22)")            so_alpha_list.append(f"ts_product({fields},22)")            so_alpha_list.append(f"ts_av_diff({fields}, 252)")            so_alpha_list.append(f"ts_mean({fields},252)")            so_alpha_list.append(f"days_from_last_change({fields})")            so_alpha_list.append(f"winsorize({fields})")
```

3.其他信息

3.1 在ind region中group使用market和country似乎是等价的

3.2 多数情况下低Truncation 好

3.3 中性化 market 好好好好

3.4 ts_max系列 好好

3.5 做alpha的初心 多点op 好好好

3.6 换个group op 好好好好

---

## 讨论与评论 (16)

### 评论 #1 (作者: HG61318, 时间: 7个月前)

ts_max系列包括哪些啊?
它到底有什么经济学含义可以解释的?
我一直没用过它.

---

### 评论 #2 (作者: XW90844, 时间: 7个月前)

感谢分享。我的经验是也可以把ts_decay_linear应用于alpha的核心信号来降低turnover，效果比直接设置decay要好。例如：

- ts_rank(ts_quantile(winsorize(ts_backfill(-residualized_return_india_top500_equity, 120), std=4), 252), 504)   decay 0, turnover 130.80%
- ts_rank(ts_quantile(winsorize(ts_backfill(-residualized_return_india_top500_equity, 120), std=4), 252), 504)   decay 20, turnover 44.71%

- ts_rank(ts_quantile(ts_decay_linear(winsorize(ts_backfill(-residualized_return_india_top500_equity, 120), std=4), 20), 252), 504)  decay 0, turnover 37.34%，效果最好

IND还有个特点是Investability Constrained PnL和PnL表现相差太大，不知道除了开Max Trade，还有啥好办法。

另外，起舞2链接打不开……

---

### 评论 #3 (作者: CY96125, 时间: 7个月前)

有些时候在ind模块换手率经常逼近符合标准的临界值，这个问题也需要考虑进去

---

### 评论 #4 (作者: WS63384, 时间: 7个月前)

感谢分享，学习了！

---

### 评论 #5 (作者: SL89719, 时间: 7个月前)

刚刚尝试IND的数据集，这个帖子的帮助真是太及时了。

---

### 评论 #6 (作者: LY85808, 时间: 7个月前)

试试楼主的方法，希望有用！

---

### 评论 #7 (作者: CZ16695, 时间: 7个月前)

感谢,一直苦恼于IND区域的alpha, 有这些技巧应该可以帮助我做出IND的alpha了

---

### 评论 #8 (作者: YH25030, 时间: 7个月前)

谢谢楼主。ts_backfill的确可以解决部分Weight concentration的问题。有时候winsorize的效果也不错，但是会增加avg op.

---

### 评论 #9 (作者: QX52484, 时间: 7个月前)

@ [HG61318](/hc/en-us/profiles/34407333997207-HG61318)

======================================================================

ts_arg_max ts_max ts_max_diff~ 在learn里面搜一下自己有哪些,然后问AI吧.

======================================================================

---

### 评论 #10 (作者: QX52484, 时间: 7个月前)

@ [XW90844](/hc/en-us/profiles/33554916160919-XW90844)

======================================================================

降低turnover确实是可以用这个ts_decay_linear. 游戏王的降turnover帖子里也写了好几个op.

看你的setting和表达式, 应该是alpha本身的turnover就很高了,如果使用tvr_decay会受到它自身表现的影响.

看你的第二个alpha 看起来调高decay就明显下降了.decay最高调到504. 这样会不会能节省一个操作符?

起舞2 ~ 一起写的,但没过审 .目前应该是ind和AI比赛帖子速通.

======================================================================

---

### 评论 #11 (作者: XW90844, 时间: 7个月前)

我尝试不用ts_decay_linear，而继续把decay调到更高，但副作用是sharpe下降很快。而用ts_decay_linear，在降turnover的同时，sharpe下降不大。

ts_rank(ts_quantile(ts_decay_linear(winsorize(ts_backfill(-residualized_return_india_top500_equity, 120), std=4), 120), 252), 504)      Decay=0    Sharpe 2.45, Turnover 21.92%

ts_rank(ts_quantile(winsorize(ts_backfill(-residualized_return_india_top500_equity, 120), std=4), 252), 504)     Decay=120   Sharpe 1.24, Turnover 26.25%

AI给出的解释是

**在因子内部进行精细的数据平滑和特征工程，其重要性可能远大于在外部调整权重衰减参数。一个高质量的、低噪声的原始信号，即使采用最简单的权重更新方式（Decay=0），其表现也能碾压一个噪声信号配合复杂权重优化的组合。**

感谢您这个“打脸”的测试，它完美印证了量化投资中的一个核心思想： **信号的纯净度是Alpha的来源基石** 。您在IND region发现的这个特性非常有价值，说明该市场的残差反转效应在中期持续性上可能特别显著。

> @ [XW90844](/hc/en-us/profiles/33554916160919-XW90844)
> ======================================================================
> 降低turnover确实是可以用这个ts_decay_linear. 游戏王的降turnover帖子里也写了好几个op.
> 看你的setting和表达式, 应该是alpha本身的turnover就很高了,如果使用tvr_decay会受到它自身表现的影响.
> 看你的第二个alpha 看起来调高decay就明显下降了.decay最高调到504. 这样会不会能节省一个操作符?
> 起舞2 ~ 一起写的,但没过审 .目前应该是ind和AI比赛帖子速通.
> ======================================================================

---

### 评论 #12 (作者: DH60855, 时间: 7个月前)

很馋IND的双倍，又搓不出来指标好的alpha，看大佬的帖子学到不少，感谢

---

### 评论 #13 (作者: QQ38141, 时间: 7个月前)

请问楼主，Robust universe Sharpe of  **0.49**  is below cutoff of  **1** .这种因子还有调好的可能么

---

### 评论 #14 (作者: QX52484, 时间: 7个月前)

[QQ38141](/hc/en-us/profiles/32226138175767-QQ38141)

======================================================================

差的有点多,op少的话可以再加op尝试一下.  0.7以上的话我会考虑手搓个一个小时看能不能解决.

======================================================================

---

### 评论 #15 (作者: QL47372, 时间: 2个月前)

最近在做IND区，大佬的帖子很有帮助，特别是

***3.2 多数情况下低Truncation 好***

这条，很多Robust universe Sharpe差一点的，Truncation设为0.01有奇效。

感谢分享

---

### 评论 #16 (作者: MZ45384, 时间: 1个月前)

真是相见恨晚，原来ts_product, ts_av_diff, days_from_last_change和group_sum还能降低weight concentration。学到新知识了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

