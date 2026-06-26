# [Python Alpha 速查] Python Alpha 实战全景：256 个包、API 工程、三类探索方向经验分享

- **链接**: [Commented] [Python Alpha 速查] Python Alpha 实战全景256 个包API 工程三类探索方向经验分享.md
- **作者**: YZ64617
- **发布时间/热度**: 28天前, 得票: 22

## 帖子正文

## 写在前面

最近把 Python Alpha 通道认真摸了一遍，写了三版 alpha（baseline → optimized → Hurst 体制版）跑通了远程仿真，并把 BrainLabs Jupyter 的环境完整盘了一次。这帖子是把 **已经验证过的事实** 和 **还在估算阶段的经验** 分开说清楚——能跑通的给代码锚点，不能确定的标注"社区估算"，方便大家少踩坑。

> ⚠️  **数据范围声明** ：
> - **包清单** ：2026-05-26 在 BrainLabs Jupyter Notebook 用  `%pip list`  实测扫描所得，下面的版本号都是真实输出
> - **API 仿真行为** ：基于 2026-05 在远程仿真提交 Python alpha 的实际经验（含成功记录与文档）
> - **资源数值** ：simulation 沙箱内存上限官方未公开，文中所有 MB/GB 数字均为 **社区估算** ，不同账号/区域/universe 可能差异显著

## 一、环境总览（实测扫描）

`%pip list`  输出 256 个包，挑出与量化研究强相关的分类如下：

分类
数量
代表包

科学计算
6
numpy 1.24.2 / scipy 1.10.1 / pandas 1.5.3 /  **polars 0.19.12**  / sympy 1.14.0 / pyarrow 23.0.1

机器学习
4
scikit-learn 1.2.1 /  **lightgbm 3.3.5**  / xgboost 1.7.1 / catboost 1.0.5

深度学习
4

 **torch 2.0.1+cu117**  / tensorflow 2.11.1 / keras 2.11.0 / jax 0.4.5

统计建模
4

 **statsmodels 0.13.5**  / prophet 1.1.3 / cmdstanpy 1.3.0 / patsy 1.0.2

NLP
5
transformers 4.30.1 / spacy 3.5.2 / tokenizers 0.15.2 / nltk 3.0.1 / huggingface_hub 0.36.2

优化求解
2

 **Mosek 9.3.22**  / qdldl

数据处理
6
dask 2023.4.1 / h5py 3.16.0 / fsspec / joblib / networkx 3.4.2 / swifter

可视化
4
matplotlib 3.10.8 / seaborn 0.13.2 / plotly 6.7.0 / dash 4.1.0

GPU 加速
11
CUDA 11.7 全套（cublas / cudnn / cufft / nccl …）

**结论** ：BrainLabs 给的是一套相当完整的研究环境。值得专门提一下的是  **Mosek 9.3.22** ——商业版凸优化求解器，单独购买授权年费可观，平台直接内置可用。

> ⚠️  **关键差异** ：BrainLabs Jupyter ≠ 远程仿真沙箱
> - Notebook：完整 Python 环境 + GPU 可用 + 内存充裕
> - Simulation：CPU 单机、无 GPU、内存受限、有超时限制（具体上限官方未明示）
> 也就是说："Notebook 里能跑"和"submit 后能 PASS"是两回事，下面的分级就是为了划这条线。

## 二、按 Simulation 实战重新分级

### ⭐⭐⭐⭐⭐ 一线主力（资源开销小，远程仿真稳定可用）

包
主要用途
备注

 **numpy 1.24.2** 
一切的基础
推荐统一  `dtype=np.float32` ，输出向量必须  `astype(np.float32)` 

 **scipy 1.10.1** 
数值/统计/信号

 `scipy.stats.rankdata`  /  `scipy.signal.hilbert`  /  `scipy.signal.butter`  等是写自定义算子的弹药库

 **statsmodels 0.13.5** 
计量经济
ADF 单位根、Engle-Granger 协整、ARIMA、GARCH——FastExpr 没有等价算子

 **scikit-learn 1.2.1** 
通用 ML

 **已实测可用** ：本人提交记录中用  `sklearn.decomposition.PCA`  跑通 PCA 残差反转 alpha（见第四章案例）

 **polars 0.19.12** 
高速 DataFrame
比 pandas 在 rolling 类操作上更省内存，可作 pandas 替代

### ⭐⭐⭐⭐ 重要工具（用得对就是壁垒，需注意资源管理）

