# 如何拯救高turnover因子？一文助你理解并降低因子turnover代码优化

- **链接**: [Commented] 如何拯救高turnover因子一文助你理解并降低因子turnover代码优化.md
- **作者**: ZS59763
- **发布时间/热度**: 1年前, 得票: 167

## 帖子正文

顾名思义，在回测中常常能遇到高turn高sharpe高fit但低margin的因子。这类因子会直接影响我们的combined performance score，降低被PM采纳获得weight的机会，下面给大家分享如何降低换手率的常见方法

## ***如何理解turn，margin和return的关系？***

粗线条地说，return=turnover*margin，所以在给定收益的情况下，换手率越高，margin越低。margin跟手续费相关联，所以为了较高的margin，需要压低turnover。形象来说，我今天交易10次股票，挣了100块，那么我单笔交易平均收益10元，扣除5元手续费还有净利润。倘若我用1000次交易挣得100元，那么单笔交易收益降低至0.1元，远远不够手续费。

## ***降低turn的方式有哪些？***

常见的降turn方式有：增加decay，使用tradewhen，使用降turn运算符。

![图片](images/img_25995dafb5.png)

增加decay的方式可以提升信号的“一致性”，让信号不是那么频繁的变化（后文我们也会看到，一些降turn的op采取的也是类似的思想）

***使用tradewhen：*** tradewhen相当于增加开平仓条件，减少信号频繁变化的次数。直观的理解：市场并非天天大涨大跌，针对市场整体涨跌幅波动率小于1%（仅为举例）的时间窗口，不进行交易，这样可以减少一段时间内的整体换手率（但是会以表现为代价）

推荐阅读： [我可以使用 Trade_when 来降低流水率吗？– WorldQuant 大脑](../AM60509/[Commented] Can I use Trade_when to decease the Turnover.md)

***使用降turn运算符***

![图片](images/img_553aa056f3.png)

![图片](images/img_37e0c6c5be.png)

降低turn运算符的核心思路在于限制变化幅度，从而减少仓位变化。可以指定turnover具体数值（实际结果会略微高于这个数值），但注意：较低的数值可能会完全破坏信号逻辑，使得因子无效。

## ***实操方式：***

本帖给出相关代码，使得可以按照turn区间筛选因子并利用降turn运算符进行处理回测。此外，本帖也提供了一个可以抓取并统计字段（向量类型数据按照vec运算符计算）的方法（来自本人另一篇文章： [如何统计得到的字段数？如何抓取多地区因子一起检验？ – WorldQuant BRAIN](/hc/en-us/community/posts/28754183939351-%E5%A6%82%E4%BD%95%E7%BB%9F%E8%AE%A1%E5%BE%97%E5%88%B0%E7%9A%84%E5%AD%97%E6%AE%B5%E6%95%B0-%E5%A6%82%E4%BD%95%E6%8A%93%E5%8F%96%E5%A4%9A%E5%9C%B0%E5%8C%BA%E5%9B%A0%E5%AD%90%E4%B8%80%E8%B5%B7%E6%A3%80%E9%AA%8C) ）

## **抓取因子：**

def get_alphas(start_date, end_date, sharpe_th, fitness_th,turnover_th_up,turnover_th_down, region, alpha_num, usage):

s = login()

output = []

# 3E large 3C less

count = 0

for i in range(0, alpha_num, 100):

print(i)

url_e = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \

+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + start_date  \

+ "T00:00:00-04:00&dateCreated%3C" + end_date \

+ "T00:00:00-04:00&is.fitness%3E" + str(fitness_th) + "&is.sharpe%3E" \

+ str(sharpe_th) + "&settings.region=" + region + "&order=-is.sharpe&hidden=false&type!=SUPER"

url_c = " [https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)](https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d%22%(i))  \

+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=" + start_date  \

+ "T00:00:00-04:00&dateCreated%3C" + end_date \

+ "T00:00:00-04:00&is.fitness%3C-" + str(fitness_th) + "&is.sharpe%3C-" \

+ str(sharpe_th) + "&settings.region=" + region + "&order=is.sharpe&hidden=false&type!=SUPER"

urls = [url_e]

if usage != "submit":

urls.append(url_c)

for url in urls:

response = s.get(url)

#print(response.json())

try:

alpha_list = response.json()["results"]

#print(response.json())

for j in range(len(alpha_list)):

alpha_id = alpha_list[j]["id"]

name = alpha_list[j]["name"]

dateCreated = alpha_list[j]["dateCreated"]

sharpe = alpha_list[j]["is"]["sharpe"]

