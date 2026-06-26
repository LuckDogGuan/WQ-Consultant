# 获取super alpha函数（get alpha函数+get yearly-stats函数，判断最近1年sharp是否大于0）代码优化

- **链接**: [Commented] 获取super alpha函数get alpha函数get yearly-stats函数判断最近1年sharp是否大于0代码优化.md
- **作者**: AX58883
- **发布时间/热度**: 1年前, 得票: 2

## 帖子正文

def get_super_ok_alphas(s, start_date, end_date, sharpe_th, fitness_th, turnover, alpha_num, usage):

output = []

output_ok = []

# 3E large 3C less

count = 0

for i in range(0, alpha_num, 100):

print(i)

# 构造查询url

url_e = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \

+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + start_date  \

+ "T00:00:00-04:00&dateCreated%3C" + end_date \

+ "T00:00:00-04:00&is.fitness%3E" + str(fitness_th) + "&is.turnover%3C" + str(turnover) +"&is.sharpe%3E" \

+ str(sharpe_th) + "&order=-is.sharpe&hidden=false&type=SUPER"

url_c = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \

+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + start_date  \

+ "T00:00:00-04:00&dateCreated%3C" + end_date \

+ "T00:00:00-04:00&is.fitness%3C-" + str(fitness_th) + "&is.turnover%3C" + str(turnover) +"&is.sharpe%3E" \

+ str(sharpe_th) + "&order=is.sharpe&hidden=false&type=SUPER"

urls = [url_e]

if usage != "submit":

urls.append(url_c)

for url in urls:

response = s.get(url)

# print(response.json())

try:

print(f"一共找到{response.json()['count']}个super alpha")

alpha_list = response.json()["results"]

#print(response.json())

print(f"当前页 {len(alpha_list)} super alphas found")

for j in range(len(alpha_list)):

checks_data = alpha_list[j]["is"]["checks"]

if checks_data is not None:

print(f"第{j}个 super alpha checks")

has_failed = any(check['result'] == 'FAIL' for check in checks_data)

if not has_failed:

alpha_id = alpha_list[j]["id"]

print(f"当前 no failed 的 alpha_id:{alpha_id}")

while True:

result = s.get(

" [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) "

+ alpha_id

+ "/recordsets/yearly-stats"

)

print(f"获取year 结果 {result}")

if "retry-after" in result.headers:

time.sleep(float(result.headers["Retry-After"]))

else:

print("break")

break

stats = result.json()

# print(stats)

if stats.get("records", 0) == 0:

print(f"当前 no records 的 alpha_id:{alpha_id}")

continue

columns = [dct["name"] for dct in stats["schema"]["properties"]]

yearly_stats_df = pd.DataFrame(stats["records"], columns=columns).assign(alpha_id=alpha_id)

dateCreated = alpha_list[j]["dateCreated"]

sharpe = alpha_list[j]["is"]["sharpe"]

fitness = alpha_list[j]["is"]["fitness"]

turnover = alpha_list[j]["is"]["turnover"]

margin = alpha_list[j]["is"]["margin"]

decay = alpha_list[j]["settings"]["decay"]

exp = alpha_list[j]['combo']['code']

count += 1

if yearly_stats_df.loc[yearly_stats_df.index[-1], 'sharpe'] > 0:

rec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]

output_ok.append(rec)

print(rec)

else:

rec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]

output.append(rec)

# print(rec)

# output.append(alpha_id)

# count = count + 1

else:

print(f"当前 failed 的 alpha_id:{alpha_id}")

else:

print(f"第{j}个 super alpha 没有checks")

except Exception as e:

print(f"当前异常为{e}")

resp = s.get(' [https://api.worldquantbrain.com/users/self](https://api.worldquantbrain.com/users/self) ')

if  resp.status_code != 200:

print(f"resp 返回值{resp.status_code}")

else:

print("重新登录")

s = sign_in(cfg.username, cfg.password)

print("count: %d"%count)

return output,output_ok

---

## 讨论与评论 (5)

### 评论 #1 (作者: JR23144, 时间: 1年前)

![图片](images/img_c2bc2e2028.png)

请问博主写的这篇文章有何意义呢，是觉得最后一年是正值 OS大概率就是好的是吗，还是有什么特征来筛选因子，博主可以明确一下写这篇文章的启发吗

但是 要提醒博主一下，最后一年的数据中只有一个月哦，这样比较噪音会很大，个人建议可以看最后两年相加来判断哦

---

### 评论 #2 (作者: AH18340, 时间: 1年前)

感谢大佬的分享，我本人也有实现相关的功能，不过可以看到最近一年sharpe目前是只有23年一月20日的数据，数据量太少了，建议可以改成计算近2年数据，或者近3年数据可能比较有参考性。可以等权相加或者加权相加都行。欢迎其他大佬指点。

---

### 评论 #3 (作者: QZ67721, 时间: 1年前)

感谢大佬分享，最近SAC期间确实需要从服务器下载SA数据来进行更进一步的分析。上面的同学们已经讲了用最后一年的sharpe筛选可能存在的弊端，我补充一下。关于相关性的计算，其实是用最近四年的PNL来计算的，所以如果用瞪眼法判断alpha相关性是否过高，需要看最近四年的PNL曲线。考虑到动量效应依旧明显，我也是建议看2021，2022和2023这三年的情况。所谓的厂alpha，大部分就是因为最后两年的Sharpe接近平了才会出现的。

---

### 评论 #4 (作者: AX58883, 时间: 1年前)

感谢大佬的提醒，我是看到一篇帖子是要判断最近几年的sharp情况一个是避免最近几年的收益负数，另一个就是看是不是在最近几年也能保持好的sharp，不过这里的函数就只是对最后一年做判断了，简单的一刀切  [JR23144](/hc/en-us/profiles/28844048981143-JR23144)

---

### 评论 #5 (作者: AX58883, 时间: 1年前)

感谢各位大佬的建议@QZ267721  [AH18340](/hc/en-us/profiles/28845157706135-AH18340)

---

