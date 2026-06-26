# 【经验分享】基于 kafka-python实现Alpha表达式组装与回测解耦的解决方案代码优化

- **链接**: [Commented] 【经验分享】基于 kafka-python实现Alpha表达式组装与回测解耦的解决方案代码优化.md
- **作者**: JJ69164
- **发布时间/热度**: 1年前, 得票: 14

## 帖子正文

【经验分享】基于 kafka-python实现Alpha表达式组装与回测解耦的解决方案

### 背景（痛点）

各位量化前辈好，我是量化新人小白白，目前的努力目标是——走向有条件顾问，大佬们万一刷到我的帖子别笑话我哈，4个world终于跑完了，当然不是简单的跑脚本，主要是通过跑脚本和调整代码扩展脚本来逐步熟悉WQ的机制。自从接触到Machine后就着急忙慌的读了代码，也写了运行脚本跑了两天，但总感觉哪里不对劲？？既然有感觉咱就来点电嘛，就琢磨啊想啊怎么优化回测模式，左思右想终于感受到从在量化研究中Alpha 表达式生成与回测执行的强耦合这个常见痛点入手就对了，这次目标就定为——想实现Alpha表达式与回测解耦。
当然，结合world之旅也可以做一些改良实现，但试了几次总觉得不够高大上且稍显笨拙，之前接触过MQ(消息队列)，所以就想着怎么给派上用场，说干就干，走起…，基于Machine的一阶内容，我熬它几个通宵达旦，怕啥终究会大功告成的，今早一看真的可以看结果了哦，故此赶紧将心路历程及经验总结出来供大佬及前辈老师们斧正，也想通过发帖给跟我一样的新人能让我们新人看到一些希望！（懂的都懂，不懂千万别瞎琢磨…）

### 架构（构思）

咱们本次主旨就是解耦，有小伙伴可能不太理解啥叫解耦，大白话就是各干各活，互不干涉，降低依赖，减少频繁的手动启停任务，总之计算机又不知道累，让它别歇着，它歇的太久就把我们给歇菜了…。
重点重点重点来了，废话不多说，直接上图：

![图片](images/img_2bb518e140.png)

这图一上还有谁不知道咱们要咋干的吗？真没有的话那我就啰嗦几句，还不懂那就评论区使劲砸吧。
本系统架构逻辑也比较简单，就三大块分别是生产者、消息队列、消费者：
1.生产者：生产啥呢？就是咱们的alpha表达式，不管从哪来的，无外乎三大类：生成脚本直接生产表达式，另外就是之前生产的也好、跟老师借的也罢都无外乎要么以文件形式存放，要么存放在数据库中；喜欢那个，能用那个就尽享其用吧，最关键是拿到后要发送数据到消息队列，要不然存着会坏掉的。
2.消息队列：说白了就是数据管道，不过这个管道真的是无限大，就跟我们的毛细血管一样，只要计算资源管够就行。这里咱们就是指管理待回测alpha表达式的队列，当然你也可以把setting等放进来，但感觉没这必要。重点要说的是数据分区，也就是主题+优先级。
3.消费者：顾名思义就是要接收消息队列里的数据，并辅以数据解析，匹配处理逻辑完成一定的任务，就咱们量化因子处理逻辑来说就是装卸组装成可回测的alpha，然后将其扔进可用的槽位里爱煮爱炖随便你吧，像我们这种小白白只有三个独立槽位，优先级任务到了抢占槽位是少不了的。

这样描述之后，不懂的也茅塞顿开了吧。有人会问你最下面怎么还有一块没讲——对，你还真仔细，不过这不是咱们今天的重点，这一扒图里想说的是提交的事更加跟上面不耦合了，爱啥时候就啥时候，手工自动随便吧，我们今天做的这些事可不都是为了最终的提交嘛。

### 过程（实现）

