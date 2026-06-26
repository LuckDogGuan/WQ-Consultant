# 一文解锁手机自动化回测, 从此随时随地想跑就跑。---基于QPython(安卓)--附代码

- **链接**: [Commented] 一文解锁手机自动化回测 从此随时随地想跑就跑---基于QPython安卓--附代码.md
- **作者**: RJ74200
- **发布时间/热度**: 9个月前, 得票: 25

## 帖子正文

大部分人都会选择云服务器来进行批量回测,如果觉得云服务器贵or前期懒得配置云服务器，更或者假期出去游玩没办法登录云服务器来操作，或许手机端批量自动化回测是一个不错的选择.

服务器可看作是一个高配置的电脑主机,而手机则可以是低配的电脑主机,对于回测使用的内存/硬盘/网络带宽完全足够.我选择的时QPYTHON，应用无广告，可开多个py文件进程。

![图片](images/img_494f40c849.jpeg)

启动流程: 手机应用商店下载Qpython ,点击进入APP -> 中间选择扩展 -> 选择AIPY ->往下滑动点击Pandas包安装.也可以在扩展界面选择PIP客户端进入手动下载一些pip库,但是支持的没那么多.（基础配置就弄好啦。）->.py文件，选择以QPYTHON打开，点击下面的运行符号。等待即可

如何查看手机文件的主目录: 点击文件夹最上面的默认分区.我的是/storage/emulated/0/,当文件存储在其他路径时,可能有权限问题,需要让QPython拥有更多权限,一般在手机设置中.由于json写入其他目录不对问题，所以我把状态文件Qpython的文件夹中

最后附上自动化回测代码，支持自动跑一二三N阶，支持断点续测，可扩展性强，但是函数比较少，可以自己多多添加。应该是支持顾问阶段和用户阶段的，可能需要自己稍微调一下确保代码没问题（有个缺点就是无法拉取超过10000的回测量，之前的手机摔坏了，所以没用这套代码了，下个版本还没调好，有机会再分享）。

单槽回测/用户阶段记得更改：if len(arr) == 10为if len(arr) == 1。max_post为最大槽位数量，用户阶段需要改为3。

字段分词以两个空格来分词，所以传入的表达式不要使用两个空格连在一起。

主函数如下：第一个为文件名称, 以.csv结尾。列名为code

flow("news18-EUR-1-TOP2500-m2-df", region="EUR", universe="TOP2500",delay=1, neu="FAST")

其他组合函数命名：ff：代表不做组合，ts_first->对应一阶，group_second->对应二阶，when_third->对应三阶。 完全支持各种顺序组合，更改funcs = [ff, ts_first, group_second, when_third,][:]的顺序或者删减即可。

代码如下：

import requests, logging, os, sys, re

from logging.handlers import RotatingFileHandler

import json

from requests.auth import HTTPBasicAuth

import pandas as pd

from time import sleep

import datetime

import pytz

import logging

class quant:

def __init__(self, data_name: str) -> None:

self.arr = []

self.count = 0

self.path = "/storage/emulated/0/qua/" if sys.platform == "linux"\

else "C:\Project\qua\"

self.path += data_name.split("-")[0]+"/"

os.makedirs(self.path, exist_ok=True)

self.data_name =self.path+data_name

self.log_name = self.path+data_name+'-log.txt'

self.case_name = self.data_name+"-case.json"

self.case_df = self.data_name+"-df.json"

self.result_df = self.data_name+"-result.csv"

self.sess = requests.Session()

self.save_file: StopIteration = None

def login(self,):

# 用户名和密码文件brain.txt格式: ["username", "password"]

with open(self.path + '../brain.txt') as f:

self.username, self.password = json.load(f)

self.sess.auth = HTTPBasicAuth(self.username, self.password)

response = self.sess.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')

print(response)

def save_result(self, alpha_num, s_time) -> pd.DataFrame:

# 2025-07-04T22:52:30

arr = []

print(alpha_num, s_time)

for i in range(0, alpha_num+100, 100):

print(i)

url = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \

+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + s_time  \

+ "-04:00"

print(url)

response = self.sess.get(url)

print(response)

alpha_list = response.json()["results"]

print

if len(alpha_list)==0:

return pd.DataFrame(arr)

for alphas_p in alpha_list:

result = dict()

result["id"] = alphas_p["id"]

