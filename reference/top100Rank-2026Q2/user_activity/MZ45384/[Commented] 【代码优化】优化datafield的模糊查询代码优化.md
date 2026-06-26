# 【代码优化】优化datafield的模糊查询代码优化

- **链接**: [Commented] 【代码优化】优化datafield的模糊查询代码优化.md
- **作者**: QF72678
- **发布时间/热度**: 5个月前, 得票: 2

## 帖子正文

我们往往需要使用模糊查询功能查询出含义或者描述符合要求的数据字段， 但是平台目前限制了模糊查询的记录返回数，以查询"volume"为例：

![图片](images/img_ebc597443d.png) 只会返回符合要求的前100条， 而如果我们检查api的返回结果，会发现count为3528。

在模板构建或者初筛阶段，我们可能需要获取符合查询条件的所有datafield，作为模板引擎的输入。我们可以用变通的方式来实现这一目标， 先获取所有的dataset，然后在每个dataset里面查询datafield。 代码如下（基于wqb库）：

首先登录：

import wqb

import time

logger = wqb.wqb_logger()

wqbs = wqb.WQBSession(("your email", "your password"), logger=logger)

# 配置参数

CONFIG = {

'region': 'IND',  # 'USA'

'delay': 1,  # 1, 0

'universe': 'TOP500',  # 'TOP3000'

'search': '',  # 搜索关键字，为空时获取所有字段

'type': 'MATRIX',

'page_size': 100,  # 每页记录数（世坤平台最大限制）

'request_delay': 0.5,  # 请求间隔(秒)

'max_retries': 3,  # 最大重试次数

'retry_delay': 2,  # 重试延迟(秒)

}

然后获取所有的dataset

# 分页获取所有datasets的函数

def get_all_datasets():

"""获取所有符合region, delay, universe条件的datasets"""

datasets = []

limit = CONFIG['page_size']

offset = 0

total_datasets = 0

retry_count = 0

print("开始获取所有datasets...")

while True:

try:

resp = wqbs.search_datasets_limited(

CONFIG['region'],

CONFIG['delay'],

CONFIG['universe'],

limit=limit,

offset=offset,

)

# 重置重试计数器

retry_count = 0

data = resp.json()

# 检查响应是否有效

if 'count' not in data or 'results' not in data:

print("响应数据格式异常")

break

# 如果是第一次请求，获取总dataset数

if offset == 0:

total_datasets = data['count']

print(f"总datasets数: {total_datasets}")

if total_datasets == 0:

print("没有找到datasets")

break

# 提取当前页的datasets

results = data['results']

current_datasets = [item['id'] for item in results]

datasets.extend(current_datasets)

# 打印进度

current_progress = offset + len(current_datasets)

print(f"已获取 {current_progress}/{total_datasets} 个datasets")

# 如果没有更多数据或已获取所有datasets，退出循环

if not current_datasets or current_progress >= total_datasets:

break

# 更新offset

offset += len(current_datasets)  # 使用实际获取的数量而不是limit

# 添加延迟避免频繁请求

if CONFIG['request_delay'] > 0:

time.sleep(CONFIG['request_delay'])

except Exception as e:

print(f"获取datasets出错: {e}")

retry_count += 1

if retry_count >= CONFIG['max_retries']:

print(f"达到最大重试次数({CONFIG['max_retries']})，停止获取datasets")

break

print(f"第 {retry_count} 次重试，等待 {CONFIG['retry_delay']} 秒后重试...")

time.sleep(CONFIG['retry_delay'])

return datasets, total_datasets

然后在dataset中查询：

# 在每个dataset中搜索指定关键字的函数

def search_in_datasets(datasets):

"""在每个dataset中搜索指定关键字，如果search为空则获取所有字段"""

all_ids = []

total_records = 0

if CONFIG['search']:

print(f"\n开始在 {len(datasets)} 个datasets中搜索关键字: {CONFIG['search']}")

else:

print(f"\n开始在 {len(datasets)} 个datasets中获取所有字段")

for dataset_idx, dataset_id in enumerate(datasets, 1):

if CONFIG['search']:

