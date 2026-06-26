# （即插即用）AIAC 2025比赛的实践成果notebook详细代码，欢迎讨论代码优化

- **链接**: [Commented] 即插即用AIAC 2025比赛的实践成果notebook详细代码欢迎讨论代码优化.md
- **作者**: YZ14671
- **发布时间/热度**: 7个月前, 得票: 58

## 帖子正文

从比赛开始到现在已经过半了，这个过程里面也感受到了熬夜两周搭建智能体的过程，这是这段时间的一个成果，主要难点在提示词优化的边界控制上，以及具体的工作流程上进行反复的打磨，其中大家可以参考wj老师发布的具体的工作流程，在实现的基础上继续进行优化。废话不多说，以下是我的详细的AIAC比赛的notebook笔记，配置好后，即插即用，提醒！！！在使用ai时请注意好的你的钱包。

！！！第一call

import sys

import pandas as pd

import ace_lib as ace

import nest_asyncio

import asyncio

import re

from openai import AsyncOpenAI

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import httpx

nest_asyncio.apply()

_llm_instance = None

def extract_relevant_operators(alpha_expression, all_operators):

"""提取 Alpha 表达式中实际使用的操作符"""

operator_names = all_operators['name'].tolist()

used_operators = []

for op_name in operator_names:

# 使用正则表达式匹配操作符（后面跟着括号）

if re.search(rf'\b{re.escape(op_name)}\s*\(', alpha_expression):

used_operators.append(op_name)

return all_operators[all_operators['name'].isin(used_operators)]

def extract_relevant_datafields(alpha_expression, all_datafields):

"""提取 Alpha 表达式中实际使用的数据字段"""

field_ids = all_datafields['id'].tolist()

used_fields = []

for field_id in field_ids:

if field_id in alpha_expression:

used_fields.append(field_id)

return all_datafields[all_datafields['id'].isin(used_fields)]

def format_operators_for_prompt(operators_df):

"""将操作符数据格式化为简洁的字符串"""

if operators_df.empty:

return "无使用的操作符"

result = []

for _, row in operators_df.iterrows():

result.append(f"- {row['name']}: {row.get('description', 'N/A')}")

return "\n".join(result)

def format_datafields_for_prompt(datafields_df):

"""将数据字段格式化为简洁的字符串"""

if datafields_df.empty:

return "无使用的数据字段"

result = []

for _, row in datafields_df.iterrows():

result.append(f"- {row['id']}: {row.get('name', 'N/A')} (类型: {row.get('type', 'N/A')})")

return "\n".join(result)

def parse_alpha_expressions(llm_response):

"""

从 LLM 响应中解析出 Alpha 表达式

返回格式: [(expression, description), ...]

"""

lines = llm_response.strip().split('\n')

alphas = []

for line in lines:

line = line.strip()

if not line:

continue

# 尝试分离表达式和注释

if '#' in line:

parts = line.split('#', 1)

expression = parts[0].strip()

description = parts[1].strip() if len(parts) > 1 else ""

else:

expression = line

description = ""

# 简单验证：表达式应该包含括号

if '(' in expression and ')' in expression:

alphas.append((expression, description))

return alphas

# 添加重试装饰器，针对连接错误进行重试

@retry(

stop=stop_after_attempt(5),  # 最多重试5次

wait=wait_exponential(multiplier=1, min=4, max=60),  # 指数退避：4秒、8秒、16秒、32秒、60秒

retry=retry_if_exception_type((httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadTimeout, ConnectionError)),

reraise=True

)

async def call_llm(prompt, timeout=180):

"""

Interface with the LLM API to process the given prompt.

添加了重试机制和超时设置

"""

try:

# 使用更长的超时时间和自定义 httpx 客户端

http_client = httpx.AsyncClient(

timeout=httpx.Timeout(timeout, connect=30.0),

limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),

transport=httpx.AsyncHTTPTransport(retries=3)

)

client = AsyncOpenAI(

base_url=" [https://api.deepseek.com/v1](https://api.deepseek.com/v1) ",

api_key="sk-xxxxxxx",

http_client=http_client,

timeout=timeout,

max_retries=3

)

print(f"正在调用 LLM (超时设置: {timeout}秒)...")

response = await client.chat.completions.create(

model="deepseek-reasoner",

messages=[

{"role": "user", "content": prompt}

]

)

print("✓ LLM 调用成功")

return response.choices[0].message.content.strip()

except httpx.ReadTimeout as e:

print(f"✗ LLM 调用超时 ({timeout}秒): {e}")

raise

except (httpx.RemoteProtocolError, httpx.ConnectError) as e:

print(f"✗ 连接错误，准备重试: {e}")

raise

except Exception as e:

print(f"✗ 调用 LLM 时出错: {type(e).__name__}: {e}")

return None

finally:

try:

await http_client.aclose()

except:

pass

async def generate_alpha_description(alpha_id, brain_session, max_retries=3):

"""生成 Alpha 的中文描述，从量化研究员的角度分析其经济学意义"""

for attempt in range(1, max_retries + 1):

try:

print(f"\n尝试生成描述 (第 {attempt}/{max_retries} 次)...")

alpha_details = brain_session.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}").json(](https://api.worldquantbrain.com/alphas/{alpha_id}%22).json() )

alpha_expression = alpha_details['regular']['code']

print(f"Alpha 表达式: {alpha_expression}")

# 获取所有操作符和数据字段

all_operators = ace.get_operators(brain_session)

regular_operators = all_operators[all_operators['scope']=='REGULAR']

dataset_ids = ['pv87', 'fundamental17']

all_datafields = pd.concat(

[ace.get_datafields(brain_session, region='USA', universe='TOP3000', dataset_id=dataset_id, data_type='ALL')

for dataset_id in dataset_ids],

ignore_index=True

)

# 提取相关的操作符和数据字段

relevant_operators = extract_relevant_operators(alpha_expression, regular_operators)

relevant_datafields = extract_relevant_datafields(alpha_expression, all_datafields)

print(f"找到 {len(relevant_operators)} 个相关操作符和 {len(relevant_datafields)} 个相关数据字段")

# 格式化为简洁的字符串

operators_str = format_operators_for_prompt(relevant_operators)

datafields_str = format_datafields_for_prompt(relevant_datafields)

# 从资深量化研究员角度生成 prompt

prompt = f"""你是一位资深量化研究员，请从经济学和金融学的角度分析以下 Alpha 表达式：

Alpha 表达式: {alpha_expression}

使用的操作符:

{operators_str}

使用的数据字段:

{datafields_str}

请用中文提供详细分析，包括：

1. **经济学直觉**：这个 Alpha 试图捕捉什么经济现象或市场行为？

2. **信号逻辑**：为什么这种组合可能产生预测能力？

3. **潜在的市场假设**：这个 Alpha 隐含了哪些关于市场效率或投资者行为的假设？

4. **适用场景**：在什么市场环境下这个信号可能表现更好？

请保持分析简洁但深入，重点关注经济合理性。"""

# 使用更长的超时时间（3分钟）

description = await call_llm(prompt, timeout=180)

if description is None:

if attempt < max_retries:

wait_time = 2 ** attempt  # 指数退避

print(f"等待 {wait_time} 秒后重试...")

await asyncio.sleep(wait_time)

continue

return f"无法生成 Alpha 描述 (已重试 {max_retries} 次): {alpha_expression}"

print("✓ 描述生成成功")

return description.strip()

except Exception as e:

print(f"✗ 生成 Alpha 描述时出错 (第 {attempt} 次): {type(e).__name__}: {e}")

