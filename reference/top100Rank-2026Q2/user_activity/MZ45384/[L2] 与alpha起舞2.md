# 与alpha起舞2

- **链接**: [L2] 与alpha起舞2.md
- **作者**: QX52484
- **发布时间/热度**: 7 months ago, 得票: 29

## 帖子正文

由于上一次的如何利用tvr操作符与alpha起舞发布后,有点在群里成为专属名词的感觉,随继续沿用标题.

起舞1:链接 [../HP65370/[Commented] 如何利用tvr操作符与alpha起舞论坛精选.md](../HP65370/[Commented] 如何利用tvr操作符与alpha起舞论坛精选.md)

本期起舞的操作符为ts_delta.

![图片](images/img_9c9593144f.png)

可以看到如果改变decay 对tvr的提升仍然很有限. ![图片](images/img_7b1027e3d2.png)

但如果保持decay仍为15,添加ts_delta操作符

![图片](images/img_1481dba1d8.png)

![图片](images/img_ea4e0834f1.png)

原理部分:

ts_delta(x, d) Returns x - ts_delay(x, d)

假如你的原始因子很平稳：

x:  10, 10.2, 10.3, 10.4, 10.3, 10.2 ...

ts_delta(x):
      +0.2, +0.1, +0.1, -0.1, -0.1 ...

结果： **信号之间的相对排名波动增大 → 换仓更频繁 → TVR 自然变高。**

bty,顺便附带起舞1的效果

![图片](images/img_b7dfa0655c.png)

btybty

但对于alpha表现的提升上来说,tvr_decay似乎更稳定,可能是因为其基于原始数据进行,有时候更感觉像是为了换手率进行了瞬时买入卖出的噪声,即tvr改变但sharpe不变);而ts_delta是改变了原始数据的,扩大了数据的相对波动的(这段内容待验证,欢迎其他顾问参考实例讨论.)

晋升M之后也又拿到了一些新的target_tvr操作符.

ts_target_tvr_hump

ts_target_tvr_delta_limit

但实际使用下来还是仍然是基础op中的ts_target_tvr_decay比较好用,ts_target_tvr_hump 在对于ts_target_tvr_decay难以起效的情况下,可能会有奇效.但对死鱼的挽救力度也仍然有限,且修改参数带来的提升也非常之小.

或有起舞3?

---

## 讨论与评论 (3)

### 评论 #1 (作者: MP35172, 时间: 2 months ago)

这篇"起舞"系列太适合新手了！之前只知道调decay来控换手，原来 `ts_delta` 通过放大信号波动能更直接地提升TVR，原理拆解得很直观。虽然你提到它可能引入噪声，但作为学习不同算子特性的案例很有启发。准备拿手头低换手的因子试试这个思路，顺便对比下 `tvr_decay` 的效果。期待起舞3！

---

### 评论 #2 (作者: MW39826, 时间: 2 months ago)

这看起来似乎是过拟合的强行结果

---

### 评论 #3 (作者: FF56620, 时间: 2 months ago)

ts_delta的原理分析很透彻！"x - ts_delay(x, d)"这个差分形式确实能放大信号的相对波动。

关于ts_delta和tvr_decay的选择，我有一点补充：

1. **ts_delta的本质**：它是对原始信号进行差分，相当于一个高通滤波器，可能会放大噪声；tvr_decay是低通滤波器，更平滑

2. **实际应用场景**：如果你发现原始信号虽然平稳但排名波动小，可以尝试ts_delta增加换手；但如果原始信号已经有较好的排名特性，tvr_decay可能更稳健

3. **组合使用**：可以先做tvr_decay平滑，再用ts_delta放大波动，这样既控制了噪声又增加了换手

关于ts_target_tvr_hump，从原理上看是在ts_target_tvr_decay基础上增加了 hump 限制，当难以直接起效时可能会有奇效。但修改参数带来的提升通常很小，这点确实需要注意。

期待起舞3！

---

