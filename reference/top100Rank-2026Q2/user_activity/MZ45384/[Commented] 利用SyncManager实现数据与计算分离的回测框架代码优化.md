# 利用SyncManager实现数据与计算分离的回测框架代码优化

- **链接**: [Commented] 利用SyncManager实现数据与计算分离的回测框架代码优化.md
- **作者**: LT59611
- **发布时间/热度**: 6个月前, 得票: 6

## 帖子正文

- **前言**

实现数据与计算分离的回测框架，主要解决两个问题：
          1）可以随时停止回测，修改回测代码，继续回测。

2）可以随时修改回测并发数。在需要手动在官网回测的时候，可以降低后台回测并发数，空一个回测额度给官网回测，官网回测完成后，可以随时调整回台回测，最大化回测效率。

- **原理**

利用multiprocessing.managers.SyncManager，实现多进程（可以跨机器）数据共享。管理数据与后台回测分离，多个python进程独立运行：
        sim_context.py，保持回测参数（是否停止，回测并发数），因为它很简单，所以只要操作系统不挂，它不会挂。
        sim_main.py， 回测程序，在这里回测，过程中随时读取sim_context里的（是否停止，回测并发数），并报告tick（时间，sim_context或者其它监控程序可以知道）
       怎么修改回测参数（是否停止，回测并发数）？模仿sim_main.py写一个修改回测参数的脚本即可。

- **代码**

sim_context.py

```
from multiprocessing.managers  import  SyncManager,DictProxyimport timeimport signalimport sys# 全局变量：保存Managerg_manager = None # 共享对象def signal_handler(signum, frame):    """跨平台退出信号处理函数"""    print(f"\n收到退出信号 {signum}，开始优雅清理...", flush=True)      if g_manager:        g_manager.shutdown()        print("Manager已关闭", flush=True)    # 3. 退出主进程    sys.exit(0)# 注册内置的dict方法（名称可自定义，如get_dict）GLOBAL_SHARED_DICT = {"stop": False,"multi":1, "tick": ""}# ========== 2. 定义获取单例字典的方法（关键：返回同一个实例） ==========def get_global_dict():    return GLOBAL_SHARED_DICT# ========== 3. 注册方法到SyncManager ==========class MySyncManager(SyncManager):    pass# 注册“获取单例字典”的方法（禁止新建，只返回已有实例）MySyncManager.register('get_global_dict',    callable=get_global_dict,    proxytype=DictProxy  # 强制生成字典代理)if __name__ == '__main__':    # 注册退出信号（Ctrl+C）    signal.signal(signal.SIGINT, signal_handler)    g_manager = MySyncManager(address=('0.0.0.0', 5000), authkey=b'my_secret_key')    g_manager.start()    # 为什么必须新建一个连接，才能get_global_dict()?    managerCli = MySyncManager(address=('127.0.0.1', 5000), authkey=b'my_secret_key')    managerCli.connect()    print("后台服务器启动，端口5000，按Ctrl+C退出")    shared_dict = managerCli.get_global_dict()       try:
```

```
        last_snapshot = shared_dict['tick']              while True:            # 获取当前快照            current_snapshot = shared_dict['tick']                  # 对比快照，检测变化            if current_snapshot != last_snapshot:                last_snapshot = current_snapshot                print(f"tick {current_snapshot}")                      time.sleep(1)  # 每1秒检查一次，不占用CPU    except KeyboardInterrupt:        #兜底捕获Ctrl+C（防止信号处理函数未生效）        signal_handler(signal.SIGINT, None)    except Exception as e:        print(f"主进程异常：{e}", flush=True)        signal_handler(signal.SIGINT, None)
```

sim_main.py

```
from multiprocessing.managers  import  SyncManager,DictProxyimport timeclass MySyncManager(SyncManager):    pass# 注册与服务器一致的方法MySyncManager.register('get_global_dict',proxytype=DictProxy  # 必须和服务器端匹配)if __name__ == '__main__':    manager = MySyncManager(address=('127.0.0.1', 5000), authkey=b'my_secret_key')    manager.connect()    # 获取共享字典    shared_dict = manager.get_global_dict()    # 1. 读取（验证能读）    print("修改前：", shared_dict)      # 2. 修改顶层键值（直接赋值，生效）    shared_dict['tick'] = time.strftime("%m-%d %H:%M:%S")    # 3. 验证修改生效    print("修改后：", shared_dict)  
```

---

## 讨论与评论 (7)

### 评论 #1 (作者: HZ99685, 时间: 6个月前)

小白看不懂啊，大佬。

---

### 评论 #2 (作者: LG87838, 时间: 6个月前)

我是通过json文件，设置一个计算器，比如2000条暂停，尝试下一个，用了一段时间确实不够灵活。redis又有点复杂，这个可以，很简洁。

谢谢分享。

---------------------------------------------------------------------------

慢慢来，相信时间的力量。

---------------------------------------------------------------------------

---

### 评论 #3 (作者: OY62064, 时间: 6个月前)

感谢大佬的分享，这个工具不错，先试试看~

---

### 评论 #4 (作者: QQ68782, 时间: 6个月前)

学习了, 回测限制之后似乎用不到了

------------------------------------------------------------------------------------------------------------------

知识就是力量

---

### 评论 #5 (作者: JX14975, 时间: 6个月前)

跨机器响应的版本对我来说还是太超前了...我连如何运用跨机器的布置都没有头绪...当然也可能只是太懒了，不想建立与维护太多数据库...不管怎么说，先膜拜大佬，然后加入收藏夹，择日学习。

---

### 评论 #6 (作者: YQ84572, 时间: 6个月前)

有点高级的架构，不过回测限制限制数量了貌似不太能用上

谢谢分享。

---------------------------------------------------------------------------

感谢大佬的分享，祝大佬vf0.9+

---------------------------------------------------------------------------

---

### 评论 #7 (作者: MZ45384, 时间: 6个月前)

简单来说就是异步并发，随时停止吗，有点不太懂，但感觉挺高级的。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

