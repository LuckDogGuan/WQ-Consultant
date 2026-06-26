# 一种随机生成 SuperAlpha，进行机器回测的方式代码优化

- **链接**: [Commented] 一种随机生成 SuperAlpha进行机器回测的方式代码优化.md
- **作者**: WP88606
- **发布时间/热度**: 1年前, 得票: 35

## 帖子正文

听了之前 GrandMaster，Master 大佬们的分享，启发颇多，一个比较重要的一点是要交 SuperAlpha。自己确实只手动交过两个，再尝试就都是相关性无法通过测试，而且手动回测速度实在太慢了。

进过反复阅读 SuperAlpha 的文档，尝试，暂时想到了一种随机生成 SuperAlpha 的方式，最近连续几天都有交 SuperAlpha，可能也得益于 PowerPool 比赛的原因交了不少低相关性因子。

分享出来，算是抛砖引玉，有什么建议还请大佬们不吝赐教。

主要思路还是来自文档里的例子，发现这些 Selection 表达式，似乎都有一个共同点，就是多是一些判断条件，相乘，还有一个用来排序的权重字段（比如 turnover）。这个可以理解，判断条件返回布尔值，结果为假返回 0，为真返回 1，只有为真时表达式才有值。

所以想到，可不可以随机选择多个判断条件相乘，最后再乘上一个权重字段，构成表达式。

接下来就是创建条件列表，有哪些条件呢？

文档里提到可以给 alpha 打 tag，category，但是自己都是机器跑出来的，自己都无法判断是什么策略，还好可以交给大语言模型判断，对因子经济学含义的理解，我想大语言模型比我强多了。

还有老师培训时提供的灵感，使用以往比赛的限制条件，比如低 turnover，atom，低 correlation，当然应该也可以反过来，高 turnover，高 correlation，多尝试总没有错，反正是用机器跑。

还有一点需要指出，Selection Handling 的选择，看文档有点绕，为了简化，只使用 Positive，因为一些负数的权重，可以通过减法转换成正数。

然后构建了下面这些条件和权重表达式：
selection_expressions.py
```python
import datetime

def category_conditions():
    values = "NONE", "PRICE_REVERSION", "PRICE_MOMENTUM", "VOLUME", "FUNDAMENTAL", "ANALYST", "PRICE_VOLUME", "RELATION", "SENTIMENT"
    return [f"category == \"{value}\"" for value in values]

def color_conditions():
    values = "NONE", "RED", "YELLOW", "GREEN", "BLUE", "PURPLE"
    return [f"category == \"{value}\"" for value in values]

def dataset_conditions(dataset):
    return [f"in(datasets, \"{dataset}\")"]

def favorite_conditions():
    return [f"favorite", "not(favorite)"]

def long_count_conditions():
    return [f"long_count > universe_size(universe) * {percent}" for percent in [0.2, 0.3, 0.4, 0.5]]

def short_count_conditions():
    return [f"short_count > universe_size(universe) * {percent}" for percent in [0.2, 0.3, 0.4, 0.5]]

def name_conditions(name):
    return [f"name == \"{name}\""]

def neutralization_conditions(neutralizes):
    return [f"neutralization == \"{value}\"" for value in neutralizes]

def operator_count_conditions():
    return [f"operator_count <= {cnt}" for cnt in [1, 2, 4, 6, 8, 10]]

def tags_conditions(tag):
    return [f"in(tags, \"{tag}\")"]

def truncation_conditions():
    return [f"truncation <= {value}" for value in [0.01, 0.05, 1]]

def turnover_conditions():
    return [f"turnover < {value}" for value in [0.05, 0.1, 0.2, 0.3, 0.7]]

def universe_conditions(universes):
    return [f"universe == \"{value}\"" for value in universes]

def universe_size_conditions(size=1000):
    return [f"universe_size(universe) >= {size}"]

def datafields_conditions(field):
    return [f"in(datafields, \"{field}\")"]

def dataset_count_conditions():
    return [f"dataset_count <= {value}" for value in [1, 2, 3, 10]]

def self_correlation_conditions():
    return [f"self_correlation <= {value}" for value in [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]]

def prod_correlation_conditions():
    return [f"prod_correlation < {value}" for value in [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]]

def os_start_date_conditions():
    today = datetime.datetime.today()
    delta_days = [7, 14, 30, 60, 90, 120, 180, 360, 3600]
    dates = [(today-datetime.timedelta(day)).strftime('%Y-%m-%d')
             for day in delta_days]
    return [f"os_start_date > \"{date}\"" for date in dates]

def datacategories_conditions():
    values = "analyst, broker, earnings, fundamental, imbalance, insiders, institutions, \
        macro, model, news, option, other, pv, risk, sentiment, shortinterest, socialmedia".split(',')
    return [f"in(datacategories, \"{value.strip()}\")" for value in values]

def datacategory_count_conditions():
    return [f"datacategory_count <= {value}" for value in [1, 2, 3, 10]]

def datafield_count_conditions():
    return [f"datafield_count <= {value}" for value in [1, 2, 3, 5, 10]]

def weight_expressions():
    return [
        "turnover", '10-turnover',
        '10000-abs(long_count-short_count)', 'long_count+short_count', 'long_count', 'short_count',
        '10-dataset_count',
        '2-self_correlation',
        '2-prod_correlation',
        '100-datafield_count',
        '1'
    ]
```

