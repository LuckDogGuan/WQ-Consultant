# 【设计思路分享】在Linux云服务器打造不停机的alpha运行引擎

- **链接**: [Commented] 【设计思路分享】在Linux云服务器打造不停机的alpha运行引擎.md
- **作者**: ZS61081
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

这篇帖子主要分享在Linux云服务器上运行程序，可以不间断的执行alpha模拟、结果检查和自动标记。

整个模拟过程可以分为：登录、生成alpha表达式、执行模拟、执行结果检查、进行submission check。为了实现不停机的目标，对上述过程实现如下自动化的功能。

1. 一直保持登录状态。

2. 模拟执行可以按优先级自动拉取待执行的alpha表达式，并提交模拟。

3. 自动对执行完的结果，进行初筛，有error结果项，自动打标或者设置color为红色。

4.对通过初筛的结果，进行submission检查，通过检查的进行打标或设置color为绿色。

整体的模块分工如下图所示。

![图片](images/img_544f1ae06c.png)

其中有两个代码实现关键点：登录状态保存到cookie文件中；程序保持运行状态不退出。

1. 登录状态保存到cookie文件

使用cookiejar可以保存cookie到文件中。

> ```
> s = requests.Session()cookie_file = '../session_cookies.txt's.cookies = cookiejar.LWPCookieJar(cookie_file)response = s.post('https://api.worldquantbrain.com/authentication')cookie = cookiejar.Cookie(name='ace_expire_at',value=str(int(time.time() + response.json()['token']['expiry'])),domain='worldquantbrain.com',path='/',version=0,port=None,port_specified=False,domain_specified=True,domain_initial_dot=False,path_specified=True,secure=True,expires=None,discard=True,comment=None,comment_url=None,rest={'HttpOnly': None}, # 可选：额外参数rfc2109=False)s.cookies.set_cookie(cookie)s.cookies.save(ignore_discard=True, ignore_expires=True)
> ```

然后需要登录状态请求的话，就可以使用如下代码加载。

> ```
> s = requests.Session()cookie_file='../session_cookies.txt's.cookies = cookiejar.LWPCookieJar(cookie_file)s.cookies.load(ignore_discard=True, ignore_expires=True)
> ```

最后，要保持登录状态不失效，就需要使用 **定时任务** 每3小时，执行下保存cookie文件的代码；或者结合2中的程序不退出的框架实现。

2. 程序保持一直运行，并能安全退出的代码框架

用如下代码实现后，可以通过ctrl+c中断程序运行。如果使用nohup让程序运行在后台，可以结合ps和kill命令，实现程序退出。

> import logging
> import signal
> import time
> def handle_exit_signal(signum, frame):
> """信号处理函数，用于安全退出"""
> global running
> logger.info("Received termination signal, shutting down...")
> running = False
> def main():
> global running
> logger.info("Service started, waiting for tasks...")
> # 休眠3小时=3*60*60秒
> to_sleep = 3* 60 * 60
> while running:
> try:
> # 执行一些代码
> # 然后等3小时
> time.sleep(to_sleep)
> except Exception as e:
> logger.exception(f"Service encountered an error")
> # 安全关闭
> logger.info("Service stopped.")
> if __name__ == "__main__":
> # 注册信号处理
> signal.signal(signal.SIGINT, handle_exit_signal)
> signal.signal(signal.SIGTERM, handle_exit_signal)
> main()

如果大家感兴趣，下次分享个专题，详细讲述每个模块在Linux下的实现细节。

---

## 讨论与评论 (2)

### 评论 #1 (作者: SD17531, 时间: 1年前)

很感兴趣

---

### 评论 #2 (作者: LR93609, 时间: 9个月前)

感谢分享，非常专业的帖子

我在Windows系统，用subprocess的方式，顺序执行作业

![图片](images/img_dd1abfff4b.png)

你这个自动化程度很高，学到了

你这个分析更为直接，更为高效的，看起来有点像是冒泡程序

---------------------------------------------------------------------------------------

凡是发生，皆利于我；愿我所愿，尽是美好

---------------------------------------------------------------------------------------

---

