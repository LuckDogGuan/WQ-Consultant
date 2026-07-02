<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **wq_gui** (3000 symbols, 13897 relationships, 257 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({search_query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/wq_gui/context` | Codebase overview, check index freshness |
| `gitnexus://repo/wq_gui/clusters` | All functional areas |
| `gitnexus://repo/wq_gui/processes` | All execution flows |
| `gitnexus://repo/wq_gui/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->

# 因子回测与参考代码使用开发规范

本工作区包含用于回测的 Jupyter Notebook 及从社区/外部整理的辅助优化代码（统一保存在 `reference/` 下）。在日常因子开发与流程优化中，任何会话或子代理必须严格遵守以下规范：

1. **参考资料目录绝对只读 (Reference Read-Only)**：
   * `reference/` 目录下的所有回测笔记本（如 `reference/notebook/`）以及外部提取的算法脚本（如 `reference/code/`）仅作为只读参考。
   * **严禁直接修改 `reference/` 目录下的任何原始回测代码及外部参考代码**。
2. **复制测试验证规则 (Copy & Test Rule)**：
   * 如果需要优化回测流程、调整参数或验证任何开发猜想，**必须首先复制一份目标参考文件到临时测试文件夹 `scratch/` 目录中**，在 `scratch/` 中进行修改、运行和验证。
3. **小功能与模块化设计 (Granular Utilities)**：
   * 在进行流程优化时，应将具体算法与业务逻辑拆解为颗粒度小、职责单一的**小功能函数**，方便后续流程直接导入与重复调用。
4. **优先复用现有库 (Reuse Existing Libraries)**：
   * 开发或优化代码时，应尽量使用系统已有的功能组件与成熟模块（例如本项目的 `wqb` 库、`consultant_core` 等内置库），避免重复造轮子。
5. **优先使用 MCP 工具与现有库 (Prioritize MCP & Existing Libraries)**：
   * 在需要与平台进行数据交互（如因子测试、PnL 查询、数据提交、社区检索等）时，必须优先使用系统内注册的 MCP 工具（如 `wq_gui` 的 MCP 接口或 `cnhkmcp` 等相关平台工具），或直接复用本地的封装库（如 `wqb` 库和 `consultant_core` 等）。
   * 严格禁止在已有对应 MCP 功能或成熟本地库的情况下，自主通过原生的网络请求（如编写 `playwright`、`httpx` 或 `requests` 等原生逻辑）重写同质化功能。只有在现有 MCP 和现有库均无法支持所需操作时，才允许设计自研逻辑。
