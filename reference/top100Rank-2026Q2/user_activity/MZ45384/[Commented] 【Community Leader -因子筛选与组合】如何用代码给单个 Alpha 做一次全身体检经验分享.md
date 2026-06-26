# 【Community Leader -因子筛选与组合⭐】如何用代码给单个 Alpha 做一次全身体检经验分享

- **链接**: [Commented] 【Community Leader -因子筛选与组合】如何用代码给单个 Alpha 做一次全身体检经验分享.md
- **作者**: PP26750
- **发布时间/热度**: 6个月前, 得票: 13

## 帖子正文

我们每天都会生产成几千个Alpha，如果单纯的对Sharpe或者Fitness进行降序排序，这很可能无法直接找到合适的alpha，可能会找到一个厂或者是一个换手率和回测都极高的alpha，这时候如何从海量因子中筛选出真正具有价值的哪一个，就成了最头疼的问题

下面我分享一套评分逻辑。它的作用很简单：把对单因子的“好坏判断”，量化成一个0到 **约140** 的确切分数。可以让我们一眼看出这个alpha的是好是坏。

这段代码的核心逻辑，就是强行把单个alpha拉到一个多维坐标系里，进行一次“全身体检”。并且你可以自定义各个指标的权重和阈值，并且你完全可以将你平时挑选alpha的直觉，映射到这个代码中。让它替你实现全自动的alpha筛选。

下面举几个例子：

![图片](images/img_a2a88d7fe8.png)

0分

![图片](images/img_57b3381dd0.png)

136.77分

这个代码还有一个实用功能，就是它可以检测alpha是不是厂，结果我的测试这个功能的准确率是有百分之八十的，像下面这个alpha。

![图片](images/img_da6143d371.png)

各个指标都正常，且非常的优秀，但是它的pnl是不正常的，这种情况单看指标是无法判断的，在外面看着是一个很好的指标，进入页面一看pnl那是非常的痛苦啊。

![图片](images/img_0b3159f2ed.png)

我们的代码对于这样的alpha是会进行惩罚的，对于这个alpha它的分数只有67.83算是不及格的。

def evaluate_alpha_potential_train(alpha_data: dict, custom_weights: dict = None) -> dict:

# --- 1. 定义评估指标的合格标准 ---

limits = {

'sharpe': {'limit': 1.0, 'type': 'ge'},  # greater than or equal

'fitness': {'limit': 1.0, 'type': 'ge'},

'turnover': {'lower_limit': 0.05, 'upper_limit': 0.3, 'type': 'range'},

'weight_concentration': {'limit': 0.1, 'type': 'le'},

'sub_universe_sharpe': {'limit': 0.5, 'type': 'ge'},

'returns_drawdown_ratio': {'limit': 1.2, 'type': 'ge'},

'margin': {'limit': 0.0005, 'type': 'ge'}

}

# --- 2. 定义各项指标的默认权重 ---

# Sharpe 和 Fitness 最重要，Turnover次之

default_weights = {

'sharpe': 2.5,

'fitness': 3.0,

'turnover': 2.0,

'weight_concentration': 0.5,

'sub_universe_sharpe': 0.5,

'returns_drawdown_ratio': 2.0,

'margin': 1.0

}

weights = custom_weights if custom_weights is not None else default_weights

metrics = {}

alpha_data = alpha_data.get("is", {})

metrics = {'sharpe': alpha_data.get('sharpe', 0), 'fitness': alpha_data.get('fitness', 0),

'turnover': alpha_data.get('turnover', 1),

'weight_concentration': alpha_data.get('weight_concentration', 1),

'sub_universe_sharpe': alpha_data.get("sub_universe_sharpe", 0.0)}

# 使用 train_data 中的 checks 列表

for check in alpha_data.get('checks', []):

name = check.get("name", " ")

if "LOW_SUB_UNIVERSE_SHARPE" == name:

metrics['sub_universe_sharpe'] = check.get("value", 0.01)

limits['sub_universe_sharpe']['limit'] = check.get("limit", 0)

if limits['sub_universe_sharpe']['limit'] <= 0.0:

