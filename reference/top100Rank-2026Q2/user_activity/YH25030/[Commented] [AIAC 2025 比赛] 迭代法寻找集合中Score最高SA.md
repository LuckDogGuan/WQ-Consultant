# [AIAC 2025 比赛] 迭代法寻找集合中Score最高SA

- **链接**: [Commented] [AIAC 2025 比赛] 迭代法寻找集合中Score最高SA.md
- **作者**: WX89624
- **发布时间/热度**: 7个月前, 得票: 16

## 帖子正文

最近一直在参加AIAC比赛，在此分享一些构建 SA（Super Alpha） 的实践与思考，望各位前辈大佬多多指教。

**比赛的核心规则：**

1. 选出parent Alpha；
2. 基于parent Alpha，利用AI生成child Alphas；
3. 使用child Alphas构建SA参赛。

**遭遇的困难：**

我遇到的主要问题是 child Alphas 产出数量不足，导致备选池深度不够，难以组合出高分的 SA。

要从根本上解决这一问题，关键在于优化 prompt 以提升 child Alphas 的产出效率。

然而比赛时间紧迫，我必须在现有条件下，基于已生成的 child Alphas 尽可能构建出高分的  SA，否则连完赛都成问题。 *（此前比赛规则尚未调整，每天只能提交 1 个 SA， 现在规则已改为每天最多可交 4 个）*

**小池子高 score 解决方案：**

由于不清楚比赛对 SA 评分的具体规则，一通摸索后，最终我还是决定采用迭代法：

1. 先从池子中选出 10 个child Alphas，构建基础 SA；（我选了self-cor 最低的10个，并遍历了全部 risk neutralization，选择 score 最高的作为基础 SA）
2. 从剩余 alpha 中逐一遍历，每次选取一个追加到 SA 中并重新回测；(self-cor 低者优先)
3. 若回测后 score 提升，则保留该 alpha；反之则剔除；
4. 如此循环，直至处理完池中所有 child Alphas。

**具体实现（手搓）：**

由于所有 child Alphas 均带有 tag 标记，可通过  `in(tags, "A") ` 表达式筛选出所有component child Alphas。

同时，利用 alpha 的 color 属性标记其状态：color == "BLUE" 表示当前迭代中临时选中，color == "GREEN" 表示最终入选。

SA 的 selection 表达式示例如下：

> `in(tags, "parent_alpha_id") && (color == "GREEN" || color == "BLUE")`

**总结：**

通过迭代法，我确实找到了 score 优于直接全选的SA组合。过程中观察到以下现象，供大家参考：

1. 多数情况下，Sharpe 和 Fitness 越高，score 也越高；
2. 追加的 Alpha 若其 PNL 曲线走势与当前最高分 SA 的 PNL 曲线差异明显，则往往能提高 score 或降低 prod-correlation；
3. 追加的 Alpha 若使用与 SA 现有component Alphas 不同的 Dataset，则往往能显著提升 score。

由于数据样本有限，上述观察仅供参考，尚不足以形成定论，恳请老师和各位批评指正。

---

## 讨论与评论 (3)

### 评论 #1 (作者: VC17729, 时间: 7个月前)

大佬你好，（我想详细请教一下，比如分享个案例），能不能展示一个你已经提交的比较满意的SA，期望值是达到大概什么样的指标，三五么？还是只要看sharpe和fitness越好越好？另外你一般会选取多少个child_alphas去组成一个SA？这个数量选择有什么讲究吗？谢谢呀大佬呢

---

### 评论 #2 (作者: YH25030, 时间: 7个月前)

谢谢分享。的确由于own的因子池子很浅，组到好的SA不容易。一旦组了一个好的SA，基本上很难选同样的子因子再组了。自相关性检测过不了。

---

### 评论 #3 (作者: WX89624, 时间: 7个月前)

[VC17729](/hc/en-us/profiles/29159021865623-VC17729)

你好。
1. AIAC 的 SA，我都是只看加分，交加分最多的。加分高的往往 sharpe 和 fitness 表现都不差，至少是 4+
2. 组 SA 的 child_alphas 数量问题，正常来讲应该是100左右才比较稳健。奈何比赛的池子比较难有那么多 child_alphas，所以我的方案是如文中分享，选10个 sc 最低的 child_alphas，构建基础 SA 然后慢慢往里追加，就交最终得分最高的那个，不管数量。目前看来一般都有 30~50 个 child_alphas。

---

