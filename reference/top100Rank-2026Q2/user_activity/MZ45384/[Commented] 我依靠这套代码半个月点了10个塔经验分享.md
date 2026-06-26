# 我依靠这套代码，半个月点了10个塔经验分享

- **链接**: [Commented] 我依靠这套代码半个月点了10个塔经验分享.md
- **作者**: FZ98343
- **发布时间/热度**: 3个月前, 得票: 22

## 帖子正文

本人0126成为正式顾问，开始的一个月靠着使用打工人+AI聊天等工具制作模版回测，但效果始终不是很好，可能本身底子太薄，也没有深入研究用法，断断续续靠着打工人+其他AI工具，勉强点了两个塔；眼看同期的朋友群里讨论都点了好多塔，并且甚至进入了研究小组，在硬扛了半个月之后，不得不走上了一条搭建自己挖因子系统的道路，有付出总有收获，终于在上周跑通流程，并且略有小成，看到成果后，赶紧回来反哺社区，毕竟之前在社区跟各位大佬学到很多知识。

话不多说，直接上图+代码：（有疑问欢迎评论区交流，本代码还有很多优化的地方，也请大佬看后指点迷津）

1、半月提交 ![图片](images/img_497b86d5c4.png) 2、点塔数量 ![图片](images/img_eb184e4e1b.png)

3、运行日志

![图片](images/img_d79253cf39.png)

4、代码

#!/usr/bin/env python3

"""

Alpha Miner - 智能渐进式 Alpha 挖掘工具

批量处理1000个字段，每批10个

"""

import json

import sqlite3

import hashlib

import requests

import base64

import time

import pickle

from pathlib import Path

from datetime import datetime

from typing import List, Dict, Any, Optional, Tuple

import logging

from concurrent.futures import ThreadPoolExecutor, as_completed

from threading import Lock

# ============ 配置 ============

CONFIG = {

"region": "USA",

"delay": 1,

"universe": "TOP1000",

"category": "pv",

"theme": "true",

"instrument_type": "EQUITY",

# 筛选阈值

"min_sharpe_step1": 0.7,

"min_sharpe_step2": 0.7,

"min_sharpe_step3": 1.0,

"min_fitness": 0.5,

"max_turnover": 0.7,

# 提交条件

"submit_sharpe": 1.00,

"submit_fitness": 0.6,

"submit_turnover": 0.65,

# 限制

"max_fields_per_run": 10, # 默认先跑10个测试

"batch_size": 10, # 每批10个

"max_variants": 20, # 增加到20个变体

"concurrent_workers": 10, # 10并发

# 测试模式配置

"test_mode": True, # True=测试模式(10个), False=批量模式(1000个)

# ========== 回测配置 ==========

"simulation_settings": {

"truncation": 0.08,

"pasteurization": "ON",

"unit_handling": "VERIFY",

"nan_handling": "OFF",

"language": "FASTEXPR",

"visualization": False,

"test_period": "P0Y0M", # P0Y0M=10年, P0Y3M=7年, P0Y5M=5年

"max_trade": "OFF",

"max_position": "OFF",

},

# ========== 字段获取配置 ==========

"datafield_settings": {

"limit": 50, # 每次获取字段数

"offset": 0, # 起始偏移

},

}

DB_FILE = "0320/alpha_mining.db"

BASE_URL = " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) "

SESSION_FILE = "0320/brain_session.pkl"

# 设置日志

logging.basicConfig(

level=logging.DEBUG, # 改为DEBUG级别

format='%(asctime)s - %(levelname)s - %(message)s',

handlers=[

logging.FileHandler(f"0320/logs/mining_{datetime.now():%Y%m%d_%H%M%S}.log"),

logging.StreamHandler()

]

)

logger = logging.getLogger("AlphaMiner")

def save_session(session: requests.Session):

try:

with open(SESSION_FILE, 'wb') as f:

pickle.dump(session.cookies, f)

except Exception as e:

logger.warning(f"保存 session 失败: {e}")

def load_session(session: requests.Session) -> bool:

try:

if Path(SESSION_FILE).exists():

with open(SESSION_FILE, 'rb') as f:

cookies = pickle.load(f)

session.cookies.update(cookies)

returnTrue

except Exception as e:

logger.warning(f"加载 session 失败: {e}")

returnFalse

class BrainApiClient:

"""WorldQuant BRAIN API 客户端（支持 Session 持久化）"""

def __init__(self):

self.session = requests.Session()

self.session.headers.update({

'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

})

self.auth_credentials = None

self._lock = Lock()

if load_session(self.session):

logger.info("✓ 已加载之前的 session")

def authenticate(self, email: str, password: str, save: bool = True) -> Dict:

self.auth_credentials = {'email': email, 'password': password}

ifself.is_authenticated():

logger.info("✓ 使用已有 session，无需重新登录")

return {'status': 'authenticated', 'from_session': True}

logger.info("正在登录 BRAIN...")

self.session.cookies.clear()

credentials = f"{email}:{password}"

encoded = base64.b64encode(credentials.encode()).decode()

response = self.session.post(

f'{BASE_URL}/authentication',

headers={'Authorization': f'Basic {encoded}'}

)

if response.status_code == 201:

if save:

save_session(self.session)

logger.info("✓ 登录成功，session 已保存")

return {'status': 'authenticated', 'from_session': False}

else:

raise Exception(f"认证失败: {response.status_code}")

def is_authenticated(self) -> bool:

try:

response = self.session.get(f"{BASE_URL}/authentication", timeout=10)

return response.status_code == 200

except:

returnFalse

def ensure_auth(self):

withself._lock:

ifnotself.is_authenticated():

ifself.auth_credentials:

logger.info("Session 失效，重新登录...")

self.authenticate(self.auth_credentials['email'], self.auth_credentials['password'])

else:

raise Exception("未认证且无凭据")

def get_datasets(self, category: str = None) -> List[Dict]:

self.ensure_auth()

params = {

'instrumentType': CONFIG['instrument_type'],

'region': CONFIG['region'],

'delay': CONFIG['delay'],

'universe': CONFIG['universe'],

'theme': CONFIG['theme']

}

response = self.session.get(f"{BASE_URL}/data-sets", params=params)

response.raise_for_status()

data = response.json()

datasets = data.get('results', [])

if category:

datasets = [d for d in datasets if d.get('category', {}).get('id', '').lower() == category.lower()]

return datasets

def get_datafields(self, dataset_id: str) -> List[Dict]:

self.ensure_auth()

max_retries = 5

retry_delay = 3

for retry in range(max_retries):

try:

# 从CONFIG获取字段获取配置

field_cfg = CONFIG.get('datafield_settings', {})

params = {

'instrumentType': CONFIG['instrument_type'],

'region': CONFIG['region'],

'delay': str(CONFIG['delay']),

'universe': CONFIG['universe'],

'limit': str(field_cfg.get('limit', 50)),

'offset': str(field_cfg.get('offset', 0))

}

if dataset_id:

params['dataset.id'] = dataset_id

response = self.session.get(f"{BASE_URL}/data-fields", params=params)

if response.status_code == 429:

logger.warning(f" 429 请求过于频繁，{retry_delay}s 后重试 ({retry+1}/{max_retries})...")

time.sleep(retry_delay)

continue

response.raise_for_status()

return response.json().get('results', [])

except requests.exceptions.HTTPError as e:

if e.response.status_code == 400:

logger.warning(f" 数据集 {dataset_id} 在当前配置下不可用 (400错误)")

return []

if e.response.status_code == 429and retry < max_retries - 1:

logger.warning(f" 429 错误，{retry_delay}s 后重试 ({retry+1}/{max_retries})...")

time.sleep(retry_delay)

continue

raise

logger.error(f" 达到最大重试次数 ({max_retries})，放弃")

return []

def create_simulation(self, expression: str, decay: float = 0,

neutralization: str = "NONE", verbose: bool = True,

max_retries: int = 3) -> Optional[Dict]:

"""单个回测，带重试机制"""

self.ensure_auth()

if verbose:

logger.info(f" [回测配置] Expression: {expression[:80]}...")

logger.info(f" [回测配置] Region={CONFIG['region']}, Universe={CONFIG['universe']}, "

f"Delay={CONFIG['delay']}, Decay={decay}, Neutralization={neutralization}")

# 从CONFIG获取回测配置

sim_cfg = CONFIG.get('simulation_settings', {})

data = {

'type': 'REGULAR',

'settings': {

'instrumentType': CONFIG['instrument_type'],

'region': CONFIG['region'],

'universe': CONFIG['universe'],

'delay': CONFIG['delay'],

'decay': decay,

'neutralization': neutralization,

'truncation': sim_cfg.get('truncation', 0.08),

'pasteurization': sim_cfg.get('pasteurization', 'ON'),

'unitHandling': sim_cfg.get('unit_handling', 'VERIFY'),

'nanHandling': sim_cfg.get('nan_handling', 'OFF'),

'language': sim_cfg.get('language', 'FASTEXPR'),

'visualization': sim_cfg.get('visualization', False),

'testPeriod': sim_cfg.get('test_period', 'P0Y0M'),

'maxTrade': sim_cfg.get('max_trade', 'OFF'),

'maxPosition': sim_cfg.get('max_position', 'OFF'),

},

'regular': expression

}

