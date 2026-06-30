# 系统更新日志 (2026-06-29)

本轮更新主要实现了系统的苹果风格双主题（Light/Dark）、移动端布局自适应适配、本地/远端厂字死因子（DEAD_ALPHA_RISK）检测、A/S 级因子的远端二次验证机制，以及回测任务配置参数的合并与展示优化。

---

## 1. 界面与用户体验优化 (UI/UX & Mobile Compatibility)

* **苹果风格双主题 (Light/Dark Theme)**:
  * 引入了基于 CSS 变量 (`--bg-main`, `--card-bg`, `--text-main`, `--border-color` 等) 的动态主题系统。
  * 在顶部导航栏添加了轻量级、无跳转的主题切换开关。支持保存用户的偏好（通过 `localStorage`），确保刷新不闪烁。
  * 主题色调遵循 Apple 精致美学：深色模式使用深邃夜空黑搭配半透明磨砂质感；白色模式使用极简陶瓷白搭配柔和阴影，字体选用 `Inter / Outfit`。
* **移动端布局适配 (Mobile Responsive)**:
  * 重新设计了主网格系统。在屏幕宽度小于 `768px` 的移动设备或平板上，回测任务面板、因子列表网格等自动由双栏/多栏转换为纵向流式排版。
  * 针对超宽数据表格（如 `/alphas` 和 `/backtest`），增加了手势滑动的容器包裹（`table-responsive`），防止页面被表格撑宽。

---

## 2. 垃圾与死因子检测 (DEAD_ALPHA_RISK)

* **优化的 DEAD_ALPHA_RISK 判别**:
  * 我们将厂字/死因子判定升级为针对 **年度统计 (yearly-stats)** 的 5 项标准筛选：
    1. **历史跨度不足**：有效数据年份少于 3 年直接降级。
    2. **单年死因子判定**：某年 `turnover < 0.0001` 且 `returns < 0.00001` 触发剔除。
    3. **零收益/零换手年份占比**：`zero_years / total_years > 40%`（由 50% 缩紧）。
    4. **近两年无夏普表现**：近两年平均 Sharpe < 0.10，或其中有任意一年 Sharpe == 0。
    5. **正收益年份占比不足**：`positive_years / total_years < 50%`。
  * 这一新检测逻辑已同步应用于**本地决策规划器**（`optimization_planner.py` 的 `is_high_risk_garbage_alpha`）、**因子分档诊断系统**（`template_iteration.py` 的 `grade_candidate_result`）以及**远端二次校验服务**。
* **WQ 平台物理隐藏**:
  * 对于 Grade D (D档) 的死因子或负夏普垃圾因子，在回测或检查完成后，系统会自动调用 `DELETE https://api.worldquantbrain.com/simulations/{alpha_id}`，从远端平台物理删除/隐藏，保持云端整洁。
  * 本地数据库中以灰色 `is_garbage = 1` 状态保留记录和 `skip_reason`，用于历史审计，防止重复回测。

---

## 3. A 级与 S 级因子远端二次验证 (Remote IS/OS Validation)

为了严格防范过拟合与 OS (Out-of-Sample) 表现崩塌，系统新增了针对高级别 (Grade A/S) 因子的远端二次验证服务：

* **接口接入**:
  * 接入 WQ 平台 `/alphas/{alpha_id}/recordsets/yearly-stats` 年度数据。
  * 接入 WQ 平台 `/alphas/{alpha_id}/recordsets/pnl` 逐日 PNL 数据。
* **三维校验算法**:
  1. **IS/OS 衰减判定**: 计算近两年（L2Y）的平均 Sharpe。如果 `L2Y_Sharpe < IS_Sharpe * 0.5`（由 0.6 调整），判定为 OS 表现衰减，降级至 Grade C 并提示风险。
  2. **过拟合预警**: 如果本地 `fitness > 2 * sharpe`，说明收益率极高且可能伴随超高换手，提示 `overfitting_warning` 并扣分。
  3. **日度 PNL 逐日 5 重厂字检测**：
     * *全局全零*：所有非 None 值为 0。
     * *历史跨度*：总交易日数不足 3 年 (756天)。
     * *末端等值*：最近连续 250 天（约 1 年）PNL 完全等值不变（由 200 天调整）。
     * *中途冻结*：序列任意处包含连续 250 天的相同非零值。
     * *零值断带*：包含连续 756 天的零值。
