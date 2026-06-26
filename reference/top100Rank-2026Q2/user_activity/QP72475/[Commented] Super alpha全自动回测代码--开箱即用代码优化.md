# Super alpha全自动回测代码--开箱即用！代码优化

- **链接**: [Commented] Super alpha全自动回测代码--开箱即用代码优化.md
- **作者**: HW93328
- **发布时间/热度**: 1年前, 得票: 208

## 帖子正文

功能省流：随机生成selection表达式，与自定义combo表达式组合进行不间断的super alpha回测，可自定义limit、地区、中心化等选项。

特点：整合了中文论坛中的super alpha代码，点击即用

感谢JL16510大佬的多线程回测代码，感谢WP88606大佬的随机生成表达式代码。我对这两篇代码做了整合，并做了一些调整，目前用该代码生成提交了几个比赛的super alpha，指标都还可以，遂分享给大家，希望能有所帮助！

有用的话还请帮忙点个小赞！

回测程序（运行这个）superAlpha.py

```
import threadingfrom machine_lib import *import randomimport selection_expressions as seneutralization_list = ["NONE","MARKET","SECTOR","INDUSTRY","SUBINDUSTRY"]conditions = [    se.category_conditions(),    se.color_conditions(),    se.neutralization_conditions(neutralization_list),    se.datacategories_conditions(),    se.datacategory_count_conditions(),    se.dataset_count_conditions(),    se.datafield_count_conditions(),    se.long_count_conditions(),    se.short_count_conditions(),    se.operator_count_conditions(),    se.prod_correlation_conditions(),    se.self_correlation_conditions(),    se.truncation_conditions(),    se.turnover_conditions(),    se.os_start_date_conditions]weight_expressions = se.weight_expressions()# 貌似author的选项用不了def author_setting():    # 从这些条件中随机选择1-2个 拼接起来返回    author_option = ["author_returns_to_drawdown>2&&","author_returns_to_drawdown<4&&","author_fitness >= 2&&","author_sharpe >= 2&&"]    # 随机选择1到2个条件    selected_conditions = random.sample(author_option, random.randint(1, 2))    # 拼接条件字符串    result = ''.join(selected_conditions)    return resultdef find_selection_expression():    condition_length = random.randint(1, 3)    condition_list = random.sample(conditions, condition_length)    choice_conditions = []    for condition in condition_list:        if callable(condition):            condition = condition()        choice_conditions.append(random.choice(condition))    choice_weight_expression = random.choice(weight_expressions)    # author_exp = author_setting()    select_expression = "not(own)&&"+"in(classifications, 'POWER_POOL')&&" + ' * '.join([f'({exp})' for exp in (choice_conditions + [choice_weight_expression])])    with open('select_expression.txt', 'a') as f:        f.write(select_expression + '\n')    return select_expressiondef get_combo_code_list():    time_windows1 = [60,120,250,500]    selected_window1 = random.choice(time_windows1)    time_windows2 = [250, 500]    selected_window2 = random.choice(time_windows2)    ret = ['1',           f'stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, {selected_window2}); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr',           ]    return retdef multi_simulate2_sa(alpha_pools, neut, region, universe, start):    global s    s = login()    brain_api_url = 'https://api.worldquantbrain.com'    limit_of_concurrent_simulations = len(alpha_pools[0])    alpha_pools_2 = [multi_alphas for pool in alpha_pools for multi_alphas in pool]    end = len(alpha_pools_2)    print(f'length:{len(alpha_pools_2)}, start:{start}')    counter: int = start    lock = threading.Lock()    def sim_task(pools=alpha_pools_2, region=region, universe=universe, neut=neut):        while True:            global s            lock.acquire()            nonlocal counter            if counter > end - 1:                lock.release()                break            if (counter - start) % 250 == 0:  # re-login after every 60 multi_sims                s = login()            local_counter = counter            counter += 1            lock.release()            task = pools[local_counter]            sim_data_list = generate_sim_data_sa(task, region, universe, neut)            sim_data=sim_data_list[0]            try:                simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=sim_data)                print(simulation_response)                simulation_progress_url = simulation_response.headers['Location']                # simulation_progress_url = simulation_response.headers.get('location')            except:                print(" loc key error")                sleep(60)                s = login()            print(f"task {local_counter} post done")            try:                while True:                    simulation_progress = s.get(simulation_progress_url)                    if simulation_progress.headers.get("Retry-After", 0) == 0:                        break                    # print("Sleeping for " + simulation_progress.headers["Retry-After"] + " seconds")                    sleep(float(simulation_progress.headers["Retry-After"]))                status = simulation_progress.json().get("status", 0)                if status != "COMPLETE":                    print(f"Not complete : {simulation_progress_url}")                #alpha_id = simulation_progress.json()["alpha"]                # children = simulation_progress.json().get("children", 0)                # children_list = []                # for child in children:                #     child_progress = s.get(brain_api_url + "/simulations/" + child)                #     alpha_id = child_progress.json()["alpha"]                #                #     set_alpha_properties(s,                #             alpha_id,                #             name = "saTest",                #             color = None,)            except KeyError:                print(f"look into: {simulation_progress_url}")            except Exception as e:                print(f"An error occured:{e}")            print(f"task {local_counter} simulate done")    t = []    for i in range(limit_of_concurrent_simulations):        t.append(threading.Thread(target=sim_task))        t[i].start()    for i in range(limit_of_concurrent_simulations):        t[i].join()    print("Simulate done")def generate_sim_data_sa(alpha_list, region, uni, neut):    sim_data_list = []    for selection_exp, combo_exp in alpha_list:        print(selection_exp)        print(combo_exp)        simulation_data = {            'type': 'SUPER',            'settings': {                'instrumentType': 'EQUITY',                'region': region,                'universe': uni,                'delay': 1,                'decay': 6,                'neutralization': neut,                'truncation': 0.08,                'pasteurization': 'ON',                'unitHandling': 'VERIFY',                'nanHandling': 'ON',                'selectionHandling': random.choice(['POSITIVE','Non-Zero']),                'selectionLimit': random.choice([100,200,500]),                'language': 'FASTEXPR',                'visualization': False,            },            'selection': selection_exp,            'combo': combo_exp}        sim_data_list.append(simulation_data)    return sim_data_listif __name__ == '__main__':    while True:        selection_exp = []        exp = find_selection_expression()        selection_exp.append(exp)        combo_exp = get_combo_code_list()        sa_list = [(i, j) for i in selection_exp for j in combo_exp]        print(len(sa_list))        print(sa_list[0])        pools = load_task_pool(sa_list, 1, 3)        # print(pools[0])        region_dict = {"usa": ("USA", ["TOP3000", "TOP1000","TOP500", "TOP200"]),                       "asi": ("ASI", ["MINVOL1M"]),                       "eur": ("EUR", ["TOP2500", "TOP1200","TOP800", "TOP400"]),                       "glb": ("GLB", ["TOP3000", 'MINVOL1M']),                       "hkg": ("HKG", ["TOP800", "TOP500"]),                       "twn": ("TWN", ["TOP500", "TOP100"]),                       "jpn": ("JPN", ["TOP1600", "TOP1200"]),                       "kor": ("KOR", ["TOP600"]),                       "chn": ("CHN", ["TOP2000U"]),                       "amr": ("AMR", ["TOP600"])                       }        norm_opt = ["INDUSTRY", "SUBINDUSTRY", "MARKET", "SECTOR"]        risk_opt = ["FAST", "SLOW", "SLOW_AND_FAST"]        r1 = ['STATISTICAL']        cr = ["CROWDING"]        co = ["COUNTRY"]        no = ["NONE"]        neut_opt = {"USA": norm_opt + cr + risk_opt + r1,                    "GLB": co + r1,                    "EUR": co + cr + norm_opt + risk_opt + r1,                    "ASI": co + cr + norm_opt + risk_opt + no,                    "CHN": norm_opt + cr + risk_opt + r1,                    "KOR": norm_opt,                    "TWN": norm_opt,                    "HKG": norm_opt,                    "JPN": norm_opt,                    "AMR": ["COUNTRY"] + norm_opt,                    }        regi = ['usa','asi','eur','glb']        random.shuffle(regi)        for k in regi:            for i in region_dict[k][1][:1]:                print(i)                for j in neut_opt[k.upper()]:                    print(j, region_dict[k][0])                    multi_simulate2_sa(pools, j, region_dict[k][0], i, 0)
```

