# 【提升Check Submission效率】本地计算自相关和提高check的tips，效率提高10倍以上！代码优化

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwiX5h9v8Rk6D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAjABaHR0cHM6Ly9zdXBwb3J0LndvcmxkcXVhbnRicmFpbi5jb20vaGMvemgtY24vY29tbXVuaXR5L3Bvc3RzLzI4NTI0NzQyMTc0MzU5LS0lRTYlOEYlOTAlRTUlOEQlODdDaGVjay1TdWJtaXNzaW9uJUU2JTk1JTg4JUU3JThFJTg3LSVFNiU5QyVBQyVFNSU5QyVCMCVFOCVBRSVBMSVFNyVBRSU5NyVFOCU4NyVBQSVFNyU5QiVCOCVFNSU4NSVCMyVFNSU5MiU4QyVFNiU4RiU5MCVFOSVBQiU5OGNoZWNrJUU3JTlBJTg0dGlwcy0lRTYlOTUlODglRTclOEUlODclRTYlOEYlOTAlRTklQUIlOTgxMCVFNSU4MCU4RCVFNCVCQiVBNSVFNCVCOCU4QQY7CFQ6DnNlYXJjaF9pZEkiKTMxZTUzOWE1LTg3ZDgtNDQyMS04ZmI1LTQ4OTM4MzAzN2YzYQY7CEY6CXJhbmtpDDoLbG9jYWxlSSIKemgtY24GOwhUOgpxdWVyeUkiDuiHquebuOWFswY7CFQ6EnJlc3VsdHNfY291bnRpAugD--d4c520b5999acdd31fcea44eab632050c9db6044
- **作者**: XZ23611
- **发布时间/热度**: 1年前, 得票: 95

## 帖子正文

