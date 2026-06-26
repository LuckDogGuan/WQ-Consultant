# 【新人向-RA的Prod检测 —— 24h可检测600个！】即插即用！结合上一篇自相关文章！

- **链接**: [Commented] 【新人向-RA的Prod检测  24h可检测600个】即插即用结合上一篇自相关文章.md
- **作者**: LX57490
- **发布时间/热度**: 6个月前, 得票: 125

## 帖子正文

**本帖子展示了如何将前辈 [SY86571](/hc/zh-cn/profiles/30781531875223-SY86571) 的优雅避免prod检测受到限流处理及上一篇自相关检测的输出结果进行合二为一的Prod检测代码！**

当然，后续大家可以自行改进！这是给新人提供的一个检测模版代码，上一篇的本地检测自相关也是，你可以添加针对于各个地区的筛选标准，以便减少prod检测数量，以及针对每个地区加入更多的检测标准，例如GLB其他三地区的Sharpe，或者Turnover阈值，Returns阈值，Drawdown阈值，Margin阈值！

一、登录以及使用方法

1. 在代码 **600~601** 行进行登录。

2. 606行的" **SELF_ONLY** " 或 " **PPA_AND_SELF** "

" **SELF_ONLY** "：顾名思义，只选择SC阈值内进行PC检测；

" **PPA_AND_SELF** "：顾名思义，在SC和PPAC双阈值下进行PC检测。

使用" **PPA_AND_SELF** "记得两个阈值都选好 **SELF_THRESHOLD** 和 **PPA_SELF_THRESHOLD** 都设置你想要的最大值！！！！

3.  **609** 行日期， **610** 行地区，不多说了！

```

```

4. 运行效果：

在运行过程中，避免你着急寻找，会有一个中间过程文件供你进行使用：

下面是他的名字和效果图：

```

```

```

```

5. 最终代码效果：

这个代码是以 **20个alpha** 为一组，测试完后进行 **半小时** 休息，大家可自行更改！

如下图所示，可以看得出来夜间没什么人测，都不需要重试，9min直接就测完了20个alpha，大家可以根据自己的时间进行微调，例如第一次等待时长和后续重试等待时长，以及检测时间段，服务器悠闲时间段可以多测点，例如夜间到早上的时间段！

![图片](images/img_208b99200d.png)

![图片](images/img_847f8807d5.png)

输出效果如下：这也是我略微改进了上个帖子自相关代码后的效果，有了更多的条件，筛选出来的更符合我自己的需求的一个样子，并且加了GLB三地区Sharpe阈值和2年Sharpe阈值等。

![图片](images/img_729d914a5d.png)  ![图片](images/img_ba8dc99d2b.png)

6. 一个断点重测机制：

输入y：遍历之前没有检查成功的，然后接上进行回测！

输入n：自动 **删除** 之前文件并进行prod检测！ ![图片](images/img_bfb440c592.png)

7. 完整代码！

**最后祝各位顾问月月VF1.0！RA60刀！SA60！日日120刀！！！！**

**高筑墙！广积粮！缓称王！**

import requests
import time
import threading
import logging
import pandas as pd
from typing import Optional, List, Dict
import base64
import urllib3
from http.client import IncompleteRead
import os
import random
import json
import signal
import csv
import datetime
import sys
import requests

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 全局变量用于存储Prod Correlation请求的限流状态
prod_corr_remaining = 60
prod_corr_reset_time = time.time() + 60
prod_corr_lock = threading.Lock()

# 全局变量
SESSION_REFRESH_INTERVAL = 3600  # 3.5小时
last_auth_time = time.time()

# 全局变量用于存储部分结果
partial_df = pd.DataFrame()
partial_file_path = ""

def save_partial_results():
    """保存当前获取的部分结果（只保留alpha_id和prod_correlation_max）"""
    global partial_df, partial_file_path

if partial_df.empty:
        return

if not partial_file_path:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        partial_file_path = f"partial_results_{timestamp}.csv"

