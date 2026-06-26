# Super Alpha 自动生成，多线程自动回测 （mysql 版本 无惧程序宕机，断点续传）代码优化

- **链接**: [Commented] Super Alpha 自动生成多线程自动回测 mysql 版本 无惧程序宕机断点续传代码优化.md
- **作者**: JR23144
- **发布时间/热度**: 1年前, 得票: 125

## 帖子正文

我之前用了一个研究小组里大佬分享的代码，可以自动生成super alpha 并回测，但是pycharm 不小心 卡了，程序终止，于是要重新跑，重新运行时很难确定从哪里继续，造成了不必要的重复工作和时间浪费 。于是改成了 mysql  版本。

首先，你需要在你的MySQL数据库中创建一张表来存储Super Alpha的配置和回测结果。

```
CREATE TABLE `sa_alpha` (  `id` int NOT NULL AUTO_INCREMENT,  `Selection` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,  `Combo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,  `alpha_id` varchar(255) DEFAULT NULL,  `alpha_json` json DEFAULT NULL,  `add_date` date DEFAULT NULL,  `up_date` date DEFAULT NULL,  PRIMARY KEY (`id`),  UNIQUE KEY `id` (`id`)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

接下来，创建一个名为  **insert_sa.py**  的Python脚本。这个脚本会根据预设的 selections, combo, REGIONS 等参数，生成所有可能的Alpha回测配置，并将它们存储到我们刚创建的 sa_alpha 表中。

**重要：**  在运行前，请务必修改脚本中的 MYSQL_CONFIG 为你自己的数据库连接信息！

