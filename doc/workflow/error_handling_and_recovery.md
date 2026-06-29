# 错误分类处理与 OS 信息筛选优化策略

## 8. 因子问题与优化动作

| 问题 | 先看什么 | 可尝试优化 | 什么时候不优化 |
| --- | --- | --- | --- |
| self-corr 过高 | 找最高相关 OS alpha、字段、模板、region、settings | 换数据源、换经济假设、换 group/neutralization、剪掉同质候选 | `self_corr > 0.70` 或只是轻微参数差异 |
| product correlation 高 | 是否与平台常见产品暴露相似 | 换数据集、换逻辑方向、降低行业/风格暴露 | 核心逻辑无法改变时不硬救 |
| sub-universe Sharpe 低 | universe、行业集中、流动性、long/short 覆盖 | group neutralize、换 universe 合法组合、减少局部暴露、提高覆盖 | 只在局部小范围有效、换子范围就消失 |
| drawdown 高 | drawdown 日期、是否单次异常、PnL 是否厂字形 | tail/winsorize、rank/zscore、trade_when、Decay、降低极端权重 | 收益主要来自少数异常日期 |
| Sharpe 低 | 字段是否有信号、年份是否稳定、方向是否反了 | 换字段、标准化、时序窗口、neutralization sweep、降噪；稳定负 Sharpe 可反向测试一次 | 数据无信号或多项基础 checks 同时失败 |
| Fitness 低 | Sharpe、Returns、Turnover 的组合 | 提升信号质量，降低无效交易，减少噪声 | 只能靠复杂堆叠提升 |
| Margin 低 | 是否交易太频繁、收益是否被 turnover 稀释 | 降低无效交易、trade_when、Decay、更稳字段 | 只追 Sharpe 但 Margin 长期为负 |
| Turnover 高 | 信号更新频率、字段日频噪声、条件触发 | Decay、ts_mean、trade_when、目标 turnover 限制类算子 | 降 turnover 后信号完全消失 |
| Turnover 过低 | 是否信号被条件锁死、coverage 太低 | 放宽触发、减少过度平滑、换字段 | 无交易对象或字段长期不更新 |
| Weight concentration | 单票权重、行业/市值集中 | scale、rank、group neutralize、tail/winsorize、truncation | 需要极端集中才赚钱 |
| 年份断层 | yearly Sharpe / Returns / Drawdown | 换窗口、换中性化、减少短期过拟合 | 只靠最近一两年爆发 |
| 表达式复杂度高 | Operators per Alpha、嵌套层数 | 删除无效算子，回到简单经济逻辑 | 接近 8 个算子还不稳定 |

提高 Sharpe 的优先级：
1. 先换更好的字段，不先堆算子。
2. 再做标准化：rank、zscore、scale。
3. 再做时序降噪：ts_mean、ts_rank、Decay。
4. 再做 group/neutralization 去掉行业或风格伪收益。
5. 最后才做 trade_when、tail、bucket 等条件和转换。


## 9. Error 分类与处理策略

### 9.1 认证与会话错误

表现：401、403、session 过期、登录失败。

处理：
- 标记 `AUTH_ERROR`。
- 暂停新请求。
- 提示重新认证。
- 不重试回测，不消耗预算。

不需要优化 Alpha，因为问题不在表达式。

### 9.2 平台并发与限流错误

表现：concurrent simulations limit、429、`Retry-After`、长时间 pending。

处理：
- 标记 `RATE_LIMIT` 或 `CONCURRENT_LIMIT`。
- 并发降到 1。
- 按 `Retry-After` 或指数退避等待。
- pending 超时进入 `WAITING_PLATFORM`，不重复创建相同任务。

不需要优化 Alpha，因为是资源调度问题。

### 9.3 参数组合错误

表现：region/universe/delay/neutralization 不兼容，pasteurization、nanHandling、maxTrade 不支持。

