# 【工具分享】简单便捷地给大模型添加skills经验分享

- **链接**: [Commented] 【工具分享】简单便捷地给大模型添加skills经验分享.md
- **作者**: LX31898
- **发布时间/热度**: 4个月前, 得票: 13

## 帖子正文

平时总有顾问反应说自己用的AI大模型在执行任务、工作流的过程中经常出现前面把需求提完，后面执行过程ai关注的焦点逐渐偏离主线任务的情况。随着大模型的快速迭代，现在的大模型进化出了skill这个新事物来改善以上问题。

大模型、提示词、上下文的区别：

大模型的"Skill"（技能/能力）并非突然出现，而是随着模型规模扩大和训练数据增加 **逐步涌现** 的。2020年后，GPT-3等模型展现出上下文学习（In-Context Learning）能力，可视为早期skill形态；2022年ChatGPT通过RLHF训练显著提升了指令遵循等复合技能。

**三者区别** ：

- **提示词** ：用户输入的短期指令，单次有效，灵活但依赖技巧
- **上下文** ：对话中的临时信息，模型据此即时推理，窗口有限且易遗忘
- **Skill** ：模型内化的稳定能力（如代码生成、逻辑推理），无需重复提示即可调用，是参数中沉淀的"肌肉记忆"

简言之：提示词是 **外部指令** ，上下文是 **临时记忆** ，Skill是 **内部固化能力** ——前者决定"这次做什么"，后者决定"能做什么"。

