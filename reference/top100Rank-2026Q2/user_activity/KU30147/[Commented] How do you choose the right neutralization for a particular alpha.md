# How do you choose the right neutralization for a particular alpha?

- **链接**: [Commented] How do you choose the right neutralization for a particular alpha.md
- **作者**: SK95162
- **发布时间/热度**: 2个月前, 得票: 12

## 帖子正文

In my case, I often see that industry or  **statistical**   **neutralisation**  gives  **higher**   **Sharpe**  but also  **increases**   **correlation** . On the other hand, using other neutralisations results in lower Sharpe but lower correlation.

So how do you decide in such situations? Do you prioritise standalone performance or lower correlation?

Is there any rule, threshold, or framework you follow while selecting neutralisation?

---

## 讨论与评论 (6)

### 评论 #1 (作者: RM79380, 时间: 1个月前)

Diversify your submissions across different universe

---

### 评论 #2 (作者: TL72720, 时间: 1个月前)

This is a classic trade-off, SK95162! I tend to lean towards prioritizing standalone performance, but I'm always mindful of the correlation increase. Have you found any particular industries or factors that consistently drive this Sharpe vs. correlation divergence in your alphas? It might be insightful to explore whether certain risk dimensions are more sensitive to neutralization choices than others.

---

### 评论 #3 (作者: TL72720, 时间: 1个月前)

SK95162, that's a classic tradeoff many of us face in alpha development. The question really boils down to your portfolio's overall construction goals and risk budget. If you're aiming for higher standalone alpha with a belief in its robustness, you might tolerate increased correlation. However, if diversification and reduced portfolio volatility are paramount, prioritizing lower correlation even with a slightly lower Sharpe might be the better path. Have you found any specific metrics, beyond Sharpe and correlation, that help you quantify the benefit of lower correlation in your broader portfolio context?

---

### 评论 #4 (作者: CW62782, 时间: 1个月前)

I usually don’t choose neutralization only by Sharpe. If industry or statistical neutralization improves Sharpe but pushes correlation too high, the alpha may look better alone but add less value to the pool.

---

### 评论 #5 (作者: KU30147, 时间: 1个月前)

Choosing neutralization depends on balancing standalone Sharpe and diversification value. Higher Sharpe with high correlation may add little portfolio benefit, while lower-correlation alphas improve diversification. Researchers usually prefer neutralizations that maintain acceptable Sharpe while reducing common risk exposures and portfolio overlap across signals.

---

### 评论 #6 (作者: AD47730, 时间: 28天前)

I prioritise both .

---

