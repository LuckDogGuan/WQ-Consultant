# 批量隐藏数据缺失因子工具代码优化

- **链接**: [Commented] 批量隐藏数据缺失因子工具代码优化.md
- **作者**: AC13170
- **发布时间/热度**: 6个月前, 得票: 3

## 帖子正文

该代码基于游戏王大佬（ [ZS59763](/hc/zh-cn/profiles/26858512793111-ZS59763) ）的代码上进行优化，实现即插即用
 [[游戏王]批量隐藏厂与数据缺失因子（复制即用！） – WorldQuantBrain-CN](../ZS59763/[游戏王]批量隐藏厂与数据缺失因子复制即用代码优化.md)

由于大佬修改了machine_lib中的get_alphas（）函数，其给出的代码无法适配，所以我用AI对代码进行了优化，感谢大佬提供的灵感！

工具实现了对数据少于8年的因子进行隐藏，即插即用，提高筛选效率！

代码如下：

import os
import logging
import time
import requests
import datetime  # 新增导入
from machine_lib import *

def wait_get(s, url: str, max_retries: int = 10) -> "Response":  # 新增s参数（接收会话对象）
    retries = 0
    while retries < max_retries:
        while True:
            simulation_progress = s.get(url)  # 使用传入的会话对象s
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
    #print(alpha_id, "通过")
    return True

import datetime

