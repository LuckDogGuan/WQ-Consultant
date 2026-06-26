# 写给数据库新人的MongoDB教程，存储回测数据，查询。。。代码优化

- **链接**: 写给数据库新人的MongoDB教程存储回测数据查询代码优化.md
- **作者**: LW67640
- **发布时间/热度**: 1年前, 得票: 62

## 帖子正文

搜索了论坛里关于数据库的帖子，都是SQL类型的数据库，对数据库新人不太友好，MongoDB可以直接存储json数据，无需设计复杂的表结构，上手的难度比较低，想上数据库，但没有数据库基础的顾问们可以试试看。也请对Mongo熟悉的大佬们多多回复讨论。

MonogoDB的安装分为三种，直接官网下载安装包，Mac系统使用Brew安装，或者使用Docker安装。如果之前没有安装过Mongo，这三种方式选择一种即可。

我是mac系统，mongo的版本太老，通过brew升级后，运行总是报错。现在使用的是Dokcer方式。

Mongo安装好后，可以直接通过Pandas来操作，避免了学习Mongo语法的问题。可以参考下面的代码。

关于存储回测数据，可以参考HQ17963的帖子，如果云电脑的存储和性能都够强，亦或者本地电脑24小时开机，里面的代码直接复制运行即可。如果不满足上述两个条件，我的解决方法是服务器24小时定时获取回测数据，本地电脑通过脚步同步。

[分享自己实现的alpha数据库，一行代码保存所有alpha，并进行灵活查询！](/hc/zh-cn/community/posts/28883408702743-%E5%88%86%E4%BA%AB%E8%87%AA%E5%B7%B1%E5%AE%9E%E7%8E%B0%E7%9A%84alpha%E6%95%B0%E6%8D%AE%E5%BA%93-%E4%B8%80%E8%A1%8C%E4%BB%A3%E7%A0%81%E4%BF%9D%E5%AD%98%E6%89%80%E6%9C%89alpha-%E5%B9%B6%E8%BF%9B%E8%A1%8C%E7%81%B5%E6%B4%BB%E6%9F%A5%E8%AF%A2)

同步是通过Rsync增量同步的方式，脚本如下：

```
#!/bin/bash# 文件名: sync_alpha_db.sh# 功能: 从远程服务器同步Alpha数据库到本地# 远程服务器信息REMOTE_USER=""REMOTE_SERVER=""REMOTE_PATH="./sim_alpha_database"LOCAL_PATH="./sim_alpha_database"# 日志文件LOG_FILE="./sync_log.txt"# 记录开始时间echo "========================================" >> "$LOG_FILE"echo "同步开始于 $(date)" >> "$LOG_FILE"# 确保本地目录存在mkdir -p "$LOCAL_PATH"# 使用rsync进行增量同步# -a: 归档模式，保留所有文件属性# -v: 详细输出# -z: 压缩传输# --progress: 显示进度# --delete: 删除本地存在但远程不存在的文件（可选，取决于您是否希望完全镜像）rsync -avz --progress "$USER@$SERVER:$REMOTE_PATH/" "$LOCAL_PATH/" >> "$LOG_FILE" 2>&1# 检查同步结果if [ $? -eq 0 ]; then    echo "同步成功完成于 $(date)" >> "$LOG_FILE"else    echo "同步失败于 $(date)" >> "$LOG_FILE"fiecho "========================================" >> "$LOG_FILE"
```

```
import pandas as pdfrom pymongo import MongoClient# 连接到 MongoDB 服务器client = MongoClient('localhost', 27017)# 选择数据库和集合db = client['alpha_sim']collection = db['sim_alpha_result']
```

