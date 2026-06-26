# 【Community Leader - 因子回测】稳定多功能回测脚本分享——基于wqb以及wqb_app实现的回测脚本代码优化

- **链接**: [Commented] 【Community Leader - 因子回测】稳定多功能回测脚本分享基于wqb以及wqb_app实现的回测脚本代码优化.md
- **作者**: JX39934
- **发布时间/热度**: 6个月前, 得票: 42

## 帖子正文

背景:之前一直用wqb_app里面的回测脚本来回测，发现还是有很多不方便的地方，比如日志回显这些不完整，在登录和回测时也有些许不便利，所以我就自己通过gemini 3 pro模型改进了一个版本出来，依赖于wqb的Python包。

主要有以下功能：
1、自动读取脚本目录下的user_info.txt和wqb_app生成的表达式配置文件expressions_with_settings.json

2、可以自由选择single或者multi回测，以及每个线程里面的alpha数量

3、增加了一段时间反回回测状态的日志，方便查看是否卡死

4、增加每小时汇报总进度的日志

5、如果中途断开，可以根据之前断开的前缀编号继续回测

![图片](images/img_348599baa6.png)

6、自动打tag和改名（可开局自定义）

7、邮件提醒+邮件日报

8、回测失败会回显失败的表达式日志（方便查看是否因为表达式问题导致回测失败，在mult回测中很有用，因为mult回测里面只要有一个回测有问题，整个进程就都失败）

以下直接把脚本贴出来

import asyncio
import json
import os
import re
import time
import logging
import random
import smtplib
import traceback
import argparse  # <--- 【新增 1/2】引入 argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import wqb    #需要用到wqb的包

# --- 邮件配置 (请修改此处) ---
MAIL_HOST = "smtp.qq.com"    #这里因为我用的是qq邮箱，如果你也用qq邮箱就不用改
MAIL_PORT = 465    #SMTP端口号
MAIL_USER = " [XXXXXXX@qq.com](mailto:XXXXXXX@qq.com) "   # 发件人邮箱
MAIL_PASS = "XXXXXXXXX"      # 授权码
MAIL_RECEIVER = " [XXXXXXXX@qq.com](mailto:XXXXXXXX@qq.com) "  # 收件人邮箱
# ---------------------------

