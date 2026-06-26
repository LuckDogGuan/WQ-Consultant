# [Python Alpha 挑战赛] AI Agent 自动将 Fast Expression 转为 Python Alpha 并回测经验分享

- **链接**: [Python Alpha 挑战赛] AI Agent 自动将 Fast Expression 转为 Python Alpha 并回测经验分享.md
- **作者**: JX79797
- **发布时间/热度**: 1个月前, 得票: 38

## 帖子正文

本文分享一个 AI Agent 工作流： **无需手写任何 Python alpha 代码** ，直接把已有的 Fast Expression 自动转换为符合平台规范的 Python @alpha，并提交回测。

## 1. Idea

BRAIN 平台推出 Python Alpha 之后，最大的门槛不是经济逻辑，而是 **代码迁移成本** 。一条 Fast Expression 如  `-ts_zscore(ts_mean(returns, 20), 60)`  在平台上只有一行，但要写成 Python @alpha，需要：

- 理解  `data.returns`  是  `[time, n_inst]`  2D 数组
- 把  `ts_mean` 、 `ts_zscore`  翻译成 numpy 操作
- 处理嵌套 TS 算子时的  `store`  滚动缓冲区
- 确保代码"完全自包含"（不能 import 任何外部自定义模块）

我们的 Agent 能把这整条链路 **全自动完成** ，并以 MCP 工具的形式调用。

## 2. 实现

### 核心：ExprConverter 转换器

转换器通过递归下降解析 Fast Expression，对每个算子做分类处理：

- **TS 算子** （ts_mean/ts_zscore/ts_rank …）：字段参数用  `data.field` （2D），直接内联为 numpy 操作
- **CS 算子** （rank/zscore/divide …）：字段参数用  `data.field[-1]` （1D），内联为截面计算
- **嵌套 TS** （如  `ts_zscore(ts_mean(...))` ）：内层 TS 产生 1D 结果，外层 TS 需要 2D 历史，自动生成  `store`  滚动缓冲区和暖启动函数

### 真实转换示例

输入 Fast Expression：

```
-ts_zscore(ts_mean(returns, 20), 60)
```

自动生成的 Python @alpha（完整输出，无任何手工修改）：

```
from brain.alphas import alpha
import numpy as np
import numpy.typing as npt
from scipy import stats as scipy_stats

# ── Brain boilerplate ──
def pasteurize(a, u):
    a = a.copy()
    a[~u.astype(bool)] = np.nan
    return a

def neutralize(a):
    a0 = np.nan_to_num(a, nan=0, posinf=0, neginf=0)
    return a - np.mean(a0)

def scale(a):
    a0 = np.nan_to_num(a, nan=0, posinf=0, neginf=0)
    norm = np.linalg.norm(a0, ord=1)
    return a / norm if norm > 0 else a

def _ts_rank(x2d, d):
    w = x2d[-d:]
    cur = w[-1]
    out = np.nanmean(w <= cur[np.newaxis], axis=0).astype(np.float32)
    out[np.isnan(cur)] = np.nan
    return out

def _ts_decay_linear(x2d, d):
    w = x2d[-d:]
    weights = np.arange(1, len(w) + 1, dtype=np.float32)
    weights /= weights.sum()
    return np.nansum(w * weights[:, np.newaxis], axis=0).astype(np.float32)

# ── Warm-start helper (pre-fill store buffer from lookback data) ──
def _warmup_tsbuf0(data, n_inst):
    """Warm-start buffer for tsbuf0: compute 60 steps of inner TS from lookback."""
    _buf = np.full((60, n_inst), np.nan, dtype=np.float32)
    for _k in range(60):
        try:
            _v = np.asarray(np.nanmean(data.returns[-20-_k:(-_k) if _k > 0 else None], axis=0),
                            dtype=np.float32)
            if _v.shape[0] == n_inst:
                _buf[60 - 1 - _k] = _v
        except Exception:
            break
    return _buf

@alpha(
    data=['returns'],
    store=[{"name": "tsbuf0", "dims": "xi", "extend": np.float32(np.nan)}],
)
def alpha_func(data, store) -> npt.NDArray[np.float32]:
    _t0 = np.asarray(np.nanmean(data.returns[-20:], axis=0), dtype=np.float32)
    if store.tsbuf0 is None:
        store.tsbuf0 = _warmup_tsbuf0(data, _t0.shape[0])
    store.tsbuf0[:-1] = store.tsbuf0[1:].copy()
    store.tsbuf0[-1] = _t0
    a = (-(( store.tsbuf0[-1]
             - np.nanmean(store.tsbuf0[-60:], axis=0))
           / np.nanstd(store.tsbuf0[-60:], axis=0, ddof=0)))
    return a.astype(np.float32)
```

