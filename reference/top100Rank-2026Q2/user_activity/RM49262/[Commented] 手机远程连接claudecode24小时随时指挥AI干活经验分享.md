# 手机远程连接claudecode，24小时随时指挥AI干活！经验分享

- **链接**: [Commented] 手机远程连接claudecode24小时随时指挥AI干活经验分享.md
- **作者**: ZL81441
- **发布时间/热度**: 4个月前, 得票: 9

## 帖子正文

最近Clawdbot太火了，我已经被Clawdbot刷屏两天了

他实现了WhatsApp, Telegram, Discord,直接和ai对话，并且可以远程指挥你的电脑干活
 ![图片](images/img_e372a4d0eb.png) 

我也是第一时间部署到了自己的Mac mini上，老实说这个玩意权限确实有点大，想尝试的小伙伴还是整一台新的电脑或者是部署到vps上。我折腾了半天只跑通了千问的模型，使用下来觉得很兴奋，又有点小失望。兴奋是功能和潜力十分强大，交互方式十分的新颖。失望是配置起来简单，后续各种权限的设置等等，比想象的要复杂，感觉笨笨的（也不知道是不是千问的问题）

最让人失望的是他居然不能自动调用claudecode！也就是说我不能用它来帮助我做alpha工作。

于是我转念一想，用AI控制电脑，执行等 **这些功能，Claude Code 不是都有吗？**

区别在于Claude code只能在终端里交互，而 Clawdbot 让你能在聊天软件里用。 Clawdbot启发了我， **搭一座桥，把聊天软件连到 Claude Code。**

这两者原理如下：

```

```

Telegram │ ───▶ │ Bot 程序 │ ───▶ │ Claude Code

(你手机) │ ◀─── │ (你电脑) │ ◀─── │ (AI) │

```

```

1. 你在 Telegram 发消息
2. Bot 程序收到消息，转发给 Claude Code
3. Claude Code 执行任务（搜索、写文件、跑代码...）
4. Bot 程序把结果发回 Telegram

Bot 程序只是个"传话筒"，真正干活的是 Claude Code。

想法有了，于是我开始说干就干。啊不，我也不是程序员，于是我开始找开源社区有没有现成解决方案，在尝试了很多方案后失败，终于跑通了两个方案。

## **一 ：Telegram机器人**

仓库的地址如下 [https://github.com/hanxiao/claudecode-telegram](https://github.com/hanxiao/claudecode-telegram) 
 ![图片](images/img_a0c60184f2.gif) 

至于部署的方式，仓库readme文件写的比较详细，我这儿就不贴了。
如何创建telegram的机器人：

1. 打开Telegram，搜索
   [@Botfather](https://x.com/@Botfather)
2. 发送 /newbot
3. 按提示输入名称
4. 获得一个 Token （Use this token to access the HTTP API后面这一串英文和数字）

如果不会的话，可以直接把仓库地址和Token丢给Claudecode，让他来帮你安装。
最终成效
 ![图片](images/img_3571d153b2.png)

## **二：Happy coder app**

## （写稿的时候才发现，新手更加推荐！）
官方网站： [https://happy.engineering/](https://happy.engineering/)

电脑终端输入代码
npm i -g happy-coder && happy

 ![图片](images/img_fa2938d5f8.png) 
appstore或者play商店搜索happy coder下载

APP扫码终端二维码即可绑定，流程更加简单快捷，UI交互也更全面友好！
 ![图片](images/img_e5349d253a.png)

---

## 讨论与评论 (7)

### 评论 #1 (作者: ZL81441, 时间: 4个月前)

更正一下，今天又研究了一下Clawdbot，发现给Clawdbot安装一个coding-agent 的skills就手机可以调用Codex CLI, Claude Code, OpenCode等编程工具，支持GLM和minimax的codingplan，也不用担心token消耗感兴趣的小伙伴也可以尝试一下。
感觉Clawdbot这类的工具的想象空间比预想的要大不少，不仅是远程挖掘alpha

---

### 评论 #2 (作者: RM49262, 时间: 4个月前)

=====================================评论区=========================================

感谢大佬分享，这两天也被Clawdbot刷屏了

但我其实不明白的是，除了多了个聊天窗口控制的途径之外，这和我直接在Claude code中调用Skills有啥区别吗

===================================================================================

---

### 评论 #3 (作者: YQ84572, 时间: 4个月前)

Clawdbot确实很火，但是属于更多是边界，对于研究性的问题比较难以有进展，只能在远程检查或帮忙查看一些alpha感觉。
=================================感谢分享============================================

---

### 评论 #4 (作者: JX39934, 时间: 4个月前)

感谢大佬的分享，WQ国区论坛是真的牛，每次进来都能看到前沿科技，真的能让我学到很多东西，我这就回去捣鼓一下，看下能不能跑起来或者优化一下

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #5 (作者: HY20507, 时间: 4个月前)

好牛，又是前沿的技术，在wq最美好的体验莫过于此，喜欢这样探索的社区氛围，向大佬致敬

---

### 评论 #6 (作者: CY76111, 时间: 3个月前)

感谢大佬

---

### 评论 #7 (作者: XY20037, 时间: 3个月前)

太牛了大佬！把 Telegram/Happy coder 和 Claude Code 打通，实现手机远程 24 小时指挥 AI 干活，这思路直接拉满效率！还贴心纠正 Clawdbot 装 coding-agent 就能调用 Codex/Claude Code，甚至支持 GLM/minimax，这玩法的想象空间也太大了。对比直接在终端用 Claude Code，手机远程操控不用守在电脑前，挖 alpha、查数据随时随地都能搞，太贴合顾问的使用场景了。感谢分享这么前沿的玩法，国区论坛这种探索氛围真的绝了，马上去捣鼓部署！

---