limits['sub_universe_sharpe']['limit'] = 0.01

metrics['sub_universe_sharpe'] += 0.01

if metrics['sub_universe_sharpe'] < 0:

metrics['sub_universe_sharpe'] = 0

elif "CONCENTRATED_WEIGHT" == name:

metrics['weight_concentration'] = check.get("value", 0.0)

if check.get('result', "FAIL") in ("FAIL", "WARNING") and metrics['weight_concentration'] == 0.0:

logger.warning("检测到 CONCENTRATED_WEIGHT 检查为 FAIL/WARNING 但 weight_concentration 为 0，强制设为 0.8 以便评分")

metrics['weight_concentration'] = 0.8

metrics['weight_concentration'] = 0.8

is_data = alpha_data.get("is", {}) if isinstance(alpha_data, dict) and "is" in alpha_data else alpha_data

returns_val = None

drawdown_val = None

if isinstance(is_data, dict):

returns_val = is_data.get('returns', None)

drawdown_val = is_data.get('drawdown', None)

margin_val = is_data.get('margin', None)

else:

margin_val = None

rd_ratio = None

if returns_val is not None and drawdown_val not in (None, 0):

rd_ratio = returns_val / drawdown_val

metrics['returns_drawdown_ratio'] = rd_ratio

metrics['margin'] = margin_val

# --- 4. 计算每一项指标的得分 (0-1.0之间) ---

scores = {}

passed_checks = {}

# Sharpe

val = metrics['sharpe']

limit = limits['sharpe']['limit']

if val is not None:

# 得分可以超过1.0，以奖励表现优异的指标，但在最终加权时会体现

scores['sharpe'] = val / limit

passed_checks['sharpe'] = (scores['sharpe'] >= 1)

# Fitness

val = metrics['fitness']

limit = limits['fitness']['limit']

if val is not None:

scores['fitness'] = val / limit

passed_checks['fitness'] = (scores['fitness'] >= 1)

# Turnover

val = metrics['turnover']

lower_limit = limits['turnover']['lower_limit']

upper_limit = limits['turnover']['upper_limit']

if val is not None:

if lower_limit <= val <= upper_limit:

scores['turnover'] = 1.0

passed_checks['turnover'] = True

elif val > upper_limit:

scores['turnover'] = max(0.0, 1 - (val - upper_limit) / upper_limit)

passed_checks['turnover'] = False

else:

scores['turnover'] = val / lower_limit

passed_checks['turnover'] = False

# Weight-concentration

val = metrics['weight_concentration']

limit = limits['weight_concentration']['limit']

if val is not None:

# 值越小越好。如果超过限制，得分迅速下降

if val <= limit:

scores['weight_concentration'] = 1.0

else:

scores['weight_concentration'] = max(0.0, limit / val)

passed_checks['weight_concentration'] = (val <= limit)

# Sub-universe-Sharpe

val = metrics['sub_universe_sharpe']

limit = limits['sub_universe_sharpe']['limit']

if val is not None:

scores['sub_universe_sharpe'] = val / limit

passed_checks['sub_universe_sharpe'] = (scores['sub_universe_sharpe'] >= 1)

val = metrics['returns_drawdown_ratio']

limit = limits['returns_drawdown_ratio']['limit']

if val is not None:

scores['returns_drawdown_ratio'] = val / limit

passed_checks['returns_drawdown_ratio'] = (scores['returns_drawdown_ratio'] >= 1)

val = metrics['margin']

limit = limits['margin']['limit']

if val is not None:

scores['margin'] = val / limit

passed_checks['margin'] = (scores['margin'] >= 1)

# --- 5. 计算综合潜力得分 ---

total_score = 0

total_weight = 0

valid_scores_details = {}

for key, score in scores.items():

if score is not None and key in weights:

capped_score = min(max(score, -1.0), 1.5)

total_score += capped_score * weights[key]

total_weight += weights[key]

valid_scores_details[key] = {

'value': metrics[key],

'score': round(capped_score, 3),

'weight': weights[key],

'passed': passed_checks.get(key, False)

}

potential_score = (total_score / total_weight) * 100 if total_weight > 0 else 0

