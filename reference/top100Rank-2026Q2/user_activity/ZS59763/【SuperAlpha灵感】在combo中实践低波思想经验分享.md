# 【SuperAlpha灵感】在combo中实践低波思想经验分享

- **链接**: 【SuperAlpha灵感】在combo中实践低波思想经验分享.md
- **作者**: ZS59763
- **发布时间/热度**: 11个月前, 得票: 67

## 帖子正文

如题

基于低波思想写出的combo，根据最近一年的收益波动率倒数进行加权从而构建组合。

> stat=generate_stats(alpha);
> 1/ts_std_dev(stat.returns,252)

这个combo在不同select下都能较为明显地抑制波动，以下给出一个例子：

![图片](images/img_9be370b6f7.png)

![图片](images/img_89ea65d7e0.png)

![图片](images/img_0d045ac6be.png)

原始组合（1）

![图片](images/img_3c0586a5de.png)

低波combo下的组合

![图片](images/img_b2646d5c29.png)

在not own上的表现：

![图片](images/img_93d1820778.png)

![图片](images/img_af7fc12400.png)

![图片](images/img_e03f1a4e72.png)

---

## 讨论与评论 (2)

### 评论 #1 (作者: ER48854, 时间: 10个月前)

有时候不如等权，可以作为一个比较选项

---

### 评论 #2 (作者: AL13375, 时间: 9个月前)

看到优化后的pnl，真的是震惊无比，这也太直了，简直是梦中情pnl好吗！！！

游戏王大佬的研究每次都能带来惊喜！

combo我就借走啦~

期待大佬的更多产出！祝大佬本赛季定级GM！

=*=*=*=*=*=*=*=*=*=路漫漫其修远兮，吾将上下而求索=*=*=*=*=*=*=*=*=*=

---

