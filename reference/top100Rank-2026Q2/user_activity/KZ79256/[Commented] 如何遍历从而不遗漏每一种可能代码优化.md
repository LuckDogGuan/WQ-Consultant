# 如何遍历，从而不遗漏每一种可能？代码优化

- **链接**: [Commented] 如何遍历从而不遗漏每一种可能代码优化.md
- **作者**: XX42289
- **发布时间/热度**: 1年前, 得票: 30

## 帖子正文

同一个alpha表达式，可以在不同的情况下进行simulate，举一个简单的例子。比如因子a在Region为USA的时候效果良好，但是在Region为ASI时可能效果很差，但是如果你只回测了ASI的情况，可能就会错过这个 **局部最优** 的因子。因此就需要一个较全面的遍历。

而这些配置有非常多，包括Region，Delay，InstrumentType，Universe，Truncation，Neutralization，Decay等等。其中影响最大的是Region，Delay，InstrumentType，Universe，因此以这些作为循环的结构。

```
for region in REGION_LIST:    for delay in DELAY_LIST:        for instrumentType in INSTRUMENT_TYPE_LIST:  # INSTRUMENT_TYPE_LIST:            for universe in UNIVERSE_DICT["instrumentType"][instrumentType]['region'][region]:
```

以下是普通顾问可以接触到的列表，可以用于循环

```
REGION_LIST = ['USA', 'GLB', 'EUR', 'ASI', 'CHN', 'KOR', 'TWN', 'JPN', 'HKG', 'AMR']DELAY_LIST = [1, 0]INSTRUMENT_TYPE_LIST = ['EQUITY', 'CRYPTO']UNIVERSE_DICT = {    "instrumentType": {        "EQUITY": {            "region": {                "USA": [                    "TOP3000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500",                ],                "GLB": [                    "TOP3000", "MINVOL1M",                ],                "EUR": [                    "TOP1200", "TOP800", "TOP400", "ILLIQUID_MINVOL1M",                ],                "ASI": [                    "MINVOL1M", "ILLIQUID_MINVOL1M",                ],                "CHN": [                    "TOP2000U",                ],                "KOR": [                    "TOP600",                ],                "TWN": [                    "TOP500", "TOP100",                ],                "HKG": [                    "TOP800", "TOP500",                ],                "JPN": [                    "TOP1600", "TOP1200",                ],                "AMR": [                    "TOP600",                ]            }        },        "CRYPTO": {            "region": {                "GLB": [                    "TOP50", "TOP20", "TOP10", "TOP5",                ]            }        }    }}
```

可以把已经simulate过的alpha表达式保存到文件里，下一次就不会重新去计算。

命名格式可以是

```
f"{region}_{delay}_{instrumentType}_{universe}.txt"
```

---

## 讨论与评论 (8)

### 评论 #1 (作者: KZ79256, 时间: 1年前)

我想问一下

```
INSTRUMENT_TYPE_LIST = ['EQUITY', 'CRYPTO']
```

中的CRYPTO是新的运算逻辑吗，是更高级的用户可以用的吗

---

### 评论 #2 (作者: XX42289, 时间: 1年前)

CRYPTO是数字货币的数据，目前应该是只能用到EQUITY股票的数据的。所以可以先注释掉或者删掉

---

### 评论 #3 (作者: QJ65938, 时间: 1年前)

这个代码应该放到哪个位置

---

### 评论 #4 (作者: QY51391, 时间: 1年前)

请教一下那这个的思路就是在找到某个可提交alpha后遍历其的所有可能性，然后再提交？因为有的数据集不是每个地区都有数据，也就是正常在走完一个alpha筛选流程后对于待提交alphas库所做的一种遍历？但是这样做的alphas能再找到的比率大概是多少？

---

### 评论 #5 (作者: GZ81958, 时间: 10个月前)

确实应该这样，之前老是手动的去试中性化，和universe 之类的，这个过程应该是需要自动化的

---

### 评论 #6 (作者: BZ93061, 时间: 9个月前)

好思路

---

### 评论 #7 (作者: CS14313, 时间: 9个月前)

借鉴了，这样做确实可以把最优的找出来，不放过任何一种潜在可能性。

---

### 评论 #8 (作者: LZ25854, 时间: 7个月前)

感谢楼主的分享，这个思路对我帮助也挺大。之前我手动调 Region、 Delay ，效率很低，现在有了脚本就可以实现自动化，最大概率的避免了把一些局部最优的 alpha 直接筛掉的可能性。而且把 Region、Delay、InstrumentType、Universe 这些最关键的维度挑出来循环跑，我觉得对新手来说是很重要的“方向感”。
还有两个问题：
1）实际跑这些组合的时候，需要限制循环数量吗？组合太多，会不会导致很长时间都跑不完？
2）如果同一个表达式在某些配置下很好、某些配置下很差，我们应该继续优化，还是直接换表达式？

---