然后是随机生成selection表达式的代码，放到selection_expressions.py中

```
import datetimedef category_conditions():    values = "NONE", "PRICE_REVERSION", "PRICE_MOMENTUM", "VOLUME", "FUNDAMENTAL", "ANALYST", "PRICE_VOLUME", "RELATION", "SENTIMENT"    return [f"category == \"{value}\"" for value in values]def color_conditions():    values = "NONE", "RED", "YELLOW", "GREEN", "BLUE", "PURPLE"    return [f"category == \"{value}\"" for value in values]def dataset_conditions(dataset):    return [f"in(datasets, \"{dataset}\")"]def favorite_conditions():    return [f"favorite", "not(favorite)"]def long_count_conditions():    return [f"long_count > universe_size(universe) * {percent}" for percent in [0.2, 0.3, 0.4, 0.5]]def short_count_conditions():    return [f"short_count > universe_size(universe) * {percent}" for percent in [0.2, 0.3, 0.4, 0.5]]def name_conditions(name):    return [f"name == \"{name}\""]def neutralization_conditions(neutralizes):    return [f"neutralization == \"{value}\"" for value in neutralizes]def operator_count_conditions():    return [f"operator_count <= {cnt}" for cnt in [1, 2, 4, 6, 8, 10]]def tags_conditions(tag):    return [f"in(tags, \"{tag}\")"]def truncation_conditions():    return [f"truncation <= {value}" for value in [0.01, 0.05, 1]]def turnover_conditions():    return [f"turnover < {value}" for value in [0.05, 0.1, 0.2, 0.3, 0.7]]def universe_conditions(universes):    return [f"universe == \"{value}\"" for value in universes]def universe_size_conditions(size=1000):    return [f"universe_size(universe) >= {size}"]def datafields_conditions(field):    return [f"in(datafields, \"{field}\")"]def dataset_count_conditions():    return [f"dataset_count <= {value}" for value in [1, 2, 3, 10]]def self_correlation_conditions():    return [f"self_correlation <= {value}" for value in [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]]def prod_correlation_conditions():    return [f"prod_correlation < {value}" for value in [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]]def os_start_date_conditions():    today = datetime.datetime.today()    delta_days = [7, 14, 30, 60, 90, 120, 180, 360, 3600]    dates = [(today-datetime.timedelta(day)).strftime('%Y-%m-%d')             for day in delta_days]    return [f"os_start_date > \"{date}\"" for date in dates]def datacategories_conditions():    values = "analyst, broker, earnings, fundamental, imbalance, insiders, institutions, \        macro, model, news, option, other, pv, risk, sentiment, shortinterest, socialmedia".split(',')    return [f"in(datacategories, \"{value.strip()}\")" for value in values]def datacategory_count_conditions():    return [f"datacategory_count <= {value}" for value in [1, 2, 3, 10]]def datafield_count_conditions():    return [f"datafield_count <= {value}" for value in [1, 2, 3, 5, 10]]def weight_expressions():    return [        "turnover", '10-turnover',        '10000-abs(long_count-short_count)', 'long_count+short_count', 'long_count', 'short_count',        '10-dataset_count',        '2-self_correlation',        '2-prod_correlation',        '100-datafield_count',        '1'    ]
```

