# 【SA回测优化】回测前先确认selcect的alpha数量是否不低于指定的阈值代码优化

- **链接**: [Commented] 【SA回测优化】回测前先确认selcect的alpha数量是否不低于指定的阈值代码优化.md
- **作者**: SZ83096
- **发布时间/热度**: 1年前, 得票: 61

## 帖子正文

之前自动化回测superalpha的时候，发现有时候select条件可能过于严，导致跑出来的sa,select的数量过少，一直想给回测的代码加上确认select数量不低于指定阈值的功能，上周末终于实现了，有需要的小伙伴可以参考下：

```
def get_super_selection_count(    simulation_data):    """    向 api.worldquantbrain.com 发送 GET 请求，获取 count 字段值simulation_data 是个dict，回测superalpha时的 json 参数值    """    url = "https://api.worldquantbrain.com/simulations/super-selection?"    global s    select=simulation_data["selection"]    region=simulation_data["settings"]["region"]    delay= simulation_data["settings"]["delay"]    instrumentType=simulation_data["settings"]["instrumentType"]    limit=10    selectionLimit=simulation_data["settings"]["selectionLimit"]    selectionHandling= simulation_data["settings"]["selectionHandling"]    select_endoce=urllib.parse.quote(select)    print("select_count:")    querys=f"settings.instrumentType={instrumentType}&settings.region={region}&settings.delay={str(delay)}&limit={str(limit)}&selectionLimit={str(selectionLimit)}&selectionHandling={selectionHandling}&selection={select_endoce}"    try:        response = s.get(f"{url}{querys}",timeout=15)        if response != None:            json_response = response.json()            return json_response["count"]  # 返回 count 字段值    except requests.exceptions.RequestException as e:        print(f"请求失败: {e}")        return None    except ValueError:        print("响应内容不是合法的 JSON")        return None
```

上面的函数放到代码中，然后在发送回测super alpha之前，加上以下代码：

```
alpha_lowset_num=100       select_count=get_super_selection_count(sim_data)if select_count != None and select_count < alpha_lowset_num :    print(f"select alpha 数量少于 {alpha_lowset_num},跳过回测 {select_count},switch")    print(json.dumps(sim_data_list))   # 下面再添加一行代码，用于跳出你本次回测这个superalpha 的代码，比如continue 等
```

![图片](images/img_261b2dba59.png)

---

## 讨论与评论 (3)

### 评论 #1 (作者: MG88592, 时间: 1年前)

感谢橘子姐的分享，现在sa手动回测不仅等待时间长，网页还经常卡崩溃。为了微调一个参数或者稍微降低pc 可能需要坐着调好几个小时，十分恼火。
希望贴主继续分享有用的帖子，祝愿橘子姐vf继续新高。
==============================================================================

---

### 评论 #2 (作者: YX50005, 时间: 11个月前)

谢谢橘子姐的分享！刚想要这个功能就拿到了即插即用的代码，简直不要太巴适

祝愿橘子姐vf继续新高

～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

---

### 评论 #3 (作者: DZ31817, 时间: 9个月前)

20250928

------------------------------------------------------------------------------------------

感谢分享，对sa来说一般选中的alpha数量要在30个以上才有意义，才能体现统计学的力量（大数定律，中心极限定理），使组合中的alpha之间互相放大彼此的优点，弥补彼此的缺点，若小于30则可能不会产生这样的效果。楼主分享的这个工具很实用。

---

