# VSCode copilot配置MCP经验分享

- **链接**: VSCode copilot配置MCP经验分享.md
- **作者**: KZ79256
- **发布时间/热度**: 10个月前, 得票: 67

## 帖子正文

8月22日最新更新：forum已经集成在platfrom里了,platfrom可以就行VSCode copilot对于大学生可以免费使用, 所以在这里就把cnhkmcp的服务配置到里面1. 首先到github copilot申请学生认证, 这样就可以免费使用copilot了2. 下载并安装cnhkmcp安装cnhkmcp，cmd里直接输入pip install cnhkmcp3. 在左侧选择扩展, 浏览mcp,在此处安装一个官方的mcp服务, 之后找到配置的json, 或者直接新建一个C:\Users\XXX\AppData\Roaming\Code\User\mcp.json 文件(此处的XXX)是你的用户名,内部这样设置{"servers": {"worldquant-brain-platform": {"command": "python.exe","args": ["platform_functions.py"],"description": "WorldQuant BRAIN Platform MCP Server - Comprehensive trading platform integration with simulation management, alpha operations, and authentication. Credentials are stored in user_config.json in the same directory. Provides tools for creating simulations, checking status, managing alphas, and accessing platform features.",}},"inputs": []}command和args分别输入python和函数的地址4. 之后点击启动5.之后在对话框的右下角点击工具, 查看是否启动了mcp服务, 之后直接在对话框询问即可最后需要注意的是, 如果你是通过ssh连接到远端服务器时, 你的上述mcp配置应该仍在本机完成最后的最后感谢weijie老师说copilot也可以使用mcp, 之前一直没咋探索🤣

---

## 讨论与评论 (3)

### 评论 #1 (作者: ZZ31673, 时间: 7个月前)

您好请问一下，我这配置完右下角的工具没有出现，有什么方法解决吗

---

### 评论 #2 (作者: YQ84572, 时间: 6个月前)

好用好用，直接用上copilot配合mcp了====================================================================================================================

---

### 评论 #3 (作者: JF12271, 时间: 4个月前)

你好，没有找到启动按钮是为什么呢

---