包
用途
注意点

 **lightgbm 3.3.5** 
梯度提升树
远程仿真单机，务必  `n_jobs=1` ；树数量、深度建议保守

 **xgboost 1.7.1** 
梯度提升树
与 LightGBM 互补，模型集成时备用

 **Mosek 9.3.22** 
凸优化求解
可实现马科维茨 MVO 等组合优化；规模大（N>500）时建议先做宇宙预筛

 **torch 2.0.1** 
深度学习推理

 **重要** ：远程仿真无 GPU，只能在 Notebook 离线训练 → 权重存  `store`  → alpha 内  `torch.no_grad()`  推理

### ⭐⭐⭐ 战术工具（特定场景使用）

包
适用场景
备注

 **catboost 1.0.5** 
含类别特征（行业/国家）
训练慢于 LightGBM

 **jax 0.4.5** 
自动微分、超参数优化
grad/jit 有冷启动开销

 **networkx 3.4.2** 
相关性网络中心性
内存随 N² 增长，大 universe 建议先筛

 **prophet 1.1.3** 
季节性/趋势分解

 `fit`  开销较大，仅适合月度低频 alpha

 **sympy 1.14.0** 
离线符号推导
数值求解慢， **alpha 内不建议在线调用**

### ⭐⭐ 不推荐在 alpha 内直接使用

包
原因

 **transformers 4.30.1** 
模型权重大、加载耗时长，正确姿势是离线编码后存 dataset

 **spacy / nltk** 
NLP 模型加载开销大，alpha 内通常无文本数据可用

 **plotly / dash / seaborn / matplotlib** 
可视化只在 Notebook 用，alpha 必须返回  `float32`  数组

 **cmdstanpy 1.3.0** 
Stan 模型首次编译耗时较长

 **dask 2023.4.1** 
远程仿真单进程，并行收益有限

## 三、Simulation 真实可用性的三条铁证

为避免空谈，下面三条都是已经验证过的，可以直接当作"远程仿真支持 Python + 第三方包"的证据。

### 证据 1：API 提交格式（含 sklearn 跑通记录）

实际向  `POST https://api.worldquantbrain.com/simulations`  提交的 payload 关键字段：

```
{
  "type": "REGULAR",
  "settings": {
    "language": "PYTHON",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "lookback": 21,
    "decay": 6,
    "neutralization": "SUBINDUSTRY",
    "truncation": 0.1,
    "pasteurization": "ON",
    "testPeriod": "P1Y"
  },
  "regular": "from brain.alphas import alpha\nfrom sklearn.decomposition import PCA\n..."
}

```

提交后服务端返回  `Location: https://api.worldquantbrain.com/simulations/{simulation_id}` ，alpha 体使用了  `sklearn.decomposition.PCA` ，远程仿真接受。

**结论** ： `language=PYTHON`  通道存在， `from sklearn.* import`  在远程仿真中可用。

### 证据 2：三个跑通的 alpha 案例（公开代码模板）

同步开放三份在远程仿真中实际提交并跑通的 alpha，覆盖从基础到进阶的演进路径：

版本
核心思路
关键技术

 **baseline** 
1:1 复现 FASTEXPR  `trade_when(volume>ts_mean(20), signed_power(ts_rank(IV短/IV长, 60), 0.15), -1)` 

 `_ts_rank_last`  内联实现 +  `store.prev_signal` （ `dims="i"` ）实现 trade_when hold 语义

 **optimized** 
在 baseline 上做 5 处稳健性改进
rank 中心化、MAD winsorize、20/60/120 多窗口集成、sigmoid 量门控、EMA 信号平滑

 **hurst** 
增加体制识别
向量化 R/S Hurst（lags=2,4,8,16,32）+ 体制连续门控 + Hurst 跨日 EMA 平滑

三份代码合计约 350 行，核心模式：

```
@alpha(
    data=["volume", "atm_call_volatility_120d_short_term",
          "atm_call_volatility_720d_long_term_2"],
    store=[{"name": "prev_signal", "dims": "i", "extend": np.float64(np.nan)}],
)
def my_alpha(data, store) -> npt.NDArray[np.float32]:
    # ... 计算逻辑 ...
    return out.astype(np.float32)

```

### 证据 3：API 轮询时序与终态错误处理（HAR 实测）

