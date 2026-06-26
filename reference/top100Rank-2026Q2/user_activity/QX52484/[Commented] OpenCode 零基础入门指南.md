# OpenCode 零基础入门指南

- **链接**: [Commented] OpenCode 零基础入门指南.md
- **作者**: JW52291
- **发布时间/热度**: 3个月前, 得票: 64

## 帖子正文

## 一、什么是 OpenCode？

**OpenCode**  是一款类似 Claude Code 的 AI 编程助手，让你通过自然语言对话就能完成代码编写、调试和项目管理。

### https://linux.do/t/topic/1693077#p-14512621-opencode-4 为什么要用 OpenCode？

功能
说明

  **智能编程** 

用中文描述需求，自动生成代码

  **代码调试** 

自动检测错误并提供修复建议

  **项目管理** 

自动分析项目结构，理解上下文

  **免费可用** 

支持免费模型，也有高性价比的中转 API

### https://linux.do/t/topic/1693077#p-14512621-h-5 术语速查表

术语
通俗解释

 **API** 
程序之间的"通信接口"，就像餐厅的菜单

 **API Key** 
你的"身份验证码"，用来证明你有权限使用服务

 **中转 API** 
第三方提供的服务，价格比官方便宜，速度更快

 **模型** 
AI 的"大脑"，不同模型能力不同

 **Node.js** 
运行 JavaScript 程序的环境

 **nvm** 
Node.js 版本管理工具

 **CLI** 
命令行界面，通过文字输入来操作电脑

## https://linux.do/t/topic/1693077#p-14512621-h-5-6 二、5 分钟快速开始

如果你只想快速体验，按下面步骤操作：

### https://linux.do/t/topic/1693077#p-14512621-h-1-nodejs-7 步骤 1：安装 Node.js

