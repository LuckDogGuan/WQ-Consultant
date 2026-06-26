# ValueFactor 预测器：自动化滚动3个月 Alpha 表现评估代码优化

- **链接**: ValueFactor 预测器自动化滚动3个月 Alpha 表现评估代码优化.md
- **作者**: JR23144
- **发布时间/热度**: 11个月前, 得票: 78

## 帖子正文

**开箱即用，助您洞悉近期alpha提交的质量**

### 引言：为何需要这个工具？

作为一名 因子挖掘者，如何客观、持续地评估自己提交alpha的表现？我们提交的 Alpha 数量众多，手动去筛选、组合、回测最近几个月的成果，不仅耗时耗力，而且难以形成统一的评估标准。

这个工具旨在解决这一痛点。它能自动化地完成以下任务：

1. **动态筛选** ：自动识别并标记出您最近三个月内提交的 Regular Alphas。
2. **智能组合** ：将标记出的 Alphas 按区域（Region）分组，并为每个符合条件的区域生成一个 SUPER Alpha。
3. **客观评估** ：这个生成的 SUPER Alpha 本身就是一个“价值因子”（Value Factor），它的表现直观地反映了您近期研发工作的综合成效。
4. **自动化流程** ：整个过程通过一个脚本全自动执行，您只需设置一次自己的“顾问生效日期”，即可每日运行，持续追踪。

### 核心理念与设计思路

在深入代码之前，理解其背后的设计思想至关重要。

1. **为何不直接用 Selection Expression？**
   BRAIN 平台的 SUPER Alpha 在选择子 Alpha 时，默认会优先选择 **最早提交** 的 Alpha。这与我们希望评估 **近期表现** 的目标背道而驰。因此，我们不能简单地依赖 selectionLimit，而必须采用一种方式主动筛选出我们想要的 Alpha。
   ![图片](images/img_9b851d57ad.png)
2. **为什么选择用“名字(Name)”进行标记？
   对于RA 的名字的修改只修改已提交阶段的，不影响如果你在未提交阶段对于RA 名字的操作，已提交阶段的alpha 名字用的人应该少吧。**
   为了让 SUPER Alpha 能精准地选中我们想要的子 Alpha，我们需要一个“标记”。通过 API，我们可以修改 Alpha 的名字（Name）或颜色（Color）或打一个Tags 。本脚本选择使用名字，将目标 Alpha 命名为  **"CVF"** （可理解为 Calculate Value Factor）。这样，在 SUPER Alpha 的 Selection Expression 中，我们就可以使用 own && name == "CVF" 来精确抓取这些被选中的 Alpha。
   ![图片](images/img_f692cbe586.png)
3. **“滚动三月”的动态标记逻辑**
   这是整个工具的核心。脚本会执行以下逻辑：
   - **计算评估窗口** ：脚本会自动获取当前日期，并计算出 **三个月前** 的日期作为评估窗口的开始（begin_date）。同时，它会与您设定的 tobe_consultant_day（顾问生效日）进行比较，取 **更晚的那个日期** 作为最终的窗口起点，确保只评估顾问期内的 Alpha。
   - **标记新 Alpha** ：遍历所有顾问期内提交的 Alpha，如果其提交日期落在评估窗口内，且名字 **不是**  "CVF"，脚本会自动将其命名为 "CVF"。
   - **取消旧标记** ：如果一个 Alpha 的提交日期在评估窗口 **之外** ，但其名字却 **是**  "CVF"（说明它是上个周期被标记的），脚本会自动将其名字删除（设置为 None）。
4. **区域性评估与触发条件**
   为了更细致地评估，脚本会按区域（如 EUR, USA 等）对 Alpha 进行分组统计。只有当某个区域内被标记为 "CVF" 的 Alpha 数量 **达到或超过10个** 时，脚本才会为该区域生成 SUPER Alpha。 RA去组SA 要求最少RA为10个。

### 工作原理解析

整个脚本的执行流程分为两个主要阶段：

#### 阶段一：动态标记 Regular Alphas

1. **初始化与日期计算** ：脚本启动，登录 BRAIN，并根据当前日期和您设置的 tobe_consultant_day 计算出最终的评估窗口 [begin_date, end_date)。
2. **获取数据** ：调用 get_submit_alphas 函数，获取您顾问生效日之后提交的所有 Regular Alphas 的信息（ID, Region, Name, DateSubmitted）。
3. **遍历与判断** ：
   - 循环遍历每一个获取到的 Alpha。
   - 判断其提交日期 submitted_date 是否在 [begin_date, end_date) 范围内。
   - **若在范围内** ：检查其名字。如果不是 "CVF"，则调用 up_alpha_properties 函数将其命名为 "CVF"。
   - **若在范围外** ：检查其名字。如果是 "CVF"，则调用 up_alpha_properties 函数将其名字删除。
