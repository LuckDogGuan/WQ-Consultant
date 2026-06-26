# 使用[ClickHouse📕]建设你的大型数据库

- **链接**: [L2] 使用[ClickHouse]建设你的大型数据库.md
- **作者**: XX42289
- **发布时间/热度**: 1 year ago, 得票: 42

## 帖子正文

**ClickHouse**  是一个开源的列式数据库管理系统（DBMS），专为在线分析处理（OLAP）场景设计。ClickHouse 以其卓越的查询性能和高效的数据压缩能力而闻名，特别适合处理大规模数据的实时分析查询。

相比  **MySQL** ，ClickHouse 的列式存储和高效压缩使其在大规模数据分析场景下查询性能提升数十倍；相比  **MongoDB** ，ClickHouse 对复杂 SQL 查询和聚合操作的支持更强大，适合实时分析和高性能 OLAP 场景。

本文将持续更新，但不保证能连载完毕，因为我也是刚开始用这个东西，现学现卖

**前置准备：下载clickhouse并安装**

[[ClickHouse📕]Download and Install CK – WorldQuant BRAIN](/hc/en-us/community/posts/29266868911383--ClickHouse-Download-and-Install-CK) 

 **第一步：创建表，每一个表的内容都不一样，需要进行存储，下面是每一个你需要创建的表。** 。

[[ClickHouse📕]table: submitted – WorldQuant BRAIN](/hc/en-us/community/posts/29266765833239--ClickHouse-table-submitted)

[[ClickHouse📕]table: pnls – WorldQuant BRAIN](/hc/en-us/community/posts/29266954512663--ClickHouse-table-pnls)

[[ClickHouse📕]table: fields – WorldQuant BRAIN](/hc/en-us/community/posts/29266990090263--ClickHouse-table-fields)

[[ClickHouse📕]table: unsubmitted – WorldQuant BRAIN](/hc/en-us/community/posts/29266971586327--ClickHouse-table-unsubmitted)

第二步：导入数据

To Be Continue....

您的点赞就是我最大的动力

---

## 讨论与评论 (3)

### 评论 #1 (作者: LY71771, 时间: 1 year ago)

请问对硬件的要求高吗，我只有笔记本-64g/1tb，不知道是否适合。

---

### 评论 #2 (作者: XX42289, 时间: 1 year ago)

[LY71771](/hc/en-us/profiles/27182535393687-LY71771) 
回复同学，我的云服务器配置是2c4g 50gb
如果你的电脑比这个配置高，那么绝对没问题。。

你这个64g/1tb，完全够了，够的让我非常羡慕。。。。(⊙﹏⊙)

经过我的测算，1000万个因子也就占用大概40GB的硬盘，每次最多取几百mb的数据，不会把内存冲爆炸的，除非你多线程（我最多2个线程，我也冲不爆）

所以你放心吧。。

---

### 评论 #3 (作者: JB71859, 时间: 1 year ago)

这个做出来可以干什么，不是很懂

---