```
import pymysqlfrom pymysql.cursors import DictCursorimport randomimport json  # Needed to convert dict to JSON string#  数据库配置要改成你自己的MYSQL_CONFIG = {    'user': 'root',    'password': '123456',    'host': '127.0.0.1',    'database': 'world_quant',    'charset': 'utf8mb4'}selections = {    "POSITIVE": [        '1',        'own* (1-self_correlation)',        'own* (1-prod_correlation)',        'own* (1-turnover)',        'own* (1-self_correlation*turnover)',        'own* (1-prod_correlation*turnover)',        'own* (1-prod_correlation*turnover*self_correlation)',        'own* (1-self_correlation)*(1-turnover)',        'own* (1-prod_correlation)*(1-turnover)',        'own* (1-prod_correlation)*(1-self_correlation)',        'own* (1-prod_correlation)*(1-turnover)*(1-self_correlation)',        'own* (1-self_correlation)*turnover',        'own* (1-prod_correlation)*turnover',        '\r\nx = if_else(category == "PRICE_MOMENTUM", 2, 1); y = if_else(category == "PRICE_REVERSION", 0.5, 1); z = (long_count * x * y - short_count); if_else(turnover > 0.2, nan, z)',        '!in(datacategories, "pv")',        '!in(datacategories, "pv") && !in(datacategories, "analyst")',        '(!in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE") * 1/turnover',        '(!in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE") * turnover',        '(in(datacategories, "option") || in(datacategories, "model")) && (os_start_date > "2012-06-01" && color!="PURPLE") * turnover',        '(in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE") * 1/turnover',        '1/(long_count / sqrt(universe_size(universe)) )',        'in(datacategories, "analyst")',        'in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE"',        'is_nan(1);\r\n# universe_size("minvol1m");\r\n!in(datacategories, "pv") && !in(datacategories, "analyst")',        'long_count / sqrt(universe_size(universe)) ',        'long_count / sqrt(universe_size(universe)) * (turnover < 0.2)',        'long_count / sqrt(universe_size(universe)) * (turnover > 0.15)',        'not(in(datacategories, "fundamental")) * (1-self_correlation)',        'turnover<0.1 && (os_start_date > "2012-06-01" && color!="PURPLE") * 1/turnover',        'turnover>0.1 && turnover<0.2 && (os_start_date > "2012-06-01" && color!="PURPLE") * turnover',        'turnover>0.15 && (os_start_date > "2012-06-01" && color!="PURPLE") * turnover',    ],    "NON_ZERO": [],    "NON_NAN": []}combo = [    '1',    "combo_a(alpha)",    'stata = generate_stats(alpha);\r\na = stata.pnl;\r\nts_mean(a, 20)/ts_std_dev(a, 20)\r\n',    'stata = generate_stats(alpha);\r\na = stata.pnl;\r\nts_mean(a, 40)/ts_std_dev(a, 40)\r\n',    'stata = generate_stats(alpha);\r\na = stata.pnl;\r\nts_mean(a, 250)/ts_std_dev(a, 250)\r\n',    'stata = generate_stats(alpha);\r\na = stata.returns;\r\nts_mean(a, 20)/ts_std_dev(a, 20)\r\n',    'stata = generate_stats(alpha);\r\na = stata.returns;\r\nts_mean(a, 40)/ts_std_dev(a, 40)\r\n',    'stata = generate_stats(alpha);\r\na = stata.returns;\r\nts_mean(a, 250)/ts_std_dev(a, 250)\r\n',    'stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr',]REGIONS = {    "USA": ["TOP3000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500"],    "GLB": ["TOP3000", "MINVOL1M"],    "EUR": ["TOP2500", "TOP1200", "TOP800", "TOP400", "ILLIQUID_MINVOL1M"],    "ASI": ["MINVOL1M", "ILLIQUID_MINVOL1M"],    "CHN": ["TOP2000U"],}neutralizations = ['MARKET', 'SECTOR', 'INDUSTRY', 'STATISTICAL', 'CROWDING', 'FAST', 'SLOW', 'SLOW_AND_FAST']delay = 1# sess = login() # Assuming login() is defined and potentially used by machine_libregion_to_process = REGIONS["USA"]sim_config_list = []for universe in region_to_process:    for neutralization in neutralizations:        for selectionLimit in [10, 15, 20, 25, 30, 50]:            for selectionHandling in selections.keys():                for item_selection_str in selections[selectionHandling]:                    for item_combo_str in combo:                        # This dictionary will be serialized into the alpha_json column                        # AND item_selection_str & item_combo_str will go into their respective DB columns                        full_item_data_dict = {                            "type": "SUPER",                            "settings": {                                "nanHandling": "OFF",                                "instrumentType": "EQUITY",                                "delay": delay,                                "universe": universe,                                "truncation": 0.01,                                "unitHandling": "VERIFY",                                "selectionLimit": selectionLimit,                                "selectionHandling": selectionHandling,                                "pasteurization": "ON",                                "region": "USA",                                  "language": "FASTEXPR",                                "decay": 5,                                "neutralization": neutralization,                                "visualization": False,                                "testPeriod": "P2Y",                            },                            "combo": item_combo_str,  # Storing combo string inside the JSON data                            "selection": item_selection_str  # Storing selection string inside the JSON data                        }                        # We store the main components separately for easy access before DB insertion                        config_entry = {                            "full_item_data_dict": full_item_data_dict,  # This will be JSON serialized                            "item_selection_str": item_selection_str,  # For the 'Selection' DB column                            "item_combo_str": item_combo_str  # For the 'Combo' DB column                        }                        sim_config_list.append(config_entry)random.shuffle(sim_config_list)print("sim_config_list length:", len(sim_config_list))conn = Nonecursor = Nonetry:    conn = pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor)    cursor = conn.cursor()    insert_sql_sa_alpha = """       INSERT INTO sa_alpha (Selection, Combo, alpha_id, alpha_json, add_date)        VALUES (%(selection_val)s, %(combo_val)s, NULL, %(alpha_json_val)s, CURDATE())    """    inserted_count = 0    for config_entry in sim_config_list:        selection_for_column = config_entry["item_selection_str"]        combo_for_column = config_entry["item_combo_str"]        dict_for_json_column = config_entry["full_item_data_dict"]        # Convert the full item_data_dict to a JSON string        alpha_json_string = json.dumps(dict_for_json_column)        data_for_db = {            'selection_val': selection_for_column,            'combo_val': combo_for_column,            'alpha_json_val': alpha_json_string            # If using Python for date: 'add_date_val': current_date        }        try:            cursor.execute(insert_sql_sa_alpha, data_for_db)            inserted_count += 1        except pymysql.Error as e:            print(                f"Error inserting data for: Selection='{selection_for_column[:50]}...', Combo='{combo_for_column[:50]}...'")            print(f"MySQL Error: {e}")    conn.commit()    print(f"Successfully inserted {inserted_count} records into sa_alpha.")except pymysql.Error as e:    print(f"Database connection or operational error: {e}")    if conn:        conn.rollback()finally:    if cursor:        cursor.close()    if conn:        conn.close()    print("Database connection closed.")
```