首先，你需要浏览网上有些什么skill，打卡目前收录skill最多的聚合站： [Agent Skills Marketplace - Claude, Codex & ChatGPT Skills | SkillsMP](https://skillsmp.com/)

![图片](images/img_a481eb87a9.png)

之后在下面的搜索框里面输入你想寻找的关键词，例如我在这里搜的是worldquant：

![图片](images/img_25f4cd163a.png)

点击查询你会找到以上8个与之相关的skill，点开其中之一，例如brain-improve-alpha-performance，打开后页面如下，它提供了若干种部署方式：

![图片](images/img_f5761d8d77.png)

#### 以下以部署到roo-code和cli平台iflow为例，分别说明部署流程：

A. 部署到Roo-code：

#### 1. 准备工作

确保你已安装：

- **VS Code**  最新版本
- **Roo Code**  插件（从 VS Code 扩展市场安装）

#### 2. 获取 Skill 文件

由于该技能托管在 GitHub，你需要：

```
# 克隆技能仓库（假设技能在 GitHub 上）
git clone https://github.com/lori-kuo-world-quant/brain-improve-alpha-performance.git

# 或直接下载 SKILL.md 文件
curl -O https://raw.githubusercontent.com/lori-kuo-world-quant/brain-improve-alpha-performance/main/SKILL.md
```

#### 3. Roo Code 的 Skill 部署方式

Roo Code 支持两种技能部署方式：

**方式 A：手动创建项目级 Skill**

1. 在你的项目根目录创建技能文件夹：
   ```
   mkdir -p .roo/skills/brain-improve-alpha-performance
   ```
2. 将下载的  `SKILL.md`  文件复制到该目录：
   ```
   cp SKILL.md .roo/skills/brain-improve-alpha-performance/
   ```
3. 如果技能包含额外脚本或模板，一并复制到该目录
4. 验证部署：在 VS Code 中打开 Roo Code 面板，询问 "你有哪些可用技能？"，确认  `brain-improve-alpha-performance`  出现在列表中

**方式 B：使用 Skills 插件（推荐）**

1. 安装  **Skills**  VS Code 插件
2. 在插件界面搜索  `brain-improve-alpha-performance`
3. 点击安装，选择目标 Agent 为  **Roo Code**
4. 插件会自动将技能安装到  `.roo/skills/`  目录

#### 4. 使用 Skill

部署完成后，你可以直接对 Roo Code 说：

> "帮我优化这个量化策略的 Alpha 性能"

Roo Code 会自动识别上下文并调用  `brain-improve-alpha-performance`  技能，按照 SKILL.md 中定义的步骤执行：

- 分析当前 Alpha 因子表现
- 识别性能瓶颈
- 提供优化建议
- 生成改进后的策略代码

### B.在阿里云 iFlow CLI 中部署

#### 1. iFlow CLI 简介

iFlow CLI 是一款强大的终端 AI 助手，支持通过 MCP（Model Context Protocol）协议集成各种技能和服务。它允许你将 Claude Code 或自定义 Skill 转换为工作流（Workflow）使用。

#### 2. 安装 iFlow CLI

```
# macOS 一键安装
bash -c "$(curl -fsSL https://cloud.iflow.cn/iflow-cli/install.sh)"

# Windows / 其他系统
npm install -g @iflow-ai/iflow-cli
```

#### 3. 配置身份验证

编辑配置文件  `~/.iflow/settings.json` ：

```
{
  "theme": "Default",
  "selectedAuthType": "iflow",
  "apiKey": "your_iflow_api_key",
  "baseUrl": "https://apis.iflow.cn/v1",
  "modelName": "Qwen3-Coder"
}
```

从  [心流官网](https://iflow.cn/)  获取 API Key。

#### 4. 将 Skill 转换为 iFlow Workflow

参考 CSDN 上的教程，转换步骤如下：

**步骤 1：初始化项目**

```
# 进入你的项目目录
cd your-quant-project

# 启动 iFlow
iflow

# 初始化项目上下文
/init
```

**步骤 2：创建 iFlow 工作流目录结构**

```
mkdir -p .iflow/agents/brain-improve-alpha-performance
mkdir -p .iflow/commands
```

**步骤 3：迁移 Skill 内容**

1. 将  `brain-improve-alpha-performance`  的技能文件（除 SKILL.md 外）复制到：
   ```
   .iflow/agents/brain-improve-alpha-performance/
   ```
   将  `SKILL.md`  重命名为  `alpha.md`  并移动到：
2. ```
   .iflow/commands/alpha.md
   ```

编辑  `alpha.md` ，添加工作流头部配置：

```
---
name: brain-improve-alpha-performance
description: "World Quant Alpha performance optimization skill. Used for: (1) Analyzing alpha factor performance, (2) Identifying performance bottlenecks, (3) Optimizing quantitative strategies, (4) Generating improved alpha code"
license: Proprietary
workflow_trigger: /alpha
agent_path: .iflow/agents/brain-improve-alpha-performance
---

# 原有 SKILL.md 内容...
```

**步骤 4：验证工作流**

在 iFlow CLI 中输入：

```
/mcp
```

确认  `brain-improve-alpha-performance`  相关的工具已列出。

#### 5. 使用工作流

在 iFlow CLI 中直接调用：

```
# 触发工作流
/alpha

# 或输入自然语言指令
"分析我当前量化策略的 Alpha 性能并给出优化建议"
```

iFlow 会自动：

1. 加载  `.iflow/agents/brain-improve-alpha-performance/`  中的资源
2. 按照 SKILL.md 的指令执行分析
3. 调用相关工具（如需要可配置 MCP Server）
4. 输出优化后的策略代码和性能报告

### 四、进阶配置：结合阿里云 MCP Server

如果需要与阿里云服务（如云效、函数计算）集成，可以配置 MCP Server：

编辑  `~/.iflow/settings.json`  或项目内的  `.iflow/settings.json` ：

```
{
  "mcpServers": {
    "yunxiao": {
      "command": "npx",
      "args": ["-y", "alibabacloud-devops-mcp-server"],
      "env": {
        "YUNXIAO_ACCESS_TOKEN": "your_yunxiao_token"
      }
    },
    "function-compute": {
      "command": "npx",
      "args": ["@alicloud/fc-mcp-server"],
      "env": {
        "ALICLOUD_ACCESS_KEY": "your_access_key"
      }
    }
  }
}
```

这样  `brain-improve-alpha-performance`  技能就可以：

- 自动创建云效工作项跟踪优化任务
- 部署优化后的策略到阿里云函数计算
- 触发流水线进行回测验证

补充：

使用iflow平台的用户也可以：

先通过“wget skill.zip”直接下载含有skills全部内容的zip压缩包，在项目文件夹中找到/.iflow文件夹（全局模式需找到c:/user/{username}/.iflow），在里面新建名为skill的文件夹，然后将下载的zip压缩包文件解压后放进skill文件夹后，重启iflow平台即可。如果需要在iflow平台上查询插件是否安装，输入以下指令查询即可：

```
/skills
```

以上步骤完成后的界面显示如下：

![图片](images/img_66c7f56ea0.png)

---

## 讨论与评论 (6)

### 评论 #1 (作者: MG88592, 时间: 3个月前)

学会了，感谢大佬的分享，祝您新年快乐

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #2 (作者: XW23690, 时间: 3个月前)

感谢分享，好的skills能高效优化出好的alpha，用起来！

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #3 (作者: BW14163, 时间: 3个月前)

学到了，感谢分享：

1 了解到了三者区别：
提示词：用户输入的短期指令，单次有效，灵活但依赖技巧
上下文：对话中的临时信息，模型据此即时推理，窗口有限且易遗忘
Skill：模型内化的稳定能力（如代码生成、逻辑推理），无需重复提示即可调用，是参数中沉淀的"肌肉记忆"

2 学习了如何将skill部署到cli

3 学习了如何将skill部署到vs code

收藏了

---

### 评论 #4 (作者: XY20037, 时间: 3个月前)

这篇文章核心是讲清楚 AI 的 Skill，并给出部署方法：

1. 区分三个概念：提示词是单次外部指令，上下文是临时对话记忆，Skill 是模型固化的稳定能力。
2. 可以在 SkillsMP 平台搜索 WorldQuant 相关 Skill。
3. 提供两种部署方式：
   - Roo-code：在项目下创建.roo/skills 目录，放入 SKILL.md 文件使用。
   - iFlow CLI：初始化项目，将 Skill 转为工作流，配置 MCP 服务后调用。
4. 专门的 brain-improve-alpha-performance 技能可用于 Alpha 分析、瓶颈定位与代码优化。

---

### 评论 #5 (作者: MZ45384, 时间: 3个月前)

好全面的skill部署攻略，点赞了。顺便问一下大佬，skil和mcp实际用起来孰优孰劣？

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #6 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的skills配置分享，具体操作详细和详细                                                                                 ================================自信人生两百年，会当水击三千里==========================

---

