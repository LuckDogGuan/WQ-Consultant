# 保存OAuth登录认证，避免多次登录平台代码优化

- **链接**: [Commented] 保存OAuth登录认证避免多次登录平台代码优化.md
- **作者**: KM27775
- **发布时间/热度**: 1年前, 得票: 14

## 帖子正文

这个帖子借鉴这个帖子的内容。

使用Python获取API token过期时间,开箱即用

[https://support.worldquantbrain.com/hc/en-us/community/posts/32672023077911-%E4%BD%BF%E7%94%A8Python%E8%8E%B7%E5%8F%96API-token%E8%BF%87%E6%9C%9F%E6%97%B6%E9%97%B4-%E5%BC%80%E7%AE%B1%E5%8D%B3%E7%94%A8](https://support.worldquantbrain.com/hc/en-us/community/posts/32672023077911-%E4%BD%BF%E7%94%A8Python%E8%8E%B7%E5%8F%96API-token%E8%BF%87%E6%9C%9F%E6%97%B6%E9%97%B4-%E5%BC%80%E7%AE%B1%E5%8D%B3%E7%94%A8)

我使用的回测框架用到了多进程，每个进程都会调用登录平台的接口。为了避免多次调用接口，引起调用接口次数超限。这个方案把每次登录的session保存下来，当用户需要session接口，先判断接口是否超时且有效。如果有效，就返回保存的session；session无效再登录。这样就避免了多次调用登录接口。

代码如下：

> import requests
> import json
> import base64
> from datetime import datetime
> import requests
> import pickle
> from time import sleep
> def decode_jwt_exp(jwt_token):
> try:
> # 分割 JWT 的三部分
> parts = jwt_token.split('.')
> if len(parts) != 3:
> #raise ValueError("这不是一个有效的 JWT")
> print('这不是一个有效的 JWT')
> return None
> # Base64Url 解码 Payload
> payload_b64 = parts[1]
> padding = '=' * (-len(payload_b64) % 4)  # 补全 Base64
> payload_json = base64.urlsafe_b64decode(payload_b64 + padding).decode('utf-8')
> payload = json.loads(payload_json)
> # 提取 exp 字段
> exp_timestamp = payload.get('exp')
> if not exp_timestamp:
> print("未找到 exp 字段")
> return None
> # 转换时间
> exp_time = datetime.fromtimestamp(exp_timestamp)
> print("过期时间（UTC）:", exp_time.strftime('%Y-%m-%d %H:%M:%S'),exp_time,exp_timestamp)
> return exp_timestamp
> except Exception as e:
> print("解码出错:", e)
> return None
> def login():
> with open('othu2_session.pkl', 'rb') as f:
> othu2_session = pickle.load(f)
> if othu2_session:
> expires_at = decode_jwt_exp(othu2_session.cookies.get("t"))
> print(datetime.now().timestamp())
> if expires_at and datetime.now().timestamp() <expires_at - 300 :
> return othu2_session
> username = ""
> password = ""
> # Send a POST request to the /authentication API
> s = requests.Session()
> # Set up basic authentication
> s.auth = (username, password)
> response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')
> try_count=10
> while try_count>0:
> print(response.content)
> if str(response.content).find("API rate limit exceeded")>-1:
> sleep(3)
> response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')
> else:
> with open('othu2_session.pkl', 'wb') as f:
> pickle.dump(s, f)
> return s
> try_count =try_count -1
> return None
> # 示例使用
> if __name__ == '__main__':
> login()

---

## 讨论与评论 (19)

### 评论 #1 (作者: BL72197, 时间: 1年前)

我这边正想着做这块功能，现在可以直接白嫖大佬的了

---

### 评论 #2 (作者: LG87838, 时间: 1年前)

感谢分享，这个问题困惑了很久，点赞！

因为最近频繁遇到了429错误，一直在尝试解决办法，GPT也推荐了的本地保存session的方式，但实践后效果并不明显。您长时间运行的效果如何？

如果和我类似的代码小白，并且分了多个程序跑回测，打tag等，本质的问题可能是会话数量太多，本地存储session肯定会有效果，但效果可能有限。这是我最近实践的结果，还请有经验的大佬多多指教。

----------------------------------------不混信号，不拟合，多样性----------------------------------------------------

---

### 评论 #3 (作者: MH19374, 时间: 1年前)

十分有用。多谢大佬~

---

### 评论 #4 (作者: AH18340, 时间: 1年前)

感谢分享

---

### 评论 #5 (作者: SD17531, 时间: 1年前)

大佬大佬,如何使用上面的代码?直接放到machinelib里面吗?替换里面哪些方法啊?

=========================================================
=========================================================

我的代码能力实在太差了

---

### 评论 #6 (作者: FL39657, 时间: 1年前)

非常有用的代码

---

### 评论 #7 (作者: QP72475, 时间: 1年前)

不错的方法，有空我也尝试一下。

---

### 评论 #8 (作者: ML42552, 时间: 1年前)

-----------------------------

感谢大佬分享！！

------------------------------------

蹲一手回测脚本，最近自己重改异步回测脚本总是出错

------------------------------------------------------------

共好！！

---------------------------------------------------------------

---

### 评论 #9 (作者: OT17586, 时间: 1年前)

调用接口次数超限制，感谢大佬提供优秀的解决方案。您的回测框架用的多进程，请问您在回测时给打上标记，新开一个进程使用什么办法。如果只跑一阶的代码就没问题，如果分配卡槽同时跑二三阶，标记不同的一阶、二阶、三阶就会有问题。

---

### 评论 #10 (作者: KM27775, 时间: 1年前)

@ [OT17586](/hc/en-us/profiles/28942308572439-OT17586)   请问遇到什么问题？我是用数据库，一阶二阶三阶设置不同的优先级，优先跑优先级高的alpha。新开进程，就是独立的开cmd 窗口。

---

### 评论 #11 (作者: KM27775, 时间: 1年前)

@SD17531  把这两个函数copy到machine lib 就可以用了。

---

### 评论 #12 (作者: KM27775, 时间: 1年前)

@ [LG87838](/hc/en-us/profiles/26968783514775-LG87838)  效果很好，我这边还做了web系统，监控处理simulator，每一次页面功能点击几乎都需要session，之前总是出问题，现在问题很少了。

---

### 评论 #13 (作者: QZ67721, 时间: 1年前)

好帖子 顺便问问有没有更具体的操作方法，萌新不会代码，能不能直接复制粘贴放到machine_lib或者其他文件就生效呢？要把你的代码整合到我的回测代码里面，一直在报错。
++++++++++++++++人人都不看好我，偏偏我也不争气++++++++++++++++++++

---

### 评论 #14 (作者: OT17586, 时间: 1年前)

嗯，大佬顾问培训时老师说过，每个回测完的alpha都可以进行颜色、名字和tag标记

set_alpha_properties(s,

alpha_id,

name = Names,

color = None,)，但是标记的话会拖慢回测效率，老师说可以另开一个进程，这样就提升效率了一阶二阶三阶在加上标记的就有6个进程了，我利用AI写的代码实现不了，A1对应一阶,B1对应二阶C1对应三阶

---

### 评论 #15 (作者: YL70953, 时间: 1年前)

[OT17586](/hc/en-us/profiles/28942308572439-OT17586)

请问你能解决这个问题吗？ 我想在 multi_simulate 的时候给所有alpha 加tag, 但是一直都搞不定

---

### 评论 #16 (作者: KM27775, 时间: 1年前)

[OT17586](/hc/en-us/profiles/28942308572439-OT17586)   你遇到什么问题？

---

### 评论 #17 (作者: OT17586, 时间: 11个月前)

[KM27775](/hc/en-us/profiles/28857301033239-KM27775) ，谢谢大佬已经解决了。

---

### 评论 #18 (作者: CY54463, 时间: 10个月前)

感谢大佬分享，吃上好的了

---

### 评论 #19 (作者: CM31430, 时间: 10个月前)

为什么我都是201呢？反正我都给算正常了，也不知道是啥情况。

```
response.status_code in [200, 201]
```

---

