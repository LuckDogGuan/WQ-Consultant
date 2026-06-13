# 当前代码优化建议记录

日期：2026-06-13

范围：根据当前 GUI 项目代码、参考目录代码以及本轮反馈，重新整理后续优化方向。本文件只记录建议和待办，不代表已经开始改业务代码。

- 当前项目：`D:\code\WorldQuant Brain\consultant\gui`
- 原始因子机参考：`D:\SoftWare\WQ因子机\python-runtime\scripts`
- MCP / 工作流参考：`D:\SoftWare\AiWorkFlow\untracked`

## 用户反馈后的边界

1. 这是单人使用的工具，不需要把服务器安全做成多人生产系统级别。
2. 管理员密码和 WQ 密码暂时不作为优先优化项，不改现有使用方式。
3. 优先做稳定性、代码拆分、统一封装、后台任务状态机、断点恢复粒度。
4. Alpha lineage 和术语/论坛检索先写成待办，不抢当前功能主线。
5. 表达式验证器值得考虑，因为它可以在本地提前拦截错误，不消耗 WQ API。
6. `optimizeAlpha.py` 的因子增强能力值得参考，但“用哪些因子作为优化输入”还没定，需要单独设计。
7. 平台选项、operators、documentation 已有每周同步机制，暂不作为新增方向，只记录后续可与统一封装整合。

## 当前判断

当前代码已经具备可用的本地/服务器 Web 控制台雏形：FastAPI 页面、SQLite 持久化、后台 JobRunner、断点日志、定时任务、网络监控、限额等待、数据目录缓存和 Alpha 详情页。

下一阶段不建议先追求“大而全”的安全改造，也不建议直接搬旧脚本。更好的路线是把已经能跑的能力稳定下来，让长期任务更可控、更容易恢复、更容易继续扩展。

## 近期优先级

### P0：近期主线

1. 拆分 `app/main.py`

   `app/main.py` 同时承担路由、页面渲染、API、异常处理、业务组装和部分 Alpha 详情处理。路由集中在 `app/main.py:194` 到 `app/main.py:1271`，文件超过 50KB。

   建议拆成：

   - `app/routers/dashboard.py`
   - `app/routers/settings.py`
   - `app/routers/jobs.py`
   - `app/routers/alphas.py`
   - `app/routers/catalog.py`
   - `app/routers/logs.py`

   目标不是重构炫技，而是让后面加表达式验证、优化因子入口、状态机页面时，不继续堆在一个文件里。

2. 统一封装 WorldQuant API 调用

   当前 API 调用散落在：

   - `app/services/wq_client.py`
   - `consultant_core/machine_lib.py`
   - `app/services/simulation_service.py`
   - `app/services/correlation_service.py`
   - `app/services/check_service.py`

   不同地方对 `Retry-After`、401、429、超时、重登、session 生命周期处理不一致。参考目录 `D:\SoftWare\AiWorkFlow\untracked\APP\ace_lib.py` 有 `SingleSession`、`start_session`、`check_session_and_relogin`、`simulate_alpha_list_multi`；`platform_functions.py` 有 `BrainApiClient` 和 Pydantic 请求模型。

   建议后续在当前项目里抽一个轻量 `BrainClient`，先覆盖最常用能力：

   - 登录与重登
   - GET / POST 包装
   - 429 / `Retry-After` 等待
   - 401 重新登录
   - 请求超时
   - 错误消息统一格式

   先不做复杂权限、OAuth、多用户等功能。

3. 后台任务状态机优化

   当前 `JobRunner` 负责启动、暂停、恢复和失败记录，见 `app/job_runner.py:93`、`:124`、`:188`。网络监控和定时任务也会修改任务状态。现状能用，但状态流转规则分散。

   建议建立一个明确的任务状态表：

   - `queued`
   - `running`
   - `paused`
   - `waiting_limit`
   - `waiting_time_window`
   - `waiting_network`
   - `reconnecting`
   - `completed`
   - `failed`

   同时集中定义允许的状态转移，例如：

   - `queued -> running`
   - `running -> paused`
   - `running -> waiting_limit`
   - `running -> waiting_network`
   - `waiting_network -> running`
   - `reconnecting -> running`
   - `running -> completed`
   - `running -> failed`

   后续可以在页面上显示“为什么进入这个状态”，减少长时间跑任务时的不确定感。

