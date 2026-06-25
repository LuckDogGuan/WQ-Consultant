# [SuperAlpha] Not Own Selection的一二三....N阶分层框架Alpha Template

- **链接**: https://support.worldquantbrain.com/hc/en-us/community/posts/35377811169175--SuperAlpha-Not-Own-Selection%E7%9A%84%E4%B8%80%E4%BA%8C%E4%B8%89-N%E9%98%B6%E5%88%86%E5%B1%82%E6%A1%86%E6%9E%B6
- **作者**: KZ79256
- **发布时间/热度**: 8 months ago, 得票: 99

## 帖子正文

作为一个GM, 有大量的not own alpha可用, 但是之前的我的框架回测的alpha由于selection比较固定, 导致有大量的自相关性, 且出货率不高游戏王的SELECTION框架-v2的选择感觉又太手工, 没法大规模回测, 而且分层思想感觉没有贯彻到底(xixi)这时我想起了weijie老师经常说起的分层思想, 因此这里我借助分层思想做了一个Selection的框架.核心思想:通过Datasets和turnover将我可以使用的alpha按30个一组分层, 之后按照一组(一阶), 两组(二阶), 三组(三阶),..., 进行回测. combo统一使用combo_a(alpha), 其他的设置也都是固定的一个, 没有遍历, 因为本身selection的可遍历空间已经足够大了搜索空间: 无穷无尽, 我现在通过随机数随机找了200301个二阶的准备回测(只有selection的改变)效果:在EUR区域通过二阶回测, 回测37428个, 目前fit>5的有29243个, 因子之间的相关性也相对较低.做法: 这里就不放完整的代码, 有兴趣的自己开发第一步, 对可用的alpha进行分层标识在这里我的想法是通过alpha所属的Datasets和turnover将我可以使用的alpha按30个一组分层, 然后记录下来相关selection, 具体形式大致为 ((in(datasets, "xxxx")) && (turnover>=xxxx) && (turnover<xxxx))我是将分层结果保存在数据库, 大致结构如下具体做法, 是通过run selection提供的按钮从turnover从小到大获取30个因子. 代码如下def get_select_alphas(select_expr):# API 端点 URLurl = "https://api.worldquantbrain.com/simulations/super-selection"# 请求参数params = {"limit": 100,"offset": 0,"status": "ACTIVE","settings.delay": cfg.delay,"settings.instrumentType": "EQUITY","settings.region": cfg.region,"order": "-selected.weight","hidden": "false","selection": f'({select_expr}) * (1-turnover)',"selectionHandling": "POSITIVE","selectionLimit": 100}full_url = f"{url}?{urlencode(params)}"response = wqapi.wait_get(full_url)response = response.json()return responsedef get_layering_data(item_dataset):select_dataset = f'in(datasets, "{item_dataset}")'turnover_lower = -np.infturnover_upper = np.infselect_layering_data = []while True:turnover_upper = np.infselect_turnover_lower = '' if turnover_lower == -np.inf else f'turnover>={turnover_lower}'select_turnover_upper = '' if turnover_upper == np.inf else f'turnover<{turnover_upper}select_layering = ' && '.join([item for item in [select_dataset, select_turnover_lower, select_turnover_upper] if item])select_expr = ' && '.join([f'({item})' for item in [select_base, select_layering] if item])response = get_select_alphas(select_expr)if response['count'] == 0:breakresults = pd.DataFrame(response['results'])results = pd.concat([pd.json_normalize(results['selected']), pd.json_normalize(results['is'])], axis=1)# print(f"Dataset: {item_dataset}, Count: {results.shape[0]}, Turnover Lower: {turnover_lower}, Turnover Upper: {turnover_upper}")if results.shape[0] <= 45:select_layering_data.append((select_dataset, round(turnover_lower,5), np.inf, results.shape[0]))breakwhile True:turnover_upper = round(results.iloc[29].turnover+0.00005,5)select_count = results[results.turnover < turnover_upper].shape[0]select_layering_data.append((select_dataset, round(turnover_lower,5), round(turnover_upper,5), select_count))results = results[results.turnover >= turnover_upper].copy().reset_index(drop=True)turnover_lower = turnover_upperif (response['count']< 100) and (results.shape[0] <= 45):select_layering_data.append((select_dataset, round(turnover_lower,5), np.inf, results.shape[0]))breakif results.shape[0] < 35:breakif response['count'] < 100:breakreturn select_layering_data# futures = []# select_layering_data = []# task_list = datasets.copy()# task_list = sorted(task_list)# pbar = tqdm(total=len(task_list), desc="Processing tasks")# with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:#     while task_list or futures:#         while task_list and len(futures) < MAX_WORKERS:#             item_dataset = task_list.pop(0)#             futures.append(executor.submit(get_layering_data, item_dataset))#         done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)#         for d in done:#             futures.remove(d)#             item_res = d.result()#             doc_id = f"{cfg.region}_{cfg.delay}"#             doc = collection_layering.find_one({'id': doc_id}, {'_id': 0, 'values.date': 1})#             max_date = max(v['date'] for v in doc['values'])#             collection_layering.update_one(#                 {'id': doc_id},#                 {#                     '$push': {'values.$[v].values': {'$each': item_res}},#                     '$set': {'datasets_num': len(task_list)+len(futures), 'time': datetime.now().strftime('%Y%m%d-%H%M%S')}#                 },#                 array_filters=[{'v.date': max_date}]#             )#             # select_layering_data.extend(d.result())#             pbar.update(1)#             # if total_success % 20 == 0 or total_success == len(task_list):#             #     # cfg.log_message('info', f"并发进度: {total_success}/{len(task_list)}")#             #     print(f"并发进度: {total_success}/{len(task_list)}")# pbar.close()对于USA或者EUR这样的大区, 大概1-2h就可以遍历完.当然我用的是turnover来辅助分层, 你也可以用long或short来分层.第二步, 组合因子因为我们已经得到所有alpha的分层情况了, 之后我们可以选取其中一个, 或者两两组合, 或者随机选三个组合, 以此类推. 这样在选择因子里各个类型的因子的个数大致是相等的目前我是选择其中两个进行组合的, 像EUR区域的话因子通过分层大概是3523组, 排列组合C(3523, 2)就在6,304,003个待回测的因子的量级了,  你可以从中去挑选一些保持大规模回测, 基本上是测不完的大致代码如下from itertools import combinations, productdef combination(n, k):# 确保k不大于n，且为非负整数if k < 0 or k > n:return 0# 优化计算，取较小的k值if k > n - k:k = n - kresult = 1for i in range(k):result = result * (n - i) // (i + 1)return resultdef get_layering_expr(item_data):select_dataset, turnover_lower, turnover_upper = item_data.dataset, item_data.turnover_lower, item_data.turnover_upper# select_dataset = f'in(datasets, "{item_dataset}")'select_turnover_lower = '' if turnover_lower == -np.inf else f'turnover>={turnover_lower}'select_turnover_upper = '' if turnover_upper == np.inf else f'turnover<{turnover_upper}'layering_expr = ' && '.join([f"({item})" for item in [select_dataset, select_turnover_lower, select_turnover_upper] if item])return layering_exprdef combine_expr_k(df, k=2, subset_size=10):get_subset_expr = lambda x: random.sample(x, min(len(x), subset_size))# 按 dataset 分组grouped = df.groupby("dataset")["expr"].apply(list).to_dict()datasets = list(grouped.keys())results = []for ds_combo in combinations(datasets, k):# # 每个 dataset 取一条，做笛卡尔积# for pick in product(*(get_subset_expr(grouped[ds]) for ds in ds_combo)):#     results.append(" || ".join(f"({e})" for e in pick))full_product = list(product(*(grouped[ds] for ds in ds_combo)))subset_product = list(product(*(get_subset_expr(grouped[ds]) for ds in ds_combo)))k = len(subset_product)# 从完整笛卡尔积中随机采样 k 个sampled_product = random.sample(full_product, min(k, len(full_product)))results.extend([" || ".join(f"({e})" for e in pick) for pick in sampled_product])return resultsdoc_id = f"{cfg.region}_{cfg.delay}"doc = collection_layering.find_one({'id': doc_id}, {'_id': 0, 'values': 1,})['values']max_date = max(v['date'] for v in doc)select_layering_data = [v for v in doc if v['date'] == max_date][0]['values']select_layering_data = pd.DataFrame(select_layering_data, columns=['dataset', 'turnover_lower', 'turnover_upper', 'count'])select_layering_data = select_layering_data.drop_duplicates()select_layering_data['expr'] = select_layering_data.apply(get_layering_expr, axis=1)select_layering_data = select_layering_data.query('count>=15').reset_index(drop=True)layering_expr = combine_expr_k(select_layering_data, k=2, subset_size=10)layering_expr = [f"({item}) && ({select_base})" for item in layering_expr]这里展示最近一次提交的因子(((in(datasets, "pv1")) && (turnover>=0.18545) && (turnover<0.18615)) || ((in(datasets, "pv96")) && (turnover>=0.05095) && (turnover<0.06815))) && base_selection这里的base_selection是一些提前筛选的条件, 具体的可参考游戏王的帖子进行相应的改动, 例如prod_correlation, datafield_count, operator_count等第三步, 大规模回测+Check仅供参考，祝各位select愉快：）

