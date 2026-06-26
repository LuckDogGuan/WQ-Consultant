# Why Are My Rolling Signals Zero After Successful Labeling?

- **链接**: Why Are My Rolling Signals Zero After Successful Labeling.md
- **作者**: RM79380
- **发布时间/热度**: 3个月前, 得票: 2

## 帖子正文

Hello everyone,

I am on the workflow notebooks of the Data Creation Challenge and had a problem with the rolling impact signal generation.

Once the entire pipeline (search - co-mentions - knowledge graph - workflow example - LLM labeling) has been run, my dfwithlabels appears to be fine:

~20k rows labeled
 impact = 1.0 for all rows
 isthemerelated = True
 Dates span 2021-01-01 to 2021-06-30
~1000 unique entities

But in constructing the rolling signal with:

dfrollingsignal = build rolling impact signal ().
    dfwithlabels,
    entitycol="entityname",
    datecol="date",
    impactcol="impact",
    isthemerelatedcol="isthemerelated",
    window7d=7,
    window30d=30,
    rollingagg="sum",
)

I consistently get:

Non-zero 7d: 0
Non-zero 30d: 0

It can be seen that the resulting table has such columns as dailyscore, npositive, nnegative, volume, signal7d, and signal30d, yet all signals are zero.

Did anybody have such an experience when the labeling step was successful but the rolling signals were zero?
Is this because of the interpretation of the impact values within itself or the entity/date aggregation?

The advice would be highly valued.

Thank you!

---

## 讨论与评论 (0)

