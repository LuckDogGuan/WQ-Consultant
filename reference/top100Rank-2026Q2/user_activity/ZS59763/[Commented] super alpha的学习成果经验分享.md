# super alpha的学习成果经验分享

- **链接**: [Commented] super alpha的学习成果经验分享.md
- **作者**: YL21428
- **发布时间/热度**: 1年前, 得票: 28

## 帖子正文

我是去年就加入Brain的“萌新”，经历过vf暴跌，所以一直都没有什么兴趣去研究super alpha，这一次按照论坛里大佬们的经验，终于做出来了看起来还不错的super alpha.

我看的就是下面这些

[【进阶学习】Super Alpha 每日获得额外1-60USD，来此学习 – WorldQuant BRAIN](../QP72475/[Commented] 03-【进阶学习】Super Alpha 每日获得额外1-60USD来此学习Pinned.md)

![图片](images/img_b1f68a11c7.png)

接下来我就讲一下我做super alpha用了什么selection和combo

我喜欢使用的Selection Expression是if_else(turnover >= 0.15 && turnover <= 0.20, 1.5, 1) * if_else(turnover >= 0.30 && turnover <= 0.35, 1.5, 1) / operator_count * (1 - self_correlation) * if_else(in(competitions, "ACE2023"), 1, 0)

我的Combo Expression是combo_a(alpha, nlength = 500, mode = 'algo1')

我首先用两个换手率条件对股票进行筛选：

if_else(turnover >= 0.15 && turnover <= 0.20, 1.5, 1) - 当换手率在15%-20%区间时给予1.5倍增强

if_else(turnover >= 0.30 && turnover <= 0.35, 1.5, 1) - 当换手率在30%-35%区间时也给予1.5倍增强

除以operator_count - 操作者越多，信号强度会被稀释

(1 - self_correlation) - 降低自相关性高的股票权重，追求更独立的信号

if_else(in(competitions, "ACE2023"), 1, 0) - 只选择参与ACE2023比赛的股票，因为我是G2，这个周为了特定比赛，一定要设置的过滤条件

combo是借鉴论坛里的做法，我自己不太明白其中的具体思想

---

## 讨论与评论 (2)

### 评论 #1 (作者: XW61573, 时间: 1年前)

非常棒，学习学习

---

### 评论 #2 (作者: ZS59763, 时间: 1年前)

很有意义的实践，通过权重进行相关性筛选，而不是强制限制cor小于30or50，值得学习。

此外，针对combo，combo_a是个智能算法，1是等权，其他的一些组合方式就把整个因子 池的不同属性，例如turn，pnl，看做字段来跑的，ra。

---