result["code"] = alphas_p["regular"]["code"]

result["result"] = "FAIL" if  [i.get("name") for i in alphas_p["is"]["checks"] if i.get("result") == "FAIL"] else "PASS"

LOW_SUB_UNIVERSE_SHARPE = [i for i in alphas_p["is"]["checks"] if i["name"] == "LOW_SUB_UNIVERSE_SHARPE"][0]

result["sub"]=LOW_SUB_UNIVERSE_SHARPE.get("value", -2)-LOW_SUB_UNIVERSE_SHARPE.get("limit", 2)

CONCENTRATED_WEIGHT: dict = [i for i in alphas_p["is"]["checks"] if i["name"] == "CONCENTRATED_WEIGHT"][0]

result["weight"] = CONCENTRATED_WEIGHT.get("limit", 0) - CONCENTRATED_WEIGHT.get("value", 0)

aplha_is:dict = alphas_p["is"]

delete =  ["startDate", "checks", "bookSize"]

for ite in delete:

del aplha_is[ite]

# del

result.update(aplha_is)

result["settings"] = alphas_p["settings"]

arr.append(result)

return pd.DataFrame(arr)

def submit_simulations(self, index,  alpha_list, max_post=3):

if self.count % 80 == 0:

self.sess.close()

self.login()

self.count +=1

if  alpha_list:

print(alpha_list[0])

if len(alpha_list)==0:

alpha_list =alpha_list[0]

for _ in range(20):

try:

sim1 = None

sim1 = self.sess.post(' [https://api.worldquantbrain.com/simulations](https://api.worldquantbrain.com/simulations) ', json=alpha_list,)

location = sim1.headers['Location'].split("/")[-1]

break

except  Exception as e:

print(e, index, sim1)

sleep(10)

if _ == 19:

cfg.log(f"post ERROR: {index}")

return

self.arr.append((index, location))

self.save_status(index)

try:

print(self.arr)

while len(self.arr) >= max_post:

for index, ip in self.arr:

url = " [https://api.worldquantbrain.com/simulations/](https://api.worldquantbrain.com/simulations/) " + ip

sim_progress_resp = self.sess.get(url)

retry_after_sec = sim_progress_resp.headers.get("Retry-After", 0)

if retry_after_sec == 0:  # simulation done!模拟完成!

if (index, ip) in self.arr:

self.arr.remove((index, ip)) #删除对应的值

children = sim_progress_resp.json().get("children")  # 获取alpha id

status1 = sim_progress_resp.json().get("status")

if status1 == "ERROR":

cfg.log(f"status ERROR: {index} {ip}" )

print(index, status1, children)

sleep(0.1)

else:

sleep(0.25)

except Exception as e:

cfg.log(e)

print(e)

cfg.log(f"no location [{index}], sleep for 10 seconds and try next alpha.没有位置，睡10秒然后尝试下一个字母。”")

sleep(10)

def save_status(self, index):

cfg.status["case"] = index

cfg.log(str(cfg.status))

with open(self.case_name, "w") as f:

f.write(json.dumps(cfg.status))

def sims(self, df: pd.DataFrame, start: int=0, max_post: int=8):

print(len(df.index))

arr= []

start = cfg.status.get("case",-1)

i = 0

start+=1

for i, index in enumerate(df.index[start:], start=start):

alpha_s =  {

"type": "REGULAR",

"settings": df.loc[index]["settings"],

"regular": df.loc[index]["code"] }

arr.append(alpha_s)

# 每个槽位的数量,用户阶段需要设置为1

if len(arr) == 10:

print(arr[0])

cfg.log(f"index is: {index}")

cfg.qua.submit_simulations(index, arr, max_post=max_post)

arr = []

cfg.qua.submit_simulations(index, arr, max_post=max_post)

cfg.qua.submit_simulations(i, [], max_post=1)

def deal_data(self, df: pd.DataFrame,sharpe: float=0.9,n: int=1, save_file:str=""):

# 变更sharpe和fitness，按照原始表达式分组。按照fitness+sharpe排序取前n。

for a in df.index:

if df.loc[a]["sharpe"] <0:

df.iat[a]["code"] = "-"+df.loc[a]["code"]

df = df[df["longCount"]+df["shortCount"]>4]

df["total"] = abs(df["fitness"] + df["sharpe"])

