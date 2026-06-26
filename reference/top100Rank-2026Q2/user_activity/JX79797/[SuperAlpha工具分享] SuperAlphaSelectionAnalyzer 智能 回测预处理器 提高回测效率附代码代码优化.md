# [SuperAlpha工具分享] SuperAlphaSelectionAnalyzer: 智能 "回测预处理器", 提高回测效率(附代码)代码优化

- **链接**: [SuperAlpha工具分享] SuperAlphaSelectionAnalyzer 智能 回测预处理器 提高回测效率附代码代码优化.md
- **作者**: JX79797
- **发布时间/热度**: 7个月前, 得票: 106

## 帖子正文

在构建回测 Super Alpha 的过程中，我们经常会编写复杂的 `selection` 表达式来筛选符合特定条件的 alpha。但你是否遇到过以下问题：

- 不确定一个 `selection` 表达式到底能匹配到多少个 alpha？
- 想知道被选中的这批 alpha 的整体质量如何？（例如，它们的平均 Sharpe 是多少？换手率分布如何？）
- 想了解这批 alpha 的复杂度（Operator Count）和上线时间（OS Start Date）的分布？
- 想快速统计有多少 alpha 匹配了金字塔，具体匹配了哪些？

为了解决这些问题，分享 **前置分析工具** : `SuperAlphaSelectionAnalyzer`。它的核心思想是： **在回测之前，先分析；用数据洞察，驱动优化**

**核心价值：从“盲目回测”到“精确打击”**

这个工具的价值远不止于展示数据，它是一个完整工作流的开端：

1.  **减少无效回测** ：通过对 `selection` 表达式匹配的 alpha 池进行预分析，你可以快速识别出质量不佳的 alpha 集合，从而避免对其进行耗时的回测。

2.  **数据驱动的精细化分层** ：你可以先用一个宽泛的表达式（例如 `own`）进行分析，然后根据 `turnover`, `operatorCount`, `is.sharpe` 等指标的分布，获得灵感来创建更精细、更优化的分层表达式。

3.  **智能优化与迭代** ：这是我们对这个工具的终极愿景！基于分析结果，工具未来可以**自动建议或生成**新的 `selection` 子句。例如：

- 如果分析发现 `turnover` 分布在 0.05 到 0.6，工具可以自动生成 `(turnover > 0.05 && turnover < 0.2)` 和 `(turnover > 0.2)` 两个新的、更聚焦的表达式。
- 如果匹配到的 alpha 数量过多，工具可以建议加入更多筛选条件来提纯你的 alpha 池。

**代码与使用**

使用方法非常简单。首先，你需要将下面的 `SuperAlphaSelectionAnalyzer` 类代码保存为 `sa_selection_analyzer.py` 文件。不知道怎么调格式，可以用AI提取下

**模块代码: `sa_selection_analyzer.py`**

