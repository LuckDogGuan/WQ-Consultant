# 【免费API】deepseekv4系列+AI编程神器9router经验分享

- **链接**: [Commented] 【免费API】deepseekv4系列AI编程神器9router经验分享.md
- **作者**: CL86067
- **发布时间/热度**: 1个月前, 得票: 6

## 帖子正文

## 先说一下9Router 是什么？

一句话： **把你电脑上的 AI 编程工具（Claude Code、Cursor、Codex、Cline 等）全部接到免费模型上**

**妥妥编程神器，而且还能省token，就目前的opencode不是可以免费用deepseekv4-flash吗，这里直接就能免费变成api用，我都用到workbuddy里面了，速度很快，里面nvdia的NLM也可以配置进去，偶尔用一下deepseekv4pro似乎也可以，功能很强大**

**官网： [https://9router.com/](https://9router.com/)**

**GitHub地址： [https://github.com/decolua/9router](https://github.com/decolua/9router)**

**![图片](images/img_8061adfb4c.png)**

安装就两条命令：

```
npm install -g 9router
9router
```

然后仪表板在  [http://localhost:20128](http://localhost:20128)  打开。

它的工作方式：

```
你的编程工具 (Claude Code / Cursor / Codex / Cline ...)
        │
        ▼ 指向 http://localhost:20128/v1
┌─────────────────────────────────────┐
│          9Router 路由网关            │
│  • 自动翻译格式 (OpenAI ↔ Claude)    │
│  • 配额追踪 & 自动刷新 Token         │
│  • RTK 压缩省 20-40% Token          │
└──────────┬──────────────────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  免费模型      付费模型(兜底)
(Kiro/OpenCode) (Claude Code/Codex)
```

**核心功能：三层自动回退**

1. **第一层** ：先用你已有的订阅（Claude Code Pro、Codex Plus 等）
2. **第二层** ：配额用完 → 自动切到廉价模型（GLM $0.6、MiniMax $0.2）
3. **第三层** ：预算超了 → 自动切到 **免费模型** 兜底

也就是说， **永远不会因为配额用完而中断工作** 。

## 免费模型有哪些？

9Router 内置了 40+ 提供商，免费层强烈推荐这几个：

提供商

可用模型

限制

**Kiro AI**

Claude Sonnet 4.5、Haiku 4.5、GLM-5、MiniMax、 **DeepSeek 3.2**

无限制免费，AWS/Google/GitHub 登录

**OpenCode Free**

自动获取模型列表

无需登录，即连即用

**Vertex AI**

Gemini 3 Pro、DeepSeek、GLM-5

新 GCP 账户 $300 免费额度

而且 9Router 支持  **Combo（智能组合）** ，可以创建多模型链路：

```
Combo: "free-forever"
  1. kr/claude-sonnet-4.5   (Claude 4.5 免费无限)
  2. kr/glm-5               (GLM-5 免费)
  3. oc/<auto>              (OpenCode Free, 无需认证)
  每月花费: $0
```

### 然后是一些免费用deepseekv4系列的地方：

### deepseekv4-flash:

- 首推opencode，这个大家用的也蛮多的应该，我用api都蛮好用的
- 另外就是trae里面，需要排队，但是凑合能用， 我主要用这个和glm5v那个，排队快一点然后用来优化alpha或者自动挖alpha还行，顺便提一下新出的trae solo里面排队相对少一点，glm5.1这里面用一下还可以，就是目前还没法用mcp，可以用来改代码修bug
- 还有腾讯的workbuddy或者codebuddy，这个里面就是需要积分，但是之前签到可以领不少积分，然后每个月送500，现在也有新的活动，还是可以用一下的
- atomcode的免费codeplan，直接就能领，就是只能这里面用，不过类似于opencode这种还行吧，附上地址： [https://ai.atomgit.com/serverless-api](https://ai.atomgit.com/serverless-api)

![图片](images/img_70902c2270.png) 直接api的话感觉9router里面的就可以了，大家可以再研究一下

### deepseekv4-pro:

- 腾讯的龙虾Qclaw可以免费用，就是可能需要排队了，trae里面也是排队要好久
- 比较推荐这个公益站agentrouter，最近看到可以用deepseekv4pro和flash了，GitHub登录，每天签到送25刀额度，用deepseek应该蛮耐用的，结合ccswitch直接可以用到打工人上面，附上链接： [https://agentrouter.org/register?aff=kAFr](https://agentrouter.org/register?aff=kAFr)

#### 暂时就这些了，有新发现的再补充到评论区，感觉重要的是怎么用好AI，用好了直接付费也行的，这些就作为体验吧

#### 祝大家都能用AI提高效率，vf和OS都节节高！

---

## 讨论与评论 (4)

### 评论 #1 (作者: BW14163, 时间: 1个月前)

兄弟，这波信息量太顶了！你简直是把2026年的AI编程“外挂”全掏出来了。
你说得非常到位，9Router 确实就是那个能把所有昂贵的 AI 编程工具（Claude Code、Cursor 等）和免费模型（DeepSeek、GLM、Kimi）打通的“万能转接头”。

这篇分享简直是开发者的“零元购”福音！9Router 通过三层自动回退策略解决配额焦虑。特别是整理的 DeepSeek V4 系列白嫖清单，OpenCode Free 即插即用，AgentRouter 还能领额度跑 Pro 模型，太实用了。RTK 压缩能省 20-40% Token 更是点睛之笔，今晚就照着配置，实现 AI 编程无限续杯！感谢大佬的避坑指南！

---

### 评论 #2 (作者: MM27120, 时间: 1个月前)

要钱的token还是不舍得买

---

### 评论 #3 (作者: FX25214, 时间: 1个月前)

想请教一下大佬都是怎么去选择和鉴别这些集成平台的？有很多平台虽然免费提供api但是使用效果实际上都大打折扣，颇有一番一分钱一分货的意味。大佬在使用这个集成平台时的实际体验如何，与直接付费购买是否能感受到一些实质性的区别呢？
-------------------------------------------------来自传奇耐打王的疑问-----------------------------

---

### 评论 #4 (作者: XW23690, 时间: 28天前)

感谢大佬分享

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

