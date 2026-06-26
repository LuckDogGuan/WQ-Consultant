# For the neutralize slow/ fast mode

- **链接**: [Commented] For the neutralize slow fast mode.md
- **作者**: LH33235
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

Please help to give advise when try to use neutralize slow/ fast mode? I am getting stuck with this stones. Thank you all !

---

## 讨论与评论 (3)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi, the signal in this neutralize is quite good. I don't know if you are having difficulty finding the signal or reducing the correlation or something else. Knowing the problem will help everyone give more accurate advice.

---

### 评论 #2 (作者: AK40989, 时间: 1年前)

In general, I choose  *neutralize fast*  when working with short-term or reversion-style alphas that align more with fast-turnover dynamics, this helps clean up quick market noise without over-smoothing. On the other hand, I use  *neutralize slow*  for longer-horizon or trend-based alphas where stability and lower turnover are more important. When in doubt or if the alpha mixes characteristics,  *slow + fast*  can help balance both ends. The right mode often depends on your alpha's nature, how reactive or persistent the signal is.

---

### 评论 #3 (作者: NS62681, 时间: 1年前)

Use  `neutralize=slow`  for longer-horizon or trend-following alphas where signal stability and low turnover are priorities. If you're unsure, or if your alpha combines both short- and long-term traits,  `slow_and_fast`  can provide a more balanced approach. Ultimately, the best neutralization mode depends on the alpha's nature how reactive or persistent the signal is.

---

