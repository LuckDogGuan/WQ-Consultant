# WorldQuant BRAIN Alpha 智能分数分配系统

- **链接**: WorldQuant BRAIN Alpha 智能分数分配系统.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 6

## 帖子正文

# WorldQuant BRAIN Alpha 智能分数分配系统

## 📊 系统概述

这是一个用于 WorldQuant BRAIN 平台的 Alpha 智能评分和分数分配系统。核心目标是将  **100,000 分** 按照 Alpha 质量智能分配，确保高质量、稳定且有趋势的 Alpha 获得更多资源。

## 🎯 核心特性

### 1. 多维度评分系统

系统采用  **6 个维度** 评估 Alpha 质量，并使用加权综合评分：

评分维度
权重
说明

 **Sharpe** 
25%
风险调整后收益

 **Fitness** 
25%
综合适应度

 **Returns** 
10%
累计收益率

 **Margin** 
15%
每股收益

 **Stability Score** 
10%
稳定性得分（PnL 曲线平滑度 + Sharpe 稳定性）

 **Trend Score** 
15%
趋势得分（近两年 PnL 趋势 + Sharpe 趋势）

所有指标先通过  **MinMaxScaler**  归一化到 0-100 分，然后加权求和。

### 2. 多阶段智能筛选

系统采用 **五层过滤机制** ，逐步筛选出高质量 Alpha：

```
┌─────────────────────────────────────────────────────────────┐
│  第 1 层：PPA 类型筛选（可选）                                 │
│  - ppa_only: 只选择 PowerPool Alpha                          │
│  - exclude_ppa: 排除 PowerPool Alpha                         │
│  - all: 不筛选                                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  第 2 层：OS (Out-of-Sample) 预筛选                           │
│  - 舍弃：OS Sharpe < 0.7                                      │
│  - 优先：OS Sharpe > 1.4 且 OS Margin > 0.001                │
│  - 保留：其他                                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  第 3 层：Margin 筛选（按区域差异化）                          │
│  - USA: Margin > 6.0 (bp)                                    │
│  - GLB/EUR: Margin > 10.0 (bp)                               │
│  - ASI: Margin > 15.0 (bp)                                   │
│  - Others: Margin > 10.0 (bp)                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  第 4 层：Returns 筛选                                         │
│  - USA: Returns > 5%                                          │
│  - Others: Returns > 4%                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  第 5 层：近两年 Sharpe 筛选                                   │
│  - 要求倒数第 2 年和倒数第 3 年的年度 Sharpe 均 > 1.0         │
└─────────────────────────────────────────────────────────────┘

```

### 3. 稳定性与趋势评分算法

#### 稳定性评分（Stability Score）

通过两个指标衡量 Alpha 的稳定性：

**a) PnL 曲线平滑度**

```
def calculate_stability_score(alpha_pnl_series, yearly_stats_df):
    stability_score = 0

    # 使用 Savitzky-Golay 滤波平滑 PnL 曲线
    smoothed = savgol_filter(pnl_clean, window_length=window_size, polyorder=3)

    # 计算实际 PnL 与线性拟合的均方误差（归一化）
    mse_val = raw_mse_vs_line / pnl_var

    # 评分标准
    if mse_val < 0.01: stability_score += 50    # 非常平滑
    elif mse_val < 0.05: stability_score += 30  # 较平滑
    elif mse_val < 0.1: stability_score += 10   # 一般

```

**b) Sharpe 比率稳定性**

```
    # 计算年度 Sharpe 的变异系数 (CV)
    cv_sharpe = yearly_stats_df['sharpe'].std() / yearly_stats_df['sharpe'].mean()

    if cv_sharpe < 0.1: stability_score += 50    # 非常稳定
    elif cv_sharpe < 0.2: stability_score += 30  # 较稳定
    elif cv_sharpe < 0.3: stability_score += 10  # 一般

```

#### 趋势评分（Trend Score）

评估 Alpha 是否处于上升趋势：

