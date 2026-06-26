# Ace

- **链接**: [Commented] Ace.md
- **作者**: AK58648
- **发布时间/热度**: 5个月前, 得票: 3

## 帖子正文

I have been recently trying to run IND risk-neutralized alphas, but in the settings I cannot seem to place the neutralization. I am getting the neutralization selected is invalid. Is there anyone who has encountered the same issue, and what is a possible fix?

---

## 讨论与评论 (2)

### 评论 #1 (作者: SS35873, 时间: 5个月前)

For the IND region, the Statistical neutralization isn't available so it might be because you are trying to use that it is showing you an error.

---

### 评论 #2 (作者: JN96079, 时间: 5个月前)

In the IND region,  **STATISTICAL** neutralization isn’t supported, so the error you’re seeing may be due to trying to apply that setting. If your alpha relies on statistical neutralization, you’ll need to switch to a different neutralization method for IND, such as SLOW or SLOW and FAST.

^^JN

---