if attempt < max_retries:

wait_time = 2 ** attempt

print(f"等待 {wait_time} 秒后重试...")

await asyncio.sleep(wait_time)

else:

return f"生成描述时出错 (已重试 {max_retries} 次): {str(e)}"

return f"生成描述失败: 已达到最大重试次数 ({max_retries})"

async def generate_new_alphas(alpha_description, original_expression, brain_session, max_retries=3):

"""

基于经济学原理生成高质量的 Alpha 变体

允许改变操作符结构以提升因子质量

"""

for attempt in range(1, max_retries + 1):

try:

print(f"\n尝试生成新 Alpha (第 {attempt}/{max_retries} 次)...")

num_alphas = 5

# 获取所有可用的操作符

all_operators = ace.get_operators(brain_session)

regular_operators = all_operators[all_operators['scope']=='REGULAR']

operators_list = regular_operators['name'].tolist()

dataset_ids = ['pv87', 'fundamental17']

data_fields = pd.concat(

[ace.get_datafields(brain_session, region='USA', universe='TOP3000', dataset_id=dataset_id, data_type='ALL')

for dataset_id in dataset_ids],

ignore_index=True

)

# 提取数据字段信息

datafields_summary = []

for _, row in data_fields.iterrows():

datafields_summary.append(f"{row['id']} (类型: {row.get('type', 'N/A')}, 名称: {row.get('name', 'N/A')})")

datafields_str = "\n".join(datafields_summary[:150])  # 提供更多字段选择

# 从资深量化研究员角度设计 prompt

prompt = f"""你是一位资深量化研究员，专注于开发具有明确经济学意义的 Alpha 因子。

【原始 Alpha 分析】

表达式: {original_expression}

经济学解读:

{alpha_description}

【可用资源】

操作符（部分）: {', '.join(operators_list[:50])}

可用数据字段:

{datafields_str}

【任务要求】

基于原始 Alpha 的经济学直觉，生成 {num_alphas} 个高质量的变体表达式。

【核心原则 - 作为顶级 BRAIN 顾问】

1. **经济合理性优先**：每个 Alpha 必须有清晰的经济学逻辑，避免纯数据挖掘

2. **低换手率**：优先使用较长的时间窗口（如 ts_decay_linear, ts_mean），避免高频交易信号

3. **稳健性**：使用 winsorize、rank、neutralize 等操作符提升因子稳健性

4. **多样性**：探索不同的数据类别（基本面、情绪、技术指标）以提升金字塔覆盖度

【操作符结构调整指南】

- 可以改变操作符组合以提升因子质量

- 推荐的稳健操作符：ts_decay_linear, ts_mean, ts_rank, winsorize, rank, neutralize

- 避免过度复杂的嵌套（不超过 4-5 层）

- 时间窗口建议：5-60 天（避免过短导致高换手）

【数据字段选择】

- 优先选择基本面数据（earnings, revenue, cash_flow 等）

- 考虑分析师预期数据（consensus, estimate）

- 可以组合不同类型的数据以捕捉多维信号

【语法规范】

- type=MATRIX 字段可直接使用

- type=VECTOR 字段必须用 Vector() 包装

- type=GROUP 字段只能作为 Group 操作符参数

- 确保所有括号匹配，参数格式正确

【输出格式】

请生成 {num_alphas} 个表达式，每行一个，格式如下：

表达式1  # 经济学逻辑说明

表达式2  # 经济学逻辑说明

...

示例格式：

ts_decay_linear(rank(fundamental17_sales_growth), 20)  # 捕捉销售增长的持续性趋势

"""

# 使用更长的超时时间（3分钟）

response = await call_llm(prompt, timeout=180)

if response is None:

if attempt < max_retries:

wait_time = 2 ** attempt

print(f"等待 {wait_time} 秒后重试...")

await asyncio.sleep(wait_time)

continue

return f"生成新 Alpha 失败 (已重试 {max_retries} 次)，请检查 LLM 连接。"

print("✓ 新 Alpha 生成成功")

return response.strip()

except Exception as e:

print(f"✗ 生成新 Alpha 时出错 (第 {attempt} 次): {type(e).__name__}: {e}")

if attempt < max_retries:

wait_time = 2 ** attempt

print(f"等待 {wait_time} 秒后重试...")

await asyncio.sleep(wait_time)

else:

return f"生成新 Alpha 时出错 (已重试 {max_retries} 次): {str(e)}"

return f"生成新 Alpha 失败: 已达到最大重试次数 ({max_retries})"

async def main():

# 启动 Brain 会话

brain_session = ace.start_session()

# Alpha ID 列表

alpha_ids = ["kqEnlEA8"]

for alpha_id in alpha_ids:

print(f"\n{'='*60}")

print(f"处理 Alpha ID: {alpha_id}")

print(f"{'='*60}")

# 获取原始表达式

alpha_details = brain_session.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}").json(](https://api.worldquantbrain.com/alphas/{alpha_id}%22).json() )

original_expression = alpha_details['regular']['code']

# 步骤 1: 生成 Alpha 的经济学描述（带重试）

alpha_description = await generate_alpha_description(alpha_id, brain_session, max_retries=3)

if alpha_description and not alpha_description.startswith("无法") and not alpha_description.startswith("生成描述时出错") and not alpha_description.startswith("生成描述失败"):

print(f"\n【Alpha 经济学分析】\n{alpha_description}")

# 步骤 2: 基于经济学原理生成新的高质量 Alpha（带重试）

new_alphas_response = await generate_new_alphas(alpha_description, original_expression, brain_session, max_retries=3)

print(f"\n【生成的高质量 Alpha 变体】\n{new_alphas_response}")

# 步骤 3: 解析生成的 Alpha 表达式

parsed_alphas = parse_alpha_expressions(new_alphas_response)

if not parsed_alphas:

print("\n警告: 未能从 LLM 响应中解析出有效的 Alpha 表达式")

continue

print(f"\n成功解析 {len(parsed_alphas)} 个 Alpha 表达式，开始模拟...")

# 步骤 4: 逐个模拟生成的 Alpha

successful_simulations = []

failed_simulations = []

for idx, (expression, description) in enumerate(parsed_alphas, 1):

print(f"\n--- 模拟 Alpha {idx}/{len(parsed_alphas)} ---")

print(f"表达式: {expression}")

print(f"说明: {description}")

try:

# 生成 Alpha 配置

simulate_data = ace.generate_alpha(

regular=expression,

alpha_type="REGULAR",

region="USA",

universe="TOP3000",

delay=1,

decay=0,

neutralization="INDUSTRY",

truncation=0.08,

pasteurization="ON",

nan_handling="OFF",

unit_handling="VERIFY",

visualization=True

)

# 执行模拟

print("正在提交模拟...")

simulation_result = ace.simulate_single_alpha(brain_session, simulate_data)

child_alpha_id = simulation_result.get('alpha_id')

if child_alpha_id:

print(f"✓ 模拟成功! Alpha ID: {child_alpha_id}")

# 设置 Alpha 属性和标签

full_description = f"【父 Alpha】{alpha_id}\n【经济学逻辑】{description}\n【原始分析】{alpha_description[:200]}..."

ace.set_alpha_properties(

brain_session,

child_alpha_id,

tags=[alpha_id],

regular_desc=full_description

)

print(f"✓ 已设置标签和描述")

successful_simulations.append({

'alpha_id': child_alpha_id,

'expression': expression,

'description': description

})

else:

print(f"✗ 模拟失败: 未返回 Alpha ID")

failed_simulations.append({

'expression': expression,

'reason': '未返回 Alpha ID'

})

