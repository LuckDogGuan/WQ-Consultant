# 【经验分享】【未完成】基于Genius Rank插件进一步评估自己和各个Genius Level的守门员还有多大差距

- **链接**: 【经验分享】【未完成】基于Genius Rank插件进一步评估自己和各个Genius Level的守门员还有多大差距.md
- **作者**: RM49262
- **发布时间/热度**: 9个月前, 得票: 1

## 帖子正文

插件地址： [https://github.com/zhangkaihua88/WebDataScope](https://github.com/zhangkaihua88/WebDataScope)

首先还是感谢大佬开发的Genius Rank插件，非常方便又好用！

目前临近季度末尾，有不少人会在季末冲一波Genius榜单，但目前插件唯一的美中不足就是我不知道对于 **Operator Per Alpha** 以及 **Field Per Alpha** 这两个数据，在最后这段时间里我究竟要把 **每天新交的alpha具体限制到一个怎样的水平** 才能追上前面的人。

所以我Vibe coding了一下，把插件获取的Genius列表进行进一步简单分析，评估自己在季度末这段时间如何能更有机会追上前面的人。只是简单的经验分享，如有不足还请各位指正。

1. 首先是导出Genius Rank的json文件。目前最新版本的WorldQuant Scope插件已经有了导出json文件的功能。但不知为何我在Chrome上运行的时候一直报错。所以这里再分享一个从Chrome中直接获取Genius Rank列表的方法：

打开Genius网页→F12打开控制台→Application→Extension Storage→ Worldquant Scope→ Local → WQPRANKDATA  然后在下方右键复制即可

2.以下是我Vibe Coding的Python代码，主要作用就是

- 向上差距对比: 对Gold/Expert/Master用户，与下一目标等级最后一名用户的对比

- 向下优势对比: 对Expert/Master/Grandmaster用户，与当前等级最后一名用户的对比

- 可视化进度条: 直观显示各项指标的差距

- 根据不同的每日提交频率（1-4个 Alpha/天）计算：

- 新 Alpha 需要达到的 Operator Avg 和 Field Avg

- 可行性评估（标注"不可能"的情况）

import json

import math

from datetime import datetime, timedelta

from typing import Dict, List, Tuple, Optional, Any

class GeniusRankingAnalyzer:

"""Main class for analyzing Genius rankings and generating improvement recommendations."""

def __init__(self, rank_data_path: str = "rank.json"):

"""

Initialize the analyzer with ranking data.

Args:

rank_data_path: Path to the rank.json file

"""

self.rank_data_path = rank_data_path

self.data = self._load_data()

# Level criteria from genius.js

self.level_criteria = {

"expert": {

"alphaCount": 20,

"pyramidCount": 10,

"combinedAlphaPerformance": 0.5,

"combinedSelectedAlphaPerformance": 0.5

},

"master": {

"alphaCount": 120,

"pyramidCount": 20,

"combinedAlphaPerformance": 1.0,

"combinedSelectedAlphaPerformance": 1.0

},

"grandmaster": {

"alphaCount": 220,

"pyramidCount": 50,

"combinedAlphaPerformance": 2.0,

"combinedSelectedAlphaPerformance": 2.0

}

}

# Six-dimensional metrics (in display order) - matching genius.js exactly

self.metrics_higher_better = ["operatorCount", "fieldCount", "communityActivity", "maxSimulationStreak"]

self.metrics_lower_better = ["operatorAvg", "fieldAvg"]

# Display order: Operator Count, Field Count, Operator Avg, Field Avg, Community Activity, Max Simulation Streak

self.all_metrics = ["operatorCount", "fieldCount", "operatorAvg", "fieldAvg", "communityActivity", "maxSimulationStreak"]

# Calculate level distributions

self._calculate_level_distributions()

def _load_data(self) -> List[Dict]:

"""Load and parse the rank.json data."""

try:

with open(self.rank_data_path, 'r', encoding='utf-8') as f:

json_data = json.load(f)

return json_data.get('array', [])

except FileNotFoundError:

raise FileNotFoundError(f"Could not find {self.rank_data_path}. Please ensure the file exists.")

except json.JSONDecodeError as e:

raise ValueError(f"Invalid JSON format in {self.rank_data_path}: {e}")

def _calculate_level_distributions(self):

"""Calculate the number of users for each level based on the base count."""

# Assume minimum alpha count for base users (you might need to adjust this)

base_alpha_count = 20  # This should be configured based on actual settings

self.base_count = len([user for user in self.data if user.get('alphaCount', 0) >= base_alpha_count])

self.level_counts = {

'grandmaster': math.ceil(self.base_count * 0.02),

'master': math.ceil(self.base_count * 0.08),

'expert': math.ceil(self.base_count * 0.2)

}

def determine_user_level(self, user_data: Dict, use_final_level: bool = True) -> str:

"""

Determine the user's level based on the full ranking system.

Args:

user_data: User's data dictionary

use_final_level: Whether to use finalLevel (True) or achievedLevel (False)

Returns:

User's final level ('gold', 'expert', 'master', 'grandmaster')

"""

if use_final_level:

# Use the complete ranking system like genius.js

all_data = self.calculate_all_levels_and_boundaries()

user_id = user_data.get('user')

for user in all_data['data']:

if user.get('user') == user_id:

return user.get('finalLevel', 'gold')

return 'gold'

else:

# Legacy method for achievedLevel only

for level in ["grandmaster", "master", "expert"]:

criteria = self.level_criteria[level]

# Check basic conditions

alpha_check = user_data.get('alphaCount', 0) >= criteria['alphaCount']

pyramid_check = user_data.get('pyramidCount', 0) >= criteria['pyramidCount']

if not (alpha_check and pyramid_check):

continue

return level

return 'gold'

def calculate_rankings_for_level(self, users: List[Dict], level: str) -> List[Dict]:

"""

Calculate six-dimensional rankings for users at a specific level.

Args:

users: List of user data

level: Level to calculate rankings for

Returns:

List of users with calculated rankings

"""

# Filter users based on level criteria

if level != 'gold':

criteria = self.level_criteria[level]

qualified_users = []

for user in users:

if (user.get('alphaCount', 0) >= criteria['alphaCount'] and

user.get('pyramidCount', 0) >= criteria['pyramidCount']):

# For now, skip performance check to match the original logic

qualified_users.append(user.copy())

else:

qualified_users = [user.copy() for user in users]

# Initialize total rank

for user in qualified_users:

user['totalRank'] = 0

# Calculate rankings for "higher is better" metrics

for metric in self.metrics_higher_better:

values = [user.get(metric, 0) for user in qualified_users]

sorted_values = sorted(values, reverse=True)

for user in qualified_users:

user_value = user.get(metric, 0)

try:

rank = sorted_values.index(user_value) + 1

except ValueError:

rank = len(sorted_values)

user[f'{metric}Rank'] = rank

user['totalRank'] += rank

# Calculate rankings for "lower is better" metrics

for metric in self.metrics_lower_better:

values = [user.get(metric, 0) for user in qualified_users]

sorted_values = sorted(values)

for user in qualified_users:

user_value = user.get(metric, 0)

try:

rank = sorted_values.index(user_value) + 1

except ValueError:

rank = len(sorted_values)

user[f'{metric}Rank'] = rank

user['totalRank'] += rank

return qualified_users

def find_user_by_id(self, user_id: str) -> Optional[Dict]:

"""Find a user by their ID."""

for user in self.data:

if user.get('user', '') == user_id:

return user

return None

def calculate_all_levels_and_boundaries(self) -> Dict:

"""

Calculate all user levels and boundaries exactly like genius.js

Returns:

Dictionary with processed data and boundaries

"""

# Make a copy of data to avoid modifying original

data = [user.copy() for user in self.data]

# Initialize finalLevel to 'gold' for all users

for item in data:

item['finalLevel'] = 'gold'

# Calculate rankings for each model (exactly like genius.js)

for model in ["gold", "expert", "master", "grandmaster"]:

if model == 'gold':

itemData = [dict(item, originalIndex=index) for index, item in enumerate(data)]

else:

# Filter by level criteria

criteria = self.level_criteria[model]

itemData = []

for index, item in enumerate(data):

if(item.get('alphaCount',0)>=criteria['alphaCount']and

item.get('pyramidCount', 0) >= criteria['pyramidCount']):

# For now, skip performance check like in genius.js (geniusCombineTag logic)

itemData.append(dict(item, originalIndex=index))

# Calculate totalRank for this model

for item in itemData:

item['totalRank'] = 0

# Calculate ranks for "higher is better" metrics

for col in ["operatorCount", "fieldCount", "communityActivity", "maxSimulationStreak"]:

sorted_values = sorted([item.get(col, 0) for item in itemData], reverse=True)

for item in itemData:

value = item.get(col, 0)

try:

rank = sorted_values.index(value) + 1

except ValueError:

rank = len(sorted_values)

item[col + 'Rank'] = rank

item['totalRank'] += rank

# Calculate ranks for "lower is better" metrics

for col in ["operatorAvg", "fieldAvg"]:

sorted_values = sorted([item.get(col, 0) for item in itemData])

for item in itemData:

value = item.get(col, 0)

try:

rank = sorted_values.index(value) + 1

except ValueError:

rank = len(sorted_values)

item[col + 'Rank'] = rank

item['totalRank'] += rank

# Update original data with calculated ranks

for item in itemData:

original_index = item['originalIndex']

data[original_index][model + 'TotalRank'] = item['totalRank']

for col in ["operatorCount", "fieldCount", "communityActivity", "maxSimulationStreak", "operatorAvg", "fieldAvg"]:

data[original_index][model + col + 'Rank'] = item.get(col + 'Rank', 0)

data[original_index]['achievedLevel'] = model

# Calculate level counts based on base users

base_alpha_count = 20  # Assuming minimum alpha count like genius.js

baseCount = len([user for user in data if user.get('alphaCount', 0) >= base_alpha_count])

grandmasterCount = round(baseCount * 0.02)

masterCount = round(baseCount * 0.08)

expertCount = round(baseCount * 0.2)

# Assign final levels (exactly like genius.js)

# Expert assignment

expert_eligible = [item for item in data if item.get('achievedLevel') in ['expert', 'master', 'grandmaster']]

expert_eligible.sort(key=lambda x: x.get('expertTotalRank', float('inf')))

for index, item in enumerate(expert_eligible):

if index < expertCount + masterCount + grandmasterCount:

# Find original item in data and update

for orig_item in data:

if orig_item.get('user') == item.get('user'):

orig_item['finalLevel'] = 'expert'

break

# Master assignment

master_eligible = [item for item in data if item.get('achievedLevel') in ['master', 'grandmaster']]

master_eligible.sort(key=lambda x: x.get('masterTotalRank', float('inf')))

for index, item in enumerate(master_eligible):

if index < masterCount + grandmasterCount:

# Find original item in data and update

for orig_item in data:

if orig_item.get('user') == item.get('user'):

orig_item['finalLevel'] = 'master'

break

# Grandmaster assignment

grandmaster_eligible = [item for item in data if item.get('achievedLevel') == 'grandmaster']

grandmaster_eligible.sort(key=lambda x: x.get('grandmasterTotalRank', float('inf')))

for index, item in enumerate(grandmaster_eligible):

if index < grandmasterCount:

# Find original item in data and update

for orig_item in data:

if orig_item.get('user') == item.get('user'):

orig_item['finalLevel'] = 'grandmaster'

break

# Find boundaries (last person in each final level)

boundaries = {}

for level in ['expert', 'master', 'grandmaster']:

level_users = [user for user in data if user.get('finalLevel') == level]

if level_users:

# Sort by the appropriate totalRank

rank_field = level + 'TotalRank'

level_users.sort(key=lambda x: x.get(rank_field, float('inf')))

boundaries[level] = level_users[-1]  # Last (worst) in this level

return {

'data': data,

'boundaries': boundaries,

'counts': {

'base': baseCount,

'expert': expertCount,

'master': masterCount,

'grandmaster': grandmasterCount

}

}

def get_level_boundaries(self) -> Dict[str, Dict]:

"""

Calculate the boundaries for each level (last person in each level).

Returns:

Dictionary with level boundaries

"""

result = self.calculate_all_levels_and_boundaries()

return result['boundaries']

def calculate_gap_analysis(self, user_data: Dict, target_level: str, boundaries: Dict) -> Dict:

"""

Calculate gap analysis between user and target level boundary.

Args:

user_data: User's data

target_level: Target level to compare against

boundaries: Level boundaries data

Returns:

Gap analysis results

"""

target_data = boundaries.get(target_level)

if not target_data:

return {}

gap_analysis = {}

for metric in self.all_metrics:

user_value = user_data.get(metric, 0)

target_value = target_data.get(metric, 0)

gap = user_value - target_value

gap_analysis[metric] = {

'user_value': user_value,

'target_value': target_value,

'gap': gap,

'is_positive': gap >= 0

}

return gap_analysis

def calculate_advantage_analysis(self, user_data: Dict, current_level: str, boundaries: Dict) -> Dict:

"""

Calculate advantage analysis between user and their current level boundary.

Args:

user_data: User's data

current_level: User's current level

boundaries: Level boundaries data

Returns:

Advantage analysis results

"""

boundary_data = boundaries.get(current_level)

if not boundary_data:

return {}

advantage_analysis = {}

for metric in self.all_metrics:

user_value = user_data.get(metric, 0)

boundary_value = boundary_data.get(metric, 0)

advantage = user_value - boundary_value

# For "lower is better" metrics, reverse the advantage logic

if metric in self.metrics_lower_better:

advantage = boundary_value - user_value

advantage_analysis[metric] = {

'user_value': user_value,

'boundary_value': boundary_value,

'advantage': advantage,

'is_positive': advantage >= 0

}

return advantage_analysis

def calculate_improvement_scenarios(self, user_data: Dict, target_data: Dict,

days_remaining: int = 30) -> Dict:

"""

Calculate improvement scenarios for different daily submission rates.

Args:

user_data: User's current data

target_data: Target user's data to match

days_remaining: Days remaining in the season

Returns:

Improvement scenarios for 1-4 alphas per day

"""

scenarios = {}

current_alpha_count = user_data.get('alphaCount', 0)

for daily_alphas in range(1, 5):

additional_alphas = days_remaining * daily_alphas

new_alpha_count = current_alpha_count + additional_alphas

scenario = {}

# Calculate for Operator Avg (lower is better)

current_operator_avg = user_data.get('operatorAvg', 0)

target_operator_avg = target_data.get('operatorAvg', 0)

if current_operator_avg <= target_operator_avg:

# User is already better or equal, no improvement needed

scenario['operatorAvg'] = "无需改进"

else:

# Calculate what avg is needed for new alphas to reach target overall avg

current_operator_total = current_operator_avg * current_alpha_count

required_total = target_operator_avg * new_alpha_count

additional_total_needed = required_total - current_operator_total

if additional_alphas > 0:

required_avg = additional_total_needed / additional_alphas

if required_avg <= 1.0:

scenario['operatorAvg'] = "不可能"

else:

scenario['operatorAvg'] = round(required_avg, 2)

else:

scenario['operatorAvg'] = "N/A"

# Calculate for Field Avg (lower is better)

current_field_avg = user_data.get('fieldAvg', 0)

target_field_avg = target_data.get('fieldAvg', 0)

if current_field_avg <= target_field_avg:

# User is already better or equal, no improvement needed

scenario['fieldAvg'] = "无需改进"

else:

# Calculate what avg is needed for new alphas to reach target overall avg

current_field_total = current_field_avg * current_alpha_count

required_total = target_field_avg * new_alpha_count

additional_total_needed = required_total - current_field_total

if additional_alphas > 0:

required_avg = additional_total_needed / additional_alphas

if required_avg <= 1.0:

scenario['fieldAvg'] = "不可能"

else:

scenario['fieldAvg'] = round(required_avg, 2)

else:

scenario['fieldAvg'] = "N/A"

# Calculate for Count metrics (these need to reach specific totals)

target_operator_count = target_data.get('operatorCount', 0)

current_operator_count = user_data.get('operatorCount', 0)

scenario['operatorCount'] = max(0, target_operator_count - current_operator_count)

target_field_count = target_data.get('fieldCount', 0)

current_field_count = user_data.get('fieldCount', 0)

scenario['fieldCount'] = max(0, target_field_count - current_field_count)

scenarios[f'{daily_alphas}_per_day'] = scenario

return scenarios

def generate_html_report(self, user_id: str, days_remaining: int = 30) -> str:

"""

Generate a comprehensive HTML report for the user.

Args:

user_id: User ID to analyze

days_remaining: Days remaining in the season

Returns:

HTML string of the complete report

"""

user_data = self.find_user_by_id(user_id)

if not user_data:

return self._generate_error_html(f"User {user_id} not found in the ranking data.")

# Get complete analysis using genius.js logic

all_data = self.calculate_all_levels_and_boundaries()

boundaries = all_data['boundaries']

# Find user's processed data

user_processed = None

for user in all_data['data']:

if user.get('user') == user_id:

user_processed = user

break

if not user_processed:

return self._generate_error_html(f"用户 {user_id} 在处理后的数据中未找到。")

current_level = user_processed.get('finalLevel', 'gold')

# Determine target level for gap analysis

level_hierarchy = ['gold', 'expert', 'master', 'grandmaster']

current_index = level_hierarchy.index(current_level)

target_level = level_hierarchy[current_index + 1] if current_index < 3 else None

# Use the processed user data which already has correct rankings

user_in_level = user_processed

# Calculate gap analysis (upward comparison)

gap_analysis = {}

target_user_data = None

if target_level and target_level in boundaries:

target_user_data = boundaries[target_level]

gap_analysis = self.calculate_gap_analysis(user_data, target_level, boundaries)

# Calculate advantage analysis (downward comparison)

advantage_analysis = {}

if current_level != 'gold' and current_level in boundaries:

advantage_analysis = self.calculate_advantage_analysis(user_data, current_level, boundaries)

# Calculate improvement scenarios

improvement_scenarios = {}

if target_level and target_level in boundaries and current_level != 'grandmaster':

improvement_scenarios = self.calculate_improvement_scenarios(

user_data, boundaries[target_level], days_remaining

)

return self._generate_html_content(

user_id, user_data, current_level, gap_analysis, advantage_analysis,

improvement_scenarios, target_level, target_user_data, user_processed, days_remaining

)

def _generate_error_html(self, error_message: str) -> str:

"""Generate an error HTML page."""

return f"""<!DOCTYPE html>

<html lang="zh-CN">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>错误 - Genius排名分析</title>

<style>{self._get_css_styles()}</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>错误</h1>

</div>

<div class="content">

<div class="card">

<h2>分析错误</h2>

<p style="color: #dc3545; font-size: 1.2em;">{error_message}</p>

<p>请检查用户ID并重试。</p>

</div>

</div>

</div>

</body>

</html>"""

def _generate_html_content(self, user_id: str, user_data: Dict, current_level: str,

gap_analysis: Dict, advantage_analysis: Dict, improvement_scenarios: Dict,

target_level: Optional[str], target_user_data: Optional[Dict], user_processed: Dict, days_remaining: int) -> str:

"""Generate the main HTML content."""

# User summary section

user_summary_html = self._generate_user_summary_html(user_id, user_data, current_level, user_processed)

# Six-dimensional metrics section

metrics_html = self._generate_metrics_html(user_data)

# Gap analysis section

gap_html = ""

if gap_analysis and target_level and target_user_data:

gap_html = self._generate_gap_analysis_html(gap_analysis, target_level, target_user_data)

# Advantage analysis section

advantage_html = ""

if advantage_analysis and current_level != 'gold':

# Get the boundary user data from the all_data we already have access to

all_data = self.calculate_all_levels_and_boundaries()

boundary_user_data = all_data['boundaries'].get(current_level)

advantage_html = self._generate_advantage_analysis_html(advantage_analysis, current_level, boundary_user_data)

# Improvement scenarios section

improvement_html = ""

if improvement_scenarios and target_level:

improvement_html = self._generate_improvement_scenarios_html(

improvement_scenarios, target_level, days_remaining

)

return f"""<!DOCTYPE html>

<html lang="zh-CN">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Genius排名分析 - {user_id}</title>

<style>{self._get_css_styles()}</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>Genius排名分析</h1>

<div class="user-id">用户ID: {user_id}</div>

</div>

<div class="content">

{user_summary_html}

{metrics_html}

{gap_html}

{advantage_html}

{improvement_html}

</div>

</div>

</body>

</html>"""

def _generate_user_summary_html(self, user_id: str, user_data: Dict, current_level: str, user_processed: Dict) -> str:

"""Generate user summary section."""

alpha_count = user_data.get('alphaCount', 0)

pyramid_count = user_data.get('pyramidCount', 0)

# Calculate actual rank in current level

all_data = self.calculate_all_levels_and_boundaries()

level_users = [u for u in all_data['data'] if u.get('finalLevel') == current_level]

rank_field = current_level + 'TotalRank'

# Sort by totalRank to get actual position

level_users.sort(key=lambda x: x.get(rank_field, float('inf')))

# Find user's position (1-based ranking)

rank_in_level = 'N/A'

for idx, user in enumerate(level_users):

if user.get('user') == user_id:

rank_in_level = idx + 1

break

return f"""

<div class="card">

<h2>用户概要</h2>

<div class="user-summary">

<div class="summary-item">

<div class="value"><span class="level-badge level-{current_level.upper()}">{current_level.upper()}</span></div>

<div class="label">当前等级</div>

</div>

<div class="summary-item">

<div class="value">{rank_in_level}</div>

<div class="label">总排名</div>

</div>

<div class="summary-item">

<div class="value">{alpha_count}</div>

<div class="label">Alpha数量</div>

</div>

<div class="summary-item">

<div class="value">{pyramid_count}</div>

<div class="label">金字塔数量</div>

</div>

</div>

</div>"""

def _generate_metrics_html(self, user_data: Dict) -> str:

"""Generate six-dimensional metrics section."""

return f"""

<div class="card">

<h2>六维指标</h2>

<div class="user-summary">

<div class="summary-item">

<div class="value">{user_data.get('operatorCount', 0)}</div>

<div class="label">Operator Count</div>

</div>

<div class="summary-item">

<div class="value">{user_data.get('operatorAvg', 0):.2f}</div>

<div class="label">Operator Avg</div>

</div>

<div class="summary-item">

<div class="value">{user_data.get('fieldCount', 0)}</div>

<div class="label">Field Count</div>

</div>

<div class="summary-item">

<div class="value">{user_data.get('fieldAvg', 0):.2f}</div>

<div class="label">Field Avg</div>

</div>

<div class="summary-item">

<div class="value">{user_data.get('communityActivity', 0):.1f}</div>

<div class="label">Community Activity</div>

</div>

<div class="summary-item">

<div class="value">{user_data.get('maxSimulationStreak', 0)}</div>

<div class="label">Max Simulation Streak</div>

</div>

</div>

</div>"""

def _generate_gap_analysis_html(self, gap_analysis: Dict, target_level: str, target_user_data: Dict) -> str:

"""Generate gap analysis table."""

rows = ""

for metric in self.all_metrics:

if metric not in gap_analysis:

continue

data = gap_analysis[metric]

user_val = data['user_value']

target_val = data['target_value']

gap = data['gap']

is_positive = data['is_positive']

# Format values

if isinstance(user_val, float):

user_str = f"{user_val:.2f}"

target_str = f"{target_val:.2f}"

gap_str = f"{gap:+.2f}"

else:

user_str = str(user_val)

target_str = str(target_val)

gap_str = f"{gap:+d}" if gap != 0 else "0"

# Determine color based on whether user is better than target

if gap == 0:

gap_class = "gap-neutral"  # Black color for equal values

elif metric in self.metrics_lower_better:

# For "lower is better" metrics, negative gap means user is better (lower value)

gap_class = "gap-positive" if gap < 0 else "gap-negative"

else:

# For "higher is better" metrics, positive gap means user is better (higher value)

gap_class = "gap-positive" if gap > 0 else "gap-negative"

# Calculate progress bar - redesigned for better visualization

if metric in self.metrics_lower_better:

# For "lower is better" metrics, show user vs target with target as goal

max_val = max(user_val, target_val, 1)

user_progress = (user_val / max_val) * 100

target_progress = (target_val / max_val) * 100

# Use green if user is better (lower), red if worse (higher)

bar_color = "#28a745" if user_val <= target_val else "#dc3545"

else:

# For "higher is better" metrics, show user vs target with target as minimum goal

max_val = max(user_val, target_val, 1)

user_progress = (user_val / max_val) * 100

target_progress = (target_val / max_val) * 100

# Use green if user is better (higher), red if worse (lower)

bar_color = "#28a745" if user_val >= target_val else "#dc3545"

metric_display = metric.replace('operatorCount', 'Operator Count') \

.replace('operatorAvg', 'Operator Avg') \

.replace('fieldCount', 'Field Count') \

.replace('fieldAvg', 'Field Avg') \

.replace('communityActivity', 'Community Activity') \

.replace('maxSimulationStreak', 'Max Simulation Streak')

rows += f"""

<tr>

<td>{metric_display}</td>

<td>{user_str}</td>

<td>{target_str}</td>

<td class="{gap_class}">{gap_str}</td>

<td>

<div class="progress-bar-container">

<div class="progress-bar" style="width: {user_progress:.1f}%; background-color: {bar_color};"></div>

<div class="progress-marker" style="left: {target_progress:.1f}%;">目标</div>

</div>

</td>

</tr>"""

target_user_id = target_user_data.get('user', 'Unknown')

return f"""

<div class="card">

<h2>Genius向上差距对比 (目标: {target_level.upper()} - {target_user_id})</h2>

<p>与{target_level.upper()}等级最后一名用户的对比。</p>

<table>

<thead>

<tr>

<th>指标</th>

<th>你的数值</th>

<th>目标数值 (最后一名{target_level.title()})</th>

<th>差距</th>

<th>可视化</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

</div>"""

def _generate_advantage_analysis_html(self, advantage_analysis: Dict, current_level: str, boundary_user_data: Dict) -> str:

"""Generate advantage analysis table."""

rows = ""

for metric in self.all_metrics:

if metric not in advantage_analysis:

continue

data = advantage_analysis[metric]

user_val = data['user_value']

boundary_val = data['boundary_value']

advantage = data['advantage']

is_positive = data['is_positive']

# Format values

if isinstance(user_val, float):

user_str = f"{user_val:.2f}"

boundary_str = f"{boundary_val:.2f}"

advantage_str = f"{advantage:+.2f}"

else:

user_str = str(user_val)

boundary_str = str(boundary_val)

advantage_str = f"{advantage:+d}" if advantage != 0 else "0"

advantage_class = "gap-positive" if is_positive else "gap-negative"

# Calculate progress bar for advantage (user vs boundary)

if metric in self.metrics_lower_better:

# For "lower is better", show user vs boundary

max_val = max(user_val, boundary_val, 1)

user_progress = (user_val / max_val) * 100

boundary_progress = (boundary_val / max_val) * 100

# Use green if user is better (lower), red if worse (higher)

bar_color = "#28a745" if user_val <= boundary_val else "#dc3545"

else:

# For "higher is better", show user vs boundary

max_val = max(user_val, boundary_val, 1)

user_progress = (user_val / max_val) * 100

boundary_progress = (boundary_val / max_val) * 100

# Use green if user is better (higher), red if worse (lower)

bar_color = "#28a745" if user_val >= boundary_val else "#dc3545"

metric_display = metric.replace('operatorCount', 'Operator Count') \

.replace('operatorAvg', 'Operator Avg') \

.replace('fieldCount', 'Field Count') \

.replace('fieldAvg', 'Field Avg') \

.replace('communityActivity', 'Community Activity') \

.replace('maxSimulationStreak', 'Max Simulation Streak')

rows += f"""

<tr>

<td>{metric_display}</td>

<td>{user_str}</td>

<td>{boundary_str}</td>

<td class="{advantage_class}">{advantage_str}</td>

<td>

<div class="progress-bar-container">

<div class="progress-bar" style="width: {user_progress:.1f}%; background-color: {bar_color};"></div>

<div class="progress-marker" style="left: {boundary_progress:.1f}%;">边界</div>

</div>

</td>

</tr>"""

boundary_user_id = boundary_user_data.get('user', 'Unknown') if boundary_user_data else 'Unknown'

return f"""

<div class="card">

<h2>Genius向下优势对比 (当前: {current_level.upper()} - {boundary_user_id})</h2>

<p>与你当前{current_level.upper()}等级最后一名用户的对比，展示你的优势。</p>

<table>

<thead>

<tr>

<th>指标</th>

<th>你的数值</th>

<th>等级边界 (最后一名{current_level.title()})</th>

<th>优势</th>

<th>可视化</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

</div>"""

def _generate_improvement_scenarios_html(self, scenarios: Dict, target_level: str, days_remaining: int) -> str:

"""Generate improvement scenarios table."""

rows = ""

# Generate rows for each metric

for metric in ['operatorAvg', 'fieldAvg']:

metric_display = '目标Operator Avg' if metric == 'operatorAvg' else '目标Field Avg'

row_data = []

for daily in range(1, 5):

key = f'{daily}_per_day'

value = scenarios.get(key, {}).get(metric, 'N/A')

if value == 'Impossible' or value == '不可能':

row_data.append('<span class="impossible">不可能</span>')

elif value == '无需改进':

row_data.append('<span class="no-improvement">无需改进</span>')

else:

row_data.append(str(value))

rows += f"""

<tr>

<td>{metric_display}</td>

<td>{row_data[0]}</td>

<td>{row_data[1]}</td>

<td>{row_data[2]}</td>

<td>{row_data[3]}</td>

</tr>"""

return f"""

<div class="card">

<h2>每日提交改进要求</h2>

<p>为了在赛季结束前达到目标{target_level.upper()}的整体平均值，<strong>新alpha</strong>需要的平均值 (剩余{days_remaining}天)。</p>

<table>

<thead>

<tr>

<th>指标</th>

<th>每天1个Alpha</th>

<th>每天2个Alpha</th>

<th>每天3个Alpha</th>

<th>每天4个Alpha</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

<small>*'目标Operator/Field Avg'指的是你每天提交的新alpha所需的平均值，以将你的整体平均值降至目标等级。'无需改进'表示你当前已经比目标更好。'不可能'意味着即使新alpha的平均值为最低的1，也无法达到目标平均值。</small>

</div>"""

def _get_css_styles(self) -> str:

"""Return the CSS styles for the HTML report."""

return """

body {

font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

background-color: #f0f2f5;

color: #333;

margin: 0;

padding: 20px;

}

.container {

max-width: 1200px;

margin: auto;

background: #fff;

border-radius: 8px;

box-shadow: 0 2px 4px rgba(0,0,0,0.1);

overflow: hidden;

}

.header {

background-color: #4a4a4a;

color: white;

padding: 20px;

text-align: center;

}

.header h1 {

margin: 0;

font-size: 2em;

}

.header .user-id {

font-size: 1.2em;

opacity: 0.8;

}

.content {

padding: 20px;

}

.card {

background: #f9f9f9;

border: 1px solid #e1e1e1;

border-radius: 8px;

padding: 20px;

margin-bottom: 20px;

}

.card h2 {

margin-top: 0;

border-bottom: 2px solid #eee;

padding-bottom: 10px;

color: #4a4a4a;

}

.user-summary {

display: grid;

grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));

gap: 20px;

align-items: center;

}

.summary-item {

text-align: center;

}

.summary-item .value {

font-size: 2em;

font-weight: bold;

color: #1a73e8;

}

.summary-item .label {

font-size: 0.9em;

color: #666;

}

.level-badge {

display: inline-block;

padding: 5px 15px;

border-radius: 15px;

font-weight: bold;

color: white;

}

.level-GOLD { background-color: #FFD700; color: #333;}

.level-EXPERT { background-color: #C0C0C0; }

.level-MASTER { background-color: #CD7F32; }

.level-GRANDMASTER { background-color: #6c757d; }

table {

width: 100%;

border-collapse: collapse;

margin-top: 20px;

}

th, td {

padding: 12px;

text-align: left;

border-bottom: 1px solid #ddd;

}

th {

background-color: #f2f2f2;

font-weight: 600;

}

.gap-positive { color: #28a745; }

.gap-negative { color: #dc3545; }

.gap-neutral { color: #333; }

.progress-bar-container {

width: 100%;

background-color: #e9ecef;

border-radius: .25rem;

height: 20px;

position: relative;

}

.progress-bar {

height: 100%;

background-color: #1a73e8;

border-radius: .25rem;

display: flex;

align-items: center;

justify-content: center;

color: white;

font-size: 12px;

}

.progress-marker {

position: absolute;

top: -2px;

border-left: 2px dashed #666;

height: 24px;

font-size: 10px;

color: #666;

padding-left: 3px;

white-space: nowrap;

}

.impossible {

color: #dc3545;

font-weight: bold;

}

.no-improvement {

color: #28a745;

font-weight: bold;

}

"""

def main():

"""Main function to run the analyzer."""

print("Genius排名分析工具")

print("=" * 40)

# Initialize analyzer

try:

analyzer = GeniusRankingAnalyzer()

print(f"✓ 已加载 {len(analyzer.data)} 个用户记录")

except Exception as e:

print(f"✗ 数据加载错误: {e}")

return

# Get user input

user_id = input("\n请输入要分析的用户ID: ").strip()

if not user_id:

print("未提供用户ID，退出程序。")

return

try:

days_remaining = int(input("请输入赛季剩余天数 (默认30): ") or "30")

except ValueError:

days_remaining = 30

# Generate analysis

print(f"\n📊 正在分析用户 {user_id}...")

try:

html_report = analyzer.generate_html_report(user_id, days_remaining)

# Save to file

output_filename = f"{user_id}_ranking_analysis.html"

with open(output_filename, 'w', encoding='utf-8') as f:

f.write(html_report)

print(f"✓ 分析完成！报告已保存为: {output_filename}")

print(f"📁 在浏览器中打开该文件以查看详细分析。")

except Exception as e:

print(f"✗ 生成分析报告时出错: {e}")

if __name__ == "__main__":

main()

下方为两张测试截图：

祝大家这个季度都能评上Genius!

---

## 讨论与评论 (0)

