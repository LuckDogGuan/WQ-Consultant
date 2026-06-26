# 一键检验alpha稳定plus 版本代码优化

- **链接**: [L2] 一键检验alpha稳定plus 版本代码优化.md
- **作者**: YZ70114
- **发布时间/热度**: 11个月前, 得票: 84

## 帖子正文

原贴：
 [../JL71699/一键检验alpha稳定性代码优化.md?input_string=%E4%B8%80%E9%94%AE%E6%A3%80%E9%AA%8Calpha%E7%A8%B3%E5%AE%9Aplus%20%E7%89%88%E6%9C%AC](../JL71699/一键检验alpha稳定性代码优化.md?input_string=%E4%B8%80%E9%94%AE%E6%A3%80%E9%AA%8Calpha%E7%A8%B3%E5%AE%9Aplus%20%E7%89%88%E6%9C%AC)  
@ [JL71699](/hc/en-us/profiles/23363707892759-JL71699)   感谢JL 大佬的初版，以及kitty 哥 [DZ31817](/hc/en-us/profiles/25751669201943-DZ31817)  发的有关decay 的研究图

对于原版一键检验alpha稳定性 做了下优化

1. decay 直接填写固定值遍历

2.  ASI 地区最近需要强制开启maxTrade 做了修改

3. dataframe 打印format 出百分比和万分比数值，显示更直观

4.画图修改使用plotly 画图

![图片](images/img_cf9a40fadb.png)  ![图片](images/img_2c623876cd.png)

#一键检验稳定性
import time
import json
import requests
import pandas as pd
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
from urllib.request import urlopen

#这里填alpha
alpha_id_ori='jxRvMmj'
force_truncation = None

def login():
    username = "你的账号"
    password = "你的密码"

# Create a session to persistently store the headers
    s = requests.Session()

    # Save credentials into session
    s.auth = (username, password)

    # Send a POST request to the /authentication API
    response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')
    print(response.content)
    return s

s = login()

#=========================================

def locate_alpha(s, alpha_id):
    while True:
        alpha = s.get(" [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id)
        if "retry-after" in alpha.headers:
            time.sleep(float(alpha.headers["Retry-After"]))
        else:
            break
    string = alpha.content.decode("utf-8")
    metrics = json.loads(string)
    # print(metrics["regular"]["code"])

dateCreated = metrics["dateCreated"]
    sharpe = metrics["is"]["sharpe"]
    fitness = metrics["is"]["fitness"]
    turnover = metrics["is"]["turnover"]
    margin = metrics["is"]["margin"]
    returns = metrics["is"]["returns"]
    drawdown = metrics["is"]["drawdown"]
    decay = metrics["settings"]["decay"]
    exp = metrics["regular"]["code"]
    universe = metrics["settings"]["universe"]
    truncation = metrics["settings"]["truncation"]
    neutralization = metrics["settings"]["neutralization"]
    region = metrics["settings"]["region"]
    testPeriod = metrics["settings"]["testPeriod"]

# triple =pd.DataFrame([[alpha_id,  sharpe, turnover, fitness, margin]])
    triple = [
        alpha_id,
        sharpe,
        turnover,
        fitness,
        margin,
        exp,
        region,
        universe,
        neutralization,
        decay,
        truncation,
        testPeriod,
        returns,
        drawdown,
    ]
    return triple

sharp_list = []
df = pd.DataFrame(columns=["alpha_id", "sharpe", "turnover", "fitness", "margin","returns","drawdown"])

alpha_line = []
tem = locate_alpha(s, alpha_id_ori)

[
    alpha_id,
    sharpe,
    turnover,
    fitness,
    margin,
    exp,
    region,
    universe,
    neutralization,
    decay,
    truncation,
    testPeriod,
    returns,
    drawdown,
] = tem
use_truncation = truncation
if force_truncation is not None and force_truncation > 0:
    use_truncation = force_truncation

# 根据 decay 的值选择不同的 decay_tem 列表
decay_tem_list = [0, 1, 5, 20, 60]

# 固定的 neutralization_tem 列表
neutralization_tem_list = [
    "SUBINDUSTRY",
    "INDUSTRY",
    "SECTOR",
    "MARKET",
    "CROWDING",
    "STATISTICAL",
    "SLOW_AND_FAST",
    "FAST",
    "SLOW",
    "REVERSION_AND_MOMENTUM"
]
if region == "ASI" or region == "EUR" or region == "GLB":
    neutralization_tem_list.append("COUNTRY")
# neutralization_tem_list = ['SUBINDUSTRY']
# 使用列表推导式生成 simulation_data
max_trade = "OFF"
if region == "ASI":
    max_trade = "ON"
alpha_line.extend(
    {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": region,
            "universe": universe,
            "delay": 1,
            "decay": decay_tem,
            "neutralization": neutralization_tem,
            "truncation": use_truncation,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "ON",
            "language": "FASTEXPR",
            "visualization": True,
            "testPeriod": testPeriod,
            "maxTrade": max_trade,
        },
        "regular": exp,
    }
    for decay_tem in decay_tem_list
    for neutralization_tem in neutralization_tem_list
)
alpha_total = len(alpha_line)
print(f"total simulate {alpha_total} alphas")
wbs = []
for alpha_data in alpha_line:
    while True:
        count = 0
        try:
            # Send multisimulation request
            response = s.post(
                " [https://api.worldquantbrain.com/simulations](https://api.worldquantbrain.com/simulations) ", json=alpha_data
            )
            # Check response

