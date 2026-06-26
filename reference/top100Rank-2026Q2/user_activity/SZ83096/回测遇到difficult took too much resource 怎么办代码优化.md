# 回测遇到difficult ,took too much resource 怎么办？代码优化

- **链接**: 回测遇到difficult took too much resource 怎么办代码优化.md
- **作者**: SZ83096
- **发布时间/热度**: 7个月前, 得票: 64

## 帖子正文

平台更新或者服务不稳定的时候，代码回测时会经常遇到下面2种回测ERROR的情况：

第一种：

```
{    "id": "xxx",    "type": "REGULAR",    "status": "ERROR",    "message": "There was an error while running the simulation.Please try again or contact BRAIN support if this problem persists."}
```

第二种：

```
{"id": "xxx","type": "REGULAR","status": "ERROR","message": "Your simulation probably took too much resource."}
```

第一种，一般是平台的原因导致的，回测的表达式是没问题的。如果经常遇到这种而不处理直接跳过，可能会遗漏一些有信号的alpha。可以在遇到的时候，将表达式存到json文件，后续补统一回测。

第二种，可能是平台的问题，也可能是表达式确实消耗的资源过大。这种错误，可以通过减少子槽的个数来避免，具体减到多少，看实际情况，一般见到6，7个子槽，就可以了。

分享下代码判断上面2种错误的处理

```
def append_to_jsonl(filename, data):"""追加数据到JSONL文件"""withopen(filename, 'a', encoding='utf-8') as f:    json.dump(data, f, ensure_ascii=False)    f.write('\n') # 每行一个JSON对象
```

```
length=len(simulation_progress.json()["children"])for child_ in range(0,length):    child=simulation_progress.json()["children"][child_]    try:        res=my_get(f"https://api.worldquantbrain.com/simulations/{child}",timeout=15)        err_mes1='There was an error while running the simulation. Please try again or contact BRAIN support if this problem persists'        err_mes2="Your simulation probably took too much resource"        if res.json()["status"] == "ERROR" :            if err_mes1 in res.json()['message']:                append_to_jsonl('brain_difficult.json',[region,universe,neut,alpha_pools[tx][ty]])            if err_mes2 in res.json()['message']:                append_to_jsonl('brain_too_much_resource.json',[region,universe,neut,alpha_pools[tx][ty]])
```

---

## 讨论与评论 (7)

### 评论 #1 (作者: LR93609, 时间: 7个月前)

感谢分享，终于明白第一种的问题所在了，总以为自己做错什么了。

---------------------------------------------------------------------------
Combine：          Σ（深度 × 稳健 × 多样性）
Value factor：     Σ（数量 × 质量 × 独特性）
Weight factor：  Σ（特有贡献 × 投资强度）
---------------------------------------------------------------------------

---

### 评论 #2 (作者: AH18340, 时间: 7个月前)

这个simulations缓存时间为一天，需要在一天之内访问

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #3 (作者: FF56620, 时间: 7个月前)

我之前都以为是一种错误直接放弃掉了，原来是两种错误啊，感谢分享

------------------------------------------
Pursue scalable, repeatable opportunities rooted in probability.

------------------------------------------

---

### 评论 #4 (作者: CC73983, 时间: 7个月前)

有个很奇怪的现象是  第一种错误  换一个alpha就能通过回测  但是重新回测这条又会报这个错

我一直以为是alpha的问题  竟然不是吗  但我出现第一种错误的alpha尝试重新回测好几次  从来没成功过 T T

---

### 评论 #5 (作者: BW14163, 时间: 7个月前)

感谢分享，回测时还有一种情况，比较少见：有时候三更半夜，回测就卡在那里不动弹了，第二天早上，打开云服务器，发现，回测器空跑了一晚上

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

### 评论 #6 (作者: SZ83096, 时间: 6个月前)

[BW14163](/hc/en-us/profiles/28900537669399-BW14163)  我没遇到过这种情况，我会记录每个回测请求回测的时间，如果超过阈值，就主动delete掉，并把表达式存本地，后续再根据情况处理。我感觉，有这种问题的，要么是代码有bug，要么是非python脚本直接运行的方法来回测，图形化的界面来回测，一般比较可能遇到这种问题

---

### 评论 #7 (作者: MY49971, 时间: 3个月前)

感谢大佬分享

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

