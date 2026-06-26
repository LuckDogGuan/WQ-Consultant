# Alpha Appears in Signals but Not in Genius Pyramid

- **链接**: [Commented] Alpha Appears in Signals but Not in Genius Pyramid.md
- **作者**: RC80429
- **发布时间/热度**: 10个月前, 得票: 20

## 帖子正文

This has happened to me a few times—for example, when I used an earnings data field in the alpha logic. Sometimes when I create an alpha, it appears in my signals, but when I use an earnings data field to build a pyramid, it doesn’t show up in the Genius Pyramid.

Does anyone know why this happens? Is it related to  **dataset restrictions** ,  **operator compatibility** , or something else? Would appreciate any guidance on this.

---

## 讨论与评论 (1)

### 评论 #1 (作者: JN96079, 时间: 9个月前)

There are definitely more data categories you have in such signals...Dataset has an issue with the Genius pyramid, only with the data category. For example, using Earnings and Risk datasets in a signal will count as 2 pyramids, Earnings and Risk. Otherwise, if you use, let's say, Earnings, Risk and Price Volume, you will have 0 pyramid effect. You get?

In short, to create a pyramid, you need a maximum of 2 data categories from any dataset to complete it. As a tip, you can try atom alphas, best in pyramid construction

---