if len(response.headers["Location"]) > 0:
                print(
                    f"Alpha location get successfully: {response.headers['Location']}"
                )
                wbs.append(response.headers["Location"])
                break
        except:
            count = count + 1
            # s = sign_in(username, password)
            print("Error in sending simulation request. And retry after 5s")
            time.sleep(5)
            if count > 10:
                s = login()
            if count > 30:
                break
print(len(wbs))

#========================================

df_list = []
df_list = pd.DataFrame(
    columns=[
        "alpha_id",
        "neutralization",
        "decay",
        "sharpe",
        "fitness",
        "turnover",
        "margin",
        "returns",
        "drawdown"
    ]
)
tem = locate_alpha(s, alpha_id_ori)
[
    alpha_id_ori,
    sharpe,
    turnover,
    fitness,
    margin,
    exp,
    region,
    universe,
    neutralization,
    decay,
    truncation,
    testPeriod,
    returns,
    drawdown,
] = tem
new_row = [alpha_id_ori, neutralization, decay, sharpe, fitness, turnover, margin, returns, drawdown]
df_list.loc[len(df_list)] = new_row
print(df_list)

for wb in wbs:
    # 发送请求
    url = wb
    while 1:  # 对1个simulated测试
        data = s.get(url).text
        if "progress" not in data and "error" not in data:
            json_data = json.loads(data)  # 将文本转为字典
            alpha_value = json_data["alpha"]  # 直接获取 alpha 字段
            print(alpha_value)
            tem = locate_alpha(s, alpha_value)
            [
                alpha_id,
                sharpe,
                turnover,
                fitness,
                margin,
                exp,
                region,
                universe,
                neutralization,
                decay,
                truncation,
                testPeriod,
                returns,
                drawdown,
            ] = tem
            new_row = [
                alpha_id,
                neutralization,
                decay,
                sharpe,
                fitness,
                turnover,
                margin,
                returns,
                drawdown,
            ]
            df_list.loc[len(df_list)] = new_row  # 直接赋值（确保 df 已初始化列名）
            break
        else:
            print("progressing")
            time.sleep(60)
            continue
df_list = df_list.drop_duplicates(subset="alpha_id", keep="first")

#=========================================

#显示df 数据
print(alpha_id_ori)

df_sorted = df_list.sort_values("neutralization")
df_multiindex = df_sorted.set_index(["neutralization", "decay"])

#df 数据做处理，returns turnover，drawdown 显示为百分比后面加%，margin 显示万分比后面加‱
df_multiindex['returns'] = df_multiindex['returns'] * 100
df_multiindex['turnover'] = df_multiindex['turnover'] * 100
df_multiindex['drawdown'] = df_multiindex['drawdown'] * 100
df_multiindex['margin'] = df_multiindex['margin'] * 10000

# 使用styler格式化显示，添加百分号和万分号
styled_df = df_multiindex.style.format({
    'returns': '{:.2f}%',
    'turnover': '{:.2f}%', 
    'drawdown': '{:.2f}%',
    'margin': '{:.2f}‱',
    'sharpe': '{:.4f}',
    'fitness': '{:.4f}'
})

styled_df

#=========================================

from time import sleep
def get_pnl(s, alpha_id):
    finished = False
    while True:
        pnl = s.get(' [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) ' + alpha_id + '/recordsets/pnl')
        if pnl.headers.get('Retry-After', 0) == 0:
             break
        print('Sleeping for ' + pnl.headers['Retry-After'] + ' seconds')
        sleep(float(pnl.headers['Retry-After']))
    # print('PNL retrieved')
    return pnl

df1 = pd.DataFrame()

for alpha_id in df_list['alpha_id'].unique():
    print(alpha_id)
    json_data = get_pnl(s, alpha_id).json()['records']
    df = pd.DataFrame(json_data)
    df=df.iloc[:,0:2]
    df.columns = ['date', alpha_id]
    df.set_index('date', inplace=True)
    df1 = pd.merge(df1, df, left_index=True, right_index=True, how='outer')

df1.index = pd.to_datetime(df1.index)
start_time=df1.index[0]-pd.Timedelta(days=1)
start_time

#=========================================

import plotly.graph_objects as go

# 假设 df1 是你的时间序列 DataFrame，行索引是日期，列是不同的曲线
# 示例代码继续使用 df1
fig = go.Figure()

