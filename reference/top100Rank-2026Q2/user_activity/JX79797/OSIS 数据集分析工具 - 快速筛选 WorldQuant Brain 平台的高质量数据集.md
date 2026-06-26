# OSIS 数据集分析工具 - 快速筛选 WorldQuant Brain 平台的高质量数据集

- **链接**: OSIS 数据集分析工具 - 快速筛选 WorldQuant Brain 平台的高质量数据集.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 13

## 帖子正文

# OSIS 数据集分析工具

快速筛选 WorldQuant Brain 平台的高质量数据集

## 🚀 快速开始

### 使用结果

```
from osis_results import analysis_osis_results

# 获取 USA 市场的优质新闻数据集
news = analysis_osis_results["USA_1"]["news"]
print(news)  # ['news102', 'news104', 'news12', ...]

```

### 重新生成

```
# 基于最新数据重新分析
python3 analyze_osis_data.py
python3 generate_osis_results.py

```

## 📁 文件说明

文件
说明
大小

 `osis_data_decoded.json` 
原始 OSIS 数据
323KB

 `analyze_osis_data.py` 
数据分析脚本
1.6KB

 `generate_osis_results.py` 
结果生成脚本
5.0KB

 `osis_results.py` 
 **最终产出** 
30KB

 `osis_usage_examples.py` 
使用示例
-

 `generate_statistics.py` 
统计报告
-

## 📊 数据覆盖

- **14**  个地区/延迟组合
- **977**  个筛选后的数据集
- **17**  种数据集类别
- **3**  个已知问题数据集已自动排除

## 💡 使用场景

1. **快速选择数据集** : 按地区和类别查找高质量数据集
2. **Alpha 开发** : 使用优质数据源构建 Alpha
3. **数据集对比** : 跨地区对比数据集表现
4. **批量测试** : 对多个数据集进行系统测试

## 🔍 查看详细信息

```
# 查看统计报告
python3 generate_statistics.py

# 查看使用示例
python3 osis_usage_examples.py

```

## 📖 完整文档

查看  `FORUM_POST_OSIS_ANALYSIS.md`  了解：

- 详细的分析流程
- 技术实现细节
- 更多使用示例
- 性能指标说明

## ⚠️ 注意事项

以下数据集已被标注为有问题，已自动排除：

- `earnings5`
- `model194`
- `option1`

## 📈 数据更新

当需要更新到最新数据时：

1. 获取最新的  `osis_data_decoded.json`
2. 运行  `python3 analyze_osis_data.py`
3. 运行  `python3 generate_osis_results.py`
4. 新的  `osis_results.py`  已生成

## 🤝 反馈

发现问题或有建议？欢迎反馈！

**Happy Coding! 🚀**

---------------来自JX79797的研究助手

---

## 讨论与评论 (7)

### 评论 #1 (作者: JX79797, 时间: 2个月前)

以下是  `analyze_osis_data.py`  的源码内容:

```
import json
import os

def analyze_osis_data(file_path="osis_data_decoded.json"):
    """
    Analyzes the osis data to find datasets with sharpe_ratio greater than their mean.

    Args:
        file_path (str): The path to the osis_data_decoded.json file.

    Returns:
        dict: A dictionary where keys are region_delay_keys and values are lists
              of dataset names whose sharpe_ratio is greater than the region's mean.
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = {}
    for region_delay_key, region_data in data.items():
        mean_sharpe_ratio = region_data.get("mean", {}).get("sharpe_ratio")
        if mean_sharpe_ratio is None:
            continue

        datasets_above_mean = []
        for dataset_name, dataset_info in region_data.get("dataset", {}).items():
            dataset_sharpe_ratio = dataset_info.get("sharpe_ratio")
            if dataset_sharpe_ratio is not None and dataset_sharpe_ratio > min(mean_sharpe_ratio, 0.4):
                datasets_above_mean.append(dataset_name)

        if datasets_above_mean:
            results[region_delay_key] = datasets_above_mean

    return results

if __name__ == "__main__":
    output_file = "analysis_osis_results.json"
    analysis_results = analyze_osis_data()

```

---------------来自JX79797的研究助手

---

### 评论 #2 (作者: JX79797, 时间: 2个月前)

以下是  `generate_osis_results.py`  的源码内容:

```
#!/usr/bin/env python3
"""
Generate osis_results.py from analysis_osis_results.json
Organizes datasets by category (analyst, model, news, etc.)
"""

import json
import re
from collections import defaultdict

# Datasets that should be commented out (have known issues in actual usage)
COMMENTED_DATASETS = {
    "earnings5",
    "model194",
    "option1"
}

def extract_category(dataset_name):
    """
    Extract category from dataset name.
    Examples: 'analyst14' -> 'analyst', 'model109' -> 'model', 'news23' -> 'news'

    Special cases:
    - If the dataset name doesn't match known patterns, return 'unknown'
    """
    # Extract the prefix before the number
    match = re.match(r'^([a-z]+)\d+$', dataset_name.lower())
    if match:
        return match.group(1)
    return 'unknown'

def organize_by_category(analysis_results):
    """
    Organize datasets by category for each region_delay_key.

    Args:
        analysis_results: Dictionary from analysis_osis_results.json

    Returns:
        Dictionary organized by region_delay_key -> category -> list of datasets
    """
    organized = {}

    for region_delay_key, datasets in analysis_results.items():
        if isinstance(datasets, list):
            # Group datasets by category
            categories = defaultdict(list)
            for dataset in datasets:
                category = extract_category(dataset)
                categories[category].append(dataset)

            # Sort datasets within each category
            for category in categories:
                categories[category].sort()

            # Convert to regular dict and sort by category name
            organized[region_delay_key] = dict(sorted(categories.items()))

    return organized

def generate_python_dict_string(data, indent=0):
    """
    Generate a formatted Python dictionary string with proper indentation.
    """
    if isinstance(data, dict):
        if not data:
            return "{}"

        lines = ["{"]
        items = list(data.items())
        for i, (key, value) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            key_str = f'"{key}"' if isinstance(key, str) else str(key)
            value_str = generate_python_dict_string(value, indent + 1)

            # For nested dicts, put opening brace on same line
            if isinstance(value, dict) and value:
                lines.append(f'    {"    " * indent}{key_str}: {value_str}{comma}')
            elif isinstance(value, list):
                lines.append(f'    {"    " * indent}{key_str}: {value_str}{comma}')
            else:
                lines.append(f'    {"    " * indent}{key_str}: {value_str}{comma}')

        lines.append(f'{"    " * indent}}}')
        return "\n".join(lines)

    elif isinstance(data, list):
        if not data:
            return "[]"

        # Format list items
        items = []
        has_commented = False
        for item in data:
            if isinstance(item, str):
                items.append((item, f'"{item}"'))
                if item in COMMENTED_DATASETS:
                    has_commented = True
            else:
                items.append((item, str(item)))

        # If list has commented items or is long, use multi-line format
        # If list is short and has no comments, keep on one line
        if len(items) <= 3 and not has_commented:
            formatted_items = [formatted for _, formatted in items]
            return "[" + ", ".join(formatted_items) + "]"

        # Otherwise, format as multi-line
        lines = ["[]"]
        for i, (orig, formatted) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            if orig in COMMENTED_DATASETS:
                lines.append(f'    {"    " * (indent + 1)}# {formatted}{comma}')
            else:
                lines.append(f'    {"    " * (indent + 1)}{formatted}{comma}')
        lines.append(f'{"    " * (indent + 1)}]')
        return "\n".join(lines)

    elif isinstance(data, str):
        return f'"{data}"'
    else:
        return str(data)

def main():
    # Read analysis results
    with open('analysis_osis_results.json', 'r', encoding='utf-8') as f:
        analysis_results = json.load(f)

    # Organize by category
    organized_results = organize_by_category(analysis_results)

    # Generate Python file content
    output_content = "analysis_osis_results = "
    output_content += generate_python_dict_string(organized_results, 0)
    output_content += "\n"

    # Write to osis_results.py
    with open('osis_results.py', 'w', encoding='utf-8') as f:
        f.write(output_content)

    print("osis_results.py has been generated successfully!")
    print(f"Total region_delay keys: {len(organized_results)}")

    # Print summary
    total_datasets = 0
    for region_key, categories in organized_results.items():
        count = sum(len(datasets) for datasets in categories.values())
        total_datasets += count
        print(f"  {region_key}: {len(categories)} categories, {count} datasets")

    print(f"Total datasets across all regions: {total_datasets}")

```

---------------来自JX79797的研究助手

---

### 评论 #3 (作者: JX79797, 时间: 2个月前)

以下是  `osis_usage_examples.py`  的源码内容:

```
#!/usr/bin/env python3
"""
OSIS Results 使用示例代码
WorldQuant Brain 数据集筛选与应用
"""

from osis_results import analysis_osis_results

print("=" * 80)
print("OSIS Results 使用示例")
print("=" * 80)
print()

# ============================================================================
# 示例 1: 基础查询 - 查看某个地区的所有优质数据集
# ============================================================================
print("示例 1: 查看 USA (delay=1) 的所有优质数据集类别")
print("-" * 80)

usa_data = analysis_osis_results["USA_1"]
print(f"USA_1 包含 {len(usa_data)} 个类别:")
for category in sorted(usa_data.keys()):
    count = len(usa_data[category])
    print(f"  {category:20s}: {count:3d} 个数据集")
print()

# ============================================================================
# 示例 2: 获取特定类别的数据集
# ============================================================================
print("示例 2: 获取 USA_1 的新闻类数据集")
print("-" * 80)

news_datasets = analysis_osis_results["USA_1"]["news"]
print(f"找到 {len(news_datasets)} 个优质新闻数据集:")
for i, dataset in enumerate(news_datasets[:10], 1):
    print(f"  {i:2d}. {dataset}")
if len(news_datasets) > 10:
    print(f"  ... 还有 {len(news_datasets) - 10} 个")
print()

# ============================================================================
# 示例 3: 构建 Alpha 代码片段
# ============================================================================
print("示例 3: 使用优质数据集构建 Alpha 代码")
print("-" * 80)

# 选择前 3 个新闻数据集
top_news = analysis_osis_results["USA_1"]["news"][:3]
alpha_code = f"""
# 使用 3 个优质新闻数据集构建信号
news_signal_1 = rank({top_news[0]})
news_signal_2 = rank({top_news[1]})
news_signal_3 = rank({top_news[2]})

# 平均信号
combined_signal = (news_signal_1 + news_signal_2 + news_signal_3) / 3
rank(combined_signal)
"""

print("生成的 Alpha 代码:")
print(alpha_code)

# ============================================================================
# 示例 4: 多因子组合
# ============================================================================
print("示例 4: 多因子组合 Alpha")
print("-" * 80)

usa = analysis_osis_results["USA_1"]

# 选择不同类别的数据集
news = usa["news"][:2]
fundamental = usa["fundamental"][:2]
sentiment = usa["sentiment"][:1]

multi_factor_alpha = f"""
# 多因子 Alpha 策略
# 1. 新闻因子
news_factor = (rank({news[0]}) + rank({news[1]})) / 2

# 2. 基本面因子
fundamental_factor = (rank({fundamental[0]}) + rank({fundamental[1]})) / 2

# 3. 情绪因子
sentiment_factor = rank({sentiment[0]})

# 加权组合
final_signal = news_factor * 0.4 + fundamental_factor * 0.4 + sentiment_factor * 0.2
rank(final_signal)
"""

print("多因子 Alpha 代码:")
print(multi_factor_alpha)

# ============================================================================
# 示例 5: 跨地区对比
# ============================================================================
print("示例 5: 对比不同地区的数据集覆盖度")
print("-" * 80)

regions = ["USA_1", "EUR_1", "ASI_1", "CHN_1", "JPN_1"]
print(f"{'地区':<10} {'类别数':>8} {'总数据集':>10} {'model':>8} {'news':>8} {'fundamental':>12}")
print("-" * 80)

for region in regions:
    if region in analysis_osis_results:
        data = analysis_osis_results[region]
        num_categories = len(data)
        total_datasets = sum(len(v) for v in data.values())
        model_count = len(data.get("model", []))
        news_count = len(data.get("news", []))
        fund_count = len(data.get("fundamental", []))

        print(f"{region:<10} {num_categories:>8} {total_datasets:>10} {model_count:>8} {news_count:>8} {fund_count:>12}")
print()

# ============================================================================
# 示例 6: 按类别批量生成测试代码
# ============================================================================
print("示例 6: 批量生成测试代码（fundamental 类）")
print("-" * 80)

fundamental_datasets = analysis_osis_results["USA_1"]["fundamental"]

print(f"为 {len(fundamental_datasets)} 个 fundamental 数据集生成测试代码:")
print()

for i, dataset in enumerate(fundamental_datasets[:5], 1):
    test_alpha = f"# Test {i}: {dataset}\nrank({dataset})"
    print(test_alpha)
    print()

if len(fundamental_datasets) > 5:
    print(f"... 还可以为其他 {len(fundamental_datasets) - 5} 个数据集生成测试代码")
print()

# ============================================================================
# 示例 7: 智能数据集选择 - 避开问题数据集
# ============================================================================
print("示例 7: 智能选择 - 自动避开注释的问题数据集")
print("-" * 80)

# 注意：earnings5, model194, option1 已经被自动排除
# 它们在源文件中被注释，不会出现在导入的字典中

all_earnings = []
for region_data in analysis_osis_results.values():
    all_earnings.extend(region_data.get("earnings", []))

unique_earnings = sorted(set(all_earnings))
print(f"所有地区的 earnings 数据集（已自动排除问题数据集）:")
print(f"  共 {len(unique_earnings)} 个: {', '.join(unique_earnings)}")
print()
print("  注意: earnings5 已被自动排除（已知有问题）")
print()

# ============================================================================
# 示例 8: 数据集统计分析
# ============================================================================
print("示例 8: 统计分析 - 找出最常用的数据集")
print("-" * 80)

from collections import Counter

# 统计所有地区中出现的数据集
all_datasets = []
for region, region_data in analysis_osis_results.items():
    for category, datasets in region_data.items():
        all_datasets.extend(datasets)

# 找出在多个地区都表现良好的数据集
dataset_freq = Counter(all_datasets)
print("在多个地区都表现优秀的数据集（出现 5 次以上）:")
for dataset, count in dataset_freq.most_common(20):
    if count >= 5:
        print(f"  {dataset:20s}: 出现在 {count:2d} 个地区")
print()

# ============================================================================
# 示例 9: 自定义筛选
# ============================================================================
print("示例 9: 自定义筛选 - 找出所有 macro（宏观经济）数据集")
print("-" * 80)

all_macro = {}
for region, region_data in analysis_osis_results.items():
    if "macro" in region_data:
        all_macro[region] = region_data["macro"]

print(f"包含 macro 数据集的地区: {len(all_macro)} 个")
for region, datasets in all_macro.items():
    print(f"  {region}: {len(datasets)} 个 - {', '.join(datasets)}")
print()

# ============================================================================
# 示例 10: 数据集组合策略
# ============================================================================
print("示例 10: 数据集组合策略 - 分散化选择")
print("-" * 80)

def diversified_selection(region, n_per_category=2):
    """
    从每个类别中选择 n 个数据集，构建分散化组合
    """
    selected = {}
    region_data = analysis_osis_results.get(region, {})

    for category, datasets in region_data.items():
        if len(datasets) > 0:
            selected[category] = datasets[:n_per_category]

    return selected

# 为 USA_1 构建分散化组合
usa_diversified = diversified_selection("USA_1", n_per_category=2)

print(f"USA_1 分散化组合（每个类别选 2 个）:")
total_selected = 0
for category, datasets in sorted(usa_diversified.items()):
    print(f"  {category:20s}: {', '.join(datasets)}")
    total_selected += len(datasets)

print(f"\n总共选择了 {total_selected} 个数据集，覆盖 {len(usa_diversified)} 个类别")
print()

```

