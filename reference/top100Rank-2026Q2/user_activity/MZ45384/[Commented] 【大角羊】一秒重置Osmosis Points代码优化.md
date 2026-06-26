# 【大角羊】一秒重置Osmosis Points！代码优化

- **链接**: [Commented] 【大角羊】一秒重置Osmosis Points代码优化.md
- **作者**: AL13375
- **发布时间/热度**: 4个月前, 得票: 4

## 帖子正文

随手写了个根据region和alpha type（regular、super）重置Osmosis Points的代码，供大佬们参考（开箱即用）

```
import requestsimport jsonimport redis# global rdsrds = redis.Redis(host='localhost', port=6380, db=0, decode_responses=True)# 登录并返回 sessiondef login():    res=rds.get('wq_session')    if not res:        from os.path import expanduser        with open(expanduser('brain_credentials.txt')) as f:            credentials = json.load(f)        username, password = credentials        s = requests.Session()        s.auth = (username, password)        res = s.post('https://api.worldquantbrain.com/authentication')        cookies_dict = res.cookies.get_dict()        rds.set('wq_session', json.dumps(cookies_dict), ex=10000)        print(res.content)        return res    cookies = json.loads(res)    session = requests.Session()    session.cookies.update(cookies)     # 重新注入 cookies    return sessiondef reset_oms_point(s, region, type="REGULAR"):    url = (        f"https://api.worldquantbrain.com/users/self/alphas?limit=50&offset=0" + \        f"&status!=UNSUBMITTED%1FIS-FAIL&settings.region=" + region + \        f"&order=-dateSubmitted&hidden=false"    )    if type:        url += f"&type={type}"    resp = s.get(url)    data = resp.json()    results = data.get("results", [])    alpha_scores=[{item['id']:item['osmosisPoints']} for item in results if item['osmosisPoints']]    alpha_scores = sorted(alpha_scores, key=lambda x: list(x.values())[0], reverse=True)    total_score=sum([list(d.values())[0] for d in alpha_scores if list(d.values())[0] is not None])    print(f"当前{region}地区{type} ALPHA OM总分：{total_score}")    print(*alpha_scores, sep="\n")    oms_alphas_ids = [item['id'] for item in results if item['osmosisPoints']]    for id in oms_alphas_ids:        s.patch(f"https://api.worldquantbrain.com/alphas/{id}", json={"osmosisPoints": None})           print(f"重置{region}地区{type} ALPHA OM分数完成！")if __name__ == "__main__":    # 初始化登录会话    session = login()    # USA EUR GLB ASI AMR    region = "AMR"      # REGULAR SUPER NONE    type = ""    # 重置分数    reset_oms_point(session, region, type)
```

需要手动输入的是region和alpha的type，type可以设置为REGULAR、SUPER或者空（如代码中所示）。

最后祝大家的Osmosis rank日日高！！！

---

## 讨论与评论 (2)

### 评论 #1 (作者: YW80612, 时间: 2个月前)

谢谢试试，试试看

---

### 评论 #2 (作者: MZ45384, 时间: 1个月前)

感谢大佬的一键清除osmosis分数代码，但是还要开启redis管理session有点麻烦了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

