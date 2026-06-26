# 【自动化脚本】在unsubmitted列表中快速检索可提交alpha

- **链接**: [Commented] 【自动化脚本】在unsubmitted列表中快速检索可提交alpha.md
- **作者**: VC17729
- **发布时间/热度**: 1年前, 得票: 16

## 帖子正文

大家好我是Vincent，使用了社区中自动提交simulate和alpha的script，效率得到了巨大提升，但是在使用中感觉还缺了一环。

此脚本可从unsubmitted列表获取可提交的alpha_id，基于浏览器交互，需要调出chrome登陆获取。

如此从测试到提交全部可自动化完成，可以把所有精力放在公式及其背后含义的研究上。

另效率可能一般，全当抛砖引玉。如有可直接通过接口检索的方法欢迎告知讨论。

使用说明：建议在jupyter上运行，在执行第二部分前需要手动将fitness选项调出，并每页显示所有待检索个数，可自行设置需要检索的值，或者直接使用默认值。如果你的显示顺序和我不一致，需要去调整第二部分开头div的序号。

![图片](images/img_2e881fb9ad.png)

执行成功显示如下，即我的这29个sharp和fitness符合要求的中有8个是可以去尝试提交的。

注意：此方法仅检索可提交alpha_id，并不保证一定提交成功，可根据xx同学的分享进行下一步提交。

![图片](images/img_5c6a48a63f.png)

################  分隔线  ################

# 导入

from DrissionPage import Chromium

from os.path import expanduser

import json

# Load credentials # 加载凭证

with open(expanduser('../brain.txt')) as f:

credentials = json.load(f)

# Extract username and password from the list # 从列表中提取用户名和密码

username, password = credentials

# 连接浏览器

browser = Chromium()

# 获取标签页对象

tab = browser.latest_tab

def login():

# 访问网页

tab.get(' [https://platform.worldquantbrain.com/alphas/unsubmitted](https://platform.worldquantbrain.com/alphas/unsubmitted) ')

tab('tx=Accept').click()

tab('#email').input(username, clear=True)

tab('#password').input(password, clear=True)

tab('x://button[@type="submit"]').click()

tab('tx=Alphas').click()

login()

################  分隔线  ################

from tqdm import trange

def get_alpha(sharp=1.25,fitness=1):

tab = browser.latest_tab

tab('x://div[@class="rt-thead -filters"]/div/div[12]//input').input(f'>{sharp}', clear=True)

tab('x://div[@class="rt-thead -filters"]/div/div[15]//input').input(f'>{fitness}\n', clear=True)

tab.wait(3)

alpha_id_list = []

tab_alpha_num = len(tab.eles('x://div[@class="rt-tbody"]/div'))

for i in trange(1,tab_alpha_num+1):

# 点击name以获取alpha id

tab(f'x://div[@class="rt-tbody"]/div[{i}]//*[text()="anonymous"]').click()

tab.wait(1)

if tab('x://*[text()="Submit Alpha"]/../..').states.is_clickable:

alpha_url = tab('x://*[text()="Open alpha details in new tab"]/..').attr('href')

alpha_id = alpha_url[-7:]

alpha_id_list.append(alpha_id)

return alpha_id_list

get_alpha()

################  分隔线  ################

---

## 讨论与评论 (9)

### 评论 #1 (作者: JR23144, 时间: 1年前)

不用这么写 爬网页，不如直接调用api

```
https://api.worldquantbrain.com/alphas/{alpha_id}
```

---

### 评论 #2 (作者: DM28368, 时间: 1年前)

Your sharing is really useful. I have applied it for 2 days now and with calling API my work efficiency has increased a lot (before I used to simulate alpha manually).

---

### 评论 #3 (作者: XD81759, 时间: 1年前)

感谢分享

---

### 评论 #4 (作者: YS42224, 时间: 9个月前)

学习一下

---

### 评论 #5 (作者: CC85858, 时间: 9个月前)

感谢分享

---

### 评论 #6 (作者: CY66739, 时间: 9个月前)

请问如何通过alpha_id得知是哪一个alpha呢

如果想要转到第二页该怎么实现

---

### 评论 #7 (作者: CC85858, 时间: 9个月前)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

在未提交的alpha处随便点击一个alpha，在搜索栏中替换成你想搜索的alpha id即可

---

### 评论 #8 (作者: CY66739, 时间: 9个月前)

尊敬的作者 我基于你目前的代码 实现了跳页功能 我可以把这个代码开源分享嘛

---

### 评论 #9 (作者: YL96878, 时间: 6个月前)

谢谢

---

