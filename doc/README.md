# WQ Consultant GUI — 文档总目录

> **最后更新**：2026-06-30
> **维护原则**：所有设计决策、工作流、评估规则均以本 `doc/` 目录为唯一权威来源。代码更新后须同步维护对应文档。

---

## 目录结构

```
doc/
├── README.md                       ← 📌 本文件：全局导航
├── wqb.md                          ← WQB 库快速参考
├── wqb_integration_plan.md         ← WQB 库集成方案（历史计划）
│
├── design/                         ← 页面设计与功能规划
│   └── template_iteration_page_plan.md
│
├── workflow/                       ← 业务流程与阶段规范
│   ├── candidate_submission_workflow.md
│   ├── backtest_three_stages.md
│   ├── error_handling_and_recovery.md
│   └── system_updates_20260629.md  ← 最新系统变更详细设计
│
└── reference/                      ← 因子评估知识库（只增不删）
    ├── alpha_assessment_and_grading.md
    └── platform_retirement_and_salvage.md
```

---

## 快速导航

| 文档 | 核心内容 | 适用场景 |
|------|---------|---------|
| [alpha_assessment_and_grading.md](reference/alpha_assessment_and_grading.md) | S/A/B/C/D 五档评级标准、垃圾因子判定（负夏普/厂字/DEAD_ALPHA_RISK）、A级远端二次验证规则 | 因子定级、隐藏策略、优化方向决策 |
| [platform_retirement_and_salvage.md](reference/platform_retirement_and_salvage.md) | D档因子 WQ 平台物理删除机制、Check 失败定向拯救模板 | 平台端清理、失败因子挽救改写 |
| [candidate_submission_workflow.md](workflow/candidate_submission_workflow.md) | 候选提交全流程、字段 Catalog、数据错误处理、人工提交决策规范 | 回测结果分级 → 提交前检查 |
| [backtest_three_stages.md](workflow/backtest_three_stages.md) | 三阶段（FO/SO/TH）优化配置、Per-Job 参数覆盖机制 | 配置批量回测任务 |
| [error_handling_and_recovery.md](workflow/error_handling_and_recovery.md) | 网络中断、API 限额、Checkpoint 持久化与自动重连 | 长周期任务保障 |
| [template_iteration_page_plan.md](design/template_iteration_page_plan.md) | 模板迭代页面结构、多选数据集、Tabbed Preset、表达式本地验证 | 模板迭代功能开发参考 |
| [system_updates_20260629.md](workflow/system_updates_20260629.md) | 苹果风格双主题、移动端适配、DEAD_ALPHA_RISK、A级远端验证、回测参数合并 | 系统更新详细设计与实现细节 |

---

## 核心规则速查

### 因子级别（S/A/B/C/D）与 S 级评级（Premium/Standard/Marginal）

*   **云端同步无数量限制**：同步最近 30 天云端因子时无数量上限拦截，获取全部回测记录以便进行自相关性与 IS/OS 本地诊断。
*   **因子级别 (Grade) 与评级 (Rating)**：系统分档为 S/A/B/C/D 五级。“因子评级”是专门针对 **Grade S (黄金级) 因子** 设立的二次细分，分为三个评级；非 S 级因子评级统一为 Substandard (不合格)。

