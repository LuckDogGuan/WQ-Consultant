# 利用可视化选项Visulization来阅读理解数据字段经验分享

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwgXELIyiBw6D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAehodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzEzNzEyOTE2NjAzMTEtJUU1JTg4JUE5JUU3JTk0JUE4JUU1JThGJUFGJUU4JUE3JTg2JUU1JThDJTk2JUU5JTgwJTg5JUU5JUExJUI5VmlzdWxpemF0aW9uJUU2JTlEJUE1JUU5JTk4JTg1JUU4JUFGJUJCJUU3JTkwJTg2JUU4JUE3JUEzJUU2JTk1JUIwJUU2JThEJUFFJUU1JUFEJTk3JUU2JUFFJUI1BjsIVDoOc2VhcmNoX2lkSSIpMzFhZDg3NzAtNDA2YS00ZTJhLWE5YTUtOWI0NmNjZWU3YzdjBjsIRjoJcmFua2kMOgtsb2NhbGVJIgp6aC1jbgY7CFQ6CnF1ZXJ5SSIMTUc4ODU5MgY7CFQ6EnJlc3VsdHNfY291bnRpGg%3D%3D--e453475acde7f9858e520f8a23f89b4656c7c58f
- **作者**: LL87164
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

目的：多一个理解数据字段的方法，增加点阅读数据集的兴趣点。缘起：无论是培训还是一对一咨询，Kunqi老师总是强调多去读一下数据集。实际操作当中，发现很多数据字段就是一个非常简洁的描述。即使使用GPT等分析，得到的也是一些泛泛的解释。总感觉有些乏味，一时不知从何入手。碰巧在浏览一个数据集下的字段时，发现很多行业相关的风险因子的字段。如 rsk62_beta_1_100_banks : Bank Industry Beta. 字面理解应该是在银行业这个因子上的风险暴露。接下来想多尝试一些方式去进一步验证一下其属性。方法：先尝试的是用户阶段的 6 tips to explore new data，表达式（rsk62_beta_1_100_banks）下，发现 coverage 并不是预期的那样（只覆盖银行业因此覆盖率不会高）。于是想到了Setting下的Visulization选项可以按行业展示数据分布，于是打开了这个选项，发现了一些有意思的观测点，如下所示：可以看出这个字段并不是只覆盖银行业但其行业的风险系数的平均绝对值是最明显的（说最高好像有点不严谨）过了一遍其他行业在这个因子上的暴露，也可以发现另外一些有意思的点，如地产和工程行业容易想到会明显，但是 pipelines 和 office furnishings 这两个行业不太容易想到。期望以上内容作为抛砖引玉，能带来大家更多更好的方法去阅读理解数据集。最后，针对这样的 Industry Beta 数据字段，到底应该如何应用于 Alpha 的构建，也希望能得到高手们的指点。

---

## 讨论与评论 (6)

### 评论 #1 (作者: MG88592, 时间: 1年前)

平台对于很多东西的解释确实都比较简洁，对于我等0基础小白理解起来确实是后知后觉，在群里出现了很多次，终于在某天对它豁然开朗。

---

### 评论 #2 (作者: LL87164, 时间: 1年前)

MG88592除非天才，我觉得大家也都是从0起步的，服从正态分布的规律。还是得练。期望早日和您一样开悟。

---

### 评论 #3 (作者: YC99622, 时间: 1年前)

居然还有这个功能，本小白都没发现，感谢楼主分享，我得像楼主一样做研究。

---

### 评论 #4 (作者: LL87164, 时间: 1年前)

YC99622研究谈不上。顶多是找不到更好的办法时无意中蒙的。找到其他阅读理解数据字段的好方法后，记得回来和大家分享一下。

---

### 评论 #5 (作者: LL87164, 时间: 1年前)

MG88592豁然开朗谈不上，但是今天好像有那么点感觉了。

---

### 评论 #6 (作者: WT26072, 时间: 6个月前)

楼主的疑问也是我的疑问，从0开始的量化总是哪里都不懂，又懵懂的做下去，希望能有更好的研究和解读吧

---

