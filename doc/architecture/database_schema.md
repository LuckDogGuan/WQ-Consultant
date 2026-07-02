# Database Schema 数据库设计说明

本系统使用 SQLite 本地数据库（通常保存在 `data/gui.db`），用以存储因子缓存、后台任务记录和同步日志。

---

## 核心数据表结构

### 1. `alpha_records` (因子数据表)
存储所有拉取或本地录入的因子元数据。
* **`alpha_id`**: 主键，如 `USA_TOP3000_c18_s158_t7_f120`。
* **`alpha_type`**: 评级档位，当前仅保留 `S`, `A`, `B`, `C` 级（D 级已废除并归入 C 级）。
* **`is_garbage`**: 标记位，若为 `1` 则表示该因子已由于低质量或重复而被判定为垃圾，在主列表隐藏。
* **`payload`**: JSON 文本，极其关键。存储了因子的全量回测包数据，其内 `recordsets_data` -> `pnl` 时序数组是进行本地自相关性计算的唯一数据源。

---

## 核心组件与代码映射

* **数据库表结构初始化定义**: 包含建表语句 `CREATE TABLE IF NOT EXISTS alpha_records...`。
  * 源码位置: [storage.py:L25](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/storage.py#L25)
* **因子记录的增量写入与更新 (Upsert)**: `upsert_alpha` 具体的 SQL 执行逻辑。
  * 源码位置: [storage.py:L95](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/storage.py#L95)
