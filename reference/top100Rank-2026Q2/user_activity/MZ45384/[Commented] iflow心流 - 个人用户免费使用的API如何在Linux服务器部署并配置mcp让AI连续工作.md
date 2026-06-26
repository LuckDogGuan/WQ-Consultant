# iflow心流 - 个人用户免费使用的API，如何在Linux服务器部署并配置mcp，让AI连续工作

- **链接**: [Commented] iflow心流 - 个人用户免费使用的API如何在Linux服务器部署并配置mcp让AI连续工作.md
- **作者**: LW67640
- **发布时间/热度**: 6个月前, 得票: 72

## 帖子正文

iFlow目前有两种免费的使用方式：

1. iflow CLI 是一款终端AI助手，类似流行的Gemini cli, 可以分析代码、执行编程任务、处理文件操作。

2. 提供了API接口，可以结合Roo， Cline等使用，最近论坛里流行的72变也可以用。

```
如果你还在观望大模型，没有付费订阅，没有稳定的接口，推荐一试。如果你的服务器还没有一个24小时打工的AI助手，也推荐一试。
```

我这里主要说明前一种，因为可以在我们的服务器上用起来，结合tmux，给一个指令：在没有成功提交之前，不要询问我。。。第二天睡醒看看有木有好运。

iflow CLI的安装方法如下，官网也有详细的教程可以参考。

打开vs code，ssh到服务器，执行以下命令，我的是linux服务器，运行第一条命令一次通过。

```
# 一键安装脚本，会安装全部所需依赖bash -c "$(curl -fsSL https://gitee.com/iflow-ai/iflow-cli/raw/main/install.sh)"# 已有Node.js 20+npm i -g @iflow-ai/iflow-cli@latest
```

安装好以后，执行iflow，就进入命令行界面。这里需要额外的一个申请API的步骤：