---

## 讨论与评论 (16)

### 评论 #1 (作者: CC85858, 时间: 8 months ago)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------好厉害，正在想怎么实现无穷无尽的selection。不知道平台有没有可以实现“随机选择”的功能

---

### 评论 #2 (作者: YH25030, 时间: 8 months ago)

谢谢大佬分享这个框架。按照这个思路分层，三五的Not Own SA岂不是要多得交不完了！

---

### 评论 #3 (作者: LG37773, 时间: 8 months ago)

正在准备优化一下SA的回测，就看到了华子哥的帖子。华子哥是我们中国区顾问的榜样，每次Genius评级都排在第一位。也感谢华子哥各种代码的分享。  点赞

---

### 评论 #4 (作者: DS48533, 时间: 8 months ago)

宝藏idea，分层应该不止可以通过Datasets和turnover，然后数量多的话，可以稍微把每层的范围放大的感觉。学到了，找机会复现下～感谢分享

---

### 评论 #5 (作者: SJ65808, 时间: 8 months ago)

decay、datafield_count、operator_count  分层也不错======================================================================================================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #6 (作者: LA79055, 时间: 8 months ago)

感谢游戏王大佬分享的idea。这篇分享思路很新颖，进一步的细分有助于减小 PC。通过datasets与turnover等指标的进一步分层能更系统地发现可选择的 alpha 数量，便于规模化检验。

