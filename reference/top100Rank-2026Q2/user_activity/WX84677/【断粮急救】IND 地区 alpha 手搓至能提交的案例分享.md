# 【断粮急救】IND 地区 alpha 手搓至能提交的案例分享

- **链接**: 【断粮急救】IND 地区 alpha 手搓至能提交的案例分享.md
- **作者**: WX84677
- **发布时间/热度**: 6个月前, 得票: 7

## 帖子正文

一、序言相信做过 IND 地区的朋友都知道，此地区挖 alpha 总有一道槛 “Robust universe Sharpe”。我也是被这个问题折磨了很久，最终结合论坛大佬的分享及自己的实践摸索，算是有了些针对性优化的套路，在此结合案例分享给大家。首先，感谢来自ZX12447的帖子：《关于IND地区Robust universe sharpe的改善方法》二、套路分享：1. 先调 Settings Neutralization，获得表现最佳的配置。2. 表达式中若没有 group_ 操作符，给表达式套上一个 group_* 操作符（遍历  group_rank、group_zscore、group_neutralize、group_normalize）分组参数用 'market'，寻找最佳表现 alpha。3. 遍历 group_ 操作符参数（market，sector，industry，subindustry）寻找最佳表现 alpha。4. 表达式中时序操作符参数微调，例如 ts_zscore, ts_mean, ts_backfill 等等，遍历有经济学含义的日期参数（5， 22， 66， 126， 252， 504），捕捉 Robust universe Sharpe 的变化趋势，再进行微调。例如 22 -> 66 -> 126 ，发现 Robust universe Sharpe 先升后降，则可继续在 22~66 之间继续寻找合适的参数。5. 尝试追加 winsorize, kth_element, ts_backfill, group_backfill 等操作符，仅对核心信号作处理。此举意在不破坏表达式逻辑的情况下进行数据优化（补全、去极值），看是否有更优表现。6. 尝试增加 signed_power 操作符，意图对不改变信号方向的前提下对信号作缩放，看能否有更优表现。7. 尝试增加 ts_mean, ts_scale, ts_quantile，此举属于最后挣扎，追加操作符后原数据分布有调整，信号原逻辑大概率已被破坏。Robust universe Sharpe > 0.85 的 alpha 可作为种子。将以上步骤过一遍，若还没有明显好转 ，建议果断放弃。另外每一步调整后记得看下 pc ，避免做无用功。三、实战案例分享：1、遍历后确认 Nuetralization 设为 SLOW 最佳，表现如下：2、遍历 group 操作符参数，发现 sector 效果更优：3、调整 kth_element 操作符参数 120 -> 504 效果更优：4、增加 group_backfill 补全数据，去除极值，优化成功：四、写在最后运用此套路，我成功调出来了四个 alpha，但鲁棒性测试表现均一般，可见有过拟合风险。此法在断粮、冲塔等不得已之时可以尝试，平日慎用。

---

## 讨论与评论 (0)