访问  [Node.js 官网](https://nodejs.org/) ，下载 LTS 版本（长期支持版），双击安装包一路点击"下一步"即可。

### https://linux.do/t/topic/1693077#p-14512621-h-2-opencode-8 步骤 2：安装 OpenCode

打开终端（Windows 按  `Win + R` ，输入  `cmd`  回车），执行：

```
npm install -g opencode-ai@latest

```

### https://linux.do/t/topic/1693077#p-14512621-h-3-9 步骤 3：验证安装

```
opencode --version

```

如果显示版本号（如  `1.2.3` ），说明安装成功！

### https://linux.do/t/topic/1693077#p-14512621-h-4-10 步骤 4：启动使用

```
opencode

```

首次启动会提示你选择模型，可以选择免费的  **GLM-4.7**  直接开始！

## https://linux.do/t/topic/1693077#p-14512621-h-11 三、环境准备

### https://linux.do/t/topic/1693077#p-14512621-h-12 系统要求

- **Windows** : Windows 10 或更高版本
- **macOS** : macOS 10.15 或更高版本
- **Linux** : 主流发行版均可

### https://linux.do/t/topic/1693077#p-14512621-nodejs-220-13 安装 Node.js（版本 >= 22.0）

#### https://linux.do/t/topic/1693077#p-14512621-a-14 方法 A：直接下载安装（推荐新手）

1. 访问官网： [https://nodejs.org/](https://nodejs.org/)
2. 下载带有  **LTS**  标签的版本（这是稳定版）
3. 双击安装包，一路点击"下一步"直到完成
4. 安装完成后重启终端

#### https://linux.do/t/topic/1693077#p-14512621-b-nvm-15 方法 B：使用 nvm 安装（适合需要管理多版本的进阶用户）

```
# 安装 nvm（Windows 用户需要先安装 nvm-windows）
# 安装指定版本的 Node.js
nvm install 22.22.0

# 使用这个版本
nvm use 22.22.0

# 验证安装
node --version

```

**nvm 是什么？**  nvm 是 Node Version Manager 的缩写，就像手机的应用商店，可以安装、切换不同版本的 Node.js。

## https://linux.do/t/topic/1693077#p-14512621-opencode-16 四、安装 OpenCode

### https://linux.do/t/topic/1693077#p-14512621-h-41-17 4.1 正式安装

在终端中执行：

```
npm install -g opencode-ai@latest

```

> **提示** ： `-g`  表示全局安装，安装后可以在任何地方使用  `opencode`  命令。

安装过程可能需要 1-3 分钟，取决于你的网络速度。

### https://linux.do/t/topic/1693077#p-14512621-h-42-18 4.2 验证安装

```
opencode --version

```

输出示例：

```
1.2.3

```

### https://linux.do/t/topic/1693077#p-14512621-h-43-opencode-19 4.3 启动 OpenCode

```
opencode

```

首次启动会显示模型选择界面，你可以选择：

选项
说明

 **GLM-4.7** 
免费使用，适合入门体验

 **Claude** 
需要 API Key，功能更强

 **其他** 
根据需求选择

## https://linux.do/t/topic/1693077#p-14512621-h-20 五、配置自定义模型

### https://linux.do/t/topic/1693077#p-14512621-h-51-21 5.1 为什么要配置自定义模型？

官方提供的免费模型虽然能用，但可能：

- 响应速度较慢
- 功能受限
- 有使用额度限制

通过配置 **中转 API** ，你可以：

- 获得更快的响应速度
- 使用更强大的模型（如 Claude、GPT-4）
- 成本更低（比官方便宜 50-80%）

### https://linux.do/t/topic/1693077#p-14512621-h-52-5-22 5.2 方案一：快速配置（推荐新手，5 分钟搞定）

#### https://linux.do/t/topic/1693077#p-14512621-h-1-23 第 1 步：登录认证

在 OpenCode 中执行：

```
/connect

```

然后按提示操作：

1. 选择  **Anthropic**
2. 选择  **Manually enter API Key**
3. 输入你的 API Key（格式： `sk-xxxxxx` ）

**API Key 从哪来？**

- 公益站：注册后在控制台获取
- 中转站：购买后获得
- 本地代理：自行搭建后生成

#### https://linux.do/t/topic/1693077#p-14512621-h-2-24 第 2 步：修改配置文件

找到配置文件：

- **Windows** :  `%APPDATA%\opencode\opencode.json`
- **macOS/Linux** :  `~/.config/opencode/opencode.json`

> **如何快速打开？**
> Windows 用户按  `Win + R` ，输入  `%APPDATA%\opencode` ，回车即可打开文件夹。

在  `provider`  字段中添加：

```
{
  "provider": {
    "anthropic": {
      "options": {
        "baseURL": "https://你的API地址/v1"
      }
    }
  }
}

```

**重要提示** ：

- 大部分中转站需要在 URL 后面加  `/v1`
- 示例地址格式： `https://example.com/v1`

#### https://linux.do/t/topic/1693077#p-14512621-h-3-25 第 3 步：选择模型

在配置文件中设置默认模型：

```
{
  "model": "anthropic/claude-sonnet-4"
}

```

不同中转站的模型名称可能不同，请咨询你的 API 提供商。

#### https://linux.do/t/topic/1693077#p-14512621-h-4-26 第 4 步：验证配置

重启 OpenCode，随便问个问题测试：

```
opencode

```

输入： `你好，请介绍一下自己`

如果能正常回复，说明配置成功！

### https://linux.do/t/topic/1693077#p-14512621-h-53-27 5.3 方案二：自定义供应商（推荐进阶用户）

如果你需要同时使用多个 API 渠道，可以配置自定义供应商。

#### https://linux.do/t/topic/1693077#p-14512621-h-1-28 第 1 步：添加自定义供应商

```
opencode auth login

```

选择：

1. **Other**
2. 输入供应商 ID（如  `my-router` ，全小写英文）
3. 输入 API Key

#### https://linux.do/t/topic/1693077#p-14512621-h-2-29 第 2 步：完整配置

编辑  `opencode.json` ：

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "my-router": {
      "npm": "@ai-sdk/anthropic",
      "options": {
        "baseURL": "https://api.example.com/v1",
        "apiKey": "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
      },
      "models": {
        "claude-sonnet": {
          "name": "claude-sonnet",
          "limit": {
            "context": 200000,
            "output": 64000
          }
        }
      }
    }
  }
}

```

**参数说明** ：

- `baseURL` : API 服务地址
- `apiKey` : 你的 API Key（请替换为真实的）
- `models` : 可用的模型列表
- `context` : 上下文长度（越大能处理越长的对话）
- `output` : 最大输出长度

#### https://linux.do/t/topic/1693077#p-14512621-h-3-30 第 3 步：连接使用

```
# 启动 OpenCode
opencode

# 执行连接命令
/connect

# 选择你创建的供应商
my-router

```

### https://linux.do/t/topic/1693077#p-14512621-h-54-31 5.4 方案三：本地代理（推荐高级用户）

如果你需要统一管理多个 API 渠道，或者需要调试流量，可以搭建本地代理。

#### https://linux.do/t/topic/1693077#p-14512621-cliproxyapi-32 安装 CLIProxyAPI

```
# 克隆项目
git clone https://github.com/router-for-me/CLIProxyAPI
cd CLIProxyAPI

# 安装依赖
npm install

