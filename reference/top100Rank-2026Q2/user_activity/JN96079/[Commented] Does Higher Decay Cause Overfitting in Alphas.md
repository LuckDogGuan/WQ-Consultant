# Does Higher Decay Cause Overfitting in Alphas?

- **链接**: [Commented] Does Higher Decay Cause Overfitting in Alphas.md
- **作者**: SD92473
- **发布时间/热度**: 9个月前, 得票: 21

## 帖子正文

I’m trying to better understand the role of decay values in alpha construction. Can using higher decay lead to overfitting by relying too heavily on past signals, and if so, what range of decay values tends to work best in practice? I’m particularly interested in how different decay settings influence both in-sample and out-of-sample performance.

---

## 讨论与评论 (10)

### 评论 #1 (作者: VK89116, 时间: 9个月前)

from my experience decay of 10 works well sometimes 5 but putiing a lot higher value can weaken signal.

---

### 评论 #2 (作者: TP85668, 时间: 9个月前)

Great question. Using a higher decay can sometimes lead to overfitting, because it places too much weight on historical signals and may artificially smooth short-term noise, making the alpha look stronger in-sample but weaker out-of-sample. On the other hand, too low a decay might fail to capture persistent effects. In practice, many researchers test a reasonable range (e.g., 3–10 days) and look for consistency across universes and time periods. The key is to validate whether the predictive power remains stable OS, rather than optimizing decay only for IS performance.

---

### 评论 #3 (作者: JC84638, 时间: 9个月前)

Higher decay doesn’t really cause “overfitting” in the usual sense. Very  *low*  decay is more prone to overfitting since it can chase short-term noise. Very  *high*  decay instead makes signals smoother and slower, which can underreact or lag rather than overfit. In practice, useful ranges depend on the signal type — e.g. 5–30 for short-term, 60–120 for medium-term, and 252+ for long-term trends (I often use 300+ days). The key is checking in-sample vs out-of-sample stability. (jzc

---

### 评论 #4 (作者: SP14747, 时间: 9个月前)

Really interesting points raised here. I’d add that decay isn’t just about avoiding overfitting or lag—it’s about aligning the memory of your signal with the horizon of the effect you’re trying to capture. Short-term anomalies usually need smaller decay to stay responsive, while structural or fundamental-driven effects can tolerate (or even require) longer decay to filter noise. The sweet spot comes from testing across horizons and checking whether the edge persists OS without excessive turnover or signal erosion.

---

### 评论 #5 (作者: SY65468, 时间: 9个月前)

Great question! Higher decay by itself doesn’t automatically cause overfitting — the real issue is when decay values are fine-tuned just to make the backtest look good without checking if they hold out-of-sample. If decay is set too high, the alpha can get stuck in old market patterns and fail to adapt when conditions change. If it’s too low, it reacts to every fluctuation and ends up chasing noise. The real overfitting risk comes from over-optimizing decay on a per-alpha basis, like tweaking it to the exact decimal that gives the best Sharpe in history, which usually won’t generalize to the future.

---

### 评论 #6 (作者: AY28568, 时间: 9个月前)

Good question, Decay decides how much importance we give to recent data compared to older data. If the decay is too high, the alpha may overfit by focusing too much on recent patterns that don’t last. If it’s too low, the signal may become weak and slow to react. There isn’t a single “best” value, since it depends on the type of alpha and the market. The safest approach is to test different decay values and compare both in-sample and out-of-sample results to find a balance between stable performance and quick adaptability.

---

### 评论 #7 (作者: AG14039, 时间: 9个月前)

Excellent question. Setting a higher decay can risk overfitting, as it gives excessive weight to historical data and may overly smooth short-term fluctuations, making the alpha appear stronger in-sample but weaker out-of-sample. Conversely, too low a decay might miss persistent effects. In practice, many researchers test a reasonable range (e.g., 3–10 days) and evaluate consistency across universes and time periods. The main goal is to ensure the alpha’s predictive power remains stable out-of-sample, rather than tuning decay solely for in-sample performance.

---

### 评论 #8 (作者: SG91420, 时间: 9个月前)

In essence, decay regulates the amount of weight you provide to previous signals while creating an alpha. While a shorter decay makes the signal more responsive to recent data, a larger decay spreads the signal over a longer horizon.

---

### 评论 #9 (作者: JN96079, 时间: 9个月前)

I concur with  [JC84638](/hc/en-us/profiles/28348489344151-JC84638) . However, I usually use decay settings between 4 and 20, mostly for short-term signals; otherwise, I might sometimes tweak the decay setting to around 50 to 70 to strengthen or control some downside of my signal, such as Sharpe and fitness.

---

### 评论 #10 (作者: AG14039, 时间: 9个月前)

In short, decay controls how much emphasis past signals have in an alpha. A shorter decay makes the alpha react quickly to recent changes, whereas a longer decay smooths the signal over a wider time horizon.

---

