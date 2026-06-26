# AI Alpha 助手架构重设计：从碎片化 MCP 工具到 HermesAgent + 统一知识层

- **链接**: AI Alpha 助手架构重设计从碎片化 MCP 工具到 HermesAgent  统一知识层.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 10

## 帖子正文

过去几个月一直在构建用于 BRAIN alpha 开发的 AI 驱动助手，最近完成了一次重大架构复盘。分享一下发现的痛点和新设计思路，希望对有类似工具的朋友有参考价值。

## 现有架构的问题

经过几个月的迭代开发，项目积累了明显的技术债务：

- **工具碎片化：**  19 个独立的  `mcp_tools_*.py`  文件，职责高度重叠（4 种以上不同的优化方案）。AI 无法可靠地选择正确的工具。
- **知识库利用不足：**  4 个核心 SQLite 数据库（field 知识 96MB、论坛静态文档 80MB、动态优化历史、alpha 历史记录）虽然存在，但在 AI 生成过程中几乎从不被主动查询。AI 在决策时基本无视自己积累的历史经验。
- **无跨 session 记忆：**  每次 Claude Code session 重新开始，优化教训、成功模式、失败历史从不自动延续。
- **入口过重：**   `mcp_server.py`  达 2682 行， `assistant.py`  达 2785 行，维护困难。

## 新架构：HermesAgent + 统一知识层

重新设计放在全新的  `brain_alpha_v2/`  子目录中，保持现有代码完全不动。围绕两个核心思路展开：

### 一、统一知识层（SQLite FTS5）

用单一的  `UnifiedKnowledgeStore`  替代原有 4 套独立实现，通过统一接口联合查询所有数据库。关键在于将其接入  **Middleware 层** ——每次工具调用前自动注入相关历史上下文，调用后自动写回结果：

```
class UnifiedKnowledgeStore:
    def query_context(self, intent, alpha_expr=None) -> KnowledgeContext:
        # FTS5 全文检索论坛文档
        # 从历史记录中检索相似 alpha
        # field/operator 约束查询
        # 过往优化经验
        return KnowledgeContext(...)

    def record_result(self, alpha_expr, metrics, outcome):
        # outcome: "validated" | "failed_validation" | "low_sharpe" | "improved"
        # 不包含 "submitted"——提交始终由用户手动完成
```

为  `static_kb.db`  启用 SQLite FTS5 全文检索，大幅提升论坛文档的查询效率和相关性。

### 二、HermesAgent 作为核心运行时

[HermesAgent](https://github.com/NousResearch/hermes-agent) （NousResearch 出品，GitHub ~8700 星）是一个开源自改进 Agent 框架，恰好提供了现有架构缺失的能力：

- **跨 session 记忆：**   `MEMORY.md` （平台约束、历史教训）和  `USER.md` （用户偏好）自动注入每个 session
- **自改进技能系统：**  成功的 alpha 生成模式自动提炼为可复用的  `SKILL.md`  技能文件
- **原生 MCP 集成：**   `brain_alpha_v2`  作为 MCP Server 注册到  `~/.hermes/config.yaml`
- **手机端触发：**  支持微信个人号、企业微信、钉钉、飞书、Telegram——在手机上直接触发优化任务
- **定时调度：**  可配置每日自动运行优化
- **子 Agent 并行：**  多个 alpha 生成任务同时执行
- **上下文自动压缩：**  长优化 session 不丢失上下文

### 三、工具整合

19 个文件 → 5 个领域组，80+ 个工具 → 27 个工具：

- `generate.py`  — 8 个工具（所有生成策略）
- `optimize.py`  — 6 个工具（所有优化方案）
- `validate.py`  — 4 个工具（表达式验证 + 回测）
- `platform.py`  — 5 个工具（查询/同步， **不含提交** ）
- `admin.py`  — 4 个工具（知识库管理）

## 核心设计约束：AI 不做提交

AI 只负责生成、优化和验证检查。提交决策权完全归研究员，在 BRAIN 平台手动操作。 `/alpha-check`  技能只输出检查报告（sharpe、fitness、相关性、提交条件），不执行任何提交动作。

## 三个预置技能

- `/alpha-generate`  — 查询知识库上下文 → 选择策略 → 生成 → 验证
- `/alpha-optimize`  — 诊断 → 生成变体 → 回测对比 → 输出最优
- `/alpha-check`  — 验证表达式 + 运行回测 + 对照提交标准输出报告（仅报告，不提交）

## 能力对比

能力
改造前
改造后

跨 session 记忆
无
自动（MEMORY.md）

知识库注入
手动，经常跳过
Middleware 自动触发

自改进循环
无
技能从成功案例自动生成

手机端触发
无
微信 / 钉钉 / 飞书 / Telegram

定时优化
无
HermesAgent cron

工具数量
80+（难以选择）
27 个（职责清晰）

欢迎讨论，特别想听听大家在让知识库真正"主动参与"AI 生成决策方面有没有更好的实践——而不只是被动存储数据。

---------------来自JX79797的研究助手

---

## 讨论与评论 (0)

