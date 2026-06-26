# 【 SA赚钱大法 】怎么快速找到有可能降低prod到0.5以下的sa进行调整代码优化

- **链接**: [Commented] 【 SA赚钱大法 】怎么快速找到有可能降低prod到05以下的sa进行调整代码优化.md
- **作者**: SZ83096
- **发布时间/热度**: 1年前, 得票: 75

## 帖子正文

fit>5,prod小于5的SA,是小伙伴们都追求的梦中SA。那么如何快速找到有比较大的可能可以调整到低于0.5的SA进行调整呢？

这里的思路是：

```
1、获取已有的SA列表（包含详细信息）；（代码回测super alpha，    这样你就可以有超级多的superalpha 选择了）2、检查自相关性（参考 KZ79256 大佬的帖子），如果自相关超过5，就跳过检查生产相关3、检查生产相关性，并获取每个相关性区间的alpha数，最后存入本地文件。  根据check结果，选择fit>5, 0.4-0.5区间，0.5-0.6区间相对较少的SA，尝试降低prod,   这样成功的概率会比较高。
```

代码如下：（本地自相关性的计算，这里就不详细描述了，可自行参考  **KZ79256** 大佬的帖子 ； [看这里](../KZ79256/本地0误差计算自相关性【即插即用版】代码优化.md) )

```
    # 加载本地pnl数据    os_alpha_ids, os_alpha_rets = load_data()    start=0    # alpha_infos是个列表，列表中是每个alpha的详细信息，可通过get_alpha函数获取    alpha_infos = alpha_infos[start:]    for i  in range(0,len(alpha_infos)):         alpha_info=alpha_infos[i]         alpha_id=alpha_info["id"]         print(f"begin check id :{i+start}, {alpha_id}")         # append_to_file 函数是个记录日志的函数         append_to_file("check.log",f"begin check id :{i+start}, {alpha_id} ",True)         date_create=alpha_info["dateCreated"]         fitness = alpha_info['is']['fitness']         sharpe = alpha_info['is']['sharpe']         turnover = alpha_info['is']['turnover']         margin = alpha_info['is']['margin']         drawdown = alpha_info['is']['drawdown']         returns = alpha_info['is']['returns']         region = alpha_info['settings']['region']         checks=alpha_info["is"]["checks"]         LOW_2Y_SHARPE=0         for item in checks:             if item["name"] == LOW_2Y_SHARPE:                 LOW_2Y_SHARPE=item["value"]         #检查自相关         corr_id,corr_value=calc_self_corr( alpha_id, os_alpha_rets,  os_alpha_ids,None,True,None)         f = float(corr_value)         rounded_f = round(f, 4)         if   rounded_f >=0.5:             print(f"selfcorr more than 0.5,and self > 0.7 ;switch {alpha_id};  self:{rounded_f}")             set_alpha_properties(alpha_id=alpha_id, name=f"SELF_CORR_{rounded_f}", color="BLUE")             continue         num4_num5=0         num5_num6=0         num6_num7=0         while True:         # 获取prod 相关性值            response=my_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod")            if response != None:                try:                    res=response.json()                    prod=res["max"]                    for list_ in res["records"]:                    # 获取相关性在0.4-0.5区间的alpha数                        if list_[0] == 0.4 and list_[1] == 0.5:                            num4_num5=list_[2]                    # 获取相关性在0.5-0.6区间的alpha数                        if list_[0] == 0.5 and list_[1] == 0.6:                            num5_num6=list_[2]                    # 获取相关性在0.6-0.7区间的alpha数                        if list_[0] == 0.6 and list_[1] == 0.7:                            num6_num7=list_[2]                    break                except Exception as e:                    print(f"get prod failed,try again")            sleep(10)         if  fitness > 5 and prod < 0.5 and sharpe >5 and LOW_2Y_SHARPE >=5:             print(f"begin submit alpha: {alpha_id}")             append_to_file("submit.log",f"fit>5,prod<5的alpha id: {alpha_id}",True)             #submit_alpha(s,alpha_id)         com_des=alpha_info["combo"]["description"]         select_des=alpha_info["selection"]["description"]         set_alpha_properties(alpha_id,f"PROD_{str(prod)}","RED")         a=json.dumps([alpha_id,f"self:{rounded_f}",f"prod:{prod}",{"num4_num5":num4_num5,"num5_num6":num5_num6,"num6_num_7":num6_num7,"fitness":fitness,"sharpe":sharpe,"turnover":turnover,"drowdown":drawdown,"returns":returns,"region":region}])         append_to_file("res.txt",a,True)    print(f"finish check")
```

check的结果res.txt如下：

![图片](images/img_9213eef0ca.png)

**⚠️⚠️：**

**在降低prod时，注意不要过拟合 ：）**

---

## 讨论与评论 (16)

### 评论 #1 (作者: ML42552, 时间: 1年前)

-----------------------

太强了橙子姐！！

不愧是vf巨高的女人！！

想要开箱即用版（厚脸皮）

------------------------------------------------------

共好！！

---

### 评论 #2 (作者: DX67257, 时间: 1年前)

那如何降低 prod corr呢

---

### 评论 #3 (作者: AM12075, 时间: 1年前)

获取到因子的id之后，怎么根据id在网页中找到对应的super alpha呢？

---

