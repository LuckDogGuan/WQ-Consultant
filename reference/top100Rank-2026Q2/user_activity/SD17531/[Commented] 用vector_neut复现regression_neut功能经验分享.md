# 用vector_neut复现regression_neut功能经验分享

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwiXGtd%2Bmhs6D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAZNodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzAzNTAzNjY5Mzk3OTktJUU3JTk0JUE4dmVjdG9yLW5ldXQlRTUlQTQlOEQlRTclOEUlQjByZWdyZXNzaW9uLW5ldXQlRTUlOEElOUYlRTglODMlQkQGOwhUOg5zZWFyY2hfaWRJIik0YmY0OGY0MC01MzIwLTRiYzktYjNiNi1lNzRlNzc4OTI3YzIGOwhGOglyYW5raQ86C2xvY2FsZUkiCnpoLWNuBjsIVDoKcXVlcnlJIgxTRDE3NTMxBjsIVDoScmVzdWx0c19jb3VudGkb--79916dfb8a387d0b28b9c690637805508076e9f0
- **作者**: LL87164
- **发布时间/热度**: 1年前, 得票: 19

## 帖子正文

目的在没有 regression_neut(Y, X) 使用权限的情况下如何利用可用操作符实现同样的功能方法vector_neut(Y, X) 和 regression_neut(Y, X) 在中心化数据的情况下是等价的，但在未中心化的数据上会因为截距 a 的存在而产生差异。要完全复现 regression_neut(Y, X) 的功能，要确保数据中心化，或者手动计算截距 a 和斜率 b，然后构造输出。不同点及数学等价性分析计算方式：regression_neut(Y, X)：使用最小二乘回归（Ordinary Least Squares, OLS）来拟合 Y = a + b * X。这里的 a 和 b 是通过最小化残差平方和得到的拟合值是 a + b * X，残差是 Y - (a + b * X)。vector_neut(x, y)：使用向量投影来计算 x 在 y 上的线性分量。投影公式为 proj_y(x) = (x · y / y · y) * y。输出 x* = x - proj_y(x)。截距的处理：regression_neut 显式地计算了截距 a，并在拟合值中使用它：a + b * X。vector_neut 的投影方法隐含地假设数据已经被中心化（即均值为 0）。如果 x 和 y 没有中心化，vector_neut 的投影不会包含截距项，相当于强制通过原点的回归（即 a = 0 的情况）。数学等价性：如果 X 和 Y 已经被中心化（即 Mean(X) = 0, Mean(Y) = 0），那么 vector_neut(Y, X) 和 regression_neut(Y, X) 的结果是等价的。因为在中心化后，回归的截距 a 会变成 0，此时回归方程简化为 Y = b * X，而 vector_neut 的投影也等价于这种无截距的回归。如果 X 和 Y 没有中心化，regression_neut 会计算非零的 a，而 vector_neut 不会考虑截距，导致两者结果不同。最终方案综合分析，中心化后使用 vector_neut是可行的方案，因为：vector_neut 已经非常接近 regression_neut 的功能，唯一的差异是截距 a 的处理。通过中心化 X 和 Y，我们可以消除截距的影响，使 vector_neut 的结果等价于 regression_neut。最终表达式vector_neut(normalize(Y, useStd = false, limit = 0.0), normalize(X, useStd = false, limit = 0.0))看到有不少刚刚成为顾问但还没有regression_neut权限的新人都在问，所以发一下，希望有所帮助。

---

## 讨论与评论 (9)

### 评论 #1 (作者: GL61467, 时间: 1年前)

知识储备丰富

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

膜拜大佬  但是这两个操作符  我都没有啊

---

### 评论 #3 (作者: LL87164, 时间: 1年前)

SD17531regression_neut是做横截面维度上的一元线性回归。理论上可以尝试用公式替代。但是个人不建议这么做，除了复杂增加工作量以外，如果只是想套一个模版获得可提交alpha，结果可能不能令人满意。还是把时间精力花在对数据及其特征的理解上，以及为什么要用regression_neut，目的是什么。从这个角度上看看有什么新的思路，或者考虑换其他的模版，这样可能比较划算。我也是在学习摸索阶段，一点初浅体会，个人意见，仅供参考。

---

### 评论 #4 (作者: JL16510, 时间: 1年前)

感谢分享，很多不常见的操作符的理论部都不清楚，期待能有更多关于相关分享。

---

### 评论 #5 (作者: LL87164, 时间: 1年前)

JL16510“The math in real, academic, finance is not actually that hard. Understanding how to use the equations, and see what they really mean about the world···that’s hard.” - John Cochrane多谢鼓励！

---

### 评论 #6 (作者: YW93864, 时间: 1年前)

SD17531LL87164我赞同LL87164的想法，与其复现regression_neut，理解表达式或者模板是更重要的。这里借楼说个题外话，如果想使用regression_neut而没有这个运算符的情况下，可以考虑使用减号或者除号，前者是系数为1的回归取残差，后者是对x和y同时取log再做系数为1的回归取残差。可以先考虑使用这两个简单运算符做代替。另外，楼主提供的对于vector_neut的解读给了我很多insights，这是之前没有考虑到的。Great and thanks!

---

### 评论 #7 (作者: CC21336, 时间: 1年前)

我刚成为顾问，这两个我都没有

---

### 评论 #8 (作者: LL87164, 时间: 1年前)

CC21336理解。看来平台是随机分配不同操作符。那看看有没有group_regression_neut，如果有，这个应该比regression_neut功能又多了一层，从字面上看还可以做分组内的横截面回归。总之，理解自己可用的操作符然后去找相应的模版比较好。

---

### 评论 #9 (作者: LL87164, 时间: 1年前)

今天发现一个更有趣的问题：如果之前已经做了group_neutralize，二者是否可以直接替换？这个问题想明白，基本上就算是吃透了。

---

