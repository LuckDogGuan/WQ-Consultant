# 【新人指南】SA 从入门到进阶，使用 ACE 工具构建与回测 SuperAlpha：代码实战指南论坛精选

- **链接**: [Commented] 【新人指南】SA 从入门到进阶使用 ACE 工具构建与回测 SuperAlpha代码实战指南论坛精选.md
- **作者**: MH33574
- **发布时间/热度**: 1年前, 得票: 44

## 帖子正文

## 一、前置准备：ACE 工具包结构概览

BRAIN 平台提供的 ACE（Alpha Creation Engine）工具包，支持用户使用 Python 自动化构建、模拟并分析 Alpha 与 SuperAlpha 策略。可以从 BRAIN 平台  `Learn`  页面左下角的  `Documentation for ACE API Library`  下载。

典型包含以下文件：

文件名
功能

 `ace_lib.py` 
     核心交互函数，用于创建与提交表达式

 `helpful_functions.py` 
    补充函数，支持结果格式化、数据提取

 `how_to_use.ipynb` 
    使用示例， **第五部分专门展示 SuperAlpha 用法** 

 `requirements.txt` 
    所需依赖模块

 `README.md` 
    安装与环境配置说明

## 二、初始化会话

```
from ace_lib import start_session

session = start_session()

```

## 三、构建一个基本的 SuperAlpha 表达式

```
from ace_lib import generate_alpha

alpha_data = generate_alpha(
    alpha_type='SUPER',
    selection='fitness > 2 && turnover < 0.2',
    combo='1',
    selection_limit=30,
    selection_handling='POSITIVE',
    region='USA',
    universe='TOP3000'
)

```

说明：

- `selection`  为筛选表达式；
- `combo`  为组合权重表达式（此处为等权）；
- 其他参数对应于平台回测设置。

## 四、运行 Selection 测试（避免长时间无效回测）

```
from ace_lib import run_selection

run_selection(session, {
    'selection': 'fitness > 2 && turnover < 0.2',
    'selectionLimit': 30,
    'selectionHandling': 'POSITIVE',
    'settings.delay': 1,
    'settings.region': 'USA',
    'settings.instrumentType': 'EQUITY'
})

```

返回的是所有被选中的 Alphas 列表，可提前判断表达式是否筛选出足够数量的有效 Alpha。

## 五、提交回测并获取结果

```
from ace_lib import simulate_single_alpha
from helpful_functions import prettify_result

result = simulate_single_alpha(session, alpha_data)
prettify_result([result])

```

支持以 DataFrame 格式返回关键指标，便于与平台界面对比分析。

## 六、构建更复杂的 Combo 表达式

```
alpha_data = generate_alpha(
    alpha_type='SUPER',
    selection='fitness > 2',
    combo="""
        stats = generate_stats(alpha)
        ir = ts_ir(stats.returns, 250)
        ir * (1 - stats.turnover)
    """,
    selection_limit=30,
    region='USA'
)

```

此处  `generate_stats()`  提取各 Alpha 在组合中的 daily return 数据，结合 IR 与换手率进行动态加权。

## 七、批量构建多个 SuperAlpha 组合用于策略研究

```
alpha_list = [
    generate_alpha(alpha_type='SUPER', selection='fitness > 2', combo='1'),
    generate_alpha(alpha_type='SUPER', selection='prod_correlation < 0.5', combo='1 - reduce_max(self_corr(generate_stats(alpha).returns, 500))'),
    generate_alpha(alpha_type='SUPER', selection='turnover < 0.3', combo='ts_ir(generate_stats(alpha).returns, 250)')
]

```

```
from ace_lib import simulate_alpha_list
results = simulate_alpha_list(session, alpha_list)
prettify_result(results)

```

支持构建表达式矩阵，并统一回测、比对结果，用于表达式优化与调参。

## 八、典型表达式模板示例（Selection + Combo）

### Selection 表达式模板

用法
表达式

表现与稳健性
 `(fitness > 2) * (1 - self_correlation)` 

多因子加权
 `0.6 * (1 - turnover) + 0.4 * (1 - prod_correlation)` 

全球中性化
 `neutralization == "COUNTRY" && os_start_date <= "2022-01-01"` 

外部 Alpha

 `not(own)` （需配额）

自有优先权
 `(turnover < 0.2) + 100 * own` 

### Combo 表达式模板

用法
表达式

等权
 `1` 

基于信息比
 `ts_ir(generate_stats(alpha).returns, 250)` 

惩罚高相关
 `1 - reduce_max(self_corr(generate_stats(alpha).returns, 500))` 

加权组合
 `ir * (1 - stats.turnover)` 

## 九、常见问题排查

问题
可能原因

模拟结果为 0 个 Alpha
表达式过于严格，或未正确设置  `selection_handling` 

表现平淡无波动
combo 表达式缺乏有效权重区分，建议使用  `generate_stats`  进行因子构造

模拟失败但无报错
检查  `selection_limit`  是否低于 10，或是否违反 Operator Count 限制（8000）

