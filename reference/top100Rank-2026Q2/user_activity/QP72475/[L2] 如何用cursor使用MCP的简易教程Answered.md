# 如何用cursor使用MCP的简易教程Answered

- **链接**: [L2] 如何用cursor使用MCP的简易教程Answered.md
- **作者**: ZH41150
- **发布时间/热度**: 10 months ago, 得票: 54

## 帖子正文

第一步去官网下载cursor，认准这个图标 ![图片](images/img_2ba2877054.png)

第二步 需要中文版的，去应用商店安装个中文插件即可

![图片](images/img_34971dfec4.png)

第三步 安装cnhkmcp——到new chat里输入pip install cnhkmcp

![图片](images/img_fbacb8c6b9.png)

想要方便的话可以直接告诉他你想装在哪个盘，哪个文件里，方便一会定位，可以节省时间

第四步 设置MCP文件——跟着图片标志操作

![图片](images/img_594fbd9363.png)  ![图片](images/img_e4ce6650a0.png)

记得在user_config.json输入 **worldquantbrain** 的账号密码

MCP设置代码在群里有，可以自行群里领取

设置这里要留意看清楚，

worldquant-brain-platform

worldquant-brain-forum

这两个后缀不一样的，填地址的时候不要填错了

注意！自8月起，俩个功能已经合并到一个mcp里了，所以你不用装两个。

第五步 展示安装成功

![图片](images/img_bda57dd537.png)

第六步 直接在new chat里输入测试连通性

![图片](images/img_c5d0c32cd8.png) 缺失的文件，他会咨询你是否安装，缺啥装啥，装好他会自动重新测试一遍

记得需要打开论坛的时候必须科学上网~接下来可以自由使用cursor干活了

---

## 讨论与评论 (23)

### 评论 #1 (作者: ZZ37826, 时间: 10 months ago)

请问能发一下MCP的设置代码吗？我的群里好像没有。

---

### 评论 #2 (作者: HH54988, 时间: 10 months ago)

下载了MCP为什么他说我没有那些工具

---

### 评论 #3 (作者: LJ86847, 时间: 10 months ago)

请问可以分享一下MCP的设置代码吗

---

### 评论 #4 (作者: WL21087, 时间: 10 months ago)

+1 MCP代码新手村里也没有

---

### 评论 #5 (作者: CM31430, 时间: 10 months ago)

我用的mac，tool刚开始提示为0，需要将那个user_config这个文件export到环境里，然后就能看到tools了

---

### 评论 #6 (作者: ZZ37826, 时间: 10 months ago)

请问可以分享一下MCP代码？

---

### 评论 #7 (作者: ZH41150, 时间: 10 months ago)

{

"mcpServers": {

"worldquant-brain-platform": {

"command":  "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe",

"args": [

"D:\cnhkmcp\cnhkmcp\untracked\platform_functions.py"

],

"description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication.Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features."

},

"worldquant-brain-forum": {

"command":  "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe",

"args": [

"D:\cnhkmcp\cnhkmcp\untracked\forum_functions.py"

],

"description": "WorldQuant BRAIN Forum MCP Server - Forum interaction and knowledge extraction tools. Provides glossary access, forum post reading, and community features.Credentials are stored in user_config.json in the same directory. Supports headless browser automation for forum scraping and content extraction."

}

}

} [ZZ37826](/hc/en-us/profiles/33841678941207-ZZ37826)  [LJ86847](/hc/en-us/profiles/31133393299479-LJ86847)  [WL21087](/hc/en-us/profiles/30729062429591-WL21087)   先凑合用这个吧，我还没去更新最新版的代码

---

### 评论 #8 (作者: LX71036, 时间: 9 months ago)

========

之前在群里看到各位大佬用mcp用得很智能，而且还有设置一些工作流，但是错过了那些直播，所以来论坛找找，感觉博主写的很清晰明了，就来试试看自己能不能设置出来，感谢大佬的分享！

