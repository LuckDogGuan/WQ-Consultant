# WorldQuant Brain 论坛经验贴与代码验证报告

本报告针对本地 `reference/unverified/` 目录下的 11 个论坛经验贴与工具文件进行了全面测试与分类验证。我们对所有代码进行了依赖项补全与格式清洗（去除不换行空格 `\xa0`、纠正缩进、添加动态配置读取逻辑），分类归档至 `reference/code/`，并针对各脚本的核心逻辑运行了单元测试（可通过 [test_code_references.py](../scratch/test_code_references.py) 进行验证）。

---

## 📂 代码分类归档清单 (`reference/code/`)

| 类别 | 模块名称 | 来源文章 | 核心功能说明 |
|:---|:---|:---|:---|
| **Pruning** (剪枝) | [expression_pruner.py](./code/pruning/expression_pruner.py) | [构建因子...剪枝...](./unverified/datafields_and_pruning/构建因子表达式解析器对数据进行高效剪枝-prune%20函数新方法实现代码优化.md) | 基于表达式的语法结构对因子进行去重剪枝，同一结构中仅保留 Sharpe/Fitness 最高的因子。 |
| **Pruning** (剪枝) | [correlation_pruner.py](./code/pruning/correlation_pruner.py) | [结合自相关做剪枝...](./unverified/correlation_reduction/结合自相关做剪枝，提高回测效率代码优化.md) | 基于日收益率 Pearson 相关性矩阵进行贪心剪枝（保留相关度低且综合得分最高的因子组合）。 |
| **Optimization** (优化) | [robust_sharpe_optimizer.py](./code/optimization/robust_sharpe_optimizer.py) | [[工具分享]一键 Robust Sharpe...](./unverified/sharpe_and_pnl_optimization/[工具分享]一键%20%20Robust%20Sharpe优化辅助.md) | 针对给定的 Alpha 进行三阶段多维度参数网格寻优（中性化 -> Decay/Truncation -> 表达式变体）。 |
| **Analysis** (分析) | [super_alpha_correlation.py](./code/analysis/super_alpha_correlation.py) | [【新人向-SA的本地计算SC】...](./unverified/correlation_reduction/【新人向-SA的本地计算SC】复制即用！跟上后一篇PC检测代码！代码优化.md) | 并行下载并批量计算目标 SuperAlpha 与当前 OS 阶段所有因子间的最大相关性，对低相关因子打标。 |
| **Analysis** (分析) | [fast_pnl_downloader.py](./code/analysis/fast_pnl_downloader.py) | [[另辟蹊径]不限额快速获取Pnl](./unverified/sharpe_and_pnl_optimization/[另辟蹊径]不限额快速获取Pnl.md) | 绕过 WQ 每小时 2000 次的 standard PnL API 限额，利用比赛 before-and-after-performance 接口快速获取因子时序数据。 |

---

## 📝 详细验证与经验总结

### 1. [expression_pruner.py](./code/pruning/expression_pruner.py)
* **来源文件**: [构建因子...剪枝...](./unverified/datafields_and_pruning/构建因子表达式解析器对数据进行高效剪枝-prune%20函数新方法实现代码优化.md)
* **是否有用**: **非常有用**。
* **测试结果**: **测试通过**。在测试用例中，成功解析并按表达式结构分类，保留了同组内夏普最高的 `group_neutralize(ts_rank(close, 10), sector)`，剔除了其他同类参数的变体。
* **功能摘要**: 因子挖掘中会生成大量只有参数不同的同构因子（如 `ts_rank(close, 10)` 与 `ts_rank(close, 20)`）。该算法通过拆解表达式提取出操作符和字段列表，作为字符串结构 key 归类，从而进行大范围高效去重，避免重复提交相同构架的因子，降低高互相关风险。

### 2. [correlation_pruner.py](./code/pruning/correlation_pruner.py)
* **来源文件**: [结合自相关做剪枝...](./unverified/correlation_reduction/结合自相关做剪枝，提高回测效率代码优化.md)
* **是否有用**: **非常有用**。
* **测试结果**: **测试通过**。使用 mock 数据构造了高度相关的因子组合，算法成功贪心保留了综合得分高的因子，剔除了互相关系数 $\ge 0.7$ 的冲突因子。
* **功能摘要**: 实现两两因子间的日收益率 Pearson 相关系数矩阵计算，并在本地基于 `0.5 * fitness + 0.5 * margin`（或回退至纯 Sharpe）的得分模式对因子降序排列，利用贪心算法依次检索并剔除与已保留因子相关性过高的变量，极大加快了进入增强阶段的筛选效率。

