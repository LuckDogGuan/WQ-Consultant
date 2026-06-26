# 监控进程和日志，避免回测长时间中断，避免连续回测天数指标清零代码优化

- **链接**: [Commented] 监控进程和日志避免回测长时间中断避免连续回测天数指标清零代码优化.md
- **作者**: LG87838
- **发布时间/热度**: 1年前, 得票: 58

## 帖子正文

成为顾问后 ，云服务器在长期的回测中，出现异常而导致非主观地中断的问题难免会遇到。我的解决方式是：监控回测脚本的进程和回测日志记录。定时检查这两项，如果没有出现异常，就保持静默，继续监测；如果异常，就通过Bark推送告警信息到手机。Bark也是来自论坛里一位大佬的分享，但帖子搜索不到了。和推送邮件，推送feishu等类似。用自己熟悉的就好。

- 通过监测回测脚本的系统进程，可以避免回测脚本的异常退出。

- 通过监测回测脚本的运行日志，可以避免没有向服务器发送回测记录而空转。

- 在每天某个时间点定时推送一条消息，keep alive机制，避免这个监控脚本异常。

以下是监测脚本的代码，修改成自己的回测脚本名称和日志名称即可直接使用。

```
import psutilimport timeimport jsonimport osfrom datetime import datetime, timedeltafrom tools import push_wxclass ProcessMonitor:    def __init__(self):        self.last_alert_time = {}  # 用于存储上次警报时间        self.known_pids = set()    # 用于存储已知的PID        self.pid_to_script = {}    # 用于存储PID到脚本名称的映射        self.json_last_modified = {}  # 用于存储JSON文件的上次修改时间            def check_python_scripts(self):        current_pids = set()        alerts = []        pid_to_script = {}                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):            try:                if 'python' in proc.info['name'].lower():                    cmdline = proc.info['cmdline']                    if cmdline:                        cmdline_str = ' '.join(cmdline)                        for script in [                            # 'async_multi_sim05.py', 'process_sim10.py',                             'process_super.py', 'process_sim001.py']:                            if script in cmdline_str:                                current_pids.add(proc.info['pid'])                                pid_to_script[proc.info['pid']] = script            except (psutil.NoSuchProcess, psutil.AccessDenied):                pass                # 检查是否有进程消失        disappeared_pids = self.known_pids - current_pids        if disappeared_pids:            # 使用上次保存的PID到脚本的映射来获取脚本名称            script_info = []            for pid in disappeared_pids:                if pid in self.pid_to_script:                    script_info.append(f"{self.pid_to_script[pid]} (PID: {pid})")                else:                    script_info.append(f"未知脚本 (PID: {pid})")                        alerts.append(f"警告：以下脚本已停止运行: {', '.join(script_info)}")                # 更新已知PID和PID到脚本的映射        self.known_pids = current_pids        self.pid_to_script = pid_to_script                return alerts    def check_json_files(self):        json_files = {            'process_sim001.py': 'logs/sim_guigu01.log',             'async_multi_sim05.py': '/root/wquant/BackTest/logs/consumer_05.log'        }                alerts = []        current_time = datetime.now()                for script, json_file in json_files.items():            file_path = os.path.join('/root/wquant', json_file)            if not os.path.exists(file_path):                alerts.append(f"警告：配置文件 {json_file} 不存在")                continue                            try:                file_stat = os.stat(file_path)                last_modified = datetime.fromtimestamp(file_stat.st_mtime)                                # 检查文件是否45分钟未更新                if current_time - last_modified > timedelta(minutes=65):                    # 避免重复警告                    if (json_file not in self.last_alert_time or                         current_time - self.last_alert_time[json_file] > timedelta(minutes=45)):                        alerts.append(f"警告：guigu {script} 已超过45分钟未更新")                        self.last_alert_time[json_file] = current_time            except Exception as e:                alerts.append(f"警告：配置文件 {json_file} 出现错误: {str(e)}")                return alerts    def run(self):        print("监控程序已启动，只有在出现异常情况时才会显示警告信息...")        last_keep_alive_date = None  # 记录上次发送keep alive的日期                while True:            alerts = []            alerts.extend(self.check_python_scripts())            alerts.extend(self.check_json_files()            # keep alive 机制：每天上午10:00发送一次            now = datetime.now()            if now.hour == 10 and (last_keep_alive_date is None or last_keep_alive_date != now.date()):                keep_alive_msg = f"[KeepAlive] 监控程序存活，时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"                print(keep_alive_msg)                push_wx(keep_alive_msg)                last_keep_alive_date = now.date()                        if alerts:                print(f"\n=== 警告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")                for alert in alerts:                    print(alert)                    push_wx(alert)                print("-" * 50)                        time.sleep(5)  # 每5秒检查一次if __name__ == "__main__":    monitor = ProcessMonitor()    monitor.run()
```

---

## 讨论与评论 (4)

### 评论 #1 (作者: XC66172, 时间: 1年前)

感谢楼主的分享，避免连续回测天数指标清零的代码非常有必要. 尤其如果你有长途旅行或出差，有时候一不小心就可能错过了。（有两个可能，所有回测都跑完了，你又刚好长时间没去看；或者vs code突然崩溃了，所有程序都没有在跑）

对我来说，因为我也有监控日志，结合楼主的想法，我应该会设置每天定时自动跑类似这样的脚本，去看当天的监控日志里是否跑了任何回测（搜索关键词和当天日期post done?)，如果有推送信息当天已有回测；如果没有则自动跑几条回测，推送信息给自己。这样的话可以让自己更安心些~~

========================================================

每天醒来就搓搓因子，总有一个是好的！ FIGHTING LABUBU

=========================================================

---

### 评论 #2 (作者: YZ70114, 时间: 1年前)

如果有时间有精力，改造现有项目增加任务管理的机制更适合长时间任务的执行

=======================================================================
生活就像海洋 只有意志坚强的人 才能到达彼岸
=======================================================================

---

### 评论 #3 (作者: JR23144, 时间: 1年前)

感谢博主的分享，您的经验很有启发。关于程序监控，我也建立了一套自己的“强提醒”机制。我写了一个监控脚本，当主程序意外中断或崩溃时，它会自动触发一个告警流程。首先，它会在一小时的窗口期内，持续尝试向我的手机邮箱发送警报邮件。考虑到网络可能不稳定导致邮件发送失败，我还设计了一个备用方案（Fallback）：如果邮件在设定时间内无法成功发出，脚本会自动调用电脑的播放器，无限循环播放音乐。这样，即使在断网的情况下，我也能通过这个“物理”声音警报，及时发现程序已崩溃，从而进行手动重启。

===================VF 1.0===========================

---

### 评论 #4 (作者: DZ31817, 时间: 9个月前)

感谢分享，我目前的方法是使用while True和try except等来处理异常情况，但使用过程中还是有些错误是连try except也处理不了的（会导致try except也中断），这种情况下楼主分享的这种监听机制就很实用了。

---

