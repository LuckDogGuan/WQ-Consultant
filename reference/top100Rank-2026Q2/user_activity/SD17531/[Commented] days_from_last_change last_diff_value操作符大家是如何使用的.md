# days_from_last_change, last_diff_value操作符大家是如何使用的？

- **链接**: [Commented] days_from_last_change last_diff_value操作符大家是如何使用的.md
- **作者**: AH18340
- **发布时间/热度**: 1年前, 得票: 22

## 帖子正文

days_from_last_change：Amount of days since last change of x 距离上次x变化的天数

last_diff_value:Returns last x value not equal to current x value from last d days 返回最后一个x值不等于最近d天的当前x值

这两个操作符感觉很难用于alpha中，有哪个大佬使用过的吗？一般是怎么使用的？

祝大家vf1.0 人人都是GM

---

## 讨论与评论 (3)

### 评论 #1 (作者: SD17531, 时间: 1年前)

这两个操作符大有可为的,
但是我以前使用的时候出现了一个问题,那就是ts_delta(datafield, days_from_last_change(datafield))这个总是报错,不清楚哪里有问题.我们可以简单对比一下:
ts_delay(datafield, d)是返回d天前这个datafield的值;
last_diff_value(datafield)如果正常运行,是返回上一个datafield的值.
两者的区别在于,如果你这对这个数据字段的更新频率并不清楚,第一个你很可能取不到值.比如年更新的数据,d填写66,是找不到数值的.但是last_diff_value是可以保证找值的.不清楚更新更新频率的情况下,last_diff_value更好.
days_from_last_change这个是返回一个d,这个要搭配使用了ts_delta(datafield, days_from_last_change(datafield)),这个就是变化值了.他也是稳定性强,会准确返回修改的间隔.
如果我们要用前后对比的数据,那么使用ts_delta(datafield,d)就会出现d设置不合理导致取不到数值的情况,也会丧失一部分的精确性,因为这个d是固定值,太死板了.设置为66的话,以季度报告为例,他不是严格按照时间间隔区分的,而且也可能在一个季度内出现修改,修改后才是争取的报告.
前面讲了不少废话,我建议是你可以找一下你带ts_delay或者ts_delta的Alpha,去自己修改一下,也许会收获好的效果.比如最近周会分享速度,加速度,也许就可以使用这两个操作符去优化.

---

### 评论 #2 (作者: WF37935, 时间: 9个月前)

[SD17531](/hc/zh-cn/profiles/27215746752791-SD17531)    ts_delta(datafield, d)，这个d只能是数字，不能是days_from_last_change(datafield)这种的

---

### 评论 #3 (作者: YC81895, 时间: 4个月前)

@ [SD17531](/hc/en-us/profiles/27215746752791-SD17531) ，感谢大佬，很好的解释了ts_delay和last_diff_value的差别，关于days_from_last_change,是否在news和sentiment数据集中比较好用，比如长时间没有负面新闻或负面情绪就是好消息。

---

