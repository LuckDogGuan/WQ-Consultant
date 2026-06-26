# 多线程遍历回测super alpha代码优化

- **链接**: [Commented] 多线程遍历回测super alpha代码优化.md
- **作者**: JL16510
- **发布时间/热度**: 1 year ago, 得票: 70

## 帖子正文

def multi_simulate2_sa(alpha_pools, neut, region, universe, start):
    global s

s = login()

brain_api_url = ' [https://api.worldquantbrain.com](https://api.worldquantbrain.com) '

limit_of_concurrent_simulations = len(alpha_pools[0])

alpha_pools_2 = [multi_alphas for pool in alpha_pools for multi_alphas in pool]
    # print(alpha_pools_2)

end = len(alpha_pools_2)

print(f'length:{len(alpha_pools_2)}, start:{start}')
    counter: int = start
    lock = threading.Lock()

def sim_task(pools=alpha_pools_2, region=region, universe=universe, neut=neut):
        while True:
            global s
            lock.acquire()
            nonlocal counter
            if counter > end - 1:
                lock.release()
                break
            if (counter - start) % 250 == 0:  # re-login after every 60 multi_sims
                s = login()
            local_counter = counter
            counter += 1
            lock.release()
            task = pools[local_counter]
            sim_data_list = generate_sim_data_sa(task, region, universe, neut)
            sim_data=sim_data_list[0]
            try:
                simulation_response = s.post(' [https://api.worldquantbrain.com/simulations](https://api.worldquantbrain.com/simulations) ', json=sim_data)
                simulation_progress_url = simulation_response.headers['Location']
                # simulation_progress_url = simulation_response.headers.get('location')
            except:
                print(" loc key error")
                sleep(600)
                s = login()

print(f"task {local_counter} post done")

try:
                while True:
                    simulation_progress = s.get(simulation_progress_url)
                    if simulation_progress.headers.get("Retry-After", 0) == 0:
                        break
                    # print("Sleeping for " + simulation_progress.headers["Retry-After"] + " seconds")
                    sleep(float(simulation_progress.headers["Retry-After"]))

status = simulation_progress.json().get("status", 0)
                if status != "COMPLETE":
                    print(f"Not complete : {simulation_progress_url}")

"""
                #alpha_id = simulation_progress.json()["alpha"]
                children = simulation_progress.json().get("children", 0)
                children_list = []
                for child in children:
                    child_progress = s.get(brain_api_url + "/simulations/" + child)
                    alpha_id = child_progress.json()["alpha"]

set_alpha_properties(s,
                            alpha_id,
                            name = "%s"%name,
                            color = None,)
                """
            except KeyError:
                print(f"look into: {simulation_progress_url}")
            except:
                print("other")

print(f"task {local_counter} simulate done")

t = []
    for i in range(limit_of_concurrent_simulations):
        t.append(threading.Thread(target=sim_task))
        t[i].start()

for i in range(limit_of_concurrent_simulations):
        t[i].join()

print("Simulate done")

def generate_sim_data_sa(alpha_list, region, uni, neut):
    sim_data_list = []
    for selection_exp, combo_exp in alpha_list:
        # print(selection_exp)
        # print(combo_exp)
        simulation_data = {
            'type': 'SUPER',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': uni,
                'delay': 1,
                'decay': 6,
                'neutralization': neut,
                'truncation': 0.08,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'selectionHandling': 'POSITIVE',
                'selectionLimit': 1000,
                'language': 'FASTEXPR',
                'visualization': False,
            },
            'selection': selection_exp,
            'combo': combo_exp}

sim_data_list.append(simulation_data)
    return sim_data_list

```
import threading
```

```
from machine_lib import *
```

selection_exp=['turnover<0.15']
combo_exp=['stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr);maxCorr = reduce_max(ic); 1 - maxCorr']
sa_list=[(i,j) for i in selection_exp for j in combo_exp]
print(len(sa_list))
print(sa_list[0])

pools = load_task_pool(sa_list, 1, 3)
# print(pools[0])
region_dict = {"usa": ("USA", ["TOP3000", "TOP1000", "TOP500", "TOP200"]),
               "asi": ("ASI", ["MINVOL1M"]),
               "eur": ("EUR", ["TOP2500","TOP1200", "TOP800", "TOP400"]),
               "glb": ("GLB", ["TOP3000", 'MINVOL1M']),
               "hkg": ("HKG", ["TOP800", "TOP500"]),
               "twn": ("TWN", ["TOP500", "TOP100"]),
               "jpn": ("JPN", ["TOP1600", "TOP1200"]),
               "kor": ("KOR", ["TOP600"]),
               "chn": ("CHN", ["TOP2000U"]),
               "amr": ("AMR", ["TOP600"])}

norm_opt=["INDUSTRY", "SUBINDUSTRY", "MARKET", "SECTOR"]
risk_opt=["FAST","SLOW","SLOW_AND_FAST"]
r1=['STATISTICAL']
cr=["CROWDING"]
co=["COUNTRY"]
no=["NONE"]
neut_opt={"USA":norm_opt+cr+risk_opt+r1,
          "GLB":co+r1,
          "EUR":co+cr+norm_opt+risk_opt+r1,
"ASI":co+cr+norm_opt+risk_opt+no,
"CHN":norm_opt+cr+risk_opt+r1,
          "KOR":norm_opt,
          "TWN":norm_opt,
          "HKG":norm_opt,
          "JPN":norm_opt,
          "AMR": ["COUNTRY"]+norm_opt,
          }

