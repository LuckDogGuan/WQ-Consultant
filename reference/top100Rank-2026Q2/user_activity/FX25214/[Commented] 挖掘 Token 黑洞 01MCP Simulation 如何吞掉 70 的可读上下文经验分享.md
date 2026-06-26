# 挖掘 Token 黑洞 01：MCP Simulation 如何吞掉 70%+ 的可读上下文经验分享

- **链接**: [Commented] 挖掘 Token 黑洞 01MCP Simulation 如何吞掉 70 的可读上下文经验分享.md
- **作者**: EL94401
- **发布时间/热度**: 1个月前, 得票: 10

## 帖子正文

## 先说背景：为什么我开始认真抠 token

我最近给自己定的节奏，是尽量每天围绕一个 pyramid 做 alpha 挖掘。

正好赶上模型平台活动，赠送了 2 亿 token。

乍一看很多。

但真实跑起来后，我发现每天消耗 4000 万 token 并不夸张。

字段探索、表达式生成、simulation、check、复盘、交接，只要 agent 连续工作几个小时，token 很快就会被吃掉。

这件事对 WQB 顾问尤其现实。

像我这种目前顾问级别还不高、value factor 不高、Osmosis 值也不高的阶段，payment 本来就偏低。

换句话说，alpha mining 的收入还不一定能 cover AI token 的消耗成本。

所以 token optimization 对我不是“工程洁癖”，而是很实际的生存问题。

如果每天挖一个 pyramid，却让大量 token 浪费在搬运重复 JSON、展开完整 simulation detail、反复读低价值上下文上，这套流程就很难长期跑下去。

## 这篇文章的依据

这篇不是纯理论推演。

它来自我自己近期 WQB alpha mining 实战里的真实 artifact 和复盘数据。

下面会先给真实 raw-to-summary 数据，再解释为什么多轮迭代后，这个问题会从“省 50% 左右”继续放大到“70%+ 的可读上下文差异”。

## 我挖到的第一个 Token 黑洞

我最近优化 WQB alpha mining workflow 时，发现一个很典型的 token 黑洞：

每次跑 simulation，MCP 会返回完整 alpha object。

里面有很多内容：

- expression
- settings
- metrics
- checks
- pyramid 信息
- pending 状态
- warning
- error

这些信息当然有价值。

但问题是：agent 每一轮决策并不需要完整对象。

它真正需要的，往往只是几行摘要：

`alpha_id
expression
sharpe / fitness / turnover
关键 checks
是否 match 目标 pyramid
下一步该继续、修复、还是淘汰
`

如果完整 response 每次都直接进入对话，agent 就会把大量 token 花在“阅读和搬运原始数据”上，而不是花在判断上。

【小结】

simulation 本身不是黑洞。

simulation 的 raw response 默认进入上下文，才是黑洞。

## 这个问题是怎么暴露的

最早不是从账单里发现的，而是从体感里发现的。

一轮 alpha mining 里，agent 经常会这样工作：

`写一批 expressions
调用 create_multi_simulation
MCP 返回 3-5 个完整 alpha objects
agent 阅读每个 alpha detail
总结哪些好、哪些坏、下一步怎么改
再跑下一批
`

这个流程看起来没问题。

但跑几轮后，上下文会膨胀得很快。

尤其是每个 batch 都返回多个完整对象时，重复内容会随迭代持续叠加。

比如 KOR/D1/FUNDAMENTAL 那轮复盘里，我记录到：

- 总共约 47 次 simulation。
- MCP multi_simulation 调用 8 次。
- MCP detail/check 调用 6 次。
- multi_simulation 一次会返回 3-5 个完整 alpha objects。
- 每个 alpha detail 约 100 行。
- 其中大量 settings、checks、investability 信息会重复出现。

也就是说，agent 在每个 batch 后都要读一堆很长的对象。

可是真正决定下一步的，通常只是少数几个字段。

## 为什么完整 response 会浪费 token

