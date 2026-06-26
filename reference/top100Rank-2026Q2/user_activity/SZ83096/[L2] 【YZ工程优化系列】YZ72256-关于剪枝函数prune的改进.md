# 【YZ工程优化系列】YZ72256-关于剪枝函数prune的改进

- **链接**: [L2] 【YZ工程优化系列】YZ72256-关于剪枝函数prune的改进.md
- **作者**: YZ72256
- **发布时间/热度**: 1 year ago, 得票: 11

## 帖子正文

本文对剪枝函数进行了优化，使其可以针对不同的字段前缀进行剪枝，从而可以实现不同类型数据的同时剪枝。 **如果本文对你有帮助欢迎点赞，如果其他想法也欢迎在评论区留言。**

同一个数据字段得到的不同因子的表现大概率是相似的，对他们都进行二阶甚至三阶的回测性价比很低。 **剪枝函数可以减少同字段因子的数量，从而提高高阶因子的多样性** 。

初始官方提供的prune函数只能提供单类型数据字段的剪枝（参数prefix只能提供一个字段前缀），而如果一种前缀类型字段进行集中回测会导致因子产出集中在一个pyramid中；且需要手动调整prune参数设置，难以做到多类型全自动回测，从而降低因子的广度，提高了手动操作的时间成本。

针对上述问题，我对初始prune函数进行了优化，使其可以对不同prefix前缀的字段都进行剪枝，同时对于超过保留数目的字段因子进行了随机保留，期望 **减少同表现因子扎堆的现象** 。

## ***1. 因子前缀的获取***

首先，我们需要得到可能多的因子前缀，我遍历了gold可以得到的所有matrix和vector数据字段。

```
s = login()region_universe_dict = {    'USA': ['TOP3000', 'TOP1000', 'TOP500', 'TOP200', 'ILLIQUID_MINVOL1M', 'TOPSP500'],    'GLB': ['TOP3000', 'MINVOL1M'],    'EUR': ['TOP1200', 'TOP800', 'TOP400', 'ILLIQUID_MINVOL1M'],    'ASI': ['MINVOL1M', 'ILLIQUID_MINVOL1M'],}# field_name = []for region in region_universe_dict.keys():    for universe in region_universe_dict[region]:        if region in ['GLB', 'ASI']:            delay_list = [1]        else:            delay_list = [0, 1]        for delay in delay_list:            # 得到所有数据集信息            sets = get_datasets(s, region=region, universe=universe, delay=delay)            if len(sets) > 0:                # 得到所有字段信息                for dataset in sets['id']:                    datafield = get_datafields(s, dataset_id = dataset, region=region, universe=universe, delay=delay)                    if len(datafield) > 0:                        field_name += datafield[datafield['type'] == 'MATRIX']['id'].to_list()                        field_name += datafield[datafield['type'] == 'VECTOR']['id'].to_list()                    print(f'region = {region}, universe = {universe}, delay = {delay}, dataset_id = {dataset}, len(df) = {len(datafield)}, len(f) = {len(field_name)}')            else:                print(f'region = {region}, universe = {universe}, delay = {delay}, no dataset')# 去重 50138field_name = list(set(field_name))
```

进行去重处理后人工提取出多个字段前缀（要求前缀对应的数据数量大于3个），其中有9个字段前缀数量超过300个，以及有56个无前缀字段。

```
# 所有前缀（基于20250117时候的gold所能拥有的数据字段）forename = ['pv', 'fnd', 'mdl', 'oth', 'anl', 'ern', 'insd', 'imb',           'inst', 'mcr', 'news', 'sta', 'rsk', 'scl', 'opt', 'nws',           'fn', 'est', 'implied', 'mws', 'rp', 'act', 'shrt', 'pcr',           'historical', 'ptg', 'rel', 'se', 'quick', 'put', 'forward',           'rd', 'correlation', 'call', 'fscore', 'parkinson', 'eps',           'snt', 'income', 'rtk', 'cr', 'rec', 'debt', 'beta', 'unsystematic',           'systematic', 'assets', 'liabilities', 'operating', 'return',           'cashflow']# 数量超过300个的前缀（基于20250117时候的gold所能拥有的数据字段）prefix_forename = ['pv', 'fnd', 'mdl', 'oth', 'anl', 'fn', 'est', 'mws', 'nws']# 无前缀字段other_field = ['ppent', 'vwap', 'high', 'employee', 'ppent_net', 'rad', 'open',               'annualdiv', 'split', 'capex', 'high_52wks', 'goodwill', 'current_ratio',               'volume_10wks', 'sga_expense', 'inventory_turnover', 'preferred_dividends',               'depre_amort', 'working_capital', 'sales_growth', 'marketbeta', 'totalreturn',               'price', 'bookvalue_ps', 'sharesout', 'cap', 'cogs', 'ebitda', 'price_26wks',               'dividend', 'depre', 'invested_capital', 'cash_st', 'revenue', 'adv20', 'accum_depre',               'enterprise_value', 'shares', 'sales_ps', 'low_52wks', 'equity', 'sales', 'close',               'interest_expense', 'pretax_income', 'chgprice', 'sp500', 'accounts_payable',               'cost_of_revenue', 'retained_earnings', 'cash', 'low', 'ebit', 'growth', 'inventory', 'volume']
```

