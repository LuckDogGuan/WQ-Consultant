# 新手课代码分享

- **链接**: [Commented] 新手课代码分享.md
- **作者**: JL11546
- **发布时间/热度**: 2个月前, 得票: 90

## 帖子正文

以下代码我以代码块作为区分，各位可以将代码块拷贝到Jupter Notebook中运行，请确保.env文件和代码在同一目录下。

```
import jsonfrom os.path import expanduserfrom os import environimport pandas as pdimport requestsfrom requests.auth import HTTPBasicAuthimport time# Load credentialstry:    with open(expanduser('brain_credentials.txt')) as f:        credentials = json.load(f)except FileNotFoundError:    credentials = (environ.get('BRAIN_USERNAME'), environ.get('BRAIN_PASSWORD'))# Extract username and password from the listusername, password = credentials# Create a session objectsess = requests.Session()# Set up basic authenticationsess.auth = HTTPBasicAuth(username, password)# Send a POST request to the API for authenticationresponse = sess.post('https://api.worldquantbrain.com/authentication')# Print response status and content for debuggingprint(response.status_code)print(response.json())
```

```
## 获取数据集ID为 fundamental6 下的所有数据字段def get_datafields(        s,        instrument_type: str = 'EQUITY',        region: str = 'USA',        delay: int = 1,        universe: str = 'TOP3000',        dataset_id: str = '',        data_type: str = 'MATRIX',        search: str = ''):    offset = 0    datafields_list = []    while True:        url_template = "https://api.worldquantbrain.com/data-fields?" + \                       f"&instrumentType={instrument_type}" + \                       f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" + \                       f"&offset={offset}" + \                       f"&type={data_type}"        url_template += (f"&search={search}" if search else "")        resp = sess.get(url_template)        results = resp.json()        # print(results)        if 'results' not in results:            print(f"Unexpected response: {results}")            break        else:            print(f"Fetched {len(results['results'])} data fields with offset {offset}.")            datafields_list.append(results['results'])            if len(results['results']) < 50:                print("Fetched the last batch of data fields.")                break            offset += 50            time.sleep(5)           datafields_list_flat = [item for sublist in datafields_list for item in sublist]    datafields_df = pd.DataFrame(datafields_list_flat)    return datafields_dffundamental6 = get_datafields(s=sess, dataset_id='pv13', data_type='GROUP')
```

```
datafields_list = fundamental6['id'].valueslen(datafields_list)
```

alpha_list = []

group_ops_list = ['group_mean', 'group_neutralize']

ts_ops_list = ['ts_mean', 'ts_rank']

days = [63, 126]

group = ['market', 'sector', 'industry']

```
for datafield in datafields_list:    for group_ops in group_ops_list:        for ts_ops in ts_ops_list:            for day in days:                for group in group:                                      print("正在将如下 Alpha 表达式与 setting 封装")                    print(f'{group_ops}({ts_ops}({datafield}, {days}), {group})')                               simulation_data = {                        'type' : 'REGULAR',                        'settings' : {                            'instrumentType' : 'EQUITY',                            'region' : 'USA',                            'universe' : 'TOP3000',                            'delay' : 1,                            'decay' : 0,                            'neutralization' : 'MARKET',                            'truncation' : 0.08,                            'pasteurization': 'ON',                            'unitHandling' : 'VERIFY',                            'nanHandling': 'ON',                            'language' :'FASTEXPR',                            'visualization':False,                        },                      "regular": f'{group_ops}({ts_ops}({datafield}, {days}), {group})'                    }                    alpha_list.append(simulation_data)
```

```
for alpha in alpha_list:  sim_resp = sess.post(    "https://api.worldquantbrain.com/simulations",    json = alpha  )  try:    sim_progress_url = sim_resp.headers['Location']    while True:      sim_progress_resp = sess.get(sim_progress_url)      retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))      if retry_after_sec == 0:  # simulation done!          break      time.sleep(retry_after_sec)    alpha_id = sim_progress_resp.json()["alpha"]  # the final simulation result    print(alpha_id)  except:    print("no location, sleep for 10 seconds and try next alpha")    time.sleep(10)
```

---

## 讨论与评论 (25)

### 评论 #1 (作者: HZ14936, 时间: 2个月前)

感谢

---

### 评论 #2 (作者: ZL15100, 时间: 2个月前)

