# WQ Consultant GUI — 文档总目录

> **最后更新**：2026-06-30
> **维护原则**：所有设计决策、工作流、评估规则均以本 `doc/` 目录为唯一权威来源。代码更新后须同步维护对应文档。

---

## 目录结构

```
doc/
├── README.md                       ← 📌 本文件：全局导航与目录说明
├── alpha_lifecycle/                ← 因子全生命周期流程（精读推荐）
│   ├── acquisition.md              ← 因子获取、过滤与入库规则
│   ├── grading_model.md            ← S/A/B/C 四档定级规则
│   └── retirement.md               ← C级致命缺陷因子物理退休与垃圾标记
├── architecture/                   ← 系统全局架构
│   └── system_overview.md          ← 整体设计与模块职责
├── archive/                        ← 历史文档归档
│   ├── alpha_inspection_optimization_record.md
│   ├── only_new_logic_bug.md
│   ├── system_updates_20260629.md
│   └── system_updates_20260630.md
├── changelog/                      ← 系统重构记录
│   └── refactoring_20260702.md
├── design/                         ← UI/UX 与页面规划
│   └── template_iteration_page_plan.md
├── reference/                      ← 因子评估知识库（只增不删）
│   ├── alpha_assessment_and_grading.md
│   ├── optimizable_alpha_classification.md
│   └── platform_retirement_and_salvage.md
├── todo_optimization/              ← 待优化因子集中处理
│   └── README.md
├── troubleshooting/                ← 故障排查与日志优化
│   ├── log_limit.md
│   └── rate_limiting_analysis.md
└── workflow/                       ← 业务流程与配置规范
    ├── alpha_inspection_flow.md
    ├── backtest_profile.md
    ├── backtest_three_stages.md
    ├── candidate_submission_workflow.md
    └── error_handling_and_recovery.md
```

---

## 快速导航