try:
        # 关键修改：只保存alpha_id和prod_correlation_max两列
        partial_df[['alpha_id', 'prod_correlation_max']].to_csv(partial_file_path, index=False)
        logging.info(f"已保存部分结果到: {partial_file_path}（仅保留关键列）")
    except Exception as e:
        logging.error(f"保存部分结果失败: {e}")

def handle_interrupt(signum, frame):
    """处理中断信号"""
    logging.warning("检测到程序中断，正在保存当前结果...")
    save_partial_results()
    logging.info("部分结果已保存，程序退出")
    os._exit(1)  # 立即退出程序

def load_partial_results(file_path: str) -> pd.DataFrame:
    """加载部分结果文件（只读取alpha_id和prod_correlation_max）"""
    try:
        # 关键修改：只读取需要的两列
        df = pd.read_csv(file_path, usecols=['alpha_id', 'prod_correlation_max'])
        logging.info(f"从部分结果文件加载了 {len(df)} 条记录（仅关键列）")
        return df
    except Exception as e:
        logging.error(f"加载部分结果失败: {e}")
        return pd.DataFrame()

def ensure_session_valid(session, last_auth_time):
    """确保会话有效，如果超过刷新间隔则重新登录"""
    current_time = time.time()
    if current_time - last_auth_time > SESSION_REFRESH_INTERVAL:
        logging.info("会话已超过3.5小时，正在刷新...")
        try:
            # 尝试删除现有认证
            session.delete(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')
        except:
            pass  # 忽略删除错误

# 重新登录
        new_session = sign_in(USERNAME, PASSWORD)
        logging.info("会话刷新成功")
        return new_session, current_time
    return session, last_auth_time

def sign_in(username: str, password: str) -> Optional[requests.Session]:
    """登录WorldQuant Brain平台"""
    session = requests.Session()
    try:
        # 构造认证字符串
        auth_str = f"{username}:{password}"
        # 转换为字节并Base64编码
        auth_bytes = auth_str.encode('utf-8')
        base64_bytes = base64.b64encode(auth_bytes)
        base64_str = base64_bytes.decode('utf-8')

headers = {
            "Authorization": f"Basic {base64_str}",
            "Content-Type": "application/json"
        }

# 发送认证请求（启用SSL验证）
        response = session.post(
            ' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ',
            headers=headers,
            verify=True  # 启用SSL证书验证
        )

# 检查响应状态
        if response.status_code in [200, 201]:
            user_id = response.json().get('user', {}).get('id', '未知用户')
            logging.info(f"登录成功: 用户ID {user_id}")
            return session
        else:
            logging.error(f"登录失败: 状态码 {response.status_code}, 响应: {response.text[:200]}")
            return None
    except requests.exceptions.SSLError as ssl_err:
        # 处理SSL错误
        logging.error(f"SSL连接错误: {ssl_err}")
        # 尝试不使用SSL验证（仅限测试环境）
        try:
            logging.warning("尝试不使用SSL验证...")
            # 重新创建headers（确保变量作用域正确）
            auth_bytes = f"{username}:{password}".encode('utf-8')
            base64_str = base64.b64encode(auth_bytes).decode('utf-8')
            headers = {
                "Authorization": f"Basic {base64_str}",
                "Content-Type": "application/json"
            }

response = session.post(
                ' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ',
                headers=headers,
                verify=False  # 禁用SSL验证
            )
            if response.status_code in [200, 201]:
                user_id = response.json().get('user', {}).get('id', '未知用户')
                logging.warning(f"登录成功(无SSL验证): 用户ID {user_id}")
                return session
            else:
                logging.error(f"无SSL验证登录失败: 状态码 {response.status_code}")
                return None
        except Exception as fallback_err:
            logging.error(f"无SSL验证登录异常: {fallback_err}")
            return None
    except Exception as e:
        logging.error(f"登录过程中发生错误: {e}")
        return None

def safe_get_error_detail(response):
    """安全获取错误详情，处理各种响应格式"""
    try:
        content = response.json()
        if "detail" in content:
            return content["detail"]
        if "error" in content:
            return content["error"]
        if "message" in content:
            return content["message"]
        return json.dumps(content, indent=2)
    except json.JSONDecodeError:
        if "text/html" in response.headers.get("Content-Type", ""):
            return "HTML响应: " + response.text[:500] + "..."
        return response.text if response.text else '无错误详情'

def calculate_retry_delay(attempt, max_retries, error_type=None):
    """智能计算重试延迟时间，使用指数退避+抖动策略"""
    base_delay = 1.0
    if error_type == 'rate_limit':
        base_delay = 5.0
    elif error_type == 'client_error':
        base_delay = 2.0
    elif error_type == 'server_error':
        base_delay = 3.0

delay = base_delay * (2 ** min(attempt, 8))
    jitter = random.uniform(0.5, 1.5)
    delay *= jitter
    return min(delay, 60.0)

def get_prod_correlation_max(session: requests.Session, alpha_id: str, max_retries: int = 5) -> Optional[float]:
    global prod_corr_remaining, prod_corr_reset_time, last_auth_time

# 确保会话有效
    session, last_auth_time = ensure_session_valid(session, last_auth_time)

url = f" [https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod](https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod) "
    retries = 0
    empty_retries = 0
    max_empty_retries = 10

# 新增：基础等待时间和增量
    base_wait = 20.0  # 初始20秒
    increment = 10.0  # 每次增加10秒

while retries < max_retries:
        # 检查限流状态
        with prod_corr_lock:
            current_time = time.time()
            if prod_corr_remaining <= 3 and prod_corr_reset_time > current_time:
                wait_time = max(3, prod_corr_reset_time - current_time)
                logging.info(f"等待限流重置: {wait_time:.1f}秒 (剩余次数: {prod_corr_remaining})")
                time.sleep(wait_time)

try:
            # 发送请求
            resp = session.get(url, timeout=(15, 60))  # 增加超时时间

# 处理200响应
            if resp.status_code == 200:
                # 更新限流状态
                with prod_corr_lock:
                    try:
                        remaining_str = resp.headers.get("Ratelimit-Remaining", "60")
                        reset_str = resp.headers.get("Ratelimit-Reset", "60")
                        prod_corr_remaining = int(remaining_str.split('.')[0])
                        reset_seconds = float(reset_str.split('.')[0])
                        prod_corr_reset_time = current_time + reset_seconds
                    except Exception as e:
                        logging.warning(f"解析限流头部失败: {e}")

# 处理空响应 - 新的时间控制策略
                if not resp.content:
                    # 计算当前等待时间
                    current_wait = base_wait + (empty_retries * increment)

# 应用上限限制
                    if current_wait > 300:
                        current_wait = 300
                    # 超过120秒后保持在120-180秒范围
                    elif current_wait > 120:
                        current_wait = 120 + random.uniform(0, 60)  # 120-180秒随机

logging.warning(
                        f"空响应，等待 {current_wait:.1f}秒 (空响应重试: {empty_retries + 1}/{max_empty_retries})")
                    time.sleep(current_wait)

empty_retries += 1
                    if empty_retries >= max_empty_retries:
                        logging.error(f"达到最大空响应重试次数 {max_empty_retries}")
                        return None
                    continue

# 解析JSON响应
                try:
                    data = resp.json()
                    return float(data.get("max", 0))
                except ValueError:
                    logging.error(f"JSON解析失败: {resp.text[:100]}...")
                    return None

# 处理401未授权错误
            elif resp.status_code == 401:
                logging.warning("会话过期，尝试重新登录...")
                session = sign_in(USERNAME, PASSWORD)
                last_auth_time = time.time()
                continue  # 不消耗重试次数

# 处理429限流错误
            elif resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", "70"))
                logging.warning(f"429限流，等待 {retry_after}秒")
                time.sleep(retry_after)
                continue  # 不消耗重试次数

# 处理400客户端错误
            elif resp.status_code == 400:
                error_detail = safe_get_error_detail(resp)
                logging.error(f"400客户端错误: {error_detail}")
                return None  # 不重试

# 处理5xx服务器错误
            elif 500 <= resp.status_code < 600:
                wait_time = calculate_retry_delay(retries, max_retries, 'server_error')
                logging.error(f"服务器错误({resp.status_code})，等待 {wait_time:.2f}秒")
                time.sleep(wait_time)
                retries += 1
                continue

# 其他错误
            else:
                error_detail = safe_get_error_detail(resp)
                logging.error(f"错误状态: {resp.status_code}, 详情: {error_detail}")
                return None

# 处理网络错误
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, IncompleteRead) as e:
            wait_time = calculate_retry_delay(retries, max_retries)
            logging.error(f"网络错误({type(e).__name__})，等待 {wait_time:.2f}秒")
            time.sleep(wait_time)
            retries += 1
        except requests.exceptions.RequestException as e:
            wait_time = calculate_retry_delay(retries, max_retries)
            logging.error(f"请求异常: {e}，等待 {wait_time:.2f}秒")
            time.sleep(wait_time)
            retries += 1

