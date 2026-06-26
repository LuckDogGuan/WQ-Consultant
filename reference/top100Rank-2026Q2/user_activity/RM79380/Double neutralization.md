# Double neutralization

- **链接**: Double neutralization.md
- **作者**: RM79380
- **发布时间/热度**: 3个月前, 得票: 3

## 帖子正文

Sometimes an alpha may be biased by  **two factors**  like  **country**  and  **industry** . To remove both at the same time, use  **group_cartesian_product** , which creates groups of stocks with the  **same country and industry**  and neutralizes within them.

Applying group_neutralize twice in sequence eg

**group_neutralize(group_neutralize(alpha, industry), country)** cannot be deemed as double neutralization since the second neutralization cancels the first one. True double neutralization requires  **combined grouping** , not sequential neutralization.

---

## 讨论与评论 (0)

