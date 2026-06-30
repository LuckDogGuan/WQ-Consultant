# 回测任务参数配置记录

更新时间：2026-07-01

## 当前口径

- 回测页不再单独配置地区组合。
- 地区组合从“设置 -> 本地数据目录与系统维护”的本地 catalog 缓存读取，优先使用 `USA/ASI/EUR` 中已有缓存的地区；如果没有缓存，则回退到设置页当前 `region`。
- “地区槽位与线程”只保留一套 FO/SO/TH 配置，并应用到所有参与地区。
- 顾问等级使用表驱动配置：
  - `starter`：`fundamental`、`pv`
  - `gold`：`fundamental`、`pv`、`analyst`、`model`
  - `master`：全部 dataset
- 王哥严格版默认参数：
  - 自相关安全线 `0.68`，硬线 `0.70`
  - Prod Corr 优秀线 `0.50`，硬线 `0.70`
  - Turnover 提醒线 `0.10`，硬线 `0.15`
  - 算子数量上限 `8`
  - D 档默认本地隐藏，并进入远端隐藏/retire 流程

## 运行统计

回测页右侧统计卡读取 `/api/jobs/{job_id}/summary`，显示最近一个回测任务：

- 总产出因子数
- 通过因子数：`S/A/B` 或 `CHECKED_PASS`
- D 档隐藏数：`alpha_type = D` 或 `is_garbage = 1`
- 运行效率：因子数 / 任务运行分钟数

## 后续扩展点

- 新顾问等级只改 `ADVISOR_LEVEL_DATASET_PREFIXES`。
- 如果后续确实需要不同地区不同槽位，再恢复 `region_stage_config` 的地区级 UI；当前代码仍保留内部结构，但 UI 只写一套共享值。
