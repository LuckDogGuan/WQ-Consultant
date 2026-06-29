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

* **本地 DEAD_ALPHA_RISK 判别**:
  * 算法优化器在遍历年度统计数据时，如果发现某年 `turnover < 0.0001` 且 `returns ≈ 0`（即 PnL 曲线在该年进入完全平坦的"厂字"状态），判定为 `DEAD_ALPHA_RISK`。
  * 被判定的因子会自动打上 `DEAD_ALPHA_RISK` 标签，评级直接降为 Grade D，在因子目录默认隐藏，并且不会进入后续阶段 of 优化。
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
  1. **IS/OS 衰减判定**: 计算近两年（L2Y）的平均 Sharpe。如果 `L2Y_Sharpe < IS_Sharpe * 0.6`，判定为 OS 表现衰减，降级至 Grade C 并提示风险。
  2. **过拟合预警**: 如果本地 `fitness > 2 * sharpe`，说明收益率畸高且可能伴随超高换手，提示 `overfitting_warning` 并扣分。
  3. **末端平坦度 (厂字) 检测**: 读取最近 200 个交易日的 PNL 值。如果末端连续 200 天 PNL 完全相同或零换手，直接降为 Grade D。
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

## 5. 开发验证情况

* 单元测试用例全部通过（103 passed），覆盖了 `template_iteration`、`backtest_progress`、`optimization_planner` 等核心控制模块。
* 平台 DELETE 模拟接口以及 yearly-stats 接口的解析模块均已通过 Mock/实际测试。