转换器自动推断所需  `lookback = max_window × 2 = 120` ，可直接填入  `settings.lookback` 。

### 完整 API 提交示例

```
import requests

# 由转换器生成的 Python 代码（见上方）
python_code = """..."""

payload = {
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
        "language": "PYTHON",
        "visualization": False,
        "lookback": 120,   # 由转换器自动推断
    },
    "regular": python_code,   # 注意：Python 模式仍用 "regular" 字段
}

resp = session.post("https://api.worldquantbrain.com/simulations", json=payload)
progress_url = resp.headers["Location"]
```

### MCP 工具一行调用

如果在 MCP 环境下使用，整个流程只需一个工具调用：

```
convert_to_python_backtest(alpha_id="your_alpha_id")
```

工具会自动：① 读取 alpha 的 fast expression → ② 转换为 Python 代码 → ③ 推断 lookback → ④ 提交回测 → ⑤ 返回结果。

## 3. 提交页面展示

以下是转换后的代码提交到平台后的回测设置结构（截图对应上方 API 参数）：

- **Language** ：PYTHON
- **Region** ：USA | Universe：TOP3000 | Delay：1
- **Neutralization** ：SUBINDUSTRY
- **Lookback** ：120（由  `max_window × 2`  自动推断）
- **Regular field** ：自动生成的完整 Python @alpha 代码（含 store buffer、warmup、所有 helper inline）

转换器的核心价值在于： **把迁移门槛从"会写 numpy/store 的 Python 程序员"降低到"会写 Fast Expression 的 BRAIN 用户"** 。已有的每一条 Fast Expression alpha 都可以一键转为 Python 模式回测，无需重写逻辑。

---

## 讨论与评论 (7)

### 评论 #1 (作者: JX79797, 时间: 1个月前)

补充：以下是完整的转换器核心代码和操作符库代码，可直接集成到自己的项目中。

## Part 1 — python_converter.py（ExprConverter 核心）

完整文件约 850 行，这里贴出最关键的三部分：

### ① 内联映射表 _TS_INLINE / _CS_INLINE（TS/CS 算子 → numpy 表达式）

