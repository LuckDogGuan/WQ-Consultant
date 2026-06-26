# HCAC 2025 AMA - Ask me Anything

- **链接**: [Commented] HCAC 2025 AMA - Ask me Anything.md
- **作者**: SJ72038
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

Hi everyone,

We are hosting an AMA (Ask Me Anything) session on the BRAIN forum for the HCAC 2025 competition. This is an opportunity for you to ask any questions you may have about the competition, and for our expert team to anything on your mind.

We understand that the competition can be challenging, and we want to ensure that you have the information and support you need to succeed.

Ask away!

---

## 讨论与评论 (32)

### 评论 #1 (作者: PP87148, 时间: 1年前)

"Hello,

I'm excited about the upcoming "Ask Me Anything" session! Could you please let me know the deadline for submitting questions?

---

### 评论 #2 (作者: CT60525, 时间: 1年前)

I have a question, if the alpha turnover is approximately 9% in IS, and the turnover rate when the OS exceeds 10%, will it be counted outside the OS?

---

### 评论 #3 (作者: EO24865, 时间: 1年前)

How can one build alphas from vector data fields

---

### 评论 #4 (作者: EO24865, 时间: 1年前)

How can one reduce self correlation and prod correlation

---

### 评论 #5 (作者: NM98411, 时间: 1年前)

Hi,can i ask why does this competition not use the same rule as previous competitions, which compared OS using merged alpha, but instead compare OS with individual small alphas?

---

### 评论 #6 (作者: KR61581, 时间: 1年前)

What is the weightage of OS and IS score

---

### 评论 #7 (作者: PN39025, 时间: 1年前)

Can you tell me how to reduce Tunover to match the competition while still keeping greater than 90% of the original alpha sharpness. And the other thing I'm wondering about is that the OS score will be updated in the middle of the competition like before, right?

---

### 评论 #8 (作者: CO99662, 时间: 1年前)

Competition dataset are so challenging as they have high prod correlation, any smoothing operators to help this?

---

### 评论 #9 (作者: LM22798, 时间: 1年前)

when you have high number of alphas does it guarantee a high OS score, unlike someone with low number of alphas?

---

### 评论 #10 (作者: MB13430, 时间: 1年前)

Hi,

In OS, if my alpha turnover exceeds 10% while IS turnover remains below 10%, will it be considered for scoring?

Thank You

---

### 评论 #11 (作者: MY83791, 时间: 1年前)

It is noticed that Aggregate parameters are heavily compromised while keeping the turnover low.

Please help.

---

### 评论 #12 (作者: VV63697, 时间: 1年前)

I want to know is it actually helpful for me to make low turnover alphas as mentioned by Nitish Maini in the opportunity webinar these alphas have a really bad OS performance so in a bigger pool it would be benefecial for the company but for an individual would it be helpful .

---

### 评论 #13 (作者: CT69120, 时间: 1年前)

[KR61581](/hc/en-us/profiles/17898299879319-KR61581)

The weighting between IS and OS scores will be 25%:75%. This means the final score will be calculated using the formula:

**0.25 * IS Score + 0.75 * OS Score**

