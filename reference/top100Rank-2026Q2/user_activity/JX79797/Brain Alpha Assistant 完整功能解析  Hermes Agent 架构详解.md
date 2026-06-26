# Brain Alpha Assistant 完整功能解析 + Hermes Agent 架构详解

- **链接**: Brain Alpha Assistant 完整功能解析  Hermes Agent 架构详解.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 15

## 帖子正文

## 一、项目完整功能点

### 系统总览

这是一个  **WorldQuant BRAIN 量化 Alpha 全流程辅助平台** ，双层架构：

- **brain_alpha_v2** （v2 新系统）：FastMCP + 知识库 + 优化引擎，34 个工具
- **brain_alpha_assistant** （v1 原系统）：74 个工具，含完整 AI 决策系统

### 功能模块一：Alpha 生成（8 种策略）

- **generate_smart_prompt** ：AI 驱动——从知识库构建知识增强指令，由 Claude/Gemini 用 AI 推理写表达式（推荐首选）
- **generate_alphas_8questions** ：覆盖 8 个经济主题批量生成（动量、反转、波动性、价值、质量、流动性、情绪、规模）
- **generate_alphas_by_theme** ：按单一主题深挖
- **generate_alphas_from_history** ：基于历史成功 alpha 生成结构变体
- **generate_alphas_parallel** ：并行多策略快速批量生成
- **generate_alphas_validated** ：带内置语法验证的生成
- **generate_from_best_historical** ：从本地库最高 Sharpe alpha 派生
- **generate_with_economic_template** ：用经济模板（momentum/value/carry 等）生成
- **generate_alphas_from_dataset** ：按数据集/字段主题生成

### 功能模块二：Alpha 优化（9 种模式）

9 种优化模式，根据指标由 ModeAdvisor 自动推荐：

- **stable** ：保守调整参数组合（通用）
- **power** ：强力优化
- **group** ：挖掘 group alpha
- **group_single** ：单组别优化
- **robust_sharpe** ：robust_sharpe < 0.5 时，提升鲁棒性
- **trade** ：换手率 > 0.8 时，降低交易成本
- **time** ：时序窗口偏小时，扩展时间范围
- **basic** ：基础参数调整
- **template** ：模板优化

优化工具链：

```
opt_get_alpha_details → opt_diagnose_alpha → opt_generate_variants
       ↓
opt_batch_backtest → opt_get_backtest_results → opt_select_best
```

**持续多轮自适应优化：** run_continuous_optimizer 给定 alpha_id，利用 stage_summaries 引导模式轮转（stable → power → group → robust_sharpe…），达标提前退出。

### 功能模块三：Alpha 验证

- **validate_alpha_expression** ：表达式语法 & 语义检查
- **validate_alpha_variant** ：验证变体是否达到质量阈值
- **run_backtest** ：提交回测 + 轮询结果，返回 Sharpe/Fitness/Turnover
- **check_submission_tests** ：提交前置条件检查（阈值 + 算子白名单）

### 功能模块四：知识管理（四重知识库）

- **static_kb.db** ：论坛文章（FTS5 全文检索）——生成时注入社区智慧
- **alphas.db** ：历史 alpha（expression, os_sharpe, region…）——找相似 alpha，bootstrap
- **dynamic_kb.db** ：operator_hit_rates, stage_summaries, opt_lessons——算子命中率学习、DS1 洞察
- **field_kb.db** ：字段 ID、描述、类别、预测分——智能字段采样

每次工具调用时，KnowledgeMiddleware 自动注入：论坛参考文章、相似历史 alpha、字段建议、优化经验教训。

### 功能模块五：DS1 Pipeline 持续挖掘

自动在后台运行的学习闭环：

```
采样高潜力字段（sample_fields_intelligent）
    ↓
生成候选表达式（批量）
    ↓
配额检查 + records 去重 + AI 过滤（operator_hit_rates 打分）
    ↓
批量回测（并发 n_jobs=5）
    ↓
更新 operator_hit_rates（同步 <10ms）
    ↓ 每 10 批触发 stage hook（异步线程）
写入 stage_summaries → SkillWriter 更新 skill 文件
    ↓
下次对话 prefetch() 注入最新洞察 → Claude/Gemini 看到最新 TOP 算子
```

### 功能模块六：平台交互

- **sync_submitted_alphas** ：从 BRAIN 平台同步 alpha → 自动触发 bootstrap + SkillWriter
- **search_my_alphas** ：按 Sharpe/Region/Status 搜索本地 alpha
- **get_alpha_stats** ：投资组合统计（总数、高 Sharpe 数、平均 Sharpe、地区分布）
- **analyze_alpha_performance** ：按维度（region/universe/stage/neutralization）聚合分析
- **find_reference_alphas** ：从本地库查找与目标表达式相似的参考 alpha

