# 【老毛课堂】同时测10000个alpha的Prod Correlation和Self Correlation!!

- **链接**: [Commented] 【老毛课堂】同时测10000个alpha的Prod Correlation和Self Correlation.md
- **作者**: XM75236
- **发布时间/热度**: 1年前, 得票: 65

## 帖子正文

- 把下面的代码的prod改成self就是测self-correlation拉

> **温馨提示:alpha_Ids不要放太多,一次真的测10000个你当玩那!?**

```
import asyncioimport timeimport aiohttpasync def login(session):    username = ""    password = ""    auth = aiohttp.BasicAuth(username, password)    async with session.post('https://api.worldquantbrain.com/authentication', auth=auth) as response:        print(f"Login response status: {response.status}")  # 打印状态码        response_content = await response.text()        print(f"Login response content: {response_content}")  # 打印响应内容        if response.status not in (200, 201):            print("Login failed!")  # 这里是因为状态码不在成功范围内            return False  # 登录失败        return True  # 登录成功async def get_check_prod(session, alpha_id):    while True:        async with session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod") as response:            if response.status == 401:  # 检查未授权的状态码                print(f"Unauthorized access for alpha_id: {alpha_id}.")                return None  # 明确返回 None            if "Retry-After" in response.headers:                await asyncio.sleep(float(response.headers["Retry-After"]))            else:                try:                    result = await response.json()                    print({alpha_id: result['max']})                except Exception as e:                    print(f"Error for alpha_id: {alpha_id}, {e}")                returnasync def main():    async with aiohttp.ClientSession() as session:  # 在main中创建会话        if not await login(session):  # 登录并检查是否成功            return  # 如果登录失败，提前退出        alpha_ids = [            '1111111',            'aaaaaaa',        ]        tasks = []        for alpha_id in alpha_ids:            tasks.append(get_check_prod(session, alpha_id))        await asyncio.gather(*tasks)# 入口点if __name__ == "__main__":    start_time = time.time()    asyncio.run(main())    end_time = time.time()    total_time = end_time - start_time    # 转换成分钟和秒    print(f"总耗时: {total_time // 60:.0f}分{total_time % 60:.0f}秒")
```

---

## 讨论与评论 (13)

### 评论 #1 (作者: JB71859, 时间: 1年前)

太棒了大佬，这个可真多是帮了我大忙了，非常感谢大佬的分享。

---

### 评论 #2 (作者: XM75236, 时间: 1年前)

看到的朋友,欢迎点个赞啊

```
import asyncioimport timeimport aiohttpasync def login(session):    username = ""  # 这里填写用户名    password = ""  # 这里填写密码    auth = aiohttp.BasicAuth(username, password)    async with session.post('https://api.worldquantbrain.com/authentication', auth=auth) as response:        print(f"Login response status: {response.status}")  # 打印状态码        response_content = await response.text()        print(f"Login response content: {response_content}")  # 打印响应内容        if response.status not in (200, 201):            print("Login failed!")  # 这里是因为状态码不在成功范围内            return False  # 登录失败        return True  # 登录成功async def get_check_prod(session, alpha_id):    while True:        async with session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod") as response:            if response.status == 401:  # 检查未授权的状态码                print(f"Unauthorized access for alpha_id: {alpha_id}.")                return None  # 明确返回 None            if "Retry-After" in response.headers:                await asyncio.sleep(float(response.headers["Retry-After"]))            else:                try:                    result = await response.json()                    print({alpha_id: result['max']})                except Exception as e:                    print(f"Error for alpha_id: {alpha_id}, {e}")                returnasync def main():    async with aiohttp.ClientSession() as session:  # 在main中创建会话        if not await login(session):  # 登录并检查是否成功            return  # 如果登录失败，提前退出        alpha_ids = [            '1111111',  # 这里放入一些你要测的alpha的ID            'aaaaaaa',  # 注意不要放太多,一般不超过10个        ]        tasks = []        for alpha_id in alpha_ids:            tasks.append(get_check_prod(session, alpha_id))        await asyncio.gather(*tasks)# 入口点if __name__ == "__main__":    start_time = time.time()    asyncio.run(main())    end_time = time.time()    total_time = end_time - start_time    # 转换成分钟和秒    print(f"总耗时: {total_time // 60:.0f}分{total_time % 60:.0f}秒")
```

