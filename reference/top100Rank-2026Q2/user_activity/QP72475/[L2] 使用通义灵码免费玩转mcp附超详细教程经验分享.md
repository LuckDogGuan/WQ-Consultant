# 使用通义灵码免费玩转mcp，附超详细教程！经验分享

- **链接**: [L2] 使用通义灵码免费玩转mcp附超详细教程经验分享.md
- **作者**: HW93328
- **发布时间/热度**: 10 months ago, 得票: 122

## 帖子正文

**8月22日最新更新：forum已经集成在platfrom里了,platfrom可以就行**

Lingma是阿里旗下的一款AI coder，可以集成在vscode、pycharm等IDE中帮助代码的编写，当然它也支持使用智能体+MCP。Lingma插件中自带千问Qwen的三款模型（免费使用）就像在网页问答一样，因此在Lingma中使用mcp就不需要额外的api付费了。

接下来就进入安装使用教程：

1.安装Lingma插件，以Pycharm为例

在设置中找到【插件】，搜索Lingma进行安装，安装后会提示重启IDE，重启即可。

![图片](images/img_24225eba21.png)

2.安装mcp——步骤1

安装cnhkmcp就不多说了，终端执行以下命令

```
pip install cnhkmcp
```

到了第一个可能会困扰大家的地方，如何找到cnhkmcp安装的路径，并找到我们需要的两个文件路径呢

没有问题，一样使用Lingma可以解决

![图片](images/img_924f52a4c8.png)

我们需要的两个文件就在这一路径的untracked目录下，进入untracked目录复制具体的文件路径即可。

（这里我是mac系统，如果是windows其实就是路径不一样而已，可能就是一个C盘的路径）

接下来我们继续寻找python解释器的路径，同样问Lingma就可以了

![图片](images/img_218ad2d532.png)

！！请注意，要使用这个mcp你的python版本必须在3.11及以上，不然的话在第一步pip的时候就会出错

这里最后Lingma也是给出了我们想要的python路径，如果是windows则以python.exe结尾

3.安装mcp——步骤2

接下来我们进行mcp的配置，点击头像进入个人中心->mcp服务 就可以进入如下界面，再点击红框中的图标，进入mcp配置文件。

![图片](images/img_e06f7d10e2.png)

mcp配置文件

将command和args对应替换，保存关闭即可。

![图片](images/img_6f0f3f3701.png)

此时platform可能还无法加载成功，因为还需要安装一个库

pip install email-validator

安装后刷新一下两个mcp，应该就能正常使用了。附一张我和mcp对话的实例。

（config.json不要忘记填入自己的账号）

![图片](images/img_6fa14a1949.png)

好了，到此mcp就配置好了，如果觉得有用，请一定要给个小赞！感谢！

---

## 讨论与评论 (27)

### 评论 #1 (作者: MY21251, 时间: 10 months ago)

先赞后看，顺便补充一点：通义灵码的对话框左下角有3个选项，选“智能体”更好些，其他选项好像无法正常使用，正在尝试中。之前用的deepseek的api，1小时烧了2块钱，还是用免费的吧。

---

### 评论 #2 (作者: JG91554, 时间: 10 months ago)

选“智能体” ，可以调用mcp,但执行失败，

执行 MCP 工具失败worldquant-brain-platform/search_forum_posts

Paramters:

`{
"search_query": "news dataset template"
}`

---

### 评论 #3 (作者: ZY16272, 时间: 10 months ago)

感谢大佬整理，为我AI跑alpha提供了莫大帮助

---

### 评论 #4 (作者: BW14163, 时间: 10 months ago)

先赞一个，回头就拿来试试，之前买了deepseek的

---

### 评论 #5 (作者: JZ18078, 时间: 10 months ago)

参照这个在vscode里也安装成功，感谢

---

### 评论 #6 (作者: HW54322, 时间: 10 months ago)

顶一下，感谢

---

### 评论 #7 (作者: XW61573, 时间: 10 months ago)

我也安装成功，但读取value factor trend score时总是提示失败，然后工具就找不到了，不知道怎么回事

---

### 评论 #8 (作者: LG79469, 时间: 10 months ago)

需要的两个文件就在这一路径的untracked目录下，这里的两个文件指的什么呀，是untracked目录下forum_functions.py和platform_functions.py吗？

---

### 评论 #9 (作者: LN13989, 时间: 10 months ago)

安装成功，mcp的api感觉不是很稳定，有时候调用会超时

---

### 评论 #10 (作者: JZ18078, 时间: 10 months ago)

在对话框的底部，看到有一个“工具”，把工具打开，就可以正确获取到value factor trend score相关数据了。

---

### 评论 #11 (作者: TB73554, 时间: 10 months ago)

```
请问我的两个mcp服务连接失败是因为什么？
```

---

### 评论 #12 (作者: NC52525, 时间: 10 months ago)

效果怎么样？

---

### 评论 #13 (作者: MZ35432, 时间: 9 months ago)

