# 【Alpha灵感】股票推荐系统-随机贴现现金流Alpha Template

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwgXRjSXwB86D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAdtodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzQ5MTIwMzA5NjczMTktLUFscGhhJUU3JTgxJUI1JUU2JTg0JTlGLSVFOCU4MiVBMSVFNyVBNSVBOCVFNiU4RSVBOCVFOCU4RCU5MCVFNyVCMyVCQiVFNyVCQiU5Ri0lRTklOUElOEYlRTYlOUMlQkElRTglQjQlQjQlRTclOEUlQjAlRTclOEUlQjAlRTklODclOTElRTYlQjUlODEGOwhUOg5zZWFyY2hfaWRJIikyN2UwODUzZC00ZTQwLTRkZjUtYjMxYi01ODRjNmUwNjg0ODMGOwhGOglyYW5raQ46C2xvY2FsZUkiCnpoLWNuBjsIVDoKcXVlcnlJIgxZSDI1MDMwBjsIVDoScmVzdWx0c19jb3VudGkQ--f19177cbf6d130ee2d843f8fd75a628f202aa08e
- **作者**: RZ39578
- **发布时间/热度**: 9个月前, 得票: 10

## 帖子正文

【Alpha灵感】股票推荐系统-随机贴现现金流Idea想法通过随机折现现金流构建企业公允价值分布，计算当前企业价值处于企业公允价值分布中的位置，判断当前企业价值是否被低估，高估，决定买入，卖出。论文链接：https://support.worldquantbrain.com/hc/en-us/community/posts/15770966939671-Research-Raper-12-Stock-Recommendations-from-Stochastic-Discounted-Cash-Flows原文逻辑通过企业未来现金流 作为自变量，企业收入的对数作为因变量构建模型将所得模型放入蒙特卡洛模拟得到随机现金流分布通过代入企业随机现金流分布到DCF赋值模型，得到企业价值分布再计算企业价值分布-各项成本得到股票价值分布带入当今股票价值，计算其在分布中的位置，决定是否买入，卖出模拟结果可以看到论文中的推荐系统可以准确判断当前 股票价值在公允股票价值分布中的位置概念解释1 企业价值完全收购一家企业，市场愿意付出的钱这里企业的价值并非看资产值多少钱，而是看企业制造利润的能力。2 折现现金流（DCF)把未来的现金流 按照资本成本 折算为当前价值。假设银行每年利率3.5%,那么1年后的103.5跟现在的100是等值的，dcf就是把未来的现金流折算为当前价值，用于评估企业值多少钱。3 加权平均资本成本(Weight Average Capital Cost)表示每年向资金来源付出的回报占总资本的比率一家公司如果单向银行借钱，利率3.5%，那么3.5%就是企业的加权平均资本成本。但企业的融资来源一般会有多个,通过计算各来源资本占比以及其预期回报可以得到 企业的加权平均资本成本（wacc)。Equity:股权资金Debt:债务资金4 蒙特卡洛模拟通过不断地随机，逼近事物原先的值https://www.bilibili.com/video/BV1fo4y1977h5 DCF估值模型在这个模型中，企业价值由未来能产生的现金流决定，第一部分的累加表示 企业在n年内的现金流折算为当前的企业估值-part1，第二部分表示n年之后的现金流折算为当前的企业估值-part2。Alpha构建1 用回归模型拟合[未来现金流&企业收入]的关系cf_margin = (ebitda-capex-(working_capital-last_diff_value(working_capital,504)))/log(revenue);a = ts_regression(log(revenue),cf_margin,1080,lag=0,rettype=2);b = ts_regression(log(revenue),cf_margin,1080,lag=0,rettype=1);2 用市场均值作为随机值模拟蒙特卡洛x= group_mean(cf_margin,1,market);# simulate_log(revenue)y=a*x+b;cf_random = y*cf_margin;3 计算 加权平均资本支出（WACC)# wacc# risk_market:市场风险risk_market = ts_delta(pv13_revere_index_value,1)/ts_delay(pv13_revere_index_value,1);# re:股权风险re = fnd6_optrfr+fnd6_beta*(risk_market-fnd6_optrfr);e = fnd6_mkvalt;d = debt_lt+debt_st;# 债务风险rd = fnd6_intpn/d;# 税收比率tc = income_tax / pretax_income;v = e + d;k= (e/v)*re + (d/v)*rd *(1-tc);4 通过DCF估值模型计算 公允企业价值分布day=60;g= k/5;enterprise_value_random = ts_mean(cf_random/signed_power(1+k,ts_step(day)),day)*day + cf_random*(1+g)/(signed_power(1+k,day)*(k-g));5 计算当前企业价值位置并根据位置确定 分配权重。ev_random_mean = ts_mean(enterprise_value_random,1080);ev_random_dev = ts_std_dev(enterprise_value_random,1080);alpha = (enterprise_value-ev_random_mean)/ev_random_dev;#此处0.67，以及1.15为论文中0.25与0.125的换算trade_when(abs(alpha)>0.67,if_else(abs(alpha)>1.15,-2*alpha,-alpha),-1)Alpha初步结果可以看到总体结果还是不错的，作为基本面alpha turnover也很低，说明企业公允价值分布的计算是有效的。但sharpe太低了，推测是交易频率门槛过高导致的，考虑降低交易门槛以及增加对于偏离公允价值企业的反应降低交易门槛+提升alpha对于信号反应在拉低门槛，以及拉高反应后，表现还不如之前，推测是更改了原论文的推荐比例问题，所以这里打算单独提升alpha对于极值的反应.单独提升alpha对于信号反应结果还是一样，所以没有办法通过简单的降低交易门槛，拉高alpha反应的方式 提升alpha表现，所以接下来打算引入论文中的 横截面推荐系统，将其与当前的单股推荐系统结合得到更强的信号。检查 ev_random信号是否有效-排除结果来自trade_when()不过在此之前，需要再检查算出的ev_random分布是否有效，于是将其换成data中的enterprise_value,结果如下说明 计算出来的ev_random为有效值。改进Alpha引入论文中横截面推荐系统log_revenue = log(revenue);cf_margin = (ebitda-capex-(working_capital-last_diff_value(working_capital,504)))/log(revenue);a = ts_regression(log_revenue,cf_margin,1080,lag=0,rettype=2);b = ts_regression(log_revenue,cf_margin,1080,lag=0,rettype=1);# random_value 用市场均值作为随机值x= group_mean(cf_margin,1,market);# simulate_log(revenue)y=a*x+b;cf_random = y*cf_margin;# wacc 加权平均资本支出risk_market = ts_delta(pv13_revere_index_value,1)/ts_delay(pv13_revere_index_value,1);re = fnd6_optrfr+fnd6_beta*(risk_market-fnd6_optrfr);e = fnd6_mkvalt;d = debt;rd = fnd6_intpn/d;tc = income_tax / pretax_income;v = e + d;k= (e/v)*re + (d/v)*rd *(1-tc);# DCF估算企业价值day=60;g= k/5;enterprise_value_random = ts_mean(cf_random/signed_power(1+k,ts_step(day)),day)*day + cf_random*(1+g)/(signed_power(1+k,day)*(k-g));# 计算当前企业价值所处位置ev_random_mean = ts_mean(enterprise_value_random,1080);ev_random_dev = ts_std_dev(enterprise_value_random,1080);alpha = (enterprise_value-ev_random_mean)/ev_random_dev;# 单股票推荐系统ssq = trade_when(abs(alpha)>0.67,if_else(abs(alpha)>1.15,-2*alpha,-alpha),-1);# 横截面股票推荐系统neu_rank_alpha = group_neutralize(rank(alpha),densify(industry));csq = trade_when(abs(neu_rank_alpha)>0.1,neu_rank_alpha,-1);csq+ssq可以看到，sharpe增加了，但总体增加不多，可能是横截面推荐系统并没有引入更多的有效信号。问题如果我后续还要继续改进该alpha应该从哪些方面入手？wacc（加权平均资本支出）的计算实在是很繁琐，有没有什么数据字段可以替代的？这种跟着论文复现的alpha，应该不具有抽象为模板的能力，那么我们如何从这些论文中获得我们的alpha模板呢？

