# Can We Adjust the Alpha Evaluation in Combined Power Pool Alpha Performance by modifying 'PowerPoolSelected' Tags?

- **链接**: Can We Adjust the Alpha Evaluation in Combined Power Pool Alpha Performance by modifying PowerPoolSelected Tags.md
- **作者**: FZ60707
- **发布时间/热度**: 1年前, 得票: 26

## 帖子正文

Can we adjust the Alpha of the Combined Power Pool Alpha Performance evaluation ourselves? That is, can we adjust the alphas for the evaluation by adding or removing a tag called 'PowerPoolSelected'? Or does it mean that the alphas of all submissions to PPAC go into the evaluation?

---

## 讨论与评论 (10)

### 评论 #1 (作者: DN41247, 时间: 1年前)

Yes, we can tag/untag Alphas that match Powerpool Alpha, by the tag called 'PowerPoolSelected'. But all Alphas submitted to the Power pool will be considered for correlation check ( <0.5 or sharpe better than 10% to be passed)

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

HiFZ60707, I think tagging and removing the name will not affect the performance of the combo power pool. Last quarter, I also removed the tag but the power pool points were still calculated.

---

### 评论 #3 (作者: FZ60707, 时间: 1年前)

PN39025Hello, thank you for your response. You mentioned that you removed "PowerPoolSelected," but it still contributed to the calculation of the Combined Power Pool Alpha Performance. I’d like to confirm: Are you certain that you deletedalltags containing "PowerPoolSelected"? If so, and the Combined Power Pool Alpha Performance still appears (with no "PowerPoolSelected" tags present), then removing the tags indeed has no effect on it.Could you please double-check the alpha data up toMay 30thto verify this? If there are truly no "PowerPoolSelected" tags but the Combined Power Pool Alpha Performance still exists, then deleting the tags does not impact it. I’d appreciate it if you could confirm this once more.

---

### 评论 #4 (作者: PN39025, 时间: 1年前)

I confirmed that I deleted all the cards but I'm not sure when it was selected for the combo calculation as it could have been calculated before I deleted all the cards.

---

### 评论 #5 (作者: DH50715, 时间: 11个月前)

Only alphas officially selected by the system are included in the PPAC evaluation. The tag is system-assigned, not user-controlled.

---

### 评论 #6 (作者: AK40989, 时间: 11个月前)

Thanks, this clears it up. So just to confirm the “PowerPoolSelected” tag is system-assigned and removing it manually doesn’t affect whether an alpha is included in the Combined Power Pool evaluation,

---

### 评论 #7 (作者: NT84064, 时间: 10个月前)

From current platform behavior, the Combined Power Pool Alpha Performance metric is calculated using the subset of alphas that are explicitly tagged asPowerPoolSelectedas of the cutoff date for the quarter. This means you can influence which alphas are included in that combined evaluation by adding or removing the tag before the deadline. It does not automatically include all submissions to PPAC unless those submissions are also tagged. That said, tagging decisions should be strategic — adding a weak or unstable alpha to your Power Pool can dilute the combined Sharpe, while removing a strong one can reduce it. The best approach is to regularly review your tagged set, backtest the combined portfolio effect, and lock in the final selection before the official cutoff.

---

### 评论 #8 (作者: NT84064, 时间: 10个月前)

Thanks for asking this — it’s a critical clarification for anyone aiming to optimize their Combined Power Pool Alpha Performance score. Many consultants might assume that all PPAC submissions are automatically counted, but your question highlights the importance of understanding the tagging mechanism. By raising this point, you’re helping others realize that thePowerPoolSelectedtag is not just an administrative label, but a direct performance lever for Genius level calculations. I appreciate that you brought this up in a straightforward way, as it invites those with first-hand testing experience to share confirmation or nuances, making it easier for everyone to fine-tune their tagging strategy.

---

### 评论 #9 (作者: LB76673, 时间: 9个月前)

Youcannot fully controlthe Combined Power Pool Alpha Performance (CPAP) metric just by manually tagging or untagging alphas. ThePowerPoolSelectedtag is mainly your way of nominating which alphas you want considered for the PowerPool Alpha Competition (PPAC). Once the quarter closes, the system takes asnapshotof your tagged set, applies internal filtering, and then uses that pool to compute your CPAP. So it’s not the case that every alpha you ever submitted to PPAC will count forever; only the alphas that are actively taggedPowerPoolSelectedat the snapshot date are considered. At the same time, untagging an alpha after it’s already been “locked in” for that quarter won’t remove it from the evaluation until the next cycle.

---

### 评论 #10 (作者: RK48711, 时间: 9个月前)

Exactly, you’ve got it. The “PowerPoolSelected” tag is assigned automatically by the system, and removing it manually won’t change whether an alpha counts toward the Combined Power Pool evaluation.

---

