# 精准剪枝器(即插即用版)-----SUE因子横向点塔工具篇代码优化

- **链接**: [Commented] 精准剪枝器即插即用版-----SUE因子横向点塔工具篇代码优化.md
- **作者**: JY35107
- **发布时间/热度**: 7个月前, 得票: 25

## 帖子正文

### Hi , Everybody!

### 我是新人顾问Kola。

> 很高兴之前分享的两个因子收到了很多反馈，让我十分鼓舞，没看过的小伙伴这边贴出模板链接。

```
SUE因子篇一：https://support.worldquantbrain.com/hc/en-us/community/posts/34144202102551--Alpha%E7%81%B5%E6%84%9F-%E6%A0%87%E5%87%86%E5%8C%96%E7%9B%88%E5%88%A9%E6%84%8F%E5%A4%96-SUE%E5%9B%A0%E5%AD%90 SUE因子篇二：../MZ45384/[Commented] 【Alpha模板】标准化盈利意外-SUE因子2升级篇--全市场横向无痛点塔 AnlFnd附模板Alpha Template.md?page=1#community_comment_36030940286743 
```

其中，看到有小伙伴关于 **精准筛选某一相关含义数据字段（如eps/cap等）用于模板批量回测** 的讨论。

这里，我想到一个非常经常遇到的情景：我在论坛中很高兴的找到了一个漂亮的模板，或者和AI一起学习了一个非常简洁的研究论文，很好，下一步就可以开始酷酷生产啦！But，似乎接下来需要先找刚才文章要求的主信号（如eps、return、cap...）了，但是怎么精准且精简的找到他们呢（正如你说知道的，许多时候直接搜索可能存在覆盖面不够广泛的情况）？

基于这样的场景需求，我制作了一套高效剪枝无关字段，专门用于捕获 **Data名称及Data描述中含有目标词** 的代码！代码我在帖中分享出来，大家可以一起参考看看，希望能同大家多多点塔啦！！！

一句话介绍： **这是一个用于在平台上自动搜索想要的具体含义相关字段，提前做好无关剪枝后基于有效目标字段生成和回测指定模板的生产工具。**

**让我们为模板插上翅膀，一起大展宏图吧！**

欢迎大家使用及共创，并恳切各位看官喜欢的话记得按赞♥、讨论✉️！

---------------------------------------------------------------------------------------------------------------

**一、主要功能**

- 🔍 自动搜索包含 指定 字段的数据集

- 📊 提取和筛选 指定 相关字段（字段名或描述中包含该字段）

- 🧮 基于模板自动生成 Alpha 表达式

- 🚀 批量回测生成的 Alpha 表达式

- 💾 自动保存处理进度和结果

二、 **配置说明**

**确保安装 wqb、pandas**

**pip install wqb**

在运行程序前，放在有 **machine_lib.py** 的文件夹中，打开该文件，在配置区域填写以下必要配置：

1. 登录凭证（必需）

YOUR_NAME = " [your_email@example.com](mailto:your_email@example.com) "  # 替换账号

YOUR_PASSWORD = "your_password"      # 替换密码

```

1. 文件路径配置（可选）

PROGRESS_FILE = 'eps_processing_progress.json'           # 进度文件

EPS_FIELDS_FILE = 'eps_fields_found.json'                # EPS字段记录

EPS_ALPHA_EXPRESSIONS_FILE = 'eps_alpha_expressions.json' # Alpha表达式

```

1. 数据集筛选条件（用来筛选字段的条件，填入想要的关键词和对于字段的alphacount要求，这里以eps为例）

MIN_ALPHA_COUNT = 0  # 最小Alpha数量阈值

EPS_RELATED_KEYWORDS = ['eps']  # EPS相关关键词

```

1. Alpha表达式模板（填入所有想跑的模板，替换字段的部分写入{FIELD}）

ALPHA_TEMPLATES = [

"x={FIELD};ts_av_diff(x, 120)/ts_std_dev(x, 220)",

"current_eps ={FIELD};prev_eps = ts_delay(current_eps , 120);eps_std = ts_std_dev(current_eps , 220);SUE = (current_eps - prev_eps) / eps_std;ts_std_dev(SUE, 21) < 2.0"

]

```

- `{FIELD}` 会被自动替换为实际的字段ID