说我是码农也好，准码农也罢，既然架构都这么干，那接下来咱就来点更干的干货，上代码时刻到。
既然咱们都是搞python的，那么咱们这里也就直接用kafka-python，具体配置啥的不用我讲了吧，要真的要要要的话那就评论区回复1000个“想要kafka-python具体配置”，如果大家真的需要我抽空可以再发个帖子给大家分享下。
来吧，麻袋准备好装代码吧，以machine一阶为例核心代码如下奉上。

1.生产者：
首先，根据machine一二阶逻辑编写脚本罗列表达式
其次，组装fo_pools为message的data，其它参数根据需要取舍就好（保证生成和消费的前后一致性）
最后，调用producer.send单次或多次发送消息机制将组装好的数据发送给消息队列。

```
#用kafka消息机制发送要处理的alpha表达式给kafka服务器def firstAlphasKafkaProducer()    s = login()   df = get_datafields(s, dataset _id='analyst4', region='UsA', universe='ToP3000', delay=1)pc_fields =process_datafields(df)   first_order =first_order_factory(pc_fields,ts_ops)print(first_order[:10])   print("生产表达式数量:%s"%len(first_order))      # 赋予alpha表达式一个初始decay   init_decay = 6   fo_alpha_list =[]   for alpha in first_order:      fo_alpha_list.append((alpha, init_decay))   #随机采样快速评结一个数据集的潜力   random.shuffle(fo_alpha_list)   print("数量:%s"% len(fo_alpha_list))   print(fo_alpha_list[:5])   # Load alphas to task pools   fo_pools =load task_pool_single(fo_alpha_list,limit of single simulations: 3)   print(fo_pools[e])   for i in range(len(fo_pools)):      message ={'id': i,'data': fo_pools[i], 'neut': 'SUBINDUSTRY', 'region': 'USA', 'universe': 'TOP3000', 'start': 0}
```

```
       producer.send('alphaxxx'，value=message)       print(f'正在发送message:{message}')       time.sleep(1) # 控制发送频率防止阻塞
```

2.消费者：
首先，从消息队列中不间断地获取数据；
其次，拿到数据后结合发送规则解析获取我们回测所需要的参数；
最后，调用回测函数进行回测就好。

```
def firstAlphasKafkaConsumer():
```

```
# 持续消费消息 try:    for message in consumer:        print(f"""            收到消息:            主题: {message.topic}            分区: {message.partition}            偏移量: {message.offset}            内容: {message.value}        """)        fo_pool = []        myData = message.value['content']['data']        # print('myData: %s'%myData)        fo_pool.append(myData)        # Simulate First Order        single_simulate(fo_pool, message.value['neut'], message.value['region'], message.value['universe'], message.value['start'])
```

```
except KeyboardInterrupt:    print("用户中断操作")finally:    consumer.close()  # 关闭消费者连接
```

到这里有朋友就说了，你咋把消息队列给漏了，其实也没漏，它就在生产者和消费者中都有，只不过消息队列肯定不能自己写嘛。（我要是能写个可以商用的消息队列出来那我就不…了）

### 效果（检验）

消费者后台打印效果如下：

收到消息:
                    主题: alphaXXX
                    分区: 0
                    偏移量: 4
                    内容: {'priority': 'normal', 'content': {'id': 465,  'data': [['group_rank(-ts_delta(winsorize(ts_backfill(anl4_ptp_flag, 120), std=4), 120),densify(pv13_r2_min2_3000_sector))', 6], ["group_neutralize(ts_sum(winsorize(ts_backfill(anl4_totassets_number, 120), std=4), 120),densify(bucket(rank(assets),range='0.1, 1, 0.1')))", 6], ['group_rank(-ts_std_dev(winsorize(ts_backfill(anl4_flag_erbfintax, 120), std=4), 240),densify(industry))', 6]], 'neut': 'SUBINDUSTRY', 'region': 'USA', 'universe': 'TOP3000', 'start': 0}}

201
{'user': {'id': 'alphaXXX'}, 'token': {'expiry': 14400.0}, 'permissions': ['TUTORIAL', 'WORKDAY']}
task 2001 post done of alphaXXX.
task 2001 simulate done of alphaXXX.
Simulate done