一个完整 alpha object 对平台是合理的。

但对 agent 决策来说，它太胖了。

完整 response 里通常有这些东西：

`alpha_id
regular expression
settings
is metrics
checks
check thresholds
check messages
pyramid match
pending correlation status
warnings
error details
`

这里不是说这些字段没用。

而是它们的使用频率不一样。

【高频决策字段】

`sharpe
fitness
turnover
关键 fail checks
是否 match pyramid
classification
`

【低频诊断字段】

`完整 check message
完整 settings
完整 raw response
异常 error body
`

如果不分层，所有字段都会默认进入上下文。

于是每一轮都在发生三件低价值事情：

1. agent 反复读取重复 settings。
2. agent 反复读取完整 checks，而不是只看关键 fail/pending。
3. agent 把 raw response 再人工压缩成 summary。

这其实是把数据工程问题交给语言模型处理了。

更合理的分工应该反过来：

`脚本负责搬运和压缩数据
agent 负责基于摘要做判断
`

## 我的改法：加一层 Simulation Summary

我的解决方案很直接：

在 MCP simulation 和 agent 上下文之间，加一层低 token summary。

新的结构是：

`MCP simulation
raw result 写入 artifact
summary projection 写入 artifact
agent 默认只读 summary
只有诊断单个 alpha 时才打开 raw
`

这个方案后来沉淀成了一个稳定入口：

`scripts/wqb_simulate_summary.py \
  --mode live \
  --input payloads.json \
  --run-id <run_id> \
  --concurrency 2 \
  --batch-size 4 \
  --agent
`

它做四件事：

- 完整平台结果写入本地 raw artifact。
- 压缩结果写入 simulation summary。
- 关键进度写入 progress log。
- agent 模式压低终端噪音，避免 tqdm、INFO、归档 print 继续进入对话。

重点不是“丢掉 raw 数据”。

raw 数据仍然保留。

只是它不再默认进入推理链路。

## Summary 里保留什么

我没有做简单文本截断。

我做的是结构化 projection。

每条结果只保留这些字段：

- expression_id：给本批表达式一个稳定编号。
- alpha_id：后续按需查 raw/detail/corr。
- expression：知道这条结果来自哪个表达式。
- sharpe / fitness / turnover / margin：核心表现。
- matches_pyramid：是否命中目标 pyramid。
- key_checks：只保留关键 checks。
- settings：保留必要 settings，方便比较。
- classification：快速判断结果状态。
- error：保存失败原因。

这样 agent 看到的是“决策行”，而不是完整 alpha object。

比如旧流程里，agent 可能要读一整段 detail，最后自己总结：

`这个 alpha Sharpe 还可以，但有 fail check，目前 corr pending，先不要提交。
`

新流程里，summary 直接给出可判断的信息：

`E017
alpha = qMnl92JV
sharpe = 1.59
fitness = 1.87
turnover = 0.247
classification = has_fail_checks
key_checks = IS_LADDER_SHARPE FAIL, PROD_CORRELATION PENDING
matches_pyramid = KOR/D1/FUNDAMENTAL
`

这条摘要不替 agent 做最终判断。

但它把判断所需的信息摆到了正确密度。

## 实测：单 batch 先省 50% 左右

我用了 artifact 体积做一个粗略验证。

这不是精确 token 计费统计。

但它对判断“进入阅读层的信息量是否下降”很有参考价值。

几组已经走 low-token wrapper 的 run，结果如下：

KOR/D1/FUNDAMENTAL dossier budgetpool：

raw 97,821 bytes，summary 50,045 bytes，约减少 49%。

USA/D1/SHORTINTEREST dossier budgetpool：

raw 219,729 bytes，summary 93,853 bytes，约减少 57%。

EUR/D0/OTHER batch2：

raw 25,218 bytes，summary 13,032 bytes，约减少 48%。

EUR/D0/OTHER batch3：

raw 25,072 bytes，summary 12,900 bytes，约减少 49%。

四组样本合在一起：