logging.error(f"超过最大重试次数 {max_retries}")
    return None

def read_data_from_file(file_path: str) -> pd.DataFrame:
    """从文件(Excel或CSV)中读取数据，并应用过滤条件"""
    try:
        if not os.path.exists(file_path):
            logging.error(f"文件不存在: {file_path}")
            return pd.DataFrame()

# 读取文件
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            engine = 'openpyxl' if file_path.lower().endswith('.xlsx') else None
            df = pd.read_excel(file_path, engine=engine)
        else:
            logging.error(f"不支持的文件格式: {file_path}")
            return pd.DataFrame()

# 检查必要列是否存在 - 使用正确的列名'ppac_correlation'
        required_columns = ['alpha_id', 'self_correlation', 'ppac_correlation']
        missing_cols = [col for col in required_columns if col not in df.columns]

# 特殊提示："ppa_correlation"是常见错误拼写
        if missing_cols and "ppa_correlation" in df.columns:
            logging.warning("检测到可能的列名拼写错误：使用'ppa_correlation'代替'ppac_correlation'")
            df.rename(columns={'ppa_correlation': 'ppac_correlation'}, inplace=True)
            missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
            logging.error(f"文件缺少必要列: {', '.join(missing_cols)}")
            return pd.DataFrame()

# 应用过滤条件
        if FILTER_MODE == "SELF_ONLY":
            filtered_df = df[df['self_correlation'] <= SELF_THRESHOLD]
            logging.info(f"使用单独SELF筛选: self≤{SELF_THRESHOLD}")
        elif FILTER_MODE == "PPA_AND_SELF":  # 使用正确的ppac_correlation列名
            filtered_df = df[
                (df['self_correlation'] <= SELF_THRESHOLD) &
                (df['ppac_correlation'] <= PPA_SELF_THRESHOLD)  # 这里是关键
                ]
            logging.info(f"使用双重筛选: self≤{SELF_THRESHOLD} 且 ppac≤{PPA_SELF_THRESHOLD}")
        else:
            logging.error(f"无效的筛选模式: {FILTER_MODE}")
            return pd.DataFrame()

