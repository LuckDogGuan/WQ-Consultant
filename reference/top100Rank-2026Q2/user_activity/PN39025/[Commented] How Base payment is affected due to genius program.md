# How Base payment is affected due to genius program

- **链接**: [Commented] How Base payment is affected due to genius program.md
- **作者**: ST37368
- **发布时间/热度**: 1年前, 得票: 12

## 帖子正文

Hello everyone,

Is the Genius program going to affect the base payment? I am in the gold level as per the Q4 genius result but I have a good value factor and in the last 3 days I can see a drastic drop in my base payment.

Can anyone please clarify on this?

---

## 讨论与评论 (22)

### 评论 #1 (作者: NT63388, 时间: 1年前)

Hello @ [ST37368](/hc/en-us/profiles/4927283487127-ST37368) ,

The base payment is not affected by the Genius program; this was clearly mentioned in the webinar.

However, the base payment is calculated based on comparisons with other Consultants. For instance, due to the influence of Genius levels, many Consultants are now focusing on "Pyramid theme multipliers" (currently offering up to x2). If you are not working in line with this approach, your base payment may decrease significantly.

I hope this clarifies your concern!

---

### 评论 #2 (作者: PP87148, 时间: 1年前)

Hi  [ST37368](/hc/en-us/profiles/4927283487127-ST37368) ,

As  [NT63388](/hc/en-us/profiles/6348096761239-NT63388)  mentioned, it was clearly stated during the opportunity webinar held on 7th Jan 2025 that the Genius Program levels are solely intended to determine quarterly payments and will not impact any other payments, such as base or referral payments.

However, with the recent disclosure of levels, the pyramid multipliers have been adjusted. This change introduces the possibility that fellow consultants submitting high-quality alphas into the pool may earn higher payments as a result.

---

### 评论 #3 (作者: RB25229, 时间: 1年前)

Hi  [ST37368](/hc/en-us/profiles/4927283487127-ST37368) ,

The base payment is not affected by the Genius program; that is clearly mentioned in the FAQs.

but try to reduce correlation it might improve your value factor.

---

### 评论 #4 (作者: PN39025, 时间: 1年前)

Hi  [ST37368](/hc/en-us/profiles/4927283487127-ST37368) , It won't affect your daily payout, but if you reach low level you won't be able to access much good data and make many themes with high coefficient and good performance. Try to improve your genius level

---

### 评论 #5 (作者: RB20756, 时间: 1年前)

Hi, 
Base or referral payment is not going to be effect by Genius program as mentioned in the webinar. It is only going to effect your quarterly payment.

---

### 评论 #6 (作者: AB15407, 时间: 1年前)

My base payment has also decreased significantly.
In addition to the reasons others have mentioned, I believe it’s also because Consultants at the Expert level and above can create Super-Alpha using Alphas from other Consultants. This makes it easier and more efficient to create high-quality Super-Alphas, which significantly reduces the base payment for those in the Gold rank.

---

### 评论 #7 (作者: AC63290, 时间: 1年前)

The Genius program does influence the base payment, as rankings and levels are tied to contributions and performance metrics. While value factor is an important indicator of the quality of your alphas, the program also evaluates other criteria such as tie breakers and overall participation in determining your level.

If your base payment has dropped drastically despite good value factors, it might be due to a shift in how contributions are weighted under the Genius program. It’s recommended to review the program's updated guidelines or reach out to support for clarification on the exact factors impacting your payment. Stay proactive! 🚀

---

### 评论 #8 (作者: AT42545, 时间: 1年前)

Hello  [ST37368](/hc/en-us/profiles/4927283487127-ST37368)

I have also notice the same thing since a few days, used to get around 10 dollar per day before the genius result now getting 2-3.

---

### 评论 #9 (作者: UG81605, 时间: 1年前)

The value factor might have refreshed, hence the less base payment. Usually this is the right time to refresh value factors.

---

### 评论 #10 (作者: TL60820, 时间: 1年前)

