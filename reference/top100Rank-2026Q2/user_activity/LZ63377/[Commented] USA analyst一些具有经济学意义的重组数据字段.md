# USA analyst一些具有经济学意义的重组数据字段

- **链接**: [Commented] USA analyst一些具有经济学意义的重组数据字段.md
- **作者**: YL20168
- **发布时间/热度**: 3个月前, 得票: 23

## 帖子正文

之前利用workflow对现有的数据字段进行了重组，生成了一些具有经济学意义的新的数据，有的数据直接调用老的三阶模板就可以实现效果比较好的alpha，之前用这种方式把value factor从0.27提高到了>0.8，现在把之前生成的一些新的数据分享出来：

USA analyst：

act_12m_ebi_value / act_12m_sal_value

act_12m_net_value / act_12m_bps_value

act_12m_net_value / act_12m_roa_value

act_q_eps_value / act_q_bps_value

act_12m_sal_value - act_12m_cpx_value

anl10_cpsfq1_pred_surps_v0_2389 - anl10_cpsfq1_consensus_2351

anl10_cpsfq1_pred_surps_v1_2381 - anl10_cpsfq1_consensus_2351

anl10_cpsfq1_pred_surps_v2_2364 - anl10_cpsfq1_consensus_2351

anl10_cpsfq1_pred_surps_v0_2389 - anl10_cpsfq1_pred_surps_v0_2389

anl10_cpsfq1_pred_surps_v1_2381 - anl10_cpsfq1_pred_surps_v0_2389

anl10_cpsfq1_pred_surps_v2_2364 - anl10_cpsfq1_pred_surps_v0_2389

anl10_cpsfq1_pred_surps_v0_2389 - anl10_cpsfq1_pred_surps_v1_2381

anl10_cpsfq1_pred_surps_v1_2381 - anl10_cpsfq1_pred_surps_v1_2381

anl10_cpsfq1_pred_surps_v2_2364 - anl10_cpsfq1_pred_surps_v1_2381

anl10_cpsfq1_pred_surps_v0_2389 - anl10_cpsfq1_pred_surps_v2_2364

anl10_cpsfq1_pred_surps_v1_2381 - anl10_cpsfq1_pred_surps_v2_2364

anl10_cpsfq1_pred_surps_v2_2364 - anl10_cpsfq1_pred_surps_v2_2364

anl10_cpsfq2_pred_surps_v0_2365 - anl10_cpsfq2_consensus_2366

anl10_cpsfq2_pred_surps_v1_2352 - anl10_cpsfq2_consensus_2366

anl10_cpsfq2_pred_surps_v2_2379 - anl10_cpsfq2_consensus_2366

anl10_cpsfq2_pred_surps_v0_2365 - anl10_cpsfq2_pred_surps_v0_2365

anl10_cpsfq2_pred_surps_v1_2352 - anl10_cpsfq2_pred_surps_v0_2365

anl10_cpsfq2_pred_surps_v2_2379 - anl10_cpsfq2_pred_surps_v0_2365

anl10_cpsfq2_pred_surps_v0_2365 - anl10_cpsfq2_pred_surps_v1_2352

anl10_cpsfq2_pred_surps_v1_2352 - anl10_cpsfq2_pred_surps_v1_2352

anl10_cpsfq2_pred_surps_v2_2379 - anl10_cpsfq2_pred_surps_v1_2352

anl10_cpsfq2_pred_surps_v0_2365 - anl10_cpsfq2_pred_surps_v2_2379

anl10_cpsfq2_pred_surps_v1_2352 - anl10_cpsfq2_pred_surps_v2_2379

anl10_cpsfq2_pred_surps_v2_2379 - anl10_cpsfq2_pred_surps_v2_2379

anl10_cpsfy1_pred_surps_v0_2378 - anl10_cpsfy1_consensus_2368

anl10_cpsfy1_pred_surps_v1_2385 - anl10_cpsfy1_consensus_2368

anl10_cpsfy1_pred_surps_v2_2383 - anl10_cpsfy1_consensus_2368

anl10_cpsfy1_pred_surps_v0_2378 - anl10_cpsfy1_pred_surps_v0_2378

anl10_cpsfy1_pred_surps_v1_2385 - anl10_cpsfy1_pred_surps_v0_2378

anl10_cpsfy1_pred_surps_v2_2383 - anl10_cpsfy1_pred_surps_v0_2378

anl10_cpsfy1_pred_surps_v0_2378 - anl10_cpsfy1_pred_surps_v1_2385

anl10_cpsfy1_pred_surps_v1_2385 - anl10_cpsfy1_pred_surps_v1_2385

