# Alpha PNL 合法性检测,【自动剔除 “厂” Alpha等无效Alpha，实现高效率剪枝】代码优化

- **链接**: [Commented] Alpha PNL 合法性检测【自动剔除 厂 Alpha等无效Alpha实现高效率剪枝】代码优化.md
- **作者**: JR23144
- **发布时间/热度**: 1年前, 得票: 123

## 帖子正文

在进行培训代码回测时，我发现一个规律：如果一个 Alpha 在一阶回测时表现为 “厂” Alpha（指 PNL 呈现特定不良模式），那么基于这个 Alpha 进行后续的二阶、三阶优化或组合，其结果大概率仍然是“厂”Alpha。因此，我认为有必要在初步筛选阶段就将这类 Alpha 剔除。

![图片](images/img_e53ae55211.png)

两个步骤，就能开箱即用

**1.** 新建一个名为 **pnl_test.py**  的Python 文件  **，粘贴下列代码（并修改登录信息为你的实际登录信息）**

```
import osfrom dotenv import load_dotenvimport loggingimport timeimport requestsfrom machine_lib import *class cfg:    env_path = "user.env"    load_dotenv(dotenv_path=env_path)    username = os.environ["USER_NAME"]    password = os.environ["PASSWORD"]def sign_in(username, password):    s = requests.Session()    s.auth = (username, password)    try:        response = s.post('https://api.worldquantbrain.com/authentication')        response.raise_for_status()        logging.info("Successfully signed in")        return s    except requests.exceptions.RequestException as e:        logging.error(f"Login failed: {e}")        return Nonedef wait_get(url: str, max_retries: int = 10) -> "Response":    retries = 0    while retries < max_retries:        while True:            simulation_progress = sess.get(url)            if simulation_progress.headers.get("Retry-After", 0) == 0:                break            time.sleep(float(simulation_progress.headers["Retry-After"]))        if simulation_progress.status_code < 400:            break        else:            time.sleep(2 ** retries)            retries += 1    return simulation_progressdef check_consecutive_non_zero_values(alpha_id, data, required_streak=200):    if not data or len(data) < required_streak:        return True    def check_column(column_data):        if len(column_data) < required_streak:            return True        current_streak_count = 0        current_streak_value = None        for value in column_data:            if value != 0:                if value == current_streak_value:                    current_streak_count += 1                else:                    current_streak_value = value                    current_streak_count = 1            else:                current_streak_value = None                current_streak_count = 0            if current_streak_count >= required_streak:                return False        return True    column1_values = []    column2_values = []    for row in data:        if len(row) >= 3:            column1_values.append(row[1])            column2_values.append(row[2])        else:            pass    if column1_values and column2_values:        is_col1_all_zeros = all(v == 0 for v in column1_values)        is_col2_all_zeros = all(v == 0 for v in column2_values)        if is_col1_all_zeros or is_col2_all_zeros:            print(alpha_id, "不合法")            return False    if not check_column(column1_values):        print(alpha_id, "不合法")        return False    if not check_column(column2_values):        print(alpha_id, "不合法")        return False    print(alpha_id, "通过")    return Truedef get_alpha_pnl_legal(alpha_id: str) -> bool:    pnl = wait_get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl").json()    records = pnl["records"]    return check_consecutive_non_zero_values(alpha_id, records)def get_alpha_pnl_legal_list(fo_tracker: list) -> list:    global sess    sess = sign_in(cfg.username, cfg.password)    fo_tracker =[fo for fo in fo_tracker if get_alpha_pnl_legal(fo[0])]    return fo_trackersess = sign_in(cfg.username, cfg.password)
```

**2.  在notebook中** 修改其中筛选第一次回测完的Alpha

```
fo_tracker = get_alphas("06-12", "06-13", 1, 0.7, "ASI", 200, "track")# 添加以下几行import pnl_testf_num = len(fo_tracker)print(f_num,"个alpha 进行pnl合法检测，请耐心等待")fo_tracker = pnl_test.get_alpha_pnl_legal_list(fo_tracker)print(f_num -len(fo_tracker),"个不合法的pnl,已被剔除" )
```

