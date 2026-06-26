# Multiple Entries for the Same Year in  Backtest Results

- **链接**: [Commented] Multiple Entries for the Same Year in  Backtest Results.md
- **作者**: NA11329
- **发布时间/热度**: 7个月前, 得票: 43

## 帖子正文

When applying a 1 year test period, the platform produces two distinct performance entries for the year 2022, despite the expectation that each calendar year would yield a single result. Similarly, when a 5-year test period is used, the year 2018 appears twice, with one instance displaying a pronounced decline in performance. I would appreciate clarification on how the platform defines and assigns test windows to specific years, why multiple entries correspond to the same calendar year, and what accounts for the substantial discrepancies in performance between entries within the same year.

![图片](images/img_beac80128a.png)

From the image above under a 1 year test period, notice how 2022 appears twice, with one instance exhibiting a substantial performance deviation.

---

## 讨论与评论 (11)

### 评论 #1 (作者: JN65269, 时间: 7个月前)

1. **Why you see the same year twice**

The platform doesn’t test exactly by calendar year (Jan–Dec).
Instead, it tests using  **rolling windows** .

Example for a 1-year test:

- Test 1: Jan 2021 → Dec 2021
- Test 2: Feb 2021 → Jan 2022

Both tests touch 2022, so when results are grouped by year, 2022 shows up  **twice** .

1. **How the platform decides the year**

It usually assigns a test window to the year where the window  **ends** .

So:

- Jan 2021 → Dec 2021 → counted as 2021
- Feb 2021 → Jan 2022 → counted as 2022

This is why overlapping windows can appear in the same calendar year.

1. **Why the results are different**

Each window covers different days.
If one window includes a bad period in the market, its performance drops.
Example:

- Window A: mostly good months → high performance
- Window B: includes crash months → big drop

So even for the same year, numbers can be very different.

Hope this could  be of some help.

---

### 评论 #2 (作者: ME83843, 时间: 7个月前)

what research! This is so amazing and such an observation is commendable

A good observation quant

---

### 评论 #3 (作者: TP85668, 时间: 7个月前)

The platform uses  **rolling test windows** , not fixed calendar-year periods. This means multiple 12-month windows can all end in the same calendar year—for example, Feb-2021→Feb-2022 and Apr-2021→Apr-2022—so both are labeled “2022.” Because each window captures different market conditions, their performances can differ sharply. The same applies to the 5-year period: several 60-month windows end in 2018, so that year appears more than once.

---

### 评论 #4 (作者: AG14039, 时间: 6个月前)

The platform relies on rolling test windows rather than fixed calendar-year periods, so multiple 12-month windows can end in the same year—such as Feb-2021→Feb-2022 and Apr-2021→Apr-2022—and both get labeled as “2022,” even though they cover different market conditions and may produce very different results. The same logic applies to the 5-year tests, where several 60-month windows can all end in 2018, causing that year to appear multiple times.

---

### 评论 #5 (作者: MO25461, 时间: 6个月前)

Great question—this is exactly the kind of thinking that shows you’re digging beneath surface-level results.

The behavior comes from the platform using  **rolling test windows rather than calendar years** . A single year can appear multiple times because it belongs to different start-date windows, and performance differs due to  **path dependence and regime effects** , not a reporting error.

---

### 评论 #6 (作者: FO15582, 时间: 6个月前)

This shows that you have been keen on observing multiple entries for the same year. This is a great insight for all of us. Cheers.

---

### 评论 #7 (作者: PA75047, 时间: 6个月前)

The platform shows more than one entry for the same year because each result does not represent a calendar year on its own. Instead, every entry comes from a moving test window. For example, a one year test window is not tied to January to December of a single year. It can start in the middle of one year and end in the middle of the next year. So a window that ends in 2022 and another window that also ends in 2022 will both appear under that year even though they cover different dates. The same thing happens with longer windows like five years. One five year window may start earlier than another, so the performance inside those windows will not match. This is why the same year may appear twice and why the numbers look very different. The system is showing every rolling window that ends in that year, not one fixed result per year.

---

### 评论 #8 (作者: AG14039, 时间: 6个月前)

The platform displays multiple entries for the same year because each result corresponds to a rolling test window rather than a fixed calendar year. A one-year window, for example, isn’t bound to January–December; it may start mid-year and end mid-year, so different windows that both end in 2022 can appear under the same year even though they cover different date ranges. The same logic applies to longer horizons like five-year windows, where differing start points lead to different performance outcomes. As a result, the same year can appear multiple times with varying numbers, since the system reports every rolling window that ends in that year rather than a single annual summary.

---

### 评论 #9 (作者: NN89351, 时间: 6个月前)

The platform uses rolling windows, not fixed years, so multiple 12-month periods can end in the same year (e.g., Feb-21→Feb-22 and Apr-21→Apr-22 both labeled “2022”). Each window covers different conditions, so results vary. Same for 5-year windows—several end in 2018, so that year repeats.

---

### 评论 #10 (作者: NS62681, 时间: 5个月前)

The platform shows multiple entries for the same year because results are based on rolling windows, not fixed calendar periods. A one-year test window can start and end at different points in time, so several windows may all finish in the same year while covering different date ranges. The same applies to longer horizons, like five-year windows. As a result, a single year can appear multiple times with different values, since each entry represents a distinct rolling window ending in that year rather than one annual summary.

---

### 评论 #11 (作者: HT71201, 时间: 5个月前)

Years appear multiple times because results come from rolling windows, not calendar years. Each window may end in the same year but cover different periods, producing different values.

---

