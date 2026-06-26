# [AIAC2] Alpha 生成系统：AI驱动的量化策略优化框架经验分享

- **链接**: [Commented] [AIAC2] Alpha 生成系统AI驱动的量化策略优化框架经验分享.md
- **作者**: JX79797
- **发布时间/热度**: 4个月前, 得票: 86

## 帖子正文

- ✅ **自动生成** 符合 BRAIN 平台规范的 Alpha 表达式

- ✅ **智能优化** 基于 5-Agent 架构的多阶段优化流程

- ✅ **持续运行** 自动循环直到达成目标（Sharpe ≥ 1.58, Fitness ≥ 1.0）

- ✅ **完全遵循** WorldQuant 第一定律和 Playbook 优化规则

**🏗️ 系统架构**

**整体架构图**

**![图片](images/img_0f2541df02.png)**

**核心组件架构**

![图片](images/img_c9b53f7578.png)

**💡 核心特性**

**1. 智能数据管理**

**DataManager**：完整的操作符和字段管理

- ✅ **167个REGULAR操作符**：从 `operator_params.json` 和 `operators_latest.json` 加载

- ✅ **完整参数验证**：每个操作符的 min_inputs/max_inputs

- ✅ **字段元数据**：包含 type (scalar/vector), category, region, delay

- ✅ **按需加载**：配置哪个国家，按需加载字段数据

- ✅ **操作符使用指南**：自动生成格式化的参数说明供 AI 参考

```python

# 示例：操作符参数验证

operator_params = {

'divide': {'min_inputs': 2, 'max_inputs': 2},

'rank': {'min_inputs': 1, 'max_inputs': 1},

'ts_decay_linear': {'min_inputs': 2, 'max_inputs': 2},

}

# ✓ 正确: divide(close, volume)

# ✗ 错误: divide(close) - 参数不足！

```

**2. 混合生成策略**

**Cycle 1**：初始生成

- **MultiAI Generator**：3个并发 AI 客户端，每个生成 10 个 Alpha

- **智能采样**：前 50 个高频字段 + 随机采样至 150 个

- **自动验证**：生成后立即验证，拒绝无效表达式

**Cycle 2+**：优化迭代

- **50% 优化**：使用 5-Agent 系统优化最佳 Alpha（生成 15 个变体）

- **50% Data-Driven**：基于经济主题生成新 Alpha（15 个）

- **自动去重**：避免重复表达式

**3. 5-Agent 优化系统（核心创新）**

**Agent 1: 诊断 Alpha**

- 识别症状（按优先级 P5 > P4 > P3）

- 症状类型：high_turnover, low_fitness, high_correlation, weight_concentration, low_sharpe

- 提供根因分析和建议关注点

**Agent 2: 策略规划**

- 根据诊断结果选择优化策略

- 提供具体的修改技术（如 "Add ts_decay_linear", "Change field"）

- 预估改善效果

**Agent 3: 变体生成（最核心）**

- **4个候选表达式库**：

- Library A (Time Series)：用于 high_turnover, low_sharpe

- Library B (Grouping)：用于 low_fitness, weight_concentration

- Library C (Advanced)：用于特定问题

- Library D (Transformation)：通用变换

- **严格规则验证**：

- 第一定律（禁止 rank+rank, zscore*zscore）

- 经济窗口（仅允许 [5, 22, 66, 120, 252, 504]）

- 操作符参数（基于 DataManager 验证）

- **多样性保证**：至少 3 个库，多种优化方向

- 生成 8 个验证通过的变体

**Agent 4: 执行规划**

- 隐含在 MultiStageExecutor 中

- 批量回测所有变体

- 统一打标签 "gemini-2.5-flash"

**Agent 5: 评估结果**

- 选择最佳变体（按 Sharpe 排名）

- 判断是否达标（Sharpe ≥ 1.58, Fitness ≥ 1.0）

- 决定是否继续优化

**4. 多阶段执行流水线**

```

Stage 1 (1step): 初始回测 (30 Alphas)

↓ Filter: Sharpe ≥ 0.0

↓ Select: Top 20

Stage 2 (2step): 剪枝 (20 Alphas)

↓ Filter: Sharpe ≥ 0.5

↓ Select: Top 10

Stage 3 (3step): 深度优化 (10 Alphas)

↓ Filter: Fitness ≥ 1.0

↓ Select: Top 5

Stage 4 (extra): 准备提交 (5 Alphas)

↓ Filter: Sharpe ≥ 1.58

↓ 最佳候选集

```

每个阶段：

- 自动提交回测到 BRAIN 平台

- 统一打标签 "gemini-2.5-flash"

- 记录性能指标（Sharpe, Fitness, Turnover）

- 逐级筛选，确保质量

**5. 完整的规则验证**

**第一定律检查**

```python

# ❌ 禁止的模式

rank(close) + rank(volume) # 不同归一化方法的算术运算

zscore(x) * zscore(y) # zscore 的非线性运算

rank(close) + zscore(volume) # 混合归一化

rank(rank(close)) # 双重归一化

# ✅ 正确的模式

rank(close + volume) # 先组合后归一化

ts_rank(close, 20) * ts_rank(volume, 20) # 时间序列 rank 可以组合

```

**经济窗口验证**

```python

# ✅ 允许的窗口（有经济学意义）

[5, 22, 66, 120, 252, 504]

# 5 = 1周, 22 = 1月, 66 = 1季度, 120 = 半年, 252 = 1年, 504 = 2年

# ❌ 禁止的窗口（无经济学意义）

[7, 10, 14, 30, 60, 100, 200, 250]

```

