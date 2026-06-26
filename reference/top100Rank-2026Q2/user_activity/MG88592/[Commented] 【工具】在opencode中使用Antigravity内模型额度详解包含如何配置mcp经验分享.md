# 【工具】在opencode中使用Antigravity内模型额度详解（包含如何配置mcp）经验分享

- **链接**: [Commented] 【工具】在opencode中使用Antigravity内模型额度详解包含如何配置mcp经验分享.md
- **作者**: PZ64174
- **发布时间/热度**: 4个月前, 得票: 60

## 帖子正文

最近geminicli使用时总提示“We are currently experiencing high demand.We apologize and appreciate your patience./model to switch models.”。让我很苦恼，正好最近刷论坛看到OB佬之前推荐的"在OpenCode中使用Antigravity的Claude额度" ![图片](images/img_ff6f3ac4ca.png)

尝试安装后发现安装使用没有那么简单，在这详细描述一下安装使用过程，并且opencode在使用过程中与iflow cli、gemini cli有些许差别，我会把我遇到的问题与方案在后续描述中一一说清。

安装步骤：

1. 先安装opencode
  2. 找到~/.config/opencode/opencode.json，如果没有就创建一个，内容就写
  "plugin": [
      "opencode-antigravity-auth@latest"
    ],保存
  3. 打开终端 npm install -g opencode-antigravity-auth 运行
  4. 运行opencode auth login 选择Google 登录，登录走完流程会结束任务，这个时候重新输  入opencode auth login，选择Google 选第一个，然后选这个会刷新一下，然后选择已经登录的账号选择

![图片](images/img_e35d81b739.png)

![图片](images/img_c3c72c61ce.png)

![图片](images/img_a3606d8c90.png)    5. 到这里再打开终端 输入 opencode，/models 就能看到Claude Opus 4.6 Thinking (Antigravity)还有其他的模型了

### **关于mcp配置：**

这是geminicli的mcp配置：

![图片](images/img_4f89e4adb4.png)

这是opencode的mcp配置： ![图片](images/img_d372e25a0b.png)

代码如下：

```
"mcp": {    "worldquant-brain-platform": {      "type": "local",      "command": [        "F:\\python\\python.exe",        "F:\\python\\Lib\\site-packages\\cnhkmcp\\untracked\\platform_functions.py"      ],      "enabled": true,      "timeout": 600000    }  }
```

参照两张图片，把对应的配置复制就行。

关于我在使用时跟geminicli最大区别的地方，geminicli与iflow cli都有yolo模式，但是opencode没有直接的yolo模式，不过可以在opencode.json内进行配置

```
"permission": "allow"
```

这么写就是所有操作都通过，也可以直接在opencode的对话框中输入“ *开启 YOLO 模式。接下来的所有操作（包括 bash 命令执行、文件修改、环境配置）请直接自主运行，不要向我请求确认。直到任务完成或遇到不可恢复的系统错误为止。* ”

也可以在opencode.json中配置单个权限，详细大家可以查看opencode文档。 [权限 | OpenCode](https://opencode.ai/docs/zh-cn/permissions/)

---

## 讨论与评论 (6)

### 评论 #1 (作者: MG88592, 时间: 3个月前)

学会了，感谢大佬的分享，祝您新年快乐

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #2 (作者: XW23690, 时间: 3个月前)

讲的很详细，赞

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #3 (作者: BW14163, 时间: 3个月前)

最近geminicli使用时总提示“We are currently experiencing high demand.We apologize and appreciate your patience./model to switch models.”。之前还好，换个model继续跑。

然而，今天出问题了，所有model都报错。让我很苦恼，正好看到这篇帖子了，为你点赞，收藏，学习一下。

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

### 评论 #4 (作者: XY20037, 时间: 3个月前)

这篇 **OpenCode 对接 Antigravity 模型额度** 的教程太及时了！精准解决了 geminicli 高负载报错的痛点，还补充了 MCP 配置、YOLO 模式等关键细节，是能直接落地的实战指南。

### 核心价值 & 解决的痛点

1. **替代高负载的 geminicli** ：解决 "We are currently experiencing high demand" 报错问题，把 Antigravity 的 Claude 额度（如 Opus 4.6）无缝接入 OpenCode
2. **补齐关键配置细节** ：
   - 完整的插件安装 + Google 登录流程（含二次登录的坑）
   - 专属的 MCP 配置代码（适配 BRAIN 平台）
   - OpenCode 无原生 YOLO 模式的替代方案

### 关键步骤拆解（重点标注）

#### 1. 核心安装流程（避坑版）

bash

运行

```
# 1. 先装 OpenCode（已装可跳过）
npm install -g opencode-ai@latest

# 2. 安装 Antigravity 认证插件
npm install -g opencode-antigravity-auth@latest

# 3. 创建/编辑配置文件 ~/.config/opencode/opencode.json
{
  "plugin": ["opencode-antigravity-auth@latest"]
}

# 4. 登录（关键：需两次执行登录命令）
opencode auth login  # 第一次选Google，走完流程后退出
opencode auth login  # 第二次选Google，选已登录的账号

```

👉  **坑点提醒** ：第一次登录仅完成授权流程，需二次执行才能绑定账号，很多人会卡在这里。

#### 2. MCP 配置（对接 BRAIN 平台核心）

直接复制到  `opencode.json`  中，替换自己的 Python 路径即可：

json

```
{
  "mcp": {
    "worldquant-brain-platform": {
      "type": "local",
      "command": [
        "F:\\python\\python.exe",  // 替换为你的Python路径
        "F:\\python\\Lib\\site-packages\\cnhkmcp\\untracked\\platform_functions.py"  // 替换为MCP脚本路径
      ],
      "enabled": true,
      "timeout": 600000
    }
  }
}

```

#### 3. YOLO 模式配置（OpenCode 专属）

- 全局放行（推荐）：在  `opencode.json`  加  `"permission": "allow"`
- 临时开启：在对话框输入指令：
  plaintext
  ```
  开启 YOLO 模式。接下来的所有操作（包括 bash 命令执行、文件修改、环境配置）请直接自主运行，不要向我请求确认。直到任务完成或遇到不可恢复的系统错误为止。
  ```

👉 区别：geminicli/iflow cli 有原生 YOLO 指令，OpenCode 需手动配置 / 输入。

### 适配场景 & 补充建议

- 适合人群：被 geminicli 高负载报错困扰、想复用 Antigravity 额度的 Master/GM 顾问
- 小优化：
  1. 配置后重启 OpenCode 再执行  `/models` ，确保 Claude 模型列表加载完整
  2. 若登录失败，检查网络代理（需确保 Google 账号能正常登录）
  3. MCP 超时时间可根据自己的回测速度调整（600000 = 10 分钟，足够应对大部分场景）

### 总结

1. 核心是通过  `opencode-antigravity-auth`  插件，把 Antigravity 的 Claude 额度接入 OpenCode，替代高负载的 geminicli；
2. 安装关键是「两次登录」，MCP 配置需替换自己的 Python 路径，YOLO 模式需手动配置；
3. 完美解决了 geminicli 模型报错问题，同时保留 OpenCode 的全功能特性（如插件、Skills）。

这个方案是当前对接 Antigravity 额度最稳定的方式之一，尤其适合依赖 AI 写因子、做批量回测的顾问，实操性拉满！

---

### 评论 #5 (作者: SJ65808, 时间: 3个月前)

感谢分享，之前也碰到过这个问题

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #6 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的配置分享，操作十分详细                                                                                          ================================自信人生两百年，会当水击三千里==========================

---

