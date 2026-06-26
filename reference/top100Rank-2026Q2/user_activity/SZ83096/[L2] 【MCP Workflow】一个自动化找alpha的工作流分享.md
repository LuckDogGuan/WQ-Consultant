# 【MCP Workflow】一个自动化找alpha的工作流分享

- **链接**: [L2] 【MCP Workflow】一个自动化找alpha的工作流分享.md
- **作者**: FF56620
- **发布时间/热度**: 9 months ago, 得票: 99

## 帖子正文

先看一下效果，目前跑的效果不错，我使用codex和claude code跑，都可以获得不错的效果，简单贴一张效果图可结合之前的帖子https://support.worldquantbrain.com/hc/en-us/community/posts/34208186164631-%E6%9D%A5%E8%87%AAMCP%E7%9A%84operator%E6%8C%87%E5%8C%97-%E7%BB%88%E4%BA%8E%E7%9C%8B%E6%87%82%E4%BA%86%E5%A4%A7%E5%A4%9A%E6%95%B0%E7%9A%84%E5%B9%B3%E5%8F%B0operator一并喂给AI，可减少由于操作符引起的错误工作流程如下：# Alpha 开发工作流（D1 版）## 🎯 目标与范围（顾问标准）- 目标：在 D1 设置下，系统化发现 Sharpe 与 Fitness 达标、可提交生产的 Alpha。- 成功标准（顾问提交门槛）：- Sharpe > 1.58；Fitness > 1.0。- Turnover 在 1%–70%；单票最大权重 <10%。- 需通过 Sub-Universe、自相关（Self-corr）与全平台相关（Prod-corr）测试；IS-Ladder（D1）阈值：Fail=1.59；2–5年≥2.38；6年≥2.22；7年≥2.06；8年≥1.90；9年≥1.74；10年≥1.59。## 📦 标准参数获取（MCP）- 使用 `get_platform_setting_options` 查询可用组合（instrument_type/region/delay/universe/neutralization），据此设置回测参数。- USA：以 D1 为默认；选择液体类 universe（如 TOP 系列）。- ASI：仅支持 D1；`universe=MINVOL1M/ILLIQUID_MINVOL1M`；`max_trade=ON` 必须开启。- 通用：`language=FASTEXPR`、`pasteurization=ON`；其余按平台建议。## ✅ Step 0 预检清单- 认证：完成平台登录（401 需重新认证）。- 数据：确认目标数据集可访问；统计字段 coverage、userCount、类型（MATRIX/VECTOR/GROUP）。- 参数：使用 `get_platform_setting_options` 自检参数组合合法性，避免 400。- 表达式：字段存在性、类型匹配（VECTOR 需 `vec_sum/vec_avg` 聚合）、语法检查。- 时间窗口规范：`ts_*` 仅允许 {5, 22, 66, 126, 255}（周、月、季、半年、年），不使用其他窗口。## 🔍 Phase 1 数据集分析（字段优选）- 选择标准：- coverage ≥ 0.4 优先；- userCount 适中（避开极高拥挤与极低稀缺）；- 类型以 MATRIX 为主，VECTOR 先聚合再用，GROUP 用于分组/中性化。- 分层：A+（高优先）、B（次优先）、C（探索）。## 🚀 Phase 2 初次批量验证（8个/批）- 强约束：仅使用加、减、乘、除四则运算两两组合；每个表达式恰好两个字段；同批尽量不重复字段对；字段限 MATRIX；延迟一致（D1）。- 缺失与异常的最小化处理：- 允许 `ts_backfill(x, d, k=1, ignore="NAN")`，d ∈ {5, 22, 66, 126, 255}；- 允许 `add/subtract/multiply` 的 `filter=true`；- 允许在最外层一次 `pasteurize(expr)`。- 规模与门槛（初次抽样）：- 先生成并测试约 100 个两两组合（8/批，共约 13 批）。- 目标：累计找到 ≥10 个组合满足 Sharpe≥0.8 且 Fitness≥0.6。- 若未达标：替换/扩充字段池、调整字段配对方式，重复 Phase 2，直至达标。- 示例（占位，替换 field1…field16）：```textfield1 + field2field3 - field4field5 * field6field7 / field8field9 + field10field11 - field12field13 * field14field15 / field16```- 示例（带缺失值处理）：```textpasteurize(field1 / ts_backfill(field2, 22))add(ts_backfill(field1, 22), field2, true)subtract(field1, ts_backfill(field2, 66), true)multiply(ts_backfill(field1, 22), field2, true)```## 📈 Phase 3 评估与闸门（不做参数微调）- 单批评估：- max_sharpe ≥ 1.0 → 进入 Phase 4 做模板验证。- 0.8 ≤ max_sharpe < 1.0 → 记录为候选，优先探索其他字段对；达标后再进入 Phase 4。- 0.5 ≤ max_sharpe < 0.8 → 直接转换到其他字段类型或主题。- max_sharpe < 0.5 → 立即放弃并记录。- 推进门槛：累计 ≥10 个 Sharpe≥0.8 & Fitness≥0.6 的组合后进入 Phase 4。## 🔧 Phase 4 模板检索与验证（MCP）- 模板来源：`get_documentations`（Alpha Examples 等）、`search_forum_posts`（按数据集/字段/主题）、内部模板库。- 字段映射（用 `get_datafields` 校验）：MATRIX 直用；VECTOR 先 `vec_avg/vec_sum`；GROUP 仅做 `group_*`/`neutralize`；ts 窗口仅 {5, 22, 66, 126, 255}。- 批次生成（8/批）：跨模板家族取样，不做参数微调。- 模板家族与示例（占位）：- 分组排序：`group_rank(x, industry)`、`group_rank(x, subindustry)`- 分组标准化：`group_zscore(x, industry)`- 单层中性化：`group_neutralize(zscore(x), industry)`- 双层中性化：`group_neutralize(group_neutralize(x, industry), bucket(cap, 10))`- 截面标准化：`winsorize(zscore(x), 4)`、`quantile(zscore(x), driver=gaussian)`- 向量中性化：`vector_neut(x, y)`- 执行与评估：用 `create_multiSim`（8/批）回测，ASI 确保 `max_trade=ON`；按 Phase 3 闸门判断。## 🔁 迭代与回退策略- 触发：Phase 2 未达 10 个候选，或 Phase 4/5 未过顾问门槛/IS-Ladder/Sub-Universe/Self/Prod-Corr/区域特定测试。- 回退：返回 Phase 2 更新字段池，重采样约 100 个组合并重试；保留有效模板家族方向，优先更换底层字段/主题。- 执行循环：通过 MCP 工具实现 Phase 2 采样与 `create_multiSim` → Phase 3 闸门 → Phase 4 模板检索与回测 → Phase 5 顾问测试；未通过则回退。## 🧮 Phase 5 去重、多样性与稳健性- 相关性：对内/外部 Alpha 做相关性筛选（|ρ| < 0.3）。- 多样性：覆盖不同数据主题/字段家族/操作符族。- 稳健性：- OS 验证与滚动窗口；逐年一致性（Sharpe/IC）；分位单调性；换手与成本敏感性。- D0/D1 交叉自检：如字段也有 D0 数据，可做 D0 自检（非必需）。- 区域特异：ASI 需 Robust Universe Test（返回与 Sharpe ≥90%），max_trade=ON。## 🗂️ Phase 6 文档化与资产化- 记录：批次ID、表达式、参数、指标（Sharpe/Fitness/turnover/IC/年化/回撤）。- 属性：为成功 Alpha 设置 name/tags/描述（dataset/fields/operators/neutralization/delay）。- 沉淀：更新字段质量库与模板库。## 📚 MCP 调用指引（汇总）- 参数与可选项：`get_platform_setting_options`- 数据集与字段：`get_datasets`、`get_datafields`- 模板与学习材料：`get_documentations`- 论坛模板搜索：`search_forum_posts`- 多表达式回测：`create_multiSim`（8/批）- 相关性与提交检查：`check_correlation`、`get_submission_check`

