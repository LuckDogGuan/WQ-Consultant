# Osmosis competition 打分V2-精细化筛选alpha池

- **链接**: [L2] Osmosis competition 打分V2-精细化筛选alpha池.md
- **作者**: CC21336
- **发布时间/热度**: 5个月前, 得票: 10

## 帖子正文

Osmosis competition 第一周结果公布前，自己没有对alpha池进行精选。因为组SA的时候，alpha个数比较多的情况下，通常指标会比较好看。因此自己一度曾错认为alpha池中个数越多，整体表现很可能会更好，于是把大多数alpha都入选到池中。但打完分后，观察Leaderboard,我的ASI地区，Daly PNL ASI 几乎每天都是亏的，相反近期刚参与的 GLB/IND 全部alpha本身数目比较少，但大多数情况下却是赚的。同时排行榜中，有大佬只选那么10几20几alpha，Daly PNL; Total Score ; Combo IR Rank 却表现非常好。反观自己第一周的Combo results公布后，表现却非常差。

这个结果，充分说明了比赛期间WeiJie老师反复强调 alpha池中独特与优异的重要性，如果全选一锅煮的话，绝对是误入歧途。这便失去了比赛的意义。

眼看，美国东部时间 12 月 28 日 23:59 的 Osmosis 积分即将公布，于是重新修改了代码，准备重新抽奖。代码主要思路如下：

①先通过 夏普、Fitness、回撤、保证金、换手率等硬性指标进行基础筛选；

②对初步筛选池进行验证，提前排除不能参与Osmosis的Alpha；

③获取alpha的IS Summary近11年信息：考察近3-4年的历史表现稳定性，进行多维度评估 ，进一步筛选alpha池。

④因alpha数目过多，PNL是否流畅美观，用肉眼目检，显然是不现实的。

现列举两个配置项，大家能对主要思路一目了然：

**第一阶段：Alpha池筛选配置：**

![图片](images/img_7a0c072052.png)

**第二阶段：Alpha打分配置：**

![图片](images/img_a0f346270e.png)

附上其它几篇经典参考贴。

**参考帖:**

**[XX42289](/hc/en-us/profiles/14187300941847-XX42289)   [【轻松点击即可完成参赛】CA 降维 + 多指标聚类数评判 + KMeans / 层次 / DBSCAN 聚类的 Osmosis 点数分配工具]([Commented] 【课代表】【轻松点击即可完成参赛】CA 降维  多指标聚类数评判  KMeans  层次  DBSCAN 聚类的 Osmosis 点数分配工具经验分享.md)**

[JR23144](/hc/en-us/profiles/28844048981143-JR23144)   [【贺六浑】-【工具配置】OC2025 一键清空分数脚本]([L2] 【贺六浑】-【工具配置】OC2025 一键清空分数脚本经验分享.md)

[JX79797](/hc/en-us/profiles/30384388968343-JX79797)    [[OC2025]指标准入和多维度评分一键参与OC2025]([Commented] [OC2025]指标准入和多维度评分一键参与OC2025.md)

[CC21336](/hc/en-us/profiles/28830671151383-CC21336)   [Osmosis 给你100000美金，每个alpha买多少？分享4种给自己alpha池打分的方案-打完就飙升]([Commented] Osmosis 给你100000美金每个alpha买多少分享4种给自己alpha池打分的方案-打完就飙升经验分享.md)

参考代码：

from machine_lib import*

import urllib.parse

import logging

import numpy as np

import pandas as pd

from datetime import datetime, timedelta

from scipy.stats import rankdata, zscore, pearsonr, kurtosis, skew

from sklearn.preprocessing import StandardScaler, RobustScaler

from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

import time

import json

import warnings

warnings.filterwarnings('ignore')

# ============================

# 获取年度统计信息

# ============================

def get_alpha_yearly_stats(s, alpha_id: str, max_retries=5):

"""获取Alpha年度统计数据"""

retry_delay = 3

for attempt in range(max_retries):

try:

logging.info(f"获取Alpha {alpha_id} 的年度统计数据 (尝试 {attempt + 1}/{max_retries})")

response = s.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats](https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats) ")

response.raise_for_status()

text = (response.text or "").strip()

if not text:

if attempt < max_retries - 1:

logging.warning(f"Alpha {alpha_id} 年度统计数据为空，重试中...")

time.sleep(retry_delay)

retry_delay *= 1.5

continue

else:

return {}

try:

stats_data = response.json()

if stats_data:

print(f"alpha_id: {alpha_id} 的 yearly stats OK")

return stats_data

else:

if attempt < max_retries - 1:

logging.warning(f"Alpha {alpha_id} 年度统计JSON为空，重试中...")

time.sleep(retry_delay)

retry_delay *= 1.5

continue

else:

return {}

except json.JSONDecodeError as parse_err:

if attempt < max_retries - 1:

logging.warning(f"Alpha {alpha_id} 年度统计JSON解析失败，重试中...")

time.sleep(retry_delay)

retry_delay *= 1.5

continue

else:

raise

except requests.RequestException as e:

if attempt < max_retries - 1:

logging.warning(f"获取Alpha {alpha_id} 年度统计失败，重试中: {e}")

time.sleep(retry_delay)

retry_delay *= 1.5

continue

else:

raise

return {}

# ============================

# 清除Alpha分数函数

# ============================

def clear_alpha_score(s, alpha_id: str, old_osmosisPoints: str):

"""

一个专门用于清除 Alpha 分数的函数。

它通过将 'osmosisPoints' 字段设置为 null 来实现。

"""

params = {"osmosisPoints": None}  # 在 requests 中, None 会被序列化为 JSON null

response = s.patch(

f" [https://api.worldquantbrain.com/alphas/{alpha_id}](https://api.worldquantbrain.com/alphas/{alpha_id}) ", json=params

)

if response.status_code == 200:

print(f"成功清除 Alpha {alpha_id} 的分数 (原分数: {old_osmosisPoints})。")

return "SUCCESS"

else:

print(f"清除 Alpha {alpha_id} 分数失败，状态码: {response.status_code}, 信息: {response.text}")

return "FAILED"

# ============================

# 核心筛选器类

# ============================

class CompetitionAlphaScreener:

"""比赛专用Alpha筛选器"""

def __init__(self, session, config=None, **kwargs):

"""

初始化筛选器

参数:

- session: 登录会话

- config: 配置对象

- **kwargs: 动态配置参数

"""

self.session = session

# 配置

