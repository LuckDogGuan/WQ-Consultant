# 2024 super alpha比赛心得经验分享

- **链接**: [Commented] 2024 super alpha比赛心得经验分享.md
- **作者**: QH29412
- **发布时间/热度**: 1年前, 得票: 21

## 帖子正文

### surperAlpha比赛在2024年的可使用范围是USA，ASI，EUR

![图片](images/img_cd0a74d862.jpeg)

对同一个数据集，可以选择在各个universe上面创建super alpha。

个人经历：这篇是去年参加比赛的心得，略微修改。去年成为正式顾问后一个多月就参加这个SA的比赛，比赛结束后权限就收回了。我靠自己的努力终于在去年圣诞节获得了属于自己的SA权限，总来的说经验还要靠比赛来提升吧。

# Selection Expression 部分

**Alpha Properties**  **选择**

1. 一般选择turnover < 0.30，对ASI区域，建议使用更小的turnover，在使用 [Risk Neutralized Alphas](https://platform.worldquantbrain.com/learn/documentation/advanced-topics/getting-started-risk-neutralized-alphas) 时会拉高整体的turnover。

a,  筛选alpha 观察整体turnover < 0.10时，建议使用“Slow Factors”设置，效果更佳。

b,  筛选alpha 观察整体turnover > 0.20时,  建议使用“Fast Factors”设置，效果更佳。

1. 一般选择prod_correlation< 0.6，可以选出idea比较新的alpha，最后的prod-corr 也会较好。

3.  平时跑过的数据集，多留意它的特点。有的DS可能sharp优秀，margin一般；有的DS是margin 很好，但turnover很高。可以把他们放在一起做一个增强，可以通过 category 或者DS in(datasets, "fundamental6") 来选取你的alpha 组合。

**SuperAlpha selection features**  **选择-Auther information**

1. 一般设置 author_returns_to_drawdown>2,官方建议是author_returns_to_drawdown > 1 && author_returns_to_drawdown < 4。可以根据不是数据集的alpha情况调整，这个参数有时可有可无，但有时至关重要。
2. Author Fitness or Author Sharpe 效果类似，一般设置author_fitness >= 2 or author_sharpe >= 2 ,个人比价倾向于fitness，具有很强的综合性且一般不容易通过算法调整，能够体现author的综合素质。但是，不同的数据集下面的alpha的特性不同，为了满足能select 出足够多的alpha，具体参数适当调整。
3. 我大部分是基于 Selection Handling = "Non-Zero"创建的super alpha。

## 🌰例子： ![图片](images/img_680a1c10c3.jpeg)

## Combo Expression 部分

USA建议时间窗口选择：250，500；ASI建议时间窗口选择：60，120，250.

stats = generate_stats(alpha); ts_mean(stats.returns, 500)；

---

## 讨论与评论 (14)

### 评论 #1 (作者: ML42552, 时间: 1年前)

感谢分享，另外想问大佬sa有没有工程化用机器跑。

预祝大佬在2025年的sa大赛中获得佳绩！

---

### 评论 #2 (作者: YB15978, 时间: 1年前)

感谢楼主分享，有时候明明选择了10个alpha，但运行comb时还是提示alpha数量小于10不知道是什么原因，之前以为是user阶段提交的alpha不能使用，但排出user阶段的alpha后，最近又出现这个问题，请问楼主知道大概是什么原因吗

---

### 评论 #3 (作者: QH29412, 时间: 1年前)

hello,  [ML42552](/hc/en-us/profiles/27182530443671-ML42552)   我没有用程序跑super alpha，看个人习惯。

---

### 评论 #4 (作者: QH29412, 时间: 1年前)

YB15978， 你是选的都是自己的alpha 么？ select 部分的右上角， 有个“View all” 的蓝色小字，你可以点进去看看所有的alpha列表。自己的alpha，点name标签也可以看详情页的。你排查一下，是不是显示的问题。最后的最后，还有问题提交support。

---

### 评论 #5 (作者: ZS59763, 时间: 1年前)

很有用的分享，点赞！！！

这边有一个小小的问题需要讨论：prodcor小于0.6，或者小于0.5，是可以选到cor低的因子的，但如果大家都放了这个设置，意味着大家都在相同的因子上做组合，这个是不是又背离初衷了呢？

==============================================

“我的回合，抽卡！“——《游戏王》

==============================================

---

### 评论 #6 (作者: QP72475, 时间: 1年前)

大神如果有空出一个combo expression教程就更好了。

---

### 评论 #7 (作者: DT40395, 时间: 1年前)

感谢楼主分享！对于combo selection可以再多举些例子吗？另外大佬组合所用的因子都是自己的吗？            发现用自己的因子去组合自相关性还是挺高的，另外SA比赛的得分会对自相关性以及prod相关性有评分吗？ 2025SA比赛已经提交了两个SA因子，不过目前还是只会比较简单的一些selection表达，希望和大佬多多探讨！

---

### 评论 #8 (作者: XC66172, 时间: 1年前)

感谢大佬分享，SAC比赛到一半再看这篇文章，感觉很有共鸣~

我发现我提交的很多SA都是使用了某些中性化的 (SLOW, FAST, RAM等），不过确实可以再看一下SLOW和FAST是否真的和TURNOVER存在一定关系

prod_correlation的阈值倒不是我SELECT的选项。因为我觉得prod_correlation大一些，是因为大家都觉得该因子好，也许是它本身的数据确实很亮眼。

---

### 评论 #9 (作者: JB71859, 时间: 1年前)

==============================================

感谢大佬的分享，结合你的方式在通过ai来组合，让我得到了很多可以提交的sa，期待大佬做关于sa新的分享。

==============================================

---

### 评论 #10 (作者: BW14163, 时间: 9个月前)

讲的很细致，很全面，谢谢分享

---

### 评论 #11 (作者: CW99271, 时间: 8个月前)

太优秀了，讲得很详细，流程很清楚，等我学会了，过来跟你分享一下过程

---

### 评论 #12 (作者: SL81184, 时间: 6个月前)

感谢大佬分享

---

### 评论 #13 (作者: YQ84572, 时间: 6个月前)

这篇比赛心得很实在！我验证了 `prod_correlation<0.6` 确实能筛出新奇想法，PC控制得很好。按作者建议，我用 `author_fitness>=2` 和 `turnover<0.3` 筛选，组合的稳健性明显提升。在亚洲市场用小换手因子，慢速设置效果更好。新手注意别只看夏普，综合fitness和低PC才是关键。

---

### 评论 #14 (作者: LJ12230, 时间: 2个月前)

感谢大佬分享！

---