4. **统计数量** ：在标记过程中，脚本会按区域统计符合条件的 "CVF" Alpha 数量，为下一阶段做准备。

#### 阶段二：生成并命名 SUPER Alphas

1. **构建回测任务** ：遍历上一阶段统计出的各区域 "CVF" 数量。如果某个区域的数量 >= 10，则构建一个 SUPER Alpha 的回测请求 item_data。其中关键配置为：
   - selection: 'own && name == "CVF"' (只选择我们标记的Alpha)
   - combo: '1' (简单求和)
   - settings.selectionLimit: 设为该区域的 "CVF" Alpha 数量。
2. **并行提交** ：使用 ThreadPoolExecutor (线程池)，将所有构建好的回测任务并行提交到 BRAIN 服务器。这大大提升了处理效率，尤其当您在多个区域都有足够数量的 Alpha 时。
3. **等待与获取结果** ：simulate_super_alpha 函数负责处理单个回测任务。它会提交请求，然后通过 wait_get 函数轮询检查回测状态，直到任务完成或失败。
4. **自动重命名** ：一旦一个 SUPER Alpha 成功生成，simulate_and_rename_super_alpha 函数会立即获取其 ID，并将其重命名为一个标准格式：YYYYMMDDVFT_{REGION}（例如：20250819VFT_EUR）。这便于您在平台上查找和管理这些每日生成的价值因子。

### 如何使用

本脚本被设计为“开箱即用”，您只需进行极少的配置。

#### 1. 前置准备

- 确保您的环境中已安装必要的库。
- 确保您的项目路径下有 machine_lib.py 文件，并且其中的 login() 函数可以正常工作（无需手动输入账号密码）。

#### 2. 唯一需要修改的参数

打开脚本，找到下面这行代码，将其中的日期修改为您 **正式成为顾问的日期** 。

```
# 全部代码中只需要修改一处  成为顾问的日期，也就是你alpha开始算钱的日子 ====================
tobe_consultant_day = "2025-04-14"
```

#### 3. 可选修改的参数

- **查询数量** ：如果您在顾问期间提交的 Regular Alphas 总数 **远大于1000** ，请修改下面这行代码中的 1000 为一个更大的数字。
  ```
  all_consultant_alphas = get_submit_alphas(s, tobe_consultant_day, end_date, 1000)
  ```
- **并发线程数** ：如果您希望调整同时进行回测的任务数量，可以修改 MAX_WORKERS 的值。
  Generated python
  ```
  MAX_WORKERS = 3
  ```

#### 4. 运行脚本

完成上述配置后，直接运行此 Python 脚本即可。它会自动完成所有的工作。

### 完整代码

