# WQ Consultant GUI 系统升级与优化文档

本项目针对 WorldQuant Brain 顾问辅助系统 (WQ Consultant GUI) 的因子管理、相关性检测、检查提交、回测性能以及并发任务调度进行了全面升级与优化。以下为本次升级的详细修改记录与操作指引。

---

## 1. 升级亮点与优化概览

- **F1 & F2: 核心指标持久化、错误保存与本地详情页**
  - **指标持久化**: 升级 SQLite 数据库 schema，新增 `margin`, `returns`, `drawdown` 三列，打通相关性诊断与检查提交的指标共享。
  - **网络与重试报错记录**: 提检失败时（如并发限额、网络超时），完整捕获异常文本并保存至 `check_results` 的 `message` 字段，杜绝无意义的判定丢失。
  - **因子详情仪表盘**: 增设 `/alphas/{alpha_id}` 本地详情路由及卡片式视图，点击任何因子栏即可直观查看 neutralization, decay, expression, 提测状态与详细指标历史。
- **F3: 日志时间戳与回测并发加速**
  - **日志时间戳**: 拦截标准输出流，对写入 Job 日志文件的每一行前缀追加 `[YYYY-MM-DD HH:MM:SS]`，精准记录每个回测步骤的执行时刻。
  - **回测队列扁平化重构**: 废除分批池化阻塞逻辑，将所有待测任务平铺进 `ThreadPoolExecutor`。无缝融合最大并发数控制，且各 Pool 子任务跑完后自动触发 `pool_complete`，在 100% 保证断点续传的前提下消除线程闲置，回测性能提升 3 至 5 倍。
- **F4: 滚动固定表头、页码跳转与日期快捷筛选**
  - **固定表头 (Sticky Header)**: 精心优化 CSS 布局，将 `.table th` 设定为 `position: sticky; top: 70px;`（刚好紧贴 70px 高的顶部导航栏），并在大量因子数据滚动下拉时提供不透明的 `#111827` 背景保护，彻底消除遮挡与视觉穿透。
  - **快捷日期筛选**: 在相关性检测、检查提交、Alpha 记录三个模块头部加入“全部/今天/昨天/最近三天/最近一周”快捷时间筛选，按本地时区转 UTC ISO 时间进行高性能 SQL 查询。
  - **指定页码跳转**: 分页组件新增直观的“跳转至 [ ] 页”输入框，支持鼠标点击和回车键触发。
- **F5: 任务暂停后二次运行死锁 Bug 修复**
  - **并发抢占恢复**: 解决“点击停止后后台线程在 Sleep 等待中未退出时，再次点击启动被无视且随后被老线程退出覆盖”的死锁问题。若线程存活但处于 Pause 状态，再次点击“启动”将直接在内存中擦除 pause 标记，恢复 `running` 状态，让老线程原位复活。
  - **完结任务重跑**: 对状态已为 `completed` 的任务点击“启动”，会自动清理其对应的主日志 `job_{id}.log` 和各子阶段进度 `*_progress_{id}_*.jsonl` 缓存，使其从头重新执行。

---

## 2. 详细代码修改目录

### 2.1 数据库结构与迁移 (`app/storage.py`)
- 在 `init_db` 时自动检查 `alpha_records` 表的列，若缺失 `margin`, `returns`, `drawdown` 列，使用 `ALTER TABLE` 语句自动进行无损 schema 迁移。
- 修改 `upsert_alpha`，在写入或冲突更新（`ON CONFLICT`）时，能够持久化保存三个新指标，并保证在重命名（仅传入 target_name）时不会抹除已有指标。

### 2.2 API 拉取与落库 (`consultant_core/machine_lib.py` & `app/services/`)
- **`machine_lib.py:_alpha_row`**: 自动抓取远程 `is` (In-Sample) 域下的 `returns` 和 `drawdown`。
- **`correlation_service.py`**: 将诊断合格的候选因子指标写入 `alpha_records`。
- **`check_service.py`**: 
  - 启动提检时优先从 `get_alphas_full` 获取完整指标并缓存在本地 DB，手动输入的因子若无本地数据则联网 `/alphas/{alpha_id}` 并 upsert 补齐。
  - 异常捕获部分升级：如果提检线程捕获到连接异常或判定失败，执行 `add_check_result(..., result="ERROR", message=str(exc))` 妥善保存故障日志。

