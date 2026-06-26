# 【开箱即用】WorldQuant API调用神器：告别回测中429、502错误和三重认证保证机制代码优化

- **链接**: [Commented] 【开箱即用】WorldQuant API调用神器告别回测中429502错误和三重认证保证机制代码优化.md
- **作者**: BL72197
- **发布时间/热度**: 11个月前, 得票: 30

## 帖子正文

429 错误相信大家都是老熟人了，这个问题最经常就是出现在我们回测的过程中，特别是 get 请求获取回测进度的时候，我们的回测过程就是先 post data 开始回测，post 完成后，会一直轮询发送 get 请求去获取回测进度和结果，那么我们的代码是怎么工作的？其实就是一直 sleep retry-after 秒数后，重新去 get 一次是否回测完成，那么当中究竟发送了多少次 get 请求？

![图片](images/img_cd67455c7d.jpeg)

93 次！！！这是10 个批量回测 1 阶表达式所用的 get 请求次数（如果是回测 GLB 数量还要翻倍），所以我们应该能理解这个报错的原因

429 Client Error: Too Many Requests for url
很明显就是字面的意思，官方说你发送了太多请求了 =。=，至于 502 错误其实都是一样被官方限速所致。
其实我们每次发送 get 请求轮询回测是否完成，api 都会返回进度，就如我们页面回测看到的一样

![图片](images/img_7d2c7506b4.jpeg)

一般情况 35%这里是卡最长时间的，我们只需要根据进度来调整每次轮询的间隔就可以了，只要进度超过 35%，后面就很快完成了。

```
sleep_time = 60 if progress_status <= 0.35 else 5
```

![图片](images/img_85df0c6f8d.jpeg)

代码优化后总请求次数从 93-->5大幅下降，下图是跑了近一个月的回测日志，可以看到每天发生 429 错误的次数降到个位数，问题基本得到解决。

![图片](images/img_3ac323c06c.jpeg)

从此我们的回测就是跑多少成功多少

![图片](images/img_6f98618224.jpeg)

接下来 session 认证的问题也是非常影响回测效率的因素之一，我这里设计了 3 重 session 认证保障

**第一道：内存里的Session**  - 解决长任务中，某次循环更新了 session 后怎么同步给全局的问题。

**第二道：文件里的Session**  - 解决多进程或者不同脚本之间 session 共用的问题。

**第三道：重新登录**  - 如果文件里的也过期了，那就重新输入用户名密码登录，然后把新的登录信息保存到文件和内存里。

这套三层认证机制确保了：

- ✅  **零中断** ：请求过程中自动处理认证问题
- ✅  **高性能** ：优先使用最快的认证方式
- ✅  **高可用** ：多重备份确保认证成功，最大减少登录次数
- ✅  **易维护** ：自动化处理，无需手动干预

#### 基于上面的问题解决，我重新封装了 api 客户端，优化了 get 和 post 请求，这套代码我直接分享给大家