```
# sa_selection_analyzer.pyimport urllib.parsefrom collections import Counterimport pandas as pdclass SuperAlphaSelectionAnalyzer:"""一个用于获取和分析 Super Alpha selection 表达式匹配结果的工具类。"""def__init__(self, session):"""初始化分析器。:param session: 已登录的 WorldQuant BRAIN session 对象。"""ifnotsession:raiseValueError("Session 对象不能为空。")self.session=sessionself.raw_results= []self.df=Nonedeffetch_alphas(self, selection_expr: str, region: str='USA', delay: int=1, selection_limit: int=1000) -> 'SuperAlphaSelectionAnalyzer':"""获取所有匹配表达式的 alpha 数据，并存储在实例内部。返回 self，以支持链式调用。"""print(f"正在为区域 '{region}' (Delay: {delay}) 拉取表达式的全部结果:")print(f" -> {selection_expr}")self.raw_results= []total_count_from_api=Nonebase_url="https://api.worldquantbrain.com/simulations/super-selection"params= {"settings.instrumentType": "EQUITY","settings.region": region,"settings.delay": delay,"selection": selection_expr,"limit": 100,"selectionLimit": selection_limit,"selectionHandling": "POSITIVE"}next_url=f"{base_url}?{urllib.parse.urlencode(params)}"page_num=1whilenext_url:print(f"正在拉取第 {page_num} 页数据...")try:response=self.session.get(next_url)response.raise_for_status()data=response.json()ifpage_num==1:total_count_from_api=data.get("count")iftotal_count_from_apiisnotNone:print(f"API 报告总数: {total_count_from_api} 条记录。")else:print("警告: 未能在第一页响应中找到 'count' 字段。")results_on_page=data.get("results", [])ifresults_on_page:self.raw_results.extend(results_on_page)next_url=data.get("next")ifnext_urland"http://"innext_urland":443"innext_url:next_url=next_url.replace("http://", "https://").replace(":443", "")page_num+=1exceptExceptionase:print(f"请求 API 时发生错误: {e}")try:print("API 错误响应:", response.text)except:pass# 清空已拉取的数据，表示失败self.raw_results= []breakprint(f"数据拉取完毕，共 {len(self.raw_results)} 条记录。")iftotal_count_from_apiisnotNone:iflen(self.raw_results) ==total_count_from_api:print(f"验证成功: 拉取到的记录数 ({len(self.raw_results)}) 与 API 报告的总数 ({total_count_from_api}) 一致。")else:print(f"!!! 验证失败: 拉取到的记录数 ({len(self.raw_results)}) 与 API 报告的总数 ({total_count_from_api}) 不一致。 !!!")ifself.raw_results:self.df=pd.json_normalize(self.raw_results)# 创建一个统一的 os.sharpe 列来处理不同的数据结构或缺失数据self.df['os.sharpe_unified'] =self.df.apply(self._extract_os_sharpe, axis=1)else:self.df=pd.DataFrame() # 如果没有结果，则创建一个空的DataFramereturnselfdef_extract_os_sharpe(self, row):"""一个辅助函数，用于从不同可能的位置提取 os.sharpe。"""# 优先尝试从 os.checks 列表中获取if'os.checks'inrowandisinstance(row['os.checks'], list):forcheckinrow['os.checks']:ifisinstance(check, dict) andcheck.get('name') =='SHARPE'and'value'incheck:returncheck['value']# 如果上面找不到，再尝试直接从 os.sharpe 获取if'os.sharpe'inrow:returnrow['os.sharpe']returnNone# 都找不到则返回Nonedefget_count(self) -> int:"""返回拉取到的 alpha 总数。"""returnlen(self.raw_results)defget_dataframe(self) -> pd.DataFrame:"""返回包含所有数据的 pandas DataFrame。"""returnself.dfdefget_metrics_summary(self, columns: list=None) -> pd.DataFrame:"""返回核心数值指标的统计摘要。"""ifself.dfisNoneorself.df.empty:print("没有数据可供分析。请先调用 fetch_alphas()。")returnNoneifcolumnsisNone:columns= ['is.sharpe', 'os.sharpe_unified', 'is.turnover', 'is.fitness','is.prodCorrelation', 'is.longCount', 'is.shortCount', 'regular.operatorCount']existing_cols= [colforcolincolumnsifcolinself.df.columns]ifnotexisting_cols:print("指定的列在数据中都不存在。")returnNonepd.set_option('display.float_format', lambdax: '%.3f'%x)returnself.df[existing_cols].describe(percentiles=[.25, .5, .75])defget_group_counts(self, group_by_column: str) -> pd.Series:"""按指定列进行分组并计数。"""ifself.dfisNoneorself.df.empty:print("没有数据可供分析。请先调用 fetch_alphas()。")returnNoneifgroup_by_columnnotinself.df.columns:print(f"错误: 列 '{group_by_column}' 不存在。")returnNonereturnself.df.groupby(group_by_column).size().sort_index()defget_failed_checks_summary(self) -> pd.Series:"""统计 IS Checks 中各项失败的次数。"""ifself.dfisNoneorself.df.emptyor'is.checks'notinself.df.columns:print("没有 'is.checks' 数据可供分析。")returnNonefailed_checks=self.df['is.checks'].explode().apply(lambdax: x['name'] ifisinstance(x, dict) andx.get('result') =='FAIL'elseNone)failed_counts=failed_checks.value_counts()returnfailed_countsifnotfailed_counts.emptyelsepd.Series(dtype=int)defget_pyramid_summary(self) -> pd.DataFrame:"""统计金字塔的匹配情况。"""ifself.dfisNoneorself.df.emptyor'is.checks'notinself.df.columns:print("没有 'is.checks' (pyramids) 数据可供分析。")returnNonepyramid_check=self.df['is.checks'].explode().dropna().apply(lambdax: xifisinstance(x, dict) andx.get('name') =='MATCHES_PYRAMID'andx.get('result') =='PASS'elseNone)alphas_with_pyramids=pyramid_check.dropna().index.unique().sizeprint(f"匹配到金字塔的 Alpha 总数: {alphas_with_pyramids}")all_pyramids=pyramid_check.dropna().apply(lambdax: [p['name'] forpinx.get('pyramids', [])])pyramid_counts=Counter(pforsublistinall_pyramidsforpinsublist)ifnotpyramid_counts:returnpd.DataFrame(columns=['Pyramid', 'Count'])pyramid_df=pd.DataFrame(pyramid_counts.items(), columns=['Pyramid', 'Count']).sort_values(by='Count', ascending=False).reset_index(drop=True)returnpyramid_dfdefget_worst_performers_report(self, sort_by_column: str, n: int=50, columns_to_show: list=None):"""找出按指定指标排序表现最差的 n 个 alpha，并展示它们的指定特征。:param sort_by_column: 用于排序的列 (e.g., 'os.sharpe_unified').:param n: 返回的最差 alpha 的数量.:param columns_to_show: 要展示的列.:return: 包含最差 n 个 alpha 特征的 DataFrame."""ifself.dfisNoneorself.df.empty:print("没有数据可供分析。请先调用 fetch_alphas()。")returnNoneifsort_by_columnnotinself.df.columns:print(f"错误: 排序参照列 '{sort_by_column}' 不存在。")returnNone# 确保排序列是数值类型self.df[sort_by_column] =pd.to_numeric(self.df[sort_by_column], errors='coerce')# 排序并选出最差的 n 个 (处理 NaN 值，将它们视为最差)worst_df=self.df.sort_values(by=sort_by_column, ascending=True, na_position='first').head(n)ifcolumns_to_showisNone:columns_to_show= ['id', sort_by_column, 'is.turnover', 'regular.operatorCount', 'is.sharpe']existing_cols= [colforcolincolumns_to_showifcolinworst_df.columns]returnworst_df[existing_cols]defget_conditional_subset(self, condition_column: str, operator: str, value: float) -> pd.DataFrame:"""根据指定条件筛选 alpha，并返回筛选后的 DataFrame 子集。:param condition_column: 用于筛选的列 (e.g., 'os.sharpe_unified').:param operator: 运算符 ('>', '<', '==', '>=', '<=').:param value: 用于比较的值.:return: 筛选后的 pandas DataFrame 子集."""ifself.dfisNoneorself.df.empty:print("没有数据可供分析。请先调用 fetch_alphas()。")returnpd.DataFrame()# 检查列是否存在，并处理缺失值ifcondition_columnnotinself.df.columns:print(f"错误: 条件列 '{condition_column}' 不存在。")returnpd.DataFrame()# 在比较前，确保列是数值类型，并将无法转换的设置为NaNnumeric_column=pd.to_numeric(self.df[condition_column], errors='coerce')# 根据操作符构建筛选条件ifoperator=='>':condition=numeric_column>valueelifoperator=='<':condition=numeric_column<valueelifoperator=='==':condition=numeric_column==valueelifoperator=='>=':condition=numeric_column>=valueelifoperator=='<=':condition=numeric_column<=valueelse:print(f"错误: 不支持的运算符 '{operator}'。")returnpd.DataFrame()# 应用筛选条件 (fillna(False)确保NaN值不被选中)subset_df=self.df[condition.fillna(False)]print(f"\n筛选条件: `{condition_column}{operator}{value}` | 匹配到的 Alpha 数量: {len(subset_df)}")ifsubset_df.empty:print("没有 Alpha 满足此条件。")returnsubset_dfdefget_sharpe_distribution(self, column: str='os.sharpe') -> pd.Series:"""计算 Sharpe 比率的分布情况。将 Sharpe 值分到预定义的桶中并计数。"""ifself.dfisNoneorself.df.emptyorcolumnnotinself.df.columns:print(f"没有 '{column}' 数据可供分析。")returnNone# 定义分桶的边界bins= [-float('inf'), -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, float('inf')]# 定义每个桶的标签labels= ["x < -1.5","-1.5 <= x < -1.0","-1.0 <= x < -0.5","-0.5 <= x < 0.0","0.0 <= x < 0.5","0.5 <= x < 1.0","1.0 <= x < 1.5","1.5 <= x < 2.0","2.0 <= x < 2.5","x >= 2.5"]# 使用 pd.cut 进行分桶sharpe_bins=pd.cut(self.df[column], bins=bins, labels=labels, right=False)# 统计每个桶的数量distribution=sharpe_bins.value_counts().sort_index()returndistribution
```