你的点赞和鼓励是我持续分享的动力！2025.04.08 更新  每日的pnl差值应该是diff而不是pct，感谢研究小组的各位大大们！现在可以做到和平台计算0差值【Check Submission都做什么？】要提升效率首先要理解其背后的逻辑是什么！我粗略的把这个过程依次分为以下三个顺序：检查回测结果是否有FAIL，如果有FAIL这个过程会很快检查Self Correlation，这个速度就慢下来了，不过可以本地完成，后面会分享检查Prod Coorelation，无法本地完成，最耗时的步骤【理解Check Submission的限流机制】通过大量实践发现，我发现以下三个规律在一批check中，开始会很快，然后就变得异常慢，并开始出现check self/product correlation error 的超时情况所以我推测这个背后是有限流机制的，也就是说前XXX个相关性测试会是MAX Speed，单位时间内相关性的请求次数越多，就会降速。Alpha中含有FAIL的情况，不会触发限流虽然同时check的最大并发是3个，但由于限流机制的存在，并发并不会提高效率。【如何提升效率？】理解了限流机制后，那提升效率的大原则就出来了减少单位时间内的总的相关性的请求对于需要请求的要进行优先级的排序具体的思路有以下几点：第一步: 利用prune剪枝函数，对于每个字段的最好的3个进行筛选, 再进行请求。这样做的好处有两个:大量的相似alpha，如果最好的可以通过测试，可以先进行提交，这样后面的就可以不用再检查，或者可以在本地计算自相关性后排除（后面介绍方法）。如果PC相关性很高，则大概率后面的相关性也不容易降下来，那就放低优先级。第二步：进一步排除一些含有某些特定字段的alpha。当我们做了几轮第一步后发现，有些特定字段的PC都在0.85以上了，那这里可以直接从list中暂且移除掉，连剪枝后的3个也移除掉第三步：移除PnL异常的曲线，或覆盖率低的alphas经常有一些alpha的PnL是直线等无效的曲线，提前移除list，不要发送请求有一些alpha只有最近3-4年有数据，从质量优先的角度考虑，放到后面低优先级再check第四步：本地计算自相关性，排除自相关高于0.7的alphas相关性计算取值是有PnL数据的最近四年，即2018年7月16-2022年7月15日。注意这个窗口会随着平台的数据更新而动态调整先拉取已经提交过的alpha的pnl到本地，这里注意要处理risk neturalized pnl和super alpha的pnl再拉取这批待提交的alpha的pnl到本地对所有的pnl依次计算每日的差值diff，然后计算差值的最大相关性（皮尔逊相关系数），移除最大相关性高于0.7的。注意这里要处理差值是nan的情况通过以上四个步骤，可以最大化的利用我们相关性检查的MAX Speed的价值，而不是一直几百甚至上千个list去一个个的check submission【部分的实现代码】第一步：prune 函数可以直接复用即可第二步：删除关键字，这里可以有tracker和exprission两种使用方式def filter_alpha(tracker,keys,return_type):if return_type == 'tracker':def contains_keyword(sublist, keys):return any(key in " ".join(map(str, sublist)) for key in keys)tracker['next'] = [item for item in tracker['next'] if not contains_keyword(item, keys)]tracker['decay'] = [item for item in tracker['decay'] if not contains_keyword(item, keys)]return trackerelif return_type == 'expression':original_list = tracker['next'] + tracker['decay']expression_list = [item[1] for item in original_list]result = [expr for expr in expression_list if not any(key in expr for key in keys)]return result第三步：获取pnl的代码可以在Ace Library里面下载（Learn，右下角）3.1 获取 pnldef get_alpha_pnl(session, alpha_id):count = 0while True:if count>30:s = login()count = 0pnl = session.get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl")retry_after = pnl.headers.get("Retry-After")if retry_after:# print(f"Sleeping for {retry_after} seconds")sleep(float(retry_after))# sleep(10)else:# print(f"{alpha_id} PnL retrieved")count += 1return (pnl, alpha_id)3.2 批量拉取pnldef fetch_pnls(session, alpha_list):pnl_ls = []with concurrent.futures.ThreadPoolExecutor() as executor:# Create a list of tasksfutures = [executor.submit(get_alpha_pnl, session, alpha_id) for alpha_id in alpha_list]for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):result = future.result()pnl_ls.append(result)return pnl_ls3.3 转化pnl，主要用于处理super alpha和含有risk netrulized 的pnl，转化为dataframedef get_pnl_panel(session, alpha_list):alpha_pnls = fetch_pnls(session, alpha_list)pnl_df = pd.DataFrame()for pnl, alpha_id in tqdm(alpha_pnls):# 检查pnl对象是否有json方法，如果有，则调用该方法获取数据if hasattr(pnl, 'json') and callable(pnl.json):data = pnl.json()else:# 假设pnl已经是字典格式data = pnl# 检查records的列数if len(data['records'][0]) == 2:df = pd.DataFrame(data['records'], columns=['Date', alpha_id])df.set_index('Date', inplace=True)elif len(data['records'][0]) == 3:properties = data['schema']['properties']# 如果含有'risk-neutralized-pnl'，则保留这一列，并删除其他额外的列if any(prop['name'] == 'risk-neutralized-pnl' for prop in properties):records = [record[:2] for record in data['records']]df = pd.DataFrame(records, columns=['Date', alpha_id])df.set_index('Date', inplace=True)else:# 如果records的列数为3，但不包含'risk-neutralized-pnl'，则跳过这个alpha_idcontinue# 将当前alpha_id的DataFrame与总的DataFrame合并if pnl_df.empty:pnl_df = dfelse:pnl_df = pd.merge(pnl_df, df, on='Date', how='outer')return pnl_df第四步： 选取覆盖率大于0.4（这个值大家自定义即可）def check_remove_low_pnl(s,bar,ids):is_pnl_df = get_pnl_panel(s,ids)df_diff = is_pnl_df.diff(axis=0)df_processed = df_diff.apply(lambda x: x.apply(lambda y: 1 if abs(y) > 1e-10 else 0))non_zero_counts = df_processed.sum(axis=0)total_counts = df_processed.count(axis=0)percentages = non_zero_counts / total_countsids_to_keep = percentages[percentages > bar].index.tolist()ids_to_remove = [id for id in ids if id not in ids_to_keep]# 打印结果print('KEEP:{',len(ids_to_keep),'个} ',ids_to_keep)print('REMOVE:{',len(ids_to_remove),'个} ',ids_to_remove)return ids_to_keep,is_pnl_df第五步：本地计算自相关性，这个和平台结果有一定误差，但不超过2%5.1 获取已经提交alpha的pnldef get_n_os_alphas(session, total_alphas, limit=100, max_retries=10):fetched_alphas = []offset = 0retries = 0while len(fetched_alphas) < total_alphas and retries < max_retries:try:response = session.get(f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}")response.raise_for_status()alphas = response.json()["results"]fetched_alphas.extend(alphas)if len(alphas) < limit:breakoffset += limitretries = 0except requests.HTTPError as http_err:print(f"HTTP error occurred: {http_err}, retrying in {2 ** retries} seconds...")time.sleep(2 ** retries)  # 指数退避策略retries += 1  # 增加重试次数continue  # 继续下一次循环，不增加offsetexcept Exception as err:print(f"An error occurred: {err}")breakreturn fetched_alphas[:total_alphas]def get_submitted_all(s,max: int = 300):os_alpha_list = get_n_os_alphas(s, max)os_alpha_ids = [item['id'] for item in os_alpha_list]os_pnl_df = get_pnl_panel(s,os_alpha_ids)os_ret_df = os_pnl_df - os_pnl_df.ffill().shift(1)return os_ret_df5.2 计算相关性def gold_mining(s,is_ret_df, os_ret_df):is_df = is_ret_df[(pd.to_datetime(is_ret_df.index)>pd.to_datetime(is_ret_df.index).max() - pd.DateOffset(years=4)]os_df = os_ret_df[(pd.to_datetime(os_ret_df.index)>pd.to_datetime(os_ret_df.index).max() - pd.DateOffset(years=4)]is_df = is_df.replace(0, np.nan)os_df = os_df.replace(0, np.nan)gold_ids = []for col_is in is_df.columns:ret = is_df[col_is]ret = pd.concat([ret,os_df],axis=1)corr_=ret.corr()cor_max = corr_.iloc[0,1:].max()if cor_max<0.7:gold_ids.append(col_is)else:if np.isnan(cor_max):cor_max = 0set_alpha_properties(s,col_is, name= 'NO_DATA', regular_desc= cor_max, tags=['MOVE'])else:set_alpha_properties(s,col_is, name= col_is, regular_desc= cor_max, tags=['Self Correlation'])print(gold_ids)return gold_idsdef check_remove_self_correlation(s,ids,os_ret_df):is_pnl_df = get_pnl_panel(s,ids)is_ret_df = is_pnl_df - is_pnl_df.ffill().shift(1)pass_is_ids = gold_mining(s,is_ret_df, os_ret_df)return pass_is_ids希望可以提升大家的效率，不再苦等！