self.config = {

'region': kwargs.get('region', "ASI"),

'analysis_years': kwargs.get('analysis_years', 3),

'exclude_recent_years': kwargs.get('exclude_recent_years', 1),

'target_pool_size': kwargs.get('target_pool_size', 40),

'consultant_date': kwargs.get('consultant_date', datetime(2025, 3, 11)),

# 基础筛选阈值

'min_sharpe': kwargs.get('min_sharpe', 2.0),

'min_fitness': kwargs.get('min_fitness', 1.3),

'max_drawdown': kwargs.get('max_drawdown', 10.0),

'min_margin': kwargs.get('min_margin', 10.0),

'min_turnover': kwargs.get('min_turnover', 3.0),

'max_turnover': kwargs.get('max_turnover', 40.0),

# 年度筛选阈值

'min_sharpe_ny_mean': kwargs.get('min_sharpe_ny_mean', 1.8),

'max_sharpe_ny_std': kwargs.get('max_sharpe_ny_std', 0.8),

'min_fitness_ny_mean': kwargs.get('min_fitness_ny_mean', 1.3),

'min_positive_ratio': kwargs.get('min_positive_ratio', 0.6),

'min_available_years': kwargs.get('min_available_years', 3),

# API配置

'batch_size': kwargs.get('batch_size', 5),

'request_delay': kwargs.get('request_delay', 1),

'max_retries': kwargs.get('max_retries', 3),

'initial_limit': kwargs.get('initial_limit', 200),

# 输出配置

'verbose': kwargs.get('verbose', True),

}

self.cache = {}

self.alpha_pool = []

self.stats = {

'total_processed': 0,

'with_yearly_data': 0,

'passed_basic': 0,

'passed_updatable': 0,  # 新增：通过可更新性测试

'passed_yearly': 0,

'final_selected': 0,

}

def get_alpha_basic_metrics(self, alpha_id, max_retries=None):

"""

获取Alpha基础指标

参数:

- alpha_id: Alpha ID

- max_retries: 最大重试次数

返回:

- dict: Alpha基础指标

"""

if max_retries is None:

max_retries = self.config['max_retries']

for attempt in range(max_retries):

try:

alpha_url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}](https://api.worldquantbrain.com/alphas/{alpha_id}) "

alpha_resp = self.session.get(alpha_url)

if alpha_resp.status_code != 200:

if attempt < max_retries - 1:

time.sleep(2)

continue

else:

return None

data = alpha_resp.json()

is_data = data.get('is', {})

metrics = {

'id': alpha_id,

'fitness': is_data.get('fitness', 0.0),

'longCount': is_data.get('longCount', 0.0),

'shortCount': is_data.get('shortCount', 0.0),

'turnover': is_data.get('turnover', 0.0),

'returns': is_data.get('returns', 0.0),

'drawdown': is_data.get('drawdown', 0.0),

'margin': is_data.get('margin', 0.0),

'sharpe': is_data.get('sharpe', 0.0),

}

return metrics

except Exception as e:

if attempt < max_retries - 1:

time.sleep(2)

else:

logging.error(f"获取Alpha {alpha_id} 基础指标失败: {e}")

return None

def get_alpha_current_score(self, alpha_id, max_retries=2):

"""

获取Alpha当前分数

参数:

- alpha_id: Alpha ID

- max_retries: 最大重试次数

返回:

- str: 当前分数

"""

for attempt in range(max_retries):

try:

alpha_url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}](https://api.worldquantbrain.com/alphas/{alpha_id}) "

alpha_resp = self.session.get(alpha_url)

if alpha_resp.status_code != 200:

if attempt < max_retries - 1:

time.sleep(1)

continue

else:

return "unknown"

data = alpha_resp.json()

# 尝试从不同位置获取分数

score = data.get('osmosisPoints', 'unknown')

if score is None:

score = 'null'

return str(score)

except Exception as e:

if attempt < max_retries - 1:

time.sleep(1)

else:

return "unknown"

return "unknown"

def test_alpha_updatable_with_clear(self, alpha_id, test_score=1, max_retries=2):

"""

测试Alpha是否可以更新分数，测试后立即清除

参数:

- alpha_id: Alpha ID

- test_score: 测试分数

- max_retries: 最大重试次数

返回:

- tuple: (是否可更新, 错误信息)

"""

update_url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}](https://api.worldquantbrain.com/alphas/{alpha_id}) "

# 先获取当前分数

current_score = self.get_alpha_current_score(alpha_id)

for attempt in range(max_retries):

try:

# 1. 测试更新分数

response = self.session.patch(update_url, json={"osmosisPoints": int(test_score)})

if response.status_code == 200:

# 2. 立即清除测试分数

clear_result = clear_alpha_score(self.session, alpha_id, str(test_score))

if clear_result == "SUCCESS":

return True, None

else:

# 清除失败，尝试重试清除

for clear_attempt in range(2):

time.sleep(1)

clear_result = clear_alpha_score(self.session, alpha_id, str(test_score))

if clear_result == "SUCCESS":

return True, None

# 如果清除失败，记录错误

return False, f"测试成功但清除失败: {clear_result}"

else:

# 测试更新失败

try:

error_data = response.json()

error_msg = str(error_data.get('osmosisPoints', ['未知错误'])[0])

return False, error_msg

except:

return False, f"HTTP {response.status_code}"

except Exception as e:

if attempt < max_retries - 1:

time.sleep(1)

else:

return False, str(e)

return False, "达到最大重试次数"

def calculate_recent_Ny_sharpe_mean(self, yearly_stats, analysis_years=None, exclude_recent_years=None):

"""

计算最近N年的Sharp均值（排除最近M年）

参数:

- yearly_stats: 年度统计数据

- analysis_years: 分析年数

- exclude_recent_years: 排除最近年数

返回:

- tuple: (Sharp均值, 实际使用年数, 标准差) 或 (None, None, None)

"""

try:

if not yearly_stats or 'records' not in yearly_stats:

return None, None, None

records = yearly_stats['records']

if not records:

return None, None, None

# 使用配置值或参数值

analysis_years = analysis_years if analysis_years is not None else self.config['analysis_years']

exclude_recent_years = exclude_recent_years if exclude_recent_years is not None else self.config['exclude_recent_years']

# 提取年份和Sharp值

year_sharpe_data = []

for record in records:

if len(record) > 6:  # 确保有足够的字段

try:

year_str = str(record[0])

sharpe_value = float(record[6])  # Sharp值通常在索引6

year_sharpe_data.append((int(year_str), sharpe_value))

except (ValueError, IndexError, TypeError):

continue

if not year_sharpe_data:

return None, None, None

# 按年份降序排序

year_sharpe_data.sort(key=lambda x: x[0], reverse=True)

# 排除最近N年

if exclude_recent_years > 0 and len(year_sharpe_data) > exclude_recent_years:

year_sharpe_data = year_sharpe_data[exclude_recent_years:]

# 获取最近N年的数据

recent_sharpe_values = []

for i, (year, sharpe) in enumerate(year_sharpe_data):

if i >= analysis_years:

break

recent_sharpe_values.append(sharpe)

if not recent_sharpe_values or len(recent_sharpe_values) < 2:

return None, None, None

# 计算均值、实际年数、标准差

sharpe_mean = np.mean(recent_sharpe_values)

actual_years = len(recent_sharpe_values)

sharpe_std = np.std(recent_sharpe_values) if len(recent_sharpe_values) > 1 else 0

return sharpe_mean, actual_years, sharpe_std

except Exception as e:

logging.error(f"计算最近{analysis_years}年Sharp均值异常: {e}")

return None, None, None

def get_alpha_comprehensive_data(self, alpha_id, max_retries=None):

"""

获取Alpha的完整数据

参数:

- alpha_id: Alpha ID

- max_retries: 最大重试次数

返回:

- dict: Alpha完整数据

"""

if max_retries is None:

max_retries = self.config['max_retries']

# 检查缓存

if alpha_id in self.cache:

return self.cache[alpha_id]

# 获取基础指标

base_metrics = self.get_alpha_basic_metrics(alpha_id, max_retries)

if not base_metrics:

return None

# 获取年度统计数据

yearly_stats = get_alpha_yearly_stats(self.session, alpha_id, max_retries)

if yearly_stats:

# 计算最近N年的Sharp均值（排除最近M年）

sharpe_mean, actual_years, sharpe_std = self.calculate_recent_Ny_sharpe_mean(yearly_stats)

if sharpe_mean is not None:

# 动态字段名

analysis_years = self.config['analysis_years']

field_name = f'sharpe{analysis_years}Y'

base_metrics[field_name] = sharpe_mean

base_metrics[f'{field_name}_actual_years'] = actual_years

base_metrics[f'{field_name}_std'] = sharpe_std

base_metrics['has_yearly_stats'] = True

else:

# 如果无法计算N年均值，使用当前Sharp值

analysis_years = self.config['analysis_years']

field_name = f'sharpe{analysis_years}Y'

base_metrics[field_name] = base_metrics['sharpe']

base_metrics[f'{field_name}_actual_years'] = 0

base_metrics[f'{field_name}_std'] = 0

base_metrics['has_yearly_stats'] = False

else:

# 如果无法获取年度统计数据，使用当前Sharp值

analysis_years = self.config['analysis_years']

field_name = f'sharpe{analysis_years}Y'

base_metrics[field_name] = base_metrics['sharpe']

base_metrics[f'{field_name}_actual_years'] = 0

base_metrics[f'{field_name}_std'] = 0

base_metrics['has_yearly_stats'] = False

# 缓存结果

self.cache[alpha_id] = base_metrics

return base_metrics

def collect_alpha_candidates(self, limit=None, offset=0, batch_size=None):

"""

收集Alpha候选列表

参数:

- limit: 限制数量

- offset: 偏移量

- batch_size: 批处理大小

返回:

- list: Alpha候选列表

"""

if limit is None:

limit = self.config['initial_limit']

if batch_size is None:

batch_size = self.config['batch_size']

alphas_data = []

start_date_str = urllib.parse.quote(self.config['consultant_date'].astimezone().isoformat(timespec='seconds'))

# 获取Alpha列表

url = (

f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?"

f"limit={limit}&offset={offset}"

f"&dateCreated%3E={start_date_str}"

f"&settings.region={self.config['region']}"

f"&status!=UNSUBMITTED%1FIS-FAIL"

f"&hidden=false"

f"&type!=SUPER"

f"&settings.delay=1"

)

# 添加基础筛选条件

url += (

f"&is.sharpe%3E={self.config['min_sharpe']}"

f"&is.fitness%3E={self.config['min_fitness']}"

f"&is.margin%3E={self.config['min_margin'] * 0.0001}"

f"&is.drawdown%3C={self.config['max_drawdown'] * 0.01}"

)

url += "&order=-dateSubmitted"

try:

resp = self.session.get(url)

if resp.status_code != 200:

logging.error(f"获取Alpha列表失败，状态码：{resp.status_code}")

return []

data = resp.json()

results = data.get("results", [])

# 提取Alpha ID

alpha_ids = [item['id'] for item in results]

if self.config['verbose']:

print(f"获取到 {len(alpha_ids)} 个Alpha ID，开始收集详细数据...")

# 分批获取详细数据

for i in range(0, len(alpha_ids), batch_size):

batch_ids = alpha_ids[i:i+batch_size]

if self.config['verbose']:

batch_num = i // batch_size + 1

total_batches = (len(alpha_ids) + batch_size - 1) // batch_size

print(f"  处理批次 {batch_num}/{total_batches} ({len(batch_ids)}个Alpha)")

for alpha_id in batch_ids:

metrics = self.get_alpha_comprehensive_data(alpha_id)

if metrics:

alphas_data.append(metrics)

self.stats['total_processed'] += 1

if metrics.get('has_yearly_stats', False):

self.stats['with_yearly_data'] += 1

# 批次间延迟

if i + batch_size < len(alpha_ids):

time.sleep(self.config['request_delay'])

return alphas_data

except Exception as e:

logging.error(f"收集Alpha候选列表异常: {e}")

return []

def apply_basic_filters(self, alpha_metrics_list):

"""

应用基础筛选

参数:

- alpha_metrics_list: Alpha指标列表

返回:

- list: 筛选后的Alpha列表

"""

filtered = []

for metrics in alpha_metrics_list:

conditions = []

# 基础指标筛选

conditions.append(metrics.get('sharpe', 0) >= self.config['min_sharpe'])

conditions.append(metrics.get('fitness', 0) >= self.config['min_fitness'])

conditions.append(metrics.get('drawdown', 0) < self.config['max_drawdown']*0.01)

conditions.append(metrics.get('margin', 0) >= self.config['min_margin']*0.0001)

turnover = metrics.get('turnover', 0)

conditions.append(self.config['min_turnover']*0.01 <= turnover <= self.config['max_turnover']*0.01)

# 所有条件满足

if all(conditions):

filtered.append(metrics)

self.stats['passed_basic'] = len(filtered)

if self.config['verbose']:

print(f"基础筛选: {len(alpha_metrics_list)} -> {len(filtered)} ({len(filtered)/len(alpha_metrics_list)*100:.1f}%)")

return filtered

def apply_updatable_test(self, alpha_metrics_list, test_score=1):

"""

应用可更新性测试，测试后立即清除分数，移除不能打分的Alpha

参数:

- alpha_metrics_list: Alpha指标列表

- test_score: 测试分数

返回:

- tuple: (可更新的Alpha列表, 不可更新的Alpha列表)

"""

updatable_alphas = []

non_updatable_alphas = []

if self.config['verbose']:

print(f"\n开始测试Alpha可更新性（测试分数: {test_score}，测试后立即清除）...")

print(f"总共 {len(alpha_metrics_list)} 个Alpha需要测试")

for i, metrics in enumerate(alpha_metrics_list, 1):

alpha_id = metrics['id']

if self.config['verbose'] and (i % 10 == 0 or i == 1 or i == len(alpha_metrics_list)):

print(f"  测试进度: {i}/{len(alpha_metrics_list)}")

# 测试Alpha是否可以更新（测试后立即清除）

updatable, error_msg = self.test_alpha_updatable_with_clear(alpha_id, test_score)

if updatable:

updatable_alphas.append(metrics)

else:

non_updatable_alphas.append({

'id': alpha_id,

'metrics': metrics,

'error': error_msg

})

self.stats['passed_updatable'] = len(updatable_alphas)

if self.config['verbose']:

print(f"可更新性测试完成:")

print(f"  可更新Alpha数量: {len(updatable_alphas)}")

print(f"  不可更新Alpha数量: {len(non_updatable_alphas)}")

if non_updatable_alphas:

print(f"\n不可更新Alpha列表 (前10个):")

for alpha_info in non_updatable_alphas[:10]:

alpha_id_short = alpha_info['id'][:12] + '...' if len(alpha_info['id']) > 12 else alpha_info['id']

error_msg = alpha_info['error']

if 'non-compensated' in str(error_msg).lower():

reason = "非补偿Alpha"

elif 'HTTP' in str(error_msg):

reason = f"HTTP错误: {error_msg}"

else:

reason = f"其他错误: {error_msg}"

print(f"  ID: {alpha_id_short}, 原因: {reason}")

if len(non_updatable_alphas) > 10:

print(f"  ... 还有 {len(non_updatable_alphas) - 10} 个不可更新Alpha")

return updatable_alphas, non_updatable_alphas

def apply_yearly_filters(self, alpha_metrics_list):

"""

应用年度绩效筛选

参数:

- alpha_metrics_list: Alpha指标列表

返回:

- list: 筛选后的Alpha列表

"""

filtered = []

for metrics in alpha_metrics_list:

if not metrics.get('has_yearly_stats', False):

# 无年度数据，跳过年度筛选

continue

conditions = []

# 获取动态字段名

analysis_years = self.config['analysis_years']

sharpe_field = f'sharpe{analysis_years}Y'

std_field = f'{sharpe_field}_std'

actual_years_field = f'{sharpe_field}_actual_years'

# 检查是否有足够的数据年数

if actual_years_field in metrics:

conditions.append(metrics[actual_years_field] >= self.config['min_available_years'])

# 检查N年夏普均值

if sharpe_field in metrics and not pd.isna(metrics[sharpe_field]):

conditions.append(metrics[sharpe_field] >= self.config['min_sharpe_ny_mean'])

# 检查N年夏普标准差

if std_field in metrics and not pd.isna(metrics[std_field]):

conditions.append(metrics[std_field] <= self.config['max_sharpe_ny_std'])

# 盈利年占比（简化处理，如果N年夏普均值大于0，则认为盈利年占比高）

if sharpe_field in metrics and metrics[sharpe_field] > 0:

conditions.append(True)

else:

conditions.append(False)

# 所有条件满足

if all(conditions):

filtered.append(metrics)

self.stats['passed_yearly'] = len(filtered)

if self.config['verbose']:

yearly_count = sum(1 for m in alpha_metrics_list if m.get('has_yearly_stats', False))

if yearly_count > 0:

print(f"年度筛选: {yearly_count} -> {len(filtered)} ({len(filtered)/yearly_count*100:.1f}%)")

return filtered

def build_alpha_pool(self, target_size=None):

"""

构建Alpha池

参数:

- target_size: 目标池大小

返回:

- list: 最终Alpha池

"""

if target_size is None:

target_size = self.config['target_pool_size']

if self.config['verbose']:

print("="*60)

print("比赛专用Alpha筛选系统")

print("="*60)

print(f"目标地区: {self.config['region']}")

print(f"分析年数: {self.config['analysis_years']}年 (排除最近{self.config['exclude_recent_years']}年)")

print(f"目标池大小: {target_size}")

print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("-"*60)

# 1. 收集Alpha候选

alphas_data = self.collect_alpha_candidates()

if not alphas_data:

print("错误: 未获取到Alpha数据")

return []

if self.config['verbose']:

print(f"✓ 收集到 {len(alphas_data)} 个Alpha候选")

# 2. 第一阶段筛选: 基础指标

filtered_stage1 = self.apply_basic_filters(alphas_data)

if not filtered_stage1:

print("错误: 基础筛选后无符合条件的Alpha")

return []

if self.config['verbose']:

print(f"✓ 基础筛选通过: {len(filtered_stage1)} 个Alpha")

# 3. 可更新性测试: 移除不能打分的Alpha

updatable_alphas, non_updatable_alphas = self.apply_updatable_test(filtered_stage1, test_score=1)

if not updatable_alphas:

print("错误: 无可以打分的Alpha")

return []

if self.config['verbose']:

print(f"✓ 可更新性测试通过: {len(updatable_alphas)} 个Alpha")

# 4. 第二阶段筛选: 年度绩效

filtered_stage2 = self.apply_yearly_filters(updatable_alphas)

if not filtered_stage2:

print("错误: 年度筛选后无符合条件的Alpha")

return []

if self.config['verbose']:

print(f"✓ 年度筛选通过: {len(filtered_stage2)} 个Alpha")

# 5. 如果数量超过目标，选择前N个

if len(filtered_stage2) > target_size:

# 按夏普值排序

filtered_stage2.sort(key=lambda x: x.get('sharpe', 0), reverse=True)

final_pool = filtered_stage2[:target_size]

else:

final_pool = filtered_stage2

self.stats['final_selected'] = len(final_pool)

self.alpha_pool = final_pool

if self.config['verbose']:

print(f"✓ 最终选择: {len(final_pool)} 个Alpha")

print("-"*60)

self.print_summary()

print("="*60)

return final_pool

def print_summary(self):

"""打印统计摘要"""

if not self.alpha_pool:

print("Alpha池为空")

return

print("\nAlpha池统计摘要:")

print(f"Alpha数量: {len(self.alpha_pool)}")

# 性能指标

sharpe_values = [a.get('sharpe', 0) for a in self.alpha_pool]

fitness_values = [a.get('fitness', 0) for a in self.alpha_pool]

drawdown_values = [abs(a.get('drawdown', 0)) * 100 for a in self.alpha_pool]

turnover_values = [a.get('turnover', 0) * 100 for a in self.alpha_pool]

margin_values = [a.get('margin', 0) * 0.01 for a in self.alpha_pool]

print(f"平均夏普: {np.mean(sharpe_values):.2f} (范围: {min(sharpe_values):.2f}-{max(sharpe_values):.2f})")

print(f"平均Fitness: {np.mean(fitness_values):.2f} (范围: {min(fitness_values):.2f}-{max(fitness_values):.2f})")

print(f"平均回撤: {np.mean(drawdown_values):.2f}%")

print(f"平均换手率: {np.mean(turnover_values):.1f}%")

print(f"平均保证金: {np.mean(margin_values):.2f}%")

# ============================

# 打分系统

# ============================

class AlphaScorer:

"""Alpha打分系统"""

def __init__(self, session, **kwargs):

"""

初始化打分系统

参数:

- session: 登录会话

- **kwargs: 配置参数

"""

self.session = session

# 配置

self.config = {

'allocation_method': kwargs.get('allocation_method', 'weighted'),

'total_score': kwargs.get('total_score', 100000),

# 方法参数

'softmax_temp': kwargs.get('softmax_temp', 0.1),

'min_base_score': kwargs.get('min_base_score', 100),

'use_pca': kwargs.get('use_pca', True),

# 权重配置

'weights': kwargs.get('weights', {

'softmax': 0.4,

'rank': 0.3,

'cluster': 0.3

}),

'cluster_weight': kwargs.get('cluster_weight', 0.3),

# 输出配置

'verbose': kwargs.get('verbose', True),

}

def calculate_turnover_score(self, turnover):

"""

计算turnover得分，理想区间为8-20%

参数:

- turnover: 换手率

返回:

- float: turnover得分 (0-1)

"""

if pd.isna(turnover):

return 0.5

ideal_center = 14.0

ideal_min = 8.0

ideal_max = 20.0

if ideal_min <= turnover <= ideal_max:

distance = abs(turnover - ideal_center) / (ideal_max - ideal_min)

score = 1.0 - distance

elif turnover < ideal_min:

score = max(0, turnover / ideal_min)

else:

score = max(0, 1.0 - (turnover - ideal_max) / (4 * ideal_max)) if ideal_max > 0 else 0

return max(0, min(1, score))

def calculate_balance_score(self, long_count, short_count):

"""

计算多空平衡得分

参数:

- long_count: 多头数量

- short_count: 空头数量

返回:

- float: 多空平衡得分 (0-1)

"""

if pd.isna(long_count) or pd.isna(short_count):

return 0.5

if long_count == 0 and short_count == 0:

return 0.0

if long_count == 0 or short_count == 0:

return 0.2

ratio = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) > 0 else 0