**使用范例: `test_superalpha_selection.py`**

然后，你可以像下面这样调用它（假设你的登录函数在 `machine_lib.py` 中）：

```
# example_usage.pyimport argparseimport pandas as pdfrom sa_selection_analyzer import SuperAlphaSelectionAnalyzerfrom machine_lib import logindef main():"""这是一个如何使用 SuperAlphaSelectionAnalyzer 类的示例。"""parser=argparse.ArgumentParser(description="使用 SuperAlphaSelectionAnalyzer 来拉取并分析 alpha 数据。")parser.add_argument("selection_expr",type=str,help="要测试的 FASTEXPR 筛选表达式 (请使用引号包裹).")parser.add_argument("--region", type=str, default="USA", help="目标区域 (默认: USA).")parser.add_argument("--delay", type=int, default=1, help="目标延迟 (默认: 1).")parser.add_argument("--selection-limit", type=int, default=1000, help="Super Alpha 的 selectionLimit 参数 (默认: 1000).")args=parser.parse_args()print("正在初始化会话...")sess=login()ifnotsess:print("登录失败，无法继续。")return# 1. 创建分析器实例analyzer=SuperAlphaSelectionAnalyzer(sess)# 2. 拉取数据 (这一步会自动处理分页、验证和数据转换)analyzer.fetch_alphas(selection_expr=args.selection_expr,region=args.region,delay=args.delay,selection_limit=args.selection_limit)# 3. 如果成功拉取到数据，则调用各种分析方法ifanalyzer.get_count() >0:# 打印核心指标摘要print("\n"+"="*60)print("1. 关键指标聚合分析")print("="*60)metrics_summary=analyzer.get_metrics_summary()print(metrics_summary)# 打印 OS Start Date 分布print("\n"+"="*60)print("2. 按 OS Start Date 分组统计")print("="*60)os_date_dist=analyzer.get_group_counts('os.startDate')print(os_date_dist.to_string())# 打印 IS Checks 失败统计print("\n"+"="*60)print("3. IS Checks 失败项统计")print("="*60)failed_summary=analyzer.get_failed_checks_summary()ifnotfailed_summary.empty:print(failed_summary.to_string())else:print("在 IS Checks 中没有发现失败项。")# 打印金字塔匹配摘要print("\n"+"="*60)print("4. 金字塔 (Pyramids) 匹配分析")print("="*60)pyramid_summary=analyzer.get_pyramid_summary()ifnotpyramid_summary.empty:print(pyramid_summary.to_string())# --- 新增：最差表现者分析 ---print("\n"+"="*60)print("5. 最差表现者分析 (按 os.sharpe_unified 排序)")print("="*60)# 获取 os.sharpe 最差的 50 个 alpha 的报告worst_performers_df=analyzer.get_worst_performers_report(sort_by_column='os.sharpe_unified',n=50,columns_to_show=['id', 'os.sharpe_unified', 'is.turnover', 'regular.operatorCount'])ifworst_performers_dfisnotNoneandnotworst_performers_df.empty:print("--- OS Sharpe 最差的 50 个 Alpha 的特征列表 ---")# 使用 to_string() 保证所有行都被打印print(worst_performers_df.to_string())print("\n--- 如何解读 ---")print("请观察上面列表中的 'is.turnover' 列。如果这些表现最差的 alpha 大都具有相似的 turnover (例如，普遍偏高或偏低)，")print("你就可以在你的主 selection 表达式中加入一个反向的条件 (例如 `&& is.turnover < 0.4`) 来过滤掉它们。")else:print("没有找到足够的数据来进行最差表现者分析。")print("\n示例脚本执行完毕。")if __name__ == "__main__":main()
```