---

## 讨论与评论 (39)

### 评论 #1 (作者: QQ68782, 时间: 1年前)

感谢，解决了一些最近的疑惑

---

### 评论 #2 (作者: QQ68782, 时间: 1年前)

补充一点，可以把 alpha 添加到“Alpha list”，对比相似性和 pnl 曲线。alpha list 在 alphas 界面右上角，或者 alpha 列表复选框后面的按钮

---

### 评论 #3 (作者: CL49716, 时间: 1年前)

能给个例子么

---

### 评论 #4 (作者: XX42289, 时间: 1年前)

不知道为什么，精确到计算某两个self corr的时候，误差比较大。整体的时候误差会小一点

---

### 评论 #5 (作者: PL16768, 时间: 1年前)

楼主好！分享很有用！有三个问题：1.近4年pnl的皮尔逊相关系数，近4年的具体日期多久更新一次，可以给出具体的时间吗？2.代码里计算corr的方式用的好像不是pnl的绝对值，而是percent，哪个是对的？3.用了楼主的代码，很多alpha被标记为self-corralation了，但随便找了一个点了下提交，居然提上去了。。

---

### 评论 #6 (作者: CZ10093, 时间: 1年前)

PL16768握手！！！！！对于第3条，终于看到有人遇到与我类似的问题了。如果你在研究小组中，就能看到我在群里发现的case，同样两个alpha，用pandas计算出来的correlation是0.6x，而brain平台上计算出来的才0.4x。用pandas计算出来的correlation就是与brain平台上对不上。所以目前我在本地计算时卡correlation的门槛是0.8，有的alpha本地计算结果是0.75，照样能够提交，因为这个alpha在brain平台上计算出来的self corr才0.55.