| 档位 (Grade) | 评级 (Rating) | 核心标准 | 系统动作 |
|:-----|:------|:---------|:---------|
| **S** (黄金) | 1. **优质 (Premium)** | Sharpe ≥ 1.70，Fitness ≥ 1.50，Margin ≥ 0.0015，prod_corr ≤ 0.35 | 顶级 S 级，后台巡检与云端同步优先推荐提交 |
| | 2. **一般 (Standard)** | Sharpe ≥ 1.58，Fitness ≥ 1.20，Margin ≥ 0.0012，prod_corr ≤ 0.45 | 优秀 S 级，表现良好，直接提交 |
| | 3. **边际 (Marginal)** | S级兜底（满足 Sharpe ≥ 1.58，Fitness ≥ 1.0，Margin ≥ 0.0010，self_corr ≤ 0.68，prod_corr < 0.50） | 合格 S 级，需二次稳健性检查后决定 |
| **A** (标准) | 不合格 (Substandard) | Sharpe ≥ 1.50，Fitness ≥ 0.80，Margin ≥ 0.0008，self_corr ≤ 0.70，prod_corr < 0.70 | **触发自动 Checks 与 PnL 拉取**，合格后进入提交队列 |
| **B** (审核) | 不合格 (Substandard) | Sharpe ≥ 1.25，Fitness ≥ 0.60，Margin ≥ 0.0005，相关性 < 0.70 | **触发自动 Checks 与 PnL 拉取**，允许送入优化规划，需人工审核 |
| **C** (优化) | 不合格 (Substandard) | 表现较弱，或存在自相关、Turnover 等警告，但无直接 D 级标志 | **触发自动 Checks 与 PnL 拉取**，进入优化规划筛选队列 |
| **D** (垃圾) | 不合格 (Substandard) | 负夏普 (`sharpe < 0`) / 厂字死因子 / 极致相关 (`self_corr > 0.7` 或 `prod_corr >= 0.7`) / 检查失败 / 未来函数泄漏 / 交易股票数 < 30 | 本地隐藏 + WQ 平台物理删除 (`DELETE /simulations/{id}`) |

### 厂字因子 / DEAD_ALPHA_RISK 判断条件

1. **IS 层**：本地 `alpha_type == 'SKIP'` 或 `status == 'FAIL/ERROR'`
2. **多头/空头归零拦截（全年度核查）**：任意年份 `longCount == 0` 或 `shortCount == 0`（退化死因子直接拦截）
3. **远端年度统计层（C 级及以上均触发拉取）**：
   - 某年 `turnover < 0.0001` 且 `returns < 0.00001` → 判定 DEAD_ALPHA_RISK
   - L2Y Sharpe（近2年均值） < IS Sharpe × 0.50 → 判定 OS 表现衰减，降级至 C 级并标注 os_decay_warning
   - 本地 `fitness > 2 * sharpe` → 过拟合预警，降级 C 级

### 远端自动核验与补充拉取触发逻辑（C 级及以上）

```
IF grade in {S, A, B, C}:
    1. IF status == "UNSUBMITTED":
       → 自动向远端平台提交 Checks 核验 (GET /check)
    2. IF 缺失 yearly-stats 或 PnL 明细:
       → GET /alphas/{id}/recordsets/yearly-stats 并入库
       → 遍历逐年 turnover/returns/longCount/shortCount → 检测 DEAD_ALPHA_RISK
       → 计算 L2Y_Sharpe（近2年均值）→ 对比 IS Sharpe 判定衰减
    3. 综合结论：
       - DEAD_ALPHA_RISK / 多空归零命中 → 降级为 D，物理退休删除
       - L2Y_Sharpe < IS_Sharpe × 0.50 → 降至 C，标注"os_decay_warning"并优化
       - 全部通过 → 保持对应原等级，标注"remote_verified ✓"
```

---

## 开发日志

| 版本 | 日期 | 变更摘要 |
|-----|------|---------|
| v1.0 | 2026-06-01 | 初始文档结构建立，基础候选提交工作流 |
| v2.0 | 2026-06-14 | 三阶段回测优化、Per-Job 参数覆盖、模板迭代页面 |
| v3.0 | 2026-06-29 | 五档评级模型（S/A/B/C/D）、垃圾因子隐藏、平台 DELETE 退休、Check 失败拯救模板 |
| v4.0 | 2026-06-29 | 苹果风格双主题、移动端响应式、DEAD_ALPHA_RISK 识别、A级远端二次验证与回测参数合并 |
| v5.0 | 2026-06-30 | Scheme A 自动重命名（无死锁异步实现）、Grade D 因子无死锁自动退休删除、S 级三档细分评级（Premium/Standard/Marginal）、云端同步无数量上限 |

---

> **注意**：`reference/` 目录下的文件为**只增不改**的知识库，任何新规则以追加方式写入；不得删除已确认的历史条目。

