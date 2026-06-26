# 关于IND地区Robust universe sharpe的改善方法经验分享

- **链接**: [Commented] 关于IND地区Robust universe sharpe的改善方法经验分享.md
- **作者**: ZX12447
- **发布时间/热度**: 7个月前, 得票: 39

## 帖子正文

相信有很多顾问和我一样在回测IND地区的alpha的过程中经常遇到Robust universe sharpe较低因此达不到提交要求的问题，经过不断探索社区里各位大神的建议，我发现一些有效解决这个问题的方法，但是我这里的修改方法仅供参考，而且只针对"Robust universe sharpe"这个问题，大家不要学我用了很多operater后让alpha过度拟合了。

![图片](images/img_b191f26870.png)

上图是我回测IND地区的alpha时遇到的Robust universe Sharpe的问题，Robust universe Sharpe还差一点点就达到标准，后面我发现使用以下运算符可以让这个问题得到改善:

group_backfill、group_zscore、winsorize、group_neutralize、group_rank、ts_scale、signed_power，在一个alpha使用以上这几个运算符的其中一两个就好，不建议全部使用，会有过度拟合的问题。其次，如果使用以上的运算符后还是差一点的话可以通过修改时间来解决这个问题，一般我们使用运算符中的时间大多数是252,若时间改成275或者是其他的时间可能可以改善Robust universe Sharpe的问题。不过改时间的话不利于alpha可解释性，如果是实在没法用运算符去修改了可以尝试从时间的角度去修改。还有就是修改Decay或者Truncation还有Neutralization都能帮助我们解决Robust universe alpha这个问题。

![图片](images/img_380727c782.png)

我在修改完运算符里的时间后最终我的alpha通过了Robust universe sharpe这个问题。(但是我这个alpha用了太多运算符导致了过度拟合的问题，大家不要学!!!)

-------------------------------------------------------------------------------------------------------

希望我的分享可以有效帮助到大家，不过我还是个新顾问(非常小白的那种程度)，对于很多金融层面的知识都不是非常理解，本次分享只是在N次回测后得出的结论，但不一定具有金融角度的意义。如果有更好的方法可以改善IND地区的Robust universe alpha问题，还请各位大神指导！！！非常期待与感谢大家的探讨！！！

---

## 讨论与评论 (11)

### 评论 #1 (作者: XW23690, 时间: 7个月前)

感谢分享，特别要注意过拟合问题，我也分享下我的方法。IND区域有robust问题我通常只做一个操作符运算，如果还是不行我就选择放弃。一般情况下，对于数据long count和short count比较少的数据，我选择group_backfill(x,sector,120,std=4)或者ts_backfill(x,120)处理；对于数据集中带有score或者rank的，因统计方法或者地区不同而产生的不同数据字段，我会用max(x1,x2)或者min(x1,x2)来代替x1；至于其他的，我简单遍历一些group_rank等运算符，更改下decay=0、5、20，实在不能通过的我就放弃了。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #2 (作者: YH25030, 时间: 7个月前)

谢谢大佬分享。winsorize和ts_backfill我经常用，常常有意想不到的效果。好几次直接把因子从ppa升级到ra. signed_power我还没有尝试过。下次手搓ra的时候，可以试试。

---

### 评论 #3 (作者: AM12075, 时间: 7个月前)

看完你的经验分享确实挺有启发的，我这边也想请教几个点。你提到 group_backfill、winsorize、group_neutralize 这些 op 对提升 Robust universe Sharpe 很有帮助，那你在实测中有没有发现某些字段对这些操作特别敏感？比如有些 field 用 group_zscore 之后明显改善，但另一些几乎没反应。

另外我也挺好奇你说的“改时间”这一招，像把 252 换成 275、300 这种，我自己试过几次，偶尔灵有效果，但有时候反而会导致 prod corr 或 turnover 出问题，有没有总结过大概哪些场景下改时间最稳？

还有用了太多 op 之后过拟合，这个我也踩过坑。请问你现在有没有形成一套“最多用几层”“多少个 op”这样的自我限制？感觉这部分如果能有点经验，会对我们这些刚做 IND 的顾问很有帮助。

---

### 评论 #4 (作者: HL81191, 时间: 7个月前)

感谢分享，之前跑的脚本有很多没能通过，试了下，将decay从60降至20，Robust universe Sharpe由0.72变成超过1通过了，但是turnover由22%升至41%，然后再微调一下就通过了，后面几天又有alpha可以交了

---

### 评论 #5 (作者: MY82844, 时间: 6个月前)

感谢分享，backfill有时候产生的变化挺大的，另外，注意到有另一个类似的算子kth_element(x, d, k)，两者使用上有什么区别吗？

---

### 评论 #6 (作者: XG98059, 时间: 6个月前)

亲测好用的，感谢大佬分享。

---

### 评论 #7 (作者: SL52857, 时间: 6个月前)

实验了一下，该天数确实会有一点用处，只是确实无法做出合理的经济学解释

---

### 评论 #8 (作者: OZ41942, 时间: 6个月前)

感谢分享，运算符确实可以改善robust，再结合turnover的降低可以有效生成alpha

---

### 评论 #9 (作者: AH18340, 时间: 6个月前)

1.group_backfill、group_zscore、winsorize、group_neutralize、group_rank、ts_scale、signed_power，在一个alpha

2.修改时间来解决这个问题，

3.修改Decay或者Truncation还有Neutralization

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #10 (作者: DQ66419, 时间: 6个月前)

感谢分享改善IND地区alpha回测中Robust universe sharpe低的方法，IND好多都是这个robust测试不通过。可用group_backfill等运算符（选1-2个防过拟合），或改时间（如252换275，但是这个确实不好分辨经济学意义，相当于12个月改成了13个月）。多用运算符个人感觉也不一定会真的导致过拟合，因为是在一个已经有明确信号的基础上再进行优化的，当然只是个人理解，如果不对，勿喷，哈哈。

---

### 评论 #11 (作者: XC51024, 时间: 5个月前)

但是我觉得在改善robust的时候，turnover会不可避免的抬高，特别是你调参数的时候，会导致既不符合经济学逻辑，而且费率还高不赚钱

---

