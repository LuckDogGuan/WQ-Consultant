# 脚本记录Osmosis point每日变化代码优化

- **链接**: 脚本记录Osmosis point每日变化代码优化.md
- **作者**: WL27618
- **发布时间/热度**: 5个月前, 得票: 61

## 帖子正文

不知道Osmosis point的leaderboard的api之后会不会变化, 我想既然之后每周都要更新osmosis point, 用定时脚本记录历史变化应该比较有必要. 方便自己监测质量
 ![图片](images/img_8e34b31ac1.png)

# monitor_osmosis.py

import asyncio

import aiohttp

import json

import logging

import os

import pandas as pd

from datetime import datetime

import sys

# Add project root to sys.path to allow imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from util.network_util import _request_with_retry

from api.login import async_login_to_brain

logger = logging.getLogger("OsmosisMonitor")

OSMOSIS_URL = " [https://api.worldquantbrain.com/competitions/OC2025](https://api.worldquantbrain.com/competitions/OC2025) "

HISTORY_FILE = "osmosis_history.json"

# ======================================================

# ✅ 1. Fetch Osmosis Data

# ======================================================

async def fetch_osmosis_data(session) -> dict:

"""Fetch data from the Osmosis Competition API."""

logger.info(f"Fetching Osmosis data from {OSMOSIS_URL}...")

try:

data = await _request_with_retry(session=session, url=OSMOSIS_URL)

return data

exceptExceptionas e:

logger.error(f"Failed to fetch Osmosis data: {e}")

returndict()

# ======================================================

# ✅ 2. Compare and Update History

# ======================================================

def process_and_save(current_data: dict):

"""

Load history, compare current user stats with the last record,

print a summary of changes, and save the new record.

"""

ifnot current_data or"leaderboard"notin current_data:

logger.warning("⚠️ No user stats found in 'leaderboard' field.")

return

# Use actual date for daily tracking

now = datetime.now()

today_date = now.strftime("%Y-%m-%d")

today_full = now.strftime("%Y-%m-%d %H:%M:%S")

current_stats = current_data["leaderboard"]

# Load history

history = dict()

if os.path.exists(HISTORY_FILE):

try:

withopen(HISTORY_FILE, "r") as f:

history = json.load(f)

exceptExceptionas e:

logger.error(f"Failed to read history file: {e}")

# Find the latest previous record

sorted_dates = sorted([d for d in history.keys() if d < today_date], reverse=True)

last_date = sorted_dates[0] if sorted_dates else None

last_record = history.get(last_date, dict()) if last_date else dict()

last_stats = last_record.get("stats", dict())

if last_date:

logger.info(f"Comparing with last record from: {last_date}")

else:

logger.info("No previous records found for comparison.")

# --- 1. General Metrics ---

general_metrics = ['rank', 'totalScore']

general_summary = []

for key in general_metrics:

curr_val = current_stats.get(key)

prev_val = last_stats.get(key)

change_str = ""

if curr_val isnotNoneand prev_val isnotNone:

diff = curr_val - prev_val

if diff >0:

change_str = f" (🔺 +{diff})"

if key =="rank": change_str =f" (🔻 +{diff})"# Drop in rank

elif diff <0:

change_str = f" (🔻 {diff})"

if key =="rank": change_str =f" (🔺 {diff})"# Improve in rank

val_str = f"{curr_val}{change_str}" if curr_val is not None else "N/A"

general_summary.append(f"{key.capitalize()}: {val_str}")

print("\n🏆 My Osmosis Performance Update:")

print(f"📅 Today: {today_full}")

print(" | ".join(general_summary))

print("-"*60)

# --- 2. Regional Metrics Table ---

regions = ['ASI', 'EUR', 'GLB', 'IND', 'USA']

metric_map = {

'cumulativePNL': 'PnL',

'osmosisAlphas': 'Alphas',

'osmosisOSAfterCostIRRank': 'IR Rank',

'osmosisPointsAllocated': 'Points'

}

region_rows = []

for region in regions:

row = {'Region': region}

for prefix, col_name in metric_map.items():

full_key = f"{prefix}{region}"

curr_val = current_stats.get(full_key)

prev_val = last_stats.get(full_key)

val_str = str(curr_val) if curr_val is not None else "N/A"

if curr_val isnotNoneand prev_val isnotNoneandisinstance(curr_val, (int, float)):

diff = curr_val - prev_val

if diff !=0:

sign = "+" if diff > 0 else ""

# Logic: Rank -> lower is better (green), others -> higher is better (green)

# Use standard arrows for direction, user interprets meaning

icon ="🔺"if diff >0else"🔻"

# Context aware icon coloring (simulated)

if"Rank"in col_name:

# Rank increase (numeric) is bad

pass

val_str += f" ({icon} {sign}{diff})"

row[col_name] = val_str

region_rows.append(row)

df_regions = pd.DataFrame(region_rows)

ifnot df_regions.empty:

pd.set_option('display.max_rows', None)

pd.set_option('display.width', 1000)

# Reorder columns

cols = ['Region', 'PnL', 'Alphas', 'IR Rank', 'Points']

print(df_regions[cols].to_string(index=False))

else:

print("No regional metrics found.")

# Save today's record (overwrite if run multiple times today)

history[today_date] = {

"updated_at": today_full,

"stats": current_stats

}

try:

withopen(HISTORY_FILE, "w") as f:

json.dump(history, f, indent=2)

logger.info(f"\n✅ History updated in {HISTORY_FILE}")

exceptExceptionas e:

logger.error(f"Failed to save history: {e}")

# ======================================================

# ✅ 3. Main Workflow

# ======================================================

async def main():

asyncwith aiohttp.ClientSession() as session:

# 1. Login

await async_login_to_brain(session)

# 2. Fetch Data

data = await fetch_osmosis_data(session)

# 3. Process and Save

process_and_save(data)

if __name__ == "__main__":

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

asyncio.run(main())

log是这样, 会存一个history的json

![图片](images/img_1528342cf9.png)

---

## 讨论与评论 (2)

### 评论 #1 (作者: XZ81923, 时间: 5个月前)

谁告诉你每周要变化的？哪里来的消息？

---

### 评论 #2 (作者: LK39823, 时间: 2个月前)

=================================================================================

现在已经有统计的网站了，是可视化的，这个用不到了，不过感谢大佬的分享

===============================================================================                                                                                                 ================================自信人生两百年，会当水击三千里==========================

---

