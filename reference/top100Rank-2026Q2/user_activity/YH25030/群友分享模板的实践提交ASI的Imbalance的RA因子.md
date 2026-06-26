# 群友分享模板的实践，提交ASI的Imbalance的RA因子

- **链接**: 群友分享模板的实践提交ASI的Imbalance的RA因子.md
- **作者**: YH25030
- **发布时间/热度**: 8个月前, 得票: 2

## 帖子正文

因为一二三模板没有找到ASI的Imbalance的信号，所以尝试其他方法。记得小虎哥在顾问群里分享过一个模板，就想试一下，竟然找到了信号，提交了一个RA。分享给大家，希望对大家有帮助。1.整理数据 ：log(<data_field>/ts_mean(<data_field>, 252))2.主信号：ts_scale(log(<data_field>/ts_mean(<data_field>, 252)),252)3.增强信号：group_zscore(ts_scale(log(<data_field>/ts_mean(<data_field>,252)), 252),densify(pv13_4l_scibr))

---

## 讨论与评论 (1)

### 评论 #1 (作者: JX14975, 时间: 8个月前)

这个模板是小虎哥多久分享的？我居然没有发现。要是有热心顾问能够总结一下群里的模板就好了，我上个月换了手机，忘备份微信数据了。

---

