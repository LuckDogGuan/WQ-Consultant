# osmosisPoints一键清零代码

- **链接**: [Commented] osmosisPoints一键清零代码.md
- **作者**: ZZ81910
- **发布时间/热度**: 3个月前, 得票: 63

## 帖子正文

对自己osmosisPoints不满意的小伙伴注意了，在这里我提供一份一键清零代码希望对大家有所帮助，填上账户密码，总数100以下一键清零，100以上多点几次，或者自己改代码。代码如下：

```
import requestsfrom os import environfrom time import sleepimport timeimport jsonimport pandas as pdimport randomimport picklefrom itertools import productfrom itertools import combinationsfrom collections import defaultdictimport picklefrom openpyxl import load_workbookfrom openpyxl import Workbookfrom pathlib import Pathimport openpyxldef login():    username = ""    password = ""    # Create a session to persistently store the headers    s = requests.Session()    # Save credentials into session    s.auth = (username, password)    # Send a POST request to the /authentication API    response = s.post('https://api.worldquantbrain.com/authentication')    print(response.content)    print('consultant lib')    return ss = login()alpha_ids = []try:    alphas_url = f'https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=0&status!=UNSUBMITTED%1FIS-FAIL&osmosisPoints%3E0&order=osmosisPoints&hidden=false'    alphas = s.get(alphas_url)    requests = alphas.json()['results']    for i in requests:        alpha_ids.append(i['id'])except Exception as e:    print(e)print(len(alpha_ids))try:    for alpha_id in alpha_ids:        sleep(0.5)        set_null_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"        set_null = s.patch(set_null_url, json={"osmosisPoints": None})        print(set_null.json())except Exception as e:    print(e)
```

---

## 讨论与评论 (24)

### 评论 #1 (作者: SZ83096, 时间: 3个月前)

感谢虎哥！

---

### 评论 #2 (作者: YZ51589, 时间: 3个月前)

感谢分享 帮大忙

---

### 评论 #3 (作者: ZZ13271, 时间: 3个月前)

那么请问，我alpha个数超过100，要怎么改代码呢

---

### 评论 #4 (作者: PS55811, 时间: 3个月前)

这个我记得之前已经有大佬分享过类似的代码了

---

### 评论 #5 (作者: TT21691, 时间: 3个月前)

感谢大佬分享，os rank调整起来确实麻烦，一键清空方便很多。

---

### 评论 #6 (作者: SJ65808, 时间: 3个月前)

很有用的代码，最近os表现一直很糟糕，是时候调整一波了

==================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #7 (作者: MY49971, 时间: 3个月前)

感谢分享，很有用的功能

==================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #8 (作者: YH25030, 时间: 3个月前)

多谢大佬分享代码！

==================================================================================
Life is about waiting for the right moment to act. So, RELAX. You’re not LATE. You’re not EARLY.
You are very much ON TIME, and in your, TIME ZONE Destiny set up for you.
==================================================================================

---

### 评论 #9 (作者: CZ39633, 时间: 3个月前)

大佬的分享真的太及时了！我感觉在os出来了以后很多人其实都有类似的困扰，但真正能把问题拆解清楚、再给出这么直接可用的解决方案的人并不多。看得出来您不仅技术扎实，而且非常懂大家的实际需求，连不同区间的处理方式都考虑到了，细节真的到位。对我们这些还在摸索阶段的人来说，这种“拿来就能用”的经验分享太珍贵了，能少走很多弯路。

---

### 评论 #10 (作者: WA25180, 时间: 3个月前)

学习了

---

### 评论 #11 (作者: ZY95930, 时间: 3个月前)

很好用的代码，osmosis分配点数，事半功倍。

---

### 评论 #12 (作者: AM12075, 时间: 3个月前)

下列代码开箱即用

import urllib.parse

import sys

from datetime import datetime

# 假设该库返回requests.Session对象

from machine_lib import login

def clear_osmosis_points(s, region, start_date, target_score=2000, clear_to_value=1):

"""

清除指定地区、指定日期后，osmosisPoints为指定分数的所有alpha的分数

:param s: requests.Session对象，已完成登录的会话

:param region: 地区大写：USA, EUR ... ...

:param start_date: 过滤日期，获取该日期之后的因子

:param target_score: 要清除的目标分数，默认为2000

:param clear_to_value: 清除后设置的值，默认为1（API要求最小值>=1）

:return: 清除的alpha数量

"""

alphas_data = []

# 对日期字符串进行URL编码

if start_date.tzinfo is None:

from datetime import timezone

start_date = start_date.replace(tzinfo=timezone.utc)

start_date_str = urllib.parse.quote(start_date.astimezone().isoformat(timespec='seconds'))

limit = 100

offset = 0

# 分页获取所有alpha数据

while True:

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&dateCreated%3E={start_date_str}"

f"&settings.region={region}"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&hidden=false"

f"&type!=SUPER"

f"&order=-dateSubmitted"

)

try:

print(f"正在请求第 {offset // limit + 1} 页数据... (offset={offset})")