balance_score = ratio ** 0.5 if ratio >= 0 else 0

return min(1, max(0, balance_score))

def calculate_sharpe_stability_score(self, sharpe, sharpeNY, sharpeNY_std):

"""

计算Sharp稳定性得分

参数:

- sharpe: 当前Sharp值

- sharpeNY: 最近N年Sharp均值

- sharpeNY_std: 最近N年Sharp标准差

返回:

- float: Sharp稳定性得分 (0-1)

"""

if pd.isna(sharpe) or pd.isna(sharpeNY):

return 0.5

if sharpeNY == 0:

if sharpe > 0:

return 0.8

elif sharpe < 0:

return 0.2

else:

return 0.5

# 计算当前Sharp相对于N年均值的表现

ratio = sharpe / sharpeNY

# 评分逻辑

if ratio >= 1.5:

# 当前Sharp显著高于N年均值（+50%以上），表现大幅提升

return 1.0

elif ratio >= 1.2:

# 当前Sharp明显高于N年均值（+20%以上）

return 0.9

elif ratio >= 1.0:

# 当前Sharp略高于或等于N年均值

return 0.8

elif ratio >= 0.8:

# 当前Sharp略低于N年均值（-20%以内）

return 0.6

elif ratio >= 0.5:

# 当前Sharp明显低于N年均值（-50%以内）

