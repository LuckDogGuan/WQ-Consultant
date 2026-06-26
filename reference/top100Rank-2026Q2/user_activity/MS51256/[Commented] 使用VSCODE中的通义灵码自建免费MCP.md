# 使用VSCODE中的通义灵码自建免费MCP

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwiXJWqQTSE6D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAcFodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzY2MTcwMTkwNzM5NDMtJUU0JUJEJUJGJUU3JTk0JUE4VlNDT0RFJUU0JUI4JUFEJUU3JTlBJTg0JUU5JTgwJTlBJUU0JUI5JTg5JUU3JTgxJUI1JUU3JUEwJTgxJUU4JTg3JUFBJUU1JUJCJUJBJUU1JTg1JThEJUU4JUI0JUI5TUNQBjsIVDoOc2VhcmNoX2lkSSIpMjA3MmRmMWQtOTg0Ny00NzE5LWFkMWQtYWE0NDcyZGVlNTQ4BjsIRjoJcmFua2kOOgtsb2NhbGVJIgp6aC1jbgY7CFQ6CnF1ZXJ5SSIMTVM1MTI1NgY7CFQ6EnJlc3VsdHNfY291bnRpLQ%3D%3D--93ededbed1ff4425a77411620faf815463a19264
- **作者**: WY85693
- **发布时间/热度**: 7个月前, 得票: 12

## 帖子正文

论坛里面大家讨论的都很多，但是还是会踩各种各样的坑。这次我来手把手教大家怎么在VSCODE中利用阿里的通义灵码建一个免费的MCP。首先下载安装VSCODE；在插件市场安装通义灵码；安装大佬们编写好的mcp库。pip install cnhkmcp 。此时需要你明确清楚的知道你的cnhkmcp安装的位置，后面需要导入脚本。如果不知道，可以直接在通义灵码当中询问，【我安装的cnhkmcp的位置在哪？】打开通义灵码的个人设置（要登陆）。在右上角点击新增MCP-配置文件添加 。这里coomand是写你当前执行python的运行位置。(版本要在3.11以上)。args是你刚刚安装cnhkmcp包位置中的platform_functions.py。description是这个mcp的一个简单描述，用于分辨，怎么写都行。"WorldQuant BRAIN Platform Mcp Server - Comprehensive trading platform integration with simulation managementalpha operations, and authentication. Credentials are stored inuser config.json in the same directory. Provides tools for creatingsimulations, checking status, managing alphas, and accessing platform features."配置好了之后，在相同位置的user_config.json中，写入你的brain平台的账号密码。所有内容配置好了之后，有个测试，点击测试，在所有步骤正确的情况下，就可以查看大佬们写的mcp工具了。最后希望大家都能装好自己的MCP。:D

---

## 讨论与评论 (9)

### 评论 #1 (作者: MS51256, 时间: 6个月前)

===============================MS51256的评论===============================感谢大佬的分享，mcp不断在不同的平台不同的ai中应用，在可预见的未来国区的因子质量将会被ai显著提升，期待每一位顾问的分享，期待国区再创佳绩。================================Do your best ================================

---

### 评论 #2 (作者: CC52425, 时间: 6个月前)

这个是需要走梯子吗， 按照步骤操作后，提示failed to initialize MCP client for worldquant-brain-platform: transport error: context deadline exceeded使用命令行执行了下 python  /xxxx/platform_functions.py    xxxx为个人路径， 会一些提示报错，根据报错改进吧， 我这边是因为缺少模块，所以pip 安装了模块了正常可以使用了

---

### 评论 #3 (作者: CY76111, 时间: 6个月前)

大佬，怎么用呢？

---

### 评论 #4 (作者: WY85693, 时间: 6个月前)

CC52425不需要走梯子，这个看起来主要是因为你的网络环境问题。建议禁用或检查防火墙，更新vscode和里面的插件

---

### 评论 #5 (作者: TT21691, 时间: 6个月前)

对于免费的来说，还是不错的，在实际的工作流中，可以先使用免费的测试，效果不错再使用一些付费的模型。

---

### 评论 #6 (作者: AH18340, 时间: 6个月前)

通义灵码用了感觉效果不是很好，不懂其他大佬的如何=============================================================================The best time to plant a tree is 20 years ago. The second-best time is now.=============================================================================

---

### 评论 #7 (作者: FF65210, 时间: 6个月前)

ai经常显示调用mcp工具错误是什么原因，前两天刚装下来，还不太会用，能出一份通义mcp使用攻略吗

---

### 评论 #8 (作者: CC21336, 时间: 6个月前)

一直用的DeepSeek，每天耗费2块，准备试一试这个免费版本

---

### 评论 #9 (作者: HY20507, 时间: 4个月前)

条理很清晰，所有的mcp安装差不多都是这个路数，可以当作一个范本，向大佬致敬

---