```

```

**结果展示**

当我们运行 `python3 test_superalpha_selection.py "not(own)"` 时，你将得到类似下面这样清晰的报告：

正在为区域 'USA' (Delay: 1) 拉取表达式的全部结果:
  -> not(own)
正在拉取第 1 页数据...
API 报告总数: 634 条记录。
正在拉取第 2 页数据...
正在拉取第 3 页数据...
正在拉取第 4 页数据...
正在拉取第 5 页数据...
正在拉取第 6 页数据...
正在拉取第 7 页数据...
数据拉取完毕，共 634 条记录。
验证成功: 拉取到的记录数 (634) 与 API 报告的总数 (634) 一致。

============================================================
1. 关键指标聚合分析
============================================================
       is.sharpe  os.sharpe_unified  is.turnover  is.fitness  is.prodCorrelation  is.longCount  is.shortCount  regular.operatorCount
count    634.000            634.000      634.000     634.000             634.000       634.000        634.000                634.000
mean       2.008              0.615        0.232       1.261               0.501      1139.047       1096.144                 12.610
std        0.556              0.962        0.171       0.420               0.309       463.600        436.408                 10.077
min       -1.280             -1.870        0.010      -1.220               0.000        39.000          0.000                  0.000
25%        1.670              0.080        0.077       1.040               0.085       898.250        881.750                  7.000
50%        2.040              0.680        0.201       1.180               0.634      1183.500       1146.500                 10.000
75%        2.380              1.198        0.360       1.440               0.688      1510.750       1471.750                 15.000
max        3.460              3.530        0.699       3.170               0.992      3114.000       2070.000                 64.000

============================================================
2. 按 OS Start Date 分组统计
============================================================
os.startDate
2020-03-10      1
2020-06-21      2
2020-06-22      2
2020-06-23      2
2020-06-24      1
2020-06-30      2
2020-08-16     48
2020-11-12      1
2020-11-14      2
2020-11-15      1
2020-11-16      1
2020-11-20      1
2020-11-22      1
2020-11-23      2
2020-11-24      2
2020-11-27      1
2020-11-30      2
2020-12-01      2
2020-12-03      1
2020-12-04      3
2020-12-05      1
2020-12-15      2
2020-12-16      1
2020-12-17      1
2020-12-20      2
2020-12-24      3
2020-12-26      1
2020-12-28      2
2020-12-29      1
2020-12-30      4
2020-12-31      4
2021-01-01      3
2021-01-02      4
2021-01-03      4
2021-01-04      1
2021-01-06      1
2021-01-08      1
2021-01-12      1
2021-01-15      3
2021-01-16      2
2021-01-28      1
2021-01-31      2
2021-02-01      4
2021-02-02      4
2021-02-03      4
2021-02-04      4
2021-02-05      4
2021-02-06      4
2021-02-07      3
2021-02-08      4
2021-02-09      3
2021-02-10      4
2021-02-11      4
2021-02-12      4
2021-02-13      3
2021-02-14    462

============================================================
3. IS Checks 失败项统计
============================================================
在 IS Checks 中没有发现失败项。

============================================================
4. 金字塔 (Pyramids) 匹配分析
============================================================
匹配到金字塔的 Alpha 总数: 0

============================================================
5. 最差表现者分析 (按 os.sharpe_unified 排序)
============================================================
--- OS Sharpe 最差的 50 个 Alpha 的特征列表 ---
          id  os.sharpe_unified  is.turnover  regular.operatorCount
