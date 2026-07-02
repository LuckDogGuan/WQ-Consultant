# 一二三阶段回测优化流程

## 7. 一二三阶段优化流程

三阶段不是“越堆越复杂”，而是逐步收敛。每阶段都要有输入、动作、过滤、输出、停止条件。

### 7.0 阶段参数与开关的作业级别配置 (Per-Job Override)

自 2026-06-29 版本起，批量回测任务在创建时支持在页面 Launch Form (折叠面板中) 针对 FO/SO/TH 的各子阶段配置是否启动以及对应的运行/过滤参数：
- **参数存储**：这些设置直接作为作业的 `params` 属性存入数据库 `jobs` 表的 `params` 字段。
- **优先级原则**：运行回测作业时，系统优先读取当前作业 `params` 中的覆盖参数（通过 `get_bool_param`, `get_int_param`, `get_float_param`, `get_str_param` 等辅助解析器处理），若作业 `params` 中缺失对应配置，则自动回退至 `settings` 表的全局配置。
- **穿插相关性检查**：在 FO/SO/TH 阶段穿插调用的本地相关性检测（`run_inline_correlation_check`）也会自动根据当前作业的 `job_id` 加载对应的 `params` 覆盖相关性 Sharpe 阈值和 Prod 相关性上限。

### 7.1 阶段 1：FO / 一阶探索

目标：先判断字段和基础逻辑有没有信号。

输入：
- 服务器可用字段。
- `webdatascope` 历史统计较好的字段。
- 用户勾选地区：`USA / ASI / EUR`。

动作：
- 做字段画像，不直接大规模套模板。
- 先跑简单表达式：rank、zscore、ts_rank、ts_mean、ts_delta、group_rank 等基础结构。
- 数据画像建议使用：
  - `datafield != 0 ? 1 : 0`
  - `ts_std_dev(datafield, N) != 0 ? 1 : 0`，`N=5,22,66,252`
  - `abs(datafield) > X`
  - `ts_median(datafield, 1000) > X`
  - `X < scale_down(datafield) && scale_down(datafield) < Y`

过滤：
- coverage 太低且 backfill 后仍无交易对象，D 档。
- 任意年份 longCount 或 shortCount == 0 (厂字停牌死因子)，D 档。
- 全 0、全 NaN、长期常数，D 档。
- 单点 Sharpe 高但年份断层，降档。

输出：
- FO 候选。
- 字段质量表。
- 坏字段隐藏原因。

停止条件：
- 字段本身无信号，不进入二阶。
- 一阶结果已经算子过多，不进入二阶。

### 7.2 阶段 2：SO / 二阶扩展

目标：在保留原始经济逻辑的前提下，提升稳定性和泛化。

动作：
- 扫 Decay：建议 `[0, 1, 3, 5, 10, 20]`。
- 扫 Neutralization：至少覆盖 `MARKET`、`SECTOR`、`INDUSTRY`、`SUBINDUSTRY`、`STATISTICAL`；其他如 `CROWDING`、`FAST`、`SLOW`、`COUNTRY` 按平台可用选项选择。
- 做 group 处理：`group_rank`、`group_zscore`、`group_neutralize`。
- 做时序降噪：`ts_mean`、`ts_rank`、`ts_decay_linear`、`ts_backfill`。
- 对高 turnover 可尝试 `trade_when`、Decay、`ts_mean`、目标 turnover delta 限制类算子；不能为了压 turnover 把信号锁死。
- 对负 Sharpe 但绝对值稳定的表达式，可测试一次反向，不做无限反转尝试。

过滤：
- Decay 曲线断崖式下跌，视为不稳定。
- Neutralization 一换就崩，说明可能是行业/风格暴露，不优先提交。
- 本地 PnL 相关矩阵中与已有候选高度相似，先剪枝，避免重复回测。

输出：
- SO 候选。
- 每个候选的 settings sweep 摘要。
- 相关性剪枝记录。

停止条件：
- 需要靠堆 8 个左右算子才过线，停止。
- 修改后经济逻辑已经变成另一个因子，停止并作为新候选记录。

### 7.3 阶段 3：TH / 三阶收敛

目标：只处理明确病因，形成可人工提交候选。

动作：
- 复核 self-corr、prod-corr、sub-universe、drawdown、yearly stats、PnL shape。
- 对 S/A/B/C 分档。
- 对 C 档只做单病因修复：高 turnover、回撤高、sub-universe fail、weight concentration、margin 低等。
- 对临界候选只生成少量变体，不做大规模爬山。

过滤：
- self-corr > 0.70：C 档致命缺陷（原 D 档），不再优化。
- product correlation 高且没有新数据源或新经济逻辑：C 档致命缺陷或人工放弃。
- 回撤来自少数极端日期且无法解释：C 档致命缺陷。
- 年份表现严重断层：C 档致命缺陷或 B 档人工复核。

输出：
- S/A：可人工提交候选。
- B：人工复核候选。
- C（一般缺陷）：优化队列。
- C（致命缺陷）：隐藏坏 alpha，执行 WQ 平台物理删除。