except Exception as e:

print(f"✗ 模拟出错: {str(e)}")

failed_simulations.append({

'expression': expression,

'reason': str(e)

})

# 步骤 5: 输出总结

print(f"\n{'='*60}")

print(f"模拟总结 - 父 Alpha: {alpha_id}")

print(f"{'='*60}")

print(f"成功: {len(successful_simulations)} 个")

print(f"失败: {len(failed_simulations)} 个")

if successful_simulations:

print("\n成功的 Alpha:")

for item in successful_simulations:

print(f"  - {item['alpha_id']}: {item['expression'][:60]}...")

if failed_simulations:

print("\n失败的 Alpha:")

for item in failed_simulations:

print(f"  - {item['expression'][:60]}... (原因: {item['reason']})")

else:

print(f"\n{alpha_description}")

print("由于描述生成错误，跳过 Alpha 生成。")

！！！第二call

asyncio.run(main())

！！！第三call

# 检索性能指标、可视化和分析

# 选出冠军alpha

import matplotlib.pyplot as plt

import seaborn as sns

import numpy as np

from datetime import datetime

# 设置中文字体支持

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']

plt.rcParams['axes.unicode_minus'] = False

async def get_alpha_performance(brain_session, alpha_id):

"""获取 Alpha 的性能指标"""

try:

alpha_details = brain_session.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}").json(](https://api.worldquantbrain.com/alphas/{alpha_id}%22).json() )

# 提取关键性能指标

is_stats = alpha_details.get('is', {})

performance = {

'alpha_id': alpha_id,

'sharpe': is_stats.get('sharpe'),

'fitness': is_stats.get('fitness'),

'turnover': is_stats.get('turnover'),

'returns': is_stats.get('returns'),

'drawdown': is_stats.get('drawdown'),

'margin': is_stats.get('margin'),

'expression': alpha_details.get('regular', {}).get('code', ''),

'created_at': alpha_details.get('created')

}

return performance

except Exception as e:

print(f"获取 Alpha {alpha_id} 性能时出错: {e}")

return None

async def get_alphas_by_tag(brain_session, tag):

"""通过标签获取 Alpha 家族"""

try:

# 获取用户的所有 IS 阶段 Alphas

response = brain_session.get(

" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ",

params={'stage': 'IS', 'limit': 100}

).json()

alphas = response.get('results', [])

# 筛选包含指定标签的 Alphas

tagged_alphas = []

for alpha in alphas:

if tag in alpha.get('tags', []):

tagged_alphas.append(alpha['id'])

print(f"找到 {len(tagged_alphas)} 个带有标签 '{tag}' 的 Alphas")

return tagged_alphas

except Exception as e:

print(f"获取标签 Alphas 时出错: {e}")

return []

def visualize_performance(performance_data, parent_alpha_id):

"""可视化性能对比"""

if not performance_data:

print("没有可用的性能数据")

return

# 过滤掉 None 值

valid_data = [p for p in performance_data if p and all(

p.get(k) is not None for k in ['sharpe', 'fitness', 'turnover']

)]

if not valid_data:

print("没有完整的性能数据可供可视化")

return

df = pd.DataFrame(valid_data)

# 创建 2x2 子图

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

fig.suptitle(f'Alpha 家族性能对比 (父 Alpha: {parent_alpha_id})', fontsize=16, fontweight='bold')

# 1. Sharpe vs Fitness 散点图

ax1 = axes[0, 0]

scatter = ax1.scatter(df['sharpe'], df['fitness'],

c=df['turnover'],cmap='viridis',

s=200, alpha=0.6, edgecolors='black')

ax1.set_xlabel('Sharpe Ratio', fontsize=12)

ax1.set_ylabel('Fitness', fontsize=12)

ax1.set_title('Sharpe vs Fitness (颜色=Turnover)', fontsize=14)

ax1.grid(True, alpha=0.3)

# 添加颜色条

cbar = plt.colorbar(scatter, ax=ax1)

cbar.set_label('Turnover', fontsize=10)

# 标注 Alpha ID

for idx, row in df.iterrows():

ax1.annotate(row['alpha_id'][:6],

(row['sharpe'], row['fitness']),

fontsize=8, alpha=0.7)

# 2. 性能指标柱状图对比

ax2 = axes[0, 1]

x = np.arange(len(df))

width = 0.25

ax2.bar(x - width, df['sharpe'], width, label='Sharpe', alpha=0.8)

ax2.bar(x, df['fitness'], width, label='Fitness', alpha=0.8)

ax2.bar(x + width, df['turnover'], width, label='Turnover', alpha=0.8)

ax2.set_xlabel('Alpha Index', fontsize=12)

ax2.set_ylabel('指标值', fontsize=12)

ax2.set_title('关键指标对比', fontsize=14)

ax2.set_xticks(x)

ax2.set_xticklabels([f"#{i+1}" for i in range(len(df))], fontsize=9)

ax2.legend()

ax2.grid(True, alpha=0.3, axis='y')

# 3. Turnover 分布

ax3 = axes[1, 0]

ax3.barh(range(len(df)), df['turnover'], color='coral', alpha=0.7, edgecolor='black')

ax3.set_yticks(range(len(df)))

ax3.set_yticklabels([aid[:8] for aid in df['alpha_id']], fontsize=9)

ax3.set_xlabel('Turnover', fontsize=12)

ax3.set_title('换手率对比', fontsize=14)

ax3.grid(True, alpha=0.3, axis='x')

# 添加参考线（低换手率阈值）

ax3.axvline(x=0.1, color='green', linestyle='--', linewidth=2, label='低换手阈值 (0.1)')

ax3.legend()

# 4. 综合评分雷达图（选择前3个）

ax4 = axes[1, 1]

if len(df) > 0:

# 归一化数据到 0-1

metrics = ['sharpe', 'fitness', 'returns', 'margin']

available_metrics = [m for m in metrics if m in df.columns and df[m].notna().any()]

if len(available_metrics) >= 3:

# 选择前3个 Alpha

top_alphas = df.nlargest(min(3, len(df)), 'fitness')

angles = np.linspace(0, 2 * np.pi, len(available_metrics), endpoint=False).tolist()

angles += angles[:1]

ax4 = plt.subplot(2, 2, 4, projection='polar')

for idx, row in top_alphas.iterrows():

values = []

for metric in available_metrics:

val = row[metric]

# 简单归一化

max_val = df[metric].max()

min_val = df[metric].min()

if max_val != min_val:

normalized = (val - min_val) / (max_val - min_val)

else:

normalized = 0.5

values.append(normalized)

values += values[:1]

ax4.plot(angles, values, 'o-', linewidth=2, label=row['alpha_id'][:8])

ax4.fill(angles, values, alpha=0.15)

ax4.set_xticks(angles[:-1])

ax4.set_xticklabels(available_metrics, fontsize=10)

ax4.set_ylim(0, 1)

ax4.set_title('Top 3 Alphas 综合对比', fontsize=14, pad=20)

ax4.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

ax4.grid(True)

else:

ax4.text(0.5,0.5,'数据不足，无法生成雷达图',

ha='center', va='center', fontsize=12)

ax4.axis('off')

plt.tight_layout()

plt.show()

return df

async def llm_analyze_results(performance_df, parent_alpha_id, brain_session):

"""LLM 分析实验结果并提出建议"""

if performance_df is None or len(performance_df) == 0:

return "没有可用的性能数据进行分析"

# 准备数据摘要