```
import osimport requestsimport jsonimport loggingimport base64from datetime import datetimeimport picklefrom time import sleepimport timefrom typing import Optional, Dictlogger = logging.getLogger(__name__)class WqApiClient:    """    一个用于与 WorldQuant BRAIN API 交互的客户端。    该客户端处理 API session 的认证、持久化和自动刷新。    使用方法:    1. 直接修改下方 `__init__` 方法中的 `username` 和 `password` 默认值,       将其替换为您的真实凭证。    2. (可选) 修改 `save_path` 的默认值来指定 session 文件的存储位置。    3. 在您的代码中, 通过 `client = WqApiClient()` 来创建实例并使用。    示例:        logging.basicConfig(level=logging.INFO) # 配置日志        api_client = WqApiClient()        # 现在 api_client 已经配置好并登录，可以使用了    """    def __init__(        self,        worker_logger: Optional[logging.Logger] = None    ):        """        初始化 WqApiClient。        """        self.username = "YOUR_USERNAME"  # <--- 在这里填写您的用户名        self.password = "YOUR_PASSWORD"  # <--- 在这里填写您的密码        self.save_path = './sessions'        self.logger = worker_logger or logger        if self.username == "YOUR_USERNAME" or self.password == "YOUR_PASSWORD":            self.logger.warning("请直接修改 WqApiClient 的 __init__ 方法, 设置您的用户名和密码。")            raise ValueError("未配置凭证")        self.s: Optional[requests.Session] = None        self._login()  # 创建客户端时进行初始登录    def _decode_jwt_exp(self, jwt_token):        try:            parts = jwt_token.split('.')            if len(parts) != 3:                self.logger.info('这不是一个有效的 JWT')                return None            payload_b64 = parts[1]            padding = '=' * (-len(payload_b64) % 4)            payload_json = base64.urlsafe_b64decode(payload_b64 + padding).decode('utf-8')            payload = json.loads(payload_json)            exp_timestamp = payload.get('exp')            if not exp_timestamp:                self.logger.info("未找到 exp 字段")                return None            exp_time = datetime.fromtimestamp(exp_timestamp)            self.logger.debug(f"过期时间(UTC): {exp_time.strftime('%Y-%m-%d %H:%M:%S')}")            return exp_timestamp        except Exception as e:            self.logger.info(f"解码出错: {e}")            return None    def _check_and_refresh_session(self):        """        检查 session 是否有效或即将过期，如果需要则刷新。        这个方法会直接更新 self.s，而不是返回一个新的session。        """        othu2_session_path = os.path.join(self.save_path, f'othu2_session.pkl')        # 检查内存中的session        if self.s:            expires_at = self._decode_jwt_exp(self.s.cookies.get("t"))            if expires_at and time.time() < expires_at - 600:                self.logger.debug("内存中的 Session 状态良好。")                return # Session is good, no need to do anything        # 检查文件中的session        if os.path.exists(othu2_session_path):            try:                with open(othu2_session_path, 'rb') as f:                    existing_session = pickle.load(f)                                expires_at = self._decode_jwt_exp(existing_session.cookies.get("t"))                if expires_at and time.time() < expires_at - 600:                    self.logger.info("从文件加载的 Session 状态良好。")                    self.s = existing_session                    return            except (pickle.UnpicklingError, EOFError, AttributeError, KeyError) as e:                self.logger.error(f"加载或解析 session 文件失败: {e}，将强制刷新。")        # 如果内存和文件中的session都无效，则强制刷新        self.logger.warning("Session 过期或无效，正在强制刷新...")        self._login(force_refresh=True)    def _login(self, force_refresh: bool = False):        """        登录到 WorldQuant BRAIN API 并将会话对象(session)持久化。        :param force_refresh: 如果为 True，则强制重新登录，即使存在有效的会话文件。        """        othu2_session_path = os.path.join(self.save_path, f'othu2_session.pkl')        if not force_refresh and os.path.exists(othu2_session_path):            try:                with open(othu2_session_path, 'rb') as f:                    self.logger.info(f'加载 {othu2_session_path} 文件')                    session = pickle.load(f)                expires_at = self._decode_jwt_exp(session.cookies.get("t"))                if expires_at:                    expires_time = datetime.fromtimestamp(expires_at)                    if datetime.now().timestamp() < expires_at - 300:                        self.logger.info(f"发现还在有效期的 othu2_session 文件，过期时间: {expires_time}，直接使用。")                        self.s = session                        return                    else:                        self.logger.info("发现 othu2_session 文件将过期或者已过期，重新登录。")                else:                    self.logger.info("othu2_session 文件无效, 重新登录。")            except (pickle.UnpicklingError, EOFError, AttributeError, KeyError) as e:                self.logger.error(f"加载或解析 session 文件失败: {e}，将重新登录。")        self.logger.info(f'通过 API 登录 WorldQuant Brain: {self.username}')        s = requests.Session()        s.auth = (self.username, self.password)        while True:            try:                response = s.post('https://api.worldquantbrain.com/authentication', timeout=30)                response.raise_for_status()                self.logger.info("Authentication successful.")                                # 确保保存目录存在                os.makedirs(self.save_path, exist_ok=True)                with open(othu2_session_path, 'wb') as f:                    pickle.dump(s, f)                self.s = s                break            except requests.HTTPError as e:                self.logger.error(f"HTTP error occurred: {e}. Retrying...")                sleep(10)            except Exception as e:                self.logger.error(f"Error during authentication: {e}. Trying to login again.")                sleep(10)    def post(        self, url: str,         data: Optional[dict] | Optional[list],        max_retry: int = 3,         fail_sleep: int = 30    ) -> Optional[requests.Response]:        self._check_and_refresh_session()        retry = max_retry        while retry > 0:            try:                response = self.s.post(url, json=data, timeout=30)                response.raise_for_status()                self.logger.info(f"发送 post 请求成功, 响应状态码: {response.status_code}")                return response            except requests.HTTPError as e:                if response.status_code == 401 or 'Unauthorized' in str(e):                    self.logger.warning("Session 可能已过期，强制刷新并重试...")                    self._login(force_refresh=True)                else:                    self.logger.error(f"发送 post 请求失败, 将在 {fail_sleep} 秒后重试: {e}")                    time.sleep(fail_sleep)                    retry -= 1            except Exception as e:                self.logger.error(f"未知错误, 将在 {fail_sleep} 秒后重试: {e}")                time.sleep(fail_sleep)                retry -= 1        return None    def get_result(        self, url: str,         max_retry: int = 3,         fail_sleep: int = 30,         job_timeout: Optional[int] = None,        request_type: str = None,        params: Optional[dict] = None    ) -> Optional[Dict]:        self._check_and_refresh_session()        start_time = time.time()        retry = max_retry        total_get_count = 0        while retry > 0:            if job_timeout and time.time() - start_time > job_timeout:                self.logger.error(f"总耗时超过 {job_timeout / 60} 分钟, 停止重试")                return None            try:                response = self.s.get(url, timeout=30, params=params)                total_get_count += 1                response.raise_for_status()                if response.headers.get("Retry-After", 0) != 0:                    # Handle long polling with progress                    if request_type == 'simulation':                        progress_status = response.json().get('progress', 0)                        sleep_time = 60 if progress_status <= 0.35 else 5                        time.sleep(sleep_time)                    elif request_type == 'fetch_data':                        time.sleep(3)                    else:                        time.sleep(float(response.headers["Retry-After"]))                else:                    if response.text.strip():                        if request_type == 'simulation':                            self.logger.info(f"请求获取回测结果成功, 一共发送了 get 请求 {total_get_count} 次")                        return response.json()                    else:                        return None            except requests.HTTPError as e:                if response.status_code == 401 or 'Unauthorized' in str(e):                    self.logger.warning("Session 可能已过期，强制刷新并重试...")                    self._login(force_refresh=True)                else:                    self.logger.error(f"请求获取数据失败, 将在 {fail_sleep} 秒后重试: {e}")                    time.sleep(fail_sleep)                    retry -= 1            except (ValueError, json.JSONDecodeError) as e:                self.logger.error(f"JSON解析失败, 响应内容: {response.text[:200]}...")                return None            except Exception as e:                self.logger.error(f"未知错误, 将在 10 秒后重试: {e}")                time.sleep(10)                retry -= 1        return None
```

