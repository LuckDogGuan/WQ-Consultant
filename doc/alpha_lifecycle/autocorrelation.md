# Autocorrelation Local Check 自相关计算限额机制

自相关性是指因子本身时序收益率与本地已有已回测因子的时序收益率进行对比后得出的 Pearson 线性相关度。此步骤耗时极长，对服务器请求频次与网络带宽消耗巨大。

---

## S 级因子限额计算规则

为了避免大规模无效的 PnL 下载与相关性比对开销，系统采取了以下限额机制：
1. **仅 S 级因子触发 PnL 拉取**: 在增量“获取服务器因子”或手动发起“刷新自相关性”时，系统只筛选出定级为 **S 级** 的因子。
2. **下载与缓存**: 登录官方平台，下载最新的 OS/PPA 核心因子收益率矩阵库，随后单独发起该 S 级因子的 PnL 数据下载。
3. **计算 Pearson 自相关**: 在本地内存中，将该 S 级因子的时序收益率与收益率库做线性 Pearson 矩阵关联度比对，从而生成 `prod_corr` 和 `ppa_corr`。
4. **非 S 级因子直接跳过**: A、B、C 等级的因子不下载 PnL，不计算 Pearson 相关度，直接保存。

---

## 核心组件与代码映射

* **自相关 Pearson 计算函数**: `_run_autocorrelation` 在本地缓存并比对收益率矩阵。
  * 源码位置: [background_inspector.py:L460](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/background_inspector.py#L460)
* **获取因子任务中的 S 级自相关限额调用**:
  * 源码位置: [sync_service.py:L283](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/sync_service.py#L283)
* **手动刷新自相关任务中的 S 级自相关调用**: `run_refresh_correlation_job` 对本地 S 级因子进行扫表刷新。
  * 源码位置: [sync_service.py:L511](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/sync_service.py#L511)