# 重试机制

for retry in range(max_retries):

try:

if retry > 0:

logger.info(f" 第 {retry+1} 次重试...")

time.sleep(2 ** retry)

response = self.session.post(f"{BASE_URL}/simulations", json=data)

if response.status_code == 429:

logger.warning(f" 429 请求过于频繁，等待 {2 ** retry}s 后重试...")

time.sleep(2 ** retry)

continue

response.raise_for_status()

break

except requests.exceptions.HTTPError as e:

if e.response.status_code == 429:

logger.warning(f" 429 错误，等待后重试...")

time.sleep(2 ** retry)

if retry == max_retries - 1:

logger.error(f" 达到最大重试次数，放弃")

returnNone

continue

logger.error(f" HTTP 错误: {e}")

returnNone

except Exception as e:

logger.error(f" 请求异常: {e}")

returnNone

else:

returnNone

location = response.headers.get('Location')

ifnot location:

logger.warning(" 没有返回 Location 头")

returnNone

# 等待完成

for attempt in range(80):

try:

resp = self.session.get(location)

if resp.status_code == 200:

retry = resp.headers.get('Retry-After', 0)

if float(retry) == 0:

sim_data = resp.json()

alpha_id = sim_data.get('alpha')

if alpha_id:

# 获取 alpha 详细信息

alpha_resp = self.session.get(f"{BASE_URL}/alphas/{alpha_id}")

if alpha_resp.status_code == 200:

alpha_data = alpha_resp.json()

# 从 alpha_data['is'] 中获取性能指标

is_data = alpha_data.get('is', {})

if is_data:

perf_data = {

'sharpe': is_data.get('sharpe'),

'fitness': is_data.get('fitness'),

'turnover': is_data.get('turnover')

}

alpha_data['performance'] = perf_data

if verbose:

logger.info(f" [性能指标] Sharpe={perf_data.get('sharpe', 'N/A')}, "

f"Fitness={perf_data.get('fitness', 'N/A')}, "

f"Turnover={perf_data.get('turnover', 'N/A')}")

else:

logger.warning(f" 未找到性能数据 (is字段为空)")

if verbose:

logger.info(f" [Alpha ID] {alpha_id}")

return alpha_data

else:

logger.warning(f" 获取 Alpha 详情失败: {alpha_resp.status_code}")

else:

logger.warning(" 模拟完成但没有 alpha ID")

break

time.sleep(float(retry))

else:

time.sleep(2)

except Exception as e:

logger.error(f" 等待结果时出错: {e}")

time.sleep(2)

returnNone

class DB:

def __init__(self, clear_existing=True):

Path(DB_FILE).parent.mkdir(exist_ok=True)

Path("0320/logs").mkdir(exist_ok=True)

self.init_tables(clear_existing=clear_existing)

def conn(self):

c = sqlite3.connect(DB_FILE)

c.row_factory = sqlite3.Row

return c

def init_tables(self, clear_existing=True):

withself.conn() as c:

if clear_existing:

# 清空现有数据

c.execute("DELETE FROM fields")

c.execute("DELETE FROM mining_log")

c.execute("DELETE FROM good_alphas")

c.execute("DELETE FROM tested_combinations")

logger.info("✓ 已清空数据库表")

c.executescript("""

CREATE TABLE IF NOT EXISTS fields (

field_id TEXT PRIMARY KEY,

region TEXT,

dataset TEXT,

field_name TEXT,

theme TEXT

);

CREATE TABLE IF NOT EXISTS mining_log (

id INTEGER PRIMARY KEY AUTOINCREMENT,

field_name TEXT,

step INTEGER,

expression TEXT,

sharpe REAL, fitness REAL, turnover REAL,

status TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS good_alphas (

hash TEXT PRIMARY KEY,

expr TEXT,

region TEXT,

sharpe REAL, fitness REAL, turnover REAL,

alpha_id TEXT,

submitted INTEGER DEFAULT 0

);

CREATE TABLE IF NOT EXISTS tested_combinations (

id INTEGER PRIMARY KEY AUTOINCREMENT,

field_name TEXT,

expression TEXT,

region TEXT,

universe TEXT,

delay INTEGER,

tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

UNIQUE(field_name, expression, region, universe, delay)

);

""")

def save_field(self, region, dataset, field):

fid = f"{region}_{dataset}_{field}"

withself.conn() as c:

c.execute(

"INSERT OR IGNORE INTO fields (field_id, region, dataset, field_name, theme) VALUES (?,?,?,?,?)",

(fid, region, dataset, field, "")

)

def log_step(self, field_name: str, step: int, expression: str,

result: Optional[Dict], status: str):

