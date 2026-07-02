# 巡检与同步流程优化记录 (Optimization Record)

**时间**: 2026-06-30
**状态**: 已完成 (Completed)

## 1. 第一阶段：首屏加载与防崩溃优化

### 1.1 页面加载提速 (FastAPI 渲染瓶颈)
* **问题**: 本地共有近万个因子记录，进入 `/alphas` 页面时，系统会全量查询并执行数万次 `json.loads` 解析和动态计算，导致 3-5 秒的高延迟。
* **解决**: 在 `app/main.py` 的 `/alphas` 路由中，若 `show_hidden != "1"`，则在 SQL 查询中加入 `WHERE a.is_garbage = 0` 过滤条件。此举避免了将数千个已淘汰的垃圾因子加载到 Python 内存中进行循环解析。

### 1.2 增强 WQ API 调用的鲁棒性 (防止 429 限频导致的 JSON 解析崩溃)
* **问题**: 运行高频任务时，平台限频会导致 API 返回 200 状态码但内容为空或为 HTML 页面。此时直接调用 `resp.json()` 会触发 `JSONDecodeError` 异常中断，导致因子的自相关性、状态和名字未能成功更新。
* **解决**: 
  * 在 `app/services/check_service.py` 中：对 `resp.json()` 增加了 `try-except` 保护和 `Content-Type` 校验，在返回非 JSON 内容时安全返回 ERROR，防止异常抛出。
  * 在 `app/services/background_inspector.py` 中：对 `yearly-stats`、`pnl` 和因子详情请求的 `resp.json()` 进行包装，拦截并捕获异常，确保不会中断后续的自相关性计算和评级定级逻辑。

### 1.3 优化后台守护服务 (BackgroundInspector) 处理效率
* **问题**: 之前单次轮询只处理 1 个 D 级垃圾因子且每次重复登录，导致大量积压垃圾因子退休极慢。
* **解决**: 改进了守护进程的轮询清理逻辑。
  * **会话复用**: 复用 `Session` 避免大量无意义的重复登录。
  * **批量处理**: 允许在单次轮询中批量收集并处理最多 50 个 Grade D 因子的退休，大幅加快历史旧因子的物理淘汰速度。

---

## 2. 第二阶段：分段获取、手动控制与定时同步优化

### 2.1 云端因子同步按天分片并发加速 (绕过 10k offset 限制)
* **问题**: WQ API 查询的 offset 上限最大为 10,000。如果用户在一个较长的时间段内（如最近 30 天）模拟了超过 10,000 个因子，分页查询会被直接截断。此外，WQ 的时间区间是开区间（`< end_date`），会导致今天提交的因子无法被拉取到。
* **解决**: 
  * 在 `app/services/sync_service.py` 中，将 30 天 lookback 划分为**以 1 天为跨度的分片**进行并发下载。因为 WQ 规定单日提交上限是 5,000 个，以 1 天为分片能百分百保证不会触碰 10k 的 offset 限制。
  * 最后一个分片的结束时间延展至**明天 (today + 1)**，防止遗漏今天最新模拟的数据。

### 2.2 增加单因子“本地自相关性检查”按钮
* **问题**: 用户希望在因子详情中对某一个特定因子手动发起本地自相关计算，以此获得其最新的 `prod_corr` 和 `ppa_corr` 相关性指标，并实现自动改名。
* **解决**:
  * 增加 `/api/alphas/{alpha_id}/local_correlation_check` 接口，调起本地相关性数据库比对并更新数据库评级。
  * 若评级达到 C 级或以上，则自动触发符合平台格式规范的 Scheme A 远程重命名，完成后刷新界面。



---

## 3. 数据落库与规范 (Data Persisted)
经过本次优化，我们确保每个通过远程 check 核验的因子，均能正常保存以下数据：
1. **相关性**: `prod_corr` 和 `ppa_corr`。
2. **核验状态**: `CHECKED_PASS`, `CHECKED_FAIL`, `CHECKED_ERROR` 及失败详情明细。
3. **名称同步**: Scheme A 格式如 `S_US_T3K_c18_s158_t7_f120`。
4. **时序与评估明细**: 成功将其存入 `recordsets_data` 内。