提交 alpha 后，服务端返回  `Location`  头给一个 simulation 资源 URL，客户端需要 **轮询 GET 该 URL**  获取进度，直到出现终态。下面所有数据来自浏览器 HAR 抓包实测。

#### 3.1 三种终态对照表

状态
message 字段
settings
regular
alpha 字段
含义

 `COMPLETE` 
无
✅
✅
✅ alphaId
成功，可拿业绩数据

 `ERROR` 
✅ 有可读信息
❌
❌
❌
业务规则失败（如 resume 冲突、settings 非法）

 `FAIL` 
❌
❌
❌
❌
平台错误或用户代码异常（ **哑失败** ，无消息）

> **HAR 实测错误信息样本** ：
> - `"Inconsistent result resuming simulation from alpha store"`  —— alpha 缓存不一致

#### 3.2 轮询时序观测（HAR 实测六例）

Simulation ID
轮询次数
终态
估算耗时 (5s/次)

 `1reNloada5kca0BprmseeXv` 
19
COMPLETE
~95s

 `2QKOqT4Yr5b79oBedTJtRil` 
29
ERROR
~145s

 `4BAPXo9G95eic7OiHWbDFGg` 
38
COMPLETE
~190s

 `1F82sl4ew55WcCGsaaR8fRn` 
14
FAIL
~70s

 `LUDiz4HU4C19oznP0Okx9P` 
14
FAIL
~70s

 `3VabmBbBv4Sv9QfpyrwBRdA` 
16
COMPLETE
~80s

**经验值** ：单次 alpha 提交至终态通常需 70-200 秒；FAIL 哑失败通常较快（≈70s 内完成）。

#### 3.3 progress 字段推进规律

1. **第 1 次** ： `progress=0.1`
2. **第 2-3 次** ： `progress=0.15`
3. **第 3-4 次起** ：跳到  `progress=0.35`  后 **长时间不动** （实际计算阶段）
4. **终态** ： `progress`  字段消失，出现  `status`  字段（ `COMPLETE`  /  `ERROR`  /  `FAIL`  之一）

> 💡  **客户端实现要点** ：
> - 不要用  `progress`  做超时判断——它在 0.35 会卡很久，但 simulation 仍在正常计算
> - **以  `status`  字段是否出现作为终止条件** ，建议轮询间隔 5s、最大轮询 60 次（5 分钟超时）
> - 收到  `FAIL`  时 **没有 message 可读** ，只能凭 simulation ID 复现或重提，建议在客户端记录请求 payload 用于回溯

## 四、Python Alpha 的三类创新方向

### 方向 A：复现 FASTEXPR 算子

入门必修。FastExpr 一行  `ts_rank(x, 252)`  在 Python 里要内联实现：

```
def _ts_rank_last(window):
    """ts_rank(x, d) 等价：当前值在过去 d 天的百分位 [0, 1]"""
    today = window[-1]
    valid = ~np.isnan(window)
    n_valid = valid.sum(axis=0).astype(np.float64)
    less = ((window < today[None, :]) & valid).sum(axis=0).astype(np.float64)
    out = np.full_like(today, np.nan, dtype=np.float64)
    mask = (n_valid > 1) & (~np.isnan(today))
    out[mask] = less[mask] / (n_valid[mask] - 1.0)
    return out

```

**注意** ：远程仿真不识别外部模块，自定义算子需用  `inspect.getsource()`  或直接复制粘贴的方式 **内联到 alpha 文件内** 。社区已经沉淀了 44 个 TA-Lib 风格的扩展算子（op_ema / op_rsi / op_bollinger / op_atr / op_hurst …），需要时自取并内联。

### 方向 B：FastExpr 做不到的算子（差异化壁垒）

算子
依赖包
金融含义

 **Hurst 指数** 
numpy（向量化 R/S 简化）
H<0.5 均值回归；H>0.5 动量持续 → 自适应策略选择

 **协整对冲** 
 `statsmodels.tsa.stattools.coint` 
Engle-Granger 协整 → 统计套利

 **滚动 PCA 残差** 

 `sklearn.decomposition.PCA`  或  `numpy.linalg.svd` 

自动剔除系统性风险，输出特异收益

 **Kalman 平滑** 
scipy 或手写
比 ts_decay_linear 对结构性变化响应更快

 **路径依赖类** 
numpy + store
连涨/最大回撤/regime 状态——无状态的 FastExpr 做不到

### 方向 C：ML/DL 因子

#### LightGBM 滚动训练（推荐主力）

