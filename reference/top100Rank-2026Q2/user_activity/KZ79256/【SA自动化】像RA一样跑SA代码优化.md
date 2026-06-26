# 【SA自动化】像RA一样跑SA代码优化

- **链接**: 【SA自动化】像RA一样跑SA代码优化.md
- **作者**: KZ79256
- **发布时间/热度**: 1年前, 得票: 71

## 帖子正文

SA自动化跑和RA自动化跑是一样的，只不过给的json文件不太一样。这篇post大概说一下流程，由于我是基于数据库跑的，所以没法完全放到这

selection和combo的一些候选项（有些是收集群里的，或者根据自己的东西定义的，这里面的颜色PURPLE是我在user阶段提交的alpha的标记）

```
selections = {    "POSITIVE": [        '1',        'own* (1-self_correlation)',        'own* (1-prod_correlation)',        'own* (1-turnover)',        'own* (1-self_correlation*turnover)',        'own* (1-prod_correlation*turnover)',        'own* (1-prod_correlation*turnover*self_correlation)',        'own* (1-self_correlation)*(1-turnover)',        'own* (1-prod_correlation)*(1-turnover)',        'own* (1-prod_correlation)*(1-self_correlation)',        'own* (1-prod_correlation)*(1-turnover)*(1-self_correlation)',        'own* (1-self_correlation)*turnover',        'own* (1-prod_correlation)*turnover',        '\r\nx = if_else(category == "PRICE_MOMENTUM", 2, 1); y = if_else(category == "PRICE_REVERSION", 0.5, 1); z = (long_count * x * y - short_count); if_else(turnover > 0.2, nan, z)',        '!in(datacategories, "pv")',        '!in(datacategories, "pv") && !in(datacategories, "analyst")',        '(!in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE") * 1/turnover',        '(!in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE") * turnover',        '(in(datacategories, "option") || in(datacategories, "model")) && (os_start_date > "2012-06-01" && color!="PURPLE") * turnover',        '(in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE") * 1/turnover',        '1/(long_count / sqrt(universe_size(universe)) )',        'in(datacategories, "analyst")',        'in(datacategories, "pv") && os_start_date > "2012-06-01" && color!="PURPLE"',        'is_nan(1);\r\n# universe_size("minvol1m");\r\n!in(datacategories, "pv") && !in(datacategories, "analyst")',        'long_count / sqrt(universe_size(universe)) ',        'long_count / sqrt(universe_size(universe)) * (turnover < 0.2)',        'long_count / sqrt(universe_size(universe)) * (turnover > 0.15)',        'not(in(datacategories, "fundamental")) * (1-self_correlation)',        'turnover<0.1 && (os_start_date > "2012-06-01" && color!="PURPLE") * 1/turnover',        'turnover>0.1 && turnover<0.2 && (os_start_date > "2012-06-01" && color!="PURPLE") * turnover',        'turnover>0.15 && (os_start_date > "2012-06-01" && color!="PURPLE") * turnover',    ],    "NON_ZERO": [    ],    "NON_NAN": [    ]}combo = [    '1',    "combo_a(alpha)",    'stata = generate_stats(alpha);\r\na = stata.pnl;\r\nts_mean(a, 20)/ts_std_dev(a, 20)\r\n',    'stata = generate_stats(alpha);\r\na = stata.pnl;\r\nts_mean(a, 40)/ts_std_dev(a, 40)\r\n',    'stata = generate_stats(alpha);\r\na = stata.pnl;\r\nts_mean(a, 250)/ts_std_dev(a, 250)\r\n',    'stata = generate_stats(alpha);\r\na = stata.returns;\r\nts_mean(a, 20)/ts_std_dev(a, 20)\r\n',    'stata = generate_stats(alpha);\r\na = stata.returns;\r\nts_mean(a, 40)/ts_std_dev(a, 40)\r\n',    'stata = generate_stats(alpha);\r\na = stata.returns;\r\nts_mean(a, 250)/ts_std_dev(a, 250)\r\n',    'stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr',    # 'stats = generate_stats(alpha); ts_ir(stats.pnl, 20) ',    # 'stats = generate_stats(alpha); ts_ir(stats.pnl, 250) ',    # 'stats = generate_stats(alpha); ts_ir(stats.returns, 250)',    # 'stats = generate_stats(alpha); ts_ir(stats.turnover, 20) ',    # 'stats = generate_stats(alpha); ts_ir(stats.turnover, 250)',    # 'stats = generate_stats(alpha); ts_ir(stats.turnover, 3) ']
```

生成跑的数据，遍历UNIVERSE, NEUTRALIZATION

