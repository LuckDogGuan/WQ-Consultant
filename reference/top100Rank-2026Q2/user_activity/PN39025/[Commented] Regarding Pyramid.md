# Regarding Pyramid.

- **链接**: [Commented] Regarding Pyramid.md
- **作者**: PT88153
- **发布时间/热度**: 1年前, 得票: 2

## 帖子正文

Can anyone tell what is the new rule of pyramid in alpha submittion.

---

## 讨论与评论 (18)

### 评论 #1 (作者: NL99431, 时间: 1年前)

Chỉ có những alpha dùng từ 1-2 bộ data mới được tính vào kim tự tháp, những alpha dùng từ 3 bộ data đổ lên sẽ không được tính vào kim tự tháp

---

### 评论 #2 (作者: ST50816, 时间: 1年前)

For a pyramid to be counted it must contain datasets less than two <2

---

### 评论 #3 (作者: PT88153, 时间: 1年前)

[ST50816](/hc/en-us/profiles/28620747421719-ST50816)  Is there any criteria regarding the operators also?

---

### 评论 #4 (作者: PT88153, 时间: 1年前)

[NL99431](/hc/en-us/profiles/22757429223831-NL99431)   Có bất kỳ quy tắc nào liên quan đến Người vận hành được sử dụng không?

---

### 评论 #5 (作者: CM45657, 时间: 1年前)

[../DM28368/[Commented] THE NEW  PYRAMID COUNT UPDATE.md](../DM28368/[Commented] THE NEW  PYRAMID COUNT UPDATE.md)   the question will be answed in the aboye post directed by thelink above

---

### 评论 #6 (作者: VP21767, 时间: 1年前)

One alpha can only in max 2 pyramids. For example min(rsk70_mfm2_usfast_prospect_specret_monthly, cap)+ts_rank(rsk59_squeeze_risk) count 2 pyramids and min(rsk70_mfm2_usfast_prospect_specret_monthly, cap)+ts_rank(rsk59_squeeze_risk+ts_regression(insd1_gvkey)) count 0 pyramids because there are 3 different datas are cap, insd1_gvkey and risk datacategory.

---

### 评论 #7 (作者: PN39025, 时间: 1年前)

Hi, pyramids are only counted when the alpha you submit has less than 2 pyramids. If there are more, they will not be counted.

---

### 评论 #8 (作者: CG95734, 时间: 1年前)

Hi, alphas with more than 3 pyramids will not count in completing any pyramaid but will be paid

---

### 评论 #9 (作者: HD25387, 时间: 1年前)

Thanks everyone for the clarification! So, if I understand correctly, only alphas using less than 2 datasets and fewer than 3 pyramids will be counted toward the pyramid? Just wanted to be sure before submitting.

---

### 评论 #10 (作者: NM74693, 时间: 1年前)

Even regular alphas that are not power pool selected?

---

### 评论 #11 (作者: AC63290, 时间: 1年前)

The "pyramid rule" in alpha submission on the WorldQuant BRAIN platform refers to a guideline that limits the number of similar or correlated alphas a participant can submit. This rule aims to encourage diversity in alpha strategies and prevent the submission of redundant models.

---

### 评论 #12 (作者: TP18957, 时间: 1年前)

To clarify the updated pyramid rules based on recent community feedback and the support article, an alpha will count toward pyramid completion only if it uses  **fewer than 2 datasets**  and  **fewer than 3 pyramids** . This means if your alpha relies on 3 or more datasets or contains more than 2 pyramid structures internally, it will still be evaluated and paid (if it performs well), but it  **won’t**  count toward your pyramid-building progress. Importantly, this rule applies regardless of whether the alpha is Power Pool–selected or a regular submission. Keeping the data and pyramid count minimal is now key for advancing the pyramid track.

---

### 评论 #13 (作者: SP39437, 时间: 1年前)

To clarify the updated pyramid rules based on recent community insights and the official support article: an alpha will only count toward pyramid completion if it uses fewer than 2 datasets and contains fewer than 3 internal pyramid structures. This means that if your alpha uses 3 or more datasets or more than 2 nested pyramids, it can still be evaluated and rewarded based on performance, but it won’t contribute to your pyramid-building progress. Notably, this rule holds regardless of whether the alpha is selected for the Power Pool or is a standard submission. The key takeaway is that in order to advance effectively along the pyramid track, it’s now essential to keep your dataset usage and internal pyramid complexity low.

Have you found any specific techniques or operator combinations that allow for creative yet minimalistic pyramids under the new constraints?

---

### 评论 #14 (作者: SK90981, 时间: 1年前)

Pyramids are only taken into account if your submitted alpha has fewer than two pyramids.  They won't be included if there are more.

---

### 评论 #15 (作者: AC63290, 时间: 1年前)

I couldn't find an official update on pyramid rules for alpha submissions this quarter. Typically, "pyramids" refer to the number of  **`pyramid()`  operator constructs**  used per alpha. Each nested or separate  `pyramid()`  call counts toward your pyramid count. If there have been recent changes, I recommend:

1. Reviewing the latest  **Brain platform release notes** .
2. Asking directly on the  **community forum**  or checking official  **WorldQuant announcements**  for new guidance.

Let me know if you'd like me to dig deeper.

---

### 评论 #16 (作者: AG14039, 时间: 1年前)

The new pyramid rule for alpha submission emphasizes structured dataset usage across tiers. To progress through the Genius pyramid and unlock higher levels (like Gold, Expert, Master, etc.), you now need to submit Alphas that use specific datasets associated with each tier segment. Submissions must be unique and relevant to those datasets, and each part of the pyramid lights up only when criteria are met for that dataset group. This encourages more diverse research and ensures a broader exploration of available data fields in your alpha development.

---

### 评论 #17 (作者: NT84064, 时间: 1年前)

Thank you for bringing up this question about the new pyramid rule — it’s an area where a lot of consultants, myself included, can benefit from more clarity and shared experiences. With the Genius scoring framework now more tightly integrated with pyramid completion, understanding how to build and maintain a well-structured pyramid is crucial to maximizing our submission quality and pass rates. By asking this, you’re giving everyone a chance to revisit their approach and ensure they aren’t missing important updates in the workflow. I really appreciate you opening up this discussion; it encourages knowledge-sharing and helps us collectively stay aligned with Brain’s best practices. I look forward to seeing more detailed explanations from experienced consultants and hope this sparks more tips on how to effectively plan and track pyramid progress. Thanks again for initiating such a relevant topic!

---

### 评论 #18 (作者: TP19085, 时间: 1年前)

To clarify the revised pyramid rules—based on recent community findings and the official guidance—an alpha only qualifies toward pyramid progression if it uses fewer than two datasets and includes no more than two internal pyramid structures. In other words, if your alpha incorporates three or more datasets or exceeds two nested pyramids, it may still perform well and receive recognition, but it won't count toward fulfilling pyramid-building milestones. This rule applies universally—whether your alpha is chosen for the Power Pool or submitted as a standard entry.

The main takeaway: progressing through the pyramid track now requires careful attention to simplicity in both dataset selection and structural design.

To adapt, many are exploring leaner alpha designs that prioritize creativity within tighter constraints. Have you discovered any specific operator combinations or techniques that help maintain expressiveness while staying compliant with these updated pyramid requirements? Minimalism doesn't have to mean compromise—it can drive smarter innovation.

---