---

## 讨论与评论 (24)

### 评论 #1 (作者: FF56620, 时间: 9 months ago)

开始工作流的方式：按照工作流，对 GLB analyst进行探索 @workflow.md 可用操作符参见 @operators.json 运行过程中，不要停下，直到完成目标

---

### 评论 #2 (作者: FF56620, 时间: 9 months ago)

因为这个工作流是在codex下完成的，同时最近claude code总有不同程度的降智，所以用codex跑起来效果反而比cc更好，codex配置MCP的方式，和其他JSON形式不同，codex使用/.codex/config.toml文件进行配置，配置方式如下：[mcp_servers.wqb_mcp]command = "python"args = ["your_path/cnhkmcp/untracked/platform_functions.py"]description = "WorldQuant BRAIN Platform MCP Server - Core tools for interacting with the BRAIN platform, including simulation, alpha management, and data access. Credentials are stored in user_config.json."

---

### 评论 #3 (作者: BW16434, 时间: 9 months ago)

您好，大佬，你上面说的可用操作符参见的operators.json这个文件内容是什么，能展示下吗

---

### 评论 #4 (作者: FG26814, 时间: 9 months ago)

大佬的工作流，看着就很清晰明了， 至少我看懂， 我想AI 也能明白， 只要调好 工具即可。就看实测中工作流消耗的token 有多少， 是不是可以再把固定的工作流，再固化成为代码，只效给AI 做探索，做经济直觉 工作？

