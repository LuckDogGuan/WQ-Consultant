# 如何在VSCODE上安装我发现的MCP？傻瓜式教程来了经验分享

- **链接**: 如何在VSCODE上安装我发现的MCP傻瓜式教程来了经验分享.md
- **作者**: MG88592
- **发布时间/热度**: 10个月前, 得票: 167

## 帖子正文

8月22日最新更新：forum已经集成在platfrom里了,platfrom可以就行！亮一个灯就行！！！！！！第一步：在Vscode商店下载Roo code插件；第二步：在终端输入pip install cnhkmcp ， pip install pydantic[email]，pip install email-validator第三步：打开mcp本地目录，找到untracked文件夹，路径应该是  site-packages/cnhkmcp/untracked第四步：找到该文件夹里的user_config.json打开编辑输入你在worldquantbrain的账号密码。第五步：打开VScode 的RooCode插件，左边导航栏袋鼠图标，配置一个api，以ds api为例（打开deepseek，右上角api开放平台，api keys，创建，复制，粘贴进来（记得充钱））。第六步：插件右上角... 选择mcp server点上两个按钮，然后编辑全局mcp。第八步：对 MCP 文件进行配置，示例配置文件如下：args 分别是两个 mcp 文件的绝对路径，command 是你 python 程序的绝对路径。请根据你电脑的具体路径进行更改。配置成功应该是两个绿灯（科学上网）如果平台连接失败，尝试安装（ ）接下来你有可以让他来帮你干活啦！快来创建你自己的量化公司，招募并培训你的员工吧！{"mcpServers": {"worldquant-brain-platform": {"command": "/opt/anaconda3/bin/python","args": ["/opt/anaconda3/lib/python3.12/site-packages/cnhkmcp/untracked/platform_functions.py"],"description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features. Includes 25+ MCP tools for authentication, simulation creation, alpha management, dataset access, performance analysis, competition management, user profile operations, forum integration, and advanced analytics."}}}

---

## 讨论与评论 (49)

### 评论 #1 (作者: DS48533, 时间: 10个月前)

这么好的帖子，没人夸一夸嘛，让我一步一步配置下。

---

### 评论 #2 (作者: CT44536, 时间: 10个月前)

forum mcp死活装不上，很神奇

---

### 评论 #3 (作者: LJ86847, 时间: 10个月前)

我的 forum mcp配置好了，一直连接不上

---

### 评论 #4 (作者: LZ63459, 时间: 10个月前)

🐮非常好的帖子

---

### 评论 #5 (作者: WS48176, 时间: 10个月前)

不用deepseek，用豆包行不行啊

---

### 评论 #6 (作者: MG88592, 时间: 10个月前)

CT44536LJ86847forum已经集成在platfrom里了,platfrom可以就行

---

### 评论 #7 (作者: JG91554, 时间: 10个月前)

forum mcp是不是直接通过platform mcp调用的？

---

### 评论 #8 (作者: XY53622, 时间: 10个月前)

worldquant-brain-forumglobal       MCP error -32000: Connection closed我也是报这个错，怎么解决?

---

### 评论 #9 (作者: XY53622, 时间: 10个月前)

好像worldquant-brain-forumglobal不用呢，所以不需要呢，是不是这样?

---

### 评论 #10 (作者: NC52525, 时间: 10个月前)

forum也是一直连不上

---

### 评论 #11 (作者: TY31819, 时间: 10个月前)

大佬们，请问找不到mcp本地目录是怎么回事啊

---

### 评论 #12 (作者: BW14163, 时间: 10个月前)

感谢大佬分享mcp教学，总算成功部署了

---

### 评论 #13 (作者: ZX52486, 时间: 10个月前)

一篇非常好的入门帖子，通俗易懂，实操简单

---

### 评论 #14 (作者: TS96358, 时间: 10个月前)

配置好了，太有用了

---

### 评论 #15 (作者: XZ35933, 时间: 10个月前)

我也出现了worldquant-brain-forumglobalMCP error -32000: Connection closed不知道什么原因

---

