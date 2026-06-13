# Alpha 优化规划器阶段记录

日期：2026-06-13

## 目标

第一阶段只生成优化计划，不直接消耗 WorldQuant Brain API 做远程回测。规划器负责从本地 `alpha_records` 和 `check_results` 中找出值得优化的 Alpha，并根据提交检查返回的失败类型选择后续 `optimizeAlpha.py` 增强方向。

## 候选规则

1. 因子等级为 `marginal`、`standard`、`premium` 时进入候选池。
2. 已经过提交检查的因子也进入候选池，来源包括 `CHECKED_*` 状态或 `check_results` 记录。
3. `substandard` 默认不进入候选池，除非后续明确开启人工强制优化。
4. 缺少 Alpha 表达式时跳过，因为无法生成增强变体。
5. 失败或 ERROR 类型检查项数量大于等于 2 时跳过，不做自动优化。

## 错误类型策略

| 检查错误 | 优化方向 | 对应 `optimizeAlpha.py` 能力 |
| --- | --- | --- |
| `SELF_CORRELATION` | 降低自相关，改变结构或分组形态 | `runGroup`, `runTrade`, `runStable` |
| `PROD_CORRELATION` | 降低产品相关性，调整中性化、分组、模板 | `runGroup`, `runTemplate`, `runStable` |
| `LOW_SHARPE`, `LOW_FITNESS` | 提升基础收益质量 | `runTemplate`, `runRuntime`, `runBasic`, `runPower` |
| `LOW_MARGIN` | 提升边际收益，调整 decay/truncation/power | `runStable`, `runPower` |
| `HIGH_TURNOVER`, `LOW_TURNOVER` | 调整换手率 | `runTrade`, `runStable` |
| 未知单一失败 | 小批量保守探索 | `runStable`, `runTemplate` |

## 第一阶段交付

1. 新增独立服务 `app/services/optimization_planner.py`。
2. 新增单元测试 `tests/test_optimization_planner.py`。
3. 服务输出优化计划，不启动远程回测任务。
4. 提供只读 API：`GET /api/optimization/plans?limit=200`，返回本地优化计划、可优化数量和跳过数量。
5. 后续阶段再把计划接入后台任务，并复用或迁移 `optimizeAlpha.py` 的变体生成能力。

## 第二阶段交付

1. 新增页面 `GET /optimization`，用于人工查看优化候选计划。
2. 页面支持按可优化/跳过、因子等级、优化策略筛选。
3. 页面展示 Alpha ID、状态、等级、策略、建议模式、失败检查、原因和表达式摘要。
4. 新增侧边栏入口“优化规划”。
5. 当前页面仍为只读，不执行远程 API，不提交回测任务。

## 第三阶段交付

1. 新增轻量本地表达式验证器 `app/services/expression_validator.py`。
2. 验证范围包括空表达式、括号/引号闭合、常见 operator 参数数量。
3. 未知 operator 只返回 warning，不直接阻断，避免平台每周新增 operator 后误杀。
4. 优化规划器会在生成计划前执行本地验证；明显非法表达式跳过，跳过原因是 `invalid_expression`。
5. 新增接口 `POST /api/expressions/validate`，请求体示例：`{"expression": "rank(close)"}`。
6. `/optimization` 页面展示表达式检查状态、warning 数和 error 数。

## 第四阶段交付

1. 新增本地 Alpha 增强变体生成器 `app/services/alpha_enhancement.py`。
2. 生成器根据优化计划的 `suggested_modes` 生成小批量表达式候选，不提交远程回测。
3. 已落地的模式：
   - `stable`: `winsorize`、`ts_backfill` 类稳定性包装。
   - `group`: `group_rank`、`group_zscore`、`group_neutralize` 分组增强。
   - `trade`: `trade_when` 非空和成交量门控。
   - `template`: `rank`、`zscore`、`normalize`、`ts_rank`、`ts_zscore`。
   - `power`: `signed_power`。
   - `runtime/basic`: `ts_delta`、`ts_mean` 的基础包装。
4. 新增接口 `GET /api/optimization/variants/{alpha_id}?max_variants=30`，返回源计划和候选表达式。
5. 变体生成后会再次执行本地表达式验证，明显非法的变体不会返回。

## 后续待办

1. 接入真正的增强任务：把 `GET /api/optimization/variants/{alpha_id}` 的输出交给现有 simulation pipeline。
2. 增加更细粒度断点：按源 Alpha、策略 mode、候选表达式三个层级记录状态。
3. 将完整 PLY 表达式验证器作为增强版可选校验，前提是依赖和 operator 数据源稳定。
