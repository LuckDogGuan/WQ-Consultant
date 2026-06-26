# 快速过滤掉含有FAIL项的Alpha

- **链接**: [Commented] 快速过滤掉含有FAIL项的Alpha.md
- **作者**: LJ64268
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

我们通过get_alpha筛选出sharpe和fitness合格alpha_id后进行check_submission速度会很慢，我的脚本是在check_submission之前，先把alpha_id进行一次筛选，过滤掉含有FAIL项的alpha_id。这样可以减少check_submission的数量，从而提升一些效率，这样在check_submission时只剩下了需要检查相关性的alpha_id。当然了，如果对提交alpha要求更高的，可以加上WARNING过滤。无论你是否参加了比赛，没有WARNING的alpha在提交时都会有更好的效果。以下是具体实现的代码，我是把get_alpha获取的alpha_id存入了csv文件，然后从文件中读取来进行筛选的，嫌麻烦的可以去掉这部分；最后合格的alpha_id也是写入csv文件，并且按照Sharpe从大到小排序。

注：一次100个并发，速度非常快。

import datetime

import os

import time

import requests

import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from threading import Lock

from machine_lib import*

pd.set_option('expand_frame_repr', False)

pd.set_option('display.max_rows', 1000)

pd.set_option('display.max_colwidth', 100)

# 定义全局计数器

written_count = 0

# 用于收集检查通过的alpha_id及其HARPE值

valid_alphas = {}

# 创建线程锁

valid_alphas_lock = Lock()

written_count_lock = Lock()

# 每200个检查后重新登录

CHECK_BATCH_SIZE = 200

REQUEST_TIMEOUT = 10

# 用于收集检查失败的alpha_id

failed_alphas = []

failed_alphas_lock = Lock()

def submit_alpha(s, alpha_id):

global written_count

submit_url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}](https://api.worldquantbrain.com/alphas/{alpha_id}) "

attempts = 0

while attempts < 5:

attempts += 1

print(f"Attempt {attempts} to submit {alpha_id}.")

while True:

try:

res = s.get(submit_url, timeout=REQUEST_TIMEOUT, headers={'Connection': 'close'})

if "retry - after" in res.headers:

time.sleep(float(res.headers["Retry - After"]))

continue

except requests.RequestException as e:

print(f"请求 {submit_url} 时出现网络异常: {e}")

time.sleep(3)

continue

try:

data = res.json()["is"]["checks"]

df = pd.DataFrame(data)

columns_to_display = ['name', 'value','result']

valid_columns = [col for col in columns_to_display if col in df.columns]

if not valid_columns:

print("没有可用的列进行显示。")

else:

print(df[valid_columns])

if'result' in df.columns:

if (df['result']!= 'FAIL').all():

# 提取LOW_FITNESS的value

low_fitness_row = df[df['name'] == 'LOW_SHARPE']

if not low_fitness_row.empty:

low_fitness_value = low_fitness_row['value'].values[0]

with valid_alphas_lock:

valid_alphas[alpha_id] = low_fitness_value

with written_count_lock:

written_count += 1

else:

# 新增失败记录

with failed_alphas_lock:

failed_alphas.append(alpha_id)

except (KeyError, ValueError):

print("解析响应JSON数据时出现错误。")

return res.status_code

return 404

if __name__ == '__main__':

s = login()

# 读取CSV文件获取alpha_id列表

csv_file_path = r"D:\WorldQuant\xxx.csv"

try:

df = pd.read_csv(csv_file_path, header=None)

if 'alpha_id' in df.columns:

submittable_alphas = df['alpha_id'].tolist()

else:

submittable_alphas = df.iloc[:, 0].tolist()

except FileNotFoundError:

print(f"未找到文件: {csv_file_path}")

import sys

sys.exit(1)

# 最多并发100个请求

max_workers = 100

total_alphas = len(submittable_alphas)

for i in range(0, total_alphas, CHECK_BATCH_SIZE):

batch_alphas = submittable_alphas[i:i + CHECK_BATCH_SIZE]

with ThreadPoolExecutor(max_workers=max_workers) as executor:

futures = []

for alpha_id in batch_alphas:

future = executor.submit(submit_alpha, s, alpha_id)

futures.append(future)

for future in futures:

status_code = future.result()

if status_code == 404:

alpha_id = batch_alphas[futures.index(future)]

print(f"跳过 {alpha_id}，继续处理下一个Alpha ID。")

if i + CHECK_BATCH_SIZE < total_alphas:

print("完成当前批次检查，重新登录...")

# 关闭当前会话

time.sleep(1)

s.close()

time.sleep(1)

s = login()

# 关闭最后一个会话

s.close()

# 获取北京时间当天日期

beijing_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = 8)))

date_str = beijing_time.strftime("%Y%m%d")

csv_filename = f"xxx{date_str}.csv"

folder_path = r"D:\WorldQuant"

csv_path = os.path.join(folder_path, csv_filename)

# 检查文件夹是否存在，不存在则创建

if not os.path.exists(folder_path):

os.makedirs(folder_path)

# 对valid_alphas按照SHARPE值从大到小排序

sorted_alphas = sorted(valid_alphas.items(), key = lambda item: item[1], reverse = True)

sorted_alpha_ids = [alpha_id for alpha_id, _ in sorted_alphas]

# 将排序后的alpha_id统一写入文件，使用 'w' 模式覆盖写入

with open(csv_path, 'w', newline='') as f:

for alpha_id in sorted_alpha_ids:

f.write(alpha_id + '\n')

# 打印统计信息（新增失败数量显示）

print(f"检查通过的alpha_id共 {written_count} 个，失败的共 {len(failed_alphas)} 个。")

---

## 讨论与评论 (3)

### 评论 #1 (作者: BW14163, 时间: 1年前)

感谢分享，待会就拿去试试，先给你点个赞

---

### 评论 #2 (作者: ZS59763, 时间: 1年前)

很有意思的修改，感谢你的分享，有一点小小的建议，保存下来的csv可以做成增量的形式，如果已经在csv里里面就跳过，不在则加入，这样能进一步缩小范围

---

### 评论 #3 (作者: MY65447, 时间: 2个月前)

拜读了此文，收获满满，启发良多，深感学无止境。非常感谢大佬的分享！

==============================================================

Keep going every day, and you will surely reap greater rewards

==============================================================

---