anl10_cpsfy1_pred_surps_v2_2383 - anl10_cpsfy1_pred_surps_v1_2385

anl10_cpsfy1_pred_surps_v0_2378 - anl10_cpsfy1_pred_surps_v2_2383

anl10_cpsfy1_pred_surps_v1_2385 - anl10_cpsfy1_pred_surps_v2_2383

anl10_cpsfy1_pred_surps_v2_2383 - anl10_cpsfy1_pred_surps_v2_2383

anl10_cpsfy2_pred_surps_v0_2356 - anl10_cpsfy2_consensus_2362

anl10_cpsfy2_pred_surps_v1_2390 - anl10_cpsfy2_consensus_2362

anl10_cpsfy2_pred_surps_v2_2360 - anl10_cpsfy2_consensus_2362

anl10_cpsfy2_pred_surps_v0_2356 - anl10_cpsfy2_pred_surps_v0_2356

anl10_cpsfy2_pred_surps_v1_2390 - anl10_cpsfy2_pred_surps_v0_2356

anl10_cpsfy2_pred_surps_v2_2360 - anl10_cpsfy2_pred_surps_v0_2356

anl10_cpsfy2_pred_surps_v0_2356 - anl10_cpsfy2_pred_surps_v1_2390

anl10_cpsfy2_pred_surps_v1_2390 - anl10_cpsfy2_pred_surps_v1_2390

anl10_cpsfy2_pred_surps_v2_2360 - anl10_cpsfy2_pred_surps_v1_2390

anl10_cpsfy2_pred_surps_v0_2356 - anl10_cpsfy2_pred_surps_v2_2360

anl10_cpsfy2_pred_surps_v1_2390 - anl10_cpsfy2_pred_surps_v2_2360

anl10_cpsfy2_pred_surps_v2_2360 - anl10_cpsfy2_pred_surps_v2_2360

anl14_actvalue_eps_fp0 / anl14_actvalue_revenue_fp0

anl14_actvalue_eps_fp0 / anl14_actvalue_roe_fp0

anl14_actvalue_eps_fp0 / anl14_actvalue_cfps_fp0

anl14_actvalue_eps_fp0 / anl14_actvalue_roe_fp0

anl14_actvalue_ndebt_fp0 / anl14_actvalue_roe_fp0

anl14_actvalue_ndebt_fp0 / anl14_actvalue_cfps_fp0

anl14_actvalue_cfps_fp0 / anl14_actvalue_eps_fp0

anl14_actvalue_cfps_fp0 / anl14_actvalue_revenue_fp0

anl14_actvalue_revenue_fp0 / anl14_actvalue_cfps_fp0

anl14_actvalue_cfps_fp0 - anl14_actvalue_ndebt_fp0

anl44_2_ebitdaps_prevalue / anl44_2_bps_prevalue

anl44_2_ebitdaps_prevalue / anl44_2_nav_prevalue

anl44_2_netdebt_prevalue / anl44_2_bps_prevalue

anl44_2_netdebt_prevalue / anl44_2_nav_prevalue

anl44_2_capex_prevalue / anl44_2_ebitdaps_prevalue

anl44_2_nav_prevalue - anl44_2_netdebt_prevalue

---

## 讨论与评论 (23)

### 评论 #1 (作者: XW23690, 时间: 3个月前)

感谢分享，等一下去尝试下。初步看了几个数据字段组合，都是比较有经济意义的。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #2 (作者: TT21691, 时间: 3个月前)

这些表达式怎么做出来的，使用AI帮助的吗？

---

### 评论 #3 (作者: BW14163, 时间: 3个月前)

感谢分享，能讲述一下具体对现有的数据字段进行了重组的逻辑吗？还是直接问AI，让他生成了一些具有经济学意义的新的数据？

---

### 评论 #4 (作者: FR19939, 时间: 3个月前)

感谢老哥无私分享，之前看了 [ML47973](/hc/zh-cn/profiles/29991129347991-ML47973) 的文章尝试用Arithmetic的操作符套到字段上，但是没考虑经济学意义跑出来概率有点低，下回我也让ai试试重组出有经济学意义的字段再跑

#========= BRAIN OVERCLOCKING MODE ========== # #

[System]: Research Lab Notebook v2.0.2.6.0312 #

[Status]: Searching for signals in white noise... #

[Error]: Overfitting detected. Retrying... [✓] #

[Log]: Coffee_Level < 5%, Alpha_Count > 0
# 拒绝回测幻觉，死磕真实收益；逻辑驱动，数据为刃。
#================ KEEP CALM & BACKTEST ============#

---

