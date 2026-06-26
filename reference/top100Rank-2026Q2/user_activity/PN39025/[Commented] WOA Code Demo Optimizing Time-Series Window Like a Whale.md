# WOA Code Demo: Optimizing Time-Series Window Like a Whale

- **链接**: [Commented] WOA Code Demo Optimizing Time-Series Window Like a Whale.md
- **作者**: DV64461
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

As a follow-up to my previous post on  **Whale Optimization (see here:  [https://support.worldquantbrain.com/hc/en-us/community/posts/31897002447255-Using-Whale-Optimization-to-Tune-Time-Series-Arguments-A-Double-Edged-Sword](/hc/en-us/community/posts/31897002447255-Using-Whale-Optimization-to-Tune-Time-Series-Arguments-A-Double-Edged-Sword) )** , here’s a simple implementation I’ve used to optimize the time window for time-series operators like  `ts_delta(close, X)` .

This code searches for the best  `X`  (e.g., 20–300) that maximizes a fitness function (here, simplified for demo):

```
import numpy as np

# Sample fitness function: replace this with actual alpha evaluation
def fitness_function(window):
    # Dummy logic for demonstration: replace with actual backtest score
    return -np.abs(window - 120) + np.random.normal(0, 1)  # max at window=120

def whale_optimization(num_whales=10, max_iter=20, lb=20, ub=300):
    whales = np.random.uniform(lb, ub, num_whales)
    best_whale = whales[0]
    best_score = fitness_function(best_whale)

    for t in range(max_iter):
        a = 2 - t * (2 / max_iter)
        for i in range(num_whales):
            r = np.random.rand()
            A = 2 * a * r - a
            C = 2 * r
            p = np.random.rand()
            l = np.random.uniform(-1, 1)

            if p < 0.5:
                if abs(A) < 1:
                    D = abs(C * best_whale - whales[i])
                    whales[i] = best_whale - A * D
                else:
                    rand_whale = whales[np.random.randint(num_whales)]
                    D = abs(C * rand_whale - whales[i])
                    whales[i] = rand_whale - A * D
            else:
                distance = abs(best_whale - whales[i])
                whales[i] = distance * np.exp(1 * l) * np.cos(2 * np.pi * l) + best_whale

            # Keep whales in bounds
            whales[i] = np.clip(whales[i], lb, ub)

            # Evaluate and update best
            score = fitness_function(whales[i])
            if score > best_score:
                best_score = score
                best_whale = whales[i]

    return int(best_whale), best_score

# Run optimization
best_window, best_fitness = whale_optimization()
print("Optimal Window:", best_window)
print("Best Fitness Score:", best_fitness)

```

**Results:**

- Optimized time window (e.g.,  `ts_delta(close, 127)` )
- Use in your alphas carefully, and cross-validate on other regions.

Let me know if anyone has tried other swarm methods like Firefly or Bat Algorithm for this kind of optimization!

Would you like a version tailored for multi-argument alpha tuning (e.g., optimizing both window and decay)?

---

## 讨论与评论 (12)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi, with this demo, your idea is quite good, but what I wonder is where you collect the data to implement it ?

---

### 评论 #2 (作者: UG81605, 时间: 1年前)

Its a great approach to optimize lookback days, but this can lead to overfitting of signal. WQ mentions many times that you shld use 5,20,60,120 and 250 as lookback days as these make sense in economic ways. 
And also a single alpha is never important rather than combination of diverse alphas are important. So its better to not dive in optimizations of alphas with parameters unnecessarily. This is what i think.

---

### 评论 #3 (作者: DV64461, 时间: 1年前)

[PN39025](/hc/en-us/profiles/1532011933942-PN39025) , I just optimize the times window, so just format it into your alpha string in python and then optimize it

---

### 评论 #4 (作者: DV64461, 时间: 1年前)

[UG81605](/hc/en-us/profiles/5342475745559-UG81605)  youre correct, but I also say that mind your code to avoid overfiting. But rather than that, it could be used to optimize other parts of alpha that are digit, somehow I think we could ultilize it.

You r also right about 1 alpha is not a big problem, but if you have the better alpha, it is also good for your combined portfolio.

---

### 评论 #5 (作者: ML46209, 时间: 1年前)

Nice demo! I agree that Whale Optimization is a neat approach for tuning time windows, but as UG81605 mentioned, it’s important to balance optimization with economic intuition to avoid overfitting. Combining multiple diverse alphas usually yields better robustness than overly fine-tuning single parameters. Would love to see a multi-parameter version if you decide to share!

---

### 评论 #6 (作者: AC63290, 时间: 1年前)

Its a great approach to optimize lookback days, but this can lead to overfitting of signal. WQ mentions many times that you shld use 5,20,60,120 and 250 as lookback days as these make sense in economic ways.
And also a single alpha is never important rather than combination of diverse alphas are important. So its better to not dive in optimizations of alphas with parameters unnecessarily. This is what i think.

---

### 评论 #7 (作者: TP18957, 时间: 1年前)

This is a great demonstration of how metaheuristic algorithms like Whale Optimization Algorithm (WOA) can be applied in quantitative finance for parameter tuning. While the optimization of  `ts_delta(close, X)`  is a good case study, I believe this framework could be extended to jointly optimize multiple parameters, such as decay rates in  `decay_linear`  or multiple window lengths in stacked operators. One idea is to evolve a solution vector, e.g.,  `[window1, decay1, window2]` , and use a composite fitness function that balances alpha performance across training and validation periods to mitigate overfitting. Would be interesting to compare this WOA approach with CMA-ES or even Bayesian Optimization for stability and convergence.

---

### 评论 #8 (作者: TP18957, 时间: 1年前)

Thanks for sharing this WOA-based approach—it’s not only educational but also a thoughtful reminder that innovation in alpha generation goes beyond just theory. I appreciate how you've made the algorithm digestible and framed it within the practical boundaries of alpha development. Even if some argue this kind of tuning can lead to overfitting, your emphasis on cross-validation and awareness of WQ’s economic intuition guidelines shows responsibility in experimentation. Sharing code like this helps others experiment and learn new techniques responsibly, and I truly believe these kinds of discussions help evolve the WQ Brain ecosystem in a collaborative and forward-thinking way.

---

### 评论 #9 (作者: SK90981, 时间: 1年前)

Whale Optimization offers a smart way to tune time-series parameters, but cross-validation is key to avoid overfitting and ensure robustness across regions.

---

### 评论 #10 (作者: SP39437, 时间: 1年前)

This is a strong example of applying metaheuristic algorithms like the Whale Optimization Algorithm (WOA) to quantitative finance, particularly for tuning alpha parameters. While optimizing a single parameter such as ts_delta(close, X) is insightful, extending this framework to simultaneously optimize multiple parameters—like decay rates in decay_linear or various window lengths in stacked operators—could unlock greater potential. A promising approach might involve evolving a solution vector, for instance [window1, decay1, window2], and using a composite fitness function that balances alpha performance over both training and validation sets to reduce overfitting risks. Comparing WOA’s performance with other methods like CMA-ES or Bayesian Optimization could also provide useful insights into stability and convergence speed. Thanks for sharing this WOA approach; it’s both educational and practical, highlighting the importance of responsible experimentation with cross-validation and economic intuition. Openly sharing such code fosters collaboration and helps advance the Brain ecosystem thoughtfully.

---

### 评论 #11 (作者: SS63636, 时间: 1年前)

The WOA-based approach to optimizing time-series parameters like the lookback window is both innovative and practical, especially when combined with proper cross-validation to mitigate overfitting risks. While it's true that WQ emphasizes standard economic timeframes (like 5, 20, 60, 120, and 250), exploring metaheuristic techniques like Whale Optimization can still offer value when applied responsibly. It’s exciting to think about extending this method to multi-parameter tuning or comparing it with alternatives like CMA-ES or Bayesian Optimization. Thoughtful experimentation like this can really drive meaningful advancements in alpha development.

---

### 评论 #12 (作者: DV64461, 时间: 1年前)

[SK90981](/hc/en-us/profiles/15224150642455-SK90981)  Absolutely, Whale Optimization is indeed powerful for parameter tuning! Cross-validation is critical here—do you have a preferred method or specific approach you find effective for maintaining robustness, especially when applying tuned parameters across different regions?

---