595  Erba0rJ             -1.870        0.010                      6
509  G30KQ2O             -1.860        0.051                      6
241  ozgxQM5             -1.830        0.073                     17
261  kmJ6mO8             -1.760        0.128                     19
327  0Q23Nlq             -1.700        0.266                      7
409  5qn3rJ5             -1.670        0.018                      7
607  1nWm03R             -1.570        0.022                      3
552  9A93a9q             -1.560        0.061                      4
599  Q5KEq5w             -1.540        0.017                     11
48   ov6Rxn5             -1.530        0.014                      1
283  YkEXJVA             -1.490        0.077                     10
624  AOLrJ5l             -1.470        0.051                      2
326  oz05Pn6             -1.450        0.267                      7
623  Q5WNLkr             -1.450        0.015                      3
463  nOMkb0q             -1.430        0.048                      4
578  zJ8XOJE             -1.430        0.015                     10
615  XYaVKPz             -1.410        0.017                      7
614  lRaEZZO             -1.390        0.023                      3
526  lRzdoPx             -1.350        0.034                      5
548  lRQgY3N             -1.340        0.018                      1
628  PXxdrpE             -1.340        0.018                      2
549  Q5nMZGK             -1.330        0.090                     10
613  1nWGjaM             -1.320        0.020                      2
341  vzEwejA             -1.320        0.075                      4
554  Erkg36r             -1.310        0.043                      9
560  XYpeonm             -1.310        0.036                      4
305  Ea2bkrr             -1.310        0.285                      7
582  8KjGe7X             -1.250        0.037                      3
237  mzXAY5x             -1.250        0.055                     28
287  K8zazmk             -1.240        0.143                     17
525  Q5lPjGw             -1.220        0.024                      5
629  Q5OrOkK             -1.220        0.029                      2
612  xmvlYqn             -1.180        0.024                      1
461  aWqXev6             -1.160        0.027                      5
501  ZWkvJY3             -1.140        0.014                      1
395  9AqW9R2             -1.120        0.018                      5
581  PX2gndp             -1.090        0.037                      7
498  N5kGNae             -1.040        0.019                      4
592  qmzQ2WE             -1.040        0.033                      6
513  nOY3Vw3             -1.030        0.015                      1
340  Yk3Jlmv             -1.010        0.205                      7
34   G6L9omG             -1.010        0.034                      7
284  EaNjNjP             -0.950        0.043                      3
306  xzEKP7b             -0.910        0.115                     10
606  WWlnZEZ             -0.890        0.071                      6
377  WXvl63d             -0.880        0.025                      0
477  Q5X6AJr             -0.860        0.019                     11
288  PlgAQN7             -0.850        0.262                      8
610  1nWG9rJ             -0.850        0.024                     16
41   61lgRO5             -0.810        0.095                     20

--- 如何解读 ---
请观察上面列表中的 'is.turnover' 列。如果这些表现最差的 alpha 大都具有相似的 turnover (例如，普遍偏高或偏低)，
你就可以在你的主 selection 表达式中加入一个反向的条件 (例如 `&& is.turnover < 0.4`) 来过滤掉它们。

希望这个工具能帮助到大家！欢迎提出改进意见。

---

## 讨论与评论 (11)

### 评论 #1 (作者: RM49262, 时间: 7个月前)

=====================================评论区=========================================

感谢大佬分享优秀的Super Alpha 思路，先码再看，准备拿来在AIAC组SA的时候派上用场

===================================================================================

---

### 评论 #2 (作者: DS48533, 时间: 7个月前)

[JX79797](/hc/en-us/profiles/30384388968343-JX79797) ，感觉你每个帖子都好干啊，喜欢，最近刚好需要学习SA，后面尝试运行玩玩～

---

### 评论 #3 (作者: SY43349, 时间: 7个月前)

跑了一下作者的代码，能够直观的给出一些特征，有一个小建议要是能够进一步指定标记就好了，这样就能直接获得一个可提交代码。  下面是作者代码的保留格式可复制版，由AI提取本地运行未见错误。

- sa_selection_analyzer.py