### 评论 #16 (作者: KL35691, 时间: 10个月前)

一直是MCP error -32000: Connection closedMCP error -32000: Connection closed也开了科学上网，就还有其他办法吗？

---

### 评论 #17 (作者: LX11859, 时间: 10个月前)

大家可以试试更换python版本。一开始我也是出现错误由于我的python是用anaconda管理安装的，里面有两个版本一开始用了3.12.8版本，报错之后就试试换了另外一个3.12.7版本，一下子就连上了。

---

### 评论 #18 (作者: LR93609, 时间: 10个月前)

1.他说自己完美解决了，他的办法是把后面forum的部分全部删掉，只保留platform2. 这是他处理的结果。

---

### 评论 #19 (作者: HW54322, 时间: 10个月前)

一步步配置mcp，终于成功了

---

### 评论 #20 (作者: SX13432, 时间: 10个月前)

把后面forum的部分全部删掉，只保留platform，成功。一个绿灯。

---

### 评论 #21 (作者: JD22447, 时间: 10个月前)

“8月22日最新更新：forum已经集成在platfrom里了,platfrom可以就行”,是那个cnhkmcp版本支持？1.4.8版本是否已经支持了？但这个版本的platform还是不包含forum里面的功能。

---

### 评论 #22 (作者: SS86363, 时间: 9个月前)

mcp安裝失敗怎麼回事

---

### 评论 #23 (作者: QW78773, 时间: 9个月前)

非常好帖子，使我的alpha旋转

---

### 评论 #24 (作者: YZ64617, 时间: 9个月前)

新手的一些发现和体验，希望对大家有帮助。pip 安装是会把mcp工具安装到系统/conda环境里，找起来比较麻烦。推荐直接把cnhkmcp这个包，作为一个python项目，独立放到一个地方。使用uv等工具，创建一个.venv。因为，cnhkmcp里，不只有tools。方便跑APPuser/pwd文件，在里面。独立出来，会很方便。mac系统的conda 默认环境，参考server.json如下：{"mcpServers": {"worldquant-brain-platform": {"command": "/opt/anaconda3/bin/python","args": ["/opt/anaconda3/lib/python3.12/site-packages/cnhkmcp/untracked/platform_functions.py"],"description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features. Includes 25+ MCP tools for authentication, simulation creation, alpha management, dataset access, performance analysis, competition management, user profile operations, forum integration, and advanced analytics."}}}

---

### 评论 #25 (作者: HL16090, 时间: 9个月前)

vscode 安装roo code 版本不兼容怎么办？

---

### 评论 #26 (作者: RT69601, 时间: 9个月前)

我也报错 MCP error -32000: Connection closed，查了下猜测是连接的问题，验证登录邮箱失败，pip install pydantic[email]，pip install email-validator，把上面这两个安装上就好了

---

### 评论 #27 (作者: TY59174, 时间: 9个月前)

如果出现:worldquant-brain-forumMCP error -32000: Connection closed可以修改 forum_function.py, 增加下面的第30行:# Initialize forum MCP servertry:from mcp.server.fastmcp import FastMCPforum_mcp = FastMCP('brain_forum_server')forum_mcp.run()except ImportError:# Fallback for testingforum_mcp = None

---

### 评论 #28 (作者: TY59174, 时间: 9个月前)

第30行:  forum_mcp.run()

---

### 评论 #29 (作者: EZ95675, 时间: 9个月前)

谢谢分享！现在已经安装成功。请问有具体的使用教学么？

---

### 评论 #30 (作者: MM57166, 时间: 8个月前)

厉害

---

### 评论 #31 (作者: DL67446, 时间: 8个月前)

大佬，我按照你的步骤编写了args和command，但没有显示出最后的结果，是哪个代码还需要运行一下吗？但我看没有运行的按钮啊

---

### 评论 #32 (作者: XY50888, 时间: 8个月前)

就是需要这种Step by step的好贴子，谢谢

---

### 评论 #33 (作者: HZ99685, 时间: 8个月前)

