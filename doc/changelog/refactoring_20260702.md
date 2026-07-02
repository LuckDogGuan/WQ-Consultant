# 重构日志: 因子拉取与自相关性计算限额机制 (2026-07-02)

## 1. 重构动因与背景

在此次重构之前，系统存在以下问题：
*   **重复且低效的后台任务**: 因子列表页存在“同步云端因子”、“刷新本地因子 (自相关)”以及“计算自相关性 (限有PnL)”三个按钮，任务定义与接口设计存在较多冗余。
*   **计算与网络开销巨大**: 原逻辑会对本地所有 B 级及以上的因子在线下载 PnL 数据并做自相关，对 WQ API 的频控限制和系统带宽造成极高压力。
*   **评级规则冗余**: 存在 S/A/B/C/D 五级评级规则，但 D 级因子与 C 级因子的业务差异较小，D 级的物理退休判定不够饱满。

---

## 2. 核心重构与代码变更

我们做出了以下几处深度的代码与架构调整：

### A. 清理废弃路由、函数与按钮
*   **前端修改**: 从 [alphas.html](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/templates/alphas.html) 中删除了三个旧按钮，新放置了“获取服务器因子”与“刷新自相关性”两个按键。
*   **后台路由与接口清理**: 
    *   删除了 `/api/alphas/sync`、`/api/alphas/sync_local`、`/api/alphas/calc_correlation` 的 API 路由 ([main.py](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/main.py))。
    *   在 [sync_service.py](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/sync_service.py) 中删除了对应的三个旧运行任务函数。
    *   在 [job_runner.py](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/job_runner.py) 中删除了这三个任务的 `kind` 条件分发分支。

### B. 开发“获取服务器因子”任务 (`get_server_alphas`)
*   **实现逻辑**: 从云端拉取最近 30 天已完成因子，引入严苛的入库硬过滤：只录取 `Sharpe >= 1.25`、`Fitness >= 0.6`、`Margin >= 0.0005` 且本地不重复的优质因子。
*   **限额自相关**: 为降低带宽开销，入库时实时定级，**只有定级为 S 级的新因子**才会自动在线下载 PnL 并运行本地 Pearson 线性自相关计算，非 S 级因子跳过此自动步骤。
*   **源码位置**: [sync_service.py:L138](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/sync_service.py#L138)

### C. 开发“刷新自相关性”任务 (`refresh_correlation`)
*   **实现逻辑**: 专为本地已经存在且非垃圾的因子服务。扫表时过滤出**仅属于 S 等级**的因子，拉取最新 OS/PPA 核心收益率库，在线单独下载其 PnL 并计算自相关性，进行重估与改名。
*   **源码位置**: [sync_service.py:L511](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/sync_service.py#L511)

### D. 评级合并为 S/A/B/C 与自动退休规则调整
*   **级别合并**: 在定级分类决策树 [template_iteration.py:L368](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/template_iteration.py#L368) 中，将原本会判定为 D 等级的因子直接改为返回评级 **C 级**（废除原 D 级）。
*   **退休触发范围扩大**: 在 [background_inspector.py:L670](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/background_inspector.py#L670) 中，将自动执行远程物理退休并本地 `is_garbage = 1` 隐藏的触发等级，从 D 级调整为了 **C 级**。即所有定级重估为 C 级的弱质或缺陷因子都会被自动在平台上退休下线。

### E. 测试用例重构
*   修补并更新了 `tests/test_local_sync_job.py` 与 `tests/test_background_inspector.py` 的测试用例，将 mock 分支、路径请求、断言全部修正为新的任务与路由。