- 可以添加多个模板，每个找到的EPS字段都会为每个模板生成一个表达式

1. Decay值配置（可选）

DEFAULT_DECAY = 6      # 默认decay值

DECAY_ESTIMATE = 8     # estimate相关字段的decay值

DECAY_ACTUAL = 5       # actual相关字段的decay值

```

1. 批量回测参数（可选）

BACKTEST_PARAMS_GLB = (10, 4)      # GLB区域的回测参数 (任务池大小, 并发数)

BACKTEST_PARAMS_OTHER = (10, 8)    # 其他区域的回测参数

```

1. 默认处理组合（遍历的region组合，外循环）

DEFAULT_REGION_UNIVERSE_COMBINATIONS = [

("ASI", "ILLIQUID_MINVOL1M", 1),

("GLB", "MINVOL1M", 1),

]

- 格式：`[(region, universe, delay), ...]`

**三、 命令行参数详解**

| 参数 | 类型 | 默认值 | 说明 |

|------|------|--------|------|

| `--start` | int | 1 | 从第几个数据集开始处理 |

| `--no-simulate` | flag | False | 只生成表达式，不进行回测 |

**四、运行日志截图**

**![图片](images/img_f7b2c8edc1.png)**

图1：遍历当前region、universe、delay组合的全部数据集筛选出符合条件的字段

![图片](images/img_f154f73cf5.png)

图2：字段收集完毕以后统一生成并批量回测

**五、源码**