按照以上评论里大家的操作都操作了一遍，platform还是显示MCP error -32000，无语了。搞了一整天还是找不到问题出在哪里。python314绝对路径在c：\program files\python314,难道必须在users下才行吗？求解。我找到问题所在了，参照trae配置的那篇帖子，command这里的路径不用写全，只要写python就可以了，大家避坑。

---

### 评论 #34 (作者: WC83400, 时间: 8个月前)

MCP必须科学上网才能用吗？

---

### 评论 #35 (作者: WS63384, 时间: 7个月前)

谢谢分享，终于安装成功了。

---

### 评论 #36 (作者: SC16582, 时间: 7个月前)

我使用这个MCP经常遇到无法连接服务器的情况，不清楚到底是哪里的问题，后来自己重写了一个本地的MCP，现在多数功能可以正常使用了，还需要进一步的完善，大家要是遇到同样的情况，特别是无法连接服务器，或者无法提交回测，或者回测超时，你就能理解我为什么要重写代码了。

---

### 评论 #37 (作者: HL16090, 时间: 6个月前)

成功安装，谢谢大佬

---

### 评论 #38 (作者: YT52851, 时间: 6个月前)

感谢大佬的分享，请问下这个安装到远程机上，还是电脑本地使用呢

---

### 评论 #39 (作者: TS11790, 时间: 6个月前)

这个问题roo code打不开，大家有遇到吗

---

### 评论 #40 (作者: TS11790, 时间: 6个月前)

我找到问题所在了，VSCODE版本太老，与roocode 不兼容

---

### 评论 #41 (作者: WC64477, 时间: 6个月前)

随着上下文增加，功能开发，token消耗还是很大的，尽量用免费的模型。

---

### 评论 #42 (作者: HJ90192, 时间: 6个月前)

我配置到第六步，Roo code 插件右上角三个点...点开里面没有MCP SEVER选项可能是什么原因呢？前面步骤都正确进行了的

---

### 评论 #43 (作者: TS11790, 时间: 6个月前)

回答HJ90192，更新了的，在设置里面，自己多找找，能找到的

---

### 评论 #44 (作者: JC31003, 时间: 6个月前)

请问我的第六步为什么没mcp servers这个选项

---

### 评论 #45 (作者: BX86068, 时间: 5个月前)

感谢，已经安装成功，但是deepseek总是在按照他原本设定好的固定的工作流程来处理，每次新任务都要浪费不少token，得再mcp的workflow上下功夫了

---

### 评论 #46 (作者: YB15978, 时间: 5个月前)

-------------------------------------------------------------------------------------------------------------------------感谢大佬分享，我也报MCP error -32000: Connection closed  错误，按楼上的邮箱验证也pip了，还是报错，还有啥绝招可以使用呢----------------------------------------------------------------------------------------------------------------

---

### 评论 #47 (作者: YB15978, 时间: 5个月前)

----------------------------------------------------------------------------------------------------------------MCP error -32000: Connection closed  错误 居然突然成功了需要仔细检查 配置文件，这个错误大概率是配置路径不正确，可以把配置的"command":"args"放到命令行中运行, 出现如下显示，确保路径没问题C:\Users\17352\AppData\Local>C:\Users\17352\AppData\Local\Programs\Python\Python313\python.exe C:\Users\17352\AppData\Local\Programs\Python\Python313\Lib\site-packages\cnhkmcp\untracked\APP\chmcp\untracked\platform_functions.pyWorldQuant BRAIN MCP Server Starting...路径正确后，roo code中重新载入配置，应该就没问题了。----------------------------------------------------------------------------------------------------------------

---

### 评论 #48 (作者: YC13885, 时间: 4个月前)

cnhkmcp这个库是已经没有了吗，我pip的时候找不到，github上也搜索不到呢

---

### 评论 #49 (作者: ZD74815, 时间: 3个月前)

Date/time: 2026-03-26T10:50:05.730Z
Extension version: 3.51.1
Provider: deepseek
Model: deepseek-chat

Error executing MCP tool:
MCP error -32001: Request timed out这是什么原因，回测均失败了

---