运行 superAlpha.py就可以开始自动回测啦~

当然该代码还有很多小问题，希望大佬们可以继续完善！

都看到这了，点个赞再走吧~~

---

## 讨论与评论 (63)

### 评论 #1 (作者: MY27687, 时间: 1年前)

=========================================MY27687====================================

感谢大佬提供的自动回测super alpha代码，最近正在研究回测super alpha的框架，提供了思路，还有自动随机生成selection_expressions，并引入多线程，全程自动，太感谢了！！！！

====================================================================================

---

### 评论 #2 (作者: AH18340, 时间: 1年前)

感谢大佬分享

---

### 评论 #3 (作者: DX67257, 时间: 1年前)

给大佬点个赞

---

### 评论 #4 (作者: DZ72671, 时间: 1年前)

================

=======非常厉害，没想到sa也可以代码跑======

=======膜拜================

---

### 评论 #5 (作者: DX67257, 时间: 1年前)

```
 'selectionHandling': random.choice(['POSITIVE','Non-Zero']),
```

这行代码有时会报错，Non-Zero应为 NON_ZERO

---

### 评论 #6 (作者: PS11956, 时间: 1年前)

感谢分享，我试着运行了一下，没有成功，报错 loc key error 不知道是什么原因：

not(own)&&in(classifications, 'POWER_POOL')&&(turnover < 0.3) * (in(datacategories, "fundamental")) * (os_start_date > "2025-03-11") * (1)
1
not(own)&&in(classifications, 'POWER_POOL')&&(turnover < 0.3) * (in(datacategories, "fundamental")) * (os_start_date > "2025-03-11") * (1)
stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr
<Response [400]>
 loc key error
<Response [400]>
 loc key error

---