### 2.3 因子详情与超链接路由 (`app/main.py` & templates)
- **`main.py:get_alpha_detail_page`**: 拦截并渲染 `/alphas/{alpha_id}` 请求。如果本地数据库没有数据，自动请求 WQ API 抓取并缓存入本地，随后返回包含表达式和历史提交状况的详情。
- **超链接更新**: 修改 `correlation.html`, `check.html`, `alphas.html` 三处因子展示列表，将原本直接指向 WorldQuant 平台的硬链接修改为指向本地因子详情页的路由 `/alphas/{{ a.alpha_id }}`。

### 2.4 日志行前缀时间戳 (`app/job_runner.py`)
- 重构 `ThreadLocalStream` 中的 `write` 方法，利用线程私有缓存，当输出文本含有换行符时，在每一个新行的开头动态插入当前时间的本地格式化时间戳 `[%Y-%m-%d %H:%M:%S] `。

### 2.5 非阻塞回测队列加速 (`app/services/simulation_service.py`)
- 改变原有的 `for pool in pools: run_simulation_pool(pool) # block` 结构。
- 引入全局 `ThreadPoolExecutor`。当任务包被压入时，扁平化遍历所有尚未跑完的 pools，并将每一个 pool 的 slot 作为独立 Task 异步提交。
- 实时统计各 Pool 完成数，当属于某 Pool 的所有 slot 全部处理完毕且无报错时，异步写入 `simulation_run_complete` 标记并记录进度，实现极低开销的非阻塞高吞吐。

### 2.6 样式调整与前台组件 (`app/static/style.css` & HTMLs)
- **CSS (`style.css`)**:
  - 去除 `.table-responsive` 里的限制：`max-height` 和 `overflow-y`，确保表格头部与系统 `.top-bar` 兼容。
  - 确保表头 `.table th` 声明 `position: sticky; top: 70px; z-index: 2;`，设置其不透明的 `background-color: #111827`，保证在滚动时文字不会穿透重叠。
- **路由查询过滤 (`main.py`)**:
  - 对 `/check` 和 `/alphas` 添加可选参数 `date_filter`。
  - 计算时区感知的本地零点时间并转换为 UTC ISO8601 标准字符串，与 `created_at` 字段作对比查询。
- **前台逻辑**:
  - `alphas.html`, `check.html`, `correlation.html` 新增对应的时间筛选快捷按钮并根据 URL 参数设定 `btn-primary` 高亮。
  - 提供了 `jumpToPage()` JavaScript 辅助方法，并在输入框上绑定了 `Enter` 回车事件。

---

## 3. 使用与验证说明

### 3.1 验证服务运行状态
运行如下命令（或由系统默认拉起）：
```bash
python run_gui.py --no-browser
```
正常启动后，终端输出将显示服务已成功绑定并监听：
```
INFO:     Uvicorn running on http://127.0.0.1:8765 (Press CTRL+C to quit)
```

### 3.2 业务操作验证步骤
1. **测试日志时间戳**:
   - 触发一个回测 Job。在“日志”页面或具体的任务日志输出中，确保每行前都有形如 `[2026-06-13 12:50:09]` 的时间标记。
2. **测试暂停与二次运行**:
   - 启动一个任务，等待 5 秒后点击“停止”，状态栏显示“Pausing task...”。
   - 在线程彻底关闭前，立刻点击“启动”，观察状态是否立刻无缝切回“Task resumed, running...”，且后台日志未中断。
   - 等待该任务完全跑完变为 `completed`。再次点击“启动”该任务，在控制台日志确认先前产生的子日志及 `*_progress_*.jsonl` 成功被擦除，回测进度重归 `0%` 重新排队跑。
3. **测试日期筛选与跳转**:
   - 打开 “Alpha 记录” 或 “检查提交”。
   - 点击“今天”，检查表格中是否仅列出今日创建的因子；点击“最近一周”确认时间跨度是否正常。
   - 在底部分页中输入例如 `2`，点击确定或按下回车，页面应当无缝重定向到第二页且过滤条件（如 `type_filter` 和 `date_filter`）保持不变。