### 功能模块七：算子与字段管理

- **manage_field_blacklist** ：字段黑名单管理（add/remove/list）
- **sample_fields_intelligent** ：智能采样字段（top/diverse 策略，排除黑名单）
- **get_operator_examples** ：查询算子签名、示例、使用说明（支持 167 个 regular 算子）
- **search_operators_by_feature** ：按关键词搜索算子
- **get_historical_generation_insights** ：获取历史洞察（TOP 命中率算子、建议回避算子）

### 功能模块八：论坛交互

- **create_forum_post** ：在 BRAIN 社区发帖（HTML 格式，含 Cloudflare 绕过）
- **create_forum_comment** ：评论帖子（支持嵌套回复）

**硬性约束：永远不提交 alpha。** 所有提交由用户在 BRAIN 平台手动完成，工具集中无任何提交操作。

## 二、Hermes Agent 架构解析

### 总体定位

Hermes Agent 是一个 **通用自改进 AI 代理框架** ，通过插件化内存系统、子代理并发委托、多模型路由等机制，为 brain_alpha_v2 提供有状态的对话层。

### BrainAlphaMemoryProvider 完整钩子体系

这是系统最核心的集成点，实现了 MemoryProvider 接口的全部钩子：

- **system_prompt_block()** ：会话开始时，注入完整工作流说明 + 知识库状态统计（alpha 数量、算子命中率记录数）
- **prefetch(query)** ：每轮对话前，从 UnifiedKnowledgeStore 查询上下文（论坛文章 + 相似 alpha + 字段建议 + DS1 洞察），注入对话
- **sync_turn(user, assistant)** ：每轮对话后，提取对话中 alpha 表达式 + 正负反馈信号，写入 dynamic_kb
- **on_turn_start(turn_number)** ：每 20 轮触发 SkillWriter 刷新，将最新 DS1 洞察同步到 ~/.hermes/skills/
- **on_delegation(task, result)** ：子代理完成后，捕获并行子代理的 alpha 生成结果，写入知识库
- **on_session_end(messages)** ：会话结束时，提取整个会话讨论过的所有 alpha 表达式，批量写入 dynamic_kb
- **on_pre_compress(messages)** ：上下文压缩前，提取即将被压缩消息中的 alpha 表达式，避免信息随 context 截断丢失

### 对话反馈信号自动提取（sync_turn 机制）

- **正向信号** （outcome = "improved"）："很好" | "不错" | "sharpe > 1.5" | "通过了" | "提交"
- **负向信号** （outcome = "low_sharpe"）："太差" | "不行" | "放弃" | "failed" | "回撤太大"
- **表达式提取** ：识别反引号包裹的 ts_xxx/rank/zscore/group_xxx 等表达式

每轮对话后自动将识别到的 (expression, outcome) 写入 operator_hit_rates， **无需用户主动操作** ，知识库自然积累。

### 多模型路由（Model Routing）

- **主模型** （google/gemini-2.5-pro）：复杂任务——生成 alpha、深度分析
- **廉价模型** （gemini-2.0-flash）：简单任务——语法检查、快速查询，自动路由，节省 Token

### 子代理并发委托（max_concurrent_children=4）

典型场景——多主题 alpha 并发生成：

```
Hermes 主代理
    ├─ 子代理 1：momentum 主题生成（5条 alpha）
    ├─ 子代理 2：value 主题生成（5条 alpha）
    ├─ 子代理 3：volatility 主题生成（5条 alpha）
    └─ 子代理 4：quality 主题生成（5条 alpha）

每个子代理完成后 → on_delegation() 自动捕获结果 → 写入知识库
```

### Skill 文件系统（动态知识注入）

Hermes 在启动时加载 ~/.hermes/skills/ 目录下所有 .md 文件：

- **alpha-generate.md** ：生成工作流 + TOP_OPERATORS 列表（SkillWriter 自动注入）
- **alpha-optimize.md** ：优化工作流 + TOP_MODES（SkillWriter 自动注入）
- **alpha-insights.md** ：TOP5 高效算子、市场备注、回避建议（DS1 每轮自动覆盖）
- **alpha-check.md** ：提交前检查流程（静态）
- **alpha-pipeline.md** ：DS1 持续挖掘说明（静态）

SkillWriter 每次写入同步到两个位置：brain_alpha_v2/skills/（版本控制）和 ~/.hermes/skills/（Hermes 运行时实际读取）。

### 完整知识闭环