**操作符参数验证**

```python

# 基于 DataManager 的完整参数定义

# ✓ 正确: divide(close, volume) - 2个参数

# ✗ 错误: divide(close) - 缺少第2个参数

# ✗ 错误: rank(close, volume) - rank只接受1个参数

```

---

🔥 结构特点

**1. 单 Notebook 架构**

所有代码在一个 Jupyter Notebook 中（37个单元格）：

- ✅ **易于理解**：完整研究过程可视化

- ✅ **易于分享**：单文件包含所有逻辑

- ✅ **易于运行**：无需复杂的项目结构

- ✅ **AIAC2 友好**：符合竞赛展示要求

**2. 同步设计（简化）**

- 不使用 `async/await`（简化 Notebook 执行）

- 使用 OpenRouter API 替代 gemini-cli-sdk

- 直接 HTTP 调用 BRAIN 平台 API

- 同步轮询回测结果

**3. AI + 规则混合**

**AI 负责**：

- 创造性生成变体

- 理解经济学逻辑

- 组合不同的操作符和字段

- 提供改进建议

**规则引擎负责**：

- 100% 准确的规则验证

- 确定性检查（可重现）

- 快速过滤无效表达式

- 详细的错误报告

**4. 数据按需加载**

**DataChecker**：运行前检查数据可用性

- 检查操作符数据文件是否存在

- 检查字段数据是否下载（按 region/delay）

- 报告缺失的数据，提供下载提示

- 只有数据检查通过才进入初始化

**DataManager**：按需加载字段

- 配置 `region="USA", delay=1`，只加载 USA_1 的字段

- 自动检测可用的 categories

- 缓存已加载的字段，避免重复读取

- 支持多 region 切换（EUR, ASI, GLB, etc.）

**5. 持续优化循环**

```python

# 终止条件（优先级顺序）

1. SUCCESS: >= 10 个 Alphas 符合目标 (Sharpe ≥ 1.58, Fitness ≥ 1.0)

2. MANUAL STOP: 用户手动停止

3. MAX CYCLES: 达到最大周期数 (默认 50)

4. STAGNATION: 停滞检测（10个周期内 Sharpe 提升 < 0.1）

---

## 讨论与评论 (9)

### 评论 #1 (作者: JC25837, 时间: 4个月前)

这个流程确实很理想，但是有时候AI会卡住或者随意输出结果，那该如何？你这个是工作流还是skill？

---

### 评论 #2 (作者: HQ20665, 时间: 4个月前)

太强了，大佬用什么框架实现的？

---

### 评论 #3 (作者: SF42622, 时间: 4个月前)

太牛了，完美的研究框架，大佬能分享吗 😄

---

### 评论 #4 (作者: JR57542, 时间: 4个月前)

太强了，我也有搭建，但是没有大佬的完整！参考学习了！

- ====================================================================================
  ==================纸上得来终觉浅，绝知此事要躬行======================================
  60

---

### 评论 #5 (作者: LL46807, 时间: 4个月前)

不愧是gm大佬

---

### 评论 #6 (作者: MZ45384, 时间: 4个月前)

不亏是xu佬，这套系统太详细了，学习了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #7 (作者: YX50005, 时间: 4个月前)

太强啦～准备吸收xu佬的思路，看看怎么优化自己的pipeline，竟然全部是在jupyter notebook里实现的，太膜拜了！感觉现在即使是AI写代码，最不擅长的其实就是jupyter notebook了

---------------------If you come to the forum to study hard every day, you will get a GM---------------------------------

---------------------------------------------------------------------------------------------------------------------------

---

### 评论 #8 (作者: LK39823, 时间: 4个月前)

这个属于个工作流还是skills？大佬是不是保留了一些？还是直接可以拿来用的？

===================================================================================

**5-Agent 优化系统（核心创新）**

**Agent 1: 诊断 Alpha**

- 识别症状（按优先级 P5 > P4 > P3）

- 症状类型：high_turnover, low_fitness, high_correlation, weight_concentration, low_sharpe

- 提供根因分析和建议关注点

**Agent 2: 策略规划**

- 根据诊断结果选择优化策略

- 提供具体的修改技术（如 "Add ts_decay_linear", "Change field"）

- 预估改善效果

**Agent 3: 变体生成（最核心）**

- **4个候选表达式库**：

- Library A (Time Series)：用于 high_turnover, low_sharpe

- Library B (Grouping)：用于 low_fitness, weight_concentration

- Library C (Advanced)：用于特定问题

- Library D (Transformation)：通用变换

- **严格规则验证**：

- 第一定律（禁止 rank+rank, zscore*zscore）

- 经济窗口（仅允许 [5, 22, 66, 120, 252, 504]）

- 操作符参数（基于 DataManager 验证）

- **多样性保证**：至少 3 个库，多种优化方向

- 生成 8 个验证通过的变体

- 决定是否继续优化   这个核心模块里面总觉的少了很多东西，大佬想请问一下这里面是不是得再自己写一下优化的方法什么的？是不是得告诉ai用什么方法才能降低换手率 ，比如用哪些操作符才能降低换手率？我看你这里面是有添加现成的模版吗？

=================================================================================

---

### 评论 #9 (作者: CZ39633, 时间: 2个月前)

====================================================================================                        感谢大佬的AIAC2工程分享 。这个框架太齐全了                                                                                ================================自信人生两百年，会当水击三千里==========================

---

