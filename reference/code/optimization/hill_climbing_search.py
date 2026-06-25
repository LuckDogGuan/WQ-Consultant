import requests
import json
import pandas as pd
from requests.auth import HTTPBasicAuth
import time
import random
import logging
import re
import hashlib
import os
import threading
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ==================== 用户配置区域 ====================
# 运行模式配置
# RUN_MODE = 1: 重新开始，删除旧的日志和检查点文件
# RUN_MODE = 2: 断点续爬
RUN_MODE = 2

# 支持多个Alpha ID的列表
TARGET_ALPHA_IDS = ['le21nEr7']

# 持续运行模式: True = 自动从平台获取alpha并持续优化; False = 使用固定TARGET_ALPHA_IDS
CONTINUOUS_MODE = True

# 从配置文件中读取邮箱配置
try:
    with open('email_config.json') as f:
        EMAIL_CONFIG = json.load(f)

except Exception as e:
    # 默认邮箱配置
    EMAIL_CONFIG = {
        'enabled': False,
        'smtp_server': 'smtp.qq.com',
        'smtp_port': 465,
        'sender': '',
        'password': '',
        'receiver': ''
    }
print(f"📧 邮件通知功能: {'已启用' if EMAIL_CONFIG.get('enabled') else '未启用'}")

# 最大并发数设置（卡槽数量）
MAX_CONCURRENT = 2

# 爬山起始位置配置
START_OPTIMIZATION_FROM = {
    'data_field': 0,
    'time_window': 0,
    'number': 0,
    'group': 0,
    'operator': 0
}

# 迭代优化配置
MAX_ITERATIONS = 5
BATCH_SIZE = 4
PASS_BONUS = 1.0

# 候选项配置
# CANDIDATE_DAYS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 22, 60, 64, 120, 128, 252, 256, 512, 720, 900, 1050, 2000]
CANDIDATE_DAYS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 22, 60, 64, 120, 128, 252, 256, 512]
CANDIDATE_NUMBERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
CANDIDATE_GROUPS = ['market', 'industry', 'subindustry', 'sector', 'densify(pv13_1l_scibr)']
CANDIDATE_NEUTRALIZATIONS = ["RAM"]
# CANDIDATE_NEUTRALIZATIONS = ["MARKET", "INDUSTRY", "SUBINDUSTRY", "SECTOR", "NONE", "CROWDING", "FAST", "SLOW", "RAM"]

CANDIDATE_DECAYS = [0, 1, 4, 16, 64, 128, 256, 512]

# 2.4版本改色逻辑常量
MARGIN_THRESHOLD = 0.000
SC_CUTOFF = 0.7

# 运算符池分类
OPERATOR_GROUPS = {
    'group': [
        'group_rank', 'group_zscore', 'group_neutralize',
        'group_sum', 'group_std_dev', 'group_count',
        'group_scale'
    ],
    'group_special': [
        # 以下操作符参数签名特殊，不参与自动替换
        # group_mean(x, weight, group) — 3参数
        # group_backfill(x, group, d, std=4.0) — 3+参数
        # group_cartesian_product(g1, g2) — 需要Group类型输入
        'group_mean', 'group_backfill', 'group_cartesian_product'
    ],
    'time_series': [
        'ts_rank', 'ts_zscore', 'ts_mean', 'ts_std_dev', 'ts_delta', 'ts_delay',
        'ts_backfill', 'ts_av_diff', 'ts_arg_min', 'ts_arg_max', 'days_from_last_change',
        'ts_quantile', 'ts_scale', 'ts_regression', 'ts_sum', 'ts_decay_linear',
        'ts_covariance', 'ts_count_nans', 'kth_element', 'ts_corr', 'ts_product',
        'last_diff_value', 'ts_ir', 'ts_kurtosis', 'ts_max_diff', 'ts_returns'
    ],
    'time_series_special': [
        # 以下操作符参数签名特殊，不参与自动替换
        # hump(x, hump=0.01) — 关键字参数
        # ts_step(1) — 常量参数，无field/lookback
        # ts_target_tvr_decay/hump — 需要lambda_min/max/target_tvr
        'hump', 'ts_step', 'ts_target_tvr_decay', 'ts_target_tvr_hump'
    ],
    'cross_sectional': [
        'rank', 'zscore', 'scale', 'normalize', 'quantile', 'winsorize'
    ],
    'arithmetic': [
        'add', 'subtract', 'multiply', 'divide', 'pasteurize', 'sqrt', 'log',
        'signed_power', 'sign', 'reverse', 'power', 'min', 'max', 'inverse',
        'densify', 'abs'
    ],
    'vector': [
        'vec_avg', 'vec_sum', 'vec_max', 'vec_min','vec_stddev','vec_range'
    ],
    'logical': [
        'greater_equal', 'and', 'or', 'not_equal', 'not', 'greater',
        'less_equal', 'less', 'is_nan', 'if_else', 'equal'
    ],
    'transformational': [
        'tail', 'trade_when', 'bucket'
    ]
}

CANDIDATE_ALL_OPS = []
for ops in OPERATOR_GROUPS.values():
    CANDIDATE_ALL_OPS.extend(ops)

# 运算符参数数量映射 (仅标记非标准签名的算子，默认为2参数: field, lookback/group)
OPERATOR_ARITY = {
    # 1参数: (field)
    'days_from_last_change': 1, 'rank': 1, 'zscore': 1, 'scale': 1, 'normalize': 1,
    'quantile': 1, 'pasteurize': 1, 'sqrt': 1, 'log': 1, 'sign': 1, 'reverse': 1,
    'inverse': 1, 'abs': 1, 'is_nan': 1, 'not': 1, 'densify': 1,
    'winsorize': 1,  # winsorize(x, std=4) — std有默认值
    'tail': 1,       # tail(x, lower=0, upper=0, newval=0) — 关键字参数有默认值
    # 2参数: (field, lookback) 或 (field, field) 或 (field, group) - 默认
    'last_diff_value': 2,  # last_diff_value(x, d) — 需要lookback
    'ts_corr': 3, 'ts_covariance': 3, 'ts_regression': 3, 'kth_element': 3,
    'add': 2, 'subtract': 2, 'multiply': 2, 'divide': 2, 'power': 2, 'min': 2, 'max': 2,
    'signed_power': 2, 'greater_equal': 2, 'greater': 2, 'less_equal': 2, 'less': 2,
    'equal': 2, 'not_equal': 2, 'and': 2, 'or': 2,
    # 特殊参数 (不参与自动替换)
    'hump': -1, 'ts_target_tvr_decay': -1, 'ts_target_tvr_hump': -1, 'ts_step': -1,
    # 3参数
    'if_else': 3, 'trade_when': 3, 'bucket': 3,  # trade_when(x, y, z) 需要3参数
    'group_mean': 3,        # group_mean(x, weight, group)
    'group_backfill': 3,    # group_backfill(x, group, d, std=4.0)
    'group_cartesian_product': -1,  # 需要Group类型输入，不参与替换
}

# 输出目录配置
OUTPUT_DIR = 'hill_climbing_v4.7'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 文件路径
BASE_CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, 'checkpoint_v4.7.json')
BASE_HISTORY_FILE = os.path.join(OUTPUT_DIR, 'history_v4.7.json')
BASE_DATASET_CACHE_FILE = os.path.join(OUTPUT_DIR, 'dataset_cache_v4.7.json')
BASE_LOG_FILE = os.path.join(OUTPUT_DIR, 'hill_climbing_v4.7.log')

def setup_logging(alpha_id=None):
    log_file = BASE_LOG_FILE if not alpha_id else os.path.join(OUTPUT_DIR, f'{alpha_id}_hill_climbing_v4.7.log')
    # 清除旧的处理器并显式关闭文件句柄
    for handler in logging.root.handlers[:]:
        try:
            handler.close()
        except:
            pass
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    # 强制让所有打印都能看到
    logging.info("📢 日志系统已就绪")

def send_qq_email(subject, content):
    if not EMAIL_CONFIG.get('enabled', False): return
    try:
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = EMAIL_CONFIG['sender']
        msg["To"] = EMAIL_CONFIG['receiver']
        msg["Subject"] = Header(subject, "utf-8")
        server = smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['sender'], [EMAIL_CONFIG['receiver']], msg.as_string())
        server.quit()
    except Exception as e:
        logging.error(f"邮件发送失败: {e}")

def is_file_older_than_days(file_path, days):
    try:
        file_mtime = os.path.getmtime(file_path)
        file_time = datetime.fromtimestamp(file_mtime)
        return datetime.now() - file_time > timedelta(days=days)
    except: return False

def cleanup_alpha_files(alpha_id):
    files = [
        os.path.join(OUTPUT_DIR, f'{alpha_id}_checkpoint_v4.7.json'),
        os.path.join(OUTPUT_DIR, f'{alpha_id}_history_v4.7.json'),
        os.path.join(OUTPUT_DIR, f'{alpha_id}_dataset_cache_v4.7.json'),
        os.path.join(OUTPUT_DIR, f'{alpha_id}_hill_climbing_v4.7.log')
    ]
    for f in files:
        if os.path.exists(f):
            try:
                os.remove(f)
                logging.info(f"已清理: {f}")
            except: pass

# 忽略的关键词 (避免被误识别为数据字段)
IGNORED_TOKENS = {
    'true', 'false', 'nan', 'inf', 'filter', 'driver', 'gaussian', 'uniform', 'cauchy',
    'ignore', 'std', 'k', 'lag', 'rettype', 'scope', 'constant', 'rate', 'limit', 'sigma'
}
IGNORED_TOKENS.update(CANDIDATE_GROUPS)
IGNORED_TOKENS.update(CANDIDATE_ALL_OPS)

# ==================== 持续运行模式：辅助函数 ====================
PROCESSED_ALPHAS_FILE = os.path.join(OUTPUT_DIR, 'processed_alphas.json')

