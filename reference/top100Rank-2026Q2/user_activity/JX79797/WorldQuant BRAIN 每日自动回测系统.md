# 🤖 WorldQuant BRAIN 每日自动回测系统

- **链接**: WorldQuant BRAIN 每日自动回测系统.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 5

## 帖子正文

# WorldQuant BRAIN 每日自动回测系统

使用 GitHub Actions 实现每天自动生成并回测 Alpha 表达式，无需服务器，完全免费！

## 项目简介

本项目利用 GitHub Actions 的定时任务功能，每天自动：

1. 生成 10 个随机不重复的 Alpha 表达式
2. 调用 WorldQuant BRAIN API 进行回测
3. 生成 Markdown 报告（直接在 GitHub 仓库首页显示）
4. 自动提交结果到仓库

**特点：**

- ✅ 零服务器成本（使用 GitHub Actions 免费额度）
- ✅ 零配置（只需 2 个 GitHub Secrets）
- ✅ 自动去重（避免重复生成相同 Alpha）
- ✅ 支持本地测试和云端自动化
- ✅ 实时报告（README.md 自动更新）

## 项目结构

```
daily-simulation/
├── .github/
│   └── workflows/
│       └── daily-backtest.yml    # GitHub Actions 工作流配置
├── data/
│   ├── fields.csv                # 字段列表（200个跨区域共通字段）
│   ├── gold_operators.csv        # 操作符定义
│   └── history.txt               # 历史 Alpha 记录（自动更新）
├── main.py                       # 主程序（约 700 行）
├── requirements.txt              # Python 依赖
├── .gitignore                    # Git 忽略配置
└── README.md                     # 自动生成的回测报告

```

## 快速开始

### 第 1 步：创建 GitHub 仓库

1. 登录 GitHub，创建新仓库（如  `daily-simulation` ）
2. 可以设为私有（Private）保护隐私

### 第 2 步：创建目录结构

```
mkdir -p .github/workflows
mkdir -p data
touch data/history.txt

```

### 第 3 步：创建配置文件

#### `.github/workflows/daily-backtest.yml`

```
name: Daily Alpha Backtest

on:
  schedule:
    # 每天 UTC 06:00 = 北京时间 14:00
    - cron: '0 6 * * *'

  # 允许手动触发
  workflow_dispatch:

jobs:
  backtest:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    # 授予写入权限以便提交结果
    permissions:
      contents: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${ secrets.GITHUB_TOKEN }

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run daily backtest
        env:
          # 🔑 从 GitHub Secrets 读取凭证并设置为环境变量
          BRAIN_USERNAME: ${ secrets.BRAIN_USERNAME }
          BRAIN_PASSWORD: ${ secrets.BRAIN_PASSWORD }
        run: |
          python main.py

      - name: Commit and push results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/history.txt README.md
          git diff --quiet && git diff --staged --quiet || git commit -m "📊 Daily backtest report: $(date +'%Y-%m-%d %H:%M:%S') UTC"
          git push

```

#### `requirements.txt`

```
requests==2.31.0
pandas==2.2.0

```

#### `.gitignore`

```
# 敏感信息 - 绝对不要提交！
user_info.txt

# Python
*.pyc
__pycache__/
*.pyo
*.pyd
.Python

# 虚拟环境
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# macOS
.DS_Store

# 临时文件
*.log
*.tmp

```

## 主程序代码

### `main.py` （完整代码）

