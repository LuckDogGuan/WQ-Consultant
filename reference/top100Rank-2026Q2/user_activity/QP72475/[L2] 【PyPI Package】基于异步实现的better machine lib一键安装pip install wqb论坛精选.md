# 【PyPI Package】基于异步实现的better machine lib，一键安装pip install wqb论坛精选

- **链接**: [L2] 【PyPI Package】基于异步实现的better machine lib一键安装pip install wqb论坛精选.md
- **作者**: HD44583
- **发布时间/热度**: 1年前, 得票: 78

## 帖子正文

分享网络好工具之 **wqb** ！

**仓库 / 下载 / 更新 / 用法：** 
 **PyPI:**   [pypi.org/project/wqb](https://pypi.org/project/wqb/) 
 **GitHub:**   [github.com/rocky-d/wqb](https://github.com/rocky-d/wqb)

- 使用前请认真阅读README.md
- 核心类wqb.WQBSession继承requests.Session，兼容machine_lib.py
- 自动认证机制，再也无需担心session过期
- 日志完善INFO & WARNING，log文本文件+控制台输出
- 方法涵盖Datasets, Fields, Alphas, Simulate, Check, Submit
- 核心methods基于异步实现，效率提升显著（相比旧machine_lib.py）
- 更多methods等你探索
- 如遇问题欢迎在GitHub仓库中提Issues

USA/1/TOP3000 实测约 50k/天（下图右侧部分，对比左侧部分旧machine_lib.py效率提升约50%）

![图片](images/img_466ed006fa.png)

祝大家新春快乐，Python蛇年快乐，新的一年Alpha多多！

[👉来自其他同学的补丁👉自己更改和完善后的wqb库 – WorldQuant BRAIN](../LW67640/[Commented] 自己更改和完善后的wqb库代码优化.md)

---

## 讨论与评论 (38)

### 评论 #1 (作者: LW67640, 时间: 1年前)

感谢大佬的代码，Readme的示例里有一个小bug，倒数第二行少了字典的key

resp = wqbs.search_operators()

# print(resp.json())

operators = [item['name'] for item in resp.json()]

# print(operators)

operators_by_category = {}

for item in resp.json():

name = item['name']

category = item['category']

if category notin operators_by_category:

operators_by_category[category] = []

operators_by_category[category].append(name)

print(operators_by_category)

---

### 评论 #2 (作者: ML56811, 时间: 1年前)

Bug Fix:

#### `wqb.WQBSession.search_operators(...) 中`

```
    if category not in operators_by_category:
        operators_by_category = []
```

#### 应该改为：

```
    if category not in operators_by_category:
        operators_by_category[category] = []
```

非常感谢博主提供的工具。

---

### 评论 #3 (作者: HD44583, 时间: 1年前)

非常感谢！GitHub仓库已更正，PyPI主页会在下个版本中更正。

---

### 评论 #4 (作者: BA51127, 时间: 1年前)

确实，这个wqb库听起来挺方便的。话说，我上次在处理数据集的时候，也遇到了类似的效率问题。有没有可能这个新库能帮上忙？ 个人感觉，自动认证机制是个亮点，之前总是被session过期搞得头疼，这个改进能省不少事。 不过...核心methods基于异步实现，效率提升显著，这个得亲自试试才知道。USA/1/TOP3000的实测数据看起来不错，大概3成的效率提升，值得一试。👍

---

### 评论 #5 (作者: XW85841, 时间: 1年前)

非常感谢提供好用的工具，但是还是不太会，是否可以帮忙打包成类似于模板代码的压缩文件，直接下载安装并替换掉原来的机械模板代码？谢谢

---

### 评论 #6 (作者: HD44583, 时间: 1年前)

不需要手动下载源码文件，像安装其他第三方库一样安装wqb就可以用了

> pip install wqb

用的时候可以直接import

> import wqb

可以参考下面的例子 - 新手课第二次作业wqb重写的版本：

[Examples · rocky-d/wqb · Discussion #3](https://github.com/rocky-d/wqb/discussions/3)

---

### 评论 #7 (作者: CT98586, 时间: 1年前)

非常感谢大佬的代码，今天简单探索了一下，我补充几点中间遇到的问题

1.这个包是基于脚本运行的，如果在jupyter环境中运行，simulate，check等调用asyncio.run()的方法会报一个

RuntimeError: asyncio.run() cannot be called from a running event loop

导致该问题的原因是Jupyter本身已经运行了事件循环，直接调用asyncio.run()会冲突

解决方法为在导入nest_asyncio 包，添加代码如下

import nest_asyncio

nest_asyncio.apply()

2.关于测试simulate部分，对参数做一个简单解释，可能大佬们都知道，主要希望也许对和我一样的小白有一定参考和帮助：对于代码

multi_alphas = wqb.to_multi_alphas(alphas, 10)

concurrency = 8

其中concurrency是并发数量，表示并发8个multi_simulate窗口，而上面的to_multi_alphas的第二个参数则是每个multi_simulate窗口有多少个单个的测试窗口从而实现高并发

3.作者提供的代码貌似在回测完alpha之后输出的resp并不直接包含sharpe，fitness等信息，需要使用locate_alpha或者filtter_alphas等功能进行进一步的定位

如有错误，还请大家指正谢谢

---

### 评论 #8 (作者: HD44583, 时间: 1年前)

感谢 [CT98586](/hc/en-us/profiles/28847461245719-CT98586) 的解释说明，我再补充下。

首先，第1点中提到的jupyter中的运行问题还有另一种方式解决，即使用Python中的await保留字。
在事件循环已经启动的情况下，可以使用
await <coroutine function>(...)
的方式直接运行一个协程函数，如：

> resps = await concurrent_simulate(multi_alphas, 8)

其次，第3点中提到的函数返回值其实涉及到这套工具的设计理念（在项目README.md中也有说明）。
与原有machine_lib.py不同，函数的返回值可能是list或者dict等类型的数据，
wqb.WQBSession主要方法的返回值统一为requests.Response或者Iterable[requests.Response]类型。
这是为了提供更加统一的交互API，并且保证了原始数据的完整性，以及后续操作的自由度，
想要访问数据可以通过requests.Response.json()结合wqb.WQBSession.locate_alpha()等方法实现。

---

### 评论 #9 (作者: XH35040, 时间: 1年前)

求助大佬，为什么我在

### Create a  `wqb.WQBSession`  object

部分输入正确的emali和password后报错为

kwargs: {'auth': <requests.auth.HTTPBasicAuth object at 0x0000021D432E7830>}
<Response [401]>:
    status_code: 401
    reason: Unauthorized

请问该如何修复，谢谢！

---

### 评论 #10 (作者: LJ69468, 时间: 1年前)

惊叹于大佬的代码功底，非常实用好用的工具。对于批量回测的方法，我对于retry这段源码不太明白，想请教一下大佬。参数max_tries默认600，看代码是遍历600次，中间没有看到任何根据回测状态compeleted中断循环的操作，看起来是循环睡眠600次，这里的逻辑不太明白，请指教。

![图片](images/img_f0e925f73a.png)

---

### 评论 #11 (作者: HD44583, 时间: 1年前)

回复 [XH35040](/hc/en-us/profiles/22086523611543-XH35040) ：

可以检查一下是否以元组的形式传递了email和password。

> import wqb
> wqbs = wqb.WQBSession(
> ('<email>', '<password>'),
> logger=wqb.wqb_logger(),
> )

如果仍有问题麻烦提供更详细的上下文以便分析。

---

### 评论 #12 (作者: HD44583, 时间: 1年前)

回复 [LJ69468](/hc/en-us/profiles/25889708694039-LJ69468) ：

感谢认可，已私聊技术细节。

（交流代码实现可以发到 [issues](https://github.com/rocky-d/wqb/issues) ，或者分享用例 [discussions](https://github.com/rocky-d/wqb/discussions) ，更加方便快捷）

---

### 评论 #13 (作者: XH35040, 时间: 1年前)

谢谢回复，但是仍是无法login，请问这和每次登入需要人脸识别有关吗？

---

### 评论 #14 (作者: HD44583, 时间: 1年前)

回复 [XH35040](/hc/en-us/profiles/22086523611543-XH35040) ：

BRAIN平台目前没有人脸识别，应该是你设备上的自动补全密码，代码跟这个没有关系。

---

### 评论 #15 (作者: YZ72256, 时间: 1年前)

感谢wqb大佬的开源分享，不知道未来有没有可能增加数据库这一功能，自己捣鼓数据库捣鼓不明白......再次感谢！

---

### 评论 #16 (作者: KB18445, 时间: 1年前)

我尝试在Alpha Machine.ipynb中使用大佬开发的wqb库

import wqb

import asyncio

import nest_asyncio

nest_asyncio.apply()

frommachine_libimport*

from asyncio.log import logger

from wqb import WQBSession

# 省略login、get_datafields、process_datafields部分

first_order = first_order_factory(pc_fields, ts_ops)

print(first_order[:10])

print(len(first_order))

# Pad initial decay with alpha

init_decay = 6

fo_alpha_list = []

for alpha in first_order:

fo_alpha_list.append((alpha, init_decay))

random.shuffle(fo_alpha_list)

print(len(fo_alpha_list))

print(fo_alpha_list[:5])

# 取前100个作为测试

alphas = fo_alpha_list[:100]

print(len(alphas))

multi_alphas = wqb.to_multi_alphas(alphas, 10)

concurrency = 8  # 1 <= concurrency <= 10

resps = asyncio.run(

wqbs.concurrent_simulate(

multi_alphas,  # `alphas` or `multi_alphas`

concurrency,

)

)

for idx, resp in enumerate(resps, start=1):

print(idx)

print(resp.status_code)

print(resp.text)

结果报错：

"Invalid data. Expected a dictionary, but got list."
请问是alpha需要做调整吗？

---

### 评论 #17 (作者: KB18445, 时间: 1年前)

改了下遍历内容，已经可以了，多谢大佬开源
# Pad initial decay with alpha

init_decay = 6

fo_alpha_list = []

# for alpha in first_order:

#     fo_alpha_list.append((alpha, init_decay))

for item in first_order:

alpha = {

'type': 'REGULAR',

'settings': {

'instrumentType': 'EQUITY',

'region': 'USA',

'universe': 'TOP3000',

'delay': 1,

'decay': 13,

'neutralization': 'INDUSTRY',

'truncation': 0.13,

'pasteurization': 'ON',

'unitHandling': 'VERIFY',

'nanHandling': 'OFF',

'language': 'FASTEXPR',

'visualization': False

},

'regular': item,

}

fo_alpha_list.append(alpha)

random.shuffle(fo_alpha_list)

print(len(fo_alpha_list))

print(fo_alpha_list[:1])

---

### 评论 #18 (作者: WL13229, 时间: 1年前)

[HD44583](/hc/en-us/profiles/27705611217687-HD44583)

香港地区需要人脸识别验证后登录

---

### 评论 #19 (作者: HD44583, 时间: 1年前)

回复 [YZ72256](/hc/en-us/profiles/27031098060439-YZ72256) ：

当前大版本0.2.x暂时没有做数据库的计划，不过未来有可能加入pandas.DataFrame相关的API，有了DataFrame数据库就方便了。

---

### 评论 #20 (作者: JT84734, 时间: 1年前)

我现在有一个问题，就是 `simulate` 返回的数据里面有 `'alpha': 'Ybj3bmJ'`

```
{'id': '33V5Ka5QO50W8LEJ1RqiQGz', 'type': 'REGULAR', 'settings': {'instrumentType': 'EQUITY', 'region': 'USA', 'universe': 'TOP3000', 'delay': 1, 'decay': 13, 'neutralization': 'INDUSTRY', 'truncation': 0.13, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'OFF', 'language': 'FASTEXPR', 'visualization': False}, 'regular': 'liabilities/assets', 'status': 'COMPLETE', 'alpha': 'Ybj3bmJ'}

```

而 `concurrent_simulate` 返回的数据里没有找到 `'alpha': 'Ybj3bmJ'` ，不知道有没有办法获取到。

我现在想如果可以获取到 `'alpha':`  的值，那在完成 `concurrent_simulate` 之后就对上面 `concurrent_simulate` 的alpha设置一次名称

```
{'children': ['4DQEmy5V4VdaYmL3GqMMFM', '2IMTeFf7y50kcKZr7Pn7mLf', '43VCxm16P4P39x11bQEE7Fcb', 'ZNEntbNJ5itaz7Uu2mDfaE'], 'type': 'REGULAR', 'settings': {'instrumentType': 'EQUITY', 'region': 'USA', 'delay': 1, 'language': 'FASTEXPR'}, 'status': 'COMPLETE'}
```

---

### 评论 #21 (作者: JT84734, 时间: 1年前)

刚刚发现  `concurrent_simulate`  传入 `multi_alphas` 返回的会是children，传入 `alphas` 返回的内容会包含alpha id 。
然后使用 `https://api.worldquantbrain.com/simulations/children_id`  可以获取到上面simulate返回的数据，接着就可以取到alpha_id了。

```
# resps 是concurrent_simulate 返回的值
all_children = []
for idx, resp in enumerate(resps, start=1):
    json_data = json.loads(resp.text)
    children = json_data.get('children', [])
    all_children.extend(children)

def get_alphas(children,session):
    alphas = []
    for child in children:
        url = f"https://api.worldquantbrain.com/simulations/{child}"
        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            alpha = data.get('alpha', None)
            if alpha is not None:
                alphas.append(alpha)
        else:
            print(f"Failed to retrieve data for {url}. Status code: {response.status_code}")
    return alphas

all_alphas = get_alphas(all_children,wqbs)
print(all_alphas)
```

---

### 评论 #22 (作者: ZX27801, 时间: 1年前)

请问下作者concurrent_simulate支持断点嘛？就是停止程序后下次会从未仿真的alpha开始simulate

---

### 评论 #23 (作者: LL87164, 时间: 1年前)

我目前的试用体会是用machine_lib和Alpha Machine做前后两头的工作，中间结果存入本地JSON文件，用wqb跑回测。这样改动工作量最小，又能体现各自的优势。

---

### 评论 #24 (作者: LL87164, 时间: 1年前)

[ZX27801](/hc/en-us/profiles/28902564931095-ZX27801)

我问过了，目前不支持。建议从log里判断完成了百分之多少，按此截断再跑。不会很精准，但也够用了。

---

### 评论 #25 (作者: YK42677, 时间: 1年前)

非常棒，确实能够有效提升回测效率。

---

### 评论 #26 (作者: XZ23611, 时间: 1年前)

开始迈出使用wqb的第一步，现在已经可以实现异步回测！  配合machine lib里的generate_sim_data 可以最小化改动现在代码

expression_pair=[]
for expression in expressions[740:]:
    expression_pair.append((expression, 4))  # decay

region = 'USA'
uni = 'TOP3000'
neut = 'STATISTICAL'

alpha_list = generate_sim_data(expression_pair,region,uni,neut)
alpha_list[:3]

---

### 评论 #27 (作者: YX23928, 时间: 1年前)

实测wqb两个月，很稳健，提高了工程效率，希望concurrent_simulate的方法能集成set_alpha_properties的功能，再次感谢大佬的wqb工程

---

### 评论 #28 (作者: YY57768, 时间: 1年前)

求问一下各位大佬，wqb这个库里面貌似没有看到批量生产alpha的函数啊

---

### 评论 #29 (作者: SW66069, 时间: 1年前)

感谢分享，效率提高很多

---

### 评论 #30 (作者: CR35762, 时间: 1年前)

根据以上各位大佬的经验，我是用原来的machine_lib把alpha list存入json文件，然后读出后用wqb跑的，但是看起来效率没有提升反而下降了（一小时才50来个），是我还是条件顾问（目前是参加的iqc）只能3个线程的原因吗？还是哪里有问题。以下是我用的简单代码，去掉了登陆和日志部分：

```
import jsonimport datetimefrom wqb import WQBSession, printimport wqbdef read_json_file(file_path):    try:        withopen(file_path, 'r') asfile:        data=json.load(file)        returndata    exceptFileNotFoundError:        print(f"文件 {file_path} 未找到")        returnNone    exceptjson.JSONDecodeErrorase:        print(f"JSON解码错误: {e}")        returnNonedef on_success(vars: dict[str, object]) -> None:    wqbs: wqb.WQBSession=vars['self']    nn="002"    dd=datetime.date.today()    os_name=str(dd.strftime("%Y%m%d")) +str(nn)    #修改alpha的name    alpha_id=vars['resp'].json()['alpha']    #print(alpha_id+" name is :"+os_name)    resp=wqbs.patch_properties(         alpha_id,         name=os_name, # '<name>'         log=None,     )file_path = 'list_alpha.json'result = read_json_file(file_path)if result:     concurrency=3     try:         resps=awaitwqbs.concurrent_simulate(result,concurrency,on_success=on_success,log_gap=10)         print('alpha_ids:', *(resp.json()['alpha'] forrespinresps), sep='\n')     exceptException as e:         print(f"发生错误:{e}")
```

---

### 评论 #31 (作者: BW14163, 时间: 1年前)

感谢大佬分享代码，这两天就开始尝试学习异步操作。

---

### 评论 #32 (作者: MX83967, 时间: 11个月前)

这个回测程序中断后，再继续跑的话，如何截断呢？是在这里设置截断数值参数吗？ ![图片](images/img_c065f181c0.png)

---

### 评论 #33 (作者: ZZ37826, 时间: 10个月前)

能问一下，submit的返回值有关于alpha的全部信息吗？还是只有再访问一次alpha_id才能获取检查信息呢？

---

### 评论 #34 (作者: BW94444, 时间: 9个月前)

WQB的回测效率是会受到Region/Delay/InstrumentType/Dataset影响的么？？

---

### 评论 #35 (作者: MZ35432, 时间: 9个月前)

我个人是把 machine lib 里面的htttp 进行了改进，调用 httpx  这个高性能http 客户端来进行请求 对比原来的性能确实提高一些，但没做过具体数据对比

---

### 评论 #36 (作者: CY76111, 时间: 7个月前)

感谢分享，谢谢

---

### 评论 #37 (作者: TW27682, 时间: 6个月前)

哇，这么高的回测数量吗？但是，现在每天限制10000了，咋处理呢？

---

### 评论 #38 (作者: TW27682, 时间: 6个月前)

wqb 很好用啊。构建自己的代码，非常有帮助。谢谢分享

---

