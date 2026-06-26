# 【PPAC 提交经验分享】注意！Prod Correlation 报错，实际卡点可能是 Power Pool 相关性

- **链接**: 【PPAC 提交经验分享】注意Prod Correlation 报错实际卡点可能是 Power Pool 相关性.md
- **作者**: JR23144
- **发布时间/热度**: 1年前, 得票: 91

## 帖子正文

各位还在肝 PPAC 的朋友们，大家好！

最近在提交 Power Pool Alpha 的时候，遇到了一个有点迷惑的报错情况，研究了一下，想把经验分享给大家，希望能帮到可能遇到同样问题的人。

**情况是这样的：**

大家知道，PPAC 的规则里明确写着 Power Pool Alpha  **豁免检查 Prod Correlation** 。同时，对于 “Self-Correlation” 中的  **“与已标记为Power Pool的Alphas的相关系数 ≤0.5”**  这一条，如果超过了，系统也是不会允许检查通过的。

**但诡异的地方来了：**

当我这个 Power Pool 相关系数（比如 0.6104）确实超过 0.5 时，我收到的 **并不是** 预期的明确 Power Pool 相关性超标的因此无法提交的 FAIL，而是直接收到另一个  **FAIL** ，提示信息是  **“Prod correlation 0.9311 is above cutoff of 0.7 and Sharpe not better by 10.0% or more.”**

**我的分析和结论是：**

尽管 PPAC 规则中 Prod Correlation 是豁免项，但当你的  **“Power Pool的Alphas的相关系数” 实际上已经大于 0.5 时，系统似乎会转而通过 Prod Correlation (>0.7) 这个条件来卡住你的提交，并给出 FAIL。**

也就是说，虽然错误信息显示的是 Prod Correlation 问题，但 **根本原因很可能是你的 Alpha 与现有 Power Pool Alpha 的相关性超过了 0.5 的阈值** 。它没有直接报 Power Pool 相关性超标导致 FAIL，而是“借用”了 Prod Correlation 的名义。

**给大家的提醒：**

所以，如果你在提交 Power Pool Alpha 时，明明知道 Prod Correlation 是豁免的，但最后却收到了因为 Prod Correlation 过高（比如 >0.7）而导致的 FAIL，那么请 **务必回头检查你的 Alpha 与现有 Power Pool Alphas 的相关系数是否已经超过了 0.5** 。这很可能才是真正的症结所在！

![图片](images/img_f47a17a7ca.png)

虽然规则说放低了条件，不查 Prod-Correlation，但还是需要我们注意，避免提交IS表现很差的Alpha，从而影响我们的 Value Factor。

希望这个小发现能帮到大家，祝各位提交顺利！

---

## 讨论与评论 (3)

### 评论 #1 (作者: DZ31817, 时间: 1年前)

这个逻辑其实是power pool alpha的优先级高于regular alpha，当power pool alpha检测不通过后，系统会将其作为regular alpha处理，看是否满足regular alpha的条件，如果满足则作为regular alpha提交，如果不满足就会返回regular alpha的检测失败信息。

---

### 评论 #2 (作者: FL39657, 时间: 1年前)

确实会有这种情况，感谢楼主提醒

---

### 评论 #3 (作者: WJ40623, 时间: 5个月前)

是说如果报错：

- Pure Power Pool submission does not match any Power Pool Theme.      没关系，只要符合Regular alpha的标准还可以继续提交吗？

---

