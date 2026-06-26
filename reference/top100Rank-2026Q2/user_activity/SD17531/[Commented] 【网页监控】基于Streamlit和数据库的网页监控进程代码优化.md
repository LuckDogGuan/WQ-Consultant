# 【网页监控】基于Streamlit和数据库的网页监控进程代码优化

- **链接**: [Commented] 【网页监控】基于Streamlit和数据库的网页监控进程代码优化.md
- **作者**: KZ79256
- **发布时间/热度**: 1年前, 得票: 28

## 帖子正文

由于我是基于数据库跑alpha的，每次想监控跑了多少，还有多少没跑，程序是不是在运行，都要用相应的代码在数据库或者命令行中运行。为了便捷我使用Streamlit做了个网页来查看运行情况（可能需要公共ip）

其中Streamlit是一个非常简单的制作网页的方法，在访问网页时调用后端python代码实时渲染网页，通过st.write可以向网页中写入dataframe，st.markdown向网页写入markdown语法

**一些库的导入和侧边栏制作**

因为我用的时mongo数据库管理alpha，可以适时改写成自己的

```python

import streamlit as st

from streamlit_extras.colored_header import colored_header

from streamlit_option_menu import option_menu

from streamlit_extras.badges import badge

# from streamlit_card import card

import pandas as pd

import numpy as np

from pymongo import MongoClient, UpdateOne

from pymongo import errors

from datetime import datetime

import pytz

import json

#侧边栏制作

with st.sidebar:

select_option = option_menu(

"WQB-监控",

[

"数据库监控",

"收入监控",

],

icons=[

'house',

'arrow-repeat',

],

menu_icon="boxes", default_index=0

)

if select_option == "数据库监控":

这个网页你想做的内容

其余同理

```

**首先是程序监控**

效果如下

![图片](images/img_c22aea48f7.png)

通过下述代码，可以获得正在运行的程序，注意第一行的command应该改成你程序运行命令，以显示你正在运行的程序

```python

command = 'ps aux | grep "python main.py --action" | grep -v grep'

result = subprocess.run(command, shell=True, text=True, capture_output=True)

# 解析输出

data = []

for line in result.stdout.strip().split("\n"):

parts = line.split(maxsplit=10)  # 解析 ps aux 的格式

if len(parts) == 11:  # 确保解析正确

data.append(parts)

# 定义列名（ps aux 的标准列）

columns = ["USER", "PID", "CPU%", "MEM%", "VSZ", "RSS", "TTY", "STAT", "START", "TIME", "COMMAND"]

# 转换为 Pandas DataFrame

df = pd.DataFrame(data, columns=columns)

colored_header(label=f"程序监控",description="",color_name="red-70")

st.write(df)

```

**接下来是数据库alpha状态监控**

效果如下

![图片](images/img_8e0905c836.png)

我把alpha用两个标识，一个是alpha state（用于描述该alpha是什么状态，等待运行，正在运行，运行完毕，正在获取is数据，获取完毕，以及因为各种原因丢弃的alpha和运行失败的），一个是bs stage（目前的alpha属于第几阶段，或者模板是什么）

目前我在自动跑regular alpha和super alpha，所以会有两个数据库要监视

通过mongo查询相应的alpha状态，然后写入网页，这样我就可以通过看pending，running来查看还有多少要运行，正在跑的alpha的状态

由于每个人的思路不太一样，这里就只是抛砖引玉，不放具体的代码了，写入的核心还是st.markdown，st.write

**收入监控**

效果展示

![图片](images/img_eea0bb9433.png)

这部分的核心主要是把每天的收入实时展示，我也可以不用因为收入专门查看网页了，并且按照base payment的计算方式展示出相应的影响因素，为了后续分析收入提供便利

这部分代码也不展示了，只是说一下思路

按钮可以使用

cols = st.columns(3)

cols[0].button("刷新收入数据", on_click=reload_fee_data, use_container_width=True)

**当然也可以监控更多的东西，但是我现在没有想到还要弄啥监控，慢慢更这个帖子吧**

---

## 讨论与评论 (6)

### 评论 #1 (作者: SD17531, 时间: 1年前)

大佬太牛了

---

### 评论 #2 (作者: MH19374, 时间: 1年前)

大佬太牛了

---

### 评论 #3 (作者: ZS59763, 时间: 1年前)

大佬太牛了

---

### 评论 #4 (作者: WA94369, 时间: 1年前)

大佬牛

---

### 评论 #5 (作者: XC66172, 时间: 1年前)

大佬太专业了~  不过REGULAR ALPHA如果提交了多于一个，应该看不了这一个RA对应的收入吧？

=============================================

睡醒就搓搓因子，总有一个是好的。FIGHTING LABUBU

=============================================

---

### 评论 #6 (作者: KZ79256, 时间: 9个月前)

[XC66172](/hc/en-us/profiles/28880767093655-XC66172)

> 应该看不了这一个RA对应的收入吧？

是的

=============================================

FIGHTING MOMO

=============================================

---

