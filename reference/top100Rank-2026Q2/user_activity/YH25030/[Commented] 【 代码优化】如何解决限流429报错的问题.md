# 【 代码优化】如何解决限流429报错的问题

- **链接**: [Commented] 【 代码优化】如何解决限流429报错的问题.md
- **作者**: XB37939
- **发布时间/热度**: 5个月前, 得票: 35

## 帖子正文

## 前言

近期调用api时经常提示api limit，status_code == 429，这就是api限流了。限流后会导致获取不到results，导致代码报错。

比如get_datafields方法datafields_list.append(datafields.json()['results'])时报错

![图片](images/img_e7fe7ea8d4.png)

![图片](images/img_ef15d09944.jpeg)

## 解决方案

添加重试机制即可解决限流问题

![图片](images/img_45e0ad414d.png)

## 代码

### 核心代码：

for x in range(0, count, 50):

datafields = s.get(url_template.format(x=x))

#如果状态是429

while datafields.status_code == 429:

print("status_code 429, sleep 3 seconds")

time.sleep(3)

datafields = s.get(url_template.format(x=x))

datafields_list.append(datafields.json()['results'])

### 普通重试机制，一直循环直到执行成功：

def get_datafields(

s,

instrument_type: str = 'EQUITY',

region: str = 'USA',

delay: int = 1,

universe: str = 'TOP3000',

dataset_id: str = '',

search: str = ''

):

if len(search) == 0:

url_template = " [https://api.worldquantbrain.com/data-fields](https://api.worldquantbrain.com/data-fields) ?" +\

f"&instrumentType={instrument_type}" +\

f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" +\

"&offset={x}"

count = s.get(url_template.format(x=0)).json()['count']

else:

url_template = " [https://api.worldquantbrain.com/data-fields](https://api.worldquantbrain.com/data-fields) ?" +\

f"&instrumentType={instrument_type}" +\

f"&region={region}&delay={str(delay)}&universe={universe}&limit=50" +\

f"&search={search}" +\

"&offset={x}"

count = 100

datafields_list = []

for x in range(0, count, 50):

datafields = s.get(url_template.format(x=x))

#如果状态是429

while datafields.status_code == 429:

print("status_code 429, sleep 3 seconds")

time.sleep(3)

datafields = s.get(url_template.format(x=x))

datafields_list.append(datafields.json()['results'])

datafields_list_flat = [item for sublist in datafields_list for item in sublist]

datafields_df = pd.DataFrame(datafields_list_flat)

return datafields_df

### 进阶代码，重试五次，失败即失败

def get_datafields(

s,

instrument_type: str = 'EQUITY',

region: str = 'USA',

delay: int = 1,

universe: str = 'TOP3000',

dataset_id: str = '',

search: str = ''

):

if len(search) == 0:

url_template = " [https://api.worldquantbrain.com/data-fields](https://api.worldquantbrain.com/data-fields) ?" +\

f"&instrumentType={instrument_type}" +\

f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" +\

"&offset={x}"

count = s.get(url_template.format(x=0)).json()['count']

else:

url_template = " [https://api.worldquantbrain.com/data-fields](https://api.worldquantbrain.com/data-fields) ?" +\

f"&instrumentType={instrument_type}" +\

f"&region={region}&delay={str(delay)}&universe={universe}&limit=50" +\

f"&search={search}" +\

"&offset={x}"

count = 100

datafields_list = []

for x in range(0, count, 50):

datafields = s.get(url_template.format(x=x))

retrycount=5

#如果状态是429

while datafields.status_code == 429 and retrycount > 0:

print("status_code 429, sleep 3 seconds")

time.sleep(3)

datafields = s.get(url_template.format(x=x))

retrycount-=1

datafields_list.append(datafields.json()['results'])

datafields_list_flat = [item for sublist in datafields_list for item in sublist]

datafields_df = pd.DataFrame(datafields_list_flat)

return datafields_df

## 总结

世界上唯一不变的就是变，代码也不是一成不变的，要与时俱进，不断优化。

希望大家可以不断的优化代码，提高效率，早日进阶，多赚dollar

---

## 讨论与评论 (22)

