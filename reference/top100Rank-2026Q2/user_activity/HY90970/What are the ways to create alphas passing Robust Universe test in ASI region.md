# What are the ways to create alphas passing Robust Universe test in ASI region?

- **链接**: What are the ways to create alphas passing Robust Universe test in ASI region.md
- **作者**: HY90970
- **发布时间/热度**: 9个月前, 得票: 3

## 帖子正文

What are the ways to create alphas passing Robust Universe test in ASI region?I am facing difficulty in submitting the alphas in ASI region. What are some of the practices that should can be followed? This region has liquidity issues in real world trading because of which stricter constraint has been imposed which may help in OS performance. But, understanding the process to create such alphas is vital. Please share your insights for this.

---

## 讨论与评论 (1)

### 评论 #1 (作者: TP85668, 时间: 9个月前)

Great question. In the ASI region, the Robust Universe test is indeed stricter due to liquidity constraints. A few practices that usually help:Favor liquid universes: Apply filters like ADV- or volume-based operators to reduce exposure to illiquid names.Turnover control: Use decay, smoothing, and clipping to prevent sudden trading spikes.Neutralization: Neutralize against size/liquidity factors to avoid over-concentration in thinly traded stocks.Simplify signals: Simple, stable signals often pass robustness better than highly complex, noisy formulas.Cross-check universes: Test your alpha across multiple universes (TOP3000, MINVOL1M, etc.) to see if the signal is robust.Passing Robust Universe in ASI is less about “trick formulas” and more about designing alphas that are naturally stable, liquid, and tradable.

---

