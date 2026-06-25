# 本地Self Correlation检查的实现与改进（本地存储，仅增量拉取进一步提升效率，适用Super Alpha）代码优化

- **链接**: https://support.worldquantbrain.com/hc/en-us/community/posts/30683782083991
- **作者**: MH33574
- **发布时间/热度**: 1 year ago, 得票: 31

## 帖子正文

您的点赞留言是我持续分享的最大动力！您的点赞留言是我持续分享的最大动力！您的点赞留言是我持续分享的最大动力！索引文章鸣谢：【提升Check Submission效率】一些可以提升Check Submission的Tips，效率提高10倍以上！【新人避坑】关于Alpha本地计算 self-correlation 结果偏差巨大的解决方案一、什么是Self Correlation？计算原理Self correlationMaximum Pearson correlation coefficient from comparing a given Alpha to all other Alphas submitted by the same user.Checks the correlation of your Alpha with the rest of your OS Alphas. If an Alpha is uncorrelated, then it passes self correlation test. Otherwise, only one out of a group of highly correlated Alphas passes the test. SeeFAQfor details.常见误区：1. 以为是表达式的相关性，其实是pnl来判断的2. 直接用pnl计算，其实是用每日的变化来判断的3. 计算周期，当前pnl时间的最近四年即：2019年1月20-2023年1月21日二、如何本地计算？ 实现思路1. 本地存储已经提交过的alpha pnl到一个csv文件中，避免重复拉取，在后期提交几百个以后会很慢。2. 获取所有已提交alpha的alpha id列表，比对本地csv文件中，定位近期增量alpha id3. 拉取增量alpha id的pnl（daily 变化的），更新本地CSV4. 将要检查的pnl 矩阵与本地最新的矩阵进行相关性系数计算，由于存在一定误差，可以稍微放松至0.715. 超过0.71的进行打标排除。6. 该方法也适用于Super Alpha三、实现代码* 当pnl实际变化少于4年时（即在19年之前都是平的）算的可能不准，但这种alpha我都已经提前剔除掉了def get_submitted_all(s,max: int = 300,addtional_id = [], (用于包含一些准备提交但尚未提交的alphas）type = 'REGULAR',mode = 'ADD'):os_alpha_list = get_n_os_alphas(s, max,type = type)os_alpha_ids = [item['id'] for item in os_alpha_list]if mode == 'ALL':os_alpha_ids.extend(addtional_id)os_pnl_df = get_pnl_panel(s,os_alpha_ids)os_ret_df = os_pnl_df.pct_change(axis=0)else:#读取历史已保存pnlif type == 'REGULAR':file_name_MH = f'latest_regular_pnl_MH.csv'else:file_name_MH = f'latest_super_pnl_MH.csv'#这里只是一个拼装存储路径的函数，根据你自己的情况修改file_path_1 = get_file_path(file_name_MH,function_code=1)history_ret_df= pd.read_csv(file_path_1,index_col='Date')add_ids = [id for id in os_alpha_ids if id not in history_ret_df.columns]if(len(add_ids)>0):add_pnl_df = get_pnl_panel(s,add_ids)add_ret_df = add_pnl_df.pct_change(axis=0)os_ret_df = pd.concat([history_ret_df, add_ret_df], axis=1, ignore_index=False)#更新csvos_ret_df.to_csv(file_path_1, index=True, sep=',', encoding='utf-8')print(' '.join(add_ids) + ' has added')print(f'This account has: {len(update_ret_df.columns)}')else:os_ret_df = history_ret_dfprint('no new ID added')return os_ret_df-----------------------------------------------------------------def get_n_os_alphas(session, total_alphas, limit=100, max_retries=10,type='REGULAR'):fetched_alphas = []offset = 0retries = 0while len(fetched_alphas) < total_alphas and retries < max_retries:try:response = session.get(f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}")response.raise_for_status()alphas = response.json()["results"]regular_items = [item for item in alphas if item.get('type') == 'REGULAR']super_items = [item for item in alphas if item.get('type') == 'SUPER']if type == 'REGULAR':fetched_alphas.extend(regular_items)elif type == 'SUPER':fetched_alphas.extend(super_items)if len(alphas) < limit:breakoffset += limitretries = 0except requests.HTTPError as http_err:print(f"HTTP error occurred: {http_err}, retrying in {2 ** retries} seconds...")time.sleep(2 ** retries)  # 指数退避策略retries += 1  # 增加重试次数continue  # 继续下一次循环，不增加offsetexcept Exception as err:print(f"An error occurred: {err}")breakreturn fetched_alphas[:total_alphas]------------------------------------------------------------def fetch_pnls(session, alpha_list):pnl_ls = []with concurrent.futures.ThreadPoolExecutor() as executor:# Create a list of tasksfutures = [executor.submit(get_alpha_pnl, session, alpha_id) for alpha_id in alpha_list]for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):result = future.result()pnl_ls.append(result)return pnl_ls-----------------------------------------------------------------def get_pnl_panel(session, alpha_list):alpha_pnls = fetch_pnls(session, alpha_list)pnl_df = pd.DataFrame()for pnl, alpha_id in tqdm(alpha_pnls):# 检查pnl对象是否有json方法，如果有，则调用该方法获取数据if hasattr(pnl, 'json') and callable(pnl.json):data = pnl.json()else:# 假设pnl已经是字典格式data = pnlrecords = [record[:2] for record in data['records']]df = pd.DataFrame(records, columns=['Date', alpha_id])df.set_index('Date', inplace=True)# 将当前alpha_id的DataFrame与总的DataFrame合并if pnl_df.empty:pnl_df = dfelse:pnl_df = pd.merge(pnl_df, df, on='Date', how='outer')pnl_df = pnl_df.sort_index()return pnl_df------------------------------------------------------------------def get_alpha_pnl(session, alpha_id):count = 0while True:if count>30:s = login()count = 0pnl = session.get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl")retry_after = pnl.headers.get("Retry-After")if retry_after:# print(f"Sleeping for {retry_after} seconds")sleep(float(retry_after))# sleep(10)else:# print(f"{alpha_id} PnL retrieved")count += 1return (pnl, alpha_id)----------------------------------------------------------------def gold_mining(s,is_ret_df, os_ret_df,type):is_df = is_ret_df[(pd.to_datetime(is_ret_df.index)>pd.to_datetime('2019-01-20'))&(pd.to_datetime(is_ret_df.index)<pd.to_datetime('2023-01-21'))]os_df = os_ret_df[(pd.to_datetime(os_ret_df.index)>pd.to_datetime('2019-01-20'))&(pd.to_datetime(os_ret_df.index)<pd.to_datetime('2023-01-21'))]gold_ids = []for col_is in is_df.columns:ret = is_df[col_is]ret = pd.concat([ret,os_df],axis=1)corr_=ret.corr()cor_max = corr_.iloc[0,1:].max()if cor_max<0.71:gold_ids.append(col_is)else:if np.isnan(cor_max):cor_max = 0set_alpha_properties(s,col_is, name= 'NO_DATA', regular_desc= cor_max, tags=['MOVE'])else:if type == 'REGULAR':set_alpha_properties(s,col_is, name= col_is, regular_desc= cor_max, tags=['Self Correlation'])else:set_alpha_properties(s,col_is, name= cor_max, selection_desc= cor_max, tags=['Self Correlation'])print(gold_ids)return gold_ids您的点赞留言是我持续分享的最大动力！您的点赞留言是我持续分享的最大动力！您的点赞留言是我持续分享的最大动力！

---

## 讨论与评论 (17)

### 评论 #1 (作者: KZ79256, 时间: 1 year ago)

self-corr计算的是同一region的结果，目前的代码比较的是所有region的，可能还需要在加上一个判断region的。--------------------------------------------------------------------------------------------------------------Passion

---

### 评论 #2 (作者: KZ79256, 时间: 1 year ago)

另外，同一region的SA和RA之间也是要检查相关性的。看代码好像只是在RA之间或者SA之间检查，由于get_submitted_all只能返回一种类型的alpha--------------------------------------------------------------------------------------------------------------Passion

---

### 评论 #3 (作者: LL87164, 时间: 1 year ago)

当pnl实际变化少于4年时（即在19年之前都是平的）算的可能不准但这种alpha我都已经提前剔除掉了这种平的如何筛选出来的，通过页面查看还是代码判断？

---

### 评论 #4 (作者: MH33574, 时间: 1 year ago)

KZ79256确实，因为是本地计算还是挺快的就没有做进一步的区分。SA 一般我都要比较高的sharp fitness 筛选，和regular 遇到相关性的几率几乎没有

---

### 评论 #5 (作者: MH33574, 时间: 1 year ago)

LL87164参考我开头索引的check submission的那个帖子里已经有提供了

---

### 评论 #6 (作者: LY40948, 时间: 1 year ago)

您好！我想问一下您在拉取pnl时有没有出现过：未提交的alpha拉取的pnl，与已提交的alpha拉取的pnl，它们之间的时间序列对不上，未提交的会有若干天是没有pnl数据的。这导致我在使用代码计算self corr时还是会出现非常大的误差（>0.2）

---

### 评论 #7 (作者: KZ79256, 时间: 1 year ago)

MH33574因为是本地计算还是挺快的就没有做进一步的区分个人感觉还是需要区分一下，因为其他区域的alpha的pnl会影响本区域的self-corr，可能导致过高的错估self-corr。并不是快不快的问题

---

### 评论 #8 (作者: KM27775, 时间: 1 year ago)

if cor_max<0.71:gold_ids.append(col_is)这边的代码可以优化一下，分不同的区间，给alpha打不同的tag。譬如self01，表示self correction小于0.1譬如self02，表示self correction大于0.1，小于0.2这样提交alpha的时候，同等条件，优先选择self01的alpha提交。

---

### 评论 #9 (作者: ZP42727, 时间: 1 year ago)

太赞了！ 本来说要自己写一个， 突然给开了顾问论坛权限，那就谢谢啦。

---

### 评论 #10 (作者: DA64370, 时间: 1 year ago)

不知道为什么我本地计算的一直与平台有很大差距，有的差0.5，有的差0.1，跟平台计算的几乎没有关联

---

### 评论 #11 (作者: HJ33503, 时间: 1 year ago)

selfcorrelation在本地计算确实会更快，但是同样有一个问题，有时候会面临大量表现类似的alpha，提交一个一堆alpha不能提交的情况，很多时候就是这些alpha占用了大量check时间，如果能优化最好，不知道大家有什么好的方法，同时本地计算selfcorrelation，数量上来以后其实也很慢，有时候先提交几个同一dataset下面的alpha后续check反而比较快，因为会prodcorrelation的检测是最费时间的

---

### 评论 #12 (作者: MH33574, 时间: 1 year ago)

KM27775好主意！通常也不用分的太细  一般0.5以下的对SA的增益就很不错了

---

### 评论 #13 (作者: MH33574, 时间: 1 year ago)

KZ79256嗯  是可以在本地做一个字典，每次只计算该region下的  应该是最好的解决方案。哪天有时间优化一下。跨区域alpha导致pnl的相似的我觉得是个极小概率事件

---

### 评论 #14 (作者: SX83613, 时间: 1 year ago)

MH335741. 以为是表达式的相关性，其实是pnl来判断的2. 直接用pnl计算，其实是用每日的变化来判断的3. 计算周期，当前pnl时间的最近四年即：2019年1月20-2023年1月21日请问这三条信息，是如何获知的呢？网站上有没有明确说明的地方？尽管第2条说是“用每日的变化来判断的”，但gold_mining这个方法里，不还是直接用了pnl计算corr吗？

---

### 评论 #15 (作者: DZ31817, 时间: 1 year ago)

感谢分享。一个发现：我一开始使用变化的百分比来计算相关性，误差很大，甚至达到0.2左右。后来经过和群友讨论和实际测试，发现只使用每天的变化差值本身，而不是变化百分比来计算相关性，能够得到很精准的结果。供大家参考。

---

### 评论 #16 (作者: ZP42727, 时间: 1 year ago)

我测试也是误差比较大， 是不是日期没有对上。

---

### 评论 #17 (作者: TL42173, 时间: 1 year ago)

感谢分享

---