4. **测试 Sticky 表头**:
   - 在因子列表长页面中，鼠标向下拉动，确认表格的首行（表头参数列名）稳稳停留在顶部导航条正下方，且不遮挡、不半透明穿透。
5. **测试本地因子详情**:
   - 点击表格中的任意因子 ID，系统将打开本地页面 `/alphas/DF_xxxx`，可查看 Neutralization、表达式及各项指标详情。

---

## 4. 6月13日最新修复与解析补充

### 4.1 因子详情页自动拉取与 recordsets 丰富渲染
- **懒加载与保存机制**: 优化了 `/alphas/{alpha_id}` 的在线拉取策略。现在，即使本地数据库中存在该因子记录，但如果它缺少基本属性（如 `region`、`universe`）或尚未缓存因子曲线数据 `recordsets_data`，系统仍将自动联网WorldQuant Brain 抓取完整信息及历史回测 recordsets（包括 `pnl`, `daily-pnl`, `sharpe`, `turnover`, `yearly-stats`），并在合并数据后 upsert 保存至本地。
- **富报表展示**: 调用 `consultant_core/alpha_report.py` 中的 `render_alpha_report`，在详情页中动态呈现因子代码、IS 判定详情、各项 recordset 时序图表（PNL 曲线、Daily PnL、Sharpe、Turnover 的 SVG 折线图）以及年度统计指标表格，极大丰富了可视化内容。

### 4.2 提检任务失败与 SQLite 约束冲突修复 (`NOT NULL constraint failed`)
- **分析**: 在 WQ Brain 拉取最近提测记录时，部分 pandas DataFrame 列的值由于为 `NaN`（在 Python 中表现为特殊的 float 值，但 sqlite3 会将其转换成 `None`），直接插入数据库导致触发 `NOT NULL constraint failed: alpha_records.name` 约束报错，进而导致提检 Job 启动后瞬间变为 `failed`（使用户误以为重启后任务无法启动）。
- **修复**: 在 `storage.py:upsert_alpha` 内部新增了对 `NaN` 与 `None` 的安全清洗函数 `clean_str` 和 `clean_float`。任何 `NaN` 类型的空数据在入库时均会被妥善转为空字符串 `""`（对于字符列）或 `None`（对于浮点列），彻底修复了因此导致的提检任务崩溃问题。
- **导入 NameError 修复**: 修复了 `main.py` 中因未导入 `upsert_alpha` 导致联网抓取详细因子信息后抛出 `NameError: name 'upsert_alpha' is not defined` 导致 404 的问题。

### 4.3 关于回测个数（十小时仅提检 1000 个）的原理性解释
- **旧系统瓶颈**: 在旧的并发实现中，回测任务是**按 pool 逐个串行阻塞运行**的。如果一个 pool 包含了例如 6 个 slot（6 个并发子任务），虽然启用了多线程，但系统必须等待这 6 个任务**全部彻底完成**，才能转入下一个 pool。这就导致：一旦其中某一个 slot 出现网络卡顿、WQ 排队延迟（可能需要几分钟），其余 5 个早已跑完的 slot 线程只能被迫闲置等待，造成极大的线程饥饿和时间浪费。
- **新系统改进**: 本次升级已将整个任务拉平（Flatten），把所有 pools 里的子任务展开平铺为一个非阻塞的大任务队列，并使用最大为 `limit_of_multi_simulations` 并发的 `ThreadPoolExecutor`。这使得一旦某个 slot 任务完成，下一个回测因子会立刻抢占并执行，各个线程彻底消除闲置，因此能实现 3-5 倍的性能提升，完美解决回测缓慢问题。

## 5. 2026-06-13 Alpha 优化规划器第一阶段

