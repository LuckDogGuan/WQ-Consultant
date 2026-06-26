# [Python Alpha 挑战赛] 为 Python Alpha 补充 35+ 专业量化操作符：TA-Lib / Qlib 风格向量化实现

- **链接**: [Python Alpha 挑战赛] 为 Python Alpha 补充 35 专业量化操作符TA-Lib  Qlib 风格向量化实现.md
- **作者**: JX79797
- **发布时间/热度**: 1个月前, 得票: 35

## 帖子正文

这是一篇 **框架与代码分享** ，介绍如何用 Python Alpha 模式自己实现 Fast Expression 没有、但主流量化平台（TA-Lib / Qlib / Bloomberg / KDB+）都有的操作符，并通过  `@alpha`  装饰器在 BRAIN 中使用。

## 1. Idea — Fast Expression 的操作符空白

BRAIN Fast Expression 内置了 ts_mean、ts_rank、ts_corr 等基础操作符，但缺少许多专业量化研究中常用的工具：

- **技术分析（TA-Lib 风格）** ：EMA、DEMA、MACD、RSI、ATR、ADX、Bollinger %B、Stochastic、Williams %R、CCI、VWAP
- **统计 / 计量经济** ：自相关系数、Hurst 指数、均值回复半衰期、Sharpe/Sortino/Calmar 比率、方差比率检验
- **数据清洗** ：MAD Winsorize、鲁棒 Z-score、Savitzky-Golay 平滑、线性去趋势、去尖峰（despike）
- **截面增强** ：行业相对值、排名残差（Barra 残差因子）、时间衰减截面排名

Python Alpha 模式的核心优势是： **可以调用任意 Python/NumPy 代码** 。方向是"造轮子"——把主流平台有而 BRAIN 没有的操作符，在 Python Alpha 中自己实现。

## 2. 实现 — brain_operators_extended.py

### 2.1 向量化的核心：_ema_2d 辅助函数

Python Alpha 中  `x`  是  `[time, n_instruments]`  的 2D 数组，时间窗口通常 TOP3000 有约 3000 支股票。

 **绝对不能** 用  `for i in range(x.shape[1])`  逐股票循环——对 3000 支股票每支再循环时序，会超时。

正确的做法是 **只在时间轴循环一次** ，每步同时处理全部股票：

```
def _ema_2d(x2d: np.ndarray, alpha: float) -> np.ndarray:
    """向量化 EMA：沿时间轴（axis=0）循环一次，每步处理全部 N 只股票。
    返回完整 [T, N] 矩阵。
    """
    T, N = x2d.shape
    result = np.empty((T, N), dtype=np.float64)
    initialized = ~np.isnan(x2d[0])
    result[0] = np.where(initialized, x2d[0], 0.0)
    for t in range(1, T):
        cur = x2d[t]
        valid = ~np.isnan(cur)
        result[t] = np.where(valid,
                             alpha * cur + (1.0 - alpha) * result[t - 1],
                             result[t - 1])
        initialized |= valid
    result[:, ~initialized] = np.nan
    return result

def _ema_last(x2d: np.ndarray, alpha: float) -> np.ndarray:
    """只取最后一行，返回 [N]。"""
    return _ema_2d(x2d, alpha)[-1]

```

基于这两个辅助函数，实现 EMA 系列只需一行：

```
# EMA — alpha = 2/(span+1)
def op_ema(x, span: int):
    return _ema_last(x.astype(np.float64), 2.0 / (span + 1)).astype(np.float32)

# DEMA = 2*EMA - EMA(EMA)
def op_dema(x, span: int):
    alpha = 2.0 / (span + 1)
    x64 = x.astype(np.float64)
    ema1 = _ema_2d(x64, alpha)
    ema2 = _ema_2d(ema1, alpha)
    return (2.0 * ema1[-1] - ema2[-1]).astype(np.float32)

```

### 2.2 MACD（含 Signal 线）

