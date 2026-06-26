# 自动提交Alpha的接口

- **链接**: [Commented] 自动提交Alpha的接口.md
- **作者**: XX42289
- **发布时间/热度**: 1年前, 得票: 108

## 帖子正文

大家好，我是XX，BRAIN Master, 相信有非常多的人感受到了提交因子的痛苦，这里给一些对python数量的同学一个自动提交因子的代码，希望大家可以喜欢。

Hello everyone, I am XX. I believe that many people have felt the pain of submitting factors. Here is a code for some students who are interested in python to automatically submit factors. I hope you can like it.

```
import datetimeimport osimport timeimport pandas as pdimport requestspd.set_option('expand_frame_repr', False)pd.set_option('display.max_rows', 1000)pd.set_option('display.max_colwidth', 100)def submit_alpha(s, alpha_id):    submit_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit"    attempts = 0    while attempts < 5:        attempts += 1        print(f"Attempt {attempts} to submit {alpha_id}.")        # 第一轮提交        while True:            res = s.post(submit_url)            if res.status_code == 201:                print(f"Alpha {alpha_id} POST Status 201. Start submitting...")                break            elif res.status_code == 400:                print(f"Alpha {alpha_id} POST Status {res.status_code}.")                print(f"Alpha {alpha_id} Already POST.")                print(res.content)                break            elif res.status_code == 403:                print(f"Alpha {alpha_id} POST Status {res.status_code}.")                print(pd.DataFrame(res.json()["is"]["checks"])[['name', 'value', 'result']])                return res.status_code            else:                print(f"Alpha {alpha_id} POST Status {res.status_code}.")                print(res.content)                time.sleep(3)        # 第二轮提交        count = 0        s_t = datetime.datetime.now()        while True:            res = s.get(submit_url)            if res.status_code == 200:                retry = res.headers.get('Retry-After', 0)                if retry:                    count += 1                    time.sleep(float(retry))                    if count % 75 == 0:                        print(f"Alpha {alpha_id} GET Status 200. Waiting... {datetime.datetime.now()-s_t}.")                else:                    print(f"Alpha {alpha_id} was submitted successfully.")                    return res.status_code            elif res.status_code == 403:                print(f"Alpha {alpha_id} GET Status {res.status_code}.")                print(f"Alpha {alpha_id} submit failed. Need Improvement.")                print(pd.DataFrame(res.json()["is"]["checks"])[['name', 'value', 'result']])                return res.status_code            elif res.status_code == 404:                print(f"Alpha {alpha_id} GET Status {res.status_code}.")                print(f"Alpha {alpha_id} submit failed. Time Out.")                break            else:                print(f"Alpha {alpha_id} GET Status {res.status_code}.")                print(f"Alpha {alpha_id} submit failed. Time Out.")                print(res.headers)                print(res.content)                break    return 404if __name__ == '__main__':    s = requests.Session()    # 替换你的信息   s.auth = (username, password)    response = s.post('https://api.worldquantbrain.com/authentication')    # 这里面替换你的alpha_id    submittable_alphas = ['8lwqWpv']    for alpha_id in submittable_alphas:        status_code = submit_alpha(s, alpha_id)
```

---

## 讨论与评论 (21)

### 评论 #1 (作者: ZX69629, 时间: 1年前)

x谢谢大佬

---

### 评论 #2 (作者: YY99247, 时间: 1年前)

请问，返回429是不是由于提交的太多，被封了

---

### 评论 #3 (作者: MJ47574, 时间: 1年前)

十分感谢，我无视了submit时的第一个post请求，导致我的alpha自动提交代码无法正常运行，现在我可以完善他了。

---

### 评论 #4 (作者: WC77208, 时间: 1年前)

有api能查符合需求的id吗

---

### 评论 #5 (作者: TM21476, 时间: 1年前)

你好，我有一个问题，想要请教，如果这样写的话，他这个是不是只是根据httpd状态码来判断是否提交成功，只是申请提交了，而不是真正的提交成功呢？（因为我想要写一个根据他的返回状态来控制提交的次数的小功能）。

---

### 评论 #6 (作者: YL34798, 时间: 1年前)

![图片](images/img_2d1a0b8a6d.png) 大佬，可不可以解释如果我想输入一个比较复杂的表达式，然后像图中这样的，但是平台说不行，我也不知道为什么，就是我想给每个表达式起一个名字，然后代入if—else中，但是每次都不行。可不可以给解答一下，非常感谢

---

### 评论 #7 (作者: HW64723, 时间: 1年前)

请问楼主alphaID还用一个一个换吗

---

### 评论 #8 (作者: MZ40316, 时间: 1年前)