无法使用非自有池
须先提交 1 个自有池 SuperAlpha，或使用  `own`  限定表达式范围

## 十、建议工作流

1. 用 Selection 表达式设计多个子策略筛选逻辑（标签 + 指标）；
2. 通过 Run Selection 快速检验表达式是否生效；
3. 构造多个 Combo 权重函数，组合不同策略维度；
4. 使用  `simulate_alpha_list`  批量测试，选择最佳组合结构；
5. 固定 Universe、Region 与 Neutralization，优化权重函数；
6. 对比等权组合作为 baseline，确保组合表达式具备有效性；
7. 利用平台反馈与评分机制，构建长期组合研究体系。

## 十一、结语

借助 ACE 工具，研究者可以突破平台界面限制，系统化地构建、回测与优化 SuperAlpha 策略。这不仅加速了表达式调参流程，也为更高阶的策略管理、组合研究与平台成长提供了结构化路径。

建议顾问在构建 SuperAlpha 策略时，将 ACE 作为主要实验与迭代平台，在逻辑稳定后，再通过平台界面提交关键策略，形成完整的策略研发闭环。

---

## 讨论与评论 (22)

### 评论 #1 (作者: BW14163, 时间: 1年前)

讲的很全面，看了之后深受启发

---

### 评论 #2 (作者: DX67257, 时间: 1年前)

谢谢大佬分享，学习到了

---

### 评论 #3 (作者: WW42444, 时间: 1年前)

写的非常好，如果我交第一个SA之前看的话能省很多时间

---

### 评论 #4 (作者: ZK23637, 时间: 1年前)

感谢大佬分享。

```
from ace_lib import run_selection
```

gold级别的顾问的ace_lib里面好像没有 `run_selection` 这个函数，可以分享一下吗。

---

### 评论 #5 (作者: BJ10003, 时间: 1年前)

整个帖子说的内容非常到位，写的太棒了。就需要读一读这样的帖子来进行super alpha的学习，初入门的萌新对于SA有太多不清楚的点，比如怎么进行多个selection 和com 的组合等等，这一块有太多需要学习，这个内容像及时雨解决了燃眉之急，点赞！！！

---

### 评论 #6 (作者: AH18340, 时间: 1年前)

感谢大佬分享，学到了

---

### 评论 #7 (作者: JR23144, 时间: 1年前)

厉害呢 学到了

---

### 评论 #8 (作者: AM12075, 时间: 1年前)

请问代码可以直接跑然后回测sa吗？

---

### 评论 #9 (作者: DZ31138, 时间: 1年前)

下载了没有第五部分，哭泣

---

### 评论 #10 (作者: LQ69554, 时间: 1年前)

感谢大佬分享，学到了😊😊😊

---

### 评论 #11 (作者: FF24581, 时间: 1年前)

谢谢大佬分享，正在为开始super alpha而苦恼。

---

### 评论 #12 (作者: XW38100, 时间: 10个月前)

活到老，学到老

---

### 评论 #13 (作者: SX13432, 时间: 9个月前)

感谢大佬分享，小gold从学习ace_lib开始，从0到1

---------------------------------------------------------------------------------------------------------------

可以从 BRAIN 平台  `Learn`  页面左下角的  `Documentation for ACE API Library`  下载。

----------------------------------------------------------------------------------------------------------------

---

### 评论 #14 (作者: SX13432, 时间: 9个月前)

补充一句：

Apart from the IDEs you might need some specific packages which we have recommended in the requirements.txt file A simple 'pip install -r requirements.txt' in the command line will install these packages for you.

除了集成开发环境，你可能还需要一些特定的包，这些包我们已在requirements.txt文件中推荐。在命令行中简单输入“pip install -r requirements.txt”即可为你安装这些包。

---

### 评论 #15 (作者: JL66317, 时间: 7个月前)

感谢大佬分享，学到了😊😊😊

---------------------------------------------------------------------------------------------------------------

可以从 BRAIN 平台  `Learn`  页面左下角的  `Documentation for ACE API Library`  下载。

----------------------------------------------------------------------------------------------------------------

---

### 评论 #16 (作者: WF91159, 时间: 7个月前)

感谢分享

---

### 评论 #17 (作者: CQ55469, 时间: 5个月前)

感谢分享

---

### 评论 #18 (作者: BX86068, 时间: 5个月前)

感谢分享，对于我的super alpha 很有帮助，但有个问题，selection那里我打fitness平台无法识别，请问这是权限的问题吗

---

### 评论 #19 (作者: JC31003, 时间: 5个月前)

太感谢了,手搓的质量都不怎么样

---

### 评论 #20 (作者: BX86068, 时间: 4个月前)

感谢楼主的分享，但是为什么how to use的文件里没有第五部分，整个文件讲的都是regular alpha，以后官方还会补吗

---

### 评论 #21 (作者: LC79929, 时间: 1个月前)

感谢分享，虽然还有一些没看懂，但大概理解了意思

===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================

---

### 评论 #22 (作者: XH28239, 时间: 1个月前)

感谢，学到了，刚开始做superalpha，一头雾水，现在可以慢慢学

---