---

### 评论 #7 (作者: MH33574, 时间: 1年前)

CL49716不明白你说的例子是啥，这是我现在做轮询check的逻辑 供参考while i < rounds:print("检查第", i + 1, "轮")th_tracker = get_alphas(start_date,end_date , sharp_bar, fitness_bar,region, alpha_max,usage,tags=tags )alpha_list = []alpha_list = th_tracker['next'] + th_tracker['decay']ids = [item[0] for item in alpha_list]print('初始长度： ', len(alpha_list))print('----------------------------')print('开始剪枝')ids = prune_multiple(pre_fix,alpha_list,keep_num=keep_number)print('剪枝后长度： ', len(ids))print('----------------------------')print('开始去除关键字')ids = check_filter_and_tag(keys,ids,th_tracker,tag_flag=0)print('去除关键字后长度： ', len(ids))print('----------------------------')print('开始去除去除低PnL')ids_to_keep,is_pnl_df = check_remove_low_pnl(s,bar,ids,task)print('去除低PnL后长度： ', len(ids_to_keep))print('----------------------------')print('开始去除去除高自相关性')silver_bag = check_remove_self_correlation(s,ids_to_keep,ids,is_pnl_df,os_ret_df,alpha_list)print('去除自相关性后长度： ', len(silver_bag))if len(silver_bag)<50:keep_number = 10elif len(silver_bag)<=30:keep_number = 30print('----------------------------')gold_bag = []try:gold_bag = check_submission(silver_bag, gold_bag, 0)except Exception as e:error_message = f"Error: {str(e)}"logging.error(error_message)send_notifications(s,error_message)if len(gold_bag) > 0:view_alphas(gold_bag)gold_bag_str = '\n'.join(f"{item[0]},{item[1]} "for item in gold_bag)result_str = f"Your submittable alpha: {gold_bag_str}"send_notifications(s,result_str)breakelif i == rounds or len(silver_bag)==0:result_str = "No Submittable Alphas"send_notifications(s,result_str)breaki = i+1

---

### 评论 #8 (作者: MH33574, 时间: 1年前)

XX42289这个没有具体试过，可能和pnl数据分布相关，因为用到的只是max，所以我自己测试max的时候基本误差很小，0.7的阈值也可以自己设定，只移除过大的。

---

### 评论 #9 (作者: MH33574, 时间: 1年前)

PL16768有三个问题：1.近4年pnl的皮尔逊相关系数，近4年的具体日期多久更新一次，可以给出具体的时间吗？仔细看代码  5.2里已经有了。时间更新这个是平台机制，好像半年左右。2.代码里计算corr的方式用的好像不是pnl的绝对值，而是percent，哪个是对的？你说的percentage是去除低pnl的那部分吧，那不是在算correlation，而是去移除一些不规则pnl，无效回测3.用了楼主的代码，很多alpha被标记为self-corralation了，但随便找了一个点了下提交，居然提上去了。。你要先自己调试，用本地算出来的max 和平台计算出来的去比较，多测试几个。另外这个是有误差的，你可以把本地计算判定0.7的阈值做调整  比如0.75