df["exp"] = df["code"].apply(lambda x: x.split("  ")[1] if "  " in x else x)

df["op"] = df["code"].apply(lambda x: x.split("(")[1] if "(" in x else x)

df.sort_values(by="total", inplace=True,ascending=False)

df.to_csv(self.save_file +".csv")

df = df[(abs(df["sharpe"])>=sharpe) | (abs(df["fitness"]) >= 1)]

df = df.groupby(["exp", "op"]).head(n)

df = df[["code", "settings"]]

df.to_json(self.case_df)

cfg.status = {}

return df

#原始序列

def ff(df :pd.DataFrame):

return df

# ts序列

def ts_first(df: pd.DataFrame, days:list = [5, 22, 66, 252]) ->pd.DataFrame:

ts_ops = ["ts_rank", "ts_zscore", "ts_delta",  "ts_sum", "ts_delay",

"ts_std_dev", "ts_mean",  "ts_arg_min", "ts_arg_max","ts_scale", "ts_quantile"]

arr = []

for i in df.index:

for op in ts_ops:

for day in days:

arr.append({"code": f'{op}({df.loc[i]["code"]}, {day})',

"settings": df.loc[i]["settings"]})

return pd.DataFrame(arr)

def group_second(df: pd.DataFrame,):

groups=["group_rank", "group_zscore", "group_scale", "group_neutralize"]

gps = ["industry", "subindustry"]

if df.loc[df.index[0], "settings"]["region"] in ["GLB", "EUR","ASI"]:

gps += ["group_cartesian_product(country, industry)",

"group_cartesian_product(country, subindustry)"]

arr = []

for i in df.index:

for op in groups:

for gp in gps:

arr.append({"code": f'{op}({df.loc[i]["code"]}, {gp})',

"settings": df.loc[i]["settings"]})

return pd.DataFrame(arr)

def when_third(df:pd.DataFrame,) ->pd.DataFrame:

open_events = ['group_rank(ts_std_dev(returns,60),sector)>0.7',

'ts_mean(volume,5)>ts_mean(volume,60)',

'ts_zscore(returns,60)>2',

'ts_std_dev(returns, 5)>ts_std_dev(returns, 20)',

'returns<0.09',

'ts_corr(close,volume,5)>0',

'ts_corr(close,volume,5)<0',

'returns>-0.09',

"abs(returns)<0.10"]

# open_events=["rank(rp_css_business)>0.8","ts_rank(rp_css_business,22)>0.8",

# "rank(vec_avg(nws3_scores_posnormscr))>0.8",

# "ts_rank(vec_avg(nws3_scores_posnormscr),22)>0.8",]

arr=  []

for i in df.index:

for op in open_events:

arr.append({"code":f'{op}? {df.loc[i]["code"]}:-1',

"settings": df.loc[i]["settings"]})

return pd.DataFrame(arr)

def cases(func, df, sharpe=1.4, max_post=7, s_time=""):

cfg.qua.save_file = cfg.qua.data_name + f"-{func.__name__}.csv"

arrs = func(df)

if not cfg.status.get("time"):

now = datetime.datetime.now(pytz.timezone('America/New_York'))

s_time =  now.isoformat().split(".")[0]

cfg.status["time"] = s_time

cfg.status["func"] = func.__name__

print(cfg.status)

cfg.qua.sims(arrs, start=0,max_post=max_post)

df: pd.DataFrame = cfg.qua.save_result(len(arrs), cfg.status.get("time"))

df = cfg.qua.deal_data(df, sharpe=sharpe,)

return df

def log(name,):

logger = logging.getLogger(name)

formater = logging.Formatter( "[%(asctime)s] %(message)s", '%Y-%m-%d %H:%M:%S' )

logger.setLevel(logging.DEBUG)

# if not show:

file_log = logging.FileHandler(name, )

file_log.setFormatter(formater)

logger.addHandler(file_log)

ch = logging.StreamHandler()

ch.setFormatter(formater)

logger.addHandler(ch)

return logger

class cfg:

qua: quant = None

status = {}

log = None

def flow(data_name, settings: dict= {}, region= "USA",universe="TOP3000", delay=1,neu="SUBINDUSTRY" ):

cfg.qua = quant(data_name)

cfg.log = log(cfg.qua.log_name).info

# 加载原始文件

df = pd.read_csv(cfg.qua.data_name+".csv")

# 状态