"""记录每一步的结果"""

sharpe = 0.0

fitness = 0.0

turnover = 0.0

if result:

perf = result.get('performance', {})

if perf:

sharpe = float(perf.get('sharpe', 0))

fitness = float(perf.get('fitness', 0))

turnover = float(perf.get('turnover', 0))

withself.conn() as c:

c.execute("""

INSERT INTO mining_log (field_name, step, expression, sharpe, fitness, turnover, status)

VALUES (?, ?, ?, ?, ?, ?, ?)

""", (field_name, step, expression[:200], sharpe, fitness, turnover, status))

return sharpe, fitness, turnover

def is_tested(self, field_name: str, expression: str) -> bool:

withself.conn() as c:

cursor = c.execute("""

SELECT 1 FROM tested_combinations

WHERE field_name=? AND expression=? AND region=? AND universe=? AND delay=?

""", (field_name, expression, CONFIG['region'], CONFIG['universe'], CONFIG['delay']))

return cursor.fetchone() isnotNone

def mark_tested(self, field_name: str, expression: str):

withself.conn() as c:

c.execute("""

INSERT OR IGNORE INTO tested_combinations (field_name, expression, region, universe, delay)

VALUES (?, ?, ?, ?, ?)

""", (field_name, expression, CONFIG['region'], CONFIG['universe'], CONFIG['delay']))

class AlphaVariantGenerator:

"""生成 Alpha 变体"""

REGION_SETTINGS = {

"USA": {"decays": [0, 3, 10, 20], "neutralizations": ["FAST", "MARKET", "SECTOR"]}

}

# 基于operator.json的算子，设计20个有经济学意义的模板

COMPLEX_TEMPLATES = [

# ========== 1. 均值回归类 ==========

("rank(ts_zscore({f}, 20))", "Zscore标准化"),

("rank(ts_zscore(ts_mean({f}, 5), 20))", "短期均值Zscore"),

("rank(-ts_zscore(ts_mean({f}, 60), 252))", "长期均值反转"),

("rank(ts_zscore(winsorize({f}), 60))", "稳健Zscore去极值"),

# ========== 2. 动量趋势类 ==========

("rank(ts_delta({f}, 5))", "5日动量"),

("rank(ts_delta({f}, 20))", "20日动量"),

("rank(ts_delta({f}, 5) / ts_mean({f}, 20))", "动量强度比"),

("rank(ts_mean({f}, 5) / ts_mean({f}, 20))", "短长均线比"),

("rank(ts_decay_linear(ts_zscore({f}, 60), 10))", "衰减加权动量"),

("rank(ts_decay_linear({f}, 20))", "线性衰减趋势"),

# ========== 3. 波动率调整类 ==========

("rank(ts_zscore({f}, 20) / ts_std_dev({f}, 60))", "夏普比率型"),

("rank(ts_delta({f}, 5) / ts_std_dev({f}, 20))", "标准化动量"),

("rank(signed_power(ts_delta({f}, 5), 0.5))", "波动率压缩"),

("rank(ts_av_diff({f}, 20))", "均值偏离"),

# ========== 4. 量价结合类 ==========

("rank(ts_corr({f}, ts_delta({f}, 1), 20))", "自相关趋势"),

("rank(ts_covariance({f}, ts_mean({f}, 5), 20))", "协方差趋势"),

("rank(ts_regression({f}, ts_step(), 60, 0, 0))", "时间回归斜率"),

("rank(ts_quantile({f}, 60))", "分位数排名"),

# ========== 5. 极端值/反转类 ==========

("rank(if_else(ts_zscore({f}, 20) > 2, -1, if_else(ts_zscore({f}, 20) < -2, 1, 0)))", "极端值反转"),

("rank(ts_arg_max({f}, 60) - ts_arg_min({f}, 60))", "极值位置差"),

("rank(ts_kurtosis({f}, 60))", "峰度异常"),

("rank(ts_count_nans({f}, 20))", "缺失值模式"),

]

def __init__(self):

self.settings = self.REGION_SETTINGS.get(CONFIG['region'], self.REGION_SETTINGS["USA"])

import random

self.random = random

self.random.seed(42)

def generate_variants(self, field: str) -> List[Tuple[str, float, str, str]]:

variants = []

decays = self.settings["decays"]

neus = self.settings["neutralizations"]

variants.append((f"rank(ts_zscore(winsorize({field}), 20))", decays[0], neus[0], "基础优化"))

selected_templates = self.random.sample(self.COMPLEX_TEMPLATES, min(3, len(self.COMPLEX_TEMPLATES)))

for tmpl, desc in selected_templates:

variants.append((tmpl.format(f=field), decays[1], neus[0], desc))

variants.append((f"rank(ts_mean(ts_zscore({field}, 20), 5))", decays[2], neus[0], "平滑动量"))

complex_expr = selected_templates[0][0].format(f=field)

variants.append((complex_expr, decays[1], neus[1] if len(neus) > 1 else neus[0], "中性化"))

variants.append((f"rank(-ts_zscore(ts_mean({field}, 60), 252))", decays[3], neus[0], "长周期反转"))

if len(variants) < CONFIG['max_variants']:

variants.append((

f"rank(ts_zscore({field}, 20) + 0.5 * ts_zscore(ts_delta({field}, 5), 20))",

decays[2], neus[0], "综合信号"

))

return variants[:CONFIG['max_variants']]

class SmartAlphaMiner:

"""智能渐进式 Alpha 挖掘器"""

def __init__(self, clear_db=True):

self.db = DB(clear_existing=clear_db)

self.client = BrainApiClient()

self.variant_gen = AlphaVariantGenerator()

self.stats = {

'total_fields': 0,

'step1_pass': 0,

'step2_pass': 0,

'step3_pass': 0,

'variants_tested': 0,

'submittable': 0

}

self._lock = Lock()

def log_summary(self):

logger.info("=" * 60)

logger.info("挖掘统计摘要")

logger.info("=" * 60)

logger.info(f"总测试字段数: {self.stats['total_fields']}")

logger.info(f"Step1 通过 (原始): {self.stats['step1_pass']}")

logger.info(f"Step2 通过 (去极值): {self.stats['step2_pass']}")

logger.info(f"Step3 通过 (完整处理): {self.stats['step3_pass']}")

logger.info(f"变体测试数: {self.stats['variants_tested']}")

logger.info(f"可提交 Alpha: {self.stats['submittable']}")

logger.info("=" * 60)

def test_field_step1(self, field: Dict) -> Optional[Tuple[Dict, Dict]]:

"""测试 Step 1，返回 (field_info, result)"""

field_name = field['field_name']

# 直接用字段，不加rank

expr = field_name

logger.info(f"\n[Step1] 字段: {field_name}")

logger.info(f" 表达式: {expr}")

result = self.client.create_simulation(expr, verbose=True) # 打开详细日志

ifnot result:

logger.info(f" ✗ Step1 无结果，跳过该字段")

returnNone

perf = result.get('performance', {})

sharpe = float(perf.get('sharpe', 0)) if perf else 0

fitness = float(perf.get('fitness', 0)) if perf else 0

turnover = float(perf.get('turnover', 0)) if perf else 0

logger.info(f" [Step1 结果] Sharpe={sharpe:.3f}, Fitness={fitness:.3f}, Turnover={turnover:.3f}")

logger.info(f" [Step1 阈值] Sharpe >= {CONFIG['min_sharpe_step1']}")

passed = sharpe >= CONFIG['min_sharpe_step1']

self.db.log_step(field_name, 1, expr, result, "PASS"if passed else"FAIL")

if passed:

logger.info(f" ✓ Step1 PASS")

withself._lock:

self.stats['step1_pass'] += 1

return (field, result)

else:

logger.info(f" ✗ Step1 FAIL: Sharpe {sharpe:.3f} < {CONFIG['min_sharpe_step1']}")

returnNone

def test_variant(self, variant: Dict) -> bool:

"""测试单个变体"""

field_name = variant['field_name']

expr = variant['expr']

decay = variant['decay']

neu = variant['neu']

desc = variant['desc']

logger.info(f"[变体] {field_name} - {desc}: {expr[:60]}...")

result = self.client.create_simulation(expr, decay=decay, neutralization=neu, verbose=False)

withself._lock:

self.stats['variants_tested'] += 1

ifnot result:

logger.info(f" ✗ 无结果")

returnFalse

perf = result.get('performance', {})

sharpe = float(perf.get('sharpe', 0)) if perf else 0

fitness = float(perf.get('fitness', 0)) if perf else 0

turnover = float(perf.get('turnover', 0)) if perf else 0

logger.info(f" 结果: Sharpe={sharpe:.3f}, Fitness={fitness:.3f}, Turnover={turnover:.3f}")

self.db.log_step(field_name, 4, expr, result, "PASS"if sharpe >= CONFIG['submit_sharpe'] else"FAIL")

meets_submit = (sharpe >= CONFIG['submit_sharpe'] and

fitness >= CONFIG['submit_fitness'] and

turnover <= CONFIG['submit_turnover'])

if meets_submit:

logger.info(f" ★★★ 达到提交条件!")

self.db.save_good_alpha(expr, result)

withself._lock:

self.stats['submittable'] += 1

returnTrue

else:

fail_reasons = []

if sharpe < CONFIG['submit_sharpe']:

fail_reasons.append(f"Sharpe不足")

if fitness < CONFIG['submit_fitness']:

fail_reasons.append(f"Fitness不足")

if turnover > CONFIG['submit_turnover']:

fail_reasons.append(f"Turnover过高")

logger.info(f" ✗ {', '.join(fail_reasons)}")

returnFalse

def run(self, email: str, password: str, max_fields: int = None):

"""运行完整挖掘流程 - 每批10个字段，达标的立即执行变体"""

max_fields = max_fields or CONFIG['max_fields_per_run']

batch_size = CONFIG['batch_size']

logger.info("=" * 60)

logger.info("Alpha Miner - 智能渐进式挖掘")

logger.info("=" * 60)

logger.info(f"配置: Region={CONFIG['region']}, Universe={CONFIG['universe']}, "

f"Delay={CONFIG['delay']}, Category={CONFIG['category']}")

logger.info(f"目标字段数: {max_fields}, 每批: {batch_size}")

logger.info(f"流程: 每批{batch_size}个字段并行Step1 -> 达标的串行执行变体 -> 下一批")

logger.info("=" * 60)

self.client.authenticate(email, password)

logger.info("✓ 认证成功\n")

# 获取数据集和字段

logger.info("获取数据集...")

datasets = self.client.get_datasets(CONFIG['category'])

logger.info(f"找到 {len(datasets)} 个 {CONFIG['category']} 类别数据集")

all_fields = []

for ds in datasets:

ds_id = ds.get('id')

logger.info(f" 获取 {ds_id} 的字段...")

fields = self.client.get_datafields(ds_id)

for f in fields:

field_name = f.get('id') or f.get('name')

all_fields.append({

'field_name': field_name,

'dataset': ds_id

})

self.db.save_field(CONFIG['region'], ds_id, field_name)

logger.info(f" 保存了 {len(fields)} 个字段，累计 {len(all_fields)}")

if len(all_fields) >= max_fields:

break

# 限制字段数

all_fields = all_fields[:max_fields]

logger.info(f"\n总共收集 {len(all_fields)} 个字段")

ifnot all_fields:

logger.error("没有获取到任何字段")

return0

# 分批处理：每批10个，先并行Step1，达标的立即执行变体

total_batches = (len(all_fields) + batch_size - 1) // batch_size

logger.info(f"\n将分 {total_batches} 批处理，每批流程:")

logger.info(f" 1. 并行执行{batch_size}个字段的Step1")

logger.info(f" 2. 达标的字段串行执行10个变体")

logger.info(f" 3. 进入下一批\n")

for batch_idx in range(total_batches):

start = batch_idx * batch_size

end = min(start + batch_size, len(all_fields))

batch_fields = all_fields[start:end]

logger.info(f"\n{'='*80}")

logger.info(f"【第 {batch_idx+1}/{total_batches} 批】字段 {start+1}-{end}")

logger.info(f"{'='*80}")

# Step 1: 批量并行测试这10个字段

logger.info(f"\n>> Step1: 并行测试{batch_size}个字段...")

passed_step1 = []

with ThreadPoolExecutor(max_workers=CONFIG['concurrent_workers']) as executor:

futures = {executor.submit(self.test_field_step1, field): field for field in batch_fields}

for future in as_completed(futures):

try:

result = future.result()

if result:

passed_step1.append(result[0])

except Exception as e:

logger.error(f"测试出错: {e}")

logger.info(f"\n>> Step1 完成: {len(passed_step1)}/{len(batch_fields)} 个字段达标")

# Step 4: 收集所有变体，批量并发测试

if passed_step1:

all_variants = []

for field in passed_step1:

field_name = field['field_name']

variants = self.variant_gen.generate_variants(field_name)

for expr, decay, neu, desc in variants:

all_variants.append({

'field': field,

'field_name': field_name,

'expr': expr,

'decay': decay,

'neu': neu,

'desc': desc

})

logger.info(f"\n>> 变体测试: {len(passed_step1)}个字段共{len(all_variants)}个变体，10并发执行...")

# 并发测试所有变体

with ThreadPoolExecutor(max_workers=10) as executor:

futures = {executor.submit(self.test_variant, v): v for v in all_variants}

for future in as_completed(futures):

try:

future.result()

except Exception as e:

logger.error(f"变体测试出错: {e}")

else:

logger.info(f"\n>> 本批无达标字段，跳过变体测试")

logger.info(f"\n>> 【第{batch_idx+1}批完成】")

# 所有批次完成后打印统计

self.log_summary()

self.view_submittable_alphas()

