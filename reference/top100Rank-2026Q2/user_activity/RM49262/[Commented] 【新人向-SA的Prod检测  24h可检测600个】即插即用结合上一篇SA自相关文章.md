# 【新人向-SA的Prod检测 —— 24h可检测600个！】即插即用！结合上一篇SA自相关文章！

- **链接**: [Commented] 【新人向-SA的Prod检测  24h可检测600个】即插即用结合上一篇SA自相关文章.md
- **作者**: LX57490
- **发布时间/热度**: 5个月前, 得票: 109

## 帖子正文

### **本帖子展示了如何将前辈 [SY86571](/hc/zh-cn/profiles/30781531875223-SY86571) 的优雅避免prod检测受到限流处理及上一篇自相关检测的输出结果进行合二为一的SA-Prod检测代码！**

**一、登录及其配置参数**

1.  40，41行输入账号密码；

2.  38行更改时间，依据于上一篇自相关代码跑出来的文件时间；

3.  42行 **“**  **SELF_CORR_THRESHOLD = 0.58”** ，

三五可以改为0.5，0.5更容易出货；

二五可以改为0.58，以及查看各个alpha的其他指标来决定交不交！

阈值灵感来源游戏王大佬 [ZS59763](/hc/en-us/profiles/26858512793111-ZS59763) ！

**![图片](images/img_1e354b0724.png)**

**二、断点重连机制**

1.输入y，跳过之前检测成功的并继续监测！

![图片](images/img_986f0ca134.png)

2. 输入n，开始新监测，并生成新的中间文件供你在prod没检测完提前选择！

中间文件命名方式：partial_results_20260109_174340.csv

![图片](images/img_d455a5fd88.png)  ![图片](images/img_7596ed6d6b.png)

限流处理，每小时测试25个SA的prod后就休息半小时！

25*24=600 SA！！！！

以上都是一个基本框架，大家可以根据自己的流程进行改代码！！！！

#### 三、完整代码：

**最后祝各位顾问月月VF1.0！RA60刀！SA60！日日120刀！！！！**

**高筑墙！广积粮！缓称王！**

import requests

import time

import threading

import logging

import pandas as pd

import os

import random

import json

import signal

import datetime

import traceback

from urllib3.util.retry import Retry

from requests.adapters import HTTPAdapter

import base64

import urllib3

from typing import List, Dict, Optional

# 禁用SSL警告

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置日志

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 全局变量用于存储Prod Correlation请求的限流状态

prod_corr_remaining = 60

prod_corr_reset_time = time.time() + 60

prod_corr_lock = threading.Lock()

# 全局变量

SESSION_REFRESH_INTERVAL = 3600  # 3.5小时

last_auth_time = time.time()

# 全局变量用于存储部分结果

partial_results = []

partial_file_path = ""

# ===== 配置参数 - 只需修改这里 =====

START_DATE = "01-01"  # 起始日期（MM-DD格式）

REGION = "EUR"  # 区域

USERNAME = ""

PASSWORD = ""

SELF_CORR_THRESHOLD = 0.58  # 自相关阈值，只处理小于此值的Alpha

# ================================

# 获取当前脚本所在目录

script_dir = os.path.dirname(os.path.abspath(__file__))

# 输入文件路径

INPUT_FILE = os.path.join(script_dir, f"Superalpha_results_{START_DATE}_{REGION}.xlsx")

# 输出文件路径（与代码同目录）

OUTPUT_FILE = os.path.join(script_dir, f"Superalpha_prod_correlation_results_{START_DATE}_{REGION}.xlsx")

def create_session():

"""创建带有重试机制的会话"""

session = requests.Session()

retry_strategy = Retry(

total=5,

backoff_factor=1,

status_forcelist=[429, 500, 502, 503, 504],

allowed_methods=["GET", "POST"]

)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)

session.mount("http://", adapter)

return session

def save_partial_results():

"""保存当前获取的部分结果"""

if not partial_results:

return

global partial_file_path

if not partial_file_path:

# 生成带时间戳的文件名

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

partial_file_path = f"partial_results_{timestamp}.csv"

try:

# 使用CSV格式保存

df = pd.DataFrame(partial_results)

df.to_csv(partial_file_path, index=False)

logging.info(f"已保存部分结果到: {partial_file_path}")

except Exception as e:

logging.error(f"保存部分结果失败: {e}")

