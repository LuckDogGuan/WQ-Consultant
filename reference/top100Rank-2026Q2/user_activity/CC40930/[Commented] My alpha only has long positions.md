# My alpha only has long positions

- **链接**: [Commented] My alpha only has long positions.md
- **作者**: HJ39505
- **发布时间/热度**: 3年前, 得票: 2

## 帖子正文

As I wrote in the title, my alpha longs only(e.g., long count 2000, short count 0), even though I neutralized it. I did not neutralize it myself, I used the market neutralize option in the settings.

How is this possible? Shouldn't the weight sum to zero after the neutralization?

Thanks for your help in advance!

---

## 讨论与评论 (7)

### 评论 #1 (作者: AS34454, 时间: 3年前)

It would help if you could share details about the Alpha expression. Some operators could have led to this scenario.

---

### 评论 #2 (作者: HJ39505, 时间: 3年前)

I'm not quite sure if it would be okay to share the whole Alpha(I don't mind, but worried that it might violate community rule), but these are the options and the Alpha expression that I wrote.

UNIVERSE=TOP3000

DELAY=1

NEUTRALIZATION=Market

DECAY=4

TRUNCATION=0.08

PASTEURIZATION=On

NAN HANDLING=Off

ts_arg_max(split, window) > split ? 1 : 0

---

### 评论 #3 (作者: PK56323, 时间: 3年前)

The split field is the key here. Stock splits are very rare events and for most of the instruments, it is always equal to 1. So, if you look at the cross-section i.e. across instruments, for most days you will see all 1's. Neutralizing them across any group(not just market) and irrespective of you use it in settings or using group_neutralize in alpha expression, will give you all 0's and 0 is counted as long. Hence, sum of alpha values post-neutralization is still 0.

---

### 评论 #4 (作者: HJ39505, 时间: 3年前)

Oh, so 0 is counted as long. Thanks!

---

### 评论 #5 (作者: XL31477, 时间: 1年前)

**Yeah,  [HJ39505](/hc/en-us/profiles/8731439525527-HJ39505) , that's right. As  [PK56323](/hc/en-us/profiles/1521105688502-PK56323)  explained, since 0 is counted as long in this case, even after the market neutralization, you end up with only long positions showing. It's due to the nature of the split field where most values are 1 and neutralizing them results in 0s being treated as long. That's why the weight sum doesn't work as you expected. Hope this clears it up for you.**

---

### 评论 #6 (作者: DK20528, 时间: 1年前)

Yes, ideally, after using market neutralization, the weight sum should be close to zero. If you're still seeing only long positions with no shorts, it's possible that the neutralization method in your settings isn't fully balancing the positions, or there could be an issue with how the model is interpreting or applying the neutralization. Double-check the neutralization settings (e.g., the specific factor or method used) to ensure it's properly applied. If the problem persists, it might be worth reviewing the underlying data or model logic to identify any potential issues.

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

The market neutralization option helps reduce factor exposure but does not guarantee a perfectly balanced set of long and short positions. The key takeaway is that neutralization removes systematic factor exposure, not necessarily the imbalance between long and short positions. To achieve a balanced long-short portfolio, you may need to experiment with custom neutralization or adjust your alpha signal more directly (e.g., by using ranking or quantiles).

---

