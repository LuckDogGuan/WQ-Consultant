# 新人小小小心得

- **链接**: [Commented] 新人小小小心得.md
- **作者**: LZ84152
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

作为新人一开始真的使用三阶段代码无脑交，没有太多思考，后来发现无脑提交的alpha质量高的不多，但又不太想为了交而交，索性开始逛起了论坛，就来说说论坛对于新人来说比较重要的一些小tip。
一、alpha 提交基础规则

对于vf0.5的新人，不知道如何评价alpha质量，可以查看这篇文章

[日赚90刀💵作为新人，我是怎么样从value factor 0.5升到0.99的？ – WorldQuant BRAIN](../JR23144/[Commented] 日赚90刀作为新人我是怎么样从value factor 05升到099的经验分享.md)

有时候有些alpha的其他内容表现都很好，但就是turnover比较高，margin较低，可以查看

[如何提高流水率？– WorldQuant 大脑](/hc/en-us/articles/20251419309719-How-to-improve-Turnover)

***删除 [对于check，要记住check只有三个槽，同时每天四个alpha提交完后，check无法运行。所以要一直check就不能一次交满4个alpha，可以选择每天更新前提前半小时交最后一个。]***

二、效率提升经验总结

即插即用的多线程提交，把它放在multi_simulate_dynamic中修改一下就好，不会直接两个代码放gpt，要他改为多线程一般也就好了。

```
import concurrent.futureswith concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:    # 当队列未空 或 存在正在运行的任务时，持续循环    while not task_queue.empty() or futures:        # 当活动任务数小于10且队列中还有任务时持续提交        while not task_queue.empty() and len(futures) < 8:            try:                task = task_queue.get(timeout=2)            except Empty:                break            # 提交任务并加入列表            times = datetime.datetime.now()            args.log_id.Info(f"processing task: {now_id}")            future = executor.submit(simulate_and_check, task, args, s, now_id)            futures.append(future)            task_queue.task_done()            now_id += 1        # 等待任意一个任务完成        if futures:            done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)            futures = list(not_done)
```

二、模板的选择

对于如何找alpha，可以看下面两个链接，一个英文和一个中文的alpha模板合集：

[【Alpha Template Collections】- Continuously Update – WorldQuant BRAIN](../CH36668/[Commented] 【Alpha Template Collections】- Continuously UpdatePinnedAlpha Template.md)

[如何找到更多alpha的思考（新手进阶篇）系列 - 第三篇：论坛内的模版 – WorldQuant BRAIN](../KZ79256/[Commented] 如何找到更多alpha的思考新手进阶篇系列 - 第三篇论坛内的模版.md)

我自己先择差不多抛弃了三阶段方式，主要是现在更新点亮dines区域的数据集点亮规则变了，现在主要尝试论坛中的模板加套一个二阶段，二阶段可以是分组，也可以是trade_when。之后就是尝试更多的一些模板的可能性。

---

## 讨论与评论 (4)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

论坛中的模版本身的op已经有点多了，再套一个阶段，有过拟合的感觉，这个需要注意啊

---

### 评论 #2 (作者: MY27687, 时间: 1年前)

关于check可以使用论坛本地check，check过多平台会限流,影响效率

[../KZ79256/本地0误差计算自相关性【即插即用版】代码优化.md](../KZ79256/本地0误差计算自相关性【即插即用版】代码优化.md)

---

### 评论 #3 (作者: MS51256, 时间: 1年前)

对于check，要记住check只有三个槽，同时每天四个alpha提交完后，check无法运行。所以要一直check就不能一次交满4个alpha，可以选择每天更新前提前半小时交最后一个。
有这个说法吗
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #4 (作者: LZ84152, 时间: 1年前)

对于check, 我交满4个ra和1个sa都没问题，仍然可以check，应该是没有这个限制了。

对于论坛中的模版本身的op已经有点多问题，再套一个会过拟合问题确实会有点，但我其实都是使用论坛中的简单模板比如 [[Alpha Template] Time-Series Sentiment Comparison Template – WorldQuant BRAIN](../CC40930/[Commented] [Alpha Template] Time-Series Sentiment Comparison TemplateAlpha Template.md) ，毕竟最近一段时间都是为了PPAC努力。

---