请问这段代码可以直接使用吗，还是有地方修改？如果需要改哪里

---

### 评论 #9 (作者: DZ89754, 时间: 1年前)

这个代码我应该怎么改才能自己直接用

---

### 评论 #10 (作者: PM24407, 时间: 1年前)

非常感谢你的分享，我受益良多，同时我也会尽量分享一些有用的东西出来，祝你alpha高量高质天天交！

---

### 评论 #11 (作者: SX83613, 时间: 1年前)

Status 429      b'{"detail":"THROTTLED"}'  状态码429是被限流了吗

---

### 评论 #12 (作者: JC65152, 时间: 1年前)

有没有如何筛选alpha的代码方法，跑代码时有很多alpha其实是不能通过测试，如果不筛选情况下，每个都submit其实会浪费很多时间，也浪费服务器资源。

---

### 评论 #13 (作者: DM28368, 时间: 1年前)

Thank you for taking the time to share this useful knowledge, Hope to read more quality articles like this from you. I have a question, can this python language check self cor, pro cor with all alpha? and it often has errors when I use it to check multiple alphas at the same time so I still don't know how to fix this? Hope you can answer my question.
Have a nice day!

---

### 评论 #14 (作者: SJ59424, 时间: 1年前)

谢谢，用这套代码交起来方便

---

### 评论 #15 (作者: XX42289, 时间: 1年前)

这里是XX42239，回复一下两位同学的问题
 [SX83613](/hc/en-us/profiles/28885913890071-SX83613)    [YY99247](/hc/en-us/profiles/28858457478679-YY99247)

Status 429      b'{"detail":"THROTTLED"}'  
统一回复一下，出现以上信息，就是你被Ban了，建议休息十分钟再提交，因为提交的次数是有限的。

你会一直报错，直到你拥有了权限

---

### 评论 #16 (作者: XX42289, 时间: 1年前)

```
s.auth = (username, password)
```

```
submittable_alphas = ['8lwqWpv']
```

这个代码是不能直接运行的，你需要修改你自己的用户名和密码（这我肯定没有啊！！你自己要改！！）
另外要修改submittable_alphas的这个列表，在里面加入你想要提交的因子的id

id在url里面可以找到的。一共修改这两个地方就可以运行拉！！

---

### 评论 #17 (作者: XX42289, 时间: 1年前)

[HW64723](/hc/en-us/profiles/28846682458775-HW64723)

回答：请问楼主alphaID还用一个一个换吗？

这里我给出的是一个list，所以你可以一个一个写上去，不用换，

比如你可以写10个进去。

例如

```
submittable_alphas = ['8lwqWpv', '82222pv', '8l3333v', '8lwq444', '8lw5555v', '8lw1111v']
```

当然你也可以自动生成一个list，然后传入，这样就不用手动了，具体的代码需要自己去探索一下了。

---

### 评论 #18 (作者: XX42289, 时间: 1年前)

[JC65152](/hc/en-us/profiles/28903449192343-JC65152)

当然可以获取alpha，试试理解下面这个代码，然后自己写一个函数出来。如果感兴趣的话，后续我也会发个新的帖子

```
url_e = (f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}"         f"&tag%3D{tag}&is.longCount%3E={longCount_th}&is.shortCount%3E={shortCount_th}"         f"&settings.region={region}&is.sharpe%3E={sharpe_th}&is.fitness%3E={fitness_th}"         f"&settings.universe={universe}&status=UNSUBMITTED&dateCreated%3E={start_date}"         f"T00:00:00-04:00&dateCreated%3C{end_date}T00:00:00-04:00&type=REGULAR&color!={color_exclude}&"         f"settings.delay={delay}&settings.instrumentType={instrumentType}&order=-is.sharpe&hidden=false&type{super_tag}")response = s.get(url_e)
```

---

### 评论 #19 (作者: XX42289, 时间: 1年前)

[YL34798](/hc/en-us/profiles/28914132150295-YL34798)

大佬，可不可以解释如果我想输入一个比较复杂的表达式，然后像图中这样的，但是平台说不行，我也不知道为什么，就是我想给每个表达式起一个名字，然后代入if—else中，但是每次都不行。可不可以给解答一下，非常感谢

回答一下这个问题，你写的很不错的，你只是漏了 ; 分号

每一句话都需要一个;

最后一行的因子值是不需要;的

---

### 评论 #20 (作者: KZ79256, 时间: 1年前)

话说为什么会有两轮提交哇，一个是post一个是get，是要排除什么特殊情况哇

==============================================================================

---

### 评论 #21 (作者: CW99271, 时间: 10个月前)

楼主你好，我想问下提交是否有限制，每几分钟可以提交一次，一天可以提交多少个？

---

