# 【Python代码】不限速Check SA代码优化

- **链接**: [Commented] 【Python代码】不限速Check SA代码优化.md
- **作者**: OB53521
- **发布时间/热度**: 11个月前, 得票: 77

## 帖子正文

这个代码在 [WY79548](/hc/en-us/profiles/28867788431255-WY79548) 大佬的代码上加了一些小功能并且改为了py文件，非常感谢 [WY79548](/hc/en-us/profiles/28867788431255-WY79548) 大佬。具体改动：每次check半小时之后等待半小时继续从未完成的sa开始check，如图所示，大概运行了18个小时，每个小时基本稳定在5-7个左右，我放在服务器上运行不太需要担心时间的问题，收到邮件后我再看看具体文件选择交哪个。邮箱功能可以替换为自己习惯使用的通知方式（飞书、钉钉、微信）。

![图片](images/img_073011c436.png)

![图片](images/img_ff25df3677.png)

## 完整代码：

import requests

from datetime import datetime

import os

import json

import traceback

import logging

from time import sleep

import time

import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

```

```

# 设置日志配置

def setup_logging():

"""设置日志配置"""

log_filename = f"SAcheck_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(

level=logging.INFO,

format='%(asctime)s - %(levelname)s - %(message)s',

handlers=[

logging.FileHandler(log_filename, encoding='utf-8'),

logging.StreamHandler()

]

)

return logging.getLogger(__name__)

```

```

# 初始化日志

logger = setup_logging()

```

```

# 邮件发送功能

def send_email(subject, body, to_emails=["你的邮箱地址"]):

"""

发送邮件通知

:param subject: 邮件主题 str

:param body: 邮件正文 str

:param to_emails: 收件人邮箱 list

"""

# 邮件服务器配置

smtp_server = "smtp.qq.com"

smtp_port = 587

smtp_user = "你的邮箱地址" # 发送者邮箱

smtp_password = "你的邮箱授权码" # 授权码

```

```

try:

# 创建MIME消息对象

msg = MIMEMultipart()

msg["From"] = smtp_user

msg["To"] = ", ".join(to_emails)

msg["Subject"] = subject

```

```

# 添加邮件正文

msg.attach(MIMEText(body, "plain"))

```

```

# 连接至SMTP服务器

server = smtplib.SMTP(smtp_server, smtp_port)

server.starttls() # 启动TLS加密

server.login(smtp_user, smtp_password) # 登录SMTP服务器

```

```

# 发送邮件

server.sendmail(smtp_user, to_emails, msg.as_string())

logger.info("邮件发送成功！")

print("📧 邮件通知发送成功！")

```

```

exceptExceptionas e:

logger.error(f"邮件发送失败: {e}")

print(f"📧 邮件发送失败: {e}")

```

```

finally:

try:

server.quit()

except:

pass

```

```

# 时间格式化函数

def format_time(seconds):

"""将秒数转换为 xx小时yy分zz秒 的格式"""

if seconds <0:

return"0秒"