```
import lightgbm as lgb

model = lgb.LGBMRegressor(
    n_estimators=30,        # 保守起步
    max_depth=3,
    num_leaves=8,
    min_child_samples=20,
    n_jobs=1,               # 远程仿真单进程，必须 1
    verbose=-1,
)

```

#### Tiny Autoencoder（PyTorch 离线训 + 在线推理）

正确范式：BrainLabs 离线训练 → 权重存  `store`  → alpha 内  `torch.no_grad()`  前向；进阶可用纯 numpy 复刻 forward 节省框架开销。

#### 大模型端到端（Transformer/LSTM）

不推荐。远程仿真无 GPU，CPU 推理时间预算紧张。建议在 Notebook 离线训练 → 预测值上传成 dataset → alpha 内查表使用。

## 五、Simulation 常见问题 Checklist

下表是社区与个人实战中累计的高频问题， **资源数值为社区估算/经验值** ，并非官方公布：

类目
现象
建议解法

 **dtype** 
float64 内存翻倍
全程  `dtype=np.float32` ，输出  `astype(np.float32)` 

 **并行** 
n_jobs=-1 内存随核数线性放大
强制  `n_jobs=1` 

 **大模型** 
RandomForest 100 树训练吃内存
改 LightGBM 30~50 树

 **NLP** 
transformers 在线加载/推理
离线编码 → 存 dataset → alpha 内只查表

 **prophet** 
每日 fit 成本高
仅适合低频 alpha

 **pandas 链式** 
隐式 copy 倍增内存
切到 polars 或纯 numpy

 **大 N 协方差** 
N×N 矩阵随 N² 膨胀
先做宇宙预筛

 **每股票循环训练** 
时间成本爆炸
改 panel 整体训练

 **可视化对象返回** 
报错 "Alpha vector is not float32"
matplotlib 等只在 Notebook 用

 **store 维度** 

 `_validate_store`  报错
严格遵守源码 dims（见第六章）

### 神经网络专项提醒

- **远程仿真无 GPU** ：Notebook  `torch.cuda.is_available() == True` ，仿真为  `False`
- **离线训练 → 在线推理** 是唯一稳妥路线：
  1. BrainLabs Notebook 训练
  2. `state_dict`  拍平存  `store["weights"]` （ `dims="x"` ）
  3. alpha 内  `torch.no_grad()`  纯 CPU 前向
  4. 模型尺寸建议保守，进阶可用 numpy 重新实现 forward

## 六、 `store`  源码铁律（基于 brain SDK 源码）

这一节最容易踩坑。直接给源码出处：

`brain/simulations/simulations.py:15`

```
_DIMENSIONS = ["i", "x"]

```

**意思是  `dims`  字段的合法字符只有两个** ：

- **`"i"`**  = instruments axis（股票轴）。universe 扩张时 **自动 padding** ，配合  `extend`  字段使用
- **`"x"`**  = free axis（自由轴）。长度由 ndarray.shape 决定，不会自动扩展

合法组合： `"i"`  /  `"x"`  /  `"ix"`  /  `"xi"`  /  `"xx"`  /  `"ii"`  …

❌ 常见误区（包括我自己之前踩过的坑）：

- `extend=0.0`  +  `ndarray.float32` ——类型必须严格匹配（建议  `np.float32(0)`  或  `np.float64(np.nan)` ）
- 不初始化容器就直接  `store.X = ...` ——首次调用  `store.X is None` ，必须先建数组

```
# ✅ 正确范式：滚动 EWMA（来自实战 alpha 案例）
@alpha(
    data=["close"],
    store=[{"name": "ewma", "dims": "i", "extend": np.float32(0)}],
)
def ewma_alpha(data, store):
    n = data.close.shape[1]
    if store.ewma is None:
        store.ewma = np.zeros(n, dtype=np.float32)
    today = data.close[-1].astype(np.float32)
    store.ewma = (0.1 * today + 0.9 * store.ewma).astype(np.float32)
    return (today - store.ewma).astype(np.float32)

```

> 💡 教训： **永远向上游追溯信源** 。我之前凭印象写过  `dims="p"` ，结果是源码里根本没有这个值——只有读 SDK 源码这一条路是确定的。

## 七、提交前 Checklist

项
说明

☐ 输出向量 dtype
 `astype(np.float32)` 

☐ 模型并发
 `n_jobs=1` 

☐ 模型规模
LightGBM  `n_estimators`  保守、tree depth 浅

