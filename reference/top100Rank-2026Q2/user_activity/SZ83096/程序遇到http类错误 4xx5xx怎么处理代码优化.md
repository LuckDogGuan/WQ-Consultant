# 程序遇到http类错误 4xx,5xx怎么处理代码优化

- **链接**: 程序遇到http类错误 4xx5xx怎么处理代码优化.md
- **作者**: SZ83096
- **发布时间/热度**: 1年前, 得票: 59

## 帖子正文

最近经常有小伙伴提到遇到429错误，偶尔也遇到5xx错误。就我个人的理解，429是限频返回的错误,可通过调整自己代码中接口请求的频率，且代码需要兼容处理这类错误。5xx类错误，是服务器出现异常导致的，需要客户端进行重试。

在brain的各类接口中，最经常调用的几个接口有

```
1、回测 post 请求接口：/simulations2、打tag 的patch 请求接口3、其他get请求，get回测接口，get alpha详情等接口4、登录认证接口
```

关于登录认证接口，有小伙伴反馈遇到过429错误，我个人是没有遇到过的，但是有遇到5xx错误，登录429的问题，可以参考课代表新发的帖子，我自己也是使用全局变量来避免频繁登录的。

我之前修改为全局变量session的时候，还遇到一个错误，忘记在需要调用session的函数中增加 global s这行代码了，导致回测中断了几个小时。小伙伴们如果也修改为用全局变量session,记得避过这个坑~~

1,2,3接口，请求的时候经常会遇到各种http错误，为了避免重复的处理错误的代码，我把reqest请求和处理错误的代码封装到了一个函数中，在发起请求的时，直接调用该函数即可，函数如下：

该函数考虑了session过期 401 错误，429 限频，5xx错误的处理，后续如果有新的错误需要特殊处理，可直接在函数中增加对新错误的处理。

```
import requestsimport timefrom requests.exceptions import Timeout,HTTPError,RequestExceptiondef my_req(request_method,url,json_data=None,timeout=None):"""request_method 可选值： post,get,patch  ;stringurl: 请求的Urljson_data: json格式的请求参数timeout: 请求超时的时间设置，int"""   # 使用全局的session    global s    retries=0    max_retries=3    while retries < max_retries:        try:            # 发送回测请求（使用全局变量的s ）            if request_method == "post" and json_data != None:                response = s.post(url, json=json_data, timeout=timeout if timeout is not None else 15)            # 设置alpha 属性            elif request_method == "patch" and json_data  != None:                response = s.patch(url, json=json_data)            elif request_method == "get":                       #其他get请求                response = s.get(url,timeout=timeout if timeout is not None else 15)            try:                response.raise_for_status()                # 没有错误，直接返回结果                return response            except HTTPError as http_err:                if response.status_code == 401 or "Unauthorized" in str(http_err):                    print(f" status code:{response.status_code} 未认证,relogin")                    print("401未认证，尝试重新登录...")                    try:                        new_session = login()                        if new_session != None:                            s = new_session                    # 重置retries或继续使用剩余次数                    # retries = 0  # 可选：重新登录后重置计数器                    except Exception as e:                        print(f"登录失败: {str(e)}")                        retries += 1                    continue                elif response.status_code ==403 or "403 " in str(http_err):                    print(f"status code:{response.status_code} Forbidden 无权限访问（认证成功但权限不足）,{response.content},break")                    return None                elif response.status_code in [429,500,502,503,504]:                    wait = 2 ** retries  # 指数退避                    print(f"status code: {response.status_code} ,{response.content} ,sleep 5 and retry" )                    time.sleep(wait)                    retries += 1                else:                    raise http_err        except Timeout as e:            print(f"timeout err {e}, sleep 30 and retry")            retries += 1            time.sleep(5)        except RequestException as e:            print(f"请求失败: {str(e)}")            retries += 1            time.sleep(5)        except Exception as e:            print(f"error err {e} ,exit get request")            print(f"未知错误: {str(e)}")            retries += 1            # return None    print(f"达到最大重global session试次数 {max_retries}，放弃请求")    return None
```

如何使用该函数：

```
# 发送回测请求：reponse =my_req(request_method="post",url=url,json_data=sim_data_list,timeout=15)# 设置属性：reponse =my_req(request_method="patch",url=url,json_data=alpha_properties_json,timeout=15)# 其他get请求reponse =my_req(request_method="get",url=url,timeout=15)后续根据response 结果处理：if response !=None:#请求成功：  xxxelse:# 请求失败：# 如果是回测 请求没有成功，我最后是把任务重新加回队列；  yyy
```

还有个问题，如果同时开2个脚本设置属性，是一定会遇到429限频错误的。我是只跑1个脚本单独设置属性，函数每次调用一次设置属性，就sleep 1-2s，持续24小时运行。

---

## 讨论与评论 (2)

### 评论 #1 (作者: BW14163, 时间: 1年前)

好奇，如何只跑1个脚本单独设置属性，是将单独设置属性的脚本 import进其他的程序中直接调用吗？这个过程在win如何实现呢

---

### 评论 #2 (作者: SZ83096, 时间: 1年前)

[BW14163](/hc/en-us/profiles/28900537669399-BW14163) :

在回测完成后，将获得的child id数组存入数据库；然后另外的脚本从数据库中读取并设置属性。

