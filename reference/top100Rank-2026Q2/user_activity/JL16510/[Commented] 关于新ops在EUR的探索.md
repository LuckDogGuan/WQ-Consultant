# 关于新ops在EUR的探索

- **链接**: [Commented] 关于新ops在EUR的探索.md
- **作者**: ZZ13271
- **发布时间/热度**: 1年前, 得票: 39

## 帖子正文

首先声明：灵感来自于我自己的猜测和尝试，欢迎大家多多讨论

idea：怀疑eur很多国家拖后腿，所以想着grouping从country入手，这里我选择group_rank，再结合ts_target_tvr_hump这个操作符，表达式与所想不一定契合。欢迎各位高手指正。模版如下：

ts_mean(ts_target_tvr_hump(group_rank({data},country), lambda_min=0, lambda_max=1, target_tvr=0.1),5)

表现如下，随机找了一个，未做调整就发上来了，见谅：

![图片](images/img_224bcde46a.png)

![图片](images/img_7a64e2b6f1.png)

---

## 讨论与评论 (11)

### 评论 #1 (作者: SD17531, 时间: 1年前)

请大佬多教我本领,谢谢.

---

### 评论 #2 (作者: ZZ13271, 时间: 1年前)

更正一下

-ts_mean(ts_target_tvr_hump(group_rank({data},country), lambda_min=0, lambda_max=1, target_tvr=0.1),5)

模版需要加负号

---

### 评论 #3 (作者: EL94401, 时间: 1年前)

感谢分享。Assumption，简练清晰。

---

### 评论 #4 (作者: PW58059, 时间: 1年前)

虎哥出品，必属精品。

---

### 评论 #5 (作者: KD86036, 时间: 1年前)

学习了，感谢分享

---

### 评论 #6 (作者: LL95667, 时间: 1年前)

感谢老虎哥无私分享

---

### 评论 #7 (作者: HZ69256, 时间: 1年前)

感谢虎哥精品分享。

有几点问题分享：

1.是不是可以将ts_mean和ts_target_tvr_hump这两个操作符互换位置，效果是不是会有一些不同？

2.ts_mean应该可以泛化，换成其他几个ts操作符，比如ts_max，ts_min，ts_max_diff，ts_arg_max等，说不定也会有一定的效果。

3.EUR可行的话，GLB和ASI说不定也可以跑出东西。

---

### 评论 #8 (作者: JB71859, 时间: 1年前)

虎哥出品，必属精品。

---

### 评论 #9 (作者: JL16510, 时间: 1年前)

使用降低trv的操作符后，因子的质量怎样？个人感觉因子的性能会有所降低，不知道虎哥是否观察提交的因子os？

---

### 评论 #10 (作者: HH34943, 时间: 1个月前)

相关性会不会过高现在用

---

### 评论 #11 (作者: XW23690, 时间: 1个月前)

感谢分享，正好尝试一下EUR 的 D0

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