```
# sa_selection_analyzer.pyimport urllib.parsefrom collections import Counterimport pandas as pdclass SuperAlphaSelectionAnalyzer:    """    一个用于获取和分析 Super Alpha selection 表达式匹配结果的工具类。    """    def __init__(self, session):        """        初始化分析器。        :param session: 已登录的 WorldQuant BRAIN session 对象。        """        if not session:            raise ValueError("Session 对象不能为空。")        self.session = session        self.raw_results = []        self.df = None    def fetch_alphas(        self,        selection_expr: str,        region: str = 'USA',        delay: int = 1,        selection_limit: int = 1000    ) -> 'SuperAlphaSelectionAnalyzer':        """        获取所有匹配表达式的 alpha 数据，并存储在实例内部。        返回 self，以支持链式调用。        """        print(f"正在为区域 '{region}' (Delay: {delay}) 拉取表达式的全部结果:")        print(f" -> {selection_expr}")        self.raw_results = []        total_count_from_api = None        base_url = "https://api.worldquantbrain.com/simulations/super-selection"        params = {            "settings.instrumentType": "EQUITY",            "settings.region": region,            "settings.delay": delay,            "selection": selection_expr,            "limit": 100,            "selectionLimit": selection_limit,            "selectionHandling": "POSITIVE"        }        next_url = f"{base_url}?{urllib.parse.urlencode(params)}"        page_num = 1        while next_url:            print(f"正在拉取第 {page_num} 页数据...")            try:                response = self.session.get(next_url)                response.raise_for_status()                data = response.json()                if page_num == 1:                    total_count_from_api = data.get("count")                    if total_count_from_api is not None:                        print(f"API 报告总数: {total_count_from_api} 条记录。")                    else:                        print("警告: 未能在第一页响应中找到 'count' 字段。")                results_on_page = data.get("results", [])                if results_on_page:                    self.raw_results.extend(results_on_page)                next_url = data.get("next")                if next_url and "http://" in next_url and ":443" in next_url:                    next_url = next_url.replace("http://", "https://").replace(":443", "")                page_num += 1            except Exception as e:                print(f"请求 API 时发生错误: {e}")                try:                    print("API 错误响应:", response.text)                except Exception:                    pass                # 清空已拉取的数据，表示失败                self.raw_results = []                break        print(f"数据拉取完毕，共 {len(self.raw_results)} 条记录。")        if total_count_from_api is not None:            if len(self.raw_results) == total_count_from_api:                print(f"验证成功: 拉取到的记录数 ({len(self.raw_results)}) 与 API 报告的总数 ({total_count_from_api}) 一致。")            else:                print(f"!!! 验证失败: 拉取到的记录数 ({len(self.raw_results)}) 与 API 报告的总数 ({total_count_from_api}) 不一致。 !!!")        if self.raw_results:            self.df = pd.json_normalize(self.raw_results)            # 创建一个统一的 os.sharpe 列来处理不同的数据结构或缺失数据            self.df['os.sharpe_unified'] = self.df.apply(self._extract_os_sharpe, axis=1)        else:            self.df = pd.DataFrame()  # 如果没有结果，则创建一个空的DataFrame        return self    def _extract_os_sharpe(self, row):        """        一个辅助函数，用于从不同可能的位置提取 os.sharpe。        """        # 优先尝试从 os.checks 列表中获取        if 'os.checks' in row and isinstance(row['os.checks'], list):            for check in row['os.checks']:                if isinstance(check, dict) and check.get('name') == 'SHARPE' and 'value' in check:                    return check['value']        # 如果上面找不到，再尝试直接从 os.sharpe 获取        if 'os.sharpe' in row:            return row['os.sharpe']        return None  # 都找不到则返回None    def get_count(self) -> int:        """返回拉取到的 alpha 总数。"""        return len(self.raw_results)    def get_dataframe(self) -> pd.DataFrame:        """返回包含所有数据的 pandas DataFrame。"""        return self.df    def get_metrics_summary(self, columns: list = None) -> pd.DataFrame:        """返回核心数值指标的统计摘要。"""        if self.df is None or self.df.empty:            print("没有数据可供分析。请先调用 fetch_alphas()。")            return None        if columns is None:            columns = [                'is.sharpe', 'os.sharpe_unified', 'is.turnover', 'is.fitness',                'is.prodCorrelation', 'is.longCount', 'is.shortCount', 'regular.operatorCount'            ]        existing_cols = [col for col in columns if col in self.df.columns]        if not existing_cols:            print("指定的列在数据中都不存在。")            return None        pd.set_option('display.float_format', lambda x: '%.3f' % x)        return self.df[existing_cols].describe(percentiles=[.25, .5, .75])    def get_group_counts(self, group_by_column: str) -> pd.Series:        """按指定列进行分组并计数。"""        if self.df is None or self.df.empty:            print("没有数据可供分析。请先调用 fetch_alphas()。")            return None        if group_by_column not in self.df.columns:            print(f"错误: 列 '{group_by_column}' 不存在。")            return None        return self.df.groupby(group_by_column).size().sort_index()    def get_failed_checks_summary(self) -> pd.Series:        """统计 IS Checks 中各项失败的次数。"""        if self.df is None or self.df.empty or 'is.checks' not in self.df.columns:            print("没有 'is.checks' 数据可供分析。")            return None        failed_checks = self.df['is.checks'].explode().apply(            lambda x: x['name'] if isinstance(x, dict) and x.get('result') == 'FAIL' else None        )        failed_counts = failed_checks.value_counts()        return failed_counts if not failed_counts.empty else pd.Series(dtype=int)    def get_pyramid_summary(self) -> pd.DataFrame:        """统计金字塔的匹配情况。"""        if self.df is None or self.df.empty or 'is.checks' not in self.df.columns:            print("没有 'is.checks' (pyramids) 数据可供分析。")            return None        pyramid_check = self.df['is.checks'].explode().dropna().apply(            lambda x: x if isinstance(x, dict) and x.get('name') == 'MATCHES_PYRAMID' and x.get('result') == 'PASS' else None        )        alphas_with_pyramids = pyramid_check.dropna().index.unique().size        print(f"匹配到金字塔的 Alpha 总数: {alphas_with_pyramids}")        all_pyramids = pyramid_check.dropna().apply(            lambda x: [p['name'] for p in x.get('pyramids', [])]        )        pyramid_counts = Counter(p for sublist in all_pyramids for p in sublist)        if not pyramid_counts:            return pd.DataFrame(columns=['Pyramid', 'Count'])        pyramid_df = pd.DataFrame(            pyramid_counts.items(),            columns=['Pyramid', 'Count']        ).sort_values(by='Count', ascending=False).reset_index(drop=True)        return pyramid_df    def get_worst_performers_report(        self,        sort_by_column: str,        n: int = 50,        columns_to_show: list = None    ):        """        找出按指定指标排序表现最差的 n 个 alpha，并展示它们的指定特征。        :param sort_by_column: 用于排序的列 (e.g., 'os.sharpe_unified').        :param n: 返回的最差 alpha 的数量.        :param columns_to_show: 要展示的列.        :return: 包含最差 n 个 alpha 特征的 DataFrame.        """        if self.df is None or self.df.empty:            print("没有数据可供分析。请先调用 fetch_alphas()。")            return None        if sort_by_column not in self.df.columns:            print(f"错误: 排序参照列 '{sort_by_column}' 不存在。")            return None        # 确保排序列是数值类型        self.df[sort_by_column] = pd.to_numeric(self.df[sort_by_column], errors='coerce')        # 排序并选出最差的 n 个 (处理 NaN 值，将它们视为最差)        worst_df = self.df.sort_values(by=sort_by_column, ascending=True, na_position='first').head(n)        if columns_to_show is None:            columns_to_show = ['id', sort_by_column, 'is.turnover', 'regular.operatorCount', 'is.sharpe']        existing_cols = [col for col in columns_to_show if col in worst_df.columns]        return worst_df[existing_cols]    def get_conditional_subset(        self,        condition_column: str,        operator: str,        value: float    ) -> pd.DataFrame:        """        根据指定条件筛选 alpha，并返回筛选后的 DataFrame 子集。        :param condition_column: 用于筛选的列 (e.g., 'os.sharpe_unified').        :param operator: 运算符 ('>', '<', '==', '>=', '<=').        :param value: 用于比较的值.        :return: 筛选后的 pandas DataFrame 子集.        """        if self.df is None or self.df.empty:            print("没有数据可供分析。请先调用 fetch_alphas()。")            return pd.DataFrame()        # 检查列是否存在，并处理缺失值        if condition_column not in self.df.columns:            print(f"错误: 条件列 '{condition_column}' 不存在。")            return pd.DataFrame()        # 在比较前，确保列是数值类型，并将无法转换的设置为NaN        numeric_column = pd.to_numeric(self.df[condition_column], errors='coerce')        # 根据操作符构建筛选条件        if operator == '>':            condition = numeric_column > value        elif operator == '<':            condition = numeric_column < value        elif operator == '==':            condition = numeric_column == value        elif operator == '>=':            condition = numeric_column >= value        elif operator == '<=':            condition = numeric_column <= value        else:            print(f"错误: 不支持的运算符 '{operator}'。")            return pd.DataFrame()        # 应用筛选条件 (fillna(False)确保NaN值不被选中)        subset_df = self.df[condition.fillna(False)]        print(f"\n筛选条件: `{condition_column}{operator}{value}` | 匹配到的 Alpha 数量: {len(subset_df)}")        if subset_df.empty:            print("没有 Alpha 满足此条件。")        return subset_df    def get_sharpe_distribution(self, column: str = 'os.sharpe') -> pd.Series:        """        计算 Sharpe 比率的分布情况。        将 Sharpe 值分到预定义的桶中并计数。        """        if self.df is None or self.df.empty or column not in self.df.columns:            print(f"没有 '{column}' 数据可供分析。")            return None        # 定义分桶的边界        bins = [-float('inf'), -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, float('inf')]        # 定义每个桶的标签        labels = [            "x < -1.5",            "-1.5 <= x < -1.0",            "-1.0 <= x < -0.5",            "-0.5 <= x < 0.0",            "0.0 <= x < 0.5",            "0.5 <= x < 1.0",            "1.0 <= x < 1.5",            "1.5 <= x < 2.0",            "2.0 <= x < 2.5",            "x >= 2.5"        ]        # 使用 pd.cut 进行分桶        sharpe_bins = pd.cut(self.df[column], bins=bins, labels=labels, right=False)        # 统计每个桶的数量        distribution = sharpe_bins.value_counts().sort_index()        return distributio
```