```
# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from machine_lib import *  # 假设 login() 在这里
from concurrent.futures import ThreadPoolExecutor, wait
import json

# ===================================================================
# PART 1: 函数定义
# ===================================================================

def up_alpha_properties(s, alpha_id, name: str = None):
    """
    一个简化的函数，专门用于修改alpha的名字。
    """
    if name is None:
        # 删除名字
        params = {"name": None}
    else:
        # 设置新名字
        params = {"name": name}

    response = s.patch(
        f"https://api.worldquantbrain.com/alphas/{alpha_id}", json=params
    )
    if response.status_code == 200:
        print(f"成功将 Alpha {alpha_id} 的名字修改为 '{name}'。")
    else:
        print(f"修改 Alpha {alpha_id} 名字失败，状态码: {response.status_code}, 信息: {response.text}")

REGIONS = {
            "USA": "TOP3000",
            "GLB": "TOP3000",
            "EUR": "TOP2500",
            "ASI": "MINVOL1M",
            "CHN": "TOP2000U",
            'KOR': 'TOP600',
            'TWN': 'TOP500',
            'HKG': 'TOP800',
            'JPN': 'TOP1600',
            'AMR': 'TOP600',
            # ... 只取其中一个就行了 因为无论选哪一个universe ，都会默认用该区域下的任何alpha
        }

def get_submit_alphas(s, start_date, end_date, alpha_num):
    # 此函数保持您提供的版本
    output = []
    count = 0
    for i in range(0, alpha_num, 100):
        print(f"正在获取第 {i} 到 {i + 100} 个 alpha...")
        url_e = f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}" \
                f"&status!=UNSUBMITTED%1FIS_FAIL&dateSubmitted>={start_date}T00:00:00-04:00" \
                f"&dateSubmitted<{end_date}T00:00:00-04:00&order=-is.sharpe&hidden=false&type!=SUPER&settings.delay=1"
        try:
            response = s.get(url_e)
            response.raise_for_status()
            alpha_list = response.json()["results"]
            if not alpha_list:
                print("已获取所有符合条件的 alpha。")
                break
            for j in range(len(alpha_list)):
                alpha_id = alpha_list[j]["id"]
                region = alpha_list[j]["settings"]["region"]
                name = alpha_list[j]["name"]
                dateSubmitted = alpha_list[j]['dateSubmitted']
                rec = [alpha_id, region, name, dateSubmitted]
                output.append(rec)
            count += len(alpha_list)
        except Exception as e:
            print(f"获取alpha时发生异常: {e}")
            resp = s.get('https://api.worldquantbrain.com/users/self')
            if resp.status_code != 200:
                print(f"用户会话可能已过期，状态码: {resp.status_code}")
            break
    print(f"总共获取了 {len(output)} 个 alphas。")
    return output

def wait_get(s, url: str, max_retries: int = 10) -> "Response":
    """发送带有重试机制的 GET 请求。"""
    retries = 0
    while retries < max_retries:
        while True:
            simulation_progress = s.get(url)
            if simulation_progress.headers.get("Retry-After", 0) == 0:
                break
            time.sleep(float(simulation_progress.headers["Retry-After"]))
        if simulation_progress.status_code < 400:
            if "ERROR" in simulation_progress.text:
                try:
                    data = simulation_progress.json()
                    message = data.get("message")
                    print(f"回测检查失败 {url}：{message}")
                except json.JSONDecodeError:
                    print(f"回测检查失败 {url}：{simulation_progress.text}")
            return simulation_progress
        else:
            time.sleep(2 ** retries)
            retries += 1
    print(f"达到最大重试次数后，获取 {url} 仍然失败。")
    return simulation_progress

def simulate_super_alpha(s, data, alpha_fail_attempt_tolerance=5):
    """提交SUPER alpha回测，等待完成，并返回alpha ID。"""
    failure_count = 0
    while failure_count < alpha_fail_attempt_tolerance:
        try:
            print(f"正在为区域 {data['settings']['region']} 提交SUPER alpha回测...")
            simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=data)
            simulation_response.raise_for_status()  # 检查提交是否成功

            simulation_progress_url = simulation_response.headers['Location']
            child_id = simulation_progress_url.split('/')[-1]

            print(f"回测任务 {child_id} 已提交，正在等待结果...")
            child_progress_response = wait_get(s, f'https://api.worldquantbrain.com/simulations/{child_id}')

            if child_progress_response.status_code == 200:
                child_progress = child_progress_response.json()
                if child_progress['status'] in ['COMPLETE', 'WARNING']:
                    print(f"回测 {child_id} 成功！新的 SUPER alpha ID: {child_progress['alpha']}")
                    return child_progress['alpha']  # 成功，返回 alpha ID
                else:
                    print(
                        f"回测 {child_id} 失败或被取消，状态: {child_progress['status']}, 原因: {child_progress.get('message')}")
                    return None  # 回测失败
            else:
                print(f"获取回测结果 {child_id} 失败，状态码: {child_progress_response.status_code}")
                failure_count += 1
                time.sleep(15)

        except Exception as e:
            print(f"提交回测或等待过程中发生异常: {e}。正在重试...")
            time.sleep(15)
            failure_count += 1
            if failure_count % 3 == 0:  # 每3次失败重新登录一下
                print("尝试重新登录...")
                s = login()

    print(f"为区域 {data['settings']['region']} 的回测任务失败次数过多，放弃。")
    return None  # 多次失败后，返回 None

def simulate_and_rename_super_alpha(s, item_data):
    """完整流程：提交、等待、成功后重命名"""
    new_alpha_id = simulate_super_alpha(s, item_data)

    if new_alpha_id:
        # 生成新名字，例如：20250819VFT_EUR
        today_str = datetime.now().strftime("%Y%m%d")
        region = item_data["settings"]["region"]
        new_name = f"{today_str}VFT_{region}"

        print(f"准备将新的 SUPER alpha {new_alpha_id} 重命名为 '{new_name}'...")
        up_alpha_properties(s, new_alpha_id, name=new_name)
    else:
        print(f"由于区域 {item_data['settings']['region']} 的SUPER alpha创建失败，跳过重命名。")

# ===================================================================
# PART 2: 主逻辑
# ===================================================================

s = login()

# --- 阶段一：标记Regular Alphas ---
tobe_consultant_day = "2025-04-14"  # 全部代码中只需要修改一处  成为顾问的日期，也就是你alpha开始算钱的日子 ====================
calculate_month = datetime.now().strftime("%Y-%m")
calc_month_obj = datetime.strptime(calculate_month, "%Y-%m")
begin_date_obj = calc_month_obj - relativedelta(months=3)
begin_date = begin_date_obj.strftime("%Y-%m-%d")
end_date_obj = datetime.now() + timedelta(days=1)
end_date = end_date_obj.strftime("%Y-%m-%d")

print("配置信息:")
print(f"自动获取的计算月份: {calculate_month}")
print(f"顾问开始日: {tobe_consultant_day}")
if tobe_consultant_day > begin_date:
    print(f"顾问开始日晚于计算日期，将使用顾问开始日作为有效起始点。")
    begin_date = tobe_consultant_day
print(f"最终生效的VF窗口开始日期: {begin_date}")
print("-" * 30)

all_consultant_alphas = get_submit_alphas(s, tobe_consultant_day, end_date, 1000)

print("\n开始处理 Regular Alphas...")
begin_date_compare = datetime.strptime(begin_date, "%Y-%m-%d").date()
end_date_compare = datetime.strptime(end_date, "%Y-%m-%d").date()
regions_num = {}

for alpha_data in all_consultant_alphas:
    alpha_id, region, alpha_name, date_submitted_str = alpha_data
    if region not in regions_num:
        regions_num[region] = 0

    submitted_date = datetime.fromisoformat(date_submitted_str).date()

    if begin_date_compare <= submitted_date < end_date_compare:
        regions_num[region] += 1
        if alpha_name != "CVF":
            up_alpha_properties(s, alpha_id, name="CVF")
    else:
        if alpha_name == "CVF":
            up_alpha_properties(s, alpha_id, name=None)

# --- 阶段二：创建和重命名SUPER Alphas ---
print("\n开始创建 SUPER Alphas...")
sim_data_list = []
for query_region, num in regions_num.items():
    if num >= 10:  # 只有当一个区域有足够数量的CVF alpha时才创建
        print(f"区域 {query_region} 有 {num} 个CVF alpha，符合创建SUPER alpha的条件。")
        item_data = {
            "type": "SUPER",
            "settings": {
                "nanHandling": "OFF", "instrumentType": "EQUITY", "delay": 1,
                "universe": REGIONS.get(query_region, "TOP3000"),  # 使用.get()更安全
                "truncation": 0.01, "unitHandling": "VERIFY", "selectionLimit": num,
                "selectionHandling": "POSITIVE", "pasteurization": "ON", "region": query_region,
                "language": "FASTEXPR", "decay": 5, "neutralization": "INDUSTRY",
                "visualization": False, "testPeriod": "P2Y",
            },
            "combo": '1', "selection": 'own&&name == \"CVF\"',
        }
        if query_region in ["ASI"]:
            item_data["settings"]["maxTrade"] = "ON"
        sim_data_list.append(item_data)

if not sim_data_list:
    print("\n没有需要创建的 SUPER alpha。程序结束。")
else:
    # 使用线程池并行处理
    MAX_WORKERS = 2
    print(f"\n准备使用 {MAX_WORKERS} 个线程并行创建和重命名 {len(sim_data_list)} 个 SUPER alpha...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        futures = [executor.submit(simulate_and_rename_super_alpha, s, batch) for batch in sim_data_list]
        # 等待所有任务完成
        wait(futures)

    print("\n所有滚动检测并生成SA处理任务已完成。")
```