# 对于绝对不能容忍的失败项，给予巨大惩罚

if metrics['weight_concentration'] >= 0.2:

potential_score *= (1 - metrics['weight_concentration'])

TURNOVER_LIMIT = 0.3  # 您的合格上限

TURNOVER_PENALTY_RATE = 5.0  # 这是一个可调参数：数字越大，惩罚越陡峭

turnover_val = metrics.get('turnover', 0.0)

if turnover_val > TURNOVER_LIMIT:

excess_turnover = turnover_val - TURNOVER_LIMIT

penalty_multiplier = np.exp(-excess_turnover * TURNOVER_PENALTY_RATE)

potential_score *= penalty_multiplier

penalty_weights = {

'weight_concentration': 10.0,

'turnover': 15.0,

'returns_drawdown_ratio': 10.0,

'fitness': 20.0,

'returns': 10.0

}

max_penalty_per_item=20.0

total_penalty = 0

if metrics['returns_drawdown_ratio'] is None:

total_penalty += max_penalty_per_item

elif metrics['returns_drawdown_ratio'] < 1.0:

deficit = 1.0 - metrics['returns_drawdown_ratio']

penalty = min(deficit * penalty_weights['returns_drawdown_ratio'], max_penalty_per_item)

total_penalty += penalty

if returns_val is None:

total_penalty += max_penalty_per_item

elif returns_val < 0.05:

deficit = 0.05 - returns_val

penalty = min((deficit / 0.05) * penalty_weights['returns'], max_penalty_per_item)

total_penalty += penalty

if metrics['fitness'] is None:

total_penalty += max_penalty_per_item

elif metrics['fitness'] < 0.8:

deficit = 0.8 - metrics['fitness']

penalty = min(deficit * penalty_weights['fitness'], max_penalty_per_item)

total_penalty += penalty

potential_score = max(0, potential_score - total_penalty)

is_qualified = all(passed_checks.values())

return {

'is_qualified': is_qualified,

'potential_score': round(potential_score, 2),

'details': valid_scores_details,

}

最后祝大家都能在平台获得满意的成绩，如果对这个代码有疑问或者建议可以随时在评论区提出，我会力所能及的解答的

---

## 讨论与评论 (7)

### 评论 #1 (作者: ML34246, 时间: 5个月前)

这个评分指标很好，有指标可以让ai做迭代甚至做rl了，之后有空了试试

---

### 评论 #2 (作者: ZY23886, 时间: 5个月前)

感谢大佬分享

我复现了一下

把代码存为

core.py