基于我的实践经验，我想补充几点优化建议：

关于代码结构的改进 您当前的嵌套循环结构会产生大量组合（数据字段×组操作×时序操作×天数×分组），可能导致API请求过于密集。我建议增加批次控制和错误处理机制，比如：

- 添加请求间隔控制，避免触发API限制
- 实现失败重试机制，提高成功率
- 增加结果保存功能，避免数据丢失
关于参数选择的优化 我发现您选择的参数组合很有代表性，但可以进一步优化：

- days=[63, 126] 的选择很好，覆盖了季度和半年度周期
- 可以考虑增加 [21, 42] 等短期窗口，捕捉不同频率的信号
- 分组选择 ['market', 'sector', 'industry'] 很全面，体现了不同层级的中性化
关于实际应用的建议 在实际使用中，我发现这种批量生成方法有几个关键注意事项：

1. 质量控制 ：建议在提交前增加简单的语法检查，避免无效表达式
2. 结果筛选 ：建立自动化的结果评估标准，只保留有潜力的alpha
3. 资源管理 ：合理控制并发数量，避免对平台造成过大压力
关于扩展可能性 这个脚本框架很有潜力，可以进一步扩展为：

- 多市场批量测试（USA/EUR/ASI等）
- 动态参数优化（根据历史表现调整参数范围）
- 智能筛选系统（基于Sharpe、Turnover等指标自动过滤）
感谢分享这个实用的工具！期待看到更多关于批量alpha生成和优化的技术讨论。

---

### 评论 #3 (作者: goliter(LG97237), 时间: 2个月前)

这串代码产出的alpha是不是都出现了语法错误？首先是ts_mean接收的参数应该是3个而代码中全为2个，以及ts_mean, ts_rank接收的第一个参数不应该都是group类型的，而datafields_list里类型全是group，是代码有问题还是我执行出了问题？

---

### 评论 #4 (作者: Dennis zeng(DZ34853), 时间: 2个月前)

感谢，我只能对着录播课，一边暂停，一边打。很多时间还切换屏幕，我其实一直看不清完整代码，就因为这个原因，我卡住一个月。我是非程序员，一窍不通的

---

### 评论 #5 (作者: CG80191, 时间: 2个月前)

请问大家这个代码没顾问权限能运行吗我在jupyter notebook跑了半天没一个通过的

---

### 评论 #6 (作者: Ouyang Liu(LO84823), 时间: 2个月前)

```
系统显示没有brain_credentials.txt怎么办
```

---

### 评论 #7 (作者: BT44189, 时间: 2个月前)

这串代码直接用的话会出现语法错误：

1.首先是group_mean接收的参数应该是3个而代码中为2个，可以将列表中group_mean删掉，只留group_

neutralize，先跑通代码，后续再调整；

2.ts_mean, ts_rank接收的第一个参数不能是group类型的，必须是matrix类型的，可以先将代码中data_type='GROUP'改为data_type='MATRIX'，先跑通代码，后续可以再调整数据集。

---

### 评论 #8 (作者: CK88801, 时间: 2个月前)

`group_mean(x, weight, group)` ，各参数含义如下：

- **`x`  (计算目标)** ： 需要求调和平均数的具体数值或表达式。在示例中，它是  `close/eps` （即市盈率 P/E ratio）。
- **`weight`  (权重参数)** ： 这是一个 **可选** 的权重参数，用于在计算时赋予不同成员不同的比重。在给定的示例  `group_mean(close/eps, 1, industry)`  中，传入了  `1` ，这意味着在该示例中对所有股票采取了等权重计算。
- **`group`  (分组变量)** ： 用于定义如何将数据进行分类或分组的基准变量。该方法会分别计算每个组内的调和平均数。在示例中，它是  `industry` （行业），意味着程序会按不同的行业分别计算市盈率的调和平均数。

---

### 评论 #9 (作者: goliter(LG97237), 时间: 2个月前)

我发现错误了，按代码表意应该是要请求fundamental6这个数据集，他的id应该是fundamental6而非pv13，而且请求的数据类型应该是matrix而不是group

```
fundamental6 = get_datafields(s=sess, dataset_id='pv13', data_type='GROUP')
```

按原文这个代码拼接出的alpha全是没法通过语法检测的。
再有就是我之前说过的group_mean需要三个参数

---