for col in df1.columns:
    fig.add_trace(go.Scatter(
        x=df1.index,
        y=df1[col],
        mode='lines',
        name=col,
        hovertemplate=(
            f"<b>{col}</b><br>"
            "日期: %{x}<br>"
            "值: %{y:.2f}<extra></extra>"
        )
    ))

fig.update_layout(
    title="多时间序列对比",
    xaxis_title="日期",
    yaxis_title="数值",
    legend_title="类别",
    width=1000,
    height=600,
    template="plotly_white",
    hovermode='x unified'
)

fig.show()

---

## 讨论与评论 (17)

### 评论 #1 (作者: XH10010, 时间: 1年前)

赞，比原版好像更直观一些

---

### 评论 #2 (作者: AL13375, 时间: 1年前)

很实用的优化，期待更多的分享！

---

### 评论 #3 (作者: XW85841, 时间: 1年前)

感谢大佬的无私奉献。

最近刚好遇到需要轮换检测不同中性化下某一些alpha是否可以提交、但又不会批量设置settings，现在有了这个工具，简直是久旱逢甘霖啊——一键检验Alpha 的稳定性大大简化了手工微调的测试流程，对于不会代码的我来说，简直不要太棒了！

先试用一段时间，有了效果再回来继续分享！祝大佬VF到1.0！

---

### 评论 #4 (作者: XW85841, 时间: 1年前)

刚刚跑通了这段代码，已经可以把某个指定的alpha按照不同中性化、不同dacey的设置测试并输出了相应的综合图线，非常感谢大佬及这段代码中其他几位大神的无私奉献。但是有一个问题：这里的dacey设定的几个固定数字，是怎么选择的，可不可以修改或者说仅仅固定dacey来遍历中性化？或者说是反过来，按照定一原则去分别跑，然后在对照？还有对于跑出来的图线的解释或者说判断，有没有建议（主要是不会看这个图像有什么作用），仅仅是用于判断这个alpha本身是否健壮？还是说可根据这个来选择合适的中性化策略？

期待求指导，谢谢！

---

### 评论 #5 (作者: ZZ10277, 时间: 1年前)

太感谢了，有了这个就方便多了，不用一遍遍手动去换设置回测了！

---

### 评论 #6 (作者: YZ70114, 时间: 1年前)

@ [XW85841](/hc/en-us/profiles/27698980580119-XW85841)

decay_tem_list 这里就可以设置几个固定值，我当前选用的的是

```
decay_tem_list = [1, 12, 24, 32]
```

neutralization_tem_list 也是固定的，可以按照自己需要修改

对于当前的PnL 曲线只是看个大概，后面想优化下增加个判断怎么才算是健壮的，我现在的做法是，结合sharpe 等数值去判断，如果需要更细致的查看，当前的alpha 回测visualization是打开的，回看对应alpha 是可以再结合看看

---

### 评论 #7 (作者: ZS59763, 时间: 1年前)

很好用的改善 ，点赞！

同时 也想问一下，我在用的时候会出现，跑完，get到一半就 出错 的情况，这个要怎么解决呢？

========================================================================

“王牌总是在最后出场”——《游戏王》

========================================================================

---

### 评论 #8 (作者: JG91554, 时间: 1年前)

为啥运行报这个错：

ell In[3], line 25  23 neutralization = metrics["settings"]["neutralization"]

24 region = metrics["settings"]["region"]

---> 25 testPeriod = metrics["settings"]["testPeriod"]

27 # triple =pd.DataFrame([[alpha_id, sharpe, turnover, fitness, margin]])

28 triple = [

29 alpha_id,

30 sharpe,  (...)

43  44 ] KeyError: 'testPeriod'

---

### 评论 #9 (作者: FL39657, 时间: 1年前)

更直观，更好用了，感谢楼主提供的代码

---

### 评论 #10 (作者: MZ45384, 时间: 1年前)

请问，为什么neutralization列表不包含RAM, SLOW, FAST和SLOＷ＿ＡＮＤ＿ＦＡＳＴ吗

---

### 评论 #11 (作者: YZ70114, 时间: 1年前)

[MZ45384](/hc/en-us/profiles/29472943154455-MZ45384)  可以自行加上 代码遗留问题而已

---

### 评论 #12 (作者: CF35175, 时间: 1年前)

佬, 链接咋404了

---

### 评论 #13 (作者: YZ70114, 时间: 1年前)

代码补档 不走github了

---

### 评论 #14 (作者: FF76003, 时间: 11个月前)

df_list显示未定义呀，大佬

---

### 评论 #15 (作者: YZ70114, 时间: 11个月前)

尴尬 漏了 df_list 相关

---

### 评论 #16 (作者: XW23690, 时间: 8个月前)

感谢分享，另外请问一下setting中的Neutralization设定“RAM ”好像加不进去，python会报错说没有这个选项，不知各位伙伴有没有遇到相同问题，其他的Neutralization倒是可以

---

### 评论 #17 (作者: YZ70114, 时间: 8个月前)

[XW23690](/hc/en-us/profiles/32613849420311-XW23690)   RAM  是

REVERSION_AND_MOMENTUM

---

