# ［PPAC］使用程序提交alpha之前，必需做的一件事经验分享

- **链接**: [Commented] PPAC使用程序提交alpha之前必需做的一件事经验分享.md
- **作者**: LG37773
- **发布时间/热度**: 1年前, 得票: 19

## 帖子正文

## 一、背景：

近期开始了Power Pool Alphas Competition 2025的比赛，受到新老顾问的欢迎。特别是不进行Prod correlation的测试，很多以前不能提交的alpha也可以提交了。参加比赛还有其他的一些福利就不一一表述。

参加比赛时，提交alpha会有一个特别的动作需要完成，就是填写Alpha的description，而且需要按照指定的template进行填写。

![图片](images/img_35b80c88f0.png)

具体template如下：
Idea: 
Rationale for data used: 
Rationale for operators used:

## 二、解决方案：

手动填写是个重复劳动的工作，既然在使用Python就让程序来完成吧。

在machine lib中，修改set_alpha_properties函数。添加参数regular_desc，不能使用自带的参数selection_desc。

将alpha的description通过这个参数，传进函数内进行更新。

为了看贴子的同学也有收获，直接分享代码。欢迎点赞留言。

```
def set_alpha_properties(    s,    alpha_id,    name: str = None,    color: str = None,    selection_desc: str = "None",    regular_desc: str = None,   #changed by new version    combo_desc: str = "None",    tags: str = ["ace_tag"],):    """    Function changes alpha's description parameters    """     params = {        "color": color,        "name": name,        "tags": tags,        "category": None,        "regular": {"description": regular_desc},  # changed by new version        # "regular": {"description": None},        "combo": {"description": combo_desc},        "selection": {"description": selection_desc},    }    response = s.patch(        "https://api.worldquantbrain.com/alphas/" + alpha_id, json=params    )
```

调用set_alpha_properties函数时，指定Description：

```
from machine_lib import *sess =login()alpha_id = 'XXXXX'  #<==== 替换成自己的alpha idPPAC_desc = '''Idea: This alpha for Power Pool Alphas Competition 2025Rationale for data used: The data utilized in this alpha is highly reliable.Rationale for operators used: The chosen operators are specifically selected for their suitability and effectiveness in executing the required operations.'''set_alpha_properties(sess, alpha_id=alpha_id,regular_desc=PPAC_desc)status_code = submit_alpha(sess, alpha_id)  #submit_alpha function has been defined. if status_code == 200:    print('alpha was successfully submitted')
```

这样就实现了自动提交alpha, 然后可以进一步优化，定时提交等等。

我们不断地扩展alpha machine的功能，更高效地完成工作。希望能够帮助到大家，欢迎大家在评论区留言。

---

## 讨论与评论 (5)

### 评论 #1 (作者: HQ17963, 时间: 1年前)

感谢分享，针对最近提交困难的问题，在这里贴一下我自用的提交代码（需先设置description）

> from machine_lib import login
> import time
> s=login()
> login_time=time.time()
> import traceback
> import requests
> def submit(id_):
> global login_time,s
> print('submitting',id_)
> while True:
> try:
> if time.time()-login_time>3600*3.5: # 3.5小时后重新登陆
> s=login()
> login_time=time.time()
> a=s.post(f' [https://api.worldquantbrain.com/alphas/{id_}/submit](https://api.worldquantbrain.com/alphas/{id_}/submit) ')
> print(a.text)
> if a.status_code==403:
> print('创建提交任务失败（可能是已提交、达到今日上限、存在FAIL无法提交）')
> break
> print('已创建提交任务')
> submit_ok=False
> while True:
> a=s.get(f' [https://api.worldquantbrain.com/alphas/{id_}/submit](https://api.worldquantbrain.com/alphas/{id_}/submit) ')
> if a.status_code==404:
> raise ValueError('提交任务已结束')
> if 'retry-after' in a.headers:
> time.sleep(1)
> continue
> if a.text == '':
> continue
> if 'Bad Gateway' in a.text:
> continue
> print(a.text)
> if a.text[0]!='{': # 返回json说明提交任务结束
> continue
> submit_ok=True
> break
> if submit_ok:
> print('提交成功')
> break
> except requests.exceptions.ReadTimeout:
> pass
> except KeyboardInterrupt as e:
> raise e
> except:
> traceback.print_exc()
> time.sleep(1)
> while True:
> submit('8PwmPvV')
> submit('d1G8ro2')
> print('一轮提交结束，为防止没提交上，继续提交')
> time.sleep(1800)

---

### 评论 #2 (作者: OB53521, 时间: 1年前)

感谢大佬的代码，非常有用！还有个问题想问一下，这个评论区的submit方法和上面文章中的submit_alpha方法不是同一个吧，我看要传的参数也不一样，是否可以分享一下捏🥺

---

### 评论 #3 (作者: LG37773, 时间: 1年前)

@  [OB53521](/hc/en-us/profiles/28890356914711-OB53521)

请参照 课代表的贴子，提供了submit_alpha的接口：

[../DM28368/[Commented] 自动提交Alpha的接口.md](../DM28368/[Commented] 自动提交Alpha的接口.md)

---

### 评论 #4 (作者: ZS59763, 时间: 1年前)

感谢你的分享 和帖子，十分有用，点赞！

---

### 评论 #5 (作者: DZ31817, 时间: 1年前)

20250401

------------------------------------------------------------------------------------------

感谢分享，想请教一下自动提交PPAC因子，如何保证提交因子的质量，对各个指标具体设置哪些代码筛选的门槛呢。我现在还是要人工检查一下各项指标看是否有异常、看下性能对比等再提交，毕竟PPAC影响vf，还是想谨慎一些。感觉机器自动提交要做好筛选避免交特别爆炸的alpha。

---