接下来是随机选择条件，组装 selection 表达式的代码：

```python
import random
import selection_expressions as se
from settings import get_universe_list, get_neutralization_list

region = 'USA'
delay = 1
universe_list = get_universe_list(region)
neutralization_list = get_neutralization_list(region)
conditions = [
    se.category_conditions(),
    se.color_conditions(),
    se.neutralization_conditions(neutralization_list),
    se.universe_conditions(universe_list),
    se.datacategories_conditions(),

se.datacategory_count_conditions(),
    se.dataset_count_conditions(),
    se.datafield_count_conditions(),
    se.long_count_conditions(),
    se.short_count_conditions(),
    se.operator_count_conditions(),

se.prod_correlation_conditions(),
    se.self_correlation_conditions(),
    se.truncation_conditions(),
    se.turnover_conditions(),

se.os_start_date_conditions
]
weight_expressions = se.weight_expressions()

def find_selection_expression():
    while True:
        condition_length = random.randint(1, 4)
        condition_list = random.sample(conditions, condition_length)
        choice_conditions = []
        for condition in condition_list:
            if callable(condition):
                condition = condition()
            choice_conditions.append(random.choice(condition))
        choice_weight_expression = random.choice(weight_expressions)
        select_expression = ' * '.join([f'({exp})' for exp in (choice_conditions + [choice_weight_expression])])
        logger.info(f'random select expression: {select_expression}'    )
        selection_limit = random.choice([20, 30, 50, 70, 100])
        # 检查选择的alpha是否够十个，不然无法进行回测，页面上有这个API：/simulations/super-selection，wqb库好像没有
        response = wqb.get_super_selection(region=region, delay=delay, selection=select_expression, selection_limit=selection_limit)
        if not response or response['count'] < 10:
            continue
        return select_expression, selection_limit

```

结合 combo 表达式，生成最终的 alpha，combo 有点复杂，还不知道如何大量生成，主要使用了文档中的例子，还有 combo_a 操作符。

```python
def get_combo_code_list():
    ret = ['1',
           'stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr'
           ]
    for day in [500]:
        for algo in ['algo1', 'algo2', 'algo3']:
            code = f"combo_a(alpha, nlength = {day}, mode = '{algo}')"
            ret.append(code)
    return ret

def generate_super_alpha():
    select_expression, selection_limit = find_selection_expression()
    combo_expression = random.choice(get_combo_code_list())
    neutralization = random.choice(neutralization_list)
    return {
        'type': 'SUPER',
        'settings': {
            'instrumentType': 'EQUITY', 'region': 'USA', 'universe': 'TOP3000', 'delay': 1, 'decay': 5, neutralization: 'INDUSTRY', 'truncation': 0.08, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'OFF', 'language': 'FASTEXPR', 'visualization': False, 'testPeriod': 'P2Y', 'maxTrade': 'ON', 'selectionHandling': 'POSITIVE', 'selectionLimit': selection_limit
        },
        'combo': combo_expression,
        'selection': select_expression
    }
    return {
        "type": "SUPER",
        "settings": {

},
        "combo": combo_expression,
        "selection": select_expression
    }
```
总之，这样生成的SuperAlpha应该还是非常有限的，可能过一段时间就会枯竭了，还需要不断的添加新的低相关性的RegularAlpha才可能延续。combo表达式对PNL影响比较大，还有待学习。

---

## 讨论与评论 (21)

### 评论 #1 (作者: MH19374, 时间: 1年前)

666

---

### 评论 #2 (作者: ZZ44620, 时间: 1年前)

大佬，有具体使用的例子吗，卡在了检查选择alpha数量上

---

### 评论 #3 (作者: WP88606, 时间: 1年前)

Hi， [ZZ44620](/hc/en-us/profiles/28856702901527-ZZ44620) ，感谢评论，这个是super_selection API的一种具体实现，s是已登录的session