`raw artifact 总计：367,840 bytes
summary artifact 总计：169,830 bytes
进入阅读层的信息量减少：约 54%
`

所以，单看一次 raw-to-summary projection，节省不是凭感觉。

它来自真实 artifact 的体积对比。

## 为什么标题说 70%+

因为 alpha mining 不是只跑一次 simulation。

它经常是一批接一批地跑。

旧流程里，前面 batch 的 verbose detail 会留在对话上下文里。

后面每一轮推理，agent 都会继续背着它走。

新流程里，上一轮只留下 summary 和少量决策状态。

可以用一个很简单的模型估算：

`假设每个 batch 的 raw response 大小为 R
summary 大小约为 0.46R

旧流程：
历史 raw detail 留在上下文里
第 N 轮需要背着 1R + 2R + ... + NR

新流程：
每轮只读当前 summary 和少量状态
近似为 N * 0.46R
`

多轮迭代后，累计可读上下文节省大约是：

1 轮：约 54%。

2 轮：约 69%。

3 轮：约 77%。

4 轮：约 82%。

5 轮：约 85%。

所以标题里写“70%+”，指的不是单个 MCP response 被压缩 70%。

它指的是两轮以上 simulation 迭代后，避免 verbose raw detail 在上下文里重复滞留和反复被携带。

如果跑到 3-5 个 batch，这个累计差异会更明显。

## 优化前后，工作流变成什么样

旧流程：

`MCP 返回什么
agent 就读什么
agent 再总结什么重要
`

新流程：

`MCP 返回 raw
脚本保存 raw
脚本生成 summary
agent 只读 summary
需要诊断时再打开 raw
`

这带来三个直接变化。

第一，agent 的注意力更集中。

它不再反复读完整对象，而是直接比较核心指标和关键 checks。

第二，artifact 更可审计。

raw 和 summary 都落盘。

想复盘时，可以回到 raw。

日常决策时，只用 summary。

第三，交接更轻。

下一轮 agent 不需要重读完整 simulation detail。

只要先看 simulation summary 和 progress log，就能恢复大部分上下文。

## 我现在的规则

这次优化后，我给自己定了几条很简单的规则。

1. 同一批待跑表达式 >= 2 条时，默认走 simulation summary wrapper。
2. agent 驱动 live simulation 时，加 agent mode。
3. 默认只把 simulation summary 带入对话。
4. 只有需要诊断单个 alpha 时，才打开 raw result。
5. progress 写入 progress log，不要让长任务日志刷进 stdout。

这几条规则只解决一个问题：

不要让 MCP simulation raw response 默认吞掉上下文。

## 最后的结论

这次优化给我的最大提醒是：

token efficiency 不是让模型少思考，而是让模型少搬运。

MCP simulation 返回完整对象是合理的。

因为平台需要完整表达结果。

但 AI agent 的默认上下文，不应该承接所有 raw response。

更好的分工是：

`raw response 留给 artifact
summary 留给 agent
diagnosis 按需展开
`

如果你也在用 AI agent 跑工具链任务，可以检查一下：

是不是有某个工具每次都返回很大的 JSON，而 agent 每次其实只需要其中 5-10 个字段？

如果有，那很可能就是你的第一个 Token 黑洞。

后面有机会我会继续拆“挖掘 Token 黑洞”系列。

下一篇可以单独讲字段枚举、operator 文档、correlation polling 或长任务日志。

但这篇先只讲一个点：

MCP simulation raw response，要先进 artifact，再进 summary，最后才按需进入上下文。

## 下一步实验：渐进式披露

我接下来还想继续实验一个更完整的版本：

把这个流程做成“渐进式披露”。

第一层，只给 agent 看 compact summary。

第二层，按 alpha_id 展开关键 checks。

第三层，才打开完整 raw detail。

目标是让上下文像调试器一样按需展开，而不是每次把所有信息一次性倒进来。

等这套实验跑通、数据更稳定后，我会再单独写一篇，把设计和效果分享出来。

