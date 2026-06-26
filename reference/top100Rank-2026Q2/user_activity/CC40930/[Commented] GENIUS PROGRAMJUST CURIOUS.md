# GENIUS PROGRAM;JUST CURIOUS!

- **链接**: [Commented] GENIUS PROGRAMJUST CURIOUS.md
- **作者**: PO51191
- **发布时间/热度**: 1年前, 得票: 9

## 帖子正文

The onset of the genius programme has provided a unique opportunity for consultants to scale up their research and get a chance to earn some decent quarterly payments. Even though most of the questions pertaining the programme have been answered in various sessions,I still have some:

1.The provisional leaderboard ranks users based on number of alpha submissions.Is that alone enough or the pyramid count carries much more weight?

2.In the event that some alphas get decommissioned,what happens to the distinct number of operators/fields used in the tie breaker?Does it also reduce the pyramid count?

3.Hypothetically;I submit an alpha that covers the following pyramids: AMR/D1/PV *1.3 AMR/D1/Fundamental *1.8 AMR/D1/Model *1.8. The final pyramid theme multiplier is 1.3. How do they arrive at 1.3 and how relevant is this multiplier in base and quarterly payments(Value and weight factors)?

4.With regards to the quarterly payments for the fourth quarter of 2024(Q4 2024),will the payment reflect the genius compensation plan in the next payment cycle or will the plan start in Q1 2025? If not,why?

I hope someone will address these concerns. Thanks!

---

## 讨论与评论 (15)

### 评论 #1 (作者: DP11917, 时间: 1年前)

Hi, you don't need to care about the current leaderboard because they are sorted by the number of alphas submitted, just wait for the genius results

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

[Hi PO51191](/hc/en-us/profiles/17394561981463-PO51191) ,The current ranking is ranked by signal. If you want to know in detail what level you can be at, you should call the leaderboard api to rank the criteria and you will know your position.

---

### 评论 #3 (作者: PN39025, 时间: 1年前)

Here is the code so you can get information from the leaderboard to analyze and change your strategy.

```
import timeimport pandas as pddef leaderboard(s, limit=100, offset=0):    """    Function gets leaderboard for competition and returns it as a DataFrame.    """    max_try = 5    leader_list = []    for x in range(offset, limit + offset, 100):        for _ in range(max_try):            result = s.get(                f"https://api.worldquantbrain.com/consultant/boards/genius?limit=100&offset={x}&aggregate=user"            )            if 'results' in result.json():                break            else:                time.sleep(5)        leader_list.extend(result.json()['results'])    if not leader_list:        return pd.DataFrame()    return pd.DataFrame(leader_list)leaderboard_table = leaderboard(s,limit  = 5000,offset = 0)leaderboard_table
```

---

### 评论 #4 (作者: PN39025, 时间: 1年前)

Depending on when alpha stops working. It will not be counted in the genius and value factor or weight if it is before considering those factors.

---

### 评论 #5 (作者: PN39025, 时间: 1年前)

Hi  [Hi PO51191](/hc/en-us/profiles/17394561981463-PO51191) ,As WQ has clearly stated, the 4th quarter is still calculated according to the old rules of value factor and weight. Starting from the 1st quarter of 2025, it will be calculated according to genius combined with value factor and weight.

---

### 评论 #6 (作者: PN39025, 时间: 1年前)

They will take the lowest theme factor to calculate for you. And it only applies to daily payments, not quarterly payments.

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

Leaderboard Ranking (Alpha Submissions vs. Pyramid Count):

The provisional leaderboard ranks consultants based on the number of alpha submissions, but the pyramid count also plays a significant role. The Pyramid system evaluates the quality and depth of the research, which gives a clearer picture of a consultant's performance. The pyramid count generally carries more weight because it reflects the consistency and effectiveness of the alphas submitted. A higher number of pyramids generally leads to better chances for higher ranks and more compensatory rewards.
Impact of Decommissioned Alphas on Tie Breakers:

If an alpha gets decommissioned, it typically removes its associated operators/fields from the tie-breaker calculation. This will impact the distinct number of operators/fields and may lower the pyramid count as well, depending on how significant the decommissioned alpha was in terms of your overall pyramid structure. The tie-breaker calculation ensures that the most relevant and operational alphas are taken into account for rankings, so decommissioned alphas will have a negative impact on both your pyramid count and performance.
Pyramid Theme Multiplier:

When you submit an alpha covering multiple pyramids, the final pyramid theme multiplier (e.g., 1.3) is determined based on the weighting of the different pyramids involved. Each pyramid type (e.g., AMR/D1/PV, AMR/D1/Fundamental, AMR/D1/Model) has its own impact on the overall multiplier. The 1.3 multiplier likely reflects the combined impact and effectiveness of the pyramids, weighted by their importance or complexity. This multiplier is used to adjust the value factor and the weight factor in terms of base and quarterly payments. The multiplier directly affects how your alpha contributions are measured, influencing your compensation.

---

### 评论 #8 (作者: KN18968, 时间: 1年前)

[PN39025](/hc/en-us/profiles/1532011933942-PN39025)

"As WQ has clearly stated, the 4th quarter is still calculated according to the old rules of value factor and weight. Starting from the 1st quarter of 2025, it will be calculated according to genius combined with value factor and weight."

Is this information still correct? Today's webinar reported that payment quarer Q4/2024 is calculated based on genius level.

---

### 评论 #9 (作者: PN39025, 时间: 1年前)

Hi  [KN18968](/hc/en-us/profiles/27485747350295-KN18968) , there is a new announcement that Q4 2024 will still be calculated according to the old rules. And the level of Q4 will be calculated for Q1 2025. For the value factor and weight of alpha submitted in Q1, it will be calculated for the quarty in Q1.

---

### 评论 #10 (作者: TN33707, 时间: 1年前)

Your inquiries delve deep into the mechanics of the programme and highlight critical aspects that could influence participant strategy significantly.

---

### 评论 #11 (作者: TN44329, 时间: 1年前)

These are truly insightful inquiries that delve into the core mechanics of the programme. Exploring these questions further will surely enhance clarity for all the participants involved.

---

### 评论 #12 (作者: DK30003, 时间: 1年前)

When you submit an alpha covering multiple pyramids, the final pyramid theme multiplier (e.g., 1.3) is determined based on the weighting of the different pyramids involved. Each pyramid type (e.g., AMR/D1/PV, AMR/D1/Fundamental, AMR/D1/Model)

---

### 评论 #13 (作者: PT27687, 时间: 1年前)

It seems like you have some very insightful questions regarding the genius program that could clarify a lot for participants. Understanding how the leaderboard rankings are determined and how the multipliers work could really help strategize submissions effectively. It might be beneficial to reach out to someone who handles the program directly, as they would have the most accurate information on these points.

---

### 评论 #14 (作者: QN13195, 时间: 1年前)

These are insightful questions that highlight both technical and structural aspects of the programme. Having clarity on how ranking factors are weighted and how potential decommissioning impacts calculations would indeed be beneficial for all contributors.

---

### 评论 #15 (作者: CM46415, 时间: 2个月前)

Good structured questions on GENIUS mechanics. Pyramid weighting likely dominates submissions, decommissioning reduces active metrics, and multipliers are normalized signals. Quarterly payout changes are typically applied prospectively, not retroactively.

---