```
# TS 算子内联表：直接生成 numpy 代码，不需要 op_* 包装函数
# 每个 lambda 接收 (x_expr: str, d: int, ...) → numpy 表达式字符串
_TS_INLINE = {
    "ts_mean":       lambda x, d: f"np.nanmean({x}[-{d}:], axis=0)",
    "ts_sum":        lambda x, d: f"np.nansum({x}[-{d}:], axis=0)",
    "ts_std_dev":    lambda x, d: f"np.nanstd({x}[-{d}:], axis=0, ddof=0)",
    "ts_min":        lambda x, d: f"np.nanmin({x}[-{d}:], axis=0)",
    "ts_max":        lambda x, d: f"np.nanmax({x}[-{d}:], axis=0)",
    "ts_median":     lambda x, d: f"np.nanmedian({x}[-{d}:], axis=0)",
    "ts_delay":      lambda x, d: f"{x}[-{int(d) + 1}]",
    "ts_delta":      lambda x, d: f"({x}[-1] - {x}[-{int(d) + 1}])",
    "ts_returns":    lambda x, d: f"np.where({x}[-{int(d)+1}] != 0, {x}[-1] / {x}[-{int(d)+1}] - 1, np.nan)",
    "log_diff":      lambda x, d: f"(np.log(np.where({x}[-1]>0,{x}[-1],np.nan)) - np.log(np.where({x}[-{int(d)+1}]>0,{x}[-{int(d)+1}],np.nan)))",
    "ts_zscore":     lambda x, d: f"(({x}[-1] - np.nanmean({x}[-{d}:], axis=0)) / np.nanstd({x}[-{d}:], axis=0, ddof=0))",
    "ts_rank":       lambda x, d: f"_ts_rank({x}, {d})",
    "ts_decay_linear": lambda x, d: f"_ts_decay_linear({x}, {d})",
    "ts_av_diff":    lambda x, d: f"np.nanmean(np.diff({x}[-{int(d)+1}:], axis=0), axis=0)",
    "ts_min_diff":   lambda x, d: f"({x}[-1] - np.nanmin({x}[-{d}:], axis=0))",
    "ts_max_diff":   lambda x, d: f"(np.nanmax({x}[-{d}:], axis=0) - {x}[-1])",
    "ts_ir":         lambda x, d: f"(np.nanmean({x}[-{d}:], axis=0) / np.nanstd({x}[-{d}:], axis=0, ddof=0))",
    "ts_arg_max":    lambda x, d: f"(len({x}[-{d}:]) - 1 - np.nanargmax({x}[-{d}:][::-1], axis=0)).astype(np.float32)",
    "ts_arg_min":    lambda x, d: f"(len({x}[-{d}:]) - 1 - np.nanargmin({x}[-{d}:][::-1], axis=0)).astype(np.float32)",
    "ts_skewness":   lambda x, d: f"scipy_stats.skew({x}[-{d}:], axis=0, nan_policy='omit')",
    "ts_kurtosis":   lambda x, d: f"scipy_stats.kurtosis({x}[-{d}:], axis=0, nan_policy='omit')",
    "ts_count_nans": lambda x, d: f"np.sum(np.isnan({x}[-{d}:]), axis=0).astype(np.float32)",
    "ts_percentage": lambda x, d, p: f"np.nanpercentile({x}[-{d}:], {p} * 100, axis=0)",
}

```

### ② _emit()：递归 AST 遍历，生成 numpy 表达式字符串

```
def _emit(self, node, parent_op, ts_context=False):
    """递归生成 Python 表达式字符串。
    ts_context=True 时字段用 data.field（2D），否则用 data.field[-1]（1D）。
    """
    if node.kind == "literal":
        v = node.value
        return str(int(v)) if isinstance(v, float) and v == int(v) else str(v)

    if node.kind == "neg":
        return f"(-{self._emit(node.args[0], parent_op, ts_context)})"

    if node.kind == "kwarg":
        val_str = self._emit(node.args[0], parent_op, ts_context)
        return f"{node.value}={val_str}"

    if node.kind == "field":
        name = node.value
        self._fields.add(name)
        return f"data.{name}" if ts_context else f"data.{name}[-1]"

    # ── call node ────────────────────────────────────
    op = node.value

    # 1. TS 内联优先（直接生成 numpy，不产生 op_* 包装）
    if op in _TS_OPS:
        result = self._try_ts_inline(op, node.args)
        if result is not None:
            return result

    # 2. CS 内联
    if op not in _TS_OPS:
        result = self._try_cs_inline(op, node.args, ts_context)
        if result is not None:
            return result

```

### ③ _emit_with_store_buffer()：嵌套 TS 算子的 store 缓冲方案

当表达式出现  `ts_zscore(ts_mean(returns, 20), 60)`  这类嵌套 TS 时，内层  `ts_mean`  返回 1D，外层  `ts_zscore`  需要历史窗口，无法直接切片。解决方案：写入持久化 store 缓冲区，每步滚动更新。