```
#!/usr/bin/env python3
"""
WorldQuant BRAIN 每日自动回测脚本
每天生成 10 个随机 Alpha 表达式并执行回测，生成 Markdown 报告

支持两种凭证来源：
1. 环境变量：BRAIN_USERNAME, BRAIN_PASSWORD（GitHub Actions）
2. user_info.txt 文件（本地开发）
"""
import sys
import os
import random
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple, Set
import time

# ============================================================================
# 第 1 部分：Alpha 生成器类
# ============================================================================

class SimpleAlphaGenerator:
    """随机生成不重复的 Alpha 表达式"""

    def __init__(self, operators_file: str, fields_file: str, history_file: str):
        """
        初始化生成器

        Args:
            operators_file: 操作符 CSV 文件路径
            fields_file: 字段 CSV 文件路径
            history_file: 历史记录文件路径
        """
        self.operators = self._load_operators(operators_file)
        self.fields = self._load_fields(fields_file)
        self.history = self._load_history(history_file)
        self.history_file = history_file

        print(f"  加载了 {len(self.operators)} 个操作符")
        print(f"  加载了 {len(self.fields)} 个字段")
        print(f"  历史记录: {len(self.history)} 个")

    def _load_operators(self, filepath: str) -> List[str]:
        """加载操作符列表"""
        df = pd.read_csv(filepath)
        # 筛选常用操作符
        common_ops = [
            'rank', 'scale', 'zscore', 'log', 'abs', 'sqrt',
            'ts_rank', 'ts_mean', 'ts_delta', 'ts_zscore', 'ts_sum',
            'decay', 'divide', 'subtract', 'add', 'multiply',
            'ts_std_dev', 'ts_skewness', 'ts_kurtosis',
            'group_rank', 'group_neutralize'
        ]
        available_ops = df['name'].tolist()
        return [op for op in common_ops if op in available_ops]

    def _load_fields(self, filepath: str) -> List[str]:
        """加载字段列表"""
        df = pd.read_csv(filepath)
        # 只使用 matrix 类型字段（不需要聚合，避免语法错误）
        matrix_fields = df[df['type'] == 'matrix']['name'].tolist()
        return matrix_fields

    def _load_history(self, filepath: str) -> Set[str]:
        """加载历史记录"""
        try:
            with open(filepath, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()

    def generate_unique_alphas(self, count: int = 20) -> List[str]:
        """
        生成指定数量的不重复 Alpha 表达式

        Args:
            count: 需要生成的数量

        Returns:
            Alpha 表达式列表
        """
        alphas = set()
        max_attempts = count * 20  # 防止无限循环

        patterns = [
            self._pattern_single_op,
            self._pattern_binary_op,
            self._pattern_nested,
            self._pattern_ts_op,
            self._pattern_ts_binary,
        ]

        attempts = 0
        while len(alphas) < count and attempts < max_attempts:
            attempts += 1

            # 随机选择模式
            pattern_func = random.choice(patterns)
            expr = pattern_func()

            # 检查是否重复
            if expr and expr not in self.history and expr not in alphas:
                alphas.add(expr)

        return list(alphas)

    def _pattern_single_op(self) -> str:
        """模式1: op(field)"""
        op = random.choice(['rank', 'scale', 'zscore', 'log', 'abs', 'sqrt'])
        field = random.choice(self.fields)
        return f"{op}({field})"

    def _pattern_binary_op(self) -> str:
        """模式2: op(field1, field2)"""
        f1 = random.choice(self.fields)
        f2 = random.choice(self.fields)

        # 确保不是同一个字段
        while f2 == f1 and len(self.fields) > 1:
            f2 = random.choice(self.fields)

        op = random.choice(['divide', 'subtract', 'add', 'multiply'])
        return f"{op}({f1}, {f2})"

    def _pattern_nested(self) -> str:
        """模式3: outer_op(inner_op(field), param)"""
        field = random.choice(self.fields)
        inner_op = random.choice(['rank', 'log', 'scale', 'zscore'])
        outer_op = random.choice(['ts_rank', 'ts_mean', 'decay'])
        period = random.randint(5, 20)

        return f"{outer_op}({inner_op}({field}), {period})"

    def _pattern_ts_op(self) -> str:
        """模式4: ts_op(field, period)"""
        op = random.choice(['ts_rank', 'ts_mean', 'ts_delta', 'ts_zscore', 'ts_sum', 'ts_std_dev'])
        field = random.choice(self.fields)
        period = random.randint(5, 30)

        return f"{op}({field}, {period})"

    def _pattern_ts_binary(self) -> str:
        """模式5: ts_op(op(field1, field2), period)"""
        f1 = random.choice(self.fields)
        f2 = random.choice(self.fields)

        while f2 == f1 and len(self.fields) > 1:
            f2 = random.choice(self.fields)

        inner_op = random.choice(['divide', 'subtract'])
        outer_op = random.choice(['ts_rank', 'ts_mean', 'ts_delta'])
        period = random.randint(5, 20)

        return f"{outer_op}({inner_op}({f1}, {f2}), {period})"

# ============================================================================
# 第 2 部分：回测执行器类
# ============================================================================

class BacktestRunner:
    """执行 Alpha 回测"""

    def __init__(self, username: str, password: str):
        """
        初始化并登录

        Args:
            username: BRAIN 用户名
            password: BRAIN 密码
        """
        self.session = self._login(username, password)
        self.regions = self._get_available_regions()

    def _login(self, username: str, password: str) -> requests.Session:
        """登录 BRAIN API"""
        s = requests.Session()
        s.auth = (username, password)

        try:
            response = s.post('https://api.worldquantbrain.com/authentication', timeout=30)
            response.raise_for_status()
            print("  ✅ 登录成功")
            return s
        except Exception as e:
            raise Exception(f"登录失败: {e}")

    def _get_available_regions(self) -> List[Tuple[str, str]]:
        """获取可用的区域和宇宙组合"""
        return [
            ('USA', 'TOP3000'),
            ('EUR', 'TOP2500'),
        ]

    def run_backtest(self, alpha_expr: str) -> Dict:
        """
        执行单个 alpha 回测（遇到并发限制时自动重试）

        Args:
            alpha_expr: Alpha 表达式

        Returns:
            回测结果字典
        """
        # 随机选择参数
        region, universe = random.choice(self.regions)
        delay = 1  # 使用 delay=1，所有区域都支持
        decay = random.randint(0, 100)  # 0-100 随机整数
        truncation = round(random.uniform(0.01, 0.2), 4)  # 0.01-0.2 随机浮点数
        neutralization = self._get_neutralization(region)

        simulation_data = {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
            },
            'regular': alpha_expr
        }

        # 第 1 步：提交模拟（处理并发限制）
        retry_count = 0
        simulation_progress_url = None

        while simulation_progress_url is None:
            try:
                resp = self.session.post(
                    'https://api.worldquantbrain.com/simulations',
                    json=simulation_data,
                    timeout=60
                )

                # 检查是否是并发限制错误
                try:
                    json_data = resp.json()
                    detail = json_data.get('detail', '') if isinstance(json_data, dict) else ''

                    if resp.status_code == 429 or 'CONCURRENT_SIMULATION_LIMIT_EXCEEDED' in detail:
                        retry_count += 1
                        if retry_count % 10 == 0:
                            print(f"      ⏳ 并发限制，已重试 {retry_count} 次...")
                        time.sleep(1)
                        continue

                    # 其他错误
                    if detail and detail != 'CONCURRENT_SIMULATION_LIMIT_EXCEEDED':
                        return {
                            'success': False,
                            'alpha': alpha_expr,
                            'region': region,
                            'universe': universe,
                            'error': f'API 错误: {detail}'
                        }
                except ValueError:
                    # 不是 JSON 响应，可能有 Location header
                    pass

                # 检查 Location header（异步模拟的进度 URL）
                simulation_progress_url = resp.headers.get('Location')
                if not simulation_progress_url:
                    return {
                        'success': False,
                        'alpha': alpha_expr,
                        'region': region,
                        'universe': universe,
                        'error': f'无 Location header (status={resp.status_code})'
                    }

            except requests.exceptions.Timeout:
                return {
                    'success': False,
                    'alpha': alpha_expr,
                    'error': '提交超时（60秒）'
                }
            except Exception as e:
                return {
                    'success': False,
                    'alpha': alpha_expr,
                    'error': f'提交异常: {type(e).__name__}: {str(e)}'
                }

        # 超时返回
        if time.time() - start_time >= max_wait_time:
            return {
                'success': False,
                'alpha': alpha_expr,
                'error': f'回测超时（{max_wait_time}秒）'
            }

        # 第 2 步：轮询模拟进度（最多等待 15 分钟）
        start_time = time.time()
        max_wait_time = 900  # 15 分钟

        while time.time() - start_time < max_wait_time:
            try:
                resp = self.session.get(simulation_progress_url, timeout=60)

                # 检查 Retry-After header
                retry_after = resp.headers.get('Retry-After')
                if retry_after and float(retry_after) > 0:
                    time.sleep(float(retry_after))
                    continue

                # 模拟完成，获取 alpha_id
                result = resp.json()
                alpha_id = result.get('alpha')

                if not alpha_id:
                    return {
                        'success': False,
                        'alpha': alpha_expr,
                        'region': region,
                        'universe': universe,
                        'error': f'未获取到 alpha ID (keys={list(result.keys())})'
                    }

                break  # 跳出轮询循环

            except requests.exceptions.Timeout:
                return {
                    'success': False,
                    'alpha': alpha_expr,
                    'error': '进度查询超时（60秒）'
                }
            except Exception as e:
                return {
                    'success': False,
                    'alpha': alpha_expr,
                    'error': f'进度查询异常: {type(e).__name__}: {str(e)}'
                }

        # 超时返回
        if time.time() - start_time >= max_wait_time:
            return {
                'success': False,
                'alpha': alpha_expr,
                'error': f'回测超时（{max_wait_time}秒）'
            }

        # 第 3 步：获取 alpha 详情（sharpe, fitness, turnover 等）
        try:
            while True:
                detail_resp = self.session.get(
                    f'https://api.worldquantbrain.com/alphas/{alpha_id}',
                    timeout=60
                )

                # 检查 Retry-After header
                retry_after = detail_resp.headers.get('Retry-After')
                if retry_after and float(retry_after) > 0:
                    time.sleep(float(retry_after))
                    continue

                # 获取详情
                metrics = detail_resp.json()
                is_data = metrics.get('is', {})

                if not is_data:
                    return {
                        'success': False,
                        'alpha': alpha_expr,
                        'region': region,
                        'universe': universe,
                        'error': 'Alpha 详情中无 is 数据'
                    }

                return {
                    'success': True,
                    'alpha': alpha_expr,
                    'region': region,
                    'universe': universe,
                    'delay': delay,
                    'decay': decay,
                    'truncation': truncation,
                    'neutralization': neutralization,
                    'sharpe': is_data.get('sharpe', 0),
                    'fitness': is_data.get('fitness', 0),
                    'turnover': is_data.get('turnover', 0),
                    'error': None
                }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'alpha': alpha_expr,
                'error': 'Alpha 详情获取超时（60秒）'
            }
        except Exception as e:
            return {
                'success': False,
                'alpha': alpha_expr,
                'error': f'Alpha 详情获取异常: {type(e).__name__}: {str(e)}'
            }

    def _get_neutralization(self, region: str) -> str:
        """根据区域返回合适的中性化策略"""
        neut_map = {
            'USA': 'SUBINDUSTRY',
            'EUR': 'SUBINDUSTRY',
            'GLB': 'SUBINDUSTRY',
            'ASI': 'SUBINDUSTRY',
            'JPN': 'SUBINDUSTRY',
            'KOR': 'SECTOR',
            'AMR': 'SECTOR',
            'IND': 'SECTOR',
        }
        return neut_map.get(region, 'SUBINDUSTRY')

# ============================================================================
# 第 3 部分：报告生成器类
# ============================================================================

class ReportGenerator:
    """生成 Markdown 报告"""

    def __init__(self, output_file: str = 'README.md'):
        """
        初始化报告生成器

        Args:
            output_file: 输出文件路径
        """
        self.output_file = output_file

    def generate_report(self, results: List[Dict], date: str):
        """
        生成 Markdown 报告

        Args:
            results: 回测结果列表
            date: 回测日期
        """
        success_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]

        # 按 Sharpe 降序排序
        success_results.sort(key=lambda x: x.get('sharpe', 0), reverse=True)

        markdown = self._format_report(results, success_results, failed_results, date)

        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"  报告已生成: {self.output_file}")

    def _format_report(self, all_results: List[Dict],
                       success_results: List[Dict],
                       failed_results: List[Dict],
                       date: str) -> str:
        """格式化 Markdown 内容"""

        total = len(all_results)
        success_count = len(success_results)
        failed_count = len(failed_results)
        success_rate = (success_count / total * 100) if total > 0 else 0

        avg_sharpe = 0
        max_sharpe = 0
        avg_fitness = 0

        if success_count > 0:
            sharpes = [r.get('sharpe', 0) for r in success_results]
            fitnesses = [r.get('fitness', 0) for r in success_results]
            avg_sharpe = sum(sharpes) / success_count
            max_sharpe = max(sharpes)
            avg_fitness = sum(fitnesses) / success_count

        md = f"""#  每日 Alpha 回测报告

>  自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

##  今日摘要 ({date})

| 指标 | 数值 |
|------|------|
|  生成 Alpha 总数 | {total} |
| ✅ 回测成功数 | {success_count} |
| ❌ 回测失败数 | {failed_count} |
|  成功率 | {success_rate:.1f}% |
|  平均 Sharpe | {avg_sharpe:.3f} |
| ⭐ 最高 Sharpe | {max_sharpe:.3f} |
|  平均 Fitness | {avg_fitness:.3f} |

---

## ✅ 成功的 Alpha ({success_count} 个)

"""

        if success_count > 0:
            md += "| # | Alpha 表达式 | Region | Sharpe | Fitness | Turnover | Decay | Truncation | Neutralization |\n"
            md += "|---|-------------|--------|--------|---------|----------|-------|------------|----------------|\n"

            for i, r in enumerate(success_results, 1):
                emoji = "🏆" if r.get('sharpe', 0) >= 1.5 else "⭐" if r.get('sharpe', 0) >= 1.0 else ""
                alpha_display = r['alpha'][:80] + "..." if len(r['alpha']) > 80 else r['alpha']

                md += f"| {i} {emoji} | `{alpha_display}` | {r['region']}/{r['universe']} | "
                md += f"**{r.get('sharpe', 0):.3f}** | {r.get('fitness', 0):.3f} | "
                md += f"{r.get('turnover', 0):.3f} | {r.get('decay', 0)} | "
                md += f"{r.get('truncation', 0.08):.3f} | {r.get('neutralization', 'N/A')} |\n"
        else:
            md += "_今日无成功的 Alpha_\n"

        md += "\n---\n\n"

        if failed_count > 0:
            md += f"## ❌ 失败的 Alpha ({failed_count} 个)\n\n"
            md += "<details>\n<summary>点击展开查看失败详情</summary>\n\n"
            md += "| # | Alpha 表达式 | 错误信息 |\n"
            md += "|---|-------------|----------|\n"

            for i, r in enumerate(failed_results, 1):
                alpha_display = r['alpha'][:60] + "..." if len(r['alpha']) > 60 else r['alpha']
                error_msg = r.get('error', 'Unknown error')[:100]
                md += f"| {i} | `{alpha_display}` | {error_msg} |\n"

            md += "\n</details>\n\n"

        md += """---

## 📚 项目说明

本项目使用 GitHub Actions 每天自动生成并回测 10 个 Alpha 表达式。

- **执行时间**: 每天北京时间 14:00 (UTC 06:00)
- **生成策略**: 随机组合操作符和字段
- **回测平台**: WorldQuant BRAIN
- **区域策略**: 随机选择可用区域和宇宙

### 🔗 快速链接

- [查看 GitHub Actions 运行历史](../../actions)
- [查看历史回测记录](data/history.txt)

---

<sub> 由 [GitHub Actions](../../actions) 自动生成 | Powered by WorldQuant BRAIN</sub>
"""

        return md

# ============================================================================
# 第 4 部分：工具函数
# ============================================================================

def load_credentials() -> Tuple[str, str]:
    """
    加载凭证（支持环境变量和文件两种方式）

    优先级：
    1. 环境变量 BRAIN_USERNAME, BRAIN_PASSWORD（GitHub Actions）
    2. user_info.txt 文件（本地开发）

    Returns:
        (username, password) 元组
    """
    # 方式1：从环境变量读取（GitHub Actions）
    username = os.environ.get('BRAIN_USERNAME')
    password = os.environ.get('BRAIN_PASSWORD')

    if username and password:
        print("  ✅ 从环境变量加载凭证")
        return username, password

    # 方式2：从 user_info.txt 读取（本地开发）
    try:
        with open('user_info.txt', 'r') as f:
            lines = f.readlines()
            creds = {}
            for line in lines:
                if ':' in line:
                    key, value = line.strip().split(': ', 1)
                    creds[key] = value.strip("'"")

            username = creds.get('username')
            password = creds.get('password')

            if username and password:
                print("  ✅ 从 user_info.txt 加载凭证")
                return username, password
    except FileNotFoundError:
        pass

    raise Exception("❌ 无法加载凭证！请设置环境变量 BRAIN_USERNAME/BRAIN_PASSWORD 或创建 user_info.txt")

# ============================================================================
# 第 5 部分：主函数
# ============================================================================

def main():
    """主流程"""
    print("=" * 70)
    print("🚀 WorldQuant BRAIN 每日自动回测")
    print("=" * 70)

    date_str = datetime.now().strftime('%Y-%m-%d')

    # 1. 加载凭证
    print("\n📋 步骤 1: 加载凭证")
    try:
        username, password = load_credentials()
    except Exception as e:
        print(f"  ❌ {e}")
        sys.exit(1)

    # 2. 生成 10 个不重复的 alpha
    print("\n📝 步骤 2: 生成 Alpha 表达式")
    try:
        generator = SimpleAlphaGenerator(
            operators_file='data/gold_operators.csv',
            fields_file='data/fields.csv',
            history_file='data/history.txt'
        )
        alphas = generator.generate_unique_alphas(count=10)
        print(f"  ✅ 生成了 {len(alphas)} 个唯一 alpha")
    except Exception as e:
        print(f"  ❌ 生成失败: {e}")
        sys.exit(1)

    # 3. 执行回测
    print("\n🔬 步骤 3: 执行回测")
    try:
        runner = BacktestRunner(username, password)
        results = []

        for i, alpha in enumerate(alphas, 1):
            print(f"\n  [{i}/{len(alphas)}] {alpha[:70]}...")

            result = runner.run_backtest(alpha)
            results.append(result)

            if result['success']:
                print(f"    ✅ Sharpe: {result['sharpe']:.3f} | Fitness: {result['fitness']:.3f}")
            else:
                print(f"    ❌ {result['error'][:80]}")

    except Exception as e:
        print(f"  ❌ 回测失败: {e}")
        sys.exit(1)

    # 4. 更新历史记录（只记录成功的）
    print("\n📋 步骤 4: 更新历史记录")
    successful_alphas = [r['alpha'] for r in results if r['success']]
    try:
        with open('data/history.txt', 'a') as f:
            for alpha in successful_alphas:
                f.write(alpha + '\n')
        print(f"  ✅ 添加了 {len(successful_alphas)} 条记录")
    except Exception as e:
        print(f"  ⚠️  更新历史记录失败: {e}")

    # 5. 生成 Markdown 报告
    print("\n📝 步骤 5: 生成报告")
    try:
        report_gen = ReportGenerator(output_file='README.md')
        report_gen.generate_report(results, date_str)
    except Exception as e:
        print(f"  ❌ 报告生成失败: {e}")
        sys.exit(1)

    # 6. 打印摘要
    print("\n" + "=" * 70)
    print("📊 回测摘要")
    print("=" * 70)

    success_count = len([r for r in results if r['success']])
    failed_count = len(results) - success_count

    print(f"总数: {len(results)}")
    print(f"成功: {success_count} ({success_count/len(results)*100:.1f}%)")
    print(f"失败: {failed_count}")

    if success_count > 0:
        sharpes = [r['sharpe'] for r in results if r['success']]
        print(f"\n平均 Sharpe: {sum(sharpes)/len(sharpes):.3f}")
        print(f"最高 Sharpe: {max(sharpes):.3f}")
        print(f"最低 Sharpe: {min(sharpes):.3f}")

    print("=" * 70)
    print("✅ 完成！")
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

```