if os.path.exists(cfg.qua.case_name):

with open(cfg.qua.case_name, "r") as f:

cfg.status = json.load(f)

# 存在中间过程文件

if os.path.exists(cfg.qua.case_df):

df = pd.read_json(cfg.qua.case_df)

if "settings" not in df.columns:

df["code"] = "  " + df["code"] + "  "

settings = {

"instrumentType": "EQUITY",

"region": region,

"universe": universe,

"delay": delay,

"decay": 0,

"neutralization": neu,

"truncation": 0.08,

"pasteurization": "ON",

"unitHandling": "VERIFY",

"nanHandling": "ON",

"language": "FASTEXPR",

"visualization": False }

df = df.to_dict()

df["settings"] ={i:settings for i in list(df["code"].keys())}

df = pd.DataFrame(df)

print("status: ", cfg.status)

cfg.qua.login()

funcs = [ff, ts_first, group_second, when_third,][:] #

for i, func  in enumerate(funcs):

if cfg.status.get("func") and cfg.status.get("func")!= func.__name__:

continue

# sharpe：用于筛选进入下一阶段的最低要求

df = cases(func, df, sharpe=0.7+i*0.2, max_post=8)

df: pd.DataFrame = None

for i in os.listdir(cfg.qua.path):

if data_name +"-df"  in i:

continue

if data_name +".csv" in i:

dft = pd.read_csv(cfg.qua.path+i)

df = pd.concat([df, dft])

df.to_csv(cfg.qua.data_name+"-all.csv")

flow("news18-EUR-1-TOP2500-m2-df", region="EUR", universe="TOP2500",delay=1, neu="SUBINDUSTRY")

---

## 讨论与评论 (26)

### 评论 #1 (作者: YZ88594, 时间: 9个月前)

江山代有才人出，666，手机也能回测了。感觉以后手表也能回测。

---

### 评论 #2 (作者: ZH39644, 时间: 9个月前)

手机自动化回测， 没想到还能够这样用，感谢大佬分享！ QPYTHON， 下次我也试试！

---

### 评论 #3 (作者: YH25030, 时间: 9个月前)

谢谢您的分享。我用我的旧华为手机试了一下。虽然在云电脑上跑没有问题，可是在手机上跑就会系统报错。不知道这个APP对手机性能有啥要求。还是我的技术还是有点欠缺。

---

### 评论 #4 (作者: QL33236, 时间: 9个月前)

使用termux会不会更好呢

---

### 评论 #5 (作者: DS48533, 时间: 9个月前)

慷慨啊，还附带了一套123n阶代码，研究下

---

### 评论 #6 (作者: QZ28759, 时间: 9个月前)

这篇分享太棒了！内容详实，从环境配置到避坑指南都讲得很清楚，尤其是断点续测和权限管理的提醒非常实用。代码结构清晰，扩展性强，对于移动端回测来说是很好的入门和参考。感谢作者的无私分享，期待您的下一个版本！

---

### 评论 #7 (作者: AH18340, 时间: 9个月前)

感谢大佬分享，受到大佬启发，我们是不是可以开发个安卓app自己装到手机上，然后后台运行。岂不是爽歪歪。

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #8 (作者: YX50005, 时间: 9个月前)

大佬的想法和行动能力真是太酷了！如果想省钱的话，甚至可以省略云电脑的钱。不管是外出旅游，上班摸鱼，还是通勤杀时间都是好伴侣啊。还可以对旧的安卓机进行废物利用，佩服佩服，不知道5年的前的安卓机能不能跑的动。以及长时间跑手机会不会死机

==================================Keep Fit=====================================

---

### 评论 #9 (作者: SJ65808, 时间: 9个月前)

感谢大佬分享的黑科技~~

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #10 (作者: LH44620, 时间: 9个月前)

我是用了服务器加web，这种网站的形式方便我用移动端（IOS端）来进行随时操作。并且我发现tx的云服务器可以支持浏览器端的vscode，用手机端、pad端的浏览器就可以操作vscode，还是很方便的。

---

### 评论 #11 (作者: WY52278, 时间: 9个月前)

66666666666666，没想到还能用手机回测 。感谢分享

---

### 评论 #12 (作者: NL80893, 时间: 9个月前)

--------------------------------------------------------------------------------------------------------------------------

哇哦！！！老顾问表示：“您可太厉害了！“，这岂不是随时随地便捷回测！从此坐地铁的路不再孤单~