return 0.4

elif ratio >= 0:

# 当前Sharp显著低于N年均值（但仍为正）

return 0.2

elif ratio >= -0.5:

# 当前为负，但历史为正

return 0.1

else:

# 当前大幅为负

return 0.0

def calculate_alpha_scores(self, alpha_metrics_list, weights=None, analysis_years=3):

"""

为每个alpha计算综合得分

参数:

- alpha_metrics_list: Alpha指标列表

- weights: 权重配置

- analysis_years: 分析年数

返回:

- DataFrame: 包含综合得分的DataFrame

"""

if not alpha_metrics_list:

logging.warning("没有alpha数据用于计算得分")

return pd.DataFrame()

df = pd.DataFrame(alpha_metrics_list)

# 检查必要的列是否存在

required_columns = ['fitness', 'returns', 'margin', 'sharpe', 'drawdown', 'turnover', 'longCount', 'shortCount']

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:

logging.warning(f"缺失列: {missing_columns}，使用默认值填充")

for col in missing_columns:

df[col] = 0.0

# 动态字段名

sharpe_field = f'sharpe{analysis_years}Y'

std_field = f'{sharpe_field}_std'

# 确保有sharpeNY列

if sharpe_field not in df.columns:

logging.warning(f"没有{sharpe_field}列，将使用sharpe值作为替代")

df[sharpe_field] = df.get('sharpe', 0.0)

df[std_field] = 0.0

# 确保有标准差列

if std_field not in df.columns:

df[std_field] = 0.0

# 默认权重配置

if weights is None:

weights = {

'fitness': 0.15,

'returns': 0.15,

'margin': 0.10,

'sharpe': 0.15,

'sharpeNY': 0.10,

'sharpe_stability': 0.15,

'drawdown': 0.10,

'turnover': 0.05,

'balance': 0.05,

}

# 归一化越大越好的指标

for col in ['fitness', 'returns', 'margin', 'sharpe', sharpe_field]:

if len(df) > 1 and df[col].nunique() > 1:

df[f'{col}_score'] = rankdata(df[col].fillna(0)) / len(df)

else:

df[f'{col}_score'] = 0.5

# 计算Sharp稳定性得分

df['sharpe_stability_score'] = df.apply(

lambda row: self.calculate_sharpe_stability_score(

row['sharpe'],

row[sharpe_field],

row[std_field]

),

axis=1

)

# 处理drawdown(越小越好)

if 'drawdown' in df.columns and len(df) > 1 and df['drawdown'].nunique() > 1:

neg_drawdown = -df['drawdown'].fillna(df['drawdown'].max() if df['drawdown'].max() > 0 else 1)

df['drawdown_score'] = rankdata(neg_drawdown) / len(df)

else:

df['drawdown_score'] = 0.5

# 处理turnover

df['turnover_score'] = df['turnover'].apply(lambda x: self.calculate_turnover_score(x))

# 计算多空平衡得分

df['balance_score'] = df.apply(lambda row: self.calculate_balance_score(row['longCount'], row['shortCount']), axis=1)

# 计算综合得分

df['composite_score'] = (

weights['fitness'] * df['fitness_score'] +

weights['returns'] * df['returns_score'] +

weights['margin'] * df['margin_score'] +

weights['sharpe'] * df['sharpe_score'] +

weights['sharpeNY'] * df[f'{sharpe_field}_score'] +

weights['sharpe_stability'] * df['sharpe_stability_score'] +

weights['drawdown'] * df['drawdown_score'] +

weights['turnover'] * df['turnover_score'] +

weights['balance'] * df['balance_score']

)

# 归一化到[0,1]

if len(df) > 1 and df['composite_score'].nunique() > 1:

score_min = df['composite_score'].min()

score_max = df['composite_score'].max()

if score_max > score_min:

df['composite_score'] = (df['composite_score'] - score_min) / (score_max - score_min)

else:

df['composite_score'] = 0.5

else:

df['composite_score'] = 0.5

return df

def assign_scores_with_softmax(self, df, total_score=100000, temperature=0.1):

"""

使用softmax函数分配分数

参数:

- df: 包含综合得分的DataFrame

- total_score: 总分

- temperature: 温度参数

返回:

- DataFrame: 包含分配分数的DataFrame

"""