处理：
- 标记 `SETTING_ERROR`。
- 从平台 settings 选项重新取合法组合。
- 同一表达式只允许修正 settings 后重跑有限次数。
- settings 变化导致结果结构明显改变时，记录为新候选。

优化的是配置，不是表达式。

### 9.4 表达式语法与算子错误

表现：operator 参数不匹配、类型不匹配、unknown operator、unauthorized operator。

处理：
- 标记 `EXPRESSION_ERROR`。
- 定位 operator、field、参数类型。
- 只做最小修复：类型转换、参数补齐、替换同类基础算子。
- 如果需要大幅改逻辑，进入人工复核，不自动生成大量变体。

不优化的情况：
- 需要堆很多层算子才修好。
- 算子无权限。
- 字段类型和模板根本不匹配。

### 9.5 数据字段错误

表现：field 不存在、dataset 不可访问、coverage 极低、全 0、全 NaN、常数列、longCount + shortCount 接近 0。

处理：
- 标记 `DATAFIELD_ERROR`。
- 对 field 做画像，不直接调 alpha。
- 可尝试 `ts_backfill`、窗口调整、事件触发、group 处理。
- 字段长期无变化或覆盖不可救，D 档隐藏。
- `NO_WEBDATASCOPE_STATS` 不是硬错误，只降低推荐置信度。
- `SERVER_FIELD_UNAVAILABLE` 是硬错误，不进入回测。

### 9.6 数据同步错误

表现：服务器 catalog 拉取失败、本地 webdatascope 缺失或解析失败、scope 缺失、字段无法 join。

处理：
- 服务器失败标记 `SERVER_CATALOG_ERROR`，等待重试。
- 本地 webdatascope 失败标记 `WEBDATASCOPE_CACHE_ERROR`，只影响排序和历史提示。
- scope 缺失标记 `NO_SCOPE_STATS`，继续使用服务器字段。
- join 失败标记 `CATALOG_JOIN_MISS`，展示但不给历史质量分。

不需要优化 Alpha，因为这是目录同步问题。

### 9.7 指标检查失败

表现：Sharpe fail、Fitness fail、Turnover fail、Margin fail、Sub-universe fail、Weight concentration fail。

处理：
- Sharpe/Fitness 低：先判断字段和逻辑，不盲目叠算子。
- Turnover 高：Decay、trade_when、ts_mean、目标 turnover 限制。
- Margin 低：减少无效交易，避免只追 Sharpe。
- Sub-universe fail：检查 universe、行业集中、group neutralize、region 特异性。
- 权重集中：检查 tail、scale、rank、group 分布。


## 10. OS 信息筛选与优化建议

OS 信息只做筛选、相关性和复盘，不做反复调参目标。

建议读取字段：
- alpha id
- type，优先 `REGULAR`
- status / stage，优先 OS 或 submitted 后可用于相关性池的 alpha
- region
- delay
- universe
- dateSubmitted / dateCreated
- settings
- regular expression
- IS 指标摘要
- OS PnL returns，优先最近约 4 年
- checks 结果

筛选建议：
- 只把自有 OS 池作为 self-corr 基准。
- 按 region 分池，USA、ASI、EUR 不混成一个基准。
- PnL returns 缺失的 OS alpha 标记 `OS_PNL_MISSING`，不参与本地相关性计算。
- 过旧且没有近期 PnL 的 alpha 标记 `STALE_OS_REFERENCE`。
- 用最高相关 OS alpha 解释风险：同字段、同模板、同 neutralization、同 region 还是同经济逻辑。
- product correlation 只作为风险标签和扣分项，不能替代官方 check。

好的 OS 参考：
- PnL returns 完整。
- 与候选同 region、同 delay。
- 状态明确，能用于 self-corr。
- 已知表达式和字段，方便解释相关来源。

坏的 OS 参考：
- 没有 PnL。
- region 不匹配。
- type 不明确。
- 状态不稳定或已隐藏。
- 只有表达式相似但没有 PnL 证据。
