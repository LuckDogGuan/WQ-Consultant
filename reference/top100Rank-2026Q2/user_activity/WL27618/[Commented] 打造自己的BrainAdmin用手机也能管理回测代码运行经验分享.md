# 打造自己的BrainAdmin！用手机也能管理回测代码运行！经验分享

- **链接**: [Commented] 打造自己的BrainAdmin用手机也能管理回测代码运行经验分享.md
- **作者**: HW93328
- **发布时间/热度**: 1年前, 得票: 99

## 帖子正文

# 1.前言

想要制作这个BrainAdmin的原因：1.登录云服务器非常卡（可能是配置低的原因），每次想查看代码运行情况都要被硬控好久。2.在手边没有电脑或者懒得打开电脑的场景下，通过ipad/手机就可以对模板的回测运行进行管理，非常灵活方便。3.将其他一些功能代码集成到系统中，方便使用和管理。

接下来会对系统功能进行逐一介绍，我最看重的还是在ipad和手机上也能进行操作，在没有电脑的场景下还是非常方便的。

ipad端

![图片](images/img_bf804183e6.png)

手机端

![图片](images/img_a31864da2a.png)

整个系统看起来还是比较粗糙的，毕竟是自用嘛，很多细节上都是本着能用就行的程度哈哈哈，也希望有开发经验的大佬能够提出指点（手动抱拳~）

# 2.模板回测管理功能介绍

首先来介绍构建这个系统的初衷，用来管理回测代码运行的部分，接下来的展示为了方便都以PC网页为例。

整个模板管理页面可以分为三个部分：

![图片](images/img_35b6277857.png)

①.左侧一列是模板启动/关闭 管理面板

启动模板进行回测：在表单中填入Region、Universe、dataset等参数，点击开启，该回测程序就会在后端启动起来，当然这里需要填入的参数也因程序和模板的不同而需因人而异。

后端启动回测程序的代码如下：

```
# 每次运行前清空日志with open('tmp2.log', 'w') as f:    pass  # 启动一个子进程运行回测程序，并且传入所需参数process = subprocess.Popen(['python', 'templates2.py', region, universe, dataset, njobs],stdout=open('tmp2.log','a'), stderr=subprocess.STDOUT)print(f"PID of tmp2: {process.pid}")# 保存该程序对应的进程template_processes['tmp2'] = process# 更新Template表中的状态Template.objects.filter(template_name=template_name).update(status=1)
```

点击停止，后端会根据找到对应的子进程关闭，并发送关闭成功的通知

![图片](images/img_e5fa885f93.png)

推送信息相关的代码在论坛中也有大佬分享过，有兴趣可以搜索一下~

②.模板状态信息

这个数据表中保存了所有模板的信息，方便确认当前模板的运行状态

③.统计每小时的回测数量

在这个系统中设置了一个定时任务，每到整点时就触发函数获取上一个小时的回测数量，若是连续三个小时的回测数量都是0，则会发送通知警告回测数量的异常（时间宝贵！）

获取数量的代码之后放在评论区中。

模板日志查看功能：

该功能可以方便通过网页随时查看回测程序的运行情况

![图片](images/img_42167bf6f3.png)

# 3.其他功能介绍

一、输入alpha_id 就可以进行提交alpha，省去在网页上等待的时间~

![图片](images/img_a99f5bf061.png)

二、在这个系统中我获取了已提交因子，将其信息放在表中方便进行数据分析。当然也可以再做一个表格，获取一些满足条件的unsubmitted 因子，方便进行筛选。

![图片](images/img_48635dec74.png)

待完善：主页上也可以放一些数据类的内容，目前是简单设计了一下，图中数据均为随机填写，后面可以通过brain api获取。

![图片](images/img_e21955487d.png)

以上就是本文的全部内容啦，觉得有用的话还麻烦点个小赞啦~也希望大佬们提供些思路，这个系统中还能填充进哪些实用内容！

---

## 讨论与评论 (14)

### 评论 #1 (作者: XC66172, 时间: 0年前)

感谢大佬分享~ 这种前端展示数据很实用

可以了解一下这个BRAIN ADMIN是用什么制作的吗？（是python的哪个库吗）

另外在手机和iPad操作 是通过打开某个URL网页来访问吗？

========================================

fighting labubu!

========================================

---

### 评论 #2 (作者: WL27618, 时间: 0年前)

你简直是我知己! 我也是用前端传参管理模版, 除了我功能没这么多. 不支持这么多设备, 还有我不是用子进程, 是直接用tmux会话启停单个儿模版任务的

=================================================================================

---

### 评论 #3 (作者: JX79797, 时间: 0年前)

先点赞 再评论 太强了

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #4 (作者: VW73191, 时间: 0年前)

太厉害了，手动点赞，太适合我这种板砖人了，不知道是否可以分享这个工具?

---

### 评论 #5 (作者: ZH87224, 时间: 0年前)

技术栈能否分享一下

---

### 评论 #6 (作者: HW93328, 时间: 0年前)

由于定时获取每小时回测数量的代码比较长，所以单独放在评论区，有需要的同学可以看看：

