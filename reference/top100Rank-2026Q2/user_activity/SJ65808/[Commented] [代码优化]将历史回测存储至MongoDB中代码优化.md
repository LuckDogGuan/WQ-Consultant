# [代码优化]将历史回测存储至MongoDB中代码优化

- **链接**: [Commented] [代码优化]将历史回测存储至MongoDB中代码优化.md
- **作者**: WD55029
- **发布时间/热度**: 3个月前, 得票: 62

## 帖子正文

将回测存储在本地数据库有许多好处。首先可以方便自己检索全部回测，更精细化的筛选需要提交的内容。其次在回测限流5000的时代，我们可以通过检测哈希值避免重复回测从而更高效的利用我们回测的机会。我个人选择了MongoDB因为官方API的simulation是json格式，传统关系型数据库建表复杂，而MongoDB可以直接储存json，使用起来很直接方便。

我这里分享一个我自己使用的将回测存储至本地mongoDB的python脚本，以及我经常会使用的一些query命令。

```

import sqlite3

import sys

import re

import os

import pandas as pd

import hashlib

from pymongo import MongoClient, ASCENDING

import json

# Set default save directory to the current script's directory (database folder)

DEFAULT_SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(DEFAULT_SAVE_DIR, exist_ok=True)

# Change working directory to the script's directory

os.chdir(DEFAULT_SAVE_DIR)

print(f"Changed working directory to: {DEFAULT_SAVE_DIR}")

from machine_lib import *

from typing import Dict, List, Optional, Sequence, Tuple, Union

import requests

import pickle

import os

# 定义登录函数

def login():

session = requests.Session()

login_url = " [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) "

username = "YOUR_USERNAME"

password = "YOUR_PASSWORD"

session.auth = (username, password)

response = session.post(login_url)

if response.status_code == 201:

print(response.content)

return session

else:

raise Exception("Login failed")

def fetch_alphas_by_date_range(

session: requests.Session, start_date: str, end_date: str

) -> List[Dict]:

"""Return submitted (OS) alphas within the date range (inclusive).

Args:

start_date: Start date in YYYY-MM-DD format.

end_date: End date in YYYY-MM-DD format.

"""

print(f"Fetching alphas from {start_date} to {end_date}...")

# Ensure dates are comparable strings (ISO format works for string comparison)

# Append time to make full comparison easy

# User suggested format: 2025-11-01T04:00:00.000Z

start_iso = f"{start_date}T00:00:00Z"

end_iso = f"{end_date}T23:59:59Z"

alphas: List[Dict] = []

limit = 50

offset = 0

while True:

# Use server-side filtering for performance

params = {

"stage": "OS",

"order": "-dateSubmitted",

"limit": limit,

"offset": offset,

"dateSubmitted>": start_iso,

"dateSubmitted<": end_iso,

}

BASE_URL = " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) "

resp = session.get(f"{BASE_URL}/users/self/alphas", params=params)

resp.raise_for_status()

payload = resp.json()

results = payload.get("results", []) if isinstance(payload, dict) else payload

if not results:

break

alphas.extend(results)

offset += limit

total = payload.get("count", 0) if isinstance(payload, dict) else 0

if offset >= total or len(results) < limit:

break

return alphas

def fetch_simulated_alphas_by_date_range(

session: requests.Session, start_date: str, end_date: str

) -> List[Dict]:

"""Return submitted (OS) alphas within the date range (inclusive).

Args:

start_date: Start date in YYYY-MM-DD format.

end_date: End date in YYYY-MM-DD format.

"""

print(f"Fetching alphas from {start_date} to {end_date}...")

# Ensure dates are comparable strings (ISO format works for string comparison)

# Append time to make full comparison easy

# User suggested format: 2025-11-01T04:00:00.000Z

start_iso = f"{start_date}T00:00:00Z"

end_iso = f"{end_date}T23:59:59Z"

alphas: List[Dict] = []

limit = 100

offset = 0

while True:

# Use server-side filtering for performance

params = {

"status": "UNSUBMITTED\x1FIS_FAIL",

"order": "-dateCreated",

"limit": limit,

"offset": offset,

"dateCreated>": start_iso,

"dateCreated<": end_iso,

"hidden": "false"

}

BASE_URL = " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) "

resp = session.get(f"{BASE_URL}/users/self/alphas", params=params)

resp.raise_for_status()

payload = resp.json()

results = payload.get("results", []) if isinstance(payload, dict) else payload

if not results:

break

alphas.extend(results)

offset += limit

total = payload.get("count", 0) if isinstance(payload, dict) else 0

print(offset)

if offset >= total or len(results) < limit:

break

return alphas

def save_alpha_json_by_date(start_date, end_date):

# 获取session（自动处理登录）

session = login()

# 使用session进行请求

response = session.get(' [https://platform.worldquantbrain.com/alphas/unsubmitted](https://platform.worldquantbrain.com/alphas/unsubmitted) ')

# print(response.text)

date_range = pd.date_range(start=start_date, end=end_date)

for cur_date in [date.strftime(f"%Y-%m-%d") for date in date_range]:

alphas = fetch_simulated_alphas_by_date_range(session, cur_date, cur_date)

with open(f'alpha_json/{cur_date}.json', 'w', encoding='utf-8') as f:

json.dump(alphas, f, ensure_ascii=False)

f.close()

# 使用示例

if __name__ == "__main__":

# save_alpha_json_by_date("2026-01-23", "2026-01-23")

start_date = "2026-03-01"

end_date = "2026-03-03"

save_alpha_json_by_date("2026-03-01", "2026-03-03")

date_range = pd.date_range(start=start_date, end=end_date)

# print(date_range)

client = MongoClient("mongodb://localhost:27017/")

# client.admin.command('ping')

db = client["worldquant"]

# Create a collection (similar to a table in SQL)

collection = db["simulated_alpha"]

# print("Connected to MongoDB successfully!")

for cur_date in [date.strftime(f"%Y-%m-%d") for date in date_range]:

print(cur_date)

with open(f"alpha_json/{cur_date}.json", 'r', encoding='utf-8') as f:

alphas = json.load(f)

for alpha in alphas:

# print(alpha)

settings = alpha["settings"]

if alpha['type'] == "REGULAR":

expr = alpha["regular"]["code"]

dict_str = json.dumps(settings, sort_keys=True)

expr_no_whitespace = re.sub(r'\s+', '', expr)

expr_str = expr_no_whitespace.replace("'", '"')

combined = f"{dict_str}{expr_str}"

hash_obj = hashlib.sha256(combined.encode('utf-8'))

hash_str = hash_obj.hexdigest()

alpha["hash"] = hash_str

elif alpha['type'] == "SUPER":

combo_expr = alpha["combo"]["code"]

selection_expr = alpha["selection"]["code"]

dict_str = json.dumps(settings, sort_keys=True)

expr = combo_expr + selection_expr

expr_no_whitespace = re.sub(r'\s+', '', expr)

expr_str = expr_no_whitespace.replace("'", '"')

combined = f"{dict_str}{expr_str}"

hash_obj = hashlib.sha256(combined.encode('utf-8'))

hash_str = hash_obj.hexdigest()

alpha["hash"] = hash_str

else:

pass

existing = collection.find_one({"hash": hash_str})

if existing is None:

collection.insert_one(alpha)

print("DONE")

```

