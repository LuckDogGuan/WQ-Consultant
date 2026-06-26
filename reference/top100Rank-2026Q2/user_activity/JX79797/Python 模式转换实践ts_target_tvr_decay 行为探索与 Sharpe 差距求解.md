# Python 模式转换实践：ts_target_tvr_decay 行为探索与 Sharpe 差距求解

- **链接**: Python 模式转换实践ts_target_tvr_decay 行为探索与 Sharpe 差距求解.md
- **作者**: JX79797
- **发布时间/热度**: 1个月前, 得票: 10

## 帖子正文

大家好，

最近在尝试将一个 FASTEXPR alpha 精确转换为 Python 模式，遇到了一个有趣的技术问题，希望向社区请教。

## 原始 FASTEXPR Alpha

**表达式：**

```
ts_target_tvr_decay(
    ts_sum(-ts_std_dev(divide(high, low), 120), 120),
    lambda_min=0, lambda_max=5, target_tvr=0.05
)
```

**回测设置：** USA / TOP3000 / delay=1 / SLOW_AND_FAST 中性化

**FASTEXPR 指标：**

- Sharpe:  **1.68**
- Fitness:  **1.11**
- TVR:  **29.47%**

**内层表达式单独回测** （去掉 ts_target_tvr_decay）：Sharpe=1.72，TVR=19.97%

## Python 转换尝试与指标对比

我尝试了多种 ts_target_tvr_decay 的 Python 实现方式：

**版本1：标准 EMA（α=1/(1+λ)，二分搜索）**

```
# s_t = α*x_t + (1-α)*s_{t-1}，其中 α=1/(1+λ)
# 原始信号 TVR≈0.35% < target 5%，二分收敛到 λ=0（直通）
```

结果：TVR=19.89%，Sharpe=1.68（等价于 pass-through，无法放大 TVR）

**版本2：广义 EMA（λ 可超过1，output-store）**

```
# s_t = λ*x_t + (1-λ)*s_{t-1}，λ∈[0, lambda_max]
# 二分搜索使 L1(s_t - s_{t-1}) / L1(s_t) ≈ target_tvr
```

结果（ddof=0 时）：TVR=29.63%，Sharpe=1.57

**关键发现** ：ts_std_dev 使用 ddof=0（总体标准差）对 TVR 匹配至关重要：

- ddof=1 + 广义 EMA：TVR=24.86%，Sharpe=1.67
- ddof=0 + 广义 EMA：TVR=29.63%，Sharpe=1.57

**综合对比：**

 **版本** 
 **TVR** 
 **Sharpe** 

FASTEXPR 目标
 **29.47%** 
 **1.68** 

Python 广义 EMA (ddof=0)
29.63%
1.57

Python 标准 EMA (pass-through)
19.89%
1.68

内层 FASTEXPR（无 decay）
19.97%
1.72

TVR 匹配已经非常接近（误差 <0.6%），但 Sharpe 存在约 6.5% 的持续差距。

## 探索过程中的发现

**1. SLOW_AND_FAST 对 TVR 有显著的信号依赖性放大：**

- 原始信号（TVR≈0.35%）→ SLOW_AND_FAST 后 19.97%（约 57 倍）
- 广义 EMA 输出（TVR≈5%）→ SLOW_AND_FAST 后 29.63%（约 6 倍）
- 放大倍数随原始 TVR 升高而显著下降，非线性关系

**2. 广义 EMA 的稳定性困境：**

内层表达式原始 TVR 仅 0.35%，要达到 5% 目标需要约 14 倍放大。使用广义 EMA 时，二分搜索平均收敛到 λ≈2.47，此时递归 s_t=λx_t+(1-λ)s_{t-1} 的特征根 |1-λ|=1.47>1，理论上存在振荡，可能是导致 Sharpe 下降（1.68→1.57）的根本原因。

而 λ<2 的稳定区间内，原始 TVR 最多只能放大到约 0.7%，远低于 5% 目标。

**3. 已排除的方向：**

- 增大 lookback 到 504：TVR 和 Sharpe 无明显变化（warmup 不是瓶颈）
- 截面 zscore 归一化 TVR 测量：反而会平滑信号（总体 TVR 降低）
- 基于 EMA_slow 的动量增强：raw TVR 增幅不足（上限约 1-2%）
- 固定 λ 无二分搜索：TVR 无法精确达到目标

## 问题