=========

---

### 评论 #9 (作者: LQ97658, 时间: 9 months ago)

感谢分享，跟着教程已经成功安装！

---

### 评论 #10 (作者: EZ95675, 时间: 9 months ago)

请问安装完之后应该怎么用呢？比方说MCP里面有get_documentations这种函数，这些是怎么调用的呢？是直接在Roo Code对话框里说，还是要通过Python调用？

谢谢解答！

---

### 评论 #11 (作者: BW14163, 时间: 8 months ago)

******************************************************************************************************************
感谢大佬分享关于cursor中使用MCP的细致教程。

目前还是在用vscode，收藏了，后期需要转cursor时，直接拿来用

祝大佬vf高高 ，base多多！！

********************************每天坚持学一个知识点，尽量不混信号，不过拟合***********************

---

### 评论 #12 (作者: QM70930, 时间: 7 months ago)

我的论坛一直无法使用，我也尝试下载了这个驱动，也没有啥用，又没有用过的可以给我分享下经验

![图片](images/img_c0d6de57f2.png)

---

### 评论 #13 (作者: XW75773, 时间: 7 months ago)

您好，大佬，我想问下我在cursor配置完，路径也对，但是这样的，这个是怎么回事尼 ![图片](images/img_5bd4d8fbd2.png)

---

### 评论 #14 (作者: JS34795, 时间: 6 months ago)

论坛功能无法使用platforms能够正常使用

---

### 评论 #15 (作者: YC48942, 时间: 6 months ago)

感谢分享！很实用的新手教程

---

### 评论 #16 (作者: MK45089, 时间: 6 months ago)

[XW75773](/hc/en-us/profiles/34367768980631-XW75773)  应该是这三个路径没有配置对：

1、

"args": [

"D:\cnhkmcp\cnhkmcp\untracked\forum_functions.py"

2、

"args": [

"D:\cnhkmcp\cnhkmcp\untracked\platform_functions.py"

3、"command":  "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe",   可以检查自己计算机对应文件的实际位置，然后更换

---

### 评论 #17 (作者: PL95083, 时间: 6 months ago)

感谢大佬，非常的详细

---

### 评论 #18 (作者: YQ84572, 时间: 6 months ago)

这篇帖子提供了非常实用且清晰的Cursor配置指南，尤其对需要连接平台的用户来说简直是“及时雨”。作者将复杂的安装过程分解为六大步骤，从软件下载、语言设置到关键的MCP配置，每个环节都给出了具体操作和避坑提示——最贴心的是，指南不仅教“怎么做”，还解释了“为什么”：例如建议自定义安装路径以便后续定位，体现了对用户效率的周全考虑。整体来看，这份教程既降低了使用门槛，又通过流程化的梳理提升了配置成功率，展现了社区共享经验的宝贵价值。期待更多人能借此高效地驾驭AI工具，释放生产力！

---

### 评论 #19 (作者: ZL35633, 时间: 6 months ago)

感谢大佬的分享。
我的配置如下，供大家参考。

{

"mcpServers": {

"worldquant-brain-platform": {

"command": "/opt/homebrew/anaconda3/envs/mcp/bin/python3",

"args": [

"/Users/xxxx/workspace/consultant/cnhkmcp/untracked/platform_functions.py"

],

"description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features."

}

}

}

---

### 评论 #20 (作者: YM58332, 时间: 6 months ago)

您好，群怎么加入啊？

---

### 评论 #21 (作者: KB56639, 时间: 5 months ago)

1. ![图片](images/img_2d6b3c1a7d.png) 请问大佬这个怎么办呢？

---

### 评论 #22 (作者: YY71984, 时间: 4 months ago)

请问各位大佬，配置完应该怎么使用呢？怎么找到可以提交的Alpha呢？

---

### 评论 #23 (作者: XW75773, 时间: 3 months ago)

感谢大佬分享

---