# 启动服务
npm start

```

服务启动后会监听  `8317`  端口。

#### https://linux.do/t/topic/1693077#p-14512621-opencode-33 配置 OpenCode 使用本地代理

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "local-proxy": {
      "npm": "@ai-sdk/anthropic",
      "options": {
        "apiKey": "local-proxy-key",
        "baseURL": "http://127.0.0.1:8317/v1"
      }
    }
  },
  "model": "local-proxy/claude-sonnet"
}

```

## https://linux.do/t/topic/1693077#p-14512621-h-34 六、安装增强插件

### https://linux.do/t/topic/1693077#p-14512621-h-61-oh-my-opencode-35 6.1 什么是 Oh My OpenCode？

**Oh My OpenCode**  是 OpenCode 的增强插件，类似于手机的主题商店，安装后可以：

- **多 AI 协作** ：同时调用多个 AI 模型
- **专业智能体** ：内置前端工程师、架构师等专业角色
- **提示词优化** ：自动优化你的指令
- **并行任务** ：同时执行多个任务

### https://linux.do/t/topic/1693077#p-14512621-h-62-36 6.2 安装插件

```
npm install -g oh-my-opencode

```

### https://linux.do/t/topic/1693077#p-14512621-h-63-37 6.3 配置插件

在  `opencode.json`  中添加：

```
{
  "plugin": [
    "oh-my-opencode"
  ]
}

```

### https://linux.do/t/topic/1693077#p-14512621-h-64-38 6.4 验证安装

启动 OpenCode，执行：

```
/help

```

如果看到新增的命令列表，说明插件安装成功！

### https://linux.do/t/topic/1693077#p-14512621-h-65-skills-39 6.5 使用 Skills

安装插件后，你可以使用各种 Skill 来增强 OpenCode 的能力：

```
# 查看可用的 skills
/skills

# 使用特定 skill
/skill writing-plans

```

## https://linux.do/t/topic/1693077#p-14512621-skills-40 七、Skills 技能详解

### https://linux.do/t/topic/1693077#p-14512621-h-71-skills-41 7.1 什么是 Skills？

**Skills**  是 OpenCode 的"技能卡"，就像游戏里的技能书一样，装上之后 OpenCode 就能拥有特定的专业能力。

举个例子：

- 装了  `frontend-ui-ux`  skill，OpenCode 就能帮你设计精美的界面
- 装了  `backend-design`  skill，OpenCode 就能帮你设计数据库结构
- 装了  `writing-plans`  skill，OpenCode 就能帮你制定详细的项目计划

### https://linux.do/t/topic/1693077#p-14512621-h-72-skills-42 7.2 Skills 的三种安装方式

#### https://linux.do/t/topic/1693077#p-14512621-h-43 方式一：全局安装（推荐新手）

全局安装的 skill 可以在任何项目中使用，就像手机的全局设置一样。

**安装路径** ：

- **Windows** :  `C:\Users\你的用户名\.config\opencode\skills\`
- **macOS/Linux** :  `~/.config/opencode/skills/`

**目录结构示例** ：

```
~/.config/opencode/skills/
├── frontend-ui-ux/           # 前端 UI/UX 设计技能
│   └── SKILL.md
├── backend-design/           # 后端设计技能
│   └── SKILL.md
├── code-refactoring/         # 代码重构技能
│   └── SKILL.md
└── writing-plans/            # 编写计划技能
    └── SKILL.md

```

**安装步骤** ：

1. 打开 skills 目录（如果不存在就新建）
2. 创建 skill 文件夹（如  `my-skill` ）
3. 在文件夹内创建  `SKILL.md`  文件
4. 重启 OpenCode 即可生效

#### https://linux.do/t/topic/1693077#p-14512621-h-44 方式二：项目级安装

只在特定项目中生效，就像项目的专属配置。

**安装路径** ：在你的项目根目录下

```
你的项目/
├── src/
├── package.json
└── .opencode/
    └── skills/
        ├── frontend-coding-standards/
        │   └── SKILL.md
        └── project-specific/
            └── SKILL.md

```

**特点** ：

- 优先级高于全局 skill（同名 skill 会覆盖全局的）
- 可以随项目一起提交到 Git
- 团队成员共享相同的 skill 配置

#### https://linux.do/t/topic/1693077#p-14512621-h-45 方式三：多编辑器同步（推荐团队使用）

如果你同时使用 Cursor、Claude Code、OpenCode 等多个 AI 编辑器，可以通过软链接让 skill 配置在所有编辑器中同步。

**思路** ：建立一个统一的 skill 仓库，然后让各个编辑器都链接到这个仓库。

**操作步骤** （Windows 示例）：

1. 在  `~/.claude/skills`  目录下存放所有 skill
2. 创建符号链接让其他编辑器共享：

```
# 让 Cursor 共享 Claude 的 skills
New-Item -ItemType Junction -Path "$HOME\.cursor\rules\skills" -Target "$HOME\.claude\skills"

