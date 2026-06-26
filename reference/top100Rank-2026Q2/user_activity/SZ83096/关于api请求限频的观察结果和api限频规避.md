# 关于api请求限频的观察结果和api限频规避

- **链接**: 关于api请求限频的观察结果和api限频规避.md
- **作者**: SZ83096
- **发布时间/热度**: 7个月前, 得票: 24

## 帖子正文

```
1. 首先，可以确认，每个接口，1小时2000次的请求;2. 当其中1个接口 1小时2000次的请求用完后，我观察到，【 可能 】 会影响到其他的一些接口也被限频（不确定，有时候有影响，有时候没有影响，某个接口被限频后，页面查看alpha，有些接口会触发429【比如before-and-after-performance 接口 ，很确定没有触发429，1小时内使用没有超过2000次】有些接口没有触发429 )3、以上的接口，限频后重置的时间都是相同的时间点
```

以上观察结果，可以看如下截图

![图片](images/img_3fc86c0d02.png)

![图片](images/img_83b6a8bba7.png)

![图片](images/img_d5c37e7cfa.png)

![图片](images/img_3a0e35dd05.png)

![图片](images/img_4cffbff296.png)

4、怎么合理利用好api每个小时的请求次数又不影响网页查看，操作alpha呢？

在代码中，请求api后同时检查header中频率限制的相关信息，设置一个冗余阈值，在请求次数达到冗余阈值时，请求暂时进入休眠，等待新的请求额度刷新后再恢复api请求

```
def get_headers(response):    return {'ratelimit_limit': response.headers.get('Ratelimit-Limit'),    'ratelimit_remaining': response.headers.get('Ratelimit-Remaining'),    'ratelimit_reset': response.headers.get('Ratelimit-Reset'),    'retry_after': response.headers.get('Retry-After'),    'x_ratelimit_limit_hour': response.headers.get('X-Ratelimit-Limit-Hour'),    'x_ratelimit_remaining_hour': response.headers.get('X-Ratelimit-Remaining-Hour')}在get请求后面增加代码：response = s.get(url,timeout=timeout )try:    response.raise_for_status()    ratelimit_remaining=int(get_headers(response)['ratelimit_remaining'])    ratelimit_reset=int(get_headers(response)['ratelimit_reset'])    if (ratelimit_remaining) <= 20: # 可以自定义冗余阈值        print(f"ratelimit_remaining: {ratelimit_remaining}, ratelimit_reset: {ratelimit_reset}, sleep {ratelimit_reset+60} seconds")        time.sleep(ratelimit_reset+60)
```

碎碎念： 在中午11点前不要脚本多线程api 拉取数据，或者代码里api的冗余阈值放大些，免得页面操作限频，导致没法查看要提交的alpha 了。

---

## 讨论与评论 (0)