这里面有一些是我自己分装的函数，比如sendmessage用于推送消息，还有一些django框架中用于操作数据库的函数，整体逻辑就是这样的。

```
def count_perHour():    s = login()    now = datetime.now()    print(f"[获取回测数量] Running count_perHour at {datetime.now()}")    # 检查，不要有重复数据    now_hour = now.replace(minute=0, second=0, microsecond=0)    # 检查当前小时是否已存在数据    exists = SimulateCountPerHour.objects.filter(end_datetime__year=now.year,                                                 end_datetime__month=now.month,                                                 end_datetime__day=now.day,                                                 end_datetime__hour=now.hour).exists()    if exists:        print(f"该小时 {now_hour} 的数据已存在，跳过插入。")        return None  # 或者返回之前的 count 值等    start_datetime = now - timedelta(hours=13)    end_datetime = now - timedelta(hours=12)    end_date = end_datetime.strftime("%Y-%m-%d")    end_time = end_datetime.strftime("%H:%M:%S")    start_date = start_datetime.strftime("%Y-%m-%d")    start_time = start_datetime.strftime("%H:%M:%S")    # 用于获取每小时回测的数量    url = (        f"https://api.worldquantbrain.com/users/self/alphas?limit=10&offset=0"        "&status=UNSUBMITTED%1FIS_FAIL"        f"&dateCreated%3E={start_date}T{start_time}-04:00&dateCreated%3C{end_date}T{end_time}-04:00"    )    max_retries = 5  # 设置最大重试次数    retries = 0    while retries < max_retries:        try:            response = s.get(url)            data = response.json()            count = data["count"]            # 保存到数据库            SimulateCountPerHour.objects.create(end_datetime=now,count=count)            print(f"[保存回测数量] {datetime.now()} 回测数量为: {count}")            # 检查是否连续三个小时全部为0            latest_records = SimulateCountPerHour.objects.all().order_by('-end_datetime')[:3]            if all(record.count == 0 for record in latest_records):                sendMessage("⚠️ 最近3小时内回测数量均为0，请注意！")            return count        except (requests.HTTPError, KeyError) as e:            print(f"请求失败: {e}, 正在尝试重新请求... (尝试次数: {retries + 1}/{max_retries})")            retries += 1            time.sleep(10)    SimulateCountPerHour.objects.create(end_datetime=now, count=0)    latest_records = SimulateCountPerHour.objects.all().order_by('-end_datetime')[:3]    if all(record.count == 0 for record in latest_records):        sendMessage("⚠️ 最近3小时内回测数量均为0，请注意！")    print("已达到最大重试次数，无法获取数据。默认填充0")    sendMessage(f"获取回测count已达到最大重试次数，无法获取数据。默认填充0")    return 0  # 达到最大重试次数后返回None
```

---

### 评论 #7 (作者: HW93328, 时间: 0年前)

这个BrainAdmin目前没有完整代码分享和试用哈，系统里的核心功能和代码思路也在文中分享了，大家有兴趣也可以自己搭建一个~我这个系统是基于django框架搭建的，为了简化工作量也没有用到前端的框架。django这个框架还是比较简单的，没开发经验的同学找下教学视频也能很快学会。希望这篇帖子能对大家有所帮助！

---

### 评论 #8 (作者: HW93328, 时间: 0年前)

为了让获取回测数量的函数每小时自动运行，代码中实用到了apscheduler库

```
from apscheduler.schedulers.background import BackgroundScheduler
```

```
# 全局变量保存调度器实例_scheduler = Nonedef start_scheduler():    global _scheduler    # 避免在 reloader 进程中启动调度器，避免启动两次    if os.environ.get('RUN_MAIN') == 'true':        print("This is the reloader process. Scheduler not started.")        return    if _scheduler is not None:        print("Scheduler already running.")        return    _scheduler = BackgroundScheduler()    from app01.utils.util_funcs import count_perHour    # 每小时整点运行一次任务    _scheduler.add_job(        count_perHour,        'cron',        minute=0  # 整点执行    )    _scheduler.start()    print("Scheduler started and will run every hour at :00")
```

---

### 评论 #9 (作者: XM75236, 时间: 0年前)

您很棒,愿不愿意共创.
如果愿意的化,请给我github地址,我会定期根据issue提供代码

============================================================

================业精于勤荒于嬉,行成于思毁于随===================

============================================================

---

### 评论 #10 (作者: ZX59531, 时间: 0年前)

感谢大佬分享，请问这个软件是在哪里获取？

---

### 评论 #11 (作者: HZ20306, 时间: 0年前)

感谢您的分享，阅读完本贴感觉收获良多，可以问一下您这套系统前后端使用了哪些技术栈吗？

---

### 评论 #12 (作者: SW66069, 时间: 11个月前)

太强了，狠狠点赞

---

### 评论 #13 (作者: TB73554, 时间: 10个月前)

感谢大佬分享，真的对于外出没有电脑很有用。

---

### 评论 #14 (作者: SM90987, 时间: 10个月前)

大佬这个页面做的很漂亮，但是我没写过前端框架，只能先用python脚本执行了，不过受到很大启发，我也尝试构建自己的admin系统，谢谢

---

