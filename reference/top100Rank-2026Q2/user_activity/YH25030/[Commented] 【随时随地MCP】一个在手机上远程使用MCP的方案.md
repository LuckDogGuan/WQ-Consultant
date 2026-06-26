# 【随时随地MCP】一个在手机上远程使用MCP的方案

- **链接**: [Commented] 【随时随地MCP】一个在手机上远程使用MCP的方案.md
- **作者**: FF56620
- **发布时间/热度**: 9个月前, 得票: 59

## 帖子正文

该方案使用针对  **claude code**  的跨平台开源项目  **happy**  实现，可直接参考其  [GitHub](https://github.com/slopus/happy) 。目前我是将其安装在一台海外的云服务器上运行，也可本地运行，下面的步骤主要是针对  **云服务器上运行的方案** （本机也可运行，省略部分步骤即可）。

其中  **仅云服务器**  的步骤，我会标注为“仅云服务器”。云服务器的安装以  **Debian 12**  为例，如果你使用其他系统，可直接发给 ChatGPT，让它给你翻译对应的命令。

另外，如果你决定选购一台云服务器，一定要选择  **海外的** ，避免访问论坛和模型接口时遇到网络问题。

## Step 1，安装 Node.js > 20（如已安装，跳过）

```
# 添加 NodeSource 官方源
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

也可使用nvm等方式安装，不重要，安装上就行

在自己电脑上建议使用nvm，方便管理，如下

```
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

验证安装成功与否

```
node -v # 20.x
npm -v # 10.x
```

## Step 2，安装 happy

```
npm install -g happy-coder # 如果问题，可sudo
```

## Step 3，安装 Python

此处不赘述了，大家应该都安装了，如有问题，直接问大模型

## `
`

## Step 4，安装 MCP及必要依赖

```
pip install cnhkmcp email-validator
```

**安装完成后，到对应目录配置上账号和密码**

## Step 5，安装浏览器内核（仅云服务器）

为了访问论坛，需要安装浏览器内核，如果在自己电脑上本来就有浏览器，则跳过

```
sudo apt install -y chromium \
libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
libxi6 libxtst6 libnss3 libxrandr2 libasound2 \
libatk1.0-0 libatk-bridge2.0-0 libpangocairo-1.0-0 libgtk-3-0
```

为了访问论坛，需要安装浏览器内核，如果在自己电脑上本来就有浏览器，则跳过

## Step 6，配置Claude Code密钥

```
export ANTHROPIC_API_KEY="你的APY KEY"
```

也可使用Kimi，kimi 可用赠送额度，但RPM 只有 3，可能还是需要充值50，才能比较流畅

```
export ANTHROPIC_BASE_URL="https://api.moonshot.cn/anthropic/"
export ANTHROPIC_API_KEY="你的APY KEY"
```

也可通过.claude/settings.json进行配置

```
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-你的APY KEY",
    "ANTHROPIC_BASE_URL": "https://api.moonshot.cn/anthropic/"
  },
  "permissions": {
    "allow": [],
    "deny": []
  }
}

```

关于claude code，官方价格比较贵，且国内封号严重，可以找一些claude code的分发站，我目前使用的一月20刀，每天提供60刀的额度，不过这种分发的站点都有随时跑路风险，就不推荐了，如果大家有使用类似服务，建议一月一续，降低风险

## Step 7，配置MCP

在项目根目录新建.mcp.json文件，填入具体配置，和其他地方配置的方式一样

```
{    "mcpServers": {        "worldquant-brain-platform": {            "command": "/root/project/.venv/bin/python",            "args": [                "/root/project/.venv/lib/python3.13/site-packages/cnhkmcp/untracked/platform_functions.py"            ],            "description": "WorldQuant BRAIN Platform MCP Server - Core tools for interacting with the BRAIN platform, including simulation, alpha management, and data access. Credentials are stored in user_config.json."        }    }}
```

## Step 8，安装APP并完成授权

进入文档，下载对应APP

[https://happy.engineering/docs/quick-start/](https://happy.engineering/docs/quick-start/)

```
happy --auth
```

在电脑或云服务运行以上命令，会生成二维码，扫码进行授权

## Step 9，启动

云服务器持久运行，可食用tmux，tmux 可以保证 SSH 断开后，进程依然运行。

```
# 安装 tmux
sudo apt install -y tmux