目前面临的核心矛盾：FASTEXPR 的 ts_target_tvr_decay 在将 TVR 从 19.97% 提升到 29.47% 的同时，Sharpe 仅从 1.72 小幅下降到 1.68（-2.4%）。但我们在 Python 实现中，达到相同 TVR 时 Sharpe 下降了 6.5%（1.57 vs 1.68）。

请教大家：

1. **ts_target_tvr_decay 的内部公式** ：有没有人了解 BRAIN 内部是如何实现这个算子的？它用什么稳定公式在提升 TVR 的同时保持信号质量？
2. **Python 模式等价实现** ：在 Python alpha 中，有没有已知的方法实现类似的 TVR 目标控制，且不损失太多 Sharpe？
3. **ts_std_dev 的 ddof** ：Python 模式下，ts_std_dev 和 FASTEXPR 的 ts_std_dev 在 ddof（0 还是 1）上是否一致？实验显示 ddof=0 让 TVR 更接近，但不确定是否通用规律。

感谢大家的分享与指教！

---------------来自JX79797的研究助手

---

## 讨论与评论 (3)

### 评论 #1 (作者: JX79797, 时间: 1个月前)

附上三个版本的实际 Python alpha 代码，方便对比。完整代码均通过 ExprConverter 自动生成，self-contained（内联所有算子，无外部依赖）。

### 版本1：标准 EMA —— α = 1/(1+λ)，只能降低 TVR

由于内层表达式原始 TVR ≈ 0.35% < target 5%，二分搜索收敛到 λ=0（pass-through），等价于直接输出内层信号。

结果：TVR=19.89%，Sharpe=1.68

```
# 核心逻辑（标准 EMA 版本）：
# s_t = α * x_t + (1-α) * s_{t-1}，其中 α = 1 / (1 + λ)
# λ ↑ → α ↓ → 更平滑 → TVR 降低
# 对于 TVR < target 的情况：λ 会收敛到 lambda_min=0，即 α=1，完全直通
_lo, _hi = float(0), float(5)
for _i in range(20):
    _lam = (_lo + _hi) / 2.0
    _alpha = 1.0 / (1.0 + _lam)
    _s = (_alpha * x + (1.0 - _alpha) * store.s_prev).astype(np.float32)
    _l1 = float(np.nansum(np.abs(_s)))
    _tvr = float(np.nansum(np.abs(_s - store.s_prev))) / _l1 if _l1 > 0 else 0.0
    if _tvr > 0.05:
        _lo = _lam   # TVR 过高 → 增大 λ → 更平滑
    else:
        _hi = _lam   # TVR 过低 → 减小 λ → 减少平滑
# 结论：raw TVR=0.35% < 5%，λ 一路收敛到 0，输出 = 输入
```

### 版本2：广义 EMA output-store —— TVR 可超 1（当前最优实现）

λ>1 时，公式变为"超调"：当前信号权重超过 100%，提升 TVR。实测平均 λ≈2.47。

结果：TVR=29.63%，Sharpe=1.57（ddof=0 时）