The Genius program does not have an impact on daily payouts. From my personal experience, your daily payout is primarily determined by factors such as QualityFactorScaled, QuantityFactorScaled, ValueFactor, and SelfGrowth. If you can consistently maintain a specific level of IS performance for submissions, as outlined in your post, it is unlikely that your daily payout will fluctuate significantly. However, it’s important to note that even a single day of not meeting these standards can result in a noticeable drop in your payout. Therefore, maintaining a steady performance over time is crucial for achieving consistent results.

---

### 评论 #11 (作者: MB13430, 时间: 1年前)

Hello  [ST37368](/hc/en-us/profiles/4927283487127-ST37368)

The base payment is not influenced by the Genius program. It solely depends on the alpha quality and your current value factor.

---

### 评论 #12 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #13 (作者: NM98411, 时间: 1年前)

How do you construct multi-factor models that integrate ESG (Environmental, Social, Governance) factors, and what methods do you use to assess the impact of ESG factors on long-term portfolio performance?

---

### 评论 #14 (作者: deleted user, 时间: 1年前)

A lower standard deviation (volatility) of returns will help improve the Sharpe ratio. This can be achieved by diversifying the portfolio across different assets or asset classes, managing position sizing, or using hedging strategies to reduce overall risk.

---

### 评论 #15 (作者: PN39025, 时间: 1年前)

Hi  [NM98411,](/hc/en-us/profiles/5646822985623-NM98411)  [TK95999](/hc/en-us/profiles/18243496991767-TK95999)  , are you possibly going off-topic from the original post's question? I feel like your answer is not very relevant to the purpose of the post.

---

### 评论 #16 (作者: KP26017, 时间: 1年前)

Sau đây là mã để bạn có thể lấy thông tin từ bảng xếp hạng để phân tích và thay đổi chiến lược của mình.

```
import time import pandas as pd def leaderboard(s, limit=100, offset=0):     """     Hàm lấy bảng xếp hạng cho cuộc thi và trả về dưới dạng DataFrame.     """     max_try = 5     leader_list = []     for x in range(offset, limit + offset, 100):         for _ in range(max_try):             result = s.get(                 f"https://api.worldquantbrain.com/consultant/boards/genius?limit=100&offset={x}&aggregate=user"             )             if 'results' in result.json():                 break             else:                 time.sleep(5)         leader_list.extend(result.json()['results'])     if not leader_list:         return pd.DataFrame()     return pd.DataFrame(leader_list) leaderboard_table = leaderboard(s,limit = 5000,offset = 0) leaderboard_table
```

---

### 评论 #17 (作者: KP26017, 时间: 1年前)

Depending on when alpha stops working. It will not be counted in the genius and value factor or weight if it is before considering those factors.

---

### 评论 #18 (作者: TN48752, 时间: 1年前)

It sounds like the system you're talking about is designed in such a way that even if someone does their best and completes the maximum number of pyramids available to them, they won't reach the Grandmaster level unless they have access to all 107 pyramids. The 60 pyramids that are unavailable could be an obstacle to progression to that top tier.

---

### 评论 #19 (作者: NM98411, 时间: 1年前)

How do you implement differentiable programming for end-to-end portfolio risk modeling, and what are the advantages of automatic differentiation in computing risk sensitivities?

---

### 评论 #20 (作者: MA97359, 时间: 1年前)

Genius levels impact quarterly payouts, access to operators and data fields, login timings, and SuperAlpha selection. However, base payouts remain unaffected, as confirmed by WorldQuant.

---

### 评论 #21 (作者: AK40989, 时间: 1年前)

Your question about the impact of the Genius program on base payments is quite relevant, especially with the recent changes in focus among consultants. It seems that while the program itself doesn't directly affect base payments, the competitive landscape it creates can influence how payments are calculated based on performance relative to others.

---

### 评论 #22 (作者: DK30003, 时间: 1年前)

How do you construct multi-factor models that integrate ESG (Environmental, Social, Governance) factors, and what methods do you use to assess the impact of ESG factors on long-term portfolio performance?

---