---

### 评论 #7 (作者: LL49894, 时间: 8 months ago)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------学习了，感谢大佬分享

---

### 评论 #8 (作者: CW99271, 时间: 7 months ago)

EUR地区回测的效果确实惊人，fit>5的比例这么高。不过有个小疑问想请教一下华子哥：在组合不同层的因子时，有没有考虑过不同datasets之间的风格互补性？比如某些dataset偏向动量，某些偏向价值，如果能在分层基础上再加入风格标签的约束，这样会不会让组合效果更稳定？另外在实际回测中，这些通过分层随机组合的selection，在不同市场下的表现一致性如何？有没有出现某些组合在特定时期突然失效的情况？

---

### 评论 #9 (作者: AH18340, 时间: 7 months ago)

有幸现在拜读了华子哥的贴子，553我来了=============================================================================The best time to plant a tree is 20 years ago. The second-best time is now.=============================================================================

---

### 评论 #10 (作者: MZ45384, 时间: 7 months ago)

Wow！Endless selection expression。华子哥太有实力菈，具体数据集（pv1, analyst35等）&& 分层（turnover， short count， long count等），不过要在这么具体的数据集中select还能批量成功，看来只适用于not(own)了。（悲哭）======================================================================================知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%# sys.setrecursionlimit(α∞)# PnL = ∑(Robustness * Creativity)#无限探索、鲁棒性优先，创新性增值======================================================================================

---

### 评论 #11 (作者: XC66172, 时间: 6 months ago)

感谢华子哥的分享，分层的思想很重要，以往我只是简单的选datacatogories, 原来还可以datasets * turnover这样去选更独特的因子。有空去改一下自己的框架。==================================================FIGHTING LABUBU!~=================================================

---

### 评论 #12 (作者: PZ64174, 时间: 6 months ago)

感谢华子哥分享！最近因为回测限制，停了随机sa回测，来论坛找找sa手搓的经验贴，游戏王跟华子哥提出的分层给了我很大的启发！存在无限的可能！今天就去试一试！====================================================================一年一个台阶，一步一个脚印====================================================================

---

### 评论 #13 (作者: LG87838, 时间: 4 months ago)

从研究小组找到线索来到了这篇帖子，论坛里的宝藏太多了。学不完，真的学不完。。。感谢华子哥分享！虽然VF低到吃低保，SUPER ALPHA还是需要持续提交的。游戏王、华子哥...各位大佬提供的思路太有启发了。====================================================================慢慢来，相信时间的力量。====================================================================

---

### 评论 #14 (作者: JJ69164, 时间: 3 months ago)

2026年3月13日 我的量化进行了300天了，可我感觉还不会的有很多很多哦...===================================================================================================================我写评论的日子===================================今天，得到群里大佬们指引说有 super Alpha 的帖子可以学习了，我加速度赶紧过来观摩学习一下咯，大佬的货真多，厉害了！！！前1个月交的 super Alpha 都fitness大于2都难，交的我都想绝望了，3月份想努力努力开始交几个好一点的 super Alpha 试试，有跟我一样渴望想出高fitness的 super Alpha  的同学吗？一起交流，一起成长，从学习本帖开始吧~大佬，看完后有个问题请教下，如果第一步得到数据下面这两个有其一或两个都有的话是不是就相当于没有用上turnover来辅助分层了呢？也就是说是不是没有意义，构建  super Alpha 时需要舍弃掉呢？？？turnover_lower = -np.infturnover_upper = np.inf===================================================================================================================祝点赞的大佬高VF=================================

---

### 评论 #15 (作者: LK39823, 时间: 3 months ago)

感谢华子哥分享，我之前还一直不是特别理解分层思想，读到这篇帖子，才明白具体操作方法，，很有启发，我的own做出来的pc普遍大于0.6，没出过三五的，回去我也试试这个===================================================================================一点点进步，相信我也能日均50刀===================================================================================加油==================================================================================

---

### 评论 #16 (作者: SJ65808, 时间: 3 months ago)

又看了一遍，很有收获，华子哥真乃国区之光~~======================================================================================================纸上得来终觉浅，绝知此事要躬行======================================

---

