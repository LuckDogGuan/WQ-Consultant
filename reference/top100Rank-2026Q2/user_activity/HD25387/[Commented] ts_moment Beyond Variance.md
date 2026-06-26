# ts_moment Beyond Variance

- **链接**: [Commented] ts_moment Beyond Variance.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 34

## 帖子正文

`ts_moment(x, d, k)`  generalizes statistical moments. While k=2 gives variance, higher values capture skewness (k=3) and kurtosis (k=4).
Example:  `ts_moment(returns, 60, 3)`  flags asymmetry in return distributions, which may indicate behavioral biases. These higher moments can add depth beyond mean-variance frameworks.
👉 Question: Have you successfully used higher-moment features in alpha design, or do they add too much noise?

---

## 讨论与评论 (2)

### 评论 #1 (作者: HD25387, 时间: 8个月前)

Higher-moment features are powerful but fragile. I’ve found skewness can sometimes highlight behavioral effects, while kurtosis is trickier and often too noisy without careful smoothing. In practice, they work best when layered with more stable factors rather than used standalone.

---

### 评论 #2 (作者: AG14039, 时间: 6个月前)

Higher-moment features have a lot of potential but tend to be delicate. Skewness can occasionally capture behavioral patterns, whereas kurtosis is much harder to use reliably and usually requires significant smoothing to tame the noise. In my experience, these features perform best when they’re combined with more stable factors rather than deployed on their own.

---