resp = s.get(url, timeout=30)

if resp.status_code != 200:

print(f"请求出错，状态码：{resp.status_code}")

if resp.status_code == 401:

print("错误：未授权访问，请检查登录状态")

elif resp.status_code == 403:

print("错误：访问被拒绝，请检查权限")

break

data = resp.json()

results = data.get("results", [])

alphas_data.extend(results)

print(f"已获取 {len(results)} 条数据，累计 {len(alphas_data)} 条")

# 安全地获取count值，处理None情况

total_count = data.get("count")

if total_count is None:

total_count = 0

elif not isinstance(total_count, (int, float)):

try:

total_count = int(total_count)

except (ValueError, TypeError):

total_count = 0

if offset + len(results) >= total_count or len(results) < limit:

break

offset += limit

except Exception as e:

print(f"数据获取异常：{e}")

import traceback

traceback.print_exc()

break

# 筛选出osmosisPoints为目标分数的alpha

alphas_to_clear = []

osmosis_points_stats = {}  # 统计不同分数的alpha数量

for item in alphas_data:

# 安全地获取osmosisPoints值，处理None、缺失字段、非数字值等情况

raw_points = item.get('osmosisPoints')

if raw_points is None:

osmosis_points = 0

elif isinstance(raw_points, (int, float)):

osmosis_points = int(raw_points)

else:

# 如果不是数字类型，尝试转换，失败则使用0

try:

osmosis_points = int(raw_points)

except (ValueError, TypeError):

osmosis_points = 0

# 再次确保osmosis_points是整数（双重保险）

if not isinstance(osmosis_points, int):

try:

osmosis_points = int(osmosis_points)

except (ValueError, TypeError):

osmosis_points = 0

# 统计分数分布

osmosis_points_stats[osmosis_points] = osmosis_points_stats.get(osmosis_points, 0) + 1

if osmosis_points > 0:

alphas_to_clear.append({

'id': item['id'],

'osmosisPoints': osmosis_points

})

# 打印分数分布统计（用于调试）

if osmosis_points_stats:

print(f"\n获取到的alpha分数分布统计：")

# 使用更安全的排序方法：将所有键转换为可比较的值

# 先验证所有键都是数字类型

cleaned_stats = {}

for score, count in osmosis_points_stats.items():

if not isinstance(score, (int, float)):

try:

clean_score = int(score)

except (ValueError, TypeError):

clean_score = 0

cleaned_stats[clean_score] = cleaned_stats.get(clean_score, 0) + count

else:

cleaned_stats[int(score)] = count

# 现在所有键都确保是整数，可以安全排序

sorted_items = sorted(cleaned_stats.items(), reverse=True)

for score, count in sorted_items:

marker = " ← 目标" if score == target_score else ""

print(f"  {score}分: {count}个{marker}")

print(f"\n找到 {len(alphas_to_clear)} 个有分数的alpha")

# 打印前几个alpha的详细信息（用于调试）

if alphas_to_clear:

print("\n前3个待清除的alpha信息：")

for i, alpha in enumerate(alphas_to_clear[:3], 1):

print(f"  {i}. Alpha ID: {alpha['id']}, 当前分数: {alpha['osmosisPoints']}")

if not alphas_to_clear:

print("没有需要清除的alpha")

return 0

# 清除这些alpha的分数（设置为clear_to_value，因为API要求最小值>=1）

cleared_count = 0

failed_count = 0

print(f"\n开始清除分数（将设置为{clear_to_value}，API要求最小值>=1）...")

print("-" * 80)

for idx, alpha in enumerate(alphas_to_clear, 1):

try:

update_url = f" [https://api.worldquantbrain.com/alphas/{alpha['id']}](https://api.worldquantbrain.com/alphas/{alpha['id']}) "

# 设置请求头，确保Content-Type正确

headers = {

'Content-Type': 'application/json',

'Accept': 'application/json'

}

# 使用PATCH请求更新osmosisPoints字段（设置为clear_to_value，因为API不允许0）

patch_resp = s.patch(update_url, json={"osmosisPoints": clear_to_value}, headers=headers, timeout=10)

# 状态码200或204都认为成功

if patch_resp.status_code in [200, 204]:

print(f"[{idx}/{len(alphas_to_clear)}] ✓ Alpha ID：{alpha['id']} - 已发送清除请求（原分数：{alpha['osmosisPoints']}，目标：{clear_to_value}）")

cleared_count += 1

else:

# 打印详细的错误信息

error_msg = f"状态码：{patch_resp.status_code}"

try:

error_data = patch_resp.json()

error_msg += f"，错误信息：{error_data}"

except:

error_msg += f"，响应内容：{patch_resp.text[:200]}"

# 如果是405错误，提供更详细的提示

if patch_resp.status_code == 405:

error_msg += f"\n    提示：API不支持PATCH方法，可能需要使用其他端点或方法"

# 如果是400错误，提供更详细的提示

elif patch_resp.status_code == 400:

error_msg += f"\n    提示：API验证失败，请检查请求参数是否符合要求（osmosisPoints最小值>=1）"