def handle_interrupt(signum, frame):

"""处理中断信号"""

logging.warning("检测到程序中断，正在保存当前结果...")

save_partial_results()

logging.info("部分结果已保存，程序退出")

os._exit(1)  # 立即退出程序

def load_partial_results(file_path: str) -> List[Dict]:

"""加载部分结果文件"""

try:

df = pd.read_csv(file_path)

logging.info(f"从部分结果文件加载了 {len(df)} 条记录")

return df.to_dict('records')

except Exception as e:

logging.error(f"加载部分结果失败: {e}")

return []

def ensure_session_valid(session, last_auth_time):

"""确保会话有效，如果超过刷新间隔则重新登录"""

current_time = time.time()

if current_time - last_auth_time > SESSION_REFRESH_INTERVAL:

logging.info("会话已超过3.5小时，正在刷新...")

try:

# 尝试删除现有认证

session.delete(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')

except:

pass  # 忽略删除错误

# 重新登录

new_session = sign_in()

logging.info("会话刷新成功")

return new_session, current_time

return session, last_auth_time

def sign_in() -> Optional[requests.Session]:

"""登录WorldQuant Brain平台"""

session = create_session()

try:

# 构造认证字符串

auth_str = f"{USERNAME}:{PASSWORD}"

# 转换为字节并Base64编码

auth_bytes = auth_str.encode('utf-8')

base64_bytes = base64.b64encode(auth_bytes)

base64_str = base64_bytes.decode('utf-8')

headers = {

"Authorization": f"Basic {base64_str}",

"Content-Type": "application/json"

}

# 发送认证请求

response = session.post(

' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ',

headers=headers,

verify=False  # 禁用SSL验证

)

# 检查响应状态

if response.status_code in [200, 201]:

user_id = response.json().get('user', {}).get('id', '未知用户')

logging.info(f"登录成功: 用户ID {user_id}")

return session

else:

logging.error(f"登录失败: 状态码 {response.status_code}, 响应: {response.text[:200]}")

return None

except Exception as e:

logging.error(f"登录过程中发生错误: {e}")

return None

def safe_get_error_detail(response):

"""安全获取错误详情，处理各种响应格式"""

try:

content = response.json()

if "detail" in content:

return content["detail"]

if "error" in content:

return content["error"]

if "message" in content:

return content["message"]

return json.dumps(content, indent=2)

except json.JSONDecodeError:

if "text/html" in response.headers.get("Content-Type", ""):

return "HTML响应: " + response.text[:500] + "..."

return response.text if response.text else '无错误详情'

def calculate_retry_delay(attempt, max_retries, error_type=None):

"""智能计算重试延迟时间，使用指数退避+抖动策略"""

base_delay = 1.0

if error_type == 'rate_limit':

base_delay = 5.0

elif error_type == 'client_error':

base_delay = 2.0

elif error_type == 'server_error':

base_delay = 3.0

delay = base_delay * (2 ** min(attempt, 8))

jitter = random.uniform(0.5, 1.5)

delay *= jitter

return min(delay, 60.0)

def get_prod_correlation_max(session: requests.Session, alpha_id: str, max_retries: int = 5) -> Optional[float]:

global prod_corr_remaining, prod_corr_reset_time, last_auth_time

# 确保会话有效

session, last_auth_time = ensure_session_valid(session, last_auth_time)

url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod](https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod) "

retries = 0

empty_retries = 0

max_empty_retries = 10

base_wait = 20.0  # 基础等待时间设为20秒

while retries < max_retries:

# 检查限流状态

with prod_corr_lock:

current_time = time.time()

if prod_corr_remaining <= 3 and prod_corr_reset_time > current_time:

wait_time = max(3, prod_corr_reset_time - current_time)

logging.info(f"等待限流重置: {wait_time:.1f}秒 (剩余次数: {prod_corr_remaining})")

time.sleep(wait_time)

try:

# 发送请求

resp = session.get(url, timeout=(15, 60))  # 增加超时时间

# 处理200响应

if resp.status_code == 200:

# 更新限流状态

with prod_corr_lock:

try:

remaining_str = resp.headers.get("Ratelimit-Remaining", "60")

reset_str = resp.headers.get("Ratelimit-Reset", "60")

prod_corr_remaining = int(remaining_str.split('.')[0])

reset_seconds = float(resp.headers.get("Ratelimit-Reset", "60"))