### 3. [robust_sharpe_optimizer.py](./code/optimization/robust_sharpe_optimizer.py)
* **来源文件**: [[工具分享]一键 Robust Sharpe...](./unverified/sharpe_and_pnl_optimization/[工具分享]一键%20%20Robust%20Sharpe优化辅助.md)
* **是否有用**: **非常有用**。
* **测试结果**: **语法与编译通过**。已完成与全局配置 `user_config.json` 登录凭据的动态对接，去除了硬编码账户密码，并且在并发任务调度中处理了异常重试。
* **功能摘要**: 针对未能通过平台 `LOW_ROBUST_UNIVERSE_SHARPE` 检验的因子，提供了一键式自动化优化管道。分三阶段测试：中性化方式寻优 -> 衰减（Decay）与截断值（Truncation）参数网格模拟 -> 四类因子表达式局部突变（包含 winsorize/group_zscore 等算子挂载），以选出在 sub-universe 下稳健夏普率最高的配置组合。

### 4. [super_alpha_correlation.py](./code/analysis/super_alpha_correlation.py)
* **来源文件**: [【新人向-SA的本地计算SC】...](./unverified/correlation_reduction/【新人向-SA的本地计算SC】复制即用！跟上后一篇PC检测代码！代码优化.md)
* **是否有用**: **非常有价值的工具**。
* **测试结果**: **语法与编译通过**。修复了原帖中由于换行与 `\xa0` 带来的编译错误，提取为独立的类，并集成到我们的系统参数调用中。
* **功能摘要**: SuperAlpha (SA) 阶段的提交对与已提交 OS 因子之间的自相关性 (SC) 有着严格要求（例如不能高于 0.3/0.4）。该工具利用多线程拉取本地或平台 OS 因子 PnL 收益序列，快速计算拟提交 SA 因子的最大自相关系数值，从而防止占用线上提交队列或导致提交直接被拒。

### 5. [fast_pnl_downloader.py](./code/analysis/fast_pnl_downloader.py)
* **来源文件**: [[另辟蹊径]不限额快速获取Pnl](./unverified/sharpe_and_pnl_optimization/[另辟蹊径]不限额快速获取Pnl.md)
* **是否有用**: **非常实用（API 级骚操作）**。
* **测试结果**: **语法与编译通过**。
* **功能摘要**: WQ 官方的标准 PnL 获取 API （`/recordsets/pnl`）存在每小时 2000 次的严格限额。该帖子发现了一个比赛详情的子接口：`/competitions/{competition_id}/alphas/{alpha_id}/before-and-after-performance`，其中当 before 为空时，after 所携带的 PnL 数据正是完整时序 PnL。该接口暂无每小时限额，本工具实现了自动获取当前所有比赛并依次尝试该接口的逻辑，极大提高了大量因子 PnL 的本地下载速度。

---

## 💡 纯经验分享帖子精炼总结

### 6. [【wqapp优化】找灵感提示词优化经验分享.md](./unverified/workflow_and_tools/【wqapp优化】找灵感提示词优化经验分享.md)
* **有用性**: **对提示词设计与自动因子生成非常有用**。
* **核心经验**:
  * **System Prompt 替换**: 原始 `give_me_idea` 模块的灵感生成逻辑容易陷入套路化。通过替换 `BRAIN_Alpha_Template_Expert_SystemPrompt.md`，可以强迫大模型掌握并使用全部 125 个操作符。
  * **提供 8 类高效模板蓝图**: 包含波动率调整动量、行业中性化截面价值、带衰减的短期反转、CAPM 式因子残差、依波动率切换的条件 Alpha、多因子等权与协方差配权组合、分析师预期修正动量、附带稳定性过滤的质量因子等。
  * **引入系统化测试流程**: 指导模型在输出模板的同时配套输出 Discrete 变量网格（如回看周期 window 选择）和 Continuous 变量范围（如 winsorize 限制），以供后续回测调度。

### 7. [VF0.98+Expert直升Grandmaster我是怎么做的.md](./unverified/submission_and_progression/VF0.98+Expert直升Grandmaster我是怎么做的.md)
* **有用性**: **极高的阶段规划与提交策略指导价值**。
* **核心经验**:
  * **GM 晋升核心指标**: 必须同时满足：提交数 > 220，三大 combine 之一的 performance > 2.0，点塔数（Tower） > 60，且六维雷达图排名不拖后腿（特别是平均操作符数、平均字段数）。
  * **季度节奏规划**:
    * **前两个月（稳字诀）**: 集中在 Analyst、Fundamental 等数据覆盖度高的易开发塔，一个月集中攻克 2-3 个主流大地区（USA/GLB/EUR/ASI/IND），交高质量因子（Sharpe > 1.0, Fitness > 0.7）以稳住季度 combine。
    * **最后一个月（冲刺期）**: 集中力量点难度高的偏门塔。为了六维评分及凑点塔点数，可以适当交一些低表现的垃圾 PPA 或硬凑不常用算子，牺牲短期月度 VF 换取综合达标。
  * **保持低复杂性**: 尽量使用简单、有强经济学解释性的因子（平均操作符控制在 2.0 出头），这对于稳住 combine 不退化至关重要。

