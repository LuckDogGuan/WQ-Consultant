# 【代码分享】相关性剪枝，减少无效回测，拷贝即用代码优化

- **链接**: [Commented] 【代码分享】相关性剪枝减少无效回测拷贝即用代码优化.md
- **作者**: QL88701
- **发布时间/热度**: 2个月前, 得票: 17

## 帖子正文

无论是在跑一二阶还是模板时，尽管他们的字段或者操作符不一样但都无法避免会回测出一堆相关性很高因子（这里说的相关性是指因子在这批因子中的最大相关性，并非平台的PC），如果想要对这批因子再工作时往往又会回测出更大一批存在相关性更高的因子，因此进行相关性剪枝变得尤为重要，这可以大大提高工作效率。

效果展示： ![图片](images/img_4db5e86912.png)

经验所得，我推荐阈值设置成0.8就行了。

废话不多说，下面是完整代码，我基本都加了注释，方便大家阅读，可以直接拷贝进你的回测系统，十分方便。

#相关性剪枝

def correlation_pruning(fo_tracker, correlation_threshold=0.7):

"""

对fo_tracker进行相关性剪枝，筛出互相关性大于阈值的因子

互相关性是指这个因子在这堆因子中的最大相关性

Args:

fo_tracker: alpha跟踪器数据，格式为[(alpha_id, expr, sharpe, ...), ...]

correlation_threshold: 相关性阈值，默认为0.7

Returns:

剪枝后的fo_tracker列表

"""

if len(fo_tracker) <= 1:

return fo_tracker

print(f"开始相关性剪枝，初始因子数量: {len(fo_tracker)}")

# 获取alpha_id列表

alpha_ids = [rec[0] for rec in fo_tracker]

# 获取所有alpha的PnL数据

alpha_pnls = pd.DataFrame()

s = login()

for alpha_id in alpha_ids:

try:

pnl = s.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl").json(](https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl%22).json() )

df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])

df = df.rename(columns={'date':'Date', 'pnl':alpha_id})

df = df[['Date', alpha_id]]

df = df.set_index('Date')

alpha_pnls = pd.concat([alpha_pnls, df], axis=1)

except Exception as e:

print(f"获取alpha {alpha_id} 的PnL数据失败: {e}")

continue

if alpha_pnls.empty:

print("无法获取PnL数据，跳过相关性剪枝")

return fo_tracker

# 计算收益率

alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)

# 使用最近10年的数据（参考selfCorrCheck.py）

alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index) > pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=10)]

# 动态相关性剪枝 - 注意：去掉高相关性因子后下一个因子的互相关性可能会改变

remaining_alphas = alpha_ids.copy()

pruned_alphas = []

iteration = 0

while remaining_alphas:

iteration += 1

print(f"第 {iteration} 轮剪枝，剩余因子数量: {len(remaining_alphas)}")

# 计算当前剩余因子的相关性矩阵

current_rets = alpha_rets[remaining_alphas]

# 处理缺失值

current_rets = current_rets.dropna(how='all')

if len(current_rets) < 10:  # 确保有足够的数据点

print("数据点不足，停止剪枝")

break

corr_matrix = current_rets.corr()

# 找到每个因子的最大互相关性

max_correlations = {}

for alpha in remaining_alphas:

# 排除自身相关性

other_alphas = [a for a in remaining_alphas if a != alpha]

if other_alphas:

try:

max_corr = corr_matrix.loc[alpha, other_alphas].max()

max_correlations[alpha] = max_corr

except KeyError:

max_correlations[alpha] = 0

else:

max_correlations[alpha] = 0

# 找到最大互相关性最高的因子

if not max_correlations:

break

max_corr_alpha = max(max_correlations.items(), key=lambda x: x[1])

alpha_id, max_corr = max_corr_alpha

if max_corr > correlation_threshold:

# 移除相关性最高的因子

remaining_alphas.remove(alpha_id)

pruned_alphas.append(alpha_id)

print(f"剪枝因子 {alpha_id}，最大互相关性: {max_corr:.4f}")

else:

# 所有剩余因子的最大互相关性都低于阈值，停止剪枝

print(f"所有剩余因子的最大互相关性均低于阈值 {correlation_threshold}，停止剪枝")

break

# 构建剪枝后的结果

pruned_fo_tracker = []

for rec in fo_tracker:

alpha_id = rec[0]

if alpha_id in remaining_alphas:

pruned_fo_tracker.append(rec)

print(f"相关性剪枝完成: {len(fo_tracker)} -> {len(pruned_fo_tracker)} 个因子")

print(f"剪枝了 {len(pruned_alphas)} 个因子: {pruned_alphas}")

return pruned_fo_tracker

---

## 讨论与评论 (5)

### 评论 #1 (作者: HH34943, 时间: 2个月前)

这里跟原始的123阶模版代码的相关性剪枝有区别吗

---

### 评论 #2 (作者: JX14975, 时间: 2个月前)

楼主的帖子相比原有的相关性剪枝帖子的不同点在于使用了最大互相关性作为判断剪枝顺序的最优先标准。理论上能够找出最多的阈值以上的alpha，从而能够找到尽可能多的可提交因子。值得参考。

---

### 评论 #3 (作者: WL58980, 时间: 2个月前)

大佬的帖子太有用了，受益匪浅呀！！！感谢！！！

============================================================================

Study hard — quality over quantity, no room for mediocrity. Cherish every learning opportunity, stay focused, and learn from the experts. Keep pushing!

============================================================================

---

### 评论 #4 (作者: QL88701, 时间: 2个月前)

这里的剪枝优先筛掉相关性最大的因子，但是并不考虑高相关性因子的性能指标，考虑引入指标参考，保留部分高相关且指标好的因子。

===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================

---

### 评论 #5 (作者: MZ45384, 时间: 1个月前)

好久没看到相关性剪纸的新观点帖子了。二三级阶筛选作用很大，大大减少了多余的回测。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