returnself.stats['submittable']

def view_submittable_alphas(self):

withself.db.conn() as c:

c.row_factory = sqlite3.Row

alphas = [dict(r) for r in c.execute("SELECT * FROM good_alphas WHERE region=?", (CONFIG['region'],))]

ifnot alphas:

logger.info("\n没有可提交的 Alpha")

return

logger.info(f"\n{'='*60}")

logger.info(f"可提交 Alpha 列表 (共 {len(alphas)} 个)")

logger.info('='*60)

for a in alphas:

logger.info(f"\n表达式: {a['expr'][:70]}...")

logger.info(f"Sharpe: {a['sharpe']:.3f}, Fitness: {a['fitness']:.3f}, Turnover: {a['turnover']:.3f}")

def main():

import argparse

parser = argparse.ArgumentParser(description="智能 Alpha 挖掘工具")

parser.add_argument("--run", action="store_true", help="运行完整挖掘流程")

parser.add_argument("--email", required=True, help="BRAIN 邮箱")

parser.add_argument("--password", required=True, help="BRAIN 密码")

parser.add_argument("--region", default="USA", help="地区")

parser.add_argument("--universe", default="TOP1000", help="Universe")

parser.add_argument("--category", default="pv", help="数据集类别")

# 模式选择

parser.add_argument("--test", action="store_true", help="测试模式: 只跑10个字段验证")

parser.add_argument("--full", action="store_true", help="批量模式: 跑1000个字段")

parser.add_argument("--max-fields", type=int, default=None, help="最大测试字段数(覆盖模式)")

parser.add_argument("--batch-size", type=int, default=10, help="每批字段数")

parser.add_argument("--workers", type=int, default=3, help="并发数")

parser.add_argument("--clear-db", action="store_true", help="清空数据库（默认保留）")

# 回测配置覆盖

parser.add_argument("--truncation", type=float, default=None, help="截断值 (默认0.08)")

parser.add_argument("--test-period", type=str, default=None, help="测试周期: P0Y0M=10年, P0Y3M=7年")

parser.add_argument("--pasteurization", type=str, default=None, help="Pasteurization: ON/OFF")

# 字段获取配置覆盖

parser.add_argument("--field-limit", type=int, default=None, help="每数据集获取字段数 (默认50)")

args = parser.parse_args()

CONFIG['region'] = args.region

CONFIG['universe'] = args.universe

CONFIG['category'] = args.category

CONFIG['batch_size'] = args.batch_size

CONFIG['concurrent_workers'] = args.workers

# 应用回测配置覆盖

if args.truncation isnotNone:

CONFIG['simulation_settings']['truncation'] = args.truncation

if args.test_period isnotNone:

CONFIG['simulation_settings']['test_period'] = args.test_period

if args.pasteurization isnotNone:

CONFIG['simulation_settings']['pasteurization'] = args.pasteurization

# 应用字段获取配置覆盖

if args.field_limit isnotNone:

CONFIG['datafield_settings']['limit'] = args.field_limit

# 模式判断

if args.full:

CONFIG['test_mode'] = False

CONFIG['max_fields_per_run'] = 1000

logger.info("=" * 60)

logger.info("【批量模式】将测试 1000 个字段")

logger.info("=" * 60)

elif args.test or (not args.max_fields and CONFIG['test_mode']):

CONFIG['test_mode'] = True

CONFIG['max_fields_per_run'] = 10

logger.info("=" * 60)

logger.info("【测试模式】将测试 10 个字段验证流程")

logger.info(" 确认无误后，使用 --full 参数跑批量模式")

logger.info("=" * 60)

# 命令行参数覆盖

if args.max_fields:

CONFIG['max_fields_per_run'] = args.max_fields

miner = SmartAlphaMiner(clear_db=args.clear_db)

if args.run:

miner.run(args.email, args.password)

else:

parser.print_help()

if __name__ == "__main__":

main()

---

## 讨论与评论 (19)

### 评论 #1 (作者: BL59663, 时间: 2个月前)

大佬，这个代码缩进改的我怀疑人生了。。。

---

### 评论 #2 (作者: QL88701, 时间: 2个月前)

十分感谢！！这是直接把焚决交出来了！！！

===================================================

每日谨记：提交因子不能抱侥幸心理！！坚持一定会有结果！！

守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”
无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。===================================================

---

### 评论 #3 (作者: JZ74499, 时间: 2个月前)

贴主运行的时候只采样模板而非数据集吗？这样每天5000个回测是怎么做到同时点多个数据集的塔的？

---

### 评论 #4 (作者: CC52425, 时间: 2个月前)

大佬， 是直接跑  Categories 这个大类吗，会不会数据字段太多，