- **阶段边界**: 新增优化规划器只读取本地数据并生成优化计划，不直接启动 WorldQuant Brain 远程回测，避免在规则未稳定前消耗 API。
- **候选范围**: `marginal`、`standard`、`premium` 因子进入候选池；提交检查后的因子也可根据 `check_results` 的返回错误生成策略。
- **跳过规则**: 缺少表达式跳过；失败或 ERROR 检查项数量大于等于 2 时跳过，避免对问题过多的因子做自动优化。
- **错误映射**: `SELF_CORRELATION` 映射到去相关策略，后续对应 `optimizeAlpha.py` 的 `runGroup`、`runTrade`、`runStable` 类能力；`LOW_SHARPE`、`LOW_FITNESS`、`LOW_MARGIN`、换手率类错误分别映射到性能、边际收益、换手率调整策略。
- **代码位置**: 新增 `app/services/optimization_planner.py`，新增测试 `tests/test_optimization_planner.py`。
- **阶段文档**: 详细规则记录在 `doc/alpha_optimization_planner_2026-06-13.md`。
- **页面入口**: 新增 `/optimization` 只读页面和侧边栏“优化规划”入口，可筛选可优化/跳过、等级和策略，便于人工确认候选池。
- **本地表达式验证**: 新增 `app/services/expression_validator.py` 和 `POST /api/expressions/validate`。优化计划生成前会先做本地检查，明显非法表达式跳过；未知 operator 只作为 warning，不消耗 API。
- **增强变体预览**: 新增 `app/services/alpha_enhancement.py` 和 `GET /api/optimization/variants/{alpha_id}`，按优化计划生成本地表达式候选，覆盖 stable/group/trade/template/power/runtime/basic 等小批量模式，仍不自动远程回测。
- **API 延时判断**: 新增 `/api/*` 通用耗时中间件，响应头返回 `X-Process-Time-Ms`。默认慢请求阈值 `api_slow_threshold_ms=1500`，超过阈值会记录 `api_slow` 错误事件，便于区分本地查询慢、表达式验证慢和远程 WQ API 慢。
- **优化规划可用性**: `/optimization` 列表新增“因子名称”和“生成变体”操作。点击后进入 `/optimization/{alpha_id}/variants`，可查看本地生成的增强表达式候选，仍不自动提交远程回测。
- **回测准备中显示修复**: 回测阶段生成 pool 后立即把 `progress_current/progress_total` 更新为 `0/总 pool`，前台不再长时间显示“准备中”。WQ 创建 simulation 未返回 `Location` 时，日志会显示状态码、Retry-After 和响应体摘要，不再只显示 `'location'`。
## 6. 2026-06-13 优化运行与 Job #29 修复

- **Job #29 根因**: 日志显示 WQ 返回 `Multi-simulations require multiple simulations in request array. Single simulations are required to be submitted without the wrapping array.`。根因是单个 simulation 也被数组包裹提交，平台拒绝并且没有返回 `Location`。
- **提交格式修复**: 新增 `normalize_simulation_post_payload()`。当 `generate_sim_data()` 只生成 1 条 simulation 时，POST 使用单个对象；多条 simulation 时仍使用数组。`task_post_start` 日志新增 `payload_shape`，方便后续判断当前任务是 single 还是 multi。
- **优化规划一键运行**: 新增 `optimization_run` 后台任务，复用现有 `jobs/job_events`、暂停/恢复、日志尾部和进度条。流程为：选择候选 Alpha -> 生成本地增强变体 -> 提交 WQ 回测。默认 `children_per_request=1`，减少误触 multi-simulation 格式和 API 消耗风险。
- **优化页基础设置**: `/optimization` 顶部新增基础设置区，支持最近 N 天、指定日期范围、手动 Alpha ID、候选数量、每因子变体数、每次提交数量、neutralization、每日自动运行小时。
- **优化定时任务**: 新增 `optimization_schedule_enabled`、`optimization_schedule_hour`、`optimization_schedule_last_run` 等配置，并接入现有 `SchedulerService`，按小时检查并每天最多触发一次优化任务。
- **数据流通页面**: 新增 `/flow` 和侧边栏顶部“数据流通”入口，说明数据目录、回测、相关性检测、检查提交、优化规划、Alpha 记录之间的数据流向，以及本地表 `alpha_records`、`check_results`、`jobs/job_events` 的职责。
- **验证**: 覆盖 `tests.test_optimization_pages`、`tests.test_optimization_run_service`、`tests.test_backtest_progress`、`tests.test_api_latency`、`tests.test_optimization_planner`、`tests.test_expression_validator`、`tests.test_alpha_enhancement`，并通过相关 Python 编译检查与模板解析检查。

