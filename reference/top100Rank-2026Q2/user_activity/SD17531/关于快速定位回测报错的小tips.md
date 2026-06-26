# 关于快速定位回测报错的小tips

- **链接**: 关于快速定位回测报错的小tips.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 20

## 帖子正文

各位顾问好,在我们回测alpha的过程中,总会由于这样那样的情况,导致发给服务器去回测的数据存在一点问题,这时候就会导致回测报错,页面会返回一个报错的URL,通常情况下,我们需要点开返回给我的报错信息URL,然后从那里面的每一个child去再次复制打开,才能看到具体的错误信息,这个方式太过繁琐了.所以我简单写了一个python函数,直接在IDE里面查看具体的错误信息,代码如下:def filter_non_cancelled_results(s, url):try:# 使用 session 对象发送请求获取 URL 的内容response = s.get(url)response.raise_for_status()  # 检查请求是否成功data = response.json()# 提取 children 列表children = data.get("children", [])# 存储非 CANCELLED 状态的结果non_cancelled_results = []# 遍历 children 列表中的每个元素for child_id in children:# 构建新的 URLnew_url = f"https://api.worldquantbrain.com/simulations/{child_id}"try:# 使用 session 对象发送请求获取新 URL 的内容child_response = s.get(new_url)child_response.raise_for_status()  # 检查请求是否成功child_data = child_response.json()# 检查状态是否不是 CANCELLEDif child_data.get("status") != "CANCELLED":non_cancelled_results.append(child_data)except requests.RequestException as e:print(f"请求 {new_url} 时出错: {e}")# 避免请求太快,这个可以修改sleep(1)# 打印非 CANCELLED 状态的结果for result in non_cancelled_results:print(result)except requests.RequestException as e:print(f"请求 {url} 时出错: {e}")except ValueError as e:print(f"解析 JSON 数据时出错: {e}")filter_non_cancelled_results(s, 'https://api.worldquantbrain.com/simulations/*******')只会把出现error的child信息打印出来,报错信息可能如下:{'id': '***', 'type': 'REGULAR', 'status': 'ERROR', 'message': 'Attempted to use unknown variable ***', 'location': {'line': 3, 'start': 116, 'end': 117, 'property': 'regular'}}{'id': '***', 'type': 'REGULAR', 'status': 'ERROR', 'message': 'Attempted to use unknown variable ***', 'location': {'line': 3, 'start': 117, 'end': 118, 'property': 'regular'}}

---

## 讨论与评论 (3)

### 评论 #1 (作者: QH29412, 时间: 1年前)

平台最近经常有operator 权限和 field 字段的调整，您这个可以打印cancel 那个切片中，定位到没有权限child 的alpha 表达式么？非 CANCELLED报错好像很少。

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

@QH29412这个报错信息,网页上只给到我们这么多数据,所以单从网页报错的角度,无法定位到具体的alpha表达式.但是,使用jupyter跑代码的的时候,还是可以很方便的找到你的这个报错的一批代码的pool的排序的,你可以大概看一下jupyter打印出来的数据是第几条,根据这个去找到你传入的pool的具体十个alpha,然后打印出来看看其中哪一个表达式包含了没有权限的field或者operator.不过我个人不是很建议这种方式哈,因为一个field或者operator没有权限的时候,报错是一大片的,实际上大概率你这批simulation已经无法满足你原先的需求了,这个时候更应该做的是修改你的代码,去掉所有会出现报错的表达式,datafield基本上是整个数据集都没有权限都要去掉,才能顺利跑其他没有错误的表达式.

---

### 评论 #3 (作者: QH29412, 时间: 1年前)

感谢您的回复！您遇到的问题，可能跟我的不同。没有权限的数据集无法查询到，我是习惯跑之前，先看一下数据集的基本情况。

---

