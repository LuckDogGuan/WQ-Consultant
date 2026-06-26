# How Do You Pass the ASI “JPN Sharpe ≥ 1” Test?

- **链接**: [Commented] How Do You Pass the ASI JPN Sharpe  1 Test.md
- **作者**: JC84638
- **发布时间/热度**: 5个月前, 得票: 5

## 帖子正文

I have a slightly painful question:

**How are people getting JPN Sharpe ≥ 1 inside ASI?? 😭**

**Is there a  *systematic*  way you guys handle JPN inside ASI?**

My JPN leg is almost dead... (jzc

---

## 讨论与评论 (4)

### 评论 #1 (作者: MY82844, 时间: 5个月前)

Is that a reasonable approach to develop good alphas in JPN region, then generalize that into the bigger ASI region which includes JPN?

---

### 评论 #2 (作者: JN96079, 时间: 5个月前)

You can try using operators that help in managing general sharpness, for example, you can use ts_backfill with a low lookback, such as between 5 and 30. Otherwise, you can use low decay, around 4 and 8, which works for me.

Other methods for using operators would be using group operators, moreso group_neutralize. But others also work well as well, just try them out.

---

### 评论 #3 (作者: DG92378, 时间: 5个月前)

Try doing a lot of diversification in the datafields you use.

---

### 评论 #4 (作者: CC52804, 时间: 3个月前)

An incredible question,

This is exactly the kind of thinking that separates signal engineering from simple factor replication.

Most people just combine signals mechanically, but Jerry is clearly thinking about information transformation and alpha architecture.

Really impressive perspective. (nok

---