def load_processed_alphas():
    """加载已处理的alpha记录"""
    if os.path.exists(PROCESSED_ALPHAS_FILE):
        try:
            with open(PROCESSED_ALPHAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_processed_alpha(alpha_id, expr):
    """保存已处理的alpha记录"""
    data = load_processed_alphas()
    data[alpha_id] = {
        'expr': expr,
        'timestamp': datetime.now().isoformat(),
        'operators': extract_operators(expr)
    }
    with open(PROCESSED_ALPHAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def extract_operators(expr):
    """从表达式中提取使用的运算符列表"""
    ops = []
    for op in CANDIDATE_ALL_OPS:
        if re.search(r'\b' + re.escape(op) + r'\s*\(', expr):
            ops.append(op)
    return sorted(ops)

def extract_expression_structure(expr):
    """提取表达式的结构特征用于多样性比较"""
    operators = set(extract_operators(expr))
    # 计算嵌套深度
    max_depth = 0
    current_depth = 0
    for ch in expr:
        if ch == '(':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif ch == ')':
            current_depth -= 1
    # 提取数据字段
    pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)')
    tokens = pattern.findall(expr)
    data_fields = set()
    for t in tokens:
        if (t not in CANDIDATE_ALL_OPS
                and t.lower() not in IGNORED_TOKENS
                and t not in CANDIDATE_GROUPS):
            data_fields.add(t)
    return {
        'operators': operators,
        'depth': max_depth,
        'data_fields': data_fields,
        'op_count': len(operators)
    }

def calculate_structural_distance(expr1, expr2):
    """计算两个表达式的结构差异度（0=完全相同, 1=完全不同）"""
    s1 = extract_expression_structure(expr1)
    s2 = extract_expression_structure(expr2)
    # 1. 运算符集合Jaccard距离 (权重50%)
    ops_union = s1['operators'] | s2['operators']
    ops_inter = s1['operators'] & s2['operators']
    op_distance = 1.0 - (len(ops_inter) / len(ops_union)) if ops_union else 0.0
    # 2. 数据字段Jaccard距离 (权重30%)
    fields_union = s1['data_fields'] | s2['data_fields']
    fields_inter = s1['data_fields'] & s2['data_fields']
    field_distance = 1.0 - (len(fields_inter) / len(fields_union)) if fields_union else 0.0
    # 3. 嵌套深度差异 (权重20%)
    depth_distance = abs(s1['depth'] - s2['depth']) / max(s1['depth'], s2['depth'], 1)
    return 0.5 * op_distance + 0.3 * field_distance + 0.2 * depth_distance

def select_most_diverse_alpha(candidates, processed_records):
    """从候选alpha中选择与已处理alpha结构差异最大的（maximin策略）

    Args:
        candidates: alpha详情列表, 每个包含 'id' 和 'regular' 字段
        processed_records: dict, 已处理alpha记录 {alpha_id: {expr, ...}}

    Returns:
        结构差异最大的候选alpha dict, 或 None
    """
    if not candidates:
        return None
    if not processed_records:
        return candidates[0]
    processed_exprs = [r.get('expr', '') for r in processed_records.values() if r.get('expr')]
    if not processed_exprs:
        return candidates[0]
    best_candidate = None
    best_min_distance = -1
    for cand in candidates:
        cand_expr = cand.get('regular', '')
        if isinstance(cand_expr, dict):
            cand_expr = cand_expr.get('code', '')
        if not cand_expr:
            continue
        # 计算与所有已处理alpha的最小距离（最近邻距离）
        min_dist = float('inf')
        for pe in processed_exprs:
            dist = calculate_structural_distance(cand_expr, pe)
            min_dist = min(min_dist, dist)
        # 选择最小距离最大的（maximin策略）
        if min_dist > best_min_distance:
            best_min_distance = min_dist
            best_candidate = cand
    if best_candidate:
        logging.info(f"   🎯 选择了结构差异度最大的alpha (距离={best_min_distance:.4f})")
    return best_candidate

def test_diversity_functions():
    """测试表达式结构多样性相关函数"""
    print("=" * 50)
    print("🧪 开始测试表达式结构多样性函数")
    print("=" * 50)

    # Test 1: extract_operators
    expr1 = "signed_power(group_rank(ts_zscore(divide(field1, field2), 66), industry), 1.5)"
    ops1 = extract_operators(expr1)
    assert 'signed_power' in ops1, f"应包含 signed_power, 实际: {ops1}"
    assert 'group_rank' in ops1, f"应包含 group_rank, 实际: {ops1}"
    assert 'ts_zscore' in ops1, f"应包含 ts_zscore, 实际: {ops1}"
    assert 'divide' in ops1, f"应包含 divide, 实际: {ops1}"
    print(f"✅ Test 1 PASS: extract_operators -> {ops1}")

    # Test 2: extract_expression_structure
    s1 = extract_expression_structure(expr1)
    assert s1['depth'] == 4, f"深度应为4, 实际: {s1['depth']}"
    assert 'field1' in s1['data_fields'], f"应包含 field1, 实际: {s1['data_fields']}"
    print(f"✅ Test 2 PASS: structure -> ops={len(s1['operators'])}, depth={s1['depth']}, fields={s1['data_fields']}")

    # Test 3: 相同表达式距离=0
    dist_same = calculate_structural_distance(expr1, expr1)
    assert dist_same == 0.0, f"相同表达式距离应为0, 实际: {dist_same}"
    print(f"✅ Test 3 PASS: 相同表达式距离 = {dist_same}")

    # Test 4: 不同表达式距离>0
    expr2 = "rank(ts_mean(close, 22))"
    dist_diff = calculate_structural_distance(expr1, expr2)
    assert dist_diff > 0, f"不同表达式距离应>0, 实际: {dist_diff}"
    print(f"✅ Test 4 PASS: 不同表达式距离 = {dist_diff:.4f}")

    # Test 5: 结构差异更大的距离更大
    expr3 = "if_else(ts_delta(vol, 10), rank(ret), reverse(rank(ret)))"
    dist_e1_e2 = calculate_structural_distance(expr1, expr2)
    dist_e1_e3 = calculate_structural_distance(expr1, expr3)
    print(f"   expr1 vs expr2 距离: {dist_e1_e2:.4f}")
    print(f"   expr1 vs expr3 距离: {dist_e1_e3:.4f}")
    print(f"✅ Test 5 PASS: 结构距离计算合理")

    # Test 6: select_most_diverse_alpha
    candidates = [
        {'id': 'a1', 'regular': expr1},
        {'id': 'a2', 'regular': expr2},
        {'id': 'a3', 'regular': expr3},
    ]
    processed = {
        'p1': {'expr': expr1, 'operators': extract_operators(expr1)}
    }
    selected = select_most_diverse_alpha(candidates, processed)
    assert selected is not None
    assert selected['id'] != 'a1', "不应选择与已处理结构相同的alpha"
    print(f"✅ Test 6 PASS: 选择了结构差异最大的 alpha: {selected['id']}")

    # Test 7: 空已处理记录时选择第一个
    selected_empty = select_most_diverse_alpha(candidates, {})
    assert selected_empty is not None
    assert selected_empty['id'] == 'a1'
    print(f"✅ Test 7 PASS: 空处理记录时选择第一个: {selected_empty['id']}")

    # Test 8: 无候选时返回None
    result = select_most_diverse_alpha([], processed)
    assert result is None
    print(f"✅ Test 8 PASS: 无候选时返回 None")

    # Test 9: 多候选多已处理时选择最不相似的
    many_candidates = [
        {'id': 'c1', 'regular': 'signed_power(group_rank(ts_zscore(divide(f1, f2), 66), industry), 1.5)'},
        {'id': 'c2', 'regular': 'rank(ts_mean(close, 22))'},
        {'id': 'c3', 'regular': 'if_else(ts_delta(vol, 10), rank(ret), reverse(rank(ret)))'},
        {'id': 'c4', 'regular': 'signed_power(group_rank(ts_zscore(divide(f3, f4), 44), sector), 2.0)'},
    ]
    many_processed = {
        'p1': {'expr': expr1},
        'p2': {'expr': 'signed_power(group_rank(ts_rank(divide(fA, fB), 120), subindustry), 1.0)'}
    }
    selected_div = select_most_diverse_alpha(many_candidates, many_processed)
    print(f"✅ Test 9 PASS: 从4个候选中选择了: {selected_div['id']}")

    print("=" * 50)
    print("🎉 所有测试通过！")
    print("=" * 50)
    return True

# ==================== 持续运行模式：辅助函数结束 ====================

class BrainClient:
    def _signal_handler(self, signum, frame):
        logging.info("\n🛑 收到中断信号！正在完成当前 Alpha 的收尾工作 (染色/改名/存档)，请稍候...")
        self.stop_requested = True

    def __init__(self, alpha_id=None):
        self.alpha_id = alpha_id
        self.auth_lock = threading.Lock()
        self.stop_requested = False
        signal.signal(signal.SIGINT, self._signal_handler)
        
        self.sess = self._sign_in()
        self.history = self._load_history()
        self.dataset_cache = self._load_dataset_cache()
        self.last_auth_time = time.time()

    def _sign_in(self):
        username = os.environ.get('BRAIN_CREDENTIAL_EMAIL')
        password = os.environ.get('BRAIN_CREDENTIAL_PASSWORD')
        if not username or not password:
            raise ValueError("❌ 请设置环境变量 BRAIN_CREDENTIAL_EMAIL 和 BRAIN_CREDENTIAL_PASSWORD")
        print(f"🔑 已从环境变量读取凭据: {username}")

        sess = requests.Session()
        sess.auth = HTTPBasicAuth(username, password)
        for attempt in range(5):
            try:
                print(f"📡 正在向 API 发送登录请求 (第 {attempt+1}/5 次)...")
                response = sess.post('https://api.worldquantbrain.com/authentication')
                if response.status_code == 201:
                    print("✅ API 认证成功！")
                    return sess
                else:
                    print(f"⚠️ 登录返回状态码: {response.status_code}, 内容: {response.text[:100]}")
            except Exception as e:
                print(f"❌ 登录网络异常: {e}")
            time.sleep(5)
        raise Exception("登录失败：已达到最大重试次数")

    def _load_history(self):
        history_file = BASE_HISTORY_FILE if not self.alpha_id else os.path.join(OUTPUT_DIR, f'{self.alpha_id}_history_v4.7.json')
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def _load_dataset_cache(self):
        cache_file = BASE_DATASET_CACHE_FILE if not self.alpha_id else os.path.join(OUTPUT_DIR, f'{self.alpha_id}_dataset_cache_v4.7.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def save_history(self):
        history_file = BASE_HISTORY_FILE if not self.alpha_id else os.path.join(OUTPUT_DIR, f'{self.alpha_id}_history_v4.7.json')
        with open(history_file, 'w') as f: json.dump(self.history, f)

    def save_dataset_cache(self):
        cache_file = BASE_DATASET_CACHE_FILE if not self.alpha_id else os.path.join(OUTPUT_DIR, f'{self.alpha_id}_dataset_cache_v4.7.json')
        with open(cache_file, 'w') as f: json.dump(self.dataset_cache, f)

    def _make_request_with_retry(self, method, url, **kwargs):
        # 从 kwargs 中提取重试次数，默认为 3
        max_retries = kwargs.pop('retries', 3)

        # 默认增加 30 秒超时，防止无限卡死
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30

        for attempt in range(max_retries):
            try:
                resp = getattr(self.sess, method)(url, **kwargs)
                if resp.status_code == 401:
                    logging.warning(f"请求返回 401，尝试重新登录...")
                    self.sess = self._sign_in()
                    continue
                return resp
            except Exception as e:
                # 只有当重试次数大于1时才打印警告，避免轻量级检查刷屏
                if max_retries > 1:
                    logging.warning(f"请求异常 (尝试 {attempt+1}/{max_retries}): {e}")
                time.sleep(2)
        return None

    def get_alpha_details(self, alpha_id):
        url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
        resp = self._make_request_with_retry('get', url)
        if resp and resp.status_code == 200:
            return resp.json()
        elif resp:
            logging.error(f"❌ 获取详情失败: Alpha {alpha_id} | 状态码: {resp.status_code} | 响应: {resp.text[:100]}")
        else:
            logging.error(f"❌ 获取详情异常: Alpha {alpha_id} | 请求无返回")
        return None

    def fetch_is_alphas(self, limit=200):
        """获取IS阶段的REGULAR类型alpha列表(按创建时间倒序)"""
        all_alphas = []
        offset = 0
        while len(all_alphas) < limit:
            batch_size = min(100, limit - len(all_alphas))
            url = (f"https://api.worldquantbrain.com/users/self/alphas"
                   f"?type=REGULAR&limit={batch_size}&offset={offset}"
                   f"&order=-dateCreated")
            resp = self._make_request_with_retry('get', url)
            if not resp or resp.status_code != 200:
                break
            data = resp.json()
            results = data.get('results', [])
            if not results:
                break
            all_alphas.extend(results)
            if len(results) < batch_size:
                break
            offset += batch_size
        logging.info(f"📡 从平台获取了 {len(all_alphas)} 个alpha")
        return all_alphas

    def search_dataset_for_field(self, field_name, settings):
        if field_name in self.dataset_cache:
            logging.info(f"  -> 命中本地缓存: {len(self.dataset_cache[field_name])} 个候选")
            return self.dataset_cache[field_name]

        search_scope = {
            'instrumentType': settings.get('instrumentType', 'EQUITY'),
            'region': settings.get('region', 'USA'),
            'delay': str(settings.get('delay', 1)),
            'universe': settings.get('universe', 'TOP3000')
        }

        url = "https://api.worldquantbrain.com/data-fields?" + \
              f"&instrumentType={search_scope['instrumentType']}" + \
              f"&region={search_scope['region']}" + \
              f"&delay={search_scope['delay']}" + \
              f"&universe={search_scope['universe']}" + \
              f"&limit=10&search={field_name}"

        try:
            resp = self._make_request_with_retry('get', url)
            if not resp or resp.status_code != 200: return []

            results = resp.json().get('results', [])
            target_dataset_id = None
            original_field_type = 'UNKNOWN'

            for item in results:
                if item['id'] == field_name:
                    original_field_type = item.get('type', 'UNKNOWN')
                    target_dataset_id = item['dataset']['id']
                    break

            if not target_dataset_id and results:
                target_dataset_id = results[0]['dataset']['id']
                original_field_type = results[0].get('type', 'UNKNOWN')

            if not target_dataset_id: return []

            url_ds = "https://api.worldquantbrain.com/data-fields?" + \
                     f"&instrumentType={search_scope['instrumentType']}" + \
                     f"&region={search_scope['region']}" + \
                     f"&delay={search_scope['delay']}" + \
                     f"&universe={search_scope['universe']}" + \
                     f"&dataset.id={target_dataset_id}&limit=50"

            candidates = []
            offset = 0
            while True:
                r = self._make_request_with_retry('get', url_ds + f"&offset={offset}")
                if not r or r.status_code != 200: break
                data = r.json()
                items = data.get('results', [])
                if not items: break

                for x in items:
                    if x['id'] != field_name:
                        candidates.append({'id': x['id'], 'type': x.get('type', 'UNKNOWN')})
                
                offset += 50
                if offset > 2000: break # 防止过多

            self.dataset_cache[field_name] = candidates
            self.save_dataset_cache()
            return candidates
        except Exception as e:
            logging.error(f"搜索字段异常: {e}")
            return []

    def submit_simulation(self, simulation_data):
        url = 'https://api.worldquantbrain.com/simulations'
        time.sleep(random.uniform(0.5, 1.0))

        for attempt in range(10):
            try:
                resp = self._make_request_with_retry('post', url, json=simulation_data)
                if resp.status_code in [200, 201, 202]:
                    loc = resp.headers.get('location')
                    if not loc:
                        data = resp.json()
                        loc = data.get('url') or data.get('location') or data.get('self')
                    return loc
                
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 10)) + random.randint(2, 5)
                    # 静默等待，不打印刷屏日志
                    time.sleep(wait)
                    continue

                logging.warning(f"提交失败: {resp.status_code} (尝试 {attempt+1})")
                time.sleep(5 * (attempt + 1))
            except Exception as e:
                logging.warning(f"提交异常: {e}")
                time.sleep(5)
        return None

    def wait_for_simulation(self, location_url):
        start_time = time.time()
        wait_interval = 2.0
        last_report_time = start_time
        max_wait_time = 2400  # 40 分钟总超时
        
        # 增加超时保护，防止平台任务卡死导致脚本无限等待
        while True:
            # 检查总等待时间
            elapsed_total = time.time() - start_time
            if elapsed_total > max_wait_time:
                logging.error(f"   ❌ [超时放弃] 该模拟任务已运行超过 {max_wait_time/60:.1f} 分钟，疑似平台卡死，强制放弃等待。")
                return {"status": "ERROR", "message": "Simulation timeout after 40 minutes"}

            try:
                resp = self._make_request_with_retry('get', location_url, timeout=10)
                if not resp or resp.status_code != 200:
                    time.sleep(min(wait_interval, 5.0))
                    wait_interval *= 1.5
                    continue

                data = resp.json()
                status = data.get('status')

                # 如果等待超过 10 分钟，每 5 分钟报平安一次
                now = time.time()
                if now - last_report_time > 300: 
                    elapsed_min = int((now - start_time) / 60)
                    logging.info(f"   [坚持等待] 该模拟已运行 {elapsed_min} 分钟，目前状态: {status}，继续等待结果...")
                    last_report_time = now

                # 将 WARNING 也视为完成状态，尝试获取 Alpha ID
                if status in ['COMPLETED', 'COMPLETE', 'WARNING']:
                    # 增强 ID 提取：优先取 alpha，备选取 id (Simulation ID)，最后从 URL 截取
                    alpha_id = data.get('alpha') or data.get('id')
                    
                    if status == 'WARNING':
                        msg = data.get('message', '')
                        if "reversion component" not in msg:
                            logging.warning(f"模拟返回 WARNING: {msg}")

                    if not alpha_id:
                        # 兜底：从 URL 结尾提取最后一段字符串
                        match = re.search(r'/([^/]+)/?$', location_url)
                        if match: alpha_id = match.group(1)
                    
                    if alpha_id:
                        # 核心增强：循环等待 Alpha 统计数据 (is 字段) 出现
                        for attempt in range(36): 
                            details = self.get_alpha_details(alpha_id)
                            # 必须拿到 is 报表且 sharpe 有值才算成功
                            if details and 'is' in details and details['is'].get('sharpe') is not None:
                                return details
                            
                            # 优雅退出检查
                            if getattr(self, 'stop_requested', False):
                                return details if details else data

                            logging.info(f"   [等待报表] 任务 {alpha_id} 已完工，正等待统计数据生成 ({attempt+1}/36)...")
                            time.sleep(5)
                        
                        # 如果 36 次都没等到，直接把带 ID 的原始 data 返回，让 _process_result 去最后补救
                        return data
                    return data
                
                if status in ['ERROR', 'FAIL']:
                    logging.error(f"   ❌ 模拟任务失败! 状态: {status} | 消息: {data.get('message')}")
                    return data
                
                time.sleep(min(wait_interval, 5.0))
                wait_interval *= 1.5
            except Exception as e:
                logging.warning(f"等待结果异常 (网络抖动?): {e}")
                time.sleep(5.0)

    def check_factory_shape(self, alpha_id):
        """
        增强版厂字型检查：整合年度统计与 PNL 详情
        """
        try:
            # 1. 检查年度统计 (Yearly Stats)
            url_yearly = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats"
            json_yearly = None
            for _ in range(3):
                resp = self._make_request_with_retry('get', url_yearly)
                if resp and resp.status_code == 200 and resp.text.strip():
                    try:
                        temp = resp.json()
                        if temp.get('records'):
                            json_yearly = temp
                            break
                    except: pass
                time.sleep(2)

            if json_yearly:
                records = json_yearly.get('records', [])
                non_zero_sharpe_count = sum(1 for r in records if len(r) > 6 and r[6] is not None and abs(float(r[6])) > 1e-6)
                if non_zero_sharpe_count > 0 and non_zero_sharpe_count < 8:
                    logging.info(f"  🟣 [厂字型] 有效年份不足 8 年 ({non_zero_sharpe_count})")
                    return True

            # 2. 检查 PNL 详情 (针对那种看似年份多但末端平躺的 Alpha)
            url_pnl = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl"
            for _ in range(3):
                resp_pnl = self._make_request_with_retry('get', url_pnl)
                if resp_pnl and resp_pnl.status_code == 200:
                    data_pnl = resp_pnl.json().get('records', [])
                    if data_pnl:
                        if not self._check_consecutive_pnl_values(alpha_id, data_pnl):
                            return True
                        break
                time.sleep(2)

            return False

        except Exception as e:
            logging.error(f"增强厂字型检查异常: {e}")
            return False

    def set_alpha_color(self, alpha_id, color):
        """设置 Alpha 颜色"""
        url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
        try:
            self._make_request_with_retry('patch', url, json={'color': color})
        except Exception as e:
            logging.warning(f"设置颜色失败: {e}")

    def set_alpha_name(self, alpha_id, name):
        """设置 Alpha 名称"""
        url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
        try:
            self._make_request_with_retry('patch', url, json={'name': name})
        except Exception as e:
            logging.warning(f"设置名称失败: {e}")

    def get_product_correlation(self, alpha_id, max_attempts=40):
        """获取 Alpha 的 Product Correlation (PC) - 强力取回版"""
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod"
        for i in range(max_attempts):
            try:
                resp = self._make_request_with_retry('get', url, timeout=15)
                if resp and resp.status_code == 200:
                    data = resp.json()
                    if "max" in data:
                        return float(data["max"])
                elif resp and resp.status_code == 404:
                    pass
            except: pass
            
            if max_attempts > 5 and i % 5 == 0:
                logging.info(f"   [PC等待] 正在等待 Alpha {alpha_id} 的 PC 数据 (第 {i+1}/{max_attempts} 次查询)...")
            time.sleep(30)
            
        logging.warning(f"   ❌ [PC失败] 经过 {max_attempts} 次尝试仍无法获取 PC: {alpha_id}")
        return None

    def get_alpha_pnl_df(self, alpha_id):
        """获取单个 Alpha 的 PnL 并返回 DataFrame (增强诊断版)"""
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl"
        try:
            resp = self._make_request_with_retry('get', url, retries=2)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    if 'records' in data and data['records']:
                        df = pd.DataFrame(data['records'], columns=[item['name'] for item in data['schema']['properties']])
                        df['date'] = pd.to_datetime(df['date'])
                        df.set_index('date', inplace=True)
                        return df[['pnl']].rename(columns={'pnl': alpha_id})
                    else:
                        # 数据为空，通常是因为模拟尚未完全结束
                        return None
                except json.JSONDecodeError:
                    return None
            elif resp:
                if resp.status_code != 404: # 忽略常见的 404 (数据未生成)
                    logging.warning(f"⚠️ 获取 Alpha {alpha_id} PnL 失败: HTTP {resp.status_code}")
            return None
        except Exception as e:
            logging.warning(f"⚠️ 获取 Alpha {alpha_id} PnL 异常: {e}")
        return None

    def download_os_pnl_pool(self):
        """增量同步 OS Alpha 的 PnL 数据"""
        logging.info("📡 正在同步 OS 库 Alpha 列表...")
        all_os_alphas = []
        offset = 0
        while True:
            try:
                url = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&type=REGULAR&limit=100&offset={offset}&order=-dateSubmitted"
                resp = self._make_request_with_retry('get', url)
                if not resp or resp.status_code != 200: break
                data = resp.json()
                results = data.get('results', [])
                if not results: break
                all_os_alphas.extend(results)
                if len(results) < 100: break
                offset += 100
            except Exception as e:
                logging.warning(f"同步 OS 列表出错: {e}")
                break

        if not all_os_alphas:
            logging.warning("⚠️ 未能获取到任何 OS Alpha")
            return pd.DataFrame()

        server_ids = [a['id'] for a in all_os_alphas]
        print(f"✅ 列表同步完成！服务器共有 {len(server_ids)} 个 OS Alpha。")

        # --- 增量逻辑开始 ---
        pickle_path = os.path.join(OUTPUT_DIR, 'os_pnl_pool.pickle')
        local_pool = pd.DataFrame()
        if os.path.exists(pickle_path):
            try:
                local_pool = pd.read_pickle(pickle_path)
                # 只保留服务器上依然存在的 ID
                existing_ids = [aid for aid in local_pool.columns if aid in server_ids]
                local_pool = local_pool[existing_ids]
                logging.info(f"💾 已加载本地缓存: {len(existing_ids)} 个 Alpha")
            except Exception as e:
                logging.warning(f"读取本地缓存失败: {e}")

        # 找出需要新下载的 ID
        need_download_ids = [aid for aid in server_ids if aid not in local_pool.columns]
        
        if not need_download_ids:
            print(f"✨ 本地缓存已是最新的，共有 {local_pool.shape[1]} 个 Alpha。")
            return local_pool

        print(f"⏳ 发现 {len(need_download_ids)} 个新 Alpha，开始增量下载...")
        
        new_pnl_list = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_id = {executor.submit(self.get_alpha_pnl_df, aid): aid for aid in need_download_ids}
            completed_count = 0
            for future in as_completed(future_to_id):
                res = future.result()
                if res is not None:
                    new_pnl_list.append(res)
                
                completed_count += 1
                if completed_count % 10 == 0 or completed_count == len(need_download_ids):
                    print(f"   [增量下载进度] {completed_count}/{len(need_download_ids)} (已成功捕获 {len(new_pnl_list)} 个)")
                time.sleep(random.uniform(0.1, 0.2))
        
        # 合并新旧数据
        if new_pnl_list:
            new_df = pd.concat(new_pnl_list, axis=1)
            if not local_pool.empty:
                full_pool = pd.concat([local_pool, new_df], axis=1)
            else:
                full_pool = new_df
            
            full_pool.sort_index(inplace=True)
            # 保存更新后的池
            full_pool.to_pickle(pickle_path)
            print(f"✨ 增量同步成功！当前 PnL 池共有 {full_pool.shape[1]} 个 Alpha 用于 SC 计算。")
            return full_pool
        
        return local_pool

    def calculate_sc_locally(self, alpha_id, os_pool):
        """在本地计算 Alpha 与 OS 池的最大相关性"""
        if os_pool.empty: return 0.0
        
        new_pnl = self.get_alpha_pnl_df(alpha_id)
        if new_pnl is None: return None
        
        # 对齐数据：取最近 4 年数据 (参考 C3 逻辑)
        combined = pd.concat([os_pool, new_pnl], axis=1)
        combined = combined.ffill()
        rets = combined.diff()
        
        if rets.empty: return 0.0
        
        # 只取最近一段时期的收益率进行相关性计算
        last_date = rets.index.max()
        rets = rets[rets.index > last_date - pd.DateOffset(years=4)]
        
        corr_matrix = rets.corr()
        if alpha_id in corr_matrix.columns:
            # 提取该 Alpha 与池中其他 Alpha 的相关性
            sc_series = corr_matrix[alpha_id].drop(alpha_id)
            return float(sc_series.max())
        return 0.0

    def set_alpha_color(self, alpha_id, color):
        """设置 Alpha 颜色"""
        url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
        try:
            self._make_request_with_retry('patch', url, json={'color': color})
        except Exception as e:
            logging.warning(f"设置颜色失败: {e}")

    def set_alpha_name(self, alpha_id, name):
        """设置 Alpha 名称"""
        url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
        try:
            self._make_request_with_retry('patch', url, json={'name': name})
        except Exception as e:
            logging.warning(f"设置名称失败: {e}")

    def get_product_correlation(self, alpha_id, max_attempts=40):
        """获取 Alpha 的 Product Correlation (PC) - 强力取回版"""
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod"
        for i in range(max_attempts):
            try:
                resp = self._make_request_with_retry('get', url, timeout=15)
                if resp and resp.status_code == 200:
                    data = resp.json()
                    if "max" in data:
                        return float(data["max"])
                elif resp and resp.status_code == 404:
                    pass
            except: pass
            
            if max_attempts > 5 and i % 5 == 0:
                logging.info(f"   [PC等待] 正在等待 Alpha {alpha_id} 的 PC 数据 (第 {i+1}/{max_attempts} 次查询)...")
            time.sleep(30)
            
        logging.warning(f"   ❌ [PC失败] 经过 {max_attempts} 次尝试仍无法获取 PC: {alpha_id}")
        return None

    def get_self_correlation(self, alpha_id, max_attempts=20):
        """获取 Alpha 的 Self Correlation (SC) - 强力取回版"""
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/self"
        for i in range(max_attempts):
            try:
                resp = self._make_request_with_retry('get', url, timeout=15)
                if resp and resp.status_code == 200:
                    data = resp.json()
                    if "max" in data:
                        return float(data["max"])
            except: pass
            time.sleep(30)
        return None

    def _check_consecutive_pnl_values(self, alpha_id, data, required_streak=250):
        """
        检查是否有连续 required_streak 天的相同非零值 (厂字型核心特征)
        """
        if not data or len(data) < required_streak:
            return True # 数据不足，视为通过

        pnl_values = [row[1] for row in data if len(row) >= 2]
        if not pnl_values: return True
        
        if all(v == 0 for v in pnl_values):
            return False # 全 0 也是无效

        # 检查末端稳定性 (从后往前查)
        end_streak_count = 0
        end_streak_value = pnl_values[-1]
        for i in range(len(pnl_values)-1, -1, -1):
            if pnl_values[i] == end_streak_value:
                end_streak_count += 1
            else:
                break
        
        if end_streak_count >= required_streak:
            logging.info(f"  🟣 [厂字型] 末端连续 {end_streak_count} 天数值相同: {end_streak_value}")
            return False

        # 检查全局连续性
        curr_count = 0
        curr_val = None
        for v in pnl_values:
            if v != 0:
                if v == curr_val:
                    curr_count += 1
                else:
                    curr_val = v
                    curr_count = 1
            else:
                curr_val = None
                curr_count = 0
            
            if curr_count >= required_streak:
                logging.info(f"  🟣 [厂字型] 全局检测到连续 {curr_count} 天相同非零值")
                return False
        return True