---

### 评论 #3 (作者: SY10217, 时间: 1年前)

大佬，请教下有的返回结果是none，意味着什么啊 ![图片](images/img_444f026823.png)

---

### 评论 #4 (作者: XM75236, 时间: 1年前)

[SY10217](/hc/en-us/profiles/28830404094487-SY10217)

```
 if response.status == 401:  # 检查未授权的状态码                print(f"Unauthorized access for alpha_id: {alpha_id}.")                return None  # 明确返回 None
```

可以看到,这是因为返回不是401.也就是这次访问被服务端拒绝了或直接抛弃了.
这是网络波动,或者限流导致的.在高峰期会限流,或者你测的多了也会限流.
建议一次不要测太多,每次时间有点间隔.这个跟网页端实现的效果是相同的,那儿慢一点,这个也慢一点.只是这个方便一点.
亲测,早上7-10点之间基本不会限流.

---

### 评论 #5 (作者: PN39025, 时间: 1年前)

你好，我觉得你的工具挺不错的，但是我们可以使用多进程（ `multiprocessing` ）来同时运行3个检查相关性（check corr）的任务。这可以大幅提升效率。以下是实现的方式：

### 使用  `multiprocessing`  示例

import multiprocessing
import time

# 模拟的相关性检查函数
def check_corr(task_id):
    print(f"任务 {task_id} 正在运行...")
    time.sleep(2)  # 模拟处理时间
    print(f"任务 {task_id} 完成！")
    return f"任务 {task_id} 的结果"

def main():
    tasks = [1, 2, 3]  # 任务列表
    with multiprocessing.Pool(processes=3) as pool:  # 创建一个包含3个worker的进程池
        results = pool.map(check_corr, tasks)  # 并行运行任务
    print("所有任务已完成：")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()

---

### 评论 #6 (作者: TQ88961, 时间: 1年前)

请教各位，怎么在网站里看到 alpha_id?

---

### 评论 #7 (作者: LH44620, 时间: 1年前)

“2025-02-04 16:28:14,761 - ERROR - Error for alpha_id: o6Ew3XJ, 'max'

2025-02-04 16:28:16,532 - ERROR - Error for alpha_id: mgo22gW, 'max'

2025-02-04 16:28:16,573 - ERROR - Error for alpha_id: 5QE75oz, 'max'

2025-02-04 16:28:16,573 - ERROR - Error for alpha_id: OrAwG7b, 'max'”

大佬，是不是全是这样就是被限流了

---

### 评论 #8 (作者: XM75236, 时间: 1年前)

[LH44620](/hc/en-us/profiles/26717918976919-LH44620) 
是的.理论上这跟你用别的代码check一样的,会被限流
所以你不应该一次性放太多的alpha_id

但是有点奇怪的是,我这边这个代码在大多数情况下,限流并不严重,一般50个以内都能跑的出来全部的结果

但假如你本来就在跑check代码,这时候你跑这个prod检查,很大可能会被限流
加油吧少年

Success is not achieved by merely dreaming big, but by consistently taking small, purposeful steps forward every single day, persevering through setbacks, learning from failures, and never losing sight of the ultimate goal, for it is this unwavering dedication and continuous effort that will ultimately lead you to the summit of your aspirations.

---

### 评论 #9 (作者: LH44620, 时间: 1年前)

[XM75236](/hc/en-us/profiles/27031596028951-XM75236)

还真是，当时无意间开了一个check进程，后来发现关了就好多了！

---

### 评论 #10 (作者: JR23144, 时间: 1年前)

THROTTLED  被限流之后，多久能恢复呀

---

### 评论 #11 (作者: JC15018, 时间: 8个月前)

感谢分享，正在学习降低PC的一些方法。

---

### 评论 #12 (作者: SC16582, 时间: 6个月前)

太棒了！感谢分享！

---

### 评论 #13 (作者: YW34314, 时间: 3个月前)

真的是太感谢大佬提供的check代码了，今天我就去试试。之前都是每次提交完才可以看到PC，导致提交了一些PC较高的alpha，有了这个代码，就可以优先选择那些低PC的alpha交了，对提高自己的VF也有很大的帮助。

---

