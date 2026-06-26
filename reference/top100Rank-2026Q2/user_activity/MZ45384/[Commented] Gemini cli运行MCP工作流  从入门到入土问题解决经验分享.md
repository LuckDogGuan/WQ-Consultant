# Gemini cli运行MCP工作流  从入门到入土问题解决经验分享

- **链接**: [Commented] Gemini cli运行MCP工作流  从入门到入土问题解决经验分享.md
- **作者**: TL53163
- **发布时间/热度**: 6个月前, 得票: 72

## 帖子正文

在拜读了OB53521大佬的 ***AI自动探索Alpha*** 文章后，我大受震撼，500-800次回测出3个Ra有图有真像，简直在告诉我抄作业就能过上每天都有Ra交的日子。回头再看自己还在每天往ppa池子里投毒，让我下定决心要把这个工作流跑起来。下面是我从零搭建跑起来该工作流的流程和遇到的问题，希望能帮到大家。

**重点** ：

1. 获取一个Gemini学生认证的Google账号 ✨
2. 安装并运行Gemini Cli
3. 使用cnhkmcp执行OB大佬的工作流

### **一、获取一个Gemini学生认证的Google账号** ✨

学生认证非常重要，我一下午消耗了上千万token，但这是免费的

**途径1： [[Commented] 【Community Leader - 工具配置】一文讲完用Gemini 3 Pro进行无限Alpha探索附学生优惠方法提示词在服务器中使用经验分享.md]([Commented] 【Community Leader - 工具配置】一文讲完用Gemini 3 Pro进行无限Alpha探索附学生优惠方法提示词在服务器中使用经验分享.md)**

阅读此文章的 **学生优惠** 部分，花20￥左右即可弄到    ***麻烦程度：高***

**途径2:**  某鱼直接搜索 `gemini学生认证成品号`，花不到100￥买一个认证过的Google账号         ***麻烦程度：低***

**问题1** ：途径1访问失败，显示 ` ***This offer is not available*** `

**答** ：1.切换Google Play的地区为 ***美区，*** 可以搜到ChatGpt就改成功了。

2.使用所有你可用的USA节点尝试访问认证页面

3.尝试换Google账号、换梯子

如果仍不能解决，使用途径2，简单方便，就是有跑路风险

### **二、安装并运行Gemini Cli 💫**

安装，运行教程依旧参考OB的文章，推荐使用 **命令行**

![图片](images/img_504ad37acc.png)

**问题1** ：安装完成，输入gemini命令后选择Google账号登录，网页认证失败如图

![图片](images/img_ba11040d1c.png)

