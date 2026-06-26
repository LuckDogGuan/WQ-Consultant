# 给新手跑region和dataset的小建议

- **链接**: [Commented] 给新手跑region和dataset的小建议.md
- **作者**: XX42289
- **发布时间/热度**: 1年前, 得票: 38

## 帖子正文

我是一个 ***10月25日*** 才加入顾问计划的新人，经过非常非常多的尝试，每天花费了大量时间后， ***现在因子交了167个，金字塔完成了48个。*** 

前期新人跑数据挖掘遇到的大问题就是， **region** 的选择和 **dataset** 的选择，因为每个类型的数据集和每个地区的难度都是不一样的，所以前期新人更适合选一些简单的region或者dataset。

接下来我将分享一下我个人的一些心得体会，希望对新人有所帮助。

## 首先是region的选择。

region一共有10个，分别是：USA, GLB, EUR, ASI, CHN, KOR, TWN, JPN, HKG, AMR。

```
REGION_LIST = ['USA', 'GLB', 'EUR', 'ASI', 'CHN', 'KOR', 'TWN', 'JPN', 'HKG', 'AMR']
```

他们的简单程度我认为是

ASI > USA > TWN > EUR > GLB > JPN = CHN = HKG > KOR > AMR （都是delay 1的）

## 然后是category的选择

category一共有16个，分别是：pv, fundamental, analyst, socialmedia, news, option, model, shortinterest, institutions, other, sentiment, insiders, earnings, macro, imbalance, risk。

```
DATASET_CATEGORY_LIST = ['pv', 'fundamental', 'analyst', 'socialmedia', 'news', 'option', 'model', 'shortinterest', 'institutions', 'other', 'sentiment', 'insiders', 'earnings', 'macro', 'imbalance', 'risk']
```

他们的简单程度我认为是

model > pv > analyst = fundamental > other > option > institutions = news = insiders = sentiment > macro = risk = shortinterest = socialmedia > earnings > imbalance （都是delay 1的）

另外不建议新手去做delay 0的，我跑了近50万个都没有一个可以交的。

---

## 讨论与评论 (8)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

amr确实很难跑，但架不住给的多。analyst感觉需要慎重，因为会做出一堆能提交的，但卡相关性后就一两个。

---

### 评论 #2 (作者: XZ23611, 时间: 1年前)

[ZS59763](/hc/en-us/profiles/26858512793111-ZS59763)

相关性降低大法，换group field，other455 1200个   搂一遍经常可以降下来  还能点亮other pyramid

---

### 评论 #3 (作者: XL31477, 时间: 1年前)

感谢楼主的无私分享！作为一个刚接触不久的新人，正被 region 和 dataset 的选择问题困扰，这篇帖子来得太及时了。您总结的简单程度排序很清晰，让我对从哪里入手有了方向。不过我很好奇，您是通过怎样的方式来判断这些 region 和 category 的难易程度呢？是根据跑出来的 alpha 数量，还是有其他的衡量指标？另外，对于那些较难的 region 和 dataset，您觉得在积累了一定经验后，应该从哪些方面突破会比较好呢？期待您的进一步解答，再次感谢！

---

### 评论 #4 (作者: PZ64174, 时间: 1年前)

[XZ23611](/hc/en-us/profiles/16499300380951-XZ23611)    大佬您好我想请问一下，换group field是怎么操作呢？不太清楚，我现在遇到了很多不错信号的alpha但是由于Prod Corr被卡了，看到了您的这个回答，想看看能不能解决我这个问题

---

### 评论 #5 (作者: LL83568, 时间: 8个月前)

我还是现在开始跑asi的

---

### 评论 #6 (作者: SL52857, 时间: 7个月前)

跑amr一直没跑出来

---

### 评论 #7 (作者: QM70930, 时间: 4个月前)

居然给我分配AMR,太看的起我了

---

### 评论 #8 (作者: WL27319, 时间: 1个月前)

没明白group field具体怎么换，大佬可以赐教一下吗

---

