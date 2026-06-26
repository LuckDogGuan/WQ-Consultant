# <为限流做准备>一个函数获取今日回测总数

- **链接**: [Commented] 为限流做准备一个函数获取今日回测总数.md
- **作者**: XX42289
- **发布时间/热度**: 6个月前, 得票: 81

## 帖子正文

```
def query_backtest_count(s):    """使用已登录的session查询今日已回测数量"""    # 获取当前中国时间（UTC+8），减去13小时得到UTC-5时间    utc_now = datetime.utcnow()    china_time = utc_now + timedelta(hours=8)  # 中国时间（UTC+8）    target_time = china_time - timedelta(hours=13)  # 减去13小时得到UTC-5时间        # 获取日期（YYYY-MM-DD格式）    date = target_time.strftime('%Y-%m-%d')    next_date = (target_time + timedelta(days=1)).strftime('%Y-%m-%d')        # 构建API URL    api_url = (        'https://api.worldquantbrain.com/users/self/alphas?'        f'limit=100&offset=0&'        f'status=UNSUBMITTED%1FIS_FAIL&'        f'dateCreated%3E={date}T00:00:00-05:00&'        f'dateCreated%3C={next_date}T00:00:00-05:00&'        f'order=-dateCreated&hidden=false'    )        try:        response = s.get(            api_url,            headers={                'accept': 'application/json;version=3.0'            },            timeout=10        )                if not response.ok:            raise Exception(f'请求失败：{response.status_code} {response.reason}')                data = response.json()        count = data.get('count', 0)                result = {            'status': 'success',            'data': {                'count': count,                'date': date            }        }                return result            except Exception as e:        return {            'status': 'error',            'message': str(e)        }
```

函数可以直接使用。但是需要配合一个session，请自行用ace_lib或machine_lib进行登录

例如s = login()

返回的result['data']['count']就是今日回测量（最大限制10000条，仅限流后使用才准确）

实现难度不大，大家可以把这个直接放到自己的回测框架中做每日限制。

---

## 讨论与评论 (15)

### 评论 #1 (作者: LM81527, 时间: 6个月前)

你这个真及时

---

### 评论 #2 (作者: XX42289, 时间: 6个月前)

注意！这是用你今日成功回测的因子数来进行的模糊判断。

真实的当日回测量需要用simulate来获得返回，可以看一下下面这篇learn