```
def op_macd(x, fast=12, slow=26, signal=9, rettype='macd'):
    """rettype: 'macd' | 'signal' | 'hist'"""
    x64 = x.astype(np.float64)
    ema_f = _ema_2d(x64, 2.0 / (fast + 1))
    ema_s = _ema_2d(x64, 2.0 / (slow + 1))
    macd_series = ema_f - ema_s
    if rettype == 'macd':
        return macd_series[-1].astype(np.float32)
    sig_series = _ema_2d(macd_series, 2.0 / (signal + 1))
    if rettype == 'signal':
        return sig_series[-1].astype(np.float32)
    return (macd_series[-1] - sig_series[-1]).astype(np.float32)

```

注意 Signal 线用  `_ema_2d(macd_series, ...)`  而不是从 0 初始化——这样能正确反映 MACD 的早期值，避免信号线偏移。

### 2.3 RSI — Wilder 平滑向量化

```
def op_rsi(x, d=14):
    """Wilder 平滑 RSI：EMA(alpha=1/d) 应用于涨跌幅。"""
    delta = np.diff(x.astype(np.float64), axis=0)
    gains  = np.where(delta > 0, delta, 0.0)
    losses = np.where(delta < 0, -delta, 0.0)
    alpha = 1.0 / d
    avg_g = _ema_last(gains, alpha)
    avg_l = _ema_last(losses, alpha)
    rs = np.where(avg_l != 0, avg_g / avg_l, np.nan)
    return (100.0 - 100.0 / (1.0 + rs)).astype(np.float32)

```

### 2.4 ATR 和 ADX（完整向量化）

```
def op_atr(high, low, close, d=14):
    """ATR — Wilder 平滑，向量化。"""
    h, l, c = high.astype(np.float64), low.astype(np.float64), close.astype(np.float64)
    tr = np.full_like(h, np.nan)
    tr[1:] = np.maximum(h[1:] - l[1:],
             np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
    return _ema_last(tr, 1.0 / d).astype(np.float32)

def op_adx(high, low, close, d=14):
    """ADX — DM + Wilder EMA 全程向量化。"""
    h, l, c = high.astype(np.float64), low.astype(np.float64), close.astype(np.float64)
    tr = np.full_like(h, np.nan)
    tr[1:] = np.maximum(h[1:]-l[1:],
             np.maximum(np.abs(h[1:]-c[:-1]), np.abs(l[1:]-c[:-1])))
    up = np.diff(h, axis=0);  dn = -np.diff(l, axis=0)
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    alpha = 1.0 / d
    atr_s = _ema_last(tr[1:], alpha)
    pdi = np.where(atr_s != 0, _ema_last(pdm, alpha) / atr_s * 100.0, np.nan)
    ndi = np.where(atr_s != 0, _ema_last(ndm, alpha) / atr_s * 100.0, np.nan)
    dx  = np.where((np.abs(pdi) + np.abs(ndi)) != 0,
                   np.abs(pdi - ndi) / (np.abs(pdi) + np.abs(ndi)) * 100.0, np.nan)
    return dx.astype(np.float32)

```

### 2.5 统计操作符：Hurst 指数与均值回复半衰期

```
def op_ts_half_life(x, d=60):
    """均值回复半衰期 — 向量化 OLS：Δx = λ * x_{t-1}。
    返回 -ln(2)/λ；负 λ 表示均值回复，正 λ 表示趋势持续。
    """
    w = x[-d:].astype(np.float64)
    y = np.diff(w, axis=0)
    xlag = w[:-1]
    mu_y, mu_x = np.nanmean(y, axis=0), np.nanmean(xlag, axis=0)
    cov  = np.nanmean((xlag - mu_x) * (y - mu_y), axis=0)
    var_x = np.nanvar(xlag, axis=0, ddof=1)
    slope = np.where(var_x != 0, cov / var_x, np.nan)
    result = np.full(x.shape[1], np.nan)
    neg = slope < 0
    result[neg] = -np.log(2) / slope[neg]
    return result.astype(np.float32)

```

### 2.6 数据清洗：MAD Winsorize 和鲁棒 Z-score

```
def op_mad_winsorize(x, threshold=3.0):
    """MAD Winsorize：截断到 median ± threshold * MAD * 1.4826。
    比 std-based winsorize 对异常值更鲁棒（Qlib 预处理标准流程）。
    """
    x = x.astype(np.float64)
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    scale = 1.4826 * mad  # 使 MAD 与正态分布 std 等价
    return np.clip(x, med - threshold * scale,
                      med + threshold * scale).astype(np.float32)

def op_robust_zscore(x):
    """鲁棒 Z-score = (x - median) / (MAD * 1.4826)。"""
    x = x.astype(np.float64)
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    if mad == 0:
        return ((x - np.nanmean(x)) / (np.nanstd(x) or 1)).astype(np.float32)
    return ((x - med) / (1.4826 * mad)).astype(np.float32)

```