summary_stats = {

'total_alphas': len(performance_df),

'avg_sharpe': performance_df['sharpe'].mean(),

'max_sharpe': performance_df['sharpe'].max(),

'avg_fitness': performance_df['fitness'].mean(),

'max_fitness': performance_df['fitness'].max(),

'avg_turnover': performance_df['turnover'].mean(),

'min_turnover': performance_df['turnover'].min()

}

# 找出最佳 Alpha

best_alpha = performance_df.loc[performance_df['fitness'].idxmax()]

# 构建分析 prompt

prompt = f"""你是一位资深量化研究员，请分析以下 Alpha 实验结果：

【实验概况】

- 父 Alpha ID: {parent_alpha_id}

- 生成的变体数量: {summary_stats['total_alphas']}

【性能统计】

- 平均 Sharpe: {summary_stats['avg_sharpe']:.4f} (最高: {summary_stats['max_sharpe']:.4f})

- 平均 Fitness: {summary_stats['avg_fitness']:.4f} (最高: {summary_stats['max_fitness']:.4f})

- 平均 Turnover: {summary_stats['avg_turnover']:.4f} (最低: {summary_stats['min_turnover']:.4f})

【最佳 Alpha】

- ID: {best_alpha['alpha_id']}

- Sharpe: {best_alpha['sharpe']:.4f}

- Fitness: {best_alpha['fitness']:.4f}

- Turnover: {best_alpha['turnover']:.4f}

- 表达式: {best_alpha['expression']}

【详细数据】

{performance_df[['alpha_id', 'sharpe', 'fitness', 'turnover', 'returns']].to_string()}

请提供以下分析：

1. **实验成果评估**

- 这批 Alpha 的整体质量如何？

- 是否有突出的表现者？

2. **关键发现**

- 哪些因子组合或数据字段表现最好？

- Sharpe、Fitness、Turnover 之间的权衡如何？

3. **改进方向**

- 基于当前结果，下一轮实验应该关注什么？

- 建议调整哪些参数或尝试哪些新的数据组合？

4. **金字塔策略**

- 从金字塔多样性角度，建议探索哪些新的数据类别或因子逻辑？

请用中文提供简洁但深入的分析。"""

print("\n正在生成 LLM 分析报告...")

analysis = await call_llm(prompt, timeout=180)

return analysis

async def analyze_alpha_family(parent_alpha_id):

"""完整的 Alpha 家族分析流程"""

brain_session = ace.start_session()

print(f"\n{'='*60}")

print(f"Alpha 家族分析 - 父 Alpha: {parent_alpha_id}")

print(f"{'='*60}\n")

# 步骤 1: 通过标签获取 Alpha 家族

print("步骤 1: 检索 Alpha 家族...")

alpha_ids = await get_alphas_by_tag(brain_session, parent_alpha_id)

if not alpha_ids:

print(f"未找到带有标签 '{parent_alpha_id}' 的 Alphas")

return

# 步骤 2: 获取所有 Alpha 的性能数据

print("\n步骤 2: 获取性能指标...")

performance_data = []

for alpha_id in alpha_ids:

print(f"  获取 {alpha_id} 的性能数据...")

perf = await get_alpha_performance(brain_session, alpha_id)

if perf:

performance_data.append(perf)

if not performance_data:

print("未能获取任何性能数据")

return

print(f"\n成功获取 {len(performance_data)} 个 Alpha 的性能数据")

# 步骤 3: 可视化性能对比

print("\n步骤 3: 生成可视化图表...")

performance_df = visualize_performance(performance_data, parent_alpha_id)

# 步骤 4: LLM 分析结果

print("\n步骤 4: LLM 分析实验结果...")

analysis = await llm_analyze_results(performance_df, parent_alpha_id, brain_session)

print(f"\n{'='*60}")

print("LLM 分析报告")

print(f"{'='*60}\n")

print(analysis)

# 返回结果供后续使用

return {

'performance_df': performance_df,

'analysis': analysis,

'alpha_ids': alpha_ids

}

# 执行分析

parent_alpha_id = "kqEnlEA8"  # 替换为你的父 Alpha ID

results = await analyze_alpha_family(parent_alpha_id)

！！！第四call

# ==================== Cell 4: 完整的自动迭代优化系统 ====================

# ===== 辅助函数声明 =====

async def get_alphas_by_tag(brain_session, tag):

"""根据标签获取 Alpha ID 列表"""

try:

# 直接使用 Brain API 获取用户的 Alpha 列表

url = f" [https://api.worldquantbrain.com/users/self/alphas?stage=IS&limit=100](https://api.worldquantbrain.com/users/self/alphas?stage=IS&limit=100) "

alphas_response = brain_session.get(url).json()

# 过滤出带有指定标签的 Alpha

alpha_ids = []

for alpha in alphas_response.get('results', []):

if tag in alpha.get('tags', []):

alpha_ids.append(alpha['id'])

print(f"找到 {len(alpha_ids)} 个带有标签 '{tag}' 的 Alphas")

return alpha_ids

except Exception as e:

print(f"获取 Alpha 列表失败: {e}")

return []

async def get_alpha_performance(brain_session, alpha_id):

"""获取单个 Alpha 的性能指标"""

try:

alpha_details = ace.get_simulation_result_json(brain_session, alpha_id)

if not alpha_details or 'is' not in alpha_details:

return None

is_data = alpha_details['is']

return {

'alpha_id': alpha_id,

'sharpe': is_data.get('sharpe', 0),

'fitness': is_data.get('fitness', 0),

'returns': is_data.get('returns', 0),

'turnover': is_data.get('turnover', 0),

'margin': is_data.get('margin', 0),

'drawdown': is_data.get('drawdown', 0),

'expression': alpha_details.get('regular', {}).get('code', '')

}

except Exception as e:

print(f"获取 Alpha {alpha_id} 性能失败: {str(e)}")

return None

def visualize_performance(performance_data, parent_alpha_id):

"""可视化性能数据"""

if not performance_data:

print("没有数据可供可视化")

return

df = pd.DataFrame(performance_data)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

fig.suptitle(f'Alpha Family {parent_alpha_id} - Performance Overview', fontsize=16)

# Sharpe vs Fitness

axes[0, 0].scatter(df['sharpe'], df['fitness'], alpha=0.6, s=100)

axes[0, 0].set_xlabel('Sharpe Ratio')

axes[0, 0].set_ylabel('Fitness')

axes[0, 0].set_title('Sharpe vs Fitness')

axes[0, 0].grid(True, alpha=0.3)

# Turnover vs Returns

axes[0, 1].scatter(df['turnover'], df['returns'], alpha=0.6, s=100, c='green')

axes[0, 1].set_xlabel('Turnover')

axes[0, 1].set_ylabel('Returns')

axes[0, 1].set_title('Turnover vs Returns')

axes[0, 1].grid(True, alpha=0.3)

# Sharpe Distribution

axes[1, 0].hist(df['sharpe'], bins=20, alpha=0.7, color='blue', edgecolor='black')

axes[1, 0].set_xlabel('Sharpe Ratio')

axes[1, 0].set_ylabel('Frequency')

axes[1, 0].set_title('Sharpe Distribution')

axes[1, 0].grid(True, alpha=0.3)

# Top Alphas

top_df = df.nlargest(10, 'sharpe')

axes[1, 1].barh(range(len(top_df)), top_df['sharpe'])

axes[1, 1].set_yticks(range(len(top_df)))

axes[1, 1].set_yticklabels([aid[:8] for aid in top_df['alpha_id']])

axes[1, 1].set_xlabel('Sharpe Ratio')

axes[1, 1].set_title('Top 10 Alphas by Sharpe')

axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()

plt.show()

async def select_best_alphas(performance_df, criteria='balanced', top_n=3):

"""选择最佳 Alpha"""

if performance_df.empty:

return []

df = performance_df.copy()

if criteria == 'sharpe':

df = df.sort_values('sharpe', ascending=False)

elif criteria == 'fitness':

df = df.sort_values('fitness', ascending=False)

elif criteria == 'balanced':

# 综合评分: Sharpe * 0.4 + Fitness * 0.3 + (1/Turnover) * 0.3

df['score'] = (df['sharpe'] *0.4+

df['fitness'] *0.3+

(1 / (df['turnover'] + 0.01)) * 0.3)

df = df.sort_values('score', ascending=False)

best = df.head(top_n).to_dict('records')

print(f"\n选出 Top {len(best)} Alpha:")

for i, alpha in enumerate(best, 1):

print(f"{i}. {alpha['alpha_id']}")

print(f"   Sharpe: {alpha['sharpe']:.4f}, Fitness: {alpha['fitness']:.4f}, Turnover: {alpha['turnover']:.4f}")

return best

async def decide_next_iteration(performance_df, current_iteration, max_iterations):

"""决策是否继续迭代"""

if current_iteration >= max_iterations:

return False, "达到最大迭代次数", []

if performance_df.empty:

return False, "没有有效的性能数据", []

# 检查是否有改进

avg_sharpe = performance_df['sharpe'].mean()

avg_fitness = performance_df['fitness'].mean()

if avg_sharpe < 0.5 or avg_fitness < 0.3:

return False, "整体性能过低，建议重新设计策略", []

suggestions = [

"继续优化参数",

"尝试新的数据字段组合",

"调整时间窗口以降低换手率"

]

return True, "性能有提升空间，继续迭代", suggestions

async def llm_analyze_results(performance_df, parent_alpha_id, brain_session):

"""LLM 分析结果"""

if performance_df.empty:

return "没有数据可供分析"

stats = {

'count': len(performance_df),

'avg_sharpe': performance_df['sharpe'].mean(),

'max_sharpe': performance_df['sharpe'].max(),

'avg_fitness': performance_df['fitness'].mean(),

'avg_turnover': performance_df['turnover'].mean()

}

prompt = f"""分析以下 Alpha 家族的性能数据:

Alpha 数量: {stats['count']}

平均 Sharpe: {stats['avg_sharpe']:.4f}

最高 Sharpe: {stats['max_sharpe']:.4f}

平均 Fitness: {stats['avg_fitness']:.4f}

平均 Turnover: {stats['avg_turnover']:.4f}

请提供简洁的分析（3-5 句话）:

1. 整体表现评价

2. 主要优势

3. 需要改进的方面

"""

response = await call_llm(prompt, timeout=60)

return response if response else "分析失败"

async def llm_iteration_suggestions(performance_df, iteration, best_alphas):

"""LLM 生成迭代优化建议"""

if not best_alphas:

return "没有最佳 Alpha 可供分析"

top_alpha = best_alphas[0]

prompt = f"""当前是第 {iteration} 轮迭代。

最佳 Alpha 表现:

- 表达式: {top_alpha['expression']}

- Sharpe: {top_alpha['sharpe']:.4f}

- Fitness: {top_alpha['fitness']:.4f}

- Turnover: {top_alpha['turnover']:.4f}

请提供 3-5 条具体的优化建议，每条建议应该:

1. 针对具体问题

2. 给出可操作的改进方向

3. 简洁明了（每条 1-2 句话）

"""

response = await call_llm(prompt, timeout=60)

return response if response else "建议生成失败"

async def export_alpha_family(parent_alpha_id, performance_df, best_alphas, output_file):

"""导出 Alpha 家族报告"""

with open(output_file, 'w', encoding='utf-8') as f:

f.write(f"Alpha Family Report: {parent_alpha_id}\n")

f.write(f"Generated: {datetime.now()}\n")

f.write("="*80 + "\n\n")

f.write(f"Total Alphas: {len(performance_df)}\n")

f.write(f"Average Sharpe: {performance_df['sharpe'].mean():.4f}\n")

f.write(f"Average Fitness: {performance_df['fitness'].mean():.4f}\n")

f.write(f"Average Turnover: {performance_df['turnover'].mean():.4f}\n\n")

f.write("Top 5 Best Alphas:\n")

f.write("-"*80 + "\n")

for i, alpha in enumerate(best_alphas[:5], 1):

f.write(f"\n{i}. Alpha ID: {alpha['alpha_id']}\n")

f.write(f"   Expression: {alpha['expression']}\n")

f.write(f"   Sharpe: {alpha['sharpe']:.4f}\n")

f.write(f"   Fitness: {alpha['fitness']:.4f}\n")

f.write(f"   Turnover: {alpha['turnover']:.4f}\n")

print(f"✓ 报告已导出到: {output_file}")

return output_file

# ===== 主要函数 =====

async def generate_optimized_alphas_from_best(best_alphas, brain_session, optimization_suggestions, num_new_alphas=5):

"""基于最佳 Alpha 和优化建议生成新一轮 Alpha"""

print(f"\n{'='*60}")

print(f"基于最佳 Alpha 生成新一轮优化变体")

print(f"{'='*60}\n")

if not best_alphas or len(best_alphas) == 0:

print("没有可用的最佳 Alpha")

return []

# 选择表现最好的 Alpha 作为基础

base_alpha = best_alphas[0]

base_expression = base_alpha['expression']

base_alpha_id = base_alpha['alpha_id']

print(f"基础 Alpha ID: {base_alpha_id}")

print(f"基础表达式: {base_expression}")

print(f"性能指标: Sharpe={base_alpha['sharpe']:.4f}, Fitness={base_alpha['fitness']:.4f}, Turnover={base_alpha['turnover']:.4f}\n")

# 获取操作符和数据字段

all_operators = ace.get_operators(brain_session)

regular_operators = all_operators[all_operators['scope']=='REGULAR']

operators_list = regular_operators['name'].tolist()

dataset_ids = ['pv87', 'fundamental17']

data_fields = pd.concat([

ace.get_datafields(brain_session,region='USA',universe='TOP3000',

dataset_id=dataset_id, data_type='ALL')

for dataset_id in dataset_ids

], ignore_index=True)

datafields_summary = [

f"{row['id']} (类型: {row.get('type','N/A')}, 名称: {row.get('name','N/A')})"

for _, row in data_fields.iterrows()

]

datafields_str = "\n".join(datafields_summary[:150])

# 构建优化 prompt

prompt = f"""你是一位资深量化研究员，正在进行 Alpha 因子的迭代优化。

【上一轮最佳 Alpha】

表达式: {base_expression}

性能: Sharpe={base_alpha['sharpe']:.4f}, Fitness={base_alpha['fitness']:.4f}, Turnover={base_alpha['turnover']:.4f}

【优化建议】

{optimization_suggestions}

【可用资源】

操作符（部分）: {', '.join(operators_list[:50])}

可用数据字段:

{datafields_str}

【优化任务】

基于上述最佳 Alpha 和优化建议，生成 {num_new_alphas} 个改进版本的 Alpha 表达式。

【优化策略】

1. **保留优势**: 保持最佳 Alpha 中表现好的核心逻辑

2. **针对性改进**: 根据优化建议调整参数或操作符

3. **渐进式变化**: 每次只改变 1-2 个关键要素，避免过度变异

4. **多样化探索**: 在保持核心逻辑的同时，尝试不同的实现方式

【具体改进方向】

- 如果 Turnover 过高: 增加时间窗口参数（如 20→40），使用 ts_decay_linear

- 如果 Sharpe 不足: 尝试组合更多数据字段，增强信号强度

- 如果 Fitness 偏低: 添加 winsorize、rank、neutralize 提升稳健性

- 探索新的数据类别: 基本面、分析师预期、情绪指标等

【语法规范】

- type=MATRIX 字段可直接使用

- type=VECTOR 字段必须用 Vector() 包装

- type=GROUP 字段只能作为 Group 操作符参数

- 确保所有括号匹配，参数格式正确

【输出格式】

请生成 {num_new_alphas} 个表达式，每行一个，格式如下：

表达式1  # 改进说明

表达式2  # 改进说明

...

示例：

ts_decay_linear(rank(fundamental17_sales_growth), 40)  # 增加时间窗口从20到40，降低换手率

"""