hours = int(seconds // 3600)

minutes = int((seconds % 3600) // 60)

remaining_seconds = int(seconds % 60)

if hours >0:

returnf"{hours}小时{minutes:02d}分{remaining_seconds:02d}秒"

elif minutes >0:

returnf"{minutes}分{remaining_seconds:02d}秒"

else:

returnf"{remaining_seconds}秒"

```

```

def login():

"""登录函数，增加重试机制"""

username = "你的BRAIN邮箱"

password = "你的密码"

max_retries = 3

for attempt inrange(max_retries):

try:

s = requests.Session()

s.auth = (username, password)

response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')

if response.status_codein [200,201]:# 200 OK 或 201 Created 都视为成功

logger.info(f"登录成功，状态码: {response.status_code}")

print(response.content)

return s

else:

logger.warning(f"登录失败，状态码: {response.status_code}")

logger.warning(f"响应内容: {response.text}") # 添加响应内容以便调试

if attempt < max_retries -1:

time.sleep(2 ** attempt) # 指数退避

exceptExceptionas e:

logger.error(f"登录异常 (尝试 {attempt + 1}/{max_retries}): {str(e)}")

if attempt < max_retries -1:

time.sleep(2 ** attempt)

else:

raiseException(f"登录失败，已尝试 {max_retries} 次")

raiseException("登录失败")

```

```

# ## 2.一些函数的定义

```

```

from os import environ

from time import sleep

import time

import json

import pandas as pd

import random

import pickle

from itertools import product

from itertools import combinations

from collections import defaultdict

from urllib.parse import urljoin

import pickle

import requests

import json

from os.path import expanduser

from requests.auth import HTTPBasicAuth

from datetime import datetime, timezone, timedelta

```

```

class RealTimeSaver:

"""实时保存类，用于在处理过程中持续保存数据"""

def__init__(self, filename_prefix="SAcheck_realtime"):

self.filename_prefix= filename_prefix

self.current_time= datetime.now().strftime("%Y%m%d_%H%M%S")

self.save_filename=f"{filename_prefix}_{self.current_time}.txt"

self.progress_filename=f"{filename_prefix}_progress_{self.current_time}.json"

self.initialize_files()

definitialize_files(self):

"""初始化保存文件"""

try:

withopen(self.save_filename,'w', encoding='utf-8') as f:

f.write("Super Alpha实时处理结果\n")

f.write("="*80 + "\n")

f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

f.write("="*80 + "\n\n")

f.write("字段说明:\n")

f.write("[Alpha ID, Sharpe, Turnover, Fitness, Margin, Decay, ProdCorr]\n")

f.write("="*80 + "\n\n")

# 初始化进度文件

progress_data = {

"start_time": datetime.now().isoformat(),

"processed_count":0,

"last_processed_index":-1,

"total_count":0,

"errors": []

}

withopen(self.progress_filename,'w', encoding='utf-8') as f:

json.dump(progress_data, f, indent=2, ensure_ascii=False)

logger.info(f"实时保存文件初始化完成: {self.save_filename}")

logger.info(f"进度文件初始化完成: {self.progress_filename}")

exceptExceptionas e:

logger.error(f"初始化保存文件失败: {str(e)}")

raise

defsave_alpha_result(self, alpha_data, index, total_count):

"""保存单个alpha的处理结果"""

try:

withopen(self.save_filename,'a', encoding='utf-8') as f:

f.write(f"{index + 1:3d}. {alpha_data}\n")

iflen(alpha_data) >=7and alpha_data[6] isnotNone:

prod_corr = alpha_data[6]

if prod_corr <=0.7:

f.write(" ✅ prod correlation ≤ 0.7 (推荐)\n")

else:

f.write(" ⚠️ prod correlation > 0.7\n")

f.write("\n")

# 更新进度

self.update_progress(index, total_count)

logger.info(f"已保存第 {index + 1} 个alpha结果: {alpha_data[0] if alpha_data else 'Unknown'}")

exceptExceptionas e:

logger.error(f"保存alpha结果失败 (index: {index}): {str(e)}")

defupdate_progress(self, processed_index, total_count, error_msg=None):

"""更新处理进度"""

try:

withopen(self.progress_filename,'r', encoding='utf-8') as f:

progress_data = json.load(f)

progress_data["processed_count"] = processed_index + 1

progress_data["last_processed_index"] = processed_index

progress_data["total_count"] = total_count

progress_data["last_update"] = datetime.now().isoformat()

if error_msg:

progress_data["errors"].append({

"index": processed_index,

"error": error_msg,

"timestamp": datetime.now().isoformat()

})

withopen(self.progress_filename,'w', encoding='utf-8') as f:

json.dump(progress_data, f, indent=2, ensure_ascii=False)

exceptExceptionas e:

logger.error(f"更新进度失败: {str(e)}")

defsave_error(self, error_msg, context=""):

"""保存错误信息"""

try:

withopen(self.save_filename,'a', encoding='utf-8') as f:

f.write(f"\n❌ 错误: {error_msg}\n")

if context:

f.write(f" 上下文: {context}\n")

f.write(f" 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

logger.error(f"错误已保存到文件: {error_msg}")

exceptExceptionas e:

logger.error(f"保存错误信息失败: {str(e)}")

deffinalize_save(self, final_data):

"""最终保存完整结果"""

try:

withopen(self.save_filename,'a', encoding='utf-8') as f:

f.write("\n" + "="*80 + "\n")

f.write("最终排序结果\n")

f.write("="*80 + "\n\n")

prod_under_07_found = False

for i, item inenumerate(final_data,1):

f.write(f"{i:3d}. {item}\n")

iflen(item) >=7and item[6] isnotNone:

prod_corr = item[6]

if prod_corr >0.7andnot prod_under_07_found:

f.write(" " + "-"*60 + "\n")

f.write(" 以上Alpha的prod correlation > 0.7\n")

f.write(" " + "-"*60 + "\n")

prod_under_07_found = True

f.write(f"\n处理完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

f.write(f"总共处理: {len(final_data)} 个Alpha\n")

logger.info(f"最终结果已保存完成")

exceptExceptionas e:

logger.error(f"最终保存失败: {str(e)}")

```

```

def get_latest_monday(tz=None):

"""获取最近的周一日期"""

try:

if tz isNone:

tz = timezone(timedelta(hours=-4))

now = datetime.now(tz)

days_since_monday = now.weekday()

monday = now - timedelta(days=days_since_monday)

monday_start = monday.replace(hour=0, minute=0, second=0, microsecond=0)

return monday_start.isoformat(timespec='minutes')

exceptExceptionas e:

logger.error(f"获取周一日期失败: {str(e)}")

raise

```

```

reverse_super_alpha_list = []

```

```

def super_score(rec):

"""计算super_alpha得分的函数，增加异常处理"""

try:

# 一个粗略计算super_alpha得分的函数,权重可调整

sharpe = rec[1]**3 if len(rec) > 1 and rec[1] is not None else 0

turnover = rec[2] if len(rec) > 2 and rec[2] is not None else 0

fitness = rec[3]**3 if len(rec) > 3 and rec[3] is not None else 0

margin = rec[4] if len(rec) > 4 and rec[4] is not None else 0

iflen(rec) <=5or rec[5] isNone:

pc = 9999999

else:

pc = rec[6] * 1000000 if len(rec) > 6 and rec[6] is not None else 0

return sharpe * (1- turnover) * fitness * margin - pc

exceptExceptionas e:

logger.error(f"计算super_score失败: {str(e)}, rec: {rec}")

return0

```

```

def check_prod(alpha_bag, start, saver=None):

"""检查prod correlation，添加30分钟工作+30分钟休息的智能时间控制"""

from datetime import datetime, timedelta

current_start = start

work_duration = 30 # 工作30分钟

rest_duration = 30 # 休息30分钟

while current_start <len(alpha_bag):

try:

s = login()

work_start_time = datetime.now()

logger.info(f"开始新的30分钟工作周期，从索引 {current_start} 开始，总共 {len(alpha_bag)} 个alpha")

print(f"\n🚀 开始新的30分钟工作周期，从索引 {current_start} 开始")

print(f"⏰ 工作开始时间: {work_start_time.strftime('%H:%M:%S')}")

# 记录工作周期开始到实时文件

if saver:

try:

withopen(saver.save_filename,'a', encoding='utf-8') as f:

f.write(f"\n🚀 工作周期开始 - {work_start_time.strftime('%H:%M:%S')}\n")

f.write(f" 从索引 {current_start} 开始，目标: 30分钟工作周期\n")

f.write("="*60 + "\n\n")

exceptExceptionas save_error:

logger.error(f"保存工作周期开始信息失败: {str(save_error)}")

# ✅ 完全保持原有逻辑，但加入时间检查

for idx, i inenumerate(alpha_bag):

if idx < current_start:

continue

# 🚨 关键修复：在开始处理每个alpha之前检查时间

current_time = datetime.now()

elapsed_time = current_time - work_start_time

if elapsed_time.total_seconds() > work_duration *60:

# 🚨 关键修复：立即设置索引，避免异常时索引丢失

current_start = idx # 优先设置索引，确保即使异常也不会丢失

logger.info(f"工作时间已达到30分钟，准备处理索引 {idx} 时发现时间到了")

print(f"\n⏰ 工作时间已达到30分钟，准备处理索引 {idx} 时发现时间到了")

print(f"💤 程序将休息30分钟，避免API限速...")

print(f"📍 下次将从索引 {idx} (Alpha ID: {i[0]}) 重新开始")

# 保存工作周期信息到实时文件

if saver:

try:

withopen(saver.save_filename,'a', encoding='utf-8') as f:

f.write(f"\n⏰ 工作周期结束 - {datetime.now().strftime('%H:%M:%S')}\n")

f.write(f" 已工作30分钟，下次从索引 {idx} (Alpha ID: {i[0]}) 开始\n")

f.write(f" 开始30分钟休息...\n")

f.write("="*60 + "\n\n")

exceptExceptionas save_error:

logger.error(f"保存工作周期信息失败: {str(save_error)}")

# 休息30分钟

rest_start_time = datetime.now()

rest_end_time = rest_start_time + timedelta(minutes=rest_duration)

logger.info(f"开始休息30分钟，下次从索引 {idx} 开始，休息时间: {rest_start_time.strftime('%H:%M:%S')} - {rest_end_time.strftime('%H:%M:%S')}")

print(f"💤 休息开始: {rest_start_time.strftime('%H:%M:%S')}")

print(f"💤 休息结束: {rest_end_time.strftime('%H:%M:%S')}")

# 发送工作周期完成邮件

try:

work_elapsed_time = (rest_start_time - work_start_time).total_seconds()

overall_progress = ((idx / len(alpha_bag)) * 100) if len(alpha_bag) > 0 else 0

cycle_email_subject = f"[SA检查] 工作周期完成 - 第{idx//30 + 1}轮"

cycle_email_body = (

f"时间: {rest_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"

f"🎯 Super Alpha工作周期完成！\n\n"

f"--- 本周期统计 ---\n"

f"工作时长: {format_time(work_elapsed_time)}\n"

f"处理到索引: {idx}\n"

f"当前Alpha: {i[0] if i else'Unknown'}\n\n"

f"--- 总体进度 ---\n"

f"已检查: {idx}/{len(alpha_bag)} ({overall_progress:.2f}%)\n"

f"下次从索引 {idx} 继续\n\n"

f"💤 现在开始30分钟休息...\n"

f"预计休息结束: {rest_end_time.strftime('%H:%M:%S')}"

)

send_email(cycle_email_subject, cycle_email_body)

exceptExceptionas email_error:

logger.error(f"发送工作周期邮件失败: {str(email_error)}")

# 显示倒计时（每5分钟显示一次）

for minute inrange(rest_duration):

time.sleep(60) # 等待1分钟

remaining = rest_duration - minute - 1

if remaining %5==0and remaining >0:

print(f"💤 还需休息 {remaining} 分钟...")

elif remaining ==0:

print("🚀 休息结束，准备继续工作...")

# 索引已经在休息前设置了，这里只是确认

logger.info(f"休息结束，从索引 {current_start} (Alpha ID: {alpha_bag[current_start][0]}) 继续")

break# 跳出内层循环，开始新的工作周期

# 显示进度信息

if idx %100==0:

print(f"📊 进度: {idx}/{len(alpha_bag)} ({idx/len(alpha_bag)*100:.1f}%)")

elapsed_minutes = elapsed_time.total_seconds() / 60

remaining_minutes = work_duration - elapsed_minutes

print(f"⏰ 本轮工作已进行: {elapsed_minutes:.1f}分钟, 剩余: {remaining_minutes:.1f}分钟")

if idx %200==0& idx !=0:

s = login()

# 🚨 关键：原有的核心处理逻辑在时间检查之后

print(f"🔄 开始处理 Alpha {idx}: {i[0]}")

pc = get_check_prod(s, i[0]) # 这里可能会花很长时间

i.append(pc)

alpha_bag[idx] = i

print(i)

print(f"✅ 完成处理 Alpha {idx}: {i[0]}")

print(f"Processed {idx} alphas")

# 只添加实时保存，不改变原有流程

if saver:

try:

saver.save_alpha_result(i, idx, len(alpha_bag))

# 优化日志频率：每10个alpha记录一次保存日志

if (idx +1) %10==0:

logger.info(f"已保存第 {idx + 1} 个alpha结果: {i[0]}")

exceptExceptionas save_error:

logger.error(f"保存alpha结果失败: {str(save_error)}")

else:

# 如果正常完成所有alpha的处理

logger.info("所有alpha处理完成")

print("\n🎉 所有alpha处理完成！")

break

exceptKeyboardInterrupt:

logger.info("用户手动中断了处理过程")

print("\n⌨️ 用户手动中断了处理过程")

if saver:

saver.save_error("用户手动中断", f"在索引 {idx if 'idx' in locals() else current_start} 处中断")

raise

exceptExceptionas e:

error_msg = f"check_prod函数出现错误: {str(e)}\n{traceback.format_exc()}"

logger.error(error_msg)

print(f"❌ 处理出错: {str(e)}")

# 🚨 关键修复：保存当前应该继续的索引

if'idx'inlocals():

# 如果错误发生在处理某个alpha时，下次从这个alpha继续

current_start = idx

error_context = f"在处理索引 {idx} 时出错"

print(f"📍 下次将从索引 {idx} 继续处理")

logger.info(f"出错索引: {idx}，下次从此索引继续")

else:

# 如果错误发生在其他地方，保持当前的current_start

error_context = f"在索引 {current_start} 附近出错"

print(f"📍 下次将从索引 {current_start} 继续处理")

logger.info(f"保持当前索引: {current_start}")

if saver:

saver.save_error(error_msg, error_context)

# 出错时也休息一下，然后继续

print("💤 出错了，休息5分钟后继续...")

logger.info(f"出错休息5分钟，下次从索引 {current_start} 开始")

time.sleep(300) # 休息5分钟

continue

```

```

def get_check_prod(s, alpha_id):

"""获取prod correlation，完全保持原有逻辑，优化日志频率"""

# 添加静态变量来跟踪日志记录时间

ifnothasattr(get_check_prod,'last_wait_log_time'):

get_check_prod.last_wait_log_time = 0

ifnothasattr(get_check_prod,'wait_count'):

get_check_prod.wait_count = 0

whileTrue:

result = s.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod](https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod) ")

if"retry-after"in result.headers:

sleep_time = float(result.headers["Retry-After"])

# 优化日志记录频率：每60秒记录一次，或者是第一次

current_time = time.time()

get_check_prod.wait_count += 1

if (current_time - get_check_prod.last_wait_log_time>60) or get_check_prod.wait_count==1:

logger.info(f"Alpha {alpha_id} 服务器要求等待 {sleep_time} 秒 (等待次数: {get_check_prod.wait_count})")

get_check_prod.last_wait_log_time = current_time

time.sleep(sleep_time)

elif result.status_code==429:

print("Rate limit exceeded, sleeping for 60 seconds")

logger.warning(f"Alpha {alpha_id} 速率限制，等待60秒")

time.sleep(60)

continue

else:

try:

r = result.json()

print({alpha_id: r['max']})

logger.info(f"Alpha {alpha_id} prod correlation: {r['max']}")

# 重置等待计数器，因为成功获取到结果了

get_check_prod.wait_count = 0

return r['max']

exceptExceptionas e:

print(f"Error for alpha_id: {alpha_id}, {e}")

logger.error(f"处理alpha {alpha_id} 时出错: {str(e)}")

return

```

```

def score(rec):

"""计算alpha得分的函数，增加异常处理"""

try:

# 一个粗略计算alpha得分的函数,权重可调整

sharpe = rec[1] * 5 if len(rec) > 1 and rec[1] is not None else 0

turnover = rec[2] if len(rec) > 2 and rec[2] is not None else 0

fitness = rec[3] * 5 if len(rec) > 3 and rec[3] is not None else 0

margin = rec[4] * 2 if len(rec) > 4 and rec[4] is not None else 0

return sharpe * (1- turnover) * fitness * margin

exceptExceptionas e:

logger.error(f"计算score失败: {str(e)}, rec: {rec}")

return0

```

```

def verfiy_result(res):

"""验证结果，增加异常处理"""

try:

ifnot res or'is'notin res or'checks'notin res['is']:

logger.warning(f"结果格式异常: {res}")

returnFalse

checks = res['is']['checks']

flag = True

for check in checks:

if check['result'] in ['FAIL','ERROR']:

flag = False

if check['name'] =="LOW_SHARPE":

reverse_super_alpha_list.append([

res.get('id', 'Unknown'),

res['is'].get('sharpe', 0),

res['is'].get('fitness', 0),

res['is'].get('margin', 0)

])

logger.info(f"IS检查失败: {res.get('id', 'Unknown')}, {check['name']}, {check['result']}")

print("IS failed:", res.get('id','Unknown'), check['name'], check['result'])

break

return flag

exceptExceptionas e:

logger.error(f"验证结果时出现错误: {str(e)}, res: {res}")

returnFalse

```

```

def sus(start, end, sharpe_th, fitness_th, alpha_num, usage, saver=None):

"""搜索alpha，增加异常处理和实时保存"""

max_retries = 3

s = None

output = []

count = 0

try:

s = login()

logger.info(f"开始搜索alpha，时间范围: {start} 到 {end}")

logger.info(f"筛选条件: sharpe > {sharpe_th}, fitness > {fitness_th}, 最大数量: {alpha_num}")

for i inrange(0, alpha_num,100):

retry_count = 0

success = False

while retry_count < max_retries andnot success:

try:

logger.info(f"处理批次: {i}-{i+100}")

url_e = (" [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d) " % i +

"&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E="+ start +

"&dateCreated%3C"+ end +

"&is.fitness%3E"+str(fitness_th) +"&is.sharpe%3E"+

str(sharpe_th) +"&order=-is.sharpe&hidden=false&type=SUPER")

url_c = (" [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d) " % i +

"&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E="+ start +

"&dateCreated%3C"+ end +

"&is.fitness%3C-"+str(fitness_th) +"&is.sharpe%3C-"+

str(sharpe_th) +"&order=is.sharpe&hidden=false&type=SUPER")

urls = [url_e]

if usage !="submit":

urls.append(url_c)

for url in urls:

try:

response = s.get(url)

response.raise_for_status() # 抛出HTTP错误

alpha_list = response.json().get("results", [])

for j, alpha_data inenumerate(alpha_list):

try:

ifnotverfiy_result(alpha_data):

continue

alpha_id = alpha_data.get("id", "Unknown")

name = alpha_data.get("name", "")

dateCreated = alpha_data.get("dateCreated", "")

is_data = alpha_data.get("is", {})

sharpe = is_data.get("sharpe", 0)

fitness = is_data.get("fitness", 0)

turnover = is_data.get("turnover", 0)

margin = is_data.get("margin", 0)

longCount = is_data.get("longCount", 0)

shortCount = is_data.get("shortCount", 0)

settings = alpha_data.get("settings", {})

decay = settings.get("decay", 0)

count += 1

if (longCount + shortCount) >100:

rec = [alpha_id, sharpe, turnover, fitness, margin, decay]

print(rec)

# 根据turnover计算penalty

if turnover >0.7:

rec.append(decay * 4)

elif turnover >0.6:

rec.append(decay * 3 + 3)

elif turnover >0.5:

rec.append(decay * 3)

elif turnover >0.4:

rec.append(decay * 2)

elif turnover >0.35:

rec.append(decay + 4)

elif turnover >0.3:

rec.append(decay + 2)

output.append(rec)

# 实时保存初步结果

if saver:

saver.save_alpha_result(rec, len(output) - 1, alpha_num)

exceptExceptionas e:

logger.error(f"处理单个alpha数据失败: {str(e)}")

continue

except requests.exceptions.RequestExceptionas e:

logger.error(f"请求URL失败: {url}, 错误: {str(e)}")

raise

exceptExceptionas e:

logger.error(f"处理URL响应失败: {url}, 错误: {str(e)}")

raise

success = True

exceptExceptionas e:

retry_count += 1

error_msg = f"批次 {i} 处理失败 (尝试 {retry_count}/{max_retries}): {str(e)}"

logger.error(error_msg)

if saver:

saver.save_error(error_msg, f"批次: {i}")

if retry_count < max_retries:

sleep_time = 2 ** retry_count

logger.info(f"等待 {sleep_time} 秒后重试...")

time.sleep(sleep_time)

# 重新登录

try:

s = login()

except:

pass

else:

logger.error(f"批次 {i} 处理失败，跳过")

logger.info(f"搜索完成，总共找到 {count} 个alpha，筛选出 {len(output)} 个")

print("count: %d"% count)

# 按score排序

output.sort(key=score, reverse=True)

return output

exceptExceptionas e:

error_msg = f"sus函数出现严重错误: {str(e)}\n{traceback.format_exc()}"

logger.error(error_msg)

if saver:

saver.save_error(error_msg)

raise

```

```

# ## 3.筛选本周super alpha

#

# - 通过datatime函数 获取本周开始时间与现在时间作为alpha筛选范围(每周不同alpha副本)

# - 便于修改的筛选条件

# - 自动过滤IS failed alpha 并给出failed:原因

# - 对于shapre,fitness绝对值大小符合筛选条件,符号为负的alpha,单独列出,以待修改

#

```

```

# In[3]:

```

```

try:

tz_ny = timezone(timedelta(hours=-4))

# start = get_latest_monday(tz_ny)

start = "2025-7-22T00:00-04:00"

end = datetime.now(tz_ny).isoformat(timespec='minutes')

```

```

print(f"开始时间(默认本周一开始时间): {start}")

print(f"结束时间: {end}")

logger.info(f"设置时间范围: {start} 到 {end}")

except Exception as e:

logger.error(f"设置时间范围失败: {str(e)}")

raise

```

```

# In[4]:

```

```

# 创建实时保存器

saver = RealTimeSaver("SAcheck_super_list")

```

```

try:

'''

起始时间 结束时间 shapre fitness

对于开始时间想要细调,也可以换成

super_list=sus("2025-06-17T06:06-04:00",end,5,5,300, "track")

这样的形式 来细调

避免反复check 某些alpha的prod corr

'''

super_list = sus(start, end, 4, 3, 300, "track", saver)

logger.info(f"成功获取 {len(super_list)} 个super alpha")

print(f"成功获取 {len(super_list)} 个super alpha")

# 保存初步结果

saver.finalize_save(super_list)

except Exception as e:

error_msg = f"获取super_list失败: {str(e)}\n{traceback.format_exc()}"

logger.error(error_msg)

saver.save_error(error_msg)

super_list = [] # 确保变量存在

```

```

# In[5]:

```

```

try:

print("反向super alpha列表:")

for i in reverse_super_alpha_list:

print(i)

logger.info(f"反向super alpha: {i}")

except Exception as e:

logger.error(f"打印反向super alpha列表失败: {str(e)}")

```

```

# ## 4.对筛选出的alpha进行prod corr检查

#

# - 修改保存在输入的super_list全局变量中,**支持断点继续**

#

# - 对于none prod corr再获取

```

```

# In[ ]:

```

```

if super_list:

# 创建专门用于prod检查的保存器

prod_saver = RealTimeSaver("SAcheck_prod_check")

try:

# 最后一个参数为开始位置，可断点继续

check_prod(super_list,0, prod_saver)

logger.info("prod correlation检查完成")

exceptExceptionas e:

error_msg = f"prod correlation检查失败: {str(e)}\n{traceback.format_exc()}"

logger.error(error_msg)

prod_saver.save_error(error_msg)

else:

logger.warning("super_list为空，跳过prod correlation检查")

```

```

# In[ ]:

```

```

try:

cnt_not_none = 0

cnt_len = 0

cccnt = 0

jishu = []

none_list = []

for i in super_list:

cccnt += 1

iflen(i) >=7:

cnt_len += 1

if i[6] isnotNone:

cnt_not_none += 1

else:

jishu.append(cccnt - 1)

none_list.append(i)

else:

jishu.append(cccnt - 1)

none_list.append(i)

print(f"Total alphas with length >= 7: {cnt_len}, Alphas with non-None prod check: {cnt_not_none}")

logger.info(f"统计: 长度>=7的alpha: {cnt_len}, 有prod检查结果的: {cnt_not_none}, 需要重新检查的: {len(none_list)}")

except Exception as e:

logger.error(f"统计prod检查结果失败: {str(e)}")

none_list = []

jishu = []

```

```

# In[ ]:

```

```

if none_list:

# 为需要重新检查的alpha创建保存器

retry_saver = RealTimeSaver("SAcheck_retry_prod")

try:

result_bag = check_prod(none_list, 0, retry_saver)

logger.info(f"重新检查完成，处理了 {len(none_list)} 个alpha")

exceptExceptionas e:

error_msg = f"重新检查prod correlation失败: {str(e)}\n{traceback.format_exc()}"

logger.error(error_msg)

retry_saver.save_error(error_msg)

```

```

# In[ ]:

```

```

try:

for i inrange(len(none_list)):

print(f"none_list[{i}]: {none_list[i][0]},super_list[{jishu[i]}]: {super_list[jishu[i]][0]}")

if none_list[i][0] == super_list[jishu[i]][0]:

iflen(none_list[i]) >=8:

none_list[i][6] = none_list[i][7]

super_list[jishu[i]] = none_list[i]

print("None list更新完成:")

for item in none_list:

print(item)

logger.info("none_list数据合并到super_list完成")

except Exception as e:

logger.error(f"合并none_list数据失败: {str(e)}")

```

```

# ## 5.排序输出

#

```

```

# In[ ]:

```

```

try:

super_list.sort(key=super_score, reverse=True)

logger.info(f"按super_score排序完成，共 {len(super_list)} 个alpha")

print("排序后的super_list:")

for i, item inenumerate(super_list):

print(f"{i +1}. {item}")

except Exception as e:

logger.error(f"排序失败: {str(e)}")

```

```

# In[ ]:

```

```

try:

flag = True

for item in super_list:

print(item)

iflen(item) >=7and item[6] isnotNoneand item[6] >0.7and flag:

flag = False

print("-------------------除了正上方那一个以上均为prod<0.7------------------------")

```

```

# 保存最终结果到文件

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

filename = f"SA-{current_time}.txt"

```

```

withopen(filename,'w', encoding='utf-8') as f:

f.write("Super Alpha筛选结果\n")

f.write("="*80 + "\n")

f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

f.write(f"总数量: {len(super_list)}\n")

f.write("="*80 + "\n\n")

f.write("字段说明:\n")

f.write("[Alpha ID, Sharpe, Turnover, Fitness, Margin, Decay, ProdCorr]\n")

f.write("=" * 80 + "\n\n")

if super_list:

prod_under_07_found = False

for i, item inenumerate(super_list,1):

# 检查是否有prod correlation数据

iflen(item) >=7and item[6] isnotNone:

prod_corr = item[6]

f.write(f"{i:3d}. {item}\n")

# 标记prod correlation > 0.7的分界线

if prod_corr >0.7andnot prod_under_07_found:

f.write(" " + "-"*60 + "\n")

f.write(" 以上Alpha的prod correlation > 0.7 (建议优先考虑)\n")

f.write(" " + "-"*60 + "\n")

prod_under_07_found = True

else:

f.write(f"{i:3d}. {item} [prod correlation未检查]\n")

else:

f.write("没有找到符合条件的Super Alpha\n")

f.write("\n" + "="*80 + "\n")

f.write("注意事项:\n")

f.write("1. prod correlation < 0.7 的alpha通常更容易通过审核\n")

f.write("2. 建议优先选择prod correlation较低的alpha进行提交\n")

f.write("3. 如需提交，请将选中的Alpha ID复制到相应的提交脚本中\n")

f.write("\n处理过程中的错误和异常都已记录在日志文件中\n")

f.write(f"日志文件: SAcheck_log_{datetime.now().strftime('%Y%m%d')}_*.log\n")

```

```

print(f"\n✅ Super Alpha筛选结果已保存到文件: {filename}")

logger.info(f"最终结果已保存到文件: {filename}")

# 创建总结报告

summary_filename = f"SAcheck_summary_{current_time}.txt"

withopen(summary_filename,'w', encoding='utf-8') as f:

f.write("SAcheck处理总结报告\n")

f.write("="*50 + "\n")

f.write(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

f.write(f"处理结果: 成功筛选出 {len(super_list)} 个Super Alpha\n")

# 统计prod correlation情况

has_prod = sum(1 for item in super_list if len(item) >= 7 and item[6] is not None)

low_prod = sum(1 for item in super_list if len(item) >= 7 and item[6] is not None and item[6] <= 0.7)

f.write(f"有prod correlation数据: {has_prod}\n")

f.write(f"prod correlation ≤ 0.7: {low_prod}\n")

f.write("="*50 + "\n")

print(f"✅ 处理总结已保存到文件: {summary_filename}")

logger.info("处理完成，所有结果已保存")

# 发送最终完成邮件

try:

final_email_subject = f"🎉 [SA检查] 全部完成 - {len(super_list)}个Super Alpha"

final_email_body = (

f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

f"🎉 恭喜！Super Alpha检查任务已全部完成！\n\n"

f"--- 最终统计 ---\n"

f"总Alpha数量: {len(super_list)} 个\n"

f"有prod correlation数据: {has_prod} 个\n"

f"prod correlation ≤ 0.7: {low_prod} 个 (推荐)\n"

f"prod correlation > 0.7: {has_prod - low_prod} 个\n\n"

f"--- 文件生成 ---\n"

f"最终结果文件: {filename}\n"

f"处理总结文件: {summary_filename}\n\n"

f"📋 推荐的Super Alpha (prod ≤ 0.7):\n"

)

# 添加前10个推荐的Super Alpha

recommended_count = 0

for i, item inenumerate(super_list[:50]):# 检查前50个

iflen(item) >=7and item[6] isnotNoneand item[6] <=0.7:

recommended_count += 1

if recommended_count <=10:

alpha_id = item[0]

sharpe = item[1] if len(item) > 1 else 'N/A'

prod_corr = item[6]

final_email_body += f" {recommended_count:2d}. {alpha_id} (sharpe: {sharpe}, prod: {prod_corr})\n"

if low_prod >10:

final_email_body += f" ... 还有 {low_prod - 10} 个推荐Alpha\n"

if low_prod ==0:

final_email_body += " 暂无prod correlation ≤ 0.7的Alpha\n"

final_email_body += f"\n📝 完整列表请查看文件: {filename}"

send_email(final_email_subject, final_email_body)

exceptExceptionas email_error:

logger.error(f"发送最终完成邮件失败: {str(email_error)}")

except Exception as e:

error_msg = f"保存最终结果失败: {str(e)}\n{traceback.format_exc()}"

logger.error(error_msg)

print(f"❌ 保存文件时出错: {e}")

# 即使出错也发送邮件通知

try:

error_email_subject = f"❌ [SA检查] 处理出错"

error_email_body = (

f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

f"❌ Super Alpha检查过程中出现错误！\n\n"

f"错误信息: {str(e)}\n\n"

f"已处理数量: {len(super_list) if'super_list'inlocals() else0} 个\n"

f"请检查日志文件获取详细信息。"

)

send_email(error_email_subject, error_email_body)

exceptExceptionas email_error:

logger.error(f"发送错误邮件失败: {str(email_error)}")

```

```

print("\n🎉 SAcheck处理完成！")

print("📁 生成的文件包括:")

print(" - 实时保存的处理结果")

print(" - 进度跟踪文件")

print(" - 最终排序结果")

print(" - 详细的日志文件")

print(" - 处理总结报告")

print("📧 邮件通知已发送完成情况")

---

## 讨论与评论 (13)

### 评论 #1 (作者: YB49779, 时间: 11个月前)

感谢大佬的分享！我有一个小问题就是这个代码是否可以进行修改实现ra的check呢？谢谢大佬！

==============================================================================================================================================================================================================================================================================================================================================

---

### 评论 #2 (作者: HW93328, 时间: 11个月前)

感谢大佬的分享！因为有prod check限流的问题，每次手动check都只能分批进行，非常麻烦，这个代码非常好的解决了这一问题，谢谢大佬，之后看看能否在这一代码的基础上对ra也实现这个功能，感谢大佬分享！

================================================================================================================================================================================

---

### 评论 #3 (作者: OB53521, 时间: 11个月前)

[YB49779](/hc/en-us/profiles/26716038151319-YB49779)  理论上是可以的。有段代码我已经在尝试使用了，但不知道是不是我最近的alpha太烂了，暂时还没有check出来可以提交的，也有可能是代码的原因，总之还在调整中，确认没有问题后会发帖子。

---

### 评论 #4 (作者: YH25030, 时间: 11个月前)

感谢您的宝贵分享。我最近也做SAcheckd的代码。跟您的代码对比，感觉自己的代码真是不忍直视。这个代码做一下修改，估计可以用来check RA的prod。我准备深挖下去看看。

---

### 评论 #5 (作者: OB53521, 时间: 10个月前)

[YH25030](/hc/en-us/profiles/28941108652823-YH25030)  过奖了，只是站在巨人的肩膀上，同时期待你的RAcheck代码分享！

---

### 评论 #6 (作者: LL88284, 时间: 10个月前)

感谢大佬的分享！，请问有没有完整代码文件可供下载的，git或者其他云盘

---

### 评论 #7 (作者: BW16434, 时间: 10个月前)

感谢大佬的分享，从中吸收到很多东西，慢慢消化下，在调整为自己适合的代码，谢谢。

---

### 评论 #8 (作者: TB73554, 时间: 8个月前)

感谢大佬的分享，最近开始做SA，这个check真的是帮了我大忙。参考大佬您的代码，我做了一些小小的修改，增加了通过的super alpha颜色设置功能，这样方便不看邮件时在平台上就可以看到可提交的SA，希望能够继续优化，产出优质的SA，感谢大佬！

---

### 评论 #9 (作者: KJ35210, 时间: 8个月前)

尽管还没足够数量组SA，但相信博主和大家的选择，感谢分享

---

### 评论 #10 (作者: GY62435, 时间: 8个月前)

大佬，这个直接用jupyter notebook运行就行吗

---

### 评论 #11 (作者: YQ51506, 时间: 8个月前)

这个代码在WY79548大佬的基础上增加了半小时轮询机制和邮件通知功能，从技术实现角度看确实很实用。不过作为量化研究员，我更关注的是这个check SA的具体应用场景和量化价值。代码中使用了requests库进行API调用，加入了指数退避的重试机制，这些在量化数据获取中都是很常见的处理方式。在WorldQuant Brain平台上，我们通常使用operator来构建alpha因子进行回测，这种定时检查的工具更多是辅助性的技术实现。邮件通知功能可以替换为其他通知方式的设计很灵活，但建议在异常处理方面可以更完善一些。

---

### 评论 #12 (作者: DH50144, 时间: 5个月前)

跑出来的alpha ID怎样在平台中那么多的ID早出来呢？平台中也不会显示alpha ID ![图片](images/img_b63e32ce17.png)

---

### 评论 #13 (作者: SZ50491, 时间: 2个月前)

感谢分享，已经run起来了，之前都是自己一个个的在网页上点击操作，等待的时间好漫长。

但是奈何自己的代码能力有限，在论坛上也找了一些，但是都没能跑起来，好在发现了这篇。

本来想自己改一下，不发送邮件，可惜改了之后，报错。更别提给alpha加颜色了，后续慢慢努力学习吧。

再次感谢！

---

