# 筛选历史回测中满足PPAC的alpha（含代码）代码优化

- **链接**: [Commented] 筛选历史回测中满足PPAC的alpha含代码代码优化.md
- **作者**: DZ31817
- **发布时间/热度**: 1年前, 得票: 27

## 帖子正文

PPAC比赛大幅降低了提交条件，给我们带来了增加收入的机会。我们历史的回测中有大量满足PPAC条件的alpha，可以通过代码筛选出来并挑选提交。其中过于久远的alpha需要重新模拟。此外，提交的时候也要尽可能挑选各项指标好的alpha来提交，毕竟PPAC也影响vf。

代码主要原理是通过machine_lib的get_alpha函数，在返回的response中找到response['results']['is']['checks']]中'name' == 'MATCHES_COMPETITION'并且'result' == 'PENDING'的alpha，即为满足PPAC比赛条件的alpha。

参考代码如下：

![图片](images/img_9a68d08346.png)

---

## 讨论与评论 (7)

### 评论 #1 (作者: HJ33503, 时间: 1年前)

====================================================================================

好思路，这样可以快速筛选到满足比赛的alpha，我之前都没关注到pending这个result，谢谢分享

====================================================================================

---

### 评论 #2 (作者: OB53521, 时间: 1年前)

非常感谢大佬提供的代码，这两天为了比赛非常头疼，尤其是当比赛放低了标准之后，每个alpha都不能直接进行check，因为不想错过可以提交的、表现不错的alpha。通过这套代码能够更加灵活地调节自己筛选alpha的标准，既节约了时间，又能最大限度地在限流的影响下check足够多的alpha！

---

### 评论 #3 (作者: XZ23611, 时间: 1年前)

建议先从已经提交过的alpha里面找OS好的，如果OS差的就不要交了

---

### 评论 #4 (作者: CC21336, 时间: 1年前)

请教一下代码中 simu_name 是代表什么含义？它与 name=alpha_list[j]['name']是有没有什么关系，我需要从哪里获取到这个simu_name ？

---

### 评论 #5 (作者: DZ31817, 时间: 1年前)

CC21336

这个是我自己加的，在alpha表达式的注释中加入这次模拟的一些信息来打标签，筛选的时候就看表达式中是不是包含相关的字符串，来实现筛选的效果，是打tag的方式的一种平替，如果没有使用此种方法可以忽略。

---

### 评论 #6 (作者: JR23144, 时间: 1年前)

博主写的不错， 不过在程序中 ，competition_result 本身就是bool 值， 不需要些 if  competition_result==True   直接写   if competition_result  就行了 并且现在 MATCHES_COMPETITION  已经改成了MATCHES_THEMES

```
# 之前代码不变alpha_list = response.json()["results"]# print(response.json())for j in range(len(alpha_list)):    c_r = True      for k in alpha_list[j]["is"]["checks"]:        if k["name"] == 'MATCHES_THEMES' and k['result']=='PENDING':            c_r = False      if c_r: # 如果不是 满足 ppac的 alpha 则跳过        continue    alpha_id = alpha_list[j]["id"]    name = alpha_list[j]["name"]    dateCreated = alpha_list[j]["dateCreated"]    sharpe = alpha_list[j]["is"]["sharpe"]#接后续代码
```

---

### 评论 #7 (作者: ZZ12657, 时间: 6个月前)

写的不错

---

