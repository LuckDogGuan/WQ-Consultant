# 使用浏览器开发者工具查看http请求，用于本地代码请求对应功能经验分享

- **链接**: [Commented] 使用浏览器开发者工具查看http请求用于本地代码请求对应功能经验分享.md
- **作者**: AH18340
- **发布时间/热度**: 1年前, 得票: 43

## 帖子正文

前言：

worldquant平台在网页端提供了很多功能，但是需要我们手动在浏览器操作费时费力。如回测alpha我们改成了本地用代码跑，但是有些其他功能我们也想要实现怎么办呢？这里将介绍使用浏览器的开发者工具来查看请求路径和请求参数，实现本地请求相关功能。

1.浏览器开发者工具介绍

这里推荐使用谷歌浏览器，在对应网页中可以使用f12快捷键打开开发者工具，或者如下图所示打开

![图片](images/img_6f7862d6e7.png)

开发者工具如下图所示，主要看network网络这里

![图片](images/img_07921aa0c6.png)

2.查看Neutralization=“RAM"的回测使用什么参数

在页面上选中对应选项

![图片](images/img_2bf81723e4.png)

打开开发者工具，清空前面的请求，点击回测

![图片](images/img_452b181ed6.png)

这时候我们可以在开发中工具上看到调用的请求路径和参数

![图片](images/img_bb6a8c5ed5.png)

![图片](images/img_7160c6d0bb.png)

这样我们只需要在代码中传“REVERSION_AND_MOMENTUM”就能进行RAM中性化的模拟回测

3.查看计算prod_correlation的接口

照例打开开发者工具，清空列表，点击查看prod_correlation的按钮

![图片](images/img_34e3fb357c.png)

在开发者工具上可以看到请求路径

![图片](images/img_65d1eb6154.png)

结束之后可以查看返回值

![图片](images/img_b32314faad.png)

根据与页面上的值进行对比，prod_correlation值是这个max值

![图片](images/img_9c9cab839a.png)

这样我们就可以构造Get  [https://api.worldquantbrain.com/alphas/{alphaId}/correlations/prod](https://api.worldquantbrain.com/alphas/{alphaId}/correlations/prod)  解析返回值 获得prod_correlation,结合数据库就可以将测的结果存在数据库中，不用一个打开页面查看，直接筛选数据库，找到合适的alpha进行提交

4.Performance Comparison 也可以根据如此使用本地调用查看提交后加分多少，然后筛选合适加分选项提交super alpha

---

## 讨论与评论 (11)

### 评论 #1 (作者: ZL42615, 时间: 1年前)

这么好的一篇文章，对于向类似我这种新人，程序再弱一些的来说，绝对是福音。能否再说详细一些会更好理解些，最好能附上相关的模板示例说明，可能会更生动形象些。期待大佬的继续干货分享！！

---

### 评论 #2 (作者: HW93328, 时间: 1年前)

感谢分享，之前一直想用api获取一些信息，在平台上找到的api说明文档也没有特别搞懂，最终还是在中文论坛上寻找各位大佬代码中使用到的api连接才获取到数据。原来在打开网页的时候在控制台就可以找到对应的api连接，非常实用，感谢楼主，马上投入实践！

===========================================

---

### 评论 #3 (作者: KM27775, 时间: 1年前)

获取prod_correlation的python代码：

> def product_corr(alpha_id):
> session = login()
> if not session:
> return {"code":1,"msg":"Could not login"}
> try:
> res= session.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod](https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod) ")
> print(res.text)
> while True:
> if res.status_code == 200:
> print(f"Alpha {alpha_id} GET Status 200")
> break
> if res.status_code == 201:
> print(f"Alpha {alpha_id} GET Status 201. Start submitting...")
> elif res.status_code == 400:
> print(f"Alpha {alpha_id} GET Status {res.status_code}.")
> print(f"Alpha {alpha_id} Already GET.")
> print(res.content)
> break
> elif res.status_code == 403:
> print(f"Alpha {alpha_id} GET Status {res.status_code}.")
> #print(pd.DataFrame(res.json()["is"]["checks"])[['name', 'value', 'result']])
> return {"code":1,"msg":f"Alpha {alpha_id} GET Status {res.status_code}.",'msg_code':-1}
> else:
> print(f"Alpha {alpha_id} GET Status {res.status_code}.")
> print(res.content)
> sleep(3)
> print(res.json()['max'])
> except requests.exceptions.RequestException as e:
> print(str(e))
> sleep(20)
> jsonData = product_corr(alpha_id)
> return jsonData

---

### 评论 #4 (作者: LG87838, 时间: 1年前)

感谢分享，对于新人熟悉worldquant的API非常有帮助。

还可以通过类似postman等api工具记录测试，把api统一整理起来，方便后续的测试和使用。

-----------------------------------------------------------------------------------------------------------------

---

### 评论 #5 (作者: FL39657, 时间: 1年前)

对于代码新手来说真的很有用，之前一直想用一些功能但是找不到api接口，因此迟迟没有优化代码，看了楼主分享的帖子之后，恍然大悟

---

### 评论 #6 (作者: QP72475, 时间: 1年前)

感谢分享，以后可以自己查看接口和返回数据了。

---

### 评论 #7 (作者: SD17531, 时间: 1年前)

学到了啊, 以后需要找什么API请求地址,直接在网页上发起请求,然后监控新请求就行了,甚至请求参数都包含在里面了. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 什么时候才能跟大佬一样牛逼

---

### 评论 #8 (作者: CC28359, 时间: 1年前)

可以使用一些常见的MITM软件，比如mitmproxy并在脚本中加入相应的代理可以更方便分析、同时也支持二次开发。

---

### 评论 #9 (作者: QZ67721, 时间: 1年前)

感谢大佬分享，之前一直在试着修改machine_lib里面的get_alphas函数，但是里面关于网络请求的API地址真的一直写错，导致查询不到结果，出错太多了，搞得我都不干继续尝试，生怕给封了之类的。看了大佬的帖子，我直接在网页上填好了搜索条件，然后打开开发者工具，找到里面的API请求地址，他直接就是一个完整的URL，我直接进行替换就完成任务了。谢谢。

---

### 评论 #10 (作者: BW14163, 时间: 1年前)

感谢大佬分享的思考方式，也感谢评论区大佬分享的PC测试代码，亲自测试非常好用！Wonderful！

---

### 评论 #11 (作者: DZ31817, 时间: 9个月前)

20250928

------------------------------------------------------------------------------------------

感谢分享，有不少想用代码实现的功能，苦于不知道api，只能各种求问大佬，或者翻阅论坛帖子，或者查看官方文档，即使如此一些小众功能的接口也不一定能找得到，这篇帖子分享的方法真是帮了大忙。

---