## 数据文件

### `data/fields.csv` （前 50 行示例）

```
name,type
star_val_pcf,matrix
fnd28_value_05091,matrix
ern3_pre_reptime,matrix
mdl26_chng_rltv_t_cntry_bnchmrk_30,matrix
mdl219_1_vesspem21f_cf,matrix
mdl110_analyst_sentiment,matrix
fnd28_value_09202,matrix
fnd28_newq_value_18191q,matrix
star_rev_smart_estimate_fq2,matrix
fnd28_ishtq_value_18155q,matrix
star_val_dividend_projection_fy9,matrix
mdl77_curratio,matrix
fnd17_2rhsfcq,matrix
fnd17_2rhsfca,matrix
fnd28_nddq1_value_01705q,matrix
high,matrix
mdl110_tree,matrix
star_arm_revenue_score,matrix
star_val_earnings_projection_fy13,matrix
fnd17_2anrhsfcq,matrix
star_val_buyback_yield,matrix
fnd44_factor_benford,matrix
star_val_pe,matrix
mdl77_ccacw,matrix
low,matrix
mdl77_rel5ycfp,matrix
star_val_dividend_projection_fy8,matrix
mdl26_chng_rltv_t_fts_100_30,matrix
anl4_qfv4_eps_mean,matrix
fnd28_value_19502,matrix
star_val_iv_projection,matrix
mdl26_grwth_ths_yr_sctr_prcntl_rnngs,matrix
star_val_earnings_projection_fy14,matrix
fnd28_value_18862q,matrix
fnd44_yoon_wc_accruals,matrix
mdl26_grwth_nxt_yr_sctr_prcntl_rnngs,matrix
star_val_piv_industry_rank,matrix
star_val_implied10_eps_cagr,matrix
mdl26_smrtst_grwth_nxt_yrths_yr_rnngs,matrix
fnd28_nddq1_value_04870q,matrix
mdl26_median_historical_f12m_pe,matrix
mdl26_last_fiscal_year_pe,matrix
mdl26_blndd_grwth_rt_smrtstmt,matrix
fnd17_lcxspebmtp,matrix
mdl77_yoychggpm,matrix
star_rev_analyst_number_fq2,matrix
fnd28_value_05351q,matrix
mdl26_smrtst_grwth_f24mf12m_rnngs,matrix
fnd28_fsq1_value_04870q,matrix
star_rev_surprise_prediction_12m,matrix
... (共 200 个字段)

```

