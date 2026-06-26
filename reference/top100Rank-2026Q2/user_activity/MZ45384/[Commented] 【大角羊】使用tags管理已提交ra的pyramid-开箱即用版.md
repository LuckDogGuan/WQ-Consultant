# 【大角羊】使用tags管理已提交ra的pyramid-开箱即用版

- **链接**: [Commented] 【大角羊】使用tags管理已提交ra的pyramid-开箱即用版.md
- **作者**: AL13375
- **发布时间/热度**: 7个月前, 得票: 6

## 帖子正文

在我看来，已提交的alpha是个人的专属宝藏。它们应该被挖掘利用，而不是已提交就让任不管，实在是太可惜了。

对于已提交的regular alpha和power pool alpha，可以考虑从以下几个方面来挖掘剩余价值：

- 横向点塔：比如将USA中成功点塔的数据集也放到其他地区去跑，一般也会有不错的信号；
- 更换模板：将出信号的alpha所在的数据集用在其他好用的模板中，也可以挖掘出不错的alpha；
- 换中性化

所以我写了一段代码来实现对已提交的alpha分析其点亮的pyramid并将其增添到tags中（只增加不改变原tags），这样就可以在网页上通过tags筛选某数据集下的alpha了。代码如下：

```
import requestsimport jsonimport timefrom collections import defaultdictdef login():    from os.path import expanduser    with open(expanduser('brain_credentials.txt')) as f:        credentials = json.load(f)    username, password = credentials    # Create a session to persistently store the headers    s = requests.Session()    # Save credentials into session    s.auth = (username, password)    # Send a POST request to the /authentication API    response = s.post('https://api.worldquantbrain.com/authentication')    print(response.content)    return sdef get_submited_alphas(s,start_date, end_date, alpha_num, region):    output = []    count = 0    for i in range(0, alpha_num, 100):        print(i)        url="https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % (i)\            + "&status!=UNSUBMITTED%1FIS-FAIL&type=REGULAR" \            +"&dateSubmitted%3E=" + start_date +"T00:00:00-04:00&dateSubmitted%3C" + end_date +"T00:00:00-04:00&order=-dateSubmitted&hidden=false"        if region:            url+="&settings.region="+region        while True:            result = s.get(url)            if "retry-after" in result.headers:                time.sleep(float(result.headers["Retry-After"]))            else:                break        res=result.json()        alpha_list = res["results"]        for j in range(len(alpha_list)):            alpha_id = alpha_list[j]["id"]            name = alpha_list[j]["name"]            dateCreated = alpha_list[j]["dateCreated"]            sharpe = alpha_list[j]["is"]["sharpe"]            fitness = alpha_list[j]["is"]["fitness"]            turnover = alpha_list[j]["is"]["turnover"]            margin = alpha_list[j]["is"]["margin"]            colour = alpha_list[j]["color"]            tags = alpha_list[j]["tags"]            decay = alpha_list[j]["settings"]["decay"]            neutralization = alpha_list[j]["settings"]["neutralization"]            pyramids = []            for sorf in alpha_list[j]["is"]["checks"]:                if sorf['name'] == "MATCHES_PYRAMID":                    for py in sorf['pyramids']:                        pyramids.append(py['name'].split("/")[-1])            count += 1            exp = alpha_list[j]['regular']['code']            rec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay,neutralization,tags,colour,pyramids]            output.append(rec)    print("count: %d" % count)    return output
```

```
region=Nonealpha_num=2000s = login()alphas = get_submited_alphas(s,"2024-01-01", "2025-12-31", alpha_num, region)
```

```
alpha_details=[[i[0],i[-1],i[-3]] for i in alphas]
```

```
alpha_format=defaultdict(list)for i in alpha_details:    alpha_format[i[0]]=list(dict.fromkeys(i[1] + i[2]))
```

```
for i,j in alpha_format.items():    response = s.patch("https://api.worldquantbrain.com/alphas/" + i, json={"tags": j})
```

我相信从已提交alpha中还能挖掘出更多有价值的信息，也欢迎各位大佬分享自己的观点！

---

## 讨论与评论 (1)

### 评论 #1 (作者: MZ45384, 时间: 5个月前)

能展示几个示例或者应用吗，看看效果蛤。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

