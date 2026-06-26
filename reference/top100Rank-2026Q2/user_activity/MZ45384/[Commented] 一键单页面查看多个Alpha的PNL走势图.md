# 一键单页面查看多个Alpha的PNL走势图

- **链接**: [Commented] 一键单页面查看多个Alpha的PNL走势图.md
- **作者**: TT21691
- **发布时间/热度**: 7个月前, 得票: 5

## 帖子正文

在平台上对比不同alpha的表现时，往往需要手动输入alpha id在链接中打开多个页面，不利于对多个alpha进行表现对比，所以我做了一个可以一键在单个页面查看多个alpha PNL图的工具。
效果展示：

支持查看多条PNL曲线 ![图片](images/img_e8add0ec1c.png)

支持只查看单条曲线。 ![图片](images/img_f9fe7dcbca.png)

支持计算相关性：
 ![图片](images/img_3ee65dfa6b.png) 
代码
```

import matplotlib

matplotlib.use('Agg')  # 使用非交互式后端

import matplotlib.pyplot as plt

import matplotlib.dates as mdates

from datetime import datetime

import time  # 添加time模块导入

import asyncio

import json

import requests

import os

from flask import Flask, render_template, request, jsonify

import io

import base64

from loguru import logger

app = Flask(__name__, template_folder='./pnl_templates')

brain_api_url = " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) "

# 创建临时目录存储图片

if not os.path.exists('static'):

os.makedirs('static')

def login():

try:

username, password = "",""  # 这里需要填入实际的用户名和密码

session = requests.Session()

session.auth = (username, password)

response = session.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')

if response.status_code == 201:

return session

elif response.status_code == 429:

retry_after = response.headers.get('Retry-After', 0)

time.sleep(float(retry_after))

return login()

else:

logger.error(f"登录失败! 状态码: {response.status_code}, 响应内容: {response.content.decode('utf-8')}")

return None

except Exception as e:

logger.error(f"登录异常，{e}")

return None

s = login()

async def async_wait_get(session: requests.Session, url: str, max_retries: int = 10) -> requests.Response:

"""带重试机制的 GET 请求（异步版本）"""

retries = 0

while retries < max_retries:

response = session.get(url)

if retries%9==0 and retries>0:

logger.info(f"正在请求 {url} 第{retries}次")

if response.status_code==401:

logger.info(f"url 401, retry {url}")

global s

s = login()

continue

retry_after = float(response.headers.get("Retry-After", 0))

if retry_after > 0:

await asyncio.sleep(2 ** retries)

retries += 1

continue

if response.status_code < 400:

return response

response.raise_for_status()

return response

async def async_get_alpha_info(alpha_id: str):

"""获取 Alpha 的详细信息"""

url = brain_api_url + "/alphas/" + alpha_id

while True:

result = await async_wait_get(s,url)

if "retry-after" in result.headers:

await asyncio.sleep(float(result.headers["Retry-After"]))

else:

break

return result.json()

async def async_get_alpha_pnl_json(alpha_id: str):

"""获取单个 alpha 的 PnL 数据（异步版本）"""

url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl](https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl) "

while True:

result = await async_wait_get(s,url)

if "retry-after" in result.headers:

await asyncio.sleep(float(result.headers["Retry-After"]))

else:

break

return result.json()

async def async_generate_pnl_plot(alpha_id: str):

"""生成 PnL 图表和对应的原始数据（用于前端悬停交互）

Parameters:

-----------

alpha_id : str

Alpha 的 ID

Returns:

--------

tuple: (img_data, plot_data)

img_data: 图片的 BytesIO 对象

plot_data: 包含原始数据的字典，用于前端交互

"""

try:

# 获取 PnL 数据

data = await async_get_alpha_pnl_json(alpha_id)

print("完整数据结构:", json.dumps(data, indent=2)[:500] + "...")  # 打印部分结构

# 从 schema 中获取列名和标题

schema = data.get('schema', {})

properties = schema.get('properties', [])

# 第一列是日期，其他列是数据系列

date_column = properties[0] if properties else {'name': 'date', 'title': 'Date'}

data_columns = properties[1:] if len(properties) > 1 else []

# 打印列信息

print(f"日期列: {date_column.get('title')}")

print("数据列:")

for i, col in enumerate(data_columns):

print(f"  {i}: {col.get('name')} - {col.get('title')}")

# 处理数据

dates = []

dates_str = []  # 存储字符串格式的日期

all_series = []  # 存储所有数据系列

series_names = []  # 存储系列名称

series_data = {}  # 用于前端的系列数据

# 初始化数据系列

for col in data_columns:

series_name = col.get('title', f'Series {len(series_names) + 1}')

series_names.append(series_name)

all_series.append([])

series_data[series_name] = []

# 填充数据

for record in data['records']:

date_str = record[0]

dates_str.append(date_str)

date = datetime.strptime(date_str, '%Y-%m-%d')

dates.append(date)

# 处理数据列

for i in range(len(data_columns)):

if i + 1 < len(record):  # 确保索引不越界

value = record[i + 1]

all_series[i].append(value)

series_data[series_names[i]].append(value)

else:

all_series[i].append(0)

series_data[series_names[i]].append(0)

# 创建图表 - 调整尺寸，为底部图例留出足够空间

fig, ax = plt.subplots(figsize=(12, 6))

# 定义颜色列表

colors = [

'#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#228B22',

'#6A4C93', '#1982C4', '#8AC926', '#FF595E', '#FFCA3A'

]

# 绘制所有数据系列

for i in range(len(data_columns)):

color = colors[i % len(colors)]

label = series_names[i]

ax.plot(dates, all_series[i], linewidth=1.8, color=color, label=label, alpha=0.8)

# 添加零线

ax.plot([dates[0], dates[-1]], [0, 0], color='red', linestyle='--', alpha=0.7, linewidth=1.2, label='Break-even')

# 设置图表属性

ax.set_ylabel('PnL', fontsize=12, fontweight='bold')

ax.set_title(f'Alpha {alpha_id} - PnL Over Time', fontsize=14, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3)

# 格式化y轴标签

def format_y_axis(x, p):

if abs(x) >= 1e6:

return f'${x/1e6:.1f}M'

elif abs(x) >= 1e3:

return f'${x/1e3:.0f}K'

else:

return f'${x:.0f}'

ax.yaxis.set_major_formatter(plt.FuncFormatter(format_y_axis))

# 格式化x轴

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

ax.xaxis.set_major_locator(mdates.YearLocator())

ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))

# 调整字体大小

ax.tick_params(axis='both', which='major', labelsize=10)

ax.tick_params(axis='both', which='minor', labelsize=8)

# 自动调整x轴标签角度

plt.xticks(rotation=45)

# 调整布局，为底部图例留出空间

plt.subplots_adjust(bottom=0.25)

# 优化图例显示

ax.legend(

loc='upper center',

bbox_to_anchor=(0.5, -0.18),

ncol=min(6, len(series_names) + 1),  # +1 包含零线

fontsize=8,

framealpha=0.9,

handlelength=1.2,

handletextpad=0.3,

columnspacing=0.8,

labelspacing=0.3

)

# 保存图表到 BytesIO

img = io.BytesIO()

plt.savefig(

img,

format='png',

dpi=120,

bbox_inches='tight',

facecolor='white',

edgecolor='none'

)

img.seek(0)

plt.close()

# 准备前端需要的交互数据

plot_data = {

'alpha_id': alpha_id,

'dates': dates_str,

'series_names': series_names,

'series_data': series_data,

'y_min': min([min(series) for series in all_series]) if all_series else 0,

'y_max': max([max(series) for series in all_series]) if all_series else 0,

'x_range': [dates_str[0], dates_str[-1]] if dates_str else ['', ''],

'colors': colors[:len(series_names)]  # 保存颜色信息

}

print(f"成功生成图表和交互数据，包含 {len(series_names)} 个数据系列")

return img, plot_data

except Exception as e:

print(f"生成图表时出错: {e}")

import traceback

traceback.print_exc()

return None, None

def format_alpha_info(alpha_info):

"""格式化 Alpha 信息为 HTML 可显示的格式"""

if not alpha_info:

return "无法获取 Alpha 信息"

info_html = []

# 第一行：ID, Type, Date Created

first_line = []

first_line.append(f"<strong>ID:</strong> {alpha_info.get('id', 'N/A')}")

first_line.append(f"<strong>Type:</strong> {alpha_info.get('type', 'N/A')}")

first_line.append(f"<strong>Date Created:</strong> {alpha_info.get('dateCreated', 'N/A')[:10]}")

info_html.append("&nbsp;&nbsp;&nbsp;&nbsp;".join(first_line))

# 第二行：Region, Universe, Neutralization

second_line = []

settings = alpha_info.get('settings', {})

second_line.append(f"<strong>Region:</strong> {settings.get('region', 'N/A')}")

second_line.append(f"<strong>Universe:</strong> {settings.get('universe', 'N/A')}")

second_line.append(f"<strong>Neutralization:</strong> {settings.get('neutralization', 'N/A')}")

info_html.append("&nbsp;&nbsp;&nbsp;&nbsp;".join(second_line))

# 性能指标 - 修改显示格式

is_data = alpha_info.get('is', {})

# Returns: 乘以100，显示为百分比

returns = is_data.get('returns')

if returns is not None:

returns_pct = returns * 100

info_html.append(f"<strong>Returns:</strong> {returns_pct:.2f}%")

else:

info_html.append(f"<strong>Returns:</strong> N/A")

# Margin: 乘以1000，显示为千分比

margin = is_data.get('margin')

if margin is not None:

margin_per_thousand = margin * 10000

info_html.append(f"<strong>Margin:</strong> {margin_per_thousand:.2f}‱")

else:

info_html.append(f"<strong>Margin:</strong> N/A")

# Turnover: 乘以100，显示为百分比

turnover = is_data.get('turnover')

if turnover is not None:

turnover_pct = turnover * 100

info_html.append(f"<strong>Turnover:</strong> {turnover_pct:.2f}%")

else:

info_html.append(f"<strong>Turnover:</strong> N/A")

# Sharpe 和 Fitness 保持不变

info_html.append(f"<strong>Sharpe:</strong> {is_data.get('sharpe', 'N/A'):.2f}")

info_html.append(f"<strong>Fitness:</strong> {is_data.get('fitness', 'N/A'):.2f}")

# Alpha 代码

regular = alpha_info.get('regular', {})

code = regular.get('code', 'N/A')

info_html.append(f"<strong>Code:</strong> <code>{code}</code>")

return "<br>".join(info_html)

@app.route('/', methods=['GET', 'POST'])

def index():

if request.method == 'POST':

alpha_ids_input = request.form.get('alpha_ids', '')

alpha_ids = [aid.strip() for aid in alpha_ids_input.replace(',', ' ').replace('\n', ' ').split() if aid.strip()]

results = []

for alpha_id in alpha_ids:

# 获取 Alpha 信息

alpha_info = asyncio.run(async_get_alpha_info(alpha_id))

info_html = format_alpha_info(alpha_info)

# 生成图表和交互数据

img_data, plot_data = asyncio.run(async_generate_pnl_plot(alpha_id))

result_item = {

'alpha_id': alpha_id,

'info_html': info_html,

'plot_data': json.dumps(plot_data) if plot_data else None  # 转换为JSON字符串

}

if img_data:

# 转换为base64

img_base64 = base64.b64encode(img_data.getvalue()).decode('utf-8')

result_item['image'] = img_base64

results.append(result_item)

return render_template('results.html', results=results)

return render_template('index.html')

@app.route('/self_corr/<alpha_id>')

async def async_get_self_corr(alpha_id):

"""获取 Alpha 的自相关性数据"""

try:

url = brain_api_url + "/alphas/" + alpha_id + "/correlations/self"

while True:

result = await async_wait_get(s,url)

if "retry-after" in result.headers:

await asyncio.sleep(float(result.headers["Retry-After"]))

else:

break

self_corr = result.json()['max']

if self_corr is not None:

return jsonify({

'success': True,

'self_corr': self_corr,

'source': 'calculated'

})

else:

return jsonify({

'success': False,

'error': '无法获取自相关性数据'

})

except Exception as e:

return jsonify({

'success': False,

'error': str(e)

})

@app.route('/power_corr/<alpha_id>')

async def get_power_corr(alpha_id):

"""获取 Alpha 的 Power Corr 数据"""

try:

url = brain_api_url + "/alphas/" + alpha_id + "/correlations/power-pool"

while True:

result = await async_wait_get(s,url)

if "retry-after" in result.headers:

await asyncio.sleep(float(result.headers["Retry-After"]))

else:

break

power_corr = result.json()['max']

if power_corr is not None:

return jsonify({

'success': True,

'power_corr': power_corr,

'source': 'calculated'

})

else:

return jsonify({

'success': False,

'error': '无法获取 Power Corr 数据'

})

except Exception as e:

return jsonify({

'success': False,

'error': str(e)

})

@app.route('/prod_corr/<alpha_id>')

async def async_get_prod_corr(alpha_id):

"""获取 Alpha 的 Prod Corr 数据"""

try:

url = brain_api_url + "/alphas/" + alpha_id + "/correlations/prod"

while True:

result = await async_wait_get(s,url)

if "retry-after" in result.headers:

await asyncio.sleep(float(result.headers["Retry-After"]))

else:

break

prod_corr = result.json()['max']

if prod_corr is not None:

return jsonify({

'success': True,

'prod_corr': prod_corr,

'source': 'calculated'

})

else:

return jsonify({

'success': False,

'error': '无法获取 Prod Corr 数据'

})

except Exception as e:

return jsonify({

'success': False,

'error': str(e)

})

# 创建 HTML 模板

def create_templates():

"""创建必要的 HTML 模板文件"""

if not os.path.exists('./pnl_templates'):

os.makedirs('./pnl_templates')

# 首页模板（保持不变）

index_html = '''

<!DOCTYPE html>

<html lang="zh-CN">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Alpha PnL 可视化工具</title>

<style>

body {

font-family: Arial, sans-serif;

max-width: 1200px;

margin: 0 auto;

padding: 20px;

background-color: #f5f5f5;

}

.container {

background-color: white;

padding: 30px;

border-radius: 10px;

box-shadow: 0 2px 10px rgba(0,0,0,0.1);

}

h1 {

color: #333;

text-align: center;

margin-bottom: 30px;

}

.form-group {

margin-bottom: 20px;

}

label {

display: block;

margin-bottom: 8px;

font-weight: bold;

color: #555;

}

textarea {

width: 100%;

height: 120px;

padding: 10px;

border: 1px solid #ddd;

border-radius: 5px;

font-family: monospace;

resize: vertical;

}

.help-text {

font-size: 12px;

color: #666;

margin-top: 5px;

}

.btn {

background-color: #2E86AB;

color: white;

padding: 12px 30px;

border: none;

border-radius: 5px;

cursor: pointer;

font-size: 16px;

transition: background-color 0.3s;

}

.btn:hover {

background-color: #1a5a7a;

}

.btn-container {

text-align: center;

margin-top: 20px;

}

</style>

</head>

<body>

<div class="container">

<h1>Alpha PnL 可视化工具</h1>

<form method="POST">

<div class="form-group">

<label for="alpha_ids">输入 Alpha IDs:</label>

<textarea id="alpha_ids" name="alpha_ids" placeholder="请输入 Alpha ID，多个 ID 用逗号、空格或换行分隔&#10;例如：&#10;E5WQJvPm&#10;ABC123&#10;XYZ789"></textarea>

<div class="help-text">每行一个 Alpha ID，或使用逗号/空格分隔多个 ID</div>

</div>

<div class="btn-container">

<button type="submit" class="btn">生成 PnL 图表</button>

</div>

</form>

</div>

</body>

</html>

'''

# 结果页面模板

results_html = '''<!DOCTYPE html>

<html lang="zh-CN">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Alpha PnL 结果</title>

<!-- 引入 Chart.js -->

<script src=" [https://cdn.jsdelivr.net/npm/chart.js"></script](https://cdn.jsdelivr.net/npm/chart.js%22></script) >

<style>

body {

font-family: Arial, sans-serif;

max-width: 1400px;

margin: 0 auto;

padding: 20px;

background-color: #f5f5f5;

font-size: 16px;

}

.header {

text-align: center;

margin-bottom: 30px;

}

h1 {

font-size: 28px;

color: #333;

}

.back-btn {

background-color: #6c757d;

color: white;

padding: 12px 24px;

text-decoration: none;

border-radius: 5px;

display: inline-block;

margin-bottom: 25px;

font-size: 16px;

font-weight: bold;

}

.back-btn:hover {

background-color: #545b62;

}

.results-grid {

display: grid;

grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));

gap: 25px;

margin-top: 20px;

}

.result-item {

background-color: white;

padding: 25px;

border-radius: 10px;

box-shadow: 0 2px 10px rgba(0,0,0,0.1);

}

.alpha-info {

font-size: 15px;

line-height: 1.6;

margin-bottom: 20px;

padding: 15px;

background-color: #f8f9fa;

border-radius: 5px;

border-left: 4px solid #2E86AB;

}

.alpha-info code {

background-color: #e9ecef;

padding: 4px 6px;

border-radius: 3px;

font-family: monospace;

font-size: 14px;

display: block;

margin-top: 8px;

word-break: break-all;

}

.chart-container {

margin-top: 20px;

text-align: center;

border: 1px solid #eee;

border-radius: 5px;

padding: 10px;

background-color: white;

position: relative;

overflow: hidden;

}

.chart-note {

font-size: 12px;

color: #666;

margin-top: 8px;

font-style: italic;

}

.corr-container {

display: flex;

align-items: center;

margin-bottom: 12px;

gap: 10px;

padding: 10px;

background-color: #f8f9fa;

border-radius: 5px;

}

.corr-text {

font-weight: bold;

color: #333;

min-width: 90px;

font-size: 16px;

}

.corr-btn {

width: 32px;

height: 32px;

border-radius: 50%;

border: none;

color: white;

cursor: pointer;

display: flex;

align-items: center;

justify-content: center;

transition: all 0.3s;

font-size: 14px;

font-weight: bold;

}

.self-corr-btn {

background-color: #28a745;

}

.power-corr-btn {

background-color: #ffc107;

color: #000;

}

.prod-corr-btn {

background-color: #17a2b8;

}

.corr-btn:hover {

transform: scale(1.1);

opacity: 0.9;

}

.corr-btn.loading {

animation: spin 1s linear infinite;

}

.corr-result {

font-weight: bold;

margin-left: 8px;

min-width: 100px;

font-size: 16px;

}

.corr-source {

font-size: 12px;

color: #666;

margin-left: 8px;

font-style: italic;

}

.self-corr-result {

color: #28a745;

}

.power-corr-result {

color: #e0a800;

}

.prod-corr-result {

color: #17a2b8;

}

@keyframes spin {

0% { transform: rotate(0deg); }

100% { transform: rotate(360deg); }

}

.no-results {

text-align: center;

color: #666;

font-size: 20px;

padding: 50px;

}

.alpha-id-header {

font-size: 20px;

font-weight: bold;

color: #2E86AB;

margin-bottom: 15px;

padding-bottom: 8px;

border-bottom: 2px solid #2E86AB;

}

/* 图例样式 */

.chart-legend {

display: flex;

flex-wrap: wrap;

justify-content: center;

margin-top: 10px;

gap: 10px;

}

.legend-item {

display: flex;

align-items: center;

cursor: pointer;

padding: 4px 8px;

border-radius: 4px;

transition: all 0.2s;

font-size: 12px;

}

.legend-item:hover {

background-color: #f0f0f0;

}

.legend-item.active {

background-color: #e6f3ff;

font-weight: bold;

}

.legend-color {

width: 12px;

height: 12px;

border-radius: 2px;

margin-right: 6px;

}

@media (max-width: 768px) {

.results-grid {

grid-template-columns: 1fr;

}

body {

font-size: 14px;

}

}

</style>

</head>

<body>

<a href="/" class="back-btn">← 返回输入页面</a>

<div class="header">

<h1>Alpha PnL 分析结果</h1>

</div>

{% if results %}

<div class="results-grid">

{% for result in results %}

<div class="result-item">

<div class="alpha-id-header">Alpha ID: {{ result.alpha_id }}</div>

<div class="alpha-info">

{{ result.info_html|safe }}

</div>

<!-- Self Corr 部分 -->

<div class="corr-container">

<span class="corr-text">Self Corr</span>

<button class="corr-btn self-corr-btn" data-alpha-id="{{ result.alpha_id }}" data-type="self" title="计算自相关性">

<span>✓</span>

</button>

<span class="corr-result self-corr-result" id="self-corr-{{ result.alpha_id }}">

{% if result.self_corr is defined %}

{{ "%.4f"|format(result.self_corr) }}

<span class="corr-source"></span>

{% endif %}

</span>

</div>

<!-- Power Corr 部分 -->

<div class="corr-container">

<span class="corr-text">Power Corr</span>

<button class="corr-btn power-corr-btn" data-alpha-id="{{ result.alpha_id }}" data-type="power" title="计算 Power 相关性">

<span>⚡</span>

</button>

<span class="corr-result power-corr-result" id="power-corr-{{ result.alpha_id }}">

{% if result.power_corr is defined %}

{{ "%.4f"|format(result.power_corr) }}

<span class="corr-source"></span>

{% endif %}

</span>

</div>

<!-- Prod Corr 部分 -->

<div class="corr-container">

<span class="corr-text">Prod Corr</span>

<button class="corr-btn prod-corr-btn" data-alpha-id="{{ result.alpha_id }}" data-type="prod" title="计算 Prod 相关性">

<span>🔄</span>

</button>

<span class="corr-result prod-corr-result" id="prod-corr-{{ result.alpha_id }}">

{% if result.prod_corr is defined %}

{{ "%.4f"|format(result.prod_corr) }}

<span class="corr-source"></span>

{% endif %}

</span>

</div>

<!-- 图表容器（使用 Chart.js） -->

<div class="chart-container" id="chart-container-{{ result.alpha_id }}">

<canvas id="chart-{{ result.alpha_id }}"></canvas>

<!-- 自定义图例 -->

<div class="chart-legend" id="legend-{{ result.alpha_id }}"></div>

<div class="chart-note">提示：点击图例可以单独查看某条线，再次点击恢复所有线条</div>

<!-- 存储原始数据（隐藏） -->

<div class="plot-data" style="display: none;" id="plot-data-{{ result.alpha_id }}">

{{ result.plot_data|safe }}

</div>

</div>

</div>

{% endfor %}

</div>

<script>

// 存储每个图表的实例

const chartInstances = {};

/**

* 初始化单个图表的交互功能

*/

function initChartInteraction(alphaId) {

const dataElement = document.getElementById(`plot-data-${alphaId}`);

if (!dataElement || !dataElement.textContent) {

console.warn(`没有找到 ${alphaId} 的图表数据`);

return;

}

try {

// 解析原始数据

const plotData = JSON.parse(dataElement.textContent);

if (!plotData || !plotData.dates || !plotData.series_data) {

console.warn(`图表数据格式不正确: ${alphaId}`);

return;

}

console.log(`成功加载 ${alphaId} 的数据，包含 ${plotData.dates.length} 个数据点`);

// 创建 Chart.js 图表

createChart(alphaId, plotData);

} catch (error) {

console.error(`解析 ${alphaId} 的图表数据时出错:`, error);

}

}

/**

* 使用 Chart.js 创建交互式图表

*/

function createChart(alphaId, plotData) {

const ctx = document.getElementById(`chart-${alphaId}`).getContext('2d');

const legendContainer = document.getElementById(`legend-${alphaId}`);

// 准备数据

const dates = plotData.dates;

const seriesNames = plotData.series_names;

const seriesData = plotData.series_data;

const colors = plotData.colors || [

'#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#228B22',

'#6A4C93', '#1982C4', '#8AC926', '#FF595E', '#FFCA3A'

];

// 创建数据集

const datasets = seriesNames.map((name, index) => {

return {

label: name,

data: seriesData[name],

borderColor: colors[index % colors.length],

backgroundColor: colors[index % colors.length] + '20', // 添加透明度

borderWidth: 2,

pointRadius: 0,

pointHoverRadius: 4,

tension: 0.1,

hidden: false

};

});

// 添加零线

datasets.push({

label: 'Break-even',

data: Array(dates.length).fill(0),

borderColor: 'red',

backgroundColor: 'transparent',

borderWidth: 1,

borderDash: [5, 5],

pointRadius: 0,

tension: 0,

hidden: false

});

// 创建图表

const chart = new Chart(ctx, {

type: 'line',

data: {

labels: dates,

datasets: datasets

},

options: {

responsive: true,

maintainAspectRatio: true,

// 禁用所有缩放和拖动交互

interaction: {

mode: 'nearest',

axis: 'x',

intersect: false

},

plugins: {

legend: {

display: false // 禁用默认图例，使用自定义图例

},

tooltip: {

mode: 'index',

intersect: false,

callbacks: {

label: function(context) {

let label = context.dataset.label || '';

if (label) {

label += ': ';

}

const value = context.parsed.y;

// 格式化数值

if (Math.abs(value) >= 1e6) {

label += '$' + (value / 1e6).toFixed(2) + 'M';

} else if (Math.abs(value) >= 1e3) {

label += '$' + (value / 1e3).toFixed(0) + 'K';

} else {

label += '$' + value.toFixed(0);

}

return label;

}

}

},

// 禁用缩放插件

zoom: false

},

scales: {

x: {

type: 'category',

grid: {

display: true,

color: 'rgba(0, 0, 0, 0.1)'

},

ticks: {

maxRotation: 45,

minRotation: 45

}

},

y: {

grid: {

display: true,

color: 'rgba(0, 0, 0, 0.1)'

},

ticks: {

callback: function(value) {

if (Math.abs(value) >= 1e6) {

return '$' + (value / 1e6).toFixed(1) + 'M';

} else if (Math.abs(value) >= 1e3) {

return '$' + (value / 1e3).toFixed(0) + 'K';

} else {

return '$' + value;

}

}

}

}

},

// 禁用点击选择

onClick: function(e, elements) {

// 阻止默认的点击行为

e.stopPropagation();

},

// 禁用悬停时的数据点选择

hover: {

mode: 'index',

intersect: false

},

// 禁用动画，防止点击时出现缩放效果

animation: {

duration: 0

},

// 禁用元素高亮

elements: {

point: {

hoverRadius: 4,

radius: 0

}

}

}

});

// 存储图表实例

chartInstances[alphaId] = chart;

// 创建自定义图例

createCustomLegend(chart, legendContainer, alphaId);

}

/**

* 创建自定义图例

*/

function createCustomLegend(chart, container, alphaId) {

container.innerHTML = '';

chart.data.datasets.forEach((dataset, index) => {

const legendItem = document.createElement('div');

legendItem.className = 'legend-item';

legendItem.dataset.index = index;

const colorBox = document.createElement('div');

colorBox.className = 'legend-color';

colorBox.style.backgroundColor = dataset.borderColor;

const text = document.createElement('span');

text.textContent = dataset.label;

legendItem.appendChild(colorBox);

legendItem.appendChild(text);

// 点击图例时的处理

legendItem.addEventListener('click', function() {

const datasetIndex = parseInt(this.dataset.index);

toggleDataset(chart, datasetIndex, container);

});

container.appendChild(legendItem);

});

}

/**

* 切换数据集的显示状态

*/

function toggleDataset(chart, datasetIndex, legendContainer) {

const datasets = chart.data.datasets;

const isHidden = !datasets[datasetIndex].hidden;

// 如果点击的是当前唯一显示的线，则恢复所有线

const visibleCount = datasets.filter(d => !d.hidden).length;

if (visibleCount === 1 && datasets[datasetIndex].hidden === false) {

// 恢复所有线

datasets.forEach(dataset => {

dataset.hidden = false;

dataset.borderWidth = 2;

});

} else {

// 隐藏所有其他线，显示当前线

datasets.forEach((dataset, index) => {

if (index === datasetIndex) {

dataset.hidden = false;

dataset.borderWidth = 3; // 加粗当前线

} else {

dataset.hidden = true;

dataset.borderWidth = 2;

}

});

}

// 更新图例状态

updateLegendState(chart, legendContainer);

// 更新图表

chart.update();

}

/**

* 更新图例状态

*/

function updateLegendState(chart, legendContainer) {

const datasets = chart.data.datasets;

const legendItems = legendContainer.getElementsByClassName('legend-item');

Array.from(legendItems).forEach(item => {

const index = parseInt(item.dataset.index);

if (datasets[index].hidden) {

item.classList.remove('active');

item.style.opacity = '0.5';

} else {

item.classList.add('active');

item.style.opacity = '1';

}

});

}

document.addEventListener('DOMContentLoaded', function() {

const buttons = document.querySelectorAll('.corr-btn');

// 相关性计算按钮逻辑

buttons.forEach(button => {

button.addEventListener('click', function() {

const alphaId = this.getAttribute('data-alpha-id');

const corrType = this.getAttribute('data-type');

const resultSpan = document.getElementById(corrType + '-corr-' + alphaId);

let apiEndpoint = '';

switch(corrType) {

case 'self':

apiEndpoint = '/self_corr/' + alphaId;

break;

case 'power':

apiEndpoint = '/power_corr/' + alphaId;

break;

case 'prod':

apiEndpoint = '/prod_corr/' + alphaId;

break;

}

const originalHTML = this.innerHTML;

this.innerHTML = '⏳';

this.classList.add('loading');

resultSpan.innerHTML = '计算中...';

resultSpan.style.color = '#6c757d';

fetch(apiEndpoint)

.then(response => response.json())

.then(data => {

this.innerHTML = originalHTML;

this.classList.remove('loading');

if (data.success) {

let resultValue;

switch(corrType) {

case 'self':

resultValue = data.self_corr;

resultSpan.className = 'corr-result self-corr-result';

break;

case 'power':

resultValue = data.power_corr;

resultSpan.className = 'corr-result power-corr-result';

break;

case 'prod':

resultValue = data.prod_corr;

resultSpan.className = 'corr-result prod-corr-result';

break;

}

resultSpan.innerHTML = resultValue.toFixed(4);

if (data.source === 'calculated') {

resultSpan.innerHTML += ' <span class="corr-source"></span>';

}

} else {

resultSpan.innerHTML = '错误: ' + data.error;

resultSpan.style.color = '#dc3545';

}

})

.catch(error => {

this.innerHTML = originalHTML;

this.classList.remove('loading');

resultSpan.innerHTML = '请求失败';

resultSpan.style.color = '#dc3545';

console.error('Error:', error);

});

});

});

// 初始化所有图表

document.querySelectorAll('.plot-data').forEach(dataElement => {

const alphaId = dataElement.id.replace('plot-data-', '');

initChartInteraction(alphaId);

});

});

</script>

{% else %}

<div class="no-results">

没有生成任何结果，请检查输入的 Alpha ID 是否正确。

</div>

{% endif %}

</body>

</html>

'''

# 写入模板文件

with open('./pnl_templates/index.html', 'w', encoding='utf-8') as f:

f.write(index_html)

with open('./pnl_templates/results.html', 'w', encoding='utf-8') as f:

f.write(results_html)

if __name__ == '__main__':

# 创建模板文件

create_templates()

# 启动 Flask 应用

print("启动 Alpha PnL 可视化工具...")

print("访问 http://localhost:5005 使用工具")

app.run(debug=True, host='0.0.0.0', port=5005)

```

---

## 讨论与评论 (5)

### 评论 #1 (作者: JR57542, 时间: 5个月前)

很有用，有了这个对比起来直观多了，哈哈

---

### 评论 #2 (作者: FF65210, 时间: 5个月前)

感谢大佬提供的工具，祝大佬VF1.0

---

### 评论 #3 (作者: SZ20589, 时间: 5个月前)

大佬这代码这么漂亮，应该花了很多时间吧。

之前需要手动输入alpha id在链接中打开多个页面，不好对多个alpha进行表现对比，大佬这个可以一键在单个页面查看多个alpha PNL图的工具，方便多了。

我试下看看效果哈。

=============================================================================

========Genius is one percent inspiration and ninety-nine percent perspiration.=============

==============================================================================

---

### 评论 #4 (作者: MZ45384, 时间: 5个月前)

非常不错的功能，方便而简洁。要是把项目上传到github就更好了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #5 (作者: TT21691, 时间: 5个月前)

是的，因为brain平台上对比很不方便，所以我

做了这个工具。后续还可以考虑和ai结合。

---

