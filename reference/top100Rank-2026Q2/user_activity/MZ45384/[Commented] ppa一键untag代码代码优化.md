# ppa一键untag代码代码优化

- **链接**: [Commented] ppa一键untag代码代码优化.md
- **作者**: ZZ81910
- **发布时间/热度**: 2个月前, 得票: 61

## 帖子正文

```
对自己ppa的不满意的小伙伴注意啦，这里提供一份untag ppa的代码。注意：以下代码不能删除ppa+aiac双tag的alpha，所以首先要手动untag这样的alpha。另外，代码一次只能untag100个alpha，总数超过100，要多点几次。不过以上两个问题都可以通过修改代码来解决。另外，通过对代码改造，可以实现自动tag ppa。总之大佬们各显神通吧import requestsfrom os import environfrom time import sleepimport timeimport jsonimport pandas as pdimport randomimport picklefrom itertools import productfrom itertools import combinationsfrom collections import defaultdictimport picklefrom openpyxl import load_workbookfrom openpyxl import Workbookfrom pathlib import Pathimport openpyxldef login():    username = ""    password = ""    # Create a session to persistently store the headers    s = requests.Session()    # Save credentials into session    s.auth = (username, password)    # Send a POST request to the /authentication API    response = s.post('https://api.worldquantbrain.com/authentication')    print(response.content)    print('consultant lib')    return ss = login()alpha_ids = []try:    alphas_url = f'https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=0&status!=UNSUBMITTED%1FIS-FAIL&tag%3DPowerPoolSelected&order=-dateSubmitted&hidden=false'    alphas = s.get(alphas_url)    requests = alphas.json()['results']    for i in requests:        alpha_ids.append(i['id'])except Exception as e:    print(e)print(len(alpha_ids))try:    for alpha_id in alpha_ids:        sleep(0.5)        untag_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"        untag = s.patch(untag_url, json={"tags": []})        print(untag.json())except Exception as e:    print(e)
```

---

## 讨论与评论 (2)

### 评论 #1 (作者: HH34943, 时间: 2个月前)

untag什么意思，这份代码是做什么的

---

### 评论 #2 (作者: MZ45384, 时间: 1个月前)

你就是那位一键untagged然后重新选择一遍，ppa combine上升4+的大佬吗。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