☐ Torch 推理

 `torch.no_grad()`  包住前向

☐ 禁忌 import
不在 alpha 内 import transformers / prophet / matplotlib / dash

☐ store 维度

 `dims`  仅用  `"i"`  /  `"x"`  组合， `extend`  类型与 ndarray dtype 严格匹配

☐ 池外处理
 `np.where(universe_mask, out, np.nan)` 

☐ Notebook 自测
模拟一日数据，断言  `np.isfinite`  比例正常

## 八、远程仿真"包可用性"探针

不知道哪些包在 alpha 内能 import？别猜，提交一次这个 alpha 看 result：

```
from brain.alphas import alpha
import numpy as np

@alpha(data=["close"])
def remote_package_probe(data):
    """信号编码 import 成功/失败：1.0 = 成功, 0.0 = 失败"""
    n = data.close.shape[1]
    signal = np.zeros(n, dtype=np.float32)
    test_packages = [
        'numpy', 'scipy', 'pandas', 'polars',
        'sklearn', 'lightgbm', 'xgboost', 'catboost',
        'torch', 'jax', 'statsmodels',
        'mosek', 'networkx', 'sympy',
        'transformers', 'prophet', 'spacy',
    ]
    for i, pkg in enumerate(test_packages):
        if i >= n:
            break
        try:
            __import__(pkg)
            signal[i] = 1.0
        except Exception:
            signal[i] = 0.0
    return signal

```

提交后看 result viewer 里前 N 只股票的 alpha 值，1.0 / 0.0 即包可用性。

## 九、社区动向同步（2026-05）

下面两条是社区资源， **非本人作品** ，引用前请自行评估。

### 1. 44 个 Python Only 扩展算子库（帖内附完整源码，可直接内联使用）

仿 TA-Lib / Qlib / Bloomberg 风格的  `brain_operators_extended.py` ，约 400 行源码 **已在论坛帖正文中完整贴出** ，包含 44 个算子的具体实现，分四类：

- **A 类 技术分析（约 20 个）** ：op_ema / op_macd / op_rsi / op_atr / op_bollinger_pct_b / op_dpo / op_kdj / op_obv …
- **B 类 统计计量（9 个）** ：op_ts_autocorr / op_ts_hurst / op_ts_half_life / op_ts_sharpe / op_ts_sortino / op_ts_max_drawdown / op_ts_calmar / op_rolling_beta / op_variance_ratio
- **C 类 数据清洗（11 个）** ：op_robust_zscore / op_mad_winsorize / op_iqr_winsorize 等
- **D 类 截面增强（4 个）** ：op_composite_rank / op_cross_decile / op_rank_residual / op_decay_rank

**仅 Python Alpha 可用** ，远程仿真不识别外部模块，需用  `inspect.getsource()`  或复制粘贴方式内联到 alpha cell。

- 来源帖：post-40178078863895
- 论坛链接： [../JX79797/[Python Alpha] 对标 TA-LibQlibBloomberg 的补充操作符库  技术分析统计计量数据清洗截面增强共 44 个.md](../JX79797/[Python Alpha] 对标 TA-LibQlibBloomberg 的补充操作符库  技术分析统计计量数据清洗截面增强共 44 个.md)
- 发布日期：2026-05-02（2026-05-13 更新）

### 2. brain_alpha_v2 自动化框架（仅设计说明，未公开源码）

作者发布的 MCP 工具， **帖内只描述接口与功能，未给出实现源码** ：

- `convert_to_python_backtest(alpha_id)` ：把 FASTEXPR alpha 转 Python 模式，DFS 提取算子源码并按依赖顺序内联
- `optimize_python_alpha(alpha_id, num_variants=5)` ：自动生成扩展算子变种（默认按概率注入 op_mad_winsorize / op_robust_zscore 等截面清洗）
- AI 不可用时降级为规则替换（ts_mean → ts_decay_linear 等）
- 帖中提及"21 个单测通过"，但单测与工具实现均未公开
- 来源帖：post-40187551660055
- 论坛链接： [../JX79797/新增 Python 回测支持convert_to_python_backtest  optimize_python_alpha.md](../JX79797/新增 Python 回测支持convert_to_python_backtest  optimize_python_alpha.md)
- 发布日期：2026-05-03（2026-05-23 更新）

> 📌 两个帖子作者相同（JX79797），从时间线看，第二个工具内部很可能调用第一个算子库；但帖中未明示，仅作合理推断。

