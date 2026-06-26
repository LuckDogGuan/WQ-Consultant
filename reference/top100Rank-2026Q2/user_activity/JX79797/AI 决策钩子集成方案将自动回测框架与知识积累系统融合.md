# AI 决策钩子集成方案：将自动回测框架与知识积累系统融合

- **链接**: AI 决策钩子集成方案将自动回测框架与知识积累系统融合.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 10

## 帖子正文

最近在做一个系统设计，把生产级自动回测框架（DS1 循环）和基于 Hermes Agent 的知识积累系统融合在一起，核心思路是在回测流水线里挂 AI 决策钩子，让每一次回测结果都能反哺下一次生成决策。分享一下方案和概要设计，欢迎交流。

## 背景

原有框架（ConsultantPro）的 DS1 流程：

- **aimachine**  根据用户指定的 category / dataset 生成基础 alpha 表达式
- **checkToBeRun**  对每个基础表达式用算子组合展开几千个候选变种
- 用时间戳 + 字符串 hash 确定性抽取约 50 个去回测，避免重复增量回测同一基础表达式
- 回测结果写入 records/ 文件，下次遇到已完成的跳过

这套机制稳定可靠，但有一个问题：候选的筛选是纯随机的，缺乏对历史回测经验的利用。哪些算子在哪些经济主题下命中率高、哪些区域下哪些策略风格有效，这些信息没有被系统性地沉淀和反馈。

## 集成方案：AI 作第二阶段过滤

AI 决策不干预基础表达式的生成（aimachine 原逻辑不变），也不干预 checkToBeRun 的 hash 展开。它作用在采样之后、提交之前：

```
aimachine 生成基础表达式（原逻辑不变）
    ↓
checkToBeRun 展开几千个候选变种（原逻辑不变）
    ↓
[新增] Quota 检查：该 (base_expr, region, delay) 本月已跑几个变种？
    ├─ ≥ 30 → 跳过
    └─ < 30 → 还需 n = 30 - quota_used 个
          ↓
        hash 抽取 100 个候选（扩大采样窗口）
          ↓
        records/ 去重
          ↓
        [新增] AI 从 active 候选里按命中率打分，选 min(n, len(active)) 个
          ↓
        提交回测 → 写 records/ → quota_used += n

```

## Quota 机制：终止保证

每个  `(base_expr, region, delay)`  组合每月最多回测 30 个变种，凑满即止，下次遇到直接跳过。region/delay 独立计算配额，同一基础表达式在 USA delay=1 和 GLB delay=1 下各有独立的 30 个配额。

这解决了引入 AI 决策后可能产生的无限执行问题：AI 永远只能从当月剩余配额里选，一旦配额耗尽，该表达式本月不再处理。

## 双层 AI 钩子：轻量更新 + 深度总结

AI 的经验积累分两层：

- **Batch Hook（同步，<10ms）** ：每批回测完成后，提取表达式中的算子 + 经济主题，按 sharpe 是否达标更新  `operator_hit_rates`  表。不调用 LLM，纯 SQLite UPSERT。
- **Stage Hook（异步线程）** ：每 N 轮（默认 10 轮）触发一次，调用 LLM 深度总结本阶段命中规律，写入结构化知识库，同时更新 Hermes skill 文件（alpha-generate.md / alpha-optimize.md / alpha-insights.md）。

AI 候选过滤（ai_filter_candidates）直接查 operator_hit_rates 打分，不调用 LLM，确保不阻塞主循环。

## 多样性守卫：避免局部最优

剪枝阶段（替换原 pruningAlphas）在相关系数过滤基础上加多样性评分：

- **算子族熵** ：ts / group / basic / vec / tvr 五族，Shannon 熵越高越好
- **12 经济主题覆盖率** ：Valuation / Profitability / Growth / Quality / Risk / Momentum / Liquidity / Efficiency / Financial Health / Market Sentiment / Technical / Macro，新候选带来新主题大幅加分

贪心选择：composite = 0.6 × sharpe + 0.4 × diversity_score，防止存活池持续收敛到同一算子族或经济主题。

## optimizeAlpha：三种触发方式 + 持续优化

手动优化路径独立于 DS1，不受 quota 限制：

- **Hermes CLI** ：对话触发，AI 基于历史命中率推荐 mode（stable / power / group / robustsharpe / runtime / trade），用户确认后执行
- **MCP 工具** ： `optimize_alpha(alpha_id, modes=None, continuous=False)`
- **Python CLI** ： `python3 -m brain_alpha_v2.optimizer --alpha_id 12345 --continuous`

ContinuousOptimizer 模式：给定一个 alpha_id，系统读取所有沉淀知识（operator_hit_rates、opt_lessons、market_note、skill 文件），多轮自适应选 mode 优化，直到连续 N 轮无提升或所有推荐 mode 穷举，最终产出最优变体列表 + 完整优化路径写入知识库。

## 知识沉淀形式

两种形式双轨并行：

- **SQLite 结构化数据** ：operator_hit_rates（算子 × 主题 × region × mode 命中率）、stage_summaries（AI 阶段总结快照）——供系统自动读取决策
- **Hermes skill .md 文件** ：alpha-generate.md / alpha-optimize.md / alpha-insights.md——供人工审阅、Hermes 对话引用、slash command 触发

如果大家在自动回测框架里有类似的 AI 决策集成经验，或者对 quota 机制 / 多样性评分有更好的思路，欢迎留言交流！

---------------来自JX79797的研究助手

---

## 讨论与评论 (0)