```
def _emit_with_store_buffer(self, op, args, d, fn):
    """为嵌套 TS 生成 store 缓冲区代码。
    内层 TS 结果每步写入 store.tsbufN（shape [d, n_inst]），
    外层 TS 从缓冲区读取完整历史窗口。
    """
    buf_key = f"tsbuf{self._buf_counter}"
    tmp_var = f"_t{self._buf_counter}"
    self._buf_counter += 1
    self._store_keys.append({"name": buf_key, "dims": "xi"})  # [window, n_inst]

    inner_expr = self._emit(args[0], parent_op=op, ts_context=False)
    warmup_fn  = f"_warmup_{buf_key}"

    # 注入到函数体（在 a = ... 之前执行）
    self._pre_stmts += [
        f"    {tmp_var} = np.asarray({inner_expr}, dtype=np.float32)",
        f"    if store.{buf_key} is None:",
        f"        store.{buf_key} = {warmup_fn}(data, {tmp_var}.shape[0])",
        f"    store.{buf_key}[:-1] = store.{buf_key}[1:].copy()",  # FIFO shift
        f"    store.{buf_key}[-1]  = {tmp_var}",                    # append latest
    ]

    # 暖启动函数：首次调用时用 lookback 数据回填过去 d 步，消除冷启动期
    shifted = re.sub(
        r"\[(-\d+):\]",
        lambda m: f"[{m.group(1)}-_k:(-_k) if _k > 0 else None]",
        inner_expr,
    )
    shifted = re.sub(        # 处理 ts_delay/ts_delta 展开的点索引 [-N]
        r"\[-(\d+)\]",
        lambda m: f"[-{m.group(1)}-_k]",
        shifted,
    )
    warmup_src = (
        f"def {warmup_fn}(data, n_inst):\n"
        f"    _buf = np.full(({d}, n_inst), np.nan, dtype=np.float32)\n"
        f"    for _k in range({d}):\n"
        f"        try:\n"
        f"            _v = np.asarray({shifted}, dtype=np.float32)\n"
        f"            if _v.shape[0] == n_inst:\n"
        f"                _buf[{d} - 1 - _k] = _v\n"
        f"        except Exception:\n"
        f"            break\n"
        f"    return _buf\n"
    )
    self._warmup_defs.append(warmup_src)

```

### ④ _infer_lookback()：自动推断所需 lookback

```
def _infer_lookback(expression: str, minimum: int = 21) -> int:
    """扫描所有 TS 算子的整数窗口参数，取最大值 * 2 作为安全缓冲。
    例如 ts_mean(returns, 20) → max_win=20 → lookback=40
    上限 504（约 2 年）。
    """
    tokens = _tokenize(expression)
    root, _ = _parse(tokens)
    max_win = [minimum]

    def _scan(node):
        if node.kind == "call" and node.value in _TS_OPS:
            for arg in node.args:
                if arg.kind == "literal" and isinstance(arg.value, int) and arg.value > 1:
                    max_win[0] = max(max_win[0], arg.value)
        for child in node.args:
            _scan(child)

    _scan(root)
    return min(max_win[0] * 2, 504)

```

## Part 2 — brain_operators_extended.py（Python-only 操作符库）

完整文件约 725 行，以下是四个分类的代表性实现：

### 核心辅助函数（向量化的关键）

```
import numpy as np
from scipy import stats as scipy_stats
from scipy.signal import savgol_filter

def _f64(x): return x.astype(np.float64) if x.dtype != np.float64 else x.copy()
def _win(x, d): return x[-d:] if len(x) >= d else x
def _sdiv(a, b):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(b != 0, a / b, np.nan)
_safe_div = _sdiv

def _ema_2d(x2d: np.ndarray, alpha: float) -> np.ndarray:
    """向量化 EMA（沿时间轴）。
    只循环 T 次（不是 T*N），每步同时更新全部 N 只股票。
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

```

### A. 技术分析操作符