代码食用方法

```
# 先在 __ini__() 中填写账号密码self.username="YOUR_USERNAME"# <--- 在这里填写您的用户名self.password="YOUR_PASSWORD"# <--- 在这里填写您的密码
```

```
# 下面是具体示例client = WqApiClient()# 发送回测 post 请求sim_data_list = 1 个批次回测的 data# simulation_response 直接就是 post 返回的 jsonsimulation_response = client.post('https://api.worldquantbrain.com/simulations', data=sim_data_list, max_retry=5, fail_sleep=90)progress_url = simulation_response.headers.get('Location', '')# 获取回测结果的 get 请求# job_timeout 为整个轮询请求的总超时时间，防止任务卡死# result 为请求返回的 json 结果# request_type 回测选择 simulation，拉取数据选择 fetch_dataresult = client.get_result(progress_url, job_timeout=1800, request_type='simulation', max_retry=5, fail_sleep=90)
```

```
# 获取 alpha 信息alpha_id = 'xxxxxxx'alpha_result = client.get_result(f"https://api.worldquantbrain.com/alphas/{alpha_id}", max_retry=5, fail_sleep=10)# 获取 pnl 数据url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl"pnl = client.get_result(url, request_type='fetch_data')# check prod corrurl = f'https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod'prod_corr_result = client.get_result(url, request_type='fetch_data', job_timeout=20*60)
```

