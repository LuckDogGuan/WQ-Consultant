# 网页回测很卡，摆脱网页手搓

- **链接**: [Commented] 网页回测很卡摆脱网页手搓.md
- **作者**: ZL15100
- **发布时间/热度**: 2个月前, 得票: 32

## 帖子正文

本程序的作用：1，拜托网页回测。2，还可以回测所有的中性化和maxtrade开启或者不开启。

使用方法：注释里面都写清楚了，我还是说明一下。alphaid参数是你要在哪个alpha的基础上进行优化；test_all_netu = True时，是遍历所有中性化，maxtrade；test_all_netu = False时，往express_arr 里面添加要回测的表达式，即可进行批量回测，速度很快。

下面是全部的代码

import copy

import requests

import time

from time import sleep

import json

import pandas as pd

import random

import pickle

from urllib.parse import urljoin

from itertools import product

from itertools import combinations

from collections import defaultdict

import os

from os import environ

from os.path import expanduser

import datetime

import numpy as np

alpha_id = 'KPwOMNk1' # O05b13Xb

test_all_netu = True #测试所有风险中性化

test_all_netu = False #配置不变，测试不同的表达式，代替网页手搓

express_arr = [] #优化的表达式，test_all_netu=False时，往里面添加表达式

alpha_name = alpha_id

sess = login()

so_tracker = my_locate_alpha(sess, alpha_id)

alphas = [] # 'STATISTICAL'

region = so_tracker['settings']['region']

netu_all = []

if region != 'IND':

netu_all = ['STATISTICAL','REVERSION_AND_MOMENTUM','SLOW_AND_FAST', 'FAST', 'SLOW', 'CROWDING', 'MARKET', 'SECTOR', 'INDUSTRY','SUBINDUSTRY']

else:

netu_all = ['REVERSION_AND_MOMENTUM','SLOW_AND_FAST', 'FAST', 'SLOW', 'CROWDING', 'MARKET','SECTOR', 'INDUSTRY','SUBINDUSTRY']

#netu_all = ['REVERSION_AND_MOMENTUM','SLOW_AND_FAST', 'FAST', 'SLOW', 'CROWDING']

max_trade = ['ON','OFF']

th_alpha_list = []

if not test_all_netu:

for express in express_arr:

th_alpha_list.append({"type":so_tracker["type"], "settings":so_tracker["settings"], "regular": express})

else :

for netu in netu_all: #maxTrade

for maxtrade in max_trade:

alpha2 = copy.deepcopy(so_tracker)

alpha2['settings']['neutralization'] = netu

alpha2['settings']['maxTrade'] = maxtrade

th_alpha_list.append(alpha2)

print("表达式数量:%s"%len(th_alpha_list))

if test_all_netu:

every_mul_count = 8

mul_count = 3

else :

every_mul_count = 8

mul_count = 7

fo_pools = load_task_pool(th_alpha_list, every_mul_count, mul_count)

multi_simulate_2(fo_pools, alpha_name, 0)

#my_locate_alpha函数如下：

def my_locate_alpha(s, alpha_id):

while True:

alpha = s.get(" [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id)

if "retry-after" in alpha.headers:

time.sleep(float(alpha.headers["Retry-After"]))

else:

break

string = alpha.content.decode('utf-8')

metrics = json.loads(string)

typ = metrics['type']

settings = metrics["settings"]

exp = metrics['regular']['code']

exp = exp.replace('\r', '').replace('\n', '')

sharpe = metrics["is"]["sharpe"]

if sharpe < 0:

exp = "-%s"%exp

return {"type":typ, "settings":settings, "regular": exp}

#multi_simulate_2函数如下：

def multi_simulate_2(alpha_pools, alpha_name, start):#batch_size 没批次个数，比如6X6=36

s = login()

brain_api_url = ' [https://api.worldquantbrain.com](https://api.worldquantbrain.com) '

for x, pool in enumerate(alpha_pools):

if x < start: continue

progress_urls = []

for y, task in enumerate(pool):

# 10 tasks, 10 alpha in each task

sim_data_list = task

try:

simulation_response = s.post(' [https://api.worldquantbrain.com/simulations](https://api.worldquantbrain.com/simulations) ', json=sim_data_list)

simulation_progress_url = simulation_response.headers['Location']

progress_urls.append(simulation_progress_url)

except:

print("location key error: %s"%simulation_response.content)

sleep(600)

s = login()

import datetime

time_now = datetime.datetime.now()

print("%s pool %d task %d post done"%(time_now,x,y))

get_alpha_id_url = []

for j, progress in enumerate(progress_urls):

try:

while True:

simulation_progress = s.get(progress)

if simulation_progress.headers.get("Retry-After", 0) == 0:

break

#print("Sleeping for " + simulation_progress.headers["Retry-After"] + " seconds")

sleep(float(simulation_progress.headers["Retry-After"]))

status = simulation_progress.json().get("status", 0)

if status != "COMPLETE":

print("Not complete : %s"%(progress))

else:

children = simulation_progress.json().get("children", 0)

for child in children:

get_alpha_id_url.append(brain_api_url + "/simulations/" + child)

except KeyError:

print("look into: %s"%progress)

except Exception as e:

print(f"other error: {e}")

time_now = datetime.datetime.now()

print("%s pool %d task %d simulate done"%(time_now, x, j))

if len(get_alpha_id_url) > 0:

thread = threading.Thread(target=lambda: thread_set_property(get_alpha_id_url, alpha_name))

thread.start()

print("Simulate done")

thread_set_property函数如下：

def thread_set_property(getalphaid_url,alpha_name):

s = login()

print(f"start thread_set_property")

count = 0

for url in getalphaid_url:

count += 1

alpha_id = ''

try:

child_progress = s.get(url)

alpha_id = child_progress.json()["alpha"]

res_alpha = locate_alpha(s, alpha_id) #[alpha_id, exp, sharpe, turnover, fitness, returns, drawdown ,margin, dateCreated, decay]

tags = ['0']

if((res_alpha[3] <= 0.4 and abs(res_alpha[2]) >= 1.2 and abs(res_alpha[7]) >= 0.0009) or

(res_alpha[3] <= 0.4 and abs(res_alpha[2]) >= 1.5 and abs(res_alpha[7]) >= 0.001) or

###判断是否优秀因子(换手率，sharpe, margin)

(res_alpha[3] <= 0.6 and abs(res_alpha[2]) >= 2.0 and abs(res_alpha[7]) >= 0.0015)):

if get_alpha_pnl_legal(s, alpha_id):

tags = ['1']

set_alpha_properties(s,alpha_id,name = alpha_name,color = None, tags = tags)

sleep(0.1)

except:

print(f'###注意异常： {alpha_id} {url}')

sleep(1)

s = login()

print(f"thread_set_property finish: {count}")

#thread_set_property函数如下

def thread_set_property(getalphaid_url,alpha_name):

s = login()

print(f"start thread_set_property")

count = 0

for url in getalphaid_url:

count += 1

alpha_id = ''

try:

child_progress = s.get(url)

alpha_id = child_progress.json()["alpha"]

res_alpha = locate_alpha(s, alpha_id) #[alpha_id, exp, sharpe, turnover, fitness, returns, drawdown ,margin, dateCreated, decay]

tags = ['0']

if((res_alpha[3] <= 0.4 and abs(res_alpha[2]) >= 1.2 and abs(res_alpha[7]) >= 0.0009) or

(res_alpha[3] <= 0.4 and abs(res_alpha[2]) >= 1.5 and abs(res_alpha[7]) >= 0.001) or

###判断是否优秀因子(换手率，sharpe, margin)

(res_alpha[3] <= 0.6 and abs(res_alpha[2]) >= 2.0 and abs(res_alpha[7]) >= 0.0015)):

if get_alpha_pnl_legal(s, alpha_id):

tags = ['1']

set_alpha_properties(s,alpha_id,name = alpha_name,color = None, tags = tags)

sleep(0.1)

except:

print(f'###注意异常： {alpha_id} {url}')

sleep(1)

s = login()

print(f"thread_set_property finish: {count}")

#set_alpha_properties函数如下：

def set_alpha_properties(

s,

alpha_id,

name: str = None,

color: str = None,

selection_desc: str = "None",

combo_desc: str = "None",

tags: str = ["ace_tag"],

):

"""

Function changes alpha's description parameters

"""

params = {

"color": color,

"name": name,

"tags": tags,

"category": None,

"regular": {"description": None},

"combo": {"description": combo_desc},

"selection": {"description": selection_desc},

}

response = s.patch(

" [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id, json=params

)

---

## 讨论与评论 (4)

### 评论 #1 (作者: CC35164, 时间: 2个月前)

不错不错，是比网页快一点点，已亲测！

---

### 评论 #2 (作者: FZ60707, 时间: 2个月前)

感谢分享这么详细的代码！终于可以摆脱网页回测的卡顿了，批量测试中性化和maxtrade的脚本非常实用，回头我也试试看

========================================================================================================================================================================

---

### 评论 #3 (作者: YY51812, 时间: 2个月前)

还是不太明白怎么用？代码小白求指教，我现在网页特别卡，阿尔法一个也提交不上去

---

### 评论 #4 (作者: ZL15100, 时间: 1个月前)

@ [Yin yi yi(YY51812)](/hc/en-us/profiles/39688454512023-Yin-yi-yi-YY51812) 
给alpha_id赋值就可以了，即你需要优化哪个alpha的id

---