prod_corr_reset_time = current_time + reset_seconds

except Exception as e:

logging.warning(f"解析限流头部失败: {e}")

# 处理空响应

if not resp.content:

# 使用固定步长的增长策略，避免等待时间失控

if base_wait >= 120.0:  # 达到上限后不再增加

current_wait = 120.0

else:

current_wait = min(base_wait * (1 + empty_retries * 0.3), 120.0)

# 根据限流情况智能调整等待时间

with prod_corr_lock:

if prod_corr_remaining < 5 and prod_corr_reset_time > time.time():

time_gap = prod_corr_reset_time - time.time()

if 0 < time_gap < 120:

current_wait = max(current_wait, time_gap + 5)  # 确保覆盖重置时间

else:

current_wait = min(current_wait, 5)  # 如果重置时间较远，适度缩短等待

logging.warning(f"空响应，等待 {current_wait:.1f}秒 (空响应重试: {empty_retries + 1}/{max_empty_retries})")

time.sleep(current_wait)

base_wait = current_wait  # 更新基础等待时间

empty_retries += 1

if empty_retries >= max_empty_retries:

logging.error(f"达到最大空响应重试次数 {max_empty_retries}")

return None

continue

# 解析JSON响应

try:

data = resp.json()

return float(data.get("max", 0))

except ValueError:

logging.error(f"JSON解析失败: {resp.text[:100]}...")

return None

# 处理401未授权错误

elif resp.status_code == 401:

logging.warning("会话过期，尝试重新登录...")

session = sign_in()

last_auth_time = time.time()

continue  # 不消耗重试次数

# 处理429限流错误

elif resp.status_code == 429:

retry_after = float(resp.headers.get("Retry-After", "70"))

logging.warning(f"429限流，等待 {retry_after}秒")

time.sleep(retry_after)

continue  # 不消耗重试次数

# 处理400客户端错误

elif resp.status_code == 400:

error_detail = safe_get_error_detail(resp)

logging.error(f"400客户端错误: {error_detail}")

return None  # 不重试

# 处理5xx服务器错误

elif 500 <= resp.status_code < 600:

wait_time = calculate_retry_delay(retries, max_retries, 'server_error')

logging.error(f"服务器错误({resp.status_code})，等待 {wait_time:.2f}秒")

time.sleep(wait_time)

retries += 1

continue

# 其他错误

else:

error_detail = safe_get_error_detail(resp)

logging.error(f"错误状态: {resp.status_code}, 详情: {error_detail}")

return None

# 处理网络错误

except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:

wait_time = calculate_retry_delay(retries, max_retries)

logging.error(f"网络错误({type(e).__name__})，等待 {wait_time:.2f}秒")

time.sleep(wait_time)

retries += 1

except requests.exceptions.RequestException as e:

wait_time = calculate_retry_delay(retries, max_retries)

logging.error(f"请求异常: {e}，等待 {wait_time:.2f}秒")

time.sleep(wait_time)

retries += 1

except Exception as e:

logging.error(f"未知错误: {e}")

traceback.print_exc()

retries += 1

logging.error(f"超过最大重试次数 {max_retries}")

return None

def read_and_filter_data(file_path: str) -> pd.DataFrame:

"""从Excel文件中读取数据并应用自相关过滤"""

try:

if not os.path.exists(file_path):

logging.error(f"文件不存在: {file_path}")

return pd.DataFrame()

# 读取Excel文件

df = pd.read_excel(file_path)

# 检查必要列是否存在

if 'alpha_id' not in df.columns:

logging.error("文件缺少alpha_id列")

return pd.DataFrame()

# 检查自相关列是否存在

if 'self_correlation' not in df.columns:

logging.error("文件缺少self_correlation列，无法过滤")

return pd.DataFrame()

# 应用自相关过滤

original_count = len(df)

df = df[df['self_correlation'] < SELF_CORR_THRESHOLD]

filtered_count = len(df)

logging.info(f"从 {file_path} 中读取到 {original_count} 条记录")

logging.info(f"应用自相关过滤 (阈值: {SELF_CORR_THRESHOLD})，保留 {filtered_count} 条记录")

return df

except Exception as e:

logging.error(f"读取文件失败: {e}")

return pd.DataFrame()

def process_alpha_ids(session: requests.Session, df: pd.DataFrame):

