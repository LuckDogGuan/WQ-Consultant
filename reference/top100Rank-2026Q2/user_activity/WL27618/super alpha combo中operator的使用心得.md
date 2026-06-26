# super alpha combo中operator的使用心得

- **链接**: super alpha combo中operator的使用心得.md
- **作者**: WL27618
- **发布时间/热度**: 1年前, 得票: 75

## 帖子正文

![图片](images/img_113c0d2cbd.png) 如图, combo中有两种状态, 
1. alpha: dimension是selection的个数(40为例) x dates x 所有instruments, 是把普通alpha stack之后得到的
2. output: dimension是 dates x selection个数, 意义是某天某个alpha的weight

从第一种状态转换成第二种状态有generate_stats(_)._ 和combo_a(_) 两种方式

其中两种状态能使用的operator是不同的. 如图所示, 有些是因为dimension不匹配, 有些operator是只能使用在instruments上 > <. 操作instrument和state的weight我觉得都是正常的使用方式. 有些像reduce_operator, 我目前看下来只能和self_corr搭配, 感觉使用非常受限

当然这些都是我自己的实验结果和理解, 如果有错误, 希望大家在评论区指正

---

## 讨论与评论 (3)

### 评论 #1 (作者: YX50005, 时间: 1年前)

说好了来点赞，我来了！

---

### 评论 #2 (作者: DT40395, 时间: 1年前)

感谢大佬分享，想问下大佬对于combo expression 和  selection expression 有没有推荐的搭配啊？这样看combo有点晕晕的，目前对于combo还没有研究太多，目前只会在selection表达之后资金均等分配.....希望之后在深究combo之后 和大佬多多探讨，以求得更有效的表达。每一次实验和思考都是进步呀！

---

### 评论 #3 (作者: WL27618, 时间: 1年前)

关于combo的写法:
今天在会上的补充, 原来第一阶段可以用的不仅是country, sector这些字段. 至少pv字段也可以用在instruments阶段.
还有根据我的实验, combo的最终结果是做了scale. 所以是不是即使池子里有逆向信号, 也不能给负的权重反着买?

关于combo的算法:
我之前也遍历了不少combo组合, 包括让ai提示一些有经济学意义的组合. 效果都很差, 即使有点效果, 但是选的instrument一多就失效了. 可能只用self_corr相关的有点用.

今天在群友的提示下, 稍微复刻了combo_a的算法.
if_else(ts_delay(stats.returns,250)!=0,ts_mean(stats.returns,2520)/power(ts_std_dev(stats.returns,250),2),0)

感觉之前的失败主要在于时间长度选的太保守了. combo_a累计returns的想法和为控制波动的巨大牺牲, 都给我挺大启发. 我大胆的调大了一些时间参数, 果然效果比之前好了不少.

接下来至少可以做
1. 微调combo_a的参数
2. 尝试在时间序列上加权
3. 尝试结合一些其他self_corr相关参数.

---

