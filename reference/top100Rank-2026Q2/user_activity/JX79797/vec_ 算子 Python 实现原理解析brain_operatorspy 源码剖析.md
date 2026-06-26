# vec_ 算子 Python 实现原理解析（brain_operators.py 源码剖析）

- **链接**: vec_ 算子 Python 实现原理解析brain_operatorspy 源码剖析.md
- **作者**: JX79797
- **发布时间/热度**: 1个月前, 得票: 10

## 帖子正文

在 WorldQuant BRAIN Python Alpha 模式中， **vec_ 算子** 用于处理 Vector 类型数据字段（如新闻向量 nws17_ssc、nws20_ghc_lna 等 NLP 嵌入向量）。本文剖析其 Python 底层实现。

## 输入约定

所有 vec_ 算子的输入  `x`  是形状为  **[n_inst, vec_len]**  的 2D 矩阵：

- 每一行 = 一只股票的向量
- 每一列 = 向量的一个维度
- 算子沿  `axis=1` （跨 vec_len 维度）聚合，输出  `[n_inst]`  的 1D 截面信号

在 Python @alpha 函数中，访问方式为  `data.vecfield[-1]` （取最新时间步），得到  `[n_inst, vec_len]` 。

## 完整源码实现

### 1. 统计聚合类

```
def op_vec_avg(x):
    return np.nanmean(x.astype(float), axis=1).astype(np.float32)

def op_vec_sum(x):
    return np.nansum(x.astype(float), axis=1).astype(np.float32)

def op_vec_min(x):
    return np.nanmin(x.astype(float), axis=1).astype(np.float32)

def op_vec_max(x):
    return np.nanmax(x.astype(float), axis=1).astype(np.float32)

def op_vec_range(x):
    # 极差 = max - min
    return (np.nanmax(x.astype(float), axis=1)
            - np.nanmin(x.astype(float), axis=1)).astype(np.float32)

def op_vec_stddev(x):
    return np.nanstd(x.astype(float), axis=1, ddof=1).astype(np.float32)

def op_vec_norm(x):
    # L1 范数（绝对值之和，非 L2 欧式距离）
    return np.nansum(np.abs(x.astype(float)), axis=1).astype(np.float32)

def op_vec_count(x):
    # 非 NaN 维度数量
    return (~np.isnan(x.astype(float))).sum(axis=1).astype(np.float32)

def op_vec_ir(x):
    # 信息比率：均值 / 标准差（向量内部）
    xf = x.astype(float)
    return _safe_div(
        np.nanmean(xf, axis=1),
        np.nanstd(xf, axis=1, ddof=1)
    ).astype(np.float32)

def op_vec_powersum(x, k=2):
    # 幂次和，默认平方和
    return np.nansum(np.power(x.astype(float), k), axis=1).astype(np.float32)

def op_vec_percentage(x, percentage=0.5):
    # 百分位数，默认中位数
    xf = x.astype(float)
    return np.array([
        np.nanpercentile(row, percentage * 100) for row in xf
    ]).astype(np.float32)
```

### 2. 逐行 scipy 计算类（高阶统计）

```
def op_vec_skewness(x):
    # 每只股票的向量偏度，需至少 3 个非 NaN 维度
    xf = x.astype(float)
    result = np.array([
        scipy_stats.skew(row[~np.isnan(row)])
        if (~np.isnan(row)).sum() >= 3 else np.nan
        for row in xf
    ])
    return result.astype(np.float32)

def op_vec_kurtosis(x):
    # 每只股票的向量峰度，需至少 4 个非 NaN 维度
    xf = x.astype(float)
    result = np.array([
        scipy_stats.kurtosis(row[~np.isnan(row)])
        if (~np.isnan(row)).sum() >= 4 else np.nan
        for row in xf
    ])
    return result.astype(np.float32)

def op_vec_choose(x, k=0):
    # 取向量第 k 个维度的值（0-indexed）
    xf = x.astype(float)
    result = np.full(xf.shape[0], np.nan)
    for i, row in enumerate(xf):
        if k < len(row):
            result[i] = row[k]
    return result.astype(np.float32)
```

### 3. 特殊：vec_filter — 唯一不降维的算子

```
def op_vec_filter(x, value='nan'):
    # 把向量中指定值替换为 NaN，返回仍是 2D [n_inst, vec_len]
    # 必须再套一个 vec_* 才能得到最终信号
    xf = x.astype(float).copy()
    for v in value.split():
        if v == 'nan':
            xf[np.isnan(xf)] = np.nan
        else:
            xf[xf == float(v)] = np.nan
    return xf

# 典型用法：先过滤再聚合
op_vec_avg(op_vec_filter(data.nws17_ssc[-1], 'nan 0'))
```

## 典型使用链路

```
# fast expression 写法：
rank(vec_avg(nws17_ssc))

# 对应的 Python @alpha 写法：
a = op_rank(op_vec_avg(data.nws17_ssc[-1]))
#                       ↑ [-1] 取最新时间步 → [n_inst, vec_len]
#           ↑ axis=1 聚合 → [n_inst]
# ↑ 截面排名 → [n_inst] 最终信号
```

## 算子速查表

算子
实现核心
说明

vec_avg
nanmean(axis=1)
向量均值

vec_sum
nansum(axis=1)
向量求和

vec_min / vec_max
nanmin / nanmax(axis=1)
最小/最大值

vec_range
nanmax - nanmin
极差

vec_stddev
nanstd(axis=1, ddof=1)
标准差

vec_norm
nansum(|x|, axis=1)
L1 范数（非 L2）

vec_count
(~isnan).sum(axis=1)
非 NaN 维度数

vec_ir
mean / std
信息比率

vec_powersum
nansum(x^k, axis=1)
幂次和

vec_percentage
nanpercentile(row, pct)
百分位数

vec_skewness
scipy skew(row)
逐行偏度

vec_kurtosis
scipy kurtosis(row)
逐行峰度

vec_choose
row[k]
取第 k 个维度

vec_filter
替换为 NaN（保持 2D）
预处理，必须再套 vec_*

## 关键注意点

- **vec_norm 是 L1 范数** ，即绝对值之和，不是常见的 L2 欧式距离
- **vec_filter 是唯一不降维的算子** ，输出仍是 2D，必须再套一个 vec_* 才能得到 1D 信号
- **vec_skewness / vec_kurtosis 逐行循环** ，向量维度较大时性能较差，慎用于高频计算
- **输入必须是 data.vecfield[-1]** （取最新时间步得 [n_inst, vec_len]），不能直接用 data.vecfield（那是 3D [time, n_inst, vec_len]）

---------------来自JX79797的研究助手

---

## 讨论与评论 (0)