"""处理DataFrame中的alpha_id，获取每个的max值并保存到文件"""

global partial_results, partial_file_path

# 注册中断信号处理

signal.signal(signal.SIGINT, handle_interrupt)

# 检查是否存在部分结果文件

partial_files = [f for f in os.listdir() if f.startswith("partial_results_") and f.endswith(".csv")]

if partial_files:

logging.info(f"检测到部分结果文件: {partial_files[0]}")

response = input("是否从部分结果文件继续处理? (y/n): ").strip().lower()

if response == 'y':

partial_file_path = partial_files[0]

partial_df = pd.read_csv(partial_file_path)

# 合并部分结果

df = df.merge(partial_df[['alpha_id', 'prod_correlation_max']],

on='alpha_id', how='left', suffixes=('', '_partial'))

# 获取已处理的alpha_id

processed_ids = set(partial_df['alpha_id'])

logging.info(f"跳过 {len(processed_ids)} 个已处理的alpha_id")

else:

# 添加空列用于存储结果

df['prod_correlation_max'] = None

# 如果没有部分结果，添加空列

if 'prod_correlation_max' not in df.columns:

df['prod_correlation_max'] = None

# 获取需要处理的alpha_id

to_process = df[df['prod_correlation_max'].isna()]

total = len(to_process)

if total == 0:

logging.info("所有alpha_id已处理完成，无需额外处理")

save_results(df)

return

# 批次处理配置

PER_BATCH_COUNT = 25  # 每批处理的Alpha数量

BREAK_DURATION = 1800  # 30分钟休息时间（秒）

batch_start_time = time.time()  # 记录批次开始时间

processed_in_batch = 0  # 当前批次计数

logging.info(f"开始处理 {total} 个alpha_id... (每{PER_BATCH_COUNT}个为一组)")

print("提示: 按Ctrl+C可中断程序并自动保存当前结果")

success_count = 0

failure_count = 0

batch_number = 1  # 当前批次编号

for i, row in to_process.iterrows():

alpha_id = row['alpha_id']

self_corr = row.get('self_correlation', 'N/A')

logging.info(f"处理 {i + 1}/{total}: {alpha_id} (自相关: {self_corr:.4f})")

max_value = get_prod_correlation_max(session, alpha_id)

if max_value is not None:

df.at[i, 'prod_correlation_max'] = max_value

logging.info(f"成功获取 {alpha_id} 的max值: {max_value:.4f}")

success_count += 1

else:

df.at[i, 'prod_correlation_max'] = -1  # 标记失败

logging.warning(f"获取 {alpha_id} 的max值失败")

failure_count += 1

# 每处理1个alpha_id保存一次部分结果

partial_results = df[['alpha_id', 'prod_correlation_max']].to_dict('records')

save_partial_results()

# 每处理1个打印批次状态（新增批次信息）

with prod_corr_lock:

remaining_time = max(0, prod_corr_reset_time - time.time())

batch_elapsed = time.time() - batch_start_time

logging.info(

f"进度: {i + 1}/{total} | 批处理: {processed_in_batch + 1}/{PER_BATCH_COUNT} (已用: {batch_elapsed:.0f}s)" +

f" | 成功: {success_count} | 失败: {failure_count} | API剩余: {prod_corr_remaining} | 重置: {remaining_time:.1f}秒后")

# 更新批次计数器

processed_in_batch += 1

# 检查是否完成一个批次

if processed_in_batch >= PER_BATCH_COUNT:

batch_end_time = time.time()

batch_duration = batch_end_time - batch_start_time

# 计算批次实际处理时间，确保整批处理不超过1小时

if batch_duration < 3600:  # 3600秒=1小时

remaining_time = 3600 - batch_duration

logging.info(f"已完成批次 #{batch_number} ({PER_BATCH_COUNT}个Alpha)")

logging.info(f"批次耗时: {batch_duration:.2f}秒, 剩余时间: {remaining_time:.2f}秒")

logging.info(f"休息 {BREAK_DURATION//60} 分钟后继续...")

time.sleep(max(remaining_time, BREAK_DURATION))  # 确保休息不少于30分钟

else:

logging.info(f"已完成批次 #{batch_number} ({PER_BATCH_COUNT}个Alpha), 耗时: {batch_duration:.2f}秒")

logging.info(f"休息 {BREAK_DURATION//60} 分钟后继续...")