```
存数据库的代码：import sqlite3# child id数组插入数据库的函数：def insert_into_db(db_path, key, value, tablename):    """向数据库插入数据"""    conn = sqlite3.connect(db_path)    cursor = conn.cursor()    try:        cursor.execute(f"INSERT INTO \"{tablename}\" (key, value) VALUES (?, ?)", (key, value))        conn.commit()        print(f"Inserted: {key} -> {value}")    except sqlite3.IntegrityError:        print(f"Key '{key}' already exists.")    finally:        conn.close()创建存child id 数组的表：def initialize_db(db_path, tablename):    """    初始化数据库并根据给定的表名创建表。    :param db_path: 数据库文件路径（包含文件名）    :param tablename: 要创建的表名    """    try:        # 连接到SQLite数据库（如果数据库不存在，则会自动创建）        conn = sqlite3.connect(db_path)        cursor = conn.cursor()        # 动态生成创建表的SQL语句        create_table_query = f'''CREATE TABLE IF NOT EXISTS {tablename} (                                    id INTEGER PRIMARY KEY AUTOINCREMENT,                                    key TEXT UNIQUE,                                    value TEXT)'''        # 执行创建表的SQL语句        cursor.execute(create_table_query)        # 提交事务        conn.commit()        print(f"数据库 '{db_path}' 和表 '{tablename}' 已成功初始化。")    except sqlite3.Error as e:        print(f"发生错误：{e}")    finally:        # 关闭数据库连接        if conn:            conn.close()# 插入数据insert_into_db(save_child_simulaet_urldb, progress, json.dumps(children), saveurl_table)
```

从数据库读取并设置属性的关键部分代码：

```
# 从数据库读取，import sqlite3def query_entry(db_path, tablename,order):    """    根据键查询数据库中的记录。    :param db_path: SQLite 数据库文件路径    ：tablename ： 表名    :param order: 要查询的键 的id    :return: 对应的值，如果不存在则返回 None    """    print(db_path)    print(f"从db中 获取alpha,需要{order}")    conn = sqlite3.connect(db_path)    cursor = conn.cursor()    print(db_path)    print(tablename)    cursor.execute(f"SELECT value FROM \"{tablename}\" WHERE id=?", (order,))    result = cursor.fetchone()    if result is None:        print(f"获取失败：{order} {result}")    else:        print(f"获取成功：{order} {result}")    conn.close()    return result[0] if result else None从数据库读取child id并设置属性：（部分代码）def process_child_simulate_reult( db,tablename,alpha_name,tag,order_id,ok_file,failed_to_get_resul):    brain_api_url = 'https://api.worldquantbrain.com'    if os.path.exists(order_file):        with open(order_file, "r") as f:            order_id = int(f.read().strip())  # 从文件中读取 order    else:        order_id=order_id    while True:  # 无限循环        simulate_ids_str = query_entry(db, table, order_id)        if not simulate_ids_str:            print(f"未找到 ID，等待 5 分钟后重试...")            append_to_file(log_file, f"未找到 ID {order}，等待 2 分钟后重试...")            sleep(120)  # 等待 2 分钟            continue  # 继续下一次循环        # 只有在成功获取数据后才更新 order        try:            simulate_ids = json.loads(simulate_ids_str)  # 确保 simulate_ids_str 有效        except json.JSONDecodeError:            print(f"解析 JSON 失败: {simulate_ids_str}")            append_to_file(log_file, f"解析 JSON 失败: {simulate_ids_str}")            # 将失败的 simulate_ids_str 写入文件            append_to_file(failed_to_get_result, simulate_ids_str)            order_id += 1            continue  # 跳过当前循环，继续尝试        # 更新 order 并写入文件        order_id += 1  # 更新 order        with open(order_file, "w") as f:            f.write(str(order_id))  # 将当前 order 写入文件        alpha_infos=[]        for simulate_id in simulate_ids:#            child_progress =my_req(request_method="get",url=f"{brain_api_url}/simulations/{simulate_id}",timeout=15)            if child_progress == None:                print(f"处理 {simulate_id} 时发生错误")                print("跳过这个采集.")                append_to_file(log_file, f"处理 {simulate_id} 时发生错误: ")                append_to_file(failed_to_process_url, f"{brain_api_url}/simulations/{simulate_id}")                continue            try:                print(f"{brain_api_url}/simulations/{simulate_id}")                append_to_file(log_file, f"{brain_api_url}/simulations/{simulate_id}")                alpha_id = child_progress.json()["alpha"]                alpha_properties_json =  {                      "color": "RED",                       "name": "xxx",                       "tags":["xxx"],                       "category": None,                       "regular": {"description": description},                        "combo": {"description": "None"},                       "selection": {"description":"None"},                       }                reponse =my_req(request_method="patch",url=f"https://api.worldquantbrain.com/alphas/{alpha_id}",json_data=alpha_properties_json,timeout=15)                if res == None:                    print(f" {alpha_id} get alpha detail,set alpha_name failed,switch")                    continue            except Exception as e:                print(f"处理 {simulate_id} 时发生错误: {e}")                print("跳过这个采集.")                append_to_file(log_file, f"处理 {simulate_id} 时发生错误: {e}")                append_to_file(failed_to_process_url, f"{brain_api_url}/simulations/{simulate_id}")                sleep(5)
```

---

