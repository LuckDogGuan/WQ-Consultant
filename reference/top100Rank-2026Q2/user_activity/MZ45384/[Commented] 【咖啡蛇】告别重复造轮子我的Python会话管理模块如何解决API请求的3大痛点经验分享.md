# 【咖啡蛇】告别重复造轮子！我的Python会话管理模块如何解决API请求的3大痛点经验分享

- **链接**: [Commented] 【咖啡蛇】告别重复造轮子我的Python会话管理模块如何解决API请求的3大痛点经验分享.md
- **作者**: QL33636
- **发布时间/热度**: 3个月前, 得票: 6

## 帖子正文

在顾问的研究工作中经常需要和API打交道，你是否也遇到过这些问题？会话过期需要手动重新登录、请求失败要反复重试、业务代码里充斥着各种异常处理逻辑...这些重复的工作不仅耗时，还容易让代码变得臃肿。

今天我想分享一个我自己封装的会话管理模块，它通过统一封装、自动重试和中间件机制，完美解决了这些痛点。

#### 💡 代码亮点

#### 🚀 核心功能与解决的痛点

**1. 统一封装，告别重复代码**

- **痛点** ：在业务代码中需要频繁处理会话创建、请求重试等通用逻辑，导致代码冗余且难以维护。
- **解决方案** ：所有请求统一调用  `request_with_retry`  函数，底层自动处理会话管理和重试逻辑，让业务代码专注于核心功能。

**2. 会话过期自动检测与重连**

- **痛点** ：会话过期时需要手动重新登录，尤其在长时间运行的任务中容易导致请求失败。
- **解决方案** ：会话管理器  `_SessionManager`  会自动检测会话是否接近过期（剩余时间小于1分钟），并在需要时自动重新登录，确保请求始终使用有效的会话。

**3. 智能重试机制，提升代码鲁棒性**

- **痛点** ：网络波动、服务端错误或限流等问题会导致请求失败，需要手动处理重试逻辑。
- **解决方案** ： `request_with_retry`  函数采用指数退避策略，在遇到网络异常或服务端错误时自动重试（最多10次），并通过中间件处理特定的限流场景。

**4. 灵活的中间件机制，应对复杂场景**

- **痛点** ：难以统一管理一些定制化的请求逻辑。
- **解决方案** ：通过  `_RequestMiddleware`  中间件机制，可以灵活添加自定义逻辑，例如：
  - **处理 Retry-After 头** ：对于需要稍后重试的GET请求，自动等待并重试。
  - **日回测次数限制** ：当回测次数达到上限时，自动等待至美东时间次日零点。
  - **并发回测限制** ：遇到并发限制时，自动重试直到成功。

- #### 🌟 中间件机制的核心优势
  - **低侵入性** ：新增功能只需添加中间件，不影响原有业务逻辑。
  - **高度可扩展** ：支持无限扩展通用请求处理逻辑，比如更加精细化的控制请求头中  `RateLimit-Remaining, `  `RateLimit-Reset`  等参数，这个也是所有相关性获取接口中都涉及的通用逻辑。

#### 💻 完整代码