if len(df) == 0:

return df

temperature = max(temperature, 1e-10)

scores = df['composite_score'].values

exp_scores = np.exp(scores / temperature)

probabilities = exp_scores / exp_scores.sum()

df['assigned_score'] = np.floor(probabilities * total_score).astype(int)

# 处理四舍五入偏差

score_diff = total_score - df['assigned_score'].sum()

if score_diff > 0:

top_indices = df.nlargest(min(score_diff, len(df)), 'composite_score').index

df.loc[top_indices, 'assigned_score'] += 1

elif score_diff < 0:

bottom_indices = df.nsmallest(min(abs(score_diff), len(df)), 'composite_score').index

for idx in bottom_indices:

if df.at[idx, 'assigned_score'] > 1:

df.at[idx, 'assigned_score'] -= 1

score_diff += 1

if score_diff == 0:

break

return df

def assign_scores_with_rank_based(self, df, total_score=100000, min_score=100):

"""

基于排名的分数分配方法

参数:

- df: 包含综合得分的DataFrame

- total_score: 总分

- min_score: 最小基础分数

返回:

- DataFrame: 包含分配分数的DataFrame

"""

if len(df) == 0:

return df

n = len(df)

min_score = max(1, min_score)

base_allocation = min_score * n

if base_allocation > total_score:

scale_factor = total_score / base_allocation

df['assigned_score'] = (min_score * scale_factor).astype(int)

return df

remaining_score = total_score - base_allocation

ranks = rankdata(df['composite_score'])

weights = np.exp(ranks / n)

normalized_weights = weights / weights.sum()

bonus_scores = np.floor(normalized_weights * remaining_score).astype(int)

df['assigned_score'] = min_score + bonus_scores

score_diff = total_score - df['assigned_score'].sum()

if score_diff != 0:

top_idx = df['composite_score'].idxmax()

df.at[top_idx, 'assigned_score'] += score_diff

return df

def assign_scores_weighted_combination(self, df, total_score=100000, cluster_weight=0.3):

"""

加权组合分配方法

参数:

- df: 包含综合得分的DataFrame

- total_score: 总分

- cluster_weight: 聚类权重

返回:

- DataFrame: 包含分配分数的DataFrame

"""

if len(df) == 0:

return df

# 计算各种方法的分数

df_softmax = self.assign_scores_with_softmax(df.copy(), total_score, self.config['softmax_temp'])

df_rank = self.assign_scores_with_rank_based(df.copy(), total_score, self.config['min_base_score'])

# 计算加权分数

weighted_scores = (

self.config['weights']['softmax'] * df_softmax['assigned_score'] +

self.config['weights']['rank'] * df_rank['assigned_score']

)

# 添加聚类调整

if cluster_weight > 0 and len(df) > 1:

try:

feature_cols = ['returns', 'margin', 'sharpe', 'drawdown', 'turnover']

available_features = [col for col in feature_cols if col in df.columns]

if len(available_features) >= 2:

X = df[available_features].fillna(0).values

scaler = RobustScaler()

X_scaled = scaler.fit_transform(X)

