# [代码优化]样本内外分布一致性分析月份对比代码分享代码优化

- **链接**: [Commented] [代码优化]样本内外分布一致性分析月份对比代码分享代码优化.md
- **作者**: TL32287
- **发布时间/热度**: 1年前, 得票: 12

## 帖子正文

对比存在，假想VF是存在成长因子，对于该方法，我借助分析师源代码编写了一份对比月份图。

这是效果图： ![图片](images/img_3d7b4e70d9.png)  ![图片](images/img_841ad5ab50.png)

直接重点戏，放代码：
根据获取到的列表数据特点编写获取月份的代码：

def get_month(alpha_list_submitted, month):

"""

根据传入的开始日期和结束日期过滤数据框

参数:

alpha_list_submitted (pd.DataFrame): 包含日期数据的数据框

startday (str): 开始日期字符串，格式为"YYYY-MM-DD"

endday (str): 结束日期字符串，格式为"YYYY-MM-DD"

返回:

pd.DataFrame: 过滤后的数据框，包含指定日期范围内的数据

"""

# 提取开始日期和结束日期的年月部分

start = f'2025-{month}'

end = f'2025-{month}'

# 从数据框的日期列提取年月部分（前7个字符）

df_range = alpha_list_submitted.copy()

df_range['year_month'] = df_range['dateSubmitted'].str[:7]

# 筛选在指定日期范围内的数据

filtered_df = df_range[(df_range['year_month'] >= start) & (df_range['year_month'] <= end)]

# 返回筛选后的数据（可选：移除临时列）

return filtered_df.drop(columns=['year_month'])
这里的2025是直接改好的，后续可以增加优化。
然后就是遍历数据跟之前的变化不大：

#获取不同的month，画出不同的month的performance

months = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

month_list = [x for x in months]

for month in month_list:

df_month = get_month(df_alpha_list_submitted, month)

df_is_performance = get_performance(df_month, 'is')

df_os_performance = get_performance(df_month, 'os')

sharpe_os, turnover_os, returns_os, margin_os, fitness_os = get_performance_metrics(df_os_performance)

sharpe_is, turnover_is, returns_is, margin_is, fitness_is = get_performance_metrics(df_is_performance)

plot_is_os_performance_matrix(df_is_performance, df_os_performance, f'Month {month}')

这一步就可以实现月份分析的部分，然后增加对比月份分析的代码：

# 定义月份对比关系

month_pairs = [

('01', '04'), ('02', '05'), ('03', '06'),

('04', '07'), ('05', '08'), ('06', '09'),

('07', '10'), ('08', '11'), ('09', '12')

]

# 对每一对月份进行对比分析

for month1, month2 in month_pairs:

# 获取两个月份的数据

df_month1 = get_month(df_alpha_list_submitted, month1)

df_month2 = get_month(df_alpha_list_submitted, month2)

# 获取两个月份的IS和OS绩效数据

df_is_performance1 = get_performance(df_month1, 'is')

df_os_performance1 = get_performance(df_month1, 'os')

sharpe_os1, turnover_os1, returns_os1, margin_os1, fitness_os1 = get_performance_metrics(df_os_performance1)

sharpe_is1, turnover_is1, returns_is1, margin_is1, fitness_is1 = get_performance_metrics(df_is_performance1)

df_is_performance2 = get_performance(df_month2, 'is')

df_os_performance2 = get_performance(df_month2, 'os')

sharpe_os2, turnover_os2, returns_os2, margin_os2, fitness_os2 = get_performance_metrics(df_os_performance2)

sharpe_is2, turnover_is2, returns_is2, margin_is2, fitness_is2 = get_performance_metrics(df_is_performance2)

# 绘制两个月份IS性能的对比图

fig, axes = plt.subplots(3, 2, figsize=(15, 15))

fig.suptitle(f'IS Performance Comparison: Month {month1} vs Month {month2}', fontsize=16)

# Sharpe Ratio 对比

sns.histplot(sharpe_is1, bins=20, kde=True, ax=axes[0, 0], color='blue', label=f'Month {month1}')

sns.histplot(sharpe_is2, bins=20, kde=True, ax=axes[0, 0], color='red', label=f'Month {month2}')