### 评论 #10 (作者: ZL71666, 时间: 2个月前)

用代码和在worldquant平台上测Alpha，有什么区别吗。代码的优势是什么

---

### 评论 #11 (作者: ZZ22049, 时间: 2个月前)

代码跑通了，但是也没有输出，代码一窍不通，问ai，我都没法信任ai给出的信息

---

### 评论 #12 (作者: Xin Shu(XS20799), 时间: 2个月前)

为什么，我有biometrics 验证，然后我就无法自动化，在成为条件顾问之前，都没有这个验证，可以自动化的

---

### 评论 #13 (作者: FZ60707, 时间: 1个月前)

这篇代码分享很实用，尤其是批量生成alpha的思路值得学习。不过直接运行确实容易遇到语法错误，比如 `group_mean` 需要三个参数，而嵌套循环里只传了两个；另外 `data_type='GROUP'` 得到的字段大多不适用于 `ts_mean` 这类时序操作，建议改为 `MATRIX` 并检查API参数。期待后续能加上简单的表达式校验和结果过滤机制，减少无效提交。对新手来说，理解平台API的字段类型和算子约束比单纯跑通代码更重要。

---

### 评论 #14 (作者: FH46076, 时间: 1个月前)

一直报“no location, sleep for 10 seconds and try next alpha”是正常情况吗 还是只有少部分会有

alpha_id

---

### 评论 #15 (作者: EJ43152, 时间: 1个月前)

为什么提交之后在网页端是看不到的？

---

### 评论 #16 (作者: ZJ90951, 时间: 1个月前)

能不能告诉下具体怎么操作呢  不是学计算机  对这方面不懂

---

### 评论 #17 (作者: RZ75811, 时间: 1个月前)

很实用的知识，谢谢老师的分享！

---

### 评论 #18 (作者: venc(VC10940), 时间: 1个月前)

老师我正常请求认证接口，为什么会报429呢，我也就请求一次
{'message': 'API rate limit exceeded'}

---

### 评论 #19 (作者: YL48537, 时间: 1个月前)

终于发现问题了，这个代码fundamental6 = get_datafields(s=sess, dataset_id='pv13', data_type='GROUP')这里的pv13不对，我看了视频里的写法，可以把'pv13'改成’fundamental6 ‘或者’analyst4‘，这样代码就通了，因为pv13系列的代码跟 **`ts_mean这个方法不适用，在网页的simulation写出代码封装好的第一行alpha：group_zscore(ts_mean(pv13_1l_scibr,63),market)并运行，结果网页报了这个错误：Incompatible unit for input of "ts_mean" at index 0, expected "Unit[]", found "Unit[Group:1]",我问了ai，说这是Alpha 表达式本身的数据类型不匹配的问题。所以，将fundamental6 = get_datafields(s=sess, dataset_id='pv13', data_type='GROUP')这段代码改成fundamental6 `** = get_datafields(s=sess, dataset_id='analyst4', data_type='MATRIX')或 **`fundamental6 `** = get_datafields(s=sess, dataset_id=' **`fundamental6 `** ', data_type='MATRIX')就行了

---

### 评论 #20 (作者: ChuanHao Hou(CH74510), 时间: 1个月前)

我也登录不了，报429，{'message': 'API rate limit exceeded'}

---

### 评论 #21 (作者: LE69726, 时间: 1个月前)

报429我也遇到了，我说一下我的解决，打印了 ：

```
credentials 这个参数发现读取txt文件的账号密码是key不是value，配置文件有问题，你可以把print(credentials)的内容告诉Ai。为什么从配置文件中读取的账号密码不是正确的，就能解决了。
```

---

### 评论 #22 (作者: WH40329, 时间: 27天前)

很容易429，要修改代码

---

### 评论 #23 (作者: YC75342, 时间: 25天前)

为啥我请求认证报错401呢

---

### 评论 #24 (作者: LY44102, 时间: 23天前)

大佬，我有个问题需要求助请教，我尝试使用python访问API批量测试数据集，但是因为算子公式出现异常导致simulation通道一直被占用，平台上并没有找到正在占用中的通道线程，我想请教如何能够取消或者中断出现异常的simulation。

---

### 评论 #25 (作者: XW61424, 时间: 16天前)

新手学习一下，现在还是啥啥都看的懂又看不懂的阶段

---