n_clusters = min(20, max(2, len(df) // 5))

if n_clusters > 1:

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

clusters = kmeans.fit_predict(X_scaled)

for i in range(n_clusters):

cluster_mask = clusters == i

cluster_size = np.sum(cluster_mask)

if cluster_size > 0:

cluster_factor = 1.0 / np.sqrt(cluster_size)

weighted_scores[cluster_mask] *= (1 + cluster_weight * cluster_factor)

except Exception as e:

if self.config['verbose']:

print(f"聚类调整失败: {e}")

# 归一化到总分

total_weighted = weighted_scores.sum()

if total_weighted > 0:

df['assigned_score'] = (weighted_scores / total_weighted * total_score).astype(int)

else:

df['assigned_score'] = (total_score // len(df))

# 调整总分

total_assigned = df['assigned_score'].sum()

diff = total_score - total_assigned

if diff != 0:

sorted_indices = df.sort_values('composite_score', ascending=False).index

adjust_count = min(abs(diff), len(df))

for i in range(adjust_count):

idx = sorted_indices[i]

if diff > 0:

df.at[idx, 'assigned_score'] += 1

else:

df.at[idx, 'assigned_score'] = max(1, df.at[idx, 'assigned_score'] - 1)

return df

def ensure_total_score_exact(self, df, total_score=100000):

"""

确保总分配分数严格等于指定总分

参数:

- df: 包含分配分数的DataFrame

- total_score: 目标总分

返回:

- DataFrame: 调整后的DataFrame

"""

if len(df) == 0:

return df

current_total = df['assigned_score'].sum()

diff = total_score - current_total

if diff == 0:

return df

df['assigned_score'] = df['assigned_score'].clip(lower=1)

if diff > 0:

sorted_indices = df.sort_values('composite_score', ascending=False).index

for i in range(diff):

idx = sorted_indices[i % len(df)]

df.at[idx, 'assigned_score'] += 1

else:

sorted_indices = df.sort_values('composite_score', ascending=True).index

for i in range(abs(diff)):

idx = sorted_indices[i % len(df)]

if df.at[idx, 'assigned_score'] > 1:

df.at[idx, 'assigned_score'] -= 1

else:

for j in range(i+1, len(df)):

next_idx = sorted_indices[j % len(df)]

if df.at[next_idx, 'assigned_score'] > 1:

df.at[next_idx, 'assigned_score'] -= 1

break

# 最终验证

final_total = df['assigned_score'].sum()

if final_total != total_score:

final_diff = total_score - final_total

if final_diff > 0:

top_idx = df['composite_score'].idxmax()

df.at[top_idx, 'assigned_score'] += final_diff

elif final_diff < 0:

bottom_idx = df['composite_score'].idxmin()

df.at[bottom_idx, 'assigned_score'] = max(1, df.at[bottom_idx, 'assigned_score'] + final_diff)

return df

def assign_scores_to_alphas(self, alpha_metrics_list, method='weighted', total_score=100000, analysis_years=3):

"""

为Alpha分配分数

参数:

- alpha_metrics_list: Alpha指标列表

- method: 分配方法

- total_score: 总分

- analysis_years: 分析年数

返回:

- DataFrame: 包含分配分数的DataFrame

- int: 总分配分数

- int: 成功更新数量

- int: 失败更新数量

"""

if not alpha_metrics_list:

print("没有Alpha数据，无法分配分数")

return pd.DataFrame(), 0, 0, 0

if self.config['verbose']:

print(f"\n为 {len(alpha_metrics_list)} 个Alpha分配 {total_score} 分...")

# 计算综合得分

df_scores = self.calculate_alpha_scores(alpha_metrics_list, analysis_years=analysis_years)

if df_scores.empty:

logging.error("无法计算Alpha综合得分")

return pd.DataFrame(), 0, 0, 0

# 分配分数

if method == 'softmax':

df_with_scores = self.assign_scores_with_softmax(

df_scores,

total_score,

self.config['softmax_temp']

)

elif method == 'rank':

df_with_scores = self.assign_scores_with_rank_based(

df_scores,

total_score,

self.config['min_base_score']

)

elif method == 'weighted':

df_with_scores = self.assign_scores_weighted_combination(

df_scores,

total_score,

self.config['cluster_weight']

)

else:

# 默认使用加权组合

df_with_scores = self.assign_scores_weighted_combination(

df_scores,

total_score,

self.config['cluster_weight']

)

# 确保总分完全匹配

df_with_scores = self.ensure_total_score_exact(df_with_scores, total_score)

# 更新分数

total_assigned = 0

successful_updates = 0

failed_updates = 0

# 按分配分数排序

df_with_scores = df_with_scores.sort_values('assigned_score', ascending=False)

if self.config['verbose']:

print(f"\n开始更新Alpha的分数...")

for idx, alpha in df_with_scores.iterrows():

alpha_id = alpha['id']

assigned_score = alpha['assigned_score']

if self.config['verbose']:

print(f"Alpha ID: {alpha_id}")

print(f"  综合得分: {alpha.get('composite_score', 0):.4f}")

print(f"  分配分数: {assigned_score}")

# 调用API更新分数

update_url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}](https://api.worldquantbrain.com/alphas/{alpha_id}) "

try:

response = self.session.patch(update_url, json={"osmosisPoints": int(assigned_score)})

if response.status_code == 200:

successful_updates += 1

if self.config['verbose']:

print(f"  ✓ 分数更新成功")

else:

failed_updates += 1

try:

error_data = response.json()

error_msg = str(error_data.get('osmosisPoints', ['未知错误'])[0])

if self.config['verbose']:

print(f"  ✗ 分数更新失败: {error_msg}")

except:

if self.config['verbose']:

print(f"  ✗ 分数更新失败: HTTP {response.status_code}")

except Exception as e:

failed_updates += 1

if self.config['verbose']:

print(f"  ✗ 更新异常: {str(e)}")

total_assigned += assigned_score

if self.config['verbose']:

print("-" * 50)

return df_with_scores, total_assigned, successful_updates, failed_updates

# ============================

# 主函数

# ============================

def main():

"""

主函数 - 两阶段处理：先筛选Alpha池，再打分分配

返回:

- DataFrame: 包含分配分数的Alpha数据

"""

# 配置日志

log_filename = f'competition_screener_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(

level=logging.INFO,

format='%(asctime)s - %(levelname)s - %(message)s',

handlers=[

logging.FileHandler(log_filename),

logging.StreamHandler()

]

)

# 初始化登录会话

try:

session = login()

print("✅ 登录成功")

except Exception as e:

logging.error(f"登录失败: {e}")

print("❌ 登录失败，请检查网络和凭据")

return []

print("\n" + "="*60)

print(" Osmosis比赛专用Alpha筛选与评分系统")

print("="*60)

# ============================================

# 第一阶段：Alpha池筛选配置

# ============================================

print("\n 第一阶段：Alpha池筛选")

print("-"*40)

# 筛选阶段配置

screener_config = {

'region': "IND",                    # 目标地区: USA(美国), EUR(欧洲), ASI(亚洲), GLB(全球), IND(印度)

'analysis_years': 4,                # 分析最近N年数据。值越大对长期稳定性要求越高，但可能排除新Alpha；值越小对近期表现更敏感，但可能忽视长期稳定性

'exclude_recent_years': 1,          # 排除最近N年数据。默认为1，排除最近1年不完整数据

'target_pool_size': 50,             # 最终要选择的Alpha数量。值越大筛选条件越宽松，值越小筛选条件越严格

'consultant_date': datetime(2025, 3, 11),  # 成为consultant的日期，用于筛选成为consultant后创建的Alpha

# 基础筛选阈值

'min_sharpe': 1.8,                  #最低夏普比率阈值。值越高筛选的Alpha风险调整后收益越好，但可能排除潜力Alpha；值越低条件越宽松，但收益质量可能下降

'min_fitness': 1.5,                 #最低Fitness阈值。值越高筛选的Alpha与市场相关性越好，但可能排除独立收益来源；值越低条件越宽松，但alpha质量可能不稳定

'max_drawdown': 15.0,               #最大回撤限制(绝对值)。值越低对风险控制越严格，但可能排除高波动高收益Alpha；值越高允许更大波动，但风险可能增加

'min_margin': 7.5,                  #最低保证金要求(百分比)。值越高筛选资本效率更高的Alpha，但可能排除需较多资金但表现好的Alpha；值越低条件越宽松

'min_turnover': 3.0,                # 最低换手率阈值。防止选择过于保守、交易不活跃的Alpha，值过低可能包含"僵尸"Alpha

'max_turnover': 40.0,               # 最高换手率阈值。防止选择过度交易、交易成本过高的Alpha，值过高可能包含交易成本侵蚀收益的Alpha

# 年度筛选阈值

'min_sharpe_ny_mean': 1.7,          # 最近N年夏普比率平均值阈值。评估长期表现稳定性，值越高对长期稳定性要求越严格，筛选出经得起时间考验的Alpha

'max_sharpe_ny_std': 0.8,           # 最近N年夏普比率标准差阈值。衡量年化表现的波动性，值越低要求表现越稳定，筛选出收益可预测性强的Alpha

'min_fitness_ny_mean': 1.4,         # 最近N年Fitness平均值阈值。评估长期alpha质量稳定性，值越高要求长期alpha质量越稳定

'min_positive_ratio': 0.6,          # 盈利年份占比阈值(0-1)。值越高要求盈利持续性越好，筛选出能持续产生正收益的Alpha

'min_available_years': 3,           # 最低可用年数。确保有足够的历史数据进行评估，值越高对数据完整性要求越高

# API配置

'batch_size': 5,                    # 批处理大小。值越大请求效率越高，但可能触发API限制；值越小对服务器压力越小，但耗时更长

'request_delay': 1,                 # 请求间隔秒数。防止API请求过于频繁，值太小可能被限制，值太大会降低效率

'max_retries': 3,                   # 最大重试次数。网络不稳定时自动重试，值越大容错性越好，但失败时等待时间更长

'initial_limit': 200,               # 初始收集Alpha数量。值越大候选池越大，找到优质Alpha概率越高，但处理时间越长

# 输出配置

'verbose': True,                    # 是否显示详细进度。True显示完整筛选过程，False只显示最终结果

}

# 创建筛选器

screener = CompetitionAlphaScreener(session, **screener_config)

# 构建Alpha池

alpha_pool = screener.build_alpha_pool()

if not alpha_pool:

print("❌ Alpha池为空，程序结束")

return []

print(f"✅ 第一阶段完成，获得 {len(alpha_pool)} 个优质Alpha")

# ============================================

# 第二阶段：Alpha打分配置

# ============================================

print("\n第二阶段：Alpha打分分配")

print("-"*40)

# 打分阶段配置

scorer_config = {

'allocation_method': 'weighted',    # 分配方法:

#   - 'softmax': 基于综合得分的指数概率分布，高分Alpha获得指数级更多分数，适合突出表现优异的Alpha

#   - 'rank': 基于排名进行指数衰减分配，保证每个Alpha都有基础分数，公平性强，适合追求稳健

#   - 'weighted': 加权组合方法，平衡softmax、rank和聚类的优点，适合综合考量多种因素

'total_score': 100000,              # 总分。分配给所有Alpha的总分数，代表要"投资"的总资金

# 方法参数

'softmax_temp': 0.1,                # softmax温度参数。控制softmax分布的"尖锐"程度：

#   - 值越低(如0.05): 分布越尖锐，高分Alpha获得更多分数，分配更集中

#   - 值越高(如0.5): 分布越平滑，分配更均匀

'min_base_score': 100,              # 最小基础分数。在使用rank方法时，每个Alpha至少获得的分数

'use_pca': True,                    # 是否使用PCA降维。在聚类分析前，是否使用主成分分析降维

# 权重配置

'weights': {                        # 在weighted方法中，各分配方法的混合权重

'softmax': 0.4,                 # softmax方法权重。40%权重给softmax方法

'rank': 0.3,                    # rank方法权重。30%权重给rank方法

'cluster': 0.3                  # 聚类调整权重。30%权重给聚类调整

},

'cluster_weight': 0.3,              # 聚类权重。聚类调整的强度：

#   - 值越大(如0.5): 聚类调整影响越大，不同类型Alpha获得更平衡的分数

#   - 值越小(如0.1): 聚类调整影响越小，分数分配更依赖原始得分

# 输出配置

'verbose': True,                    # 显示详细进度。控制程序运行时输出的详细程度

}

# 创建打分器

scorer = AlphaScorer(session, **scorer_config)

# 为Alpha池分配分数

df_with_scores, total_assigned, successful_updates, failed_updates = scorer.assign_scores_to_alphas(

alpha_pool,

scorer.config['allocation_method'],

scorer.config['total_score'],

analysis_years=screener_config['analysis_years']  # 传递分析年数

)

if df_with_scores.empty:

print("❌ 无法为Alpha池分配分数")

return []

# ============================================

# 结果统计

# ============================================

print("\n" + "="*60)

print("最终统计结果")

print("="*60)

print(f"总Alpha池数量: {len(alpha_pool)}")

print(f"总分配分数: {total_assigned} (目标: {scorer.config['total_score']})")

if total_assigned != scorer.config['total_score']:

print(f"分配分数不完整，差额: {scorer.config['total_score'] - total_assigned}")

if len(df_with_scores) > 0:

print(f"平均分数: {total_assigned/len(df_with_scores):.0f}")

print(f"最高分数: {df_with_scores['assigned_score'].max()}")

print(f"最低分数: {df_with_scores['assigned_score'].min()}")

print(f"中位数分数: {df_with_scores['assigned_score'].median():.0f}")

if len(df_with_scores) > 1:

print(f"分数标准差: {df_with_scores['assigned_score'].std():.0f}")

cv = df_with_scores['assigned_score'].std() / df_with_scores['assigned_score'].mean()

print(f"变异系数: {cv:.3f}")

print(f"API更新成功: {successful_updates} 个")

print(f"API更新失败: {failed_updates} 个")

# 分数分布

if len(df_with_scores) > 0:

print(f"\n分数分布")

print("-"*40)

score_bins = [0, 1000, 2000, 3000, 5000, 10000, float('inf')]

bin_labels = ['<1000', '1000-2000', '2000-3000', '3000-5000', '5000-10000', '>10000']

df_with_scores['score_bin'] = pd.cut(df_with_scores['assigned_score'], bins=score_bins, labels=bin_labels)

bin_counts = df_with_scores['score_bin'].value_counts().sort_index()

for bin_label, count in bin_counts.items():

percentage = count/len(df_with_scores)*100

bar_length = int(percentage/2)

bar = '█' * bar_length if bar_length > 0 else ''

print(f"{bin_label}: {count:3d}个alpha ({percentage:5.1f}%) {bar}")

# Top 10 Alpha详情

print(f"\n Top 10 Alpha详情")

print("-"*40)

top_10 = df_with_scores.head(10)

for i, (idx, alpha) in enumerate(top_10.iterrows(), 1):

alpha_id_short = alpha['id'][:12] + '...' if len(alpha['id']) > 12 else alpha['id']

print(f"{i:2d}. ID: {alpha_id_short}")

print(f"   综合得分: {alpha.get('composite_score', 0):.4f}")

print(f"   分配分数: {alpha['assigned_score']}")

print(f"   当前夏普: {alpha.get('sharpe', 0):.2f}")

# 动态获取N年夏普均值

analysis_years = screener_config['analysis_years']

sharpe_field = f'sharpe{analysis_years}Y'

if sharpe_field in alpha:

print(f"   {analysis_years}年夏普: {alpha.get(sharpe_field, 0):.2f}")

# 计算稳定性得分

if sharpe_field in alpha:

std_field = f'{sharpe_field}_std'

sharpe_std = alpha.get(std_field, 0)

stability_score = scorer.calculate_sharpe_stability_score(

alpha.get('sharpe', 0),

alpha.get(sharpe_field, 0),

sharpe_std

)

print(f"   稳定性分: {stability_score:.2f}")

print(f"\n详细日志已保存到: {log_filename}")

print("✅ 程序执行完成!")

print("="*60)

return df_with_scores

# ============================

# 主程序入口

# ============================

if __name__ == '__main__':

# 显示启动信息

print("\n" + "="*60)

print("Osmosis比赛专用Alpha筛选与评分系统")

print(f"版本: 3.2.5 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

print("="*60)

# 运行主程序

alphas = main()

---

## 讨论与评论 (3)

### 评论 #1 (作者: KH21822, 时间: 3个月前)

----------------------------------------------------------------------------------------------------------------------------------------------------

感谢您的分享

----------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #2 (作者: JR57542, 时间: 3个月前)

----------------------------------------------------------------------------------------------------------------------------------------------------

很有用，这就拿来试试

----------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #3 (作者: JL52079, 时间: 2个月前)

感谢大佬分享，大佬的代码实现了从自动筛选 、到测试其可更新性、再基于多维度指标计算综合得分，到按加权组合方法将总分合理分配给各Alpha，最后批量更新分数。一是流程完整，涵盖候选收集、基础筛选、可更新性验证、年度绩效过滤和动态打分，形成闭环。二是参数高度可配置，适应不同比赛策略。三是引入年度夏普均值和标准差来评估长期稳定性，避免只看近期表现。四是打分方法融合softmax、排名和聚类调整，兼顾头部突出与组合多样性。五是日志详尽，便于复盘。对于我这种新手小白来说简直不要太便利，再次感谢大佬的无私贡献，祝大佬永驻GM!

==================================just do it ！==================================

---