```
#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Alpha评分系统 - 核心评分模块基于多维度指标评估Alpha质量，输出0-140分的综合评分作者: Alpha Research Team版本: 1.0.0日期: 2026-01-16"""import jsonimport loggingfrom typing import Dict, List, Optional, Unionfrom datetime import datetimeimport numpy as np# 配置日志logging.basicConfig(    level=logging.INFO,    format='%(asctime)s - %(levelname)s - %(message)s')logger = logging.getLogger(__name__)class AlphaScorer:    """    Alpha评分器类    功能：    1. 评估单个Alpha的多维度指标    2. 计算综合潜力得分（0-140+分）    3. 判断Alpha是否合格    4. 输出详细的评分报告    """    def __init__(self, custom_weights: Dict = None, custom_limits: Dict = None):        """        初始化评分器        Args:            custom_weights: 自定义权重，格式: {'sharpe': 3.0, 'fitness': 2.5, ...}            custom_limits: 自定义阈值，格式: {'sharpe': {'limit': 1.2, 'type': 'ge'}, ...}        权重说明：        - sharpe: 夏普比率权重（默认2.5）        - fitness: 适应度权重（默认3.0，最重要）        - turnover: 换手率权重（默认2.0）        - weight_concentration: 权重集中度权重（默认0.5）        - sub_universe_sharpe: 子宇宙夏普权重（默认0.5）        - returns_drawdown_ratio: 收益回撤比权重（默认2.0）        - margin: 利差权重（默认1.0）        """        # 定义评估指标的合格标准        self.limits = custom_limits if custom_limits else {            'sharpe': {'limit': 1.0, 'type': 'ge'},                    # 夏普比率 >= 1.0            'fitness': {'limit': 1.0, 'type': 'ge'},                   # 适应度 >= 1.0            'turnover': {'lower_limit': 0.05, 'upper_limit': 0.3, 'type': 'range'},  # 换手率 0.05-0.3            'weight_concentration': {'limit': 0.1, 'type': 'le'},       # 权重集中度 <= 0.1            'sub_universe_sharpe': {'limit': 0.5, 'type': 'ge'},       # 子宇宙夏普 >= 0.5            'returns_drawdown_ratio': {'limit': 1.2, 'type': 'ge'},     # 收益回撤比 >= 1.2            'margin': {'limit': 0.0005, 'type': 'ge'}                   # 利差 >= 0.0005        }        # 定义各项指标的默认权重        default_weights = {            'sharpe': 2.5,            'fitness': 3.0,            'turnover': 2.0,            'weight_concentration': 0.5,            'sub_universe_sharpe': 0.5,            'returns_drawdown_ratio': 2.0,            'margin': 1.0        }        self.weights = custom_weights if custom_weights else default_weights        # 惩罚权重配置        self.penalty_weights = {            'weight_concentration': 10.0,            'turnover': 15.0,            'returns_drawdown_ratio': 10.0,            'fitness': 20.0,            'returns': 10.0        }        self.max_penalty_per_item = 20.0    def evaluate_alpha(self, alpha_data: dict, alpha_id: str = "") -> dict:        """        评估单个Alpha        Args:            alpha_data: Alpha数据，格式：                {                    "is": {                        "sharpe": 1.5,           # 夏普比率                        "fitness": 1.2,          # 适应度                        "turnover": 0.15,        # 换手率                        "weight_concentration": 0.05,  # 权重集中度                        "sub_universe_sharpe": 0.6,    # 子宇宙夏普                        "returns": 0.12,         # 收益率                        "drawdown": 0.05,        # 回撤                        "margin": 0.001,         # 利差                        "checks": [...]          # 检查列表                    }                }            alpha_id: Alpha ID（用于日志）        Returns:            评分结果字典：            {                'is_qualified': bool,        # 是否合格                'potential_score': float,     # 综合得分 (0-140+)                'details': dict,              # 各项指标详细得分                'raw_metrics': dict           # 原始指标值            }        """        try:            # 提取IS数据            is_data = alpha_data.get("is", {}) if isinstance(alpha_data, dict) and "is" in alpha_data else alpha_data            # 提取基础指标            metrics = {                'sharpe': is_data.get('sharpe', 0),                'fitness': is_data.get('fitness', 0),                'turnover': is_data.get('turnover', 1),                'weight_concentration': is_data.get('weight_concentration', 1),                'sub_universe_sharpe': is_data.get("sub_universe_sharpe", 0.0)            }            # 处理checks列表中的数据            for check in is_data.get('checks', []):                name = check.get("name", "")                if "LOW_SUB_UNIVERSE_SHARPE" == name:                    metrics['sub_universe_sharpe'] = check.get("value", 0.01)                    limit_val = check.get("limit", 0)                    if limit_val <= 0.0:                        limit_val = 0.01                        metrics['sub_universe_sharpe'] += 0.01                    self.limits['sub_universe_sharpe']['limit'] = limit_val                    if metrics['sub_universe_sharpe'] < 0:                        metrics['sub_universe_sharpe'] = 0                elif "CONCENTRATED_WEIGHT" == name:                    metrics['weight_concentration'] = check.get("value", 0.0)                    if check.get('result', "FAIL") in ("FAIL", "WARNING") and metrics['weight_concentration'] == 0.0:                        logger.warning(f"Alpha {alpha_id}: 检测到 CONCENTRATED_WEIGHT 检查为 FAIL/WARNING 但 weight_concentration 为 0，强制设为 0.8")                        metrics['weight_concentration'] = 0.8            # 提取returns和drawdown            returns_val = is_data.get('returns', None)            drawdown_val = is_data.get('drawdown', None)            margin_val = is_data.get('margin', None)            # 计算returns_drawdown_ratio            rd_ratio = None            if returns_val is not None and drawdown_val not in (None, 0):                rd_ratio = returns_val / abs(drawdown_val)            metrics['returns_drawdown_ratio'] = rd_ratio            metrics['margin'] = margin_val            # 计算每一项指标的得分            scores = {}            passed_checks = {}            # Sharpe            val = metrics['sharpe']            limit = self.limits['sharpe']['limit']            if val is not None:                scores['sharpe'] = val / limit                passed_checks['sharpe'] = (scores['sharpe'] >= 1)            # Fitness            val = metrics['fitness']            limit = self.limits['fitness']['limit']            if val is not None:                scores['fitness'] = val / limit                passed_checks['fitness'] = (scores['fitness'] >= 1)            # Turnover            val = metrics['turnover']            lower_limit = self.limits['turnover']['lower_limit']            upper_limit = self.limits['turnover']['upper_limit']            if val is not None:                if lower_limit <= val <= upper_limit:                    scores['turnover'] = 1.0                    passed_checks['turnover'] = True                elif val > upper_limit:                    scores['turnover'] = max(0.0, 1 - (val - upper_limit) / upper_limit)                    passed_checks['turnover'] = False                else:                    scores['turnover'] = val / lower_limit                    passed_checks['turnover'] = False            # Weight-concentration            val = metrics['weight_concentration']            limit = self.limits['weight_concentration']['limit']            if val is not None:                if val <= limit:                    scores['weight_concentration'] = 1.0                else:                    scores['weight_concentration'] = max(0.0, limit / val)                passed_checks['weight_concentration'] = (val <= limit)            # Sub-universe-Sharpe            val = metrics['sub_universe_sharpe']            limit = self.limits['sub_universe_sharpe']['limit']            if val is not None:                scores['sub_universe_sharpe'] = val / limit                passed_checks['sub_universe_sharpe'] = (scores['sub_universe_sharpe'] >= 1)            # Returns_drawdown_ratio            val = metrics['returns_drawdown_ratio']            limit = self.limits['returns_drawdown_ratio']['limit']            if val is not None:                scores['returns_drawdown_ratio'] = val / limit                passed_checks['returns_drawdown_ratio'] = (scores['returns_drawdown_ratio'] >= 1)            # Margin            val = metrics['margin']            limit = self.limits['margin']['limit']            if val is not None:                scores['margin'] = val / limit                passed_checks['margin'] = (scores['margin'] >= 1)            # 计算综合潜力得分            total_score = 0            total_weight = 0            valid_scores_details = {}            for key, score in scores.items():                if score is not None and key in self.weights:                    capped_score = min(max(score, -1.0), 1.5)                    total_score += capped_score * self.weights[key]                    total_weight += self.weights[key]                    valid_scores_details[key] = {                        'value': round(metrics[key], 4) if metrics[key] is not None else None,                        'score': round(capped_score, 3),                        'weight': self.weights[key],                        'passed': passed_checks.get(key, False)                    }            potential_score = (total_score / total_weight) * 100 if total_weight > 0 else 0            # 权重集中度过高惩罚            if metrics['weight_concentration'] >= 0.2:                potential_score *= (1 - metrics['weight_concentration'])            # Turnover过高惩罚            TURNOVER_LIMIT = 0.3            TURNOVER_PENALTY_RATE = 5.0            turnover_val = metrics.get('turnover', 0.0)            if turnover_val > TURNOVER_LIMIT:                excess_turnover = turnover_val - TURNOVER_LIMIT                penalty_multiplier = np.exp(-excess_turnover * TURNOVER_PENALTY_RATE)                potential_score *= penalty_multiplier            # 额外惩罚            total_penalty = 0            if metrics['returns_drawdown_ratio'] is None:                total_penalty += self.max_penalty_per_item            elif metrics['returns_drawdown_ratio'] < 1.0:                deficit = 1.0 - metrics['returns_drawdown_ratio']                penalty = min(deficit * self.penalty_weights['returns_drawdown_ratio'], self.max_penalty_per_item)                total_penalty += penalty            if returns_val is None:                total_penalty += self.max_penalty_per_item            elif returns_val < 0.05:                deficit = 0.05 - returns_val                penalty = min((deficit / 0.05) * self.penalty_weights['returns'], self.max_penalty_per_item)                total_penalty += penalty            if metrics['fitness'] is None:                total_penalty += self.max_penalty_per_item            elif metrics['fitness'] < 0.8:                deficit = 0.8 - metrics['fitness']                penalty = min(deficit * self.penalty_weights['fitness'], self.max_penalty_per_item)                total_penalty += penalty            potential_score = max(0, potential_score - total_penalty)            is_qualified = all(passed_checks.values())            return {                'is_qualified': is_qualified,                'potential_score': round(potential_score, 2),                'details': valid_scores_details,                'raw_metrics': metrics            }        except Exception as e:            logger.error(f"评估Alpha {alpha_id}时出错: {e}")            import traceback            traceback.print_exc()            return {                'is_qualified': False,                'potential_score': 0.0,                'details': {},                'error': str(e)            }class BatchScorer:    """    批量评分器类    功能：    1. 批量评分多个Alpha    2. 自动排序    3. 生成汇总报告    """    def __init__(self, scorer: AlphaScorer = None):        """        初始化批量评分器        Args:            scorer: AlphaScorer实例，如果为None则创建默认实例        """        self.scorer = scorer if scorer else AlphaScorer()        self.results = []    def score_batch(self, alphas: List[dict]) -> List[dict]:        """        批量评分Alpha列表        Args:            alphas: Alpha数据列表，每个元素格式：                {                    'id': str,              # Alpha ID                    'name': str,            # Alpha名称（可选）                    'is': dict              # IS指标数据                }        Returns:            评分结果列表，按得分降序排列        """        self.results = []        for alpha in alphas:            alpha_id = alpha.get('id', 'UNKNOWN')            alpha_name = alpha.get('name', '')            result = self.scorer.evaluate_alpha(alpha, alpha_id)            self.results.append({                'alpha_id': alpha_id,                'alpha_name': alpha_name,                'score_result': result            })        # 按得分排序        self.results.sort(key=lambda x: x['score_result']['potential_score'], reverse=True)        return self.results    def get_top_n(self, n: int) -> List[dict]:        """获取前N名"""        return self.results[:n]    def get_qualified_only(self) -> List[dict]:        """只获取合格的Alpha"""        return [r for r in self.results if r['score_result']['is_qualified']]    def get_score_statistics(self) -> dict:        """获取得分统计信息"""        if not self.results:            return {}        scores = [r['score_result']['potential_score'] for r in self.results]        qualified_count = sum(1 for r in self.results if r['score_result']['is_qualified'])        return {            'total_count': len(self.results),            'qualified_count': qualified_count,            'qualified_rate': qualified_count / len(self.results) if self.results else 0,            'max_score': max(scores) if scores else 0,            'min_score': min(scores) if scores else 0,            'avg_score': sum(scores) / len(scores) if scores else 0,            'median_score': sorted(scores)[len(scores)//2] if scores else 0        }def format_score_result(alpha_id: str, result: dict, alpha_name: str = "") -> str:    """    格式化单个Alpha的评分结果    Args:        alpha_id: Alpha ID        result: 评分结果字典        alpha_name: Alpha名称（可选）    Returns:        格式化的字符串    """    output = []    output.append("=" * 80)    output.append(f"Alpha ID: {alpha_id}")    if alpha_name:        output.append(f"Alpha名称: {alpha_name}")    output.append(f"综合得分: {result['potential_score']:.2f} 分")    output.append(f"是否合格: {'[是]' if result['is_qualified'] else '[否]'}")    output.append("-" * 80)    output.append("详细指标:")    output.append(f"{'指标':<25} {'数值':<12} {'得分':<10} {'权重':<8} {'是否通过'}")    output.append("-" * 80)    for key, detail in result.get('details', {}).items():        value_str = f"{detail['value']:.4f}" if detail['value'] is not None else "N/A"        passed_str = "[PASS]" if detail['passed'] else "[FAIL]"        output.append(f"{key:<25} {value_str:<12} {detail['score']:<10.3f} {detail['weight']:<8} {passed_str}")    output.append("=" * 80)    return "\n".join(output)def print_summary_table(results: List[dict], top_n: int = None):    """    打印汇总表格    Args:        results: 评分结果列表        top_n: 只显示前N名，None表示显示全部    """    if not results:        print("没有结果可显示")        return    # 按得分排序    sorted_results = sorted(results, key=lambda x: x.get('score_result', {}).get('potential_score', 0), reverse=True)    if top_n:        sorted_results = sorted_results[:top_n]    print("\n" + "=" * 100)    print(f"{'排名':<6} {'Alpha ID':<20} {'Alpha名称':<30} {'得分':<10} {'是否合格':<10}")    print("=" * 100)    for i, result in enumerate(sorted_results, 1):        alpha_id = result.get('alpha_id', 'N/A')        alpha_name = result.get('alpha_name', '')[:28]        score = result.get('score_result', {}).get('potential_score', 0)        qualified = result.get('score_result', {}).get('is_qualified', False)        qualified_str = '[是]' if qualified else '[否]'        print(f"{i:<6} {alpha_id:<20} {alpha_name:<30} {score:<10.2f} {qualified_str:<10}")    print("=" * 100)def save_results_to_file(results: List[dict], filename: str = "alpha_scores.json"):    """    保存结果到JSON文件    Args:        results: 评分结果列表        filename: 文件名    """    try:        # 转换为可序列化的格式        serializable_results = []        for result in results:            serializable_results.append({                'alpha_id': result.get('alpha_id'),                'alpha_name': result.get('alpha_name', ''),                'potential_score': result.get('score_result', {}).get('potential_score', 0),                'is_qualified': result.get('score_result', {}).get('is_qualified', False),                'details': result.get('score_result', {}).get('details', {}),                'raw_metrics': result.get('score_result', {}).get('raw_metrics', {})            })        with open(filename, 'w', encoding='utf-8') as f:            json.dump(serializable_results, f, ensure_ascii=False, indent=2)        logger.info(f"结果已保存到: {filename}")    except Exception as e:        logger.error(f"保存文件失败: {e}")def load_results_from_file(filename: str) -> List[dict]:    """    从JSON文件加载评分结果    Args:        filename: 文件名    Returns:        评分结果列表    """    try:        with open(filename, 'r', encoding='utf-8') as f:            data = json.load(f)        logger.info(f"从 {filename} 加载了 {len(data)} 条评分结果")        return data    except FileNotFoundError:        logger.error(f"文件不存在: {filename}")        return []    except Exception as e:        logger.error(f"加载文件失败: {e}")        return []
```