## 十、六维盲区：Python Alpha 不计 Operators

实测验证： **Python Alpha 的操作符不计入六维 "Operators per Alpha"** ，但 Fields 维度照常计入。

含义：

- 用 Python 写 100 个嵌套 op_ema 不会突破 8 op 限制
- 但 **因此 Python Alpha 不能交 PPA** （系统无法判断 8 op 上限），目前只能走 RA 通道

这一点对方向 1（深度因子）和方向 2（Mosek 优化）是天然护城河——可以堆复杂逻辑而不挤占 op 预算。

## 写在最后

这帖子的目的不是劝大家"用 Transformer 写端到端因子"，而是说清楚一件事：

> **BrainLabs 给的环境足够强，但 simulation 沙箱有它的资源边界。会用的是把 sklearn / statsmodels / numpy 在边界内用透的人，不是把 transformers 硬塞进 alpha 的人。**

- 跑通了三版 IV-期限-体制 alpha 后，最有效的不是 Hurst 也不是 EMA，而是 **MAD winsorize + 多窗口 rank 集成** 这种"老老实实做 FastExpr 做不到的事"
- LightGBM 30 树 + 5 个差异化 Python 算子，长期看比 Transformer 端到端更可能上线

> ⚠️  **数据与来源说明**
> - **包清单** ：2026-05-26 BrainLabs Jupyter  `%pip list`  实测扫描
> - **API 提交格式** ：本人 2026-05 实际 POST  `/simulations`  留存的 payload
> - **三份 alpha 案例** ：本人在远程仿真实际提交并通过的代码（IV-期限-体制 系列 baseline / optimized / hurst）
> - **`_DIMENSIONS = ["i", "x"]`** ：brain SDK 源码  `brain/simulations/simulations.py:15`
> - **资源数值（MB / GB / 时间）** ：均为 **社区估算或经验值** ，官方未公布上限，不同账号/区域/universe 可能差异显著，请以自己提交后的真实结果为准
> - **方向 4 / 5 / 6 部分代码示例** ：仅为模式参考，未在远程仿真逐一验证，使用前请自行测试

## 附录 A：BrainLabs Jupyter 完整包清单（256 个）

> 来源：2026-05-26 在 BrainLabs Jupyter Notebook 内  `%pip list`  真实输出，按字母顺序排列。

### A

- absl-py == 2.4.0
- anyio == 4.13.0
- argon2-cffi == 25.1.0
- argon2-cffi-bindings == 25.1.0
- arrow == 1.4.0
- asttokens == 3.0.1
- astunparse == 1.6.3
- async-lru == 2.3.0
- attrs == 26.1.0

### B

- babel == 2.18.0
- beautifulsoup4 == 4.14.3
- bleach == 6.3.0
- blinker == 1.9.0
- blis == 0.7.11
- boto3 == 1.42.80
- botocore == 1.42.80

### C

- catalogue == 2.0.10
- **catboost == 1.0.5**
- certifi == 2026.2.25
- cffi == 2.0.0
- charset-normalizer == 2.4.7
- click == 8.3.2
- cloudpickle == 3.1.2 (注：序列化工具)
- cmake == 4.3.1
- **cmdstanpy == 1.3.0**
- comm == 0.2.3
- confection == 0.1.5
- contourpy == 1.3.2
- convertdate == 2.4.1
- cryptography == 46.0.7
- cycler == 0.12.1
- cymem == 2.0.13

### D

- dash == 4.1.0
- **dask == 2023.4.1**
- debugpy == 1.8.20
- decorator == 5.2.1
- defusedxml == 0.7.1
- dotenv == 0.9.9

### E – F

- ephem == 4.2.1
- exceptiongroup == 1.3.1
- executing == 2.2.1
- fastjsonschema == 2.21.2
- filelock == 3.5.2
- Flask == 3.3.3
- flatbuffers == 25.12.19
- fonttools == 4.62.1
- fqdn == 1.5.1
- fsspec == 2026.3.0

### G – H

- gast == 0.4.0
- google-auth == 2.49.2
- google-auth-oauthlib == 0.4.6
- google-pasta == 0.2.0
- graphviz == 0.21
- grpcio == 1.80.0
- h11 == 0.16.0
- **h5py == 3.16.0**
- hf-xet == 1.4.5
- holidays == 0.94
- httpcore == 1.0.9
- httpx == 0.28.1
- **huggingface_hub == 0.36.2**