```
def calculate_trend_score(alpha_pnl_series, yearly_stats_df):
    trend_score = 0

    # 1. 近两年 PnL 趋势
    pnl_last_2_years = alpha_pnl_series[最近两年数据]
    slope, _ = np.polyfit(x_trend, pnl_last_2_years, 1)
    if slope > 0: trend_score += 50  # 上升趋势

    # 2. 年度 Sharpe 趋势
    slope_sharpe, _ = np.polyfit(x_yearly, yearly_stats_df['sharpe'], 1)
    if slope_sharpe > 0: trend_score += 50  # Sharpe 提升

    return trend_score

```

### 4. 金字塔类别轮次选择

为确保不同金字塔类别都有代表，系统采用 **轮次选择机制** ：

```
第 1 轮：从每个金字塔类别中选出得分最高的 1 个 Alpha
         ↓
第 2 轮：从每个金字塔类别的剩余 Alpha 中再选出得分最高的 1 个
         ↓
第 3 轮：重复...
         ↓
第 N 轮：直到某轮无新 Alpha 可选，或达到预设轮次上限

```

**配置参数** ：

```
num_selection_rounds = 7  # 轮次数量（可配置）

```

**特殊处理** ：

- 对于包含  `trade_when`  的 Alpha，使用 **第二个金字塔类别** 作为分类依据

### 5. 分数分配策略

#### 模式 1：等权重分配

```
def allocate_scores_equally(df, total_points=100000):
    n = len(df)
    score_per_alpha = total_points // n
    remainder = total_points % n

    # 平均分配
    df['allocated_score'] = score_per_alpha
    # 余数分配给前 N 个
    df.loc[df.index[:remainder], 'allocated_score'] += 1

```

#### 模式 2：按排名权重分配（几何级数）

```
def allocate_scores_by_rank(df, total_points=100000):
    n = len(df)

    # 使用几何级数，确保排名第 1 的权重是最后一名的 2 倍
    r = 2 ** (1/(n-1))
    weights = [r ** (n - i) for i in range(1, n+1)]
    weights = weights / weights.sum()

    # 分配分数
    df['allocated_score'] = (weights * total_points).astype(int)

```

**配置参数** ：

```
equal_allocation_mode = False  # True: 等权重，False: 按排名

```

### 6. 多轮重试分配机制

为确保  **100,000 分完全分配** ，系统采用多轮重试：

```
┌─────────────────────────────────────────────────────────────┐
│  第 1 阶段：首次分配                                           │
│  - 按计算好的分数为每个 Alpha 调用 API                         │
│  - 记录成功/失败的 Alpha                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
          ┌──────────────────────────┐
          │  是否有失败的分数？       │
          └──────────────────────────┘
                   ↓ 是
┌─────────────────────────────────────────────────────────────┐
│  第 2 阶段：重新分配（第 1 轮）                                │
│  - 将失败的分数平均分配给成功的 Alpha                          │
│  - 为成功的 Alpha 追加奖金分数                                 │
│  - 为成功的 Alpha 追加奖金分数                                 │
│  - 记录本轮成功/失败                                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
          ┌──────────────────────────┐
          │  是否还有失败的分数？     │
          └──────────────────────────┘
                   ↓ 是
┌─────────────────────────────────────────────────────────────┐
│  第 3-N 阶段：继续重新分配                                     │
│  - 重复第 2 阶段逻辑，最多重试 10 轮                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
          ┌──────────────────────────┐
          │  达到最大轮次仍有剩余？   │
          └──────────────────────────┘
                   ↓ 是
┌─────────────────────────────────────────────────────────────┐
│  最后尝试：强制分配                                            │
│  - 将所有剩余分数强制分配给第 1 个成功的 Alpha                 │
└─────────────────────────────────────────────────────────────┘

```

**关键代码示例** ：

```
# 第 2 阶段：重新分配失败的分数
total_lost_score = sum(失败的分数)
num_successful = len(成功的 Alpha)

bonus_per_alpha = total_lost_score // num_successful
remainder = total_lost_score % num_successful

for i, alpha in enumerate(成功的 Alpha):
    bonus = bonus_per_alpha
    if i < remainder:
        bonus += 1

    new_total_score = alpha.current_score + bonus
    # 调用 API 更新分数
    update_alpha_score(alpha_id, new_total_score)

```

## 🔧 核心配置参数

