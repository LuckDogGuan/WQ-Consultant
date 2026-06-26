# Highest SHARPE(15.69) and FITNESS(9.34) I have ever seen

- **链接**: [Commented] Highest SHARPE1569 and FITNESS934 I have ever seen.md
- **作者**: KG79468
- **发布时间/热度**: 9个月前, 得票: 6

## 帖子正文

Look at the performance of this alpha. It has out of the world fitness and sharpe and even its returns/ drawdown ratio. Also the weight is uniformly distributed .Only thing bad is its turnover. Can anyone help , how can I reduce its turnover without affecting the alpha performance

![图片](images/img_40c791740d.png)

---

## 讨论与评论 (8)

### 评论 #1 (作者: JC84638, 时间: 9个月前)

Hi,  [KG79468](/hc/en-us/profiles/30876459653015-KG79468) . Is this really a Regular Alpha? The most straightforward way is to lower Turnover using MaxTrade and Decay settings. But in most cases, reducing Turnover also lowers Sharpe—that’s unavoidable. The real question is: how much should you reduce it? I don’t think it’s something to worry too much about, because usually when Turnover goes down, Margin goes up, which is a good thing. And if it’s a D0 Alpha, it will naturally come with higher Turnover. If you can share which dataset this data belongs to, I’ll be able to give a more specific judgment.(jzc

---

### 评论 #2 (作者: CL49716, 时间: 9个月前)

trying  some target tvr opr?like ts_target_tvr_decay... it may loss some signal.

---

### 评论 #3 (作者: AC75253, 时间: 9个月前)

you can reduce the turnover by increasing decay. and can you tell which dataset you are using in this alpha?

---

### 评论 #4 (作者: NL99431, 时间: 9个月前)

Hi  [KG79468](/hc/en-us/profiles/30876459653015-KG79468)  , you can increase the decay or use the ts_target_tvr_hump operator to reduce turnover. Of course, Sharpe and fitness will also decrease, and could you capture the results after submitting this alpha? I want to know the outcome.

---

### 评论 #5 (作者: KG79468, 时间: 9个月前)

you can feel free to comment and share yours performance if it has better ratios than these

---

### 评论 #6 (作者: KG79468, 时间: 9个月前)

Hi NL99431, AC75253, CL49716, JC84638 you can check out my new community post, there I have posted more about this alpha

---

### 评论 #7 (作者: JN96079, 时间: 9个月前)

Hey,  [KG79468](/hc/en-us/profiles/30876459653015-KG79468) , you can try  ***hump*** ,  ***hump decay*** , or the more specific operator,  ***ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)*** , which helps you designate the value of turnover you want for your alpha to have.

---

### 评论 #8 (作者: RP41479, 时间: 9个月前)

Using target TVR operators like  **ts_target_tvr_decay**  can sometimes reduce signal strength, as they smooth or adjust returns to match a target volatility, potentially damping the original alpha signal.

---

