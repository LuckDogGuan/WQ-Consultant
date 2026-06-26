# 请说你想当推荐王？推荐管理工具免费送上

- **链接**: [Commented] 请说你想当推荐王推荐管理工具免费送上.md
- **作者**: TL32287
- **发布时间/热度**: 4个月前, 得票: 56

## 帖子正文

众所周知，推荐新人有100美元的奖励，但是如果新人很多又不知道转化成功没？需要很多时候翻记录才可以知道。于是我写了一个推荐新人管理工具，支持索引查询，这样在推荐新人的帮助的时候能够分开处理。eligibleAlphas能够查询成为顾问之后有没有提交满10个因子，更好的帮助老顾问解决新人的问题，做到定向可持续的输出新质人才。

创建一个refermanagement.ipynb:

from machine_lib import login

import pandas as pd

s = login()

resp = s.get(" [https://api.worldquantbrain.com/users/self/activities/referrals?order=-number](https://api.worldquantbrain.com/users/self/activities/referrals?order=-number) ")

data = resp.json()

# 解析 results 为表格

rows = []

for item in data.get("results", []):

u = item.get("user", {})

rows.append({

"inviteNumber": item.get("inviteNumber"),

"id": u.get("id"),

"country": u.get("country"),

"status": u.get("status"),

"signIn": u.get("signIn"),

"startDate": u.get("startDate"),

"eligibleAlphas": u.get("eligibleAlphas"),

"active": u.get("active"),

})

df = pd.DataFrame(rows)

print(f"共 {data.get('count', 0)} 条推荐记录")

df

#索引查询代码

# 输入ID查询推荐状态

uid = input("请输入用户ID: ").strip()

match = df[df["id"] == uid]

if match.empty:

print(f"未找到ID: {uid}")

else:

row = match.iloc[0]

status = row["status"]

invite_num = row["inviteNumber"]

if status == "consultant":

print(f"【推荐完成】ID {uid} (邀请#{invite_num}) 已成为顾问。")

print("预计将获得 100 美元推荐奖励。")

elif status == "referralCriteriaComplete":

print(f"【满足条件顾问】ID {uid} (邀请#{invite_num}) 已满足推荐条件，等待转为顾问。")

print("可参考以下步骤协助完成：提交 10+ 合格 alpha、满足一个月活跃要求等。")

elif status == "user":

print(f"【普通用户】ID {uid} (邀请#{invite_num}) 仍为 user，尚未满足顾问条件。")

print(f"  - signIn: {row['signIn']}, eligibleAlphas: {row['eligibleAlphas']}, active: {row['active']}")

---

## 讨论与评论 (14)

### 评论 #1 (作者: JX39934, 时间: 4个月前)

好东西，感谢大佬分享的代码，还有就是想问下去哪里找推荐人高效一些呢，感觉很难找到新人。

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #2 (作者: MZ45384, 时间: 4个月前)

代码有了，新人在哪里找。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #3 (作者: ZL75781, 时间: 4个月前)

好东西，我最近在学校去推荐学生来做这个，还在想应该怎么管理，这不代码就来了

=============================================================================

Fortune favors the bold.Keep calm and carry on.

=============================================================================

---

### 评论 #4 (作者: HC58447, 时间: 3个月前)

我测了下，复制粘贴的，然后啥也没有，登录文件也放在当前文件夹了

---

### 评论 #5 (作者: MG88592, 时间: 3个月前)

======================================================================================

感谢分享，祝您一路长虹

======================================================================================

---

### 评论 #6 (作者: YH55729, 时间: 3个月前)

推荐的新人都不坚持提交，很头疼啊

=============================================================================

---

### 评论 #7 (作者: XW23690, 时间: 3个月前)

很有用，那么新人在哪领取（开玩笑

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #8 (作者: YQ84572, 时间: 3个月前)

很好的管理工具，学会了，来点新鲜血液
=============================================================================