**希望这个小脚本能帮你提升回测效率。** 
 **觉得还行？一个小赞就能让我动力满满，一起day day Alpha！**

---

## 讨论与评论 (25)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很好用的代码，点赞！！！

解决了 厂一直筛不掉的问题，可惜我的服务器太垃圾，跑点大的代码就报错。

这里也提供一个优化思路：检测到厂，把它隐藏，这样就不会再出现，再筛选了

---

### 评论 #2 (作者: MY27687, 时间: 1年前)

==================================MY27687===========================================感谢大佬提供简枝工具，确实很好用，平常太容易碰到厂形的alpha，解决了很大的问题，减少了二阶段的回测，真的很有用，感谢大佬！！！！！
====================================================================================

---

### 评论 #3 (作者: SD17531, 时间: 1年前)

好思路

我也借助AI实现了一个剔除''厂''的方式, 我是直接把感觉还可以的alpha的PNL下载到本地,然后在本地直接计算了了2021和2022年的sharpe, 并且设定筛选条件, 这两年的sharpe必须要都大于1,这样就遇到的'厂'就不多了.主要还是PPA的影响,以前没有PPA的时候, 是可以通过判断2Y sharpe和另一个指标来排除这个'厂'的,这样的话,就不需要多走一步去拉取PNL数据了.不过我把上面这一步也整合到了提交alpha之前的筛选条件里面,更加关注alpha近几年的数据是否表现好.
后续如果是直接在本地根据PNL画出sharpe的话,其实都可以减少去网页看数据的操作了,打开网页经常会卡.

---

### 评论 #4 (作者: FL39657, 时间: 1年前)

在第一阶段剔除厂，可以再接下来的过程中提升不少回测效率

---

### 评论 #5 (作者: AH18340, 时间: 1年前)

感谢大佬分享，我也用了类似方法，这是主要通过

