# 【0基础手搓alpha】介绍一种手搓alpha摆脱模版束缚的方法（含有overfit风险）

- **链接**: 【0基础手搓alpha】介绍一种手搓alpha摆脱模版束缚的方法含有overfit风险.md
- **作者**: JL71699
- **发布时间/热度**: 1年前, 得票: 17

## 帖子正文

提交了很多machine alpha，有一天心血来潮，想手搓一个，但是没有idea，就随便写一个最简单的想法吧idea： 买收益率高的股票（纯瞎想的，没参考任何材料文献）先确定setting，由于本人比较懒，啥也没改，直接USA top3000 其他没动（至于为什么，也是有原因的，本人在IQC2024 mainland China final上说过，如果你尝试把中性化设置为none，你就会发现USA基本上怎么买都不会亏，你写个1都是大好走势，虽然最近不太行，但是也很不错了）下图为USA setting none 其余默认 alpha表达式为1看到这个走势是不是很想做alpha呢？初步想法ts_rank(returns,time)随便写一个时间窗口，发现效果还是很不错的很奇怪，为什么会是负的曲线，如果有大佬读到这篇文章，希望不吝赐教然后加一些过滤符，手动@ATOM2024 1st TL87739，感谢大佬的不吝赐教直接加上trade_when(group_count(alpha,market)>count,alpha,0)这个运算符很好避免了Weight concentration报错情况，之前经常遇到，感谢大佬可以将我救赎（如果你也有和我一样的困惑，可以尝试一下这个运算符）得到下面这根曲线，已经很不错了，但是turnover比较高，fitness也比较低接下来就是最喜欢的微调环节（又叫overfit环节）众所周知，turnover高了可以使用trade_when操作符降低，大家可以加入自己喜欢的条件（萝卜青菜各有所爱），当然我也在2024IQC mainland China final上介绍过其他类似的操作符，如if_else,left_tail等运算符。经过一顿操作，alpha已经只差fitness了，这下又要@研究小组里的大佬了，直接上group运算符，使用pv13（别问为什么，问就是大佬甄选），然后这个alpha的fitness得到了明显改善，但是还差一点，由于本人比较偷懒，不想再加运算符了，直接加了一个之前submit过的高fitness的alpha让他两综合，就到了可以提交的标准prod也是很低的一个alpha，幸福感又提升了一点捏，毕竟全程也只用了returns一个dataset虽然表现一般般，但是这个alpha是本人第一个手搓的alpha，还是比较有成就感的。大家应该也会有一样的想法，虽然手搓困难，但是当你能做出来，就是要比纯machine要开心一点，希望大家多多尝试（不需要你有太多知识储备，只要你敢尝试就能做出来，就像我的idea是多么普通，但是prod却很低）

---

## 讨论与评论 (7)

### 评论 #1 (作者: WL13229, 时间: 1年前)

尝试使用ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1)ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)降低一下turnover

---

### 评论 #2 (作者: LG87838, 时间: 1年前)

厉害，操作的行云流水，学习啦！

---

### 评论 #3 (作者: XH93773, 时间: 1年前)

你好，看到您的手搓Alpha历程，我的内心也跃跃欲试了，方便问一下文中所说的过滤符具体有哪些比较好用的吗？

---

### 评论 #4 (作者: JL71699, 时间: 1年前)

@XH93773，那tradewhen举例子，你可以尝试tradewhen（rank（volume）>0.1&&rank (volume）<0.9,alpha,0),这个是说截面交易量在10%到90%的股票开始执行你的alpha，剩下的股票不进行操作，这个操作可以明显降低alpha的换手率，但是对于某些靠高换手得到高收益的alpha，可能会导致sharpe和fitness有所降低，另外，你也可以尝试WL13229老师说的方法降低换手率，而对于提高fitness，可以按我文中的加入group操作符，遍历一下groupdataset可以得到你想要的fitness，但是请注意，上述方法仅限于出信号的alpha，对于噪音并不适用

---

### 评论 #5 (作者: WP88606, 时间: 1年前)

手搓是有意思，就是回测太慢了，干瞪眼

---

### 评论 #6 (作者: YQ76635, 时间: 1年前)

具体是什么group，把操作符写下行么？我都手搓一天了，就差一点fitness了

---

### 评论 #7 (作者: YQ76635, 时间: 1年前)

是另外一片研报里的idea

---