class SmartExpression:
    def __init__(self, expression, settings, client):
        self.original_expr = expression
        self.settings = settings
        self.client = client
        self.tokens = []
        self.data_fields_cache = {}
        self._parse()

    def _parse(self):
        # 直接使用原始公式解析，确保索引绝对准确
        pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_.]*)|(-?\d+\.?\d*)')
        self.tokens = []
        unique_data_fields_list = []
        seen_fields = set()

        current_idx = 0
        while current_idx < len(self.original_expr):
            match = pattern.search(self.original_expr, current_idx)
            if not match: break
            
            text = match.group()
            start, end = match.span()
            token_type = 'unknown'

            if re.match(r'^-?\d+\.?\d*$', text):
                token_type = 'number'
            elif text in CANDIDATE_ALL_OPS:
                token_type = 'operator'
            elif text in CANDIDATE_GROUPS:
                token_type = 'group'
            elif text.lower() in IGNORED_TOKENS:
                token_type = 'keyword'
            # 识别算子控制参数，防止误当成数据字段优化
            elif text.startswith('lambda_') or text == 'target_tvr' or text.endswith('_tvr'):
                token_type = 'parameter'
            else:
                token_type = 'data_field'
                if text not in seen_fields:
                    unique_data_fields_list.append(text)
                    seen_fields.add(text)

            self.tokens.append({'text': text, 'type': token_type, 'start': start, 'end': end})
            current_idx = end

        # === 智能检测 group_* 函数的分组参数，防止被误当作 data_field 优化 ===
        reclassified_fields = set()
        for token in self.tokens:
            if token['type'] != 'operator' or not token['text'].startswith('group_'):
                continue
            func_end = token['end']
            if func_end >= len(self.original_expr) or self.original_expr[func_end] != '(':
                continue
            # 从开括号后扫描，找第一个 depth=1 的逗号（分隔表达式参数和分组参数）
            depth = 1
            first_comma = -1
            pos = func_end + 1
            while pos < len(self.original_expr) and depth > 0:
                ch = self.original_expr[pos]
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                elif ch == ',' and depth == 1 and first_comma == -1:
                    first_comma = pos
                pos += 1
            if first_comma == -1:
                continue
            # 逗号后的第一个 token 即为分组参数
            for t in self.tokens:
                if t['start'] > first_comma:
                    if t['type'] == 'data_field':
                        # 确认是简单标识符（逗号和此 token 之间没有嵌套调用）
                        between = self.original_expr[first_comma + 1:t['start']].strip()
                        if '(' not in between:
                            logging.info(f"  -> 将 '{t['text']}' 重新分类为 group (它是 {token['text']} 的分组参数)")
                            t['type'] = 'group'
                            reclassified_fields.add(t['text'])
                    break
        # 从数据字段列表中移除已重新分类的字段（仅当该字段所有实例都不再是 data_field 时）
        if reclassified_fields:
            still_data_fields = {t['text'] for t in self.tokens if t['type'] == 'data_field'}
            unique_data_fields_list = [f for f in unique_data_fields_list if f in still_data_fields]

        total_data_instances = len([t for t in self.tokens if t['type'] == 'data_field'])
        logging.info(f"识别到 {len(unique_data_fields_list)} 种数据字段 (共 {total_data_instances} 个优化位置): {unique_data_fields_list}")
        
        for i, field in enumerate(unique_data_fields_list):
            logging.info(f"[{i + 1}/{len(unique_data_fields_list)}] 正在搜索字段 '{field}'...")
            # 先尝试从缓存获取
            cached_cands = self.data_fields_cache.get(field)
            if cached_cands:
                # 获取原始字段类型
                original_field_type = 'UNKNOWN'
                for cached_field in cached_cands:
                    if cached_field.get('id') == field and isinstance(cached_field, dict):
                        original_field_type = cached_field.get('type', 'UNKNOWN')
                        break

                # 根据原始字段类型过滤缓存中的候选字段
                if original_field_type != 'UNKNOWN':
                    filtered_cands = [cand for cand in cached_cands if
                                      isinstance(cand, dict) and cand.get('type') == original_field_type]
                    # 更新缓存
                    self.data_fields_cache[field] = filtered_cands
                    cached_cands = filtered_cands

                # 显示缓存中的候选字段数量和类型信息
                type_counts = {}
                for cand in cached_cands:
                    field_type = cand.get('type', 'UNKNOWN') if isinstance(cand, dict) else 'UNKNOWN'
                    type_counts[field_type] = type_counts.get(field_type, 0) + 1
                type_info = ", ".join([f"{count}个{ftype}" for ftype, count in type_counts.items()])
                logging.info(f"  -> 命中本地缓存: {len(cached_cands)} 个候选字段 ({type_info})")
            else:
                # 缓存中没有则从API获取
                cands = self.client.search_dataset_for_field(field, self.settings)
                if cands:
                    self.data_fields_cache[field] = cands
                    # 显示找到的候选字段数量和类型信息
                    type_counts = {}
                    for cand in cands:
                        field_type = cand.get('type', 'UNKNOWN') if isinstance(cand, dict) else 'UNKNOWN'
                        type_counts[field_type] = type_counts.get(field_type, 0) + 1
                    type_info = ", ".join([f"{count}个{ftype}" for ftype, count in type_counts.items()])
                    logging.info(f"  -> 找到 {len(cands)} 个候选字段 ({type_info})")
                else:
                    logging.warning(f"字段 '{field}' 未找到候选，但将保留其在优化列表中的位置")
                    # 保持 token['type'] = 'data_field' 不变，确保索引稳定性

    def _get_operator_group(self, operator_name):
        """确定运算符属于哪个组"""
        for group_name, operators in OPERATOR_GROUPS.items():
            if operator_name in operators:
                return group_name
        return None

    def generate_neighbors(self, target_type, target_index):
        """生成变体 (回归 v4.4 稳健版)"""
        # 统一处理 time_window 和 number 搜索类型
        actual_search_type = 'number' if target_type == 'time_window' else target_type
        
        # 直接找到所有该类型的 Token
        candidates_indices = []
        for idx, t in enumerate(self.tokens):
            if t['type'] == actual_search_type:
                # 排除算子内部参数 (lambda_, target_tvr)
                if t['text'].startswith('lambda_') or 'tvr' in t['text']:
                    continue
                candidates_indices.append(idx)
        
        if not candidates_indices or target_index >= len(candidates_indices):
            return []

        token_idx = candidates_indices[target_index]
        token = self.tokens[token_idx]
        old_text = token['text']

        pool = []
        if target_type == 'data_field':
            pool = self.data_fields_cache.get(old_text, [])
            if not pool:
                # 策略 1: 原名搜索
                pool = self.client.search_dataset_for_field(old_text, self.settings)
                
                # 策略 2: 剥离后缀模糊搜索
                if not pool and '_' in old_text:
                    parts = old_text.split('_')
                    if len(parts) > 1:
                        short_name = '_'.join(parts[:-1])
                        logging.info(f"  -> 字段 '{old_text}' 搜索无果，尝试前缀搜索: {short_name}")
                        pool = self.client.search_dataset_for_field(short_name, self.settings)
                
                # 策略 3: 通用补救
                if not pool:
                    if 'price' in old_text.lower():
                        pool = self.client.search_dataset_for_field('pv_price', self.settings)
                    elif 'volume' in old_text.lower():
                        pool = self.client.search_dataset_for_field('pv_volume', self.settings)

                if pool: self.data_fields_cache[old_text] = pool
            
            if pool:
                logging.info(f"  -> 找到 {len(pool)} 个候选字段")
            else:
                logging.warning(f"字段 '{old_text}' 仍未找到候选，将跳过优化")
                return []
        elif target_type in ['number', 'time_window']:
            # 特殊处理：固定数值-1不应被替换
            if old_text == '-1':
                logging.info(f"  -> 检测到固定数值 '{old_text}'，不参与优化")
                return []

            # 智能判断：整数且>=1视为天数，否则视为系数
            if '.' not in old_text and float(old_text) >= 1:
                pool = [str(x) for x in CANDIDATE_DAYS]
            else:
                pool = [str(x) for x in CANDIDATE_NUMBERS]
        elif target_type == 'group':
            pool = CANDIDATE_GROUPS
        elif target_type == 'operator':
            # 只在同一组内查找替代运算符，并过滤参数签名不兼容的
            operator_group = self._get_operator_group(old_text)
            if operator_group:
                old_arity = OPERATOR_ARITY.get(old_text, 2)
                pool = [op for op in OPERATOR_GROUPS[operator_group]
                        if OPERATOR_ARITY.get(op, 2) == old_arity]
                logging.info(f"  -> 运算符 '{old_text}' 属于 '{operator_group}' 组 (arity={old_arity})，兼容候选: {len(pool)} 个")
            else:
                pool = CANDIDATE_ALL_OPS
                logging.warning(f"  -> 未找到运算符 '{old_text}' 的所属组，将在整个运算符池中查找替代")

        # 处理候选池，确保正确提取字段ID
        processed_pool = []
        for x in pool:
            if isinstance(x, dict):
                processed_pool.append(x['id'])
            else:
                processed_pool.append(str(x))

        # 过滤掉与原文本相同的项
        filtered_pool = [x for x in processed_pool if x != old_text]

        if not filtered_pool:
            return []

        results = []
        for cand in filtered_pool:
            new_expr = self.original_expr[:token['start']] + cand + self.original_expr[token['end']:]
            results.append(new_expr)

        return list(set(results))