然后，创建另一个名为  **run_sa.py**  的Python脚本。该脚本会从数据库中查询指定 add_date 且尚未成功回测（alpha_id 为 NULL 且 up_date 为 NULL）的Alpha配置，通过多线程调用WorldQuant Brain API进行回测。成功获取到 alpha_id 后，会回填到数据库中，并更新 up_date。如果回测失败或未获取到 alpha_id，则只更新 up_date。

```
from machine_lib import *import jsonimport concurrent.futuresfrom concurrent.futures import ThreadPoolExecutorimport pymysqlfrom pymysql.cursors import DictCursorfrom datetime import date, datetime  # 需要 datetime 来处理时间戳或日期import time  # wait_get 和 simulate_alphas 中用到了 time.sleep，确保导入# 同样的这里要修改数据库配置和你自己的一样MYSQL_CONFIG = {    'user': 'root',    'password': '123456',    'host': '127.0.0.1',    'database': 'world_quant',    'charset': 'utf8mb4'}# --- 全局变量和配置 (从原代码中保留) ---# selections, combo, REGIONS, neutralizations, delay 已不再直接用于生成 sim_data_list# 它们现在被认为是已存在于数据库 alpha_json 中的配置sess = login()  # 初始化会话，simulate_alphas 会用到alpha_fail_attempt_tolerance = 5  # 每个 alpha 允许的最大失败尝试次数MAX_WORKERS = 3  # 同时处理的最大alpha数量failure_count = 0  # simulate_alphas 中用到的全局变量# --- API 调用函数 (基本保持不变) ---def wait_get(url: str, max_retries: int = 10) -> "Response":  # type: ignore    """    发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。    此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。    Args:        url (str): 目标 URL。        max_retries (int, optional): 最大重试次数，默认为 10。    Returns:        Response: 请求的响应对象。    """    retries = 0    global sess  # 确保 sess 是可访问的    while retries < max_retries:        while True:            try:                simulation_progress = sess.get(url)                if simulation_progress.headers.get("Retry-After", "0") == "0":  # Retry-After 是字符串                    break                time.sleep(float(simulation_progress.headers["Retry-After"]))            except requests.exceptions.RequestException as e:  # 更具体的异常捕获                print(f"请求 {url} 时发生网络错误: {e}, 等待后重试...")                time.sleep(5)  # 发生连接错误等，稍等后重试内部循环                continue  # 继续内部while True循环            except Exception as e:                print(f"wait_get 内部发生未知错误: {e}, url: {url}")                time.sleep(5)                continue        if simulation_progress.status_code < 400:            try:                # 尝试解析JSON，如果文本不是有效的JSON，split会出问题                content_type = simulation_progress.headers.get('Content-Type', '')                if 'application/json' in content_type:                    # 只有当内容是JSON时才尝试解析                    sim_data = simulation_progress.json()                    if isinstance(sim_data,                                  dict) and "message" in sim_data and "ERROR" in simulation_progress.text:  # 检查message字段和原始文本                        print(f"回测API返回错误信息 {url}：{sim_data.get('message')}")                elif "ERROR" in simulation_progress.text:  # 非JSON但包含ERROR                    print(f"回测API返回非JSON错误文本 {url}：{simulation_progress.text[:200]}")  # 打印部分文本            except json.JSONDecodeError:                if "ERROR" in simulation_progress.text:  # 如果JSON解析失败但文本中包含ERROR                    print(f"回测API返回错误文本 (JSON解析失败) {url}：{simulation_progress.text[:200]}")            break  # 成功或有message的错误，都跳出重试        elif simulation_progress.status_code == 401:  # 未授权            print(f"请求 {url} 遇到401未授权错误，尝试重新登录...")            sess = login()  # 重新登录            # 不需要增加 retries，因为这是会话问题，而不是请求本身的问题            # 但为了避免死循环，如果login持续失败，外部逻辑需要处理        else:            print(f"请求 {url} 失败，状态码: {simulation_progress.status_code}, 内容: {simulation_progress.text[:200]}")            time.sleep(2 ** retries)            retries += 1    if retries >= max_retries:        print(f"达到最大重试次数 {max_retries} 仍然失败: {url}")    return simulation_progressdef simulate_alphas(db_id,data_for_simulation):  # 参数名修改以示区分    """    data_for_simulation: simulation data dictionary    return alpha list or False on critical failure    """    print(        f"线程 {threading.get_ident()} 开始处理任务: ",db_id)  # 打印当前线程ID和部分信息    keep_trying = True    global failure_count  # simulate_alphas内部的失败计数器    global sess  # simulate_alphas内部使用的会话    local_failure_count = 0  # 此函数调用的失败计数    while keep_trying:        try:            simulation_response = sess.post('https://api.worldquantbrain.com/simulations', json=data_for_simulation)            simulation_response.raise_for_status()  # 如果POST请求失败（4xx, 5xx），则抛出异常            simulation_progress_url = simulation_response.headers['Location']            children_ids_str = simulation_progress_url.split('/')[-1]            children_ids = [children_ids_str]  # 假设总是单个child            alphas_results = []            for child_id in children_ids:                child_url = f'https://api.worldquantbrain.com/simulations/{child_id}'                child_progress_response = wait_get(child_url)                if child_progress_response.status_code >= 400:                    print(f"获取子任务 {child_id} 进度失败。状态码: {child_progress_response.status_code}")                    alphas_results.append(None)  # 标记此子任务失败                    continue                try:                    child_progress = child_progress_response.json()                except json.JSONDecodeError:                    print(f"解析子任务 {child_id} 响应失败。响应文本: {child_progress_response.text[:200]}")                    alphas_results.append(None)                    continue                print(f"子任务 {child_id} 状态: {child_progress.get('status')}")                if child_progress.get('status') in ['CANCELLED', 'ERROR']:  # 增加 'ERROR' 状态                    print(                        f"错误：模拟任务 {db_id} 的子任务 {child_id} 状态为 {child_progress.get('status')}, 详情: {child_progress}")                    alphas_results.append(None)                elif child_progress.get('status') in ['COMPLETE', 'WARNING']:                    alphas_results.append(child_progress.get('alpha'))  # 获取alpha ID                else:  # 其他未完成或未知状态                    print(f"子任务 {child_id} 状态未完成或未知: {child_progress.get('status')}")                    alphas_results.append(None)  # 视为未成功获取alpha            print(f"线程 {threading.get_ident()} 模拟结果: {alphas_results}")            return alphas_results  # 返回包含alpha ID或None的列表        except requests.exceptions.HTTPError as http_err:            print(f"HTTP错误发生在 simulate_alphas (POST): {http_err}, data: {str(data_for_simulation)[:100]}")            if http_err.response.status_code == 401:                print("会话可能已过期，尝试重新登录...")                sess = login()                # 不立即重试，让外部循环或重试机制处理            local_failure_count += 1        except requests.exceptions.RequestException as req_err:  # 其他网络错误，如DNS、连接超时            print(f"网络请求错误发生在 simulate_alphas: {req_err}, data: {str(data_for_simulation)[:100]}")            local_failure_count += 1        except KeyError as ke:  # 比如 'Location' 不在 headers 里            print(f"关键信息缺失 (KeyError: {ke})，可能POST请求未成功。data: {str(data_for_simulation)[:100]}")            local_failure_count += 1        except Exception as e:            print(f"simulate_alphas中发生未知异常: {e}, data: {str(data_for_simulation)[:100]}")            local_failure_count += 1        # 重试逻辑        if local_failure_count > 0:  # 只有发生错误才进入重试判断            print(f"尝试次数 {local_failure_count}/{alpha_fail_attempt_tolerance}。等待15秒后重试...")            time.sleep(15)            failure_count += 1  # 更新全局的failure_count，用于判断是否需要重新login            if failure_count >= alpha_fail_attempt_tolerance:  # 此处用全局的failure_count判断是否需要重新login                print("全局失败次数达到阈值，尝试重新登录...")                sess = login()                failure_count = 0  # 重置全局失败计数器            if local_failure_count >= alpha_fail_attempt_tolerance:  # 如果此函数内的尝试次数达到上限                print(f"此任务失败次数已达上限 {alpha_fail_attempt_tolerance}，放弃处理。")                return False  # 表示此任务彻底失败        else:  # 如果没有错误，说明成功了            keep_trying = False  # 退出while循环    return False  # 如果循环因其他原因退出（理论上不应该）# --- 数据库交互函数 ---def get_db_connection():    """建立并返回一个新的数据库连接"""    return pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor)def fetch_sim_configs_from_db(target_add_date_str: str):    """从数据库获取待处理的模拟配置"""    conn = get_db_connection()    sim_configs = []    try:        with conn.cursor() as cursor:            # 选择id和alpha_json，条件是alpha_id为空且add_date匹配            sql = "SELECT id, alpha_json FROM sa_alpha WHERE up_date IS NULL AND add_date = %s"            cursor.execute(sql, (target_add_date_str,))            sim_configs = cursor.fetchall()  # [{'id': X, 'alpha_json': 'json_string'}, ...]    except pymysql.Error as e:        print(f"从数据库读取数据失败: {e}")    finally:        if conn:            conn.close()    print(f"为日期 {target_add_date_str} 从数据库获取到 {len(sim_configs)} 条待处理记录。")    return sim_configsdef update_alpha_in_db(db_id: int, new_alpha_id: str = None):    """更新数据库中的alpha_id和up_date"""    conn = get_db_connection()    success = False    try:        with conn.cursor() as cursor:            current_date_str = date.today().isoformat()            if new_alpha_id:                sql = "UPDATE sa_alpha SET alpha_id = %s, up_date = %s WHERE id = %s"                cursor.execute(sql, (new_alpha_id, current_date_str, db_id))            else:                # 如果 new_alpha_id 为 None 或空字符串，只更新 up_date                sql = "UPDATE sa_alpha SET up_date = %s WHERE id = %s"                cursor.execute(sql, (current_date_str, db_id))            conn.commit()            success = True            action = f"已更新 alpha_id 为 {new_alpha_id}" if new_alpha_id else "仅更新 up_date"            print(f"数据库记录 ID {db_id}: {action}。")    except pymysql.Error as e:        print(f"更新数据库记录 ID {db_id} 失败: {e}")        if conn:            conn.rollback()    finally:        if conn:            conn.close()    return success# --- 任务处理函数 (用于线程池) ---import threading  # 用于获取线程ID，方便日志追踪def process_simulation_task(db_record):    """    处理单个数据库记录：解析json，调用API，更新数据库    db_record: {'id': int, 'alpha_json': str}    """    db_id = db_record['id']    alpha_json_str = db_record['alpha_json']    if not alpha_json_str:        print(f"记录 ID {db_id}: alpha_json 为空，跳过处理并更新up_date。")        update_alpha_in_db(db_id, None)        return    try:        # 解析JSON字符串为字典        simulation_params = json.loads(alpha_json_str)    except json.JSONDecodeError as e:        print(f"记录 ID {db_id}: JSON解析失败 - {e}。alpha_json: {alpha_json_str[:100]}... 跳过处理并更新up_date。")        update_alpha_in_db(db_id, None)  # 标记为已尝试        return    # 调用 simulate_alphas 函数    # simulate_alphas 返回一个列表，通常包含一个alpha ID或None，或返回False表示严重失败    api_results = simulate_alphas(db_id,simulation_params)    returned_alpha_id = None    if isinstance(api_results, list) and len(api_results) > 0:        # 取第一个结果，如果它是有效的alpha ID字符串        if api_results[0] and isinstance(api_results[0], str) and api_results[0].strip():            returned_alpha_id = api_results[0].strip()    elif api_results is False:        print(f"记录 ID {db_id}: simulate_alphas 返回 False，表示任务处理严重失败。")        # 这种情况也只更新up_date，不更新alpha_id    # 根据API结果更新数据库    update_alpha_in_db(db_id, returned_alpha_id)# --- 主程序逻辑 ---if __name__ == "__main__":    # 用户指定要处理的 add_date    target_add_date_input = "2025-06-08"    try:        # 验证日期格式        datetime.strptime(target_add_date_input, '%Y-%m-%d')    except ValueError:        print("日期格式无效，请输入 YYYY-MM-DD 格式的日期。")        exit()    # 1. 从数据库获取待处理的配置    tasks_to_process = fetch_sim_configs_from_db(target_add_date_input)    if not tasks_to_process:        print(f"日期 {target_add_date_input} 没有需要处理的记录，或数据库连接失败。")    else:        print(f"准备使用 {MAX_WORKERS} 个线程处理 {len(tasks_to_process)} 个任务...")        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:            # 为每个任务提交到线程池            future_to_task = {executor.submit(process_simulation_task, task): task for task in tasks_to_process}            for future in concurrent.futures.as_completed(future_to_task):                task_info = future_to_task[future]                try:                    future.result()  # 获取结果，主要是为了捕获在 process_simulation_task 中未捕获的异常                    # print(f"任务 (DB ID: {task_info['id']}) 完成。") # 可以在 process_simulation_task 内部打印                except Exception as exc:                    print(f"任务 (DB ID: {task_info['id']}) 执行时产生异常: {exc}")        print("所有任务处理完毕。")
```

