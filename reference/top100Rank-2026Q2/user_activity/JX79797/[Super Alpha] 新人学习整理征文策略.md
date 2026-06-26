# [Super Alpha] 新人学习，整理征文策略

- **链接**: [Super Alpha] 新人学习整理征文策略.md
- **作者**: JX79797
- **发布时间/热度**: 10个月前, 得票: 26

## 帖子正文

[../JR23144/[Commented] 【有奖】SuperAlpha征文分享你独到的selection和combination方法.md](../JR23144/[Commented] 【有奖】SuperAlpha征文分享你独到的selection和combination方法.md)

整理各位前辈的策略，并使用 三维度质量控制 结合自己的一些策略，成功提交出自己的第一个super alpha，值得新人学习

![图片](images/img_916aad8b18.jpeg)  ![图片](images/img_68b8ae323e.jpeg)

### 一、基础筛选策略

#### 1. ​ **因子拼图策略** ​（ZL29184）

- ​ **核心逻辑** ：筛选同质化Alpha降低组合冲突
- ​ **表达式** ：
  ```
  not(own) && universe=='TOP3000' && neutralization=='SECTOR' && dataset_count==1 && in(datasets,"fundamental6")
  ```
- ​ **关键参数** ：
  `Selection Handling=Positive` ,  `Selection Limit=6-20` （动态调整）
- ​ **优化方向** ：增加 `os_start_date>"2023-01-01"` 避免失效因子，按Universe规模加权

#### 2. ​ **三维度质量控制** ​（JB71859）

- ​ **表达式** ：
  ```
  (self_correlation<=0.5) * prod_correlation.between(0.15,0.6) * turnover.between(0.08,0.3) * pow(long_count+short_count,0.7)
  ```
- ​ **创新点** ：相关性阈值随市场波动动态计算：
  `corr_threshold = 0.6 - ts_std_dev(market_volatility,252)*0.1`

### 二、加权优化策略

#### 1. ​ **分层换手率加权** ​（ZS59763）

- ​ **表达式框架** ：
  ```
  ((turnover<0.07&&turnover>0.05)||(turnover<0.15&&turnover>0.13)||(turnover<0.12&&turnover>0.09)) && operator_count>3 && operator_count<13/(turnover*s_log_1p(turnover)*sigmoid(self_correlation)*sigmoid(prod_correlation)*abs(long_count-short_count))
  ```
- **核心函数** ：
  `turnover_binning()` 实现换手率自适应分箱（避免硬编码）
- ​ **权重设计** ： `log(long_count*short_count)` 提升稳定性

#### 2. ​ **多因子融合评分** ​（LA79055）

- ​ **动态权重模块** ：
  ```
  fundamental_bonus = if_else(in(datacategories,"fundamental"), 1.8-0.3*market_beta, 1.2)
  decay_adjust = clip(1.8-decay/10, 0.5, 2.0)
  base_score = sqrt(liquidity_score) * fundamental_bonus * decay_adjust
  ```
- ​ **三阶过滤机制** ：排除换手率/相关性/复杂度极端值

### 三、特殊场景策略

#### 1. ​ **复合稳健策略** ​（YB49779 + WH24469）

- ​ **表达式** ：
  ```
  (!own && in(classifications,'SIMPLE') && turnover.between(0.08,0.15)
  && favorite && color!="NONE" && os_start_date>="2023-06-01")
  * pow(prod_correlation, -0.5)  # 低相关因子更高权重
  ```
- ​ **创新点** ：
  - 动态持有期： `optimal_hold_days = ceil(20/sqrt(turnover*100))`
  - 波动率适配： `if_else(ts_regime(volatility,252)==1, 1.5, 1)`

#### 2. ​ **高频信号优化** ​（CL88457）

- ​ **换手率分箱逻辑** ：
  python
  复制
  ```
  tvr_groups = {'low':(0.05,0.12), 'mid':(0.12,0.18), 'high':(0.18,0.25)}
  active_group = next((k for k,v in tvr_groups.items() if v[0]<=turnover<v[1]), None)
  ```
- ​ **组合端创新** ：
  `>> combo_engine(stats=generate_stats(alpha), weights=random_forest_predictor(...))`

### 四、工程化实现

#### 1. ​ **自动化策略优化系统** ​（XC66172）

- ​ **遗传算法框架** ：
  ```
  param_space = {
  'turnover_low':(0.05,0.15),
  'corr_threshold':(0.3,0.6),
  'decay_max':(5,15)
  }
  genetic_algorithm(strategy_expr, fitness_func=calc_pareto_frontier, generations=50)
  ```
- ​ **多目标优化** ：最大化Sharpe率，最小化回撤

#### 2. ​ **全自动回测框架** ​（HW93328）

- ​ **核心功能** ：
  - 断点续传与多线程并发
  - MySQL数据库存储结果
  - 开源实现：Super-Alpha自动回测框架
- ​ **随机表达式生成** ：
  ```
  random_expr = f"turnover>{random.uniform(0.05,0.15)} && decay<{random.randint(5,15)}"
  ```

### 五、关键参数规范

​ **参数** 

​ **推荐值** 

​ **作用** 

​ **风险控制** 

 `Selection Limit` 
100-300
平衡多样性与性能
避免过拟合

 `operator_count` 
<10
防止复杂表达式失效
提升泛化性

 `turnover` 
0.05-0.3
剔除极端换手因子
控制交易成本

 `prod_correlation` 
0.1-0.6
排除异常相关值
防范尾部风险

 `os_start_date` 
>"2022-01-01"
选择有效OS日期
避免策略失效

---

## 讨论与评论 (0)

