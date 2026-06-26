# [代码优化]只有IS两年数据（或少于）剔除办法代码优化

- **链接**: [Commented] [代码优化]只有IS两年数据或少于剔除办法代码优化.md
- **作者**: TL32287
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

原代码链接，优化剔除厂Alpha因子系列： [../JR23144/Alpha PNL 合法性检测【自动剔除 厂 Alpha等无效Alpha实现高效率剪枝】代码优化.md](../JR23144/Alpha PNL 合法性检测【自动剔除 厂 Alpha等无效Alpha实现高效率剪枝】代码优化.md)

我发现对于厂可以进行筛除，但是对在近年仅有一两年年的数据无法做到有效的剔除。

对此，请看参考图：

![图片](images/img_bc81fe5c80.png)

可以看到，仅有几年的数据，在这之前，我因为交了很多这样的因子导致我的VF有所降低，此篇帖子也是告诫自己。

对于优化，采用获取到的数据以此修改：

代码：

import os

import logging

import time

import requests

import datetime  # 新增导入

from machine_lib import *

s = login()

def wait_get(url: str, max_retries: int = 10) -> "Response":

retries = 0

while retries < max_retries:

while True:

simulation_progress = sess.get(url)

if simulation_progress.headers.get("Retry-After", 0) == 0:

break

time.sleep(float(simulation_progress.headers["Retry-After"]))

if simulation_progress.status_code < 400:

break

else:

time.sleep(2 ** retries)

retries += 1

return simulation_progress

def check_consecutive_non_zero_values(alpha_id, data, required_streak=200):

if not data or len(data) < required_streak:

return True

def check_column(column_data):

if len(column_data) < required_streak:

return True

current_streak_count = 0

current_streak_value = None

for value in column_data:

if value != 0:

if value == current_streak_value:

current_streak_count += 1

else:

current_streak_value = value

current_streak_count = 1

else:

current_streak_value = None

current_streak_count = 0

if current_streak_count >= required_streak:

return False

return True

column1_values = []

column2_values = []

for row in data:

if len(row) >= 3:

column1_values.append(row[1])

column2_values.append(row[2])

else:

pass

if column1_values and column2_values:

is_col1_all_zeros = all(v == 0 for v in column1_values)

is_col2_all_zeros = all(v == 0 for v in column2_values)

if is_col1_all_zeros or is_col2_all_zeros:

print(alpha_id, "不合法")

return False

if not check_column(column1_values):

print(alpha_id, "不合法")

return False

if not check_column(column2_values):

print(alpha_id, "不合法")

return False

print(alpha_id, "通过")

return True

import datetime

def get_alpha_pnl_legal(alpha_id: str) -> bool:

pnl = wait_get(" [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id + "/recordsets/pnl").json()

records = pnl["records"]

# 1. 检查时间跨度是否≥8年

if not records:

return False

date_list = []

for record in records:

try:

date_obj = datetime.datetime.strptime(record[0], '%Y-%m-%d').date()

date_list.append(date_obj)

except Exception:

return False  # 日期格式错误

min_date = min(date_list)

max_date = max(date_list)

total_days = (max_date - min_date).days

if total_days < 2920:  # 2920天 ≈ 8年

return False

# 2. 检查是否连续多年零值（重点关注前两列PNL）

zero_streak_threshold = 5 * 252  # 假设每年252个交易日

col1_zeros = [record[1] == 0 for record in records]  # Combo PnL列或RA PNL列

#SA需要取消下面的注释

#col2_zeros = [record[2] == 0 for record in records]  # Equal Weight PnL列

# 检测连续零值的最大长度

def max_consecutive_zeros(arr):

max_streak = current_streak = 0

for val in arr:

current_streak = current_streak + 1 if val else 0

max_streak = max(max_streak, current_streak)

return max_streak

col1_max_zero_streak = max_consecutive_zeros(col1_zeros)

#sa需要取消下面的注释

# col2_max_zero_streak = max_consecutive_zeros(col2_zeros)

# 若任一列存在连续≥8年的零值，判定为不合格

# if col1_max_zero_streak >= zero_streak_threshold or col2_max_zero_streak >= zero_streak_threshold:

#     print(f"{alpha_id} 不合法：存在连续{zero_streak_threshold//252}年零值")

#     return False

#SA取消上面的注释，注释下面的代码

if col1_max_zero_streak >= zero_streak_threshold  >= zero_streak_threshold:

print(f"{alpha_id} 不合法：存在连续{zero_streak_threshold//252}年零值")

return False

# 3. 保留原有连续非零值检查

return check_consecutive_non_zero_values(alpha_id, records)

def get_alpha_pnl_legal_list(fo_tracker: list) -> list:

global sess

sess = s

fo_tracker = [fo for fo in fo_tracker if get_alpha_pnl_legal(fo[0])]

return fo_tracker

sess = s

第二步不变，跟原博主一样的方法。

**2.  在notebook中** 修改其中筛选第一次回测完的Alpha

```
fo_tracker = get_alphas("06-12", "06-13", 1, 0.7, "ASI", 200, "track")# 添加以下几行import pnl_testf_num = len(fo_tracker)print(f_num,"个alpha 进行pnl合法检测，请耐心等待")fo_tracker = pnl_test.get_alpha_pnl_legal_list(fo_tracker)print(f_num -len(fo_tracker),"个不合法的pnl,已被剔除" )
```

---

## 讨论与评论 (6)

### 评论 #1 (作者: SZ83096, 时间: 1年前)

============================================================

大佬，你终于把这个过滤的代码发贴了，我等了好久，差点以为无了。

感谢分享～～～

============================================================

---

### 评论 #2 (作者: BW14163, 时间: 11个月前)

蹲蹲总会有的，又蹲到一个功能性代码。感觉很赞，谢谢大佬分享代码

---

### 评论 #3 (作者: YW10763, 时间: 10个月前)

```
不合法的pnl,已被剔除
```

**这是怎么理解 是在回测已经删除了还是在当前的代码段输出中删除了？求解
===========================================================================================================================================================================================================**

---

### 评论 #4 (作者: KQ43044, 时间: 10个月前)

get_alphas  方法没有定义  我这边没有运行起来 @ [TL32287](/hc/zh-cn/profiles/29823108986647-TL32287) 大佬你可以教我一下运行起来吗

---

### 评论 #5 (作者: AM12075, 时间: 9个月前)

请问运行结果是下面这样应该怎么解决
list indices must be integers or slices, not str

=================================================================================

---

### 评论 #6 (作者: DZ31817, 时间: 9个月前)

感谢分享，我筛除这种alpha的方法跟你类似，判断pnl中是否有连续长度为x的0值出现，若有则剔除该alpha。而且现在wq的检测也变严了，有时候是连续有250个0值就不能提交，有时候甚至有2、30个连续0值就不能提交了，因此我也一般将剔除的阈值设置为2、30个。另外我剔除厂的方法也与此差不多，检测pnl的尾部是否存在连续x个0值。

---

