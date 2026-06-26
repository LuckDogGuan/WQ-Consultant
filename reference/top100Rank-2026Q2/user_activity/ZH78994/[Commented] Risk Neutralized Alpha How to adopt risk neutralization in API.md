# Risk Neutralized Alpha: How to adopt risk neutralization in API?

- **链接**: [Commented] Risk Neutralized Alpha How to adopt risk neutralization in API.md
- **作者**: NL41370
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

To adopt risk neutralization in API simulation, simply change the neutralization setting in POST/ simulations to one of the followings:

**Risk Factor Setting**

**API Setting**

Slow Factors

neutralization: "SLOW"

Fast Factors

neutralization: "FAST"

Slow + Fast Factors

neutralization:  "SLOW_AND_FAST"

```
Below is a code snippet of simulating the same API example Alpha here but with Slow Factors:simulation_data = {'type': 'REGULAR','settings': {'instrumentType': 'EQUITY','region': 'USA','universe': 'TOP3000','delay': 1,'decay': 15,'neutralization': 'SLOW','truncation': 0.08,'pasteurization': 'ON','unitHandling': 'VERIFY','nanHandling': 'OFF','language': 'FASTEXPR','visualization': False, },'regular': 'close' }simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=simulation_data)
```

Find more information on how to use API  [here](https://platform.worldquantbrain.com/learn/documentation/consultant-information/brain-api) !

---

## 讨论与评论 (14)

### 评论 #1 (作者: ZH78994, 时间: 1年前)

I would like to express my heartfelt gratitude for your generous sharing. Your willingness to offer your time, knowledge, and resources means a great deal to me. The insights you've provided have not only broadened my understanding but also inspired me to take positive steps forward. It's rare to encounter someone so selfless and giving, and I truly appreciate the impact you've had. Thank you for your kindness and for being such a valuable source of support. Your gesture will be remembered, and I am grateful for the opportunity to learn from you.

---

### 评论 #2 (作者: CC40930, 时间: 1年前)

This post effectively explains how to incorporate risk neutralization into API simulations. The clear distinctions between  `SLOW` ,  `FAST` , and  `SLOW_AND_FAST`  neutralization settings make it easy to choose the most suitable option based on alpha design and performance goals. The code snippet is particularly helpful, showing exactly how to set up a simulation with  `SLOW`  neutralization. Including specific parameters like  `universe` ,  `decay` , and  `truncation`  also highlights the flexibility of the API for tailoring simulations. For those exploring systematic risk management, this is a solid starting point to test and refine strategies.

---

### 评论 #3 (作者: TN48752, 时间: 1年前)

Hello, everyone can use the random neutralize setting technique, so that when simulated there is no bias and neutralize, it will reduce corr more effectively.

---

### 评论 #4 (作者: PL15523, 时间: 1年前)

You can choose from these options:

- For slow factors:  `"neutralization": "SLOW"`
- For fast factors:  `"neutralization": "FAST"`
- For both slow and fast factors:  `"neutralization": "SLOW_AND_FAST"`

---

### 评论 #5 (作者: DP11917, 时间: 1年前)

This setting neutralizes risk exposure related to slow-moving risk factors. It adjusts the model to remove the influence of risk factors that affect your Alpha signal over a longer time horizon or at a slower pace. This can be useful when you want to focus on faster-moving signals while ignoring long-term risk factors.

---

### 评论 #6 (作者: QG16026, 时间: 1年前)

The provided code snippet is very helpful in showing how to set up the simulation with these options. his information is invaluable for improving risk management and refining strategies. Thank you for your clear and thoughtful guidance.

---

### 评论 #7 (作者: CT68712, 时间: 1年前)

This API setting for risk neutralization is quite interesting! As a tech enthusiast, I really appreciate how you broke it down into clear categories—SLOW, FAST, and SLOW_AND_FAST. It’s fascinating how much influence the right parameters can have on alpha performance. I might have to experiment with the SLOW neutralization in my simulations to see how it adjusts my strategy. Do you think this approach will make a significant difference in managing risk exposure? It seems like a solid way to focus on fast-moving signals while minimizing long-term biases. Thanks for sharing these insights; they really help in deepening my understanding of quantitative trading strategies!

---

### 评论 #8 (作者: SV70703, 时间: 1年前)

Thank you for breaking this down so clearly! The detailed explanation of risk neutralization settings and their application in API simulations is incredibly helpful, especially with the provided code snippet. It's great to see how customizable the settings are, from focusing on slow factors to combining both slow and fast. The structured format of the simulation_data makes it intuitive to implement, and the mention of additional resources ensures we're well-supported. Appreciate you sharing this!

---

### 评论 #9 (作者: PL15523, 时间: 1年前)

n this step, you apply a  **transformation**  to the uniform distribution. This transformation reshapes the uniform distribution to match a specific distribution: a  **Gaussian (Normal)**  distribution, a  **Cauchy**  distribution, or potentially leaving it as uniform. Each of these distributions has different characteristics:

---

### 评论 #10 (作者: ML65849, 时间: 1年前)

Hi  [CT68712](/hc/en-us/profiles/15219840701719-CT68712) , SLOW and FAST Risk neutralize setting contains different kind of risks, I recommend you to try both and organize the results and lesson learned. Also try to use newly added CROWDING factors as well.

---

### 评论 #11 (作者: ND68030, 时间: 1年前)

Thank you for sharing. Besides the neutralization factor, parameters such as delay, decay, and truncation also significantly impact the simulation. For example, when using slow factors (SLOW), a decay value of 15 is reasonable, but if combined with fast factors, reducing decay might be necessary. Similarly, truncation: 0.08 helps filter out noise but may also remove important information, so it should be adjusted based on the specific strategy

---

### 评论 #12 (作者: PT27687, 时间: 1年前)

This post provides valuable insights into adjusting risk neutralization settings within API simulations. I appreciate how clearly you've outlined the different options and included a code snippet for better understanding. It might be interesting to have more examples demonstrating the outcomes when using each of the risk factors. How does each setting impact overall simulation performance?

---

### 评论 #13 (作者: FW84077, 时间: 6个月前)

thanks alot!

---

### 评论 #14 (作者: JL27448, 时间: 2个月前)

thx so much

---