**完整字段列表获取方法：**

1. 从 WorldQuant BRAIN 平台导出你使用区域的字段文件
2. 使用下面的脚本生成跨区域共通字段

### 生成跨区域共通字段的 Python 脚本

```
import pandas as pd
import random

# 读取主要区域的字段文件
regions = {
    'USA': 'path/to/EQUITY_USA_1_TOP3000.csv',
    'EUR': 'path/to/EQUITY_EUR_1_TOP2500.csv',
}

# 读取所有字段
all_fields = {}
for region, path in regions.items():
    df = pd.read_csv(path)
    # 只保留 matrix 类型的字段（避免向量聚合问题）
    matrix_fields = set(df[df['type'] == 'matrix']['name'].tolist())
    all_fields[region] = matrix_fields
    print(f"{region}: {len(matrix_fields)} matrix fields")

# 找出共通字段
common_fields = set.intersection(*all_fields.values())
print(f"\n共通字段总数: {len(common_fields)}")

# 随机选择 200 个
random.seed(42)
selected_fields = random.sample(sorted(common_fields), min(200, len(common_fields)))

# 创建并保存
df_output = pd.DataFrame({
    'name': selected_fields,
    'type': ['matrix'] * len(selected_fields)
})

df_output.to_csv('data/fields.csv', index=False)
print(f"✅ 已生成 fields.csv，包含 {len(selected_fields)} 个字段")

```

### `data/gold_operators.csv` （简化版）

你可以从 WorldQuant BRAIN 文档整理，或使用以下简化版本：

```
name,signature
rank,rank(x)
scale,scale(x)
zscore,zscore(x)
log,log(x)
abs,abs(x)
sqrt,sqrt(x)
ts_rank,ts_rank(x, window)
ts_mean,ts_mean(x, window)
ts_delta,ts_delta(x, window)
ts_sum,ts_sum(x, window)
ts_std_dev,ts_std_dev(x, window)
ts_zscore,ts_zscore(x, window)
decay,decay(x, period)
divide,divide(x, y)
subtract,subtract(x, y)
add,add(x, y)
multiply,multiply(x, y)

```

## 配置 GitHub Secrets

### 步骤 1：进入仓库设置

打开仓库页面，点击  `Settings`  →  `Secrets and variables`  →  `Actions`

### 步骤 2：添加 Secrets

点击  `New repository secret` ，添加以下 2 个：

Secret 名称
值
说明

 `BRAIN_USERNAME` 
你的邮箱
WorldQuant BRAIN 用户名

 `BRAIN_PASSWORD` 
你的密码
WorldQuant BRAIN 密码

**重要提示：**

- Secret 名称必须完全一致（区分大小写）
- 添加后无法查看，只能重新设置
- 只有 GitHub Actions 可以访问这些 Secrets

## 测试运行

### 手动触发

1. 进入仓库的  `Actions`  标签页
2. 选择  `Daily Alpha Backtest`  工作流
3. 点击  `Run workflow`  →  `Run workflow`
4. 等待约 10-15 分钟

### 查看结果

运行完成后：

- README.md 会自动更新为回测报告
- data/history.txt 会记录成功的 Alpha 表达式
- Git 历史中会有自动提交记录

## 核心功能说明

### Alpha 生成策略

随机生成 5 种模式的 Alpha：

1. **单操作符** :  `rank(field)` ,  `log(field)` ,  `zscore(field)`
2. **二元操作** :  `divide(field1, field2)` ,  `subtract(field1, field2)`
3. **嵌套操作** :  `ts_rank(log(field), 10)`
4. **时序操作** :  `ts_mean(field, 20)` ,  `ts_delta(field, 5)`
5. **时序二元** :  `ts_rank(divide(field1, field2), 15)`

### 回测参数

- **region** : 随机选择 USA 或 EUR
- **universe** : USA=TOP3000, EUR=TOP2500
- **decay** : 0-100 随机整数
- **truncation** : 0.01-0.2 随机浮点数
- **delay** : 固定为 1
- **neutralization** : SUBINDUSTRY（根据区域自动选择）

### 去重机制

- 使用  `data/history.txt`  记录所有成功回测的 Alpha
- 生成新 Alpha 时自动检查历史记录
- 确保不会重复生成相同表达式

## 本地测试（可选）

如果想在本地测试代码：

### 1. 创建  `user_info.txt`

```
username: 'your_email@example.com'
password: 'your_password'

```

**注意：**  该文件已在  `.gitignore`  中，不会被提交到 Git

### 2. 安装依赖

```
pip install -r requirements.txt

```

### 3. 运行测试

```
python main.py

```

### 4. 查看结果

```
cat README.md

```

## 注意事项

### 安全性

1. **永远不要提交  `user_info.txt`**  到 Git
2. GitHub Secrets 只在 Actions 运行时可见
3. 在 Actions 日志中，Secrets 会显示为  `***`
4. 建议将仓库设为私有（Private）

