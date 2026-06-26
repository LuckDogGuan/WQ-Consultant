# 想请教一下sa中的 Selection Handling nan

- **链接**: [Commented] 想请教一下sa中的 Selection Handling nan.md
- **作者**: QX52484
- **发布时间/热度**: 1年前, 得票: 18

## 帖子正文

weight = (   1   *(prod_correlation)   *abs(self_correlation-0.5)   *(1-turnover));bool * weight 各位老师，我想请教一下像这样改变权重是如何影响到选取alpha的？ 是得到一个具体数值，而后在Selection Handling为nan的规则下，数值越高则从因子池中优先选取吗？

---

## 讨论与评论 (2)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

我记得这种情况下，想要选到数值高的，应该选positive才对，供参考。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。

---

### 评论 #2 (作者: QX52484, 时间: 1年前)

感谢游戏王的参考意见，仔细查看了run出来的alpha select_weight和learn文档进行了比较。加深了很多理解。

原来我目前筛选alpha时经常select_weight全部为0，只能被nan筛选或具体值如3000，3种Selection Handling无差别，影响了alpha的选取。（吐槽：经测试

in(classifications, "ATOM")和

in(competitions, "HCAC2025") select_weight为1，单独输入时，三种Handing方法结果一致（为正数，非空，非nan，没毛病）。而单独输入in(competitions, "ACE2023")或in(classifications, "SIMPLE") 则select_weight为0只能被nan选取。。。。。) 另测试，positive下，

!own&&turnover>0.1选取不到alpha，0..099则正常，这是什么限制？

---

