# alpha ideas

- **链接**: [Commented] alpha ideas.md
- **作者**: FK13997
- **发布时间/热度**: 3个月前, 得票: 2

## 帖子正文

how does decay alpha affect the is ladder shape,fitness and turnover and what is the recommended decay to use ,either <or> recommended value.

---

## 讨论与评论 (2)

### 评论 #1 (作者: RR84421, 时间: 3个月前)

Umm increase in decay leads to decrease in turnover but this is not only the factor that affects your sharpe as there are many things you have to consider like fitness , drawdown, returns, margins….. and these are manipulated by several operators directly or indirectly.

Use Learn section to know more about the terms…

---

### 评论 #2 (作者: FZ60707, 时间: 2个月前)

Higher decay  smooths the alpha, reduces turnover, and often improves fitness if the signal is noisy—but it can flatten the ladder shape by lowering responsiveness. Lower decay  keeps the alpha more reactive, increasing turnover and potentially sharpening the ladder, but may hurt stability. There's no universal "recommended" value; try starting around 5 and optimize based on your alpha's half-life and backtest results.

---