```
region = 'GLB'universe = 'MINVOL1M'# region = 'EUR'# universe = 'TOP2500'# region = 'USA'# universe = 'TOP3000'code = 'anl'sharpe_threshold = 0.9fitness_threshold = 0.6pipeline = [    {        "$match": {            # "settings.region": region,            # "settings.universe": universe,            "regular.code": {"$regex": code},            "is.sharpe": {"$gt": sharpe_threshold},            "is.fitness": {"$gt": fitness_threshold}        }    },    {        "$addFields": {            "abs_sharpe": {"$abs": "$is.sharpe"},            "abs_fitness": {"$abs": "$is.fitness"}        }    }]# 执行管道查询cursor = collection.aggregate(pipeline)# 将结果转换为 DataFramedf = pd.DataFrame(list(cursor))# 关闭连接client.close()
```

---

## 讨论与评论 (7)

### 评论 #1 (作者: LG87838, 时间: 1年前)

感谢楼主的分享，您发的帖子里只是把回测数据保存到了pkl文件里，应该还少一步转存到数据库里把。不过现在有GPT，实现起来并不复杂。

另外，请教一下楼主，我现在的回测记录大约有400万条，担心查询的速度，您查询的效率如何？

-----------------------------------------不混信号，多样性，健壮性-------------------------------------------------------

---

### 评论 #2 (作者: QP72475, 时间: 1年前)

感觉很高大上的样子，有空研究一下。

---

### 评论 #3 (作者: BL59663, 时间: 1年前)

看完帖子准备自学数据库了

---

### 评论 #4 (作者: AH18340, 时间: 1年前)

感谢您的分享，个人见解，不管是使用mysql与mongodb,都是可以解决我们存储数据的要求。但是数据库除了存数据，还有查数据这块。wq平台会有不同比赛，不同theme,对应的查询语句可能就不同了。个人还是建议新手可以去网上学一下数据库的增删改查语法，只有掌握这个工具，才能更好的使用这个工具。

---

### 评论 #5 (作者: QZ67721, 时间: 1年前)

个人感觉mongodb的优势在于每次下载的数据相对完整，因为平台经常往给我们返回的数据里面加东西，如果是MySQL，那就只存储需要的字段内容，随着平台增加数据，可能需要下载新的内容，这样的话，需要修改自己的数据可以结构，就很麻烦。比如最近出的Maxtrade， 原先的alpha是没有这个的， 现在需要使用到他的时候，就需要去往自己的数据库增加maxtrade相关的字段，然后才能对他进行操作。如果是mongodb，只需要全量下载一次新的数据就行了，然后在代码阶段进行修改，会方便不少。另外就是，mongodb因为数据齐全，所以在mysql数据库缺少数据而导致需要重新从服务器下载数据的时候，mongodb只需要修改代码，直接从原先的数据库获取数据即可，方便很多。可惜我一直用的是mysql，现在下载一次数据到mongodb也要花好多时间。希望以后能更好对数据库进行管理吧。

---

### 评论 #6 (作者: EL94401, 时间: 1年前)

感谢分享。mongo作为文档型数据库，无疑对存储alpha，pnl等各种文档类型数据是更好的选择。保持原有文档的内容和结构。这个是MYSQL的关系型数据库无法比拟的。虽然带来一定的数据冗余性，但是对于多数是读操作，少更新的情况很适合。

但mongo的语法有些晦涩难懂，尤其对于一些aggregate等的聚合操作，虽然性能很高。但是对于我们alpha分析场景，有些大材小用，毕竟数据量有限。可以将mongo的数据，进行初步的过滤后，转移到pandas上操作。这样我们属于pandas的skllset，也可以更为方便用于其他场景。

另外，mongo需要建立索引，否则虽然数据增多，会有显著性能下降。也同样存在类似mysql等关系数据库，全表扫描的问题。

---

### 评论 #7 (作者: HW93328, 时间: 1年前)

感谢楼主的分享！我最近也是在研究数据库相关的内容，感觉mongodb数据库比传统关系型数据库mysql要灵活很多，对于mysql数据库设计表字段来存放alpha的数据是一个很考验能力的事情，比如regular alpha和super alpha中的字段信息就可能不同。

-----------------------------------------高sharpe，高fitness，高margin-------------------------------------------------

---