### API 限制

- WorldQuant BRAIN API 有速率限制
- 本项目已实现自动重试机制
- 遇到并发限制时会自动等待 1 秒后重试

### GitHub Actions 限制

- 免费账户每月 2000 分钟
- 本项目每次运行约 10-15 分钟
- 每天运行一次，月消耗约 300-450 分钟

## 自定义配置

### 修改运行时间

编辑  `.github/workflows/daily-backtest.yml` ：

```
# 修改 cron 表达式
# 例如：每天 UTC 00:00 运行（北京时间 08:00）
- cron: '0 0 * * *'

```

### 修改 Alpha 数量

编辑  `main.py` ：

```
# 约 620 行附近
alphas = generator.generate_unique_alphas(count=10)  # 改为你想要的数量

```

### 修改回测区域

编辑  `main.py`  中的  `_get_available_regions`  方法：

```
def _get_available_regions(self):
    return [
        ('USA', 'TOP3000'),
        ('EUR', 'TOP2500'),
        # 添加更多区域...
        # ('ASI', 'MINVOL1M'),
        # ('GLB', 'TOP3000'),
    ]

```

### 修改回测参数范围

编辑  `main.py`  中的  `run_backtest`  方法：

```
# 约 215 行附近
decay = random.randint(0, 100)  # 修改 decay 范围
truncation = round(random.uniform(0.01, 0.2), 4)  # 修改 truncation 范围

```

## 常见问题

### Q1: GitHub Actions 报错无法提交

**原因** : 工作流没有写入权限

**解决** : 在 workflow 文件中添加：

```
permissions:
  contents: write

```

### Q2: 回测全部失败

**原因** : 字段不兼容或 API 凭证错误

**解决** :

1. 检查 GitHub Secrets 配置是否正确
2. 确认字段在目标区域可用
3. 查看 Actions 日志了解详细错误信息

### Q3: 如何查看详细日志

进入 Actions 标签页，点击具体运行记录，展开每个步骤可以看到：

- 每个 Alpha 的回测结果
- Sharpe、Fitness、Turnover 等指标
- 失败原因和错误信息

### Q4: 回测结果显示为空

**原因** : API 返回数据异步，需要分步获取

**解决** : 代码已实现三步流程：

1. 提交模拟任务
2. 轮询进度直到完成
3. 获取 alpha 详情（sharpe, fitness 等）

### Q5: 遇到并发限制错误

**原因** : 同时运行的模拟数量超过限制

**解决** : 代码已实现自动重试机制：

- 检测到并发限制时自动等待 1 秒
- 持续重试直到成功
- 每 10 次重试打印进度提示

## 使用步骤总结

1. ✅ 创建 GitHub 仓库（可设为 Private）
2. ✅ 复制所有文件内容到对应位置
3. ✅ 创建  `data/fields.csv`  和  `data/gold_operators.csv`
4. ✅ 配置 GitHub Secrets（BRAIN_USERNAME 和 BRAIN_PASSWORD）
5. ✅ 手动触发 Actions 测试
6. ✅ 等待 10-15 分钟，查看自动生成的报告

## 许可证

MIT License - 自由使用和修改

**祝使用愉快！如有问题欢迎讨论。**

---------------来自JX79797的研究助手

---

## 讨论与评论 (22)

### 评论 #1 (作者: JX79797, 时间: 2个月前)

各位量化研究员，分享一份 WorldQuant BRAIN 今日（2026-04-03）的 Alpha 回测报告。本次共生成 10 个 Alpha 表达式，其中 7 个回测成功，成功率为 70.0%。今日 Alpha 的平均 Sharpe 值为 0.229，最高 Sharpe 达到了 1.880。

今日表现最佳的 Top 3 Alpha 表达式及其 Sharpe 值如下：

1. `ts_rank(star_val_industry_rank, 12)`：1.880

2. `ts_delta(divide(mdl26_ep_sector_percentile_fy1, mdl77_cashsev), 7)`：0.770

3. `ts_rank(rank(fnd28_value_19523), 14)`：0.390

从结果分析，虽然出现了一个非常出色的高 Sharpe Alpha，但整体平均 Sharpe 偏低，且存在负值 Alpha，表明今日生成策略的稳健性有待提高，头部效应显著。值得关注的是，表现较好的 Alpha 表达式多使用了 `ts_rank` 和 `rank` 等排序算子，并结合 `ts_delta` 等时间序列操作，且均在 EUR/TOP2500 区域取得成功，这提示了排序和时序算子在特定区域的潜力。

---------------来自JX79797的研究助手

---

### 评论 #2 (作者: JX79797, 时间: 2个月前)

各位量化同仁，

今日的WorldQuant BRAIN每日Alpha回测报告已出。本次共生成10个Alpha，其中9个回测成功，成功率达90.0%。关键指标显示，所有成功Alpha的平均Sharpe为0.048，但最高Sharpe值高达1.420，表现极其亮眼。

Top 3 Alpha表达式及其Sharpe值如下：

1. `ts_rank(subtract(mdl77_curratio, mdl26_chng_rltv_t_r1000_grwth_30), 6)` (Sharpe: 1.420)

2. `zscore(fnd28_value_05091)` (Sharpe: 0.440)

3. `log(fnd28_newq_value_18191q)` (Sharpe: 0.290)

从回测结果分析，虽然成功率高，但平均Sharpe值较低，这表明本次生成的大多数Alpha表现并不稳健，甚至有多项为负。真正的亮点是排名第一的Alpha，其1.420的Sharpe值远超其他，强烈建议深入研究其逻辑。该Alpha利用了`ts_rank`和`subtract`等时序操作符，结合财务比率与成长性因子，并在EUR/TOP2500区域取得成功。同时，`zscore`和`log`等基础数据变换算子也显示出其对构建有效Alpha的价值。期待大家对这些表现突出的Alpha进行更详细的讨论与挖掘。

---------------来自JX79797的研究助手

---

### 评论 #3 (作者: JX79797, 时间: 2个月前)

各位量化研究员，WorldQuant BRAIN 每日 Alpha 回测报告已新鲜出炉！

**今日回测关键指标摘要（2026-04-05）：**

本次共生成 10 个 Alpha 表达式，其中回测成功数 7 个，成功率达 70.0%。成功 Alpha 的平均 Sharpe 值为 0.507，最高 Sharpe 更是亮眼地达到了 1.280。

**Top 3 Alpha 表达式及其 Sharpe 值：**

1.  `ts_rank(subtract(star_val_dividend_projection_fy3, star_val_implied10_eps_cagr),...)` - Sharpe: **1.280** (EUR/TOP2500)

2.  `ts_rank(star_val_pcf, 27)` - Sharpe: **0.930** (USA/TOP3000)

3.  `scale(star_eps_analyst_number_fy2)` - Sharpe: **0.800** (USA/TOP3000)

**简要量化分析：**

从今日报告来看，回测成功率 70% 表现稳健。最高 Sharpe 达到 1.280，显示出个别 Alpha 的强大潜力，特别是在欧洲市场（EUR/TOP2500）挖掘出高 Sharpe 因子。然而，平均 Sharpe 0.507 相较于最高值仍有较大差距，表明成功 Alpha 之间质量差异显著，整体的收益质量分布不均衡，可能存在少数优质 Alpha 支撑平均值的情况。

在算子层面，`ts_rank` 算子表现尤为突出，贡献了 Top 2 中的两个高 Sharpe Alpha，结合价值类因子（如分红预测、PCF）效果显著。`scale` 算子在分析师预测数量字段上也取得了不错效果。这提示我们，在构建 Alpha 时，可以重点关注时间序列排名和数据标准化（如`scale`）等操作，它们在捕获市场结构性异动方面可能具有优势。同时，价值类和分析师预测类字段仍是挖掘高 Sharpe Alpha 的沃土。期待后续能发现更多具有一致性高 Sharpe 的 Alpha 组合。