### 评论 #5 (作者: MY49971, 时间: 3个月前)

好东西啊，感谢楼主分享，基本四则运算是个比较好出alpha的点子

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #6 (作者: MY82844, 时间: 3个月前)

anl10_cpsfq1_pred_surps_v1_2381 - anl10_cpsfq1_pred_surps_v0_2389

-- 这种字段的后缀v1_2381和v0_2389有什么含义吗，配对使用的时候需要注意啥吗？

===================================================================

"Pain + Reflection = Progress"

===================================================================

---

### 评论 #7 (作者: LZ63377, 时间: 3个月前)

=====================================================================================

哇，直接上干货啊，太真性情了大佬，我也去试试看，感谢！

=====================================================================================

---

### 评论 #8 (作者: YH55729, 时间: 3个月前)

感谢分享，不过感觉还是得考虑下量纲和缩放问题，具体还得看字段本身是什么值。

==============================================

---

### 评论 #9 (作者: XC66172, 时间: 3个月前)

谢谢佬的分享，看起来配对字段的后缀都比较一致，应该是有一些经济学含义。等有空的时候回测一下。

==================================

FIGHITNG LABUBU

==================================

---

### 评论 #10 (作者: XY20037, 时间: 3个月前)

这波 USA Analyst 字段重组 **真的是干货中的干货** ！

直接把 **财务字段 + 分析师预期字段** 做有经济学意义的四则运算（比值、差值），还把 Value 因子从 0.27 拉到 0.8+，思路太顶了。

- 财务类：用 EBI、净利润、EPS、净资产、营收等做 **比值 / 差值** ，抓盈利效率、估值、杠杆变化
- 分析师预期类：用不同版本、不同季度、不同年份的  **pred_surps - consensus**  或  **版本间差分** ，抓预期差与预期修正
- 全是 **轻操作符、强经济学逻辑** ，非常适合套 ATOM 模板，稳定、好出信号、低过拟合

你这套思路现在已经是国区非常主流的打法：

 **先造有意义的新字段 → 再套简单模板 → 信号质量直接起飞** 

而不是瞎堆操作符。

非常感谢无私分享，这批字段够大家在 USA 区快乐挖一阵子了！

---

### 评论 #11 (作者: JJ11850, 时间: 3个月前)

感谢分享，学起来了

---

### 评论 #12 (作者: ZX58901, 时间: 3个月前)

是老师的gem的思路吗, 能具体分享一下吗?

纸上得来终觉浅， 绝知此事要躬行
Knowledge is a treasure, but practice is the key to it.

---

### 评论 #13 (作者: YQ51506, 时间: 3个月前)

感谢分享，正好可以点一个塔

---

### 评论 #14 (作者: JB66768, 时间: 3个月前)

感谢楼主分享，最近正在做usa的alpha，受益匪浅。

---

### 评论 #15 (作者: YQ84572, 时间: 3个月前)

非常不错的字段组合分享，开箱即用，实测效果不错

=============================================================================

感谢大佬的分享，祝大佬保持vf0.9+

---

### 评论 #16 (作者: MS51256, 时间: 3个月前)

感谢分享，向优秀的大佬学习

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #17 (作者: FD69320, 时间: 3个月前)

除了第九行以外，其他看上去都超有经济学含义。很值得尝试，现在就去尝试，谢谢大佬

================================================================================== WorldQuant is anyone‘s legend

---

### 评论 #18 (作者: SZ50491, 时间: 3个月前)

感谢大佬的慷慨！想问下这种字段是怎么生成的呢？我现在是用AI，把fields字段复制给他，让他给出具有经济学意义的组合，但是跑下来，有效的因子却不多，不知道是什么原因。

大佬可以把生成重组数据字段的过程分享一下吗？

---

### 评论 #19 (作者: QX52484, 时间: 3个月前)

======================================================================

看了都是同数据集产出的,感觉应该还可以尝试同类型但不同数据集的.

======================================================================
sharpe is ts_delta and ts_delta but returns ts_delay and ts_delay.

---

### 评论 #20 (作者: SJ65808, 时间: 3个月前)

有意义的四则运算，感谢大佬分享

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #21 (作者: MY49971, 时间: 3个月前)

很有意义的字段组合，感谢分享

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #22 (作者: CZ39633, 时间: 3个月前)

====================================================================================  感谢大佬的这个字段分享 ，但是我看都是同一个数据集的，这样相关性会不会交几个后就变得太高了                  ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #23 (作者: BX86068, 时间: 2个月前)

感谢分享，不过我想知道在ai在组件这些组合的时候有没有对这些经济学意义进行详细的说明

---