### 8. [优化Sub-universe Sharpe的一个方法经验分享.md](./unverified/sharpe_and_pnl_optimization/优化Sub-universe%20Sharpe的一个方法经验分享.md)
* **有用性**: **对通过 sub-universe 检查有较高的实操意义**。
* **核心经验**:
  * **问题的根源**: 在大池子（如 TOP3000）回测优异，但次级低流动性池子（如后 2000 支）表现差，导致 `Sub-universe Sharpe below cutoff` 报错。
  * **解决方案**: 使用条件函数（如 `if_else`）将低流动性或小市值部分剔除或降低权重。
    * 基础版: `if_else(rank(cap) > 0.3, alpha, 0)`（截断小市值）。
    * 改进版（避免指标大幅崩塌）: 结合市值与基本面流动性指标共同筛选，如 `if_else(and(rank(mdl219_1_cashratio) < 0.9, rank(cap) > 0.15), alpha, 0)`。
  * **警惕与防范**:
    * 财务流动性（如现金比率 `cashratio`）不等于市场交易流动性，建议优先使用交易额 `volume * close`。
    * 硬截断容易引入参数过拟合，且高频使用会导致同质化严重、SC 暴增。可优先尝试更换中性化方式（`neutralization`）、减小 Universe（如直接在 `ILLIQUID_MINVOL1M` 回测）或调整 `decay`。

### 9. [利用mcp 和优化alpha工作流 成功优化GLB alpha的记录.md](./unverified/workflow_and_tools/利用mcp%20和优化alpha工作流%20成功优化GLB%20alpha的记录.md)
* **有用性**: **AI 自动化因子优化工作流的设计参考**。
* **核心经验**:
  * **优化闭环**: `读取初始指标 -> 因子含义分析/经济学逻辑分析 -> 算子替换/平滑 -> 8个一批次构建 create_multiSim 并行回测 -> 指标监测 -> 迭代优化 -> 去重并沉淀`。
  * **模型建议**: 强烈推荐使用 Gemini 1.5 Pro（或同级别高推理大模型），在调用平台 MCP 批量创建并查询回测进度的场景中，响应极快，错误率低。
  * **ASI 地区特异性**: ASI 地区优化时，除必须开启 `max_trade=ON` 之外，必须通过 Robust Universe Test（即次级 pool 的 Sharpe 要达到总体 pool 表现的 90% 以上）。

### 10. [掌握 Pyramid 策略：区域优化指南 🌏📈.md](./unverified/sharpe_and_pnl_optimization/掌握%20Pyramid%20策略：区域优化指南%20🌏📈.md)
* **有用性**: **对于新手从易到难“点塔”晋级很有帮助**。
* **核心经验**:
  * **第一阶段（奠基）**: 专注 ASI 与 TWN。竞争少，数据集丰富（ASI 推荐 `mdl109`、`anl14`；TWN 推荐 `oth423`、`mdl25`）。采用通用稳定模板如 `group_neutralize(ts_zscore(x, d), industry)`，在两地区各积累 30-50 个因子。
  * **第二阶段（扩展）**: 推进至 GLB 和 KOR。
    * GLB：信号容易高度重合，使用 `group_zscore(ts_zscore(x, d), region)` 进行区域 neutralization。
    * KOR：小市场高波动，利用风险中性化 `vector_neut(ts_zscore(x, d), risk_factors)` 增强稳定性。
  * **第三阶段（进阶）**: 复用已验证模板去迁移其他共享字段区域，并使用 `trade_when` 或 `bucket` 条件减少换手率，获取事件驱动的异象信号。

### 11. [【缘分一座桥优化】甫子君优化工程1代码优化.md](./unverified/sharpe_and_pnl_optimization/【缘分一座桥优化】甫子君优化工程1代码优化.md)
* **有用性**: **系统断点回测界面设计参考（伪代码/前端逻辑）**。
* **核心经验**:
  * 介绍了一种叫“缘分一座桥”的 consultant 辅助工具中，关于流式获取 Alpha 并渲染回测按钮的优化思路。
  * **断点续传设计**: 在循环渲染因子的各变体时，先调用 `CHECK_SIMULATION_RECORD` 本地数据库记录，若该变体已运行过回测，则直接渲染夏普/收益并支持跳转查看；仅对未运行过的变体渲染“触发回测”按钮。避免了网络或程序中断后，重新运行导致重复向平台发起回测申请，节省了仿真额度。