## ***2. 得到模板必须的字段列表***

由于模板内可能存在固定的字段（如最常见的close，return一类），这些字段是不能进行剪枝的，因此我们需要检查我们的模板，把固定的多次出现的字段单独拎出来。

对于跑一二三阶的朋友来说，这部分的主要的字段来自于二阶的group field，三阶函数涉及到的字段大部分是close和return这类无前缀字段（如果使用了其他trade when字段，请自行补充），这一类我们在prune函数中是默认不剪枝的。

最后我把我自己用的group和trade when相关字段进行了整合，如下：

```
group_fields = {'usa_group_pv' : ['pv13_2l_scibr', 'pv13_3l_scibr', 'pv13_4l_scibr', 'pv13_5l_scibr', 'pv13_6l_scibr',                                 'pv13_new_2l_scibr', 'pv13_new_3l_scibr', 'pv13_new_4l_scibr', 'pv13_new_5l_scibr', 'pv13_new_6l_scibr', 'pv13_r2_min10_3000_sector',                                'pv13_r2_min20_3000_sector', 'pv13_r2_min2_3000_sector', 'pv13_r2_min5_3000_sector', 'pv13_rcsed_6l'],                'usa_group_mdl' : ['mdl10_group_name'],                'asi_group_pv' : ['pv13_2_all_delay_1_sector', 'pv13_2_sector', 'pv13_2l_scibr', 'pv13_3l_scibr', 'pv13_4l_scibr',                                'sta1_minvol1m_normc20', 'sta1_minvol1m_normc5', 'sta1_minvol1m_normc50', 'sta1_minvol1mc10', 'sta1_minvol1mc2',                                'sta1_minvol1mc20', 'sta1_minvol1mc5', 'sta1_minvol1mc50'],                'eur_group_pv' : ['pv13_2_sector', 'pv13_2l_scibr', 'pv13_3l_scibr', 'pv13_4l_scibr', 'pv13_52_sector', 'pv13_5_sector',                                    'sta2_top1200_fact4_c10', 'sta2_top1200_fact4_c2', 'sta2_top1200_fact4_c20', 'sta2_top1200_fact4_c5',                                    'sta2_top1200_fact4_c50'],                'glb_group_pv' : ['pv13_10_f2_g3_minvol_1m_sector', 'pv13_10_f2_g4_minvol_1m_sector', 'pv13_10_f3_g2_minvol_1m_sector',                                'sta3_pvgroup3_sector', 'sta3_sec_sector', 'sta1_allc10', 'sta1_allc2', 'sta1_allc20', 'sta1_allc5',                                'sta1_allc50']}other_ctp_fields = ['fnd28_value_05480']    # 在通用的group的字段中
```

## ***3. 优化prune函数***

基于上述的数据结构，我们对prune函数进行了优化。对于完全不包含前缀字段的表达式，我们采取全部接收（数量很少）；对于包含前缀字段的表达式，先按照含有的字段进行分组，最后再检查包含该字段的因子数是否大于保留数量keep_num，若是大于则随机保留，不大于则全部保留。

