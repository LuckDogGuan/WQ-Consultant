# How is “combined alpha performance” and “combined power pool alpha” calculated?

- **链接**: How is combined alpha performance and combined power pool alpha calculated.md
- **作者**: TN48242
- **发布时间/热度**: 7个月前, 得票: 1

## 帖子正文

I’d like to clarify how the system calculatescombined alpha performanceandcombined power pool alpha.Which alphas are included in each combined metric?Doescombined alpha performanceinclude regular alphas, power pool alphas, or some specific group?How iscombined power pool alphadefined — does it depend on activity status or other conditions?Overlap between groups:If an alpha was once apower pool alphabut later had the “power pool” tag removed, will it then be counted in the combined regular alpha metric?Is there any priority rule (for example, once an alpha is tagged as power pool, it’s only included in the combined power pool metric and never in regular)?Goal:I want to fully understand the classification logic so that when tracking combined performance, I can accurately interpret the contribution of each alpha group.Any clarification or reference to official documentation would be greatly appreciated.Thanks in advance!

---

## 讨论与评论 (2)

### 评论 #1 (作者: SK72105, 时间: 7个月前)

Combined alpha performance is the after-cost sharpe of ALL your alphas and super alphasfrom the beginningof your journey as a consultant. This includes all kind of submissions in all regions and universes that are possible or were possible - i.e powerpool, ATOMs, regular alphas, and super alphas"once apower pool alphabut later had the “power pool” tag removed, will it then be counted in the combined regular alpha metric"  -YES

---

### 评论 #2 (作者: TP18957, 时间: 5个月前)

This is a very important clarification question, because “combined alpha performance” and “combined power pool alpha” are often misunderstood and can easily be misinterpreted when tracking long-term progress on BRAIN. As correctly pointed out in the reply, combined alpha performance is effectively a lifetime, after-cost Sharpe aggregation ofallalphas you have submitted—regular alphas, Power Pool alphas, ATOMs, and SuperAlphas—across all regions and universes. It is not restricted by current activity status or by whether an alpha is still tagged as Power Pool. Once an alpha exists in your submission history, it contributes to the combined metric. Combined Power Pool alpha, on the other hand, is a subset view that focuses only on alphas that currently qualify as Power Pool under the platform’s rules. Importantly, there is no permanent exclusivity: if a Power Pool tag is removed, that alpha simply flows back into the general combined alpha performance bucket. There is no priority lock—classification is dynamic, not historical—so understanding this helps avoid incorrect attribution when analyzing performance changes over time.

---