# 修正后定义（添加s参数，作为第一个参数）：
def get_alpha_pnl_legal(s, alpha_id: str) -> bool:  # 新增s参数
    not_legal_id = []
    # 移除内部重复登录的代码（如果还有的话）：s = login()
    pnl = wait_get(s, " [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id + "/recordsets/pnl").json()
    records = pnl["records"]

    # 后续原有逻辑保持不变...
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
    # SA需要取消下面的注释
    # col2_zeros = [record[2] == 0 for record in records]  # Equal Weight PnL列

    # 检测连续零值的最大长度
    def max_consecutive_zeros(arr):
        max_streak = current_streak = 0
        for val in arr:
            current_streak = current_streak + 1 if val else 0
            max_streak = max(max_streak, current_streak)
        return max_streak

    col1_max_zero_streak = max_consecutive_zeros(col1_zeros)
    # sa需要取消下面的注释
    # col2_max_zero_streak = max_consecutive_zeros(col2_zeros)

    # 若任一列存在连续≥8年的零值，判定为不合格
    # if col1_max_zero_streak >= zero_streak_threshold or col2_max_zero_streak >= zero_streak_threshold:
    #     print(f"{alpha_id} 不合法：存在连续{zero_streak_threshold//252}年零值")
    #     return False
    # SA取消上面的注释，注释下面的代码
    if col1_max_zero_streak >= zero_streak_threshold:  # 修正语法错误：移除多余的 >= zero_streak_threshold
        print(f"{alpha_id} 不合法：存在连续{zero_streak_threshold//252}年零值")
        not_legal_id.append(str(alpha_id))
        return False
    # 3. 保留原有连续非零值检查
    if not check_consecutive_non_zero_values(alpha_id, records):
        return False
    return True  # 确保合法时返回True

def get_alpha_pnl_legal_list(s, fo_tracker: list) -> list:  # 新增s参数
    fo_tracker = [fo for fo in fo_tracker if get_alpha_pnl_legal(s, fo[0])]  # 调用时传入s
    return fo_tracker

# 1. 修改mute()函数：添加会话参数s
def mute(s, alpha_id):  # 新增s参数（接收登录会话）
    url = " [https://api.worldquantbrain.com/alphas/"+alpha_id](https://api.worldquantbrain.com/alphas/%22+alpha_id) 
    data = {
        "hidden": True
    }
    response = s.patch(url, json=data)
    # 可选：添加响应日志，确认隐藏成功
    # print(f"隐藏Alpha {alpha_id}，响应状态码：{response.status_code}")

fo_tracker, s = get_alphas('12-01', '12-31', 1, 0.5, 'USA', 1000, 'submit')  # 接收s
f_num = len(fo_tracker)
print(f_num,"个alpha 进行pnl合法检测，请耐心等待")
count=0
print(len(fo_tracker))
for i in fo_tracker[::-1][0:]:
    if count%25==0:
        print('===========',count,'===========')
    count+=1
    if get_alpha_pnl_legal(s, i[0])==False:  # 传入会话s到get_alpha_pnl_legal()
        print(i[0],'已经隐藏')
        mute(s, i[0])  # 传入会话s到mute()

————————————————————————————————————————

get_alphas('12-01', '12-31', 1, 0.5, 'USA', 1000, 'submit')

筛选时修改参数即可('起始日期', '截止日期', Sharpe,Fitness, '地区', 数量, 'submit') 
最后一项默认不用改

————————————————————————————————————————
最后还需修改machine_lib的get_alphas（）函数，新增一个会话s = login()，让工具只需登录一次，避免反复登录

def get_alphas(start_date, end_date, sharpe_th, fitness_th, region, alpha_num, usage):
    s = login()
    output = []
    # 3E large 3C less
    count = 0
    for i in range(0, alpha_num, 100):
        print(i)
        url_e = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \
                + "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2025-" + start_date  \
                + "T00:00:00-04:00&dateCreated%3C2025-" + end_date \
                + "T00:00:00-04:00&is.fitness%3E" + str(fitness_th) + "&is.sharpe%3E" \
                + str(sharpe_th) + "&settings.region=" + region + "&order=-is.sharpe&hidden=false&type!=SUPER"
        url_c = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \
                + "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2025-" + start_date  \
                + "T00:00:00-04:00&dateCreated%3C2025-" + end_date \
                + "T00:00:00-04:00&is.fitness%3C-" + str(fitness_th) + "&is.sharpe%3C-" \
                + str(sharpe_th) + "&settings.region=" + region + "&order=is.sharpe&hidden=false&type!=SUPER"
        urls = [url_e]
        if usage != "submit":
            urls.append(url_c)
        for url in urls:
            response = s.get(url)
            #print(response.json())
            try:
                alpha_list = response.json()["results"]
                #print(response.json())
                for j in range(len(alpha_list)):
                    alpha_id = alpha_list[j]["id"]
                    name = alpha_list[j]["name"]
                    dateCreated = alpha_list[j]["dateCreated"]
                    sharpe = alpha_list[j]["is"]["sharpe"]
                    fitness = alpha_list[j]["is"]["fitness"]
                    turnover = alpha_list[j]["is"]["turnover"]
                    margin = alpha_list[j]["is"]["margin"]
                    longCount = alpha_list[j]["is"]["longCount"]
                    shortCount = alpha_list[j]["is"]["shortCount"]
                    decay = alpha_list[j]["settings"]["decay"]
                    exp = alpha_list[j]['regular']['code']
                    count += 1
                    #if (sharpe > 1.2 and sharpe < 1.6) or (sharpe < -1.2 and sharpe > -1.6):
                    if (longCount + shortCount) > 100:
                        if sharpe < -sharpe_th:
                            exp = "-%s"%exp
                        rec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]
                        print(rec)
                        if turnover > 0.7:
                            rec.append(decay*4)
                        elif turnover > 0.6:
                            rec.append(decay*3+3)
                        elif turnover > 0.5:
                            rec.append(decay*3)
                        elif turnover > 0.4:
                            rec.append(decay*2)
                        elif turnover > 0.35:
                            rec.append(decay+4)
                        elif turnover > 0.3:
                            rec.append(decay+2)
                        output.append(rec)
            except:
                print("%d finished re-login"%i)
                s = login()

print("count: %d"%count)
    return output, s  # 新增返回会话s
————————————————————————————————————————

效果如下: ![图片](images/img_dbbf0a735c.png)

---

## 讨论与评论 (2)

### 评论 #1 (作者: AC13170, 时间: 6个月前)

代码链接:  [https://pan.baidu.com/s/1ZS3hV-TZ1SffIfPU637LWg?pwd=2xcv](https://pan.baidu.com/s/1ZS3hV-TZ1SffIfPU637LWg?pwd=2xcv)  提取码: 2xcv

分享代码时，请注意不要泄露自己的账号信息

---

### 评论 #2 (作者: SJ65808, 时间: 3个月前)

筛选alpha的时候很有用，感谢大佬分享

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