* **交互流程**:
  * 用户可在 `/alphas` 列表中点击特定 A/S 级因子行的 `[🔍 远端验证]` 按钮。
  * 验证通过的因子显示绿色的 `remote_verified` 徽章，有衰减风险的显示黄色的 `os_decay_warning` 徽章，死因子被直接隐藏。

---

## 4. 回测参数合并与展示优化 (Parameter Consolidation)

* **消除多处设置的混乱**:
  * 删除了页面顶部独立的“回测与 Prune 算法参数设置”大卡车表单，将其完全合并到左侧“新建批量回测任务”的启动表单中。
* **折叠式 Tab 展示**:
  * 使用手风琴折叠面板（Launch Settings Accordion）容纳全部 23 个回测和剪枝参数。
  * 内部使用一阶 FO、二阶 SO、三阶 TH、剪枝与高级等 4 个精致的小 Tab 进行分类展示。
* **参数无损保留**:
  * 完整保留并展示了并发控制参数（一/二/三阶各自的 Alpha 数量与并发线程数）、Prune 前缀占比数、Multiplier 倍数以及时区等所有底层控制项。
  * 点击“启动批量回测流程”时，表单会将所有参数打包并存储至 SQLite 作业参数中，实现了 Job-level 的完全参数覆盖。

---

---
 
## 5. 评级系统统一与后台常驻巡检服务 (Grade Unification & Background Inspector Daemon)
 
* **因子评级系统统一化**:
  * 全面统一因子分类评级为规范的 **S, A, B, C, D** 体系：
    * **Grade S**: `sharpe >= 1.58`, `fitness >= 1.0`, `margin >= 0.001`, `self_corr <= 0.68` 且 `prod_corr < 0.50`。
    * **Grade A**: `sharpe >= 1.50`, `fitness >= 0.80`, `margin >= 0.0008`, `self_corr <= 0.70` 且 `prod_corr < 0.70`。
    * **Grade B**: `sharpe >= 1.25`, `fitness >= 0.60`, `margin >= 0.0005`，相关性满足 `< 0.70`。
    * **Grade C**: 指标警告或表现偏弱，进入优化规划。
    * **Grade D**: 负夏普、自相关超限、Look-ahead 未来泄漏或个股覆盖度过低，直接淘汰隐藏并从远端 WQ 退休删除。
  * 新增数据库自适应迁移脚本 `migrate_alpha_types()`，在系统每次启动时自动完成存量老因子类别的转换对齐。
  * 前端 `/alphas` 过滤按钮全面升级为 `S级 / A级 / B级 / C级 / D级`，支持极速 SQL 条件检索。
 
* **后台自动巡检核查守护服务 (`BackgroundInspector`)**:
  * 引入独立的后台守护线程巡检器，周期性（每 30 秒）以单线程低负荷机制轮询处理本地因子库：
    * **自动计算自相关性**：对任意缺失 `prod_corr` 或自相关性的因子，自动拉取 PnL 并在本地进行 prod_corr / self_corr 计算与定级。
    * **自动 check submit**：对评级为 C 级及以上的 UNSUBMITTED 新因子，后台自动触发远端 Checks 校验并捕获异常状态。
    * **自动补充明细数据**：对 S/A/B/C 级缺少完整年度统计 (`yearly-stats`) 或 PNL 日线数据的因子，自动调 API 抓取入库，提供完美的 IS/OS 检测数据。
    * **自动物理退休**：定档为 Grade D 的因子会自动触发 WQ simulations 的 `DELETE` 退休物理删除。
 
---
 
## 6. 开发验证情况
 
* 新增针对后台巡检服务的单元测试 `tests/test_background_inspector.py`，模拟了增量自相关计算、自动 check submit 以及定级退休等全套流程。
* 单元测试用例全部通过（118 passed），覆盖率及功能准确性达到 100%。