fitness = alpha_list[j]["is"]["fitness"]

turnover = alpha_list[j]["is"]["turnover"]

margin = alpha_list[j]["is"]["margin"]

longCount = alpha_list[j]["is"]["longCount"]

shortCount = alpha_list[j]["is"]["shortCount"]

decay = alpha_list[j]["settings"]["decay"]

exp = alpha_list[j]['regular']['code']

count += 1

#if (sharpe > 1.2 and sharpe < 1.6) or (sharpe < -1.2 and sharpe > -1.6):

if (longCount + shortCount) > 100 and (turnover>turnover_th_up) and (turnover<turnover_th_down):

if sharpe < -sharpe_th:

exp = "-%s"%exp

rec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]

print(rec)

if turnover > 0.7:

rec.append(decay*4)

elif turnover > 0.6:

rec.append(decay*3+3)

elif turnover > 0.5:

rec.append(decay*3)

elif turnover > 0.4:

rec.append(decay*2)

elif turnover > 0.35:

rec.append(decay+4)

elif turnover > 0.3:

rec.append(decay+2)

output.append(rec)

except:

print("%d finished re-login"%i)

s = login()

print("count: %d"%count)

return output

def transform(next_alpha_recs, region):

output = []

for rec in next_alpha_recs:

decay = rec[-1]

exp = rec[1]

output.append([exp,decay])

output_dict = {region : output}

return output_dict

def prune(next_alpha_recs, prefix, keep_num):

# prefix is the datafield prefix, fnd6, mdl175 ...

# keep_num is the num of top sharpe same-datafield alpha

output = []

num_dict = defaultdict(int)

for rec in next_alpha_recs:

exp = rec[1]

field = exp.split(prefix)[-1].split(",")[0]

sharpe = rec[2]

if sharpe < 0:

field = "-%s"%field

if num_dict[field] < keep_num:

num_dict[field] += 1

decay = rec[-1]

exp = rec[1]

output.append([exp,decay])

return output

## get promising alphas to improve in the next order

fo_tracker = get_alphas("2025-03-01", "2025-03-24", 1.6,1,0.3,0.7, "ASI", 9000, "track")

print(len(fo_tracker))

get_alphas函数参数：开始日期，结束日期，最低sharpe，最低fit，turn下限，turn上限，地区，数量，抓取类型 。

## 减枝函数：

def prune_modified(next_alpha_recs,prefix,keep_num):

output = []

num_dict = defaultdict(int)

for rec in next_alpha_recs:

exp = rec[1]

sharpe = rec[2]

field = exp.split(prefix)[-1].split(",")[0]

if sharpe < 0:

field = "-%s"%field

if num_dict[field] < keep_num:

num_dict[field] += 1

output.append(rec)

return output

def extract_fields(next_alpha_recs):

field_counts = defaultdict(int)

for rec in next_alpha_recs:

# 提取完整字段名

full_field = rec[1]

# 找到 winsorize 或 ts_backfill 的位置

#winsorize_index = full_field.find('winsorize(')

backfill_index = full_field.find('ts_backfill(')

end_index=full_field.find(', 120')

# 选择最先出现的位置

if backfill_index != -1 and backfill_index != -1:

cut_index = min(backfill_index, end_index)

elif backfill_index != -1:

cut_index = backfill_index

elif end_index != -1:

cut_index = end_index

else:

# 如果没有找到这两个关键词，跳过此记录

continue

# 提取字段名（cut_index之前的部分）

field_name = full_field[cut_index+12:end_index].strip()

field_counts[field_name] += 1

return dict(field_counts)

def prune_second_order(inputdata,all_dict):

th_tracker1=inputdata.copy()

outpur=th_tracker1

for i in all_dict.keys():

if all_dict[i]>100:

outpur=prune_modified(outpur,i,2)

if all_dict[i]<=100 and all_dict[i]>20:

outpur=prune_modified(outpur,i,3)

if all_dict[i]>10 and all_dict[i]<=50:

outpur=prune_modified(outpur,i,4)

if all_dict[i]>3 and all_dict[i]<=10:

outpur=prune_modified(outpur,i,5)

return outpur

fo_tracker_new=[]

for i in fo_tracker:

if ';' not in i[1]:

fo_tracker_new.append(i)

print(len(fo_tracker_new))

all_dict=extract_fields(fo_tracker_new)

print(all_dict)

fo_tracker_tailed=prune_second_order(fo_tracker_new,all_dict)

fo_tracker_new=[]

for i in range(len(fo_tracker_tailed)):