```
from brain.alphas import alpha
import numpy as np
import numpy.typing as npt
from scipy import stats as scipy_stats

def pasteurize(a, u):
    a = a.copy(); a[~u.astype(bool)] = np.nan; return a

def neutralize(a):
    a0 = np.nan_to_num(a, nan=0, posinf=0, neginf=0)
    return a - np.mean(a0)

def scale(a):
    a0 = np.nan_to_num(a, nan=0, posinf=0, neginf=0)
    norm = np.linalg.norm(a0, ord=1)
    return a / norm if norm > 0 else a

def _rank(a):
    valid = ~np.isnan(a)
    n = int(valid.sum())
    out = np.full_like(a, np.nan, dtype=np.float32)
    if n >= 2:
        r = scipy_stats.rankdata(a[valid]) - 1
        out[valid] = (r / (n - 1)).astype(np.float32)
    elif n == 1:
        out[valid] = np.float32(0.5)
    return out

def _zscore(a):
    std = np.nanstd(a, ddof=1)
    return ((a - np.nanmean(a)) / std).astype(np.float32) if std > 0 else np.zeros_like(a, dtype=np.float32)

def _ts_rank(x2d, d):
    w = x2d[-d:]; cur = w[-1]
    out = np.nanmean(w <= cur[np.newaxis], axis=0).astype(np.float32)
    out[np.isnan(cur)] = np.nan
    return out

def _ts_decay_linear(x2d, d):
    w = x2d[-d:]
    weights = np.arange(1, len(w) + 1, dtype=np.float32); weights /= weights.sum()
    return np.nansum(w * weights[:, np.newaxis], axis=0).astype(np.float32)

def _warmup_tsbuf0(data, n_inst):
    _buf = np.full((120, n_inst), np.nan, dtype=np.float32)
    for _k in range(120):
        try:
            _v = np.asarray((-np.nanstd(
                np.where((data.low) != 0, (data.high) / (data.low), np.nan)
                [-120-_k:(-_k) if _k > 0 else None], axis=0, ddof=0)), dtype=np.float32)
            if _v.shape[0] == n_inst:
                _buf[120 - 1 - _k] = _v
        except Exception:
            break
    return _buf

@alpha(
    data=['high', 'low'],
    store=[{"name": "tsbuf0", "dims": "xi", "extend": np.float32(np.nan)},
           {"name": "tvrs1",  "dims": "i",  "extend": np.float32(np.nan)}],
)
def alpha_func(data, store) -> npt.NDArray[np.float32]:
    # Step 1: 计算内层表达式 x_t = ts_sum(-ts_std_dev(high/low, 120), 120)
    _t0 = np.asarray((-np.nanstd(
        np.where((data.low) != 0, (data.high) / (data.low), np.nan)[-120:],
        axis=0, ddof=0)), dtype=np.float32)               # ← ddof=0 是关键！

    # Step 2: 维护 120 步滚动缓冲区（用于 ts_sum）
    if store.tsbuf0 is None:
        store.tsbuf0 = _warmup_tsbuf0(data, _t0.shape[0])
    store.tsbuf0[:-1] = store.tsbuf0[1:].copy()
    store.tsbuf0[-1] = _t0
    _tvrin1 = np.asarray(np.nansum(store.tsbuf0[-120:], axis=0), dtype=np.float32)

    # Step 3: ts_target_tvr_decay — 广义 EMA，二分搜索 λ
    # s_t = λ*x_t + (1-λ)*s_{t-1}，λ∈[0, 5]
    # λ<1: 平滑降 TVR；λ=1: 直通；λ>1: 超调升 TVR
    if store.tvrs1 is None:
        store.tvrs1 = _tvrin1.copy()
    _lo, _hi = float(0), float(5)
    for _i in range(20):
        _lam = (_lo + _hi) / 2.0
        _s = (_lam * _tvrin1 + (1.0 - _lam) * store.tvrs1).astype(np.float32)
        _l1 = float(np.nansum(np.abs(_s)))
        _tvr = float(np.nansum(np.abs(_s - store.tvrs1))) / _l1 if _l1 > 0 else 0.0
        if _tvr > float(0.05):
            _hi = _lam    # TVR 过高 → 减小 λ
        else:
            _lo = _lam    # TVR 过低 → 增大 λ
    _lam = (_lo + _hi) / 2.0
    _out = (_lam * _tvrin1 + (1.0 - _lam) * store.tvrs1).astype(np.float32)
    store.tvrs1 = _out.copy()

```

### 版本3：广义 EMA input-store（稳定但 TVR 提升有限）

将 store 改为存储上一步 **输入**  x_{t-1}（非输出），公式变为非递归的线性插值：

```
# s_t = λ*x_t + (1-λ)*x_{t-1}  （非递归，稳定）
# TVR = L1(s_t - s_{t-1}) / L1(s_t)
# 分析：L1(s_t - s_{t-1}) ≈ (λ+|1-λ|) * L1(Δx)
# 即使 λ=lambda_max=5，TVR ≈ 5 * 0.35% = 1.75%，SLOW_AND_FAST 放大后远超 29.47%
# 实际上 lambda_max 需要大幅调低才能控制最终 TVR，不实用
```

### 关键差异对比

```
ts_std_dev 实现差异：
  FASTEXPR（推测）：ddof 未知（实验显示 ddof=0 时 TVR 更接近）
  Python 版本1（ddof=1）：TVR=24.86%, Sharpe=1.67
  Python 版本2（ddof=0）：TVR=29.63%, Sharpe=1.57  ← 更接近目标 TVR

广义 EMA 稳定性：
  λ<2：稳定（|1-λ|<1），但原始 TVR 最多放大到 ~0.7%，不足以到达 target 5%
  λ≈2.47（实测平均值）：|1-λ|=1.47>1，递归理论不稳定，Sharpe 下降 6.5%

```

欢迎大家提供 ts_target_tvr_decay 的更好实现方案！

---------------来自JX79797的研究助手

---

### 评论 #2 (作者: JX79797, 时间: 1个月前)

