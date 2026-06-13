# 2026-06-13 架构调整记录

## 目标

本次调整围绕四个问题：Alpha 优化任务遇到 WQ 429/断连后长时间无产出、submitted Alpha 继续出现在本地候选池、页面手机端可用性不足、旧任务参数在版本升级后容易缺字段。

## Module 调整

### 1. WQ 远端等待策略

- 新增 `app/services/wq_retry_policy.py`。
- 429 使用 “4 次短等 + 第 5 次长等” 循环。
- 网络断开、连接中止、超时使用设置页重连参数：第 1~2 次短等，第 3 次及以后长等。
- `simulation_service.py` 的 POST 阶段遇到网络异常时，不再计入 3 次提交失败并跳过当前变体；会等待、重登、继续提交同一个变体。
- 成功拿到 `Location` 后重置失败计数。

### 2. submitted Alpha 本地维护

- 新增 `app/services/maintenance_service.py`。
- 新增 `submitted_cleanup` job 类型。
- `SchedulerService` 默认每天 0 点触发一次。
- 拉取平台 submitted/OS Alpha 后，将本地对应 `alpha_records` 标记为 `SUBMITTED`，并删除其 `check_results`，避免继续进入相关性检查、检查提交和优化规划候选。
- `alpha_records` 以 `alpha_id` 为主键，本身不会重复；`check_results` 每个 Alpha 只保留最新一条，旧记录在维护任务中删除。

### 3. 任务参数兼容

- 新增 `app/services/job_params.py`。
- 优化任务参数统一归一化到 `schema_version=2`。
- 旧 job 缺少字段时自动补齐默认值：
  - `source_mode=recent`
  - `recent_days=14`
  - `candidate_limit=20`
  - `children_per_request=1`
- 页面新建任务、定时任务、后台执行入口都复用同一个归一化 Interface。

### 4. 手机端适配

- `app/static/style.css` 增加窄屏规则。
- 手机端侧边栏改为横向顶部导航。
- 筛选栏、按钮组、优化操作区纵向堆叠。
- 表格使用受控横向滚动，避免挤压导致重叠。
- 弹窗、优化设置面板、Toast 适配窄屏。

## 验证

已新增并运行：

```bash
python -m unittest tests.test_wq_retry_policy tests.test_maintenance_service tests.test_job_params
```

已进行编译检查：

```bash
python -m py_compile app\services\wq_retry_policy.py app\services\maintenance_service.py app\services\job_params.py app\services\simulation_service.py app\services\optimization_run_service.py app\services\scheduler_service.py app\job_runner.py app\main.py app\storage.py
```

## 2026-06-13 UI 细节修正

- 检查提交、相关性检查、优化规划列表取消内部纵向滚轮，列表跟随页面滚动，只保留必要的横向滚动。
- 检查提交和优化规划的每页展示数量从 12 条调整为 11 条。
- 优化规划设置区调整为接近相关性检查设置区的折叠卡片视觉样式，减少嵌套面板背景差异。
- 优化规划任务详情兼容全局任务详情脚本，日志和事件都能输出；事件时间改为显示完整 `created_at`。
- 静态资源版本更新为 `20260613_ui2`，避免浏览器继续使用旧 CSS/JS 缓存。
