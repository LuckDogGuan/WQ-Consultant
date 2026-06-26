# Understanding Simulation Universes in BRAIN

- **链接**: Understanding Simulation Universes in BRAIN.md
- **作者**: RM79380
- **发布时间/热度**: 3个月前, 得票: 1

## 帖子正文

**Understanding Simulation Universes in BRAIN**

In BRAIN, the simulation universe defines the group of stocks used to evaluate an alpha. Standard universes such as TOP3000, TOP2000, and TOP1000 are based on liquidity, measured by the average dollar trading volume over the past three months.

For example, TOP3000 contains the 3,000 most liquid stocks in a region, while TOP2000 includes the top 2,000, making it a subset of TOP3000.

An important consideration is that larger universes include less liquid stocks. These stocks may introduce higher transaction costs and greater market impact during trading. Therefore, when designing alphas for larger universes, it is often helpful to apply weighting methods (such as market cap or trading volume) to reduce trading intensity in low-liquidity stocks and improve overall strategy efficiency.

---

## 讨论与评论 (0)

