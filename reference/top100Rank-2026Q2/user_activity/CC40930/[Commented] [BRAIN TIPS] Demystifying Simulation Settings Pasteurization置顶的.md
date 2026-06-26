# [BRAIN TIPS] Demystifying Simulation Settings: Pasteurization置顶的

- **链接**: [Commented] [BRAIN TIPS] Demystifying Simulation Settings Pasteurization置顶的.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 44

## 帖子正文

**What does Pasteurization do?**

The Pasteurization setting goes hand in hand with the Universe setting.

- It turns Alpha values of instruments not in the selected Universe to "NaN" (undefined data).
- "NaN" means “Not a Number”. That is, the instrument with value = NAN won't take part in Alpha expression computations.
- It is thus different from the situation where an Alpha value = 0 for an instrument, because this Alpha value can change to a non-zero value after operations like decay and neutralization, potentially resulting in weights allocated to that instrument.

**However, what happens when Pasteurization is "Off"?**

- All instruments, even those outside of the selected Universe, will be part of Alpha computation. This could affect group operations.
- The default setting for Pasteurization is "On".

There are times when you might want to turn Pasteurization "Off". For instance, if you want to compare instruments within your selected Universe against all instruments in the market, you can set Pasteurization = “Off” in the settings use the pasteurize() operator in your Alpha expression. Check the Learn article:  ["How to choose the Simulation Settings"](https://platform.worldquantbrain.com/learn/documentation/create-alphas/simulation-settings)  for an example.

But remember, the Pasteurization setting and the pasteurize() operator aren't the same. The operator also turns infinite (INF) input values to NaN, helpful to avoid allocating too much weight to an instrument.

---

## 讨论与评论 (11)

### 评论 #1 (作者: AT42510, 时间: 1年前)

Why might we want to set Pasteurization to "Off" during analysis?

---

### 评论 #2 (作者: AG20578, 时间: 1年前)

Hi AT42510!

Good question!

For example you work on small universe (like top200) but want to get information about instruments outside simulation universe.

---

### 评论 #3 (作者: TT55495, 时间: 1年前)

Hello, I want to ask if setting Pasteurization and operator Pasteurization have the same function, right? If so, what is the difference when using? operator Pasteurization will help a part of alpha get information about instruments outside simulation universe, right? Looking forward to your reply.

---

### 评论 #4 (作者: LH38752, 时间: 1年前)

This is exactly what I needed to hear. Thank you so much for breaking it down! 👍

---

### 评论 #5 (作者: AC63290, 时间: 1年前)

Pasteurization is a simulation setting that determines how instruments outside the selected Universe are handled. When Pasteurization is  **"On"**  (default), Alpha values for such instruments are set to "NaN," excluding them from computations and weight allocation. This ensures that only relevant instruments within the Universe are considered.

When Pasteurization is  **"Off,"**  all instruments, even those outside the Universe, are included, which can influence group operations. This may be useful for comparing instruments across the entire market.

The  `pasteurize()`  operator complements this setting by not only handling out-of-Universe instruments but also converting infinite (INF) values to NaN, ensuring stable and meaningful Alpha computations.

---

### 评论 #6 (作者: HV77283, 时间: 1年前)

Hi, I’d like to confirm if setting Pasteurization and operator Pasteurization serve the same purpose. If so, what’s the difference in their usage? Does operator Pasteurization allow part of the alpha to access information about instruments outside the simulation universe? Looking forward to your reply!

---

### 评论 #7 (作者: LK29993, 时间: 1年前)

**Comparing the Pasteurization setting against the pasteurize() operator:**

1) In addition to instruments not in the selected Universe, the pasteurize() operator also  **sets infinite (INF) input values to NaN** . For example, if your alpha value returns 1/0 for a particular instrument, it becomes an infinite value that can result in very high weightage to that instrument. To avoid concentrating too much weight on that instrument, we can use the pasteurize() operator to convert the alpha value to NaN.

2) The pasteurize() operator also allows you to decide **when and where to apply pasteurization** . For example, we can set Universe = TOP500, Pasteurization = ‘Off’, and this is our Alpha expression:

```
group_rank(pasteurize(sales_growth),sector) - group_rank(sales_growth,sector)
```

The pasteurize operator in the first group_rank pasteurizes input to the Alpha universe (TOP500), while the second group_rank ranks sales_growth among all instruments, even those outside the TOP500 universe.

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

Pasteurization is a critical setting that ensures Alpha computations exclude instruments outside the selected Universe by converting their values to NaN. This helps maintain focus on relevant instruments. If Pasteurization is turned off, all instruments, even those outside the Universe, influence the computation, which can impact group operations. Using the  `pasteurize()`  operator alongside this setting helps manage issues like infinite values in data, ensuring a balanced approach to weight allocation.

---

### 评论 #9 (作者: DK30003, 时间: 1年前)

Hi, I’d like to confirm if setting Pasteurization and operator Pasteurization serve the same purpose. If so, what’s the difference in their usage? Does operator Pasteurization allow part of the alpha to access information about instruments outside the simulation universe? Looking forward to your reply.

---

### 评论 #10 (作者: AK52014, 时间: 1年前)

Pasteurization determines how out-of-Universe instruments are treated in simulations. With Pasteurization "On," Alpha values for such instruments are set to "NaN," focusing only on relevant Universe instruments. When "Off," all instruments are included, enabling broader comparisons. The pasteurize() operator also converts infinite values to NaN, ensuring stable computations.

---

### 评论 #11 (作者: DS74354, 时间: 1年前)

This is a clear and well-structured explanation of Pasteurization and its implications! I appreciate the distinction you've made between the setting and the  `pasteurize()`  operator, as that can often be confusing for beginners. A small suggestion could be to elaborate a bit more on specific scenarios where turning Pasteurization "Off" might be beneficial beyond the example provided, such as in cases involving cross-universe Alpha comparisons. Additionally, a quick summary of how INF values are handled with the  `pasteurize()`  operator could reinforce its practical utility for users exploring advanced Alpha tuning. Great post overall!

---