### 评论 #1 (作者: HZ99685, 时间: 5个月前)

感谢大佬的及时贴，对小白来说太有用了！想问下，那是不是machine_lab中的所有函数都要做sleep处理了？包括MCP也是吗？

---

### 评论 #2 (作者: CC73983, 时间: 5个月前)

一般就是多页循环调用查询的时候  直接for循环里time.sleep(2)  每调一次等待2s完事儿～   1s试过不行太短

---

### 评论 #3 (作者: XF30004, 时间: 5个月前)

非常感谢，下午正好碰到了同样的问题，这下就解决了

---

### 评论 #4 (作者: TT21691, 时间: 5个月前)

确实 429这个问题从用户的时候就一直困扰着我，感谢大佬给出更好的解决方案。

---

### 评论 #5 (作者: CM48632, 时间: 5个月前)

缘分一道桥，刚429，就看到大佬的解决方案，强大呀

---

### 评论 #6 (作者: DL61056, 时间: 5个月前)

感谢大佬，很有效

---

### 评论 #7 (作者: XB37939, 时间: 5个月前)

@ [HZ99685](/hc/en-us/profiles/32603557750935-HZ99685)

machine_lab里面的最好都加 mcp的代码我不太熟悉 不建议随便修改

因为你修改的下次升级还会被覆盖~

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #8 (作者: JX39934, 时间: 5个月前)

感谢大佬的及时雨，我邀请的几个新人都是用的老版本的用户回测代码，那个是直接去拉数据集的字段来组因子回测的，所以一阶段回测脚本基本一启动就429了，后面发现是官方获取字段api加了限流，现在是1分钟30次请求，1S最多1次

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #9 (作者: YH25030, 时间: 5个月前)

最近抓取数据集常常碰到429，我是手动重试。现在用您的代码合理地设置等待和重试次数。谢谢分享。

---

### 评论 #10 (作者: JX14975, 时间: 5个月前)

[HZ99685](/hc/en-us/profiles/32603557750935-HZ99685)  与重试有关的部分都要作sleep处理，我上个月有一次写重试忘写sleep了，导致陷入死循环，点停止运行也没有响应（连重启kernel都没有弹出来），不得不关掉整个jupyter notebook，导致回测中断。

---

### 评论 #11 (作者: ER48854, 时间: 5个月前)

最近刚出来的问题，立马就有解决方案，论坛有帮助！

---

### 评论 #12 (作者: DC57744, 时间: 5个月前)

原来是这样，还是得提升自己的代码能力，感谢大佬

---

### 评论 #13 (作者: SC16582, 时间: 5个月前)

太感谢了！

---

### 评论 #14 (作者: YB15978, 时间: 5个月前)

-----------------------------------------------------------------------------------------------------------

感谢大佬无私分享，在simulate 过程中经常出现api rate limited 也是这个原因吧，感谢

-----------------------------------------------------------------------------------------------------------

---

### 评论 #15 (作者: HL81191, 时间: 5个月前)

原来是限流了，昨天获取一个analyst数据集一直失败，我还因为是我没有这个数据集的权限了，后面换了另一个数据集和一个other数据集，现在看应该是字段太多循环太快导致的

---

### 评论 #16 (作者: CZ78575, 时间: 5个月前)

感谢分享，已经修改到我的代码中了，已恢复

---

### 评论 #17 (作者: ZY88181, 时间: 5个月前)

终于有人解决这个问题了，不容易，感谢大佬。

---

### 评论 #18 (作者: HL81191, 时间: 4个月前)

现在又获取失败了，是不是要把sleep的参数再调大一点

---

### 评论 #19 (作者: XB37939, 时间: 4个月前)

[HL81191](/hc/en-us/profiles/33141062828951-HL81191)  可以把sleep搞大一点，也可以把重试次数搞多一点

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #20 (作者: GC81559, 时间: 4个月前)

终于有人解决这个问题了，非常有帮助

---

### 评论 #21 (作者: PX70901, 时间: 4个月前)

谢谢

---

### 评论 #22 (作者: XW25488, 时间: 2个月前)

感谢分享，更改代码后再去试一次

---