---

### 评论 #10 (作者: MH33574, 时间: 1年前)

CZ10093我之前遇到过这种情况是在近4年的数据不完整时候可能会出现这个情况，在我的代码里首先移除了这些alpha，如果数据表现时间过短对我是没有用的，OS容易炸

---

### 评论 #11 (作者: CZ10093, 时间: 1年前)

我在研究小组里发的那两个case，也是4年数据者是完整的。计算方法，也是按照 documentation所写的“过去4年”，也就是18～22年。计算结果照样对不上。（误差小也就算了，但是自己算是0.6x，平台算是0.4x，差太多了。）至于是不是我计算错了，反正我把两个alpha的数据都发了，让同学帮助验算，目前还没有收到指出我计算错误的反馈。

---

### 评论 #12 (作者: QQ68782, 时间: 1年前)

两个发现:1.wq的check submission得到的自相关性, 和alpha list得到的相关性, 也是不一样的2. 实测了一批数据, df.corr()算出来的相关性普遍比wq算的高, df.corr(method='kendall') 算出来的普遍比wq的低; 自己算出来的相关性大部分比较接近, 小部分偏差比较大结论来自下面的图1) alpha list的相关性0.944, check submission的相关性0.88832)对比wq check submission的相关性和df.corr(method="")三种方法算出来的相关性

---

### 评论 #13 (作者: YK42677, 时间: 1年前)

MH33574send_notifications这个方法是啥？

---

### 评论 #14 (作者: QQ68782, 时间: 1年前)

官方要不透露一下计算方式, 既能节省服务器资源, 又能提高顾问的效率, 一举多得 😄省的我们在这里猜谜语了

---

### 评论 #15 (作者: XZ23611, 时间: 1年前)

QQ68782我感觉是时间窗口导致的口径不一致的问题，checksubmission的肯定是我们需要的  因为检测需要他   只能去测试尽可能的贴近

---

### 评论 #16 (作者: XZ23611, 时间: 1年前)

QQ68782我写这个就是根据官方的来的呀   有PNL历史来的过去4年的皮尔逊相关系数

---

### 评论 #17 (作者: XZ23611, 时间: 1年前)

YK42677这个是自己写的函数，回测完了把结果发到自己的邮箱，再另一个群友发的贴子里我记得有人share过

---

### 评论 #18 (作者: HZ76661, 时间: 1年前)

分享一下我的方法：我是直接全部交给WQ网站去做check（目前开了两个线程），check通过的self corr和prod corr都写在Description里，check过的标记为绿色，报错标记为红色，点击就能很方便看见结果，目前还没有发现瓶颈，等有瓶颈了再改。如果当日提交了四个，提交其他的肯定会出现self corr 高的情况，解决方式是开脚本（一个线程）针对绿色的已提交的region check，所有压力都给WQ 不能让它歇着。

---

### 评论 #19 (作者: TT72435, 时间: 1年前)

MH33574get_alphas被魔改过吗，返回的数据包括th_tracker['next'] + th_tracker['decay']两部分

---

### 评论 #20 (作者: BA51127, 时间: 1年前)