print("正在调用 LLM 生成优化后的 Alpha...")

response = await call_llm(prompt, timeout=180)

if response is None:

print("✗ LLM 调用失败")

return []

print("✓ LLM 生成成功\n")

# 解析生成的 Alpha 表达式

parsed_alphas = parse_alpha_expressions(response)

if not parsed_alphas:

print("警告: 未能解析出有效的 Alpha 表达式")

return []

print(f"成功解析 {len(parsed_alphas)} 个 Alpha 表达式，开始模拟...\n")

# 模拟新生成的 Alpha

new_alpha_ids = []

successful_simulations = []

failed_simulations = []

for idx, (expression, description) in enumerate(parsed_alphas, 1):

print(f"--- 模拟优化 Alpha {idx}/{len(parsed_alphas)} ---")

print(f"表达式: {expression}")

print(f"说明: {description}")

try:

simulate_data = ace.generate_alpha(

regular=expression,

alpha_type="REGULAR",

region="USA",

universe="TOP3000",

delay=1,

decay=0,

neutralization="INDUSTRY",

truncation=0.08,

pasteurization="ON",

nan_handling="OFF",

unit_handling="VERIFY",

visualization=True

)

print("正在提交模拟...")

simulation_result = ace.simulate_single_alpha(brain_session, simulate_data)

child_alpha_id = simulation_result.get('alpha_id')

if child_alpha_id:

print(f"✓ 模拟成功! Alpha ID: {child_alpha_id}")

# 设置标签（使用原始父 Alpha ID）

parent_tag = base_alpha.get('parent_alpha_id', base_alpha_id)

full_description = f"【父 Alpha】{parent_tag}\n【优化自】{base_alpha_id}\n【改进说明】{description}"

ace.set_alpha_properties(

brain_session,

child_alpha_id,

tags=[parent_tag],

regular_desc=full_description

)

print(f"✓ 已设置标签: {parent_tag}\n")

new_alpha_ids.append(child_alpha_id)

successful_simulations.append({

'alpha_id': child_alpha_id,

'expression': expression,

'description': description

})

else:

print(f"✗ 模拟失败: 未返回 Alpha ID\n")

failed_simulations.append({

'expression': expression,

'reason': '未返回 Alpha ID'

})

except Exception as e:

print(f"✗ 模拟出错: {str(e)}\n")

failed_simulations.append({

'expression': expression,

'reason': str(e)

})

# 输出总结

print(f"{'='*60}")

print(f"本轮优化模拟总结")

print(f"{'='*60}")

print(f"成功: {len(successful_simulations)} 个")

print(f"失败: {len(failed_simulations)} 个")

if successful_simulations:

print("\n成功的 Alpha:")

for item in successful_simulations:

print(f"  - {item['alpha_id']}: {item['expression'][:60]}...")

if failed_simulations:

print("\n失败的 Alpha:")

for item in failed_simulations:

print(f"  - {item['expression'][:60]}... (原因: {item['reason']})")

return new_alpha_ids

asyncdeffull_auto_iteration_workflow(parent_alpha_id,max_iterations=5,alphas_per_iteration=5,

selection_criteria='balanced', min_quality_threshold=None):

"""完全自动化的迭代优化工作流"""

brain_session = ace.start_session()

print(f"\n{'#'*80}")

print(f"# 完全自动化 Alpha 迭代优化工作流")

print(f"# 初始父 Alpha: {parent_alpha_id}")

print(f"# 最大迭代次数: {max_iterations}")

print(f"# 每轮生成数量: {alphas_per_iteration}")

print(f"# 选择标准: {selection_criteria}")

print(f"{'#'*80}\n")

# 设置默认质量阈值

if min_quality_threshold is None:

min_quality_threshold = {

'sharpe': 1.5,

'fitness': 1,

'turnover': 0.15

}

all_iterations_history = []

current_parent_id = parent_alpha_id

for iteration in range(1, max_iterations + 1):

print(f"\n{'='*80}")

print(f"第 {iteration}/{max_iterations} 轮迭代")

print(f"{'='*80}\n")

iteration_start_time = datetime.now()

# ===== 步骤 1: 获取当前 Alpha 家族 =====

print("步骤 1: 检索 Alpha 家族...")

alpha_ids = await get_alphas_by_tag(brain_session, current_parent_id)

if not alpha_ids:

if iteration == 1:

print(f"第一轮未找到 Alpha，请先运行初始 Alpha 生成")

return None

else:

print("未找到新的 Alpha，使用上一轮数据")

break

print(f"找到 {len(alpha_ids)} 个 Alpha\n")

# ===== 步骤 2: 获取性能数据 =====

print("步骤 2: 获取性能指标...")

performance_data = []

for alpha_id in alpha_ids:

print(f"  获取 {alpha_id}...")

perf = await get_alpha_performance(brain_session, alpha_id)

if perf:

perf['parent_alpha_id'] = current_parent_id

performance_data.append(perf)

if not performance_data:

print("未能获取任何性能数据")

break

performance_df = pd.DataFrame(performance_data)

print(f"成功获取 {len(performance_df)} 个 Alpha 的性能数据\n")

# ===== 步骤 3: 可视化 =====

print("步骤 3: 生成可视化图表...")

visualize_performance(performance_data, current_parent_id)

# ===== 步骤 4: 选择最佳 Alpha =====

print("\n步骤 4: 选择最佳 Alpha...")

best_alphas = await select_best_alphas(performance_df, selection_criteria, top_n=3)

if not best_alphas:

print("未能选择出最佳 Alpha")

break

# ===== 步骤 5: 检查是否达到质量阈值 =====

print("\n步骤 5: 检查质量阈值...")

top_alpha = best_alphas[0]

quality_check = (

top_alpha['sharpe'] >= min_quality_threshold['sharpe'] and

top_alpha['fitness'] >= min_quality_threshold['fitness'] and

top_alpha['turnover'] <= min_quality_threshold['turnover']

)

if quality_check:

print(f"✓ 达到质量阈值!")

print(f"  Sharpe: {top_alpha['sharpe']:.4f} >= {min_quality_threshold['sharpe']}")

print(f"  Fitness: {top_alpha['fitness']:.4f} >= {min_quality_threshold['fitness']}")

print(f"  Turnover: {top_alpha['turnover']:.4f} <= {min_quality_threshold['turnover']}")

should_continue = False

reason = "达到质量阈值，优化成功"

suggestions = []

else:

# ===== 步骤 6: 决策是否继续迭代 =====

print("\n步骤 6: 迭代决策...")

should_continue, reason, suggestions = await decide_next_iteration(

performance_df, iteration, max_iterations

)

# ===== 步骤 7: LLM 分析 =====

print("\n步骤 7: LLM 分析结果...")