### 评论 #4 (作者: QZ67721, 时间: 1年前)

感谢大佬帖子，给我组建super alpha带来了新灵感，原本我的super alpha都是在网页上按照sharpe降序排列的，然后从符合提交的alpha里面挨个点击prod check。这个方式确实是太低效率了。下载SA到本地确实会好很多，我可以用我的数据库做出可视化的SA来。

仔细一看居然是橙子姐的帖子，萌新从开始到现在就一直知道有一个周奖破纪录的大佬，今天有幸拜读，开心。

---

### 评论 #5 (作者: SZ83096, 时间: 1年前)

[AM12075](/hc/en-us/profiles/30421958512663-AM12075) ：

和regular alpha一样的，

[https://platform.worldquantbrain.com/alpha/{alpha_id}](https://platform.worldquantbrain.com/alpha/{alpha_id}%C2%A0) 
上面的{alpha_id} 替换成你的alpha_id，在浏览器打开就可以看到superalpha的详细信息了。

====================================================================

---

### 评论 #6 (作者: SZ83096, 时间: 1年前)

DX67257：

一般试着调整下select 的某个条件，或者微调下combo的一些参数，以及遍历下setting的中性化设置吧。

我个人经验，优先更换下风险中和的settings，不过有时候一些风险中和的设置,比如 SLOW,FAST ，会损害alpha的一些性能，需要考虑是否能降低性能后的superalpha 的质量是否合格，sharpe是否衰退等

---

### 评论 #7 (作者: SZ83096, 时间: 1年前)

[ML42552](/hc/en-us/profiles/27182530443671-ML42552)  : 完整的代码如下：

```
import requestsfrom requests.exceptions import Timeout,HTTPError,RequestExceptionfrom typing import Union, List, Tuple,Dictfrom concurrent.futures import ThreadPoolExecutorimport loggingimport picklefrom collections import defaultdictimport numpy as npfrom tqdm import tqdmfrom datetime import datetime, timedeltaimport jsonimport pandas as pdfrom requests.adapters import HTTPAdapterfrom urllib3.util.retry import Retryimport tracebackimport osimport csvimport jsonfrom collections import defaultdictimport timeimport pprintfrom collections import defaultdictfrom time import sleep,timeimport timeimport sysimport randomfrom pathlib import Pathclass cfg:    # 使用示例    username = "xx"    password = "yyy"    data_path = Path('.')def login():    username = "xxx"    password =  "yyy"    retry_strategy = Retry(        total=3,  # 总共重试次数        backoff_factor=1,  # 每次重试之间的延迟时间（秒）        status_forcelist=[500, 502, 503, 504]  # 遇到这些HTTP状态码时重试    )    adapter = HTTPAdapter(max_retries=retry_strategy)    s = requests.Session()    s.mount("https://", adapter)    s.mount("http://", adapter)    s.auth = (username, password)    max_try = 3    retry=0    while True:        try:            response = s.post('https://api.worldquantbrain.com/authentication')            if response.status_code  in [200,201]:                print(response.content)                return s        except Exception as e:            print(f"login err :{e}")            sleep(5)        retry +=1        if retry > max_try:            break    return Nones = login()def save_obj(obj: object, name: str) -> None:    """    保存对象到文件中，以 pickle 格式序列化。    Args:        obj (object): 需要保存的对象。        name (str): 文件名（不包含扩展名），保存的文件将以 '.pickle' 为扩展名。    Returns:        None: 此函数无返回值。    Raises:        pickle.PickleError: 如果序列化过程中发生错误。        IOError: 如果文件写入过程中发生 I/O 错误。    """    with open(name + '.pickle', 'wb') as f:        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)def my_get(url,timeout=None):    retries=0    max_retries=3    global s    while retries < max_retries:        try:            # 发送请求（使用当前 session）            response = s.get(url,timeout=timeout)            try:                response.raise_for_status()                return response            except HTTPError as http_err:                status_code = response.status_code if response else None                if status_code ==401:                    try:                        new_session = login()                        if new_session !=None:                            s = new_session                    except Exception as e:                        print(f"登录失败: {str(e)}")                        retries += 1                    continue                elif status_code ==403:                    print(f"status code:{status_code} Forbidden 无权限访问（认证成功但权限不足）,{response.content},break")                    return None                elif response.status_code in [429,500,502,503,504]:                    wait = 2 ** retries  # 指数退避                    print(f"status code: {response.status_code} ,{response.content} ,sleep 5 and retry" )                    time.sleep(wait)                    retries += 1                else:                    raise http_err        except Timeout as e:            print(f"timeout err {e}, sleep 30 and retry")            retries += 1            time.sleep(5)        except RequestException as e:            print(f"请求失败: {str(e)}")            retries += 1            time.sleep(5)        except Exception as e:            print(f"error err {e} ,exit get request")            print(f"未知错误: {str(e)}")            retries += 1            time.sleep(5)            # return None, current_session    print(f"达到最大重试次数 {max_retries}，放弃请求")    return Nonedef load_obj(name: str) -> object:    """    加载指定名称的 pickle 文件并返回其内容。    此函数会打开一个以 `.pickle` 为扩展名的文件，并使用 `pickle` 模块加载其内容。    Args:        name (str): 不带扩展名的文件名称。    Returns:        object: 从 pickle 文件中加载的 Python 对象。    Raises:        FileNotFoundError: 如果指定的文件不存在。        pickle.UnpicklingError: 如果文件内容无法被正确反序列化。    """    with open(name + '.pickle', 'rb') as f:        return pickle.load(f)def wait_get(url: str, max_retries: int = 10) :    """    发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。    此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。    Args:        url (str): 目标 URL。        max_retries (int, optional): 最大重试次数，默认为 10。    Returns:        Response: 请求的响应对象。    """    retries = 0    global s    max_retries = 3    while retries < max_retries:        while True:            simulation_progress = s.get(url)            if simulation_progress.headers.get("Retry-After", 0) == 0:                break            time.sleep(float(simulation_progress.headers["Retry-After"]))        if simulation_progress.status_code < 400:            break        else:            time.sleep(2 ** retries)            retries += 1    return simulation_progressdef _get_alpha_pnl(alpha_id: str) -> pd.DataFrame:    """    获取指定 alpha 的 PnL数据，并返回一个包含日期和 PnL 的 DataFrame。    此函数通过调用 WorldQuant Brain API 获取指定 alpha 的 PnL 数据，    并将其转换为 pandas DataFrame 格式，方便后续数据处理。    Args:        alpha_id (str): Alpha 的唯一标识符。    Returns:        pd.DataFrame: 包含日期和对应 PnL 数据的 DataFrame，列名为 'Date' 和 alpha_id。    """    pnl = wait_get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl").json()    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])    df = df.rename(columns={'date':'Date', 'pnl':alpha_id})    df = df[['Date', alpha_id]]    return dfdef get_alpha_pnls(    alphas,# list[dict],    alpha_pnls, #Optional[pd.DataFrame] = None,    alpha_ids,# Optional[dict[str, list]] = None) :  # Tuple[dict[str, list], pd.DataFrame]:    """    获取 alpha 的 PnL 数据，并按区域分类 alpha 的 ID。    Args:        alphas (list[dict]): 包含 alpha 信息的列表，每个元素是一个字典，包含 alpha 的 ID 和设置等信息。        alpha_pnls (Optional[pd.DataFrame], 可选): 已有的 alpha PnL 数据，默认为空的 DataFrame。        alpha_ids (Optional[dict[str, list]], 可选): 按区域分类的 alpha ID 字典，默认为空字典。    Returns:        Tuple[dict[str, list], pd.DataFrame]:            - 按区域分类的 alpha ID 字典。            - 包含所有 alpha 的 PnL 数据的 DataFrame。    """    if alpha_ids is None:        alpha_ids = defaultdict(list)    # if alpha_ids is None:    #     alpha_ids = defaultdict(list)    if alpha_pnls is None:        alpha_pnls = pd.DataFrame()    new_alphas = [item for item in alphas if item['id'] not in alpha_pnls.columns]    if not new_alphas:        return alpha_ids, alpha_pnls    for item_alpha in new_alphas:        alpha_ids[item_alpha['settings']['region']].append(item_alpha['id'])    fetch_pnl_func = lambda alpha_id: _get_alpha_pnl(alpha_id).set_index('Date')    with ThreadPoolExecutor(max_workers=10) as executor:        results = executor.map(fetch_pnl_func, [item['id'] for item in new_alphas])    alpha_pnls = pd.concat([alpha_pnls] + list(results), axis=1)    alpha_pnls.sort_index(inplace=True)    return alpha_ids, alpha_pnlsdef get_os_alphas(limit: int = 100, get_first: bool = False) -> List[Dict]:    """    获取OS阶段的alpha列表。    此函数通过调用WorldQuant Brain API获取用户的alpha列表，支持分页获取，并可以选择只获取第一个结果。    Args:        limit (int, optional): 每次请求获取的alpha数量限制。默认为100。        get_first (bool, optional): 是否只获取第一次请求的alpha结果。如果为True，则只请求一次。默认为False。    Returns:        List[Dict]: 包含alpha信息的字典列表，每个字典表示一个alpha。    """    fetched_alphas = []    offset = 0    retries = 0    total_alphas = 100    while len(fetched_alphas) < total_alphas:        print(f"Fetching alphas from offset {offset} to {offset + limit}")        url = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}&order=-dateSubmitted"        res = wait_get(url).json()        if offset == 0:            total_alphas = res['count']        alphas = res["results"]        fetched_alphas.extend(alphas)        if len(alphas) < limit:            break        offset += limit        if get_first:            break    return fetched_alphas[:total_alphas]def calc_self_corr(    alpha_id,    os_alpha_rets,#pd.DataFrame | None = None,    os_alpha_ids, # dict[str, str] | None = None,    alpha_result , #dict | None = None,    return_alpha_pnls,    alpha_pnls #pd.DataFrame | None = None) :    """    计算指定 alpha 与其他 alpha 的最大自相关性。# return float | [] : #float | tuple[float, pd.DataFrame]:    Args:        alpha_id (str): 目标 alpha 的唯一标识符。        os_alpha_rets (pd.DataFrame | None, optional): 其他 alpha 的收益率数据，默认为 None。        os_alpha_ids (dict[str, str] | None, optional): 其他 alpha 的标识符映射，默认为 None。        alpha_result (dict | None, optional): 目标 alpha 的详细信息，默认为 None。        return_alpha_pnls (bool, optional): 是否返回 alpha 的 PnL 数据，默认为 False。        alpha_pnls (pd.DataFrame | None, optional): 目标 alpha 的 PnL 数据，默认为 None。    Returns:        float | tuple[float, pd.DataFrame]: 如果 `return_alpha_pnls` 为 False，返回最大自相关性值；            如果 `return_alpha_pnls` 为 True，返回包含最大自相关性值和 alpha PnL 数据的元组。    """    if alpha_result is None:        alpha_result = wait_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()    if alpha_pnls is not None:        if len(alpha_pnls) == 0:            alpha_pnls = None    if alpha_pnls is None:        # print(alpha_result)        _, alpha_pnls =get_alpha_pnls(alphas=[alpha_result], alpha_pnls=alpha_pnls, alpha_ids=None)        # _, alpha_pnls = get_alpha_pnls([alpha_result],alpha_pnls,alpha_id)        alpha_pnls = alpha_pnls[alpha_id]    alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)    alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index)>pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)]    res_ = os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets).sort_values(ascending=False).round(4)    self_corr = os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets).max()    if len(res_) > 0:        first_index = res_.index[0]        first_value = self_corr        print(f"{first_index}: {first_value}")    else:        first_index = None        first_value = 0    if np.isnan(self_corr):        self_corr = 0        first_value = 0    return first_index,first_valuedef download_data(sess,flag_increment=True):    """    下载数据并保存到指定路径。    此函数会检查数据是否已经存在，如果不存在，则从 API 下载数据并保存到指定路径。    Args:        flag_increment (bool): 是否使用增量下载，默认为 True。    """    if flag_increment:        try:            os_alpha_ids = load_obj(str(cfg.data_path / 'os_alpha_ids'))            os_alpha_pnls = load_obj(str(cfg.data_path / 'os_alpha_pnls'))            ppac_alpha_ids = load_obj(str(cfg.data_path / 'ppac_alpha_ids'))            exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]        except Exception as e:            logging.error(f"Failed to load existing data: {e}")            os_alpha_ids = None            os_alpha_pnls = None            exist_alpha = []            ppac_alpha_ids = []    else:        os_alpha_ids = None        os_alpha_pnls = None        exist_alpha = []        ppac_alpha_ids = []    if os_alpha_ids is None:        alphas = get_os_alphas(limit=100, get_first=False)    else:        alphas = get_os_alphas(limit=30, get_first=True)    alphas = [item for item in alphas if item['id'] not in exist_alpha]    ppac_alpha_ids += [item['id'] for item in alphas for item_match in item['classifications'] if item_match['name'] == 'Power Pool Alpha']    os_alpha_ids, os_alpha_pnls = get_alpha_pnls(alphas, alpha_pnls=os_alpha_pnls, alpha_ids=os_alpha_ids)    save_obj(os_alpha_ids, str(cfg.data_path / 'os_alpha_ids'))    save_obj(os_alpha_pnls, str(cfg.data_path / 'os_alpha_pnls'))    save_obj(ppac_alpha_ids, str(cfg.data_path / 'ppac_alpha_ids'))    print(f'新下载的alpha数量: {len(alphas)}, 目前总共alpha数量: {os_alpha_pnls.shape[1]}')import sysdef load_data(tag=None):    """    加载数据。    此函数会检查数据是否已经存在，如果不存在，则从 API 下载数据并保存到指定路径。    Args:        tag (str): 数据标记，默认为 None。    """    os_alpha_ids = load_obj(str(cfg.data_path / 'os_alpha_ids'))    os_alpha_pnls = load_obj(str(cfg.data_path / 'os_alpha_pnls'))    ppac_alpha_ids = load_obj(str(cfg.data_path / 'ppac_alpha_ids'))    if tag=='PPAC':        for item in os_alpha_ids:            os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha in ppac_alpha_ids]    elif tag=='SelfCorr':        for item in os_alpha_ids:            os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha not in ppac_alpha_ids]    else:        os_alpha_ids = os_alpha_ids    exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]    os_alpha_pnls = os_alpha_pnls[exist_alpha]    os_alpha_rets = os_alpha_pnls - os_alpha_pnls.ffill().shift(1)    os_alpha_rets = os_alpha_rets[pd.to_datetime(os_alpha_rets.index)>pd.to_datetime(os_alpha_rets.index).max() - pd.DateOffset(years=4)]    return os_alpha_ids, os_alpha_retsdef generate_time_intervals(interval_hours,start_hour='00', end_hour='23'):    """    生成指定间隔的时间段元组。    :param start_hour: 开始小时，默认为 '00'    :param end_hour: 结束小时，默认为 '23'    :param interval_hours: 时间间隔，默认为 3 小时    :return: 返回时间段元组列表    """    start_time = datetime.strptime(f"{start_hour}:00:00", "%H:%M:%S")    end_time = datetime.strptime(f"{end_hour}:59:59", "%H:%M:%S")    intervals = []    current_start = start_time    while current_start < end_time:        next_end = current_start + timedelta(hours=interval_hours)        # 如果下一个结束时间超过了最终的结束时间，则调整为最终的结束时间        if next_end > end_time:            next_end = end_time        # 格式化时间为字符串        start_str = current_start.strftime("%H:%M:%S")        end_str = next_end.strftime("%H:%M:%S")        # 添加到结果列表中        intervals.append((start_str, end_str))        # 更新当前开始时间为下一个时间段的开始        current_start = next_end    return intervalsdef append_to_file( filename, data,flag=None):    """    将给定的数据追加到指定的文本文件中，每条数据单独占一行。    :param filename: 文本文件的路径    :param data: 要追加的数据（可以是字符串或列表）    """    # 如果 data 是一个列表，则遍历每个元素并逐行写入    if isinstance(data, list):        with open(filename, 'a', encoding='utf-8') as file:            for item in data:                file.write(f"{item}\n")    else:        # 如果 data 不是列表，则直接写入        with open(filename, 'a', encoding='utf-8') as file:            if flag:                file.write(f"{datetime.now()} {data}\n")            else:                file.write(f"{data}\n")def set_alpha_properties( alpha_id, name: str = None, color: str = None,selection_desc: str = "None",  combo_desc: str = "None",tags: list = [] ):    """    Function changes alpha's description parameters    """    global s    params = {        "color": color,        "name": name,        "tags": [],        "category": None,        "regular": {"description": description},        "combo": {"description": combo_desc},        "selection": {"description": selection_desc},    }    try:        response = s.patch("https://api.worldquantbrain.com/alphas/" + alpha_id, json=params)        print(f"set alpha mess: {response}|{response.status_code}|{response.text}")    except Exception as e:        print(f"set alpha name err {e}" )def get_two_number(number):    # 将浮点数转换为字符串，保留足够的精度以避免舍入误差    number_str = f'{number:.10f}'    # 分割整数和小数部分    integer_part, fractional_part = number_str.split('.')    # 取小数点后两位数字    return fractional_part[:2]def format_value(value, value_type):    """根据类型格式化值"""    if value_type == 'percent':        return f"{value * 100:.2f}%"    elif value_type == 'permyriad':        return f"{value * 10000:.2f}‱"    else:        return valuedef flatten_json(y):    """Flatten a nested JSON object into a single-level dictionary."""    out = {}    def flatten(x, name=''):        if isinstance(x, dict):            for a in x:                flatten(x[a], name + a + '_')        elif isinstance(x, list):            i = 0            for a in x:                flatten(a, name + str(i) + '_')                i += 1        else:            out[name[:-1]] = x    flatten(y)    return outdef write_to_csv(file_path, data, first_time=False):    """Write flattened JSON data to a CSV file, appending if the file exists."""    # Check if file exists and determine if we need to write headers    file_exists = os.path.isfile(file_path)    with open(file_path, mode='a', newline='', encoding='utf-8') as f:        # Flatten each dictionary in the list and collect all unique keys        flat_data_list = [flatten_json(item) for item in data]        all_keys = set().union(*[flat_data.keys() for flat_data in flat_data_list])        writer = csv.DictWriter(f, fieldnames=sorted(all_keys))        if first_time or not file_exists:            writer.writeheader()        for flat_data in flat_data_list:            writer.writerow({key: flat_data.get(key, '') for key in sorted(all_keys)})def get_alphanew(s, url):    alpha_json = []    try:        response =s.get(url, timeout=20)        response.raise_for_status()  # 确保请求成功        alpha_list = response.json().get("results", [])        print(f'alpha_list :{len(alpha_list)} ,{url}')        for alpha in alpha_list:            alpha_id = alpha["id"]            checks = alpha["is"]["checks"]            checks_df = pd.DataFrame(checks)            name = alpha['name']            sharpe=alpha['is']["sharpe"]            fitness=alpha['is']["fitness"]            select=alpha["selection"]["code"]            if "POWER_POOL" not in select:                print("not POWER_POOL,switch ,{alpha_id}")            if  name != None and ('PROD_0.7' in name or 'PROD_0.8' in name or 'PROD_0.69' in name or 'PROD_0.68' in name or 'PROD_0.67' in name or 'PROD_0.66' in name or "SELF_CORR" in name) :                print(f"switch {name}, {alpha_id}, fit {fitness}")                continue            if not any(checks_df["result"] == "FAIL") and sharpe >=1.4 and fitness >=5:                alpha_json.append(alpha)    except requests.exceptions.RequestException as e:        print(f"An error occurred: {e}")        exc_type, exc_value, exc_traceback = sys.exc_info()        print(f"Exception type: {exc_type}, Exception value: {exc_value}")    return alpha_jsondef get_alphas(s,dates,date_offset,interval_hours,sharpe,fitness,save_alpha_infos_file,region=None,universe=None,color=None,name=None,tag=None,neutralization=None,margin=None,returns=None):    baseurl = "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=0&status=UNSUBMITTED%1FIS_FAIL"    urls = []    for start, end in dates:        time_intervals = generate_time_intervals(interval_hours=12)        for start_h,end_h in time_intervals:            startstr = f"&dateCreated%3E={start}T{start_h}{date_offset}"            endstr = f"&dateCreated%3C{start}T{end_h}{date_offset}"            datestr = f"{startstr}{endstr}"            urls.append(f"{baseurl}{datestr}")    for i in range(len(urls)):        if color:            urls[i] = f"{urls[i]}&color={color}"        if tag:            urls[i] = f"{urls[i]}&tag%3D{tag}"        if name:            urls[i] = f"{urls[i]}&name~{name}"        if region:            urls[i] = f"{urls[i]}&settings.region={region}"        if universe:            urls[i] = f"{urls[i]}&settings.universe={universe}"        if neutralization:            urls[i] = f"{urls[i]}&settings.neutralization={neutralization}"        if fitness:  # &is.fitness%3E2            urls[i] = f"{urls[i]}&is.fitness%3E={str(fitness)}"        if sharpe:  # &is.fitness%3E2            urls[i] = f"{urls[i]}&is.sharpe%3E={str(sharpe)}"        if margin:  # &is.fitness%3E2            urls[i] = f"{urls[i]}&is.margin%3E={str(margin)}"        if returns:  # &is.fitness%3E2            urls[i] = f"{urls[i]}&is.returns%3E={str(returns)}"    new_urls = []  # [(url,count)]    for i in range(len(urls)):        # 指定 super alpha        url = f"{urls[i]}&type=SUPER&order=-dateCreated&hidden=false"        count = s.get(url).json()['count']        new_urls.append((url, count))        print(f"get ok count :{count} url: {url}")        print("sleep 5")        time.sleep(5)    alphas = []    first_time = True    for url, count in new_urls:        for i in range(0, count, 100):            url_ = url.replace("offset=0", f"offset={i}")            alpha_infos = get_alphanew(s, url_)            if len(alpha_infos)>0:                alphas.extend(alpha_infos)            # for idx, json_data in enumerate(alpha_infos):            write_to_csv(save_alpha_infos_file, alpha_infos, first_time=first_time)            first_time = False    return alphasdef get_alphaid_from_file(filename):    # 定义文件名    alpha_ids = []    count = 1    try:        # 打开并读取文件        with open(filename, 'r', encoding='utf-8') as file:            # 按行读取文件内容            for line in file:                # if count < start or count > end:                #     count +=1                #     continue                # 去除行末的换行符，并根据逗号分割字符串                fields = line.strip().split(',')                # 获取并打印第一个字段                if len(fields) > 0:                    print(fields[0])                    alpha_ids.append(fields[0])        return alpha_ids    except FileNotFoundError:        print(f"文件 {filename} 未找到，请检查文件路径是否正确。")    except Exception as e:        print(f"读取文件时发生错误: {e}")def perform_task_with_retry(task, alpha_info,first_time,rounded_f,ppac_value,retries=3, delay_seconds=300):    """    尝试执行给定的任务，如果失败则重试指定次数。    :param task: 要执行的任务函数    :param retries: 重试次数    :param delay_seconds: 每次重试之间的延迟秒数    """    attempt = 0    while attempt < retries:        try:            result= task(alpha_info,first_time,rounded_f,ppac_value)            return result        except requests.exceptions.ConnectionError as e:            attempt += 1            print(f"尝试 {attempt} 失败: {e}")            if attempt < retries:                print(f"等待 {delay_seconds} 秒后重试...")                time.sleep(delay_seconds)            else:                print("已达到最大重试次数，程序终止。")                raise        except Exception as e:            # 如果是其他类型的异常，则直接抛出            print(f"发生了一个非连接错误的异常: {e}")            raisedef before_and_after_score(alpha_id):    add_score = 0    while True:        try:            res=my_get(f"https://api.worldquantbrain.com/competitions/PPAC2025/alphas/{alpha_id}/before-and-after-performance",timeout=30)            # print(res.content)            if res == None:                continue            if res.text == '' :                time.sleep(5)                continue            if res.status_code == 200:                res = res.json()                stats=res['stats']                before=stats['before']                after=stats['after']                score=res["score"]                add_score=score["after"]-score["before"]                break        except Exception as e:            print(f"get performance error ,sleep 10")            time.sleep(5)    return add_scoredef before_and_after(alpha_id):    while True:           # res=s.get(f"https://api.worldquantbrain.com/competitions/PPAC2025/alphas/{alpha_id}/before-and-after-performance")        try:            res = my_get(f"https://api.worldquantbrain.com/users/self/alphas/{alpha_id}/before-and-after-performance",timeout=15)            # print(res.content)            if res.text == '':                time.sleep(5)                continue            if res.status_code == 200:                res = res.json()                stats=res['stats']                before=stats['before']                after=stats['after']                sharpe=round(after['sharpe']-before['sharpe'],6)                fitness=round(after['fitness']-before['fitness'],6)                margin=round(after['margin']-before['margin'],6)                returns=round(after['returns']-before['returns'],6)                turnover=round(after['turnover']-before['turnover'],6)                drawdown=round(after['drawdown']-before['drawdown'],6)                pnl=after['pnl']-before['pnl']                # print(res.keys())                # score = res["score"]                # add_score = score["after"] - score["before"]                # print(add_score)                tmp={'id':alpha_id,"sharpe":sharpe,                               "fitness":fitness                               ,"margin":margin,                               "returns":returns,                               "turnover":turnover,                               "drawdown":drawdown,                               "pnl":pnl}                break        except Exception as e:            print(f"online before after failed sleep 5")            time.sleep(5)    return tmpdef write_json_array(file_path, data):    """将整个JSON数组写入指定文件"""    with open(file_path, 'w') as file:        json.dump(data, file, indent=4)def read_json_array(file_path):    """从文件中读取整个JSON数组"""    try:        with open(file_path, 'r') as file:            return json.load(file)    except FileNotFoundError:        print(f"Error: File '{file_path}' not found.")        return None    except json.JSONDecodeError as e:        print(f"Error: Failed to parse JSON from '{file_path}': {e}")        return None#config_file = 'config.json'#config = load_config(config_file)# 认证信息：#user=config["user"]#passwd=config["password"]save_alpha_infos_file="save_not_failed_apha_info_file"check_alpha_not_fail="save_check_alpha_not_fail"check_alpha_fail="save_check_alpha_fail"def generate_date_ranges_day(start_date_str, end_date_str):    """    生成从 start_date 到 end_date 的每日时间段列表：    每个元素是 (当前天, 下一天) 的字符串元组，格式为 "YYYY-MM-DD"    参数:        start_date_str (str): 起始日期字符串，格式为 "YYYY-MM-DD"        end_date_str (str): 结束日期字符串，格式为 "YYYY-MM-DD"    返回:        List[Tuple[str, str]]: 时间段列表    """    date_format = "%Y-%m-%d"    start_date = datetime.strptime(start_date_str, date_format)    end_date = datetime.strptime(end_date_str, date_format)    result = []    current = start_date    while current < end_date:        next_day = current + timedelta(days=1)        result.append((current.strftime(date_format), next_day.strftime(date_format)))        current = next_day    reversed_lst = result[::-1]    print(reversed_lst)    return reversed_lstdef delete_file(file_path):    """    删除指定路径的文件    参数:        file_path (str): 要删除的文件路径    返回:        bool: 删除成功返回True，失败返回False    """    try:        if os.path.exists(file_path):            os.remove(file_path)            print(f"文件 {file_path} 已成功删除")            return True        else:            print(f"文件 {file_path} 不存在")            return False    except Exception as e:        print(f"删除文件 {file_path} 时出错: {e}")        return Falseif __name__ == "__main__":    download_data(s,flag_increment=True)    # 需要根据比赛当前周的时间范围修改，开始时间是当前主题周的开始时间，结束时间是美东时间 +1 day填    dates=generate_date_ranges_day('2025-06-17','2025-06-21')    date_offset="-04:00"    # 这2个参数随便填的，实际上没有用,具体需要过滤的条件 ，可查看 get_alphanew 函数 进行修改    sharpe=1.4    fitness=0.8    interval_hours=12    pool_exp_save_file="alpha_file"    uniq_alphas=[]    if os.path.exists(pool_exp_save_file):        # 文件存在，读取配置        alpha_infos=read_json_array(pool_exp_save_file)        print(f"pool len: {len(alpha_infos)}")        # 如果需要临时中断，先check其他的，可以停止进程，下次继续check时，从日志begin check的最后1个id开始，修改start，继续check剩下的        start=0    else:        exist_1=read_json_array("alpha_file_bak")        alpha_infos = get_alphas(s=s,dates=dates,date_offset=date_offset,interval_hours=interval_hours,sharpe=sharpe,fitness=fitness,save_alpha_infos_file=save_alpha_infos_file)        start=0        for item in alpha_infos:            if item not in uniq_alphas :                uniq_alphas.append(item)        alpha_infos = uniq_alphas        write_json_array(pool_exp_save_file,alpha_infos)    description="""Idea: a stock's implied volatility is significantly higher than its historical averageRationale for data used: xxxxxxxxx and xxxxxxxxxxxxxxxxxxxxxRationale for operators used: ts_backfill  winsoriz aaaaa"""    count=0    check_time = 1    print(len(alpha_infos))    os_alpha_ids, os_alpha_rets = load_data()    alpha_infos = alpha_infos[start:]    append_to_file("check.log",f"==================================================",True)    for i  in range(0,len(alpha_infos)):         alpha_info=alpha_infos[i]         alpha_id=alpha_info["id"]         print(f"begin check id :{i+start}, {alpha_id}")         append_to_file("check.log",f"begin check id :{i+start}, {alpha_id} ",True)         date_create=alpha_info["dateCreated"]         fitness = alpha_info['is']['fitness']         sharpe = alpha_info['is']['sharpe']         turnover = alpha_info['is']['turnover']         margin = alpha_info['is']['margin']         drawdown = alpha_info['is']['drawdown']         returns = alpha_info['is']['returns']         region = alpha_info['settings']['region']         checks=alpha_info["is"]["checks"]         LOW_2Y_SHARPE=0         for item in checks:             if item["name"] == LOW_2Y_SHARPE:                 LOW_2Y_SHARPE=item["value"]         corr_id,corr_value=calc_self_corr( alpha_id, os_alpha_rets,  os_alpha_ids,None,True,None)         print(corr_value)         f = float(corr_value)         rounded_f = round(f, 4)         if   rounded_f >=0.5: # 按需设置             print(f"self corr more than 0.5,and self > 0.7 ;switch {alpha_id};  self:{rounded_f}")             set_alpha_properties(alpha_id=alpha_id, name=f"SELF_CORR_{rounded_f}", color="BLUE")             continue         if count==0:            first_time=True         else:            first_time=False         num4_num5=0         num5_num6=0         num6_num7=0         while True:            response=my_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod")            if response != None:                try:                    res=response.json()                    prod=res["max"]                    for list_ in res["records"]:                        if list_[0] == 0.4 and list_[1] == 0.5:                            num4_num5=list_[2]                        if list_[0] == 0.5 and list_[1] == 0.6:                            num5_num6=list_[2]                        if list_[0] == 0.6 and list_[1] == 0.7:                            num6_num7=list_[2]                    break                except Exception as e:                    print(f"noe,try again")            sleep(10)         if  fitness > 5 and prod < 0.5 and sharpe >5 and LOW_2Y_SHARPE >=5:             print(f"begin submit alpha: {alpha_id}")             append_to_file("submit.log",f"begin submit alpha: {alpha_id}",True)             #submit_alpha(s,alpha_id)             exit(0)         com_des=alpha_info["combo"]["description"]         select_des=alpha_info["selection"]["description"]         #if (com_des == None or com_des == "null") and  (select_des == None or select_des == "null" ):         print(com_des,select_des)         print(f"comdesc {com_des}, select_des: {select_des}")         set_alpha_properties(alpha_id,f"PROD_{str(prod)}","RED")         a=json.dumps([alpha_id,f"self:{rounded_f}",f"prod:{prod}",{"num4_num5":num4_num5,"num5_num6":num5_num6,"num6_num_7":num6_num7,"fitness":fitness,"sharpe":sharpe,"LOW_2Y_SHARPE":LOW_2Y_SHARPE,"turnover":turnover,"drowdown":drawdown,"returns":returns,"region":region}])         append_to_file("res.txt",a,True)         count +=1    print(f"finish check")    file_to_delete = "alpha_file"    delete_file(file_to_delete)
```

---

### 评论 #8 (作者: JR23144, 时间: 1年前)

感谢 橙子姐 的无私分享，我的SA 还在直接去服务器请求 生产相关性，有了大佬的代码后，提供了非常好的思路，先去检查本地相关性，再去服务器校验生产相关性 厉害呀

===============VF 1.0 ================================================

---

### 评论 #9 (作者: AL13375, 时间: 1年前)

原来是橘子姐的大作！！！太强了！！！能连续做出prod<0.5的sa的橘子姐果然是有秘密武器的，膜拜！！！

本来我还想一步步看完的，但是后面才发现。。。好长的代码！

橘子姐的代码能力还是太强了！

大致看了下，橘子姐的思路很好，给了我一些启发。

原本我也想自动跑sa的，但是一直想着手搓可以多学点组sa的方法，所以代码跑sa的事情一直被我搁置了，而目前似乎手搓的效果和意义已经不大了，可以考虑用代码跑了。最后祝橘子姐的vf和genius level芝麻开花节节高！

====================VF 1.0====================

---

### 评论 #10 (作者: MG88592, 时间: 1年前)

感谢橘子姐的分享，十分有用，平台回测sa 检查corrlation都耗费许久的时间，这些时间都属于平白无故的浪费。
借助于橘子姐这个代码可以快速的寻找能赚更多钱的sa，让赚钱所花的时间更短。
============================================================

===========================================================

---

### 评论 #11 (作者: PW58059, 时间: 1年前)

这篇分享简直是 Super Alpha 调整的 “效率加速器”！手动一个个查 prod 相关性的痛苦谁懂？橘子老师把之前ra中用了很多的本地自相关性筛选复刻到了SA上，跳过自相关超 5 的，再精准定位 prod 在 0.4-0.6 区间且数量较少的 SA，直接把试错成本降到最低。

代码里藏着太多细节：批量获取 SA 列表、自动记录各区间相关性数据、甚至带重试机制的 API 调用，把重复劳动全自动化了，这波操作直接把调整效率拉满。

=======================================================================
那些凌晨三点还亮着的屏幕光，终会化作晋级榜单上闪耀...
=======================================================================

---

### 评论 #12 (作者: SD17531, 时间: 1年前)

橘子姐YYDS 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
希望有一天我能有你一样的实力

---

### 评论 #13 (作者: ML42552, 时间: 1年前)

感谢橙子姐的无私奉献，今天终于有幸看上了橙子姐的完整代码，太美了！

斯帕啦西！！！

向橙子姐学习！！！！

期望橙子姐能一直高vf！！！！

可以产出更多的帖子供小弟我学习学习！

----------------------------------------------------------

共好！

---

### 评论 #14 (作者: HJ88260, 时间: 8个月前)

太牛了！这个思路简直是我们SA调参党的福音！之前一直盲打，现在终于有科学方法了——靠自相关筛一波，再盯着0.4-0.6区间的prod分布去重点突破，效率直接拉满！而且文末还贴心提醒防过拟合，真实用！已收藏，今晚就照着代码跑起来，希望也能挖到几个低prod高fit的宝藏SA！感谢大佬分享！

---

### 评论 #15 (作者: JL25609, 时间: 8个月前)

太牛了！这个思路简直是我们SA调参党的福音！之前一直盲打，现在终于有科学方法了。

俺非常需要。已收藏

---

### 评论 #16 (作者: CL86067, 时间: 7个月前)

感谢橘子姐的分享，太有帮助了，最近还全靠api请求生产相关性，但是真的慢，刷到橘子姐的这个帖子真的及时雨，原来还可以用本地自相关性来提高效率，这下感觉不怕check慢了。

再次感谢橘子姐的分享，祝一直GM,VF常驻0.98+

---