---

### 评论 #5 (作者: JL67084, 时间: 9 months ago)

感谢佬的分享

---

### 评论 #6 (作者: FG26814, 时间: 9 months ago)

今天用AWS的 Kiro 试了一下，能进行回测，但是经常会报MCP 超时的错误， 要求等待十分钟 ， 但还是时常会报错。目前流程上大致能模仿流程，也能回测，但是不能持续进行，最终失败了。目前有两点小结：1. 一直用AI 执行需要确定性事务不是明智选择， 2. 持续进行消耗的Token较大，这样成本会很高。所以我会将AI作为理解Alpha 字段的工具， 做模板可行性的验证，至于持续加回测的活，还是效给固定的硬编码。

---

### 评论 #7 (作者: HJ88260, 时间: 9 months ago)

太强了！！感谢FF大佬的无私分享，这简直是一份保姆级的D1 Alpha开发手册，把MCP工作流的价值体现得淋漓尽致。我之前自己摸索的时候，最大的痛点就是整个流程是散装的、碰运气的。要么在字段选择上就卡住了，不知道如何系统性地筛选；要么就是乱试一堆表达式，回测效率极低，好不容易有一个Sharpe看起来还不错的，一做相关性检验或者IS-Ladder测试就废了，时间全浪费了。您这个工作流直接把整个过程工业化、系统化了，尤其是Phase 2的“两两四则运算”初筛和明确的闸门标准，我觉得这是整个流程最精髓的地方！先用一个成本极低的方式快速海选“潜力股”，而不是一上来就套复杂的模板，这个思路真的解决了大问题，能节省巨量的时间和算力。另外，您把顾问级别的实战门槛和避坑指南都揉进去了，这点对我们来说太关键了。比如ASI必须开max_trade=ON、时间窗口必须用特定值、还有IS-Ladder不同年份的具体阈值，这些细节如果没人总结，自己踩坑可能要交不少“学费”。把它和之前那篇Operator指南结合食用，相当于既给了地图（工作流），又给了操作说明书（Operator详解），可靠性瞬间就上来了。我已经准备按照这个框架把自己的流程重构一下了，感觉有了这个“标尺”，Alpha开发从一种“玄学”变得更像一门“科学”了。再次感谢分享，期待您更多的实战心得！

---

### 评论 #8 (作者: ZZ37826, 时间: 9 months ago)

=============================感谢大佬分享=====================================请问这个方式是通过MCP进行提交回测的，那么效率如何呢，一般来说大模型都有最大Token的概念，那么一般可以提交几轮呢？我在想，是否可以有一种方式，让大模型在提交模拟等待的时候继续思考，而非停滞，这样是不是更能加快效率呢？“- USA：以 D1 为默认；选择液体类 universe（如 TOP 系列）。”请问此处的液体类是什么意思呢？=============================感谢大佬分享=====================================

---

### 评论 #9 (作者: QD44113, 时间: 9 months ago)

感谢分享

---

### 评论 #10 (作者: FF56620, 时间: 9 months ago)