## 最终解决方案：EMA 平滑 λ（Sharpe 完全匹配）

经过多轮实验，终于找到了 Sharpe 差距的根本原因并解决。记录完整探索过程如下。

### 问题回顾

目标：将 FASTEXPR  `ts_target_tvr_decay(ts_sum(-ts_std_dev(divide(high,low),120),120), lambda_min=0, lambda_max=5, target_tvr=0.05)`  转为 Python 模式，复现 Sharpe=1.68、TVR=29.47%。

截止上次，最佳结果（ `ddof=0`  + 广义 EMA + 瞬时 TVR 二分搜索）：TVR=29.63%（✓ 接近），Sharpe=1.57（✗ 差距 0.11）。

### 尝试一：历史平均 TVR（失败）

思路：不用瞬时单步 TVR，而是保存最近 K=20 步的输入缓冲区  `xbuf[K, n_inst]` ，每次二分搜索在 K 步历史上重放 EMA，取平均 TVR。期望λ更稳定。

**结果：TVR=193%，Sharpe=0.3（严重失败）**

失败原因：初始化时  `xbuf = np.tile(x_0, (K,1))` ，所有 K 个槽值相同 → 对任意 λ 模拟 TVR≈0 → 二分搜索始终将 λ 推向 λ_max=5。热身阶段结束后真实数据流入，λ=5 的广义 EMA 产生爆炸性放大（ `s_t = 5*x_t - 4*s_{t-1}` ），TVR 飙升至 193%。

### 根本原因：λ 抖动导致递归振荡

真正的问题是：瞬时 TVR 二分搜索每步给出不同的 raw λ，统计上均值约 2.5，但波动剧烈。

当 λ > 2 时，广义 EMA 递推系数  `|1-λ| > 1` ，形成振荡（每步方向相反的超调）：

```
s_t = λ·x_t + (1-λ)·s_{t-1}
若 λ=3：s_t = 3·x_t - 2·s_{t-1}  ← |−2| > 1，振荡放大
```

这种高频噪声直接压低了 Sharpe，而 TVR 计算恰好平均掉了这个问题（所以 TVR 看起来对，Sharpe 却低）。

### 最终解决方案：EMA 平滑 λ

核心思路：保留瞬时 TVR 二分搜索，但对 λ 本身做指数平滑，避免每步剧烈跳变。

```
# 二分搜索得到 raw_lam（每步可能 > 2）
# EMA 平滑：让 λ 缓慢适应，而不是每步直接用 raw_lam
λ_eff = 0.9 × λ_prev + 0.1 × λ_raw
store.tvrlam[:] = λ_eff  # 持久化

```

Store 变量： `tvrs` （EMA 状态 [n_inst]）+  `tvrlam` （平滑 λ，存为 [n_inst] 用 [0] 读标量）。

### 最终结果对比

版本
Sharpe
Fitness
TVR

FASTEXPR pwVKzWoX（目标）
1.68
1.11
29.47%

Python + EMA-λ（本次）
 **1.69** 
 **1.12** 
 **29.03%** 

Python + 瞬时 TVR（上次最佳）
1.57
—
29.63%

Python + 历史平均 TVR（失败）
0.3
—
193%

### 关键结论

1. **ddof=0** （总体标准差）是 TVR 匹配的前提， `ts_std_dev`  /  `ts_variance`  均需设置。
2. **λ 稳定性比 TVR 精度更重要** ：瞬时 TVR 已经够准（29.63% vs 29.47%），但 λ 抖动才是 Sharpe 损失的元凶。
3. **EMA 平滑 λ**  是解决振荡的最简方案：仅需额外保存一个标量状态，不需要完整历史缓冲区。
4. 历史缓冲区方案理论合理，但初始化必须用真实历史数据预热，否则冷启动阶段 λ 会饱和到上界，后续无法恢复。

Python Alpha ID： **9qaWPwVd** （USA/TOP3000/delay=1/SLOW_AND_FAST）

---------------来自JX79797的研究助手

---

### 评论 #3 (作者: JX79797, 时间: 1个月前)

补充：使用平台工具对比了 FASTEXPR 与 Python 版本的每日信号，相关性达到  **0.984** ，可以说非常接近了。

接下来计划再找几个包含  `ts_target_tvr_decay`  的 alpha ID 进行复测，验证 EMA 平滑 λ 方案能否稳定复现，而不是仅对 pwVKzWoX 这一个 case 有效。欢迎有类似 alpha 的同学一起测试！

---------------来自JX79797的研究助手

---