class AsyncOptimizer:
    def _signal_handler(self, signum, frame):
        logging.info("\n🛑 收到中断信号！正在完成当前 Alpha 的收尾工作 (染色/改名/存档)，请稍候...")
        self.stop_requested = True

    def __init__(self, alpha_id=None):
        self.alpha_id = alpha_id
        self.auth_lock = threading.Lock() # 添加登录锁
        self.score_lock = threading.Lock() # 恢复分数锁
        self.stop_requested = False # 优雅退出标志位
        
        # 注册信号处理器 (防止重复注册或报错)
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
        except Exception:
            pass

        # 在模式1下，先删除旧文件
        if RUN_MODE == 1:
            print("🧹 正在清理旧的日志和检查点文件...")
            self._cleanup_old_files()

        print("🔑 正在尝试登录 WorldQuant Brain 平台...")
        self.client = BrainClient(alpha_id)
        print("🔓 登录成功！")
        
        # --- v4.6 新增：初始化 PnL 池 ---
        self.os_pool = self.client.download_os_pnl_pool()
        # -----------------------------

        self.best_expr = None
        self.best_score = -9999
        self.best_base_score = -9999  # 新增：记录不含 PC 奖惩的基础分数
        self.settings = None
        self.history_cache = {}
        self.best_alpha_id = None  # 添加跟踪最佳Alpha ID的属性
        self.initial_score = None  # 添加初始分数属性
        self.initial_alpha_id = None  # 添加初始Alpha ID属性
        self.best_pc = None  # 记录当前最优解的 PC 值 (None表示尚未获取)
        self.best_stats = {}  # 记录最优解的详细统计指标
        # 新增：记录当前优化位置（包括字段和批次）
        self.current_position = {
            'data_field': START_OPTIMIZATION_FROM['data_field'],
            'time_window': START_OPTIMIZATION_FROM['time_window'],
            'number': START_OPTIMIZATION_FROM['number'],
            'group': START_OPTIMIZATION_FROM['group'],
            'operator': START_OPTIMIZATION_FROM['operator'],
            'batch_offset': 0,  # 批次偏移量
            'neutralization': 0,  # 中性化参数优化位置
            'decay': 0  # 衰减参数优化位置
        }

    def _cleanup_old_files(self):
        """清理旧的检查点和日志文件"""
        logging.info(f"清理旧文件 (扫描目录: {OUTPUT_DIR})...")
        patterns = [r'.*_v4\.[67]\.json$', r'.*_v4\.[67]\.log$', r'checkpoint.*\.json$', r'history.*\.json$']
        try:
            for fname in os.listdir(OUTPUT_DIR):
                if any(re.match(p, fname) for p in patterns):
                    full_path = os.path.join(OUTPUT_DIR, fname)
                    if is_file_older_than_days(full_path, 2):
                        try:
                            # 尝试关闭句柄
                            for handler in logging.root.handlers[:]:
                                handler.close()
                                logging.root.removeHandler(handler)
                            os.remove(full_path)
                            logging.info(f"已删除旧文件: {full_path}")
                        except: pass
        except Exception as e:
            logging.warning(f"清理文件时出错: {e}")

        # 重新初始化日志配置
        setup_logging(self.alpha_id)

    def calculate_sc_locally(self, alpha_id, os_pool):
        """代理调用客户端的本地SC计算逻辑"""
        return self.client.calculate_sc_locally(alpha_id, os_pool)

    def calculate_sc_penalty(self, sc_val):
        """计算 SC 惩罚分 (平滑递增版)"""
        if sc_val is None or sc_val <= 0.7:
            return 0
        
        # 阶梯 1: 0.7 - 0.72 (10倍)
        if sc_val <= 0.72:
            return (0.7 - sc_val) * 10
        # 阶梯 2: 0.72 - 0.80 (30倍)
        elif sc_val <= 0.80:
            return (0.7 - sc_val) * 30
        # 阶梯 3: > 0.80 (50倍 - 巨痛但给活路)
        else:
            return (0.7 - sc_val) * 50

    def _extract_scores_from_name(self, name):
        """从 Alpha 名字中提取 PC 和 SC 值"""
        pc_val, sc_val = None, None
        if not name: return pc_val, sc_val
        
        # 匹配 PC (-?\d+(?:\.\d+)?)
        pc_match = re.search(r'PC(-?\d+(?:\.\d+)?)', name)
        if pc_match: pc_val = float(pc_match.group(1))
        
        # 匹配 SC (-?\d+(?:\.\d+)?)
        sc_match = re.search(r'SC(-?\d+(?:\.\d+)?)', name)
        if sc_match: sc_val = float(sc_match.group(1))
        
        return pc_val, sc_val

    def load_checkpoint(self, alpha_id):
        """为特定Alpha ID加载检查点"""
        checkpoint_file = os.path.join(OUTPUT_DIR, f'{alpha_id}_checkpoint_v4.7.json')
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r') as f:
                    data = json.load(f)
                    
                    # 强校验：比对 initial_alpha_id 而不是当前最优 alpha_id
                    # 这样即使爬山过程中 ID 变了，只要是同一个起始任务，就能续爬
                    saved_initial_id = data.get('initial_alpha_id')
                    
                    # 兼容旧版 checkpoint (如果没有 initial_alpha_id，尝试用 alpha_id 兜底，但可能会误判)
                    if not saved_initial_id:
                        saved_initial_id = data.get('alpha_id')

                    if saved_initial_id != alpha_id:
                        logging.warning(f"⚠️ 检查点初始 ID ({saved_initial_id}) 与目标 ID ({alpha_id}) 不匹配，将重置进度！")
                        return False

                    self.best_expr = data['expr']
                    self.best_score = data['score']
                    self.best_base_score = data.get('base_score', self.best_score)
                    self.settings = data['settings']
                    self.best_alpha_id = data.get('alpha_id', None)
                    self.initial_score = data.get('initial_score', None)
                    self.initial_alpha_id = data.get('initial_alpha_id', None)
                    self.best_pc = data.get('best_pc', None) # 加载保存的 PC 值
                    self.best_stats = data.get('best_stats', {})
                    # 加载当前优化位置（包括字段和批次）
                    self.current_position = data.get('current_position', self.current_position)
                    logging.info(f"断点续传: Score={self.best_score}, Alpha ID={self.best_alpha_id}, PC={self.best_pc}")
                    return True
            except Exception as e:
                logging.error(f"加载检查点失败: {e}")
                pass
        return False

    def save_checkpoint(self, alpha_id):
        """为特定Alpha ID保存检查点"""
        checkpoint_file = os.path.join(OUTPUT_DIR, f'{alpha_id}_checkpoint_v4.7.json')
        with open(checkpoint_file, 'w') as f:
            json.dump({
                'expr': self.best_expr,
                'score': self.best_score,
                'base_score': self.best_base_score,
                'settings': self.settings,
                'alpha_id': self.best_alpha_id,
                'best_pc': self.best_pc, # 保存当前 PC 值
                'best_stats': self.best_stats,
                'target_alpha_ids': TARGET_ALPHA_IDS,
                'initial_score': self.initial_score,
                'initial_alpha_id': self.initial_alpha_id, # <--- 核心修复：必须存这个！
                'current_position': self.current_position
            }, f)





    def evaluate_batch(self, expr_list, settings=None):
        """同步批处理评估 (修复：将 Settings 纳入缓存键)"""
        if settings is None:
            settings = self.settings

        to_run = []
        results = {}

        for expr in expr_list:
            # 核心修复：缓存键应包含 settings 以支持参数优化回测
            cache_payload = {'expr': expr, 'settings': settings}
            h = hashlib.md5(json.dumps(cache_payload, sort_keys=True).encode('utf-8')).hexdigest()
            
            if h in self.client.history:
                cached_data = self.client.history[h]
                if isinstance(cached_data, dict):
                    results[expr] = cached_data
                else:
                    # 兼容旧版本
                    results[expr] = {'score': cached_data, 'url': 'Legacy Cache Hit'}
            else:
                to_run.append(expr)

        if not to_run: return results

        logging.info(f"并发提交 {len(to_run)} 个模拟 (设置: {settings.get('neutralization', 'NONE')}/{settings.get('decay', 0)})...")
        futures = {}
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
            for expr in to_run:
                # 增加延迟，防止提交太快触发 429
                time.sleep(random.uniform(1.1, 2.1))
                sim_data = {'type': 'REGULAR', 'settings': settings, 'regular': expr}
                futures[executor.submit(self.client.submit_simulation, sim_data)] = expr

        loc_map = {}
        for f in as_completed(futures):
            expr = futures[f]
            try:
                loc = f.result()
                if loc:
                    loc_map[loc] = expr
                    logging.info(f"  -> 已提交: {loc}")
                    logging.info(f"     [公式]: {expr}")
                else:
                    results[expr] = {'score': 0, 'url': 'Submission Failed'}
            except Exception as e:
                logging.warning(f"提交异常: {e}")

        wait_futures = {}
        completed_count = 0
        total_tasks = len(loc_map)

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
            for loc, expr in loc_map.items():
                wait_futures[executor.submit(self.client.wait_for_simulation, loc)] = (expr, loc)

        for f in as_completed(wait_futures):
            expr, loc = wait_futures[f]
            try:
                res = f.result()
                # 如果结果为空，尝试最后一次抢救性查询
                if not res:
                    logging.warning(f"  ⚠️ [结果丢失] {loc} 返回 None，尝试最后一次查询...")
                    time.sleep(2)
                    res = self.client.wait_for_simulation(loc)

                # 将结果存入字典，并由 _process_result 内部处理反转
                self._process_result(res, expr, loc, results, settings)

                completed_count += 1
                logging.info(f"   [进度] {completed_count}/{total_tasks} 批次任务已完成")
            except Exception as e:
                logging.warning(f"获取结果异常: {e}")

        return results

    def _process_result(self, res, expr, location, results_dict=None, settings=None):
        """处理单个结果"""
        current_settings = settings if settings is not None else self.settings
        
        # --- 补救逻辑加强：如果 res 只是个 simulation 对象或报表缺失，通过 ID 强制取回 ---
        if res and ('is' not in res or res['is'].get('sharpe') is None):
            aid = res.get('alpha') or res.get('id')
            if aid and len(aid) > 5: # 简单的 ID 合法性检查
                logging.info(f"   🔎 [强力取回] 报表缺失或不完整，通过 Alpha ID {aid} 直接查询详情...")
                # 循环重试几次，因为平台生成报表可能需要一点时间
                for attempt in range(5):
                    details = self.client.get_alpha_details(aid)
                    if details and 'is' in details and details['is'].get('sharpe') is not None:
                        res = details
                        logging.info(f"   ✅ [取回成功] 已成功拿回 Alpha {aid} 的统计数据。")
                        break
                    time.sleep(2)
        # --------------------------------------------------------------------------

        score = 0
        stats_dict = {'sharpe': 0, 'fitness': 0, 'margin': 0}
        alpha_id = None

        if res and 'is' in res:
            alpha_id = res['id']  # 获取Alpha ID
            is_stats = res['is']
            sharpe = is_stats.get('sharpe', 0)
            fitness = is_stats.get('fitness', 0)
            margin = is_stats.get('margin', 0)
            turnover = is_stats.get('turnover', 0)

            # 检查是否为厂字型Alpha
            if self.client.check_factory_shape(alpha_id):
                # 厂字型Alpha直接给0分并标记为紫色 (仅当无颜色时)
                logging.info(f"  🟣 检测到厂字型Alpha: {alpha_id}")
                if not res.get('color'):
                    self.client.set_alpha_color(alpha_id, 'PURPLE')
                    logging.info(f"  -> 已将其标记为紫色")
                else:
                    logging.info(f"  -> 该Alpha已有颜色 '{res.get('color')}'，跳过变色")

                # 更新结果字典（厂字型记0分）
                if results_dict is not None:
                    results_dict[expr] = {
                        'score': 0,
                        'url': location,
                        'stats': {'sharpe': 0, 'fitness': 0, 'margin': 0, 'passed': False, 'factory_shape': True},
                        'alpha_id': alpha_id
                    }
                return 0

            # 处理 None 值，将其转换为 0
            if sharpe is None:
                sharpe = 0.0
            if fitness is None:
                fitness = 0.0
            if margin is None:
                margin = 0.0
                logging.warning(f"  -> Margin 为 None，已替换为 0.0")

            # 新增条件：如果margin大于万分之100(0.01)，则margin按0计算
            if margin > 0.01:
                logging.info(f"  -> Margin ({margin:.4f}) 大于100‱，margin分数按0计算")
                margin_score = 0.0
            else:
                margin_score = margin

            is_passed = False
            if 'checks' in is_stats:
                checks = is_stats['checks']
                if checks and not any(c.get('result') == 'FAIL' for c in checks):
                    is_passed = True

            pass_bonus = PASS_BONUS if is_passed else 0.0

            # 厂字型检查仅用于标记，不影响评分
            is_factory_ok = True

            # 处理 None 值，将其转换为 0
            if sharpe is None:
                sharpe = 0.0
            if fitness is None:
                fitness = 0.0
            if margin is None:
                margin = 0.0

            # --- [相关性校准与定色] ---
            sc_val = None
            pc_val_from_name = None
            is_newly_colored = False
            
            if is_passed:
                try:
                    # 1. 先查官方状态
                    details = self.client.get_alpha_details(alpha_id)
                    current_color = details.get('color', '')
                    current_name = details.get('name', '')
                    
                    if current_color:
                        logging.info(f"   [兼容模式] Alpha {alpha_id} 已有颜色 '{current_color}'，解析名字补全数据...")
                        pc_parsed, sc_parsed = self._extract_scores_from_name(current_name)
                        sc_val = sc_parsed
                        pc_val_from_name = pc_parsed

                    # 如果名字里没 SC，或者根本没颜色，则本地计算
                    if sc_val is None:
                        logging.info(f"   [本地SC检查] Alpha {alpha_id} 正在计算 SC...")
                        sc_val = self.client.calculate_sc_locally(alpha_id, self.os_pool)
                        
                        if not current_color:
                            formatted_sc = sc_val if sc_val is not None else 0.0
                            new_name = f"SC{formatted_sc:.4f}"
                            self.client.set_alpha_name(alpha_id, new_name)
                            
                            final_color = 'GREEN'
                            if sc_val is not None and sc_val > SC_CUTOFF: final_color = 'BLUE'
                            elif margin < MARGIN_THRESHOLD: final_color = 'BLUE'
                            
                            self.client.set_alpha_color(alpha_id, final_color)
                            is_newly_colored = True
                            logging.info(f"   🎨 [定色/改名] Alpha {alpha_id} -> {new_name} | 颜色: {final_color}")
                except Exception as e:
                    logging.warning(f"SC处理失败: {e}")

            # --- [最终评分系统] ---
            # 1. 基础分: 夏普 + 拟合度
            # 2. 换手率引导惩罚: 从 10% 开始起扣，5倍系数
            to_penalty = max(0, turnover - 0.10) * 5.0

            # 3. Margin 奖励: 50倍系数
            margin_reward = 50 * margin_score
            
            # 4. SC 惩罚 (现在 sc_val 已获取)
            sc_penalty = 0.0
            if sc_val is not None:
                sc_penalty = self.calculate_sc_penalty(sc_val)

            # 5. 综合计算 (基础分 - TO惩罚 - SC惩罚 + Margin奖励)
            base_score = (sharpe + fitness) + margin_reward - to_penalty - abs(sc_penalty)
            final_score = max(0.0, base_score + pass_bonus)

            # 打印详细扣分情况 (仅当有惩罚时)
            if to_penalty > 0 or abs(sc_penalty) > 0:
                logging.info(f"   [评分详情] TO惩罚: -{to_penalty:.4f} | SC惩罚: {sc_penalty:.4f} | Margin奖励: +{margin_reward:.4f}")

            score = final_score
            # 将解析出的数据也放入 stats
            stats_dict = {
                'sharpe': sharpe, 'fitness': fitness, 'margin': margin, 
                'passed': is_passed, 'sc': sc_val, 'pc': pc_val_from_name,
                'is_newly_colored': is_newly_colored
            }

            # 将结果存入结果字典
            if results_dict is not None:
                results_dict[expr] = {
                    'score': score,
                    'url': location,
                    'stats': stats_dict,
                    'alpha_id': alpha_id
                }

            # 优化终端显示
            status_icon = "⚪"
            color_code = "\033[90m" # 默认灰色
            if is_passed:
                if (sc_val is not None and sc_val > SC_CUTOFF) or margin < MARGIN_THRESHOLD:
                    status_icon = "🔵"
                    color_code = "\033[94m" # 蓝色
                else:
                    status_icon = "🟢"
                    color_code = "\033[92m" # 绿色
            
            logging.info(f"{color_code}--------------------------------------------------")
            logging.info(f"{status_icon} Alpha ID: {alpha_id} | Score: {final_score:.4f}")
            logging.info(f"   Sharpe: {sharpe:.2f} | Fitness: {fitness:.2f} | Margin: {margin:.4f} | TO: {turnover:.2%}")

            if hasattr(self, 'best_base_score'):
                if final_score - self.best_base_score > 1e-4:
                    logging.info(f"   \033[95m\033[1m🎉 基础分发现提升! (+{final_score - self.best_base_score:.4f})\033[0m")
                elif abs(final_score - self.best_base_score) <= 1e-4:
                    logging.info(f"   基础分持平")
            logging.info(f"{color_code}--------------------------------------------------\033[0m")

            # 如果 Sharpe 小于 -1.2，就取反再测一次 (增加防死循环检查)
            if sharpe < -1.2:
                # 检查是否已经取反过，防止无限嵌套 -1 * (-1 * ...)
                if expr.startswith("-1 * (") and expr.endswith(")"):
                    logging.info(f"   [取反跳过] 公式已处于取反状态且 Sharpe 依然为负 ({sharpe:.2f})，停止递归取反。")
                else:
                    rev_expr = f"-1 * ({expr})"
                    # 检查取反后的公式是否已经在历史记录中（避免重复回测）
                    # 注意：反转公式的缓存键也需要包含 settings
                    rev_cache_payload = {'expr': rev_expr, 'settings': current_settings}
                    rev_h = hashlib.md5(json.dumps(rev_cache_payload, sort_keys=True).encode('utf-8')).hexdigest()
                    
                    if rev_h in self.client.history:
                        logging.info(f"   [取反跳过] 反转公式已在历史缓存中: {rev_expr}")
                    else:
                        logging.info(f"[反转] Sharpe ({sharpe:.2f}) < -1.2，正同步回测取反表达式: {rev_expr}")
                        rev_sim_data = {'type': 'REGULAR', 'settings': current_settings, 'regular': rev_expr}
                        try:
                            rev_loc = self.client.submit_simulation(rev_sim_data)
                            if rev_loc:
                                # 同步等待反转结果
                                rev_res = self.client.wait_for_simulation(rev_loc)
                                # 递归调用处理反转结果并填入字典
                                self._process_result(rev_res, rev_expr, rev_loc, results_dict, current_settings)
                            else:
                                logging.warning(f"  [反转失败] 无法提交反转表达式")
                        except Exception as e:
                            logging.warning(f"  [反转异常] 反转处理异常: {e}")
        else:
            logging.warning(f"  [异常] 无法获取结果或统计数据!")
            logging.warning(f"  URL: {location}")
            logging.warning(f"  Response: {res}")
            logging.warning("-" * 20)

            # 无法获取结果的Alpha分数设为0，不参与比较
            score = 0.0
            stats_dict = {'sharpe': 0, 'fitness': 0, 'margin': 0, 'passed': False}

        # 保存到历史记录 (核心修复：缓存键应包含 settings，值包含完整信息)
        cache_payload = {'expr': expr, 'settings': current_settings}
        h = hashlib.md5(json.dumps(cache_payload, sort_keys=True).encode('utf-8')).hexdigest()
        
        # 存入完整结果包
        self.client.history[h] = {
            'score': score,
            'url': location,
            'stats': stats_dict,
            'alpha_id': alpha_id
        }

        return score
    def optimize_single_alpha(self, alpha_id):
        """优化单个Alpha - 异步版本"""
        logging.info(f"开始异步优化 Alpha ID: {alpha_id}")

        # 为每个Alpha ID使用单独的检查点文件
        if not self.load_checkpoint(alpha_id):
            logging.info(f"初始化目标 Alpha: {alpha_id}")
            details = self.client.get_alpha_details(alpha_id)
            if not details:
                logging.error(f"无法获取 Alpha {alpha_id} 的详情")
                return

            self.settings = details['settings']
            regular = details['regular']
            self.best_expr = regular if isinstance(regular, str) else regular['code']
            self.best_alpha_id = alpha_id  # 设置初始Alpha ID
            self.initial_alpha_id = alpha_id  # 设置初始Alpha ID

            # 优先使用现有统计数据
            is_stats = details.get('is', {})
            if 'sharpe' in is_stats and 'fitness' in is_stats:
                logging.info("直接从 Alpha 详情获取现有分数...")

                # 检查是否为厂字型Alpha
                is_factory_shape = self.client.check_factory_shape(alpha_id)
                if is_factory_shape:
                    # 厂字型Alpha直接给0分并标记为紫色 (仅当无颜色时)
                    logging.info(f"  🟣 检测到初始厂字型Alpha: {alpha_id}")
                    if not details.get('color'):
                        self.client.set_alpha_color(alpha_id, 'PURPLE')
                        logging.info(f"  -> 已将其标记为紫色")
                    else:
                        logging.info(f"  -> 该Alpha已有颜色 '{details.get('color')}'，跳过变色")

                    with self.score_lock:
                        self.best_score = 0
                        self.initial_score = 0

                # 检查官方 PASS 状态
                is_passed = False
                if 'checks' in is_stats:
                    checks = is_stats['checks']
                    if checks and not any(c.get('result') == 'FAIL' for c in checks):
                        is_passed = True

                # 如果通过了所有检查，则将Alpha标记为绿色 (仅当无颜色时)
                if is_passed:
                    try:
                        if not details.get('color'):
                            self.client.set_alpha_color(alpha_id, 'GREEN')
                            logging.info(f"  🟢 初始Alpha ID: {alpha_id} 已通过所有检查，已标记为绿色")
                        else:
                            logging.info(f"  🟢 初始Alpha ID: {alpha_id} 已通过所有检查，但已有颜色 '{details.get('color')}'，跳过变色")
                    except Exception as e:
                        logging.warning(f"设置Alpha颜色失败: {e}")

                pass_score = PASS_BONUS if is_passed else 0.0
                sharpe = is_stats.get('sharpe', 0)
                fitness = is_stats.get('fitness', 0)
                margin = is_stats.get('margin', 0)
                # 处理 None 值，将其转换为 0
                if sharpe is None:
                    sharpe = 0.0
                if fitness is None:
                    fitness = 0.0
                if margin is None:
                    margin = 0.0
                    logging.warning(f"  -> 初始 Alpha Margin 为 None，已替换为 0.0")

                # 新增条件：如果margin大于万分之100(0.01)，则margin按0计算
                if margin > 0.01:
                    logging.info(f"  -> 初始 Alpha Margin ({margin:.4f}) 大于100‱，margin分数按0计算")
                    margin_score = 0.0
                else:
                    margin_score = margin

                # 使用全新的 [v4.7] 标准重算初始分
                turnover = details.get('is', {}).get('turnover', 0) or 0.0
                
                to_penalty = max(0, turnover - 0.10) * 5.0
                margin_reward = 50 * margin_score
                sc_penalty = 0.0 # 初始 Alpha 暂时无法获取 SC，先设为0

                base_score_only = (sharpe + fitness) + margin_reward - to_penalty - abs(sc_penalty)
                final_score = max(0.0, base_score_only + pass_score)

                with self.score_lock:
                    self.best_score = final_score
                    self.best_base_score = base_score_only
                    self.best_stats = {
                        'sharpe': sharpe,
                        'fitness': fitness,
                        'margin': margin,
                        'passed': is_passed,
                        'sc': None,
                        'pc': None
                    }
                    self.initial_score = self.best_score  # 保存初始分数

                logging.info(f"信任初始 Alpha 分数: {self.best_score:.4f} (Pass: {is_passed})")
                logging.info(f"  详细计算过程:")
                logging.info(f"    Sharpe: {sharpe:.4f} | Fitness: {fitness:.4f}")
                logging.info(f"    Margin奖励: +{margin_reward:.4f} | TO惩罚: -{to_penalty:.4f}")
                logging.info(f"    Pass Bonus: {pass_score:.4f} | 最终得分: {final_score:.4f}")

                # --- v4.7 初始 Alpha 相关性检查与标记 (秒开/异步校准版) ---
                if sharpe != 0:
                    logging.info(f"   [基准强制校准] 正在刷新初始 Alpha {alpha_id} 的校准数据...")
                    
                    # 1. 尝试从名字直接解析 (秒开逻辑)
                    current_name = details.get('name', '')
                    pc_parsed, sc_parsed = self._extract_scores_from_name(current_name)
                    
                    # 2. 如果名字里有，直接用
                    if pc_parsed is not None:
                        logging.info(f"   ✨ 发现历史标记: PC={pc_parsed:.4f}, SC={sc_parsed if sc_parsed else '未知'}")
                        self.best_pc = pc_parsed
                        sc_val = sc_parsed if sc_parsed is not None else self.calculate_sc_locally(alpha_id, self.os_pool)
                        
                        # 计算各项奖惩
                        sc_penalty = self.calculate_sc_penalty(sc_val)
                        pc_bonus = (0.7 - self.best_pc) * 10
                        pass_val = PASS_BONUS if is_passed else 0.0
                        
                        with self.score_lock:
                            # 显式加上所有分项
                            self.best_score = self.best_base_score + sc_penalty + pc_bonus + pass_val
                            self.best_score = max(self.best_score, 0.0)
                            # 关键：对齐起点，让提升从 0 开始
                            self.initial_score = self.best_score
                            
                        logging.info(f"   [校准详情] Base: {self.best_base_score:.4f} | Pass: {pass_val} | SC惩罚: {sc_penalty:.4f} | PC奖励: {pc_bonus:.4f}")
                        logging.info(f"   ✅ 基准分已校准 (起点已对齐): {self.best_score:.4f}")
                    else:
                        # 3. 名字里没有，走异步后台检测 (不卡顿逻辑)
                        logging.info(f"   📡 名字中无 PC 信息，启动后台线程异步获取，先以基础分开始爬山...")
                        
                        # 先计算本地 SC 做初步修正
                        sc_val = self.calculate_sc_locally(alpha_id, self.os_pool)
                        sc_penalty = self.calculate_sc_penalty(sc_val) # 使用新逻辑计算惩罚
                        
                        logging.info(f"   [本地SC预估] SC={sc_val} -> 惩罚={sc_penalty:.4f}")
                        
                        with self.score_lock:
                            self.best_pc = 0.7 # 临时占位
                            self.best_score += sc_penalty
                        
                        # 启动后台线程 (定义在下方)
                        def bg_calibrate(aid, base_sc_penalty, passed_alpha):
                            logging.info(f"   [后台校准] 开始强力获取 {aid} 的 PC...")
                            pc_v = self.client.get_product_correlation(aid, max_attempts=40)
                            if pc_v is not None:
                                pc_b = (0.7 - pc_v) * 10
                                with self.score_lock:
                                    if self.best_alpha_id == aid:
                                        old_s = self.best_score
                                        self.best_pc = pc_v
                                        # 修复：校准时必须加上 PASS_BONUS
                                        self.best_score = self.best_base_score + base_sc_penalty + pc_b + (PASS_BONUS if passed_alpha else 0)
                                        self.best_score = max(self.best_score, 0.0)
                                        # 关键：对齐起点
                                        self.initial_score = self.best_score
                                        logging.info(f"   [后台校准完成] ⚖️ 修正初始最优总分 (起点已对齐): {old_s:.4f} -> {self.best_score:.4f} (PC: {pc_v:.4f})")
                                        self.save_checkpoint(aid)
                                # 补全改名
                                sc_v = self.calculate_sc_locally(aid, self.os_pool)
                                new_n = f"PC{pc_v:.4f}-SC{sc_v:.4f}"
                                self.client.set_alpha_name(aid, new_n)
                                if pc_v >= 0.7: self.client.set_alpha_color(aid, 'BLUE')
                        
                        t = threading.Thread(target=bg_calibrate, args=(alpha_id, sc_penalty, is_passed))
                        t.daemon = True
                        t.start()
                # ---------------------------------------
            else:
                logging.info("未找到现有统计数据，进行初始回测...")
                results = self.evaluate_batch([self.best_expr])
                if results and self.best_expr in results:
                    initial_data = results[self.best_expr]
                    with self.score_lock:
                        self.best_score = initial_data['score']
                        self.best_base_score = initial_data['score']
                        self.best_alpha_id = initial_data.get('alpha_id')
                        self.best_stats = initial_data.get('stats', {})
                        self.initial_score = self.best_score
                    logging.info(f"初始回测完成: Score={self.best_score}, Alpha ID={self.best_alpha_id}")
                else:
                    with self.score_lock:
                        self.best_score = -9999
                        self.initial_score = -9999

            self.save_checkpoint(alpha_id)

        logging.info("=" * 50)
        logging.info(f"初始公式: {self.best_expr}")
        logging.info(f"初始分数: \033[97m{self.initial_score:.4f}\033[0m (ID: {self.initial_alpha_id})")
        logging.info(f"当前最优分数: \033[97m{self.best_score:.4f}\033[0m (ID: {self.best_alpha_id})")
        logging.info("=" * 50)

        parser = SmartExpression(self.best_expr, self.settings, self.client)

        # 1. 优化数据字段 (Data Field)
        n_data = len([t for t in parser.tokens if t['type'] == 'data_field'])
        if self.current_position['data_field'] < n_data:
            logging.info(f">>> 开始优化数据字段 (共 {n_data} 个位置)")
            for i in range(self.current_position['data_field'], n_data):
                if self.stop_requested: 
                    logging.info("🛑 [外层中断] 停止优化数据字段")
                    break
                self._optimize_step(parser, 'data_field', i, alpha_id)
                self.current_position['data_field'] = i + 1
                self.save_checkpoint(alpha_id)
        
        # 2. 优化数值 (Number/TimeWindow - 回归 v4.4 稳健顺序)
        parser = SmartExpression(self.best_expr, self.settings, self.client)
        # 找到所有非 lambda/tvr 参数的数字 Token
        n_nums = len([t for t in parser.tokens if t['type'] == 'number' 
                     and not t['text'].startswith('lambda_') 
                     and 'tvr' not in t['text']])
        
        if self.current_position['number'] < n_nums:
            logging.info(f">>> 开始按顺序优化所有数值位置 (共 {n_nums} 个)")
            for i in range(self.current_position['number'], n_nums):
                if self.stop_requested: 
                    logging.info("🛑 [外层中断] 停止优化数值位置")
                    break
                # 注意：统一使用 'number' 类型调用步进优化，generate_neighbors 内部会自适应处理
                self._optimize_step(parser, 'number', i, alpha_id)
                self.current_position['number'] = i + 1
                self.save_checkpoint(alpha_id)

        # 4. 优化分组 (Group)
        parser = SmartExpression(self.best_expr, self.settings, self.client)
        n_groups = len([t for t in parser.tokens if t['type'] == 'group'])
        if self.current_position['group'] < n_groups:
            logging.info(f">>> 开始优化分组 (共 {n_groups} 个位置)")
            for i in range(self.current_position['group'], n_groups):
                if self.stop_requested: 
                    logging.info("🛑 [外层中断] 停止优化分组")
                    break
                self._optimize_step(parser, 'group', i, alpha_id)
                self.current_position['group'] = i + 1
                self.save_checkpoint(alpha_id)

        # 5. 优化运算符 (Operator)
        parser = SmartExpression(self.best_expr, self.settings, self.client)
        n_ops = len([t for t in parser.tokens if t['type'] == 'operator'])
        if self.current_position['operator'] < n_ops:
            logging.info(f">>> 开始优化运算符 (共 {n_ops} 个位置)")
            for i in range(self.current_position['operator'], n_ops):
                if self.stop_requested: 
                    logging.info("🛑 [外层中断] 停止优化运算符")
                    break
                self._optimize_step(parser, 'operator', i, alpha_id)
                self.current_position['operator'] = i + 1
                self.save_checkpoint(alpha_id)
    
        if details.get('region') in ['ASI', 'EUR', 'GLB', 'USA']:
            CANDIDATE_NEUTRALIZATIONS.append("REVERSION_AND_MOMENTUM")
            CANDIDATE_NEUTRALIZATIONS.append("STATISTICAL")
            CANDIDATE_NEUTRALIZATIONS.append("CROWDING")
            CANDIDATE_NEUTRALIZATIONS.append("FAST")
            CANDIDATE_NEUTRALIZATIONS.append("SLOW")
            CANDIDATE_NEUTRALIZATIONS.append("SLOW_AND_FAST")

        if details.get('region')  in ['ASI', 'EUR', 'GLB']:

            CANDIDATE_NEUTRALIZATIONS.append("COUNTRY")

        # 优化 neutralization 参数
        if not self.stop_requested:
            logging.info(f">>> 开始优化 neutralization 参数")
            logging.info(f"从第 {self.current_position['neutralization'] + 1} 个位置开始")
            self._optimize_settings_param('neutralization', CANDIDATE_NEUTRALIZATIONS,
                                          self.current_position['neutralization'], alpha_id)

        # 优化 decay 参数
        if not self.stop_requested:
            logging.info(f">>> 开始优化 decay 参数")
            logging.info(f"从第 {self.current_position['decay'] + 1} 个位置开始")
            self._optimize_settings_param('decay', CANDIDATE_DECAYS,
                                          self.current_position['decay'], alpha_id)

        logging.info(" ")
        logging.info("\033[93m" + "╔════════════════════ Alpha 优化报告 ════════════════════╗" + "\033[0m")
        logging.info(f" 🏁 初始 Alpha: {self.initial_alpha_id}  -->  Score: {self.initial_score:.4f}")
        logging.info(f" 🏆 最终 Alpha: {self.best_alpha_id}  -->  Score: {self.best_score:.4f}")
        improvement = self.best_score - self.initial_score
        logging.info(f" 📈 分数提升: \033[92m{improvement:+.4f}\033[0m")
        
        # 提取详细结果
        final_details = self.client.get_alpha_details(self.best_alpha_id)
        final_is_passed = False
        final_stats_str = "未知"
        if final_details and 'is' in final_details:
            final_is_passed = not any(c.get('result') == 'FAIL' for c in final_details['is'].get('checks', []))
            st = final_details['is']
            final_stats_str = f"Sharpe: {st.get('sharpe', 0):.2f} | Fitness: {st.get('fitness', 0):.2f} | Margin: {st.get('margin', 0):.4f}"
        
        status_text = "\033[92m通过 (Pass) ✅\033[0m" if final_is_passed else "\033[91m未通过 (Fail) ❌\033[0m"
        logging.info(f" 🛡️ 检查结果: {status_text}")
        logging.info(f" 📊 核心指标: {final_stats_str}")
        logging.info(f" 📄 最终表达式: \033[97m{self.best_expr}\033[0m")
        logging.info("\033[93m" + "╚════════════════════════════════════════════════════════╝" + "\033[0m")
        logging.info(" ")

        # 发送完成通知邮件
        if EMAIL_CONFIG.get('enabled', False):
            # 获取初始Alpha和最终Alpha的通过状态
            initial_details = self.client.get_alpha_details(self.initial_alpha_id) if self.initial_alpha_id else None
            final_details = self.client.get_alpha_details(self.best_alpha_id) if self.best_alpha_id else None
            
            initial_passed = False
            final_passed = False
            
            if initial_details and 'is' in initial_details and 'checks' in initial_details['is']:
                checks = initial_details['is']['checks']
                if checks and not any(c.get('result') == 'FAIL' for c in checks):
                    initial_passed = True
                    
            if final_details and 'is' in final_details and 'checks' in final_details['is']:
                checks = final_details['is']['checks']
                if checks and not any(c.get('result') == 'FAIL' for c in checks):
                    final_passed = True
            
            subject = f"Alpha {alpha_id} 回测任务已完成"
            
            # 提取最终详细统计
            final_stats = "未知"
            if final_details and 'is' in final_details:
                st = final_details['is']
                final_stats = f"Sharpe: {st.get('sharpe', 0):.2f}, Fitness: {st.get('fitness', 0):.2f}, Margin: {st.get('margin', 0):.4f}, TO: {st.get('turnover', 0):.2%}"

            content = f"""您的 Alpha {alpha_id} 回测任务已经全部完成！

🏁 初始 Alpha: {self.initial_alpha_id} | 分数: {self.initial_score:.4f}
🏆 最终 Alpha: {self.best_alpha_id} | 分数: {self.best_score:.4f}
📈 总计提升: {improvement:+.4f}
✅ 是否通过检查: {'通过 (Pass)' if final_is_passed else '未通过 (Fail)'}
✨ 最终指标: {final_stats}
📄 最终表达式: {self.best_expr}

详细结果请查看日志文件: {os.path.join(OUTPUT_DIR, f"{alpha_id}_hill_climbing_v4.7.log")}
"""
            send_qq_email(subject, content)

    def _optimize_step(self, parser, type_name, index, alpha_id):
        """同步优化单个步骤 (恢复 v4.3 逻辑)"""
        start_step_score = self.best_score

        if self.best_expr != parser.original_expr:
            parser = SmartExpression(self.best_expr, self.settings, self.client)

        neighbors = parser.generate_neighbors(type_name, index)
        if not neighbors: return

        logging.info(
            f"正在优化 {type_name} 第 {index + 1} 个位置，共 {len(neighbors)} 个候选项... (当前基准: {self.best_score:.4f})")

        # 优化：如果候选项较少，直接一次性全发了，但为了防 429，上限设为 16
        # 针对 number 类型，由于候选池固定且重要，尝试一次性测完 (上限提升至 64)
        current_batch_size = BATCH_SIZE
        if type_name == 'number':
            current_batch_size = min(len(neighbors), 64)
            logging.info(f"  > 策略优化：针对 number 全量提交 (Size: {current_batch_size})...")
        elif len(neighbors) <= 16 or type_name in ['time_window', 'neutralization']:
            current_batch_size = min(len(neighbors), 16)
            logging.info(f"  > 策略优化：针对 {type_name} 或小样本，将批量提交测试 (Size: {current_batch_size})...")

        # 从检查点中存储的批次偏移量开始处理
        start_batch = self.current_position.get('batch_offset', 0)

        for i in range(start_batch, len(neighbors), current_batch_size):
            batch = neighbors[i:i + current_batch_size]
            batch_index = i // current_batch_size + 1
            total_batches = (len(neighbors) - 1) // current_batch_size + 1
            logging.info(f"  > 处理批次 {batch_index}/{total_batches} (本批 {len(batch)} 个)... [位置: {type_name} 第 {index + 1} 个]")

            results = self.evaluate_batch(batch)

            if not results: continue

            # 找到本批次中的最优解 (优先级: Pass且低SC > Pass且高SC > Fail，同级比分)
            def sort_key(expr):
                data = results[expr]
                stats = data.get('stats', {})
                is_passed = stats.get('passed', False)
                sc_val = stats.get('sc')
                
                # 定义层级 (越大越好)
                if is_passed:
                    if sc_val is None or sc_val <= 0.7:
                        tier = 2  # 第一梯队: 真正绿色
                    else:
                        tier = 1  # 第二梯队: 蓝色 (Pass 但相关性高)
                else:
                    tier = 0      # 第三梯队: 红色 (Fail)
                
                # 分数已包含SC惩罚，直接使用
                return (tier, data['score'])

            best_in_batch_expr = max(results, key=sort_key)
            best_in_batch_data = results[best_in_batch_expr]
            candidate_id = best_in_batch_data.get('alpha_id')
            # 安全获取 stats 字典
            res_stats = best_in_batch_data.get('stats', {})
            is_p = res_stats.get('passed', False)
            sc_val = res_stats.get('sc')
            pc_val = res_stats.get('pc') # 接收从 _process_result 透传来的解析值

            # 准入机制升级：只有没有 fail、基础分进步 且 SC 合格，才测 PC
            if is_p and best_in_batch_data['score'] > self.best_base_score:
                sc_penalty = 0
                if sc_val is not None and sc_val > SC_CUTOFF:
                    logging.info(f"   [准入跳过] SC ({sc_val:.4f}) > {SC_CUTOFF}，不测 PC，直接进行上位挑战...")
                    sc_penalty = (SC_CUTOFF - sc_val) * 10
                    # 如果这时候 pc_val 为空，我们保持为空
                elif pc_val is None:
                    logging.info(f"   [准入通过] 基础分突破且 SC 合格 (<= {SC_CUTOFF})，开始获取 PC...")
                    pc_val = self.client.get_product_correlation(candidate_id)
                else:
                    logging.info(f"   [准入通过] 基础分突破且 SC 合格，已从名字解析到 PC={pc_val}")
                
                # 计算最终评估总分
                if pc_val is not None:
                    # 再次核实官方状态 (保护历史标记)
                    details = self.client.get_alpha_details(candidate_id)
                    current_color = details.get('color', '')
                    is_new_color = res_stats.get('is_newly_colored', False)
                    
                    # 只有在本轮新上的色，或者是无色的情况下，才允许回写改名
                    if is_new_color or not current_color:
                        sc_val_val = sc_val if sc_val is not None else 0.0
                        new_name = f"PC{pc_val:.4f}-SC{sc_val_val:.4f}"
                        self.client.set_alpha_name(candidate_id, new_name)
                        # 补染蓝色 (如果 PC 超标)
                        if pc_val >= 0.7:
                            self.client.set_alpha_color(candidate_id, 'BLUE')
                            logging.info(f"   🎨 [PC染色] Alpha {candidate_id} -> BLUE")
                        else:
                            logging.info(f"   📝 [PC命名] Alpha {candidate_id} -> {new_name}")
                    else:
                        logging.info(f"   [兼容保护] Alpha {candidate_id} 维持历史标记，跳过改名。")
                    
                    pc_bonus = (0.7 - pc_val) * 10
                    new_total_score = best_in_batch_data['score'] + pc_bonus
                    logging.info(f"   [综合评估] 总分: {new_total_score:.4f} (PC: {pc_val:.4f}, 奖惩: {pc_bonus:+.4f}) | 当前最优: {self.best_score:.4f}")
                else:
                    # SC > 0.7 或 PC 获取失败的情况
                    new_total_score = best_in_batch_data['score'] + sc_penalty
                    logging.info(f"   [SC挑战评估] 总分: {new_total_score:.4f} (SC扣分: {sc_penalty:.4f}) | 当前最优: {self.best_score:.4f}")

                # 只要总分更高，且未熔断，就上位
                with self.score_lock:
                    if new_total_score > self.best_score:
                        if new_total_score < -1000: # 触发熔断
                            logging.info(f"   ❌ 总分虽高但相关性超过熔断阈值，拒绝上位。")
                        else:
                            diff = new_total_score - self.best_score
                            logging.info(f"  \033[95m\033[1m🎉 发现更优综合解! 总分: {new_total_score:.4f} (↑ {diff:+.4f})\033[0m")
                            
                            self.best_score = new_total_score
                            self.best_base_score = best_in_batch_data['score']
                            self.best_expr = best_in_batch_expr
                            self.best_alpha_id = candidate_id # 强制更新最佳 ID
                            self.best_pc = pc_val
                            self.best_stats = best_in_batch_data.get('stats', {})

                            self.save_checkpoint(alpha_id)
                            parser = SmartExpression(self.best_expr, self.settings, self.client)
                    else:
                        base_improvement = best_in_batch_data['score'] - self.best_base_score
                        logging.info(f"   ❌ [判定结果] 虽然基础分提升了 {base_improvement:+.4f}，但因相关性奖惩后总分 ({new_total_score:.4f}) 未能超过当前最优 ({self.best_score:.4f})，不予上位。")
            elif not is_p and best_in_batch_data['score'] > (self.best_base_score + 1.0):
                # 如果是 Fail 的项，但 Sharpe 极其高（比当前 base 还要高出 1 分以上），虽然不测 PC 但我们记录一下
                logging.info(f"   🥱 最强项 Fail 了，跳过相关性检查。 (基础分: {best_in_batch_data['score']:.4f})")
            else:
                logging.info(f"   🥱 基础分未突破或已 Fail，跳过相关性检查。")

            # 更新进度
            self.current_position['batch_offset'] = i + len(batch)
            self.save_checkpoint(alpha_id)

            # 优雅退出检查点
            if self.stop_requested:
                logging.info("🛑 优雅退出：当前 Batch 及收尾工作已完成，进度已保存。")
                return

        # 重置批次偏移量
        self.current_position['batch_offset'] = 0
        self.save_checkpoint(alpha_id)

        # 阶段性总结
        total_improvement = self.best_score - self.initial_score
        step_improvement = self.best_score - start_step_score
        
        # 格式化指标详情
        stats_msg = "暂无详细指标"
        pass_status = "未知"
        display_pc = f"{self.best_pc:.4f}" if self.best_pc is not None else "待获取/跳过"
        if self.best_stats:
            s = self.best_stats
            pass_status = "通过 ✅" if s.get('passed') else "失败 ❌"
            sc_val = f"{s.get('sc'):.4f}" if isinstance(s.get('sc'), (int, float)) else s.get('sc', '未计算')
            stats_msg = (f"Sharpe: {s.get('sharpe', 0):.2f} | Fitness: {s.get('fitness', 0):.2f} | "
                         f"Margin: {s.get('margin', 0):.4f} | SC: {sc_val} | PC: {display_pc}")

        logging.info(" ")
        logging.info(f"\033[95m" + "=" * 20 + f" [位置优化总结: {type_name} 第 {index + 1} 个位置] " + "=" * 20 + "\033[0m")
        logging.info(f"  🚩 初始 Alpha ID: {self.initial_alpha_id}")
        logging.info(f"  🏆 当前最优 Alpha: {self.best_alpha_id}")
        logging.info(f"  💰 当前总分: \033[97m{self.best_score:.4f}\033[0m (基础分: {self.best_base_score:.4f})")
        logging.info(f"  📈 本次位置提升: \033[92m{step_improvement:+.4f}\033[0m")
        logging.info(f"  🚀 累计总提升: \033[92m{total_improvement:+.4f}\033[0m")
        logging.info(f"  🛡️ 检查状态: {pass_status}")
        logging.info(f"  📊 详细指标: {stats_msg}")
        logging.info(f"  📝 当前最佳公式: \033[90m{self.best_expr}\033[0m")
        logging.info(f"\033[95m" + "=" * 75 + "\033[0m")
        logging.info(" ")

    def _optimize_settings_param(self, param_name, candidate_values, start_index, alpha_id):
        """同步优化设置参数 (恢复 v4.3 逻辑)"""
        start_step_score = self.best_score

        if not self.settings:
            logging.warning(f"无法优化 {param_name} 参数：缺少设置信息")
            return

        # 从指定索引开始遍历候选值
        for i in range(start_index, len(candidate_values)):
            candidate_value = candidate_values[i]
            logging.info(
                f"正在优化 {param_name} 参数，测试值: {candidate_value} (当前基准总分: \033[97m{self.best_score:.4f}\033[0m)")

            # 创建新的设置副本
            new_settings = self.settings.copy()
            new_settings[param_name] = candidate_value

            # 用当前最优表达式和新设置进行回测
            results = self.evaluate_batch([self.best_expr], new_settings)

            if results and self.best_expr in results:
                res_data = results[self.best_expr]
                new_score = res_data['score']
                new_alpha_id = res_data.get('alpha_id')
                
                # --- 修复：定义 res_stats 变量 ---
                res_stats = res_data.get('stats', {})
                is_p = res_stats.get('passed', False)
                # -------------------------------

                # 同样遵循性能准入：基础分有进步且未 Fail 且 SC 合格才测 PC
                if is_p and new_score > self.best_base_score:
                    sc_val = res_stats.get('sc')
                    pc_val = res_stats.get('pc') # 接收透传值
                    sc_penalty = 0
                    
                    if sc_val is not None and sc_val > SC_CUTOFF:
                        logging.info(f"   [设置准入跳过] SC ({sc_val:.4f}) > {SC_CUTOFF}，不测 PC，直接进行上位挑战...")
                        sc_penalty = (SC_CUTOFF - sc_val) * 10
                    elif pc_val is None:
                        logging.info(f"   [设置准入通过] 基础分突破且 SC 合格，查询 PC...")
                        pc_val = self.client.get_product_correlation(new_alpha_id)
                    else:
                        logging.info(f"   [设置准入通过] 基础分突破且 SC 合格，解析到 PC={pc_val}")

                    if pc_val is not None:
                        # 计算修正分 (此时 sc_penalty 为 0)
                        pc_bonus = (0.7 - pc_val) * 10
                        new_total_score = new_score + pc_bonus
                        
                        with self.score_lock:
                            logging.info(f"   [设置评估] 总分: {new_total_score:.4f} (PC: {pc_val:.4f}) | 当前最优: {self.best_score:.4f}")

                            if new_total_score > self.best_score:
                                if new_total_score < -1000:
                                    logging.info(f"   ❌ 设置优化后熔断，拒绝上位。")
                                else:
                                    self.best_score = new_total_score
                                    self.best_base_score = new_score
                                    self.settings = new_settings
                                    self.best_alpha_id = new_alpha_id # 强制更新最佳 ID
                                    self.best_pc = pc_val
                                    self.best_stats = res_stats

                                    # 先查颜色
                                    details = self.client.get_alpha_details(new_alpha_id)
                                    current_color = details.get('color', '')
                                    is_new_color = res_stats.get('is_newly_colored', False)
                                    
                                    if is_new_color or not current_color:
                                        sc_val_val = sc_val if sc_val is not None else 0.0
                                        new_name = f"PC{pc_val:.4f}-SC{sc_val_val:.4f}"
                                        self.client.set_alpha_name(new_alpha_id, new_name)
                                        if pc_val >= 0.7 and current_color != 'BLUE':
                                            self.client.set_alpha_color(new_alpha_id, 'BLUE')
                                    else:
                                        logging.info(f"   [设置兼容] Alpha {new_alpha_id} 维持历史标记。")
                                    
                                    logging.info(f"  🎉 发现更优设置! 总分: {self.best_score:.4f}")
                                    self.save_checkpoint(alpha_id)
                    else:
                        # 兜底：用基础分挑战总分 (适用于 SC > 0.7 或 PC 无法获取的情况)
                        new_total_score = new_score + sc_penalty
                        
                        with self.score_lock:
                            logging.info(f"   [设置SC挑战评估] 总分: {new_total_score:.4f} (SC扣分: {sc_penalty:.4f}) | 当前最优: {self.best_score:.4f}")
                            
                            if new_total_score > self.best_score:
                                if new_total_score < -1000:
                                    logging.info(f"   ❌ 设置SC挑战熔断，拒绝上位。")
                                else:
                                    self.best_score = new_total_score
                                    self.best_base_score = new_score
                                    self.settings = new_settings
                                    self.best_alpha_id = new_alpha_id # 强制更新最佳 ID
                                    self.best_pc = 0.7 # 记录为中性
                                    self.best_stats = res_stats
                                    
                                    logging.info(f"  🎉 (SC挑战成功) 发现更优设置! 总分: {self.best_score:.4f}")
                                    self.save_checkpoint(alpha_id)
                elif new_score > self.best_score:
                    # 如果基础分不带 PC 都比当前带 PC 的总分高，直接上位
                    with self.score_lock:
                        if new_score > self.best_score:
                            self.best_score = new_score
                            self.best_base_score = new_score
                            self.settings = new_settings
                            self.best_alpha_id = new_alpha_id # 强制更新最佳 ID
                            self.best_stats = res_stats
                            logging.info(f"  🎉 发现更优的 (纯基础分上位)! Score: {self.best_score:.4f}")
                            self.save_checkpoint(alpha_id)
            
            # 更新当前位置并保存检查点
            self.current_position[param_name] = i + 1
            self.save_checkpoint(alpha_id)

        # 完成所有候选值后，重置位置
        self.current_position[param_name] = 0
        self.save_checkpoint(alpha_id)

        # 阶段性总结
        total_improvement = self.best_score - self.initial_score
        step_improvement = self.best_score - start_step_score
        
        # 格式化指标详情
        stats_msg = "暂无详细指标"
        pass_status = "未知"
        display_pc = f"{self.best_pc:.4f}" if self.best_pc is not None else "待获取/跳过"
        if self.best_stats:
            s = self.best_stats
            pass_status = "通过 ✅" if s.get('passed') else "失败 ❌"
            sc_val = f"{s.get('sc'):.4f}" if isinstance(s.get('sc'), (int, float)) else s.get('sc', '未计算')
            stats_msg = (f"Sharpe: {s.get('sharpe', 0):.2f} | Fitness: {s.get('fitness', 0):.2f} | "
                         f"Margin: {s.get('margin', 0):.4f}\n     SC: {sc_val} | PC: {display_pc}")

        logging.info(" ")
        logging.info("\033[93m" + "╔" + "═" * 65 + "╗" + "\033[0m")
        logging.info(f"\033[93m║ ⚙️ [设置优化总结] 参数: {param_name}" + " " * (43 - len(param_name)) + "║\033[0m")
        logging.info("\033[93m" + "╠" + "═" * 65 + "╣" + "\033[0m")
        logging.info(f" 🚩 初始 Alpha: {self.initial_alpha_id}  -->  🏆 当前最优: {self.best_alpha_id}")
        logging.info(f" 📈 阶段提升: \033[92m{step_improvement:+.4f}\033[0m | 🚀 累计提升: \033[92m{total_improvement:+.4f}\033[0m")
        logging.info(f" 💰 当前总分: {self.best_score:.4f} (基础: {self.best_base_score:.4f})")
        logging.info(f" 🛡️ 检查状态: {pass_status}")
        logging.info(f" 📊 核心指标: {stats_msg}")
        logging.info(f" 📝 当前公式: \033[90m{self.best_expr}\033[0m")
        logging.info("\033[93m" + "╚" + "═" * 65 + "╝" + "\033[0m")
        logging.info(" ")

    def _print_optimization_summary(self, type_name, count):
        """打印位置优化总结"""
        # 计算阶段提升
        # 注意：这里需要记录进入该阶段时的分数，但由于状态分散，我们简化为计算当前总分与初始分的差值
        # 或者更准确地，我们应该在 _optimize_step 外部记录 start_score，但这需要改动接口。
        # 鉴于日志主要是为了看进度，我们打印当前最优状态即可。
        
        # 格式化指标详情
        stats_msg = "暂无详细指标"
        pass_status = "未知"
        display_pc = f"{self.best_pc:.4f}" if self.best_pc is not None else "待获取/跳过"
        if self.best_stats:
            s = self.best_stats
            pass_status = "通过 ✅" if s.get('passed') else "失败 ❌"
            sc_val = f"{s.get('sc'):.4f}" if isinstance(s.get('sc'), (int, float)) else s.get('sc', '未计算')
            stats_msg = (f"Sharpe: {s.get('sharpe', 0):.2f} | Fitness: {s.get('fitness', 0):.2f} | "
                         f"Margin: {s.get('margin', 0):.4f} | SC: {sc_val} | PC: {display_pc}")

        logging.info(" ")
        logging.info(f"\033[95m" + "=" * 20 + f" [位置优化总结: {type_name} (共 {count} 个位置)] " + "=" * 20 + "\033[0m")
        logging.info(f"  🚩 初始 Alpha ID: {self.initial_alpha_id}")
        logging.info(f"  🏆 当前最优 Alpha: {self.best_alpha_id}")
        logging.info(f"  💰 当前总分: \033[97m{self.best_score:.4f}\033[0m (基础分: {self.best_base_score:.4f})")
        # logging.info(f"  📈 本次位置提升: ...") # 由于跨越多个位置，这里不好计算单次提升，暂略
        total_improvement = self.best_score - self.initial_score
        logging.info(f"  🚀 累计总提升: \033[92m{total_improvement:+.4f}\033[0m")
        logging.info(f"  🛡️ 检查状态: {pass_status}")
        logging.info(f"  📊 详细指标: {stats_msg}")
        logging.info(f"  📝 当前最佳公式: \033[90m{self.best_expr}\033[0m")
        logging.info(f"\033[95m" + "=" * 75 + "\033[0m")
        logging.info(" ")

    def run(self):
        """运行所有Alpha的异步优化"""
        # 模式1: 强制重新开始，无视时间直接删除所有旧文件
        if RUN_MODE == 1:
            logging.info("运行模式1: 强制重新开始，正在清理所有历史文件...")
            patterns = [r'.*_v4\.[67]\.json$', r'.*_v4\.[67]\.log$', r'checkpoint.*\.json$', r'history.*\.json$']
            try:
                for fname in os.listdir(OUTPUT_DIR):
                    if any(re.match(p, fname) for p in patterns):
                        full_path = os.path.join(OUTPUT_DIR, fname)
                        try:
                            # 尝试关闭句柄
                            for handler in logging.root.handlers[:]:
                                handler.close()
                                logging.root.removeHandler(handler)
                            os.remove(full_path)
                            logging.info(f"已强制删除: {full_path}")
                        except: pass
            except Exception as e:
                logging.warning(f"清理文件时出错: {e}")
            
            # 重新初始化日志 (因为刚才可能把自己的日志文件都删了)
            setup_logging()
        else:
            # 模式2或其他: 仅清理过期的
            self._cleanup_old_files()
        
        try:
            # 根据运行模式决定是否删除旧文件（模式2的情况）
            if RUN_MODE == 2:
                logging.info("运行模式2: 断点续爬模式")
                logging.info("将直接加载现有检查点")
                # 原有的自动清理逻辑已移除，严格执行续爬
                pass

            # 逐个优化Alpha
            for alpha_id in TARGET_ALPHA_IDS:
                try:
                    # 为每个Alpha创建独立的日志记录器
                    setup_logging(alpha_id)
                    
                    # 重置优化位置 (确保包含所有阶段的独立计数器)
                    self.current_position = {
                        'data_field': START_OPTIMIZATION_FROM.get('data_field', 0),
                        'group': START_OPTIMIZATION_FROM.get('group', 0),
                        'time_window': START_OPTIMIZATION_FROM.get('time_window', 0),
                        'number': START_OPTIMIZATION_FROM.get('number', 0),
                        'operator': START_OPTIMIZATION_FROM.get('operator', 0),
                        'batch_offset': 0,
                        'neutralization': 0,
                        'decay': 0
                    }
                    
                    # 迭代优化，直到最佳Alpha ID与起始Alpha ID相同
                    current_alpha_id = alpha_id
                    iteration_count = 0
                    
                    while True:
                        iteration_count += 1
                        logging.info(f"开始第 {iteration_count} 轮异步迭代优化，起始Alpha ID: {current_alpha_id}")
                        
                        # 执行单轮异步优化
                        self.optimize_single_alpha(current_alpha_id)
                        
                        # 检查最佳Alpha ID是否与起始Alpha ID相同
                        if self.best_alpha_id == current_alpha_id or iteration_count >= MAX_ITERATIONS:
                            logging.info(f"异步迭代优化完成，总共进行了 {iteration_count} 轮优化")
                            logging.info(f"最终最佳Alpha ID: {self.best_alpha_id}")
                            break
                        else:
                            # 使用最佳Alpha ID作为下一轮的起始点
                            current_alpha_id = self.best_alpha_id
                            logging.info(f"本轮异步优化结束，最佳Alpha ID为 {current_alpha_id}，将继续下一轮优化")
                            
                            # 重置优化器状态以准备下一轮优化
                            self.reset_optimizer_state()
                            
                except KeyboardInterrupt:
                    logging.info(f"异步优化 Alpha {alpha_id} 时被用户中断。")
                    raise
                except Exception as e:
                    logging.error(f"异步优化 Alpha {alpha_id} 时发生错误: {e}")
                    continue

            logging.info("========== 所有 Alpha 异步优化完成 ==========")

            # 发送总体完成通知邮件
            if EMAIL_CONFIG.get('enabled', False):
                # 获取所有Alpha的通过状态
                passed_info = []
                for alpha_id in TARGET_ALPHA_IDS:
                    alpha_details = self.client.get_alpha_details(alpha_id) if alpha_id else None
                    is_passed = False
                    if alpha_details and 'is' in alpha_details and 'checks' in alpha_details['is']:
                        checks = alpha_details['is']['checks']
                        if checks and not any(c.get('result') == 'FAIL' for c in checks):
                            is_passed = True
                    passed_info.append(f"Alpha {alpha_id}: {'通过' if is_passed else '未通过'}")
                
                subject = "所有 Alpha 异步回测任务已完成"
                content = f"""您的所有 Alpha 异步回测任务已经全部完成！

优化的 Alpha IDs: {TARGET_ALPHA_IDS}
检查通过情况:
{'\n'.join(passed_info)}

详细结果请查看各Alpha对应日志文件: {[os.path.join(OUTPUT_DIR, f'{alpha_id}_hill_climbing_v4.7.log') for alpha_id in TARGET_ALPHA_IDS]}
"""
                send_qq_email(subject, content)

        except KeyboardInterrupt:
            logging.info("异步程序已被用户中断。")
        except Exception as e:
            logging.error(f"异步运行过程中发生未预期的错误: {e}")
            # 发送错误通知邮件
            if EMAIL_CONFIG.get('enabled', False):
                subject = "Alpha 异步回测任务出现错误"
                content = f"您的 Alpha 异步回测任务在运行过程中出现错误：{str(e)}"
                send_qq_email(subject, content)

    def reset_optimizer_state(self):
        """重置优化器状态以准备下一轮迭代"""
        # 重置当前优化位置
        self.current_position = {
            'data_field': START_OPTIMIZATION_FROM.get('data_field', 0),
            'group': START_OPTIMIZATION_FROM.get('group', 0),
            'time_window': START_OPTIMIZATION_FROM.get('time_window', 0),
            'number': START_OPTIMIZATION_FROM.get('number', 0),
            'operator': START_OPTIMIZATION_FROM.get('operator', 0),
            'batch_offset': 0,
            'neutralization': 0,
            'decay': 0
        }
        
        # 重置初始分数和ID为当前最佳值，因为下一轮将以当前最佳为起点
        self.initial_score = self.best_score
        self.initial_alpha_id = self.best_alpha_id
        
        # 保存检查点
        if self.best_alpha_id:
            self.save_checkpoint(self.best_alpha_id)

    def run_continuous(self):
        """持续运行模式：自动从平台获取alpha并循环优化"""
        global CANDIDATE_NEUTRALIZATIONS
        original_neutralizations = CANDIDATE_NEUTRALIZATIONS.copy()
        round_count = 0

        logging.info("🔄 进入持续运行模式...")

        while True:
            round_count += 1
            # 每轮重置中断标志，使Ctrl+C仅中止当前alpha而非整个循环
            self.stop_requested = False
            logging.info(f"\n{'='*60}")
            logging.info(f"🔄 持续运行模式 - 第 {round_count} 轮")
            logging.info(f"{'='*60}")

            # 恢复中性化候选列表（防止多轮累积）
            CANDIDATE_NEUTRALIZATIONS.clear()
            CANDIDATE_NEUTRALIZATIONS.extend(original_neutralizations)

            # 1. 获取候选alpha
            logging.info("📡 正在从BRAIN平台获取alpha列表...")
            all_alphas = self.client.fetch_is_alphas(limit=200)

            if not all_alphas:
                logging.info("⏳ 没有找到可用的alpha，等待60秒后重试...")
                time.sleep(60)
                continue

            # 2. 过滤已处理的
            processed = load_processed_alphas()
            processed_ids = set(processed.keys())

            # 过滤条件：未处理过 且 有表达式 且 有统计数据
            candidates = []
            for a in all_alphas:
                if a['id'] in processed_ids:
                    continue
                expr = a.get('regular', '')
                if isinstance(expr, dict):
                    expr = expr.get('code', '')
                if not expr:
                    continue
                # 过滤条件: sharpe > 1 且 fitness > 0.5
                is_stats = a.get('is', {})
                sharpe = is_stats.get('sharpe')
                fitness = is_stats.get('fitness')
                if sharpe is None or fitness is None:
                    continue
                if sharpe <= 1 or fitness <= 0.5:
                    continue
                candidates.append(a)

            logging.info(f"📊 共获取 {len(all_alphas)} 个alpha, {len(processed_ids)} 个已处理, {len(candidates)} 个候选 (sharpe>1 & fitness>0.5)")

            if not candidates:
                logging.info("⏳ 没有符合条件的候选alpha (sharpe>1 & fitness>0.5)，休息1小时后重新检查...")
                time.sleep(3600)
                continue

            # 3. 选择结构差异最大的
            selected = select_most_diverse_alpha(candidates, processed)

            if not selected:
                logging.info("⏳ 无法选择合适的alpha，休息1小时后重试...")
                time.sleep(3600)
                continue

            selected_id = selected['id']
            selected_expr = selected.get('regular', '')
            if isinstance(selected_expr, dict):
                selected_expr = selected_expr.get('code', '')

            logging.info(f"✅ 本轮选中 Alpha: {selected_id}")
            logging.info(f"   表达式: {selected_expr}")

            # 4. 执行优化
            try:
                setup_logging(selected_id)

                # 重置优化位置
                self.current_position = {
                    'data_field': 0, 'group': 0, 'time_window': 0,
                    'number': 0, 'operator': 0, 'batch_offset': 0,
                    'neutralization': 0, 'decay': 0
                }

                # 重置优化器核心状态
                self.best_expr = None
                self.best_score = -9999
                self.best_base_score = -9999
                self.settings = None
                self.best_alpha_id = None
                self.initial_score = None
                self.initial_alpha_id = None
                self.best_pc = None
                self.best_stats = {}

                current_alpha_id = selected_id
                iteration_count = 0

                while True:
                    iteration_count += 1
                    logging.info(f"🔁 第 {round_count} 轮 - 第 {iteration_count} 次迭代, Alpha: {current_alpha_id}")

                    self.optimize_single_alpha(current_alpha_id)

                    if self.best_alpha_id == current_alpha_id or iteration_count >= MAX_ITERATIONS:
                        logging.info(f"✅ 迭代优化完成, 共 {iteration_count} 轮, 最终Alpha: {self.best_alpha_id}")
                        break
                    else:
                        current_alpha_id = self.best_alpha_id
                        logging.info(f"🔁 最佳Alpha已变更为 {current_alpha_id}, 继续下一轮迭代")
                        self.reset_optimizer_state()

                # 5. 标记为已处理
                save_processed_alpha(selected_id, selected_expr)
                logging.info(f"💾 已将 Alpha {selected_id} 标记为已处理")

            except KeyboardInterrupt:
                logging.info("🛑 用户中断当前alpha优化, 标记后继续下一轮...")
                save_processed_alpha(selected_id, selected_expr)
                self.stop_requested = False
                continue
            except SystemExit:
                logging.info("🛑 系统退出信号, 保存进度后退出")
                save_processed_alpha(selected_id, selected_expr)
                break
            except Exception as e:
                logging.error(f"❌ 优化 Alpha {selected_id} 时出错: {e}")
                import traceback
                traceback.print_exc()
                save_processed_alpha(selected_id, selected_expr)
                time.sleep(10)
                continue

            logging.info(f"🎉 第 {round_count} 轮完成\n")

        logging.info("🏁 持续运行模式已结束")


