# 【免费API系列】最新的天工agent模型SkyClaw-v1.0限时免费用，听说蛮厉害的经验分享

- **链接**: [Commented] 【免费API系列】最新的天工agent模型SkyClaw-v10限时免费用听说蛮厉害的经验分享.md
- **作者**: CL86067
- **发布时间/热度**: 28天前, 得票: 7

## 帖子正文

## 又一个免费羊毛

之前分享过 DeepSeek V4 + 9Router 的方案，今天又发现了一个 **限时免费无限 Token**  的模型——昆仑万维天工 AI 刚发布的  **SkyClaw-v1.0** 。

关键是： **免费、无限Token、适配主流Agent工具** ，非常适合拿来当 BRAIN 开发的辅助模型。

## SkyClaw 是什么？

昆仑万维天工 AI 新出的 Agent 模型，分两个版本：

版本

定位

SkyClaw-v1.0

完整版，适合复杂任务

SkyClaw-v1-lite

轻量版，适合日常快速调用

主打 **智能体 Agent 场景** ——工具调用、多回合交互、代码生成、文件编辑这些正是我们做 BRAIN 开发时需要的。

### 实测数据

官方放出的基准测试，全面超越：

- DeepSeek V4 Flash
- Qwen 3.6 35B/27B
- Minmax 2.7

综合实力接近  **DeepSeek V4 Pro**  的水准，而且支持 **百万级超长上下文** ，长链路推理和多步任务规划能力不错。

## 怎么用？

### 方式一：在线直接体验

打开天工  [Skywork官网](https://www.tiangong.cn/) ，模型选择 SkyClaw V1.0，直接对话，零配置。

### 方式二：API 调用（重点推荐）

给 OpenClaw、WorkBuddy、Hermes、Nanobot 等工具配这个模型，3 步搞定：

**1. 注册获取 API Key**

访问  [apifree.ai](https://www.apifree.ai/)  → 注册登录 → Manage → API Key → 创建新密钥

**2. 配置 API 信息**

在你的 OpenClaw / WorkBuddy 后台填入：

```
调用地址：https://api.apifree.ai/agent/v1/chat/completions
API 密钥：刚才创建的 Key
模型名称：skywork-ai/skyclaw-v1
```

**3. 一键启用**

不会手动配置的话，直接把上面三个信息发给 OpenClaw，AI 自动帮你配好，后续直接选中 skyclaw-v1 模型就能用。 **无限 Token，随便用！**

## 实测感受

亲自在 WorkBuddy 上配了试了几天：

- 日常文案、任务规划、工具调用、多轮对话都 OK，逻辑清晰
- 兼容 OpenAI 格式，主流 Agent 框架都能直接用
- 部分时段响应速度稍微慢一点，可能是 API 网络波动，等几秒就好

## 小结

做 BRAIN 经常要跟 AI 打交道，写 Alpha 表达式、跑分析、调参数，Token 消耗起来真的不少。

现在 DeepSeek V4 Flash 已经很便宜了，再加上 SkyClaw 这种 **限时免费无限 Token**  的模型，Copilot/Claude 之类的订阅费基本可以省了。

**不过注意是限时的** ，官方没说截止时间，趁免费赶紧用上。

*P.S. 如果用来写 Alpha 表达式，建议还是用 DeepSeek V4 Pro 或者 glm5.1等，SkyClaw 更适合辅助性的任务——分析数据字段、写脚本、整理结果这些。*

*另外顺便分享一个不太一样的中转站，第一次见模型这么全的，注册送50额度，应该可以用deepseekv4Pro一段时间，可以试一下，附上链接：*

*[https://auroramos.com/?ref=CH2GYJDY](https://auroramos.com/?ref=CH2GYJDY)*

*确实第一次见模型这么全的，有点厉害,大家感兴趣可以试一下，似乎可以多注册几个号用一下 ![图片](images/img_999491b4dd.png)*

*对了，顺便今天还看到了别人分享的deepseek网页端增强插件，弄得网页也有记忆还有可以用mcp，skill什么的了，感觉很牛，这不直接可以网页上做alpha优化什么的了，公众号看到的文章，感觉真心不错啊这个，要真的好用的话*

*[https://mp.weixin.qq.com/s/o2Lay-Owbut50QQKks0DnQ](https://mp.weixin.qq.com/s/o2Lay-Owbut50QQKks0DnQ)*

github地址：

[https://github.com/zhu1090093659/deepseek-pp](https://github.com/zhu1090093659/deepseek-pp)

---

## 讨论与评论 (5)

### 评论 #1 (作者: CZ39633, 时间: 26天前)

====================================================================================  感谢大佬分享的大模型，又可以白嫖了                                                                                                                     ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #2 (作者: CL86067, 时间: 25天前)

芒果灵创不太好用，用qwen3.7-max的话还是推荐用qwen官方的吧，千问电脑版可以用，但是这个没法用mcp，qwen的就可以，甚至可以直接网页端使用，这就有点推荐了，感觉应该还不错，附上网址：

[https://chat.qwen.ai/](https://chat.qwen.ai/)

还有桌面版的下载地址，和网页几乎一样的： [https://qwen.ai/qwenchat](https://qwen.ai/qwenchat)

---

### 评论 #3 (作者: YH25030, 时间: 24天前)

好久没有薅羊毛了，等一下去试试。谢谢分享！

---

### 评论 #4 (作者: RM49262, 时间: 24天前)

=====================================评论区====================================

感谢大佬分享  从数据来看确实不错

这就试用一下 看看效果如何

=============================================================================

---

### 评论 #5 (作者: CL86067, 时间: 23天前)

补充一下，opencode可以免费用最新的minimax m3模型，这个还是比较推荐试一下，最新的应该会厉害一些吧

---

