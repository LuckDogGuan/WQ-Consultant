# [必要检查：OS比赛分数统计]OS比赛分数统计

- **链接**: [Commented] [必要检查OS比赛分数统计]OS比赛分数统计.md
- **作者**: JX39934
- **发布时间/热度**: 4个月前, 得票: 66

## 帖子正文

想必经历过之前OS比赛的家人，应该都有过分数没有打整10W分，导致比赛分数失效的悔恨经历，不用怕，我这代码来了

自动获取成为顾问的日期拉取对应地区已提交alpha的分数，最后汇总

![图片](images/img_657f47329f.png)

个人觉得是很有用的小工具，请路过的哥们帮我点点赞，评论下，谢谢大家，祝国区所有顾问都VF1.0，每季度都GM，代码请看下面,同目录需要有user_info.txt

import asyncio

import logging

import re

import wqb

from typing import List, Dict, Any

# --- 配置日志 ---

logging.basicConfig(

level=logging.INFO,

format='%(asctime)s - %(levelname)s - %(message)s'

)

logger = logging.getLogger(__name__)

# --- 辅助函数 ---

def load_credentials(filename="user_info.txt"):

"""从文件中读取账号密码 (复用原脚本逻辑)"""

try:

with open(filename, 'r', encoding='utf-8') as f:

content = f.read()

user_match = re.search(r"username:\s*'(.+?)'", content)

pass_match = re.search(r"password:\s*'(.+?)'", content)

if user_match and pass_match:

return user_match.group(1), pass_match.group(1)

return None, None

except Exception as e:

logger.error(f"读取凭证失败: {e}")

return None, None

def get_advisor_start_date(session):

"""

从 base-payment 接口获取顾问起始日期 (total -> start)

"""

url = " [https://api.worldquantbrain.com/users/self/activities/base-payment](https://api.worldquantbrain.com/users/self/activities/base-payment) "

try:

resp = session.get(url, timeout=30)

if resp.status_code != 200:

logger.warning(f"获取顾问日期失败，状态码: {resp.status_code}")

return None

data = resp.json()

start_date_str = data.get("total", {}).get("start")

if start_date_str:

# 转换为 API 需要的格式 (YYYY-MM-DD -> YYYY-MM-DDT00:00:00Z)

# 添加 Z 表示 UTC 时区

return f"{start_date_str}T00:00:00Z"

else:

logger.warning("未在响应中找到 total.start 日期")

return None

except Exception as e:

logger.error(f"获取顾问日期异常: {e}")

return None

async def fetch_competition_alphas(session: wqb.WQBSession, region: str, start_date: str = None) -> List[Dict]:

"""拉取指定区域的 OC2025 竞赛 Alpha"""

all_alphas = []

offset = 0

limit = 100  # 为了提高效率，单页获取 100 条

logger.info(f"📥 开始拉取已提交alpha分数 Alpha: Region={region}, StartDate>={start_date}")

while True:

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&settings.region={region}"

f"&order=-dateCreated"

f"&hidden=false"

)

if start_date:

url += f"&dateCreated%3E%3D{start_date}"

logger.info(f"🔗 Request URL: {url}")

try:

# 发起请求

resp = await asyncio.to_thread(session.get, url, timeout=60)

if resp.status_code != 200:

logger.error(f"请求失败: {resp.status_code} - {resp.text}")

break

data = resp.json()

results = data.get("results", [])

count = data.get("count", 0)

if not results:

logger.info("当前页无数据，结束拉取。")

break

all_alphas.extend(results)

logger.info(f"   -> 已获取 {len(all_alphas)} 条数据 (Offset: {offset}, Total Count: {count})")

offset += limit

if offset >= count:

break

except Exception as e:

logger.error(f"拉取异常: {e}")

break

return all_alphas

async def main():

print("🏆Osmosis Points 统计工具")

print("="*50)

# 1. 登录

username, password = load_credentials()

if not username:

print("❌ 未找到 user_info.txt 或格式错误")

return

session = wqb.WQBSession(wqb_auth=(username, password))

# 简单的连通性测试 (复用原脚本逻辑)

try:

if not session.locate_field('open').ok:

print("❌ 登录失败，请检查网络或密码")

return

except Exception as e:

print(f"❌ 登录检测异常: {e}")

return

print(f"✅ 登录成功: {username}")

# 2. 输入参数

region_input = input("请输入筛选区域 (例如 USA, CHN, EUR): ").strip().upper()

if not region_input:

print("❌ 区域不能为空")

return

# 3. 获取顾问日期

print("正在获取顾问起始日期...")

advisor_start_date = get_advisor_start_date(session)

if not advisor_start_date:

# Fallback default with Timezone

advisor_start_date = "2025-09-16T00:00:00Z"

print(f"获取失败，使用默认日期: {advisor_start_date}")

else:

print(f"成功获取顾问起始日期: {advisor_start_date}")

# 4. 拉取数据

alphas = await fetch_competition_alphas(session, region_input, advisor_start_date)

# 5. 统计分数

if not alphas:

print("⚠️ 未找到符合条件的 Alpha。")

return

print("\n" + "="*60)

print(f"📊 Alpha 详细得分列表 (Region: {region_input})")

print(f"{'Alpha ID':<25} | {'Name':<20} | {'Osmosis Points':<15}")

print("-" * 60)

total_points = 0.0

valid_count = 0

for alpha in alphas:

alpha_id = alpha.get('id', 'N/A')

name = alpha.get('name') or 'N/A'

# 获取 osmosisPoints，如果不存在则默认为 0

points = alpha.get('osmosisPoints', 0)

# 处理可能的 None 值

if points is None:

points = 0.0

else:

points = float(points)

if points == 0:

continue

total_points += points

valid_count += 1

# 截断过长的名字以便显示

display_name = (name[:17] + '..') if len(name) > 17 else name

print(f"{alpha_id:<25} | {display_name:<20} | {points:>10.2f}")

print("="*60)

print(f"✅ 统计完成")

print(f"🔢 Alpha 数量: {valid_count}")

print(f"🏆 总 Osmosis Points: {total_points:.4f}")

print("="*60)

if __name__ == "__main__":

try:

asyncio.run(main())

except KeyboardInterrupt:

print("\n用户取消")

---

## 讨论与评论 (5)

### 评论 #1 (作者: JX14975, 时间: 4个月前)

其实这么做没有什么必要，现在可以直接在genius的面板看到各个地区分配分数的alpha总数与总分。甚至符合标准会打勾，不符合标准会打叉。而且它更新相当即时，大概只有几分钟间隔，比比赛快多了。

---

### 评论 #2 (作者: YL48422, 时间: 4个月前)

好用，点赞

---

### 评论 #3 (作者: JX39934, 时间: 4个月前)

[JX14975](/hc/en-us/profiles/29548387470487-JX14975) 但是比赛页面也看不到哪个alpha打了多少分呀，我觉得这个还是挺方便的，可能大佬们平时喜欢存数据库，就当我没说。

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #4 (作者: XW23690, 时间: 4个月前)

现在genius可以直接看到分数了，几乎是实时的。我修改完再刷新马上就更新了。查漏补缺

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #5 (作者: MS51256, 时间: 3个月前)

感谢分享

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

