# 【免费API系列3】全球前十的AI lab——Agnes AI 的免费API，文本/图片/视频模型全免费

- **链接**: [Commented] 【免费API系列3】全球前十的AI labAgnes AI 的免费API文本图片视频模型全免费.md
- **作者**: CL86067
- **发布时间/热度**: 23天前, 得票: 4

## 帖子正文

## 又来了

上次分享了 DeepSeek V4 + 9Router 和 SkyClaw 免费无限 Token，今天又刷到一个—— **Agnes AI** 。

文本、图片、视频模型全都有，而且目前 **免费层开放中** （具体额度和截止时间以平台公告为准），接口兼容 OpenAI 格式，WorkBuddy、Hermes、OpenClaw 都能直接配。

> 原文： [可知AI - 微信公众号](https://mp.weixin.qq.com/s/HL4w5j7Ntnp8d25oBQTC3Q)

## Agnes AI 是谁？

Agnes AI 是一家 **新加坡** 的 AI 模型公司，2025 年 7 月上线，创始人 Bruce Yang。全自研多模态模型（文本、图片、视频），不依赖第三方开源框架。

### 模型排名

Agnes AI 是 **首个进入全球 AI 排行榜前 10 的新加坡 AI 实验室** ，连续三次在独立基准测试中进入全球前 10：

模型

排名

基准测试

Agnes-2.0-Flash

全球前 10

Claw-Eval（Agent 能力，超越 Gemini 和 MiniMax，某）

Agnes-Image-2.0-Flash

全球前 10

Artificial Analysis（图片编辑，盲测评分）

Agnes-Video-V2.0

全球前 10

Artificial Analysis（视频生成）

另外，Agnes-R1（7B 参数）在 HotpotQA 多跳推理上比 DeepSeek GRPO 提升 34.1%，SWE-Bench 得分 74.6%，开源模型第一。

### 定价

API 定价极低，文本模型输入 $0.03/1M tokens、输出 $0.15/1M tokens，只有 Claude Opus 4.6 的 0.6%。

## Agnes 有什么？

模型

类型

接口

agnes-2.0-flash

文本

OpenAI 兼容  `/v1/chat/completions`

agnes-image-2.0-flash

图片

`/v1/images/generations` ，支持图生图

agnes-video-v2.0

视频

`/v1/videos` ，异步生成

文本模型跑日常的文案、分析、简单代码没啥问题。图片支持图生图和多图合成，视频模型支持文生视频和图生视频。

## 怎么免费用？

### 第一步：注册拿 Key

先去  [platform.agnes-ai.com](https://platform.agnes-ai.com)  注册账号，登录后在设置里拿到 API Key。免费层有速率和调用量上限，个人开发者日常用基本够用。

### 第二步：配到工具里

#### WorkBuddy 配置

在自定义模型里填三个字段：

```
提供商：其他
接口地址：https://apihub.agnes-ai.com/v1
模型名称：agnes-2.0-flash
```

填上 API Key，保存就行。

### Hermes 配置

```
hermes config set OPENAI_API_KEY 你的key
hermes config set model.provider custom
hermes config set model.base_url https://apihub.agnes-ai.com/v1
hermes config set model.default agnes-2.0-flash
```

### Python 调用

装过 openai 包的话，直接改 base_url 就能用：

```
from openai import OpenAI

client = OpenAI(
    api_key="你的 API Key",
    base_url="https://apihub.agnes-ai.com/v1"
)

response = client.chat.completions.create(
    model="agnes-2.0-flash",
    messages=[{"role": "user", "content": "用一句话介绍你自己"}]
)
print(response.choices[0].message.content)
```

## 实测感受

原文作者说他每天跑几十万条 AI 相关的内容处理，已经把一部分任务切到 Agnes 上了，评价是"丝滑、好用够用"。

我自己试了一下，响应速度还可以，日常分析和代码生成够用。图片和视频模型还没深度测，但文本这块当个免费平替完全 OK。

## 几个入口

用途

地址

官网

[https://agnes-ai.com](https://agnes-ai.com)

API 平台

[https://platform.agnes-ai.com](https://platform.agnes-ai.com)

API 文档

[https://agnes-ai.com/doc/overview](https://agnes-ai.com/doc/overview)

## 小结

从 DeepSeek V4 到 SkyClaw 再到 Agnes，这几个月免费/低价的优质模型越来越多了。对我们做 BRAIN alpha的来说，写 Alpha、分析字段、调参数这些活儿，模型和工具选择越来越多，感觉免费的模型都好多了，用不过来了都，不过免费的一般都有期限或者限制，趁能用赶紧用上，另外免费肯定会牺牲体验，可以试着体验一下，但是最终还是应该多看看怎么优化研究流程或者AI提效上面，现在模型都好强了，我感觉自己挖不到好的alpha还是不太会用AI，学习用AI真的还有好多路要走!

*P.S. 文本用 agnes-2.0-flash，图片用 agnes-image-2.0-flash，视频用 agnes-video-v2.0，别搞混了,另外这个不知道是不是可以用到数据可视化方面,感觉可以尝试一下*

---

## 讨论与评论 (4)

### 评论 #1 (作者: RM49262, 时间: 23天前)

=====================================评论区====================================

感谢大佬分享，又知道了一个可以薅的羊毛

准备这几天拿来试试看效果怎么样

=============================================================================

---

### 评论 #2 (作者: XY20037, 时间: 21天前)

感谢大佬持续分享优质低价 AI 接口资源！Agnes 全自研多模态模型实力出众，榜单成绩亮眼，API 兼容 OpenAI 格式，接入 Hermes、WorkBuddy、原生 Python 都十分便捷。低廉计费搭配免费试用额度，刚好适配因子编写、字段梳理、回测数据分析、结果可视化等 WQ 日常研发工作。接连集齐 DeepSeek 主力生成、SkyClaw 辅助试错、Agnes 图像可视化的工具组合，大幅压缩研发成本，趁着免费窗口期抓紧接入试用，优化 AI 驱动 Alpha 挖掘全流程！

---

### 评论 #3 (作者: XC66172, 时间: 21天前)

谢谢佬分享，又有一个免费的API可以使用了~~

==========================================

FIGHTING LABUBU!~

=========================================

---

### 评论 #4 (作者: XX87502, 时间: 21天前)

=====================早日冲上GrandMaster============================================

感谢分享，让我又知道一个免费的api平台

==================纸上得来终觉浅，绝知此事要躬行======================================

---