# 让 OpenCode 共享 Claude 的 skills
New-Item -ItemType Junction -Path "$HOME\.config\opencode\skills" -Target "$HOME\.claude\skills"

```

**优势** ：

- 一处更新，处处生效
- 避免重复配置
- 团队统一规范

### https://linux.do/t/topic/1693077#p-14512621-h-73-skills-46 7.3 如何获取 Skills？

#### https://linux.do/t/topic/1693077#p-14512621-skills-47 官方/社区 Skills

可以在以下地方寻找现成的 skill：

- GitHub 搜索： `opencode skill`  或  `claude skill`
- OpenCode 官方文档
- 技术社区分享

#### https://linux.do/t/topic/1693077#p-14512621-skills-48 自己编写 Skills

如果你想创建自己的 skill，只需要：

1. 创建一个文件夹（如  `my-awesome-skill` ）
2. 在里面创建  `SKILL.md`  文件
3. 按照规范编写 skill 内容

**SKILL.md 基本结构** ：

```
# Skill 名称

## 描述
这个 skill 用来做什么...

## 使用场景
- 场景1：...
- 场景2：...

## 指令模板
当用户要求 XXX 时，你应该...

## 示例
输入：...
输出：...

```

### https://linux.do/t/topic/1693077#p-14512621-h-74-skills-49 7.4 常用 Skills 推荐

Skill 名称
用途
适用场景

 **frontend-ui-ux** 
前端 UI/UX 设计
设计页面、优化用户体验

 **backend-design** 
后端架构设计
设计 API、数据库结构

 **writing-plans** 
编写实现计划
制定项目开发计划

 **code-refactoring** 
代码重构
优化现有代码结构

 **test-driven-development** 
测试驱动开发
编写测试用例

### https://linux.do/t/topic/1693077#p-14512621-h-75-skills-50 7.5 验证 Skills 是否生效

1. 重启 OpenCode
2. 执行  `/skills`  查看已加载的 skills 列表
3. 尝试使用 skill 的功能，看是否符合预期

## https://linux.do/t/topic/1693077#p-14512621-faq-51 八、常见问题 FAQ

### https://linux.do/t/topic/1693077#p-14512621-q1-unable-to-connect-52 Q1: 提示 “Unable to connect”

**原因** ：网络连接问题，可能是代理或防火墙导致。

**解决方法** ：

如果你使用了代理软件（如 Clash、V2Ray），需要在终端中设置代理：

```
# Windows PowerShell
$env:HTTPS_PROXY="http://127.0.0.1:7890"
$env:HTTP_PROXY="http://127.0.0.1:7890"

# 或者直接在启动时指定
opencode --proxy http://127.0.0.1:7890

```

### https://linux.do/t/topic/1693077#p-14512621-q2-opencodejson-53 Q2: 找不到 opencode.json 配置文件

**原因** ：首次使用，配置文件尚未创建。

**解决方法** ：

手动创建配置文件：

1. 打开文件夹： `C:\Users\你的用户名\.config\opencode\` （Windows）
2. 如果不存在，新建  `.config`  和  `opencode`  文件夹
3. 新建文件  `opencode.json`
4. 粘贴基础配置：

```
{
  "$schema": "https://opencode.ai/config.json"
}

```

### https://linux.do/t/topic/1693077#p-14512621-q3-54 Q3: 如何切换模型？

在 OpenCode 中执行：

```
/models

```

然后按提示选择你想使用的模型。

### https://linux.do/t/topic/1693077#p-14512621-q4-55 Q4: 安装时出现权限错误

**原因** ：没有管理员权限。

**解决方法** ：

```
# Windows：以管理员身份运行 PowerShell
# 右键点击 PowerShell → 以管理员身份运行

# macOS/Linux：使用 sudo
sudo npm install -g opencode-ai@latest

```

### https://linux.do/t/topic/1693077#p-14512621-q5-opencode-56 Q5: 如何卸载 OpenCode？

```
npm uninstall -g opencode-ai

```

### https://linux.do/t/topic/1693077#p-14512621-q6-57 Q6: 如何查看已安装的版本？

```
npm list -g opencode-ai

