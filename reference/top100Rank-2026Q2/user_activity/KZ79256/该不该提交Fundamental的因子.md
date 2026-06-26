# 该不该提交Fundamental的因子

- **链接**: 该不该提交Fundamental的因子.md
- **作者**: KZ79256
- **发布时间/热度**: 1年前, 得票: 29

## 帖子正文

众所周不知，一旦某个region的因子超过50个，且Fundamental类的因子占比超过30%之后，Fundamental的因子就会被封禁（模拟也不能进行）。封禁之后只有把Fundamental类因子降到15%之后才能解禁（ [引文](/hc/en-us/articles/22696581922071-How-can-consultants-regain-access-to-the-Fundamental-dataset-category) ）。因此，我就很烦恼该不该交这个Fundamental因子，交了之后会被会被封禁。

因此，我写了一个读取alpha比例的代码，来获得当前region有没有被封禁，如果提交一个会不会被封禁，来快速让我知道我该不该提交这个Fundamental因子

```
import requestsimport pandas as pddef download_base_data():    data_subRatio = []    data_base = []    username = 'xxxx'    password = 'xxxx'    sess = requests.Session()    sess.auth = (username, password)    response = sess.post('https://api.worldquantbrain.com/authentication')    item_data = sess.get('https://api.worldquantbrain.com/users/self/activities/diversity?grouping=region,delay,dataCategory').json()['alphas']    count = pd.DataFrame([item for item in item_data if item['delay'] is not None and item['dataCategory']['id'] is None])    item_data = pd.DataFrame([item for item in item_data if item['dataCategory']['id'] == 'fundamental'])    item_data['dataDiversity'] = item_data['dataDiversity'].apply(lambda x: x['check'])    item_data.drop(columns=['dataCategory'], inplace=True)    item_data = item_data.merge(count[['region', 'delay', 'alphaCount']], on=['region', 'delay'], how='left', suffixes=('', '_sum'))    item_data['ratioCurrent'] = item_data['alphaCount'] / item_data['alphaCount_sum']    item_data['ratioNew'] = (item_data['alphaCount'] + 1) / (item_data['alphaCount_sum'] + 1)    item_data['ratioCurrent'] = item_data['ratioCurrent'].round(2)    item_data['ratioNew'] = item_data['ratioNew'].round(2)    data_subRatio = item_data    return data_subRatiodef highligh_subRatio(row):    if float(row['ratioCurrent']) > 0.3:        return ["background-color: #F59794"] * len(row)    elif float(row['ratioNew']) > 0.3:        return ["background-color: #F0BF4C"] * len(row)    else:        return ["background-color: #81d482"] * len(row)   download_base_data().style.apply(highligh_subRatio, axis=1)
```

出来的结果大概是这样的 ![图片](images/img_c85377b7a0.png)

绿色是放心交，黄色不要交，红色是比例过高

---

## 讨论与评论 (5)

### 评论 #1 (作者: AH18340, 时间: 1年前)

哥，你的账户密码

---

### 评论 #2 (作者: GL61467, 时间: 1年前)

赞一个，厉害了

---

### 评论 #3 (作者: HJ33503, 时间: 1年前)

===================================================================================

好东西，我之前一段时间交了不少的fundamental的，几个地区都被封了，但是fundamental构建的alpha比较稳定，一般不会出现爆雷，尽量控制在30以下比较好，不然之后要到15才能解锁确实麻烦

===================================================================================

---

### 评论 #4 (作者: ZS59763, 时间: 1年前)

按照我的理解，fundamental的数据一般鲁棒性很强，也可以持续，除非基本面发生严重变化（这种做空就完事了），都可以做的。就是做多了会被ban，比较心疼，还得做其他的来对冲一下

---

### 评论 #5 (作者: DZ31817, 时间: 1年前)

20250401

------------------------------------------------------------------------------------------

感谢分享，很实用的工具，我超了30%fnd已被封禁，再想拉回15%还是有难度的。而在fnd比例还在28%、29%的时候就及时收手，并且随着alpha数量的增加再同比例慢慢交fnd看起来是个好方法，至少保留了继续交fnd的机会。

---