---

## 4. 验证结果 (Verification)
- **页面刷新**: `/alphas` 过滤垃圾因子后，加载耗时缩短至毫秒级别，避免了无意义的垃圾因子解析开销。
- **并发能力**: 采用 3 个并发 worker 处理 1 天跨度的分片，不仅规避了 10k 截断，且能极大减少网络超时发生。
- **单元测试**: 核心组件和业务逻辑的自动化 `pytest` 用例全部绿灯通过（新增 local_sync_job 后，共 128 项 passed）。

---

## 5. 第三阶段：Alpha 列表与优化规划切换卡顿修复

### 5.1 根因
* `/alphas` 页面原先先查询所有匹配 Alpha，再对每条记录执行 `build_alpha_rating()`、高危因子判断，最后才在 Python 内存中分页。切换等级、日期、页码时都会重复解析整批数据。
* `/optimization` 页面原先依赖共享的 `list_optimization_plans(limit=500)` 重建最多 500 个优化计划，再在 Python 中应用“全部待优化 / 自相关性超标 / 其他性能优化 / 已跳过 / 等级 / 策略”过滤。
* 因此卡顿不是前端按钮问题，而是每次切换都触发后端重复全量计算。

### 5.2 本次处理流程
1. 更新 GitNexus 索引后，对 `get_alphas`、`get_optimization_page`、`list_optimization_plans` 做影响分析。
2. `list_optimization_plans` 影响 dashboard 与 API，风险为 HIGH，因此不修改共享函数。
3. 在页面路由内做最小优化：
   * `/alphas` 将 `is_garbage`、等级、日期、评级条件下推到 SQL，并使用 `LIMIT/OFFSET` 只对当前页 12 条记录计算评级。
   * `/optimization` 在页面路由内先用 SQL 过滤非垃圾、S/A/B/C、等级和 `CORR_FAIL`，再只对筛出的候选构建计划。
   * 增加 `idx_alpha_records_list_filters(is_garbage, alpha_type, created_at DESC)` 索引，支撑常用列表筛选。
4. 保留共享优化计划 API 行为，避免影响 dashboard 统计和后台优化任务。

### 5.3 注意事项
* 页面性能问题优先检查“分页是否下推到 SQL”。不要在 Python 中先全量 JSON 解码、评级、再分页。
* `list_optimization_plans` 是共享入口，改动前必须重新做 GitNexus impact；若风险仍为 HIGH，应优先做页面专用查询或新增显式参数，不要改变默认语义。
* `/alphas` 的评级过滤目前用 SQL 近似匹配 S 级三档阈值，再对当前页做最终展示计算；如果未来要做到“总数与复杂评级完全一致”，应把评级结果持久化成数据库列，而不是恢复全量扫描。
* WQ 平台相关判断仍以 `doc/reference/` 和两个 WQ skill 为业务边界来源；本次只优化 GUI 查询路径，不改变因子拯救、相关性红线或提交规则。

---

## 6. 第四阶段：云端同步按天断点续拉

### 6.1 根因
* 云端同步虽然按 1 天切片拉取，但成功/失败状态只存在当前任务内存里。
* 一旦某个日期分片出现 `RemoteDisconnected` 或平台临时断连，下次同步仍会从整个 lookback 区间重新拉取，导致已成功日期重复请求。
* 旧实现还在多个线程中共享同一个 WQ `requests.Session`，这会放大远端断连概率。

### 6.2 当前流程
1. 启动 `sync_alphas` 后，将 lookback 区间切为 `[day, day+1)` 的日分片。
2. 查询 `sync_chunks` 表，跳过 `status='success'` 的日期分片。
3. 对未成功分片逐天拉取，每个日期最多重试 3 次。
4. 分片成功后写入 `sync_chunks(status='success', fetched_count=N)`；即使当天没有 Alpha，也记录 success，后续不重复拉。
5. 分片失败后写入 `sync_chunks(status='failed', error=...)`，任务最终报 failed；下次同步会自动重试这些 failed 日期。
6. 已经拉取成功的数据仍会正常入库、去重并触发后续巡检；失败日期不会被标记为完成。