axes[0, 0].set_title('Sharpe Ratio Distribution')

axes[0, 0].legend()

# Turnover 对比

sns.histplot(turnover_is1, bins=20, kde=True, ax=axes[0, 1], color='blue', label=f'Month {month1}')

sns.histplot(turnover_is2, bins=20, kde=True, ax=axes[0, 1], color='red', label=f'Month {month2}')

axes[0, 1].set_title('Turnover Distribution')

axes[0, 1].legend()

# Returns 对比

sns.histplot(returns_is1, bins=20, kde=True, ax=axes[1, 0], color='blue', label=f'Month {month1}')

sns.histplot(returns_is2, bins=20, kde=True, ax=axes[1, 0], color='red', label=f'Month {month2}')

axes[1, 0].set_title('Returns Distribution')

axes[1, 0].legend()

# Margin 对比

sns.histplot(margin_is1, bins=20, kde=True, ax=axes[1, 1], color='blue', label=f'Month {month1}')

sns.histplot(margin_is2, bins=20, kde=True, ax=axes[1, 1], color='red', label=f'Month {month2}')

axes[1, 1].set_title('Margin Distribution')

axes[1, 1].legend()

# Fitness 对比

sns.histplot(fitness_is1, bins=20, kde=True, ax=axes[2, 0], color='blue', label=f'Month {month1}')

sns.histplot(fitness_is2, bins=20, kde=True, ax=axes[2, 0], color='red', label=f'Month {month2}')

axes[2, 0].set_title('Fitness Distribution')

axes[2, 0].legend()

# 计算并显示关键指标的平均值对比

comparison_data = {

'Metric': ['Sharpe', 'Turnover', 'Returns', 'Margin', 'Fitness'],

f'Month {month1}': [

sharpe_is1.mean(),

turnover_is1.mean(),

returns_is1.mean(),

margin_is1.mean(),

fitness_is1.mean()

],

f'Month {month2}': [

sharpe_is2.mean(),

turnover_is2.mean(),

returns_is2.mean(),

margin_is2.mean(),

fitness_is2.mean()

]

}

df_comparison = pd.DataFrame(comparison_data)

axes[2, 1].axis('off')

table = axes[2, 1].table(

cellText=df_comparison.round(3).values,

colLabels=df_comparison.columns,

cellLoc='center',

loc='center'

)

table.auto_set_font_size(False)

table.set_fontsize(10)

table.scale(1, 1.5)

axes[2, 1].set_title('Performance Metrics Comparison')

plt.tight_layout()

plt.subplots_adjust(top=0.95)

plt.show()

# 对每一对月份进行OS性能对比分析，有OS的时候取消注释。

for month1, month2 in month_pairs:

# 获取两个月份的数据

df_month1 = get_month(df_alpha_list_submitted, month1)

df_month2 = get_month(df_alpha_list_submitted, month2)

# 提取OS性能数据

df_os_performance1 = get_performance(df_month1, 'os')

sharpe_os1, turnover_os1, returns_os1, margin_os1, fitness_os1 = get_performance_metrics(df_os_performance1)

df_os_performance2 = get_performance(df_month2, 'os')

sharpe_os2, turnover_os2, returns_os2, margin_os2, fitness_os2 = get_performance_metrics(df_os_performance2)

# 创建OS性能对比图表

fig, axes = plt.subplots(3, 2, figsize=(15, 15))

fig.suptitle(f'OS Performance Comparison: Month {month1} vs Month {month2}', fontsize=16)

# Sharpe Ratio 对比

sns.histplot(sharpe_os1, bins=20, kde=True, ax=axes[0, 0], color='blue', alpha=0.6, label=f'Month {month1}')

sns.histplot(sharpe_os2, bins=20, kde=True, ax=axes[0, 0], color='red', alpha=0.6, label=f'Month {month2}')

axes[0, 0].set_title('Sharpe Ratio Distribution (OS)')

axes[0, 0].legend()

# Turnover 对比

sns.histplot(turnover_os1, bins=20, kde=True, ax=axes[0, 1], color='blue', alpha=0.6, label=f'Month {month1}')