感谢分享，祝大佬vf0.9++

=============================================================================

---

### 评论 #9 (作者: HW93328, 时间: 3个月前)

============================HW93328============================

未曾设想的代码，但是没有新人呜呜，带新人还是个很困难的工作~~

============================HW93328============================

---

### 评论 #10 (作者: BW14163, 时间: 3个月前)

感谢分享，不知道去哪里才能找到合适的新人

---

### 评论 #11 (作者: XY20037, 时间: 3个月前)

太感谢大佬分享这个推荐管理工具了！手动翻推荐记录查新人状态真的太费时间，这个脚本直接通过 API 拉取所有推荐数据，还能按 ID 精准查询状态（顾问 / 满足条件 / 普通用户），甚至能看到 eligibleAlphas 数量，帮新人定向解决提交因子的问题，实用性拉满！评论区大家都在问新人去哪找，其实校园渠道（像 ZL75781 大佬说的推荐学生）、量化社群 / 论坛都是不错的方向，不过带新人确实难，能有这个工具管理状态已经省了超多事，再次感谢大佬的无私分享！

---

### 评论 #12 (作者: SJ65808, 时间: 3个月前)

大佬都在哪里招新人

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #13 (作者: TL32287, 时间: 3个月前)

招聘新人推荐去小红书、BOSS、甚至量化群去打广告，不过你要是有自营流量那么更好，最好是培养一批能帮助你的新人，不然一个培训还是很累的。不然就只能10人一个批次的培训。
用推荐管理代码是可以查看新人的状态，方便你知道那些新人是值得你培养的，就像有些Alpha是赚钱的，你得投资他，没事投资Beta干什么？
新人推荐管理工具V1.5版本：

from machine_lib import login

import pandas as pd

# ========== 第一步：获取推荐用户列表 ==========

print("="*50)

print("第一步：获取推荐用户列表")

print("="*50)

s = login()

resp = s.get(" [https://api.worldquantbrain.com/users/self/activities/referrals?order=-number](https://api.worldquantbrain.com/users/self/activities/referrals?order=-number) ")

data = resp.json()

# 解析 results 为表格

rows = []

for item in data.get("results", []):

u = item.get("user", {})

rows.append({

"inviteNumber": item.get("inviteNumber"),

"id": u.get("id"),

"country": u.get("country"),

"status": u.get("status"),

"signIn": u.get("signIn"),

"startDate": u.get("startDate"),

"eligibleAlphas": u.get("eligibleAlphas"),

"active": u.get("active"),

})

df_referrals = pd.DataFrame(rows)

print(f"共 {data.get('count', 0)} 条推荐记录\n")

print(df_referrals[['inviteNumber', 'id', 'status', 'eligibleAlphas']])

# ========== 第二步：对每个推荐用户查询竞赛信息 ==========

print("\n" + "="*50)

print("第二步：查询所有推荐用户的竞赛信息")

print("="*50)

competition_results = []

for idx, referral_row in df_referrals.iterrows():

uid = referral_row['id']

print(f"\n正在查询用户 #{idx+1}: {uid}")

# 查询竞赛信息

url = f" [https://api.worldquantbrain.com/competitions/challenge/boards/leader?limit=30&offset=0&user~{uid}&aggregate=user](https://api.worldquantbrain.com/competitions/challenge/boards/leader?limit=30&offset=0&user~{uid}&aggregate=user) "

resp = s.get(url)

comp_data = resp.json()

if comp_data.get('count', 0) > 0:

result = comp_data['results'][0]

score = result.get('score', 0)

level = result.get('level', '')

# 判断用户阶段

if score < 10000:

status_msg = "【用户阶段】分数较低，需要积极提交因子！"

suggestion = "💡 提示：建议该用户多提交优质 Alpha 因子以提高分数"

else:

status_msg = "【活跃阶段】分数良好，继续保持！"

suggestion = "✅ 表现不错，继续加油！"