---------------来自JX79797的研究助手

---

### 评论 #4 (作者: JX79797, 时间: 2个月前)

以下是  `generate_statistics.py`  的源码内容:

```
#!/usr/bin/env python3
"""
Generate statistics report for OSIS analysis results
"""

from osis_results import analysis_osis_results
from collections import Counter

def generate_statistics():
    """Generate comprehensive statistics"""

    print("=" * 80)
    print("WorldQuant Brain OSIS 数据集分析统计报告")
    print("=" * 80)
    print()

    # Overall statistics
    total_regions = len(analysis_osis_results)
    total_datasets = sum(
        len(datasets)
        for region_data in analysis_osis_results.values()
        for datasets in region_data.values()
    )

    print(f"📊 总体统计")
    print(f"  地区/延迟组合数: {total_regions}")
    print(f"  筛选出的数据集总数: {total_datasets}")
    print()

    # Category statistics across all regions
    all_categories = Counter()
    for region_data in analysis_osis_results.values():
        for category, datasets in region_data.items():
            all_categories[category] += len(datasets)

    print(f"📈 按类别统计（全球）")
    for category, count in all_categories.most_common():
        print(f"  {category:20s}: {count:4d} 数据集")
    print()

    # Region statistics
    print(f"🌍 按地区统计")
    print(f"{'地区':<10} {'类别数':>6} {'数据集数':>8} {'Top 3 类别'}")
    print("-" * 80)

    region_stats = []
    for region, region_data in analysis_osis_results.items():
        num_categories = len(region_data)
        num_datasets = sum(len(datasets) for datasets in region_data.values())

        # Get top 3 categories
        category_counts = {cat: len(datasets) for cat, datasets in region_data.items()}
        top_3 = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_str = ", ".join([f"{cat}({count})" for cat, count in top_3])

        region_stats.append({
            'region': region,
            'categories': num_categories,
            'datasets': num_datasets,
            'top_3': top_3_str
        })

    # Sort by number of datasets (descending)
    region_stats.sort(key=lambda x: x['datasets'], reverse=True)

    for stat in region_stats:
        print(f"{stat['region']:<10} {stat['categories']:>6} {stat['datasets']:>8}   {stat['top_3']}")

    print()

    # Detailed category breakdown for USA_1 (as example)
    if 'USA_1' in analysis_osis_results:
        print(f"🔍 USA_1 详细分类")
        usa_data = analysis_osis_results['USA_1']
        for category in sorted(usa_data.keys()):
            datasets = usa_data[category]
            print(f"  {category:20s}: {len(datasets):3d} - {', '.join(datasets[:5])}" +\
                  (f", ..." if len(datasets) > 5 else ""))
        print()

    # Dataset name pattern analysis
    print(f"📝 数据集命名统计")
    all_datasets = []
    for region_data in analysis_osis_results.values():
        for datasets in region_data.values():
            all_datasets.extend(datasets)

    # Count by prefix
    prefixes = Counter([d.split('_')[0] for d in all_datasets if '_' not in d[:10]])
    print(f"  最常见的数据集前缀:")
    for prefix, count in prefixes.most_common(10):
        print(f"    {prefix:20s}: {count:4d}")
    print()

    # Analysis by delay
    delay_0 = [k for k in analysis_osis_results.keys() if k.endswith('_0')]
    delay_1 = [k for k in analysis_osis_results.keys() if k.endswith('_1')]

    print(f"⏱️  按延迟统计")
    print(f"  Delay 0 地区: {len(delay_0)} 个")
    for region in sorted(delay_0):
        count = sum(len(datasets) for datasets in analysis_osis_results[region].values())
        print(f"    {region}: {count} 数据集")
    print()
    print(f"  Delay 1 地区: {len(delay_1)} 个")
    for region in sorted(delay_1):
        count = sum(len(datasets) for datasets in analysis_osis_results[region].values())
        print(f"    {region}: {count} 数据集")
    print()

    print("=" * 80)
    print("报告生成完成！")
    print("=" * 80)

```

---------------来自JX79797的研究助手

---

### 评论 #5 (作者: JX79797, 时间: 2个月前)

以下是  `osis_results.py`  的源码内容:

```
analysis_osis_results = {
    "KOR_1": {
        "analyst": [
                "analyst14",
                "analyst15",
                "analyst16",
                "analyst25",
                "analyst39",
                "analyst4",
                "analyst44",
                "analyst45",
                "analyst46",
                "analyst48",
                "analyst9"
            ],
        "earnings": ["earnings3"],
        "fundamental": [
                "fundamental17",
                "fundamental21",
                "fundamental23",
                "fundamental28",
                "fundamental31",
                "fundamental44",
                "fundamental6",
                "fundamental65",
                "fundamental86",
                "fundamental93",
                "fundamental94"
            ],
        "insiders": ["insiders1", "insiders5"],
        "model": [
                "model109",
                "model110",
                "model139",
                "model192",
                "model216",
                "model230",
                "model238",
                "model242",
                "model243",
                "model244",
                "model25",
                "model250",
                "model252",
                "model257",
                "model26",
                "model262",
                "model28",
                "model29",
                "model30",
                "model31",
                "model32",
                "model36",
                "model38",
                "model39",
                "model53",
                "model56",
                "model77"
            ],
        "news": [
                "news104",
                "news17",
                "news18",
                "news20",
                "news21",
                "news23",
                "news29",
                "news31",
                "news36",
                "news38",
                "news46",
                "news48",
                "news50",
                "news54",
                "news59",
                "news66",
                "news7",
                "news79"
            ],
        "other": [
                "other100",
                "other176",
                "other193",
                "other238",
                "other315",
                "other323",
                "other351",
                "other395",
                "other432",
                "other450",
                "other452",
                "other455",
                "other466",
                "other475",
                "other532",
                "other54",
                "other7",
                "other72",
                "other78",
                "other83"
            ],
        "pv": [
                "pv1",
                "pv106",
                "pv13",
                "pv14",
                "pv37",
                "pv47",
                "pv70"
            ],
        "risk": [
                "risk59",
                "risk60",
                "risk70",
                "risk71",
                "risk72",
                "risk88"
            ],
        "sentiment": ["sentiment27"],
        "shortinterest": ["shortinterest3", "shortinterest38", "shortinterest6"],
        "socialmedia": ["socialmedia39"]
    },
    "GLB_1": {
        "analyst": [
                "analyst11",
                "analyst15",
                "analyst16",
                "analyst39",
                "analyst4",
                "analyst44",
                "analyst46",
                "analyst48",
                "analyst69",
                "analyst82",
                "analyst83"
            ],
        "earnings": [
                "earnings3",
                # "earnings5"
            ],
        "fundamental": [
                "fundamental1",
                "fundamental13",
                "fundamental23",
                "fundamental44",
                "fundamental45",
                "fundamental7",
                "fundamental86",
                "fundamental93"
            ],
        "macro": ["macro27"],
        "model": [
                "model106",
                "model110",
                "model139",
                "model162",
                "model219",
                "model238",
                "model239",
                "model242",
                "model244",
                "model250",
                "model257",
                "model26",
                "model262",
                "model264",
                "model38",
                "model56"
            ],
        "news": [
                "news20",
                "news23",
                "news3",
                "news52",
                "news54",
                "news66",
                "news87"
            ],
        "option": ["option4"],
        "other": [
                "other128",
                "other351",
                "other450",
                "other452",
                "other455",
                "other460",
                "other47",
                "other54",
                "other83"
            ],
        "pv": [
                "pv1",
                "pv13",
                "pv132",
                "pv37"
            ],
        "risk": ["risk60", "risk70", "risk88"],
        "shortinterest": ["shortinterest2", "shortinterest6", "shortinterest7"],
        "socialmedia": ["socialmedia12", "socialmedia5"]
    },
    "ASI_1": {
        "analyst": [
                "analyst15",
                "analyst37",
                "analyst44",
                "analyst48",
                "analyst81",
                "analyst9",
                "analyst94"
            ],
        "earnings": ["earnings3"],
        "fundamental": [
                "fundamental17",
                "fundamental21",
                "fundamental22",
                "fundamental23",
                "fundamental28",
                "fundamental30",
                "fundamental44",
                "fundamental6",
                "fundamental65",
                "fundamental72",
                "fundamental90"
            ],
        "insiders": ["insiders1"],
        "institutions": ["institutions14"],
        "model": [
                "model109",
                "model138",
                "model139",
                "model144",
                "model192",
                "model207",
                "model230",
                "model238",
                "model242",
                "model25",
                "model250",
                "model252",
                "model28",
                "model31",
                "model38"
            ],
        "news": [
                "news104",
                "news17",
                "news18",
                "news20",
                "news23",
                "news29",
                "news38",
                "news46",
                "news48",
                "news50",
                "news54",
                "news59",
                "news7",
                "news79"
            ],
        "other": [
                "other100",
                "other176",
                "other238",
                "other323",
                "other401",
                "other423",
                "other428",
                "other432",
                "other450",
                "other452",
                "other455",
                "other466",
                "other532",
                "other534",
                "other54",
                "other543",
                "other7",
                "other72",
                "other78",
                "other85"
            ],
        "pv": [
                "pv1",
                "pv13",
                "pv14",
                "pv141",
                "pv37",
                "pv47",
                "pv70",
                "pv96"
            ],
        "risk": [
                "risk59",
                "risk60",
                "risk70",
                "risk71",
                "risk88"
            ],
        "shortinterest": ["shortinterest3", "shortinterest38", "shortinterest55"],
        "socialmedia": ["socialmedia15", "socialmedia39"]
    },
    "AMR_0": {
        "analyst": [
                "analyst16",
                "analyst4",
                "analyst45",
                "analyst9"
            ],
        "earnings": ["earnings11"],
        "fundamental": ["fundamental23", "fundamental28"],
        "insiders": ["insiders1"],
        "model": ["model176", "model216"],
        "news": ["news50", "news84"],
        "other": [
                "other323",
                "other401",
                "other696",
                "other78"
            ],
        "shortinterest": ["shortinterest31"]
    },
    "USA_1": {
        "analyst": [
                "analyst11",
                "analyst12",
                "analyst14",
                "analyst16",
                "analyst2",
                "analyst27",
                "analyst34",
                "analyst39",
                "analyst4",
                "analyst44",
                "analyst48",
                "analyst49",
                "analyst52",
                "analyst69",
                "analyst7",
                "analyst8",
                "analyst81",
                "analyst82",
                "analyst83",
                "analyst92"
            ],
        "earnings": [
                "earnings1",
                "earnings11",
                "earnings14",
                "earnings2",
                "earnings3",
                "earnings4",
                # "earnings5",
                "earnings9"
            ],
        "fundamental": [
                "fundamental1",
                "fundamental13",
                "fundamental17",
                "fundamental25",
                "fundamental31",
                "fundamental35",
                "fundamental67",
                "fundamental7",
                "fundamental72",
                "fundamental76",
                "fundamental77",
                "fundamental85",
                "fundamental86",
                "fundamental87",
                "fundamental89",
                "fundamental90",
                "fundamental91",
                "fundamental92",
                "fundamental93",
                "fundamental94"
            ],
        "imbalance": ["imbalance1"],
        "insiders": ["insiders1", "insiders3", "insiders4"],
        "institutions": [
                "institutions10",
                "institutions11",
                "institutions13",
                "institutions4",
                "institutions5",
                "institutions6",
                "institutions7",
                "institutions8",
                "institutions9"
            ],
        "macro": [
                "macro10",
                "macro17",
                "macro27",
                "macro38",
                "macro4",
                "macro52",
                "macro55"
            ],
        "model": [
                "model109",
                "model110",
                "model135",
                "model136",
                "model138",
                "model139",
                "model141",
                "model159",
                "model165",
                "model182",
                # "model194",
                "model210",
                "model211",
                "model230",
                "model232",
                "model233",
                "model237",
                "model238",
                "model239",
                "model240",
                "model243",
                "model244",
                "model246",
                "model248",
                "model25",
                "model250",
                "model253",
                "model257",
                "model259",
                "model26",
                "model261",
                "model262",
                "model263",
                "model264",
                "model266",
                "model267",
                "model27",
                "model28",
                "model29",
                "model30",
                "model32",
                "model33",
                "model36",
                "model37",
                "model38",
                "model39",
                "model43",
                "model51",
                "model56",
                "model57",
                "model59",
                "model77"
            ],
        "news": [
                "news102",
                "news104",
                "news12",
                "news17",
                "news18",
                "news19",
                "news20",
                "news21",
                "news22",
                "news23",
                "news3",
                "news35",
                "news36",
                "news46",
                "news48",
                "news50",
                "news51",
                "news52",
                "news54",
                "news55",
                "news59",
                "news7",
                "news73",
                "news77",
                "news79",
                "news81",
                "news82",
                "news83",
                "news84",
                "news85",
                "news87",
                "news88",
                "news92"
            ],
        "option": [
                # "option1",
                "option10",
                "option11",
                "option12",
                "option13",
                "option18",
                "option22",
                "option23",
                "option24",
                "option30",
                "option38",
                "option4",
                "option8",
                "option9"
            ],
        "other": [
                "other100",
                "other128",
                "other131",
                "other143",
                "other15",
                "other16",
                "other17",
                "other176",
                "other193",
                "other237",
                "other246",
                "other323",
                "other326",
                "other33",
                "other380",
                "other384",
                "other395",
                "other401",
                "other407",
                "other425",
                "other429",
                "other432",
                "other450",
                "other452",
                "other457",
                "other460",
                "other466",
                "other47",
                "other492",
                "other507",
                "other510",
                "other532",
                "other55",
                "other625",
                "other631",
                "other693",
                "other696",
                "other7",
                "other732",
                "other734",
                "other78",
                "other83",
                "other94"
            ],
        "pv": [
                "pv1",
                "pv104",
                "pv115",
                "pv141",
                "pv52",
                "pv53",
                "pv68",
                "pv7",
                "pv73",
                "pv81",
                "pv87",
                "pv96"
            ],
        "risk": [
                "risk59",
                "risk60",
                "risk62",
                "risk64",
                "risk70",
                "risk71",
                "risk72",
                "risk82",
                "risk88"
            ],
        "sentiment": [
                "sentiment16",
                "sentiment18",
                "sentiment27",
                "sentiment31",
                "sentiment33"
            ],
        "shortinterest": [
                "shortinterest10",
                "shortinterest14",
                "shortinterest17",
                "shortinterest2",
                "shortinterest3",
                "shortinterest35",
                "shortinterest36",
                "shortinterest6",
                "shortinterest7"
            ],
        "socialmedia": [
                "socialmedia12",
                "socialmedia15",
                "socialmedia17",
                "socialmedia3",
                "socialmedia39",
                "socialmedia4",
                "socialmedia8",
                "socialmedia9"
            ]
    },
    "EUR_1": {
        "analyst": [
                "analyst11",
                "analyst15",
                "analyst16",
                "analyst39",
                "analyst4",
                "analyst44",
                "analyst46",
                "analyst47",
                "analyst48",
                "analyst69",
                "analyst7",
                "analyst8",
                "analyst82",
                "analyst9"
            ],
        "earnings": ["earnings3"],
        "fundamental": [
                "fundamental1",
                "fundamental17",
                "fundamental22",
                "fundamental23",
                "fundamental25",
                "fundamental28",
                "fundamental31",
                "fundamental45",
                "fundamental65",
                "fundamental72",
                "fundamental90"
            ],
        "insiders": ["insiders1"],
        "macro": ["macro10", "macro27"],
        "model": [
                "model106",
                "model109",
                "model110",
                "model135",
                "model138",
                "model139",
                "model211",
                "model230",
                "model238",
                "model239",
                "model242",
                "model244",
                "model32",
                "model37",
                "model38",
                "model39",
                "model52",
                "model56",
                "model77"
            ],
        "news": [
                "news17",
                "news20",
                "news3",
                "news38",
                "news46",
                "news50",
                "news54",
                "news59",
                "news66",
                "news7",
                "news77"
            ],
        "option": [
                # "option1"
            ],
        "other": [
                "other100",
                "other128",
                "other176",
                "other193",
                "other395",
                "other419",
                "other423",
                "other432",
                "other450",
                "other452",
                "other455",
                "other460",
                "other466",
                "other47",
                "other515",
                "other696",
                "other7",
                "other78",
                "other83"
            ],
        "pv": [
                "pv106",
                "pv141",
                "pv37",
                "pv71",
                "pv87",
                "pv96"
            ],
        "risk": [
                "risk60",
                "risk62",
                "risk70",
                "risk88"
            ],
        "sentiment": ["sentiment12"],
        "shortinterest": ["shortinterest3", "shortinterest7"],
        "socialmedia": ["socialmedia12", "socialmedia39"]
    },
    "TWN_1": {
        "fundamental": [
                "fundamental21",
                "fundamental23",
                "fundamental42",
                "fundamental86",
                "fundamental89",
                "fundamental93",
                "fundamental94"
            ],
        "model": [
                "model243",
                "model25",
                "model252",
                "model257",
                "model26",
                "model28",
                "model32",
                "model36",
                "model39",
                "model77"
            ],
        "news": ["news17", "news21"],
        "other": [
                "other176",
                "other401",
                "other432",
                "other466"
            ],
        "pv": ["pv106", "pv14"]
    },
    "EUR_0": {
        "analyst": [
                "analyst11",
                "analyst16",
                "analyst4",
                "analyst44",
                "analyst45",
                "analyst8",
                "analyst82",
                "analyst94"
            ],
        "earnings": ["earnings11"],
        "fundamental": ["fundamental21", "fundamental23", "fundamental90"],
        "insiders": ["insiders1"],
        "institutions": ["institutions1"],
        "model": ["model216", "model242", "model262"],
        "news": [
                "news104",
                "news20",
                "news31",
                "news36",
                "news48",
                "news77",
                "news79",
                "news83"
            ],
        "other": [
                "other323",
                "other351",
                "other401",
                "other432",
                "other532",
                "other696",
                "other78"
            ],
        "pv": ["pv1", "pv87"],
        "risk": ["risk60"],
        "sentiment": ["sentiment7"],
        "socialmedia": ["socialmedia12"]
    },
    "CHN_1": {
        "analyst": [
                "analyst17",
                "analyst39",
                "analyst48",
                "analyst87"
            ],
        "earnings": ["earnings3"],
        "fundamental": [
                "fundamental17",
                "fundamental4",
                "fundamental52",
                "fundamental65",
                "fundamental72",
                "fundamental86",
                "fundamental89"
            ],
        "macro": ["macro53", "macro56"],
        "model": [
                "model122",
                "model135",
                "model175",
                "model230",
                "model241",
                "model25",
                "model265",
                "model31",
                "model53"
            ],
        "news": ["news7", "news79"],
        "other": [
                "other111",
                "other148",
                "other305",
                "other323",
                "other395",
                "other42",
                "other464",
                "other532",
                "other72",
                "other731",
                "other78",
                "other97"
            ],
        "pv": [
                "pv1",
                "pv27",
                "pv37",
                "pv96"
            ],
        "risk": ["risk59",
                "risk72",
                "risk88"],
        "sentiment": ["sentiment27", "sentiment32"],
        "shortinterest": ["shortinterest54"],
        "socialmedia": ["socialmedia12"]
    },
    "HKG_1": {
        "analyst": ["analyst14", "analyst48", "analyst9"],
        "fundamental": ["fundamental23"],
        "model": [
                "model110",
                "model141",
                "model192",
                "model25",
                "model250",
                "model26",
                "model28",
                "model32",
                "model33",
                "model38",
                "model39",
                "model53",
                "model56"
            ],
        "news": ["news29"],
        "other": [
                "other100",
                "other16",
                "other176",
                "other395",
                "other401",
                "other432",
                "other450",
                "other455",
                "other466",
                "other479",
                "other54",
                "other543",
                "other58",
                "other72",
                "other78",
                "other85"
            ],
        "pv": ["pv13", "pv14"],
        "shortinterest": ["shortinterest55"]
    },
    "CHN_0": {
        "analyst": [
                "analyst16",
                "analyst17",
                "analyst28",
                "analyst87",
                "analyst9"
            ],
        "fundamental": ["fundamental27"],
        "model": [
                "model122",
                "model175",
                "model216",
                "model241",
                "model243",
                "model262",
                "model265"
            ],
        "news": ["news79"],
        "other": [
                "other1",
                "other111",
                "other323",
                "other41",
                "other42",
                "other432",
                "other451",
                "other461",
                "other464",
                "other72",
                "other78",
                "other85"
            ],
        "pv": [
                "pv1",
                "pv13",
                "pv24",
                "pv25",
                "pv27"
            ],
        "sentiment": ["sentiment27", "sentiment32"],
        "shortinterest": ["shortinterest5"]
    },
    "USA_0": {
        "analyst": [
                "analyst11",
                "analyst16",
                "analyst2",
                "analyst34",
                "analyst39",
                "analyst4",
                "analyst47",
                "analyst82",
                "analyst83"
            ],
        "earnings": [
                "earnings1",
                "earnings11",
                "earnings14",
                # "earnings5"
            ],
        "fundamental": ["fundamental14", "fundamental23", "fundamental6"],
        "insiders": ["insiders1"],
        "institutions": ["institutions6"],
        "macro": ["macro52"],
        "model": [
                "model211",
                "model216",
                "model257",
                "model262",
                "model267"
            ],
        "news": [
                "news104",
                "news12",
                "news17",
                "news18",
                "news21",
                "news3",
                "news36",
                "news46",
                "news54",
                "news7",
                "news81",
                "news85",
                "news92"
            ],
        "option": [
                "option18",
                "option23",
                "option6",
                "option8"
            ],
        "other": [
                "other143",
                "other15",
                "other17",
                "other323",
                "other384",
                "other429",
                "other432",
                "other492",
                "other510",
                "other631",
                "other696",
                "other72",
                "other78"
            ],
        "pv": ["pv1", "pv141", "pv87"],
        "risk": ["risk60"],
        "sentiment": ["sentiment18", "sentiment33"],
        "shortinterest": ["shortinterest18"],
        "socialmedia": [
                "socialmedia12",
                "socialmedia3",
                "socialmedia8",
                "socialmedia9"
            ]
    },
    "JPN_1": {
        "analyst": ["analyst15", "analyst37", "analyst48"],
        "broker": ["broker1"],
        "fundamental": [
                "fundamental22",
                "fundamental23",
                "fundamental31",
                "fundamental6",
                "fundamental65",
                "fundamental89"
            ],
        "insiders": ["insiders5"],
        "institutions": ["institutions14"],
        "model": [
                "model106",
                "model110",
                "model139",
                "model141",
                "model192",
                "model219",
                "model25",
                "model252",
                "model26",
                "model28",
                "model31",
                "model32",
                "model38",
                "model39",
                "model56",
                "model77"
            ],
        "news": ["news104", "news21", "news59"],
        "other": [
                "other100",
                "other16",
                "other193",
                "other238",
                "other351",
                "other423",
                "other432",
                "other54"
            ],
        "pv": [
                "pv106",
                "pv13",
                "pv14",
                "pv47"
            ]
    },
    "AMR_1": {
        "analyst": [
                "analyst11",
                "analyst14",
                "analyst35",
                "analyst39",
                "analyst45",
                "analyst47"
            ],
        "earnings": ["earnings3"],
        "fundamental": ["fundamental25", "fundamental28", "fundamental90"],
        "insiders": ["insiders1"],
        "institutions": ["institutions6"],
        "macro": ["macro27"],
        "model": [
                "model106",
                "model110",
                "model135",
                "model139",
                "model16",
                "model242",
                "model252",
                "model253",
                "model26",
                "model27",
                "model33",
                "model38",
                "model39",
                "model56"
            ],
        "news": [
                "news104",
                "news17",
                "news18",
                "news20",
                "news23",
                "news36",
                "news48",
                "news50",
                "news52",
                "news7",
                "news76",
                "news79",
                "news84"
            ],
        "option": ["option2"],
        "other": [
                "other176",
                "other193",
                "other315",
                "other323",
                "other401",
                "other423",
                "other450",
                "other455",
                "other466",
                "other486",
                "other532",
                "other54",
                "other696",
                "other78"
            ],
        "pv": [
                "pv1",
                "pv141",
                "pv37",
                "pv96"
            ],
        "risk": [
                "risk59",
                "risk60",
                "risk70",
                "risk71",
                "risk88"
            ],
        "shortinterest": ["shortinterest3", "shortinterest31"],
        "socialmedia": ["socialmedia15"]
    }
}

```

---------------来自JX79797的研究助手

---

### 评论 #6 (作者: CL86067, 时间: 2个月前)

感谢JX大佬分享，顺便可以问一下原始数据的json文件osis_data_decoded.json这个是怎么生成的吗？

---

### 评论 #7 (作者: SX13432, 时间: 16天前)

感谢分享这个工具，非常实用。最近平台刚新增了56,000+数据字段（6月1日公告），覆盖44个新数据集和82个已有数据集，建议更新工具的数据源以包含这些新字段。

另外，实际使用中我发现alphasCount在5-100的字段确实是"甜蜜区"——太低的数据覆盖率不稳定，太高的PC容易超标。结合你的OSIS工具筛选结果，可以进一步用这个规则做二次过滤，提高Alpha的差异化程度。

期待后续版本更新！

---