### I – J

- idna == 3.11
- importlib_metadata == 9.0.0
- importlib_resources == 7.1.0
- ipykernel == 7.2.0
- ipython == 8.39.0
- ipywidgets == 8.1.8
- isoduration == 20.11.0
- itsdangerous == 2.2.0
- **jax == 0.4.5**
- jedi == 0.19.2
- Jinja2 == 3.1.6
- jmespath == 1.1.0
- **joblib == 1.5.3**
- json5 == 0.14.0
- jsonpointer == 3.1.1
- jsonschema == 4.26.0
- jsonschema-specifications == 2025.9.1

### Jupyter 系列

- jupyter-activity-monitor-extension == 0.3.2
- jupyter_client == 8.8.0
- jupyter_core == 5.9.1
- jupyter-events == 0.12.0
- jupyter-lsp == 2.3.1
- jupyter_server == 2.17.0
- jupyter_server_terminals == 0.5.4
- jupyterlab == 4.5.6
- jupyterlab_pygments == 0.3.0
- jupyterlab_server == 2.28.0
- jupyterlab_widgets == 3.0.16

### K – L

- **keras == 2.11.0**
- kiwisolver == 1.5.0
- langcodes == 3.5.1
- lark == 1.3.1
- libclang == 18.1.1
- **lightgbm == 3.3.5**
- lit == 18.1.8
- locket == 1.0.0
- LunarCalendar == 0.0.9

### M

- Markdown == 3.10.2
- MarkupSafe == 3.0.3
- **matplotlib == 3.10.8**
- matplotlib-inline == 0.2.1
- mistune == 3.2.0
- **Mosek == 9.3.22** （商业级凸优化求解器）
- mpmath == 1.0.15
- murmurhash == 1.0.15

### N

- narwhals == 2.19.0
- nbclient == 0.10.4
- nbconvert == 7.17.1
- nbformat == 5.10.4
- nest-asyncio == 1.6.0
- **networkx == 3.4.2**
- nltk == 3.0.1
- notebook_shim == 0.2.4
- **numpy == 1.24.2**

### NVIDIA CUDA 11.7 全家桶

- nvidia-cublas-cu11 == 11.10.3.66
- nvidia-cuda-cupti-cu11 == 11.7.101
- nvidia-cuda-nvrtc-cu11 == 11.7.99
- nvidia-cuda-runtime-cu11 == 11.7.99
- nvidia-cudnn-cu11 == 8.5.0.96
- nvidia-cufft-cu11 == 10.9.0.58
- nvidia-curand-cu11 == 10.2.10.91
- nvidia-cusolver-cu11 == 11.4.0.1
- nvidia-cusparse-cu11 == 11.7.4.91
- nvidia-nccl-cu11 == 2.14.3
- nvidia-nvtx-cu11 == 11.7.91

### O – P

- oauthlib == 3.3.1
- opt_einsum == 3.4.0
- orjson == 3.11.8
- ovsp == 0.6.2.post0
- overrides == 7.7.0
- packaging == 26.0
- **pandas == 1.5.3**
- pandocfilters == 1.5.1
- parso == 0.8.6
- partd == 1.4.2
- pathlib_abc == 0.5.2
- pathy == 0.14.2
- patsy == 1.0.2
- pexpect == 4.9.0
- pillow == 12.2.0
- pip == 26.0.1
- platformdirs == 4.9.6
- **plotly == 6.7.0**
- plotly-resampler == 0.11.0
- **polars == 0.19.12**
- preshed == 3.0.13
- prometheus_client == 0.25.0
- prompt_toolkit == 3.0.52
- **prophet == 1.1.3**
- protobuf == 3.19.6
- psutil == 7.2.2
- ptyprocess == 0.7.0
- pure_eval == 0.2.4
- **pyarrow == 23.0.1**
- pyasn1 == 0.6.3
- pyasn1_modules == 0.4.2
- pycparser == 3.0
- pydantic == 1.10.26
- Pygments == 2.20.0
- PyMeeus == 0.5.12
- pyparsing == 3.5.2
- python-dateutil == 2.9.0.post0
- python-dotenv == 1.2.2
- python-json-logger == 4.1.0
- pytz == 2026.1.post1
- PyYAML == 6.0.3
- pyzmq == 26.4.0

### Q – R