📖 实现原理

工作流程

```
  你在Claude Code输入 → 我调用MCP获取数据 → 评分模块计算 → 返回结果       ↓             ↓           ↓       ↓    "评分Alpha ID"    brain-mcp服务      core.py    显示评分
```

前提是要安装好MCP，ilfow也可以，claude打工人也可以，然后在对话框直接跟他说

帮我将这个alphaID 进行评分

![图片](images/img_5d1e002af9.jpeg)

感谢大佬分享

---

### 评论 #3 (作者: ZH87224, 时间: 5个月前)

之前用过论坛里另外一个评估函数，基于一批因子的is表现来的，用了之后combined提升不少，这次这个看起来是绝对指标，还加入了is_check惩罚，后面试下这个效果咋样👍

---

### 评论 #4 (作者: HG61318, 时间: 5个月前)

真不错啊,思路值得借鉴.
就是给每个指标评分的算法有数据支撑吗?还是说是凭经验?
####################################################################################
摸摸后缀
####################################################################################

---

### 评论 #5 (作者: MZ45384, 时间: 5个月前)

非常优质的alpha打分策略，采用了（666）

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #6 (作者: XC35224, 时间: 4个月前)

已视奸，明天测试，感谢

---

### 评论 #7 (作者: WL27319, 时间: 3个月前)

已经用上了，期待有个好的结果。

---