print(f"  - 排名：{result.get('rank')}")

print(f"  - 等级：{level}")

print(f"  - 分数：{score}")

print(f"  - Alpha 数量：{result.get('alphas')}")

print(f"  - 学校：{result.get('university')}")

print(f"  - 国家：{result.get('country')}")

print(f"  - 国内排名：{result.get('localRank')}")

print(f"  - 状态：{status_msg}")

print(f"  - 建议：{suggestion}")

# 保存结果

competition_results.append({

'id': uid,

'rank': result.get('rank'),

'level': level,

'score': score,

'alphas': result.get('alphas'),

'university': result.get('university'),

'country': result.get('country'),

'localRank': result.get('localRank'),

'status': status_msg

})

else:

print(f"  ⚠️ 未找到该用户的竞赛信息")

# 根据推荐状态给出提示

referral_status = referral_row.get('status', '')

eligible_alphas = referral_row.get('eligibleAlphas', '0')

# 判断是否一个因子都没提交

zero_alphas = (eligible_alphas == '0' or eligible_alphas == 0 or eligible_alphas == 'None')

if referral_status == 'consultant':

print(f"  💎【顾问】该用户已成为顾问，可能不需要参加竞赛")

elif referral_status == 'referralCriteriaComplete':

print(f"  ✅【满足条件】已满足推荐条件，等待转为顾问")

print(f"     已提交 {eligible_alphas} 个合格 Alpha，表现不错！")

elif referral_status == 'user' and zero_alphas:

print(f"  ❌【未提交】该用户一个因子都未提交，需要督促！")

print(f"     建议：尽快登录并提交至少 10 个合格 Alpha 因子")

elif referral_status == 'user':

print(f"  📊【普通用户】已提交 {eligible_alphas} 个 Alpha，但分数可能较低")

print(f"     建议：继续优化因子质量，提高竞赛分数")

else:

print(f"  ℹ️  状态：{referral_status}, 已提交：{eligible_alphas} 个 Alpha")

# 保存结果

competition_results.append({

'id': uid,

'rank': None,

'level': None,

'score': None,

'alphas': int(str(eligible_alphas).replace('+', '')) if str(eligible_alphas).replace('+', '').isdigit() else 0,

'university': None,

'country': None,

'localRank': None,

'status': f'无竞赛记录-{referral_status}'

})

# ========== 第三步：汇总分析 ==========

print("\n" + "="*50)

print("第三步：汇总分析")

print("="*50)

df_competition = pd.DataFrame(competition_results)

# 合并推荐信息和竞赛信息

df_merged = pd.merge(df_referrals, df_competition, on='id', how='left')

# 显示完整信息

print("\n完整信息表:")

# 检查列是否存在，使用安全的列选择

available_cols = []

for col in ['id', 'status', 'eligibleAlphas', 'score', 'level', 'rank', 'alphas']:

if col in df_merged.columns:

available_cols.append(col)

else:

print(f"⚠️  注意：列 '{col}' 不存在")

if available_cols:

print(df_merged[available_cols].to_string())

else:

print("无法显示表格，缺少必要列")

# 统计低分用户（需要督促）

low_score_users = df_competition[df_competition['score'] < 10000]

if len(low_score_users) > 0:

print(f"\n⚠️ 需要督促的用户 (分数<10000):")

for _, row in low_score_users.iterrows():

print(f"  - {row['id']}: {row['score']}分 - 需要积极提交因子")

else:

print(f"\n✅ 所有用户分数都在 10000 以上，表现优秀！")

# 保存到 CSV（可选）

save_file = input("\n是否保存完整信息到 CSV？(y/n): ").strip().lower()

if save_file == 'y':

output_file = 'referral_competition_analysis.csv'

df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"已保存到 {output_file}")

---

### 评论 #14 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的这个推荐管理工具的分享，虽然我的推荐比较少，但是我还是先收藏                              ================================自信人生两百年，会当水击三千里==========================

---