粘贴好代码后 ，修改下面的日期，即可运行，自动回测
 ![图片](images/img_0b502e659c.png)

运行此脚本后，它会自动处理指定日期的任务。如果中途停止，下次重新运行，它会继续处理该日期下之前未完成或未成功获取 alpha_id 的记录（根据 up_date IS NULL 的条件）。

 **希望这个小脚本能帮你解放双手，专心搞模板！** 
 **觉得还行？一个小赞就能让我动力满满，一起day day Alpha！**

---

## 讨论与评论 (24)

### 评论 #1 (作者: LQ78150, 时间: 1年前)

亲测有效，感谢无私分享，妈妈再也不用担心我的SuperAlpha了，哈哈

---

### 评论 #2 (作者: MG88592, 时间: 1年前)

已赞，
感谢大佬的分享，想问一下大佬这个代码跑出来的因子大概有多少可以过查重。
发现跑出来的相当一部分都是高pc。或者是条件不满足的劣质sa。
没有手搓的好。
=========================================================================================================================================================================

---

### 评论 #3 (作者: MM78881, 时间: 1年前)

代码是非常的棒，融入了数据库的操作，再也不用担心重复选择了，知行合一的人真的非常的厉害。有个小建议就是中间的六层嵌套嵌套循环地狱，感觉可以在哪边做随机选择可能会更优雅一些。