logging.info(f"从 {file_path} 中读取到 {len(filtered_df)} 个符合条件的记录")

# 验证记录是否符合条件
        if len(filtered_df) > 0:
            sample = filtered_df.sample(min(3, len(filtered_df)))
            for _, row in sample.iterrows():
                logging.debug(f"采样记录: ID={row['alpha_id']}, "
                              f"self={row['self_correlation']:.2f}, "
                              f"ppac={row['ppac_correlation']:.2f}")

return filtered_df
    except Exception as e:
        logging.error(f"读取文件失败: {e}")
        return pd.DataFrame()

def process_data(session: requests.Session, input_df: pd.DataFrame, output_file: str):
    global partial_df, partial_file_path, last_auth_time

# 添加新列用于存储结果 (如有必要)
    if 'prod_correlation_max' not in input_df.columns:
        input_df['prod_correlation_max'] = None

# ████████ 重要修改：添加强制重置选项 ████████
    skip_partial = False  # 新增标志
    partial_files = sorted([f for f in os.listdir()
                            if f.startswith("partial_results_") and f.endswith(".csv")])

if partial_files:
        partial_file_path = partial_files[-1]
        logging.info(f"检测到部分结果文件: {partial_file_path}")

response = input("是否从部分结果文件继续处理? (y/n): ").strip().lower()
        if response == 'y':
            # ✅ 读取完整的部分结果文件（包含所有原始列）
            partial_results = pd.read_csv(partial_file_path)
            logging.info(f"从部分结果文件加载了 {len(partial_results)} 条完整记录")