BW16434就是平台文档，也可参考之前的发帖来自MCP的operator指北MCP中也内置了这个方法，可以直接让AI把它抓下来，沉淀为一个文档，后续直接让AI使用这个文档，没有必要让AI每次都去拿，这样一方面提升效率，另一方面也节约Token。希望对你有帮助。

---

### 评论 #11 (作者: FF56620, 时间: 9 months ago)

ZZ37826流动性排名，比如TOP3000，就是流动性最高的3000只股票，这个工作流是通过AI总结经验不断修订的，其中部分内容是AI自行修订的，而AI的原始回答是英文，我让他翻译成了中文，所以其中会有一些不太正确的翻译

---

### 评论 #12 (作者: FF56620, 时间: 9 months ago)

关于之前在群里分享的使用手机远程操作MCP，主要通过开源项目happy实现，可以直接参考链接中的官方文档，也可参考下面这个帖子，之前说在这里更新，最终发成了一篇帖子，这里指个路【随时随地MCP】一个在手机上远程使用MCP的方案===============================================================================================================

---

### 评论 #13 (作者: FF56620, 时间: 9 months ago)

还有一点需要注意，这个工作流主要研究对象为atom，所以前文提到使用四则运算是没问题的，但是对于跨数据集，这里就需要改一下，要强制ai给出有经济学含义的组合，否则存在很大的过拟合风险，特别注意------------------------------------------------------------

---

### 评论 #14 (作者: YH25030, 时间: 9 months ago)

感谢您的分享。对于字段进行四则运算，这个想法很有趣。我也去尝试一下。虽然表达式是否有经济学含义值得商榷，看看是不是能够做出信号。

---

### 评论 #15 (作者: HL42518, 时间: 9 months ago)

感謝大佬无私的分享~~!-----------------------------------------------------------------------------------------------------

---

### 评论 #16 (作者: ZF10741, 时间: 7 months ago)

感谢分享！我使用gemini-cli进行了测试，但是在使用过程中因为token使用量的限制，过程总是被中断，导致无法产出结果。请问佬碰到过相同问题么？有的话是如何解决的。~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~･ᴗ･ 保持热爱，奔赴星海。 ✨~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

---

### 评论 #17 (作者: ST61360, 时间: 6 months ago)

感谢分享！之前不了解工作流的书写方法，通过这篇文章学到了很多工作流方面的知识。拓展了知识边界。

---

### 评论 #18 (作者: CG92231, 时间: 6 months ago)

感谢分享

---

### 评论 #19 (作者: HJ88260, 时间: 6 months ago)

刚接触MCP工作流，看了大佬的分享真的太震撼了！想请教两个小白问题：1）Phase 2批量验证时，如果用Claude经常超时断连，有啥稳定运行的小技巧吗？我试了两次都卡在第三批回测。2）"液体类universe"具体怎么选？在平台下拉菜单里没找到TOP系列的明确选项。目前卡在参数配置这步，大佬能截图指导一下初始设置界面吗？感谢分享这么详细的流程，希望能早日跑出第一个达标alpha！

---

### 评论 #20 (作者: RG19844, 时间: 6 months ago)

用MCP调用工具回测的时候一直显示：Error executing MCP tool: MCP error -32001: Request timed out    这个是有什么需要注意特别设置还是怎么回事呢？

---

### 评论 #21 (作者: AH18340, 时间: 6 months ago)

感谢大佬的分享，太强了=============================================================================The best time to plant a tree is 20 years ago. The second-best time is now.=============================================================================

---

### 评论 #22 (作者: HC58447, 时间: 6 months ago)

这个就是直接丢给AI直接去用是吗？请问你怎么接入Claude的?我是用的第三方中转站

---

### 评论 #23 (作者: YB15978, 时间: 5 months ago)

--------------------------------------------------------------------------------------------------------感谢大佬，写得非常详细，期望大佬还有更新--------------------------------------------------------------------------------------------------------

---

### 评论 #24 (作者: JY55846, 时间: 3 months ago)

==============================================================================大佬这也写的太详细了，认真拜读每一个字符，期待有朝一日我的ai也可以这么懂事，加油==============================================================================

---