```
# EMA / DEMA
def op_ema(x, span: int):
    return _ema_last(_f64(x), 2.0 / (span + 1)).astype(np.float32)

def op_dema(x, span: int):
    alpha = 2.0 / (span + 1)
    x64 = _f64(x)
    ema1 = _ema_2d(x64, alpha)
    ema2 = _ema_2d(ema1, alpha)
    return (2.0 * ema1[-1] - ema2[-1]).astype(np.float32)

# MACD（含 Signal/Histogram）
def op_macd(x, fast=12, slow=26, signal=9, rettype='macd'):
    x64 = _f64(x)
    ema_f = _ema_2d(x64, 2.0 / (fast + 1))
    ema_s = _ema_2d(x64, 2.0 / (slow + 1))
    macd_series = ema_f - ema_s
    if rettype == 'macd':   return macd_series[-1].astype(np.float32)
    sig_series  = _ema_2d(macd_series, 2.0 / (signal + 1))
    if rettype == 'signal': return sig_series[-1].astype(np.float32)
    return (macd_series[-1] - sig_series[-1]).astype(np.float32)

# RSI — Wilder 平滑向量化
def op_rsi(x, d=14):
    delta = np.diff(_f64(x), axis=0)
    gains  = np.where(delta > 0, delta, 0.0)
    losses = np.where(delta < 0, -delta, 0.0)
    avg_g = _ema_last(gains,  1.0 / d)
    avg_l = _ema_last(losses, 1.0 / d)
    rs = _sdiv(avg_g, avg_l)
    return (100.0 - 100.0 / (1.0 + rs)).astype(np.float32)

# ATR — Wilder 平滑向量化
def op_atr(high, low, close, d=14):
    h, l, c = _f64(high), _f64(low), _f64(close)
    tr = np.full_like(h, np.nan)
    tr[1:] = np.maximum(h[1:] - l[1:],
             np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
    return _ema_last(tr, 1.0 / d).astype(np.float32)

# ADX — 完全向量化
def op_adx(high, low, close, d=14):
    h, l, c = _f64(high), _f64(low), _f64(close)
    tr = np.full_like(h, np.nan)
    tr[1:] = np.maximum(h[1:]-l[1:],
             np.maximum(np.abs(h[1:]-c[:-1]), np.abs(l[1:]-c[:-1])))
    up = np.diff(h, axis=0); dn = -np.diff(l, axis=0)
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    alpha = 1.0 / d
    atr_s = _ema_last(tr[1:], alpha)
    pdi = _sdiv(_ema_last(pdm, alpha), atr_s) * 100.0
    ndi = _sdiv(_ema_last(ndm, alpha), atr_s) * 100.0
    return _sdiv(np.abs(pdi - ndi), np.abs(pdi) + np.abs(ndi)).astype(np.float32) * 100.0

# Bollinger %B
def op_bollinger_pct_b(x, d=20, k=2.0):
    w  = _f64(_win(x, d))
    mu = np.nanmean(w, axis=0); sd = np.nanstd(w, axis=0, ddof=1)
    return _sdiv(_f64(x[-1]) - (mu - k*sd), 2*k*sd).astype(np.float32)

```

### B. 统计 / 计量经济操作符

```
# 均值回复半衰期 — 向量化 OLS
def op_ts_half_life(x, d=60):
    w    = _f64(_win(x, d))
    y    = np.diff(w, axis=0)   # Δx
    xlag = w[:-1]               # x_{t-1}
    mu_y = np.nanmean(y, axis=0); mu_x = np.nanmean(xlag, axis=0)
    cov  = np.nanmean((xlag - mu_x) * (y - mu_y), axis=0)
    var_x = np.nanvar(xlag, axis=0, ddof=1)
    slope = _sdiv(cov, var_x)
    result = np.full(x.shape[1], np.nan, dtype=np.float64)
    neg = slope < 0  # 负斜率 = 均值回复
    result[neg] = -np.log(2) / slope[neg]
    return result.astype(np.float32)

# 自相关系数
def op_ts_autocorr(x, d, lag=1):
    w = _f64(_win(x, d + lag))
    y1 = w[:-lag]; y2 = w[lag:]
    cov  = np.nanmean((y1 - np.nanmean(y1, axis=0)) *
                      (y2 - np.nanmean(y2, axis=0)), axis=0)
    std1 = np.nanstd(y1, axis=0, ddof=1)
    std2 = np.nanstd(y2, axis=0, ddof=1)
    return _sdiv(cov, std1 * std2 + 1e-14).astype(np.float32)

# 滚动 Sharpe
def op_ts_sharpe(returns, d=252, annualize=True):
    w = _f64(_win(returns, d))
    mu = np.nanmean(w, axis=0); sd = np.nanstd(w, axis=0, ddof=1)
    sr = _sdiv(mu, sd)
    return (sr * np.sqrt(252) if annualize else sr).astype(np.float32)

```

### C. 数据清洗操作符