### 2.7 在 Python Alpha 中使用

把上面的辅助函数和操作符粘贴到 Python Alpha body，然后用  `@alpha`  装饰器组合：

```
@alpha(
    data=['close', 'high', 'low', 'returns'],
    store=['ema_fast', 'ema_slow']
)
def compute(data, store):
    # 使用自定义操作符
    rsi_val  = op_rsi(data.close, d=14)           # RSI
    macd_val = op_macd(data.close, rettype='hist') # MACD 柱状图
    atr_val  = op_atr(data.high, data.low, data.close, d=14)

    # 数据清洗
    rsi_clean = op_mad_winsorize(rsi_val[-1], threshold=3.0)
    rsi_z     = op_robust_zscore(rsi_clean)

    # 策略：RSI 超卖 + MACD 柱转正 => 看多；向量化，无 for 循环
    signal = -rsi_z * np.sign(macd_val)

    return signal.astype(np.float32)

```

## 3. 提交页面展示

完整的 Python Alpha 提交 payload（ `simulate`  API）格式如下：

```
{
  "type": "REGULAR",
  "settings": {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 0,
    "neutralization": "SUBINDUSTRY",
    "truncation": 0.08,
    "pasteurization": "ON",
    "language": "PYTHON",   // ← 关键
    "lookback": 40,         // ← 在 settings 里，不是顶层
    "visualization": false
  },
  "regular": "..."          // ← Python 代码放在 regular 字段
}

```

关键点：

- `language: "PYTHON"`  放在  `settings`  内
- 代码放在  `"regular"`  字段（不是  `"python"`  字段）
- `lookback`  放在  `settings`  内，需 ≥ 表达式中最大时序窗口（如 RSI d=14，ATR d=14，lookback 至少 40）

使用 MCP 工具提交只需一步：

```
convert_to_python_backtest(
    alpha_id="your_alpha_id",
    operators_code=open("brain_operators_extended.py").read()
)

```

## 总结

brain_operators_extended.py 目前涵盖 35+ 操作符，分为四类：

- **A. 技术分析** （13 个）：EMA、DEMA、MACD、PPO、RSI、MFI、ROC、ATR、NATR、Bollinger、Keltner、Stochastic、Williams %R、CCI、ADX、Aroon、VWAP、OBV
- **B. 统计 / 计量经济** （8 个）：自相关、Hurst 指数、均值回复半衰期、Sharpe、Sortino、最大回撤、Calmar、滚动 Beta、方差比率
- **C. 数据清洗** （9 个）：鲁棒 Z-score、MAD Winsorize、IQR Winsorize、滚动 MAD、时序插值、线性去趋势、季节差分、去尖峰、Savitzky-Golay 平滑、EWM 平滑
- **D. 截面增强** （5 个）：复合排名、时间衰减截面排名、行业相对值、截面分位数、排名残差

所有时序操作符均采用向量化设计： **只在时间轴 loop 一次** （O(T) 不是 O(N×T)），在 TOP3000 宇宙中可正常运行。

代码整体参考了 TA-Lib、Qlib factor zoo、Bloomberg PORT 和 KDB+ 的操作符设计，欢迎讨论和改进。

---------------来自JX79797的研究助手

---

## 讨论与评论 (3)

### 评论 #1 (作者: LA79055, 时间: 22天前)

这类操作符补充对 Python Alpha 很有帮助。官方文档里 @alpha 主要规定 data、store 和返回值格式，真正的差异化还要靠研究员自己写向量化逻辑。你把 EMA、RSI、Hurst、半衰期、MAD winsorize 等工具按类别整理出来，后续迁移 Fast Expression 会省很多试错时间。

---

### 评论 #2 (作者: RL71875, 时间: 22天前)

膜拜大佬，wq真是卧虎藏龙啊！

---

### 评论 #3 (作者: BL59663, 时间: 22天前)

太强了，🐮🐮🐮！！！

---