- qdldl == 0.1.9.post1
- referencing == 0.37.0
- regex == 2026.6.4
- requests == 2.33.1
- requests-oauthlib == 0.5.0
- retrying == 1.4.2
- rfc3339-validator == 0.1.4
- rfc3986-validator == 0.1.1
- rfc3987-syntax == 1.5.0
- rpds-py == 0.36.0

### S

- s3transfer == 0.16.0
- safetensors == 0.7.0
- **scikit-learn == 1.2.1**
- **scipy == 1.10.1**
- **seaborn == 0.13.2**
- Send2Trash == 2.1.0
- setuptools == 65.5.0
- six == 1.17.0
- smart-open == 6.4.0
- soupsieve == 2.8.3
- **spacy == 3.5.2**
- spacy-legacy == 3.0.12
- spacy-loggers == 1.0.5
- srsly == 2.5.3
- stack-data == 0.6.3
- stanio == 0.5.1
- **statsmodels == 0.13.5**
- swifter == 1.4.0
- **sympy == 1.14.0**

### T

- **tensorboard == 2.11.2**
- tensorboard-data-server == 0.6.1
- tensorboard-plugin-wit == 1.8.1
- **tensorflow == 2.11.1**
- tensorflow-estimator == 2.11.0
- tensorflow-io-gcs-filesystem == 0.37.1
- termcolor == 3.3.0
- terminado == 0.18.1
- thinc == 8.6.12
- threadpoolctl == 3.6.0
- tinycss2 == 1.4.0
- **tokenizers == 0.15.2**
- tomli == 2.4.1
- toolz == 1.1.0
- **torch == 2.0.1+cu117**
- tornado == 6.5.5
- tqdm == 4.67.3
- traitlets == 5.14.3
- **transformers == 4.30.1**
- triton == 2.0.0
- tsdownsample == 0.14.1
- typer == 0.7.0
- typing_extensions == 4.15.0
- tzdata == 2026.1

### U – W

- uri-template == 1.3.0
- urllib3 == 2.6.3
- wasabi == 1.1.3
- wcwidth == 0.6.0
- webcolors == 25.10.0
- webencodings == 0.5.1
- websocket-client == 1.9.0
- Werkzeug == 3.1.0
- wheel == 0.46.3
- widgetsnbextension == 4.0.15
- wrapt == 2.1.2

### X – Z

- **xgboost == 1.7.1**
- zipp == 3.23.0

---

## 讨论与评论 (6)

### 评论 #1 (作者: RM49262, 时间: 23天前)

=====================================评论区====================================

感谢大佬分享 这干货实在太多了 感觉比官方文档写的都详细

祝大佬比赛取得好名次

=============================================================================

---

### 评论 #2 (作者: YH37572, 时间: 23天前)

最有含金量的一集，一看到贴子推送的邮件马上就过来赞了。

最近我也在研究python alpha，卡在了获取到alpha原始值之后的统计分析上。看到楼主贴出来的工具清单发现自己还有好多根本没用上。也是十分佩服楼主的探索和分析精神，能把这么完整的数据呈现给大家。

祝楼主base多多, VF高高

---

### 评论 #3 (作者: MY82844, 时间: 23天前)

赞排查报告，非常有帮助，点赞收藏！btw, 有些链接怎么404了，有点奇怪的

===============================================

学而不思则罔，思而不学则殆

===============================================

---

### 评论 #4 (作者: ZX68343, 时间: 22天前)

没有权限访问: [../JX79797/[Python Alpha] 对标 TA-LibQlibBloomberg 的补充操作符库  技术分析统计计量数据清洗截面增强共 44 个.md](../JX79797/[Python Alpha] 对标 TA-LibQlibBloomberg 的补充操作符库  技术分析统计计量数据清洗截面增强共 44 个.md)

---

### 评论 #5 (作者: LA79055, 时间: 22天前)

这篇整理很有价值，尤其把 Python Alpha 环境、256 个包、API 调用方式和三类研究方向分开说明，和官方 Python Alpha 文档中 raw=True、BrainCache、@alpha 装饰器、store 状态管理等要点能互相印证。对刚开始迁移 Fast Expression 的顾问来说，这种把可验证事实和经验估计分开写的方式很实用，后续复现和排查问题也更清楚。

---

### 评论 #6 (作者: HZ99685, 时间: 22天前)

代码小白完全看不懂啊，专业术语实在太多了，消化不了，大佬太牛逼了，能不能给大家做个详细的系列课程逐一讲解一下呢。

---