```
# 鲁棒 Z-score（对异常值不敏感）
def op_robust_zscore(x):
    x = _f64(x)
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    if mad == 0:
        std = np.nanstd(x)
        return ((x - np.nanmean(x)) / (std or 1)).astype(np.float32)
    return ((x - med) / (1.4826 * mad)).astype(np.float32)

# MAD Winsorize
def op_mad_winsorize(x, threshold=3.0):
    x = _f64(x)
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    scale = 1.4826 * mad
    return np.clip(x, med - threshold * scale,
                      med + threshold * scale).astype(np.float32)

# Savitzky-Golay 平滑（向量化 2D）
def op_ts_smooth_savgol(x, d, poly=3):
    w = _f64(_win(x, d))
    win_len = d if d % 2 == 1 else d - 1
    if win_len <= poly:
        return np.nanmean(w, axis=0).astype(np.float32)
    col_means = np.nanmean(w, axis=0)
    w_filled = np.where(np.isnan(w), col_means, w)
    smoothed = savgol_filter(w_filled, win_len, poly, axis=0)[-1]
    smoothed[np.isnan(w).mean(axis=0) > 0.3] = np.nan
    return smoothed.astype(np.float32)

```

### D. 截面增强操作符

```
# 排名残差（Barra 残差因子）
def op_rank_residual(y, *xs):
    """rank(y) 对 rank(x1), rank(x2), ... 做截面回归后的残差。
    去除已知因子暴露，提取纯净 alpha 信号。
    """
    ry = _f64(op_rank(y))
    rx_list = [_f64(op_rank(xi)) for xi in xs]
    y_v = ry; Xmat = np.column_stack(rx_list)
    valid = ~(np.isnan(y_v) | np.any(np.isnan(Xmat), axis=1))
    result = np.full_like(y_v, np.nan)
    if valid.sum() >= len(xs) + 2:
        beta, *_ = np.linalg.lstsq(Xmat[valid], y_v[valid], rcond=None)
        result[valid] = y_v[valid] - Xmat[valid] @ beta
    return result.astype(np.float32)

```

两个文件合计约 1600 行，都可以直接粘贴到 Python Alpha body 中使用（不需要额外 pip install，只依赖 numpy / scipy）。如有问题欢迎在帖子中留言讨论。

---------------来自JX79797的研究助手

---

### 评论 #2 (作者: LA79055, 时间: 22天前)

这篇把迁移成本讲得很清楚。Fast Expression 一行表达式背后，Python Alpha 需要处理二维历史数组、截面算子、时间序列窗口和 store 状态。官方文档也说明 simulation 会逐步调用 alpha 函数，如果 Agent 能正确处理嵌套 TS 算子，对批量迁移会很有用。

---

### 评论 #3 (作者: YS94888, 时间: 22天前)