- **test_superalpha_selection.py**

```
# example_usage.pyimport argparseimport pandas as pdfrom main_sa2_selector import SuperAlphaSelectionAnalyzerfrom wq_intergration.machine_lib import logindef main():    """    这是一个如何使用 SuperAlphaSelectionAnalyzer 类的示例。    """    parser = argparse.ArgumentParser(        description="使用 SuperAlphaSelectionAnalyzer 来拉取并分析 alpha 数据。"    )    parser.add_argument(        "--selection_expr",        type=str,        default='turnover<0.7',        help="要测试的 FASTEXPR 筛选表达式 (请使用引号包裹)."    )    parser.add_argument("--region", type=str, default="USA", help="目标区域 (默认: USA).")    parser.add_argument("--delay", type=int, default=1, help="目标延迟 (默认: 1).")    parser.add_argument("--selection-limit", type=int, default=1000, help="Super Alpha 的 selectionLimit 参数 (默认: 1000).")    args = parser.parse_args()    print("正在初始化会话...")    sess = login()    if not sess:        print("登录失败，无法继续。")        return    # 1. 创建分析器实例    analyzer = SuperAlphaSelectionAnalyzer(sess)    # 2. 拉取数据 (这一步会自动处理分页、验证和数据转换)    analyzer.fetch_alphas(        selection_expr=args.selection_expr,        region=args.region,        delay=args.delay,        selection_limit=args.selection_limit    )    # 3. 如果成功拉取到数据，则调用各种分析方法    if analyzer.get_count() > 0:        # 打印核心指标摘要        print("\n" + "=" * 60)        print("1. 关键指标聚合分析")        print("=" * 60)        metrics_summary = analyzer.get_metrics_summary()        print(metrics_summary)        # 打印 OS Start Date 分布        print("\n" + "=" * 60)        print("2. 按 OS Start Date 分组统计")        print("=" * 60)        os_date_dist = analyzer.get_group_counts('os.startDate')        print(os_date_dist.to_string())        # 打印 IS Checks 失败统计        print("\n" + "=" * 60)        print("3. IS Checks 失败项统计")        print("=" * 60)        failed_summary = analyzer.get_failed_checks_summary()        if failed_summary is not None and not failed_summary.empty:            print(failed_summary.to_string())        else:            print("在 IS Checks 中没有发现失败项。")        # 打印金字塔匹配摘要        print("\n" + "=" * 60)        print("4. 金字塔 (Pyramids) 匹配分析")        print("=" * 60)        pyramid_summary = analyzer.get_pyramid_summary()        if pyramid_summary is not None and not pyramid_summary.empty:            print(pyramid_summary.to_string())        # --- 新增：最差表现者分析 ---        print("\n" + "=" * 60)        print("5. 最差表现者分析 (按 os.sharpe_unified 排序)")        print("=" * 60)        # 获取 os.sharpe 最差的 50 个 alpha 的报告        worst_performers_df = analyzer.get_worst_performers_report(            sort_by_column='os.sharpe_unified',            n=50,            columns_to_show=['id', 'os.sharpe_unified', 'is.turnover', 'regular.operatorCount']        )        if worst_performers_df is not None and not worst_performers_df.empty:            print("--- OS Sharpe 最差的 50 个 Alpha 的特征列表 ---")            # 使用 to_string() 保证所有行都被打印            print(worst_performers_df.to_string())            print("\n--- 如何解读 ---")            print("请观察上面列表中的 'is.turnover' 列。如果这些表现最差的 alpha 大都具有相似的 turnover (例如，普遍偏高或偏低)，")            print("你就可以在你的主 selection 表达式中加入一个反向的条件 (例如 `&& is.turnover < 0.4`) 来过滤掉它们。")        else:            print("没有找到足够的数据来进行最差表现者分析。")    print("\n示例脚本执行完毕。")if __name__ == "__main__":    main()
```