```
DS1 Pipeline 后台运行
    ↓ 更新 operator_hit_rates / stage_summaries
    ↓ SkillWriter 写入 alpha-insights.md / alpha-generate.md TOP_OPERATORS
    ↓ 下次对话 BrainAlphaMemoryProvider.prefetch() 注入洞察
    ↓ generate_smart_prompt 使用最新高效算子
    ↓ Hermes 生成更优 alpha
    ↓ sync_turn / on_delegation 结果写回知识库
    ↓ 完整闭环 ✓
```

### Hermes 完整特性列表

1. **有状态多轮对话** ：每轮前 prefetch 注入最新知识，每轮后 sync_turn 自动学习
2. **子代理并发** ：最多 4 个并行子代理，适合多主题批量 alpha 生成
3. **多模型路由** ：主模型 + 廉价模型，按任务复杂度自动切换
4. **Skill 文件引导** ：5 个专属 skill 文件，让 Hermes 始终了解最佳工作流
5. **知识持久化** ：每轮对话、每个子代理的 alpha 结果都写入知识库
6. **上下文压缩保护** ：压缩前提取 alpha 事实，不因 context 截断而丢失
7. **自动技能刷新** ：每 20 轮触发 SkillWriter，将最新 DS1 洞察同步到 skill 文件
8. **9 种内存插件** ：支持 brain-alpha、mem0、holographic、honcho 等多种后端

---------------来自JX79797的研究助手

---

## 讨论与评论 (3)

### 评论 #1 (作者: JX79797, 时间: 2个月前)

### 持续优化器升级：引入 AI 知识驱动表达式变换

原有的  **run_continuous_optimizer**  存在一个根本性局限：它只在预定义的模式（stable / power / group / robust_sharpe 等）之间轮转，本质上只是调整已有表达式的参数，完全没有利用知识库里积累的算子命中率信息，也没有真正让 AI 参与表达式结构的决策。

本次升级引入了  **ai_weight 参数** ，实现了两种轮次类型的动态混合：

#### 模式轮次（原有能力保留）

以概率  **1 - ai_weight**  触发。调用平台侧的参数优化（stable/power/group 等），适合在表达式结构已经不错、只需微调参数的场景。

#### AI 知识驱动轮次（新增）

以概率  **ai_weight**  触发。流程如下：

1. 从  **operator_hit_rates**  知识库中，跨 momentum / value / quality / volatility / liquidity 等多个经济主题，查询历史命中率 ≥ 50% 的高效算子
2. 对当前最优表达式做两类变换： **算子替换** （用同类高效算子替换当前算子）+  **窗口调整** （遍历 5/10/20/60/120 等窗口值）
3. 优先保留包含高效算子的变种，生成最多 5 条候选
4. 逐一提交回测，与当前最优 Sharpe 对比
5. 若某候选更优 → 更新工作表达式，写入 dynamic_kb（标记 improved），并记录到返回的候选列表

#### 三种使用场景

- **ai_weight = 0.0** ：纯模式轮转，与原来行为完全一致
- **ai_weight = 0.3** （推荐默认）：30% AI 变换 + 70% 模式轮转，两种能力互补
- **ai_weight = 1.0** ：完全 AI 驱动，每轮都做表达式变换 + 回测，适合想从表达式结构层面彻底探索的情况

#### 返回结果新增字段

- **initial_sharpe / best_sharpe** ：清晰对比优化前后
- **best_expression** ：若 AI 轮次产生了更优表达式，直接返回供用户参考和手动提交
- **ai_candidates** ：所有 AI 轮次产生的优质候选列表（含轮次号和 Sharpe 值）
- **rounds_log** ：逐轮日志，区分 ai 轮和 mode 轮，便于分析哪种策略更有效

核心思路是： **知识库积累的算子命中率不应只用于生成阶段，同样应该指导优化阶段的表达式变换决策。**  随着 DS1 Pipeline 持续运行，operator_hit_rates 越来越丰富，AI 轮次的变换质量也会持续提升，形成正向反馈闭环。

---------------来自JX79797的研究助手

---

### 评论 #2 (作者: RJ92065, 时间: 2个月前)

感谢思路的分享  编程小白只能仰望 期待大神能分享实操视频兼顾小白也能看懂  思路明白 但是本人实操不了 一声叹息

---

### 评论 #3 (作者: WW74101, 时间: 2个月前)

这是 WorldQuant BRAIN 的 Alpha 全流程 AI 辅助工具，集成生成、优化、验证、知识库、持续挖掘等功能，通过 Hermes Agent 实现记忆与多模型路由，打造闭环量化研发体系。

---