# ✅ 只标记已完成处理的行（有有效数值或"获取失败"标记的）
            completed_mask = (
                    (partial_results['prod_correlation_max'].notna()) |
                    (partial_results['prod_correlation_max'] == "获取失败")
            )
            completed_df = partial_results[completed_mask]

# ✅ 标记跳过已完成的alpha_id（但不删除整个行）
            skip_count = len(completed_df)
            logging.info(f"跳过 {skip_count} 个已处理的alpha_id")

# ✅ 更新主数据帧：0. 保留原始数据结构 1. 只合并已处理的结果
            # 第一步：创建alpha_id到结果的映射
            result_map = completed_df.set_index('alpha_id')['prod_correlation_max'].to_dict()

# 第二步：更新主数据框的prod_correlation_max列
            mask = input_df['alpha_id'].isin(result_map.keys())
            input_df.loc[mask, 'prod_correlation_max'] = input_df.loc[mask, 'alpha_id'].map(result_map)

# ✅ 显示状态
            progress_stats = input_df['prod_correlation_max'].apply(lambda x: x is not None and x != "").sum()
            logging.info(
                f"当前状态: 共 {len(input_df)} 行, 已完成 {progress_stats} 行, 待处理 {len(input_df) - progress_stats} 行")

else:
            logging.warning("已选择不继续处理部分结果，将删除该文件并重新开始")
            try:
                os.remove(partial_file_path)
                logging.info(f"部分结果文件已删除: {partial_file_path}")
                skip_partial = True  # 标记需要跳过旧记录
            except Exception as e:
                logging.error(f"删除部分结果文件失败: {e}")
                return

# 初始化部分结果数据框（需要重置）
    partial_df = input_df.copy()

# ████████ 新增：当跳过部分结果时完全重置 ████████
    if skip_partial:
        logging.info("正在进行全新处理，清空所有历史记录")
        partial_df['prod_correlation_max'] = None  # 关键：重置所有值为未处理状态
        partial_file_path = ""  # 重置部分文件路径

# 注册中断信号处理 (...代码不变，但建议增加异常处理...)
    try:
        signal.signal(signal.SIGINT, handle_interrupt)
    except ValueError:
        pass  # 在某些线程环境下可能无法设置信号

total_count = len(partial_df)
    success_count = 0
    failure_count = 0
    processed_count = 0
    batch_size = 20  # 每20个一批

# 获取当前已处理的数量（从部分结果文件中）
    already_processed = total_count - len(input_df)

for i, row in enumerate(partial_df.itertuples(), start=1):
        alpha_id = row.alpha_id
        skip_row = False

# 跳过已处理的行
        if not pd.isna(row.prod_correlation_max) and row.prod_correlation_max != "获取失败":
            logging.info(f"跳过已处理: {alpha_id} (值: {row.prod_correlation_max})")
            processed_count += 1
            skip_row = True
        else:
            logging.info(f"处理 {i + already_processed}/{total_count + already_processed}: {alpha_id}")

# 仅对未处理的行进行实际处理
        if not skip_row:
            max_value = get_prod_correlation_max(session, alpha_id)

if max_value is not None:
                partial_df.at[row.Index, 'prod_correlation_max'] = max_value
                logging.info(f"成功获取 {alpha_id} 的max值: {max_value:.4f}")
                success_count += 1
                processed_count += 1
            else:
                partial_df.at[row.Index, 'prod_correlation_max'] = "获取失败"
                logging.warning(f"获取 {alpha_id} 的max值失败")
                failure_count += 1
                processed_count += 1  # 失败也算作已处理

