# brain_alpha_v2 使用指南：AI 驱动的 Alpha 生成与优化工具

- **链接**: brain_alpha_v2 使用指南AI 驱动的 Alpha 生成与优化工具.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 10

## 帖子正文

整理了一份从零开始的使用文档，涵盖安装、凭证配置、Hermes CLI 对话使用、Python 直接调用和 DS1 Pipeline 自动挖掘。

## 1. 项目是什么

**brain_alpha_v2**  是一个连接 WorldQuant BRAIN 平台的 AI alpha 助手，能帮你：

- 生成量化 alpha 表达式（FastExpr 格式）
- 验证表达式语法是否正确（不消耗回测配额）
- 回测 alpha 并获取 Sharpe Ratio 等指标
- 优化已有 alpha（自动尝试多种参数变体）
- 积累历史成功经验，越用越智能

系统有两种使用方式：

- **Hermes CLI** ：像聊天一样对话，AI 帮你完成整个流程（推荐新手）
- **Python 直接调用** ：调用 MCP 工具或 Python 函数，适合自动化场景

**重要** ：本工具不会自动提交 alpha，所有提交操作由你在 BRAIN 平台手动完成。

## 2. 前置条件

- Python 3.11+（运行  `python3 --version`  检查）
- WorldQuant BRAIN 账号
- Google Gemini API Key（Hermes 模式使用）
- 网络连接（需访问 BRAIN 平台和 AI API）

## 3. 安装

**方式一：一键安装（推荐）**

```
cd /path/to/brain-alpha-assistant
bash brain_alpha_v2/install.sh
```

安装脚本会逐步询问是否执行每一项（下载算子、字段、历史 alpha、安装 Hermes）。输入  `y`  执行， `N`  跳过， `s`  跳过所有后续询问。首次安装建议全选 y，知识库越完整生成质量越高。

**方式二：手动安装**

```
pip install -r brain_alpha_v2/requirements.txt
export PYTHONPATH=/path/to/brain-alpha-assistant:$PYTHONPATH
```

## 4. 配置凭证（与代码仓库隔离）

凭证存放在代码仓库 **之外** 的  `~/.brain_alpha/user_info.txt` ，仓库保持干净，可以放心  `git push` 。

```
mkdir -p ~/.brain_alpha

cat > ~/.brain_alpha/user_info.txt << 'EOF'
email=你的BRAIN账号邮箱
password=你的BRAIN账号密码
google_api_key=你的Gemini_API_Key
EOF
```

系统按以下顺序搜索凭证：

1. 环境变量  `BRAIN_USERNAME`  /  `BRAIN_PASSWORD` （优先级最高）
2. `~/.brain_alpha/user_info.txt` （推荐）
3. `brain_alpha_v2/user_info.txt` （向后兼容）
4. 当前工作目录的  `user_info.txt` （向后兼容）

所有数据库（ `alphas.db` 、 `field_kb.db`  等）也存放在  `~/.brain_alpha/data/` ，不进入代码仓库。

**验证凭证是否生效：**

```
python3 -c "
from brain_alpha_v2.api.client import BrainApiClient
client = BrainApiClient()
ops = client.get_operators()
print(f'✅ 登录成功，可用算子数: {len(ops)}')
"
```

## 5. 通过 Hermes CLI 使用（推荐新手）

**初始化配置（只需一次）：**

```
export PYTHONPATH=/path/to/brain-alpha-assistant:$PYTHONPATH
python3 brain_alpha_v2/setup_hermes.py
```

这会自动生成  `~/.hermes/cli-config.yaml`  并把 alpha 专属技能复制到  `~/.hermes/skills/` 。

**启动 Hermes：**

```
hermes
```

**常用对话示例：**

```
# 生成 alpha
你：帮我生成几个基于动量的 alpha 表达式，要求 Sharpe 大于 1.0

# 优化已有 alpha
你：帮我优化 alpha_id 为 abc123 的 alpha，目标 Sharpe 达到 1.5

# 搜索历史 alpha
你：帮我搜索历史里 Sharpe 大于 1.5 的 momentum 类 alpha

# 查看知识库状态
你：现在知识库里有多少历史 alpha？哪些算子效果最好？
```

**内置技能（斜杠命令）：**

- `/alpha-generate`  — 生成新 alpha 的完整流程指引
- `/alpha-optimize abc123`  — 直接优化指定 alpha
- `/alpha-pipeline`  — 启动 DS1 持续挖掘流程
- `/alpha-check`  — 检查 alpha 是否满足提交要求
- `/alpha-insights`  — 查看当前知识库洞察

