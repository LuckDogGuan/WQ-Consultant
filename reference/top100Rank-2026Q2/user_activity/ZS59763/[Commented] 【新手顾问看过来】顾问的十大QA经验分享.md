# 【新手顾问看过来】顾问的十大QA经验分享

- **链接**: [Commented] 【新手顾问看过来】顾问的十大QA经验分享.md
- **作者**: JA75692
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

## 自我介绍

我是一名SQL boy，一位打工的牛马，对python的了解全是靠AI生成，能读懂。 目前正在消化顾问阶段的一二三阶段的代码，正在思考如何改代码，如何提升回测效率，如何快速的分析回测的alpha，思考如何自动化回测整个流程等等...感觉后面能做的还有很多，偶尔想着想着就睡着了^.^  每当看顾问的帖子，看到大佬每天好几十刀，那叫一个眼馋😋啊（目前我就一天不到2刀😭😭😭） 下面是在这1个多月中遇到的问题，和思考的内容，写成了一个QA的回答，希望对大家有帮助，另外有不对的地方，希望大家能批评指正。

## Q1：如果只跑顾问的1 2 3阶段，调整dataset，能不能跑出啊提交的因子？

能跑出来，但是很少，很多的alpha因子都是pc过不了，都在0.8往上。所以还需要调整模板。

## Q2：一天能回测多少alpha？

我目前一天回测2W左右，不知道达到了平均水平了没有，回测的慢了，希望有大佬给点建议。由于最近再参加PPAC的比赛，这个比赛限制比较低，所以最近只提交了一阶段的因子，一阶段的因子回测的效率可能会快点。

![图片](images/img_c344787196.png)

## Q3：回测的工具

买了一个最低的阿里云服务，好像是1C2G的配置，一年大概百十块，用于回测alpha够用了。

## Q4：回测代码如何分配

把1 2 3阶段和check阶段的代码进行了拆分，拆分了几个文件，跑哪个阶段，就执行哪个脚本。

![图片](images/img_846c075512.png)

## Q5：曾经尝试过 哪种回测策略？

顾问阶段是用线程池，默认是10*10。但是如果只回测一个阶段，效率就会有点慢。后来把阶段1分了 10*4，阶段2分了10*3，阶段3分了10*3。这样同时跑三个脚本，把资源利用完全，也是可以跑出来alpha的，不过大部分都是3阶段的。

## Q6：新手奖如何拿到？

目前已经拿到100刀的新手奖，这对于我来说还是很大的鼓励。这个过程应该就是成为顾问后提交10天的alpha，就会自动发放的。我当时也没具体看规则，反正就是每天能提交就提交，达到要求就会自动发放，所以，没得到的，不要着急，达到要求，总会有的。

![图片](images/img_3c1d6f472f.png)

## Q7：回测1 2 3阶段到底是个什么？

想要了解整个流程，通读1 2 3阶段的代码是必须的。我读过之后，我对整个流程的理解如下

1、阶段一：选择合适的数据集，通过api得到相对应的字段。 然后把字段放入到一阶段的模板中，生成一个alpha因子的集合。 在把这个集合整理成一个多个线程池，一个线程池有10*10个alpha因子。 最后再对线程池中的因子进行回测。

2、阶段二：通过api获取回测过的alpha因子，当然，要加入限制条件，比如加入sharpe>1,fitness>0.7，这样，就会过滤掉一些因子，得到一些因子之后，在进行剪枝，剪枝的含义是：当有字段相似的因子，就保留前5个（默认情况），因为相似的因子即使提交后，其他的因子再次提交，可能会出现 自相关性太高过不了，所以保留前5个，够用了。剪枝之后，得到一个过滤后的集合，和阶段一样，再次放到线程池中进行回测；

3、阶段三：和阶段二一样，获取因子，过滤，剪枝，然后加入在套入新的操作符，再次进行回测。这样，因子的质量可能会越来越好。

## Q8、如何快速分析回测过的alpha？

想要分析回测过的alpha，当然是把回测过的因子记录下来。记录到文件中也好，数据库也好。当然，作为一个sql boy，是热衷于数据库的。目前我使用的是mysql，见了两张表，一个alphas，一个alpha_check。第一个存储的是get_alphas api得到的results下面的所有字段，第二张表存储的是 is下面的check所有的字段。表结构如下。