```
sim_data_list = []for cfg.universe in cfg.UNIVERSE[cfg.region]:    for cfg.neutralization in cfg.NEUTRALIZATION[cfg.region]:        for selectionLimit in [10, 15, 20, 25, 30, 50]:            for selectionHandling in selections.keys():                for item_selection in selections[selectionHandling]:                    for item_combo in combo:                        item_data = {                            "type":"SUPER",                            "settings":{                                "nanHandling":"OFF",                                "instrumentType":"EQUITY",                                "delay": cfg.delay,                                "universe": cfg.universe,                                "truncation": 0.01,                                "unitHandling":"VERIFY",                                "selectionLimit": selectionLimit,                                "selectionHandling": selectionHandling,                                "pasteurization":"ON",                                "region": cfg.region,                                "language":"FASTEXPR",                                "decay": 5,                                "neutralization": cfg.neutralization,                                "visualization": False,                                "testPeriod":"P2Y",                            },                            "combo":item_combo,                            "selection":item_selection,                        }                        sim_data_list.append(item_data)
```

`sim_data_list` 和 一二三阶段代码里的fo_alpha_list是一致的，可以用直接用来跑，不过需要注意的是，SA一共3个插槽，每个插槽只能一次跑1个

下面是我从我的代码里抽出来的跑的代码，首先是可以用于single和multi的跑的代码

```
def simulate_alphas(data):    """    data: simulation data    return alpha list    """    cfg.check_session_timeout()    if len(data) != 1:        simulation_response = cfg.sess.post('https://api.worldquantbrain.com/simulations', json=data)        simulation_progress_url = simulation_response.headers['Location']        simulation_progress = wait_get(simulation_progress_url)        try:            children = simulation_progress.json()["children"]        except:            cfg.log_message('error', f'simulate_alphas_error {simulation_progress.status_code}, {simulation_progress.text}')            raise ValueError('children')    else:        simulation_response = cfg.sess.post('https://api.worldquantbrain.com/simulations', json=data[0])        simulation_progress_url = simulation_response.headers['Location']        children = simulation_progress_url.split('/')[-1]        children = [children]    alphas = []    for i in range(len(children)):        child_progress = wait_get(f'https://api.worldquantbrain.com/simulations/{children[i]}').json()        try:            assert child_progress['status'] in ['COMPLETE', 'WARNING', 'CANCELLED'], cfg.log_message('error', f'{data[i]}, {child_progress}')            assert child_progress['status'] in ['COMPLETE', 'WARNING']            alphas.append(child_progress['alpha'])        except:            alphas.append(None)    return alphas
```

这是调用上述函数跑的函数

```
for batch in simulate_alphas:     simulate_alphas([batch])
```

可以进一步改成3个并行跑的

---

## 讨论与评论 (10)

### 评论 #1 (作者: EL94401, 时间: 1年前)

感谢分享价值含量高的文章，非常有启发。

---

### 评论 #2 (作者: SJ65808, 时间: 1年前)

请问wait_get是自定义的辅助函数还是哪个库函数？

---

### 评论 #3 (作者: KZ79256, 时间: 1年前)

[SJ65808](/hc/en-us/profiles/25875982235543-SJ65808)  是我自定义的辅助函数，差不多是这个样子

```
def wait_get(url: str, max_retries: int = 10) -> "Response":    """    发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。    此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。       Args:        url (str): 目标 URL。        max_retries (int, optional): 最大重试次数，默认为 10。       Returns:        Response: 请求的响应对象。    """    retries = 0    while retries < max_retries:        while True:            simulation_progress = sess.get(url)            if simulation_progress.headers.get("Retry-After", 0) == 0:                break            time.sleep(float(simulation_progress.headers["Retry-After"]))        if simulation_progress.status_code < 400:            break        else:            time.sleep(2 ** retries)            retries += 1    return simulation_progress
```

---

### 评论 #4 (作者: JR23144, 时间: 1年前)

请问一下 cfg 里面的内容怎么获取呢

---

### 评论 #5 (作者: JT77454, 时间: 1年前)

谢谢分享，很有帮助的帖子！

---

### 评论 #6 (作者: FF56620, 时间: 11个月前)

跑起来了，特别感谢，让我可以在没理解sa前先跑起来，更助于学习

---

### 评论 #7 (作者: CW49566, 时间: 9个月前)

感谢分享

---

### 评论 #8 (作者: TW27682, 时间: 7个月前)

我的天，sa也可以自动跑了吗？厉害啊，学习了

---

### 评论 #9 (作者: ER48854, 时间: 7个月前)

感谢分享

---

### 评论 #10 (作者: CC73983, 时间: 6个月前)

又捡了一些selection和combo  感谢楼主

---

