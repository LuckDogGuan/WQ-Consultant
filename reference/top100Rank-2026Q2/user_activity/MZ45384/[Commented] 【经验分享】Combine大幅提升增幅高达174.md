# 【经验分享】Combine大幅提升，增幅高达1.74

- **链接**: [Commented] 【经验分享】Combine大幅提升增幅高达174.md
- **作者**: WL58980
- **发布时间/热度**: 1个月前, 得票: 16

## 帖子正文

5月Combine更新了，此次更新涵盖了截至2026年3月31日整个期间提交的所有Alpha和SuperAlpha，变化情况如下图所示：

![图片](images/img_68c9b94142.png)

所有指标都提升了，既有些惊喜，但也在意料之中，因为近几个月还是花了比较多的精力去提升Combine，那我是如何做的呢？

1.Combined Alpha Performance（0.01 -> 0.99,增幅0.98）

2月28日至3月31日增幅0.98，那么这一个月里我做了什么？我针对两个方面做了改善：

（1）前两个月我的Combined Alpha Performance一直维持在0.5左右，而4月更新后却降到了0.01，我猜测是因为2月我开启了CHN区域，但只交了几个而且表现并不好而拉胯了整体的Combine，所以我3月就提交了CHN区域的不同Pyramid的Alpha，数量来到了20多个并组合了SuperAlpha。

（2）因为前期提交了少量EUR和USA区域的D0的Alpha，但后来听前辈说D0不太稳定，就一直没有提交D0了，这可能是Combined Alpha Performance一直维持在0.5左右的主要原因，虽然当时D0区域不能提交ppa，难度比较大，但还是提交了一些达标的ra。比较幸运的是5月开启了为期一个月的D0 Power Pool Alphas Thematic Competition

，前期提交了少量D0 Alpha的可以把握此次机会。

总结就是一旦开启了新的区域就要多交,并且择优提交（择优标准可以参考其他前辈的帖子），SuperAlpha也很重要，否则将会拉低整体的Combine。

2.Combined Selected Alpha Performance（-1.65 -> 0.09,增幅1.74）

Combined Selected Alpha Performance是第二次更新，没想到第二更新就从第一次的-1.65回正，比较意外。Combined Selected Alpha Performance是被系统选中的，我们无法主观选择，所以存在很大的运气成分。但如果可以保证自己提交的所有Alpha都表现较好，那么就可以维持一个高Combine，就像抽奖机里全是一等奖和特等奖，你抽到的最差也是一等奖。所以，在提交Alpha时要注重质量。

3.Combined Power Pool Alpha Performance（0.16 -> 1.52,增幅1.36）

前段时间推出可以自行选择Tag来组合自己的Power Pool Alpha，经过几个月的尝试，在第三次更新时终于迎来了提升，此次组合我做了两点：“删”和“补”。

（1）删：在Submitted页面有个指标是OS/IS Ratio，在二月份之前提交的所有Alpha应该都有这个指标数据，先筛选出所有OS/IS Ratio小于1的ppa删除PowerPoolSelected标签。

（2）补：在删除完之后再筛选出OS/IS Ratio在0.6至1区间的ppa补齐，补齐每个区域的Pyramid，确保每个Pyramid不少于3个。

删是为了保留高质量的Alpha，补是为了维持Combined  Performance地稳定性。

4.Combined Osmosis Performance（1.91 -> 2.46,增幅0.55）

关于Osmosis Performance我并没有花费太多精力，因为第一更新Combined Osmosis Performance就达到了1+。第一次筛选的方法与筛选Power Pool Alpha的方法大差不差，然后每个区域分配100000分，OS/IS Ratio越高points占比越高，后期再微调points占比以及用新提交的Alpha替换之前并不是很出色的Alpha,在几次更新后Combined Osmosis Performance一直维持在前100名左右。

以上就是我关于提升Combined Performance的经验分享，希望对大家有所帮助。Combined Performance的提升需要长期坚持下去，我也经历过Combined Performance为负的阶段，体验过每次更新前的期待与更新后的失落，尤其是新人顾问前期会因为各种因素导致Combined Performance不太理想，但只要坚持下去，经过不断地学习，一切将会变得越来越好，加油！！！另外想短期内快速提升Combined Performance可以考虑Combined Osmosis Performance和Combined Power Pool Alpha Performance，每个季度都有两次尝试的机会，第三次则决定季度等级的划分；同时也恭喜472位通过Combined Osmosis Performance提升综合Alpha表现的顾问，互勉！！！

---

## 讨论与评论 (14)

### 评论 #1 (作者: JC24357, 时间: 1个月前)

感谢佬的分享，恭喜combine大提升！