运行截图：
 ![图片](images/img_b3a0309c00.png)

![图片](images/img_8abac32f31.png)

![图片](images/img_5fb278bb8e.png)

![图片](images/img_b3d629f292.png)

---

## 讨论与评论 (6)

### 评论 #1 (作者: SX13432, 时间: 11个月前)

神器啊，先re再试，赞大神 ![图片](images/img_e351e2f9e2.png) ！

---

### 评论 #2 (作者: SX13432, 时间: 11个月前)

追评。程序很容易上手，对已提交alpha做全局评估，真的很方便！感谢分享   [JR23144](/hc/zh-cn/profiles/28844048981143-JR23144)

---

### 评论 #3 (作者: JX79797, 时间: 11个月前)

已下载使用，非常完美，还没来得及干的事情可以省下了

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #4 (作者: SL52857, 时间: 11个月前)

感谢大佬分享，代码很详细！

---

### 评论 #5 (作者: MY27687, 时间: 10个月前)

================================MY27687=============================================
确实是不错的分享，可以看到最近的提交质量，感谢大佬的分享，太方便了!!!!
祝大佬base多多，vf高高

====================================================================================

---

### 评论 #6 (作者: WH74165, 时间: 9个月前)

呜呜呜这个程序会把我alpha的名字都改掉，没仔细看。一回头幸幸苦苦做的名字分类全没了

---