1. 访问 [心流官网](https://iflow.cn/?spm=54878a4d.2ef5001f.0.0.7c1257832yovzX&open=setting) 完成注册
2. 在用户设置页面生成 API KEY
3. 在 iFlow CLI 中选择 API Key 登录并输入密钥

接下来就可以配置MCP了，这里有一点小坑，我本地和服务器都遇到了一摸一样的问题：

1. MCP的配置文件在 ~/.iflow/settings.json

2. 参考CNHKMCP里的示例文件，修改后粘贴进去，示例如下：

```
{  "cna": "DSdfksdllsklfdsljfsdljflsdjfa;dfja;f",  "selectedAuthType": "iflow",  "apiKey": "sk-Xxxxxxxxxx",  "baseUrl": "https://apis.iflow.cn/v1",  "modelName": "kimi-k2-thinking",  "searchApiKey": "sk-Xxxxxxxxxx",  "mcpServers": {    "worldquant-brain-platform": {      "command": "your_directory/bin/python",      "args": [        "your_directory/lib/python3.12/site-packages/cnhkmcp/untracked/platform_functions.py"      ],      "description": "WorldQuant BRAIN Platform MCP Server. Comprehensive trading platform integration with simulation management, alpha operations, and authentication.\nCredentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features.\n\nWorldQuant BRAIN Forum MCP Server. Forum interaction and knowledge extraction tools. Provides glossary access, forum post reading, and community features. Credentials are stored in user_config.json in the same directory. Supports headless browser automation for forum scraping and content extraction."    }  }}
```

这里可能遇到问题，文件配置好以后，再次登陆iflow会提示settings错误，无法启动。我的解决方法：

1. 不做任何修改再次运行 iflow， 会恢复正常启动。

2. 现在再次修改settings文件，输入正确的配置。

应该就可以了，目前iflow最新的版本是v0.4，支持了deepseek V3.2。

我的工作流程：

tmux 新建一个会话

执行iflow

输入提示词：获取Alpha id：xxxxx的信息，分析无法通过提交的原因，在原有表达式的基础上进行优化，要求不能超过两个数据字段，运算符不能超过7个。优化的表达式不能少于7个。你可以直接回测并提交。在没有提交成功之前，不要询问我，你的工作就是安装要求进行优化回测，直到提交成功。

第二天登陆看看结果，偶尔会有好运。

不要观望，用起来，用中学吧。

---

## 讨论与评论 (11)

### 评论 #1 (作者: XC35224, 时间: 6个月前)

感谢老哥提供的教程，很早之前就想把mcp接入心流了

---

### 评论 #2 (作者: LG87838, 时间: 6个月前)

感谢分享，早起跟着帖子尝试了iflow，挺好用的。

在72变里最新的DeepSeek 3.2运行总是报错，更换其他的模型就没问题。现在也不用找人帮忙了，继续问AI解决，哈哈。

------------------------------------------------------------------------------------------------

慢慢来，相信时间的力量。

------------------------------------------------------------------------------------------------

---

### 评论 #3 (作者: XC35224, 时间: 6个月前)

尝试了很多次手动配置，但最后总是无法连接。最后发现了一个很简单的方法，授权iflow使用所有操作，让他自行安装cnhkmcp，并配置账号密码，测试通过后接入iflow。整个过程不需要额外的人为干预，可以完全交给它实现。

---

### 评论 #4 (作者: XG43628, 时间: 6个月前)

感谢大佬分享！最早在群里看有人分享了iflow，只是一直使用着gemini cli，贴子写的很详细，准备去参照使用下iflow，看看是iflow里面的模型更聪明还是gemini cli聪明！（geminicli最近总犯倔，应该还是提示词的问题！）

==================================================================================

知难上，戒骄狂，常自省，穷途明 ==================================================================================

---

### 评论 #5 (作者: LW67640, 时间: 6个月前)

> [XG43628](/hc/en-us/profiles/30816350962711-XG43628)
> - 6个月前

> 感谢大佬分享！最早在群里看有人分享了iflow，只是一直使用着gemini cli，贴子写的很详细，准备去参照使用下iflow，看看是iflow里面的模型更聪明还是gemini cli聪明！（geminicli最近总犯倔，应该还是提示词的问题！）

两个都在使用，还有antigravity，我觉得gemini-2.5-flash挺好的，因为这个给我出了一个模版。我的提示词都比较简单。这个观察应该不具备普适性。提示词和输入的知识应该是本质。

---

### 评论 #6 (作者: CZ78575, 时间: 6个月前)

感谢老哥分享，关于iflow会提示settings错误，无法启动，实测是json格式化问题（描述这里的字数过多，没有添加换行转义），可以随便找个json格式化工具（百度很多，找个网页在线工具即可）进行格式化，符合json标准即可，实测一次配置成功

---

### 评论 #7 (作者: AH18340, 时间: 6个月前)

感谢大佬分享，已经用起来了

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #8 (作者: ZY23886, 时间: 6个月前)

用起来 你说的 这里可能遇到问题，文件配置好以后，再次登陆iflow会提示settings错误，无法启动。我的解决方法： 1. 不做任何修改再次运行 iflow， 会恢复正常启动。 2. 现在再次修改settings文件，输入正确的配置。  给了我很大帮助 感谢大佬

---

### 评论 #9 (作者: JX14975, 时间: 6个月前)

感谢大佬分享，感觉gemini最近智商下降了不少，正准备换。

有一个问题，心流官网说推荐账号登录，据称账号登录是永续的，而API KEY只能维持一周，在这里采用API KEY登录是出于什么考虑呢？

---

### 评论 #10 (作者: YQ84572, 时间: 6个月前)

===================================================================================
好用的工具，这款ai助手很有效的帮助ai alpha的研究挖掘，感谢分享

===================================================================================

---

### 评论 #11 (作者: MZ45384, 时间: 6个月前)

大佬真的会探索新工具，最近感觉Gemini-cli变笨了，还容易放弃中断甚至草率地下错误结论，所以决定换上一个iflow试试。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