# 每处理1个alpha_id保存一次部分结果
        save_partial_results()

# 每处理1个alpha_id打印一次状态
        with prod_corr_lock:
            remaining_time = max(0, prod_corr_reset_time - time.time())
            progress_info = (
                f"进度: {i + already_processed}/{total_count + already_processed} | "
                f"成功: {success_count} | 失败: {failure_count} | 跳过: {processed_count - (success_count + failure_count)} | "
                f"批次: {processed_count % batch_size}/{batch_size} | "
                f"剩余查询次数: {prod_corr_remaining} | 重置时间: {remaining_time:.1f}秒后"
            )
            logging.info(progress_info)
            # 特殊标记批次完成的时间点
            if processed_count % batch_size == 0 and processed_count > 0:
                logging.info("▬" * 60)

# 每完成20个处理（不包括跳过）休息30分钟
        if processed_count % batch_size == 0 and processed_count > 0 and not skip_row:
            # 保存当前进度
            save_partial_results()

# 休息半小时
            rest_duration = 30 * 60  # 30分钟
            logging.info("=" * 70)
            logging.info(f"*** 已完成 {batch_size} 个alpha_id, 开始休息30分钟 ***")
            logging.info("=" * 70)

start_time = time.time()
            remaining_rest = rest_duration

# 倒计时实现（允许中断）
            while remaining_rest > 0:
                try:
                    # 计算分钟和秒
                    mins, secs = divmod(remaining_rest, 60)
                    # 动态旋转符号
                    spinner = "◐◓◑◒"[int(time.time()) % 4]
                    # 进度条
                    progress_bar = "■" * int(50 * (remaining_rest / rest_duration))

status_msg = (
                        f"[休息中] 剩余时间: {mins:02.0f}:{secs:02.0f} {spinner} "
                        f"进度: [\033[34m{progress_bar.ljust(50)}\033[0m]"
                    )

# 使用单行覆盖输出
                    if remaining_rest != rest_duration:
                        # 回退到行首
                        sys.stdout.write("\r\033[K")

sys.stdout.write(status_msg)
                    sys.stdout.flush()

# 每秒更新一次
                    time.sleep(1)
                    remaining_rest = rest_duration - (time.time() - start_time)

except KeyboardInterrupt:
                    logging.warning("\n休息被中断！将提前继续处理...")
                    break

# 确保输出回到正常状态
            if remaining_rest > 0:
                sys.stdout.write("\n")

logging.info("-" * 70)
            logging.info("休息结束，刷新API会话并继续处理...")
            logging.info("-" * 70)

# 刷新会话（避免会话过期）
            session = sign_in(USERNAME, PASSWORD)
            last_auth_time = time.time()

# 打印限流状态
            with prod_corr_lock:
                logging.info(f"限流状态已重置: 剩余查询次数 {prod_corr_remaining}")

# 处理完成后删除部分结果文件
    if partial_file_path and os.path.exists(partial_file_path):
        try:
            os.remove(partial_file_path)
            logging.info(f"已删除部分结果文件: {partial_file_path}")
        except Exception as e:
            logging.error(f"删除部分结果文件失败: {e}")

# 保存结果到文件
    try:
        # 调整列顺序：将prod_correlation_max放在self_correlation和ppac_correlation之后
        columns = partial_df.columns.tolist()
        if 'self_correlation' in columns and 'ppac_correlation' in columns:
            # 找到ppac_correlation的位置
            ppac_index = columns.index('ppac_correlation')
            # 将prod_correlation_max插入到ppac_correlation之后
            columns.insert(ppac_index + 1, 'prod_correlation_max')
            # 移除原有的prod_correlation_max列（如果存在）
            if 'prod_correlation_max' in columns:
                columns.remove('prod_correlation_max')
            # 重新排列列
            partial_df = partial_df[columns]