感谢大佬的分享👍，请问ExprConverter、操作符库的完整文件到哪里领取？ [😁](https://zh.wikipedia.org/w/index.php?title=%F0%9F%98%81&action=edit&redlink=1)  [😁](https://zh.wikipedia.org/w/index.php?title=%F0%9F%98%81&action=edit&redlink=1)

---

### 评论 #4 (作者: HZ99685, 时间: 22天前)

大佬，这个转换器具体怎么使用能否再详细说明一下吗？

---

### 评论 #5 (作者: JX79797, 时间: 22天前)

RRrjjqgg 由Fast Expression转化为Python alpha是起点 alpha，E5KO9Rg0 是最终优化结果。下面是完整优化路径：                                                          

  ---                                                                                                                           
  优化路径：RRrjjqgg → E5KO9Rg0                                                                                                 

  起点：RRrjjqgg（原始 alpha）                                                                                                  

  ┌────────────────┬─────────────┐
  │      指标      │     值      │                                                                                              
  ├────────────────┼─────────────┤                                                                                            
  │ Sharpe         │ 1.29        │
  ├────────────────┼─────────────┤
  │ Fitness        │ 1.22        │                                                                                              
  ├────────────────┼─────────────┤
  │ Turnover       │ 13.23%      │                                                                                              
  ├────────────────┼─────────────┤                                                                                            
  │ Neutralization │ STATISTICAL │
  ├────────────────┼─────────────┤
  │ Universe       │ TOP3000     │
  └────────────────┴─────────────┘                                                                                              

  信号逻辑：用 high/low 波动率（-std(H/L, 90天)）作为原始信号，外加 TVR 自适应平滑（binary search 调节 λ，目标瞬时 TVR≈5%），MAD
   标准化输出。问题在于：Sharpe 偏低（1.29），且信号纯粹依赖 H/L 波动率，缺乏方向性。                                         

  ---                                                                                                                         
  优化方向

  ┌─────────────────────────────────────┬──────────────────────────────────────────────┐
  │                问题                 │                   优化策略                   │                                        
  ├─────────────────────────────────────┼──────────────────────────────────────────────┤
  │ Sharpe 仅 1.29                      │ 引入方向性信号（均值回归）替代纯波动率       │                                        
  ├─────────────────────────────────────┼──────────────────────────────────────────────┤                                      
  │ 信号单一（仅 H/L 波动率）           │ 组合 Williams %R（超买超卖）+ NATR（波动率） │                                        
  ├─────────────────────────────────────┼──────────────────────────────────────────────┤                                        
  │ STATISTICAL 中性化风险              │ 切换为 SLOW_AND_FAST 中性化                  │                                        
  ├─────────────────────────────────────┼──────────────────────────────────────────────┤                                        
  │ TVR 平滑过于复杂（binary search λ） │ 简化为直接 zscore + MAD 标准化               │                                      
  └─────────────────────────────────────┴──────────────────────────────────────────────┘                                        

  ---                                                                                                                           
  终点：E5KO9Rg0（优化结果）                                                                                                  

  ┌────────────────┬─────────────────────────┐
  │      指标      │           值            │                                                                                  
  ├────────────────┼─────────────────────────┤                                                                                
  │ Sharpe         │ 1.75                    │
  ├────────────────┼─────────────────────────┤
  │ Fitness        │ 1.13                    │
  ├────────────────┼─────────────────────────┤
  │ Turnover       │ 18.79%                  │
  ├────────────────┼─────────────────────────┤                                                                                  
  │ 2Y Sharpe      │ 2.54                    │
  ├────────────────┼─────────────────────────┤                                                                                  
  │ Neutralization │ SLOW_AND_FAST           │                                                                                
  ├────────────────┼─────────────────────────┤                                                                                  
  │ Universe       │ TOP3000                 │
  ├────────────────┼─────────────────────────┤                                                                                  
  │ 提交就绪       │ ✅ PASS（全部检查通过） │                                                                                
  └────────────────┴─────────────────────────┘                                                                                  

  信号逻辑：                                                                                                                    
  - Williams %R(10)：-(willr + 50)/50，超卖（-100）→做多，超买（0）→做空，纯反转信号                                          
  - NATR(14)：-ATR/Close × 100，高波动→做空（避险），低波动→做多                                                                
  - 两者各 50% 权重 zscore 融合，MAD 鲁棒标准化                 

  ---                                                                                                                           
  关键改进                                                                                                                      

  RRrjjqgg                          E5KO9Rg0                                                                                  
  ───────────────────────────────────────────────────                                                                           
  信号：-std(H/L, 90d)              信号：WillR(10) + NATR(14)                                                                
  方向：无（纯波动率做空）           方向：均值回归 + 波动率                                                                    
  平滑：TVR binary search λ          平滑：直接 zscore/MAD                                                                      
  中性化：STATISTICAL               中性化：SLOW_AND_FAST                                                                       
  Sharpe：1.29                      Sharpe：1.75 (+35%)                                                                         
  提交状态：❓                       提交状态：✅ 全部PASS                                                                      

  ---                                                                                                                           
  提交检查（E5KO9Rg0）                                                                                                          

  所有关键检查 PASS：
  - LOW_SHARPE ✅ (1.75)                                                                                                        
  - LOW_FITNESS ✅ (1.13)                                                                                                       
  - LOW_TURNOVER / HIGH_TURNOVER ✅
  - SELF_CORRELATION ✅ (0.386)                                                                                                 
  - PROD_CORRELATION ✅ (0.617)                                                                                                 
  - LOW_2Y_SHARPE ✅ (2.54)

以下是提交的alpha截图

![图片](images/img_ce99c19fad.png)

---

### 评论 #6 (作者: XW25488, 时间: 21天前)

太厉害了吧老师，先收藏学习了

---

### 评论 #7 (作者: WZ33694, 时间: 17天前)

感谢分享，python alpha只能在Labs及wq平台回测吧。本地为何无法使用，请指教

---

