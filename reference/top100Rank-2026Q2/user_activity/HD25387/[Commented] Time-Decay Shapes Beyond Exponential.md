# Time-Decay Shapes: Beyond Exponential

- **链接**: [Commented] Time-Decay Shapes Beyond Exponential.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 35

## 帖子正文

While exponential decay is standard, hump decay gave me better balance in some mean-reversion tests.
👉 Do you think experimenting with different decay kernels is worthwhile, or is exponential “good enough” for most cases?

---

## 讨论与评论 (2)

### 评论 #1 (作者: TP85668, 时间: 8个月前)

Great point! Exponential decay is indeed the standard, but experimenting with other shapes like hump decay can uncover different market dynamics. In some cases, alternative decay kernels may better capture short-term reversals or delayed effects. I think it’s worthwhile to test different shapes as long as we validate out-of-sample performance to avoid overfitting.

---

### 评论 #2 (作者: HD25387, 时间: 8个月前)

Really interesting topic. I’ve also found that different decay shapes can highlight dynamics that exponential sometimes smooths over — especially in mean-reversion or regime-shift contexts.
Testing a variety of kernels feels worthwhile, as long as validation stays rigorous. Curious to see what others have observed here.

---