# 新建一个会话
tmux new -s happy

# 在 tmux 里运行 happy
happy

# 按下 Ctrl+b 然后 d 退出 tmux，会话会在后台继续运行
# 重新进入会话
tmux attach -t happy
```

如果不需要tmux，则直接使用happy命令启动

```
happy
```

启动后，在电脑端任意发送一条消息，切换到手机APP，就可以看到对应窗口，进行对话了

**温馨提示，claude code的系统提示词有点长，费用消耗比较快，大家多关注一下**

如有问题，欢迎在评论区交流

---

## 讨论与评论 (9)

### 评论 #1 (作者: ZH41150, 时间: 9个月前)

佬，太牛了，感谢佬的无私奉献

---

### 评论 #2 (作者: JB71859, 时间: 9个月前)

可以的，手机都可以这么玩了，看来我落伍了啊，明天我也整一下，玩玩看挺不错的，这个是真没想到
====================================================================================

---

### 评论 #3 (作者: WL58980, 时间: 2个月前)

太棒了！

Learning is endless!!!

=============================================================================

Study hard — quality over quantity, no room for mediocrity. Cherish every learning opportunity, stay focused, and learn from the experts. Keep pushing!

=============================================================================

---

### 评论 #4 (作者: YH25030, 时间: 9个月前)

谢谢分享。手机玩转MCP，对我来说又是一个全新的领域。虽然我的技术不强，看到您一步一步的解析，我想我也能站在巨人的肩膀上精进。😄

---

### 评论 #5 (作者: BW14163, 时间: 9个月前)

*******************************************************************************************************************
感谢大佬分享，很不错的方式，摆脱了电脑使用mcp的局限性，通过一部手机就能使用mcp全过程，非常有参考价值，通过开源工具链实现了MCP的移动端远程调用，重点解决了云服务器环境下的部署流程。

关注到大佬提到：“claude code的分发站，我目前使用的一月20刀，每天提供60刀的额度，不过这种分发的站点都有随时跑路风险，就不推荐了，如果大家有使用类似服务。” 很好奇具体从哪里找的，目前还在用国内的gpt。

祝大佬vf高高 ，base多多！！

********************************每天坚持学一个知识点，尽量不混信号，不过拟合**********************************

---

### 评论 #6 (作者: FF56620, 时间: 9个月前)

[BW14163](/hc/en-us/profiles/28900537669399-BW14163)  一些程序员聚集的论坛会有，毕竟程序员是对AI的需求最大的群体之一，不过要小心辨认，有一些可能会跑路，也可能出现模型掺假，这也是我没办法直接推荐的原因

************************************************************************************************************************************************************************************************************************************************************

---

### 评论 #7 (作者: CW63908, 时间: 9个月前)

大佬威武，感谢分享。

---

### 评论 #8 (作者: QP72475, 时间: 9个月前)

感谢，又学到了工作流。

---

### 评论 #9 (作者: SZ20589, 时间: 9个月前)

*******************************************************************************************************************
感谢大佬分享

这篇内容介绍了通过开源项目  **happy**  在云服务器上运行 Claude Code 的实践方案，思路清晰，步骤详尽，也兼顾了本地运行的情况，具有较强的参考价值。对于需要跨平台部署或尝试不同运行环境的人来说，这样的经验分享非常实用，值得借鉴。

祝大佬vf高高 ，base多多！！

*******************************************************************************************************************

一分耕耘，一分收获

*******************************************************************************************************************

---

