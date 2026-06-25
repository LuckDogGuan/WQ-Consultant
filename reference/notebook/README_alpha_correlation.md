# Alpha 相关性分析与分类脚本指南

`alpha_correlation_analyzer.py` 是一个用于自动分析 WorldQuant Brain 未提交因子（Unsubmitted Alphas），进行 0 误差本地相关性计算，并根据设定指标对其进行智能分类与自动改名的脚本。

## 1. 核心功能

- **数据同步**：自动通过 API 抓取当前所有的 OS（Out-of-Sample）阶段因子数据，缓存在本地 `data_catalog/correlation_data` 中，从而实现**本地 0 误差**的自相关性计算。
- **自动分类与重命名**：从平台获取满足基础条件的因子（Sharpe > 1.0），并在判定通过后利用 `set_alpha_properties` 自动进行重命名：
  - **PPA（Power Pool Alpha）**：`Sharpe > 1.0` 且 `PPA 相关性 < 0.5` ➡️ 改名为 `PPA_相关性` (例: `PPA_0.35`)
  - **ATOM**：`近两年 Sharpe > 2.38` 且 `Prod 相关性 < 0.7` ➡️ 改名为 `ATOM_相关性` (例: `ATOM_0.61`)
  - **RA（Regular Alpha）**：`Sharpe > 1.58`、`Prod 相关性 < 0.7` 且 `通过 IS Ladder 测试` ➡️ 改名为 `RA_相关性` (例: `RA_0.65`)
- **IS 失败自动过滤机制**：遇到平台反馈测试结果为 `IS_FAIL` 的因子将直接被过滤，**除非该因子 Sharpe > 2.0**，此时它仍会进入类别研判流程。

## 2. 运行方式

在命令行（推荐在项目根目录下）直接运行：

```bash
python notebooks/alpha_correlation_analyzer.py
```

执行后，脚本会自动：
1. 下载最新的 OS 数据至缓存目录。
2. 拉取账户下所有的合格 Unsubmitted 因子。
3. 在终端打出详细的分析判定日志。
4. 在满足条件的因子上调用改名接口。

## 3. 主要参数与修改说明

如需调整参数或判定逻辑，可以直接打开 `notebooks/alpha_correlation_analyzer.py` 并在 `process_unsubmitted_alphas` 函数中进行修改。

### 3.1 限制处理数量 (Limit)
脚本末尾调用了分析函数：
```python
process_unsubmitted_alphas(sess, limit=None)
```
- **`limit=None`**：处理账号下满足初步门槛的所有未提交因子。
- 如果只想做快速测试，可以改为 `limit=5` 等固定数值。

### 3.2 初始过滤门槛 (Sharpe / IS_FAIL)
在 `process_unsubmitted_alphas` 中，调用 `get_alphas_full` 时的初始参数：
```python
alphas_df = get_alphas_full(
    sharpe_th=1.0,  # 最初步门槛：获取 Sharpe 大于 1.0 的因子
    region="USA",   # 目前只检测 USA 市场
    ...
)
```

**IS_FAIL 的特殊情况**：
```python
if status == "IS_FAIL" and sharpe <= 2.0:
    continue
```
如果您希望即使 Sharpe 较小也不跳过 IS_FAIL，或是想修改这个 2.0 的阈值，直接在此处更改即可。

### 3.3 分类阈值逻辑 (Categorization)
如果您日后希望修改 PPA / ATOM / RA 的划分边界（比如把 RA 的相关性要求由 0.7 改为 0.6），直接修改下面的核心 `if / elif` 代码块即可：
```python
# PPA: sharpe > 1.0, ppa correlation < 0.5
if sharpe > 1.0 and ppa_corr < 0.5:
    alpha_type = "PPA"
    target_name = f"PPA_{ppa_corr:.2f}"

# ATOM: L2Y sharpe > 2.38, prod correlation < 0.7
elif l2y_sharpe > 2.38 and prod_corr < 0.7:
    alpha_type = "ATOM"
...
```

## 4. 依赖说明

- 运行该脚本需要依赖 `consultant_core` 中的接口（用于登录认证、拉取因子等）。
- 本地生成的数据将保存在当前项目根目录下的 `data_catalog/correlation_data`。如需强制全量重新拉取 OS 回测集，可以删除该文件夹下的 `.pickle` 文件。