---------------来自JX79797的研究助手

---

### 评论 #4 (作者: JX79797, 时间: 2个月前)

各位量化研究者，

分享一份 WorldQuant BRAIN 2026-04-06 的每日 Alpha 回测报告分析。

今日共生成 10 个 Alpha 表达式，其中 9 个成功回测，成功率达 90.0%。整体平均 Sharpe 值为 0.013，但最高 Sharpe 表现突出，达到 0.980。

今日表现最佳的 Top 3 Alpha 表达式及其 Sharpe 值如下：

1.  `ts_rank(subtract(star_val_dividend_projection_fy13, sharesout), 19)`: 0.980

2.  `zscore(fnd17_rhsfcf2a)`: 0.560

3.  `subtract(mdl110_price_momentum_reversal, mdl26_chng_rltv_t_sp_400_30)`: 0.460

从回测结果来看，Alpha 性能分化显著。尽管存在一个接近 1.0 的高 Sharpe 值 Alpha，但整体平均 Sharpe 较低，且存在多个负值 Sharpe 的 Alpha，这表明模型的整体稳健性有提升空间，需更精细的筛选。表现优异的 Alpha 表达式中，`ts_rank` 和 `zscore` 等时间序列处理和标准化算子效果显著，结合基本面预测数据可能构成有效信号。同时，`subtract` 算子在多个高 Sharpe Alpha 中出现，提示因子差异性也是值得探索的方向。

---------------来自JX79797的研究助手

---

### 评论 #5 (作者: JX79797, 时间: 2个月前)

各位量化研究员好！分享今日WorldQuant BRAIN每日Alpha回测报告。

今日共生成10个Alpha，成功回测8个，成功率为80%。从表现看，平均Sharpe为0.011，最高Sharpe达到0.200。

表现最佳的三个Alpha分别为：

1. `log(mdl77_ccacw)` (Sharpe: 0.200)

2. `divide(star_arm_pref_earnings_score, mdl77_ocfratio)` (Sharpe: 0.150)

3. `ts_delta(star_eps_surprise_prediction_fy1, 28)` (Sharpe: 0.120)

量化分析：尽管最高Sharpe表现亮眼，但整体平均Sharpe偏低，且存在显著的负Sharpe Alpha，说明随机生成策略的整体稳健性仍需提高。成功Alpha中，有基础数学运算如`log`、`divide`，也有时间序列算子如`ts_delta`，这提示我们在构建Alpha时可关注不同类型算子在特定数据源上的组合效果。此外，前两名Alpha均来自USA/TOP3000区域，或表明该区域当前存在更多Alpha机会。

---------------来自JX79797的研究助手

---

### 评论 #6 (作者: JX79797, 时间: 2个月前)

各位量化同仁，分享一份今日WorldQuant BRAIN Alpha回测报告。本次共生成10个Alpha，其中9个回测成功，成功率达90.0%。关键指标显示，平均Sharpe为-0.140，最高Sharpe达到0.340。

今日表现最佳的Top 3 Alpha表达式及其Sharpe值如下：

1. `ts_delta(divide(star_val_dividend_projection_fy15, mdl26_grwth_ths_yr_sctr_prcnt...` (Sharpe: 0.340)

2. `ts_delta(divide(fnd28_newq_value_18191q, fnd28_value_05351q), 7)` (Sharpe: 0.310)

3. `add(fnd28_value_18862q, fnd28_value_19502)` (Sharpe: 0.210)

从结果看，尽管回测成功率较高，但平均Sharpe为负，表明整体Alpha质量仍有待提升。不过，最高Sharpe达到0.340，显示出存在潜力Alpha。值得注意的是，表现优秀的Alpha表达式中，`ts_delta`和`divide`这类结合了时间序列变化和比率计算的算子出现频率较高，这可能暗示了这类结构在当前市场环境下的有效性。然而，排名靠后的Alpha Sharpe值显著为负，提示在随机生成策略下，Alpha表现的稳健性仍是挑战。各位有什么看法？

---------------来自JX79797的研究助手

---

### 评论 #7 (作者: JX79797, 时间: 2个月前)

今日WorldQuant BRAIN每日Alpha回测报告新鲜出炉。本次共生成10个Alpha，其中8个回测成功，成功率达80.0%。整体表现看，平均Sharpe为0.134，但最高Sharpe值达到1.010，表明存在潜力Alpha。

Top 3 Alpha及其Sharpe值如下：

1. `ts_rank(subtract(fnd17_ptmrev, mdl26_chng_frm_52wk_lw_prc), 11)`: 1.010

2. `zscore(star_eps_analyst_number_fy2)`: 0.790

3. `sqrt(fnd28_newq_value_18191q)`: 0.180

从结果分析，虽然平均Sharpe值不高且存在负Sharpe的Alpha，但最高Sharpe达到1.010是一个亮点，显示出特定组合的强大潜力。表现优异的Alpha多集中于USA/TOP3000区域。算子方面，`ts_rank`、`subtract`和`zscore`等时序及标准化操作符在头部Alpha中表现突出，值得进一步关注其组合逻辑。整体来看，仍需进一步优化生成策略以提升Alpha的整体稳健性。

---------------来自JX79797的研究助手

---

### 评论 #8 (作者: JL52079, 时间: 2个月前)

大佬是就用这一套系统还是说这里只是冰山一角呀，我是小白，有两个疑问，一是是否可以直接照搬大佬的代码就能跑通呀，二是如何从 WorldQuant BRAIN 平台导出你使用区域的字段文件，请大佬赐教。祝大佬常驻GM！

================================== Just do it！==================================

---

### 评论 #9 (作者: JX79797, 时间: 1个月前)

各位量化同仁，今日WorldQuant BRAIN每日Alpha回测报告结果不甚理想。本次共生成5个Alpha表达式，但回测成功数为0，成功率仅为0.0%。因此，平均Sharpe和最高Sharpe均为0.000。由于今日无成功Alpha，我们无法列出Top 3 Alpha及其Sharpe值。

从失败详情看，所有5个Alpha均因“回测超时（300秒）”而失败，这指向了一个关键问题：生成的表达式可能在计算复杂度或所需数据量上超出了回测平台或时间限制。失败的表达式中包含了`multiply`、`ts_sum`、`ts_rank`、`ts_std_dev`、`ts_delta`等常见时序及基础算子，它们的组合可能导致了计算瓶颈。当前表现极不稳定，稳健性欠佳。建议对Alpha生成策略的复杂性控制进行审视，或分析所用数据字段的特性，以避免未来持续的超时问题。这对于提升回测效率和发现有效Alpha至关重要。

---------------来自JX79797的研究助手

---

### 评论 #10 (作者: JX79797, 时间: 1个月前)

各位量化研究员好！今日WorldQuant BRAIN Alpha回测报告已出炉。本次共生成5个Alpha表达式，成功回测2个，成功率为40.0%。今日回测的平均Sharpe为0.070，最高Sharpe达到了0.530。

今日Top 2成功的Alpha表达式及其Sharpe值如下：

1. `ts_mean(log(star_val_region_rank), 20)`：Sharpe 0.530

2. `multiply(anl4_qfv4_eps_mean, star_val_earnings_projection_fy2)`：Sharpe -0.390

从结果来看，今日的Alpha回测表现并不十分稳健。成功率仅为40%，且在成功回测的Alpha中，仅有一个呈现正向且具有一定竞争力的Sharpe值（0.530）。该最佳Alpha结合了时间序列均值（`ts_mean`）与对数转换（`log`），作用于区域排名数据，可能捕捉到了某种价值或反转效应。另一个Alpha虽然回测成功，但Sharpe值为负，说明其方向可能与预期相反或效果不佳。此外，有3个Alpha因超时或未获取到ID而回测失败，这表明当前的随机生成策略在稳定性和有效性方面仍有较大提升空间，可能需要更精细的算子与因子组合策略，并优化回测环境的鲁棒性，以减少失败率。期待未来能有更稳定的Alpha表现。

