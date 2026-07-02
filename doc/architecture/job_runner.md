# Job Runner 任务调度机制

为规避同步请求引发的 HTTP 连接阻塞与前端超时，本系统设计了一套基于 SQLite 的轻量级异步任务调度队列。

---

## 异步工作流机制

1. **创建任务**: 当用户点击前端的“获取服务器因子”或“刷新自相关性”按钮时，后端会先通过 `create_job` 接口将任务元数据（类型、入参、排队状态）写入 SQLite 的 `jobs` 表。
2. **触发运行**: 调用 `JobRunner().start_job(job_id, kind, params)` 开启后台 Worker 线程或子进程执行。
3. **状态追溯与中断**: 任务在运行中会调用 `update_job` 写入当前进度（如 50%）与工作日志事件，并在关键步骤循环中调用 `check_paused` 实现任务挂起或终止检测。

---

## 核心组件与代码映射

* **任务生命周期与分发核心**: `JobRunner` 中的 `_run_job_worker` 根据 `kind` 参数动态分发具体的业务脚本逻辑（如调用 `run_get_server_alphas_job`）。
  * 源码位置: [job_runner.py:L223](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/job_runner.py#L223)
* **任务进度与事件状态持久化**: 实现将进度百分比、错误日志等写入 `jobs` 和 `job_events` 表。
  * 源码位置: [storage.py:L311](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/storage.py#L311)
* **增量状态追溯与日志添加**: 
  * `add_job_event` 接口源码: [storage.py:L360](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/storage.py#L360)