```
# 优化后的剪枝函数def prune(next_alpha_recs, region, prefix_forename, keep_num):    # next_alpha_recs为因子数据，从get_alpha中获得    # region为对应的地区    # prefix_forename为希望进行剪枝的字段前缀，如果为空则均不剪枝（list型）    # keep_num为保留数量    output = []    field_dirt = defaultdict(list)    # 获得模板必备的字段    ctp_field = other_ctp_fields.copy()    for key, fields in group_fields.items():        if key.startswith(region): ctp_field += fields    # 开始进行剪枝    for i, rec in enumerate(next_alpha_recs):        exp = rec[1]        sharpe = rec[2]        # 遍历需要剪枝的前缀        is_has_forename = False        for forename in prefix_forename:            field = exp.split(forename)            # 若存在前缀，则会将str分为多段            if len(field) > 1:                field = forename + field[-1].split(",")[0].split(")")[0]                # 若此时组成的字段在ctp字段中，则跳过                if field in ctp_field:                    continue                # 非ctp字段则进行剪枝                if sharpe < 0:  field = "-%s"%field                # 添加到field_dirt中                field_dirt[field].append([rec[1],rec[-1],rec[7]])                is_has_forename = True                break        # 若不存在前缀，则保存到output中        if not is_has_forename:            output.append([rec[1],rec[-1],rec[7]])    # 检查不同字段数量是否超过    for field, data in field_dirt.items():        if len(data) > keep_num:            # 随机获取keep_num个数据            output += random.sample(data, keep_num)        else:            output += data    output_dict = {region : output}    return output_dict
```

## 4. 函数测试

我选取了一段时间我跑过的因子进行函数测试，测试结果正常。

![图片](images/img_ccc6751f58.png)

最后祝大家每天因子多多，base多多，value up up。 **我是YZ72256，如果本文对你有帮助欢迎点赞，如果其他想法也欢迎在评论区留言。**

---

## 讨论与评论 (5)

### 评论 #1 (作者: XX42289, 时间: 1 year ago)

太厉害了，这个prume函数确实要比最原始的要强大一点。

YZ72256同学最近写的帖子很多啊，经常看到你产出了很多非常有用的帖子。点赞了。

另外想问一下YZ72256同学，用这套剪枝的话，产出率会提高多少呢？这个有关注过吗？如果剪枝太多的话，会不会错过一些非常好的operator组合呢。

期待您的回复（不是AI，纯手打）

---

### 评论 #2 (作者: YZ72256, 时间: 1 year ago)

[XX42289](/hc/en-us/profiles/14187300941847-XX42289)  感谢评论，目前来看产出率相比刚改版时候还是有所提升的，得到的alpha数量虽然有所下降，但alpha之间的相关程度也下降了不少，从而可使用的alpha是在提高的。

目前比较关注数据的广度，因此我自己使用的剪枝数量仅为2，肯定是会错过一些组合的，这是进行剪枝就无法避免的问题，而这边采取同个字段的组合alpha进行随机选取剪枝更是可能加重这一现象，在编写代码的时候也考虑过是否要按照sharpe进行排列后保留前几项，但因可能存在weight较大从而导致sharpe和fitness都超级高的alpha，便放弃排序的方案。

因没有想出如何筛选出较好的alpha，只能退而求其次采用随机方式寄托于运气，如果XX42289同学对这方面有任何见解，也希望能不吝分享探讨，感恩！

---

### 评论 #3 (作者: BA51127, 时间: 1 year ago)

关于产出率问题，从你的描述来看，虽然alpha数量有所下降，但相关度也降低了，实际可用的alpha是增加的。不过，剪枝确实可能会错过一些好的operator组合。我也有同感，如果按照sharpe排序保留前几项，可能会因为weight过大导致sharpe和fitness都超级高的alpha被保留，这未必是最佳选择。目前随机选取剪枝的方式虽然依赖运气，但也是一种可行的折中方案。如果大家对如何筛选出较好的alpha有好的想法，欢迎一起探讨。

---

### 评论 #4 (作者: SD81732, 时间: 1 year ago)

最近在论坛搬运了好多大佬的代码，感觉自己打怪的装备在一点点升级

我在随机sample keep_num前加了个判断条件，如果超过4倍keep_num则从sharpe前4倍keep_num个中随机sample，4选1。有点像在排序和随机两者间做了个折中。晚点用这个新剪枝跑下看看。

我个人情况是，check submission没过的，大多数都是相关性太高了，换成大佬的这个剪枝方式，应该会有不少帮助的。

先行谢过！！！

---

### 评论 #5 (作者: LL87164, 时间: 1 year ago)

建议：输出结果中保留alpha_id。将来本地计算相关性时可以直接调用，不用再改代码。

```
output.append([alpha_id, exp, sharpe, decay])
```

---

