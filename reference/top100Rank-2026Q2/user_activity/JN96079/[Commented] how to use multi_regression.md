# how to use multi_regression

- **链接**: [Commented] how to use multi_regression.md
- **作者**: JL16510
- **发布时间/热度**: 9个月前, 得票: 40

## 帖子正文

Hello everyone.Regarding multi_regression(y, x1, x2,..., days=0, lag=0, solver="SVD"),description says it's solver can be "SVD"(default), "QR" or "NORMAL".What exactly does the solver refer to?Under what circumstances should SVD(or other) be used?And I'm very eager to know under what circumstances multi_regression  is equivalent to ts_regression.
Thank you very much.

---

## 讨论与评论 (7)

### 评论 #1 (作者: PM24512, 时间: 9个月前)

This post contains numerical method used to compute regression coefficients.

- **SVD** : most stable, handles multicollinearity well slower.
- **QR** : faster than SVD, good for well condition problems.
- **NORMAL** : fastest but least stable if features are correlated.

Thanks for sharing this useful insight with us.

---

### 评论 #2 (作者: TP85668, 时间: 9个月前)

Great question! The solver here refers to the method used to compute the regression coefficients (e.g., SVD, QR, Normal equations). SVD is generally more stable in cases with multicollinearity or ill-conditioned matrices, while QR and Normal may be faster when the problem is well-conditioned. As for equivalence,  `multi_regression`  can align with  `ts_regression`  when you’re essentially regressing one variable on time-lagged versions of itself, but  `multi_regression`  is broader since it allows multiple explanatory variables. Thanks for raising this topic!

---

### 评论 #3 (作者: JN96079, 时间: 9个月前)

Hi  [JL16510](/hc/en-us/profiles/25889743296151-JL16510) , on Brain, typical regression tasks involve financial predictors (features) which may be correlated, some of which may be noisy. Also, “lag” and “days” parameters may mean using past values, which can introduce multicollinearity or ill-conditioned matrices.

So:

- Use  **SVD**  by default, especially if you are not sure about your features, or suspect multicollinearity, or if the regression sometimes fails / gives wild coefficients with NORMAL.
- Use  **QR**  if SVD is slower than you can tolerate, but you want more stability than NORMAL. A good tradeoff.
- Use  **NORMAL**  for speed when everything is clean, and you just need “fast” approximate regression, for exploratory work.

For competent research, consider the following information as your starter with the above;

## *Equivalence/relations: multi_regression vs ts_regression*

First, what is  ***`ts_regression`*** :

- ##### ***ts_regression(y, x, d, lag = 0, rettype = 0)*** ; runs regression of  *y*  against x, but over time dimension (i.e. you regress time series of y on time series of x), possibly with lags, maybe out‐of‐sample over “days”, etc.

- ***multi_regression(y, x1, x2,..., days=0, lag=0, solver="SVD")*** ; regressors are multiple features (x1, x2, …), possibly with lag or days etc.

***`multi_regression(y, x1, x2, …)`***  is equivalent to doing several  ***`ts_regressions`***  (one per xi) or a combined  ***ts_regression*** .

Happy learning! ^JN

---

### 评论 #4 (作者: AG14039, 时间: 9个月前)

Excellent question! Here, the “solver” refers to the technique used to calculate regression coefficients, such as SVD, QR decomposition, or Normal equations. SVD tends to be more stable, especially when dealing with multicollinearity or poorly conditioned matrices, whereas QR and Normal methods can be faster when the problem is well-behaved. Regarding equivalence,  `multi_regression`  can match  `ts_regression`  when regressing a single variable on its own time-lagged values, but  `multi_regression`  is more general since it accommodates multiple explanatory variables. Thanks for bringing this up!

---

### 评论 #5 (作者: YQ51506, 时间: 9个月前)

关于multi_regression中solver参数的选择，SVD、QR和NORMAL分别对应不同的矩阵分解方法。SVD（奇异值分解）在处理病态矩阵时更稳定，适合特征值差异较大的情况；QR分解计算效率较高，适合常规回归问题；NORMAL直接求解正规方程，计算简单但数值稳定性较差。在WorldQuant Brain回测中，我通常根据因子数据的条件数选择solver - 数据质量较好时用QR，存在多重共线性时用SVD。至于multi_regression与ts_regression的等价性，当days=0且lag=0时，两者确实等价，都是截面回归。不过ts_regression更专注于时间序列特性，而multi_regression更通用。

---

### 评论 #6 (作者: SJ17125, 时间: 9个月前)

In  `multi_regression(y, x1, x2, …, days=0, lag=0, solver="SVD")` , the  **solver**  refers to the algorithm used to solve the linear least-squares problem behind the regression:

- **SVD (Singular Value Decomposition)**  – This is the most numerically stable method. It’s slower but handles ill-conditioned or nearly collinear predictors (x’s) well. Default for a reason.
- **QR (QR Decomposition)**  – Faster than SVD and still reasonably stable. Good for moderately sized, well-behaved data.
- **NORMAL (Normal Equations)**  – Solves directly via (X′X)−1X′Y(X'X)^{-1}X'Y(X′X)−1X′Y. This is the fastest but least stable; it can blow up if predictors are highly correlated or poorly scaled.

So, if your predictors are highly correlated or you’re unsure about the conditioning of your data,  **stick with SVD** . If you know your design matrix is well-behaved and want speed,  **QR**  is a good compromise.  **NORMAL**  should only be used when performance is critical and the predictors are clean and low-collinearity.

Regarding  **`multi_regression`  vs.  `ts_regression`** :

- `multi_regression`  fits a  **cross-sectional regression**  at each point in time across multiple x’s (predictors).
- `ts_regression`  fits a  **time-series regression**  of one variable on another over time.

They become  **equivalent**  if you’re effectively regressing one series on others  **over time for a single entity**  (i.e., no cross-sectional dimension) with the same lag and days parameters. In other words, when you’re only running a single time series regression with multiple predictors,  `multi_regression`  collapses to the same operation as  `ts_regression` .

---

### 评论 #7 (作者: LB76673, 时间: 9个月前)

Hello everyone.Regarding multi_regression(y, x1, x2,..., days=0, lag=0, solver="SVD"),description says it's solver can be "SVD"(default), "QR" or "NORMAL".What exactly does the solver refer to?Under what circumstances should SVD(or other) be used?And I'm very eager to know under what circumstances multi_regression  is equivalent to ts_regression.

---