这篇先用我自己的真实 run 数据打一个样：

不要先争论抽象的“prompt 怎么省 token”。

先把实战里最胖、最重复、最容易滚雪球的工具返回找出来。

对我这套 WQB workflow 来说，第一个被挖出来的就是 MCP simulation raw response。

如果你也遇到过类似的上下文浪费，欢迎评论区聊聊：

你那个“最能吞 token 的工具返回”是什么？

## 数据来源与复盘依据

本文依据我近期几组真实 WQB alpha mining 工作流复盘整理：

- 2026-05-15：KOR/D1/FUNDAMENTAL pyramid lighting run，记录了 simulation 调用次数、detail/check 调用次数，以及 raw alpha detail 对上下文的消耗。
- 2026-05-16：KOR/D1/FUNDAMENTAL dossier budgetpool run，用 low-token simulation summary 对 raw result 做了压缩投影。
- 2026-05-16：USA/D1/SHORTINTEREST dossier budgetpool run，用同一套 summary workflow 验证大 batch 下 raw-to-summary 的压缩比例。
- 2026-05-14：EUR/D0/OTHER 两组 batch simulation，对比了不同 batch 里 raw artifact 与 summary artifact 的体积差异。
- 同期实现并使用了 low-token simulation summary wrapper：完整平台返回保留在本地 artifact，agent 默认只读取 compact summary。

---

## 讨论与评论 (8)

### 评论 #1 (作者: QL68122, 时间: 1个月前)

我是自建数据表存储每次回测内容，自己做了关键信息摘要。每天探索10来个数据集。工程一步步的搭建起来的，最近在搭建super alpha的工作流基建代码，流程探索

---

### 评论 #2 (作者: JR57542, 时间: 1个月前)

正好有需要！还挺有用的，本质是尽量降低信息熵，而且分析的确实很细致。爱了，已经全文复制喂给ai修复我的本地了，嘿嘿感谢楼主

---

### 评论 #3 (作者: WC64477, 时间: 1个月前)

长响应对于token的花费其实不是主要的，因为实际多轮对话的缓存命中率还是比较高，整体有90%的样子。主要的问题还是multiSim的响应被截断，模型无法获得完整的回测结果；其次，占据上下文空间，使得对话停止或很快就压缩。所以核心就是需要简化响应的回测结果。至于本地存储完整结果并不是必须的，单个alpha的详细结果完全可以mcp再查一次。而且存本地单个raw文件也无法比对分析，不如搞个本地数据库。

---

### 评论 #4 (作者: FX25214, 时间: 1个月前)

![图片](images/img_80461a385b.png) 一名合格的量化研究员，就是需要对整个因子挖掘的流程都有足够的熟悉。我们非常需要清晰且明确的知道在每一个节点上，人工智能需要什么，以及为什么在这个节点他需要这些内容。这就好比我们设置加权的奖励函数。这个奖励函数的输入对象和输出对象是什么。这些都非常值得重视。解决了这些问题。效率自然提升，成本也自然下降
--------------------------------------------来自传奇耐打王的点赞------------------------------

---

### 评论 #5 (作者: LJ12230, 时间: 1个月前)

感谢分享！日积月累，日进一步......................终至山顶。

---

### 评论 #6 (作者: FF65210, 时间: 1个月前)

感谢佬的分享，最近感觉ai跑的很慢，很可能就是你说的这个原因，我用的是cc接入科大讯飞的glm5.0模型，不知道怎么优化工作流让ai降低token消耗。

===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================

---

### 评论 #7 (作者: XW23690, 时间: 28天前)

赞。我也有这种问题，有时候无意义的消耗掉很多tokens

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #8 (作者: JX14975, 时间: 25天前)

非常实用的实战分享！raw → summary → diagnosis 三层渐进披露的思路非常清晰，把数据工程放回脚本、让 AI 专注决策，这才是 token 效率的正确打开方式。期待后续系列，加油！

---