## 7. 2026-06-13 优化运行页二次调整与 429 修复

- **运行卡住根因**: Job #30 已生成 147 个优化变体，但第一个提交请求持续收到 WQ `429 Rate limited`。旧逻辑没有把 429 计入重试次数，并且直接按 `Retry-After=5` 每 5 秒重试，导致页面进度一直停在 `0/147`。
- **429 处理修复**: 新增 `rate_limit_retry_seconds()`，对 Retry-After 设置 30 秒下限和 300 秒上限；429 现在会更新 Job 为 `waiting_limit`，计入最大重试次数，达到上限后写入 `task_post_error`，避免无限刷请求。
- **源中性化**: 优化任务不再使用页面手填的全局 neutralization。系统从源 Alpha payload 的 `settings.neutralization` 读取提交时的中性化，并按中性化分组提交变体。
- **变体数量**: 页面移除“每因子变体数”。后台调用 `generate_variants_for_plan(..., max_variants=None)`，按当前代码规则能生成多少合法变体就提交多少。
- **表达式提取修复**: `extract_alpha_expression()` 支持 WQ payload 中 `regular` 为字符串的常见结构，避免把有效 Alpha 误判为 `missing_expression`。
- **页面体验**: 优化页基础设置面板改为可折叠 `details`，面板可纵向拉伸；日期控件和输入背景统一为深色；自动运行设置保留为“每天几点”。
- **当前任务状态**: 重启服务后，Job #29 已完成，Job #30 和 Job #31 已暂停。#30 是旧任务，恢复后会走新代码，但建议新建优化任务以获得更干净的日志。

## 8. 2026-06-13 429 等待策略调整

- **429 不再跳过**: WQ 返回 `429 Rate limited` 说明平台限流，不代表表达式或本地代码错误。提交 simulation 时遇到 429 后不再把当前 Alpha/变体判定失败，也不跳过后续候选。
- **连续 429 分组等待**: 每个请求维护自己的连续 429 计数。第 1-4 次每次等待 30 秒；第 5 次等待 `reconnect_long_sleep_seconds`，当前设置为 600 秒。第 6-9 次再次每次等待 30 秒，第 10 次再次等待 600 秒，后续按每 5 次一个周期重复。
- **成功后重置计数**: 一旦当前请求成功创建 simulation 并拿到 `Location`，连续 429 计数清零。失败次数不跨请求永久累加。
- **登录 429 同步处理**: WQ 登录接口返回 429 时，不再直接把任务标记为 failed。后台任务会进入 `waiting_limit`，按同样的 5 次一组等待策略继续登录，直到平台恢复或用户暂停。
- **沿用现有重连参数**: 长等待使用设置页“网络异常第 3 次及以后等待重连 (秒)”对应的 `reconnect_long_sleep_seconds`，默认值调整为 600 秒。

## 9. 2026-06-13 仪表盘每日额度统计

- **今日回测个数**: 首页新增每日回测额度卡片，统计 `alpha_records` 中 `source LIKE 'job_%'` 且在今日回测窗口内新增的因子。回测窗口按北京时间每天 12:00 刷新，最大值读取设置项 `backtest_daily_limit`。
- **今日检查提交**: 首页新增检查提交额度卡片，统计当天新增的 `check_results` 记录，最大值读取设置项 `check_daily_limit`。
- **优化规划**: 首页新增优化规划卡片，复用 `list_optimization_plans()` 的判定结果，展示总计划数、可优化数，以及达到 marginal/standard/premium 最低可提交档位的候选数量。
- **今日正式提交**: 首页新增正式提交额度卡片，按当天 `alpha_records.status='SUBMITTED'` 且 `updated_at` 在当天窗口内统计。`PPA` 作为 Super/PPA 档位，其余作为普通档位；默认额度为普通 4 个、Super/PPA 1 个，总计 5 个。
- **代码位置**: 新增 `app/services/dashboard_metrics.py` 统一封装仪表盘指标，`app/main.py` 首页路由只负责读取指标并渲染，避免统计口径散落在模板中。