... ...

收到消息:
                    主题: alphaXXX
                    分区: 0
                    偏移量: 25
                    内容: {'priority': 'normal', 'content': {'id': 466, 'data': [['group_neutralize(group_neutralize(ts_zscore(rank(call_breakeven_150)/rank(enterprise_value), 10), industry),densify(pv13_r2_min2_3000_sector))', 10], ['group_neutralize(ts_sum(winsorize(ts_backfill(anl4_fcfps_number, 120), std=4), 66),densify(pv13_r2_min20_3000_sector))', 6], ["group_zscore(ts_sum(winsorize(ts_backfill(vec_avg(anl4_dei2lqfv110_item), 120), std=4), 5),densify(bucket(rank(ts_std_dev(returns,20)),range = '0.1, 1, 0.1')))", 6]], 'neut': 'SUBINDUSTRY', 'region': 'USA', 'universe': 'TOP3000', 'start': 0}}

201
{'user': {'id': 'alphaXXX'}, 'token': {'expiry': 14400.0}, 'permissions': ['TUTORIAL', 'WORKDAY']}
task 2004 post done of alphaXXX.
task 2004 simulate done of alphaXXX.

worldquantbrain平台查看回测结果如下：

![图片](images/img_b815573375.png)

```
machinePhase2 Regular UNSUBMITTED 07/ /2025 EDT USA TOP3000 0.97 5.12% 2.18%machinePhase1 Regular UNSUBMITTED 07/ /2025 EDT USA TOP3000 0.56 1.24% 28.27%
```

```
  machinePhase2 Regular UNSUBMITTED 07/ /2025 EDT USA TOP3000 1.42 6.12% 2.18%  machinePhase1 Regular UNSUBMITTED 07/ /2025 EDT USA TOP3000 -0.19 -1.69% 0.82%...
```

### 总结

经过近期的坎坎坷坷，我最想说的是——在任何领域新人都是很艰难的，在任何行业能活到最后的都是英雄。

有朋友就说了，照你这么一波操作那我们被释放出来的大把时间后面干啥子啊，来咱说点更重点的——就是挖掘新的alpha idea咯。

期待我后面早日出新帖来分享alpha idea，这个我想迟早会来的，都耐心读到这里来了，相信你会相信我的，对吧。让我们一起奔赴那个梦想吧！——“起来，不愿做韭菜的我们…。”

感谢阅读，码字不易，敬请点赞关注收藏，当然有评论也别吝啬，有您的支持和加油后续更精彩…

---

## 讨论与评论 (5)

### 评论 #1 (作者: HW85064, 时间: 11个月前)

非常有潜力的想法！如果：

1. 能写出确定alpha通过概率的算法加入消息队列之前。（由此算法确定优先级）

2. 在消费者模块中对于可能通过test的alpha进行优化。（如何写出优化算法）

将会极大提高我们的研究效率。

---

### 评论 #2 (作者: JC20351, 时间: 11个月前)

请问world是什么

---

### 评论 #3 (作者: AC38598, 时间: 11个月前)

只要有合适的alpha idea，构建alpha expression是个很快速的过程，生产者这里不用多少时间就全部执行完成了。问题是发送alpha expression到服务器进行回测，返回结果的速度太慢，所以消费者这里基本上都是难以消费完的，时间都耗在这里了。

---

### 评论 #4 (作者: WL53365, 时间: 10个月前)

你的这个想法的确是我近期很想完成的事情，感谢你能将这个想法发在论坛上，节省了我去自己解决这个问题的时间，祝你后续的alpha idea不断涌现！

---

### 评论 #5 (作者: YX23928, 时间: 10个月前)

很有趣的想法，还是第一次看到把kafka运用到alpha挖掘，可以和app_wqb结合起来，方便生成alpha表达式。

有一个小问题，在消费者进行回测的时候需要增加回测失败的解决方案，比如失败后将alpha表达式重新放到消息队列中，防止表达式回测失败后，部分alpha未回测的情况发生。

---