此脚本使用时只需要修改28、29行的登录信息和157、158行的起止时间。

我这里是单独对expression和settings合并的字符串进行哈希，避免了因为expression中含有空格或者单引号双引号不同产生不同的哈希值。

下面分享一个我用来查询指定地区包含指定字段的回测的query命令，在补六维时可以使用

{
  $and: [
    { "regular.code": RegExp("ts_corr", "i") },
    { "settings.region": "EUR" },
    { "is.sharpe": { $gt: 1.58 } },
    { "settings.universe": "TOPCS1600" }
  ]
}

---

## 讨论与评论 (8)

### 评论 #1 (作者: XB37939, 时间: 3个月前)

厉害，我把成功的回测存到了mysql中，方便提交，回顾，学习，参考

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #2 (作者: LN22094, 时间: 3个月前)

之前也有这种想法，只不过我是将结果按照模板名分别存储，最后利用ai对csv表格进行分析

感觉数据库有点重（主要原因是也不太会）

感谢大佬的代码，今天就试试

---

### 评论 #3 (作者: AM12075, 时间: 3个月前)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

检测哈希值避免重复回测是什么原理，和检测相关性一样吗？代码中有体现吗？

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #4 (作者: SJ65808, 时间: 3个月前)

感谢大佬分享，数据量上来了，数据库还是少不了的

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #5 (作者: MY49971, 时间: 3个月前)

一直用的是mysql，是时候学习一下MongoDB了

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #6 (作者: CZ16695, 时间: 3个月前)

非常有意义,  感谢

====================================================================================
==================慢就是快==========================================================

---

### 评论 #7 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的代码分享，感觉可以用这个进行复盘                                                                              ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #8 (作者: HZ53355, 时间: 2个月前)

可以尝试一下PostgreSQL，一个数据库就足够

---