```
config = {
    # 基础配置
    'advisor_date': datetime(2025, 7, 1),      # 顾问开始日期
    'target_region': "USA",                     # 目标地区
    'page_limit': 100,                          # 每页获取数量

    # PPA 筛选模式
    'ppa_filter_mode': "ppa_only",              # "ppa_only" | "exclude_ppa" | "all"

    # OS 筛选配置
    'enable_os_filtering': True,                # 是否启用 OS 筛选
    'os_sharpe_threshold_high': 1.4,            # OS Sharpe 高阈值（优先）
    'os_sharpe_threshold_low': 0.7,             # OS Sharpe 低阈值（舍弃）
    'os_margin_threshold': 0.001,               # OS Margin 阈值

    # 轮次选择配置
    'num_selection_rounds': 7,                  # 金字塔轮次数

    # 分配模式
    'equal_allocation_mode': False,             # True: 等权重，False: 按排名

    # 清空分数配置
    'clear_osmosis_points_before_allocation': True,  # 分配前清空现有分数
    'clear_only_mode': False,                   # 只清空模式

    # CSV 分配模式（可选）
    'use_csv_allocation_mode': False,           # 是否使用 CSV 文件分配
    'csv_allocation_filepath': "allocation.csv", # CSV 文件路径

    # 并发配置
    'MAX_WORKERS_OS_FETCH': 10,                 # OS 数据获取线程数
    'MAX_WORKERS_CLEAR': 4,                     # 清空操作线程数
    'MAX_WORKERS_APPLY': 4,                     # 应用分数线程数
}

```

## 📈 运行流程示例

### 模式 1：动态计算和分配（推荐）

```
from osmosis import *
from machine_lib import login

# 初始化登录
session = login()

# 配置参数
config = {
    'advisor_date': datetime(2025, 7, 1),
    'target_region': "USA",
    'ppa_filter_mode': "ppa_only",
    'enable_os_filtering': True,
    'equal_allocation_mode': False,
    'num_selection_rounds': 7
}

# 执行完整流程
# 1. 清空现有分数（可选）
run_clear_osmosis_points(session, config)

# 2. 获取并处理 Alpha
final_df, smallest_pyramids = get_and_process_alphas(session, config)

# 3. 分配分数并更新
config['smallest_pyramid_categories'] = smallest_pyramids
execute_allocation_and_updates(session, final_df, config)

```

### 模式 2：从 CSV 文件分配

```
config = {
    'use_csv_allocation_mode': True,
    'csv_allocation_filepath': 'my_allocation.csv',
    'target_region': 'USA',
    'clear_osmosis_points_before_allocation': True
}

# 清空指定区域的分数
run_clear_osmosis_points(session, config, regions_to_clear=['USA'])

# 应用 CSV 中的分数
load_and_apply_scores_from_csv(session, config)

```

### 模式 3：只清空模式

```
config = {
    'clear_only_mode': True,
    'target_region': 'GLB',
    'MAX_WORKERS_CLEAR': 8
}

# 只清空指定区域的所有分数
run_clear_osmosis_points(session, config, regions_to_clear=['GLB'])

```

## 📊 输出示例

### 控制台输出

