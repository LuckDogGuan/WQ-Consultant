# 测测你最近2周提交的ra,ppa prod平均值

- **链接**: 测测你最近2周提交的rappa prod平均值.md
- **作者**: SZ83096
- **发布时间/热度**: 9个月前, 得票: 21

## 帖子正文

代码如下：

```
from requests.adapters import HTTPAdapterfrom urllib3.util.retry import Retryimport timeimport requestsimport jsonfrom typing import Dict, Listimport sysdef load_config(file_path):    """从指定路径加载JSON配置文件，并处理可能的异常"""    try:        with open(file_path, 'r') as file:            config = json.load(file)        return config    except FileNotFoundError:        print(f"Error: Config file '{file_path}' not found.")        sys.exit(1)    except json.JSONDecodeError as e:        print(f"Error: Failed to parse JSON from '{file_path}': {e}")        sys.exit(1)config_file = 'config.json'config = load_config(config_file)user = config["user"]passwd = config["password"]def login():    username = user    password = passwd    retry_strategy = Retry(        total=3,  # 总共重试次数        backoff_factor=1,  # 每次重试之间的延迟时间（秒）        status_forcelist=[500, 502, 503, 504]  # 遇到这些HTTP状态码时重试    )    adapter = HTTPAdapter(max_retries=retry_strategy)    s = requests.Session()    s.mount("https://", adapter)    s.mount("http://", adapter)    s.auth = (username, password)    response = s.post('https://api.worldquantbrain.com/authentication')    print(response.content)    print("ok")    return ss=login()def wait_get(url: str, max_retries: int = 10):    """    发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。    此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。    Args:        url (str): 目标 URL。        max_retries (int, optional): 最大重试次数，默认为 10。    Returns:        Response: 请求的响应对象。    """    retries = 0    while retries < max_retries:        while True:            simulation_progress = s.get(url)            if simulation_progress.headers.get("Retry-After", 0) == 0:                break            time.sleep(float(simulation_progress.headers["Retry-After"]))        if simulation_progress.status_code < 400:            break        else:            time.sleep(2 ** retries)            retries += 1    return simulation_progressdef get_os_alphas(start,end,total_alphas,limit: int = 100, get_first: bool = False,region=None) -> List[Dict]:    """    获取OS阶段的alpha列表。    此函数通过调用WorldQuant Brain API获取用户的alpha列表，支持分页获取，并可以选择只获取第一个结果。    Args:        limit (int, optional): 每次请求获取的alpha数量限制。默认为100。        get_first (bool, optional): 是否只获取第一次请求的alpha结果。如果为True，则只请求一次。默认为False。    Returns:        List[Dict]: 包含alpha信息的字典列表，每个字典表示一个alpha。    """    fetched_alphas = []    offset = 0    while len(fetched_alphas) < total_alphas:        print(f"Fetching alphas from offset {offset} to {offset + limit}")        url_ = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&type=REGULAR&limit={limit}&offset={offset}&type=REGULAR"        if region !=None:            url_=f"{url_}&settings.region={region}"        url = f"{url_}&dateSubmitted%3E{start}T04:00:00.000Z&dateSubmitted%3C{end}T04:00:00.000Z&order=-dateSubmitted"        res = wait_get(url).json()        if offset == 0:            total_alphas = res['count']        alphas = res["results"]        fetched_alphas.extend(alphas)        if len(alphas) < limit:            break        offset += limit        if get_first:            break    return fetched_alphasstart='2025-07-01'end='2025-09-25'submit_alphas = get_os_alphas(start=start,end=end,total_alphas=500)prod_count=0alpha_count=0for alpha in submit_alphas:    prod_count +=alpha["is"]["prodCorrelation"]    alpha_count +=1avg_prod=round(prod_count/alpha_count,4)print(f"avg prod: {avg_prod}")
```

![图片](images/img_9222763418.png)

---

## 讨论与评论 (0)