| 文档 | 核心内容 | 适用场景 |
|------|---------|---------|
| [architecture/system_overview.md](architecture/system_overview.md) | 整体架构与模块化分层、全局级联调度流水线 | 系统架构总览与模块定位 |
| [alpha_lifecycle/acquisition.md](alpha_lifecycle/acquisition.md) | 因子获取过滤入口、硬件去重与优良基因提纯 ([sync_service.py:L116](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/sync_service.py#L116)) | 同步与获取策略配置 |
| [alpha_lifecycle/grading_model.md](alpha_lifecycle/grading_model.md) | S/A/B/C 四档定级规则与动态阈值 ([template_iteration.py:L368](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/template_iteration.py#L368)) | 因子定级、隐藏策略、优化方向决策 |
| [alpha_lifecycle/retirement.md](alpha_lifecycle/retirement.md) | C级致命缺陷因子平台物理删除与本地灰化封存 ([background_inspector.py:L670](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/background_inspector.py#L670)) | 垃圾因子清理、平台限额管理 |
| [reference/alpha_assessment_and_grading.md](reference/alpha_assessment_and_grading.md) | S/A/B/C 四档评级标准、垃圾因子判定（负夏普/厂字/DEAD_ALPHA_RISK）、远端二次验证规则 | 因子详细评估理论参考 |
| [reference/platform_retirement_and_salvage.md](reference/platform_retirement_and_salvage.md) | C档缺陷因子 WQ 平台物理删除机制、Check 失败定向拯救模板 | 平台端清理、失败因子挽救改写 |
| [reference/optimizable_alpha_classification.md](reference/optimizable_alpha_classification.md) | 待优化因子分类矩阵（Class A/B/C）、高相关性因子拯救与闭环淘汰工作流 | 因子优化规划、自相关性降低 |
| [workflow/candidate_submission_workflow.md](workflow/candidate_submission_workflow.md) | 候选提交全流程、字段 Catalog、数据错误处理、人工提交决策规范 | 回测结果分级 → 提交前检查 |
| [workflow/backtest_three_stages.md](workflow/backtest_three_stages.md) | 三阶段（FO/SO/TH）优化配置、Per-Job 参数覆盖机制 | 配置批量回测任务 |
| [workflow/error_handling_and_recovery.md](workflow/error_handling_and_recovery.md) | 网络中断、API 限额、Checkpoint 持久化与自动重连 | 长周期任务保障 |

---

## 核心规则速查

### 因子级别（S/A/B/C 四档）与 S 级评级（Premium/Standard/Marginal）

*   **云端同步无数量限制**：同步最近 30 天云端因子时无数量上限拦截，获取全部回测记录以便进行自相关性与 IS/OS 本地诊断。
*   **因子级别 (Grade) 与评级 (Rating)**：系统分档为 S/A/B/C 四级（原 D 级在此次重构中已完全废除并归入 C 级）。“因子评级”是专门针对 **Grade S (黄金级) 因子** 设立的二次细分，分为三个评级；非 S 级因子评级统一为 Substandard (不合格)。

| 档位 (Grade) | 评级 (Rating) | 核心标准 | 系统动作 |
|:-----|:------|:---------|:---------|
| **S** (黄金) | 1. **优质 (Premium)** | Sharpe ≥ 1.70，Fitness ≥ 1.50，Margin ≥ 0.0015，prod_corr ≤ 0.35 | 顶级 S 级，后台巡检与云端同步优先推荐提交 |
| | 2. **一般 (Standard)** | Sharpe ≥ 1.58，Fitness ≥ 1.20，Margin ≥ 0.0012，prod_corr ≤ 0.45 | 优秀 S 级，表现良好，直接提交 |
| | 3. **边际 (Marginal)** | S级兜底（满足 Sharpe ≥ 1.58，Fitness ≥ 1.0，Margin ≥ 0.0010，self_corr ≤ 0.68，prod_corr < 0.50） | 合格 S 级，需二次稳健性检查后决定 |
| **A** (标准) | 不合格 (Substandard) | Sharpe ≥ 1.50，Fitness ≥ 0.80，Margin ≥ 0.0008，self_corr ≤ 0.70，prod_corr < 0.70 | **触发自动 Checks 与 PnL 拉取**，合格后进入提交队列 |
| **B** (审核) | 不合格 (Substandard) | Sharpe ≥ 1.25，Fitness ≥ 0.60，Margin ≥ 0.0005，相关性 < 0.70 | **触发自动 Checks 与 PnL 拉取**，允许送入优化规划，需人工审核 |
| **C** (缺陷/垃圾) | 不合格 (Substandard) | 1. 一般C级：表现较弱，或存在自相关、Turnover 等警告<br/>2. 致命缺陷C级（原D级）：负夏普 (`sharpe < 0`) / 厂字死因子 / 极致相关 (`self_corr > 0.7` 或 `prod_corr >= 0.7`) / 检查失败 / 未来函数泄漏 / 交易股票数 < 30 | 1. 一般缺陷：进入优化规划筛选队列<br/>2. 致命缺陷：本地隐藏 + WQ 平台物理删除 (`DELETE /simulations/{id}`) |

### 厂字因子 / DEAD_ALPHA_RISK 判断条件（规则已按需求放松）

1. **IS 层**：本地 `alpha_type == 'SKIP'` 或 `status == 'FAIL/ERROR'`，或相关性极致极高/直接报错
2. **远端统计与死因子排查层（当前已放松暂停，保留说明供评估）**：
   - 原逻辑对交易股票数 (< 30)、PnL 覆盖率、单年 `longCount == 0` 或 `shortCount == 0`、年度零换手 (`turnover < 0.0001` 且 `returns < 0.00001`)、L2Y Sharpe 衰减进行严格排查。
   - 为避免因规则过严导致大量有潜力的有效候选因子被误判为死因子/C级，现已在代码层将其放松和暂停执行。

### 远端自动核验与补充拉取触发逻辑

```
IF grade in {S, A, B}:
    1. IF status == "UNSUBMITTED":
       → 自动向远端平台提交 Checks 核验 (GET /check)
    2. 针对 C 级及以上强行拉取 yearly-stats 和严格排查的层级目前已放松，避免过多网络消耗和过度打标。
    3. 评级判定分类结果：
       - S / A / B 级合格候选因子：保存完整时序属性，供后续人工审核与提交
       - C 级（物理退休与精简存档）：统一标注 is_garbage = 1 并不进入优化队列；入库时自动剥离其庞大的时序与 PnL 数据，仅保留基础 ID 与状态标识等核心元数据，搭配 SQLite VACUUM 实现数据库极限瘦身（减小 97% 体积）
```

---

## 开发日志

| 版本 | 日期 | 变更摘要 |
|-----|------|---------|
| v1.0 | 2026-06-01 | 初始文档结构建立，基础候选提交工作流 |
| v2.0 | 2026-06-14 | 三阶段回测优化、Per-Job 参数覆盖、模板迭代页面 |
| v3.0 | 2026-06-29 | 五档评级模型（S/A/B/C/D）、垃圾因子隐藏、平台 DELETE 退休、Check 失败拯救模板 |
| v4.0 | 2026-06-29 | 苹果风格双主题、移动端响应式、DEAD_ALPHA_RISK 识别、A级远端二次验证与回测参数合并 |
| v5.0 | 2026-06-30 | Scheme A 自动重命名（无死锁异步实现）、Grade C 因子无死锁自动退休删除、S 级三档细分评级（Premium/Standard/Marginal）、云端同步无数量上限 |
| v6.0 | 2026-07-02 | 文档全面模块化重构；废除 D 级定级规则并入 C 级（四档评级 S/A/B/C）；清理冗余的同步与自相关任务；引入模块化流程图与代码物理行号关联 |
| v6.1 | 2026-07-02 | 统一合并 C 级因子（is_garbage=1）并不再进入优化规划队列；实现 C 级因子 Payload 时序大字段自动剔除与 SQLite VACUUM 碎片空间回收，将数据库体积缩减 97%（从 605MB 降至 18MB）；全量恢复 5.8 万条被删记录并重新定档 |

---

> **注意**：`reference/` 目录下的文件为**只增不改**的知识库，任何新规则以追加方式写入；不得删除已确认的历史条目。

