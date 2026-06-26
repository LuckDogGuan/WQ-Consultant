# 请教各位大佬一个关于本地Check Self Correlation程序错误的问题？

- **链接**: 请教各位大佬一个关于本地Check Self Correlation程序错误的问题.md
- **作者**: YH25030
- **发布时间/热度**: 8个月前, 得票: 37

## 帖子正文

最近在做本地check self correlation程序时候，经常报如下错误。ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))我看同时在运行的回测程序都正常，没有任何报错。我问了AI， AI让我尝试设置等待时间。我即使设置了检查一个因子，等待60或者120秒。但是运行到200个因子左右，还是有同样报错。想问问大家有没有遇到相同问题？

---

## 讨论与评论 (1)

### 评论 #1 (作者: JX14975, 时间: 8个月前)

获取pnl也有限流的，只是限制比直接用api接口检查相关性宽很多，你这个问题估计是因为最近api限流变得比较严重了。建议在检查相关性前先使用基于表达式的剪枝，减少检查量。【代码优化】基于字段结构的剪枝函数，更准确、更灵活，提升回测效率https://support.worldquantbrain.com/hc/en-us/community/posts/31928133456407

---