llm_analysis = await llm_analyze_results(performance_df, current_parent_id, brain_session)

print(f"\n【LLM 分析】\n{llm_analysis}\n")

# ===== 步骤 8: 生成优化建议 =====

print("\n步骤 8: 生成优化建议...")

llm_suggestions = await llm_iteration_suggestions(performance_df, iteration, best_alphas)

print(f"\n【LLM 优化建议】\n{llm_suggestions}\n")

# 保存本轮数据

iteration_data = {

'iteration': iteration,

'parent_alpha_id': current_parent_id,

'alpha_count': len(alpha_ids),

'performance_df': performance_df,

'best_alphas': best_alphas,

'should_continue': should_continue,

'reason': reason,

'suggestions': suggestions,

'llm_analysis': llm_analysis,

'llm_suggestions': llm_suggestions,

'duration': (datetime.now() - iteration_start_time).total_seconds()

}

all_iterations_history.append(iteration_data)

# ===== 决策点: 是否继续迭代 =====

if not should_continue:

print(f"\n{'='*80}")

print(f"✓ 迭代结束: {reason}")

print(f"{'='*80}\n")

break

# ===== 步骤 9: 生成下一轮 Alpha =====

if iteration < max_iterations:

print(f"\n步骤 9: 生成下一轮优化 Alpha...")

print(f"{'='*80}\n")

new_alpha_ids = await generate_optimized_alphas_from_best(

best_alphas, brain_session, llm_suggestions,

num_new_alphas=alphas_per_iteration

)

if not new_alpha_ids:

print("未能生成新的 Alpha，迭代终止")

break

print(f"\n✓ 成功生成 {len(new_alpha_ids)} 个新 Alpha")

print(f"等待模拟完成后进入下一轮...\n")

# 等待一段时间让模拟完成

wait_time = 30

print(f"等待 {wait_time} 秒让模拟完成...")

await asyncio.sleep(wait_time)

# ===== 最终总结 =====

print(f"\n{'#'*80}")

print(f"# 迭代优化完成")

print(f"# 总迭代轮数: {len(all_iterations_history)}")

print(f"{'#'*80}\n")

# 汇总所有 Alpha

print("汇总所有迭代的 Alpha...")

all_alpha_ids = await get_alphas_by_tag(brain_session, parent_alpha_id)

all_performance_data = []

for alpha_id in all_alpha_ids:

perf = await get_alpha_performance(brain_session, alpha_id)

if perf:

all_performance_data.append(perf)

final_performance_df = pd.DataFrame(all_performance_data)

# 选择最终的最佳 Alpha

print("\n选择最终最佳 Alpha...")

final_best_alphas = await select_best_alphas(final_performance_df, selection_criteria, top_n=5)

# 生成最终可视化

print("\n生成最终性能对比图...")

visualize_performance(all_performance_data, parent_alpha_id)

# 导出最终报告

print("\n导出最终报告...")

final_report = await export_alpha_family(

parent_alpha_id,

final_performance_df,

final_best_alphas,

output_file=f'alpha_family_{parent_alpha_id}_final_report.txt'

)

# 返回完整结果

return {

'iterations_history': all_iterations_history,

'final_performance_df': final_performance_df,

'final_best_alphas': final_best_alphas,

'final_report': final_report,

'total_alphas_generated': len(all_alpha_ids),

'total_iterations': len(all_iterations_history)

}

# ==================== 执行完全自动化工作流 ====================

# 运行完全自动化的迭代优化

parent_alpha_id = "kqEnlEA8"  # 替换为你的初始父 Alpha ID

results = await full_auto_iteration_workflow(

parent_alpha_id=parent_alpha_id,

max_iterations=8,              # 最多迭代 8 轮

alphas_per_iteration=5,        # 每轮生成 5 个 Alpha

selection_criteria='balanced',  # 综合平衡选择

min_quality_threshold={        # 质量阈值（达到即停止）

'sharpe': 1.5,

'fitness': 1,

'turnover': 0.15

}

)

# 查看结果

if results:

print(f"\n{'='*80}")

print("最终结果摘要")

print(f"{'='*80}")

print(f"总迭代轮数: {results['total_iterations']}")

print(f"总生成 Alpha 数: {results['total_alphas_generated']}")

print(f"\nTop 5 最佳 Alpha:")

for i, alpha in enumerate(results['final_best_alphas'][:5], 1):

print(f"{i}. {alpha['alpha_id']} - Sharpe: {alpha['sharpe']:.4f}, Fitness: {alpha['fitness']:.4f}")

！！！！最后欢迎在评论区讨论和留言，看到点赞和留言我会开心。

---

## 讨论与评论 (25)

### 评论 #1 (作者: YZ14671, 时间: 7个月前)

以下是一些有关的文章链接：
 [【MCP】角色配置：工作流该安排谁来执行？ – WorldQuant BRAIN](../FX25214/[Commented] 【MCP】角色配置工作流该安排谁来执行经验分享.md) 
 [AIAC 2025的一些小 Tips – WorldQuantBrain-CN](/hc/zh-cn/community/posts/36141016690199-AIAC-2025%E7%9A%84%E4%B8%80%E4%BA%9B%E5%B0%8F-Tips) 
 [[AIAC 2025 比赛] 迭代法寻找集合中Score最高SA – WorldQuantBrain-CN](../YH25030/[Commented] [AIAC 2025 比赛] 迭代法寻找集合中Score最高SA.md) 
 [AI比赛参考工作流 – WorldQuantBrain-CN](../YH25030/[Commented] AI比赛参考工作流.md) 
 [【AI Alphas Competition 2025比赛】了解最新比赛的规则和玩法 – WorldQuantBrain-CN](../MQ62208/【AI Alphas Competition 2025比赛】了解最新比赛的规则和玩法.md)

---

### 评论 #2 (作者: PS55811, 时间: 7个月前)

叹为观止！

---

### 评论 #3 (作者: LL49894, 时间: 7个月前)

请教一下大佬。这个做出来的是regular alpha么？我看比赛是要求提交super？

--------------------------------------------------------------------------------------------------------

祝VF1

---

### 评论 #4 (作者: FX25214, 时间: 7个月前)

我一直都想有一个ai全自动流程的因子生产程序，只能说看到这样的开源代码真的是太过于兴奋了，大佬的含金量还在上升！！！这份代码我会非常认真的学习和借鉴的！

---

### 评论 #5 (作者: HZ99685, 时间: 7个月前)

如果能实现自动在不同的region和dataset之间搜索和组合的功能就更完美了。

---

### 评论 #6 (作者: YZ14671, 时间: 7个月前)

该代码跑出来的是regular alpha，只有交够足够的ra才可以组装sa，代码还有很多缺陷和不足，如果大家测试后也希望大家批评指正，感谢

---

### 评论 #7 (作者: CL86067, 时间: 7个月前)

太强了，感谢大佬的无私分享，就算不参加比赛了这份代码也对新手研究ai生成alpha有很大意义，很值得我们学习，接下来就去学习尝试一下，未来的alpha研究是离不开ai了。

祝大佬ai比赛拿奖，vf节节高！

---

### 评论 #8 (作者: HZ99685, 时间: 7个月前)

感谢大佬的分享，新手小白还在研究AI比赛阶段。自己尝试在notebook运行代码后，总是报错 AsyncLibraryNotFoundError: unknown async library, or not in async context，是什么原因？

---

### 评论 #9 (作者: GZ60647, 时间: 7个月前)

同群的大佬，来膜拜一下，代码先搞下来慢慢研究

---

