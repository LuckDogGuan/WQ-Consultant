# 【alpha 高并发429处理篇】代码优化

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwgX9i8dPR46D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAYxodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzMyNDc4MzE1MjA3OTEtLWFscGhhLSVFOSVBQiU5OCVFNSVCOSVCNiVFNSU4RiU5MTQyOSVFNSVBNCU4NCVFNyU5MCU4NiVFNyVBRiU4NwY7CFQ6DnNlYXJjaF9pZEkiKTRiZjQ4ZjQwLTUzMjAtNGJjOS1iM2I2LWU3NGU3Nzg5MjdjMgY7CEY6CXJhbmtpCDoLbG9jYWxlSSIKemgtY24GOwhUOgpxdWVyeUkiDFNEMTc1MzEGOwhUOhJyZXN1bHRzX2NvdW50aRs%3D--2cf7c90a37ac516eacc1b49845511899a674336a
- **作者**: SH90982
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

Hi，小编这次更新将为大家带来高并发429的处理篇上图展示了三种高并发场景：第一种：无任何优化的高并发远程服务器高负载第二种：随机休整 效果有一点但不大第三种：小编构建的自适应退避客户端可以看到的是小编的客户端在出现大量429报错后会逐步降低请求直至出现熔断 退避等待正常后逐步恢复高并发importasyncioimporthttpximportjsonimportrandomimporttimefromtypingimportOptional, Tuple, DictfromenumimportEnumfromdataclassesimportdataclassimportosfromworldquant.logsimportget_loggerlogger=get_logger(__name__)classBackoffStrategy(Enum):"""退避策略枚举"""EXPONENTIAL="exponential"LINEAR="linear"FIXED="fixed"classJitterType(Enum):"""抖动类型枚举"""NONE="none"UNIFORM="uniform"EXPONENTIAL="exponential"FULL="full"@dataclassclassRetryConfig:"""重试配置类"""max_retries:int=3base_delay:float=1.0max_delay:float=60.0backoff_strategy: BackoffStrategy=BackoffStrategy.EXPONENTIALjitter_type: JitterType=JitterType.EXPONENTIALmultiplier:float=2.0# 针对不同错误类型的配置rate_limit_base_delay:float=5.0server_error_base_delay:float=2.0network_error_base_delay:float=1.0classCircuitBreaker:"""简单的断路器实现"""def__init__(self,failure_threshold:int=5,recovery_timeout:float=60.0):self.failure_threshold=failure_thresholdself.recovery_timeout=recovery_timeoutself.failure_count=0self.last_failure_time=0self.state="CLOSED"# CLOSED, OPEN, HALF_OPENdefcan_execute(self) ->bool:ifself.state=="CLOSED":returnTrueelifself.state=="OPEN":iftime.time()-self.last_failure_time>self.recovery_timeout:self.state="HALF_OPEN"returnTruereturnFalseelse:# HALF_OPENreturnTruedefrecord_success(self):self.failure_count=0self.state="CLOSED"defrecord_failure(self):self.failure_count+=1self.last_failure_time=time.time()ifself.failure_count>=self.failure_threshold:self.state="OPEN"classAdaptiveRetryCalculator:"""自适应重试计算器"""def__init__(self,config: RetryConfig):self.config=configself.success_rate_window=[]self.window_size=100defcalculate_delay(self,attempt:int,error_type:str="default",retry_after: Optional[float]=None) ->float:"""计算延迟时间"""ifretry_afterisnotNone:# 验证Retry-After的合理性（防止恶意服务器）retry_after=min(max(retry_after,1.0),self.config.max_delay)returnself._add_jitter(retry_after, error_type)# 根据错误类型选择基础延迟base_delay=self._get_base_delay(error_type)# 计算基础退避时间ifself.config.backoff_strategy==BackoffStrategy.EXPONENTIAL:delay=base_delay*(self.config.multiplier**(attempt-1))elifself.config.backoff_strategy==BackoffStrategy.LINEAR:delay=base_delay*attemptelse:# FIXEDdelay=base_delay# 应用最大延迟限制delay=min(delay,self.config.max_delay)# 根据成功率动态调整（自适应）delay=self._apply_adaptive_factor(delay)# 添加抖动returnself._add_jitter(delay, error_type)def_get_base_delay(self,error_type:str) ->float:"""根据错误类型获取基础延迟"""iferror_type=="rate_limit":returnself.config.rate_limit_base_delayeliferror_type=="server_error":returnself.config.server_error_base_delayeliferror_type=="network_error":returnself.config.network_error_base_delayelse:returnself.config.base_delaydef_add_jitter(self,delay:float,error_type:str) ->float:"""添加抖动以避免雷鸣群体效应"""ifself.config.jitter_type==JitterType.NONE:returndelayelifself.config.jitter_type==JitterType.UNIFORM:# 均匀抖动：在[delay/2, delay]范围内returndelay*(0.5+random.random()*0.5)elifself.config.jitter_type==JitterType.EXPONENTIAL:# 指数抖动：更好的分布特性jitter_max=delay*0.1# 10%的抖动范围returndelay+random.expovariate(1.0/jitter_max)-jitter_maxelifself.config.jitter_type==JitterType.FULL:# 全抖动：在[0, delay]范围内，对高并发场景最友好returnrandom.uniform(0, delay)else:returndelaydef_apply_adaptive_factor(self,delay:float) ->float:"""根据历史成功率应用自适应因子"""iflen(self.success_rate_window)<10:# 样本不足returndelaysuccess_rate=sum(self.success_rate_window)/len(self.success_rate_window)ifsuccess_rate<0.5:# 成功率低，增加延迟returndelay*1.5elifsuccess_rate>0.8:# 成功率高，减少延迟returndelay*0.8else:returndelaydefrecord_attempt(self,success:bool):"""记录请求尝试结果"""self.success_rate_window.append(1ifsuccesselse0)iflen(self.success_rate_window)>self.window_size:self.success_rate_window.pop(0)classhttpxPool:def__init__(self,max_connections:int=100,max_keepalive_connections:int=20,retry_config: Optional[RetryConfig]=None):# 从环境变量获取超时和重试次数，设置默认值self.timeout=httpx.Timeout(float(os.getenv('HTTPX_TIMEOUT',30.0)))self.retry_config=retry_configorRetryConfig(max_retries=int(os.getenv('HTTPX_RETRY_COUNT',3)))self._client: Optional[httpx.AsyncClient]=Noneself._lock=asyncio.Lock()self._max_connections=max_connectionsself._max_keepalive_connections=max_keepalive_connectionsself._initialized=False# 添加自适应重试计算器和断路器self.retry_calculator=AdaptiveRetryCalculator(self.retry_config)self.circuit_breaker=CircuitBreaker()asyncdefinitialize(self,auth: Optional[Tuple[str,str]]=None,headers: Optional[Dict]=None):"""异步初始化或重新初始化客户端和连接池"""asyncwithself._lock:ifself._initializedandself._clientandnotself._client.is_closed:return# 如果客户端存在但已关闭，先彻底关闭ifself._clientandself._client.is_closed:self._client=Nonelimits=httpx.Limits(max_connections=self._max_connections,max_keepalive_connections=self._max_keepalive_connections)# 步骤1: 创建客户端实例（同步操作，但很快）self._client=httpx.AsyncClient(auth=httpx.BasicAuth(auth[0], auth[1])ifauthelseNone,headers=headers,timeout=self.timeout,http2=True,# 恢复为HTTP/2，以匹配服务器要求limits=limits,verify=True)# 步骤2: 异步启动客户端（非阻塞）awaitself._client.__aenter__()self._initialized=Truelogger.info("httpx客户端池已异步初始化, 限制配置:%s", limits)asyncdefupdate_headers(self,headers: Dict):"""更新请求头"""asyncwithself._lock:ifself._client:self._client.headers.update(headers)logger.debug("请求头已更新:%s", headers)def_classify_error(self,error) ->str:"""分类错误类型"""ifisinstance(error, httpx.HTTPStatusError):status_code=error.response.status_codeifstatus_code==429:return"rate_limit"elif500<=status_code<600:return"server_error"else:return"http_error"elifisinstance(error, (httpx.ConnectError, httpx.ReadError, httpx.WriteError)):return"network_error"else:return"unknown_error"asyncdefrequest(self,method:str,url:str,**kwargs) -> httpx.Response:"""执行 HTTP 请求，支持智能重试和错误处理"""# 检查断路器状态ifnotself.circuit_breaker.can_execute():logger.error("断路器开启，请求被拒绝:%s%s", method, url)response=httpx.Response(status_code=503,content=json.dumps({"error":"Circuit breaker open","message":"服务暂时不可用，请稍后重试"}).encode(),request=httpx.Request(method, url))returnresponseretries=0last_error=Nonelogger.debug("开始HTTP请求:%s%s", method, url)whileretries<self.retry_config.max_retries:try:ifnotself._client:awaitself.initialize()ifself._clientisNone:raiseException("无法初始化 HTTP 客户端")response=awaitself._client.request(method, url,**kwargs)logger.debug("HTTP响应:%s%s->%d", method, url, response.status_code)# 记录成功并重置断路器self.retry_calculator.record_attempt(True)self.circuit_breaker.record_success()# 处理 429 错误（请求频率限制）ifresponse.status_code==429:retries+=1ifretries==self.retry_config.max_retries:logger.error("达到最大重试次数%d，仍然收到 429 错误",self.retry_config.max_retries)response.raise_for_status()# 检查 Retry-After 头retry_after=response.headers.get('Retry-After')retry_after_seconds=Noneifretry_after:try:retry_after_seconds=float(retry_after)except(ValueError,TypeError):retry_after_seconds=Nonewait_time=self.retry_calculator.calculate_delay(retries,"rate_limit", retry_after_seconds)logger.warning("请求频率限制(429)，第%d/%d次重试，等待%.2f秒",retries,self.retry_config.max_retries, wait_time)awaitasyncio.sleep(wait_time)continue# 对于非重试的错误，直接返回响应而不抛出异常returnresponseexcept(httpx.RequestError, httpx.HTTPStatusError)ase:last_error=eerror_type=self._classify_error(e)# 记录失败self.retry_calculator.record_attempt(False)self.circuit_breaker.record_failure()# 对于HTTP状态错误，检查是否需要重试ifisinstance(e, httpx.HTTPStatusError):status_code=e.response.status_code# 429已经在上面处理过了ifstatus_code==429:continue# 对于4xx错误（除了429），通常不应该重试elif400<=status_code<500:logger.error("客户端错误%d，不重试:%s", status_code,str(e))returne.response# 直接返回错误响应# 对于网络错误和5xx错误，进行重试retries+=1ifretries==self.retry_config.max_retries:logger.error("请求失败，达到最大重试次数%d:%s",self.retry_config.max_retries,str(e))# 如果是HTTP状态错误，返回原始响应ifisinstance(e, httpx.HTTPStatusError):returne.response# 如果是其他错误，创建自定义响应response=httpx.Response(status_code=500,content=json.dumps({"error":str(last_error),"message":"请求失败，达到最大重试次数"}).encode(),request=httpx.Request(method, url))returnresponse# 计算智能退避时间wait_time=self.retry_calculator.calculate_delay(retries, error_type)logger.warning("请求失败，第%d/%d次重试，等待%.2f秒 [%s]:%s",retries,self.retry_config.max_retries, wait_time, error_type,str(e))awaitasyncio.sleep(wait_time)# 如果所有重试都失败iflast_error:raiselast_errorraiseException("请求失败，未知错误")asyncdefclose(self):"""异步关闭客户端和连接池"""asyncwithself._lock:ifself._clientandnotself._client.is_closed:awaitself._client.__aexit__(None,None,None)self._initialized=Falselogger.info("httpx客户端连接池已关闭")asyncdef__aenter__(self):"""支持异步上下文管理器"""returnselfasyncdef__aexit__(self,exc_type,exc_val,exc_tb):"""退出时自动关闭连接池"""awaitself.close()以上部分是小编的自适应负载均衡的httpx客户端 建议理解异步编程的老铁食用