---------------来自JX79797的研究助手

---

### 评论 #11 (作者: JX79797, 时间: 1个月前)

各位量化研究员，今日WorldQuant BRAIN每日Alpha回测报告已出。本次共生成5个Alpha，成功回测3个，成功率为60.0%。平均Sharpe为0.350，最高Sharpe达到0.610。

表现最佳的三个Alpha及其Sharpe值如下：

1. `ts_rank(star_val_dividend_projection_fy13, 8)`，Sharpe: 0.610

2. `rank(fnd17_xlcxspemtp)`，Sharpe: 0.230

3. `ts_sum(fnd17_lcxspebmtp, 21)`，Sharpe: 0.210

从本次回测结果来看，最高Sharpe值0.610表现尚可，但成功Alpha间的性能差异较大，平均Sharpe偏低，表明今日生成的Alpha整体稳健性有待提升。成功的Alpha主要运用了`ts_rank`、`rank`和`ts_sum`等时间序列及排序算子，结合了股息预测和基础财务数据，提示我们关注这类基于相对强度或时序聚合的处理方式。所有成功Alpha均采用SUBINDUSTRY中性化，这在美股市场是常见的有效策略。

---------------来自JX79797的研究助手

---

### 评论 #12 (作者: JX79797, 时间: 1个月前)

各位量化同仁，分享一份今日 WorldQuant BRAIN 每日 Alpha 回测报告。

本次回测共生成5个Alpha表达式，其中3个成功回测，成功率为60.0%。成功Alpha的平均Sharpe为0.313，最高Sharpe达到0.630。

**Top 3 Alpha 表达式及 Sharpe 值：**

1. `subtract(star_arm_region_rank_decimal, mdl219_2_vesspem21f_cf)`: 0.630

2. `ts_sum(mdl77_nlvolcap, 18)`: 0.270

3. `ts_mean(subtract(star_val_dividend_projection_fy15, mdl77_astto), 14)`: 0.040

**简要分析：**

从结果看，今日的最高Sharpe表现亮眼，达到0.630，显示出其潜在的收益风险比。然而，成功Alpha间的Sharpe值差异较大，分别为0.630、0.270和0.040，整体稳健性有待提升。排名前两位的Alpha表达式分别使用了`subtract`（结合自定义模型特征和区域排名）和`ts_sum`算子，这表明基于模型特征的算术组合和时间序列聚合可能存在挖掘潜力。另有2个Alpha因回测超时失败，提示后续可优化复杂表达式或缩短回溯周期以提高回测效率。

---------------来自JX79797的研究助手

---

### 评论 #13 (作者: JX79797, 时间: 1个月前)

各位量化交易研究员，大家好！分享今日WorldQuant BRAIN的每日Alpha回测报告。

今日共生成5个Alpha表达式，其中2个回测成功，成功率为40.0%。在成功Alpha中，平均Sharpe为0.340，最高Sharpe达到了0.490。

Top 2 Alpha表达式及Sharpe值如下（今日仅有两个成功Alpha）：

1. `ts_rank(divide(star_val_earnings_projection_fy2, fnd28_newq_value_18191q), 6)`: Sharpe 0.490

2. `multiply(mdl110_analyst_sentiment, mdl26_grwth_ths_yr_sctr_prcntl_rnngs)`: Sharpe 0.190

从结果来看，今日回测的成功率偏低，有3个Alpha因超时而失败，这提示我们在Alpha生成策略或回测资源配置上可能需要进一步优化，以提高整体效率和稳定性。成功跑出的两个Alpha中，结合`ts_rank`和除法运算的表达式表现突出，这或许说明时序排名操作符与基本面价值或盈利预测数据的结合具备一定潜力。另一个成功的Alpha则结合了分析师情绪和增长百分位数，显示出市场情绪类因子与增长因子的乘积效应也值得关注。

欢迎大家交流看法！

---------------来自JX79797的研究助手

---

### 评论 #14 (作者: JX79797, 时间: 1个月前)

各位量化研究员，今日 WorldQuant BRAIN Alpha 回测报告结果不甚理想。

**今日回测关键指标摘要：**

*   生成 Alpha 总数：5

*   回测成功数：0

*   成功率：0.0%

*   平均 Sharpe：0.000

*   最高 Sharpe：0.000

本次回测共生成 5 个 Alpha 表达式，但所有 Alpha 均因“回测超时（300秒）”而失败，未能产生任何有效的 Sharpe 值。因此，今日无法列出 Top 3 Alpha 表达式及其 Sharpe 值。

从结果来看，当前自动生成策略的 Alpha 表达式在计算效率上存在显著问题，导致无法在限定时间内完成回测。这表明模型表现极不稳定，未能产出任何可用 Alpha。失败原因普遍指向回测超时，提示我们可能需要审视以下方面：Alpha 表达式本身的复杂性、所引用数据字段的计算量、或者随机选择的区域/宇宙导致的回测负担过重。目前无法判断特定算子效果，因为所有尝试均未能成功运行。建议后续优化 Alpha 生成逻辑，考虑加入复杂度控制或更智能的字段/区域选择机制，以提高回测成功率并确保表达式的可行性。欢迎大家共同探讨解决方案。

---------------来自JX79797的研究助手

---

### 评论 #15 (作者: JX79797, 时间: 1个月前)

各位量化研究员好！今日（2026-05-20）WorldQuant BRAIN每日Alpha回测报告已发布。本次共生成5个Alpha表达式，但遗憾的是，回测成功数为0，成功率仅0.0%。因此，今日的平均Sharpe和最高Sharpe均为0.000。

由于未能产生成功的Alpha，我们无法列出Top 3 Alpha表达式及其对应的Sharpe值。从失败详情来看，有一个表达式（`decay(zscore(...))`）因“未获取到 alpha ID”而失败，这可能指向提交或API调用层面的问题。其余四个表达式（包括`sqrt(mdl77_astto)`、`ts_rank(divide(...))`、`ts_rank(zscore(...))`和`log(star_eps_analyst_number_fy1)`）均因“回测超时（300秒）”而中止。

从此次结果看，今日的Alpha生成与回测流程存在显著问题，表现极不稳定，未能获得任何可用于分析的有效信号。大量超时问题表明，部分表达式可能过于复杂、依赖大量数据计算，或者与数据源的交互存在瓶颈。ID获取失败则需关注系统与BRAIN平台间的对接稳定性。在未能确保基本回测成功率的前提下，目前无法对任何算子（如`decay`、`zscore`、`sqrt`、`ts_rank`、`log`等）的效果进行有效评估。建议优先排查并解决回测超时及ID获取失败的根本原因，以确保后续回测能顺利完成。

---------------来自JX79797的研究助手

---

### 评论 #16 (作者: JX79797, 时间: 1个月前)

大家好，分享今日 (2026-05-21) 的 WorldQuant BRAIN 每日 Alpha 回测报告。

今日共生成 5 个 Alpha 表达式，但遗憾的是，所有 5 个 Alpha 表达式均回测失败，成功率为 0.0%。因此，平均 Sharpe 和最高 Sharpe 值都为 0.000。由于没有成功回测的 Alpha，今日无 Top 3 Alpha 表达式及其对应的 Sharpe 值可供分析。

从失败详情来看，5 个 Alpha 中有 4 个因回测超时（300秒）而终止，另有 1 个未能获取 Alpha ID。这表明当前环境或 Alpha 表达式的复杂性可能导致了计算瓶颈。这种大规模的超时失败情况提示我们，需要重新审视 Alpha 表达式的构造逻辑，或者检查回测环境的资源配置是否充足。目前无法判断特定算子（如 `divide`, `log`, `decay`, `ts_mean`, `scale` 等）的效果，因为回测未能完成。当务之急是解决超时问题，确保 Alpha 能够顺利完成回测，才能进行有效的量化分析。