### 评论 #10 (作者: YZ14671, 时间: 7个月前)

[HZ99685](/hc/zh-cn/profiles/32603557750935-HZ99685)

- 可以试一试这三个方法
  # 方案 1：使用 nest_asyncio
  import nest_asyncio
  nest_asyncio.apply()
  # 方案 2：使用 asyncio.run()
  import asyncio
  result = asyncio.run(your_async_function())
  # 方案 3：在 Jupyter 中直接 await
  result = await your_async_function()

---

### 评论 #11 (作者: PX70901, 时间: 7个月前)

牛!

---

### 评论 #12 (作者: ZL15100, 时间: 7个月前)

这代码配置在哪里运行了，在VScode里运行了，就能让MCP按照流程帮你办事吗，完全不懂，请大佬详细说明一下

---

### 评论 #13 (作者: HZ49684, 时间: 7个月前)

之前还没注意过 AIAC的比赛，看了大佬的帖子 深受启发！！已经成功用起来，实践过程发现有限流的可能 我改造了一下代码，可以有个五分钟的重试

async def simulate_alpha(expression, description, brain_session, parent_alpha_id):

"""模拟单个 Alpha 表达式（持续重试直到成功或超时5分钟）"""

max_total_time = 300  # 最大总等待时间：5分钟（300秒）

start_time = time.time()

attempt = 0

while time.time() - start_time < max_total_time:

attempt += 1

elapsed_time = time.time() - start_time

remaining_time = max_total_time - elapsed_time

try:

simulate_data = ace.generate_alpha(

regular=expression,

alpha_type="REGULAR",

region=REGION,

universe=UNIVERSE,

delay=1,

decay=0,

neutralization="INDUSTRY",

truncation=0.08,

pasteurization="ON",

nan_handling="OFF",

unit_handling="VERIFY",

visualization=True

)

print(f"正在提交模拟 (尝试 {attempt}，已等待 {elapsed_time:.1f}秒，剩余 {remaining_time:.1f}秒)...")

simulation_result = ace.simulate_single_alpha(brain_session, simulate_data)

child_alpha_id = simulation_result.get('alpha_id')

if child_alpha_id:

print(f"✓ 模拟成功! Alpha ID: {child_alpha_id} (总等待时间: {elapsed_time:.1f}秒)")

full_description = f"【父 Alpha】{parent_alpha_id}\n【经济学逻辑】{description}"

ace.set_alpha_properties(

brain_session,

child_alpha_id,

tags=[parent_alpha_id],

regular_desc=full_description

)

print(f"✓ 已设置标签和描述")

return {

'alpha_id': child_alpha_id,

'expression': expression,

'description': description,

'status': 'success',

'attempts': attempt,

'total_wait_time': elapsed_time

}

else:

# 检查模拟是否失败（status: 'FAIL'）

if simulation_result.get('status') == 'FAIL':

print(f"✗ 模拟失败: {simulation_result}")

return {

'expression': expression,

'description': description,

'status': 'error',

'reason': f"模拟失败: {simulation_result}",

'attempts': attempt,

'total_wait_time': elapsed_time

}

else:

# 其他情况（如并发限制）继续重试

print(f"⚠ 未返回 Alpha ID，等待后重试...")

wait_time = min(0.1, remaining_time)

if wait_time > 0:

print(f"等待 {wait_time:.1f} 秒后重试... (剩余总时间: {remaining_time:.1f}秒)")

await asyncio.sleep(wait_time)

else:

return {

'expression': expression,

'description': description,

'status': 'error',

'reason': f"达到最大等待时间仍未成功: 未返回 Alpha ID",

'attempts': attempt,

'total_wait_time': elapsed_time

}

except Exception as e:

error_msg = str(e)

print(f"捕获异常: {error_msg}")  # 调试信息

if "CONCURRENT_SIMULATION_LIMIT_EXCEEDED" in error_msg or "429" in error_msg:

# 固定0.01秒重试间隔

wait_time = min(0.01, remaining_time)

if wait_time > 0:

print(f"⚠ 遇到并发限制，等待 {wait_time:.1f} 秒后重试... (剩余总时间: {remaining_time:.1f}秒)")

await asyncio.sleep(wait_time)

else:

# 没有足够时间继续重试

return {

'expression': expression,

'description': description,

'status': 'error',

'reason': f"达到最大等待时间仍未成功: {error_msg}",

'attempts': attempt,

'total_wait_time': elapsed_time

}

else:

# 其他错误不重试

return {

'expression': expression,

'description': description,

'status': 'error',

'reason': error_msg,

'attempts': attempt,

'total_wait_time': elapsed_time

}

# 超时退出

elapsed_time = time.time() - start_time

return {

'expression': expression,

'description': description,

'status': 'error',

'reason': f"达到最大等待时间 ({max_total_time}秒) 仍未成功",

'attempts': attempt,

'total_wait_time': elapsed_time

}

---

### 评论 #14 (作者: MG88592, 时间: 7个月前)

感谢大佬的分享！！！！

国区大佬越来越多，无私的开源分享精神会让国区越来越强

下个季度回测数量被压缩，一定要用好ai去筛掉无效回测。太感谢了

============================================================================================================================================================================================================================================================

---

### 评论 #15 (作者: AM12075, 时间: 7个月前)

------------------------------------------------------------------------------------------------------------------------------------

请问运行结果如何，组出的SA表现怎么样，另外所有人跑同一个代码出来的因子会不会相关性很高？

------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #16 (作者: FZ24842, 时间: 7个月前)

感谢大佬分享

---

### 评论 #17 (作者: ZY90817, 时间: 7个月前)

最终的结果最好能把是否通过，指标比对和自相关性检查加进去，这样可以一眼看出哪个更好~

---

### 评论 #18 (作者: LW52547, 时间: 7个月前)

感谢分享，学习了，感想就一个字“牛”！！！

---

### 评论 #19 (作者: YZ14671, 时间: 7个月前)

@ [ZL15100，
需要AIAC比赛的相关代码配置，请在AIAC比赛的提交notbook代码链接处下载相关代码（若后续无法下载可以在学习群里找群友分享一下），以上代码只包含了notebook代码，使用时请配置自己的账号和使用模型的key，该代码使用的是DeepSeek的chat模型](/hc/en-us/profiles/33171940219927-ZL15100) ，直接在vs就可以直接使用，后续如果有时间我应该会出个具体的教程，不敢保证一定会更新，但有时间就会更新

---

### 评论 #20 (作者: JC21292, 时间: 6个月前)

要是有运行的截图就更好了

---

### 评论 #21 (作者: MS51256, 时间: 6个月前)

感谢大佬的分享！！！！

国区大佬越来越多，无私的开源分享精神会让国区越来越强

下个季度回测数量被压缩，一定要用好ai去筛掉无效回测。太感谢了

---

### 评论 #22 (作者: AP88202, 时间: 6个月前)

感谢大佬的分享！！！！

import ace_lib as ace， 请问如何下载ace_lib代码，要不代码无法运行

---

### 评论 #23 (作者: XX83557, 时间: 6个月前)

新手小白对这个不懂，能不能弄一个压缩包然后写一个说明修改哪里的文档。

---

### 评论 #24 (作者: JL40454, 时间: 6个月前)

特别好用, 尤其是分析的思路, 给了我许多启发

---

### 评论 #25 (作者: MZ45384, 时间: 4个月前)

Template Captured:

<ts_op/>(<data/>, <days/>) - <ts_op/>(<group_op/>(<data/>, <group/>), <days/>)

看起来是一个很通用的模板，希望在其他区域也好用。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

