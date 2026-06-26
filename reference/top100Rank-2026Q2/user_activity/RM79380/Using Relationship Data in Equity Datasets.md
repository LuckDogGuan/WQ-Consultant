# Using Relationship Data in Equity Datasets

- **链接**: Using Relationship Data in Equity Datasets.md
- **作者**: RM79380
- **发布时间/热度**: 3个月前, 得票: 2

## 帖子正文

Relationship data captures connections between companies and can be used in alphas depending on the datafield format.

**1. Group Form** 
Group relationship fields classify stocks into connected groups (e.g., sectors or related entities). These can be used with custom neutralization:
 `group_neutralize(alpha, group)`

Since many grouping fields are sparse, it is recommended to apply  **`densify()`**  to avoid errors:
 `group_neutralize(alpha, densify(group))`

Using this approach allows relationship data to capture competitive structure and improve alpha signals.

---

## 讨论与评论 (0)