```
import copy
import json
import logging
import random
import threading
import time
from datetime import datetime, timedelta

import pytz
import requests

__all__ = [
    'get_session',
    'request_with_retry',
]

class _SessionManager:
    """会话管理器，负责自动登录、维护和续期会话"""

    def __init__(self):
        self.session = None
        self.expiry_time = None
        self._session_lock = threading.Lock()

    def get_session(self):
        """
        获取有效的认证会话

        Returns:
            requests.Session: 认证后的会话对象
        """
        with self._session_lock:
            # 会话不存在或接近过期时重新登录
            if self.session is None or self._is_close_to_expiry():
                self._login()
            return self.session

    def _is_close_to_expiry(self):
        """
        判断会话是否接近过期

        Returns:
            bool: 会话剩余时间小于1分钟返回True，否则返回False
        """
        if self.expiry_time is None:
            return True

        return datetime.now() >= (self.expiry_time - timedelta(minutes=1))

    def _login(self):
        """登录WorldQuant BRAIN平台并创建新会话"""
        # 从凭证文件读取用户名和密码
        with open('brain_credentials.json') as fp:
            username, password = json.load(fp)

        # 初始化会话并设置认证
        self.session = requests.Session()
        self.session.auth = (username, password)

        # 发送认证请求
        response = self.session.post('https://api.worldquantbrain.com/authentication')
        response.raise_for_status()
        response_data = response.json()

        user_id = response_data.get('user', {}).get('id')
        token_expiry = response_data.get('token', {}).get('expiry', 14400.0)

        self.expiry_time = datetime.now() + timedelta(seconds=token_expiry)
        logging.info(f"用户 {user_id} 登录成功 | 会话过期时间: {self.expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")

# 会话管理器实例
_session_manager = _SessionManager()

class _RequestMiddleware:
    def __init__(self):
        self.middlewares = []

    def add(self, middleware):
        self.middlewares.append(middleware)

    def process(self, request: requests.Request, response: requests.Response) -> requests.Response:
        for middleware in self.middlewares:
            response = middleware(request, response)
        return response

_request_middleware = _RequestMiddleware()

@_request_middleware.add
def retry_after_header_middleware(request: requests.Request, response: requests.Response) -> requests.Response:
    """处理Retry-After头（仅对GET请求生效）"""
    if request.method != 'GET':
        return response

    start_time = time.time()
    while 'Retry-After' in response.headers and time.time() - start_time < 60 * 60:
        retry_after = float(response.headers.get('Retry-After'))
        time.sleep(retry_after)

        # 重新发送请求
        session = get_session()
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request)

    return response

@_request_middleware.add
def daily_simulation_limit_middleware(request: requests.Request, response: requests.Response) -> requests.Response:
    """处理日回测次数限制"""
    if response.status_code != 429 or response.json().get('detail') != 'DAILY_SIMULATION_LIMIT_EXCEEDED':
        return response

    # 计算美国东部时区次日零点的等待秒数
    est_tz = pytz.timezone('US/Eastern')
    now_utc = datetime.now(pytz.UTC)  # 先取UTC时间避免本地时区干扰
    now_est = now_utc.astimezone(est_tz)  # 转换为美国东部时间

    # 计算次日零点
    next_day_est = (now_est + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # 计算等待秒数（取整避免微秒误差）
    seconds_to_next_day = int((next_day_est - now_est).total_seconds())
    logging.warning(f"日回测次数已达上限，将等待至美国东部次日零点...")

    # 等待至理论零点 + 随机补偿延迟（应对服务端同步延迟）
    time.sleep(seconds_to_next_day + random.randint(30, 120))  # 额外加30~120秒随机延迟

    # 重新发送请求
    session = get_session()
    prepared_request = session.prepare_request(request)
    response = session.send(prepared_request)

    return response

@_request_middleware.add
def concurrent_simulation_limit_middleware(request: requests.Request, response: requests.Response) -> requests.Response:
    """处理并发回测次数限制"""
    while response.status_code == 429 and response.json().get('detail') == 'CONCURRENT_SIMULATION_LIMIT_EXCEEDED':
        time.sleep(10)

        # 重新发送请求
        session = get_session()
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request)

    return response

def get_session():
    """
    获取经过认证的会话对象（线程安全）

    Returns:
        requests.Session: 已登录的会话实例，可直接用于发送HTTP请求
    """
    return copy.deepcopy(_session_manager.get_session())

def request_with_retry(method, url, max_attempts=10, **kwargs):
    """
    带重试机制的HTTP请求函数

    通过深拷贝获取会话副本保证线程安全，使用指数退避策略处理异常

    Args:
        method (str): HTTP方法 ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
        url (str): 请求URL
        max_attempts (int): 最大请求尝试次数
        **kwargs: 传递给requests方法的其他参数

    Returns:
        requests.Response: HTTP响应对象
    """
    method = method.upper()
    retry_count = 0
    response = None

    while retry_count < max_attempts:
        # 指数退避等待（首次请求不等待）
        if retry_count > 0:
            time.sleep(min(2 ** retry_count, 60))

        try:
            request = requests.Request(method, url, **kwargs)

            session = get_session()
            prepared_request = session.prepare_request(request)
            response = session.send(prepared_request)

            # 执行请求处理逻辑
            response = _request_middleware.process(request, response)

            # 成功响应 (2xx)
            if 200 <= response.status_code < 300:
                return response

            # 客户端错误（4xx）：除429外不重试
            if 400 <= response.status_code < 500 and response.status_code != 429:
                logging.error(
                    f"请求错误 [{method} {url}] | 状态码: {response.status_code} | 响应内容: {response.text}"
                )
                return response

            # 服务器错误或429，记录日志并重试
            retry_count += 1
            logging.warning(
                f"请求异常 [{method} {url}] | 状态码: {response.status_code} | "
                f"响应内容: {response.text} | 尝试次数: {retry_count}/{max_attempts}"
            )

        except requests.exceptions.RequestException as e:
            retry_count += 1
            logging.warning(
                f"网络异常 [{method} {url}] | 错误类型: {type(e).__name__} | "
                f"错误详情: {str(e)} | 尝试次数: {retry_count}/{max_attempts}"
            )

    return response

```

---

## 讨论与评论 (6)

### 评论 #1 (作者: CZ78575, 时间: 3个月前)

=====================================评论区========================================= 挺不错的思路，用装饰器可以很方便的拓展，每次调用执行检测

============================(好东西，快把这个代码给我啊)===============================

---

### 评论 #2 (作者: RC59004, 时间: 3个月前)

为啥不用ace_lib？这种原始的请求比ace_lib有什么优势吗？

---

### 评论 #3 (作者: MZ45384, 时间: 3个月前)

超有用的帖子，在日常使用mcp的过程中我也添加了几个重试机制，但是没有大佬的系统化和场景全面，应对不同的场景来添加对应的重试方法，比如post后由于网络波动connectionaborted只需重复get_alpha_detail即可，不加的话ai可能盲目post白白浪费了simulation次数。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #4 (作者: QL33636, 时间: 3个月前)

[RC59004](/hc/en-us/profiles/33810604054551-RC59004)

我没怎么用过ace_lib。我觉得自己写的会话模块最主要的优势就是更接地气，能实现很多自己定制化的需求。至于更详细的优势说明，帖子里也已经自卖自夸过了。哈哈哈哈哈哈哈哈哈

---

### 评论 #5 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的分享，解决了会话的中断这个痛点                                                                                    ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #6 (作者: YD77867, 时间: 2个月前)

太赞了

---