---

## 讨论与评论 (8)

### 评论 #1 (作者: FG39655, 时间: 1年前)

感谢楼主分享，建议简单写几句思路，缺少缩进的纯代码看起来有些费劲-_-;;

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

大佬是否考虑过这样一种情况:假如是8*10个alpha在回测, 如果触发熔断,需要等待1分钟才可以获取进度, 那么这8个槽是否都要等待1分钟,而原本的这8个槽可能有不少在这一分钟内就已经回测结束的,比如回测USA,一般3-4分钟回测结束, 很有可能出现上面的情况.这种情况如何解决呢?另外看大佬给的图片, 使用您自己的策略后的表现,是不是样本不够大啊?是否可以多收集一部分数据,再看总体的优化?另外,大佬是否有做过统计,在三种策略下,不改变其他条件的情况,查看指定时间内各自完成了多少回测?比如各自在下午时间段测试1小时.

---

### 评论 #3 (作者: SH90982, 时间: 1年前)

介绍:我的文章连贯性很强 （PS 后期心血来潮就说不定了），../JG15244/[Commented] alpha 模拟高效篇.md这是开篇架构当然，这是我未了解顾问卡槽的用户级架构。但仍很有价值。还有，SD17531说的假如是8*10个alpha在回测, 如果触发熔断,需要等待1分钟才可以获取进度, 那么这8个槽是否都要等待1分钟。有这部分疑问的可以参考我上篇文章。系统运行全局异步 + 任务调度（自己实现基于内存管理不要cerely影响效率） 队列完成 多任务直接独立互不影响。所以我其实压根没有考虑过单进程阻塞的问题。8个任务槽熔断一个其他正常互不影响

