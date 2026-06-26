# JPN, HKG, TWN region after maxtrade

- **链接**: JPN HKG TWN region after maxtrade.md
- **作者**: DM28368
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

After the WQ update requiring maxtrade installation, it is very difficult to create alpha in the JPN, TWN, HKG regions with very low indexes. The alpha index to be able to submit is low. I want to ask if this is because the market in this region is bad or what? I hope you can answer.

---

## 讨论与评论 (4)

### 评论 #1 (作者: SD92473, 时间: 1年前)

That’s a very relevant concern. The difficulty you're facing in creating alphas forJPN, TWN, and HKGwith a high enoughalpha indexpost update (especially with themaxtrade requirement) may not be solely due to weak markets. Here are a few key factors to consider:Possible Reasons:Market Microstructure DifferencesThese markets have different liquidity profiles, trading behavior, and noise levels, which can make alpha signals less stable or harder to generalize.Lower Turnover and VolatilitySome stocks in JPN/TWN/HKG show lower turnover and price movement, reducing alpha opportunities, especially under stricter constraints.MaxTrade Constraint ImpactThemaxtrade installationpenalizes alphas with skewed or concentrated signals. In narrower universes or less liquid markets, it's harder to spread trades effectively, lowering the alpha index.Alpha SaturationThese regions might already have a high number of competing alphas in the Brain system, making it harder to produce something differentiated with good IC and low correlation.What You Can Do:Focus on universes with broader liquidity (e.g., large caps)Use neutralization and exposure constraints smartlyto reduce concentration.Benchmark your alpha vs. a simple baselinein the region — if even simple expressions score poorly, that might confirm region-level signal weakness.

---

### 评论 #2 (作者: DN45758, 时间: 1年前)

Creating strong alphas in JPN, TWN, and HKG is tough due to low liquidity, muted volatility, and maxtrade constraints. These regions may also face alpha saturation. Focus on large-cap stocks, use grouping and neutralization, simplify signals, check uniqueness, and test baselines to identify if issues are region-specific.

---

### 评论 #3 (作者: TV43543, 时间: 1年前)

Hello, as far as I know, Max Trade is a feature designed to improve the liquidity and scalability of Alphas by limiting daily position changes based on a fraction of the 20-day average daily volume (ADV20). When this feature is enabled, Alphas will adjust their positions less frequently in illiquid instruments, which helps reduce turnover and improve the Sharpe ratio. However, when Max Trade is turned on, metrics related to the Investability Constraint will not be calculated, and the performance of the Alpha (including Sharpe ratio and returns) may decrease compared to the original version.

---

### 评论 #4 (作者: AK40989, 时间: 11个月前)

This clears up a lot. I’ve been struggling with low alpha index in JPN, HKG, and TWN too post-maxtrade. If anyone has found approaches or datasets that still work well in these regions, would love to hear what’s helped.

---

