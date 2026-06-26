# Effect of Tag Changes on Combined PowerPool Alpha Performance

- **链接**: [Commented] Effect of Tag Changes on Combined PowerPool Alpha Performance.md
- **作者**: RS70387
- **发布时间/热度**: 1年前, 得票: 53

## 帖子正文

I’ve been curious about how the  **'PowerPoolSelected'**  tag affects the Combined PowerPool Alpha Performance. Specifically, if I tag or untag an Alpha using this label, does it change whether that Alpha is counted in the  **Combined PowerPool performance**  evaluation?

From previous posts and discussions, it seems that tagging was mainly used for PowerPool competition eligibility, but it’s not entirely clear if it still has any impact on the Combined PowerPool Alpha Performance metric going forward.

Has anyone tried removing the tag and noticed whether the Alpha still contributes to the Combined score? Would love to hear from those who have tested this or received clarification, just want to make sure I understand how this works going into the quarter.

---

## 讨论与评论 (9)

### 评论 #1 (作者: PN39025, 时间: 1年前)

According to the seminar I heard yesterday, when you remove the tag, it will not be counted in the combo power pool performance and when you reassign the tag, it will not be counted anymore. Last month, I also removed all the tags but still got points, I think because the time I removed the tag, the combo power pool points were already counted..

---

### 评论 #2 (作者: FZ60707, 时间: 1年前)

[PN39025](/hc/en-us/profiles/1532011933942-PN39025)    You said:when you reassign the tag, it will not be counted anymore. Really???

When I removed the tag and immediately added it again, will this ppac never be included in the calculation of the Combined PowerPool Alpha Performance?

If that's true, it would be extremely inconvenient.

---

### 评论 #3 (作者: HD25387, 时间: 1年前)

Great question — this definitely needs clearer documentation. Based on what I've observed and what PN39025 mentioned,  **timing is crucial** . Once an Alpha is  **removed from PowerPoolSelected** , it likely  **stops contributing to the Combined PowerPool score** , and re-tagging it may  **not reinstate its contribution immediately (or at all)**  for that cycle. It seems the system locks inclusion based on tag status at a certain cutoff time. Until we get official confirmation, safest practice is to  **finalize your tags at least 24–48 hours before month-end**  and avoid toggling them right before performance windows close.

---

### 评论 #4 (作者: AK40989, 时间: 11个月前)

Its still a bit fuzzy for me. if I remove and then re-add the PowerPoolSelected tag, that alpha might not get counted again for the Combined score in the same month?  Would love to hear if anyone’s tested this more systematically.

---

### 评论 #5 (作者: NT84064, 时间: 10个月前)

The  `PowerPoolSelected`  tag historically played a dual role — one in signaling eligibility for certain competitions and another in defining the subset of alphas aggregated for the Combined PowerPool Alpha Performance metric. However, platform updates in recent quarters may have decoupled the tag’s influence from the calculation process. In many current setups, the Combined PowerPool performance is determined by the platform’s internal selection rules rather than the consultant’s manual tagging, meaning that removing the tag may not impact inclusion if the alpha still meets the eligibility and ranking criteria. That said, some consultants have reported that the tag still affects certain visibility and reporting aspects in the dashboard. The safest approach is to test by running a before/after comparison on a controlled set of alphas and observing whether the Combined score changes. Documentation updates or moderator clarification could also help confirm the current operational link between tags and combined metrics.

---

### 评论 #6 (作者: SC43474, 时间: 10个月前)

I conducted a small test last month by removing the  `PowerPoolSelected`  tag from two alphas and then reapplying it after a short interval. Based on the results, those alphas did not appear to be included again in the Combined PowerPool score for that cycle. While this may be coincidental, it suggests that once an alpha is untagged, the system may effectively “lock” its inclusion for that period. It would be helpful if WorldQuant could provide an official clarification on this point, as adjusting tags near month-end currently seems uncertain and potentially risky.

---

### 评论 #7 (作者: LB76673, 时间: 9个月前)

The “PowerPoolSelected” tag historically mattered mainly for competition eligibility, but for the  **Combined PowerPool Alpha Performance (CPAP)**  metric, the platform logic is not directly tied to whether you manually tag or untag an alpha. Instead, CPAP is calculated based on the set of alphas the system recognizes as part of your PowerPool at the snapshot date. If you remove the tag, the alpha may still contribute if it meets the internal criteria (for example, if it was already included in your PowerPool submission cycle), but tagging ensures clarity and avoids the risk of exclusion.

---

### 评论 #8 (作者: RK48711, 时间: 9个月前)

Curious if removing the ‘PowerPoolSelected’ tag affects whether an alpha contributes to the Combined PowerPool performance. It was once tied to competition eligibility, but does it still influence the aggregated score? Has anyone experimented with untagging an alpha and noticed any change in how it factors into the combined metric?

---

### 评论 #9 (作者: JN96079, 时间: 9个月前)

Yes, tagging and untagging alphas for the PowerPool theme before or after submission affects the  **Combined PowerPool Performance** evaluation. Even from time to time, when the announcements of the toppers for the theme are yet to be announced, you will find that they usually suggest you make  **at least 10 tags of PowerPool alphas**  for the evaluation. So, yes, choose the best alphas for the PowerPool theme evaluation before the last day of the month.

Cheers!

---