---

### 评论 #4 (作者: JX79797, 时间: 7个月前)

1. 叠加筛选条件达到自己的目标数量
2. 去除 worst n 因子，&&turnover !=0.xxxx 
3. 搭积木式构建表达式，通过多重筛选每一块select精确数量的表达式

抛砖引玉，可以丰富下还有什么用法

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #5 (作者: XB37939, 时间: 7个月前)

=====================================评论区=========================================

感谢楼主的分享，最近也在做sa，也在寻找怎么快速高效组装sa的方法。

sa关键在于如何快速获取优质的alpha，再根据一些指标去过滤，可以参考楼主的进行学习

===================================================================================

---

### 评论 #6 (作者: CL86067, 时间: 7个月前)

大佬的思路很有用，为构建SA提供了新的优化方式，如果变成批量处理再配合论坛几位大佬的代码生成SA的系统会不会很有用呢？感觉是一个很好的方向

---

### 评论 #7 (作者: AH18340, 时间: 7个月前)

感谢大佬分享，提供了新的思路

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #8 (作者: ZM10537, 时间: 7个月前)

学习了

---

### 评论 #9 (作者: TW34761, 时间: 6个月前)

准备下载下来试试看，之前跑的那个没这么的详细

---

### 评论 #10 (作者: MG88592, 时间: 6个月前)

感谢jx哥的分享，jx哥一直分享十分有用提升效率都好方法，这些方法对新赛季降低回测数量的帮助尤为重要。

这就开始拜读，有不懂的还希望徐哥不吝赐教。

Respect 

————————————————————————————————————————

---

### 评论 #11 (作者: QL88701, 时间: 3个月前)

感觉这个代码更适合not own，对于gold选手来说用这个其实意义不大，等我上exp之后一定要尝试一下！

=================================================== 每日谨记： 提交因子不能抱侥幸心理！！ 分散，质量，margin！！ 坚持一定会有结果！！ ===================================================

---

