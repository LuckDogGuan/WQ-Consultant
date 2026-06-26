# How Important Is Dataset Selection Compared to Operator Selection?

- **链接**: [Commented] How Important Is Dataset Selection Compared to Operator Selection.md
- **作者**: DT49505
- **发布时间/热度**: 1个月前, 得票: 6

## 帖子正文

I’ve been wondering whether alpha performance is driven more by choosing the right dataset or by applying the right transformations/operators. In your experience, which contributes more to finding robust signals?

Thank you, and I’m looking forward to your feedback.

---

## 讨论与评论 (4)

### 评论 #1 (作者: PT58185, 时间: 1个月前)

both. But correct implementation makes you more confident in your research

---

### 评论 #2 (作者: CW62782, 时间: 1个月前)

A good operator can clean up a signal, but it usually can’t rescue a dataset or field with no real information. If the field has strong behavior, even simple transforms like rank, ts_rank, delta, or neutralization can work.

---

### 评论 #3 (作者: JN96079, 时间: 1个月前)

Yeah, that's right, what has been mentioned by  [PT58185](/hc/en-us/profiles/35773074046487-PT58185)  and  [CW62782](/hc/en-us/profiles/34536778058903-CW62782) . Moreso, you can try starting with dataset selection, then, when you are more confident with how you do research, try any dataset at random along the way.

^^JN

---

### 评论 #4 (作者: KU30147, 时间: 1个月前)

I think both are equally important.

---