终于有佬分享Combined Power Pool Alpha Performance的打tag心得了，学习到了可以使用OS/IS ratio作为主要的参考指标，先删除ratio<1的标签，再补上0.6<ratio<1的ppa，并且还要尽量在各个Region分散pyramid，以确保多样性。

Osmosis的给分也可以参考这个思路，OS/IS ratio越高points给的占比越高。同时还要记得用新的表现更优的alpha及时更新组合。

====================== (・∀・(・∀・(・∀・*) 保持进步，保持好奇，坚持探索  ============================
===================================================================================================

---

### 评论 #2 (作者: XZ21889, 时间: 1个月前)

感谢分享~  请问Combined Osmosis Performance在什么情况下会有啊？我这里还显示的是No matching Alphas

---

### 评论 #3 (作者: MZ45384, 时间: 1个月前)

太强了大佬，我os更新两次都是高开低走，现在只剩0.26了。看了大佬的经验有些感悟，想问每个地区大概选了多少个alpha呢？包括superalpha吗？

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #4 (作者: BW14163, 时间: 1个月前)

这篇复盘真的太干货了！特别认同你关于“删”和“补”Power Pool Alpha的策略，利用OS/IS Ratio做精细化筛选，既保证了质量又兼顾了稳定性，这种实操思路非常值得借鉴。而且你提到的“抽奖机理论”也很形象，只有保证池子里全是好货，被系统选中的运气才不会差。
从Combined Alpha Performance触底反弹，到各项数据稳步提升，这背后几个月的坚持和试错真的不容易。正如你所说，前期哪怕数据为负也不要气馁，只要找对方法持续优化，结果一定不会差。感谢大佬的无私分享，已经拿小本本记下了，接下来就照着这个思路去优化我的Alpha组合，大家一起加油，争取下季度也能冲上榜！

能具体说说关于Combined Osmosis Performance每个地区选多少个合适，选哪些地区，ppa占比多少吗？

---

### 评论 #5 (作者: WL58980, 时间: 1个月前)

如果Combined Osmosis Performance连续多个月都处于负数的话，建议一键清零重新组合。Combined Osmosis Performance对于那些Combined Performance长期处于负数的朋友们是十分友好的，它可以帮助我们快速达到genius门槛，有助于我们冲刺季度奖金。当然，新的机遇也伴随着更激烈的竞争，随着越来越多的人通过Combined Osmosis Performance达到genius门槛，那只能通过六维来一较高下了，所以后面的竞争将会越来越激烈的，加油！！！

============================================================================

Study hard — quality over quantity, no room for mediocrity. Cherish every learning opportunity, stay focused, and learn from the experts. Keep pushing!

============================================================================

---

### 评论 #6 (作者: MM38095, 时间: 1个月前)

受益匪浅，谢谢你的经验

---

### 评论 #7 (作者: LJ12230, 时间: 1个月前)

感谢大佬分享.试试大佬的方法看看效果！

---

### 评论 #8 (作者: FX25214, 时间: 1个月前)

希望佬还是更多的关注自己的Combined Alpha Performance和ppa cb，个人拙见认为这两个cb是对自己因子提交的最好的体现。也能最大程度的反应单因子提交的水平。祝愿佬这个赛季这俩的cb能稳稳破1，实现master的升级之路
----------------------------------------------------------来自传奇耐打王的点赞------------------------------------------------------------

---

### 评论 #9 (作者: FF65210, 时间: 1个月前)

感谢经验分享，cb确实是个关键的指标，对评级的影响很大，也反应了自己交的因子情况，向大佬学习，祝佬早日vf1.0.

===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================

---

### 评论 #10 (作者: CW49566, 时间: 29天前)

感谢大佬分享，学习到不错的思路：按塔来分配。

---

### 评论 #11 (作者: XW23690, 时间: 28天前)

太强了！我的os combine一直很低，学习一下思路

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #12 (作者: LL32212, 时间: 27天前)

感谢无私分享“开启新区域必多交且择优、用‘删补大法’优化 PPA 标签、靠 OS/IS 比例阶梯式分配 Osmosis 权重”的纯血干货。从低谷的失落到如今的全面开花，你的坚持和方法论直接给新人们指明了方向。收下膝盖，新季度继续互勉，一起顶峰相见！

---

### 评论 #13 (作者: LW67640, 时间: 26天前)

感谢大佬的分享，对于我这个Combined Selected 为负的人太有用了。看了佬的分析，我的问题可能是每个区域交的数量不够平均（也不够多），以及没有及时对OS/IS Ratio做筛选。感谢，马上调整，如果效果好，群里寻你发红包哈！

============================================================

长风破浪会有时，直挂云帆济沧海。

============================================================

---

### 评论 #14 (作者: DW99585, 时间: 18天前)

没有OS/IS ratio的，要入选Combined Osmosis Performance和Combined Power Pool Alpha Performance吗

---

