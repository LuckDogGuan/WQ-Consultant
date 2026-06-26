# 获取生产相关性代码改进代码优化

- **链接**: [Commented] 获取生产相关性代码改进代码优化.md
- **作者**: GW98315
- **发布时间/热度**: 5个月前, 得票: 6

## 帖子正文

最近读了大佬的一篇帖子：避免频繁登录可以复用session cookie 代码检查ppac prod 相关性-python代码

[https://support.worldquantbrain.com/hc/en-us/community/posts/35769856074007-%E9%81%BF%E5%85%8D%E9%A2%91%E7%B9%81%E7%99%BB%E5%BD%95%E5%8F%AF%E4%BB%A5%E5%A4%8D%E7%94%A8session-cookie-%E4%BB%A3%E7%A0%81%E6%A3%80%E6%9F%A5ppac-prod-%E7%9B%B8%E5%85%B3%E6%80%A7-python%E4%BB%A3%E7%A0%81?input_string=%E8%8E%B7%E5%8F%96%E7%94%9F%E4%BA%A7%E7%9B%B8%E5%85%B3%E6%80%A7](https://support.worldquantbrain.com/hc/en-us/community/posts/35769856074007-%E9%81%BF%E5%85%8D%E9%A2%91%E7%B9%81%E7%99%BB%E5%BD%95%E5%8F%AF%E4%BB%A5%E5%A4%8D%E7%94%A8session-cookie-%E4%BB%A3%E7%A0%81%E6%A3%80%E6%9F%A5ppac-prod-%E7%9B%B8%E5%85%B3%E6%80%A7-python%E4%BB%A3%E7%A0%81?input_string=%E8%8E%B7%E5%8F%96%E7%94%9F%E4%BA%A7%E7%9B%B8%E5%85%B3%E6%80%A7)

发现有几点可以优化：

1、

- 实现了智能等待机制，根据回测进度动态调整等待时间
- 在进度35%之前等待60秒，超过35%后只需等待5秒，大幅减少GET请求次数
- 有效避免429/502等错误，提高API调用成功率

2、

•  封装了多种重要功能，如获取用户信息、Alpha详情、Alpha列表等
      • 提供了相关性检查功能（生产环境和Power Pool）
      • 实现了Alpha提交资格检查功能

3、

• 实现了进度保存和加载功能，支持断点续传
      • 使用JSON文件记录处理进度，避免重复处理

4、

• 在处理完每个Alpha后添加延时，避免触发平台限流
      • 合理控制请求频率，保护账户安全

代码如下：

"""

使用 Cookie 直接访问 WorldQuant BRAIN API 的测试脚本

避免频繁登录，使用现有的 session cookie

"""

import requests

import json

import time

import pandas as pd  # 添加pandas用于Excel输出

import os

from typing import Dict, Any, Optional

# 优化配置：根据进度动态调整等待时间

# 参考：WorldQuant API调用神器：告别回测中429、502错误

WAIT_TIME_BEFORE_35_PERCENT = 60 # 35%前等待60秒

WAIT_TIME_AFTER_35_PERCENT = 5 # 35%后等待5秒

PROGRESS_THRESHOLD = 0.35 # 进度阈值

class BrainCookieClient:

"""使用 Cookie 访问 BRAIN API 的客户端"""

def __init__(self, cookie_string: str):

"""

初始化客户端

Args:

cookie_string: 完整的 Cookie 字符串

"""

self.base_url = " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) "

self.session = requests.Session()

# 解析 Cookie 字符串

self.cookies = self._parse_cookie_string(cookie_string)

self.session.cookies.update(self.cookies)

# 设置请求头

self.session.headers.update({

'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',

'Accept': 'application/json',

'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',

'Origin': ' [https://platform.worldquantbrain.com](https://platform.worldquantbrain.com) ',

'Referer': ' [https://platform.worldquantbrain.com/](https://platform.worldquantbrain.com/) ',

})

def _get_smart_wait_time(self, retry_after: float, progress: float=None) -> float:

"""

智能计算等待时间，根据进度动态调整

优化策略：

- 回测在35%进度前卡得最久，等待60秒

- 超过35%后很快完成，只需等待5秒

- 这样可以大幅减少GET请求次数，避免429/502错误

Args:

retry_after: API返回的Retry-After时间

progress: 当前进度（0.0-1.0），如果为None则使用retry_after

Returns:

优化后的等待时间

"""

if progress is None:

# 如果没有进度信息，使用API返回的时间

return retry_after

# 根据进度动态调整

if progress <= PROGRESS_THRESHOLD:

# 35%前使用较长等待时间

return WAIT_TIME_BEFORE_35_PERCENT

else:

# 35%后使用较短等待时间

return WAIT_TIME_AFTER_35_PERCENT

def _parse_cookie_string(self, cookie_string: str) -> Dict[str, str]:

"""

解析 Cookie 字符串为字典

Args:

cookie_string: Cookie 字符串，格式如 "key1=value1; key2=value2"

Returns:

Cookie 字典

"""

cookies = {}

for item in cookie_string.split(';'):

item = item.strip()

if '=' in item:

key, value = item.split('=', 1)

cookies[key.strip()] = value.strip()

return cookies

def test_connection(self) -> bool:

"""

测试连接是否有效

Returns:

是否连接成功

"""

try:

response = self.session.get(f"{self.base_url}/users/self")

if response.status_code == 200:

user_info = response.json()

print(f"✅ 连接成功！用户信息：")

print(f" - 用户ID: {user_info.get('id', 'N/A')}")

print(f" - 用户名: {user_info.get('username', 'N/A')}")

print(f" - 邮箱: {user_info.get('email', 'N/A')}")

return True

else:

print(f"❌ 连接失败，状态码: {response.status_code}")

print(f" 响应: {response.text}")

return False

except Exception as e:

print(f"❌ 连接异常: {e}")

return False

def get_alpha_details(self, alpha_id: str) -> Optional[Dict[str, Any]]:

"""

获取 Alpha 详细信息

Args:

alpha_id: Alpha ID

Returns:

Alpha 详细信息字典，失败返回 None

"""

try:

url = f"{self.base_url}/alphas/{alpha_id}"

response = self.session.get(url)

if response.status_code == 200:

alpha_data = response.json()

print(f"\n✅ 成功获取 Alpha {alpha_id} 信息：")

print(f" - 名称: {alpha_data.get('name', 'N/A')}")

print(f" - 状态: {alpha_data.get('status', 'N/A')}")

print(f" - 创建时间: {alpha_data.get('dateCreated', 'N/A')}")

# 如果有 regular 代码

if 'regular' in alpha_data and alpha_data['regular']:

code = str(alpha_data['regular'])

print(f" - Regular 代码: {code[:100]}...")

# 如果有性能指标

if 'is' in alpha_data:

is_data = alpha_data['is']

print(f" - Sharpe: {is_data.get('sharpe', 'N/A')}")

print(f" - Fitness: {is_data.get('fitness', 'N/A')}")

print(f" - Returns: {is_data.get('returns', 'N/A')}")

return alpha_data

else:

print(f"❌ 获取 Alpha 失败，状态码: {response.status_code}")

print(f" 响应: {response.text}")

return None

except Exception as e:

print(f"❌ 获取 Alpha 异常: {e}")

return None

def get_user_alphas(self, stage: str="IS", limit: int=100, color: str=None, fetch_all: bool=False) -> Optional[list]:

"""

获取用户的 Alpha 列表

Args:

stage: Alpha 阶段，"IS" 或 "OS"

limit: 每次返回数量限制（最大100）

color: Alpha 颜色过滤，如 "GREEN"，"RED" 等

fetch_all: 是否获取所有 Alpha（通过分页）

Returns:

Alpha 列表，失败返回 None

"""

try:

url = f"{self.base_url}/users/self/alphas"

all_alphas = []

if fetch_all:

# 分页获取所有 Alpha

offset = 0

while True:

params = {

'stage': stage,

'limit': min(limit, 100),  # API 限制最大为100

'offset': offset

}

# 如果指定了颜色，则添加到参数中

if color:

params['color'] = color

response = self.session.get(url, params=params)

if response.status_code == 200:

data = response.json()

alphas = data.get('results', [])

if not alphas:  # 如果没有更多 Alpha，跳出循环

break

all_alphas.extend(alphas)

# 如果返回的 Alpha 数量小于请求的数量，说明已获取完所有 Alpha

if len(alphas) < min(limit, 100):

break

offset += len(alphas)

print(f"✅ 已获取 {len(all_alphas)} 个 Alpha...")

else:

print(f"❌ 获取 Alpha 列表失败，状态码: {response.status_code}")

print(f" 响应: {response.text}")

return None

print(f"\n✅ 总共获取到 {len(all_alphas)} 个 {stage} Alpha")

if color:

print(f"（已过滤为颜色: {color}）")

else:

# 只获取指定数量的 Alpha

params = {

'stage': stage,

'limit': limit,

'offset': 0

}

# 如果指定了颜色，则添加到参数中

if color:

params['color'] = color

response = self.session.get(url, params=params)

if response.status_code == 200:

data = response.json()

all_alphas = data.get('results', [])

print(f"\n✅ 成功获取 {len(all_alphas)} 个 {stage} Alpha")

if color:

print(f"（已过滤为颜色: {color}）：")

else:

print("：")

for i, alpha in enumerate(all_alphas[:5], 1): # 只显示前5个

print(f" {i}. {alpha.get('id', 'N/A')} - {alpha.get('name', 'N/A')}")

if 'is' in alpha:

print(f" Sharpe: {alpha['is'].get('sharpe', 'N/A')}, "

f"Fitness: {alpha['is'].get('fitness', 'N/A')}")

if len(all_alphas) > 5:

print(f" ... 还有 {len(all_alphas) - 5} 个")

return all_alphas

except Exception as e:

print(f"❌ 获取 Alpha 列表异常: {e}")

return None

def check_prod_correlation(self, alpha_id: str, verbose: bool=True) -> Optional[Dict[str, Any]]:

"""

检查 Alpha 与生产环境的相关性（循环等待）

Args:

alpha_id: Alpha ID

verbose: 是否显示详细信息

Returns:

相关性数据字典，失败返回 None

"""

try:

url = f"{self.base_url}/alphas/{alpha_id}/correlations/prod"

if verbose:

print(f"\n🔍 检查 Alpha {alpha_id} 的生产相关性...")

# 循环等待检查完成（使用智能等待策略）

retry_count = 0

total_wait_time = 0

while True:

try:

response = self.session.get(url, timeout=60)

# 检查是否需要等待

if "retry-after" in response.headers:

retry_after = float(response.headers["Retry-After"])

# 尝试获取进度信息（如果API返回）

progress = None

try:

data = response.json()

progress = data.get('progress', None)

except:

pass

# 使用智能等待时间

wait_time = self._get_smart_wait_time(retry_after, progress)

if verbose and retry_count % 5 == 0: # 每5次显示一次

progress_str = f", 进度: {progress*100:.1f}%" if progress else ""

print(f" ⏳ 计算中... (已等待 {retry_count} 次, {total_wait_time:.0f}秒{progress_str})")

time.sleep(wait_time)

retry_count += 1

total_wait_time += wait_time

else:

# 检查完成

break

except requests.exceptions.Timeout:

if verbose:

print(f" ⚠️ 请求超时，继续重试...")

time.sleep(2)

continue

if response.status_code == 200:

# 检查响应内容

if not response.text or response.text.strip() == '':

if verbose:

print(f"⚠️ 响应为空，该 Alpha 可能不符合计算条件")

return None

corr_data = response.json()

if verbose:

print(f"✅ 成功获取生产相关性数据 (等待 {retry_count} 次, 总计 {total_wait_time:.0f}秒)")

# 显示最高相关性

if 'correlations' in corr_data and corr_data['correlations']:

top_corr = corr_data['correlations'][0]

print(f" 最高相关性: {top_corr.get('correlation', 'N/A'):.4f}")

print(f" 相关 Alpha: {top_corr.get('alphaId', 'N/A')}")

# 显示统计信息

if 'summary' in corr_data:

summary = corr_data['summary']

print(f" 平均相关性: {summary.get('mean', 'N/A')}")

print(f" 最大相关性: {summary.get('max', 'N/A')}")

return corr_data

else:

if verbose:

print(f"❌ 获取失败，状态码: {response.status_code}")

print(f" 响应: {response.text[:200]}")

return None

except Exception as e:

if verbose:

print(f"❌ 检查异常: {e}")

return None

def check_power_pool_correlation(self, alpha_id: str, verbose: bool=True) -> Optional[Dict[str, Any]]:

"""

检查 Alpha 与 Power Pool 的相关性（循环等待）

Args:

alpha_id: Alpha ID

verbose: 是否显示详细信息

Returns:

相关性数据字典，失败返回 None

"""

try:

url = f"{self.base_url}/alphas/{alpha_id}/correlations/power-pool"

if verbose:

print(f"\n🔍 检查 Alpha {alpha_id} 的 Power Pool 相关性...")

# 循环等待检查完成（使用智能等待策略）

retry_count = 0

total_wait_time = 0

while True:

try:

response = self.session.get(url, timeout=60)

# 检查是否需要等待

if "retry-after" in response.headers:

retry_after = float(response.headers["Retry-After"])

# 尝试获取进度信息（如果API返回）

progress = None

try:

data = response.json()

progress = data.get('progress', None)

except:

pass

# 使用智能等待时间

wait_time = self._get_smart_wait_time(retry_after, progress)

if verbose and retry_count % 5 == 0: # 每5次显示一次

progress_str = f", 进度: {progress*100:.1f}%" if progress else ""

print(f" ⏳ 计算中... (已等待 {retry_count} 次, {total_wait_time:.0f}秒{progress_str}")

time.sleep(wait_time)

retry_count += 1

total_wait_time += wait_time

else:

# 检查完成

break

except requests.exceptions.Timeout:

if verbose:

print(f" ⚠️ 请求超时，继续重试...")

time.sleep(2)

continue

if response.status_code == 200:

# 检查响应内容

if not response.text or response.text.strip() == '':

if verbose:

print(f"⚠️ 响应为空，该 Alpha 可能不符合计算条件")

return None

corr_data = response.json()

if verbose:

print(f"✅ 成功获取 Power Pool 相关性数据 (等待 {retry_count} 次, 总计 {total_wait_time:.0f}秒)")

# 显示最高相关性

if 'correlations' in corr_data and corr_data['correlations']:

top_corr = corr_data['correlations'][0]

print(f" 最高相关性: {top_corr.get('correlation', 'N/A'):.4f}")

print(f" 相关 Alpha: {top_corr.get('alphaId', 'N/A')}")

# 显示统计信息

if 'summary' in corr_data:

summary = corr_data['summary']

print(f" 平均相关性: {summary.get('mean', 'N/A')}")

print(f" 最大相关性: {summary.get('max', 'N/A')}")

return corr_data

else:

if verbose:

print(f"❌ 获取失败，状态码: {response.status_code}")

print(f" 响应: {response.text[:200]}")

return None

except Exception as e:

if verbose:

print(f"❌ 检查异常: {e}")

return None

def check_correlation_smart(self, alpha_id: str, verbose: bool=True) -> Optional[Dict[str, Any]]:

"""

智能检查相关性：自动判断是 PPAC 还是普通 Alpha，然后检查对应的相关性

Args:

alpha_id: Alpha ID

verbose: 是否显示详细信息

Returns:

相关性数据字典，失败返回 None

"""

try:

# 先获取 Alpha 详情

alpha_data = self.get_alpha_details(alpha_id)

if not alpha_data:

if verbose:

print(f"❌ 无法获取 Alpha {alpha_id} 信息")

return None

# 判断是否是 PPAC Alpha

tags = alpha_data.get('tags', [])

classifications = alpha_data.get('classifications', [])

is_ppac = 'PowerPoolSelected' in tags or any(

c.get('id', '').startswith('POWER_POOL:') for c in classifications

)

if verbose:

if is_ppac:

print(f"🎯 检测到 PPAC Alpha，检查 Power Pool 相关性...")

else:

print(f"📝 检测到普通 Alpha，检查生产相关性...")

# 根据类型检查对应的相关性

if is_ppac:

return self.check_power_pool_correlation(alpha_id, verbose=verbose)

else:

return self.check_prod_correlation(alpha_id, verbose=verbose)

except Exception as e:

if verbose:

print(f"❌ 智能检查异常: {e}")

return None

def check_alpha_submission(self, alpha_id: str, verbose: bool=True, max_retries: int=5) -> Optional[Dict[str, Any]]:

"""

检查 Alpha 是否可以提交（循环等待检查完成）

Args:

alpha_id: Alpha ID

verbose: 是否显示详细信息

max_retries: 最大重试次数

Returns:

检查结果字典，失败返回 None

"""

try:

url = f"{self.base_url}/alphas/{alpha_id}/check"

if verbose:

print(f"\n🔍 开始检查 Alpha {alpha_id}...")

# 循环等待检查完成（参考 machine_lib.py 的实现）

retry_count = 0

total_wait_time = 0

while True:

try:

# 增加超时时间到 60 秒

response = self.session.get(url, timeout=60)

# 检查是否需要等待

if "retry-after" in response.headers:

wait_time = float(response.headers["Retry-After"])

# 记录等待时间，用于检测限流

total_wait_time += wait_time

if verbose:

print(f" ⏳ 检查进行中，等待 {wait_time:.1f} 秒... (累计等待: {total_wait_time:.1f}s)")

time.sleep(wait_time)

else:

# 检查完成

break

except requests.exceptions.Timeout:

retry_count += 1

if retry_count >= max_retries:

if verbose:

print(f"❌ 请求超时，已重试 {max_retries} 次")

return None

if verbose:

print(f" ⚠️ 请求超时，重试 {retry_count}/{max_retries}...")

time.sleep(2)

continue

if response.status_code == 200:

check_data = response.json()

# 检查是否有 is 数据

if check_data.get("is", 0) == 0:

if verbose:

print(f"❌ 会话可能已过期，请重新登录")

return None

# 获取检查结果

checks = check_data.get("is", {}).get("checks", [])

if verbose:

print(f"\n✅ 检查完成！")

print(f"\n检查项目结果：")

for check in checks:

name = check.get('name', 'N/A')

result = check.get('result', 'N/A')

value = check.get('value', '')

# 跳过 REGULAR_SUBMISSION

if name == "REGULAR_SUBMISSION":

continue

# 根据结果显示不同的图标

if result == "PASS":

icon = "✅"

elif result == "FAIL":

icon = "❌"

elif result == "WARNING":

icon = "⚠️"

else:

icon = "🔍"

value_str = f" (값: {value})" if value else ""

print(f" {icon}{name}: {result}{value_str}")

# 判断是否有失败项

has_fail = any(check.get('result') == 'FAIL' for check in checks

if check.get('name') != 'REGULAR_SUBMISSION')

if has_fail:

if verbose:

print(f"\n❌ 检查未通过，不能提交")

else:

if verbose:

print(f"\n✅ 所有检查通过，可以提交！")

return check_data

else:

if verbose:

print(f"❌ 检查失败，状态码: {response.status_code}")

print(f" 响应: {response.text}")

return None

except Exception as e:

if verbose:

print(f"❌ 检查异常: {e}")

return None

def save_alpha_to_file(self, alpha_id: str, filename: str) -> bool:

"""

保存 Alpha 详细信息到文件

Args:

alpha_id: Alpha ID

filename: 保存的文件名

Returns:

是否保存成功

"""

alpha_data = self.get_alpha_details(alpha_id)

if alpha_data:

try:

with open(filename, 'w', encoding='utf-8') as f:

json.dump(alpha_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Alpha 信息已保存到: {filename}")

return True

except Exception as e:

print(f"❌ 保存文件失败: {e}")

return False

return False

def save_progress(self, processed_alpha_ids: list, filename: str = "alpha_processing_progress.json"):

"""

保存处理进度

Args:

processed_alpha_ids: 已处理的 Alpha ID 列表

filename: 保存进度的文件名

"""

progress_data = {

"processed_alpha_ids": processed_alpha_ids,

"last_update": time.time()

}

try:

with open(filename, 'w', encoding='utf-8') as f:

json.dump(progress_data, f, ensure_ascii=False, indent=2)

print(f"✅ 进度已保存到 {filename}")

except Exception as e:

print(f"❌ 保存进度失败: {e}")

def load_progress(self, filename: str = "alpha_processing_progress.json") -> list:

"""

加载处理进度

Args:

filename: 保存进度的文件名

Returns:

已处理的 Alpha ID 列表

"""

try:

if os.path.exists(filename):

with open(filename, 'r', encoding='utf-8') as f:

progress_data = json.load(f)

return progress_data.get("processed_alpha_ids", [])

else:

print(f"ℹ️ 进度文件 {filename} 不存在，将从头开始处理")

return []

except Exception as e:

print(f"❌ 加载进度失败: {e}")

return []

def main():

"""主测试函数"""

print("="*60)

print("WorldQuant BRAIN Cookie Session 测试")

print("="*60)

print("\n请按以下步骤获取Cookie:")

print("1. 登录到  [https://platform.worldquantbrain.com](https://platform.worldquantbrain.com) ")

print("2. 按F12打开开发者工具")

print("3. 选择Network标签页")

print("4. 刷新页面")

print("5. 点击任意API请求（如/users/self）")

print("6. 在Request Headers中找到'cookie'行")

print("7. 复制整行cookie值，替换下面变量的值")

print("-"*60)

# 从user_info.txt文件中读取cookie，如果不存在则使用默认值

cookie_file_path = "user_info.txt"

cookie_string = ""

try:

with open(cookie_file_path, 'r', encoding='utf-8') as f:

for line in f:

if line.startswith("cookie:"):

cookie_string = line.replace("cookie:", "").strip()

break

except FileNotFoundError:

pass

if not cookie_string:

# 如果user_info.txt中没有cookie，提示用户设置

print(f"\n⚠️  在 {cookie_file_path} 中未找到cookie配置")

print("请在user_info.txt文件中添加cookie配置，格式如下：")

print("username:your_username")

print("password:your_password")

print("cookie:your_full_cookie_string_here")

print("\n或者直接编辑此文件中的cookie_string变量")

# 提供一个示例格式，但不包含实际值

cookie_string = input("\n请输入您的cookie字符串: ").strip()

# 创建客户端

client = BrainCookieClient(cookie_string)

# 1. 测试连接

print("\n【步骤 1】测试连接...")

if not client.test_connection():

print("\n⚠️ Cookie 可能已过期或无效，请重新获取")

return

# 2. 获取用户的绿色 Unsubmitted Alpha 列表

print(f"\n【步骤 2】获取用户的绿色 Unsubmitted Alpha 列表...")

user_alphas = client.get_user_alphas(stage="IS", limit=100, color="GREEN", fetch_all=True)

if not user_alphas or len(user_alphas) == 0:

print("❌ 未找到任何绿色的 Alpha，将跳过详细信息获取步骤")

return  # 如果没有Alpha，则直接结束程序

# 加载之前的处理进度

processed_alpha_ids = client.load_progress()

print(f"✅ 已加载 {len(processed_alpha_ids)} 个已处理的 Alpha ID")

# 过滤掉已处理的 Alpha

remaining_alphas = [alpha for alpha in user_alphas if alpha.get('id') not in processed_alpha_ids]

print(f"📊 总共 {len(user_alphas)} 个 Alpha，剩余 {len(remaining_alphas)} 个待处理")

if not remaining_alphas:

print("✅ 所有 Alpha 都已处理完毕")

# 输出检查通过的 Alpha 到 Excel

if processed_alpha_ids:

print("正在生成 Excel 报告...")

# 这里需要重新获取已处理的 Alpha 的详细信息来生成 Excel

all_alpha_details = []

for alpha_id in processed_alpha_ids:

alpha_data = client.get_alpha_details(alpha_id)

if alpha_data:

# 获取提交检查结果

submission_check = client.check_alpha_submission(alpha_id, verbose=False)

checks = submission_check.get("is", {}).get("checks", []) if submission_check else []

has_fail = any(check.get('result') == 'FAIL' for check in checks

if check.get('name') != 'REGULAR_SUBMISSION')

if not has_fail and submission_check:

tags = alpha_data.get('tags', [])

classifications = alpha_data.get('classifications', [])

is_ppac = 'PowerPoolSelected' in tags or any(

c.get('id', '').startswith('POWER_POOL:') for c in classifications

)

alpha_info = {

'ID': alpha_id,

'Name': alpha_data.get('name', ''),

'Status': alpha_data.get('status', ''),

'Created': alpha_data.get('dateCreated', ''),

'Type': 'PPAC' if is_ppac else 'Regular',

'Sharpe': alpha_data.get('is', {}).get('sharpe', ''),

'Fitness': alpha_data.get('is', {}).get('fitness', ''),

'Returns': alpha_data.get('is', {}).get('returns', ''),

'Tags': ', '.join(tags) if tags else ''

}

all_alpha_details.append(alpha_info)

if all_alpha_details:

df = pd.DataFrame(all_alpha_details)

excel_filename = f"passed_alphas_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"

df.to_excel(excel_filename, index=False)

print(f"\n📊 检查通过的 Alpha 已保存到: {excel_filename}")

print(f"📈 共有 {len(all_alpha_details)} 个 Alpha 检查通过")

else:

print(f"\n📈 没有 Alpha 检查通过")

return

print(f"\n【步骤 2.1】开始连续处理 {len(remaining_alphas)} 个 Alpha...")

processed_count = len(processed_alpha_ids)  # 从已处理的数量开始

total_count = len(user_alphas)

passed_alphas = []  # 存储检查通过的Alpha

for idx, alpha in enumerate(remaining_alphas, 1):

alpha_id = alpha.get('id', None)

if not alpha_id:

continue

print(f"\n--- 处理第 {processed_count + idx}/{total_count} 个 Alpha: {alpha_id} ---")

# 获取 Alpha 详细信息

print(f"\n【步骤 {2 + processed_count + idx}.1】获取 Alpha {alpha_id} 详细信息...")

alpha_data = client.get_alpha_details(alpha_id)

if not alpha_data:

print(f"❌ 无法获取 Alpha {alpha_id} 信息，跳过...")

continue

# 判断是否是 PPAC Alpha

print(f"\n【步骤 {2 + processed_count + idx}.2】判断 Alpha 类型...")

tags = alpha_data.get('tags', [])

classifications = alpha_data.get('classifications', [])

# 检查是否有 PowerPoolSelected 标签或 POWER_POOL 分类

is_ppac = 'PowerPoolSelected' in tags or any(

c.get('id', '').startswith('POWER_POOL:') for c in classifications

)

if is_ppac:

print(f" 🎯 这是一个 PPAC Alpha")

print(f"\n【步骤 {2 + processed_count + idx}.3】检查 Power Pool 相关性...")

ppc_corr = client.check_power_pool_correlation(alpha_id, verbose=True)

else:

print(f" 📝 这是一个普通 Regular Alpha")

print(f"\n【步骤 {2 + processed_count + idx}.3】检查生产相关性...")

prod_corr = client.check_prod_correlation(alpha_id, verbose=True)

# 检查 Alpha 提交资格

print(f"\n【步骤 {2 + processed_count + idx}.4】检查 Alpha 提交资格...")

submission_check = client.check_alpha_submission(alpha_id, verbose=True)

# 检查提交资格结果，判断是否通过

checks = submission_check.get("is", {}).get("checks", []) if submission_check else []

has_fail = any(check.get('result') == 'FAIL' for check in checks

if check.get('name') != 'REGULAR_SUBMISSION')

if not has_fail and submission_check:

print(f"✅ Alpha {alpha_id} 检查通过，添加到列表中")

# 收集Alpha信息用于输出到Excel

alpha_info = {

'ID': alpha_id,

'Name': alpha_data.get('name', ''),

'Status': alpha_data.get('status', ''),

'Created': alpha_data.get('dateCreated', ''),

'Type': 'PPAC' if is_ppac else 'Regular',

'Sharpe': alpha_data.get('is', {}).get('sharpe', ''),

'Fitness': alpha_data.get('is', {}).get('fitness', ''),

'Returns': alpha_data.get('is', {}).get('returns', ''),

'Tags': ', '.join(tags) if tags else ''

}

passed_alphas.append(alpha_info)

else:

print(f"❌ Alpha {alpha_id} 检查未通过")

# 将当前处理的 Alpha 添加到已处理列表中

processed_alpha_ids.append(alpha_id)

# 保存当前进度

client.save_progress(processed_alpha_ids)

# 在处理完一个Alpha后添加延时，避免触发平台限流

delay_time = 2  # 设置延时2秒

print(f"⏳ 等待 {delay_time} 秒以避免触发平台限流...")

time.sleep(delay_time)

# 自动继续，不需要用户输入

print(f"已处理 {processed_count + idx}/{total_count} 个 Alpha，自动继续...")

print(f"\n✅ 完成！总共处理了 {len(processed_alpha_ids)} 个 Alpha")

# 将检查通过的 Alpha 输出到 Excel

if passed_alphas:

df = pd.DataFrame(passed_alphas)

excel_filename = f"passed_alphas_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"

df.to_excel(excel_filename, index=False)

print(f"\n📊 检查通过的 Alpha 已保存到: {excel_filename}")

print(f"📈 共有 {len(passed_alphas)} 个 Alpha 检查通过")

else:

print(f"\n📈 没有 Alpha 检查通过")

print("\n"+"="*60)

print("测试完成！")

print("="*60)

if __name__ == "__main__":

main()

有什么可以改进的地方，请大佬们多多指教。

---

## 讨论与评论 (1)

### 评论 #1 (作者: MZ45384, 时间: 3个月前)

很好用的代码，我使用了check_prod_correlation部分。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

