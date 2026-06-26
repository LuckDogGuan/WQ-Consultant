# [代码踩坑]回测偶然卡住不动的解决方法经验分享

- **链接**: [Commented] [代码踩坑]回测偶然卡住不动的解决方法经验分享.md
- **作者**: HQ17963
- **发布时间/热度**: 1年前, 得票: 31

## 帖子正文

许多新人会遇到回测卡住不动的情况，有两个可能的原因：

1. 有的回测就是一直不结束

解决方法：保存回测开始时间，如果回测超过半小时，就跳过该回测。

2. 网络或服务器原因

默认情况下， `requests的get()或者post()`  不会设置超时时间。如果目标服务器没有响应或响应非常慢，程序会一直等待，直到服务器返回数据或连接中断。

解决方法：加timeout参数

在每次get和post时，添加参数：

response = session.get(url, timeout=30)

response = session.post(url, timeout=30)

---

## 讨论与评论 (4)

### 评论 #1 (作者: HQ17963, 时间: 1年前)

针对第二种情况，还有一种一劳永逸的方法，即修改login函数：

> last_login_time=0
> s=None
> def login():
> global last_login_time,s
> if time.time()-last_login_time<300:
> return s
> with open("./brain_credentials.txt") as f:
> username, password = eval(f.readline())
> if s is None:
> # Create a session to persistently store the headers
> s = requests.Session()
> # 添加超时，避免一直卡住
> #  [https://github.com/psf/requests/issues/2011#issuecomment-490050252](https://github.com/psf/requests/issues/2011#issuecomment-490050252)
> **s.request = functools.partial(s.request, timeout=30)**
> # Save credentials into session
> s.auth = (username, password)
> # Send a POST request to the /authentication API
> while True:
> try:
> response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')
> except:
> traceback.print_exc()
> sleep(10)
> continue
> break
> print(response.content)
> last_login_time=time.time()
> return s

重点在于加粗的行，其原理为修改get/post调用依赖的request函数，自动加上timeout参数。

---

### 评论 #2 (作者: ZS59763, 时间: 1年前)

感谢你的分享，很有用的方法，点赞！

---

### 评论 #3 (作者: DZ31817, 时间: 1年前)

20250401

------------------------------------------------------------------------------------------

感谢分享，我此前也在自己的代码中采用了类似的方法，在卡住一段时间后（如10分钟）即跳过并post下一组，到目前为止运行良好。

---

### 评论 #4 (作者: BW14163, 时间: 1年前)

感谢分享,偶尔存在卡住的现象，改天继续改代码

---