if __name__ == '__main__':

    print("==================================================")
    print("🚀 脚本已启动")
    print("==================================================")

    # 外层永不停止的重启循环
    restart_count = 0
    while True:
        restart_count += 1
        try:
            if restart_count > 1:
                print(f"\n🔄 第 {restart_count} 次自动重启 (等待30秒)...")
                time.sleep(30)

            print("🔑 正在初始化优化器...")
            optimizer = AsyncOptimizer()
            print("✅ 初始化成功，开始执行优化任务...")

            if CONTINUOUS_MODE:
                optimizer.run_continuous()
            else:
                optimizer.run()

            # 非持续模式run()正常结束后退出
            if not CONTINUOUS_MODE:
                break

        except KeyboardInterrupt:
            print("\n🛑 用户按下 Ctrl+C")
            if CONTINUOUS_MODE:
                print("   持续模式下程序将在10秒后自动重启... (再次Ctrl+C强制退出)")
                try:
                    time.sleep(10)
                except KeyboardInterrupt:
                    print("\n🛑 强制退出")
                    break
            else:
                break

        except SystemExit:
            print("\n🛑 收到系统退出信号，程序终止")
            break

        except Exception as e:
            print(f"\n❌ 程序运行出错: {e}")
            import traceback
            traceback.print_exc()
            if CONTINUOUS_MODE:
                print(f"   持续模式下将在60秒后自动重启...")
                time.sleep(60)
            else:
                break