感谢分享这么详细的提升 Check Submission 效率的方法！这些策略确实能帮助我们更好地理解和优化流程。通过剪枝、优先级排序和本地计算自相关性等步骤，能够大大提高效率，减少不必要的请求。我特别赞同减少单位时间内的相关性请求这一点，因为这可以避免限流机制带来的延迟。对于代码部分的实现，也非常实用，尤其是过滤低 PnL 和高自相关性的部分。不过，以下几点可能有助于进一步优化：误差分析：对于计算自相关性结果与平台不一致的问题，可以进一步研究误差来源。也许可以通过对比不同时间窗口或使用多种相关性计算方法来验证。动态调整策略：可以考虑根据历史数据动态调整剪枝和优先级排序的策略。例如，使用机器学习模型预测哪些 alpha 可能通过，从而优化筛选过程。自动化和监控：引入更多自动化工具和监控机制，实时跟踪哪些步骤耗时最长或失败率最高，从而针对性地优化这些环节。社区协作：鼓励更多用户分享他们的经验和数据，以便找到更普遍适用的优化方案。这些建议可以帮助进一步提升效率和准确性，同时减少手动调整的工作量。希望对你的优化过程有所帮助！

---

### 评论 #21 (作者: ZS59763, 时间: 1年前)

分享一下我的方法，我是把get_alpha进行了魔改（根据函数就可以了），给了sharpe上下限，fitness上下限，同时可以实现多个地区因子一起检验（这不难，写个循环就可以了，但是要注意chn的阈值要放到2,.07），下边是我之前做的一版代码供参考：def get_submitable_alphas(start_date, end_date, sharpe_th, fitness_th,turn_over, region, alpha_num, usage):s = login()output = []# 3E large 3C lesssharpe_th1=sharpe_thcount = 0for re in region:if re=='CHN':sharpe_th=max(sharpe_th,2.1)else:sharpe_th=sharpe_th1for i in range(0, alpha_num, 100):print(re,i)url_e = "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)\+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2024-" + start_date  \+ "T00:00:00-04:00&dateCreated%3C2024-" + end_date \+ "T00:00:00-04:00&is.fitness%3E" + str(fitness_th) + "&is.sharpe%3E" \+ str(sharpe_th) + "&settings.region=" + re + "&order=-is.sharpe&hidden=false&type!=SUPER"url_c = "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"%(i)\+ "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2024-" + start_date  \+ "T00:00:00-04:00&dateCreated%3C2024-" + end_date \+ "T00:00:00-04:00&is.fitness%3C-" + str(fitness_th) + "&is.sharpe%3C-" \+ str(sharpe_th) + "&settings.region=" + re + "&order=is.sharpe&hidden=false&type!=SUPER"urls = [url_e]if usage != "submit":urls.append(url_c)for url in urls:response = s.get(url)#print(response.json())try:alpha_list = response.json()["results"]#print(response.json())for j in range(len(alpha_list)):alpha_id = alpha_list[j]["id"]name = alpha_list[j]["name"]dateCreated = alpha_list[j]["dateCreated"]sharpe = alpha_list[j]["is"]["sharpe"]fitness = alpha_list[j]["is"]["fitness"]turnover = alpha_list[j]["is"]["turnover"]margin = alpha_list[j]["is"]["margin"]longCount = alpha_list[j]["is"]["longCount"]shortCount = alpha_list[j]["is"]["shortCount"]decay = alpha_list[j]["settings"]["decay"]exp = alpha_list[j]['regular']['code']count += 1if (longCount + shortCount) > 50 and turnover<turn_over and 'eeps_nxt_yr' not in exp:if sharpe < -sharpe_th:exp = "-%s"%exprec = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]output.append(rec)except:print("%d finished re-login"%i)s = login()sleep(2)print("count: %d"%count)return output

---

### 评论 #22 (作者: KH94146, 时间: 1年前)

ZS59763手动点赞！

---

### 评论 #23 (作者: XX42289, 时间: 1年前)

本地计算的corr只能用来自己做分析，不能用来判断平台上的corr。pandas里的三种算法和官方只能说接近，但是没有一种算法是完全一致的，可能是因为我们获取到的数据不全

---

### 评论 #24 (作者: LL87164, 时间: 1年前)

已提交的PnL每次都重新获取一次吗？可以按时间段获取最新的吗？或按已获取过的alpha_id列表进行排除获取最新的？大家有什么经验或建议。