print(f"正在搜索dataset {dataset_idx}/{len(datasets)}: {dataset_id}")

else:

print(f"正在获取dataset {dataset_idx}/{len(datasets)}: {dataset_id}")

limit = CONFIG['page_size']

offset = 0

retry_count = 0

dataset_ids = []

while True:

try:

# 构建查询参数

search_params = {

'region': CONFIG['region'],

'delay': CONFIG['delay'],

'universe': CONFIG['universe'],

'dataset_id': dataset_id,

'type': CONFIG['type'],

'limit': limit,

'offset': offset,

}

# 只有当search不为空时才添加search参数

if CONFIG['search']:

search_params['search'] = CONFIG['search']

resp = wqbs.search_fields_limited(**search_params)

# 重置重试计数器

retry_count = 0

data = resp.json()

# 检查响应是否有效

if 'count' not in data or 'results' not in data:

print(f"dataset {dataset_id} 响应数据格式异常")

break

# 如果是第一次请求，获取总记录数

if offset == 0:

dataset_total = data['count']

if dataset_total == 0:

if CONFIG['search']:

print(f"  dataset {dataset_id} 中没有匹配的记录")

else:

print(f"  dataset {dataset_id} 中没有字段")

break

if CONFIG['search']:

print(f"  dataset {dataset_id} 中有 {dataset_total} 条匹配记录")

else:

print(f"  dataset {dataset_id} 中有 {dataset_total} 个字段")

# 提取当前页的id

results = data['results']

current_ids = [item['id'] for item in results]

dataset_ids.extend(current_ids)

# 打印进度

current_progress = offset + len(current_ids)

# 如果没有更多数据或已获取所有记录，退出循环

if not current_ids or current_progress >= data['count']:

break

# 更新offset

offset += len(current_ids)

# 添加延迟避免频繁请求

if CONFIG['request_delay'] > 0:

time.sleep(CONFIG['request_delay'])

except Exception as e:

if CONFIG['search']:

print(f"搜索dataset {dataset_id} 出错: {e}")

else:

print(f"获取dataset {dataset_id} 字段出错: {e}")

retry_count += 1

if retry_count >= CONFIG['max_retries']:

print(f"达到最大重试次数({CONFIG['max_retries']})，跳过该dataset")

break

print(f"第 {retry_count} 次重试，等待 {CONFIG['retry_delay']} 秒后重试...")

time.sleep(CONFIG['retry_delay'])

# 添加该dataset中找到的ids

all_ids.extend(dataset_ids)

total_records += len(dataset_ids)

if CONFIG['search']:

print(f"  从dataset {dataset_id} 中获取了 {len(dataset_ids)} 条记录")

else:

print(f"  从dataset {dataset_id} 中获取了 {len(dataset_ids)} 个字段")

# 添加dataset间的延迟

if CONFIG['request_delay'] > 0:

time.sleep(CONFIG['request_delay'])

return all_ids, total_records

主函数：

def main():

print("开始新的查询策略...")

print(f"配置参数: {CONFIG}")

# 第一步：获取所有datasets

datasets, total_datasets = get_all_datasets()

if not datasets:

print("没有找到任何datasets，程序结束")

return

# 第二步：在每个dataset中搜索

all_ids, total_count = search_in_datasets(datasets)

# 输出结果

if CONFIG['search']:

print(f"\n成功从 {len(datasets)} 个datasets中获取 {len(all_ids)} 条记录")

else:

print(f"\n成功从 {len(datasets)} 个datasets中获取 {len(all_ids)} 个字段")

if all_ids:

id_string = ','.join(all_ids)

print(f"所有ID: {id_string}")

else:

if CONFIG['search']:

print("未获取到任何记录")

else:

print("未获取到任何字段")

if __name__ == "__main__":

main()

这段代码会将所有符合条件的datafield的id用逗号分隔，可以直接作为模板引擎的输入，注意调用api直接有要时间间隔，这个间隔也是在开头可以配置的

---

## 讨论与评论 (1)

### 评论 #1 (作者: MZ45384, 时间: 3个月前)

非常有趣的代码，感谢大佬的模糊查询方法。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