regi = ['usa']
for k in regi:
    for i in region_dict[k][1][:1]:
        print(i)
        for j in neut_opt[k.upper()]:
            print(j, region_dict[k][0])
            multi_simulate2_sa(pools, j, region_dict[k][0], i, 0)

最后说明，该代码的多线程部分是由一位大佬编写，用于回测regler alpha，曾经分享在学习群，我在此基础改编成用于回测super alpha。如果本人看到此贴请留下相关链接，后续加上相关信息。

---

## 讨论与评论 (21)

### 评论 #1 (作者: MG88592, 时间: 1 year ago)

=================================================================
=================================================================
感谢大佬，祝愿大佬继续高base 高VF. 得偿所愿
=================================================================
=================================================================

---

### 评论 #2 (作者: NL80893, 时间: 1 year ago)

佬，请问一下是不是需要先把get alphas函数加入在代码里然后才能进行回测呀

---

### 评论 #3 (作者: JL16510, 时间: 1 year ago)

@ [NL80893](/hc/en-us/profiles/29953598557975-NL80893)  不用，只需要在selection_exp和combo_exp放入表达式就行，官网文档有super alpha相关介绍，论坛也有相关例子。

---

### 评论 #4 (作者: YW36074, 时间: 1 year ago)

感谢大佬，让我有一个更高的起点

---

### 评论 #5 (作者: ZS59763, 时间: 1 year ago)

很好用的方法，点赞。此外要提醒一下，select条件不能太严格，不然select不到10个就等于空跑

---

### 评论 #6 (作者: ML42552, 时间: 1 year ago)

感谢大佬无私分享！

---

### 评论 #7 (作者: ZH39644, 时间: 1 year ago)

感谢大佬的分享。正好要跑sa，界面回测太费时了，测了几次才一个过prod的，用代码应该会好很多！

---

### 评论 #8 (作者: YC99622, 时间: 1 year ago)

感谢大佬开源！隐隐预感最近要更VF了，先学习一波~

---

### 评论 #9 (作者: KD86036, 时间: 1 year ago)

感谢大佬开源，提高了SA的产出效率

---

### 评论 #10 (作者: CC21336, 时间: 1 year ago)

有了大佬的这个代码，我每天都能生产一个Super了，解决了我的Super ALpha 温饱问题

---

### 评论 #11 (作者: XC75618, 时间: 1 year ago)

刚提交第一个alpha感谢大佬开源，祝愿大佬继续高base 高VF高Combined。

---

### 评论 #12 (作者: YP44571, 时间: 1 year ago)

我是个新人，拜读了大佬的文章，用上应该可以批量回测省很多事了。另外想咨询下大佬们？super alpha能用代码自动check吗？大家是怎么实现的啊？要不回测多了，再手工check也是个问题啊

---

### 评论 #13 (作者: YH25030, 时间: 1 year ago)

感谢大佬分享。手搓SA搓到怀疑人生，大佬给的代码要跑起来。

---

### 评论 #14 (作者: JL16510, 时间: 1 year ago)

@ [YP44571](/hc/zh-cn/profiles/29178016678039-YP44571)  函数check_submission也可以check sa，论坛里还有本地测相关性的代码。如果赶时间，也可以直接提交，但可能遇到提交成功但Pro大于0.7的情况，对base有很大惩罚。

---

### 评论 #15 (作者: MH19374, 时间: 1 year ago)

感谢大佬分享。赠人玫瑰，手有余香。

跑下来应该把“

```
import threading
```

”添加到第一个def里。然后把文中前两个放到之前machine lib 文件里。

再创建一个新的super alpha.py， 把最下面的代码输入。然后填写自己的select and combo。和region就可以愉快的运行拉。再也不担心UI上提示运行时间过久的问题拉。

---

### 评论 #16 (作者: GL76608, 时间: 1 year ago)

感谢佬~

---

### 评论 #17 (作者: LL87164, 时间: 1 year ago)

[JL16510](/hc/en-us/profiles/25889743296151-JL16510)

两个设置问题请教：

1. region_dict = {"usa": ("USA", ["TOP3000", "TOP1000", "TOP500", "TOP200"]),

USA 为什么没有“ILLIQUID_MINVOL1M" 和”TOPSP500" 这两项

2. neut_opt={"USA":norm_opt+cr+risk_opt+r1,
      "GLB":co+r1,

GLB 为什么只选这两个中性化选项

---

### 评论 #18 (作者: YZ42550, 时间: 10 months ago)

大佬，请问一下load_task_pool这个函数是啥，是在machine_lib里面吗，machine_lib能够从哪获取呢

---

### 评论 #19 (作者: KJ35210, 时间: 8 months ago)

感谢博主的分享，准备开始组SA，看了博主们的分享，这个select和combine表达式怎么组SA，不断学习中

==============================================
未来属于你，祝好

---

### 评论 #20 (作者: MM27120, 时间: 7 months ago)

新人报道，看了同学的分享感觉学到了点东西 感谢前辈的经验

---

### 评论 #21 (作者: XD90676, 时间: 3 months ago)

想问一下machine_lib这个文件应该从哪里获取，找不到这个文件源码

---