# 根据文件扩展名决定保存格式
        if output_file.lower().endswith('.xlsx'):
            # 保存为Excel
            partial_df.to_excel(output_file, index=False)
            logging.info(f"结果已保存到Excel文件: {output_file}")
        else:
            # 默认保存为CSV
            partial_df.to_csv(output_file, index=False)
            logging.info(f"结果已保存到CSV文件: {output_file}")
    except Exception as e:
        logging.error(f"保存结果失败: {e}")

# 主程序
if __name__ == "__main__":
    # ================= 账号密码 =================
    USERNAME = ""
    PASSWORD = ""

# ================= 筛选条件配置 =================
    SELF_THRESHOLD = 0.7  # 单独self筛选阈值 (可调)
    PPA_SELF_THRESHOLD = 0.5  # ppa+self双重筛选的ppa阈值 (可调)
    FILTER_MODE = "PPA_AND_SELF"  # "SELF_ONLY" 或 "PPA_AND_SELF"

# ================= 筛选条件配置 =================
    START_DATE = "12-09"
    REGION = "EUR"

# 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

# 输入文件路径
    INPUT_FILE = os.path.join(script_dir, f"alpha_results_{START_DATE}_{REGION}.xlsx")

# 输出文件路径（与代码同目录）
    OUTPUT_FILE = os.path.join(script_dir, f"alphas_{START_DATE}_{REGION}_prod_corr.xlsx")

# 登录
    print("尝试登录...")
    session = sign_in(USERNAME, PASSWORD)
    if session is None:
        print("登录失败，请检查用户名和密码")
        exit(1)

# 从文件读取数据
    input_df = read_data_from_file(INPUT_FILE)
    if input_df.empty:
        print(f"未从 {INPUT_FILE} 中找到有效数据")
        exit(1)

# 处理数据
    print(f"\n开始处理 {len(input_df)} 个alpha_id...")
    print("提示: 按Ctrl+C可中断程序并自动保存当前结果")
    process_data(session, input_df, OUTPUT_FILE)

# 打印最终限流状态
    with prod_corr_lock:
        remaining_time = max(0, prod_corr_reset_time - time.time())
        print(f"\n处理完成! 结果已保存到 {OUTPUT_FILE}")
        print(f"最终状态: 剩余查询次数 {prod_corr_remaining}, 重置时间 {remaining_time:.2f} 秒后")

---

## 讨论与评论 (18)

### 评论 #1 (作者: ZZ31673, 时间: 6个月前)

多谢大佬提供的代码！即插即用！亲测有效！

祝大佬VF高高！BASE多多！早日GM！

===============================================================================

A man can succeed at almost anything for which he was unlimited enthusiasm

只要有无限的热情，一个人几乎可以在任何事情上取得成功

===============================================================================

---

### 评论 #2 (作者: HH54988, 时间: 6个月前)

第3步配置好后运行，显示文件不存在的报错

---

### 评论 #3 (作者: ZZ37826, 时间: 6个月前)

感谢大佬提供的代码，想问一下，这个代码一天大概能检测多少alpha的prod corr，是不是只有在未提交满4个alpha的时候才可以检测呢？会影响自身的alpha模拟吗？

===============================================================================

栽一棵树最好的时间是十年前，其次是现在。

The best time to plant a tree was ten years ago. The second best time is now.​

===============================================================================

---

### 评论 #4 (作者: DQ66419, 时间: 6个月前)