4. 断点恢复粒度变细

   当前模拟阶段通过 `*_progress_{job_id}_*.jsonl` 和 `pool_complete` 判断下一次从哪个 pool 开始，见 `app/services/simulation_service.py:601`、`:629`、`:718`。这是好的方向，但恢复粒度主要还是 pool。

   建议后续把单个 simulation task 入库，记录：

   - `pending`
   - `submitted`
   - `polling`
   - `complete`
   - `children_saved`
   - `failed`

   这样进程中断后可以更准确地恢复，避免重复提交过多 Alpha，也能更清楚地看到卡在哪个阶段。

5. 多线程 session 使用方式复核

   `app/services/correlation_service.py:316` 的 `analyze_single_alpha` 在 `ThreadPoolExecutor` 中并发执行，并共享外层 session。`app/services/check_service.py:306` 使用 `session_container`，但请求仍可能共享同一个 `requests.Session`。

   建议结合统一 `BrainClient` 一起处理：每个 worker 使用独立 session，或使用线程本地 session。这样比在每个服务里分别打补丁更稳。

### P1：功能增强候选

1. 引入表达式验证器

   `D:\SoftWare\AiWorkFlow\untracked\APP\Tranformer\validator.py` 里有基于 AST 的表达式验证器，支持函数签名、参数数量、参数类型、操作符白名单等检查。它的价值在于本地判断，不消耗 WQ API。

   建议后续先做成“提交前可选检查”：

   - FO / SO / TH 表达式生成后先本地验证。
   - 手动粘贴 Alpha 表达式时也可验证。
   - 验证失败只阻止明显格式错误，不替代 WQ 官方检查。
   - 验证器缺少最新 operator 时，不要误杀，应该提示“本地规则未知，仍可远程提交”。

2. 使用 `optimizeAlpha.py` 的因子增强能力

   原始因子机 `D:\SoftWare\WQ因子机\python-runtime\scripts\optimizeAlpha.py` 有更丰富的能力：

   - `template_factory`
   - `trade_when_factory`
   - `runStable`
   - `runGroup`
   - `runRuntime`
   - `run_rerun_mode`

   这些能力适合做“已有优质 Alpha 的二次增强”，但现在关键问题不是怎么生成变体，而是“选哪些因子作为输入”。

   暂定候选来源：

   - 相关性分析后标记为 `PPA / RA / ATOM` 的候选。
   - check 通过或接近通过，但某些指标仍可提升的候选。
   - 最近回测阶段里 Sharpe / Fitness / Margin 较好，但未进入最终提交队列的候选。
   - 手动指定的 Alpha ID 列表。

   待定问题：

   - 是否只优化 `PPA / RA / ATOM`，还是也允许优化边缘因子？
   - 是否优先优化低相关高 Sharpe，还是优先优化 check 接近通过的因子？
   - 每个原始因子最多生成多少变体，避免任务爆炸？
   - 优化结果是否需要单独 tag，避免污染原始三阶段结果？

   建议先不急着接入完整 `optimizeAlpha.py`，先做一个“优化输入池设计”。

3. 平台 options / operators / documentation 同步整合

   你已经有每周从平台获取字段和相关元数据的流程。这里暂不新增任务。

   后续如果统一 `BrainClient` 成型，可以把每周同步也接到同一套请求封装里，减少重复登录、重复错误处理和格式不一致。

### P2：暂缓待办