### 评论 #7 (作者: QD44113, 时间: 1年前)

感谢分享！

---

### 评论 #8 (作者: JX79797, 时间: 1年前)

目前还用不上，看起来很有用的样子，mark一下

```
#========= WORLDQUANT BRAIN CONSULTANT ========== ## Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%# sys.setrecursionlimit(α∞) # PnL = ∑(Robustness * Creativity)#无限探索、鲁棒性优先，创新性增值#=================奋进的小徐=======================#
```

---

### 评论 #9 (作者: ZS59763, 时间: 1年前)

很好用的代码，感谢分享 ！！！

---

### 评论 #10 (作者: YX23928, 时间: 1年前)

感谢大佬分享

====================================================================================

---

### 评论 #11 (作者: PB36509, 时间: 1年前)

非常有帮助，感谢分享！

---

### 评论 #12 (作者: CM48632, 时间: 1年前)

感谢大佬分享，代码在跑的过程中，会出现401，429等错误码，简单的测试了一下，可能存在的原因是时间的问题，也就是sleep的时间有些短。
print("Sleeping for " + simulation_progress.headers["Retry-After"] + " seconds")
sleep(60*10)
 **sleep(float(simulation_progress.headers["Retry-After"])) （这行前边 加sleep，让程序休眠时间长一点，应该就行了）** 
时间延长一点，应该就不会报错了

---

### 评论 #13 (作者: QP72475, 时间: 1年前)

最近有比赛，刚好能用上。

---

### 评论 #14 (作者: AM12075, 时间: 1年前)

import selection_expressions as se

这个显示 selection_expressions 未被定义，请问怎么解决

============================================================================================================================================================================================================================================================

---

### 评论 #15 (作者: CL63008, 时间: 1年前)

新的Risk factor 发布了,  “ Reversion and Momentum (RAM)” Factor。

它可以减少对从股票价格数据中得出的均值回归和动量的敞口。

在回测代码中，如何使用新的Risk Factor？

很简单： risk_opt = ["REVERSION_AND_MOMENTUM","FAST", "SLOW", "SLOW_AND_FAST"]

只要把REVERSION_AND_MOMENTUM，添加到list中即可。

---

### 评论 #16 (作者: FZ60707, 时间: 1年前)

================

=======非常厉害，没想到是sa的自动回测，还是开箱即用======

=======膜拜大佬================

---

### 评论 #17 (作者: XL35703, 时间: 1年前)

very helpful ~

---

### 评论 #18 (作者: MS51256, 时间: 1年前)

=======================================================================================
太强了，完美适配目前的比赛，
=-==========================================================================================================================================================================

---

### 评论 #19 (作者: ZZ10277, 时间: 1年前)

谢谢您的分享，目前正处于SA比赛阶段，这个来得很及时，希望以后推出更多的回测工具，谢谢！

---

### 评论 #20 (作者: MM78881, 时间: 1年前)

================================================================================

是的 我拿来直接用好像是有报错问题的，可能是因为我修改了中间条件的原因，因为已经是跨周了，还是得找时间自己重新写一遍，但是这个生成条件的方式还是非常直接学习的，不错不错。感谢大佬

================================================================================

---

### 评论 #21 (作者: HW93328, 时间: 1年前)

很高兴这篇文字能够对大家有所帮助，因为在提交这篇帖子的时候代码还处于初级状态，所以其中不免有一些bug出现，虽然不会直接报错，但也在一定程度上会影响代码的运行。评论区也指出了一些错误，并给出了解决方案，大家可以参考。这里我也来说一些要注意以及可以完善的点：

1.先修改selection表达式到你自己的分组，上传的代码中默认是power_pool的池子。

2.可以进一步探索Location中的url获取super alpha的详细信息，获取alpha_id设置name，desc等信息。

3.在更多地方增加try-catch机制，保证程序的稳健性。

4.重启程序时不要太快，前面的super alpha还没回测完，会报429、401错误，正常201则是发送成功。

---

### 评论 #22 (作者: AL13375, 时间: 1年前)

太强了，膜拜大佬，期待更多的分享！！！

---

### 评论 #23 (作者: LH94963, 时间: 1年前)

感谢大佬分享！太有用了！！期待后续更多分享

---

### 评论 #24 (作者: HW25474, 时间: 1年前)

感谢大佬分享

====================================================================================

---

### 评论 #25 (作者: HW93328, 时间: 1年前)