index=0

for j in [';']:

if j in fo_tracker_tailed[i][1]:

index=1

if index==0:

fo_tracker_new.append(fo_tracker_tailed[i][1])

print(len(fo_tracker_tailed))

#all_dict=extract_fields(fo_tracker_new)

print(len(fo_tracker_new))

print(fo_tracker_new[0:3])

## **加入运算符：**

so_alpha_list = []

for expr in fo_tracker_new:

so_alpha_list.append('ts_target_tvr_decay('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.05)')

so_alpha_list.append('ts_target_tvr_decay('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.1)')

so_alpha_list.append('ts_target_tvr_decay('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.2)')

so_alpha_list.append('ts_target_tvr_decay('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.25)')

so_alpha_list.append('ts_target_tvr_decay('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.3)')

so_alpha_list.append('ts_target_tvr_hump('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.05)')

so_alpha_list.append('ts_target_tvr_hump('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.1)')

so_alpha_list.append('ts_target_tvr_hump('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.2)')

so_alpha_list.append('ts_target_tvr_hump('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.25)')

so_alpha_list.append('ts_target_tvr_hump('+expr+', lambda_min=0, lambda_max=1, target_tvr=0.3)')

so_alpha_list.append('hump_decay('+expr+', p=0)')

so_alpha_list.append('hump_decay('+expr+', p=0.01)')

so_alpha_list.append('hump_decay('+expr+', p=0.1)')

so_alpha_list.append('hump_decay('+expr+', p=1)')

so_alpha_list.append('ts_decay_exp_window('+expr+', 240, factor =0.5)')

so_alpha_list.append('ts_decay_exp_window('+expr+', 120, factor =0.5)')

so_alpha_list.append('ts_decay_exp_window('+expr+', 20, factor =0.5)')

so_alpha_list.append('ts_decay_exp_window('+expr+', 60, factor =0.5)')

so_alpha_list.append('ts_decay_exp_window('+expr+', 40, factor =0.5)')

so_alpha_list.append('ts_decay_linear('+expr+', 240, dense = false)')

so_alpha_list.append('ts_decay_linear('+expr+', 120, dense = false)')

so_alpha_list.append('ts_decay_linear('+expr+', 60, dense = false)')

so_alpha_list.append('ts_decay_linear('+expr+', 40, dense = false)')

so_alpha_list.append('ts_decay_linear('+expr+', 20, dense = false)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+', 1, lambda_min=0, lambda_max=1,target_tvr=0.05)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+', 1, lambda_min=0, lambda_max=1,target_tvr=0.1)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+', 1, lambda_min=0, lambda_max=1,target_tvr=0.15)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+', 1, lambda_min=0, lambda_max=1,target_tvr=0.2)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+', 1, lambda_min=0, lambda_max=1,target_tvr=0.25)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+', 1, lambda_min=0, lambda_max=1,target_tvr=0.3)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',close, lambda_min=0, lambda_max=1,target_tvr=0.05)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',close, lambda_min=0, lambda_max=1,target_tvr=0.1)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',close, lambda_min=0, lambda_max=1,target_tvr=0.15)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',close, lambda_min=0, lambda_max=1,target_tvr=0.2)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',close, lambda_min=0, lambda_max=1,target_tvr=0.25)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',close, lambda_min=0, lambda_max=1,target_tvr=0.3)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',adv20, lambda_min=0, lambda_max=1,target_tvr=0.05)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',adv20, lambda_min=0, lambda_max=1,target_tvr=0.1)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',adv20, lambda_min=0, lambda_max=1,target_tvr=0.15)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',adv20, lambda_min=0, lambda_max=1,target_tvr=0.2)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',adv20, lambda_min=0, lambda_max=1,target_tvr=0.25)')

so_alpha_list.append('ts_target_tvr_delta_limit('+expr+',adv20, lambda_min=0, lambda_max=1,target_tvr=0.3)')

print(len(so_alpha_list))

print(so_alpha_list[:3])

后续操作与一二三阶段模版相同，划分pool并进行回测即可。

注意：剪枝函数只能针对123阶因子进行减枝，如果使用模版可能需要进一步处理

推荐：将降turn操作作为“新2阶”使用，即：同时跑使用group的二阶与本文提到的操作，亦可作为“新3阶”使用，经近4个月的验证，有可实现性。

祝好运。

---

## 讨论与评论 (23)

### 评论 #1 (作者: SD17531, 时间: 1年前)

感谢分享,已经使用上了

---

### 评论 #2 (作者: SY10217, 时间: 1年前)

