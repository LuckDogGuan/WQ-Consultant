# 【工具推荐】zcf + Claude Code + GLM-4.6：低价也能实现优质效果！经验分享

- **链接**: [Commented] 【工具推荐】zcf  Claude Code  GLM-46低价也能实现优质效果经验分享.md
- **作者**: TD65874
- **发布时间/热度**: 6个月前, 得票: 7

## 帖子正文

GLM-4.6是我目前使用过的所有AI中唯一提供‘真正’包月套餐的模型，和按token或者是‘假’包月的那些大模型相比，性价比可以说是相当高，但如果是直接使用GLM-4.6，据我使用感受而言，是比较一般的，所以，我们得搭配Claude Code来使用，这样才能达到很不错的效果。

然后在使用Claude Code的途中我又发现了一个好用的工具——zcf [GitHub - UfoMiao/zcf: Zero-Config Code Flow for Claude code & Codex]( [https://github.com/UfoMiao/zcf)（零配置,一键搞定](https://github.com/UfoMiao/zcf)%EF%BC%88%E9%9B%B6%E9%85%8D%E7%BD%AE,%E4%B8%80%E9%94%AE%E6%90%9E%E5%AE%9A)  Claude Code & Codex 环境设置 - 支持中英文双语配置、智能代理系统和个性化 AI 助手），非常适合搞不定Claude Code相关配置的朋友，具体操作非常简单：
### Step 1：安装 Node.js
zcf需要 Node 来跑，所以电脑没安装node的朋友请先安装一下node，官网：  [https://nodejs.cn/en/download](https://nodejs.cn/en/download)  ，官网下载自己系统的版本，安装之后在终端里输入：
```
node -v
npm -v
npx -v
```
能看到版本号，就说明成功了。
 ![图片](images/img_794810fcfb.png)

### Step 2：zcf 初始化
命令行中输入：`npx zcf` 打开交互式菜单，按需选择即可。
 ![图片](images/img_ba54dd2111.png)

### Step3：指定模型为GLM-4.6

![图片](images/img_a120503dc5.png)  ![图片](images/img_51a14de445.png) 
选择供应商GLM，然后输入自己的GLM-4.6的api key即可。

这一步如果没有api key的朋友，可以通过我的**邀请链接**注册：
 [https://www.bigmodel.cn/claude-code?ic=F0ICABFQRK](https://www.bigmodel.cn/claude-code?ic=F0ICABFQRK) 
或者直接进官网注册也可以：
 [https://bigmodel.cn/](https://bigmodel.cn/)

注册完之后，进入特惠专区：
 ![图片](images/img_5d7ecd0bb4.png)

![图片](images/img_331712edb3.png) 
订阅适合自己的套餐即可，订阅后点击右上角的API Key，然后创建api key并复制即可。

### Step4：开始使用
在按照zcf上面的步骤配置完成之后，我们先在控制台中cd到自己项目的地址，比如：`cd C:\Code\wqb` ，然后输入：`claude`，然后回车即可，如果出现如图所示的页面代表配置成功：
 ![图片](images/img_6d2dbf42e0.png) 
然后就可以正式使用了。

更多关于zcf的用法、参数与工作流说明可以查看文档： [ [https://zcf.ufomiao.com/zh-CN/](https://zcf.ufomiao.com/zh-CN/)](https://zcf.ufomiao.com/zh-CN/](https://zcf.ufomiao.com/zh-CN/))

==然后补充一点，如果用不习惯Claude Code cli命令行工具的，可以去vscode中下载Claude Code插件：
 ![图片](images/img_9ea331c0a8.png)

---

## 讨论与评论 (7)

### 评论 #1 (作者: PZ64174, 时间: 6个月前)

```
“群友们真是人才众多！”
```

感谢大佬分享！五花八门各式各样的ai使用方式都在论坛见到了，最近也在不断尝试新的方式进行使用，对比使用体验。看看哪个体验更好性价比更高！

====================================================================

一年一个台阶，一步一个脚印

====================================================================

---

### 评论 #2 (作者: LW67640, 时间: 6个月前)

我之前发给一个帖子关于iflow的，iflow有个人用户免费的api接口，也有glm-4.6模型，推荐给有需要的顾问。

---------------------------------------------------------------------------------

时间要花在有效率的地方

---------------------------------------------------------------------------------

---

### 评论 #3 (作者: YQ84572, 时间: 6个月前)

您发现的“GLM-4.6 + Claude Code + ZCF”确实是当前AI工具的“黄金组合”，GLM-4.6真正的包月制让高频使用毫无压力，成本仅为国际大模型的零头；Claude Code提供了顶级的代码生成与交互体验；而ZCF工具则实现了一键配置，将复杂的API对接和环境搭建化为无形。感谢分享

---

### 评论 #4 (作者: YZ64617, 时间: 6个月前)

ZCF的CCR，支持iflow，配置起来更容易和方便。

但是，几个ZCF版本之前，这种CCR配置iflow，会报错。个人感觉可能是因为iflow只提供单线程调用。

**如果用不习惯Claude Code cli命令行工具的，可以去vscode中下载Claude Code插件**

vscode中的Claude Code，需要单独配置。大家搜搜

---

### 评论 #5 (作者: MY49971, 时间: 6个月前)

AI 工具越来越多了，不知道选哪个好了...

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #6 (作者: ZH12413, 时间: 5个月前)

从Node.js安装到API配置，步骤清晰易懂，连邀请链接和截图手把手教学。
感谢细致的分享，祝大佬玩转Alpha，vf0.99+，受益多多。
==================================================================================
Hard work pays off.
==================================================================================

---

### 评论 #7 (作者: XW23690, 时间: 5个月前)

感谢分享，iflow也有GLM4.6模型可以使用，而且是免费的。CLI的调用可是事先准备好相关的prompt以及operators等md文件，我自己亲测发现也可以得到不错的信号，特别是针对优化因子，有一两个test需要优化的时候，AI能提供很好的帮助。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