很高兴这篇帖子能收获这么多顾问朋友的关注，也是体会到了顺势而为的重要性，原本这份代码是我为了super alpha competition比赛临时拼凑修改出来的（因为当时也才解锁权限没什么经验），抱着试一试的心态将这份代码写成了帖子发到了中文论坛，没想到很快就通过了，有很多朋友在评论区留言有用，也有很多朋友指出了代码中的一些错误（由于是初版代码确实不够完美）。这份代码也起到了抛砖引玉的效果，很多大佬在评论区指出修改建议和方向。感谢brain平台提供了这样一个社区，能让大家自由讨论学习！

---

### 评论 #26 (作者: PS11956, 时间: 1年前)

请问大师，这个程序如果中断，如何断点处接着跑呀？

---

### 评论 #27 (作者: BL59663, 时间: 1年前)

大佬的这篇文章值千金！！

---

### 评论 #28 (作者: CC28359, 时间: 1年前)

比赛刚开始的时候可能有些问题，现在对author开头的操作符可以用了。

---

### 评论 #29 (作者: XC66172, 时间: 1年前)

感谢大佬分享的代码，对于现在的SAC比赛很有用~~

脚本selection expression里的color_conditions() favorite_conditions() 是之前没有想过的新奇角度，可以值得尝试一下。

==============================================

每天睡醒就搓搓因子，总有一个是好的

==============================================

---

### 评论 #30 (作者: AM12075, 时间: 1年前)

**<Response [400]>
 loc key error
<Response [400]>
 loc key error**

**这个问题出现的真正原因： `selectionLimit`  超过了所选 universe 的容量** 
你随机从  `[100, 200, 500]`  里抽取  `selectionLimit` ，
但有些 universe（例如  `TOP200` 、 `MINVOL1M` ）根本没有 500 只股票，
API 校验时就直接返回 400。

修复代码建议修改为以下：

1、

```
# ① selectionLimit 不能超过 universe sizeuniverse_cap = {    "TOP3000": 3000, "TOP1000": 1000, "TOP500": 500, "TOP200": 200,    "TOP2500": 2500, "TOP1200": 1200, "TOP800": 800,  "TOP400": 400,    "TOP1600": 1600, "TOP600": 600,  "TOP3000U": 3000,    "TOP800": 800, "TOP500": 500, "TOP100": 100,    "MINVOL1M": 150,             # 实际值以官方文档为准}...uni_size   = universe_cap[uni]limit_pool = [l for l in (100, 200, 500) if l <= uni_size]'selectionLimit': random.choice(limit_pool),
```

2、

```
# ② POST 失败时打印错误并直接 return，避免后续引用未定义变量simulation_response = s.post(url, json=sim_data)if simulation_response.status_code != 201:    print("POST failed:", simulation_response.status_code, simulation_response.text)    return                        # ← 退出本次任务simulation_progress_url = simulation_response.headers['Location']
```

按以上两处修改后，再跑脚本就不会再出现  `<Response [400]> loc key error` ，
线程也不会因为  `simulation_progress_url`  未定义而抛异常。

---

### 评论 #31 (作者: LQ69554, 时间: 1年前)

太棒了，正是需要的时候。感谢分享

---

### 评论 #32 (作者: JL67084, 时间: 1年前)

楼主，出现这个怎么解决"At least 10 component alphas are required for Super Alpha"

---

### 评论 #33 (作者: YL41226, 时间: 11个月前)

请问machine_lib 在哪下载

---

### 评论 #34 (作者: WA25180, 时间: 10个月前)

感谢啦

---

### 评论 #35 (作者: YL41226, 时间: 10个月前)

请问machine_lib在哪里获取

---

### 评论 #36 (作者: YZ42550, 时间: 10个月前)

```
load_task_pool
```

这个函数在哪里呢

---

### 评论 #37 (作者: GC81559, 时间: 10个月前)

很有用

---

### 评论 #38 (作者: GC81559, 时间: 10个月前)

感谢分享

---

### 评论 #39 (作者: BZ93061, 时间: 9个月前)

组Super alpha好思路

---

### 评论 #40 (作者: BW14163, 时间: 9个月前)

感谢大佬分享

---

### 评论 #41 (作者: TB73554, 时间: 9个月前)

谢谢大佬，最近有了权限，但是不知道怎么弄superAlpha，这篇帖子真的拯救我的脑子了。

再次感谢大佬！！！

---

### 评论 #42 (作者: YL57243, 时间: 9个月前)

感谢大佬分享

---

### 评论 #43 (作者: CC85858, 时间: 9个月前)

