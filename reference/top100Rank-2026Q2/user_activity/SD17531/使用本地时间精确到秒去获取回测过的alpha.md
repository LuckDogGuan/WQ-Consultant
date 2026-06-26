# 使用本地时间,精确到秒去获取回测过的alpha

- **链接**: 使用本地时间精确到秒去获取回测过的alpha.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 23

## 帖子正文

模板里面get_alpha函数只能精确到日期, 而且使用的美国时间和我们本地时间有时差.但是通过 查看网页源代码,发现是可以用秒级精度查询alpha的,所以对get_alpha函数做了一点点小小的修改.将次代码复制替换掉原来模板里面的get_alpha函数即可使用.代码如下:

```
import pytzdef convert_to_est(china_time_str):    # 将中国时间字符串转换为datetime对象    china_time = datetime.datetime.strptime(china_time_str, "%m-%d %H:%M:%S")       # 假设年份是当前年份    china_time = china_time.replace(year=datetime.datetime.now().year)       # 定义中国时区和美国东部时区    china_tz = pytz.timezone('Asia/Shanghai')    est_tz = pytz.timezone('US/Eastern')       # 将中国时间转换为UTC时间    china_time = china_tz.localize(china_time)    utc_time = china_time.astimezone(pytz.utc)       # 将UTC时间转换为美国东部时间    est_time = utc_time.astimezone(est_tz)       return est_time.strftime("%Y-%m-%dT%H:%M:%S-05:00")def get_alphas(start_date, end_date, sharpe_th, fitness_th, region, alpha_num, usage):    s = login()    output = []    count = 0       # 转换时间格式    start_date_est = convert_to_est(start_date)    end_date_est = convert_to_est(end_date)       for i in range(0, alpha_num, 100):        print(i)        url_e = "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i) \                + "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + start_date_est  \                + "&dateCreated%3C=" + end_date_est \                + "&is.fitness%3E" + str(fitness_th) + "&is.sharpe%3E" \                + str(sharpe_th) + "&settings.region=" + region + "&order=-is.sharpe&hidden=false&type!=SUPER"        url_c = "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i) \                + "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + start_date_est  \                + "&dateCreated%3C=" + end_date_est \                + "&is.fitness%3C-" + str(fitness_th) + "&is.sharpe%3C-" \                + str(sharpe_th) + "&settings.region=" + region + "&order=is.sharpe&hidden=false&type!=SUPER"        urls = [url_e]        if usage != "submit":            urls.append(url_c)        for url in urls:            response = s.get(url)            try:                alpha_list = response.json()["results"]                print(response.json())                for j in range(len(alpha_list)):                    alpha_id = alpha_list[j]["id"]                    name = alpha_list[j]["name"]                    dateCreated = alpha_list[j]["dateCreated"]                    sharpe = alpha_list[j]["is"]["sharpe"]                    fitness = alpha_list[j]["is"]["fitness"]                    turnover = alpha_list[j]["is"]["turnover"]                    margin = alpha_list[j]["is"]["margin"]                    longCount = alpha_list[j]["is"]["longCount"]                    shortCount = alpha_list[j]["is"]["shortCount"]                    decay = alpha_list[j]["settings"]["decay"]                    exp = alpha_list[j]['regular']['code']                    count += 1                    if (longCount + shortCount) > 100:                        if sharpe < -sharpe_th:                            exp = "-%s"%exp                        rec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]                        print(rec)                        if turnover > 0.7:                            rec.append(decay*4)                        elif turnover > 0.6:                            rec.append(decay*3+3)                        elif turnover > 0.5:                            rec.append(decay*3)                        elif turnover > 0.4:                            rec.append(decay*2)                        elif turnover > 0.35:                            rec.append(decay+4)                        elif turnover > 0.3:                            rec.append(decay+2)                        output.append(rec)            except:                print("%d finished re-login"%i)                s = login()    print("count: %d"%count)    return output
```

那么调用代码的传入参数也会有相应的变化,需要在日期后面加上时分秒,其余保持不变:

```
alphas = get_alphas("01-15 19:20:23", "01-15 22:02:12", 0.0, 0.0, "ASI", 100, "submit")
```

---

## 讨论与评论 (3)

### 评论 #1 (作者: LL87164, 时间: 1年前)

试过了，有用。特别是同一天跑过不同数据集时，靠时间来过滤出想要的alpha。

---

### 评论 #2 (作者: HZ99685, 时间: 8个月前)

试了，但为什么只能跑出指定时间段内的一部分alpha呢？设置检查无误，是不是代码还有bug？

---

### 评论 #3 (作者: HZ99685, 时间: 7个月前)

现在夏令时间过去了是不是应该改一下代码？

---