期待在grandmaster的排行榜上看到你呀~加油加油！

--------------------------------------------------------------------------------------------------------------------------

---

### 评论 #13 (作者: MZ33049, 时间: 9个月前)

感谢分享，从未设想过的回测渠道

---

### 评论 #14 (作者: MS51256, 时间: 9个月前)

----------------------------------------------------------------------------------------------------------------------------

牛逼，想问一下ios可以吗  
还是只能安卓？
----------------------------------------------------------------------------------------------------------------------------

---

### 评论 #15 (作者: DA98440, 时间: 9个月前)

感谢分享，有时间的话我也研究一下在手机上部署

---

### 评论 #16 (作者: DD76063, 时间: 9个月前)

牛！正担心以后每天都要盯着电脑，假期出去不方便，结果没想到手机还能回测，江山代有才人出！

---

### 评论 #17 (作者: QP72475, 时间: 9个月前)

感谢，以后可以随时看回测情况了。

---

### 评论 #18 (作者: DQ66419, 时间: 9个月前)

用手机当服务器，还真是好想法，大佬动手能力真是强，有时间我也尝试下。但是本人代码基础太差，感觉要研究这个还需要花费很长时间。如果成功不了，或者有问题，再来请教大佬。另外不知道这样用会不会更费电，当然只是线程调接口的话，感觉应该情况还好一点。

---

### 评论 #19 (作者: LR93609, 时间: 9个月前)

感谢分享，算是黑科技，是否冗余？

我始终以为，自动化不是所有，只是工具，

研究小组群里面，老师多次分享印度和肯尼亚同事们的操作日常，

1. 回测极少；2. weight factor很高；3. 各项比赛排名靠前。

与之相反，国区同胞们一直在搞自动化，占了平台70%以上的算力。

我一直在思考这个问题，是不是我们跑偏了，误入歧途.....

------------------------------------------------------------------------

凡是发生，皆利于我；愿我所愿，尽是美好

------------------------------------------------------------------------

---

### 评论 #20 (作者: RJ74200, 时间: 9个月前)

回答一些问题: ios设备上一样可以运行，可能需要装的app不一样。对于回测量大的问题。许多数据集里面每个字段都有几十上百个alpha，基本可以说明任何一个字段在数据不缺省的情况下几乎都能做出alpha。但是往往达不到这样的能力，更多是无限搜索来获取符合要求的alpha,就像说的目前国区做ra能力较弱一些。如果有能把随意的字段做成提交alpha的能力，我觉得基本上可以boss直聘了。

---

### 评论 #21 (作者: AM12075, 时间: 9个月前)

--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
这个代码需要手机整天开着吗，还是会在后台运行呢，对电池有没有损害呢？
--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------

---

### 评论 #22 (作者: TS96358, 时间: 8个月前)

=====================早日冲上GrandMaster============================================

这个太合适了，可以用手机来看回测，国庆假期刚好合适

==================千磨万击还坚劲，任尔东西南北风======================================

---

### 评论 #23 (作者: DZ31817, 时间: 8个月前)

20251001

------------------------------------------------------------------------------------------

感谢分享，之前还有群友用树莓派来跑回测，真是异曲同工了。不过手机性能不同可能跑起来也不一样，如果是便宜的闲置手机来跑，不知道一批能支持回测多大的量，我用的便宜服务器一批回测超过5万个就会爆内存卡死了。

---

### 评论 #24 (作者: SZ20589, 时间: 8个月前)

感谢大佬分享，用手机当服务器，真是艺高人胆大，大佬动手能力和执行能力真是强，有时间我也尝试下。。

大佬的实践和创新精神真是惊为天人，有这种创新和实践精神，不管大佬干什么行业，大佬都会是业界翘楚，行业标杆。祝愿大佬早日GM， VF经久1.0。

再次感谢大佬

=============================================================================

========Genius is one percent inspiration and ninety-nine percent perspiration.=============

==============================================================================

---

### 评论 #25 (作者: JS16353, 时间: 8个月前)

看来CPU不是问题呀，我准备用树莓派试试了。

---

### 评论 #26 (作者: JY55846, 时间: 3个月前)

==============================================================================

手机端的这个听起来很不错终于不用每日背着电脑，跟着试试看，革命还要继续加油

==============================================================================

---

