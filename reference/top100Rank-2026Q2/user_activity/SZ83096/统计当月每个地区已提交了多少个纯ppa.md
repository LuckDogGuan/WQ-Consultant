# 统计当月每个地区已提交了多少个纯ppa

- **链接**: 统计当月每个地区已提交了多少个纯ppa.md
- **作者**: SZ83096
- **发布时间/热度**: 8个月前, 得票: 24

## 帖子正文

平台对四大地区提交的纯ppa 限制每个月10个；小地区总共10个；区分D0，D1；

由于我没提交D0 alpha,所以代码没区分D0，D1，默认统计的都是D1的。

```
import requestsimport timefrom typing import Dict, List, Tuplefrom requests.adapters import HTTPAdapterfrom urllib3.util.retry import Retryimport jsonimport sysdef load_config(file_path):    """从指定路径加载JSON配置文件，并处理可能的异常"""    try:        with open(file_path, 'r') as file:            config = json.load(file)        return config    except FileNotFoundError:        print(f"Error: Config file '{file_path}' not found.")        sys.exit(1)    except json.JSONDecodeError as e:        print(f"Error: Failed to parse JSON from '{file_path}': {e}")        sys.exit(1)config_file = 'config.json'config = load_config(config_file)user = config["user"]passwd = config["password"]def login():    username = user    password = passwd    retry_strategy = Retry(        total=3,  # 总共重试次数        backoff_factor=1,  # 每次重试之间的延迟时间（秒）        status_forcelist=[500, 502, 503, 504]  # 遇到这些HTTP状态码时重试    )    adapter = HTTPAdapter(max_retries=retry_strategy)    s = requests.Session()    s.mount("https://", adapter)    s.mount("http://", adapter)    s.auth = (username, password)    response = s.post('https://api.worldquantbrain.com/authentication')    print(response.content)    print("ok")    return ss=login()# get submit alphadef write_json_array(file_path, data):    """将整个JSON数组写入指定文件"""    with open(file_path, 'w') as file:        json.dump(data, file, indent=4)def read_json_array(file_path):    """从文件中读取整个JSON数组"""    try:        with open(file_path, 'r') as file:            return json.load(file)    except FileNotFoundError:        print(f"Error: File '{file_path}' not found.")        return None    except json.JSONDecodeError as e:        print(f"Error: Failed to parse JSON from '{file_path}': {e}")        return Nonedef wait_get(url: str, max_retries: int = 10):    """    发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。    此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。    Args:        url (str): 目标 URL。        max_retries (int, optional): 最大重试次数，默认为 10。    Returns:        Response: 请求的响应对象。    """    retries = 0    while retries < max_retries:        while True:            simulation_progress = s.get(url)            if simulation_progress.headers.get("Retry-After", 0) == 0:                break            time.sleep(float(simulation_progress.headers["Retry-After"]))        if simulation_progress.status_code < 400:            break        else:            time.sleep(2 ** retries)            retries += 1    return simulation_progressdef get_os_alphas(start,end,total_alphas,limit: int = 100, get_first: bool = False,region=None) -> List[Dict]:    """    获取OS阶段的alpha列表。    此函数通过调用WorldQuant Brain API获取用户的alpha列表，支持分页获取，并可以选择只获取第一个结果。    Args:        limit (int, optional): 每次请求获取的alpha数量限制。默认为100。        get_first (bool, optional): 是否只获取第一次请求的alpha结果。如果为True，则只请求一次。默认为False。    Returns:        List[Dict]: 包含alpha信息的字典列表，每个字典表示一个alpha。    """    fetched_alphas = []    offset = 0    retries = 0    # total_alphas = 100    while len(fetched_alphas) < total_alphas:        print(f"Fetching alphas from offset {offset} to {offset + limit}")        url_ = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&type=REGULAR&limit={limit}&offset={offset}&type=REGULAR"        if region !=None:            url_=f"{url_}&settings.region={region}"        url = f"{url_}&dateSubmitted%3E{start}T04:00:00.000Z&dateSubmitted%3C{end}T04:00:00.000Z&order=-dateSubmitted"        print(url)        res = wait_get(url).json()        if offset == 0:            total_alphas = res['count']        alphas = res["results"]        fetched_alphas.extend(alphas)        if len(alphas) < limit:            break        offset += limit        if get_first:            break    return fetched_alphas#def is_prune_ppa(pyramids,classifications):    ppa_flag=False    effective = pyramids['effective']    for item in classifications:        if item['id'] == "POWER_POOL:POWER_POOL_ELIGIBLE":            ppa_flag= True            break    if  effective == 2 and  ppa_flag:        return True    else:        return False# 设置获取的alpha 时间范围start='2025-10-01'end='2025-10-09'submit_alphas = get_os_alphas(start=start,end=end,total_alphas=500)# 设置要统计的月份prune_ppa_time = '2025-10'write_json_array(f"submit_alphas_{start}_{end}.json", submit_alphas)# 这里根据自己有提交alpha的月份 增删地区；region_alpha ={    'USA':{'prune_ppa_num':0, "alphas":[]},    'EUR':{'prune_ppa_num':0, "alphas":[]},    "GLB":{'prune_ppa_num':0, "alphas":[]},    "ASI":{'prune_ppa_num':0, "alphas":[]},    "AMR":{'prune_ppa_num':0, "alphas":[]},}region_alpha_2 ={    'USA':{'prune_ppa_num':0},    'EUR':{'prune_ppa_num':0},    "GLB":{'prune_ppa_num':0},    "ASI":{'prune_ppa_num':0},    "AMR":{'prune_ppa_num':0},}for alpha in submit_alphas:    region=alpha['settings']['region']    pyramids=alpha['pyramidThemes']    dateSubmitted=alpha['dateSubmitted']    classifications=alpha['classifications']    if  is_prune_ppa(pyramids, classifications) and prune_ppa_time in dateSubmitted:        region_alpha[region]['prune_ppa_num'] +=1        region_alpha[region]['alphas'].append(alpha)        region_alpha_2[region]['prune_ppa_num'] += 1write_json_array(f"prune_ppa_detail_{prune_ppa_time}.json", region_alpha)write_json_array(f'prune_ppa_summary_{prune_ppa_time}.json',region_alpha_2)
```

结果如下：

![图片](images/img_29a8d09efa.png)

---

## 讨论与评论 (3)

### 评论 #1 (作者: BW28426, 时间: 8个月前)

很久没提纯PPAC Alpha了，有些好奇如果我对应排行榜提交快满了，我把PPAC标签移除，是计数还是不计数呢?
不知道有人验证过没，如果不计数脚本应该还得判断一下是否打上了PPAC标签。
==================================================================

定期调整提交策略

定期检查提交对SA的影响

需要更好的分散性

制定符合自己的提交计划
=========================尽量提高质量，保证提交数量===================

---

### 评论 #2 (作者: SZ83096, 时间: 8个月前)

修正下纯ppa计算的函数：

```
def is_prune_ppa(pyramids,classifications):    ppa_flag=False    ra_flag=False    effective = pyramids['effective']    for item in classifications:        if item['id'] == "POWER_POOL:POWER_POOL_ELIGIBLE":            ppa_flag= True        if item['id'] == 'REGULAR:REGULAR':            ra_flag=True    if  effective == 2 and  ppa_flag and not ra_flag:        return True    else:        return False
```

---

### 评论 #3 (作者: WF37935, 时间: 8个月前)

有效金字塔为2是排除atom吗？直接判断classifications中有ppa，没有ra和atom不行吗

---