---

### 评论 #5 (作者: CZ78575, 时间: 2个月前)

==================================================================================

好东西，点塔王

----------    好东西，快把这个代码给我啊==================================================================================

---

### 评论 #6 (作者: HZ99685, 时间: 2个月前)

没有过滤margin吗？

---

### 评论 #7 (作者: WX31897, 时间: 2个月前)

有对应的数据库的表结构等配置文档吗？

---

### 评论 #8 (作者: XE68375, 时间: 2个月前)

大佬，代码复制出来，格式都乱的，能整一个可以直接运行的代码吗？谢谢

---

### 评论 #9 (作者: DR82688, 时间: 2个月前)

不错等下试试，研究一下一起进步。

---

### 评论 #10 (作者: YS63181, 时间: 2个月前)

你好，跑不起来，可以粘贴完整的吗？祝vf天天1.0

---

### 评论 #11 (作者: SZ20589, 时间: 2个月前)

感谢大佬分享模板，我试试看能不能出好的因子。

=============================================================================

========Genius is one percent inspiration and ninety-nine percent perspiration.=============

==============================================================================

---

### 评论 #12 (作者: FF65210, 时间: 2个月前)

感谢分享，点塔困难户非常需要这个，一起加油进步。

===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================

---

### 评论 #13 (作者: JZ74499, 时间: 2个月前)

我把代码用AI格式化一下跑起来了，只能说很失望：

整套代码里面连vector变量都没有处理的环节

初始字段直接中性化None开跑，设的门槛除非β字段否则别想第一步过筛

整套代码没有处理vector字段的环节

总结：就这真能在回测数量大幅限制的背景下点10个塔？我很怀疑

---

### 评论 #14 (作者: JL52079, 时间: 2个月前)

大佬，我改了格式后，能运行，但是不管换什么数据集，都获取不到字段，求指点！
输出结果如下：

2026-04-10 20:53:41,769 - INFO - ============================================================
2026-04-10 20:53:41,769 - INFO - 【测试模式】将测试 10 个字段验证流程
2026-04-10 20:53:41,772 - INFO -  确认无误后，使用 --full 参数跑批量模式
2026-04-10 20:53:41,772 - INFO - ============================================================
2026-04-10 20:53:41,772 - INFO - ✓ 已加载之前的 session
2026-04-10 20:53:41,772 - INFO - ============================================================
2026-04-10 20:53:41,772 - INFO - Alpha Miner - 智能渐进式挖掘
2026-04-10 20:53:41,772 - INFO - ============================================================
2026-04-10 20:53:41,772 - INFO - 配置: Region=USA, Universe=TOP3000, Delay=1, Category=pv1
2026-04-10 20:53:41,777 - INFO - 目标字段数: 10, 每批: 10
2026-04-10 20:53:41,777 - INFO - 流程: 每批10个字段并行Step1 -> 达标的并行变体测试
2026-04-10 20:53:41,777 - INFO - ============================================================
2026-04-10 20:53:44,275 - INFO - ✓ 使用已有 session，无需重新登录
2026-04-10 20:53:44,275 - INFO - ✓ 认证成功

2026-04-10 20:53:44,275 - INFO - 获取数据集...
2026-04-10 20:53:44,955 - INFO - 找到 0 个 pv1 类别数据集
2026-04-10 20:53:44,955 - INFO -
总共收集 0 个字段
2026-04-10 20:53:44,955 - ERROR - 没有获取到任何字段

---

### 评论 #15 (作者: FZ60707, 时间: 2个月前)

有几点建议：

1.代码缺失 save_good_alpha 方法，达标 Alpha 无法入库，跑不通主流程。

2.字段获取不分页，每个数据集只取前 50 个，遗漏大量可用字段。

3.默认 10 并发太高，极易触发 BRAIN 限流 429，建议降到 2~3 并加间隔。

4.去重机制定义了却未调用，相同表达式会重复回测，浪费配额。

5.表达式模板固化且随机种子固定，长期挖掘缺乏新意，建议外部配置模板。

==================================================================================================================================================================

---

### 评论 #16 (作者: YS60917, 时间: 2个月前)

可以指定只跑特定数据集吗

---

### 评论 #17 (作者: XH71987, 时间: 2个月前)

修改格式以后同样是无法获取数据集

---

### 评论 #18 (作者: CZ78575, 时间: 2个月前)

==================================================================================

好东西，跑起来试试

----------    好东西，快把这个代码给我啊==================================================================================

---

### 评论 #19 (作者: MZ45384, 时间: 1个月前)

是新人大佬，刚来就搭建了自己的alpha系统，十分厉害。祝大佬蒸蒸日上。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

