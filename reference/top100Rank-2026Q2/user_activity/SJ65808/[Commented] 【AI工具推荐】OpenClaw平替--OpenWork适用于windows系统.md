# 【AI工具推荐】OpenClaw平替--OpenWork，适用于windows系统。

- **链接**: [Commented] 【AI工具推荐】OpenClaw平替--OpenWork适用于windows系统.md
- **作者**: CG80910
- **发布时间/热度**: 3个月前, 得票: 9

## 帖子正文

# OpenWork 安装与配置教程

本教程将指导你完成 OpenWork 的安装、本地 MCP 配置和本地 Skill 配置。

可以实现一句话自动实现任务工作流。

## 目录

1. [环境要求](#%E7%8E%AF%E5%A2%83%E8%A6%81%E6%B1%82)
2. [安装 OpenWork](#%E5%AE%89%E8%A3%85-openwork)
3. [配置本地 MCP](#%E9%85%8D%E7%BD%AE%E6%9C%AC%E5%9C%B0-mcp)
4. [配置本地 Skill](#%E9%85%8D%E7%BD%AE%E6%9C%AC%E5%9C%B0-skill)
5. [验证配置](#%E9%AA%8C%E8%AF%81%E9%85%8D%E7%BD%AE)

## 环境要求

在开始之前，请确保你的系统满足以下要求：

- **操作系统** : Windows 10/11, macOS, 或 Linux
- **js** : 18.x 或更高版本
- **包管理器** : npm, yarn, 或 pnpm
- **可选** : Chrome 浏览器（用于 Chrome DevTools MCP）

## 安装 OpenWork

### 方法一：通过 npm 安装（推荐）

```
# 全局安装 OpenWork CLInpm install -g openwork# 验证安装openwork --version
```

### 方法二：通过 npx 运行

```
# 直接使用 npx 运行npx openwork
```

### 方法三：从源码安装

```
# 克隆仓库git clone https://github.com/openwork-ai/openwork.git# 进入目录cd openwork# 安装依赖npm install# 构建项目npm run build# 链接全局命令npm link
```

### 方法四：下载 Windows exe 安装（推荐 Windows 用户）

1. 访问 OpenWork 官方 releases 页面：

- GitHub:  [https://github.com/openwork-ai/openwork/releases](https://github.com/openwork-ai/openwork/releases)
- 或官方下载页面:  [https://opencode.ai/download](https://opencode.ai/download)

1. 下载最新版本的 Windows 安装包（.exe 或 .msi 文件）
2. 运行安装程序，按照提示完成安装
3. 验证安装（打开新的终端窗口）：

- openwork --version

双击桌面图标打开软件：

![图片](images/img_8e31aeb0ed.png)

**注意** ：Windows 安装程序会自动配置环境变量，安装完成后可以直接在命令行使用 openwork 命令。

## 配置本地 MCP

MCP（Model Context Protocol）是 OpenWork 的扩展机制，允许你集成各种工具和服务。

### 1. 创建配置文件

在项目根目录创建 opencode.jsonc 文件：

```
{  // JSON Schema 声明  "$schema": "https://opencode.ai/config.json",    // 默认使用的 Agent  "default_agent": "openwork",    // MCP 配置  "mcp": {    // Chrome DevTools MCP 示例    "chrome-devtools": {      "command": [        "npx",        "-y",        "chrome-devtools-mcp@latest"      ],      "type": "local"    },        // 自定义 MCP 服务器示例    "my-custom-mcp": {      "command": [        "node",        "/path/to/your/mcp-server.js"      ],      "type": "local"    }  },    // 默认使用的模型  "model": "opencode/big-pickle"}
```

### 2. 常用 MCP 列表

以下是一些常用的本地 MCP 工具：

MCP 名称

安装命令

用途

chrome-devtools

npx -y chrome-devtools-mcp@latest

控制 Chrome 浏览器

filesystem

npx -y @modelcontextprotocol/server-filesystem

文件系统操作

playwright

npx -y @modelcontextprotocol/server-playwright

浏览器自动化

### 3. 引用本地 pip 安装的 MCP

如果你已经通过 pip 安装了 Python 版本的 MCP 工具，可以直接引用本地安装的可执行文件。

#### 3.1 安装 Python MCP

```
# 使用 pip 安装 MCP（以 mcp-server-filesystem 为例）pip install mcp-server-filesystem# 或者安装其他常用 MCPpip install mcp-server-pythonpip install mcp-server-sqlite
```

#### 3.2 查找 pip 安装路径

```
# 查找可执行文件路径where mcp-server-filesystem      # Windows# 或which mcp-server-filesystem      # macOS/Linux# 查找 pip 安装的所有包路径pip show mcp-server-filesystem通常 pip 安装的 MCP 可执行文件位于： - Windows: C:\Users\<用户名>\AppData\Roaming\Python\Python<版本>\Scripts\ - macOS/Linux: ~/.local/bin/
```

#### 3.3 配置本地 pip MCP

在 opencode.jsonc 中配置引用本地 pip 安装的 MCP：

```
{  "mcp": {    // 引用本地 pip 安装的 filesystem MCP（Windows 示例）    "filesystem": {      "command": [        "C:\\Users\\<用户名>\\AppData\\Roaming\\Python\\Python312\\Scripts\\mcp-server-filesystem.exe"      ],      "args": [        "--allowed-directory",        "C:\\path\\to\\allowed\\directory"      ],      "type": "local"    },        // 引用本地 pip 安装的 Python MCP（macOS/Linux 示例）    "python-mcp": {      "command": [        "/Users/<用户名>/.local/bin/mcp-server-python"      ],      "type": "local"    },        // 引用本地 pip 安装的 SQLite MCP    "sqlite-mcp": {      "command": [        "C:\\Users\\<用户名>\\AppData\\Roaming\\Python\\Python312\\Scripts\\mcp-server-sqlite.exe"      ],      "args": [        "--db-path",        "C:\\path\\to\\database.db"      ],      "type": "local"    }  }}
```

#### 3.4 常用 Python MCP 列表

MCP 名称

pip 安装命令

用途

mcp-server-filesystem

pip install mcp-server-filesystem

文件系统操作

mcp-server-python

pip install mcp-server-python

Python 代码执行

mcp-server-sqlite

pip install mcp-server-sqlite

SQLite 数据库操作

mcp-server-github

pip install mcp-server-github

GitHub API 操作

**提示** ：如果你使用的是 uv（现代 Python 包管理器），可以将 pip 替换为 uv pip install，安装速度更快。

如果你的 MCP 需要环境变量，可以在配置文件中使用占位符：

```
{  "mcp": {    "my-mcp": {      "command": ["node", "server.js"],      "type": "local",      "env": {        "API_KEY": "${MY_API_KEY}"      }    }  }}
```

然后在 .env 文件中设置：

```
MY_API_KEY=your_api_key_here
```

## 配置本地 Skill

Skill 是可重用的任务模板，可以自动化重复性工作。

### 1. Skill 目录结构

在项目根目录创建 .opencode/skills 文件夹：

```
your-project/├── .opencode/│   ├── skills/│   │   ├── my-skill/│   │   │   ├── SKILL.md        # Skill 定义文件（必需）│   │   │   ├── .skill.config   # Skill 配置（可选）│   │   │   └── assets/         # 资源文件（可选）│   │   └── another-skill/│   │       └── SKILL.md│   ├── agents/                 # 自定义 Agent│   └── commands/              # 自定义命令└── opencode.jsonc
```

### 2. 创建 Skill 文件

**SKILL.md**  文件是 Skill 的核心，格式如下：

```
# Skill 名称## 描述简短描述这个 Skill 做什么## 使用场景- 场景 1- 场景 2## 步骤### 1. 第一步具体操作说明...### 2. 第二步具体操作说明...## 示例\`\`\`bash# 示例命令echo "Hello World"\`\`\`## 注意事项- 注意点 1- 注意点 2
```

### 3. Skill 配置（可选）

创建 .skill.config 文件来自定义 Skill 行为：

```
{  "name": "my-skill",  "version": "1.0.0",  "description": "My custom skill",  "trigger": ["关键词1", "关键词2"],  "env": {    "REQUIRED_VAR": "默认值"  }}
```

### 4. 使用内置 Skill

OpenWork 提供了多个内置 Skill，可以通过以下命令查看：

```
# 列出所有可用 Skillopenwork skill list# 安装内置 Skillopenwork skill install <skill-name># 创建新 Skillopenwork skill create
```

## 在 OpenWork 中使用 MCP 和 Skill

完成 MCP 和 Skill 的配置后，以下是详细的使用方法。

### 1. 使用 MCP 工具

#### 1.1 启动 OpenWork

```
# 进入你的项目目录cd your-project# 启动 OpenWork 交互式界面openwork# 或npx openwork# 指定项目路径启动openwork --path /path/to/your/project
```

#### 1.2 在对话中使用 MCP

启动 OpenWork 后，你可以直接在对话中调用 MCP 工具：

```
用户: 请帮我打开浏览器并访问 github.com# OpenWork 会自动调用 chrome-devtools MCP# 执行浏览器操作
```

#### 1.3 MCP 工具使用示例

MCP 名称

使用示例

说明

chrome-devtools

“打开 Chrome 浏览器访问百度”

浏览器自动化

filesystem

“读取当前目录下的 README.md”

文件操作

python-mcp

“运行 Python 脚本处理数据”

执行 Python 代码

sqlite-mcp

“查询 users 表的数据”

数据库操作

#### 1.4 查看可用 MCP 工具

在 OpenWork 对话中，你可以询问：

```
# 查看所有可用的 MCP 工具"列出所有可用的 MCP 工具"# 查看特定 MCP 的功能"chrome-devtools 可以做什么？"
```

### 2. 使用 Skill

#### 2.1 触发 Skill

有多种方式可以触发 Skill：

**方式一：对话中直接触发**

```
# 使用内置 Skill"帮我创建一个新的 OpenCode Skill"# 使用自定义 Skill"使用 my-skill 分析这个代码"
```

**方式二：使用 /skill**  **命令**

```
/skill list                    # 列出所有可用 Skill/skill use skill-name          # 使用指定 Skill/skill info skill-name         # 查看 Skill 详情
```

**方式三：配置文件触发**  在 .skill.config 中设置 trigger 关键词：

```
{  "name": "my-skill",  "trigger": ["分析代码", "code analysis"]}
```

当你在对话中提到这些关键词时，OpenWork 会自动建议使用对应的 Skill。

#### 2.2 Skill 工作流程

当 Skill 被触发后，OpenWork 会：

1. **加载 Skill**  **定义**  - 读取md 文件
2. **解析步骤**  - 理解 Skill 定义的各个步骤
3. **逐步执行**  - 按顺序执行每个步骤
4. **交互确认**  - 在关键步骤请求你的确认

示例：

```
用户: 创建一个新 SkillOpenWork:我会帮你创建一个新的 Skill。让我先检查一下当前的目录结构...步骤 1: 创建 Skill 目录结构- 创建 .opencode/skills/my-new-skill/ 目录- 创建 SKILL.md 文件步骤 2: 询问 Skill 详情请告诉我这个 Skill 的名称和用途：
```

#### 2.3 常用内置 Skill

OpenWork 提供以下常用内置 Skill：

Skill 名称

用途

触发方式

skill-creator

创建新的 Skill

“创建 Skill”

plugin-creator

创建插件

“创建插件”

command-creator

创建自定义命令

“创建命令”

agent-creator

创建自定义 Agent

“创建 Agent”

get-started

入门引导

“/get-started”

workspace-guide

工作区指南

“工作区指南”

### 3. MCP 与 Skill 结合使用

MCP 和 Skill 可以结合使用，实现更强大的功能：

#### 3.1 在 Skill 中调用 MCP

在 Skill 的步骤中，可以直接使用 MCP 工具：

```
# 示例 Skill：代码审查## 步骤### 1. 读取代码文件使用 filesystem MCP 读取指定目录下的代码文件### 2. 使用 AI 分析将代码发送给 AI 进行分析### 3. 生成报告使用 filesystem MCP 将审查结果写入报告文件
```

#### 3.2 完整使用示例

```
# 场景：自动化代码审查1. 启动 OpenWork$ openwork2. 调用 Skill用户: 请使用 code-review Skill 审查 ./src 目录下的代码3. Skill 执行流程- ✅ 使用 filesystem MCP 读取 ./src 目录- ✅ 使用 python-mcp 运行静态分析工具- ✅ 使用 filesystem MCP 生成审查报告4. 完成✅ 审查完成！报告已保存到 ./reports/code-review-2024.md
```

### 4. 调试 MCP 和 Skill

如果遇到问题，可以使用以下调试方法：

#### 4.1 检查 MCP 状态

```
# 列出所有 MCP 及其状态openwork mcp list# 测试特定 MCPopenwork mcp test <mcp-name># 查看 MCP 日志openwork mcp logs <mcp-name>
```

#### 4.2 检查 Skill 状态

```
# 列出所有可用 Skillopenwork skill list# 查看 Skill 详细信息openwork skill info <skill-name># 验证 Skill 配置openwork skill validate
```

#### 4.3 常见问题排查

问题

解决方法

MCP 工具不可用

检查配置文件语法，确认命令路径正确

Skill 未触发

检查 trigger 关键词或尝试手动调用

MCP 执行超时

增加 timeout 配置或检查网络

权限错误

检查文件/目录权限或 MCP 配置

## 验证配置

完成配置后，运行以下命令验证设置：

### 1. 检查配置文件

```
# 验证 opencode.jsonc 语法openwork config validate
```

### 2. 检查 MCP 连接

```
# 列出所有已配置的 MCPopenwork mcp list# 测试 MCP 连接openwork mcp test <mcp-name>
```

### 3. 检查 Skill

```
# 列出所有可用 Skillopenwork skill list# 查看 Skill 详情openwork skill info <skill-name>
```

## 常见问题

### Q1: MCP 连接失败怎么办？

1. 检查命令是否正确
2. 确认依赖已安装（运行 npm install）
3. 检查防火墙和网络设置

### Q2: Skill 不起作用？

1. 确认md 文件存在
2. 检查文件路径是否正确
3. 验证 YAML/JSON 语法

### Q3: 如何更新 OpenWork？

# 更新 CLI
npm update -g openwork

# 或重新安装
npm install -g openwork@latest

---

## 讨论与评论 (15)

### 评论 #1 (作者: BW14163, 时间: 3个月前)

感谢分享，又学到了一个新知识：OpenClaw平替--OpenWork，先收藏了，以后需要的时候再来回看拿，为你点赞

---

### 评论 #2 (作者: HZ99685, 时间: 3个月前)

小白想问一下，为什么不直接配置openclaw呢？

---

### 评论 #3 (作者: XY20037, 时间: 3个月前)

非常感谢大佬分享这么详细的 OpenWork 安装与配置教程！作为一直在用 AI 工具提升效率的顾问，一直在找稳定好用的 OpenClaw 平替，这篇教程简直太及时了。从环境准备、四种安装方式，到本地 MCP 配置、Python MCP 集成、Skill 制作，再到调试与排错，每一步都写得清晰易懂，Windows 用户也能直接上手。已经收藏准备马上部署，用来自动化日常回测、因子处理和工作流，效率肯定能大幅提升！再次感谢大佬的硬核干货！

---

### 评论 #4 (作者: FF45555, 时间: 3个月前)

感谢分享，问了下ai，给了open claw和openwork的对比，用以解答为什么要选择open work，大意是open work部署简单，可使用工作流。方便我们小白上手。

#### 选 OpenClaw 如果你：

- 需要 **深度系统操作** （如批量文件处理、代码部署、浏览器自动化、远程控制）
- 重视 **数据隐私** ，拒绝云端托管
- 有 **技术基础** ，愿意折腾配置与扩展
- 追求 **高度定制** ，想打造专属数字员工
- 希望 **跨平台** （Windows/macOS/Linux/ 嵌入式）统一自动化

#### 选 OpenWork 如果你：

- 想 **快速搭建自动化工作流** ，不想写代码
- 需要 **可视化、可调试、可共享** 的流程管理
- 是 **普通办公 / 知识工作者** ，追求易用性
- 希望 **团队复用标准化流程**
- 想要 **Claude Cowork 平替** ，免费且本地优先

### 一句话总结

- **OpenClaw = 全能数字员工** ：能深度操控电脑，适合技术玩家与重度自动化。
- **OpenWork = 可视化工作流工作台** ：易上手、流程透明，适合普通办公与团队协作。

---

### 评论 #5 (作者: TT21691, 时间: 3个月前)

openclaw相对来说功能最全，但是配置和使用上面也有很多问题，感谢大佬分享新的工具。

---

### 评论 #6 (作者: PL20130, 时间: 3个月前)

尝试好多次改环境变量始终调用的是Using model: claude-sonnet-4-5-20250929，该模型需要apiKey，启动openwork以后执行任务会出现如下报错：

Agent Error

Anthropic API key not configured

You can try sending a new message to continue the conversation.
无法使用免费的 "model": "opencode/big-pickle" ![图片](images/img_11365b6f02.png)  ![图片](images/img_e6062b2f83.png)

---

### 评论 #7 (作者: CG80910, 时间: 3个月前)

不直接配置openclaw的原因是我的主力机是dell工作站，win11系统，openclaw目前对windows系统支持不够友好，所以我找的平替，包括openclaw支持的其他能力，我也都找的平替实现

---

### 评论 #8 (作者: XW25488, 时间: 3个月前)

先收藏了，谢谢分享

---

### 评论 #9 (作者: XZ35933, 时间: 3个月前)

非常感谢！教程通俗易懂，简洁明了，节省了不少时间。

---

### 评论 #10 (作者: YX23650, 时间: 3个月前)

感谢大佬，让我这种小白也能轻松部署OpenWork，祝大佬永驻GM！

---

### 评论 #11 (作者: SJ65808, 时间: 3个月前)

收藏了，有空仔细研究一下

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #12 (作者: XW23690, 时间: 3个月前)

感谢分享，收藏了在慢慢研究。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #13 (作者: LH94963, 时间: 3个月前)

先收藏了，谢谢分享

============================================================================
=============================== 无限进步 ====================================
===========================================================================

---

### 评论 #14 (作者: MY49971, 时间: 3个月前)

新工具太多了，眼花缭乱

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #15 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的分享，我先研究一下openclow，再去研究这个                                                                 ================================自信人生两百年，会当水击三千里==========================

---