time.sleep(BREAK_DURATION)

# 重置批次计数器

batch_number += 1

processed_in_batch = 0

batch_start_time = time.time()

# 处理完成后删除部分结果文件

if partial_file_path and os.path.exists(partial_file_path):

try:

os.remove(partial_file_path)

logging.info(f"已删除部分结果文件: {partial_file_path}")

except Exception as e:

logging.error(f"删除部分结果文件失败: {e}")

# 保存最终结果

save_results(df)

def save_results(df: pd.DataFrame):

"""保存结果到文件"""

try:

# 保存为Excel

df.to_excel(OUTPUT_FILE, index=False)

logging.info(f"结果已保存到Excel文件: {OUTPUT_FILE}")

# 打印统计信息

if 'prod_correlation_max' in df.columns:

valid_results = df[df['prod_correlation_max'] >= 0]

if not valid_results.empty:

print("\nProd相关性统计:")

print(f"平均Prod相关性: {valid_results['prod_correlation_max'].mean():.4f}")

print(f"最低Prod相关性: {valid_results['prod_correlation_max'].min():.4f}")

print(f"最高Prod相关性: {valid_results['prod_correlation_max'].max():.4f}")

# 找出Prod相关性最低的5个Alpha

low_prod = valid_results.nsmallest(5, 'prod_correlation_max')

print("\nProd相关性最低的5个Alpha:")

print(low_prod[['alpha_id', 'self_correlation', 'prod_correlation_max']].to_string(index=False))

except Exception as e:

logging.error(f"保存结果失败: {e}")

# 主程序

if __name__ == "__main__":

# 打印配置信息

print(f"开始处理: {START_DATE} - {REGION}")

print(f"自相关阈值: {SELF_CORR_THRESHOLD}")

print(f"输入文件: {INPUT_FILE}")

print(f"输出文件: {OUTPUT_FILE}")

# 登录

print("尝试登录...")

session = sign_in()

if session is None:

print("登录失败，请检查用户名和密码")

exit(1)

# 从文件读取数据并应用自相关过滤

df = read_and_filter_data(INPUT_FILE)

if df.empty:

print(f"未从 {INPUT_FILE} 中找到有效数据")

exit(1)

# 处理alpha_id列表

print(f"\n开始处理 {len(df)} 个alpha_id...")

print("提示: 按Ctrl+C可中断程序并自动保存当前结果")

process_alpha_ids(session, df)

# 打印最终限流状态

with prod_corr_lock:

remaining_time = max(0, prod_corr_reset_time - time.time())

print(f"\n处理完成! 结果已保存到 {OUTPUT_FILE}")

print(f"最终状态: 剩余查询次数 {prod_corr_remaining}, 重置时间 {remaining_time:.2f} 秒后")

---

## 讨论与评论 (5)

### 评论 #1 (作者: RM49262, 时间: 5个月前)

=====================================评论区=========================================

感谢尼克大佬分享 ！  新人向内容都很有用

再多发几个可以搞成合集了

===================================================================================

---

### 评论 #2 (作者: TS96358, 时间: 5个月前)

=====================早日冲上GrandMaster============================================== 大佬，我想问一下 “38行更改时间，依据于上一篇自相关代码跑出来的文件时间；”,我去看了一下上一篇文章，是对RA进行检测呀，可是这篇文章是对SA的PC检测，请问是如何联系在一起的那？ 祝佬早日登上GM宝座！！！ ==================纸上得来终觉浅，绝知此事要躬行========================================

---

### 评论 #3 (作者: LX57490, 时间: 5个月前)

@ [TS96358](/hc/zh-cn/profiles/29178862756887-TS96358)   上一篇RA帖子还没有审核通过，悲！他比SA PC的早，但是SA PC的先发出来了！耐心等待审核通过吧！

---

### 评论 #4 (作者: XE68375, 时间: 4个月前)

请问是不是改下SA的各项阈值，改成RA的，是不是就可以检测RA的自相关

---

### 评论 #5 (作者: LX57490, 时间: 4个月前)

**@ [XE68375](/hc/zh-cn/profiles/36884435614743-XE68375) 不是 你需要进我的ID找其他三篇帖子，才能使用这个代码！**

**要现有本地sc的csv文件 才能进行PC检测，然后RA SA都有代码，你只需要自己复制更改时间就行了！**

---