print(f"[{idx}/{len(alphas_to_clear)}] ✗ Alpha ID：{alpha['id']} - 清除失败，{error_msg}")

failed_count += 1

except Exception as e:

print(f"[{idx}/{len(alphas_to_clear)}] ✗ Alpha ID：{alpha['id']} - 清除时出错：{e}")

import traceback

traceback.print_exc()

failed_count += 1

print("-" * 80)

print(f"\n清除完成！")

print(f"  成功清除：{cleared_count} 个alpha")

print(f"  清除失败：{failed_count} 个alpha")

return cleared_count

if __name__ == '__main__':

print("=" * 60)

print("清除osmosisPoints分数工具")

print("=" * 60)

# 配置参数

advisor_date = datetime(2025, 5, 1)  # 成为顾问的日期，用于过滤该日期之后的因子

target_region = "JPN"  # 目标地区

target_score = 5000  # 要清除的目标分数

clear_to_value = None  # 尝试用null删除分数

print(f"\n配置参数：")

print(f"  目标地区：{target_region}")

print(f"  起始日期：{advisor_date}")

print(f"  目标分数：所有有分数的alpha")

print(f"  清除后设置为：{clear_to_value}（API要求最小值>=1）")

# 初始化登录会话

print("\n[步骤 1/2] 正在登录...")

try:

session = login()  # 使用真实登录

print("✓ 登录成功")

except Exception as e:

print(f"✗ 登录失败：{e}")

print("请检查 machine_lib.login() 函数是否正确配置")

import traceback

traceback.print_exc()

sys.exit(1)

# 清除osmosisPoints为目标分数的alpha

print(f"\n[步骤 2/2] 正在清除所有有分数的alpha（将设置为{clear_to_value}）...")

cleared = clear_osmosis_points(

s=session,

region=target_region,

start_date=advisor_date,

target_score=target_score,

clear_to_value=clear_to_value

)

print("=" * 60)

print(f"程序执行完成，共清除 {cleared} 个alpha的分数")

print("=" * 60)

---

### 评论 #13 (作者: MZ45384, 时间: 3个月前)

非常有用的代码。感谢大佬的分享。但是建议最好把地区参数单独列出来，这样方便微调单个region。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #14 (作者: DQ66419, 时间: 3个月前)

感谢大佬分享代码，不用再一个一个手改了。
======日日精进，步步为营，积蓄力量，静待花开。Strive daily, advance step by step, gather strength, and wait for the flowers to bloom.======

---

### 评论 #15 (作者: ZZ81910, 时间: 3个月前)

如果是alpha总数超过100，加一个循环就可以了啊。如果是想清除某个地区的分数，在下面这个URL里加上区域就可以，具体可以F12自己试一下。

```
https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=0&status!=UNSUBMITTED%1FIS-FAIL&osmosisPoints%3E0&order=osmosisPoints&hidden=false
```

---

### 评论 #16 (作者: XW99584, 时间: 3个月前)

学习了，不过我还没有分配os分数，有分配os分数的代码吗

---

### 评论 #17 (作者: YQ51506, 时间: 3个月前)

- =============================================================================
  非常感谢大佬的分享，代码亲测很好用，希望能在搞一个老师说的四个方案的分配脚本，应该会有更有意思的表现
  =================================输入理解输出==================================

---

### 评论 #18 (作者: CW62372, 时间: 2个月前)

======================================================================================

太及时了，感谢大佬分享代码，就是不知道这时候改还来得及吗哈哈哈

======================================================================================

---

### 评论 #19 (作者: HL10684, 时间: 2个月前)

非常有用的代码，不用再手动一个个删除保存，节省了更多时间，很方便，要是能针对单独区域进行OS point清零就更好咧😁

==================================================================================

所遇皆为我师，望不吝赐教

==================================================================================

---

### 评论 #20 (作者: ST61360, 时间: 2个月前)

这代码真是起了大作用了。稍微修改一下就变成了批量等权分配osmosisPoints。让分配osmosisPoints的工作变的轻松很多。

---

### 评论 #21 (作者: ZY95930, 时间: 2个月前)

感谢分享，有了这个代码，真是方便多了。手动清理太耗时。

---

### 评论 #22 (作者: SZ50491, 时间: 2个月前)

感谢大佬，太省力了。另外，想问下，这个osmosisPoints是每周都要重新设置一下吗？还是一个季度就可以啊

---

### 评论 #23 (作者: FZ60707, 时间: 2个月前)

用了虎哥的代码，确实一键清零，省去了手动一个个改的麻烦。我也稍微改了下参数，针对不同region分批操作，亲测稳定好用。感谢大佬分享，期待更多实用脚本！

====================================================================================================================================================================

---

### 评论 #24 (作者: HW93328, 时间: 2个月前)

========================HW想评论========================

最近的osmosis的rank分数不是很理想，特意来论坛搜索相关的帖子学习，这个代码很实用，谢谢大佬分享，后面也要对osmosis对分配做进一步研究！

========================HW想评论========================

---

