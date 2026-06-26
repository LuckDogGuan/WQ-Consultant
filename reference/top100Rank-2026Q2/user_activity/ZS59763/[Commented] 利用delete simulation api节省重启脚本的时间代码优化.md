# 利用delete simulation api，节省重启脚本的时间代码优化

- **链接**: [Commented] 利用delete simulation api节省重启脚本的时间代码优化.md
- **作者**: WP88606
- **发布时间/热度**: 1年前, 得票: 8

## 帖子正文

使用代码跑回测时，经常（至少本人经常【流汗】）因为写错配置或其他原因需要提前结束脚本，暴力的kill掉进程后，如果直接重启程序，因为之前simulation还在Brain后台跑，占用着卡槽，会导致location error。

然后就只能在心里默默估算后台执行结束的时间，苦苦等待，或者在代码中添加sleep，不断重试。要是有获取正在占用的卡槽数量的API就好了，就可以在发现卡槽被释放时，执行下一个任务，可惜没有。

发现前端的页面上有取消simulation的操作：

![图片](images/img_65fcaf8e3a.jpeg)

API是这个DELETE  [https://api.worldquantbrain.com/simulations/{simulation_id}](https://api.worldquantbrain.com/simulations/{simulation_id})

想到能不能在程序退出时，取消掉正在跑的simulation，这样就可以直接重启程序。实践了一下，确实可行。具体方法就是，在代码中捕获Ctrl-C(kill -2 PID)引发的异常，删除simulation，再退出。

大概是这样：

```
try:    simulation_progress_url_list = multi_simulate()except KeyboardInterrupt as e:    for simulation_progress_url in simulation_progress_url_list:        delete_simulation(simulation_progress_url)
```

使用协程有点不一样，需要在主线程中捕获`KeyboardInterrupt`，在协程中捕获`asyncio.CancelledError`。

```
# main thread
try:
    main()
except KeyboardInterrupt as e:
    pass

# coroutine
async def coroutine():
    try:
        simulation_progress_url = await multi_simulate()
    except asyncio.CancelledError:
        delete_simulation(simulation_progress_url)
        raise
```

需要注意的是，delete_simulation需要使用同步代码调用API，不然还是会被主线程取消掉。

还有这个API是删除的操作，服务器可能出于安全的考虑，对调用频率有很大的限制，不过测试连续删10个还是没问题的。

---

## 讨论与评论 (1)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很有用的方法，解决了我重启代码后一直在网页上点的问题。点赞！

---