get_result 方法可以涵盖 wq 大部分 get 请求的用法，比如获取数据字段、年度数据、check等。

最后总结下，这套代码保障了回测的高效、低故障、各类异常捕获解决和便利性，大家试用如果有什么问题可以一起交流下，如果对回测系统的设计有兴趣可以看看我上一篇文章。  [../JR23144/[Commented] 构建 724 小时不间断 Alpha 回测系统基于 Celery 和动态任务队列的架构分享代码优化.md](../JR23144/[Commented] 构建 724 小时不间断 Alpha 回测系统基于 Celery 和动态任务队列的架构分享代码优化.md)

最后的最后，由于忙着工作和构思新的模版，这篇帖子鸽了比较久了，希望大家多多点赞，谢谢！

---

## 讨论与评论 (8)

### 评论 #1 (作者: AL13375, 时间: 10个月前)

大佬！太强了！这么好的东西居然现在才看到，真是相见恨晚啊！！！

都已经等不及要去部署了，但是必须先给大佬点个赞！！！

建议以后大佬多发点优化回测速度和流程，减少回测报错以及报错后等待时间的帖子，保证逢贴必赞！！！

祝大佬VF1.0 forever！！！

---

### 评论 #2 (作者: BL72197, 时间: 10个月前)

[AL13375](/hc/en-us/profiles/27647035974807-AL13375)  优化回测速度和流程在 todo 了但还没有时间去做，但目前来说还是可以的，至少回测很顺心跑了快 1 个月都没什么报错

---

### 评论 #3 (作者: SJ65808, 时间: 10个月前)

感谢大佬的分享，正好回去试验一下~~

============================================================================================================ Talk is cheap, Show me the alpha =================================

---

### 评论 #4 (作者: JX28185, 时间: 10个月前)

感谢大佬的分享，点赞

---

### 评论 #5 (作者: DZ31817, 时间: 8个月前)

20251007

------------------------------------------------------------------------------------------

感谢分享，请求数量过多的问题我之前也考虑过，并且也有意识降低请求次数，比如接口返回的retry after一般是2.5秒，我改成了3秒，之所以没改成更长，还是顾虑设置太长会浪费比较多的时间，设置的轮询窗口不可能跟回测结束的时间完全匹配，假设每个回测只是差1秒，那么1000个回测累积起来也会多浪费1000秒，而像帖子里这样设置等待5秒和60秒，可能会面临已经回测结束但还是硬等的情况。   不过报429本身也会浪费时间，就看哪种方式更高效了，可以做实验对比一下。

---

### 评论 #6 (作者: PJ60307, 时间: 8个月前)

感谢大佬分享

---

### 评论 #7 (作者: SZ20589, 时间: 8个月前)

感谢大佬分享，老是回测遇到429和503，总是sleep几秒处理，看了大佬分享的文章后，觉得要具体处理，这样可以避免遇到这些问题。

大佬的实践和创新精神真是惊为天人，有这种创新和实践精神，不管大佬干什么行业，大佬都会是业界翘楚，行业标杆。祝愿大佬早日GM， VF经久1.0。

再次感谢大佬

=============================================================================

========Genius is one percent inspiration and ninety-nine percent perspiration.=============

==============================================================================

---

### 评论 #8 (作者: GC81559, 时间: 4个月前)

相见恨晚啊，使用了之后完全解决了，太棒了大佬

---

