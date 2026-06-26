# Sharing methods for building Alphas based on new datasets

- **链接**: [Commented] Sharing methods for building Alphas based on new datasets.md
- **作者**: TP19085
- **发布时间/热度**: 5个月前, 得票: 35

## 帖子正文

Hello everyone,
For  **new Consultants** , it’s common to have fewer ideas for building Alphas. In such cases, there is a method that I often use to generate new ideas:

👉  **Start from data fields that are widely used by many users and have many alphas built on them**  (for me, typically  **more than 100 alphas** ). You can filter for these in the  **Data**  section.

After selecting the data, try  **simulating with the raw data first** :

- **Matrix-type data** :
  Simulate  **without using any operators** , and test under different  **neutralization**  settings.
- **Vector-type data** :
  Only use very basic functions such as  **`vec_avg`**  to simulate.

Based on the simulation results, focus on data that shows relatively good  **PnL, Sharpe, and Fitness** , and then further optimize from there.

I’ve found this method to be particularly useful for  **Price & Volume** ,  **Analyst** , and  **Fundamental**  datasets.

I hope this sharing can help everyone in building Alphas.
Wishing you all success!

---

## 讨论与评论 (5)

### 评论 #1 (作者: AC34118, 时间: 5个月前)

Additionally one can focus on building ideas using new data set to increase diversity. Worldquant rewards it in long term.

---

### 评论 #2 (作者: MY82844, 时间: 5个月前)

Good idea — usually we’d sort by alphas and users first in the Data Explorer, then start testing from the top. Just one issue with this approach: we often end up with alphas that have high prod correlation but are only submittable to the power pool. Still, not bad as a quick start.

---

### 评论 #3 (作者: TP85668, 时间: 5个月前)

This is a very practical approach for beginners. Starting with  **widely used, high-coverage datasets**  and testing the  **raw signal before adding operators**  helps reveal the true data behavior and avoids early overfitting. Comparing performance across different  **neutralization settings**  is also key to distinguishing structural signals from pure risk exposure. Once the raw data shows an edge, further optimization becomes much more effective and robust.

---

### 评论 #4 (作者: HD25387, 时间: 5个月前)

Very solid framework. Testing raw or minimally processed data first is an underrated step—it quickly reveals whether the dataset carries genuine signal or just factor exposure. I’ve also found that checking prod correlation early helps decide whether it’s worth refining for the main pool or keeping it as a power-pool alpha.

---

### 评论 #5 (作者: BC83045, 时间: 5个月前)

Besides, I’ve found that checking prod and self-correlation early, even at the raw-data stage, can save time when deciding whether an idea is worth refining.

---