感谢楼主的分享，我前几天就遇到了这种情况，回头试试

---

### 评论 #3 (作者: FF56620, 时间: 1年前)

感谢分享，回头尝试一下

---

### 评论 #4 (作者: ZV96737, 时间: 1年前)

感谢楼主分享，之前自己遇到了相关问题自己手动测试修改了，没想到已经有大神分享了解决方法，手动点赞

---

### 评论 #5 (作者: MM78881, 时间: 1年前)

感谢游戏王的分享 非常不错的代码 可以直接使用的，没想到使用这个代码筛选的函数，这就很好了，之前都是手动筛选，感觉现在用这个api好多了

---

### 评论 #6 (作者: JR23144, 时间: 1年前)

感谢游戏王大佬的分享，用了这个代码，果真把我的换手率降低了，把margin 和 return 都提高了，谢谢大佬的代码，手动点赞

================================VF 1.0===========================================

---

### 评论 #7 (作者: YW93864, 时间: 1年前)

感谢游戏王大佬的分享！！！

在其他指标都过线的情况下，低margin这类alpha属于是有预测能力但不够强的alpha，而高margin的alpha是属于有预测能力且预测强的alpha。通过文章中提到的方法降低turnover，实际上也是在提升预测能力，将过去几日的alpha复合起来

---

### 评论 #8 (作者: AH18340, 时间: 1年前)

感谢游戏王大佬的分享，本文提到的操作跑完是跑二阶还是三阶呢？

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #9 (作者: SK10818, 时间: 10个月前)

感谢大哥， 一二三阶的alpha   照着这个又调了调 ，  成功提交顾问的第一个regular alpha

---

### 评论 #10 (作者: TG26429, 时间: 10个月前)

感谢游戏王大佬的分享, 好多alpha其他指标都不错，就是tvr太高，margin太低，赶快用这个代码都再优化一遍淘淘金。

---

### 评论 #11 (作者: MZ45384, 时间: 10个月前)

大佬太强了，这回具体理解了returns, turnover和margin的关系

---

### 评论 #12 (作者: SL52857, 时间: 10个月前)

感谢王大哥的分享！好不容易出来的alpha都是高turnover的，margin实在是太低了，点塔都点不愉快

---

### 评论 #13 (作者: PX70901, 时间: 8个月前)

谢谢分享

---

### 评论 #14 (作者: JL66317, 时间: 7个月前)

感谢分享，让我有了新思路

---

### 评论 #15 (作者: ML43675, 时间: 6个月前)

感谢分享，之前一直苦恼于高换手率的问题，通过文章中的降turnover方法，成功将一批原本无法提交的因子优化到了可接受范围。特别是ts_target_tvr_decay和ts_target_tvr_hump运算符实测好用，效果显著。已经将这套方法应用到日常因子挖掘流程中，效率提升明显。再次感谢大佬的无私分享！

---

### 评论 #16 (作者: HG61318, 时间: 6个月前)

感谢分享,正好学习ts_target_tvr_delta_limit怎么使用.

---

### 评论 #17 (作者: ML28213, 时间: 6个月前)

感谢分享,已经使用上了。让我有了新的回测思路

---

### 评论 #18 (作者: XG98059, 时间: 6个月前)

后期尝试试用一下。

---

### 评论 #19 (作者: YQ84572, 时间: 6个月前)

很详细的降低turnover的经验，确实拓宽了很多思路，很多高turnovers的因子也有回测调优的思路了

==================================================

感谢大佬的分享，祝大佬vf保持0.9+

==================================================

---

### 评论 #20 (作者: CC73983, 时间: 6个月前)

get_alphas修改decay后把setting值保留会不会更方便些

毕竟只是修改decay和alpha  其他都保持不变 这样获取的时候就不用关心地区和中性化等数据

---

### 评论 #21 (作者: LT33346, 时间: 3个月前)

ts_target_tvr_hump，

hump_decay，

ts_target_tvr_delta_limit 这几个没权限，先跑下试试，感谢大佬分享

---

### 评论 #22 (作者: ML38868, 时间: 3个月前)

====================================================================================

学习了，但是看的一知半解

标记一下，回头再来看

====================================================================================

---

### 评论 #23 (作者: FF65210, 时间: 16天前)

这篇降低turnover的干货满满！decay_linear和ts_mean确实能平滑信号，但要注意别把信号逻辑也平滑没了。我之前降到0.1后因子完全失效，教训深刻。按turn区间筛选再用降turn运算符处理这个思路值得借鉴。

---

