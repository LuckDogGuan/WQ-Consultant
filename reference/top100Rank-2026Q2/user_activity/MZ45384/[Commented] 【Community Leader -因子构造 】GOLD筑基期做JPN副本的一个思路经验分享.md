# 【Community Leader -因子构造 💎】GOLD筑基期，做JPN副本的一个思路经验分享

- **链接**: [Commented] 【Community Leader -因子构造 】GOLD筑基期做JPN副本的一个思路经验分享.md
- **作者**: MY82844
- **发布时间/热度**: 6个月前, 得票: 18

## 帖子正文

自从ASI加了Japan Robustness Sharpe Test之后，发现做ASI的alpha难度陡增，十不存一，能不能过test感觉和开盲盒一样，和GOLD小伙伴一样，感觉亟需一个提高效率的办法。

在了解EUR的risk70数据的时候，注意到这个Great Britain Country Factor Loading的使用率非常高，一直很纳闷，难道这里有什么特别的打开方式吗？

![图片](images/img_0c23a602e4.png)

直到最近刷到Tiger大佬之前的一个 [关于JPN的帖子]([Commented] 【IDEA BY TIGER】关于在ASI如何提升JPN表现不佳的一个思路经验分享.md) ，想到是不是factor loading也可以类似market cap拿来处理JPN的问题？

于是，就形成了一个做JPN副本的一个思路：

```
if_else(abs(rsk70_mfm2_asetrd_cnt_jpn), sig, NaN)
```

使用rsk70_mfm2_asetrd_cnt_jpn做loading mask，先在有JPN有factor loading的sub universe上做回测，如果可以通过各种测试，那么既可以考虑直接提交，又可以回到ASI的整个universe上再做回测，这样理论上过Japan Robustness Sharpe Test的把握也会大一些。

举个这几天提交的例子：

先使用JPN的loading mask，挖出一个可以过测试的alpha：

![图片](images/img_dce738da64.png)

然后，我们在Visualization界面再看下JPN部分的占比：

![图片](images/img_e33844f637.png)

![图片](images/img_b3d36eaa9f.png)

![图片](images/img_e3c311cd0f.png)

最后，去掉loading mask，回到ASI的整个univese，再跑一下回测，发现就得到一个可以提交的alpha：

![图片](images/img_f20890480a.png)

过程中注意到的几个问题：

1. JPN Sharpe和JPN Robustness Sharpe是两个度量，两者还有差别

2. 使用mask之后，pnl主要贡献确实来自JPN（在上面的例子，pnl图最高的那条线来自JPN），但是并不能把非JPN的影响完全去除

3. 使用mask之后，得到的JPN Robustness Sharpe和在ASI整个universe得到的JPN Robustness Sharpe比较接近， 但是还是有些出入

4. 类似的mask方法应该可以衍生不少其它的应用，抛砖引玉，有待大家进一步发掘

---

## 讨论与评论 (11)

### 评论 #1 (作者: LJ85703, 时间: 5个月前)

你我都是gold,你怎么这么优秀

---

### 评论 #2 (作者: YQ84572, 时间: 5个月前)

很好的思路，自从asi出来japantest之后出货率简直是灾难下跌，而且无法预见性的控制japantest，楼主的分享是很好的方法。

--------------------------------------------------------------------------------------------------------------------

感谢分享，祝大佬保持vf0.9+

--------------------------------------------------------------------------------------------------------------------

---

### 评论 #3 (作者: NL80893, 时间: 5个月前)

太及时了！谁懂啊！ASI 加了 Japan Robustness Sharpe Test 之后，做 alpha 简直是地狱难度，十次回测九次折戟，完全像开盲盒一样没头绪。大佬这个用 rsk70_mfm2_asetrd_cnt_jpn 做 loading mask 的思路，直接给 GOLD 筑基期的我们指了一条明路，先在 JPN 子宇宙验证再扩展到 ASI 全宇宙，大大提高过测概率，还附带实操案例，太贴心了！已经立马记下来要去实操，感谢大佬的无私分享！
共鸣拉满！我最近也在死磕 ASI 的 JPN 测试，卡了好久都没头绪，提交的 alpha 要么栽在 JPN Robustness Sharpe 上，要么整体表现拉胯。大佬这个 mask 思路简直是神来之笔，既解决了 JPN 测试的痛点，还能提高提交效率，连注意事项都列得明明白白，太靠谱了！必须收藏起来反复研读，祝大佬多出优质 alpha！

---

### 评论 #4 (作者: MZ45384, 时间: 5个月前)

捕捉优化方法：if_else(abs(rsk70_mfm2_asetrd_cnt_jpn), a, nan)

大佬，能问一下此处的mask是什么原理？

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

### 评论 #5 (作者: JZ74499, 时间: 5个月前)

救命恩人，无需多言

---

### 评论 #6 (作者: MY82844, 时间: 5个月前)

[MZ45384](/hc/en-us/profiles/29472943154455-MZ45384)  按照AI的提示，factor loading一般是某种因子载荷，在country factor loading这边，一个公司如果在日本有某种存在，比如在东京交易所挂牌交易，一般会有这个载荷值，个人理解

---

### 评论 #7 (作者: AK76468, 时间: 5个月前)

这个方法好巧妙，没想到这个country loading可以这样用,的确是gold可以使用的好方法，如果大佬在未来达到了master就可以开启jpn地区了，到时候在jpn直接回测就更方便了。

另外如果我们在glb等复合区域遇到了表现不佳的country/region，在无论如何也解决不了的情况下，也是可以使用if_else(abs(country_factor_loading), nan, a)，去掉该国家/地区的不佳表现，以提升总体表现的。

---

### 评论 #8 (作者: JX14975, 时间: 5个月前)

学到了，rsk70_mfm2_asetrd_cnt_jpn这个字段只在jpn有值，因此可以用来选出jpn的股票。这种方法的鲁棒性比原来使用的rank(cap)在0.3-0.4之间的筛选法好多了。
另：ASI 3.12sharpe的alpha原来是存在的啊...

---

### 评论 #9 (作者: MY82844, 时间: 5个月前)

[AK76468](/hc/en-us/profiles/28846915371031-AK76468)  理论上来说，这个操作并不局限在country，对于industry看来也可以结合visualization进行类似操作，比如，有些基本面因子可能不是全板块适用的情况，也需要加以处理

╱╲╱╲
“Hedge funds are a bet on human ingenuity and the ability to outthink the market.”
— James Simons, Renaissance Technologies

---

### 评论 #10 (作者: JQ70858, 时间: 2个月前)

这个月在做ASI地区，一直想着用JAPAN反推一下ASI地区，看看到地什么情况，因为机会所有表达式都卡在日本robustnesssharpe上了。但是我没日本地区。。。不过还是得到了启发的，这个操作符好像从来没用过，今天就尝试一下。谢谢分享！

---

### 评论 #11 (作者: JC31003, 时间: 1个月前)

我用这个办法优化后变成可提交状态，但是提交时候会报错：

- Japan Robustness Sharpe check error.

![图片](images/img_3aa2b7f91d.png)

---

