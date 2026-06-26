# 【代码优化】解决429报错的方法

- **链接**: [Commented] 【代码优化】解决429报错的方法.md
- **作者**: JL11546
- **发布时间/热度**: 1年前, 得票: 62

## 帖子正文

最近回测频繁遇到429报错和Incorrect Authentication问题。起初看报错内容是触发了2000次/小时的频率限制，于是向着动态控制请求次数方向的优化，但经过一周的努力仍然无法避免429错误。于是我尝试了3个半小时自动重新登录的方式，目前运行了三天表现稳健，即使不做限速请求也没有出现429错误。以下是我的重登录方法：

首先建立一个子类继承自wqb.WQBSession，在子类的构造中调用wqb.WQBSession的构造

```
super().__init__((email, password), logger=logger, **kwargs)
```

并初始化一个属性

```
self._last_auth_ts = 0
```

然后定义重登录的方法：

```
def ensure_authenticated(self, force: bool = False) -> None:now = time.time()if force or now - self._last_auth_ts > 12600:self.logger.warning("认证可能过期，正在强制刷新 session...")try:self.delete_authentication()self.post_authentication()self.logger.info("Session 已成功刷新")except Exception as e:self.logger.error(f"刷新 session 失败: {e}")self._last_auth_ts = now
```

在每次执行与平台交互的操作（如  `get` 、 `post` 、 `patch` ）之前，先调用  `ensure_authenticated()` ，以确保会话仍处于有效状态。

注：以上代码只在wqb框架下测试有效不确保其他方法可用。

以上是我为解决 429 问题所做的研究和实现过程，如果这些内容能对其他顾问有所帮助，我会感到非常高兴，祝各位研究和投资顺利。💹

---

## 讨论与评论 (7)

### 评论 #1 (作者: QP72475, 时间: 1年前)

我也遇到过这个问题，目前用的解决方法是创建多个session轮流使用，也可以解决问题。

---

### 评论 #2 (作者: LA79055, 时间: 1年前)

请问博主该操作是限于一个程序（py）中吗？
如果启动多个py程序是否仍会因为API调用限制而再次出现429的报错？

---

### 评论 #3 (作者: JR23144, 时间: 1年前)

wqb 在10* 10 回测的时候，为啥没有打印出 回测进度

---

### 评论 #4 (作者: WL13229, 时间: 1年前)

[JR23144](/hc/en-us/profiles/28844048981143-JR23144)  可以到wqb作者帖子下提问

---

### 评论 #5 (作者: JL11546, 时间: 1年前)

/hc/zh-cn/profiles/28845324426135-LA79055  [LA79055](/hc/en-us/profiles/28845324426135-LA79055)

经过测试多个.py文件不受影响，不会报错。

---

### 评论 #6 (作者: JL11546, 时间: 1年前)

[JR23144](/hc/en-us/profiles/28844048981143-JR23144)

1. 目前平台回测卡槽限制为8个，所以未来只能使用10*8个回测；
2. concurrent_simulate返回的是一个结果的列表，例如 [<Response 200 OK>, <Response 200 OK>, RuntimeError("error message"), ...]，如果你想要打印回测进度需要自己写on_success函数，然后作为参数传入concurrent_simulate。

---

### 评论 #7 (作者: KM49592, 时间: 1年前)

最近用WQB也经常遇到429问题，感谢大佬的思路

---