```
import datetimeimport pandas as pdfrom machine_lib import *from wqb import WQBSessionimport asyncioimport wqbimport timeimport osimport jsonimport argparseimport re# ============================================================================# 配置区域 - 所有可配置的设置都在这里# ============================================================================# --- 登录凭证 ---# 请在此填写您的WorldQuant BRAIN平台登录信息YOUR_NAME = ""  # 您的用户名/邮箱YOUR_PASSWORD = ""  # 您的密码# --- 文件路径配置 ---PROGRESS_FILE = 'eps_processing_progress.json'  # 进度文件路径EPS_FIELDS_FILE = 'eps_fields_found.json'  # EPS字段记录文件路径EPS_ALPHA_EXPRESSIONS_FILE = 'eps_alpha_expressions.json'  # 生成的Alpha表达式文件路径# --- 重试设置 ---MAX_RETRIES = 5  # 最大重试次数RETRY_DELAY_INITIAL = 15  # 初始重试延迟（秒）RETRY_DELAY_MULTIPLIER = 1.5  # 重试延迟增长倍数RETRY_DELAY_MAX = 60  # 最大重试延迟（秒）BATCH_SIMULATE_MAX_RETRIES = 3  # 批量回测最大重试次数BATCH_SIMULATE_RETRY_DELAY = 30  # 批量回测重试延迟（秒）# --- 数据集筛选条件 ---MIN_ALPHA_COUNT = 0  # 字段要满足的最小Alpha数量阈值（筛选数据集时使用）EPS_RELATED_KEYWORDS = [  # 相关关键词（用于筛选数据集）    'eps']# --- Alpha表达式模板 ---ALPHA_TEMPLATES = [        "x={FIELD};ts_av_diff(x, 120)/ts_std_dev(x, 220)",        "current_eps ={FIELD};prev_eps = ts_delay(current_eps , 120);eps_std = ts_std_dev(current_eps , 220);SUE = (current_eps - prev_eps) / eps_std;ts_std_dev(SUE, 21) < 2.0"    ]# --- Decay值配置 ---DEFAULT_DECAY = 6  # 默认decay值DECAY_ESTIMATE = 8  # estimate相关字段的decay值DECAY_ACTUAL = 5  # actual相关字段的decay值# --- 批量回测参数配置 ---# 格式: (任务池大小, 并发数)BACKTEST_PARAMS_GLB = (10, 4)  # GLB区域的回测参数BACKTEST_PARAMS_OTHER = (10, 8)  # 其他区域的回测参数# --- 默认处理组合 ---# 格式: [(region, universe, delay), ...]DEFAULT_REGION_UNIVERSE_COMBINATIONS = [    ("USA", "TOP3000", 1),    ("GLB", "TOP3000", 1),]# ============================================================================# 配置区域结束# ============================================================================def parse_args():    """解析命令行参数"""    parser = argparse.ArgumentParser(description='EPS Alpha 生成程序')    parser.add_argument('--start', type=int, default=1,                      help='从第几个数据集开始处理 (默认: 1)')    parser.add_argument('--no-simulate', action='store_true',                      help='只生成表达式，不进行回测')    return parser.parse_args()def load_progress():    """加载处理进度"""    if os.path.exists(PROGRESS_FILE):        with open(PROGRESS_FILE, 'r') as f:            return json.load(f)    return {}def save_progress(progress):    """保存处理进度"""    with open(PROGRESS_FILE, 'w') as f:        json.dump(progress, f, indent=1)def load_eps_fields():    """加载已找到的EPS字段"""    if os.path.exists(EPS_FIELDS_FILE):        with open(EPS_FIELDS_FILE, 'r') as f:            return json.load(f)    return {}def save_eps_fields(eps_fields):    """保存找到的EPS字段"""    with open(EPS_FIELDS_FILE, 'w') as f:        json.dump(eps_fields, f, indent=1)def load_alpha_expressions():    """加载已生成的Alpha表达式"""    if os.path.exists(EPS_ALPHA_EXPRESSIONS_FILE):        with open(EPS_ALPHA_EXPRESSIONS_FILE, 'r') as f:            return json.load(f)    return {}def save_alpha_expressions(alpha_expressions):    """保存生成的Alpha表达式"""    with open(EPS_ALPHA_EXPRESSIONS_FILE, 'w') as f:        json.dump(alpha_expressions, f, indent=1)def is_processed(progress, region, universe, delay, dataset_id):    """检查是否已经处理过该组合"""    key = f"{region}_{universe}_{delay}_{dataset_id}"    return key in progressdef mark_as_processed(progress, region, universe, delay, dataset_id):    """标记该组合为已处理"""    key = f"{region}_{universe}_{delay}_{dataset_id}"    progress[key] = {        'region': region,        'universe': universe,        'delay': delay,        'dataset_id': dataset_id,        'processed_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    }    save_progress(progress)def initialize_session(region, universe, delay):    """初始化会话"""    max_retries = MAX_RETRIES    retry_delay = RETRY_DELAY_INITIAL       for retry in range(max_retries):        try:            print(f"正在初始化会话 (尝试 {retry + 1}/{max_retries})...")            s = WQBSession((YOUR_NAME, YOUR_PASSWORD))                       # 测试连接            test_url = "https://api.worldquantbrain.com/data-sets?limit=1"            test_resp = s.get(test_url, timeout=30)            if test_resp.status_code == 200:                print("会话初始化成功，连接测试通过")            else:                print(f"连接测试失败，状态码: {test_resp.status_code}")                raise Exception(f"连接测试失败: {test_resp.status_code}")                       pd.set_option('display.max_columns', None)            pd.set_option('display.width', 1000)            today = datetime.date.today()            date_range = {                'previous': (today - datetime.timedelta(days=1)).strftime("%m-%d"),                'next': (today + datetime.timedelta(days=1)).strftime("%m-%d")            }            return s, date_range                   except Exception as e:            error_msg = str(e).lower()            is_network_error = any(keyword in error_msg for keyword in [                'connection', 'timeout', 'reset', 'protocol', 'ssl', 'tls',                '远程主机', '连接', '超时', '重置'            ])                       if retry < max_retries - 1:                if "API rate limit exceeded" in str(e):                    print(f"认证时触发速率限制，等待 {retry_delay} 秒后重试...")                elif is_network_error:                    print(f"网络连接错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")                    print(f"等待 {retry_delay} 秒后重试...")                else:                    print(f"认证错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")                    print(f"等待 {retry_delay} 秒后重试...")                               time.sleep(retry_delay)                retry_delay = min(retry_delay * RETRY_DELAY_MULTIPLIER, RETRY_DELAY_MAX)                continue            else:                print(f"会话初始化失败，已达到最大重试次数 ({max_retries})")                print(f"最后错误: {str(e)}")                raise edef get_datasets(s, region, delay, universe):    """获取所有数据集，使用分页功能"""    max_retries = MAX_RETRIES    retry_delay = RETRY_DELAY_INITIAL    limit = 50    offset = 0    all_datasets = []       while True:        for retry in range(max_retries):            try:                url = f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region={region}&delay={delay}&universe={universe}&limit={limit}&offset={offset}"                               headers = {                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',                    'Accept': 'application/json, text/plain, */*',                    'Accept-Language': 'en-US,en;q=0.9',                    'Accept-Encoding': 'gzip, deflate, br',                    'Connection': 'keep-alive',                    'Upgrade-Insecure-Requests': '1'                }                               resp = s.get(url, headers=headers, timeout=30)                data = resp.json()                               current_datasets = data.get('results', [])                all_datasets.extend(current_datasets)                               total_count = data.get('count', 0)                print(f"已获取 {len(all_datasets)}/{total_count} 个数据集")                               if len(current_datasets) < limit:                    return pd.DataFrame(all_datasets)                               offset += limit                break                           except Exception as e:                error_msg = str(e).lower()                is_network_error = any(keyword in error_msg for keyword in [                    'connection', 'timeout', 'reset', 'protocol', 'ssl', 'tls',                    '远程主机', '连接', '超时', '重置'                ])                               if retry < max_retries - 1:                    if "API rate limit exceeded" in str(e):                        print(f"获取数据集时触发速率限制，等待 {retry_delay} 秒后重试...")                    elif is_network_error:                        print(f"网络连接错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")                        print(f"等待 {retry_delay} 秒后重试...")                    else:                        print(f"未知错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")                        print(f"等待 {retry_delay} 秒后重试...")                                       time.sleep(retry_delay)                    retry_delay = min(retry_delay * RETRY_DELAY_MULTIPLIER, RETRY_DELAY_MAX)                    continue                else:                    print(f"获取数据集失败，已达到最大重试次数 ({max_retries})")                    print(f"最后错误: {str(e)}")                    raise e       return pd.DataFrame(all_datasets)def filter_datasets_for_eps(datasets_df, region, universe, delay):    """筛选数据集，优先选择可能包含EPS字段的数据集"""    print(f"数据集列名: {datasets_df.columns.tolist()}")       # 筛选条件：alphaCount >= MIN_ALPHA_COUNT，优先选择包含EPS相关关键词的数据集    filtered_df = datasets_df[        (datasets_df["delay"] == delay) &        (datasets_df["region"] == region) &        (datasets_df["universe"] == universe) &        (datasets_df["alphaCount"] >= MIN_ALPHA_COUNT)    ].sort_values(by=['alphaCount', 'valueScore'], ascending=False)       # 进一步筛选可能包含EPS的数据集    eps_related_datasets = []    other_datasets = []       for idx, row in filtered_df.iterrows():        dataset_name = str(row.get('name', '')).lower()        dataset_id = row.get('id', '')               # 检查数据集名称是否包含EPS相关关键词        if any(keyword in dataset_name for keyword in EPS_RELATED_KEYWORDS):            eps_related_datasets.append((idx, row))        else:            other_datasets.append((idx, row))       # 合并列表，EPS相关的数据集排在前面    final_datasets = eps_related_datasets + other_datasets    final_df = pd.DataFrame([row for _, row in final_datasets])       print(f"筛选条件:")    print(f"  - delay == {delay}")    print(f"  - region == '{region}'")    print(f"  - universe == '{universe}'")    print(f"  - alphaCount >= {MIN_ALPHA_COUNT}")    print(f"符合条件的数据集数量: {len(final_df)}")    print(f"其中EPS相关数据集: {len(eps_related_datasets)}")       return final_dfdef get_eps_fields(s, dataset_id, region, universe, delay):    """获取包含EPS的字段"""    max_retries = MAX_RETRIES    retry_delay = RETRY_DELAY_INITIAL       for retry in range(max_retries):        try:            resp = s.search_fields_limited(region=region, delay=delay, universe=universe, dataset_id=dataset_id)            df = pd.DataFrame(resp.json()['results'])            break        except Exception as e:            error_msg = str(e).lower()            is_network_error = any(keyword in error_msg for keyword in [                'connection', 'timeout', 'reset', 'protocol', 'ssl', 'tls',                '远程主机', '连接', '超时', '重置'            ])                       if retry < max_retries - 1:                if "API rate limit exceeded" in str(e):                    print(f"获取字段时触发速率限制，等待 {retry_delay} 秒后重试...")                elif is_network_error:                    print(f"获取字段时网络连接错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")                    print(f"等待 {retry_delay} 秒后重试...")                else:                    print(f"获取字段时未知错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")                    print(f"等待 {retry_delay} 秒后重试...")                               time.sleep(retry_delay)                retry_delay = min(retry_delay * RETRY_DELAY_MULTIPLIER, RETRY_DELAY_MAX)                continue            else:                print(f"获取字段失败，已达到最大重试次数 ({max_retries})")                print(f"最后错误: {str(e)}")                raise e       print(f"数据集 {dataset_id} 总共有 {len(df)} 个字段")       # 筛选包含EPS的字段    eps_fields = []    for idx, row in df.iterrows():        field_id = row.get('id', '')        field_description = str(row.get('description', '')).lower()        field_type = row.get('type', '')               # 检查字段ID或描述是否包含"eps"        if 'eps' in field_id.lower() or 'eps' in field_description:            eps_fields.append({                'id': field_id,                'type': field_type,                'description': row.get('description', ''),                'dataset_id': dataset_id,                'region': region,                'universe': universe,                'delay': delay            })       print(f"找到 {len(eps_fields)} 个包含EPS的字段")    return eps_fieldsdef preprocess_vector_field(field_id):    """预处理VECTOR类型字段"""    return f'vec_avg({field_id})'def generate_eps_alpha_expressions(eps_fields):    """根据EPS字段生成Alpha表达式"""    alpha_expressions = []       for field_info in eps_fields:        field_id = field_info['id']        field_type = field_info['type']               # 如果是VECTOR类型，需要预处理        if field_type == 'VECTOR':            processed_field = preprocess_vector_field(field_id)        else:            processed_field = field_id               # 为每个模板生成表达式        for template in ALPHA_TEMPLATES:            expression = template.format(FIELD=processed_field)            alpha_expressions.append({                'expression': expression,                'field_id': field_id,                'field_type': field_type,                'processed_field': processed_field,                'template': template,                'dataset_id': field_info['dataset_id'],                'region': field_info['region'],                'universe': field_info['universe'],                'delay': field_info['delay'],                'description': field_info['description']            })       return alpha_expressionsdef batch_simulate_eps_expressions(alpha_expressions, region, universe, delay):    """批量回测EPS Alpha表达式"""    if not alpha_expressions:        print("没有Alpha表达式需要回测")        return       print(f"\n{'='*60}")    print(f"开始批量回测EPS Alpha表达式")    print(f"总表达式数量: {len(alpha_expressions)}")    print(f"区域: {region}, 宇宙: {universe}, 延迟: {delay}")    print(f"{'='*60}\n")       try:        # 为每个表达式分配decay值        alpha_list_with_decay = []        for expr_info in alpha_expressions:            # 根据字段类型和数据集分配不同的decay值            decay = DEFAULT_DECAY            if 'estimate' in expr_info['field_id'].lower():                decay = DECAY_ESTIMATE            elif 'actual' in expr_info['field_id'].lower():                decay = DECAY_ACTUAL                       alpha_list_with_decay.append((expr_info['expression'], decay))               # 创建任务池进行批量回测        print("正在创建回测任务池...")               # 根据区域设置不同的回测参数        if region == "GLB":            pools = load_task_pool(alpha_list_with_decay, BACKTEST_PARAMS_GLB[0], BACKTEST_PARAMS_GLB[1])            print(f"GLB区域使用回测参数: {BACKTEST_PARAMS_GLB[0]}, {BACKTEST_PARAMS_GLB[1]}")        else:            pools = load_task_pool(alpha_list_with_decay, BACKTEST_PARAMS_OTHER[0], BACKTEST_PARAMS_OTHER[1])            print(f"{region}区域使用回测参数: {BACKTEST_PARAMS_OTHER[0]}, {BACKTEST_PARAMS_OTHER[1]}")                   print(f"创建了 {len(pools)} 个回测任务组")               print("开始批量回测...")        # 添加重试机制处理网络连接问题        max_retries = BATCH_SIMULATE_MAX_RETRIES        retry_delay = BATCH_SIMULATE_RETRY_DELAY               for retry in range(max_retries):            try:                # 批量回测所有表达式                multi_simulate(pools, 'CROWDING', region, universe, delay)                print("批量回测完成")                break  # 成功则跳出重试循环            except Exception as e:                if "Connection" in str(e) or "ConnectionResetError" in str(e) or "ProtocolError" in str(e):                    if retry < max_retries - 1:                        print(f"网络连接错误，等待 {retry_delay} 秒后重试 ({retry + 1}/{max_retries})...")                        print(f"错误详情: {str(e)}")                        time.sleep(retry_delay)                        continue                    else:                        print(f"网络连接失败，已达到最大重试次数 ({max_retries})")                        raise e                else:                    # 非网络错误，直接抛出                    raise e               print(f"\n{'='*60}")        print(f"EPS Alpha表达式回测完成")        print(f"回测的表达式数量: {len(alpha_expressions)}")        print(f"{'='*60}\n")           except Exception as e:        print(f"批量回测过程中出现错误: {str(e)}")        print("错误详情:", e.__class__.__name__)        import traceback        print("错误堆栈:", traceback.format_exc())def collect_eps_fields_from_all_datasets(s, selected_datasets_df, region, universe, delay, start_index, progress):    """从所有数据集中收集EPS字段"""    all_eps_fields = []    processed_datasets = set()       total_datasets = len(selected_datasets_df)    print(f"\n{'='*60}")    print(f"开始收集EPS字段 - 区域: {region}, 宇宙: {universe}, 延迟: {delay}")    print(f"总共需要处理 {total_datasets} 个数据集")    print(f"{'='*60}\n")       for idx, dataset_id in enumerate(selected_datasets_df['id'], 1):        # 跳过起始位置之前的数据集        if idx < start_index:            print(f"跳过数据集 [{idx}/{total_datasets}]: {dataset_id} (在起始位置之前)")            continue                   print(f"\n处理数据集 [{idx}/{total_datasets}]: {dataset_id}")               # 检查是否已处理过        if is_processed(progress, region, universe, delay, dataset_id):            print(f"跳过已处理的数据集: {dataset_id}")            continue                   try:            print(f"正在搜索EPS字段...")            eps_fields = get_eps_fields(s, dataset_id, region, universe, delay)                       if eps_fields:                all_eps_fields.extend(eps_fields)                print(f"数据集 {dataset_id} 贡献了 {len(eps_fields)} 个EPS字段")                print(f"当前总EPS字段数量: {len(all_eps_fields)}")                               # 显示找到的EPS字段                for field in eps_fields:                    print(f"  - {field['id']} ({field['type']}): {field['description'][:100]}...")            else:                print(f"数据集 {dataset_id} 没有找到EPS字段")                       processed_datasets.add(dataset_id)            mark_as_processed(progress, region, universe, delay, dataset_id)                   except Exception as e:            print(f"处理数据集 {dataset_id} 时出错: {str(e)}")            continue       print(f"\n{'='*60}")    print(f"EPS字段收集完成")    print(f"成功处理数据集: {len(processed_datasets)}/{total_datasets}")    print(f"总EPS字段数量: {len(all_eps_fields)}")    print(f"{'='*60}\n")       return all_eps_fieldsdef process_region_universe_combination(region, universe, delay, start_index, enable_simulation=True):    """处理单个区域和参数组合"""    print(f"\n{'='*80}")    print(f"开始处理组合 - 区域: {region}, 范围: {universe}, 延迟: {delay}")    print(f"从第 {start_index} 个数据集开始处理")    print(f"回测模式: {'启用' if enable_simulation else '禁用'}")    print(f"{'='*80}\n")       # 加载进度    progress = load_progress()    eps_fields_data = load_eps_fields()    alpha_expressions_data = load_alpha_expressions()       try:        s, date_range = initialize_session(region, universe, delay)        print("正在获取数据集...")        datasets_df = get_datasets(s, region, delay, universe)        selected_datasets_df = filter_datasets_for_eps(datasets_df, region, universe, delay)               print(f"找到 {len(selected_datasets_df)} 个符合条件的数据集")               # 收集EPS字段        eps_fields = collect_eps_fields_from_all_datasets(            s, selected_datasets_df, region, universe, delay, start_index, progress        )               # 保存找到的EPS字段        key = f"{region}_{universe}_{delay}"        eps_fields_data[key] = eps_fields        save_eps_fields(eps_fields_data)               # 生成Alpha表达式        if eps_fields:            print(f"\n正在生成Alpha表达式...")            alpha_expressions = generate_eps_alpha_expressions(eps_fields)            print(f"生成了 {len(alpha_expressions)} 个Alpha表达式")                       # 保存生成的Alpha表达式            alpha_expressions_data[key] = alpha_expressions            save_alpha_expressions(alpha_expressions_data)                       # 显示生成的表达式示例            print(f"\n生成的Alpha表达式示例:")            for i, expr in enumerate(alpha_expressions[:5]):  # 显示前5个                print(f"  {i+1}. {expr['expression']}")                print(f"     字段: {expr['field_id']} ({expr['field_type']})")                print(f"     数据集: {expr['dataset_id']}")                print(f"     描述: {expr['description'][:100]}...")                print()                       # 根据参数决定是否进行回测            if enable_simulation:                print(f"\n开始回测生成的Alpha表达式...")                batch_simulate_eps_expressions(alpha_expressions, region, universe, delay)            else:                print(f"\n跳过回测阶段 (使用 --no-simulate 参数)")        else:            print("没有找到EPS字段，无法生成Alpha表达式")                   print(f"\n{'='*80}")        print(f"组合处理完成 - 区域: {region}, 范围: {universe}, 延迟: {delay}")        print(f"找到EPS字段: {len(eps_fields)}")        print(f"生成Alpha表达式: {len(alpha_expressions) if eps_fields else 0}")        print(f"{'='*80}\n")           except Exception as e:        print(f"处理组合 {region}_{universe}_{delay} 时发生严重错误: {str(e)}")        import traceback        print("错误堆栈:", traceback.format_exc())def main():    # 解析命令行参数    args = parse_args()    start_index = args.start    enable_simulation = not args.no_simulate       # 使用配置区域中的默认组合    region_universe_combinations = DEFAULT_REGION_UNIVERSE_COMBINATIONS       print(f"\n{'='*100}")    print(f"开始批量处理多个区域和参数组合 - EPS字段搜索")    print(f"总共需要处理 {len(region_universe_combinations)} 个组合")    print(f"从第 {start_index} 个数据集开始处理")    print(f"回测模式: {'启用' if enable_simulation else '禁用'}")    print(f"{'='*100}\n")       # 处理每个组合    for idx, (region, universe, delay) in enumerate(region_universe_combinations, 1):        print(f"\n{'='*100}")        print(f"处理组合 [{idx}/{len(region_universe_combinations)}]: {region} - {universe} - delay={delay}")        print(f"{'='*100}")               try:            process_region_universe_combination(                region, universe, delay, start_index, enable_simulation            )        except Exception as e:            print(f"处理组合 {region}_{universe}_{delay} 时发生错误: {str(e)}")            print("继续处理下一个组合...")            continue       print(f"\n{'='*100}")    print(f"所有组合处理完成！")    print(f"总共处理了 {len(region_universe_combinations)} 个组合")    print(f"EPS字段数据保存在: {EPS_FIELDS_FILE}")    print(f"Alpha表达式数据保存在: {EPS_ALPHA_EXPRESSIONS_FILE}")    print(f"{'='*100}")if __name__ == "__main__":    main()
```

---

## 讨论与评论 (4)

### 评论 #1 (作者: SM90987, 时间: 7个月前)

大佬，您好，我刚才简单测试了下代码，组合表达式公式都生成了，但是回测是报了loc key error错误，还在测试中

---

### 评论 #2 (作者: BW14163, 时间: 7个月前)

感谢大佬分享，很不错的帖子，读了关于模板的两个帖子，再看看这个代码帖子，感觉大佬的功底是非常不错的。搭配app，感觉非常好用！
关于这套代码的核心功能是：从平台中找关键字段,  生成 Alpha 表达式, 回测,保存结果, 全程无需人工干预。
代码中需要修改的部分是：
# 原
EPS_RELATED_KEYWORDS = ['eps']

# 新
RETURN_RELATED_KEYWORDS = ['任何需要的字段']

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
每当遇到一个RA时，不要忘了在ppac中捡垃圾的日子。
**********************************

---

### 评论 #3 (作者: RL65866, 时间: 7个月前)

这对后续的数据分析非常好用，点赞

---

### 评论 #4 (作者: SJ65808, 时间: 6个月前)

很不错的分享，模板可以进一步拓展为两个ts操作符之比

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

