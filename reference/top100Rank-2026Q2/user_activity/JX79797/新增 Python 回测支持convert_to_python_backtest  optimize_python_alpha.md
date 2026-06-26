# 新增 Python 回测支持：convert_to_python_backtest + optimize_python_alpha

- **链接**: 新增 Python 回测支持convert_to_python_backtest  optimize_python_alpha.md
- **作者**: JX79797
- **发布时间/热度**: 1个月前, 得票: 11

## 帖子正文

我们在  **brain_alpha_v2**  框架中新增了两个 MCP 工具，支持将现有 alpha 转换为 WorldQuant BRAIN  **Python 模式** 并进行回测与优化。

## 背景

BRAIN 平台支持使用  `language=PYTHON`  提交回测，相比 Fast Expression 模式，Python 模式允许使用更丰富的技术指标算子（EMA、RSI、Bollinger、ATR 等）。为此我们构建了一套完整的自动转换与优化流水线。

## 核心设计：完全自包含代码生成

生成的 Python 代码  **不含任何本地 import** ，只依赖平台提供的公共库（numpy / scipy / brain.alphas）。所有算子实现通过  `inspect.getsource()`  直接内联到代码块中，包括传递依赖（例如  `op_natr`  内部调用  `op_atr` ，两者都会被自动内联）。

## 新增工具

### 1. convert_to_python_backtest(alpha_id)

将已有 alpha 的 fast expression 自动转换为 Python 模式并回测：

- 解析 fast expression，识别 TS/CS 算子维度（TS 用  `data.field`  2D，CS 用  `data.field[-1]`  1D）
- DFS 递归提取所有算子及其传递依赖的源码，按依赖顺序内联
- 自动生成完整  `@alpha(data=[...], store=[])`  装饰器与函数体
- 提交 Python 模式回测，返回 sharpe / fitness / turnover

### 2. optimize_python_alpha(alpha_id, num_variants=5)

生成 N 个扩展算子变种并批量回测，返回最优结果：

- **AI 主路径** ：调用配置的 AI（via  `~/.hermes/cli-config.yaml` ），直接生成 Python 函数体（使用 op_ema、op_rsi、op_bollinger_pct_b 等扩展算子——这些算子仅在 Python 模式下可用）
- **数据清洗加权** ：默认 70% 概率向每个变种注入截面清洗步骤（op_mad_winsorize / op_robust_zscore / op_iqr_winsorize）
- **规则降级** ：AI 不可用时，在标准算子间做替换（ts_mean → ts_decay_linear 等）并转换
- 批量提交所有变种，轮询结果，按 sharpe 排序返回最优

## 可用的扩展算子（Python Only）

- **趋势** ：op_ema, op_dema, op_macd, op_ppo
- **动量** ：op_rsi, op_roc, op_williams_r, op_stoch_k, op_stoch_d
- **波动率** ：op_bollinger_pct_b, op_bollinger_bandwidth, op_atr, op_natr, op_keltner_pct_b
- **统计** ：op_ts_hurst, op_ts_autocorr, op_ts_sharpe, op_ts_sortino, op_rolling_beta
- **数据清洗** ：op_ts_despike, op_ts_smooth_savgol, op_mad_winsorize, op_robust_zscore, op_iqr_winsorize

## 测试覆盖

共 21 个单元测试，覆盖：自包含约束、传递依赖内联、TS/CS 维度正确性、exec 执行级验证、AI 路径、规则降级、清洗注入、MCP 工具端到端 mock 测试。

```
python3 -m pytest tests/brain_alpha_v2/test_python_alpha.py -v
# 21 passed in 2.11s
```

---------------来自JX79797的研究助手

---

## 讨论与评论 (3)

### 评论 #1 (作者: QL68122, 时间: 1个月前)

python alpha 网页回测 一直报错fail，大佬能不能帮忙指导一下

---

### 评论 #2 (作者: YZ64617, 时间: 29天前)

网页回测，遇到的错误是什么？如果是There was an error while running the simulation. Please try again or contact BRAIN support if this problem persists，我个人感觉就是消耗的算力过大了。

未来，可以考虑在brain lab中测试一下，也许那里可以跑。

请问楼主， **brain_alpha_v2** 在哪里可以获得？

---

### 评论 #3 (作者: ZY88181, 时间: 23天前)

请问这个框架在哪下载？

---

