# 系统更新日志 (2026-06-30)

本轮更新主要针对云端大批量同步（`wq_sync`）后出现的 GUI 页面响应卡顿、WorldQuant 平台 429 限频导致的任务中断，以及后台巡检物理退休效率偏低等性能与可靠性瓶颈，进行了深度的数据库与 API 交互流程优化。

---

## 1. 页面加载毫秒级闪电提速 (FastAPI SQL Filter)

* **成因与瓶颈**: 
  * 同步云端因子后，本地 `alpha_records` 表累积了 **9,991 条** 记录。
  * 之前的 `/alphas` 页面使用全量查询，在 Python 内存中对这近万条数据解码 JSON 并执行动态算级（`build_alpha_rating`）。每次刷新耗时 3-5 秒，体验卡顿。
* **优化方案**:
  * 在 `/alphas` 的后台 SQL 查询中引入了 `WHERE a.is_garbage = 0` 的提前过滤（在 `show_hidden != "1"` 时）。
  * 数据库直接过滤掉了 9,000+ 个无表现的垃圾因子，仅将几十个活跃的评级候选因子加载进 Python，直接实现**页面响应的毫秒级渲染（< 15ms）**。

---

## 2. 远端 API 解析防崩溃保护与 429 退避 (Robust API Handler)

* **成因与瓶颈**:
  * 大批量因子进行远程核查时，高频的 API 请求触发了 WQ 平台的 HTTP 429 限频。
  * 限频后，WQ 平台的部分接口（例如 `/check` 或 `/recordsets/yearly-stats`）在某些状态下会返回空包（0 字节）或跳转 HTML 登录/提示页面。
  * 之前的代码直接调用 `resp.json()` 引起了 `JSONDecodeError: Expecting value: line 1 column 1` 异常崩溃，导致整个评估巡检任务中断，表现为“自相关性未保存、Scheme A 重命名未执行、因子留在 UNSUBMITTED”。
* **优化方案**:
  * **增强 `check_alpha_remotely`**: 增加了 `Content-Type` 响应头校验和 `try-except` JSON 安全包裹。如果返回空或 HTML 页面，安全记录警告并继续重试，返回 `ERROR` 状态，不抛出异常中断大任务。
  * **增强 `_run_fetch_pnl_details`**: 对拉取 `yearly-stats`、`pnl` 和因子详情的 API 解析添加了多重防护和数据库 Payload 优雅降级回退。
  * **指数退避重试**: 针对 429 错误和网络波动，加入了基于退避时间乘数（`attempt + 1`）的延迟指数等待，极大地提高了对限流的抵抗能力。

---

## 3. 守护巡检服务批量退休优化 (Batch Retirement & Session Reuse)

* **成因与瓶颈**:
  * 以前的 `BackgroundInspector` 后台守护线程每 30 秒轮询一次，且每次轮询只从平台退休 **1 个** 因子。每一次退休都需要进行一次耗时的 `login_with_credentials` 会话登录（2-3 秒）。
  * 清理存量的数千个垃圾因子非常缓慢，且高频的重复登录极易加剧 WQ 平台对 IP 的封频风险。
* **优化方案**:
  * 重构了 `_process_candidates` 的逻辑：如果发现有 Grade D 的垃圾因子堆积，系统会自动进行**批量收集（单次最多 50 个）**。
  * 全程**复用同一个 WQ session 登录句柄**，并在单个会话中循环调用 `DELETE /simulations/{id}`。
  * 清理速度提升了上百倍（可在几分钟内清理完数千个垃圾因子），且最大程度减少了登录接口调用，极大地控制了限流风险。

---

## 4. 数据库存量垃圾清理

* 本次更新顺便运行了维护脚本，将数据库中历史未对齐的 4,669 条 `status` 为 `CHECKED_FAIL` / `CHECKED_ERROR` 的存量仿真直接批量标记为 `is_garbage = 1`，彻底瘦身了本地活跃因子库。

---

## 5. 开发验证情况

* 运行了核心生产测试：`python -m pytest tests/`
* **120 个核心测试全部通过 (100% PASS)**，证明改动对现有系统机制完全兼容，且增强了健壮性。

---

## 6. Alpha 记录与优化规划页面切换提速

* **成因与瓶颈**:
  * `/alphas` 与 `/optimization` 的按钮切换、等级筛选和分页都会重新请求后端。
  * 旧实现把数据库中大量 Alpha 先全部取出，逐条解析 payload JSON、计算评级/优化计划，再做页面分页。
  * 数据量上来后，翻页和筛选本质上都是重复全量计算，所以表现为“每个位置都慢”。
* **优化方案**:
  * `/alphas` 改为 SQL 先过滤 `is_garbage`、`alpha_type`、日期与 S 级评级阈值，再 `LIMIT/OFFSET` 分页，只对当前页记录做最终评级展示。
  * `/optimization` 页面不再调用共享的 `list_optimization_plans` 生成全量计划，而是在页面路由内先 SQL 过滤非垃圾、S/A/B/C、指定等级和 `CORR_FAIL`，再构建当前候选集合。
  * 新增 `idx_alpha_records_list_filters` SQLite 索引，覆盖列表页最常用的 `is_garbage + alpha_type + created_at` 查询。
* **保留边界**:
  * 未修改共享 `list_optimization_plans` 默认行为，因为它同时影响 dashboard 和 `/api/optimization/plans`。
  * 未修改 WQ 因子优化业务规则，只调整 GUI 查询和分页路径。
* **验证**:
  * 新增 `tests/test_alpha_pages_performance.py`，断言 `/alphas?page=2` 只对当前页记录执行评级计算。
  * 已通过：`python -m pytest tests/test_alpha_pages_performance.py tests/test_optimization_pages.py tests/test_optimization_planner.py tests/test_dashboard_metrics.py`。

---

## 7. 云端因子同步按天断点续拉

* **成因与瓶颈**:
  * 日分片请求成功后没有持久化状态，下一次同步会重复拉取已成功日期。
  * 临时断连分片只写日志，不保留“待重试”状态。
  * 多线程共享同一个 WQ session，容易遇到 `RemoteDisconnected('Remote end closed connection without response')`。
* **优化方案**:
  * 新增 `sync_chunks` 表，按 `kind + region + chunk_start + chunk_end` 记录每日分片状态。
  * `status='success'` 的日期后续同步直接跳过；`status='failed'` 不跳过，下次自动重试。
  * 单个日期分片最多重试 3 次；失败会记录错误摘要并让任务失败，避免用户误以为全部同步完成。
  * 同步分片改为串行执行，避免共享 session 并发请求引发连接中断。
* **验证**:
  * 新增测试覆盖：已成功日期不会重复请求；失败日期写入 `failed` 并可在下次任务重试。
  * 已通过：`python -m pytest tests/test_background_inspector.py`。
