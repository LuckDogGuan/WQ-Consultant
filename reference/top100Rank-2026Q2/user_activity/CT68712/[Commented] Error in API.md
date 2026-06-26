# Error in API

- **链接**: [Commented] Error in API.md
- **作者**: SD99406
- **发布时间/热度**: 1年前, 得票: 3

## 帖子正文

Hii,

Can anyone help on this error,

![图片](images/img_7fba4cbf1f.png)

---

## 讨论与评论 (22)

### 评论 #1 (作者: DN76271, 时间: 1年前)

You should specify in generate_alpha function test_period parameter:

ace.generate_alpha(x, region= "USA", universe = "TOP3000", **test_period='P2Y'** )

Please check the  [documentation](https://platform.worldquantbrain.com/learn/documentation/brain-api/ace-2023-doc#:~:text=generate_alpha(regular%3A%20str,visualization%3A%20bool%20%3D%20False)) .

---

### 评论 #2 (作者: AB64885, 时间: 1年前)

![图片](images/img_e7449eafcd.png)

Corrected syntax for test_period in API lib is mentioned above.
So rewrite the code to simulate in API
This error is because of HCAC competition, for this competition mentioned that 2 year test period. So add that to simulate

---

### 评论 #3 (作者: PP87148, 时间: 1年前)

Please use test_period = "P2Y". This will fix your error, in current HCHC we must use the testing period as 2 years only in Global and USA region.

---

### 评论 #4 (作者: NM12321, 时间: 1年前)

I am not using python's ACE library. Use the regular request library to call the simulate alpha api, then you will understand the input/output and make appropriate corrections.

---

### 评论 #5 (作者: AC63290, 时间: 1年前)

The error occurs because there's a typo in your parameter name. Here's the fix: The parameter "testperied" is incorrectly spelled - it should be "testperiod". Also, there are several other typos in your code. Here's the corrected version: alpha_list = [ace.generate_alpha(x, region="GLB", universe="MINVOL", neutralization="STATISTICAL", decay=0, testperiod="P2Y") for x in alpha_list] Key corrections: "testperied" → "testperiod" "generste_clpha" → "generate_alpha" "MINVOLIN" → "MINVOL" "STATISTICA" → "STATISTICAL" "P2rvaw0" → "P2Y" This should resolve the TypeError you're encountering.

---

### 评论 #6 (作者: CT68712, 时间: 1年前)

Hey there! I came across your post about the API error on the BRAIN platform. As a new guy in quantitative trading, I totally understand how frustrating such technical issues can be—especially when you're trying to analyze data and make strategic decisions. Have you tried checking the API documentation or reaching out to support? Also, sharing specific error messages in your community might help others provide more targeted advice. Good luck, and I hope you get it resolved soon!

---

### 评论 #7 (作者: DP14281, 时间: 1年前)

The correct way of defining test period in Brain API during HCAC in GLB or USA region as below:

test_period = "P2Y".

During this period it is mandatory to keep testing period "P2Y" only, "P2Y0M" will not be acceptable.

---

### 评论 #8 (作者: deleted user, 时间: 1年前)

- **Moving Averages**  (simple, exponential) can work well, especially when combined with price momentum strategies.
- **Factor Models** : Consider using multi-factor models that combine several characteristics like value, growth, and momentum. These can help in filtering stocks that tend to perform well in the region.

---

### 评论 #9 (作者: MA97359, 时间: 1年前)

Hi  [SD99406](/hc/en-us/profiles/21041140594071-SD99406) ,

The error seems to be with test period input, you should input P2Y for the test period instead of P2Y0M0D.
Hope this helps!

---

### 评论 #10 (作者: SD99406, 时间: 1年前)

Thanks All for help

---

### 评论 #11 (作者: RP41479, 时间: 1年前)

Please use test_period = "P2Y". This will fix your error, in current HCHC we must use the testing period as 2 years only in Global and USA region.

---

### 评论 #12 (作者: NT29269, 时间: 1年前)

You have an incorrect parameter name in the request payload. You need to use  `test_period`  instead of  `testperiod` . Also, since you are simulating the GLB alpha, set its value to  `"P2Y"`  for the HCAC competition.

---

### 评论 #13 (作者: deleted user, 时间: 1年前)

**Vary timeframes** : Mixing short-term and long-term signals helps smooth out the influence of noise in short-term price movements while maintaining the overall market trend captured by longer-term signals. This diversification can help minimize correlation with other alphas.

---

### 评论 #14 (作者: TT55495, 时间: 1年前)

Moving Averages, both simple and exponential, can be highly effective, particularly when integrated with price momentum strategies. Additionally, Factor Models are worth considering, especially multi-factor models that combine various characteristics such as value, growth, and momentum. These models can be useful in filtering stocks that are more likely to perform well within a given region.

---

### 评论 #15 (作者: HN71281, 时间: 1年前)

Check if adding  `test_period='P2Y'`  resolves the issue. The HCAC competition requires a 2-year test period, so updating the API call should help.

---

### 评论 #16 (作者: SV78590, 时间: 1年前)

### Diversifying Timeframes for Stronger Alphas:

Blending short-term and long-term signals can help filter out short-term market noise while preserving the broader trends captured by longer-term signals. This approach not only enhances signal stability but also reduces correlation with other alphas, leading to a more robust and diversified strategy.

---

### 评论 #17 (作者: PT27687, 时间: 1年前)

It sounds like you're dealing with a tricky issue! Can you provide a bit more detail about the specific error message you're encountering? Any additional context, like the API you're working with or what you've tried so far, could really help others assist you better.

---

### 评论 #18 (作者: TP19085, 时间: 1年前)

The error is due to typos in your parameter names. Key corrections:

- **"testperied" → "testperiod"**
- **"generste_clpha" → "generate_alpha"**
- **"MINVOLIN" → "MINVOL"**
- **"STATISTICA" → "STATISTICAL"**
- **"P2rvaw0" → "P2Y"**

Corrected code:

```
alpha_list = [ace.generate_alpha(x, region="GLB", universe="MINVOL", neutralization="STATISTICAL", decay=0, testperiod="P2Y") for x in alpha_list]

```

Brain API requires  `"P2Y"`  as the test period for HCAC in  **GLB/USA** , not  `"P2Y0M"` .

For strategies, Moving Averages (SMA, EMA) work well with price momentum. Multi-factor models (value, growth, momentum) help filter high-performing stocks.

---

### 评论 #19 (作者: SP39437, 时间: 1年前)

It seems like the issue is related to parameter name typos in your code. Here's the corrected version of the code based on your explanation:

`alpha_list = [ace.generate_alpha(x, region="GLB", universe="MINVOL", neutralization="STATISTICAL", decay=0, test_period="P2Y") for x in alpha_list]
`

Key corrections:

- `"testperied"`  →  `"test_period"`
- `"generste_clpha"`  →  `"generate_alpha"`
- `"MINVOLIN"`  →  `"MINVOL"`
- `"STATISTICA"`  →  `"STATISTICAL"`
- `"P2rvaw0"`  →  `"P2Y"`

Now your code should work correctly without the TypeError.

Regarding your strategies, integrating moving averages (simple and exponential) with price momentum can provide excellent signals, especially when combined with multi-factor models. These models, which mix value, growth, and momentum factors, can help identify stocks with better performance potential in a given region.

Have you considered using multi-factor models for filtering stocks in the EUR region based on these signals?

---

### 评论 #20 (作者: VN28696, 时间: 1年前)

Looks like a simple typo!  `generate_alpha()`  doesn’t recognize  `testperiod`  as a valid argument. Maybe you meant  `test_window`  or  `train_period` ? Double-check the function’s documentation to see the correct parameter name. Happens to the best of us!

---

### 评论 #21 (作者: NA18223, 时间: 1年前)

Here's the corrected version: alpha_list = [ace.generate_alpha(x, region="GLB", universe="MINVOL", neutralization="STATISTICAL", decay=0, testperiod="P2Y") for x in alpha_list] Key corrections: "testperied" → "testperiod" "generste_clpha" → "generate_alpha" "MINVOLIN" → "MINVOL" "STATISTICA" → "STATISTICAL" "P2rvaw0" → "P2Y"

---

### 评论 #22 (作者: AK40989, 时间: 1年前)

It seems like others are correct in pointing out the necessary adjustments to your API call. However, there's an alternative solution: you can simply leave the  `test_period`  field blank, and it will automatically be populated with default values. This can save you some time and help avoid potential errors in your code. Have you tried this approach to see if it resolves the issue?

---

