# WorldQuant Brain API 频控 429 与网络断开排查报告 (Rate Limiting & Network Disconnect Analysis)

本报告针对后台巡检与前端优化并发任务导致的「网络连接已断开 (10分钟重连中...)」以及 WQ 官方 API 返回 `429 (Too Many Requests)` 限制事件进行了深度分析，并梳理了系统的自动重连机制。

---

## 1. 核心日志分析与场景复现

通过分析本地 `logs/gui.log` 日志发现，在断开事件前后，系统存在如下行为特征：

```
166810: 2026-07-01 13:01:20,129 - INFO - [BackgroundInspector] Downloading correlation data & PnL for KPLPAGwj...
166811: 2026-07-01 13:01:21,754 - INFO - [BackgroundInspector] Alpha KPLPAGwj re-graded to C (prod_corr=0.9874, ppa_corr=0.9874)
166812: 2026-07-01 13:01:21,775 - INFO - [BackgroundInspector] Downloading correlation data & PnL for le0ew0R7...
166813: 2026-07-01 13:01:22,877 - INFO - Rate limited by WQ (429). Waiting 30s before retry; consecutive 429 count 3.
...
166856: 2026-07-01 13:01:53,082 - INFO - [BackgroundInspector] Downloading correlation data & PnL for 78w05Mr1...
166857: 2026-07-01 13:01:54,406 - INFO - Rate limited by WQ (429). Waiting 30s before retry; consecutive 429 count 4.
...
166896: 2026-07-01 13:02:24,403 - INFO - [BackgroundInspector] Downloading correlation data & PnL for A1wYp7xR...
166897: 2026-07-01 13:02:25,899 - INFO - Rate limited by WQ (429). Waiting 600s before retry; consecutive 429 count 5.
```

### 1.1 原因定位
1.  **突发的高频 GET 请求**：
    后台巡检任务 (`alpha_inspection` / `run_alpha_inspection_job`) 在同步/校验因子时，会顺序对大量因子发起 `GET /alphas/{alpha_id}/recordsets/pnl` 接口调用以拉取 PnL 数据。
2.  **串行零延迟的冲击**：
    由于原代码的循环中没有任何请求间隔延迟（Pacing），系统会以每 1~1.5 秒一次的速度密集轰炸官方 API。
3.  **多任务并发叠加**：
    当用户同时在前端工作台启动「优化运行任务（含有多路 Slot 并发回测与状态轮询）」和「同步/巡检任务」时，同一个出口公网 IP 的并发连接数超过了官方防火墙的安全阈值，触发了官方的 429 (Too Many Requests) 限流。

---

## 2. 自动退避与 10 分钟重连机制

当遭遇 429 报错时，系统设计了「指数级自适应退避与重试机制（由 `wq_retry_policy.py` 中的 `next_wait_seconds` 驱动）」：

*   **前 4 次失败**：系统将任务标记为 `waiting_limit`（等待频控），每次静默等待 **30 秒** 后尝试自动恢复。
*   **第 5 次连续失败**：表明 WQ 平台已对该客户端 IP 执行了中长期的拦截封锁。为避免过度请求被直接拉黑 IP，系统会启动冷却机制，强制进入 **600 秒（10分钟）** 的长休眠等待（界面状态显示为 `网络连接已断开 (10分钟重连中...)`）。
*   **指数衰退设计**：休眠过程中，本地网络监视器 (`NetworkMonitor`) 会降频为 **1分钟一次**（连续失败 5 次以上降为 **5分钟一次**）进行轻量探活。一旦 WQ 探活成功，重置失败计数，并将之前挂起的任务自动拉起并恢复。

---

## 3. 本次代码层面的防范优化

为彻底杜绝大批量同步及巡检任务因无延迟运行而造成 429 被阻断的问题，我们实施了如下优化：

1.  **大循环引入强制 Pacing 延迟**：
    *   在 `sync_service.py` 的手动巡检 `run_alpha_inspection_job` 与本地同步 `run_sync_local_alphas_job` 循环体内均新增了 **`time.sleep(1.0)`** 强制防频控延迟。
    *   在 `background_inspector.py` 执行批量退休 Grade C 垃圾因子循环中，将 sleep 间隔从 `0.1s` 调大至 **`0.8s`**，确保官方服务端有充足的连接重置缓冲。
2.  **双层节流缓冲**：
    *   通过将自相关参考库缓存于 `correlation_cache` 内存中（前述优化），将每个因子计算自相关的网络 API 依赖数降到了物理最低，配合强制 Pacing 延迟，让后台巡检流量趋于平缓。
