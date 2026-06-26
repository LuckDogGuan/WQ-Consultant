# 【prodcorr 精确分析】冲击10月积分活动

- **链接**: [Commented] 【prodcorr 精确分析】冲击10月积分活动.md
- **作者**: SJ65808
- **发布时间/热度**: 8个月前, 得票: 9

## 帖子正文

马上10月份了，平台上线了prod积分活动，本人基于wqb库总结了相关代码获取已经提交alpha的平均prodcorr值，帮助大家更好的冲击积分，代码如下

import wqb

from datetime import datetime

from wqb import FilterRange

from collections import defaultdict

def get_prodcorrelation(start_date, end_date):

logger = wqb.wqb_logger()

wqbs = wqb.WQBSession((@qq.com', 'xxx'), logger=logger)

# 日期格式转换为目标ISO格式

start_iso = f"{start_date}T04:00:00+00:00"

end_iso = f"{end_date}T04:00:00+00:00"

# 筛选数据

resps = wqbs.filter_alphas(

status='!=UNSUBMITTED',

type='REGULAR',

date_submitted=FilterRange.from_str(f"[{start_iso}, {end_iso})"),

order='dateCreated',

)

# 提取ID

alpha_ids = []

for resp in resps:

alpha_ids.extend(item['id'] for item in resp.json()['results'])

# 获取region prodcorr

results = []

for alpha_id in alpha_ids:

js = wqbs.locate_alpha(alpha_id).json()

results.append((js['settings']['region'], js['is']['prodCorrelation']))

return results

results = get_prodcorrelation(

"2025-08-01",

"2025-08-30"

)

# 统计各地区的 prodcorr 总和与alpha个数

region_stats = defaultdict(lambda: {"sum_prod": 0.0, "count": 0})

total_sum = 0.0

total_count = len(results)

for region, prod in results:

region_stats[region]["sum_prod"] += prod

region_stats[region]["count"] += 1

total_sum += prod

# 打印结果

print("=" * 60)

print("各地区结果")

for region, stats in region_stats.items():

avg_prod = stats["sum_prod"] / stats["count"]

print(f"  {region:15} | 平均值：{avg_prod:.4f} | alpha总数：{stats['count']}")

print("\n" + "-" * 60)

print("总结果")

if total_count > 0:

total_avg = total_sum / total_count

print(f"  总平均值：{total_avg:.4f} | alpha总数：{total_count}")

print("=" * 60)

最终结果如下：

![图片](images/img_4353f88587.png)

---

## 讨论与评论 (3)

### 评论 #1 (作者: YH25030, 时间: 8个月前)

你的代码分享太及时了。我刚才看了自己提交的因子，很多都是ppa，prod corr太高了。10月以后，要努力降低pc才行。

---

### 评论 #2 (作者: XD81759, 时间: 8个月前)

您好，我不太会python，出现了以下报错，想问下是什么原因？如何修正？另外，想知道您这段代码里粘贴到vscode里后，还有哪些部分需要修改，才能直接运行？

Cell In[6],   line 8
    wqbs = wqb.WQBSession((@qq.com', 'xxx'), logger=logger)
                                         ^
SyntaxError: unterminated string literal (detected at line 8)

---

### 评论 #3 (作者: FF56620, 时间: 7个月前)

============================================================
各地区结果

------------------------------------------------------------
总结果
============================================================

时间改了，还有哪里有问题呢，很奇怪

---