手把手已经配置完成，拉了最新的 cnhkmcp 包里面的路径有些小变化

---

### 评论 #14 (作者: KJ35210, 时间: 8 months ago)

按博主的操作步骤，两个文件，只成功安装一个，另一个没成功是为啥啊

worldquant-brain-forum

C:\Users\lenovo\AppData\Local\Programs\Python\Python311\python.exe

failed to initialize MCP client for worldquant-brain-forum: transport error: context deadline exceeded

---

### 评论 #15 (作者: JJ69164, 时间: 8 months ago)

你的错误解决了吗？我以为是我无法访问论坛导致的，能访问论坛的时候测试也是报错错误信息

failed to initialize MCP client for worldquant-brain-forum: transport error: context deadline exceeded

---

### 评论 #16 (作者: KY99488, 时间: 8 months ago)

大家一定注意一下，帖主截的图不完整。在args的配置上，我们要选择的是untracked上的platform_functions.py
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
即：

```
"args": [  "C:/Anaconda/envs/koko/Lib/site-packages/cnhkmcp/untracked/platform_functions.py"]#路径替换为你文件的路径
```

不然就会报错“failed to initialize MCP client for worldquant-brain-forum: transport error: context deadline exceeded”。
如若评论对你有帮助请点赞，谢谢

---

### 评论 #17 (作者: ZM82620, 时间: 8 months ago)

感谢大佬的分享和评论里的各位大佬的建议！我也安装成功了！

分享几个我在使用时遇到的小问题给可能会遇到的朋友一些帮助

1、除了上面大佬说的要切换成智能体，还需要打开工程目录（随便一个都行），不然就算切换成智能体也仅进入 **智能问答模式** ，模型无法调用 MCP 工具

2、Node.js 版本须在 v18 及以上，npm 版本须在 v8 及以上。版本过低可能导致工具调用失败

---

### 评论 #18 (作者: AL96309, 时间: 7 months ago)

感谢楼主分享，通过楼主方法成功用pycharm连接了mcp,另外附上文中需要编辑的json代码，以便其他顾问使用。将command和args部分按照文中描述替换即可。

{
"mcpServers": {
"worldquant-brain-platform": {
"command": "C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe",
"args": [
"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\Lib\site-packages\cnhkmcp\untracked\platform_functions.py"
],
"description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features. We also have a forum MCP here, WorldQuant BRAIN Forum MCP Server - Forum interaction and knowledge extraction tools. Provides glossary access, forum post reading, and community features. Credentials are stored in user_config.json in the same directory. Supports headless browser automation for forum scraping and content extraction."
}
}
}

---

### 评论 #19 (作者: YZ29225, 时间: 7 months ago)

这个后面怎么用呢？怎么生成并回测因子呢？

---

### 评论 #20 (作者: JQ70858, 时间: 7 months ago)

参考论坛这篇和另一篇在vscode上安装deepseek的文章，综合使用效果更佳。

按照楼主的步骤在vscode中成功安装通义并开始使用。

注意mcp配置文件时将command和args对应替换，保存关闭即可（这里配置的是论坛和平台两个内容所以为两段话）

并不是一毛不拔，但是对自己的知识储备尚无自信，所以没使用付费的deepseek，想通过初期多练习提升一点后再尝试使用付费的工具。

---

### 评论 #21 (作者: FP65808, 时间: 7 months ago)

老师，问一下为什么我用Lingma在对话完一次，我的mcp里的工具就是空的呢？我要手动刷新，才能出来那些工具？望求指导。 ![图片](images/img_29e5e4a5da.png)

---

### 评论 #22 (作者: CC73983, 时间: 6 months ago)

Roo Code切成Qwen的本地模型和这个有区别吗

---

### 评论 #23 (作者: CG95707, 时间: 6 months ago)

先赞一个，感谢大佬的分享

---

### 评论 #24 (作者: YQ84572, 时间: 6 months ago)

很详细的教程，感谢分享，成功配置好了mcp
==============================================================================================================================

---

### 评论 #25 (作者: JC31003, 时间: 5 months ago)

现在MCP工具是不是不能正常使用了？

---

### 评论 #26 (作者: CL96463, 时间: 3 months ago)

跟着大佬的配置，果然成功了，有些只能配置成功一个，即platform方法，我刚开始也是这样，其实是因为forum里面并没有进行mcp封装，封装后就都可以配置成功啦！

---

### 评论 #27 (作者: YM59389, 时间: 1 month ago)

目前试过了，首先非常感谢大佬的分享。然后说一下这个使用中可能的情况，因为使用的时阿里的通译灵码，所以免费，从而也导致这个有些方面不是很完善。所以对于很多需要稍微长点的时间响应的，例如进行回测等操作，就会触发通译灵码调用mcp的超时报错。我目前的方式时尝试使用py脚本 调用mcp的回测方法，进行回测，因为通译灵码 使用指令 调用脚本是不会有超时的问题

---