1. Alpha lineage

   原始因子机 `alpha_lineage.py` 有 `AlphaLineageDB`，用于记录 alpha 在各阶段的存活情况。这个方向很好，但当前先完成稳定性和核心功能。

   待办记录：

   - 设计 `alpha_lineage` 或 `alpha_events` 表。
   - 记录表达式来源、dataset、阶段、指标、剪枝原因、check 结果。
   - 后续用于复盘哪些模板、模型或字段前缀更有效。

2. 论坛 / 术语库检索

   `forum_functions.py` 有 glossary 和论坛检索能力。当前先不考虑进入核心流程。

   待办记录：

   - 未来可做成辅助解释入口。
   - 不放入回测、提交、check 的核心链路。
   - 仅用于理解字段、规则、术语或平台说明。

3. 复杂服务器安全改造

   单人使用场景下，暂不优先处理：

   - 多用户权限系统
   - 复杂密码策略
   - WQ 密码加密存储重构
   - 审计级登录日志

   仍然建议保留最小安全意识：不要公开暴露到不可信网络，不要把 `data/`、`logs/`、`credentials.json` 提交到 Git。

## 建议实施顺序

### 第一阶段：结构和稳定性

1. 拆分 `app/main.py` 到 routers。
2. 抽出轻量 `BrainClient`。
3. 统一 401 / 429 / timeout / Retry-After 处理。
4. 改造 correlation / check / simulation 的 session 使用方式。
5. 补一页任务状态机文档。

### 第二阶段：任务可恢复

1. 新增 simulation task 级别记录。
2. 将 pool 日志恢复和数据库 task 状态结合。
3. 页面显示更细的任务进度。
4. 失败任务允许按 task 重试，而不是只能按整个 job 重跑。

### 第三阶段：本地表达式验证

1. 调研 `validator.py` 依赖和可移植性。
2. 抽出最小验证入口。
3. 与当前 operators 每周同步数据对齐。
4. 先做“提示/警告”，稳定后再考虑阻止提交。

### 第四阶段：因子优化输入池

1. 明确优化输入来源。
2. 为每个来源设置筛选条件。
3. 定义每个原始因子的变体数量上限。
4. 从 `optimizeAlpha.py` 选择最小一组模板接入。
5. 给优化结果打独立 tag，避免和原三阶段结果混在一起。

## 暂不做清单

- 暂不修改服务器密码方案。
- 暂不做复杂多用户安全系统。
- 暂不直接复制 `startAllstep.py` 的无限循环和多进程流程。
- 暂不把论坛/术语检索接入核心任务链路。
- 暂不直接全量接入 `optimizeAlpha.py`。

## 结论

根据这轮反馈，后续重点应从“服务器安全大改造”调整为“单人服务器长期运行稳定性”。最值得先做的是拆分代码、统一 WorldQuant API 封装、明确后台任务状态机、细化断点恢复和复核多线程 session。表达式验证器是性价比较高的增强点，因为它能本地拦截错误、减少 API 浪费。`optimizeAlpha.py` 的能力值得用，但需要先确定优化输入池，否则容易生成大量变体而难以管理。

## 2026-06-13 阶段落地记录：Alpha 优化规划器

已按“先规划、不直接跑远程回测”的方式完成第一阶段：

1. 新增 `app/services/optimization_planner.py`，负责从本地 Alpha 记录和提交检查结果中生成优化计划。
2. 新增 `tests/test_optimization_planner.py`，覆盖 `SELF_CORRELATION` 策略、两个以上失败项跳过、等级判定、表达式提取。
3. 新增 `doc/alpha_optimization_planner_2026-06-13.md`，记录候选规则、错误类型映射和后续接入 `optimizeAlpha.py` 的边界。
4. 当前阶段不调用 WorldQuant Brain API，不生成真实增强表达式，只输出计划层结果。

后续接入顺序建议：

1. 给优化规划器增加页面或 API 预览。
2. 接入本地表达式验证器，过滤明显非法表达式。
3. 按 `suggested_modes` 接入 `optimizeAlpha.py` 的最小增强子集。
4. 把优化任务纳入后台任务状态机和更细粒度断点恢复。
