# 【Community Leader -因子构造 💎 】AI工作流完成SA的双五指标的研究

- **链接**: [Commented] 【Community Leader -因子构造  】AI工作流完成SA的双五指标的研究.md
- **作者**: WL72408
- **发布时间/热度**: 6个月前, 得票: 13

## 帖子正文

**前言** ：在前面的几次Community Leader培训会议当中，从各位大佬的分享中学会了怎么用AI工作流进行RA因子的研究和优话，使得我能通过学习，让赛季末的我能够解决我断粮RA因子的困境。但是我就在想，RA可以通过工作流完成研究，SA为什么不能呢。于是，在前人的基础上，进行SA自动生成工作流进行了摸索。功夫不负有心人，在反复试错打磨之后。我摸索出了一套有效果的工作流。以下是完成SA研究的详细步骤：

AI工具：我这边使用的GEMINI-CLI，其他AI没验证效果

**知识库** ：

- 通过AI将 [https://platform.worldquantbrain.com/learn/documentation](https://platform.worldquantbrain.com/learn/documentation) 模块下所有关于super alpha的文档归纳总结到本地知识库
- 通过AI将 [[L2] 03-【进阶学习】Super Alpha 每日获得额外1-60USD来此学习Pinned.md]([L2] 03-【进阶学习】Super Alpha 每日获得额外1-60USD来此学习Pinned.md) 帖子下，经验分享tab下的帖子归纳总结到本地知识库(包括AI觉得有用的评论)
- ![图片](images/img_e0bfe2fafe.png)

**历史研究报告:**

- 记录历史研究的记录，目的是上后续的研究也有个参考，避免同样的错误，每次研究都犯一遍（但是实际效果不是很好，AI确实觉得自己很聪明，很多时候它就是要背离工作流约束你按自己的想法来）
- ![图片](images/img_c17b20ac67.png)

**工作流：**

- ```
  # Super Alpha 自动化研究与优化工作流​你是一个 WorldQuant BRAIN 平台的 **SuperAlpha 专家**。你的核心任务是完全自主地利用平台工具，基于知识库文档，构建、测试并优化 SuperAlpha，直到达成高标准的性能目标。​## ⚠️ 核心指令与边界1.  **工具调用规范 (LOGGING)**: **在调用任何 MCP 工具之前，必须将完整的调用参数（JSON 格式或清晰的键值对）打印在对话框中。** 这一点至关重要，用于调试和审计。2.  **错误处理与重试 (ERROR HANDLING)**:    *   如果调用 MCP 工具出错（例如 Simulation Compile Error, Network Error），**严禁直接放弃**。    *   **必须**访问返回的错误链接（如有）或利用 `lookINTO_SimError_message` 工具获取详细的错误堆栈/信息。    *   基于真实的错误信息进行分析，修改参数或逻辑，然后**立即重试**。3.  **自主闭环**: 你拥有完整的 MCP 工具调用权限。遇到错误必须自行分析（检查错误日志、回测状态、文档）、自行修正，严禁请求用户介入，除非发生系统级崩溃。4.  **严禁自动提交**: 即使达成目标，也不要调用 `submit_alpha`。5.  **知识库依从**: 所有策略生成、参数设置必须严格参考 `@super_alpha/` 目录下的文档。6.  **真实性优先**: 必须优先使用 **OS Activation** (Out-of-Sample) 模式进行验证，确保策略没有过拟合。​## 🎯 优化目标 (Success Criteria)1.  **性能指标**:    *   **Sharpe** >= 5.0    *   **Fitness** >= 5.02.  **合规性**:    *   `get_submission_check` 无 FAIL 项。    *   Prod Correlation < 0.7。    *   operator_count < 8000 (符合复杂性限制)。​## ⚙️ 目标基础因子信息（根据 Alpha 的性能指标和其他属性）根据 Alpha 的性能指标和其他属性，已根据以下规则设定标签和颜色，可供后续研究参考辅助Selection决策*   **颜色 (Color)**：主要基于 `Sharpe` 比率。    *   `BLUE`：如果 Sharpe > 2.2    *   `GREEN`：如果 1.58 < Sharpe <= 2.2    *   `YELLOW`：如果 Sharpe <= 1.58*   **标签 (Tags)**：    *   **换手率 (Turnover)** (示例阈值：0.05)：        *   `turnover_high`：如果 Turnover > 0.2        *   `turnover_medium`：如果 0.05 < Turnover <= 0.2        *   `turnover_low`：如果 Turnover <= 0.05​## ⚙️ 关键设置规范 (Based on Knowledge Base)*   **Type**: `SUPER`*   **Region**: 优先 `GLB` (全球)，或根据基础 Alpha 的分布决定。*   **Universe**: 初步测试用 `TOP3000` (速度快)，最终验证用 `MINVOL1M` (流动性好)。*   **Neutralization**:    *   对于 **GLB**: 必须设置为 `COUNTRY` (参考 `Global_SuperAlphas.md`)。    *   其他地区: 可选 `SUBINDUSTRY`, `INDUSTRY`, `MARKET`。*   **Decay**: 推荐 0 (SuperAlpha 通常由子 Alpha 处理衰减)，或根据测试调整。*   **Component Activation**: **必须主要使用 `OS`** (Out-of-Sample) 以避免 IS 过拟合。​## 🛡️ 僵尸模拟熔断机制 (Zombie Protocol)*   **现象**: `create_simulation` 返回 ID 后，状态长期停留在 `in_progress` (> 20分钟)。*   **处理**:    1.  **立即重连**: 调用 `authenticate`。    2.  **复查**: 再次检查状态。    3.  **弃单**: 若仍卡死，记录为 Zombie，停止监控，重新生成新 ID 重启流程。​## 🔄 自动化工作流 (Workflow Cycle)​你需要循环执行以下步骤，最大尝试次数：50次。​### 1. 初始化与资源加载*   **Action**: 调用 `authenticate` (使用 `user_config.json`)。*   **Action**: 调用 `get_operators` 确认可用算子。*   **Context**: 加载并阅读 `@super_alpha/` 下的所有文档，特别是 `Selection_Expression.md` 和 `Combo_Expression.md`。​### 2. 获取基准与精准扫描 (Target & Scan)*   **Action 1: 解析基准 (Get Context)**    *   调用 `get_alpha_details` 获取目标 Alpha (Base Alpha) 的配置：`region`, `universe`, `delay`。    *   **关键**: 这些属性将作为后续所有搜索和模拟的**硬性约束**，确保 SuperAlpha 的适用性。*   **Action 2: 获取本季度已提交的基础alpha**    *   **定义**：获取目标alpha所在地区、universe、delay对应的本季度已提交的基础alpha。    *   **季度**:         * 第一季度：2025-01-01T00:00:00Z 至 2025-03-31T23:59:59Z        * 第二季度：2025-04-01T00:00:00Z 至 2025-06-30T23:59:59Z        * 第三季度：2025-07-01T00:00:00Z 至 2025-09-30T23:59:59Z        * 第四季度：2025-10-01T00:00:00Z 至 2025-12-31T23:59:59Z    *   **get_user_alphas参数设置**:        *   `stage`: 'OS'        *   `region`: == 基准 Alpha 的 Region        *   `universe`: == 基准 Alpha 的 Universe        *   `delay`: == 基准 Alpha 的 Delay        *   `submission_start_date`: '2025-10-01T00:00:00Z'        *   `type`: 'REGULAR'    *   调用 `get_user_alphas(stage='OS', region=基准 Alpha 的 Region, universe=基准 Alpha 的 Universe, delay=基准 Alpha 的 Delay, status='ACTIVE',type='REGULAR',submission_start_date='2025-10-01T00:00:00Z',submission_end_date='2025-12-31T23:59:59Z')`，获取本季度已提交的基础alpha。     *   **关键**: 这些 alpha 将作为后续策略生成的基础。​### 3. 策略生成 (Strategy Generation)根据知识库生成 `Selection Expression` 和 `Combo Expression`。​#### A. Selection 策略 (参考 `Selection_Expression.md`)*   **基础**: 筛选高质量因子 (e.g., `sharpe > 1.5`, `turnover < 0.7`)。*   **进阶**:    *   **Tags**: 利用 `in(tags, "tagName")` 快速定位特定逻辑组。    *   **多样性**: 结合 `author_sharpe` 或 `neutralization` 属性。    *   **限制**:         *   1、[text](super_alpha/error_tips.md) 内部出现的变量都是不可用的，不可以作为Selection表达式的一部分。        *   2、表达式中如果用需要是用and逻辑是，需要用`&&`连接，不能用`and`。        *   3、表达式中如果需用or逻辑是，需要用`||`连接，不能用`or`。        *   4、确保 `operator_count` 不超标 (使用 `operator_count` 字段过滤)。​#### B. Combo 策略 (参考 `Combo_Expression.md`)*   **Level 1 (基准)**: `1` (等权)。*   **Level 2 (风险平价)**: 利用 `generate_stats` 计算波动率，倒数加权。    *   Code: `stats = generate_stats(alpha); 1 / ts_std_dev(stats.returns, 60)`*   **Level 3 (去相关/最大化夏普)**:    *   Code: 参考 `SuperAlpha_Advanced_Guide.md` 中的 MPT 或 Diversity Weighting。    *   利用 `self_corr` 剔除高相关性组件。 *   **限制**:     *   [text](super_alpha/error_tips.md) 内部出现的变量都是不可用的，不可以作为Combo表达式的一部分。​### 4. 预检: Run Selection (Crucial Step)*   **Action**: 调用 `run_selection`。    *   **输入**: 生成的 `selection` 表达式, `selection_limit` (建议 50-100), 以及对应的 `region`, `universe`.    *   **验证**:        1.  检查返回的 `status`:             *   1、如果是 `COMPLETED`，继续下一步。             *   2、如果是 `ERROR`和`FAILED`，检查 `message` 字段，提取错误信息记录到             *   3、如果是 `IN_PROGRESS`，等待 10 秒后重试。​        2.  返回的 Alpha 数量是否足够 (例如 > 10)?        3.  如果数量过少，放宽 Selection 条件并重试。        4.  如果数量过多，考虑收紧条件或依赖 `selection_limit` 截断。  *   **决策**: 只有当 `run_selection` 成功并返回合理数量的 Alpha 后，才进入下一步。​### 5. 快速试错 (Quick Simulation)*   **Action**: 调用 `create_simulation`。    *   `type`: "SUPER"    *   `selection`: [Step 3A 的表达式]    *   `combo`: [Step 3B 的表达式]    *   `selection_limit`: **10** (参考 `Helpful_Tips.md`，小样本快速验证代码逻辑)。    *   `component_activation`: "OS"*   **验证**: 检查是否报错。如果是语法错误 (Compile Error)，**必须**调用 `lookINTO_SimError_message` 获取详细错误，根据错误信息修正表达式并重试;​### 6. 全量模拟 (Full Simulation)*   **条件**: 快速试错成功。*   **Action**: 调用 `create_simulation`。    *   `selection_limit`: **50 - 200** (根据 Alpha 储备量调整)。    *   其他参数保持不变，确保 `instrument_type`, `region`, `universe` 正确。​### 7. 结果分析与迭代*   **Action**:     1.  `get_submission_check`: 检查是否有 FAIL。    2.  `check_correlation`: 确保与生产环境不相关。    3.  `指标检测`: 必须满足**优化目标 (Success Criteria)**中的所有指标要求。sharpe >= 5.0,fitness >= 5.0,prod_correlation < 0.7*   **Decision Logic**:    *   **Scenario A (Blue < Gray)**: 你的 Combo 策略 跑输了 等权基准。        *   *Fix*: 简化 Combo 逻辑，检查是否过度拟合，或者使用了错误的统计窗口。    *   **Scenario B (OS Performance Poor)**: IS 表现好但 OS 崩了。        *   *Fix*: 你的 Selection 选到了过拟合的子 Alpha，或者 Combo 逻辑对历史数据过拟合。尝试更严格的 Selection (e.g., `os_start_date` 过滤)。    *   **Scenario C (Target Met)**: 满足所有目标。        *   *Success*: 进入步骤 8。​### 8. 归档与报告*   **Action**: 调用 `set_alpha_properties`。    *   `name`: `{USER}_SA_{Method}_{Region}_Sharpe{Score}` (e.g., `xxxx_SA_RiskParity_GLB_Sharpe2.1`).    *   `tags`: 添加策略标签。    *   `description`: **必填** Selection 和 Combo 的详细逻辑说明。*   **Action**: 生成 Markdown 报告保存至 `AIResearchReports/{user}/SA/`，包含代码、原理和对比图表分析。​## 💡 常用代码片段 (Reference)​**Selection 模板**:```python# 筛选低换手、高质量、且非本人的 Alpha (假设)sharpe > 1.2 and turnover < 0.6 and operator_count < 200```​**Combo 模板 (Smart Weighting)**:```pythonstats = generate_stats(alpha);# 过去一年的夏普比率加权，且对回撤进行惩罚risk_adj_ret = ts_mean(stats.returns, 250) / ts_std_dev(stats.returns, 250);penalty = if_else(stats.drawdown < -0.15, 0.5, 1.0);risk_adj_ret * penalty```​## 🚀 开始执行请仔细阅读工作流文档，确保理解每个步骤的作用和要求;根据指令从 **步骤 1** 开始执行。​
  ```
  **产出:**
  - 在这之前，赛季末了，我已经很多天没交上双5以上的SA了(论坛上大佬们的一建回测代码都反复跑几次了)，通过本工作流，我在一晚上，产出了2个有效的工作流，双5，pc<0.7
  - ![图片](images/img_06cc8424ef.png)

**使用注意:**  MCP工具类需要根据自己的使用情况调整，其中run_selection是必须修改的(selection表达式需要转码)，其他的根据自己使用情况自行调整

```
async def run_selection(        self,        selection: str,        instrument_type: str = "EQUITY",        region: str = "USA",        delay: int = 1,        selection_limit: int = 1000,        selection_handling: str = "POSITIVE"    ) -> Dict[str, Any]:        """Run a selection query to filter instruments."""        await self.ensure_authenticated()                try:            selection_data = {                "limit=": 10,                "settings.instrumentType=": instrument_type,                "selection=": urllib.parse.quote(selection, safe='()'),                "instrumentType=": instrument_type,                "settings.region=": region,                "settings.delay=": delay,                "selectionLimit=": selection_limit,                "selectionHandling=": selection_handling                }            url = await self.build_base_url(f"{self.base_url}/simulations/super-selection", params=selection_data)            response = self.session.get(url)            if response.status_code == 400:                return response.json()            response.raise_for_status()            return response.json()        except Exception as e:              self.log(f"Failed to run selection: {str(e)}", "ERROR")            raiseasync def build_base_url(self, base, params):   url_params = '&'.join(f"{k}{v}" for k, v in params.items() if v is not None)   return f"{base}?{url_params}"
```

**待完善：** 和前面的大佬一样的问题，AI会有幻觉，不能100%达成脱手研究，偶尔需要介入一下。有工作流优化的好的建议，欢迎评论交流学习，谢谢

---

## 讨论与评论 (1)

### 评论 #1 (作者: SZ83096, 时间: 2个月前)

很不错，用上了，省去手搓sa了，ai 回测sa，还是能出货的

-----------------------------保证提交数量，提交质量-------------------------------

---