---

## 讨论与评论 (5)

### 评论 #1 (作者: AH18340, 时间: 9个月前)

感谢大佬分享，太专业了，没大看懂- -！=============================================================================The best time to plant a tree is 20 years ago. The second-best time is now.=============================================================================

---

### 评论 #2 (作者: LR93609, 时间: 9个月前)

感谢分享，非常详细的财务成本分析，我有几个疑问，请帮忙解答：1. margin计算方法：如果用了log就变形了，建议去掉。比如，1/20=0.05，相当于5%，对于margin来讲是合理的；1/log(20)=33%，完全是两个结果，而且也不成比例。cf_margin = (ebitda-capex-(working_capital-last_diff_value(working_capital,504)))/log(revenue);2. 市场风险计算：pv13_revere_index_value：Value of specified index for the date？与市场风险是两码事。建议使用：systematic_risk_last_360_days，Systematic Risk Last 360 Days# risk_market:市场风险risk_market = ts_delta(pv13_revere_index_value,1)/ts_delay(pv13_revere_index_value,1);3. 估值计算：按照基础公式，后半部分是比值，你算成了均值，可能是笔误，建议调整enterprise_value_random = ts_mean(cf_random/signed_power(1+k,ts_step(day)),day)*day + cf_random*(1+g)/(signed_power(1+k,day)*(k-g));总之，估值模型是相对科学的，analyst和model里面都有静态或动态估值模型，确实有不错的表现。建议，如有时间，再完善一下，说不定会是一个不错的Alpha，加深对财务成本的认识。再次感谢分享，随白璧微瑕，但可圈可点，做了很多不错的尝试。--------------------------------------------------------------------------------------------------凡事发生，皆利于我；愿我所愿，尽是美好--------------------------------------------------------------------------------------------------

---

### 评论 #3 (作者: YH25030, 时间: 9个月前)

谢谢分享。想问一下这个模板回测时间正常吗？我发现如果数据字段里面数据很多，即使是USA，EUR的ts_regression回测时间会很长，GLB则是报利用资源太多的错误。不知道大佬有没有遇到同样问题。

---

### 评论 #4 (作者: RZ39578, 时间: 7个月前)

YH25030,这个模板是之前用户阶段写的，回测时间只有5年。当时在写alpha的时候，也遇到了operator使用过多的问题，特意压了几个operator。

---

### 评论 #5 (作者: RZ39578, 时间: 7个月前)

LR93609好的，谢谢建议。 现在各类知识还比较薄弱，等最近补足后，再尝试完善这个模板。

---