```

## https://linux.do/t/topic/1693077#p-14512621-h-58 八、参考资源

### https://linux.do/t/topic/1693077#p-14512621-h-59 官方文档

资源
链接

英文官网
 [https://opencode.ai/](https://opencode.ai/) 

中文文档
 [OpenCode 使用指南 (非官方)](https://opencodeguide.com/zh/docs) 

GitHub 仓库
 [GitHub - anomalyco/opencode: The open source coding agent. · GitHub](https://github.com/anomalyco/opencode)

### https://linux.do/t/topic/1693077#p-14512621-h-60 插件资源

资源
链接

Oh My OpenCode
 [GitHub - code-yeongyu/oh-my-opencode: the best agent harness · GitHub](https://github.com/code-yeongyu/oh-my-opencode)

### https://linux.do/t/topic/1693077#p-14512621-h-61 学习资源

资源
说明

Node.js 官方
 [https://nodejs.org/](https://nodejs.org/) 

npm 文档
 [https://docs.npmjs.com/](https://docs.npmjs.com/)

### https://linux.do/t/topic/1693077#p-14512621-h-62 站内资源

资源
说明

 [OpenCode 自定义服务商（中转站）接入指南](https://linux.do/t/topic/1329050) 
 [OpenCode 自定义服务商（中转站）接入指南](https://linux.do/t/topic/1329050)

## https://linux.do/t/topic/1693077#p-14512621-h-63 下一步？

恭喜你完成 OpenCode 的安装配置！

现在你可以：

1. **开始第一个项目** ：在任意文件夹执行  `opencode` ，让 AI 帮你写代码
2. **学习更多命令** ：执行  `/help`  查看所有可用命令
3. **配置 Skills** ：安装更多技能，扩展 OpenCode 的能力
4. **加入社区** ：在 GitHub 上参与讨论，分享使用心得

---

## 讨论与评论 (8)

### 评论 #1 (作者: BW14163, 时间: 3个月前)

感谢分享，为你点赞，最近论坛里面分享的这类的技术贴有一些了，希望能分享下，具体关于应用的是实战贴，如果配上图文就更好了

---

### 评论 #2 (作者: XW23690, 时间: 3个月前)

感谢分享，里面免费的模型用起来效果还不错

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #3 (作者: XY20037, 时间: 3个月前)

这份 **OpenCode 零基础入门指南** 非常保姆级，从安装、配置到进阶用法全覆盖，对咱们 BRAIN 顾问用来 **批量写因子、自动化回测分析** 特别实用。

### 核心亮点总结

1. **入门门槛极低**
   - 只需要装 Node.js，一行 npm 命令就能安装
   - 内置免费 GLM-4.7 模型，不用 API Key 就能上手
2. **适配 BRAIN 场景的关键用途**
   - 自然语言描述直接生成 alpha 表达式、批量模板
   - 自动调试回测代码、优化算子
   - 搭配插件可做自动化数据分析、脚本编写
3. **进阶配置很实用**
   - 支持中转 API，搭配 Claude 等强模型效率更高
   - Oh My OpenCode 插件实现多 AI 协作、专业角色
   - Skills 机制可以定制专属 **量化因子编写规则**
4. **FAQ 覆盖了大部分新人坑点**
   - 代理设置、配置文件找不到、权限问题都有解决方案

整体是 **工具落地性很强** 的技术帖，非常适合想提升因子研发效率的顾问，期待楼主后续更新结合 BRAIN 实战的使用教程！

---

### 评论 #4 (作者: YQ51506, 时间: 3个月前)

感谢分享、opencode+ai完整实现思路；祝楼主GM！

===========================================================================
=============================== 无限优化 ====================================
===========================================================================

---

### 评论 #5 (作者: QX52484, 时间: 3个月前)

======================================================================
很详细 感谢大佬分享
======================================================================
sharpe is ts_delta and ts_delta but returns ts_delay and ts_delay.

---

### 评论 #6 (作者: MY49971, 时间: 3个月前)

感谢分享，最近出了很多AI编程工具，有点眼花缭乱

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #7 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的关于opencode的零基础指南，对我这个小白真的很友好                                    ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #8 (作者: JX14975, 时间: 1个月前)

非常感谢 JW52291 如此详尽的 OpenCode 零基础入门指南！这篇教程对我帮助极大：从 Node.js 安装、npm 一键部署到自定义模型配置，每一步都配有清晰的代码示例和路径说明，让我这种没有 CLI 经验的新手也能在 5 分钟内跑起来。FAQ 部分对代理设置和配置文件找不到等常见坑的排查也特别贴心。再次感谢你花时间整理这份保姆级教程，期待后续结合 因子实战的进阶分享！

---