### 6.3 注意事项
* 不要手动删除 `sync_chunks`，除非明确需要强制重拉历史日期。
* 如果 WQ 平台某天数据会变化，当前策略不会自动重拉已成功日期；需要补一个“强制重拉最近 N 天”的显式开关后再做。
* 为了稳定性，当前云端同步分片改为串行；如果未来要恢复并发，应为每个 worker 使用独立 WQ session，不能共享同一个 session。

---

## 7. 第五阶段：未处理因子过滤、仪表盘与计数器优化、巡检自适应提速

**时间**: 2026-07-01
**状态**: 已完成 (Completed)

### 7.1 未处理因子过滤与列表展示优化
* **问题**: 之前同步云端因子后，大量尚未进行 PnL 拉取、自相关补算、或 Checks 检验的半成品因子会直接显示在 Alpha 列表中。这导致因子的属性（如相关性、年化收益率、年化回撤等）显示为空白或默认值，给用户带来展示不全的视觉混乱。
* **解决**: 
  * 在 `app/main.py` 的 `/alphas` 路由中，对列表展示的数据增加了 SQL 强校验：只显示已完全处理的因子，即分数（Sharpe/Fitness）、利润率（Margin）、年化收益/回撤、自相关/云端相关性（PPA/Prod）均已补全且非空的因子。
  * `where += " AND a.sharpe IS NOT NULL AND a.fitness IS NOT NULL AND a.margin IS NOT NULL AND a.returns IS NOT NULL AND a.drawdown IS NOT NULL AND a.ppa_corr IS NOT NULL AND a.prod_corr IS NOT NULL"`
  * 对于尚未处理的半成品因子，它们会保持不被列出，并交由后台巡检监视器（Background Inspector）逐步补全。一旦巡检完成，便会自动在列表中展现。

### 7.2 仪表盘与右上角计数器优化
* **进度条标签修正**: 原先所有任务都会在进度条上写死 `Pool X / Y` 标签（使得同步因子时显示 `Pool 22 / 100` 等奇怪字符）。重构了 `backtest.html` 与 `dashboard.html`，规定只有当任务类别确实是 `backtest` 时展示 `Pool X / Y`，其余任务一律仅展示百分比进度。
* **临时自动评估任务自动清理**: 同步云端因子后自动触发的评估校验任务（Job kind 为 `alpha_inspection`，如 Job #71），在其成功执行完毕后，系统会在 `app/job_runner.py` 中自动将其从 `jobs` 表和 `job_events` 历史表中物理删除，从而避免已完成的辅助型任务一直堆积占用仪表盘任务栏的显示位置。
* **右上角双重计数器展示**: 列表右上角的总数提示由原本只显示当前页过滤后的总个数，升级重构为：
  `总共已处理: {{ total }} 个 | 总共记录: {{ total }} | 总因子: {{ total_count }} | 待处理: {{ pending_count }}`
  * `total`：当前已处理完毕且符合查询过滤条件的因子数（用于正确计算前端分页数）。
  * `total_count`：当前数据库中除垃圾因子外的总非垃圾因子数（`is_garbage = 0`）。
  * `pending_count`：当前处于待处理队列中、尚缺少指标或自相关性的因子个数（`is_garbage = 0 AND 有字段为空`）。

### 7.3 后台巡检监视器 (Background Inspector) 详细运行逻辑与自适应提速
后台巡检监视器是一个独立的后台持久化守护线程（Singleton），用来对所有新增或待修补因子进行静默核算：