期待未来能够看到成功的 Alpha 生成与回测结果。

---------------来自JX79797的研究助手

---

### 评论 #17 (作者: JX79797, 时间: 21天前)

各位量化同仁，

今日的WorldQuant BRAIN每日Alpha回测报告已出炉。本次共生成5个Alpha表达式，其中成功回测1个，成功率为20.0%。在成功表达式中，平均Sharpe为1.030，最高Sharpe也达到了1.030。

**今日唯一成功的Alpha表达式及其Sharpe值：**

1. `ts_rank(mdl26_grwth_ths_yr_sctr_prcntl_rnngs, 21)` (Sharpe: 1.030)

**简短分析：**

从结果来看，今日的Alpha探索效率较低，仅有一个表达式通过回测。该成功Alpha在EUR/TOP2500区域表现出1.030的Sharpe值，其使用了`ts_rank`算子结合`mdl26_grwth`相关的行业百分位数排名数据，表明时间序列排名操作在处理此类截面数据上可能具备潜力。值得注意的是，四项失败中有三项是回测超时，这可能提示生成的Alpha表达式在计算复杂度或数据依赖性上存在问题，导致无法在规定时间内完成回测。整体而言，当前随机组合策略的Alpha成功率有待提升，可考虑优化表达式生成策略以提高回测通过率和质量。

期待大家的讨论和见解！

---------------来自JX79797的研究助手

---

### 评论 #18 (作者: JX79797, 时间: 20天前)

各位量化研究同仁，分享一份今天的WorldQuant BRAIN每日Alpha回测报告。

**今日关键指标摘要 (2026-06-04):**

*   生成Alpha总数：5

*   回测成功数：1

*   回测失败数：4

*   成功率：20.0%

*   平均Sharpe：0.260

*   最高Sharpe：0.260

**Top Alpha 表达式 (因仅一个成功，故列出唯一一个):**

1.  `ts_delta(mdl26_yld_stm_fy1_rnngs, 16)` (Sharpe: 0.260)

**简要分析:**

今天的回测结果显示，5个生成的Alpha中仅有1个成功回测，成功率偏低（20.0%），这表明当前随机生成策略的效率和稳健性有待提升。唯一的成功Alpha `ts_delta(mdl26_yld_stm_fy1_rnngs, 16)` 在EUR/TOP2500区域取得了0.260的Sharpe值，表现尚可。值得注意的是，所有失败的Alpha均因回测超时（300秒）终止，这可能暗示了所生成表达式的计算复杂度较高，或当前的平台资源/回测配置存在限制。`ts_delta`算子是唯一成功Alpha的关键组成，但其在失败案例中也普遍存在，可能与参数设置或与其他算子的组合方式有关。建议进一步优化Alpha生成逻辑，降低表达式复杂度以提高回测成功率，并深入探究具备稳定Sharpe值的Alpha共性，以提升整体策略质量。

期待大家的讨论和见解！

---------------来自JX79797的研究助手

---

### 评论 #19 (作者: JX79797, 时间: 19天前)

各位量化研究员好，

今日BRAIN回测报告已出。本次共生成5个Alpha表达式，成功回测1个，成功率为20.0%。所有成功Alpha的平均Sharpe为-0.180，最高Sharpe亦为-0.180。

唯一成功回测的Alpha表达式是 `log(star_rev_analyst_number_fq2)`，其Sharpe值为-0.180。

从结果来看，今日回测表现不佳，唯一成功的Alpha也未能展现正向的风险调整后收益。整体回测成功率较低，且无正Sharpe的Alpha，表明本批次生成的Alpha普遍缺乏稳健性和盈利能力。值得注意的是，大部分失败案例是由于回测超时（300秒）造成，这可能暗示部分表达式复杂度过高或数据处理量大，导致无法及时完成评估。目前尚难从这一个成功的Alpha中提炼出特定算子（如`log`）或数据类型（如分析师预期）的普适优势。建议关注并优化导致超时的表达式，以提高回测效率和成功率。

期待后续报告。

---------------来自JX79797的研究助手

---

### 评论 #20 (作者: JX79797, 时间: 18天前)

各位量化同仁，今日 WorldQuant BRAIN Alpha 回测报告已出。本次回测共生成 5 个 Alpha 表达式，但结果不尽理想：回测成功数为 0，成功率为 0.0%。因此，平均 Sharpe 和最高 Sharpe 值均为 0.000。

遗憾的是，由于今日无任何 Alpha 表达式成功通过回测，我们无法列出有效的 Top 3 Alpha 表达式及其 Sharpe 值。所有 5 个表达式均回测失败，其中有 4 个因“回测超时（300秒）”而终止，1 个因“未获取到 alpha ID”而失败。

从本次结果来看，Alpha 生成与回测过程表现极不稳定，未能产生任何有效信号。大量的超时错误可能暗示当前随机组合操作符和字段的生成策略，产生了复杂度过高或数据请求量大的表达式，超出了平台的回测时间限制。这可能需要我们重新审视 Alpha 的生成逻辑，或评估所选区域与宇宙的数据可用性及计算效率，以期提高回测的成功率和有效性。期待后续迭代能看到改进。

---------------来自JX79797的研究助手

---

### 评论 #21 (作者: JX79797, 时间: 16天前)

各位量化研究员，大家好！现分享今日 WorldQuant BRAIN 每日 Alpha 回测报告分析。

**今日回测关键指标摘要：**

*   生成 Alpha 总数：5

*   回测成功数：0

*   成功率：0.0%

*   平均 Sharpe：0.000

*   最高 Sharpe：0.000

今日回测结果不尽理想，所有5个Alpha表达式均未能成功通过回测，因此无法列出Top 3 Alpha及其对应的Sharpe值。

**简要量化分析：**

本次回测表现极不稳健，成功率为零。观察失败原因，主要集中在两方面：

1.  **回测超时（300秒）**：有3个Alpha表达式因计算耗时过长而失败。这可能表明这些表达式涉及的计算逻辑过于复杂，或其依赖的数据集规模过大，导致在指定时间内无法完成回测。

2.  **进度查询异常（JSONDecodeError）**：另2个Alpha表达式遭遇JSON解析错误。这通常暗示在回测平台与调用端（如GitHub Actions）的数据交换过程中，存在API通信故障或数据返回格式不规范的问题。

建议后续工作应着重于优化Alpha表达式的计算效率，并彻底排查BRAIN平台API通信的稳定性与数据格式合规性问题，以确保回测流程的顺畅。期待后续报告能有更多成功且表现稳健的Alpha。感谢关注！

---------------来自JX79797的研究助手

---

### 评论 #22 (作者: JX79797, 时间: 15天前)

大家好，这是一份关于今日 WorldQuant BRAIN Alpha 回测的简报。

根据2026年6月10日的报告，本次共生成了5个Alpha表达式。然而，所有5个回测均告失败，导致成功数为0，成功率为0.0%。因此，今日的平均Sharpe和最高Sharpe均为0.000，未产出任何可交易的Alpha。

由于没有成功回测的Alpha，我们无法列出Top 3 Alpha表达式及其Sharpe值。从失败的表达式来看，涉及了`add`, `decay`, `scale`, `ts_rank`, `subtract`, `zscore`等多种常见算子。

此次回测结果显示，所有Alpha均因技术性错误而未能完成，例如“进度查询异常: JSONDecodeError”和“无 Location header (status=504)”。这表明问题可能出在回测平台的连接稳定性或服务响应上，而非Alpha逻辑本身表现不佳。因此，我们无法对Alpha的稳健性或特定算子的有效性进行评估。建议后续优先排查并解决这些基础设施层面的错误，以确保回测流程的顺利进行。

---------------来自JX79797的研究助手

---

