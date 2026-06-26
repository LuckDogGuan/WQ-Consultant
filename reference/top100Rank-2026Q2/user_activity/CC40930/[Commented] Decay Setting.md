# Decay Setting

- **链接**: [Commented] Decay Setting.md
- **作者**: KK28219
- **发布时间/热度**: 4年前, 得票: 8

## 帖子正文

The Decay function in the Alpha settings block is a linear decay function over a period of n days where the value on day "t" is equal to the weighted average of the values from day "t" to day "t-n".

What exactly does this do to the alpha? Does this linear decay function change all input data being used in the alpha? So the actual values are not being used, but rather every input value is changed to a weighted average? In this case, why is the default decay set to 4?

---

## 讨论与评论 (7)

### 评论 #1 (作者: AS34454, 时间: 4年前)

Decay does not change the input values, it performs a weighted average on the output of your Alpha. The output of your Alpha is a  [vector of weights](/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=W-,Weight,-BRAIN%20platform%20uses) . The value of the weights get smoothened by the Decay operator. 

As a crude example- if in the recent 5 days, the Alpha provides weight of 0, 0.2, 0.4, 0.6, 0.8  to one stock. So Alpha[Today] = 0.8, Alpha [today -1] = 0.6 and so on.

Then after Decay = 5. The Alpha[Today] will be replaced by
alpha_modified = (5*alpha[today] + 4*alpha[today-1] + ... + 1*alpha[today-4]) / 15 = 0.53

No specific reason for default setting of 4.

---

### 评论 #2 (作者: KK28219, 时间: 4年前)

Thanks for the response! I understand what Decay actually does. A follow up question if I may - Is the purpose of Decay to reduce the variance in weights assigned to a particular stock over multiple days? If so, what is the fundamental logic/rationale behind doing so? If not, why is Decay even necessary?

Thanks in advance!

---

### 评论 #3 (作者: AS34454, 时间: 4年前)

Your question contains the answer :). Decay helps manage variance. Variance is another form of risk.
There are multiple  [explanations](/hc/en-us/articles/5973492634903-Can-you-explain-what-decay-is-) regarding Decay on the platform: Decay can helps smooth the Alpha values, reduce turnover, manage risk etc.

---

### 评论 #4 (作者: KK28219, 时间: 4年前)

Thanks again!

---

### 评论 #5 (作者: XL31477, 时间: 1年前)

**Hey  [KK28219](/hc/en-us/profiles/6255448444951-KK28219) ! You got it right. The decay function mainly aims to manage variance indeed. By smoothing the Alpha values, it makes the weights assigned to stocks more stable over time. This helps reduce turnover too as it won't change the weights drastically. And as variance is a form of risk, managing it is crucial for a better-performing strategy. There's no fixed rule for the default setting of 4, but it's a common choice to start with and adjust based on your specific needs.**

---

### 评论 #6 (作者: DK20528, 时间: 1年前)

The  **Decay**  function in the Alpha settings block applies a linear decay to the input data used in your alpha expression. It modifies how past data points are weighted when calculating the alpha value. Here's a detailed explanation of how it works and its effect:

### 1.  **What does the linear decay function do?**

The decay function effectively weights the input data over a period of  `n`  days. For each day  `t` , it computes a  **weighted average**  of the data from the previous  `n`  days, where more recent data points are given a higher weight, and older data points are given progressively lower weights. The decay function smooths the data to reflect a time-dependent weighting, so recent data points influence the alpha more than older ones.

- **Example of Linear Decay** :
  - If  `n = 4` , the weighted average of the last 4 days is calculated, with the most recent day receiving the highest weight, and the previous days receiving progressively smaller weights.
  - On day  `t` , the value of the alpha is adjusted based on this weighted average, with each day having a contribution proportional to its recency.

### 2.  **Does the decay function change the input data?**

Yes, the decay function modifies the input data. Instead of using the raw values for each day, it uses the  **decayed value** , which is the weighted average of the data from day  `t-n`  to day  `t` .

This means:

- If you apply decay, the alpha no longer directly uses the original values for each input variable (e.g., stock prices, indicators) but uses the  **smoothed/weighted average**  of those values over a defined period ( `n`  days).

### 3.  **Why does this happen?**

The purpose of the decay is to give more importance to  **recent information**  while reducing the influence of older data. This is important for capturing more timely signals in a dynamic market. Markets tend to change over time, and recent data is often more relevant than older data.

### 4.  **Why is the default decay set to 4?**

The default decay of 4 is likely a balanced choice for capturing recent market signals while still incorporating some historical context. The idea is:

- A decay of 4 strikes a balance between giving enough weight to recent data (for capturing momentum) while not completely ignoring older data that might provide relevant context or trends.
- A decay value that's too small (e.g., 1 or 2) would make the alpha overly sensitive to short-term fluctuations, potentially making it noisy.
- A decay value that's too large (e.g., 10 or 20) would dampen the impact of recent events and reduce the alpha's responsiveness to changes in market conditions.

A decay of  **4**  is a reasonable starting point for many alphas, as it reflects recent market behavior while considering a short history of data.

### 5.  **Effect on Alpha Construction**

When the decay is applied, it impacts how the signals and inputs interact over time. The smoothed inputs will produce an alpha that is less volatile and more focused on trends, rather than sharp, sudden movements. It can help reduce noise in the alpha signal, making it more stable and reducing overfitting to short-term data.

In summary:

- The  **decay**  adjusts the input data by applying a weighted average of the past  `n`  days, with recent data having a greater influence.
- The  **default decay of 4**  is a reasonable balance between capturing recent trends and avoiding excessive noise or smoothing.

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

- The decay function  **modifies the input data**  to give more weight to recent values and less weight to older ones, smoothing the data in a linear manner over a window of  `n`  days.
- It  **does not change the alpha formula itself** , but it changes how the inputs to that formula are represented.
- The default decay of 4 days likely balances responsiveness to recent changes with stability from historical trends. This period is typically useful in capturing medium-term signals while still accounting for recent market movements.

---

