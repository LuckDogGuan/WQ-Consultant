# [比赛专用]实现本地实时监控Osmosis分数变化

- **链接**: [比赛专用]实现本地实时监控Osmosis分数变化.md
- **作者**: JL16510
- **发布时间/热度**: 6个月前, 得票: 2

## 帖子正文

从12月22日起，Osmosis Competition 2025每天更新各比赛区域daily pnl，每隔几个小时更新osmosisPoints Allocated。即使没有更改每个区域的osmosisPoints Allocated，daily pnl也会随着时间有所变化。为了追踪daily pnl实时变化情况，通过windows自带程序+自编代码，可实现本地监控Osmosis分数实时变化，进而动态优化osmosisPoints Allocated，实现最大化daily pnl争取获得好成绩。代码如下：def get_alphas_os2025():s = login()url= "https://api.worldquantbrain.com/competitions/OC2025"# response = s.get(url)retries = 0max_retries = 10retry_interval = 1while retries < max_retries:try:response = s.get(url, timeout=(10,20))breakexcept requests.exceptions.ReadTimeout:print("上传时间过长，请检查网络或文件大小")retries += 1if retries < max_retries:print(f"{retry_interval}秒后重试...")time.sleep(retry_interval)else:print(f"达到最大重试次数 {max_retries}，放弃请求。")raise SystemExitexcept requests.exceptions.RequestException as e:print("请求失败:", e)print(f"请求失败 ({retries + 1}/{max_retries}): {str(e)}")retries += 1if retries < max_retries:print(f"{retry_interval}秒后重试...")time.sleep(retry_interval)else:print(f"达到最大重试次数 {max_retries}，放弃请求。")raise SystemExitleaderboard = response.json()["leaderboard"]return leaderboardfrom machine_lib_copy import *from datetime import datetime, timedeltaimport pandas as pdusa_time=datetime.now()- timedelta(hours=13)usa_t=usa_time.strftime("%Y-%m-%dT%H:%M:%S-05:00")fo_tracker = get_alphas_os2025()print(fo_tracker)if not fo_tracker:print('none')raise SystemExitdt = pd.DataFrame([fo_tracker])dt['usa_time']=usa_tprint(dt)# 文件路径csv_file = 'os2025.csv'# 检查文件是否存在file_exists = os.path.isfile(csv_file)# 追加数据到 CSVdt.to_csv(csv_file,mode='a',header=not file_exists,index=False,encoding='utf-8')print("数据已成功追加到 CSV 文件")再利用任务计划程序定时运行py脚本（window系统自带），或者利用程序间隔一定时间运行py脚本也行。注意选择创建任务并设置单选每天，勾选重复任务间隔并选择1小时或其他时间（如下）。

---

## 讨论与评论 (0)