==================================================================================================================================================================================================================================================================================================================================================

---

### 评论 #4 (作者: YQ51506, 时间: 1年前)

不错的代码，很有借鉴意义，赞！

---

### 评论 #5 (作者: JR23144, 时间: 1年前)

[MG88592](/hc/en-us/profiles/28831584109591-MG88592)  可以修改 selections 集合 中的内容 ，会提高 pc 哦

---

### 评论 #6 (作者: AH18340, 时间: 1年前)

感谢大佬分享

---

### 评论 #7 (作者: LZ14530, 时间: 1年前)

感谢分享，处理的流程很值得借鉴

---

### 评论 #8 (作者: FL39657, 时间: 1年前)

断点续传这个功能真的很有用，可以避免很多麻烦

---

### 评论 #9 (作者: SY90356, 时间: 1年前)

感谢！请问您的这套分享代码里是不是只跑的USA？

---

### 评论 #10 (作者: JR23144, 时间: 1年前)

![图片](images/img_bf8a209ba7.png)  [SY90356](/hc/en-us/profiles/27705939991959-SY90356)  你好，可以 修改成其他想要的区域，都是通用的， 修改如图片所示的这两个地方就能换成其他地区哦
====================================================================================

---

### 评论 #11 (作者: JZ18078, 时间: 1年前)