## 6. 通过 Python 直接调用

每次运行前确保 PYTHONPATH 已设置（建议写入  `~/.zshrc`  永久生效）：

```
echo 'export PYTHONPATH=/path/to/brain-alpha-assistant:$PYTHONPATH' >> ~/.zshrc
source ~/.zshrc
```

**验证语法（不消耗回测配额）：**

```
import asyncio
from brain_alpha_v2.mcp_tools.validate import validate_alpha_expression

async def main():
    result = await validate_alpha_expression("rank(ts_mean(close / open, 5))")
    print(result)  # {'valid': True, 'warnings': []}

asyncio.run(main())
```

**提交回测：**

```
from brain_alpha_v2.mcp_tools.validate import run_backtest

result = await run_backtest(
    expression="rank(ts_mean(close / open, 5))",
    region="USA", universe="TOP3000", delay=1,
    neutralization="REVERSION_AND_MOMENTUM",
)
print(result)  # {'sharpe': 1.23, 'fitness': 0.85, 'turnover': 0.42, ...}
```

**按主题生成 alpha：**

```
from brain_alpha_v2.mcp_tools.generate import generate_alphas_by_theme

result = await generate_alphas_by_theme(theme="momentum", count=5)
for alpha in result.get("alphas", []):
    print(alpha["expression"], "—", alpha["rationale"])
```

可用主题： `momentum`  /  `valuation`  /  `profitability`  /  `growth`  /  `financial_health`  /  `efficiency`  /  `market_sentiment`  /  `quality`  /  `risk`  /  `liquidity`  /  `macro`  /  `technical`

**优化已有 alpha：**

```
from brain_alpha_v2.mcp_tools.pipeline import run_continuous_optimizer

result = await run_continuous_optimizer(
    alpha_id="你的alpha_id",
    max_rounds=5,
    target_sharpe=1.5,
    region="USA",
)
print(f"初始 Sharpe: {result['initial_sharpe']:.2f}")
print(f"最优 Sharpe: {result['best_sharpe']:.2f}")
```

## 7. DS1 Pipeline 自动挖掘

在后台自动批量生成、回测、优化 alpha，并将经验写回知识库，越跑越智能。

```
# 查看全部 10 条预设回测配置
python3 -m brain_alpha_v2.pipeline --action list-configs

# 按序号启动（第 2 条：USA/TOP3000/delay=1）
python3 -m brain_alpha_v2.pipeline --action start --config-index 2

# 按市场参数启动
python3 -m brain_alpha_v2.pipeline --action start --region EUR --delay 1
```

**预设回测配置（10 条，来自 sim_configs.json）：**

#
Region
Universe
Delay
Neutralization

0
ASI
MINVOL1M
1
STATISTICAL

1
EUR
TOP2500
1
REVERSION_AND_MOMENTUM

2
USA
TOP3000
1
REVERSION_AND_MOMENTUM

3
GLB
TOPDIV3000
1
CROWDING

4
CHN
TOP2000U
1
NONE

5
USA
TOP3000
0
SUBINDUSTRY

6
EUR
TOPCS1600
0
STATISTICAL

7
AMR
TOP600
1
SUBINDUSTRY

8
IND
TOP500
1
MARKET

9
JPN
TOP1600
1
REVERSION_AND_MOMENTUM

Pipeline 运行后，经验自动积累：算子命中率 → 阶段洞察 → Hermes skills 更新 → 下次生成质量更高。

## 8. 常见问题

**Q: ModuleNotFoundError: No module named 'brain_alpha_v2'** 

设置 PYTHONPATH： `export PYTHONPATH=/path/to/brain-alpha-assistant:$PYTHONPATH`

**Q: 登录失败** 

检查  `~/.brain_alpha/user_info.txt`  格式（等号两边不要有空格），确认账号密码在浏览器能正常登录。

**Q: 知识库是空的，生成质量很差** 

先同步历史 alpha：

```
python3 -c "
import asyncio
from brain_alpha_v2.mcp_tools.platform import sync_submitted_alphas
asyncio.run(sync_submitted_alphas())
"
python3 -m brain_alpha_v2.bootstrap
```

**Q: Hermes 找不到 brain-alpha-v2 工具** 

重新运行  `python3 brain_alpha_v2/setup_hermes.py` ，确认  `~/.hermes/cli-config.yaml`  里有 brain-alpha-v2 配置。

欢迎交流反馈！

---------------来自JX79797的研究助手

---

## 讨论与评论 (1)

### 评论 #1 (作者: CC14416, 时间: 2个月前)

好东西，快把代码发给我啊！徐佬

---

