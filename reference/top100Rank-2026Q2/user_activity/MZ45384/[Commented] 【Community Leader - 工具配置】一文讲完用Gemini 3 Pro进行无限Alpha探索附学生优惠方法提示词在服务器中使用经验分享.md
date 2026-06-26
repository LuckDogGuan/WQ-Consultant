# 【Community Leader - 工具配置】一文讲完用Gemini 3 Pro进行无限Alpha探索（附学生优惠方法/提示词/在服务器中使用）经验分享

- **链接**: [Commented] 【Community Leader - 工具配置】一文讲完用Gemini 3 Pro进行无限Alpha探索附学生优惠方法提示词在服务器中使用经验分享.md
- **作者**: OB53521
- **发布时间/热度**: 6个月前, 得票: 103

## 帖子正文

## Intro

鉴于一些朋友不知道Gemini CLI的功能，遂写一篇帖子进行教学，目录：

1. Gemini CLI的安装和配置
2. CLI中MCP的配置
3. 使用示例
4. 领取1年免费的Gemini 3 Pro学生优惠
5. 在服务器中使用Gemini CLI
6. 服务器中无法登陆的问题解决方案

## Gemini CLI Installation

首先进行GeminiCLI的下载： [https://geminicli.com/](https://geminicli.com/)

或者通过命令进行全局安装

```
npm install -g @google/gemini-cli
```

安装完成后，在终端运行

```
gemini --version
```

如果出现  `>=0.18.4` 的版本号就说明成功了

切换到项目所在文件夹，以我自己为例

```
cd CodeProject/consultant
```

然后输入  `gemini ` 回车就可以启动Gemini Cli了

进入后运行  `/settings ` 出现如图界面

![图片](images/img_7a784767ea.png)

按回车将 Preview Features 打开，然后按Esc退出即可

再输入命令 `/model` 选择模型，如图，选择第二个Pro

![图片](images/img_9221778e51.png)

## CLI中MCP的配置

接下来是在针对Gemini CLI进行MCP的配置，首先找到Gemini所在目录，这里以Mac为例，Mac默认隐藏点文件夹和点文件，可以通过快捷键  `Shift+Space+. ` 显示。

![图片](images/img_c1ce16ebbd.png)

进入 settings.json 文件，以下是我的配置：

```
 {   "ide": {     "hasSeenNudge": true   },   "mcpServers": {     "worldquant-brain-platform": {       "command": "/Users/orange/CodeProject/consultant/run_webspider_python.sh",       "args": [         "/opt/anaconda3/envs/WebSpider/lib/python3.11/site-packages/cnhkmcp/untracked/platform_functions.py"       ],       "description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features."     }   },   "security": {     "auth": {       "selectedType": "oauth-personal"     }   },   "ui": {     "theme": "Atom One"   },   "general": {     "previewFeatures": true   } }
```

其中  `"/Users/orange/CodeProject/consultant/run_webspider_python.sh" ` 是我让AI写的命令文件，因为在Mac上很多人都遇到过无法使用Search Forum的问题。

> 如果有需要我会分享在评论区，在这里还是教学为主

根据自己文件所在位置修改路径，剩余的为主题配置、登录方式配置以及之前开启的预览特性。

## 使用示例

首先我会将Rule发送给Gemini，我通过  [Yprompt](#) ( [https://yprompt.252035.xyz/generate](https://yprompt.252035.xyz/generate) )  进行提示词的生成和优化，他会一直询问你的需求和期望，收集到足够信息后就会生成完整的提示词，有需要的朋友可以根据自己需要进行调整。

我的提示词中有很多文件都已经提前准备好，便于Gemini直接读取，减少网络请求和MCP的调用。

![图片](images/img_7b71c78e94.png)

![图片](images/img_35bf9f5841.png)

在对话中首次使用MCP会需要你的确认，直接选第三个全部允许即可。

![图片](images/img_1c26a5bb4a.png)

Gemini会自己制定Todo List。

![图片](images/img_dd9ae2f4b6.png)

## 学生优惠获取

最后是学生优惠的获取，首先打开这个链接  [https://gemini.google/students/](https://gemini.google/students/)

点击 Get Offer

![图片](images/img_b0bba091d5.png)

然后会出现一个需要填写表格的页面，我已经领取了所以页面不同。如果能出现填表页面说明网络质量是比较好的，支持获取。

复制上方的URL然后去 ***某海鲜市场。*** URL类似这样：

```
https://one.google.com/ai-student?utm_source=gemini&utm_medium=web&utm_campaign=students_web_student-lp&icid=students_web_student-lp&_gl=1*1u3v6vv*_gcl_au*NDE5MDkwOTkwLENjQyNDkxMTY.*_ga*MTU4Nzg3MNC4xNzY0MjQ5MTE3*_ga_WC57KJ50ZZ*czE3NjQzMDkzNTkbzIkZzAkdDE3NjQzMDkzNTYkaYwJGJGgw&g1_landing_page=75
```

接下来就可以在Gemini CLI愉快地使用Gemini 3 Pro了。

## 在服务器中使用Gemini CLI

在服务器中可能遇到没有权限导致安装失败的情况，这时候需要先安装NVM并激活：

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

```
source ~/.bashrc
```

然后安装Node.js

```
nvm install 22 && nvm use 22
```

输入  `node -v`  确认版本号是否为 v22.x.x

重新安装Gemini CLI

```
npm install -g @google/gemini-cli
```

**在这一步可能又会出问题，比如一直在转圈，可以看一下我的解决办法：**

首先通过npm全局安装pnpm

```
npm install -g pnpm
```

输入 pnpm -v 应该显示 10.24.0 版本号

设置pnpm的镜像源：

```
pnpm config set registry https://mirrors.cloud.tencent.com/npm/
```

运行

```
pnpm setup
```

复制输出的内容并运行，比如我的就是：

```
source /home/ubuntu/.bashrc
```

![图片](images/img_5b28c9139f.png)

再次安装，警告不用管：

![图片](images/img_22b2ae6f5d.png)

## 服务器中无法登陆Gemini的问题解决方案

有的朋友通过账号连接会出现输入验证码一直 fail 的情况，其实是因为服务器无法连接到 Google 的服务，解决办法如下。

前置条件： **本地电脑** 已开启梯子，查看你本地梯子的端口（本文以  `7890`  为例）

在VS Code中按下 `Ctrl+Shift+P`  ，输入并选择  `Remote-SSH: Open Configuration File`

选择你的配置文件，我的是： `Users/orange/.ssh/config`

```
 Host 你的服务器别名 (例如 ubuntu20.04LTS)   HostName 123.123.123.12   User root   IdentityFile ~/Downloads/key.pem   # 👇 添加下面这一行（关键！）   # 格式：RemoteForward <服务器端口> 127.0.0.1:<本地端口>   RemoteForward 7890 127.0.0.1:7890
```

**记得保存文件**

在 VS Code 中按下  `Ctrl + ,` （Mac 是  `⌘+,` ） 打开设置，点击右上角的  **“打开设置(JSON)”**  图标。

在配置文件的大括号  `{ ... }`  中添加以下内容：

```
 "terminal.integrated.env.linux": {     "http_proxy": "http://127.0.0.1:7890",     "https_proxy": "http://127.0.0.1:7890",     "all_proxy": "http://127.0.0.1:7890"   }
```

**记得再次保存文件**

然后按下快捷键  `Ctrl+Shift+p` （Mac是  `⌘+Shift+p ` ）输入  `Developer: Reload Window`

在终端输入  `curl -I https://www.google.com ` 如果返回  `HTTP/1.1 200 OK ` 说明配置成功

在终端中输入 `gemini` ，选择 **用账户登录** ，打开给出的链接，复制验证码，即可使用Gemini。

**最后，希望大家在AI助力下，VF⬆️WF⬆️塔⬆️Genius⬆️**

---

## 讨论与评论 (34)

### 评论 #1 (作者: JX14975, 时间: 6个月前)

感谢大佬，我以前尝试使用geminicli失败了，现在用clime对电脑内存负担不小，如今终于能解决这个问题。

请问是如何解决科学上网的方法不能在全局使用的问题，我的梯子好像只能在局部代理，能用来代理vscode（setting里有设置），但geminicli似乎弄不了

---

### 评论 #2 (作者: YC62305, 时间: 6个月前)

谢谢大佬分享！

---

### 评论 #3 (作者: OB53521, 时间: 6个月前)

[JX14975](/hc/en-us/profiles/29548387470487-JX14975)  我用的Clash Party，规则模式+TUN可以在终端使用cli

---

### 评论 #4 (作者: YX50005, 时间: 6个月前)

谢谢大佬分享！想咨询大佬一个问题，在获取学生优惠之后，是否可以在gemini cli外使用gemini pro3呢，感觉gemini cli这种命令行形式还是不是很适应，如果能直接调用api就好了

---------------------假如你每天都来论坛好好学习，你将会获得一个GM---------------------------------

---------------------------------------------------------------------------------------------------------------------------

---

### 评论 #5 (作者: AM12075, 时间: 6个月前)

=====================================================================

请问api需要付费吗，学生优惠包括api吗？

=====================================================================

---

### 评论 #6 (作者: OB53521, 时间: 6个月前)

=====================================================================
 [YX50005](/hc/en-us/profiles/29899344989847-YX50005)   [AM12075](/hc/en-us/profiles/30421958512663-AM12075)  
学生优惠是不包含API去使用3的额度的，
API目前只有对2.5-Flash的权限
无法使用API对CLI进行授权，
也无法在CLI以外的地方如Roo Code通过API使用3
=====================================================================

---

### 评论 #7 (作者: XM75236, 时间: 6个月前)

学生优惠不包含api

=================================================================================

Achievements are reached by hard work, but ruined by idleness; Actions are accomplished through thorough consideration, but destroyed by casual decision.​​  =================================================================================

---

### 评论 #8 (作者: SL52857, 时间: 6个月前)

想知道cli是否存在使用限度， 有的话怎么查看

---

### 评论 #9 (作者: OB53521, 时间: 6个月前)

=================================================================================
 [SL52857](/hc/en-us/profiles/27591634175511-SL52857)  存在额度，保存对话退出的时候可以看用了多少token。
=================================================================================

---

### 评论 #10 (作者: NX43642, 时间: 6个月前)

请问能否换成qwen3 code

---

### 评论 #11 (作者: YL96878, 时间: 6个月前)

也是赶上学生优惠的末班车了，成功拿下Gemini一年免费谢谢大佬

---

### 评论 #12 (作者: XG43628, 时间: 6个月前)

感谢大佬的分享，大佬的分享很全面，使用时问题的处理也很有经验！请问提示词有没有一些关于引导生成模板方面方便展示的呢？想学习下找找方向，感谢感谢。

==================================================================================

知难上，戒骄狂，常自省，穷途明 ==================================================================================

---

### 评论 #13 (作者: BZ29383, 时间: 6个月前)

大佬能问一下吗？？我这边已经安装了 gemini cli，但是使用的时候提示让我登录授权，我已经跳转到google授权页面了，登录了账号，但是最终卡在授权页面，一直不成功，请问需要手动登录吗？？还是说只需要去配置文件里面 配置 api key秘钥就行了？？

---

### 评论 #14 (作者: AH18340, 时间: 6个月前)

给大佬点赞，讲得很好

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #15 (作者: JY16044, 时间: 6个月前)

请问这个run_webspider_python.sh，是如何解决无法使用search_form函数的问题的

---

### 评论 #16 (作者: DW74351, 时间: 6个月前)

run_webspider_python.sh"  大佬这个主要是啥    可以分享一下嘛

---

### 评论 #17 (作者: OB53521, 时间: 6个月前)

==================================================================================
 [NX43642](/hc/en-us/profiles/30360590145559-NX43642)  Qwen3 Code或者智谱的GLM应该都可以在Claude Code里面通过修改setting.json的方式进行使用，并且也可以调用MCP工具。

==================================================================================

---

### 评论 #18 (作者: OB53521, 时间: 6个月前)

==================================================================================

[DW74351](/hc/en-us/profiles/32708480347927-DW74351)   [JY16044](/hc/en-us/profiles/29092872985623-JY16044)  已经弃用了，我是让AI帮我查看我的chromedriver位置，然后AI也发现即便都配置正确也无妨让MCP正确创建浏览器，于是它就去看了MCP工具的源码，并且修改了 **源码** ，但是修改内容我不清楚，可以在你们自己电脑上用AI帮助配置一下
==================================================================================

---

### 评论 #19 (作者: OB53521, 时间: 6个月前)

=============================================================================

[BZ29383](/hc/en-us/profiles/35797141974167-BZ29383)  这个一般是网络问题

=============================================================================

---

### 评论 #20 (作者: OB53521, 时间: 6个月前)

=============================================================================

[XG43628](/hc/en-us/profiles/30816350962711-XG43628)  没有尝试让他去生成模板，因为这和他的研究方向是冲突的。目前他会找到最适合研究的字段，然后围绕这个字段进行alpha的构建。

=============================================================================

---

### 评论 #21 (作者: DZ31138, 时间: 6个月前)

[Yprompt]([Commented] 【Community Leader - 工具配置】一文讲完用Gemini 3 Pro进行无限Alpha探索附学生优惠方法提示词在服务器中使用经验分享.md) ( [https://yprompt.252035.xyz/generate](https://yprompt.252035.xyz/generate) ) 这个是楼主自己部署的吗？打开没有注册功能。注册LinDo社区需要邀请码。好像直接访问还没法用。

---

### 评论 #22 (作者: OB53521, 时间: 6个月前)

[DZ31138](/hc/en-us/profiles/28855148380055-DZ31138)  这个提示词网站我在开会的时候忘记说了，这是一个免费开源的项目，作者可能是做了身份认证但是没做完，不过提供了所有人都能免费用的 **账号：demo，密码：demo**

---

### 评论 #23 (作者: QM70930, 时间: 6个月前)

![图片](images/img_2348a6a1e8.png)

---

### 评论 #24 (作者: BZ29383, 时间: 6个月前)

[OB53521](/hc/en-us/profiles/28890356914711-OB53521)  嗯，我后面看了，是我vscode命令行没有走代理，所以访问不到！！

---

### 评论 #25 (作者: HZ99685, 时间: 6个月前)

同样是解决浏览器问题，我反复让AI检查设置，但始终无法解决，它反而建议我放弃登录论坛的想法....无语

---

### 评论 #26 (作者: OB53521, 时间: 6个月前)

=============================================================================

[HZ99685](/hc/en-us/profiles/32603557750935-HZ99685)  MCP的代码里也需要修改，我的就是让Gemini 3修改的，然后可以用了。
=============================================================================

---

### 评论 #27 (作者: ZH41150, 时间: 6个月前)

[HZ99685](/hc/en-us/profiles/32603557750935-HZ99685)  浏览器问题你解决了吗？

---

### 评论 #28 (作者: ZH41150, 时间: 6个月前)

[OB25434](/hc/en-us/profiles/13803337427735-OB25434)  MCP浏览器的代码让AI改了好多遍，就是始终无法成功，只能登录上论坛，但是无法进行搜索

---

### 评论 #29 (作者: HZ99685, 时间: 6个月前)

[ZH41150](/hc/en-us/profiles/30443425856919-ZH41150)  没有解决，我发现用ifow能链接到浏览器的成功率更高，楼主说的修改，不知道AI是怎么修改的，发什么提示词给AI，一头雾水。

---

### 评论 #30 (作者: MZ45384, 时间: 6个月前)

感谢大佬的Gemini-cli build流程，但是毕业了的话是不是只能在咸鱼买账号或者认证才能用到Gemini3.0-preview。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

### 评论 #31 (作者: OB53521, 时间: 6个月前)

==================================================

首先非常感谢大家的评论和点赞，鉴于有一些问题是在会议上分享过的、还有一些是重复解释过的。

为了减少占用社区审核资源，大家如果有问题请发送邮件至：

```
jiangjuncheng253@gmail.com
```

==================================================

---

### 评论 #32 (作者: ZH12413, 时间: 6个月前)

从安装配置、MCP 设置到使用示例，再到学生优惠领取和服务器部署，每一步都写得清晰易懂，还贴心解决了 Mac 端搜索论坛、服务器安装卡顿、登录验证失败等常见问题。关键步骤配了操作指引，新手也能轻松跟着上手。有了这份指南，能少走很多配置弯路，高效开启 AI 助力因子挖掘，感谢整理分享！

---

### 评论 #33 (作者: HY20507, 时间: 4个月前)

好用，没有学生优惠的可以直接找大佬说的海鲜app

---

### 评论 #34 (作者: HH34943, 时间: 2个月前)

mcp那一步到底怎么解决啊，搞了很久要么说我setting.json文件路径有问题，要么说platfrom_functions.py文件有问题，改了很久geminicli还是没有worldquantbrain那些mcp的功能，还是用不了

---