[❗Understanding simulation limits | WorldQuant BRAIN](https://platform.worldquantbrain.com/learn/documentation/brain-api/understanding-simulation-limits)

简单来说就是你post了一个simulate后就会给你返回

simulate_response.headers["x-ratelimit-limit"],
simulate_response.headers["x-ratelimit-remaining"],
simulate_response.headers["x-ratelimit-reset"]

坏处就是会占用你一次回测的机会。

---

### 评论 #3 (作者: XX42289, 时间: 6个月前)

All successful simulations are counted, including child simulations in multi-simulations and simulations of previously existing Alphas. Duplicate Alphas that you simulate  **are not**  removed from the count.

如果你的回测重复了，那么也会占用你的一次回测机会，注意，千万不要重复回测因子！

失败的回测应该不会记录

---

### 评论 #4 (作者: WF69827, 时间: 6个月前)

已经试过了，挺好用的，感谢楼主分享。但这个脚本似乎没有考虑夏令时和冬令时的问题。于是我让AI优化了一下，以下代码开箱即用。

```
评论是不是不能把代码放进代码块，奇怪了。。。代码如下：
```

import requests
import json
from os.path import expanduser
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+ 自带，无需安装

def sign_in():
    """
    使用本地 brain_credentials.txt 登录 BRAIN，返回带认证的 session
    brain_credentials.txt 内容示例：
    ["your_username", "your_password"]
    """
    # 加载凭证
    cred_path = expanduser('brain_credentials.txt')
    with open(cred_path, 'r', encoding='utf-8') as f:
        credentials = json.load(f)

# 支持 ["user", "pwd"] 或 {"username": "...", "password": "..."}
    if isinstance(credentials, dict):
        username = credentials.get("username")
        password = credentials.get("password")
    else:
        # 默认按列表 [username, password]
        username, password = credentials

# 创建会话并设置 Basic Auth
    sess = requests.Session()
    sess.auth = HTTPBasicAuth(username, password)

# 调用认证接口
    resp = sess.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')

# 简单检查一下
    try:
        resp_json = resp.json()
    except Exception:
        resp_json = resp.text

print("登录状态码:", resp.status_code)
    print("登录返回:", resp_json)

if not resp.ok:
        raise RuntimeError("登录失败，请检查 brain_credentials.txt 或网络环境。")

return sess

def get_brain_date_window():
    """
    获取 BRAIN 使用的“今日回测窗口”的起止日期：
    - 按美东时间（America/New_York），自动处理夏令时 / 冬令时
    返回：
        date_str: 当天日期字符串 "YYYY-MM-DD"（窗口开始）
        next_date_str: 次日日期字符串 "YYYY-MM-DD"（窗口结束）
        offset_str: 当前美东时区的 UTC 偏移字符串，例如 "-05:00" 或 "-04:00"
        current_eastern: 当前美东时间（datetime 对象）
    """
    # 当前 UTC 时间
    utc_now = datetime.now(ZoneInfo("UTC"))

# 转为美东时间（自动 DST）
    eastern_now = utc_now.astimezone(ZoneInfo("America/New_York"))

# 日期窗口：从当天 00:00:00 到次日 00:00:00（美东）
    current_date = eastern_now.date()
    next_date = current_date + timedelta(days=1)

date_str = current_date.strftime("%Y-%m-%d")
    next_date_str = next_date.strftime("%Y-%m-%d")

# 构造形如 "-05:00" 的偏移字符串
    raw_offset = eastern_now.strftime("%z")  # 例如 "-0500"
    offset_str = raw_offset[:3] + ":" + raw_offset[3:]  # → "-05:00"

return date_str, next_date_str, offset_str, eastern_now

def query_backtest_count(s):
    """
    使用已登录的 session 查询【今日回测数量】（按 BRAIN 美东时间自然日）
    返回：
    {
        "status": "success",
        "data": {
            "count": int,     # 今日已产生的 alpha 数量（UNSUBMITTED 与 IS_FAIL）
            "date": "YYYY-MM-DD",
            "next_date": "YYYY-MM-DD",
            "eastern_now": "...",
            "utc_offset": "-05:00" / "-04:00"
        }
    }
    或：
    {
        "status": "error",
        "message": "错误信息"
    }
    """
    try:
        date, next_date, offset_str, eastern_now = get_brain_date_window()

# 构建 API URL（参考官方社区帖子，但把 offset 动态化）
        api_url = (
            ' [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ?'
            f'limit=100&offset=0&'
            # 这里的 status 可以按需修改，目前是 UNSUBMITTED 和 IS_FAIL
            f'status=UNSUBMITTED%1FIS_FAIL&'
            f'dateCreated%3E={date}T00:00:00{offset_str}&'
            f'dateCreated%3C={next_date}T00:00:00{offset_str}&'
            f'order=-dateCreated&hidden=false'
        )

resp = s.get(
            api_url,
            headers={
                'accept': 'application/json;version=3.0'
            },
            timeout=15
        )

if not resp.ok:
            raise RuntimeError(f'请求失败：{resp.status_code} {resp.reason} / {resp.text}')

data = resp.json()
        count = data.get('count', 0)

return {
            'status': 'success',
            'data': {
                'count': count,
                'date': date,
                'next_date': next_date,
                'eastern_now': eastern_now.isoformat(),
                'utc_offset': offset_str
            }
        }

except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

if __name__ == "__main__":
    # 1. 登录
    sess = sign_in()

# 2. 查询今日回测总数
    result = query_backtest_count(sess)

print("\n查询结果：")
    print(json.dumps(result, indent=2, ensure_ascii=False))

---

### 评论 #5 (作者: ZL91108, 时间: 6个月前)

请问现在每日限流是多少呢？

---

### 评论 #6 (作者: BW14163, 时间: 6个月前)

感谢大佬分享，正愁着限流了不知道该咋办才好了！这段代码太及时，直接抄走，把 session 塞进去就能跑，终于不用手动数，今天到底回测了多少次了。顺便把 limit 、offset 做循环，再包个重试装饰器，完美嵌套在回测的代码中，超限前自动停，省得半夜被 429 拍醒。等会再补个钉钉飞书机器人，count 一接近 8000 就推送，真正躺平。

---

### 评论 #7 (作者: YH25030, 时间: 6个月前)

谢谢课代表的分享！下个礼拜就要开始限制回测了，您的这个代码太及时了！

---

### 评论 #8 (作者: FF56620, 时间: 6个月前)

这个限制，对于用celery来跑的我来说，还没有什么比较好的方案来处理，先只能少开点槽位的方式来处理，感谢课代表分享

------------------------------------------------------------------
Pursue scalable, repeatable opportunities rooted in probability.

---

### 评论 #9 (作者: MY82844, 时间: 6个月前)

感谢分享，非常有帮助！

看到介绍，后续api也会提供计数了

![图片](images/img_904de019af.png)

---

### 评论 #10 (作者: JX14975, 时间: 6个月前)

在response.header返回可用的剩余回测数就很坏了。非计算机背景的顾问（比如我）估计从接触wq至今都没有去尝试过获取response.header，如果没有大佬的提醒我肯定会忽略这一点。

---

### 评论 #11 (作者: JW12369, 时间: 6个月前)

一直是这样做的啊， 根据时间获取未submit的alpha，也就是F12开发者工具能直接看到的这个api。
另外补充一点， 我都是传北京时间进去，里面自己转换的，不用考虑时区：

传入的是date_begin=datetime(2025, 12, 7, 0, 0, 0, tzinfo=timezone(timedelta(hours=8))
里面使用的时候变成f"&dateCreated%3E={date_begin.astimezone(pytz.timezone("US/Eastern")).isoformat()}"

补充说明一下，brain平台的时区就是pytz.timezone("US/Eastern")，所以上面那个转换完美避免了繁杂的计算和夏令冬令时考虑（他也是自动处理的），在入参每次就只输入需要的年月日时分秒就行，其他不用管了。如果想按美东时间来考虑一天，也就改成datetime(2025, 12, 7, 0, 0, 0, tzinfo=pytz.timezone("US/Eastern"))就可以了

---

### 评论 #12 (作者: AM12075, 时间: 6个月前)

------------------------------------------------------------------------------------------------------------------------------

现在用 dateCreated 的时间区间筛选，如果本地机器时间或云端脚本运行时间和实际提交时间有偏差，是否可能导致边界值（接近 00:00 或 23:59）被漏算？有没有更稳定的方式，比如直接通过 API 的“当天提交总数”字段（如果存在）或按 server timestamp 为准？

------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #13 (作者: YC62305, 时间: 6个月前)

感谢课代表xx，感谢 [WF69827](/hc/en-us/profiles/34809308462487-WF69827) ，真开箱就用了，很好用。

---

### 评论 #14 (作者: XG43628, 时间: 6个月前)

感谢大佬分享，今天刚看到，限制回测已经开始了正好能用上，这样就能知道还剩多少了，可以提前预留一些额度给手调以及ai优化！回测限制数量大概啥时候开始会继续往下调整呢？

==================================================================================

知难上，戒骄狂，常自省，穷途明 ==================================================================================

---

### 评论 #15 (作者: XX42289, 时间: 6个月前)

```
s = login()url = "https://api.worldquantbrain.com/simulations"data = {  "type": "REGULAR",  "settings": {    "maxTrade": "OFF",    "nanHandling": "OFF",    "instrumentType": "EQUITY",    "delay": 1,    "universe": "TOP3000",    "truncation": 0.08,    "unitHandling": "VERIFY",    "testPeriod": "P1Y",    "pasteurization": "ON",    "region": "USA",    "language": "FASTEXPR",    "decay": 4,    "neutralization": "SUBINDUSTRY",    "visualization": False  },  "regular": "1"}res = s.post(url, json=data)header = res.headerslocation = header.get("location")limit = header.get("x-ratelimit-limit")remaining = header.get("x-ratelimit-remaining")reset = header.get("x-ratelimit-reset")res = s.delete(location)print(location)print(f"limit: {limit}")print(f"remaining: {remaining}")print(f"reset: {reset}")
```

这个是回测方案的，更准

---