---

### 评论 #4 (作者: BJ10003, 时间: 1年前)

大佬您好，看了您分享的内容真的收获满满，对回测策略的细节拆解和思考特别有启发性，能感觉到您在这上面下了很多功夫，特别感谢您的分享！ 同时也有同样的疑惑：一是如果8*10个alpha回测时触发熔断，但是每一个槽回测的时长是不一样的，怎么只对时间超时的那部分回测；或者您在统计的时候有没有统计过那些字段更容易出现这个问题，感觉这类数据可能也能帮着进一步对比策略效率

---

### 评论 #5 (作者: SD17531, 时间: 1年前)

SH90982熔断的话,是服务器对用户所有的api操作全部限制,  此时不但任何API操作无法完成, 在网页上登录也无法完成. 我不太清楚大佬是怎么绕过这个限制,使得熔断只对一个任务造成影响, 而其他任务不受影响的.即使不触发熔断, 对于服务器来说, 我们使用的session,也经常会遇到retry_after过长的问题, 此时对于所有的请求, 服务器都是返回retry_after,比如20秒,这个限制不清楚楼主是怎么绕过的.

---

### 评论 #6 (作者: ST57347, 时间: 1年前)

如果可以稳定一个标准的回测数据，会不会更好一些===============================================================================

---

### 评论 #7 (作者: SH90982, 时间: 1年前)

SD17531你其实陷入误区，人家服务器真没有全部限流。站的角度不同，在高并发的情况下我的程序运行状态实际上是这样的所以你觉得熔断会影响整个系统只能说明你的代码存在阻塞和串行，对我来说8个槽熔断4个还有4个在跑 我现在家里的服务器还在运行回测，一点也不影响我评论昨天跑半天的成果，至于为啥没跑一天？我alpha是真的写不过来了

---

### 评论 #8 (作者: JR23144, 时间: 1年前)

看到分层延迟和JitterType.FULL我就跪了——这才是真正抗并发洪水的设计啊！之前自己瞎写sleep(random())简直弟弟。断路器整合进HTTP客户端这个操作也帅，比裸调API优雅多了。不过好奇自适应因子_apply_adaptive_factor的实际数据反馈，成功率波动大时延迟跳变会明显吗？另：retry_after合理性校验那行细节拉满，防止恶意服务器这思路学到了

---