```
from urllib.parse import urlencodedef get_super_selection(s, region, delay, selection, selection_limit=100, selection_handling='POSITIVE'):    url = f'https://api.worldquantbrain.com/simulations/super-selection'    data = {        'settings.instrumentType': 'EQUITY',        'settings.region': region,        'settings.delay': delay,        'selection': selection,        'limit': 10,        'selectionLimit': selection_limit,        'selectionHandling': selection_handling    }    url = f'{url}?{urlencode(data)}'    return s.get(url).json()
```

---

### 评论 #4 (作者: ZH39644, 时间: 1年前)

不错，感谢大佬分享！多样化选择selection，很实用！

---

### 评论 #5 (作者: WH24469, 时间: 1年前)

感谢大佬的分享，已经跑通且出alpha了，appreciate！！！

---

### 评论 #6 (作者: QP72475, 时间: 1年前)

combo目前学习资料确实有点少，我也在摸索中。

---

### 评论 #7 (作者: XC75618, 时间: 1年前)

刚提交第一个alpha感谢大佬开源，祝愿大佬继续高base 高VF高Combined。

---

### 评论 #8 (作者: FZ60707, 时间: 1年前)

感谢大佬，启发思路了

---

### 评论 #9 (作者: AM12075, 时间: 1年前)

感谢大佬的分享，要是能大量生成combo就好了

---

### 评论 #10 (作者: ML42552, 时间: 1年前)

------------------------------

感谢大佬分享，有很大得启发性

------------------------------------------------------

祝大佬vf长虹！！

----------------------------------------------------------------------------------------------------------

---

### 评论 #11 (作者: BL59663, 时间: 1年前)

大佬，不太理解这句代码，为啥是用乘号而不是用&&， select_expression = ' * '.join([f'({exp})' for exp in (choice_conditions + [choice_weight_expression])])

---

### 评论 #12 (作者: WP88606, 时间: 1年前)

[BL59663](/hc/en-us/profiles/27001087237271-BL59663) ，你好，可以用&&替换的。在python里True和1等价，False和0等价，所以bool值也可以用乘法。Fast Expression应该也一样的。为了简化这样写的，可能没那么规范。可以改成这样:

```
select_expression = ' && '.join([f'({exp})' for exp in (choice_conditions)]) + f' * {choice_weight_expression}'
```

---

### 评论 #13 (作者: XJ58115, 时间: 11个月前)

各位前辈，我这边遇到一个小麻烦：
“import selection_expressions as se” 提示找不到 selection_expressions 模块。
我对这个模块不太熟悉，恳请有经验的朋友指点一二，不胜感激！

---

### 评论 #14 (作者: WA25180, 时间: 10个月前)

感谢分享，多多学习

---

### 评论 #15 (作者: JL66317, 时间: 9个月前)

感谢大佬的分享

---

### 评论 #16 (作者: BW88106, 时间: 9个月前)

大佬，from settings import get_universe_list, get_neutralization_list，这个settings在哪能找到啊？

---

### 评论 #17 (作者: WP88606, 时间: 9个月前)

BW88106，你好，在下面这个帖子里有，因为主要还是分享思路，所以不重要的地方就没有写。 [https://support.worldquantbrain.com/hc/en-us/community/posts/28319076128407-%E5%86%99%E4%BA%86%E4%B8%80%E4%B8%AA%E8%8E%B7%E5%8F%96%E6%89%80%E6%9C%89%E5%8F%AF%E8%83%BDsettings%E7%9A%84%E5%87%BD%E6%95%B0](https://support.worldquantbrain.com/hc/en-us/community/posts/28319076128407-%E5%86%99%E4%BA%86%E4%B8%80%E4%B8%AA%E8%8E%B7%E5%8F%96%E6%89%80%E6%9C%89%E5%8F%AF%E8%83%BDsettings%E7%9A%84%E5%87%BD%E6%95%B0)

---

### 评论 #18 (作者: CW49566, 时间: 7个月前)

虽然没看懂，但还是感谢大佬分享，再学习一下基础后再来学习。

---

### 评论 #19 (作者: YM62606, 时间: 7个月前)

目前还在学习，不会组组SA，提交的顾问因子也不到100个呢！

---

### 评论 #20 (作者: CF59528, 时间: 7个月前)

感谢大神，

---

### 评论 #21 (作者: WL20457, 时间: 5个月前)

感谢大佬的分享和启发：“比如低 turnover，atom，低 correlation，当然应该也可以反过来，高 turnover，高 correlation，多尝试总没有错，反正是用机器跑”，
我曾经一度陷入类似的状况，之前追求Select 低prod_correlation的alpha，但是组出来的SA 的prod_correlation未必就低了，有时候适当放开prod_correlation，居然也有意想不到的的收货 ，多尝试没有错的！！！

---