For more details, you can refer to the following article:  [https://support.worldquantbrain.com/hc/en-us/articles/26743191705879-What-is-the-scoring-criteria-for-High-Capacity-Alphas-Competition](/hc/en-us/articles/26743191705879-What-is-the-scoring-criteria-for-High-Capacity-Alphas-Competition) .

---

### 评论 #14 (作者: UG81605, 时间: 1年前)

I have a question, isnt tuning alphas to have a higher sharpe, leads to overfitting? The merger scores are higher for higher sharpe ratios, so it might happen that many consultants trying to cross the threshold overfit unknowingly.

---

### 评论 #15 (作者: DK30003, 时间: 1年前)

Hi everyone, we are hosting an AMA (Ask Me Anything) session on the BRAIN forum for the HCAC 2025 competition. This is an opportunity for you to ask any questions you may have about the competition, and for our expert team to anything on your mind. We understand that the competition can be challenging, and we want to ensure that you have the information and support you need to succeed. Ask away

---

### 评论 #16 (作者: HT66349, 时间: 1年前)

[CT60525](/hc/en-us/profiles/18058151547159-CT60525) ,

>> If the alpha turnover is approximately 9% in IS, and the turnover rate when the OS exceeds 10%, will it be counted outside the OS?

Such Alphas will still be counted in the OS period. Their eligibility is based on the IS turnover only.

---

### 评论 #17 (作者: CT68712, 时间: 1年前)

Hi everyone! I'm super excited about the HCAC 2025 AMA session coming up! Even though I'm new to this competition, I've been diving into quantitative trading concepts and learning how to build effective alphas. I find it fascinating that the competition emphasizes minimizing turnover while maintaining sharpness. Can't wait to hear more insights on reducing turnover without sacrificing alpha quality. I've been trying to wrap my head around how to balance IS and OS scores effectively – the 25%:75% weightage is an interesting approach! Anyone else also trying to figure out the best strategies? Let's share our thoughts and tips!

---

### 评论 #18 (作者: PP87148, 时间: 1年前)

[HT66349](/hc/en-us/profiles/9313772453783-HT66349) ,

Thanks for the clarification on it.                                                                                                                                                                                                       .                                                                                                                                  .

---

### 评论 #19 (作者: NT32626, 时间: 1年前)

I believe that submitting alphas with very low turnover will not yield good results because it may fail to capture the continuous market trends. I would appreciate some suggestions for effective datasets that are suitable for this competition?

---

### 评论 #20 (作者: JL20361, 时间: 1年前)

Would you mind to sharing some suggestions on some of the good datasets to start with? That would be very helpful

---

### 评论 #21 (作者: VL52770, 时间: 1年前)

[EO24865](/hc/en-us/profiles/28027514858903-EO24865)  Vector data often contains multiple values within a day, so it should be processed with vector operators first. Depending on the dataset type, different vector operators may be applied, but I typically use  `vec_avg(data)`  as the initial approach. After that, other regular operators can be applied.

---

### 评论 #22 (作者: HT66349, 时间: 1年前)

Hi @ [NT32626](/hc/en-us/profiles/23713943380503-NT32626)  @ [JL20361](/hc/en-us/profiles/13126639293719-JL20361)

Since consultants now have different access to datasets, specific suggestions are hard to provide. However, I suggest starting with categories that have relatively lower  **data turnover** , such as analyst, model, and institutions.

For categories with inherently fast-changing data, you can still find Alphas with low turnover by using  **trade_when**  to identify trigger events or by combining with other data to reduce the overall turnover. For example,  **close**  may have high turnover,  **close/est_eps**  would have less turnover

---

### 评论 #23 (作者: AC63290, 时间: 1年前)

Thank you for organizing this AMA session. As we're currently in February 2025, I should note that I can only provide general guidance based on my knowledge cutoff of April 2024. I encourage participants to ask specific questions about competition rules, evaluation criteria, and technical requirements for optimal participation.

---

### 评论 #24 (作者: TT55495, 时间: 1年前)

Vector data typically contains multiple values within a day, so it should be processed with vector operators initially. Depending on the dataset, different operators might be suitable, but I usually begin with vec_avg(data) as the first step. Once that’s done, other standard operators can be applied.

---

### 评论 #25 (作者: PT27687, 时间: 1年前)

It’s great to see an AMA for the HCAC 2025 competition! This kind of engagement is so helpful for participants. I have a few questions about the judging criteria and any tips on what previous contestants found most beneficial. It would be awesome to gain more insights from the expert team!

---

### 评论 #26 (作者: NA18223, 时间: 1年前)

I've been diving into quantitative trading concepts and learning how to build effective alphas. I find it fascinating that the competition emphasizes minimizing turnover while maintaining sharpness. Can't wait to hear more insights on reducing turnover without sacrificing alpha quality. I've been trying to wrap my head around how to balance IS and OS scores effectively – the 25%:75% weightage is an interesting approach

---

### 评论 #27 (作者: DD24306, 时间: 1年前)

This AMA is a great opportunity! I have a few questions about the HCAC 2025 competition: What are some common challenges teams face, and how can we avoid them? Could you clarify the evaluation criteria and the weight given to factors like creativity, technical complexity, and final results? Lastly, do you have any advice for teams focusing on quantitative strategies?

---

### 评论 #28 (作者: AK40989, 时间: 1年前)

Could someone share what the final criteria for the OS (Out-of-Sample) evaluation ended up being? It would be helpful to understand how it impacted the results and strategies used in the competition!

---

### 评论 #29 (作者: SK90981, 时间: 1年前)

Come to the BRAIN forum for the HCAC 2025 AMA!  Set yourself up for victory by getting professional answers to all of your competition inquiries.

---

### 评论 #30 (作者: RB20756, 时间: 1年前)

The HCAC 2025 AMA session offers a great opportunity to discuss strategies for building effective alphas. Key topics include balancing IS and OS scores, minimizing turnover while maintaining sharpness, and leveraging datasets with lower data turnover. Participants have raised important questions about vector data processing, alpha correlation reduction, and dataset selection. Engaging in this discussion can help refine approaches to competition challenges and improve overall alpha performance.

---

### 评论 #31 (作者: DK30003, 时间: 1年前)

I have a question, if the alpha turnover is approximately 9% in IS, and the turnover rate when the OS exceeds 10%, will it be counted outside the OS?

---

### 评论 #32 (作者: DK30003, 时间: 1年前)

Hi,can i ask why does this competition not use the same rule as previous competitions, which compared OS using merged alpha, but instead compare OS with individual small alphas?

---

