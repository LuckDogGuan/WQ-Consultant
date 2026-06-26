# Tutorial for Beginners: trade_when(x, y, z) in Transformational Operators

- **链接**: [Commented] Tutorial for Beginners trade_whenx y z in Transformational Operators.md
- **作者**: XH93773
- **发布时间/热度**: 1年前, 得票: 58

## 帖子正文

The  `trade_when(x, y, z)`  operator is like a combination of a  **switch + fuse** :

- **Switch (x)** : Generates signals based on your rules (y) when conditions are met.
- **Fuse (z)** : Forces liquidation (turns to NaN) when dangerous conditions occur.
- **Other cases** : Maintains the previous signal (reduces frequent trading).

### Parameter Breakdown

This operator has three parameters, which can be understood as three questions:

1. **x (Trigger condition for trading)**
   *Question:*  When should the trading signal be updated?
   *Example:*   `volume >= ts_sum(volume, 5)/5`  (Act when trading volume surges beyond the 5-day average).
2. **y (New Alpha signal)**
   *Question:*  What new strategy should be used if trading is triggered?
   *Example:*   `rank(-returns)`  (Short stocks that have risen sharply recently).
3. **z (Exit condition)**
   *Question:*  When should forced liquidation occur?
   *Example:*   `abs(returns) > 0.1`  (Exit when daily price change exceeds 10%).

### Operational Logic (Like a Traffic Light)

🚨  **Red Light (z > 0)** : Must liquidate → Alpha = NaN
🟢  **Green Light (x > 0)** : Trade according to the new strategy → Alpha = y
🟡  **Yellow Light (Other cases)** : Maintain the original strategy → Alpha = Previous value

### Examples 🌰

**Case 1: Update strategy only when volume surges**

python

```
trade_when(  
    volume >= ts_sum(volume, 5)/5,  # Volume exceeds 5-day average  
    rank(-returns),                # Short recently大涨 (sharply rising) stocks  
    -1                             # Never trigger exit (since -1 < 0)  
)  

```

✅ When volume surges: Execute the  `rank(-returns)`  strategy.
🛑 At other times: Maintain the previous signal.
❌ Never exit: Because z = -1 never satisfies the exit condition.

**Case 2: Force liquidation during extreme price swings**

python

```
trade_when(  
    volume >= ts_sum(volume, 5)/5,  
    rank(-returns),  
    abs(returns) > 0.1  # Liquidate if daily price change exceeds 10%  
)  

```

💥 If price change exceeds 10%: Directly becomes NaN (liquidate).
📈 When volume surges and no extreme swing: Execute the new strategy.
😴 When no volume surge and no danger: Maintain the original position.

### Why Use This?

- **Reduce turnover rate** : Adjust positions only at critical moments to avoid random trading.
- **Control risk** : Use the z parameter for quick stop-loss/take-profit.
- **Flexible combination** : "Weld" multiple strategy conditions together.

### Common Questions for Beginners

- **Q: What if I don’t want a z condition for exiting?**
  → Set z to a value that is always < 0 (e.g., z = -1).
- **Q: Why use  `ts_sum(volume, 5)/5` ?**
  → This calculates the 5-day average trading volume.
- **Q: What does NaN mean?**
  → It’s like saying, "I’m out!" for this stock (close the position).

### One-Sentence Summary

`trade_when(x, y, z)`  = 🚦 Three-color traffic light + 🛑 Emergency brake

Mastering this will make your strategy act like a calm sniper, not a rookie firing randomly.

---

## 讨论与评论 (2)

### 评论 #1 (作者: PY38056, 时间: 1年前)

The  `trade_when(x, y, z)`  operator is a brilliant abstraction that captures strategic decision-making in trading with minimal code. By blending the logic of a  **switch**  (trigger-based action), a  **fuse**  (risk control), and  **signal persistence**  (to reduce noise), it encourages disciplined, event-driven trading. The traffic light analogy makes it especially intuitive—even for beginners—while allowing advanced users to finely control entry and exit logic.

---

### 评论 #2 (作者: JN96079, 时间: 11个月前)

Great information. While I struggle with the  **trade_when**  operator to reduce turnover, I now know how to use it in a more specific and better way. Thanks a lot for keeping informed!

---