#### 7.3.1 级联流水线处理 (Checkpoints Pipeline)
巡检器在每个周期扫描非垃圾因子，进行实时评级（S/A/B/C/D）分类。若为 D 级则批量呼叫 WQ 进行物理退休并标记垃圾；若为 S/A/B/C 级，则拉入包含 10 个任务的执行队列，并顺序通过以下四个流水线核查阀门：
1. **Checkpoint 1 (PnL拉取 - FETCH_PRECHECK)**: 若因子未拉取 PnL 时序数据（`pnl_fetched = False`），拉取 WQ 全量日频时序并保存。
2. **Checkpoint 2 (自相关性计算 - CORR)**: 若因子未计算本地自相关（`self_corr_checked = False`），或云端已回测失败（`ERROR`/`FAIL`）但本地未同步状态。则调用算法计算该因子与本地所有其他因子的自相关相关系数，存入 `ppa_corr`，更新等级并根据 Scheme A 统一规格重命名（如 `S_USA_TOP3000_1P65`）。
3. **Checkpoint 3 (远程Checks校验 - CHECK)**: 若因子评级在 C 级及以上，状态为 `UNSUBMITTED` 且无 Checks 历史记录。向 WQ 平台提交 Check 校验，并将 Checks（PASS/FAIL）明细和云端相关性（`prod_corr`）落库。
4. **Checkpoint 4 (年度指标补充 - FETCH)**: 若因子评级在 C 级及以上且无年度分解数据（`yearly-stats`），拉取年度数据详情并计算年化指标，做最终评级命名更新。

#### 7.3.2 自适应提速机制
为了既不占用本地硬件 CPU/内存/数据库独占锁，又不频繁请求 WQ 导致 429 报错封号，监视器使用了自适应轮询：
* 默认情况下，巡检器在每轮扫描处理完之后会进行 **30 秒** 的休眠（低碳节能）。
* **自适应变频**：若当前批次处理后，返回的工作任务数达到了单批并发上限（$\ge 10$ 个），系统会判定当前队列中还有任务积压，会自动将下一次检测的休眠等待时间由 30 秒缩短为 **3 秒**，从而进入“连轴转”状态以秒级速度消化积压，直至所有积压全部被消化干净后自动退回 30 秒睡眠。

### 7.4 静态指标拉取前置与批量增量修补
* **同步阶段前置拉取**：
  * 对底层核心客户端 `consultant_core/machine_lib.py` 中的 `_alpha_query_url` 函数进行了修改，显式请求了字段投影：
    `fields=id,name,dateCreated,regular.code,is.sharpe,is.fitness,is.turnover,is.margin,is.returns,is.drawdown,is.longCount,is.shortCount,settings.region,settings.universe,settings.neutralization,settings.decay`
  * 这确保了未来进行“同步云端因子”时，年化收益 (`returns`) 和回撤 (`drawdown`) 等静态属性在同步阶段就直接完成拉取并入库，不再留空。
* **存量缺失数据的高效批量修补 (`fix_missing_metrics`)**：
  * 在 `app/services/sync_service.py` 中新增并集成了 `fix_missing_metrics(session)` 函数。
  * 该函数会在云端同步任务快要结束（关闭会话前）自动触发。它会检索本地数据库中所有 `returns` 或 `drawdown` 缺失的活跃因子，并使用 WQ 的 Unit Separator `%1F`（多 ID 批量过滤）特性，以 **50 个 ID 为一组** 拼接后进行批量查询：
    `https://api.worldquantbrain.com/users/self/alphas?id=A1%1FA2%1FA3...&fields=...`
  * 该机制能够在不到 1 分钟的极短时间内（只需几百次请求即可处理 2.2 万因子），完全自动补齐所有存量因子的缺失静态指标，从而大幅度减轻后台巡检器的负载。

### 7.5 D 级因子过滤与前端按钮清除
* **后台 SQL 强过滤**：
  * 在 `app/main.py` 的 `/alphas` 路由中，对 `show_hidden != "1"` 的主查询中加入了 `AND a.alpha_type != 'D'`，使得凡是评级为 D（指标不达标的垃圾因子）的因子，在被后台线程物理退休前也绝不会出现在列表里。
* **前端筛选按钮移除**：
  * 在 `app/templates/alphas.html` 中，直接删除了快捷筛选栏的 `D级` 按钮切换，保证用户界面上没有对 D 级废弃垃圾因子的关注路径。