---

### 评论 #25 (作者: XZ23611, 时间: 1年前)

LL87164我看最近有一个同学给出了增量获取的方案，论坛里找一下

---

### 评论 #26 (作者: XZ23611, 时间: 1年前)

https://support.worldquantbrain.com/hc/en-us/community/posts/30683782083991-%E6%9C%AC%E5%9C%B0Self-Correlation%E6%A3%80%E6%9F%A5%E7%9A%84%E5%AE%9E%E7%8E%B0%E4%B8%8E%E6%94%B9%E8%BF%9B-%E6%9C%AC%E5%9C%B0%E5%AD%98%E5%82%A8-%E4%BB%85%E5%A2%9E%E9%87%8F%E6%8B%89%E5%8F%96%E8%BF%9B%E4%B8%80%E6%AD%A5%E6%8F%90%E5%8D%87%E6%95%88%E7%8E%87-%E9%80%82%E7%94%A8Super-Alpha

---

### 评论 #27 (作者: YX50005, 时间: 1年前)

properties = data['schema']['properties']# 如果含有'risk-neutralized-pnl'，则保留这一列，并删除其他额外的列if any(prop['name'] == 'risk-neutralized-pnl' for prop in properties):records = [record[:2] for record in data['records']]这段代码实际做的事情和注释是不是不太一样，record[:2]保留下来的还是pnl，不是risk-neutralized-pnl？

---

### 评论 #28 (作者: XZ23611, 时间: 1年前)

YX50005这个代码后来更新了  新出了那个inevitable pnl以后这套逻辑需要迭代一下，不用做那么多判断，直接只取第二列即可，就是正常的pnl  其余的pnl都是后面的列。同样适用于Super Alpha

---

### 评论 #29 (作者: HC66282, 时间: 1年前)

谢谢楼主分享的代码。今天测试了一下，跟平台的结果可以0误差了。

---

### 评论 #30 (作者: JX14975, 时间: 1年前)

考虑到实际上 self correlation 的检查规则还有一条 sharpe is better 10% and more ，我目前在get_alpha_pnl时修改了返回参数为 (pnl, (alpha_id,sharpe))。 这样在gold_mining 函数中使用mask =(ret.columns.get_level_values(1) *1.1 > (col_is[1])) | (ret.columns.get_level_values(0) == col_is[0])ret = ret.loc[:,mask]来去除sharpe太低的alpha不计算自相关。这么做的缺点是csv文件读存的过程中无法保留列名的元组性质，读取时需要强制转换一遍列名

---

### 评论 #31 (作者: KH94146, 时间: 1年前)

JX14975严谨！ 据很多顾问反馈如果PC 大于0.7的情况   收益都不会很好

---

### 评论 #32 (作者: SW66069, 时间: 1年前)

很有用，check快了很多

---

### 评论 #33 (作者: BJ10003, 时间: 1年前)

感谢帖主的分享，感觉能与另一位帖主分享的alpha下载到本地计算self_correlation的方式相互印证，更快的得到计算结果！

---

### 评论 #34 (作者: SW66069, 时间: 1年前)

谢谢楼主，帮助很多

---

### 评论 #35 (作者: AH18340, 时间: 1年前)

感谢大佬分享，收获颇多，已经本地实现的自相关性检测

---

### 评论 #36 (作者: HW85064, 时间: 10个月前)

十分感谢楼主分享，我有两个问题想要咨询：1.在get_pnl_panel方法中，为什么要检验record的列数呢？2.在本地测试时，我的record列数全都是4，这可能是什么情况？

---

### 评论 #37 (作者: HW54322, 时间: 9个月前)

提升了check的效率

---

### 评论 #38 (作者: YS42224, 时间: 9个月前)

谢谢楼主代码

---

### 评论 #39 (作者: JL66317, 时间: 9个月前)

感谢大佬分享的文章，收益很深

---