----------------------------------------------------------------------------------------------------------------------------------------------------感谢分享，今天才开始使用，趁着高vf多跑跑，看看这几天的收益怎么样                                                                                                     ----------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #44 (作者: DL61056, 时间: 9个月前)

谢谢大佬

---

### 评论 #45 (作者: BW14163, 时间: 8个月前)

******************************************************************************************************************
感谢大佬分享，很不错的工具 ，时隔3个月，终于开始用上代码，组SA了，非常激动，目前组USA地区的SA，数量选择了10，15，20. 程序运行3天了，出了200多个结果，其中还有几个3，5的，非常激动。

目前准备在其他地区，做大做强，然后继续组SA。
祝大佬vf高高 ，base多多！！

********************************每天坚持学一个知识点，尽量不混信号，不过拟合***********************

---

### 评论 #46 (作者: PS12239, 时间: 8个月前)

有一个问题请教大佬。注意到代码中是not（own）。目前我是expert，own的话没问题，unsubmitted中会显示跑出来的SA。但是not（own）的话，代码终端会显示Not complete，unsubmitted中没有SA。是我权限的问题吗或者是其他什么问题？望大佬不吝赐教

---

### 评论 #47 (作者: YM62606, 时间: 8个月前)

代码小白，具体修改哪里呢？找不到地方。多谢帮助。

---

### 评论 #48 (作者: KJ35210, 时间: 8个月前)

感谢博主的分享，最近准备开始组SA，想问下若是用代码组SA，会占用正常一二三阶代码的卡槽和线程吗

==============================================
未来属于你，祝好

---

### 评论 #49 (作者: JQ70858, 时间: 8个月前)

感谢分享，新人还未开始组sa，mark一下备用。

---

### 评论 #50 (作者: WL58980, 时间: 8个月前)

很好的文章，标记一下。

---

### 评论 #51 (作者: ZH87224, 时间: 8个月前)

有个小bug，color condition 那里写错了，写成 category 了

---

### 评论 #52 (作者: HL42518, 时间: 8个月前)

_________________________________________________________________________________

太強了,感謝大佬分享~~~~~!!!!!!

___________________________________________________________________________________

---

### 评论 #53 (作者: SZ20589, 时间: 8个月前)

感谢大佬分享，我就是用大佬的帖子的内容跑通并提交了我第一个super alpha。之前对super alpha非常迷茫，都不知道怎么办，看了大佬的文章和代码，豁然开朗，十分感谢大佬

祝愿大佬季季GM， VF经久1.0。

再次感谢大佬

=============================================================================

========Genius is one percent inspiration and ninety-nine percent perspiration.=============

==============================================================================

---

### 评论 #54 (作者: CW49566, 时间: 7个月前)

感谢大佬分享，感觉我要用大佬分享的代码跑出可提交的第一个SA了，好人一生平安。祝大佬每季都是GM。

---

### 评论 #55 (作者: XW84495, 时间: 7个月前)

请问大佬和评论区的各位，ASI地区Max Trade需要开启为ON该怎么修改代码呢？

---

### 评论 #56 (作者: WL21087, 时间: 6个月前)

[AM12075](/hc/en-us/profiles/30421958512663-AM12075)

其实作者文章里提了：

> 然后是随机生成selection表达式的代码，放到selection_expressions.py中

---

### 评论 #57 (作者: CC73983, 时间: 6个月前)

感谢楼主无私的分享 以及评论区各位佬的debug  希望跑出我的第一个sa

---

### 评论 #58 (作者: JZ89937, 时间: 6个月前)

感谢大佬分享

---

### 评论 #59 (作者: YL59387, 时间: 6个月前)

```
请问大家是怎么运行成功的，我运行了superAlpha.py代码报这个错误No module named 'machine_lib'这个模块我去下载了也找不到，请问这个模块大家是自己去下载的吗还是有现成的
```

---

### 评论 #60 (作者: CM48632, 时间: 6个月前)

@ [YL59387](/hc/en-us/profiles/34507261409303-YL59387)  培训课，老师发的一二三阶 代码里面就有 machine_lib.py,拷贝过来，就能有

---

### 评论 #61 (作者: HY20507, 时间: 5个月前)

膜拜大佬，实在是太牛了，对于构建super alpha的萌新来说，雪中送炭

---

### 评论 #62 (作者: BX86068, 时间: 3个月前)

感谢大佬分享，我的代码水平较弱，楼主的贴子给了我很大的启发

---

### 评论 #63 (作者: HL64459, 时间: 2个月前)

感谢大佬代码、已经实操

---

