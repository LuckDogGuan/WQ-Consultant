# Using ts_rank and multiply operator

- **链接**: [Commented] Using ts_rank and multiply operator.md
- **作者**: TW26190
- **发布时间/热度**: 3个月前, 得票: 8

## 帖子正文

**ts_rank**  operator measures how the current value of a variable compares to its past values over a lookback period of d days. It assigns a normalized rank between 0 and 1 where higher values indicate relatively higher positions in the historical window. It is time-series based not across different assets.

**syntax** ts_rank(x, d) x is the datafield while d is the lookback days

Multiply Operator computes the element-wise product of two or more inputs. It works with both scalars and time series data, combining them multiplicatively. By default, if any input is NaN, the result will also be NaN.

When filter = true, NaN values are treated as 1 so they do not affect the result.

Syntax multiply(x,y ...filter=false)

---

## 讨论与评论 (1)

### 评论 #1 (作者: RM79380, 时间: 2个月前)

Well put👍

---

