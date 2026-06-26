# [SuperAlpha] 基于SuperAlpha数据分析师--Own极简回测次数源源不断三五(附代码)

- **链接**: [Commented] [SuperAlpha] 基于SuperAlpha数据分析师--Own极简回测次数源源不断三五附代码.md
- **作者**: JX79797
- **发布时间/热度**: 5个月前, 得票: 84

## 帖子正文

**前置条件，需要在某一个区域有一定数量的alpha，设置一个目标选择数量范围。**

如作者EUR初始130个alpha，目前170多个alpha， SA目标数量设置40-70，设置和combo一直运行同一种，目前交了30个三五还没有断，如果不好出了 可能会变更SA目标数量和设置及combo。

作者第一次执行200多个回测，50多个三五，去除自相关，最终提交12个， 当前每执行配置在回测50-70次，基本还可以产生2-3个三五

**核心功能概览**

1. Super Alpha配置的智能生成 (`gen_configs` 命令)

动态 Selection 表达式构建：不再依赖手动编写 `selection` 表达式，而是能根据您已有的“own”Alpha数据，动态地生成满足特定条件的 `selection` 表达式。

* 它会过滤掉与市场相关性（`prod_correlation`）不高的Alpha。

* 通过分析您的Alpha在不同数据类别 (datacategories)和 数值指标 (如 turnover, long_count, prod_correlation, operator_count)上的分布，构建出多样化的原子条件。

* 这些原子条件被巧妙地组合起来，形成复杂的 `selection` 表达式，例如 `(turnover > 0.2) && (in(datacategories, 'fundamental'))`。

