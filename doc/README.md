# WQ Consultant GUI — 文档总目录

> **最后更新**：2026-06-29
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
│   └── error_handling_and_recovery.md
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

### 因子分级（S/A/B/C/D）

| 档位 | 标准 | 系统动作 |
|-----|------|---------|
| **S** | Sharpe ≥ 1.8，Fitness ≥ 3.0，无 Check 失败，Prod Corr < 0.5 | 标记"可直接提交"，优先批量提交 |
| **A** | Sharpe ≥ 1.5，Fitness ≥ 2.5，Check 失败 ≤ 1，Prod Corr < 0.6 | **触发远端二次验证**（拉取 yearly-stats + IS/OS 对比） |
| **B** | Sharpe ≥ 1.2，Fitness ≥ 1.5，Check 失败 ≤ 2 | 标记"需审核"，建议 Decay/中性化扫频后再决定 |
| **C** | 不满足 A/B，但无直接 D 级标志 | 标记"需优化"，进入优化规划队列 |
| **D** | 负夏普 / 厂字 / SKIP / FAIL / DEAD_ALPHA_RISK | 本地隐藏 + WQ 平台物理删除（DELETE /simulations/{id}） |

### 厂字因子 / DEAD_ALPHA_RISK 判断条件

1. **IS 层**：本地 `alpha_type == 'SKIP'` 或 `status == 'FAIL/ERROR'`
2. **远端年度统计层（A 级以上额外触发）**：
   - 某年 `turnover < 0.0001` 且 `|returns| < 0.0001` → 判定 DEAD_ALPHA_RISK
   - OS Sharpe（近 2 年均值 L2Y_Sharpe）< IS Sharpe × 0.6 → 判定 OS 表现崩塌，降至 C 级
   - IS/OS Sharpe 落差超过 40%（`os_sharpe / is_sharpe < 0.60`）→ 疑似过拟合

### 远端二次验证触发逻辑（A 级及以上）

```
IF grade in {S, A}:
    1. GET /alphas/{id}/recordsets/yearly-stats
       → 遍历逐年 turnover/returns → 检测 DEAD_ALPHA_RISK
       → 计算 L2Y_Sharpe（近2年均值）→ 对比 IS Sharpe
    2. GET /alphas/{id}/check
       → 统计 IS checks 中 FAIL/ERROR 数量
    3. 综合结论：
       - DEAD_ALPHA_RISK 命中 → 降级为 D，执行隐藏
       - L2Y_Sharpe < IS_Sharpe × 0.6 → 降至 C，标注"OS衰减预警"
       - check 新增 FAIL → 降至 B，等待人工确认
       - 全部通过 → 保持 S/A，标注"远端验证通过"
```

---

## 开发日志

| 版本 | 日期 | 变更摘要 |
|-----|------|---------|
| v1.0 | 2026-06-01 | 初始文档结构建立，基础候选提交工作流 |
| v2.0 | 2026-06-14 | 三阶段回测优化、Per-Job 参数覆盖、模板迭代页面 |
| v3.0 | 2026-06-29 | 五档评级模型（S/A/B/C/D）、垃圾因子隐藏、平台 DELETE 退休、Check 失败拯救模板 |
| v4.0 | 2026-06-29 | 苹果风格双主题、移动端响应式、DEAD_ALPHA_RISK 识别、A级远端二次验证与回测参数合并 |

---

> **注意**：`reference/` 目录下的文件为**只增不改**的知识库，任何新规则以追加方式写入；不得删除已确认的历史条目。