可以把最后的运行日期也存入数据库，然后下次运行的时候自动去取出这个日期，自动运行

---

### 评论 #12 (作者: YH25030, 时间: 1年前)

谢谢分享。我最近回测经常报错，也不知道那些回测需要重跑。看了您的分享，觉得利用数据库可以帮我在RA时遇到的问题。利用MySQL把每次失败的回测写入数据库，最后放到一起重跑。

====================================================================================

---

### 评论 #13 (作者: YC62305, 时间: 11个月前)

感谢大佬分享

---

### 评论 #14 (作者: XX81632, 时间: 9个月前)

看完大佬的文章我觉得我现在强的可怕！

---

### 评论 #15 (作者: YL20304, 时间: 8个月前)

感谢大佬的分享，注大佬在下一轮比赛中拿大奖！

---

### 评论 #16 (作者: CG96890, 时间: 8个月前)

在mysql 8以下创建数据库语句报错。可以改为

CREATE TABLE `sa_alpha` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Selection` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `Combo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `alpha_id` varchar(255) DEFAULT NULL,
  `alpha_json` json DEFAULT NULL,
  `add_date` date DEFAULT NULL,
  `up_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

---

### 评论 #17 (作者: CW49566, 时间: 7个月前)

精华帖，给大佬点赞。受益很大。

---

### 评论 #18 (作者: LL73664, 时间: 7个月前)

大佬 提示没有

machine_lib 文件 还是库 我能去哪里下载呢 感谢 程序小白

---

### 评论 #19 (作者: JQ70858, 时间: 7个月前)

马上去实践。一个superalpha都没提交过，还是一头雾水。。

---

### 评论 #20 (作者: YL20304, 时间: 7个月前)

感谢大佬分享，有没有最新super alpha模板呢？期待大佬更新

---

### 评论 #21 (作者: HL81191, 时间: 5个月前)

![图片](images/img_5f198a5538.png) 试了一下，生成好多个，但是回测限制不可能回测得完，先跑两天试试效果

---

### 评论 #22 (作者: HL81191, 时间: 5个月前)

提醒一下还没有跑SA的小伙伴，使用user阶段的alpha组SA会有一段时间的缺失值，大概率表现不好，所以得在selection的表达式加上" **&&(prod_correlation>0)** "来过滤user阶段的alpha。我已经跑了5000+多个了，用脚本自动交了一些SA,发现很多个的PNL都有缺失，所以才更新数据库里的Selection和alpha_json

---

### 评论 #23 (作者: GC81559, 时间: 5个月前)

这个采用数据库的方式记录sa的方法给了我很多灵感，超级有用，感谢感谢

---

### 评论 #24 (作者: YW34314, 时间: 3个月前)

非常有借鉴意义的SA生成代码，试着运行了，对代码有略微的改动，成功生成了SA并完成了回测。后面会根据自己的了解，慢慢优化selections和combo的方式。

---