@ [ZZ37826](/hc/en-us/profiles/33841678941207-ZZ37826)  按照大佬分享的内容看，是24小时600个。
“是不是只有在未提交满4个alpha的时候才可以检测呢？”---代码中调用的 [/correlations/prod](https://api.worldquantbrain.com/alphas/%7Balpha_id%7D/correlations/prod) 这个接口，交满4个也没有影响，只有check接口才会导致失败，prod接口没关系。也不会影响alpha的simulate。

---

### 评论 #5 (作者: LX57490, 时间: 6个月前)

@ [HH54988](/hc/zh-cn/profiles/33421704558103-HH54988)  因为是在上一篇文章的本地自相关基础上进行prod检测，避免无意义的prod检测！

[【新人向-RA的本地self+ppac自相关】复制即用！ – WorldQuant BRAIN](../YH25030/[Commented] 【新人向-RA的本地selfppac自相关】复制即用代码优化.md)

---

### 评论 #6 (作者: LX57490, 时间: 6个月前)

@ [ZZ37826](/hc/zh-cn/profiles/33841678941207-ZZ37826)

1. 一小时可以测25个prod，在这个代码里面我改成20个，确保新手稳定使用！实际一天能测480~600个prod，需要自行改动每小时alpha的prod查询次数！

2.  在上一篇的自相关，加入更严格的筛选条件，以及最大团检测的话，我想应该不必使用prod检测代码了！

并且和提交几个alpha应该没有关系，选择自己prod低以及指标好的alpha，通过alpha_id 打上颜色和名字，使用官方的alpha list 组内自相关即可查看能不能都提交！不过这个方法可能略有误差！

3. 影响模拟的只有“上颜色”，“打tag”，“本地PNL下载”，“上name”，因为一小时两千次查询，如果你有2000个check通过的需要下载PNL的alpha，那么这一个小时，其他回测的alpha就不能打tag和颜色了！

我的prod检测代码对此影响不大！

如果把代码时间等待改短，然后高并发，多次查询未等待，导致一小时多次请求alpha的prod，会导致429限流，从而影响alpha回测！所以需要研究prod检测之间的时间差，找一个稳定的，就可以挂机查询了！

---

### 评论 #7 (作者: CY76111, 时间: 5个月前)

谢谢大佬，好好研读一下

---

### 评论 #8 (作者: Luo Yuchen(YL83778), 时间: 5个月前)

请问上一篇帖子是没有了吗，我没有找到

---

### 评论 #9 (作者: FF65210, 时间: 5个月前)

感谢大佬，我赶紧用上这个提高效率，祝大佬早日GM。

---

### 评论 #10 (作者: ML63985, 时间: 4个月前)

---------------------------------------------------------------------------------------------------------------------------

very good，太好用了，找到了好多ra的漏网之鱼

----------------------------------------------------------------------------------------------------------------------------

---

### 评论 #11 (作者: XW83124, 时间: 4个月前)

非常好用,作为新人直接上手就能用.就是不知道为啥这个帖子我用关键词搜本地检测pc的时候没有排名在前,看的其他帖子没有很好的结果,所以问群友才找到的这个链接.真心推荐,太实用了

---

### 评论 #12 (作者: ML98929, 时间: 4个月前)

请问这个要怎么搞啊

---

### 评论 #13 (作者: MZ45384, 时间: 4个月前)

很有用的代码，太强悍了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #14 (作者: JY55846, 时间: 3个月前)

==============================================================================

非常非常实用，能帮助高效快速的实现找到有信号的因子，加油

==============================================================================

---

### 评论 #15 (作者: YP74336, 时间: 2个月前)

请教大佬，我如果使用这篇的代码，是不是就不用看上一篇帖子了？即这一片代码的功能已经涵盖本地self+ppac自相关检测了？

[【新人向-RA的本地self+ppac自相关】复制即用！ – WorldQuant BRAIN](../YH25030/[Commented] 【新人向-RA的本地selfppac自相关】复制即用代码优化.md)

---

### 评论 #16 (作者: JC84638, 时间: 2个月前)

已讚，很好的分享，但重點仍是 entire 研究流程如何整合此功能，這是需要時間沉澱的問題。

— JZC

---

### 评论 #17 (作者: FZ60707, 时间: 2个月前)

感谢大佬分享这么实用的Prod检测代码！把限流处理和自相关筛选整合到一起，确实省去了不少手动折腾的麻烦。特别是断点续传和分批休息机制，对新人非常友好，挂机检测也更安心了。准备按照帖子里建议的夜间时段跑一跑，希望能高效筛出低相关的优质因子。再次感谢，祝月月高VF！

====================================================================================================================================================================

---

### 评论 #18 (作者: ZM62323, 时间: 1个月前)

请问一下没有成为顾问的账户权限，可以用以上代码吗？

---