**答** ：1. 使用命令  set HTTP_PROXY= [http://127.0.0.1:7890/](http://127.0.0.1:7890/)

set HTTPS_PROXY= [http://127.0.0.1:7890/](http://127.0.0.1:7890/)

***7890*** 是你梯子软件的端口，Clash默认是7980。命令行输入这两条后再次访问即可成功登录，但是 **仅                限当前窗口生效** ，关闭重开得再设置。

2.Win+S搜索`编辑系统环境变量` -> `环境变量` ，在用户变量或系统变量中添加两条即可

![图片](images/img_eade750cf2.png)

### **三、使用cnhkmcp执行OB大佬的工作流 🎯**

**问题1** ：如何安装和使用cnhkmcp

**答** ：1.在cli中对话发送pip insall cnhkmcp，它会帮你安装。如果想更新，使用pip install --upgrade cnhkmcp。

2.修改gemini的settings.json配置,目录一般是C:\Users\Administrator\.gemini。如果找不到，cli问一下它装在哪里了。Settings.json内容如下，python地址替换成自己的，如果找不到地址可以让gemini帮你找。

```
 {   "ide": {     "hasSeenNudge": true   },  "mcpServers": {    "worldquant-brain-platform": {      "command": "D:\\python\\python.exe",      "args": [        "D:\\python\\Lib\\site-packages\\cnhkmcp\\untracked\\platform_functions.py"      ],      "description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features."    }  },   "security": {     "auth": {       "selectedType": "oauth-personal"     }   },   "ui": {     "theme": "Atom One"   },   "general": {     "previewFeatures": true   } }
```

3.对话输入`测试worldquant-brain-platform连接`，它会调用mcp的登录，如果显示成功，mcp功能正常。

![图片](images/img_07bca86359.png)

**问题2** ：工作流如何使用

**答** ：1.将OB帖子内的工作流保存为md文件，相较于直接对话发送工作流，更利于AI读取和理解。

2.使用`@workflow.md 尝试帮我点亮GLB的anl，delay：1.......` 这样的方式，可以选择工作流文件，                    后面再跟上自己的定制要求。

***注意*** ：@默认读取的是当前工作目录(打开命令行的目录)，最好建一个专门的文件夹存放各种供                       gemini使用的文件。

OB大佬的工作流很有用，我跑了一下午虽然没跑出Ra，但也出了不少高质量的ppa。需要注意的是工作流中很多地方让ai读取本地文件(如官方的Getting started with xxx dataset文档，论坛的各种alpha提升技巧等)，需要自己找并存起来，当ai的 **知识库** ，这样才能更大程度发挥工作流的作用。

如果对此工作流有什么优化的建议，可以访问

[https://www.notion.so/RULE-2c0126a83af380ea9164f02380ea19b5?source=copy_link](https://www.notion.so/RULE-2c0126a83af380ea9164f02380ea19b5?source=copy_link)

希望大家都能解放双手，过上每天都有RA交的日子！

---

## 讨论与评论 (11)

### 评论 #1 (作者: HZ99685, 时间: 6个月前)

总结很到位，收藏了，本地文件能否也贡献一下啊，或者开个共享文档让大家补充？

---

### 评论 #2 (作者: SL19872, 时间: 6个月前)

能否放服务器上24小时不间断运行呢

---

### 评论 #3 (作者: LG87838, 时间: 6个月前)

如果用不习惯cli，google版的vs code叫antigravity，大模型的使用流程和楼主分享的一致，免费下载后就可以使用。

----------------------------------------------------------------------------------------------------

慢就是快，相信时间的力量！

----------------------------------------------------------------------------------------------------

---

### 评论 #4 (作者: JG11137, 时间: 6个月前)

我是自己电脑跑的
1. 关于学生的账号， 可以自己申请账号，某鱼找 认证，  25米 全部搞定，
2. gemini 登录认证 也可以不用设置环境变量， clash  general 中 安装service mode ，打开 TUN mode， 即可

---

### 评论 #5 (作者: YQ84572, 时间: 6个月前)

总结的很到位，马上尝试一下，不断总结模板和思路，剩下的就交给ai工具探索，很好的工作流
---------------------------------------------------------------------------

感谢大佬的分享，祝大佬vf0.9+

---------------------------------------------------------------------------

---

### 评论 #6 (作者: MZ45384, 时间: 6个月前)

大佬总结的很全面，进一步了解了具体操作步骤，请问目前在IND有成效吗

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

### 评论 #7 (作者: TS96358, 时间: 5个月前)

=====================早日冲上GrandMaster============================================== 感谢佬给出的在布置Gemini过程中遇到的问题的解决方案，帮了我大忙了，祝佬冲上Grandmaster

==================纸上得来终觉浅，绝知此事要躬行========================================

---

### 评论 #8 (作者: BW14163, 时间: 4个月前)

感谢分享，很不错的指导帖子，gemini3 登录的问题解决了

---

### 评论 #9 (作者: LL40122, 时间: 4个月前)

cli 和模版都准备到位了，就差这个MCP工作流，学习引进来， 感谢分享~！

---

### 评论 #10 (作者: HH34943, 时间: 2个月前)

geminicli怎么用不了，显示负载过重，我现在连测试wqb连接都一直运行显示不出结果，你们可以正常使用吗

---

### 评论 #11 (作者: HH34943, 时间: 1个月前)

大佬能出篇文章说说antigravitycli怎么使用mcp工具吗，我老是没办法让他使用mcp，找不到问题出在哪里

---