```
CREATE TABLE `alphas` (  `id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `dateCreated` datetime DEFAULT NULL,  `dateModified` datetime DEFAULT NULL,  `hidden` varchar(255) DEFAULT NULL,  `code` varchar(255) DEFAULT NULL,  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,  `operatorCount` varchar(255) DEFAULT NULL,  `settings` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,  `stage` varchar(255) DEFAULT NULL,  `status` varchar(255) DEFAULT NULL,  `category` varchar(255) DEFAULT NULL,  `classifications` varchar(255) DEFAULT NULL,  `color` varchar(255) DEFAULT NULL,  `competitions` varchar(255) DEFAULT NULL,  `dateSubmitted` datetime DEFAULT NULL,  `type` varchar(255) DEFAULT NULL,  `is_check` varchar(255) DEFAULT NULL,  `check_time` datetime DEFAULT NULL,  `is_submit` varchar(255) DEFAULT NULL,  `submit_time` datetime DEFAULT NULL,  `is_pass` varchar(255) DEFAULT NULL,  `pass_time` datetime DEFAULT NULL,  `is_drawdown` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `is_fitness` varchar(255) DEFAULT NULL,  `is_investabilityConstrained` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,  `is_longCount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `is_margin` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `is_pnl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `is_returns` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `is_riskNeutralized` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,  `is_sharpe` varchar(255) DEFAULT NULL,  `is_shortCount` varchar(255) DEFAULT NULL,  `is_startDate` datetime DEFAULT NULL,  `is_turnover` varchar(255) DEFAULT NULL,  `query_start_date` varchar(255) DEFAULT NULL,  UNIQUE KEY `idx_id` (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```
CREATE TABLE `alpha_checks` (  `id` varchar(10) DEFAULT NULL,  `name` varchar(255) DEFAULT NULL,  `result` varchar(255) DEFAULT NULL,  `limit_val` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `value_val` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `themes` varchar(255) DEFAULT NULL,  `competitions` varchar(255) DEFAULT NULL,  `check_time` varchar(32) DEFAULT NULL,  UNIQUE KEY `id_name_idx` (`id`,`name`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## Q9：如何插入向两个表插入数据？

表1 alphas：写一个脚本，使用python的pymysql工具。复用之前的get_alphas api，可以得到一天中所有回测的alphas，100个一批，得到的结果转化为json，解析json，然后再写一个 insert函数，把json数据插入到数据库。数据如下。这样就可以通过sql来分析了。

![图片](images/img_75de5ba8c7.png)

![图片](images/img_d78074620e.png)

表2：alpha_checks，在顾问代码中有check的流程，我们对这块代码进入插入功能。因为回测的时候是一个alpha一个alpha进行check的，所以这个地方加入插入的操作，通过更新alphas表，当check过的alpha，更新表中的is_check=1，说明check过了，即使check阶段断了，也可以继续实现断点测试。check的时候只check is_check=0的。数据如下：

![图片](images/img_a9ce0d51e9.png)

## Q10：后续还有哪些优化点？

我也是最近刚有的想法，目前准备进行优化代码，思想如下：

当check之后的步骤，可以通过check的结果获取到alpha_id，通过alpha_id得到这个alpha_id的所有信息，sharpe、fitness、longcount等等。然后判断 sharpe、fitness，当达到条件之后，直接可以进行二阶段回测。同样，而阶段回测，也进行判断，满足条件直接进行三阶段回测。这样，就不用等待一阶段跑完，再跑二阶段，二阶段跑完跑三阶段。 实现了比较深层次的搜索过程。  这个思路不知道怎么样，请各位大佬评判一下。

好了，分享到这里结束，但是探索的过程还远远没有结束，我的思路是：最终可以搭建一个coze、n8n类似的工作流，真正的实现自动化全流程，后期只要调整相关的模板就可以了。一键修改，一键回测，一键提交，是终极目标。 所有的quant们，一起加油，希望我这个小菜鸡的思路可以帮助到大家，同时也希望大佬们也给我多点建议！ 谢谢大家！！！

---

## 讨论与评论 (7)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很有用的帖子，点赞！但同时要稍微提示一下，1g2m的跑的不是特别顺畅，卡卡的，我用的是2g4m有时候也会卡，有能力的情况下还是尽可能上高配，这样用着舒服

---

### 评论 #2 (作者: DX67257, 时间: 1年前)

非常感谢楼主分享，我是前几天获取到有条件顾问，这几天比较迷茫，不知该怎么做，通过你的分享更加清楚该怎么做了。

另外请教下，第一个问题，更换模板就是找2个或更多个数据字段，再跑1、2、3阶段，是么

---

### 评论 #3 (作者: ZT38415, 时间: 1年前)

Q10，我也想过这种做法，但是当前还没实现，我现在实现了一个基本的工作流，加入了零阶（也就是纯模板），之后筛选（我按照sharpe > 0.7, fitness > 0.5筛的）生成一阶后只跑最多2000个alpha，如果没有能升阶的就自动换到下一个预定的dataset和region。否则就一直跑完二三阶才到下一个预定dataset和region。

我当前的提交相关的是两个代码，一个用的论坛中的0误差本地自相关+自动check submission，另一个是从网页上提交一个之后对已经标注为蓝色（预备提交）的alpha进行第二次筛选。我想过里面融入最大独立集算法，但是一直在犹豫如果两个独立集大小相同应该如何评判留下哪一个，所以还没完全实现。

---

### 评论 #4 (作者: XW85841, 时间: 1年前)

已深度学习，感谢分享，再次加深了对于123阶的认识与理解。

---

### 评论 #5 (作者: JA75692, 时间: 1年前)

[DX67257](/hc/en-us/profiles/29024032470039-DX67257)  是的，我的理解是找一下有经济含义的字段组合，然后在进行跑1 2 3阶段。

---

### 评论 #6 (作者: MX83967, 时间: 10个月前)

你好，我错过顾问进阶培训了，能分享下1，2，3阶的模板代码给我吗

---

### 评论 #7 (作者: chaoxiang ao(CA87006), 时间: 1个月前)

兄弟 能分享一下这个通用的一二三阶模块代码不

---

