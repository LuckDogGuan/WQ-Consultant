# Counting Operators and Fields per Alpha in WorldQuant Brain

- **链接**: [Commented] Counting Operators and Fields per Alpha in WorldQuant Brain.md
- **作者**: BK35905
- **发布时间/热度**: 10个月前, 得票: 11

## 帖子正文

Are the arithmetic symbols   ***+  -  /  ^  =*** counted in operators per alpha? And what about  ***reverse, power, add, subtract***  etc are included in operator count, and what are the differences?

And are  categorical inputs like  ***subindustry, industry, sector,  market, and exchange*** counted in fields per alpha?

***Example 1:***

- rank(df)^3 + group_rank(df, subindustry)

***Example 2:***

- power(rank(df), 3) + group_rank(df, subsubindustry

In both examples, how many operators per alpha and fields per alpha are there?

---

## 讨论与评论 (8)

### 评论 #1 (作者: PN39025, 时间: 10个月前)

Hi, according to my experience, it is quite accurate that the first one has 3 operators and the second one has 4 operators. Please improve alpha to be more compact and have fewer operators.

---

### 评论 #2 (作者: SK72105, 时间: 10个月前)

[https://platform.worldquantbrain.com/learn/operators](https://platform.worldquantbrain.com/learn/operators)

all operators mentioned in this (except the ones exclusively for super alphas) are counted in ops/alpha; and yes the grouping fields are calculated in data field(s) per alpha

example 1 has 4 operators and 2 data fields;

example 2 has 4 operators and 2 data fields

---

### 评论 #3 (作者: TD40899, 时间: 10个月前)

As i know, inputs like  ***subindustry, industry, sector,  market, and exchange not counted for fields per alphas. you can use http get with alpha id to get more information of each alpha (include operator per alpha)***

---

### 评论 #4 (作者: AN13265, 时间: 10个月前)

Both has 3 operators

---

### 评论 #5 (作者: TP85668, 时间: 10个月前)

Yes, in WorldQuant BRAIN, arithmetic symbols like  `+ - / ^`  are  **counted as operators** . The function forms ( `power` ,  `add` ,  `reverse` , etc.) are also operators — just written explicitly. Categorical inputs such as  `industry` ,  `sector` ,  `market` ,  `exchange`  are  **counted as fields** .

- **Example 1:**   `rank(df)^3 + group_rank(df, subindustry)`
  Operators = 3 ( `rank` ,  `^` ,  `+` , plus  `group_rank` ) → total  **4 operators**
  Fields = 2 ( `df` ,  `subindustry` )
- **Example 2:**   `power(rank(df), 3) + group_rank(df, subsubindustry)`
  Operators = 3 ( `power` ,  `rank` ,  `+` , plus  `group_rank` ) → total  **4 operators**
  Fields = 2 ( `df` ,  `subsubindustry` )

---

### 评论 #6 (作者: LD50548, 时间: 10个月前)

used to overlook the grouping fields count—good reminder to always check both ops and fields when refining an Alpha

---

### 评论 #7 (作者: YM61462, 时间: 10个月前)

**Yes,**  arithmetic symbols such as  `+` ,  `-` ,  `/` ,  `^` , and  `=`   **are counted in the**   **operator count per alpha** . Similarly,  **named functions**  like  `reverse` ,  `power` ,  `add` ,  `subtract` , etc.,  **are also counted as operators** . 
However, grouping fields such as  `subindustry` ,  `industry` ,  `sector` ,  `market` , and  `exchange`  are  **not counted in the field count per alpha** .

---

### 评论 #8 (作者: AS13853, 时间: 10个月前)

thanks for such valuable comments

try to  keeping operator counts low and fields compact helps improve alpha efficiency

---