# 脚本标识，可自定义
SCRIPT_LABEL = "Master"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("simulation_task.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 全局统计变量
STATS = {
    "total": 0,
    "completed": 0,
    "success": 0,
    "failed": 0,
    "start_time": 0,
    "name_tag": "Unknown" # 用于邮件中显示当前任务标签
}

def load_credentials(filename="user_info.txt"):
    """从文件中读取账号密码"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则提取带引号的内容
        user_match = re.search(r"username:\s*'(.+?)'", content)
        pass_match = re.search(r"password:\s*'(.+?)'", content)

        if user_match and pass_match:
            return user_match.group(1), pass_match.group(1)
        else:
            raise ValueError("格式不匹配，请确保格式为 username: 'XXX' password: 'XXX'")
    except FileNotFoundError:
        logger.error(f"未找到 {filename} 文件")
        return None, None
    except Exception as e:
        logger.error(f"读取凭证失败: {e}")
        return None, None

def get_json_filepath():
    """直接加载当前目录下的默认JSON文件"""
    path = "expressions_with_settings.json"
    print(f"📂 正在读取默认文件: {path}")

    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"JSON加载失败: {e}")
            return None
    else:
        logger.error(f"文件不存在: {path}")
        return None

def extract_expression_codes(payload):
    """
    从提交的 payload 中提取表达式代码。
    支持 Single 和 Multi 结构。
    """
    codes = []
    try:
        # 1. 检查是否是 Multi 模式的列表结构
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    # 尝试提取 code
                    if 'code' in item: 
                        codes.append(item['code'])
                    elif 'regular' in item:
                        # 修复：支持 regular 直接是字符串的情况
                        if isinstance(item['regular'], str): codes.append(item['regular'])
                        elif isinstance(item['regular'], dict) and 'code' in item['regular']: codes.append(item['regular']['code'])
                    elif 'vector' in item:
                        if isinstance(item['vector'], str): codes.append(item['vector'])
                        elif isinstance(item['vector'], dict) and 'code' in item['vector']: codes.append(item['vector']['code'])

        # 2. 检查是否是 Single 模式的字典结构
        elif isinstance(payload, dict):
            if 'code' in payload: 
                codes.append(payload['code'])

            # 修复：支持 regular 直接是字符串的情况
            elif 'regular' in payload:
                if isinstance(payload['regular'], str): codes.append(payload['regular'])
                elif isinstance(payload['regular'], dict) and 'code' in payload['regular']: codes.append(payload['regular']['code'])

            elif 'vector' in payload:
                if isinstance(payload['vector'], str): codes.append(payload['vector'])
                elif isinstance(payload['vector'], dict) and 'code' in payload['vector']: codes.append(payload['vector']['code'])

            # 检查是否包含 alphas 列表 (另一种 Multi 结构)
            elif 'alphas' in payload and isinstance(payload['alphas'], list):
                for item in payload['alphas']:
                    if isinstance(item, dict):
                        if 'code' in item: codes.append(item['code'])
                        elif 'regular' in item: codes.append(item['regular'])
                    elif isinstance(item, str): codes.append(item)

except Exception:
        return ["<无法解析表达式内容>"]

    return codes

def send_email_sync(subject, content):
    """同步发送邮件函数 (底层实现)"""
    try:
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = formataddr((SCRIPT_LABEL, MAIL_USER))
        message['To'] = Header(MAIL_RECEIVER, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

if not MAIL_USER or "your_email" in MAIL_USER:
            return

server = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, [MAIL_RECEIVER], message.as_string())
        server.quit()
        logger.info(f"📧 邮件发送成功: {subject}")
    except Exception as e:
        logger.error(f"❌ 邮件发送失败: {e}")

async def send_email_async(subject, content):
    """异步包装发送邮件，避免阻塞回测循环"""
    await asyncio.to_thread(send_email_sync, subject, content)

async def daily_report_scheduler():
    """每日早上8点发送日报的后台任务"""
    last_report_date = None
    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")

        # 每天 8 点且今天没发过
        if now.hour == 8 and last_report_date != today_str:
            percent = 0
            if STATS["total"] > 0:
                percent = (STATS["completed"] / STATS["total"]) * 100

            elapsed_hours = (time.time() - STATS["start_time"]) / 3600 if STATS["start_time"] > 0 else 0

            content = (
                f"任务标签: {STATS['name_tag']}\n"
                f"日期: {today_str}\n"
                f"当前进度: {STATS['completed']}/{STATS['total']} ({percent:.2f}%)\n"
                f"成功: {STATS['success']}\n"
                f"失败: {STATS['failed']}\n"
                f"已运行: {elapsed_hours:.2f} 小时\n"
                f"脚本正在持续运行中..."
            )
            await send_email_async(f"【{SCRIPT_LABEL}日报】运行统计", content)
            last_report_date = today_str

        # 每分钟检查一次
        await asyncio.sleep(60)

async def progress_monitor():
    """每隔1小时汇报进度的后台任务"""
    while True:
        await asyncio.sleep(3600)  # 3600秒 = 1小时
        if STATS["total"] > 0:
            percent = (STATS["completed"] / STATS["total"]) * 100
            elapsed = (time.time() - STATS["start_time"]) / 3600
            logger.info("="*40)
            logger.info(f"🕒 [定时进度汇报]")
            logger.info(f"进度: {STATS['completed']}/{STATS['total']} ({percent:.2f}%)")
            logger.info(f"成功: {STATS['success']} | 失败: {STATS['failed']}")
            logger.info(f"已运行: {elapsed:.2f} 小时")
            logger.info("="*40)

async def check_status_loop(session, url, index, context_id):
    """
    通用的状态轮询函数。
    返回: (status, alpha_id_list)
    """
    timeout = 7200  # 2小时超时
    start_wait = time.time()
    last_log_time = start_wait
    retry_complete_count = 0 # 防抖计数器

    # 动态调整轮询间隔
    poll_interval = 2.0 

    while time.time() - start_wait < timeout:
        try:
            resp = await asyncio.to_thread(session.request, wqb.GET, url)
            if resp.ok:
                # 成功获取，重置轮询间隔
                poll_interval = 2.0

                data = resp.json()
                status = data.get('status', 'UNKNOWN')

                # --- 增强的 ID 提取逻辑 (支持 children 嵌套 + 自动 fetch 子仿真) ---
                async def extract_ids_recursive(obj):
                    found = []
                    if isinstance(obj, dict):
                        if 'alpha' in obj:
                            val = obj['alpha']
                            if isinstance(val, str): found.append(val)
                            elif isinstance(val, dict) and 'id' in val: found.append(val['id'])

                        if 'alphas' in obj and isinstance(obj['alphas'], list):
                            for item in obj['alphas']:
                                if isinstance(item, str): found.append(item)
                                elif isinstance(item, dict) and 'id' in item: found.append(item['id'])

                        if 'children' in obj and isinstance(obj['children'], list):
                            for child in obj['children']:
                                if isinstance(child, str):
                                    child_url = f"{wqb.URL_SIMULATIONS}/{child}"
                                    try:
                                        child_resp = await asyncio.to_thread(session.request, wqb.GET, child_url)
                                        if child_resp.ok:
                                            child_data = child_resp.json()
                                            found.extend(await extract_ids_recursive(child_data))
                                    except Exception: pass
                                elif isinstance(child, dict):
                                    found.extend(await extract_ids_recursive(child))
                    return found

valid_alphas = await extract_ids_recursive(data)

if valid_alphas:
                    return "COMPLETED", valid_alphas

# --- 状态检查 ---
                if status in ['COMPLETED', 'COMPLETE', 'FINISHED', 'ERROR', 'FAIL', 'CANCELLED']:
                    if status in ['COMPLETED', 'COMPLETE', 'FINISHED'] and retry_complete_count < 5:
                        retry_complete_count += 1
                        logger.info(f"⏳ [{index}] {context_id} 状态已完成但未见ID，等待同步 ({retry_complete_count}/5)...")
                        await asyncio.sleep(1.5) # 同步等待稍微快一点
                        continue

                    if status in ['COMPLETED', 'COMPLETE', 'FINISHED']:
                        logger.warning(f"⚠️ [{index}] {context_id} 状态为 {status} 但未发现 Alpha ID. 响应键: {list(data.keys())}")

                    return status, None

                # 修改：日志间隔调整为 180 秒 (3分钟)
                if time.time() - last_log_time > 180:
                    logger.info(f"⏳ [{index}] {context_id} 正在运行中 (Status: {status})...")
                    last_log_time = time.time()

            elif resp.status_code == 429:
                poll_interval = min(poll_interval * 1.5, 10.0)
                await asyncio.sleep(poll_interval)
                continue
            elif resp.status_code == 404:
                pass 

        except Exception:
            pass

        await asyncio.sleep(poll_interval)

    logger.warning(f"⚠️ [{index}] 等待 {context_id} 超时")
    return "TIMEOUT", None

async def process_single_task(session, semaphore, alpha_payload, name_tag, index):
    """处理单个回测任务"""
    async with semaphore:
        try:
            # 1. 提交仿真
            max_retries = 20
            retry_count = 0
            resp = None

            while retry_count < max_retries:
                resp = await asyncio.to_thread(
                    session.request,
                    method=wqb.POST, 
                    url=wqb.URL_SIMULATIONS, 
                    json=alpha_payload
                )

                if resp.status_code == 429:
                    wait_time = random.uniform(10, 20)
                    logger.warning(f"⚠️ [{index}] 槽位已满 (429)，等待 {wait_time:.1f}秒后重试... ({retry_count+1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    retry_count += 1
                    continue

                if not resp.ok:
                    raise Exception(f"仿真请求失败: {resp.status_code} - {resp.text}")

                break

            if retry_count >= max_retries:
                raise Exception(f"达到最大重试次数，放弃任务")

# 2. 解析 ID
            alpha_id = None
            sim_id = None

            try:
                result_json = resp.json()
                alpha_id = result_json.get('alpha')
                sim_id = result_json.get('id')
            except: pass 

            location = resp.headers.get('Location')
            if location:
                if '/alphas/' in location: alpha_id = location.split('/')[-1]
                elif '/simulations/' in location: sim_id = location.split('/')[-1]

# 3. 分支处理
            final_alpha_ids = []

if alpha_id:
                status, ids = await check_status_loop(session, f"{wqb.URL_ALPHAS}/{alpha_id}", index, f"Alpha {alpha_id}")
                if ids: final_alpha_ids = ids

elif sim_id:
                logger.info(f"ℹ️ [{index}] 仅获取到 Sim ID: {sim_id}，等待仿真完成...")
                status, ids = await check_status_loop(session, f"{wqb.URL_SIMULATIONS}/{sim_id}", index, f"Sim {sim_id}")

                if ids:
                    final_alpha_ids = ids
                    logger.info(f"🎉 [{index}] Sim {sim_id} 完成. ID(s): {final_alpha_ids}")
                else:
                    if status in ['ERROR', 'FAIL']:
                        logger.warning(f"⚠️ [{index}] Sim {sim_id} 失败 (Status: {status})")
                        # --- 新增：失败时回显表达式 ---
                        codes = extract_expression_codes(alpha_payload)
                        logger.error(f"❌ [{index}] 失败的表达式内容:")
                        for c in codes:
                            logger.error(f"   >>> {c}")
                        # ---------------------------
                    else:
                        logger.info(f"ℹ️ [{index}] Sim {sim_id} 完成但未生成 Alpha (Status: {status})")

else:
                logger.error(f"❌ [{index}] 提交成功但无法获取ID，强制等待 60 秒")
                STATS["failed"] += 1
                await asyncio.sleep(60)
                return

# 4. 统一改名逻辑 (无颜色)
            if final_alpha_ids:
                ids_to_rename = final_alpha_ids if isinstance(final_alpha_ids, list) else [final_alpha_ids]

                for sub_idx, aid in enumerate(ids_to_rename):
                    suffix = f"_{sub_idx}" if len(ids_to_rename) > 1 else ""
                    new_name = f"{name_tag}_{index}_{aid}{suffix}"

                    patch_data = {
                        "name": new_name, 
                        "tags": [name_tag]
                    }
                    patch_url = f"{wqb.URL_ALPHAS}/{aid}"

                    patch_resp = await asyncio.to_thread(session.request, wqb.PATCH, patch_url, json=patch_data)
                    if patch_resp.ok:
                        logger.info(f"✅ [{index}] ID:{aid} | Name:{new_name} | Tag:{name_tag}")
                        STATS["success"] += 1
                    else:
                        logger.warning(f"⚠️ [{index}] ID:{aid} 改名失败: {patch_resp.status_code}")
                        STATS["success"] += 1
            else:
                STATS["success"] += 1

except Exception as e:
            logger.error(f"❌ [{index}] 任务失败: {e}")
            STATS["failed"] += 1
            await asyncio.sleep(5)
        finally:
            STATS["completed"] += 1

async def main():
    print("🚀 WQB 自动回测与打标工具")
    print("="*50)

# 1. 登录
    username, password = load_credentials()
    if not username:
        return

    print(f"👤 检测到用户: {username}")
    session = wqb.WQBSession(wqb_auth=(username, password))

    if not session.locate_field('open').ok:
        print("❌ 登录失败，请检查 user_info.txt")
        return
    print("✅ 登录成功")

# 2. 加载数据
    expressions = get_json_filepath()
    if not expressions:
        return

total_expr = len(expressions)
    print(f"📊 加载了 {total_expr} 条表达式")

# 3. 配置参数
    try:
        range_input = input(f"请输入回测范围 (格式 '起点-终点' 或仅输入起点, 默认0-{total_expr}): ") or "0"

        if '-' in range_input:
            start_str, end_str = range_input.split('-')
            start_idx = int(start_str.strip())
            end_idx = int(end_str.strip())
        else:
            start_idx = int(range_input.strip())
            end_idx = total_expr

if start_idx < 0: start_idx = 0
        if end_idx > total_expr: end_idx = total_expr
        if start_idx >= end_idx:
            print(f"❌ 起点 ({start_idx}) 不能大于等于终点 ({end_idx})")
            return

concurrency = int(input("请输入回测进程数 (默认5): ") or 5)

        mode = input("请选择模式 (s=Single, m=Multi, 默认s): ").lower() or 's'
        is_multi = mode == 'm'

        multi_count = 1
        if is_multi:
            multi_count = int(input("请输入Multi模式下每个进程的Alpha数 (2-10, 默认3): ") or 3)

name_tag = input("请输入Alpha名称前缀和标签 (默认 AutoAlpha): ") or "AutoAlpha"
        STATS["name_tag"] = name_tag # 记录到全局变量

    except ValueError:
        print("❌ 输入无效，请输入正确的数字格式")
        return

# 4. 数据预处理
    work_list = expressions[start_idx : end_idx]
    print(f"✂️  选中范围 [{start_idx} : {end_idx}]，共 {len(work_list)} 条待处理")

if is_multi:
        print(f"🔄 正在转换为 Multi 模式 (每组 {multi_count} 个)...")
        work_list = list(wqb.to_multi_alphas(work_list, multi_count))
        print(f"📦 转换后共有 {len(work_list)} 个 Multi 任务包")

STATS["total"] = len(work_list)
    STATS["start_time"] = time.time()

# --- 发送启动邮件 ---
    start_msg = (
        f"任务已启动。\n"
        f"标签: {name_tag}\n"
        f"数量: {len(work_list)}\n"
        f"并发: {concurrency}\n"
        f"模式: {'Multi' if is_multi else 'Single'}"
    )
    await send_email_async(f"【{SCRIPT_LABEL}】任务启动通知", start_msg)
    # ------------------

# 5. 执行并发循环
    semaphore = asyncio.Semaphore(concurrency)
    tasks = []

    monitor_task = asyncio.create_task(progress_monitor())
    daily_report_task = asyncio.create_task(daily_report_scheduler()) # 启动日报任务

print("\n🔥 开始执行任务...")
    print("="*50)

try:
        for i, payload in enumerate(work_list):
            real_index = start_idx + (i * multi_count if is_multi else i)

            task = asyncio.create_task(
                process_single_task(
                    session, 
                    semaphore, 
                    payload, 
                    name_tag, 
                    real_index
                )
            )
            tasks.append(task)

await asyncio.gather(*tasks)

    except Exception as e:
        # 运行中发生未捕获异常
        err_msg = traceback.format_exc()
        logger.error(f"运行中发生严重错误: {e}")
        await send_email_async(f"【{SCRIPT_LABEL}】任务异常中断", f"任务在运行中发生错误。\n\n{err_msg}")
        raise e # 继续抛出以便外层也能捕获

finally:
        monitor_task.cancel()
        daily_report_task.cancel() # 任务结束，取消日报

    end_time = time.time()
    duration = (end_time - STATS["start_time"]) / 60

    summary = (
        f"所有任务执行完毕。\n"
        f"耗时: {duration:.2f} 分钟\n"
        f"总数: {STATS['total']}\n"
        f"成功: {STATS['success']}\n"
        f"失败: {STATS['failed']}"
    )

    print("\n" + "="*50)
    print("🎉 " + summary)
    print("="*50)

    # --- 发送完成邮件 ---
    await send_email_async(f"【{SCRIPT_LABEL}】任务完成通知", summary)

if __name__ == "__main__":
    # --- 【新增 2/2】解析命令行参数 ---
    parser = argparse.ArgumentParser(description="WQB 自动回测与打标工具")
    parser.add_argument("--label", type=str, default="Master", help="脚本标识(如: 大号/小号)，用于邮件区分")

    # 使用 parse_known_args 防止如果有其他参数传入时报错
    args, unknown = parser.parse_known_args()

    # 更新全局标识
    SCRIPT_LABEL = args.label
    # -------------------------------

try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ 用户手动停止")
        # 手动停止也可以发个邮件，如果需要的话
        # send_email_sync(f"【{SCRIPT_LABEL}】任务手动停止", "用户按下了 Ctrl+C")
    except Exception as e:
        # 捕获 main() 之外或 asyncio.run 本身的错误
        err_msg = traceback.format_exc()
        print(f"❌ 致命错误: {e}")
        send_email_sync(f"【{SCRIPT_LABEL}】致命错误报警", f"脚本发生致命错误退出。\n\n{err_msg}")

---

## 讨论与评论 (10)

### 评论 #1 (作者: YZ97204, 时间: 6个月前)

谢谢大佬的分享，已经拿来测试用了

---

### 评论 #2 (作者: FF65210, 时间: 6个月前)

❌ 邮件发送失败: Connection unexpectedly closed

❌ 致命错误: asyncio.run() cannot be called from a running event loop

请问下我的代码报错这个是怎么回事啊，我用的Jupyter Notebook跑的

---

### 评论 #3 (作者: HZ49684, 时间: 6个月前)

大佬写的文章，正好最近需要，真是解决了燃眉之急了！感谢大佬分享！

---

### 评论 #4 (作者: ZL75781, 时间: 6个月前)

可以的 对于不会写代码的人是一个不错的选择

---

### 评论 #5 (作者: ZH41150, 时间: 6个月前)

# 1. 提交仿真
            max_retries = 20
            retry_count = 0
            resp = None

            while retry_count < max_retries:
                resp = await asyncio.to_thread(
                    session.request,
                    method=wqb.POST, 
                    url=wqb.URL_SIMULATIONS, 
                    json=alpha_payload
                )

                if resp.status_code == 429:
                    wait_time = random.uniform(10, 20)
                    logger.warning(f"⚠️ [{index}] 槽位已满 (429)，等待 {wait_time:.1f}秒后重试... ({retry_count+1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    retry_count += 1
                    continue

                if not resp.ok:
                    raise Exception(f"仿真请求失败: {resp.status_code} - {resp.text}")  佬，这个仿真提交是指自动提交么

---

### 评论 #6 (作者: FZ24842, 时间: 6个月前)

挺好的脚本，避免经常盯着电脑

---

### 评论 #7 (作者: MZ45384, 时间: 6个月前)

对，我也觉得wqb的日志等方面不太完善，所以我一开始就修改了断点记录和日志输出，同时还有个session覆盖。不过远没有大佬的系统和全面。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值
======================================================================================

---

### 评论 #8 (作者: MY49971, 时间: 6个月前)

感谢大佬的分享，完善了wqb的相关功能

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #9 (作者: WL20457, 时间: 6个月前)

感谢大佬的分享的代码，代码虽小但是个完成的体系，集任务执行监控一体，代码中的asyncio.run + await 用的很精髓，这个可以避免多线程并发回测时候因为sleep导致线程卡死问题，另外贴心的加上了邮件功能。给大佬一个大大的赞！！

---

### 评论 #10 (作者: ZL75781, 时间: 4个月前)

感谢大佬分享，让我的回测系统变的更加完美了，我直接吧你的代码喂给mcp就可以让她基于你的代码进行升级！

===================================================================================
===================ZL75781 2026.1.29=================================

---