[https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id + "/recordsets/pnl

这个接口获取pnl数据，然后对比pnl尾部的数据是否连续相同，如连续相同大于整体数据的30%，就认为这个厂

---

### 评论 #6 (作者: XC66172, 时间: 1年前)

感谢楼主分享，我一般是在筛选因子的时候把厂子alpha筛选掉。不过能在一阶就过滤掉确实不错，这样二阶三阶就能节省不少回测时间了。

在研究小组里看到如果可以在SA中筛掉厂子alpha就更好了（或不给权重），等有空的时候想想COMBO表达式怎么写。

============================每天睡醒就搓搓因子，总有一个是好的=========================

---

### 评论 #7 (作者: YQ51506, 时间: 1年前)

赞，学习了！

---

### 评论 #8 (作者: JG21054, 时间: 1年前)

感谢!  借这个帖子分享一个相似的方法，通过另一个接口来剔除“厂”alpha的代码。由于“厂”alpha的Sharpe近两年都为0，所以通过接口直接获取近两年的sharpe，将近两年sharpe为0的alpha剔除掉。

这个接口还可以用来判断alpha的sharpe走势，可以参考这个数据挑选更好的alpha。也可以获取每年的夏普率，避免在有些年份的Sharpe过低或者只有几年数据的alpha。大家可以结合自己获取函数的方式运用这个接口，也可以分享一下这种接口其他的使用小技巧。

```
def get_sharpe_two_years(s, alpha_id):    """获取Alpha在2021年和2022年的Sharpe值"""    # 处理API限流    while True:        response = s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats")                # 检查是否需要重试        retry_after = response.headers.get("Retry-After")        if retry_after:            logging.debug(f"API限流，Alpha {alpha_id} 等待 {retry_after} 秒后重试")            time.sleep(float(retry_after))            continue        break            # 解析响应    result = {'2021': None, '2022': None}        try:        data = response.json()        for record in data.get("records", []):            if not record:                continue            record_year = record[0]                        if record_year in ['2021', '2022']:                if len(record) > 6 and record[6] is not None:                    sharpe = float(record[6])                    result[record_year] = sharpe                    logging.debug(f"Alpha {alpha_id} {record_year}年Sharpe值: {sharpe:.4f}")                else:                    logging.warning(f"Alpha {alpha_id} {record_year}年Sharpe值为空")                if result['2021'] is None and result['2022'] is None:            logging.warning(f"Alpha {alpha_id} 未找到2021年和2022年的数据")                return result            except (json.JSONDecodeError, IndexError, KeyError) as e:        logging.error(f"解析Alpha {alpha_id} 数据失败: {str(e)}")        return result
```

---

### 评论 #9 (作者: ML42552, 时间: 1年前)

-----------------------------------------------

感谢大佬分享，

我这边尝试了这套代码还是没有办法把厂因子去掉，

不知道大佬有没有遇过这种情况

望大佬回复，谢谢！

----------------------------------------------------------------

共好！

----------------------------------------------------------------

---

### 评论 #10 (作者: JR23144, 时间: 1年前)

[ML42552](/hc/en-us/profiles/27182530443671-ML42552)  你可以把你没去掉的 厂alpha 的PNL 发出来，看一看，我这个代码用了 1个月，发现没问题才分享出来的，不知道你是哪个地方不对，我看评论区其他人应该也是都 把 厂 alpha 去除了，实在不行的话你把你的问题也可以发在学习小组中，会有人帮你看的

---

### 评论 #11 (作者: QZ67721, 时间: 1年前)

看了大佬的帖子，也看了各位群友的回复，萌新受益良多。我也努力借助AI去在本地把功能部署起来。
-------------------------------------------------------------

要是部署失败了，我再上来问
-------------------------------------------------------------

---

### 评论 #12 (作者: YZ70114, 时间: 1年前)

感谢大佬分享，后续在剪枝的过程中我也尝试把这个用起来！

=======================================================================
生活就像海洋 只有意志坚强的人 才能到达彼岸
=======================================================================

---

### 评论 #13 (作者: BJ10003, 时间: 1年前)

**若Alpha因子在一阶回测中呈现“厂Alpha”特征（PNL曲线表现特定不良模式），则后续的二阶、三阶优化或因子组合仍大概率保持该特征**

-------------------------------------------------------------

权威的解答，果然去掉了厂型的alpha
-------------------------------------------------------------

---

### 评论 #14 (作者: AL13375, 时间: 1年前)

感谢分享，很实用的一个方法和思路，我也想到一个比较可行的办法，就是调用接口

```
https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats
```

在返回的records中会显示近年来的各指标的表现，如果近几年的数值都是0的话就可以判断该alpha的走势是“厂”型的，后面就可以把这个厂alpha剔除掉了。

可以在一阶跑完之后就进行这种筛选操作，因为一阶的走势是厂型，后续大概也是这个走势，至少也是不合格的，因此在一阶跑完后进行筛选大概率是可以提升二阶的效率的。

以上的想法目前还未用代码实现，若是有不合理的地方，欢迎各位大佬指正！！！

---

### 评论 #15 (作者: DQ70916, 时间: 10个月前)

```
fo_tracker = get_alphas("06-12", "06-13", 1, 0.7, "ASI", 200, "track")我是小白，我新建py文件后运行   提示  get_alphas  这个方法未定义，请问各位大佬是否还有其他文件，还是需要自己自定义一下
```

---

### 评论 #16 (作者: JR23144, 时间: 10个月前)

[DQ70916](/hc/en-us/profiles/32067243422231-DQ70916)

你要去检查下，这个培训的代码类是否正确引入，函数在这里面，这就没有冗余展示了

```
from machine_lib import *
```

===============================================VF1.0========================================================================================================================

---

### 评论 #17 (作者: AM12075, 时间: 10个月前)

**2.  在notebook中** 修改其中筛选第一次回测完的Alpha

这个notebook在哪里呢？

===========================================================================================================================================================================================================================================

---

### 评论 #18 (作者: CY54463, 时间: 9个月前)

我用了作者的代码，在vs进行回测后。 ![图片](images/img_3c5e62f9d9.png) 并不能筛选这个alpha.

我使用mcp，ai助手进行迭代后
 ![图片](images/img_a71abbd7f5.png) 
就可以筛选出来了.
由于是ai编写的pnl.test.py文件。我看不懂代码。最核心的筛选是pnl保存同一个值1年以上就进行排除。
如下代码可以参考

import os

from dotenv import load_dotenv

import logging

import time

import requests

from machine_lib import *

class cfg:

env_path = "user.env"

load_dotenv(dotenv_path=env_path)

username = os.environ["USER_NAME"]

password = os.environ["PASSWORD"]

def sign_in(username, password):

s = requests.Session()

s.auth = (username, password)

try:

response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')

response.raise_for_status()

logging.info("Successfully signed in")

return s

except requests.exceptions.RequestException as e:

logging.error(f"Login failed: {e}")

return None

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

def check_consecutive_non_zero_values(alpha_id, data, required_streak=250):

"""

检查是否有连续required_streak天的相同非零值

特别关注PNL序列末端的稳定性，用于检测PNL最后完全稳定的Alpha

"""

if not data or len(data) < required_streak:

return True

# 提取PNL值（每个记录的第二元素）

pnl_values = []

dates = []

for row in data:

if len(row) >= 2:  # 确保有至少两个元素（日期和PNL值）

dates.append(row[0])

pnl_values.append(row[1])

else:

dates.append("未知日期")

pnl_values.append(0)  # 数据不全时假设为0

# 检查是否所有PNL值都为0

if all(v == 0 for v in pnl_values):

print(f"{alpha_id} 不合法: 所有PNL值都为0")

return False

# 特别检查序列末端的稳定性

end_streak_count = 0

end_streak_value = pnl_values[-1] if pnl_values else None

end_index = len(pnl_values) - 1

# 从末尾向前检查连续相同值的长度

for i in range(len(pnl_values)-1, -1, -1):

if pnl_values[i] == end_streak_value:

end_streak_count += 1

else:

break

# 如果末端连续相同值超过要求的天数，判断为不合法

if end_streak_count >= required_streak:

end_date = dates[-1] if dates else "未知日期"

start_stable_date = dates[-end_streak_count] if len(dates) >= end_streak_count else "未知日期"

print(f"{alpha_id} 不合法: 检测到末端连续{end_streak_count}天相同值 {end_streak_value}, 从 {start_stable_date} 到 {end_date}")

return False

# 同时检查整个序列中的连续相同值（作为附加检查）

current_streak_count = 0

current_streak_value = None

max_streak_count = 0

max_streak_value = None

for i, value in enumerate(pnl_values):

if value != 0:

if value == current_streak_value:

current_streak_count += 1

else:

current_streak_value = value

current_streak_count = 1

else:

current_streak_value = None

current_streak_count = 0

if current_streak_count > max_streak_count:

max_streak_count = current_streak_count

max_streak_value = current_streak_value

# 如果发现连续required_streak天相同非零值，立即返回不合法

if current_streak_count >= required_streak:

start_index = i - current_streak_count + 1

start_date = dates[start_index] if start_index < len(dates) else "未知日期"

end_date = dates[i] if i < len(dates) else "未知日期"

print(f"{alpha_id} 不合法: 检测到连续{current_streak_count}天相同非零值 {current_streak_value}, 从 {start_date} 到 {end_date}")

return False

print(f"{alpha_id} 通过连续非零值检查: 最大连续相同值天数为{max_streak_count}")

return True

def check_pnl_shape(alpha_id, data, min_flat_days=252, max_flat_days=504,

rise_threshold=0.05, fall_threshold=-0.05, flat_threshold=0.02):

"""

检查PNL形状：先上升后下降，然后变平持续1-2年

参数:

alpha_id: Alpha ID

data: PNL数据

min_flat_days: 最小平坦天数（1年约252个交易日）

max_flat_days: 最大平坦天数（2年约504个交易日）

rise_threshold: 上升阈值（累计收益变化百分比）

fall_threshold: 下降阈值（累计收益变化百分比）

flat_threshold: 平坦阈值（每日收益波动百分比）

"""

if not data or len(data) < 300:  # 降低数据长度要求，至少300天

print(f"{alpha_id} PNL形状检查: 数据不足 ({len(data) if data else 0}天)")

return True  # 改为返回True，不因数据不足而过滤

# 提取PNL值（第二列）

pnl_values = []

for row in data:

if len(row) >= 2:

pnl_values.append(row[1])

else:

pnl_values.append(0)

# 如果数据长度不足以进行完整形状分析，只进行基本检查

if len(pnl_values) < max_flat_days + 100:

print(f"{alpha_id} PNL形状检查: 数据长度较短 ({len(pnl_values)}天)，进行基本稳定性检查")

# 检查最后一段时间的波动性

last_100_days = pnl_values[-100:] if len(pnl_values) >= 100 else pnl_values

volatility = np.std(last_100_days) if last_100_days else 0

# 如果波动性在合理范围内，认为通过

if volatility > 100000:  # 根据实际PNL值调整阈值

print(f"{alpha_id} PNL基本检查: 波动性较高 ({volatility:.2f})")

return True

else:

print(f"{alpha_id} PNL基本检查通过: 波动性正常 ({volatility:.2f})")

return True

# 完整形状检查（针对有足够数据的Alpha）

# 提取收益数据（假设第二列是日收益）

returns = []

for row in data:

if len(row) >= 3:

returns.append(row[1])  # 假设第二列是日收益

else:

returns.append(0)

# 计算累积净值

cumulative_pnl = [1.0]

for ret in returns:

cumulative_pnl.append(cumulative_pnl[-1] * (1 + ret/100.0))  # 假设收益是百分比

# 寻找上升阶段

max_peak = 0

peak_index = 0

for i in range(1, len(cumulative_pnl)):

if cumulative_pnl[i] > max_peak:

max_peak = cumulative_pnl[i]

peak_index = i

# 检查是否有明显的上升和下降

if peak_index < 50 or peak_index > len(cumulative_pnl) - min_flat_days - 50:

print(f"{alpha_id} PNL形状不合法: 峰值位置不合适 (索引 {peak_index})")

return True  # 改为返回True，不因峰值位置而过滤

# 检查上升幅度（从开始到峰值）

rise_percent = (cumulative_pnl[peak_index] - cumulative_pnl[0]) / cumulative_pnl[0]

if rise_percent < rise_threshold:

print(f"{alpha_id} PNL形状不合法: 上升幅度不足 {rise_percent:.2%} < {rise_threshold:.0%}")

return True  # 改为返回True，不因上升幅度而过滤

# 检查下降幅度（从峰值到某个点）

min_valley = cumulative_pnl[peak_index]

valley_index = peak_index

for i in range(peak_index, len(cumulative_pnl)):

if cumulative_pnl[i] < min_valley:

min_valley = cumulative_pnl[i]

valley_index = i

fall_percent = (cumulative_pnl[valley_index] - cumulative_pnl[peak_index]) / cumulative_pnl[peak_index]

if fall_percent > fall_threshold:

print(f"{alpha_id} PNL形状不合法: 下降幅度不足 {fall_percent:.2%} > {fall_threshold:.0%}")

return True  # 改为返回True，不因下降幅度而过滤

# 检查平坦阶段（从谷底开始）

if valley_index > len(cumulative_pnl) - min_flat_days:

print(f"{alpha_id} PNL形状不合法: 没有足够的平坦数据")

return True  # 改为返回True，不因平坦数据不足而过滤

# 检查平坦阶段的波动性

flat_returns = returns[valley_index:]

if len(flat_returns) < min_flat_days:

print(f"{alpha_id} PNL形状不合法: 平坦阶段数据不足")

return True  # 改为返回True，不因平坦阶段数据不足而过滤

# 计算平坦阶段的波动率

flat_volatility = np.std(flat_returns[:min_flat_days]) if len(flat_returns) >= min_flat_days else np.std(flat_returns)

if flat_volatility > flat_threshold:

print(f"{alpha_id} PNL形状不合法: 平坦阶段波动太大 {flat_volatility:.4f} > {flat_threshold:.4f}")

return True  # 改为返回True，不因波动太大而过滤

# 检查平坦阶段的持续时间（1-2年）

flat_duration = min(len(flat_returns), max_flat_days)

if flat_duration < min_flat_days:

print(f"{alpha_id} PNL形状不合法: 平坦持续时间不足")

return True  # 改为返回True，不因平坦持续时间不足而过滤

print(f"{alpha_id} PNL形状通过: 上升{rise_percent:.2%}, 下降{fall_percent:.2%}, 平坦{flat_duration}天")

return True

def get_alpha_pnl_legal(alpha_id: str) -> bool:

pnl = wait_get(" [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id + "/recordsets/pnl").json()

records = pnl["records"]

# 同时检查连续非零值和PNL形状

consecutive_check = check_consecutive_non_zero_values(alpha_id, records)

shape_check = check_pnl_shape(alpha_id, records)

return consecutive_check and shape_check

def get_alpha_pnl_legal_list(fo_tracker: list) -> list:

global sess

sess = sign_in(cfg.username, cfg.password)

fo_tracker =[fo for fo in fo_tracker if get_alpha_pnl_legal(fo[0])]

return fo_tracker

sess = sign_in(cfg.username, cfg.password)

# 添加numpy导入

import numpy as np

---

### 评论 #19 (作者: HJ88260, 时间: 9个月前)

JR大佬这个分享太及时了！很多人在做Alpha回测的时候，确实会忽略PNL形态的合法性，尤其是一阶Alpha如果本身是‘厂’型走势，后面再怎么组合优化基本也是白给——你这发现简直真理，早过滤早省心。

代码写得也很贴心，开箱即用，两步集成根本没啥门槛。特别是用  `check_consecutive_non_zero_values`  这类逻辑去捕捉连续异常信号，比单纯看夏普或者收益靠谱多了，能有效避免过度拟合和无效算力浪费。Retry-After 和 Session 管理这些小细节也处理得挺稳，明显是踩过坑的😂。

我现在做批量回测也习惯在第一步加这种合法性检查，相当于给Alpha池提前做一遍‘质检’，筛掉瑕疵品再往下走，效率高太多了。建议用的人多的团队甚至可以把这个步骤做到自动化流水线里，配合notebook调度，简直Day Day Alpha神器。

谢谢分享，已点赞收藏，期待更多这种能落地的干货！

---

### 评论 #20 (作者: YZ59361, 时间: 9个月前)

大佬分享确实是好东西！而且思路不止是能筛选厂字型alpha，同时很多pnl直线的异常alpha值也可以筛一筛提高回测效率。

另有一点问题，请教下大佬，代码中是拉去了pnl以及risk两条线的数据，是否也可以简化一点仅拉取pnl数据就行了，risk数据主要是出于什么考虑呢？没啥金融知识，纯粹好奇

---

### 评论 #21 (作者: AL96309, 时间: 8个月前)

谢谢大佬，代码畅通，能够准确识别出厂字alpha。我想请教一下，如果我想把厂字alpha隐藏或者删除应该怎么做呢？目前我还处于交ppac的阶段，只能手动去加description提交，要是能把厂字alpha都隐藏会省事很多~

---

### 评论 #22 (作者: YH87796, 时间: 8个月前)

=================================================================================

感谢大佬提供的代码，终于可以剔除掉厂字了。不然太浪费二阶回测字段了

==================================================================================

---

### 评论 #23 (作者: WW61680, 时间: 8个月前)

这个接口支持并发吗，还是只能串行的方式去获取

```
https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats
```

---

### 评论 #24 (作者: JW12369, 时间: 6个月前)

本了想发一篇，看到这里已经有了，我把现在用的也贴一个代码。

首先看下输出效果：

```
{'is_valid': False,  'confidence': 0.0,  'issues':  ['数据年份不足: 2年',   '负收益年份过多: 50.0%',   '正收益年份偏 少: 50.0%',   'Sharpe比率偏低: 0.09',   '零值数据过多: 10/12年'],  'metrics':  {'total_years': 12, 'data_years': 2, 'positive_years': 1, 'negative_years': 1, 'zero_years': 10, 'avg_sharpe': np.float64(0.08500000000000002), 'max_drawdown': 0.0248, 'total_pnl': 334234.0, 'avg_return': np.float64(-0.026150000000000003)}}
```

其中最重要的is_valid表示是否有效，confidence表示得分的衡量， 0表示完全没意义， 1表示有价值。

issues是其中的问题。

这里就可以自行决定直接采用is_valid，还是看一下其他问题再决定。

代码如下（输入就是yearly-stats接口的响应结果json）

import numpy as np

def validate_yearly_curve(json_data):

"""

验证年度数据曲线是否正常

Args:

json_data: 包含年度数据的JSON对象

Returns:

Dict: 包含验证结果的字典

{

'is_valid': bool,          # 曲线是否正常

'confidence': float,       # 置信度 (0-1)

'issues': List[str],       # 问题列表

'metrics': Dict[str, float] # 关键指标

}

"""

# 提取数据

records = json_data.get('records', [])

if not records:

return {

'is_valid': False,

'confidence': 0.0,

'issues': ['无数据记录'],

'metrics': {}

}

# 解析数据

years = [int(r[0]) for r in records]

pnl_values = [float(r[1]) for r in records]

sharpe_values = [float(r[6]) for r in records]

returns_values = [float(r[7]) for r in records]

drawdown_values = [float(r[8]) for r in records]

stages = [r[11] for r in records]

# 计算关键指标

data_years = sum(1 for p in pnl_values if p != 0)

positive_years = sum(1 for p in pnl_values if p > 0)

negative_years = sum(1 for p in pnl_values if p < 0)

zero_years = sum(1 for p in pnl_values if p == 0)

valid_sharpe = [s for s in sharpe_values if s != 0]

valid_pnl = [p for p in pnl_values if p != 0]

valid_returns = [r for r in returns_values if r != 0]

avg_sharpe = np.mean(valid_sharpe) if valid_sharpe else 0

max_drawdown = max(drawdown_values) if drawdown_values else 0

total_pnl = sum(pnl_values)

avg_return = np.mean(valid_returns) if valid_returns else 0

# 验证规则

issues = []

score = 100  # 初始分数

# 1. 数据完整性检查

if data_years < 3:

issues.append(f"数据年份不足: {data_years}年")

score -= 30

# 2. 负收益年份检查

if data_years > 0:

negative_ratio = negative_years / data_years

if negative_ratio > 0.3:

issues.append(f"负收益年份过多: {negative_ratio:.1%}")

score -= 25

elif negative_ratio > 0.1:

score -= 10

# 3. 正收益年份检查

if data_years > 0:

positive_ratio = positive_years / data_years

if positive_ratio < 0.6:

issues.append(f"正收益年份偏少: {positive_ratio:.1%}")

score -= 20

# 4. Sharpe比率检查

if avg_sharpe < 0.5:

issues.append(f"Sharpe比率偏低: {avg_sharpe:.2f}")

score -= 15

elif avg_sharpe < 1.0:

score -= 5

# 5. 最大回撤检查

if max_drawdown > 0.15:

issues.append(f"最大回撤较大: {max_drawdown:.1%}")

score -= 10

# 6. 零值数据检查

if zero_years > len(years) * 0.5:

issues.append(f"零值数据过多: {zero_years}/{len(years)}年")

score -= 20

# 计算置信度

confidence = max(0.0, min(1.0, score / 100.0))

is_valid = len(issues) == 0 and confidence >= 0.7

return {

'is_valid': is_valid,

'confidence': confidence,

'issues': issues,

'metrics': {

'total_years': len(years),

'data_years': data_years,

'positive_years': positive_years,

'negative_years': negative_years,

'zero_years': zero_years,

'avg_sharpe': avg_sharpe,

'max_drawdown': max_drawdown,

'total_pnl': total_pnl,

'avg_return': avg_return

}

}

---

### 评论 #25 (作者: HY20507, 时间: 4个月前)

感谢大佬，提前剔除对于现在每天回测次数有限制的情况有巨大帮助

---