sns.histplot(turnover_os2, bins=20, kde=True, ax=axes[0, 1], color='red', alpha=0.6, label=f'Month {month2}')

axes[0, 1].set_title('Turnover Distribution (OS)')

axes[0, 1].legend()

# Returns 对比

sns.histplot(returns_os1, bins=20, kde=True, ax=axes[1, 0], color='blue', alpha=0.6, label=f'Month {month1}')

sns.histplot(returns_os2, bins=20, kde=True, ax=axes[1, 0], color='red', alpha=0.6, label=f'Month {month2}')

axes[1, 0].set_title('Returns Distribution (OS)')

axes[1, 0].legend()

# Margin 对比

sns.histplot(margin_os1, bins=20, kde=True, ax=axes[1, 1], color='blue', alpha=0.6, label=f'Month {month1}')

sns.histplot(margin_os2, bins=20, kde=True, ax=axes[1, 1], color='red', alpha=0.6, label=f'Month {month2}')

axes[1, 1].set_title('Margin Distribution (OS)')

axes[1, 1].legend()

# Fitness 对比

sns.histplot(fitness_os1, bins=20, kde=True, ax=axes[2, 0], color='blue', alpha=0.6, label=f'Month {month1}')

sns.histplot(fitness_os2, bins=20, kde=True, ax=axes[2, 0], color='red', alpha=0.6, label=f'Month {month2}')

axes[2, 0].set_title('Fitness Distribution (OS)')

axes[2, 0].legend()

# 性能指标均值对比表

comparison_data = {

'Metric': ['Sharpe', 'Turnover', 'Returns', 'Margin', 'Fitness'],

f'Month {month1}': [

sharpe_os1.mean(),

turnover_os1.mean(),

returns_os1.mean(),

margin_os1.mean(),

fitness_os1.mean()

],

f'Month {month2}': [

sharpe_os2.mean(),

turnover_os2.mean(),

returns_os2.mean(),

margin_os2.mean(),

fitness_os2.mean()

]

}

df_comparison = pd.DataFrame(comparison_data)

axes[2, 1].axis('off')

table = axes[2, 1].table(

cellText=df_comparison.round(3).values,

colLabels=df_comparison.columns,

cellLoc='center',

loc='center',

colWidths=[0.2, 0.4, 0.4]

)

table.auto_set_font_size(False)

table.set_fontsize(10)

table.scale(1, 1.5)

axes[2, 1].set_title('OS Performance Metrics Comparison')

# 优化布局

plt.tight_layout()

plt.subplots_adjust(top=0.93)

plt.show()

至此，介绍完毕，感谢同僚的阅读。你的小小建议是我的一大步提升。

---

## 讨论与评论 (4)

### 评论 #1 (作者: SZ83096, 时间: 1年前)

==========================================================

大佬🐮，感谢分享，我已经提前用上大佬的代码了，很好用，可以直观看到自己每个月的提交的alpha对比情况，有助于分析提交的alpha，找出不足之处进行改进。

祝大佬vf 节节高。

==========================================================

---

### 评论 #2 (作者: ML42552, 时间: 1年前)

感谢大佬分享，我愿称汝为worldquant最强高中生！！！！

已经在用这套代码进行分析了，单从成长性来看，4月分更新的vaule factor 大幅下降似乎有迹可循，不管是提交的数量还是整体的质量上都有较大的下降。目前来看5月和6月的value factor 应该能有一定程度的提升！！！

------------------------------------------------------------------

祝愿大佬vf 节节高！！！！

---

### 评论 #3 (作者: AL13375, 时间: 11个月前)

==========================================================

大佬太牛逼了！！！感谢分享，已经用上大佬的代码了，很好用，可以直观看到自己每个月的提交的alpha对比情况，有助于分析提交的alpha，找出不足之处进行改进。

祝大佬vf 节节高，genius level 更上一层楼！！！

==========================================================

---

### 评论 #4 (作者: DZ31817, 时间: 9个月前)

20250928

------------------------------------------------------------------------------------------

这个工具对提升自己的vf有很大帮助，每次提交前运行一下再决定是否提交。好东西，收藏了。

---