```
====================================================================================
PPA 筛选模式：只获取包含 'PowerPoolSelected' 标签的 Alpha（PPA类型）
====================================================================================

PPA 筛选统计（只保留PPA）:
  - API 返回的总 Alpha 数: 450
  - 过滤掉的非PPA Alpha 数: 180
  - 最终保留的 PPA Alpha 数: 270
====================================================================================

====================================================================================
执行 OS (Out-of-Sample) 预筛选
====================================================================================
OS Sharpe 高阈值: > 1.4 (优先筛选)
OS Sharpe 低阈值: < 0.7 (直接舍弃)
OS Margin 阈值: > 0.001
====================================================================================

OS 筛选结果统计:
  - 舍弃 (OS Sharpe < 0.7): 45 个
  - 优先 (OS Sharpe > 1.4 且 OS Margin > 0.001): 78 个
  - 保留 (其他): 147 个
  - 总计保留: 225 个
====================================================================================

DEBUG: Number of alphas after all filters: 84

====================================================================================
ALPHA金字塔分布数据 (初始统计)
====================================================================================
EARNINGS              32
TECHNICAL_VOLATILITY  28
SENTIMENT             24
====================================================================================

--- 第 1 轮选择 ---
  - 在类别 'EARNINGS' 中选中 Alpha: ABC123xyz (得分: 87.45)
  - 在类别 'TECHNICAL_VOLATILITY' 中选中 Alpha: DEF456uvw (得分: 85.32)
  - 在类别 'SENTIMENT' 中选中 Alpha: GHI789rst (得分: 82.17)

--- 第 2 轮选择 ---
  - 在类别 'EARNINGS' 中选中 Alpha: JKL012opq (得分: 79.88)
  ...

最终选中的 Alpha 数量: 21

====================================================================================
第 1 阶段：首次尝试分数分配
====================================================================================

处理排名 #1 的 Alpha: ABC123xyz (尝试分配 8547 分)
  - ✓ 成功更新 Alpha ABC123xyz 的分数为 8547

处理排名 #2 的 Alpha: DEF456uvw (尝试分配 7892 分)
  - ✓ 成功更新 Alpha DEF456uvw 的分数为 7892

...

====================================================================================
第 2 阶段：重新分配 1234 点损失分数
====================================================================================
共有 19 个成功的 Alpha，每个将额外获得 64 分。
前 18 个 Alpha 将再额外获得 1 分以确保分数完全分配。

✓ 所有分数已成功分配！

====================================================================================
最终分配汇总
====================================================================================
初始选中 Alpha 数量: 21
第一阶段成功分配 Alpha 数量: 19
第一阶段失败数量: 2
重新分配执行轮次数: 1

分配结果:
✅ 分数分配完成：最终成功分配总分数 100000 分，无分数损耗。

评分权重:
  - Sharpe: 25%
  - Fitness: 25%
  - Returns: 10%
  - Margin: 15%
  - Stability Score: 10%
  - Trend Score: 15%

统计信息:
  - 选中的Alpha数量: 21
  - 最高得分: 87.45
  - 最低得分: 52.13
  - 平均得分: 71.28
  - 最高分配分数: 8612
  - 最低分配分数: 2347

✓ 详细结果已保存到: alpha_allocation_USA_20250328_153042.csv

```

### CSV 输出文件

保存的 CSV 文件包含以下列：

```
id, sharpe, fitness, returns, margin, stability_score, trend_score,
normalized_score, rank, allocated_score, pyramidCategory, code,
os_sharpe, os_margin, ...

```

## 💡 设计亮点

1. **多维度综合评估** ：不仅考虑传统指标（Sharpe、Fitness），还引入稳定性和趋势评分
2. **差异化筛选标准** ：根据不同地区设置不同的 Margin 阈值
3. **OS 数据预筛选** ：利用样本外数据提前过滤低质量 Alpha
4. **金字塔类别平衡** ：确保不同策略类型都有代表
5. **100% 分数分配** ：通过多轮重试机制确保分数完全分配，无浪费
6. **灵活配置** ：支持多种运行模式（动态计算、CSV 文件、只清空）
7. **并发优化** ：使用 ThreadPoolExecutor 加速 API 调用

## 🚀 扩展建议

1. **机器学习优化** ：可以训练模型预测 Alpha 未来表现，替代手工权重
2. **动态权重调整** ：根据市场环境自动调整各维度权重
3. **风险分散** ：增加相关性检查，避免选中高度相关的 Alpha
4. **回测验证** ：对历史数据进行回测，优化筛选阈值
5. **实时监控** ：定期重新评分和调整分数分配

## 📝 总结

这个系统通过 **多层筛选 + 多维度评分 + 智能分配** 的方式，实现了 Alpha 资源的最优配置。核心优势在于：

- ✅  **科学性** ：基于统计学方法（变异系数、线性拟合、平滑滤波）
- ✅  **稳健性** ：多轮重试机制确保分数完全分配
- ✅  **灵活性** ：支持多种配置模式，适应不同需求
- ✅  **高效性** ：并发处理 + 增量更新

欢迎讨论和交流优化建议！🎉

**免责声明** ：本系统仅供学习和研究使用，不构成投资建议。使用时请遵守平台规则。

---------------来自JX79797的研究助手

---

## 讨论与评论 (0)