* 数量与多样性控制：生成过程中，它会调用 `SuperAlphaSelectionAnalyzer` （ [https://support.worldquantbrain.com/hc/zh-cn/community/posts/37427255135127](/hc/zh-cn/community/posts/37427255135127)  帖子中详细介绍）来实时检查每个 `selection` 表达式所选取的Alpha数量（目标是 40-70 个），并确保新生成的表达式与已有的表达式在Alpha集合上具有足够的差异性（多样性）。

* 操作符限制与优化：它还会考虑BRAIN平台对 `selection` 表达式操作符数量的限制，并在生成过程中进行调整和优化，甚至会尝试排除表现不佳的Alpha来进一步精炼表达式。

* 多维度配置组合：除了智能生成的 `selection` 表达式，它还会根据您指定的区域 (Region)、Universe、中性化方法 (Neutralization) 和衰减周期 (Decay) 等参数，自动组合成完整的Super Alpha模拟配置。

* 持久化存储：所有生成的配置都会以结构化的JSON格式存储在 `records/ownsa_alpha.txt` 文件中，方便后续的模拟和追溯。

2. Super Alpha模拟的并发执行 (`run_sims` 命令)

* 任务读取与过滤：`run_sims` 命令会从 `ownsa_alpha.txt` 文件中读取指定日期的、尚未模拟（`up_date` 为空）的Super Alpha配置。

* 多线程并发：利用 `ThreadPoolExecutor`，`own_superalpha.py` 能够并发地向BRAIN平台提交多个Super Alpha模拟任务，大大缩短了等待时间。

*局部与全局失败计数：针对单个Alpha的模拟失败和全局的模拟失败，分别设置了重试次数限制和重新登录策略，提高了程序的鲁棒性。

*结果自动更新：一旦模拟完成并成功获取到 `alpha_id`，程序会自动将 `alpha_id` 和 `up_date`（更新日期）写回 `ownsa_alpha.txt` 文件，标记该记录已处理。同时，它还会自动为新生成的Alpha添加标签 (`alpha_tag`)，便于管理和筛选。

**如何使用？**

`own_superalpha.py` 通过命令行参数进行操作：

**生成配置：**

```bash

python own_superalpha.py gen_configs --region EUR

```

这将在 `records/ownsa_alpha.txt` 中生成针对 EUR 区域的 Super Alpha 配置。

**运行模拟：**

```bash

python own_superalpha.py run_sims --date 2026-01-04 --workers 3

```

这将并发启动 3 个线程，处理 `add_date` 为 `2026-01-04` 的配置，并提交模拟。

**在这里更改配置**

**![图片](images/img_7d8e9967f2.png)**

**代码分享**

```
import argparseimport osimport randomimport jsonimport concurrent.futuresfrom concurrent.futures import ThreadPoolExecutorfrom datetime import datetime, dateimport timeimport threadingimport pandas as pdfrom machine_lib import * from sa_selection_analyzer import SuperAlphaSelectionAnalyzer# 全局变量或常量FILE_WRITE_LOCK = threading.Lock()# sess = login() # 初始化会话，将在不同的函数中被使用 (将不再作为全局变量，而是在需要时创建)# --- Runlist.py 的功能 ---alpha_fail_attempt_tolerance = 5  # 每个 alpha 允许的最大失败尝试次数failure_count = 0  # simulate_alphas 中用到的全局变量def wait_get(url: str, session, max_retries: int = 10) -> "MockSession":  # type: ignore    """    发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。    此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。    """    retries = 0    while retries < max_retries:        while True:            try:                simulation_progress = session.get(url)                if simulation_progress.headers.get("Retry-After", "0") == "0":                    break                time.sleep(float(simulation_progress.headers["Retry-After"]))            except Exception as e:                print(f"请求 {url} 时发生网络错误: {e}, 等待后重试...")                time.sleep(5)                continue            except Exception as e:                print(f"wait_get 内部发生未知错误: {e}, url: {url}")                time.sleep(5)                continue        if simulation_progress.status_code < 400:            try:                content_type = simulation_progress.headers.get('Content-Type', '')                if 'application/json' in content_type:                    sim_data = simulation_progress.json()                    if isinstance(sim_data, dict) and "message" in sim_data and "ERROR" in simulation_progress.text:                        print(f"回测API返回错误信息 {url}：{sim_data.get('message')}")                elif "ERROR" in simulation_progress.text:                    print(f"回测API返回非JSON错误文本 {url}：{simulation_progress.text[:200]}")            except json.JSONDecodeError:                if "ERROR" in simulation_progress.text:                    print(f"回测API返回错误文本 (JSON解析失败) {url}：{simulation_progress.text[:200]}")            break        elif simulation_progress.status_code == 401:            print(f"请求 {url} 遇到401未授权错误，尝试重新登录...")            session = login()        else:            print(f"请求 {url} 失败，状态码: {simulation_progress.status_code}, 内容: {simulation_progress.text[:200]}")            time.sleep(2 ** retries)            retries += 1    if retries >= max_retries:        print(f"达到最大重试次数 {max_retries} 仍然失败: {url}")    return simulation_progressdef simulate_alphas(db_id, data_for_simulation, thread_session):    """    data_for_simulation: simulation data dictionary    return alpha list or False on critical failure    """    print(f"线程 {threading.get_ident()} 开始处理任务: ",db_id)    keep_trying = True    global failure_count    current_session = thread_session    local_failure_count = 0    while keep_trying:        try:            simulation_response = current_session.post('https://api.worldquantbrain.com/simulations', json=data_for_simulation)            simulation_response.raise_for_status()            simulation_progress_url = simulation_response.headers['Location']            children_ids_str = simulation_progress_url.split('/')[-1]            children_ids = [children_ids_str]            alphas_results = []            for child_id in children_ids:                child_url = f'https://api.worldquantbrain.com/simulations/{child_id}'                child_progress_response = wait_get(child_url, current_session)                if child_progress_response.status_code >= 400:                    print(f"获取子任务 {child_id} 进度失败。状态码: {child_progress_response.status_code}")                    alphas_results.append(None)                    continue                try:                    child_progress = child_progress_response.json()                except json.JSONDecodeError:                    print(f"解析子任务 {child_id} 响应失败。响应文本: {child_progress_response.text[:200]}")                    alphas_results.append(None)                    continue                print(f"子任务 {child_id} 状态: {child_progress.get('status')}")                if child_progress.get('status') in ['CANCELLED', 'ERROR']:                    print(                        f"错误：模拟任务 {db_id} 的子任务 {child_id} 状态为 {child_progress.get('status')}, 详情: {child_progress}")                    alphas_results.append(None)                elif child_progress.get('status') in ['COMPLETE', 'WARNING']:                    alphas_results.append(child_progress.get('alpha'))                else:                    print(f"子任务 {child_id} 状态未完成或未知: {child_progress.get('status')}")                    alphas_results.append(None)            print(f"线程 {threading.get_ident()} 模拟结果: {alphas_results}")            return alphas_results        except Exception as http_err:            print(f"HTTP错误发生在 simulate_alphas (POST): {http_err}, data: {str(data_for_simulation)}")            local_failure_count += 1        except KeyError as ke:            print(f"关键信息缺失 (KeyError: {ke})，可能POST请求未成功。data: {str(data_for_simulation)[:100]}")            local_failure_count += 1        except Exception as e:            print(f"simulate_alphas中发生未知异常: {e}, data: {str(data_for_simulation)[:100]}")            local_failure_count += 1        if local_failure_count > 0:            print(f"尝试次数 {local_failure_count}/{alpha_fail_attempt_tolerance}。等待15秒后重试...")            time.sleep(15)            failure_count += 1            if failure_count >= alpha_fail_attempt_tolerance:                print("全局失败次数达到阈值，尝试重新登录...")                session = login()                failure_count = 0            if local_failure_count >= alpha_fail_attempt_tolerance:                print(f"此任务失败次数已达上限 {alpha_fail_attempt_tolerance}，放弃处理。")                return False        else:            keep_trying = False    return Falsedef fetch_sim_configs_from_db(target_add_date_str: str):    """从 records/ownsa_alpha.txt 获取待处理的模拟配置（兼容原函数名）。"""    records_dir = 'records'    file_path = os.path.join(records_dir, 'ownsa_alpha.txt')    sim_configs = []    if not os.path.exists(file_path):        print(f"记录文件不存在: {file_path}")        return sim_configs    count_total = 0    with open(file_path, 'r', encoding='utf-8') as f:        for line in f:            line = line.strip()            if not line:                continue            try:                obj = json.loads(line)                count_total += 1            except Exception:                continue            up_date_val = obj.get('up_date', None)            add_date_val = obj.get('add_date', None)            if (up_date_val is None or up_date_val == '') and add_date_val == target_add_date_str:                alpha_json_obj = obj.get('alpha_json')                try:                    alpha_json_str = json.dumps(alpha_json_obj)                except Exception:                    alpha_json_str = ''                sim_configs.append({                    'id': obj.get('id'),                    'alpha_json': alpha_json_str,                })    print(f"为日期 {target_add_date_str} 从文件获取到 {len(sim_configs)} 条待处理记录（共 {count_total} 行）。")    return sim_configsdef update_alpha_in_db(db_id: int, new_alpha_id: str = None):    """更新 records/ownsa_alpha.txt 中的 alpha_id 和 up_date（兼容原函数名）。"""    records_dir = 'records'    file_path = os.path.join(records_dir, 'ownsa_alpha.txt')    tmp_path = os.path.join(records_dir, 'ownsa_alpha.tmp')    if not os.path.exists(file_path):        print(f"记录文件不存在: {file_path}")        return False    current_date_str = date.today().isoformat()    updated = False    with FILE_WRITE_LOCK:        try:            with open(file_path, 'r', encoding='utf-8') as src, open(tmp_path, 'w', encoding='utf-8') as dst:                for line in src:                    line_stripped = line.strip()                    if not line_stripped:                        dst.write(line)                        continue                    try:                        obj = json.loads(line_stripped)                    except Exception:                        dst.write(line)                        continue                    if obj.get('id') == db_id:                        if new_alpha_id:                            obj['alpha_id'] = new_alpha_id                        obj['up_date'] = current_date_str                        updated = True                        dst.write(json.dumps(obj, ensure_ascii=False) + "\n")                    else:                        dst.write(line)            os.replace(tmp_path, file_path)        except Exception as e:            print(f"更新记录 ID {db_id} 时写入失败: {e}")            try:                if os.path.exists(tmp_path):                    os.remove(tmp_path)            except Exception:                pass            return False    if updated:        action = f"已更新 alpha_id 为 {new_alpha_id}" if new_alpha_id else "仅更新 up_date"        print(f"文件记录 ID {db_id}: {action}。")    else:        print(f"未在文件中找到 ID 为 {db_id} 的记录。")    return updateddef process_simulation_task(db_record, thread_session):    """    处理单个数据库记录：解析json，调用API，更新数据库    db_record: {'id': int, 'alpha_json': str}    """    db_id = db_record['id']    alpha_json_str = db_record['alpha_json']    if not alpha_json_str:        print(f"记录 ID {db_id}: alpha_json 为空，跳过处理并更新up_date。")        update_alpha_in_db(db_id, None)        return    try:        simulation_params = json.loads(alpha_json_str)    except json.JSONDecodeError as e:        print(f"记录 ID {db_id}: JSON解析失败 - {e}。alpha_json: {alpha_json_str[:100]}... 跳过处理并更新up_date。")        update_alpha_in_db(db_id, None)        return    api_results = simulate_alphas(db_id, simulation_params, thread_session)    returned_alpha_id = None    if isinstance(api_results, list) and len(api_results) > 0:        if api_results[0] and isinstance(api_results[0], str) and api_results[0].strip():            returned_alpha_id = api_results[0].strip()            print(f"记录 ID {db_id}: alpha_id: {returned_alpha_id} API原始json: - {alpha_json_str}")            print("set_alpha_properties alpha_id: %s"%returned_alpha_id)            alpha_tag = "ownsa_"+simulation_params["settings"]["region"]+"_"+str(simulation_params["settings"]["delay"])            set_alpha_properties(thread_session,                                returned_alpha_id,                                tags=[alpha_tag])    update_alpha_in_db(db_id, returned_alpha_id)import functoolsdef worker_initializer():    """Initializes a new session for each worker thread."""    threading.current_thread().session = login()def process_simulation_task_with_session(db_record):    """Wrapper to pass the thread-local session to process_simulation_task."""    worker_session = threading.current_thread().session    process_simulation_task(db_record, worker_session)def run_simulations(args):    """    运行 Alpha 模拟。    """    # 用户指定要处理的 add_date    target_add_date_input = args.date    try:        datetime.strptime(target_add_date_input, '%Y-%m-%d')    except ValueError:        print("日期格式无效，请输入 YYYY-MM-DD 格式的日期。")        exit()    # 1. 从数据库获取待处理的配置    tasks_to_process = fetch_sim_configs_from_db(target_add_date_input)    if not tasks_to_process:        print(f"日期 {target_add_date_input} 没有需要处理的记录，或数据文件连接失败。")    else:        print(f"准备使用 {args.workers} 个线程处理 {len(tasks_to_process)} 个任务...")        with ThreadPoolExecutor(max_workers=args.workers, initializer=worker_initializer) as executor:            future_to_task = {executor.submit(process_simulation_task_with_session, task): task for task in tasks_to_process}            for future in concurrent.futures.as_completed(future_to_task):                task_info = future_to_task[future]                try:                    future.result()                except Exception as exc:                    print(f"任务 (DB ID: {task_info['id']}) 执行时产生异常: {exc}")        print("所有任务处理完毕。")# --- Genlist.py 的功能 ---def estimate_operator_count(expression: str) -> int:    """    Estimates the number of operators in a selection expression string.    This is a rough estimation and may not be perfectly accurate.    """    operators = [        # Multi-character operators first (longer operators before shorter ones)        '&&', '||', '==', '!=', '>=', '<=',        'if_else', 'ts_rank', 'ts_corr', 'ts_delta',        # Single-character operators and 'in', 'abs'        '!', '>', '<', 'in', 'abs'    ]        count = 0    temp_expression = expression        # Sort operators by length in descending order to prevent partial matches    operators.sort(key=len, reverse=True)    for op in operators:        while op in temp_expression:            count += 1            # Replace the found operator with a placeholder of the same length            # This prevents re-counting substrings (e.g., '>' in '>=')            temp_expression = temp_expression.replace(op, 'X' * len(op), 1)                 return countdef generate_and_refine_selection_expression_own(    own_alphas_df: pd.DataFrame,    region: str,    delay: int,    session,    generated_alpha_id_sets: list[set]) -> list[str]:    """    Generates a list of refined selection expressions for 'own' Super Alphas,    ensuring each expression selects between 40-70 alphas and maintains diversity.    This version is inspired by notownsa_superalpha.py for more complex and effective generation.    Args:        own_alphas_df (pd.DataFrame): DataFrame containing all 'own' alphas for the given region/delay.        region (str): The region for the Super Alpha.        delay (int): The delay for the Super Alpha.        session: The requests session object for API calls.        generated_alpha_id_sets (list[set]): A list to store sets of alpha IDs for generated expressions,                                              used to ensure diversity.    Returns:        list[str]: A list of refined selection expressions.    """    refined_expressions = []        if own_alphas_df.empty:        print("Warning: own_alphas_df is empty. Cannot generate expressions.")        return []        # 1. Initial Filtering: Filter own_alphas_df for prod_correlation > 0    if 'is.prodCorrelation' not in own_alphas_df.columns:        print("Warning: 'is.prodCorrelation' column not found in own_alphas_df. Cannot apply initial filter.")        return []        filtered_own_alphas_df = own_alphas_df[pd.to_numeric(own_alphas_df['is.prodCorrelation'], errors='coerce') > 0].copy()    if filtered_own_alphas_df.empty:        print("Warning: No alphas with positive prod_correlation. Cannot generate expressions.")        return []    # --- Dynamic Extraction of Datacategories and Datasets ---    unique_datacategories_from_df = []    if 'pyramidThemes.pyramids' in filtered_own_alphas_df.columns:        for pyramid_list in filtered_own_alphas_df['pyramidThemes.pyramids'].dropna():            if isinstance(pyramid_list, list):                for pyramid in pyramid_list:                    if isinstance(pyramid, dict) and 'name' in pyramid:                        parts = pyramid['name'].split('/')                        if len(parts) == 3:                            unique_datacategories_from_df.append(parts[2])            elif isinstance(pyramid_list, str): # Handle cases where it might be a JSON string of a list                try:                    loaded_pyramids = json.loads(pyramid_list)                    if isinstance(loaded_pyramids, list):                        for pyramid in loaded_pyramids:                            if isinstance(pyramid, dict) and 'name' in pyramid:                                parts = pyramid['name'].split('/')                                if len(parts) == 3:                                    unique_datacategories_from_df.append(parts[2])                except json.JSONDecodeError:                    parts = pyramid_list.split('/')                    if len(parts) == 3:                        unique_datacategories_from_df.append(parts[2])    unique_datacategories_from_df = list(set(unique_datacategories_from_df))    print(f"Dynamically extracted datacategories: {unique_datacategories_from_df}")    # Common dataset IDs for EUR region (hardcoded for now, can be made dynamic)    # These are examples, actual IDs might need to be fetched from BRAIN API    common_eur_datasets = [        "pv1", "pv2", "fundamental6", "earnings", "news18",         "socialmedia15", "model", "analyst", "shortinterest3",         "institutions6", "other", "sentiment", "insiders", "risk", "imbalance"    ]    # Filter common_eur_datasets to only include those that are also present in the filtered_own_alphas_df's universe    # This requires a mapping or direct check, for simplicity we'll just use the common ones for now.    # The 'settings.universe' column can be a proxy for available datasets.    unique_universes_from_df = []    if 'settings.universe' in filtered_own_alphas_df.columns:        unique_universes_from_df.extend(filtered_own_alphas_df['settings.universe'].dropna().unique().tolist())        # For generating dataset conditions, we might use a combination of unique_universes_from_df and specific common_eur_datasets    # For now, let's prioritize generating conditions based on datacategories and metrics.    # We will generate `in(datasets, '...')` conditions later based on a more robust set of actual dataset IDs.        # --- Generate Atomic Conditions ---    atomic_conditions_pool = []    # Numerical Metrics: turnover, long_count, short_count, operator_count, prod_correlation, self_correlation    metrics_to_analyze = {        'turnover': 'is.turnover',        'long_count': 'is.longCount',        'short_count': 'is.shortCount',        'operator_count': 'regular.operatorCount',        'prod_correlation': 'is.prodCorrelation',        'self_correlation': 'is.selfCorrelation'    }    # Generate metric-based conditions    for metric_name, df_col_name in metrics_to_analyze.items():        if df_col_name in filtered_own_alphas_df.columns and not filtered_own_alphas_df[df_col_name].empty:            metric_series = pd.to_numeric(filtered_own_alphas_df[df_col_name], errors='coerce').dropna()            if metric_series.empty or len(metric_series.unique()) < 2:                continue            lower_metric_name = metric_name.lower()                        # Top N conditions            random_high_percentile = random.uniform(0.6, 0.95)            atomic_conditions_pool.append(f"{lower_metric_name} > {round(metric_series.quantile(random_high_percentile), 2)}")                        # Bottom N conditions            random_low_percentile = random.uniform(0.05, 0.4)            atomic_conditions_pool.append(f"{lower_metric_name} < {round(metric_series.quantile(random_low_percentile), 2)}")                        # Middle N conditions            mid_low_p = random.uniform(0.2, 0.4)            mid_high_p = random.uniform(0.6, 0.8)            atomic_conditions_pool.append(f"{lower_metric_name} >= {round(metric_series.quantile(mid_low_p), 2)} && {lower_metric_name} <= {round(metric_series.quantile(mid_high_p), 2)}")                        # Random N (specific value) conditions            if len(metric_series) > 0:                random_value = round(random.choice(metric_series.tolist()), 2)                atomic_conditions_pool.append(f"{lower_metric_name} == {random_value}")                atomic_conditions_pool.append(f"{lower_metric_name} > {random_value}")                atomic_conditions_pool.append(f"{lower_metric_name} < {random_value}")    # Generate datacategory-based conditions    for dc_name in unique_datacategories_from_df:        atomic_conditions_pool.append(f"in(datacategories, '{dc_name.lower()}')")        # Optionally add 'not in' conditions        # atomic_conditions_pool.append(f"not(in(datacategories, '{dc_name.lower()}'))")    # Generate dataset-based conditions (using common_eur_datasets for now)    if common_eur_datasets:        for ds_name in random.sample(common_eur_datasets, min(5, len(common_eur_datasets))): # Sample a few            atomic_conditions_pool.append(f"in(datasets, '{ds_name}')")            # atomic_conditions_pool.append(f"not(in(datasets, '{ds_name}'))") # Avoid contradictory 'not in' for now    if not atomic_conditions_pool:        print("Warning: No atomic conditions could be generated. Cannot generate expressions.")        return []    # --- Global Constraints Pool (similar to notownsa_superalpha.py) ---    operator_count_conditions = ["operator_count < 8", "operator_count >= 5 && operator_count < 10", "operator_count >= 10"]    prod_correlation_conditions = ["prod_correlation < 0.7", "prod_correlation >= 0.3 && prod_correlation < 0.7", "prod_correlation >= 0.7"]    self_correlation_conditions = ["self_correlation < 0.4", "self_correlation >= 0.3 && self_correlation < 0.6"]    global_turnover_conditions = ["turnover < 0.2", "turnover >= 0.15 && turnover < 0.30", "turnover >= 0.30"]    # datacategory_count_conditions = ["datacategory_count == 1", "datacategory_count == 2"] # This is not a direct filterable field in selection expressions    global_constraints_pool = operator_count_conditions + prod_correlation_conditions + self_correlation_conditions + global_turnover_conditions    # --- Main Expression Generation Loop ---    MAX_EXPRESSION_ATTEMPTS = 500    TARGET_EXPRESSIONS_COUNT = 50    MINIMUM_ALPHA_COUNT = 40 # Target minimum alphas for a valid expression    MAXIMUM_ALPHA_COUNT = 70 # Target maximum alphas for a valid expression    OPERATOR_LIMIT = 64 # Total operator limit for the final expression    for _ in range(MAX_EXPRESSION_ATTEMPTS):        if len(refined_expressions) >= TARGET_EXPRESSIONS_COUNT:            break        # Generate an initial complex expression using OR combinations of atomic conditions        num_components = random.randint(3, min(len(atomic_conditions_pool), 6))        selected_atomic_conditions = random.sample(atomic_conditions_pool, num_components)        complex_layered_expression = " || ".join([f"({c})" for c in selected_atomic_conditions])        intermediate_op_count = estimate_operator_count(complex_layered_expression)        INTERMEDIATE_OPERATOR_LIMIT = 50 # Limit for the OR-combined part        if intermediate_op_count > INTERMEDIATE_OPERATOR_LIMIT:            # print(f"Warning: Intermediate layered expression complexity ({intermediate_op_count} operators) exceeds the limit of {INTERMEDIATE_OPERATOR_LIMIT}. Discarding.")            continue # Discard and try again        # Start with a random subset of global constraints and relax if necessary        num_global_conditions_to_add = random.randint(1, min(3, len(global_constraints_pool)))        selected_global_constraints = random.sample(global_constraints_pool, num_global_conditions_to_add)                current_global_constraints = list(selected_global_constraints) # Make a mutable copy        initial_selection_expr = ""        temp_analyzer = SuperAlphaSelectionAnalyzer(session)        # Relaxation loop for global constraints        while True:            global_constraints_str = ""            if current_global_constraints:                global_constraints_str = " && ".join([f"({cond})" for cond in current_global_constraints])                        if global_constraints_str:                initial_selection_expr = f"own && prod_correlation > 0 && ({complex_layered_expression}) && {global_constraints_str}"            else:                initial_selection_expr = f"own && prod_correlation > 0 && ({complex_layered_expression})"            current_op_count = estimate_operator_count(initial_selection_expr)            if current_op_count > OPERATOR_LIMIT:                # If even with relaxed constraints, it exceeds the limit, try removing more                if current_global_constraints:                    current_global_constraints.pop(random.randrange(len(current_global_constraints)))                    continue # Try again with fewer global constraints                else:                    break # Cannot reduce further, break out            temp_analyzer.fetch_alphas(initial_selection_expr, region=region, delay=delay, selection_limit=1000)                        current_selection_df = temp_analyzer.get_dataframe()            num_selected_alphas = len(current_selection_df) if current_selection_df is not None else 0            if MINIMUM_ALPHA_COUNT <= num_selected_alphas <= MAXIMUM_ALPHA_COUNT:                # Found a good expression, proceed to refinement (worst performers)                break            elif num_selected_alphas < MINIMUM_ALPHA_COUNT and current_global_constraints:                # Too few alphas, relax one random global constraint                current_global_constraints.pop(random.randrange(len(current_global_constraints)))            elif num_selected_alphas > MAXIMUM_ALPHA_COUNT:                # Too many alphas, try to add more random global constraints if available                remaining_global_constraints = [c for c in global_constraints_pool if c not in current_global_constraints]                if remaining_global_constraints:                    current_global_constraints.append(random.choice(remaining_global_constraints))                else:                    # No more constraints to add, break and try to refine with worst performers                    break            else: # num_selected_alphas is 0 or no more constraints to relax/add                break                # If no suitable initial expression was found after relaxation, continue to next attempt        if not (MINIMUM_ALPHA_COUNT <= num_selected_alphas <= MAXIMUM_ALPHA_COUNT):            continue        # --- Refinement: Exclude Worst Performers (Sharpe and Turnover) ---        # Calculate current operator count and remaining budget        current_op_count = estimate_operator_count(initial_selection_expr)        remaining_budget = OPERATOR_LIMIT - current_op_count                # Each Sharpe/Turnover exclusion takes ~2 operators (turnover != X)        n_worst_performers_to_exclude = int(remaining_budget / 2) # Budget for exclusions                final_refined_expr = initial_selection_expr # Start with the best found expression        if n_worst_performers_to_exclude > 0:            worst_alphas_df = temp_analyzer.get_worst_performers_report(sort_by_column='os.sharpe_unified', n=n_worst_performers_to_exclude)                        if worst_alphas_df is not None and not worst_alphas_df.empty and 'is.turnover' in worst_alphas_df.columns:                unique_turnovers = set(worst_alphas_df['is.turnover'].dropna())                                if unique_turnovers:                    exclusion_constraints = [f"turnover != {t}" for t in unique_turnovers]                    exclusion_str = " && ".join(exclusion_constraints)                                        temp_final_expr = f"{initial_selection_expr} && ({exclusion_str})"                                        # Check operator limit for the final expression                    if estimate_operator_count(temp_final_expr) <= OPERATOR_LIMIT:                        final_refined_expr = temp_final_expr                    else:                        print(f"Warning: Refined expression with exclusions exceeds operator limit. Using non-excluded expression.")            else:                print("No worst performers found, or 'is.turnover' column missing for refinement.")        else:            print(f"No operator budget left for adding worst Sharpe performers exclusions. Remaining budget: {remaining_budget}")        # Final check of the refined expression        temp_analyzer.fetch_alphas(final_refined_expr, region=region, delay=delay, selection_limit=1000)        current_selection_df = temp_analyzer.get_dataframe()        num_selected_alphas = len(current_selection_df) if current_selection_df is not None else 0        if not (MINIMUM_ALPHA_COUNT <= num_selected_alphas <= MAXIMUM_ALPHA_COUNT):            # print(f"Warning: Final refined expression resulted in {num_selected_alphas} alphas, outside target range. Discarding.")            continue # Discard if final refinement breaks the alpha count        current_alpha_ids = set(current_selection_df['id'].tolist())        # Check diversity constraint (at least 10 different alphas)        is_diverse_enough = True        for existing_id_set in generated_alpha_id_sets:            common_alphas = len(current_alpha_ids.intersection(existing_id_set))            min_len = min(len(current_alpha_ids), len(existing_id_set))            if min_len == 0:                overlap_percentage = 0.0            else:                overlap_percentage = common_alphas / min_len                        if overlap_percentage > 0.8 or (min_len - common_alphas) < 10:                is_diverse_enough = False                break                if is_diverse_enough:            refined_expressions.append(final_refined_expr)            generated_alpha_id_sets.append(current_alpha_ids)            print(f"Generated a valid expression: {final_refined_expr} with {num_selected_alphas} alphas.")            print(f"Total refined expressions: {len(refined_expressions)}")    return refined_expressionsdef generate_configs(args):    """    生成 Alpha 模拟配置。    """    run_region = args.region    delay = 1 # 固定 delay 为 1    local_session = login() # 为生成配置创建一个新的 session    # 1. 使用 SuperAlphaSelectionAnalyzer 获取所有 "own" alpha 的 DataFrame    print(f"开始获取区域 '{run_region}' (Delay: {delay}) 的所有 'own' alpha 数据...")    analyzer = SuperAlphaSelectionAnalyzer(local_session)    analyzer.fetch_alphas("own && prod_correlation > 0", region=run_region, delay=delay, selection_limit=1000)    own_alphas_df = analyzer.get_dataframe()    if own_alphas_df.empty:        print(f"未能在区域 {run_region} 获取到任何 'own' alpha。请检查登录状态或区域设置。")        return    print(f"成功获取 {len(own_alphas_df)} 个 'own' alpha。")    # The datacategories and layering_datasets are now dynamically determined inside generate_and_refine_selection_expression_own    # So, these are no longer needed here as parameters for that function call.    # Define neutralizations (still needed for overall config)    NEUTS = {    'USA': ['STATISTICAL','SLOW_AND_FAST'],    'GLB': ['STATISTICAL','SLOW_AND_FAST'],    'EUR': ['STATISTICAL','SLOW_AND_FAST'],    'ASI': ['STATISTICAL','SLOW_AND_FAST'],    'CHN': ['STATISTICAL','SLOW_AND_FAST'],    'KOR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'TWN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'HKG': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'JPN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'AMR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'COUNTRY'],    'IND': ['SLOW_AND_FAST']    }       neutralizations = NEUTS.get(run_region.upper(), ['NONE'])        combo = [        "combo_a(alpha)"    ]    REGIONS = {        "USA": ["TOP3000", ],        "GLB": ["TOP3000", "MINVOL1M"],        "EUR": ["TOP2500"],        "ASI": ["MINVOL1M", "ILLIQUID_MINVOL1M"],        "CHN": ["TOP2000U"],        "AMR": ["TOP600"],        "IND": ["TOP500"]    }    if run_region not in REGIONS:        print(f"错误: 不支持的区域 '{run_region}'。支持的区域有: {list(REGIONS.keys())}")        return    region_to_process = REGIONS[run_region]    sim_config_list = []    if run_region in ["AMR"]:        isMax = 'ON'    else:        isMax = 'OFF'    # 用于存储已生成的 selection 表达式和其对应的 alpha ID 集合，以便进行多样性检查    generated_alpha_id_sets = []        # --------------------------------------------------------------------------------    # New selection expression generation logic    # --------------------------------------------------------------------------------    selectionLimit = 1000 # 固定 selectionLimit    selectionHandling = "POSITIVE" # 假设为POSITIVE，如果需要，可以扩展    # Call the refined generate_and_refine_selection_expression_own    refined_selection_expressions = generate_and_refine_selection_expression_own(        own_alphas_df, run_region, delay, local_session,        generated_alpha_id_sets    )        if not refined_selection_expressions:        print("未能生成任何满足条件的 selection 表达式，程序结束。")        return    for universe in region_to_process:        for neutralization_item in neutralizations:            for item_selection_str in refined_selection_expressions: # 迭代精炼后的 selection 表达式                for item_combo_str in combo:                    for decay in [6]: # 根据需要调整 decay 范围                        full_item_data_dict = {                            "type": "SUPER",                            "settings": {                                "nanHandling": "OFF", "instrumentType": "EQUITY", "delay": delay,                                "universe": universe, "truncation": 0.08, "unitHandling": "VERIFY",                                "selectionLimit": selectionLimit, # 固定为 1000                                "selectionHandling": selectionHandling,                                "pasteurization": "ON", "region": run_region, "language": "FASTEXPR",                                "decay": decay, "neutralization": neutralization_item,                                "visualization": False, "testPeriod": "P0Y", "maxTrade": isMax                            },                            "combo": item_combo_str, "selection": item_selection_str                        }                        config_entry = {                            "full_item_data_dict": full_item_data_dict,                            "item_selection_str": item_selection_str,                            "item_combo_str": item_combo_str                        }                        sim_config_list.append(config_entry)    random.shuffle(sim_config_list)    print("sim_config_list length:", len(sim_config_list))    records_dir = os.path.join('records')    os.makedirs(records_dir, exist_ok=True)    file_path = os.path.join(records_dir, 'ownsa_alpha.txt')    next_id = 1    if os.path.exists(file_path):        try:            with open(file_path, 'r', encoding='utf-8') as f:                last_id = 0                for line in f:                    line = line.strip()                    if not line:                        continue                    try:                        obj = json.loads(line)                        if isinstance(obj, dict):                            curr_id = int(obj.get('id', 0))                            if curr_id > last_id:                                last_id = curr_id                    except Exception:                        continue                next_id = last_id + 1        except Exception as e:            print(f"读取现有记录文件失败，将从 1 开始编号: {e}")    inserted_count = 0    today_str = date.today().isoformat()    try:        with open(file_path, 'a', encoding='utf-8') as f:            for config_entry in sim_config_list:                selection_for_column = config_entry["item_selection_str"]                combo_for_column = config_entry["item_combo_str"]                dict_for_json_column = config_entry["full_item_data_dict"]                record = {                    "id": next_id,                    "Selection": selection_for_column,                    "Combo": combo_for_column,                    "alpha_id": None,                    "alpha_json": dict_for_json_column,                    "add_date": today_str,                    "up_date": None                }                f.write(json.dumps(record, ensure_ascii=False) + "\n")                next_id += 1                inserted_count += 1        print(f"Successfully wrote {inserted_count} records into {file_path}.")    except Exception as e:        print(f"写入记录文件失败: {e}")def main():    parser = argparse.ArgumentParser(description="WorldQuant BRAIN Alpha 管理工具")    subparsers = parser.add_subparsers(dest="command", help="可用的命令")    # Runlist 子命令    run_sim_parser = subparsers.add_parser("run_sims", help="运行 Alpha 模拟")    run_sim_parser.add_argument("--date", type=str, required=True, help="要处理的添加日期 (YYYY-MM-DD)")    run_sim_parser.add_argument("--workers", type=int, default=3, help="并发运行模拟的线程数")    run_sim_parser.set_defaults(func=run_simulations)    # Genlist 子命令    gen_config_parser = subparsers.add_parser("gen_configs", help="生成 Alpha 模拟配置")    gen_config_parser.add_argument("--region", type=str, default="EUR", help="生成配置的目标区域 (例如: EUR)")    gen_config_parser.set_defaults(func=generate_configs)    args = parser.parse_args()    if args.command:        args.func(args)    else:        parser.print_help()if __name__ == "__main__":    main()
```

---

## 讨论与评论 (18)

### 评论 #1 (作者: XG41865, 时间: 5个月前)

这里贴的代码是 robust_sharpe_optimizer.py ，不是 own_superalpha.py

---

### 评论 #2 (作者: RM49262, 时间: 5个月前)

=====================================评论区========================================

感谢大佬分享，又可以愉快的组35SA了

这就搞起来！

===================================================================================

---

### 评论 #3 (作者: XB37939, 时间: 5个月前)

大佬 代码拿下来用不了，提示缺

from sa_selection_analyzer import SuperAlphaSelectionAnalyzer

大佬看看能不能把完整可运行的代码流程整理下 多谢

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #4 (作者: FF65210, 时间: 5个月前)

大佬你好，问下这里的代码是全的吗，我跑的时候怎么报错了

---

### 评论 #5 (作者: XW23690, 时间: 5个月前)

感谢大佬分享，程序还剔除重复性高的表达式，极大缩小回测数量。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #6 (作者: PZ56655, 时间: 4个月前)

大佬，能不能再分享一下own_superalpha.py这个代码

---

### 评论 #7 (作者: WX31897, 时间: 4个月前)

ModuleNotFoundError: No module named 'sa_selection_analyzer'  ,没有这个模块，大佬能给一下吗

---

### 评论 #8 (作者: JX79797, 时间: 4个月前)

[WX31897](/hc/en-us/profiles/32196523937175-WX31897)   [PZ56655](/hc/en-us/profiles/35265056429079-PZ56655)   [FF65210](/hc/en-us/profiles/34449770999063-FF65210)  @ [XB37939](/hc/en-us/profiles/34750959351703-XB37939)

帖子开头有哪个代码链接的

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #9 (作者: HY20507, 时间: 4个月前)

### `sa_selection_analyzer.py在大佬的另一篇帖子`

`本篇帖子的文件是：`

### `own_superalpha.py`

# 1. 生成模拟配置（针对特定区域）
python own_superalpha.py gen_configs --region EUR

# 2. 运行模拟（处理特定日期的配置）
python own_superalpha.py run_sims --date 2024-01-15 --workers 3

### 参数说明

**gen_configs 命令** ：

- `--region` : 目标区域，支持 USA、GLB、EUR、ASI、CHN、KOR、TWN、HKG、JPN、AMR、IND

**run_sims 命令** ：

- `--date` : 要处理的添加日期（格式：YYYY-MM-DD）
- `--workers` : 并发线程数（默认：3）

---

### 评论 #10 (作者: PZ64174, 时间: 4个月前)

为大佬打call！打爆！太好用了！好用好用还是**的好用！

====================================================================

一年一个台阶，一步一个脚印

====================================================================

---

### 评论 #11 (作者: SD81732, 时间: 4个月前)

春节在家，准备偷师论坛升级自己的SA库，看了这帖子，直接跪了，太强悍了！

有个问题，原生代码中，每个region，只跑其中部分的universe以及neutralization，被选中的的 组合，是实践下来比较容易出好货的吗？

---

### 评论 #12 (作者: YT33830, 时间: 4个月前)

感谢大佬分享，太棒了，正在担心这几天没有好的SA，恰好看到这篇文章，解我燃眉之急

---

### 评论 #13 (作者: WX64154, 时间: 4个月前)

感谢大佬的分享

祝dollars多多

====================================================================================

====================================努力！！！=====================================

==================================================================================

---

### 评论 #14 (作者: HG61318, 时间: 3个月前)

非常感谢代码.
最近刚好在研究SA.
######################################################################
摸摸后缀
######################################################################

---

### 评论 #15 (作者: QL88701, 时间: 3个月前)

自三五架构后另一个能出三五的源代码分享，十分感谢作者的无私开源，已点赞！！

===================================================
每日谨记：
提交因子不能抱侥幸心理！！
坚持一定会有结果！！
===================================================

---

### 评论 #16 (作者: SZ50491, 时间: 2个月前)

大佬们，想请问下，我跑了好几次第一步：# 1. 生成模拟配置（针对特定区域）
python own_superalpha.py gen_configs --region EUR

但是都没有生成文件，是因为alpha数据量不够吗？

API 报告总数: 8 条记录。
正在拉取第 1 页数据...
数据拉取完毕，共 8 条记录。
验证成功: 拉取到的记录数 (8) 与 API 报告的总数 (8) 一致。
未能生成任何满足条件的 selection 表达式，程序结束。

---

### 评论 #17 (作者: JJ60218, 时间: 2个月前)

大佬请问对于各区域的中性化的选择

```
NEUTS = {    'USA': ['STATISTICAL','SLOW_AND_FAST'],    'GLB': ['STATISTICAL','SLOW_AND_FAST'],    'EUR': ['STATISTICAL','SLOW_AND_FAST'],    'ASI': ['STATISTICAL','SLOW_AND_FAST'],    'CHN': ['STATISTICAL','SLOW_AND_FAST'],    'KOR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'TWN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'HKG': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'JPN': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'],    'AMR': ['MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'COUNTRY'],    'IND': ['SLOW_AND_FAST']    }   这部分是经验吗，还是说可以随机
```

---

### 评论 #18 (作者: YS60917, 时间: 1个月前)

开始获取区域 'TWN' (Delay: 1) 的所有 'own' alpha 数据...                                                                
正在为区域 'TWN' (Delay: 1) 拉取表达式的全部结果:                                                                       
  -> own && prod_correlation > 0                                                                                        
正在为区域 'TWN' (Delay: 1) 获取表达式的总记录数:                                                                       
  -> own && prod_correlation > 0                                                                                        
API 报告总数: 35 条记录。                                                                                               
正在拉取第 1 页数据...                                                                                                  
数据拉取完毕，共 35 条记录。                                                                                            
验证成功: 拉取到的记录数 (35) 与 API 报告的总数 (35) 一致。                                                             
成功获取 35 个 'own' alpha。                                                                                            
错误: 不支持的区域 'TWN'。支持的区域有: ['USA', 'GLB', 'EUR', 'ASI', 'CHN', 'AMR', 'IND']为啥跑出来说不支持TWN  USA都是正常的呀 大佬可以解答一下吗

---

