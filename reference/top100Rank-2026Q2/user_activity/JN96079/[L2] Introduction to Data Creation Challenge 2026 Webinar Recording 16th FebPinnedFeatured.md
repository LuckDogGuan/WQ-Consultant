# Introduction to Data Creation Challenge 2026 Webinar Recording (16th Feb)PinnedFeatured

- **链接**: [L2] Introduction to Data Creation Challenge 2026 Webinar Recording 16th FebPinnedFeatured.md
- **作者**: Aziz Ansari
- **发布时间/热度**: 3 months ago, 得票: 68

## 帖子正文

This is the webinar recording of the “Introduction to Data Creation Challenge 2026” held on 16 February 2026.

The video has to be taken down in 5 days, so please watch it quickly and ask any questions in the comments.

The recording is shorter than the live webinar. Attendees of the live webinar get access to live Q&A

http://play.vidyard.com/ck81tGi6H1wpzwmiJYRfWr.html

---

## 讨论与评论 (20)

### 评论 #1 (作者: CS51388, 时间: 3 months ago)

nice the recording has really help alot thanks

---

### 评论 #2 (作者: YQ51506, 时间: 3 months ago)

Thanks for sharing the recording!👍

---

### 评论 #3 (作者: GC13416, 时间: 3 months ago)

I’m participating in DCC2026 and validating alphas built from my uploaded user-defined fields. I’m seeing these failures: LOW_SUB_UNIVERSE_SHARPE (e.g., 1.05 < 1.30), “simulation doesn’t match current IS period,” IS_LADDER_SHARPE (e.g., 0 < 1.58), and USER_DEFINED_FIELDS (cannot be submitted as regular alpha). Could you confirm whether all of these must be resolved for DCC2026 final evaluation, or whether some are only relevant to standard production alpha submission? Our understanding is that for DCC we should focus on dataset/script quality and use these alphas only for validation. Our current fix path is to rebuild the field to match the current IS window, avoid any future-looking fill, and then re-simulate with causal transformations to improve sub-universe and ladder robustness. Please advise which checks are mandatory in DCC and what the recommended best-practice verification workflow is for user-defined-field participants.

---

### 评论 #4 (作者: WL13229, 时间: 3 months ago)

[GC13416](/hc/en-us/profiles/34962957450775-GC13416)

no test is mandatory

---

### 评论 #5 (作者: PK69806, 时间: 3 months ago)

The video is good but please explain full process how to submit alphas in DDC

---

### 评论 #6 (作者: VG88979, 时间: 3 months ago)

ok, so you are saying no test is mandatory. This is true. But what one more thing we are getting is that, “simulation doesn’t match current IS period,” and this showed up when I used 15-days period while creating datafield, but in the webinar recording he told that datafield is to be created for a 2-year long period, i.e. , from 2021-01-01 to 2022-12-31. So, please confirm this time duration.

---

### 评论 #7 (作者: ME83843, 时间: 3 months ago)

what a recording!
am fascinated to be part of this great community.

---

### 评论 #8 (作者: LD27384, 时间: 3 months ago)

I only have data available for 2021–2022; there is no data for later years.

How will the platform fill in the missing data going forward and compute the out-of-sample (OS) score?

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #9 (作者: JN96079, 时间: 3 months ago)

By the way, it's not clear whether we can submit the alpha for the user-defined data fields. The errors are very clear;

**1. The simulation doesn't match the current IS period. Please clone this alpha and re-simulate.**

- Here I tried to use a 5-year period to retrieve data in the datafield creation, and the API on my side seems to suggest and recommend that I can only retrieve information for 2 years max, since it's the maximum time it's allowed to use, i.e., 2021-01-01 to 2022-12-31

**2. Alphas containing user defined fields and can't be submitted.**

- Here, I did not try to fix since it's very clear 🙂

Therefore, if we or I can get guidance on whether it's possible to submit an alpha, I'll be obliged, since the two failures are the only obstacles to submitting my alphas I have created so far.

---

### 评论 #10 (作者: XL27393, 时间: 3 months ago)

Thank you so much for providing the replay. It would be even better if subtitles could be added to aid understanding. Currently, machine translation only provides a partial understanding.

---

### 评论 #11 (作者: WT50907, 时间: 3 months ago)

Running the demo DataCreationCompetition_workflow, The uploaded created dataframes were successful; however, I couldn't simulate using the created datafields. The error is attempting to use unknow variable.

---

### 评论 #12 (作者: GC13416, 时间: 3 months ago)

When I have multiple different ideas, can I submit multiple notebooks?@WL13229

---

### 评论 #13 (作者: WL13229, 时间: 3 months ago)

[JN96079](/hc/en-us/profiles/25468856195607-JN96079)

just tag the Alpha then you will see a score on the leaderboard

---

### 评论 #14 (作者: WL13229, 时间: 3 months ago)

[WT50907](/hc/en-us/profiles/30843911205399-WT50907)

please double check the filed name you created and simulate in a correct region, delay, and universe. I do not have such a problem on my side.

---

### 评论 #15 (作者: WL13229, 时间: 3 months ago)

[GC13416](/hc/en-us/profiles/34962957450775-GC13416)

only one notebook is allowed to upload. try to fit your ideas into one df. you can make them as different functions

---

### 评论 #16 (作者: WL13229, 时间: 3 months ago)

[LD27384](/hc/en-us/profiles/34336234869655-LD27384)

Remember you have 'create_dataframe' function in your code, which will help WorldQuant to study and explore your dataframe later.

---

### 评论 #17 (作者: SO82954, 时间: 3 months ago)

This was a very helpful slide,thank you

---

### 评论 #18 (作者: AA64980, 时间: 3 months ago)

That was educative

---

### 评论 #19 (作者: MZ45384, 时间: 3 months ago)

This is too helpful! Thanks for showing the record video.

---

### 评论 #20 (作者: TM92286, 时间: 23 days ago)

this is helpful

---

