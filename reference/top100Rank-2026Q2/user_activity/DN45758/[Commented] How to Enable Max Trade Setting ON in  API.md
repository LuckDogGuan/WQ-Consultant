# How to Enable Max Trade Setting "ON" in  API?

- **链接**: [Commented] How to Enable Max Trade Setting ON in  API.md
- **作者**: HS48991
- **发布时间/热度**: 1年前, 得票: 9

## 帖子正文

Can anyone please guide me on how to turn the Max Trade setting "ON" using the API? I’m not sure where or how to enable it and would really appreciate any help or example.

---

## 讨论与评论 (25)

### 评论 #1 (作者: NS94943, 时间: 1年前)

Hi  [HS48991](/hc/en-us/profiles/8752451976855-HS48991) ,

I hope you are using the latest version of the API as the older versions do not have this setting in the code. In the latest version, you can use it like this:

```
alpha_list = ace.generate_alpha(x,region= "USA", universe = "TOP3000",delay=1, decay=0,truncation=0.03,nan_handling="ON",neutralization="SLOW",test_period="P2Y",max_trade="ON")
```

I hope this helped.

---

### 评论 #2 (作者: UG81605, 时间: 1年前)

alpha_list = [ace.generate_alpha(x,region =REGION,universe = UNIVERSE,neutralization = "COUNTRY",decay=0,delay=DELAY, max_trade= "OFF") for x in expression_list]
Here is the code snippet. You need to pass this variable to generate alpha

---

### 评论 #3 (作者: DL53864, 时间: 1年前)

A general way to observe BRAIN's APIs is by opening your browser along with the Network tab in the developer console (F12). Then, for each action you take, observe the requested APIs, including the endpoint, parameters, and body. This will help you understand how BRAIN's APIs operate

---

### 评论 #4 (作者: AG14039, 时间: 1年前)

A practical way to explore BRAIN's APIs is by opening your browser's developer console (F12) and switching to the Network tab. As you interact with the platform, you can monitor the API requests being made—paying attention to the endpoints, parameters, and request bodies. This approach helps you gain insight into how BRAIN’s APIs function behind the scenes.

---

### 评论 #5 (作者: KS69567, 时间: 1年前)

Hey  [UG81605](/hc/en-us/profiles/5342475745559-UG81605)

can you explain in details ??

**because when I give the command to the API as you told me in the comment section, an error is occurring."**

If you'd like, you can also share the  **exact command**  or  **error message**  you're seeing — I can help troubleshoot it step by step.

---

### 评论 #6 (作者: TN48242, 时间: 1年前)

To enable the Max Trade setting using the API, make sure to include  `max_trade="ON"`  when generating your alphas. This flag activates the max trade constraint during simulation or live testing. Here's the updated code snippet:

`alpha_list = [ace.generate_alpha(x, region=REGION, universe=UNIVERSE, neutralization="COUNTRY", decay=0, delay=DELAY, max_trade="ON") for x in expression_list]
`

You’ll need to pass this list into your alpha generation function to ensure it applies properly. This is especially useful when you're submitting large alpha batches and want to control execution limits more precisely. Keep in mind that older versions of the API may not support this parameter, so be sure to upgrade to the latest release if needed. Using  `max_trade="ON"`  can help improve portfolio robustness by avoiding over-concentration in specific trades. Hope this helps!

---

### 评论 #7 (作者: SD17531, 时间: 1年前)

template = {

'type': 'REGULAR',

'settings': {

'instrumentType': 'EQUITY',

'region': alpha['region'],

'universe': alpha['universe'],

'delay': alpha['delay'],

'decay': decay,

'neutralization': neut,

'truncation': 0.1,

'pasteurization': 'ON',

'unitHandling': 'VERIFY',

'nanHandling': 'OFF',

'language': 'FASTEXPR',

'visualization': False,

'maxTrade': 'ON',

},

'regular': alpha_expression

}
-----------------------------------------------------------------------------------------------------------------

You can refer to the above json ,the last key is maxTrade, and use api send this json to WQ server for simulation.

---

### 评论 #8 (作者: SP39437, 时间: 1年前)

Really appreciate this discussion—very informative! Using the browser’s Developer Tools (F12) and monitoring the Network tab is a practical and effective way to understand how BRAIN’s API functions under the hood. Each user interaction—like clicking a button or triggering a simulation—sends a specific request, and inspecting the request details (URL, headers, parameters, body) can reveal valuable insights about the internal workings of the platform. It’s especially useful for discovering supported parameters, like  `max_trade` , and for understanding version-specific behavior. The shared code snippet makes it clear how to implement the setting:

`alpha_list = [ace.generate_alpha(x, region=REGION, universe=UNIVERSE, neutralization="COUNTRY", decay=0, delay=DELAY, max_trade="OFF") for x in expression_list]
`

Knowing that older API versions might lack support for  `max_trade`  is crucial when debugging issues. Reverse-engineering like this opens up more control and transparency for strategy development.

Have you come across any lesser-known API flags or parameters that significantly affect simulation behavior?

---

### 评论 #9 (作者: AB15407, 时间: 1年前)

An interesting and helpful topic for many people.

Everyone should also take note that when using new settings (in this case, MaxTrade) in the code, thorough testing is necessary to avoid situations where no Alpha can be successfully simulated in a day, causing the "Max simulation streak" metric to reset.

---

### 评论 #10 (作者: DK20528, 时间: 1年前)

for alpha in new_alpha_list:
    alpha['settings']['maxTrade'] = 'ON'

You can use this in your code.

---

### 评论 #11 (作者: HT71201, 时间: 1年前)

You can use this in your code

alpha_list = ace.generate_alpha(x,region= "ASI", universe = "MINVOL1M",delay=1, decay=0,truncation=0.01,nan_handling="ON",neutralization="SLOW",max_trade="ON")

---

### 评论 #12 (作者: AG14039, 时间: 1年前)

This is a valuable and relevant topic for many. It's also important to remember that when introducing new settings—like MaxTrade—into your code, thorough testing is essential. Without it, you risk having days where no Alpha can be successfully simulated, which can reset your "Max simulation streak" metric.

---

### 评论 #13 (作者: AK40989, 时间: 1年前)

> for alpha in new_alpha_list:
> alpha['settings']['maxTrade'] = 'ON'
> You can use this in your code.

You are a lifesaver dude. It worked

---

### 评论 #14 (作者: AC63290, 时间: 1年前)

To turn on the Max Trade setting via API, include  `"max_trade": true`  in your simulation parameters. For example:  `{"simulation": {"parameters": {"max_trade": true}}}` . If it’s unrecognized, ensure your API version supports it. Check the official API documentation or contact support for updated syntax and access permissions.

---

### 评论 #15 (作者: RG93974, 时间: 1年前)

alpha_list = [ace.generate_alpha(x, region= region, universe = universe, nan_handling= nan_handling ,neutralization=neutralization,decay=decay,test_period = "P2Y",maxTrade=maxTrade) for x in expression_list]

alpha_list[0]

---

### 评论 #16 (作者: LR13671, 时间: 1年前)

The recent discussion around enabling the  `Max Trade`  setting in BRAIN’s API workflow has brought valuable clarity for developers and alpha researchers. The core approach shared by  **UG81605**  involves generating alphas through a loop with parameters like  `region` ,  `universe` ,  `delay` , and importantly, the  `max_trade`  flag. The exact line of code to enable this is:

---

### 评论 #17 (作者: DV64461, 时间: 1年前)

Should we always enable max trade? Because I see that if we do not enable max trade then convert it manually it will save time a little

---

### 评论 #18 (作者: SP39437, 时间: 1年前)

The recent conversation around enabling the Max Trade setting in BRAIN’s API workflow has provided helpful insights for both developers and alpha researchers. A key contribution by user UG81605 explained how to integrate this into your alpha generation loop, which typically includes parameters like region, universe, delay, and now, the  `max_trade`  flag. To activate Max Trade via API, simply include:

`{"simulation": {"parameters": {"max_trade": true}}}
`

If this setting is not recognized, make sure your API version supports it. Refer to the latest API documentation or reach out to BRAIN support for updated syntax and permission requirements.

This is an important feature for many users. However, be cautious when introducing new settings like  `max_trade` . Without proper testing, you could run into days where no alphas simulate successfully — potentially resetting your Max Simulation Streak. Always validate your setup thoroughly before running in production.

---

### 评论 #19 (作者: TP19085, 时间: 1年前)

Thanks for the insightful discussion—this has been incredibly helpful! Leveraging the browser’s Developer Tools (F12), especially the Network tab, is a hands-on and effective method for exploring how BRAIN’s API operates behind the scenes. Each platform interaction—whether it's a button click or simulation run—triggers a network request, and examining elements like the request URL, headers, query parameters, and payload can uncover critical details about the system’s functionality. This is particularly useful for identifying available parameters, such as  `max_trade` , and for recognizing differences tied to specific API versions. The provided code snippet illustrates how to incorporate the parameter effectively:

`alpha_list = [ace.generate_alpha(x, region=REGION, universe=UNIVERSE, neutralization="COUNTRY", decay=0, delay=DELAY, max_trade="OFF") for x in expression_list]
`

Being aware that older API versions may not support certain features like  `max_trade`  is vital when troubleshooting. Has anyone discovered any under-the-radar API parameters that significantly influence simulation behavior?

---

### 评论 #20 (作者: NS62681, 时间: 1年前)

This helps you spot available settings like  `max_trade` , and understand what’s version-dependent in the API. For example:

`alpha_list = [ace.generate_alpha(x, region=REGION, universe=UNIVERSE, neutralization="COUNTRY", decay=0, delay=DELAY, max_trade="OFF") for x in expression_list]
`

Older API versions might not support  `max_trade` , so keep that in mind if you run into issues.

---

### 评论 #21 (作者: DN45758, 时间: 1年前)

Absolutely—introducing new settings like MaxTrade requires careful testing. Without it, you might face days when no alpha passes simulation, breaking your "Max simulation streak." Rigorous validation ensures stability, helps catch issues early, and maintains consistent performance metrics in your alpha pipeline.

---

### 评论 #22 (作者: MK58212, 时间: 1年前)

Thanks  **@DK20528**  for sharing this helpful snippet:

for alpha in new_alpha_list:
    alpha['settings']['maxTrade'] = 'ON'

Really appreciate you taking the time to post this—super useful for the community!

---

### 评论 #23 (作者: MY83791, 时间: 1年前)

Thanks  [LR13671](/hc/en-us/profiles/4516642748055-LR13671)  for your valueable Input !!
Really appreciate your inforrmation on the recent discussion.

---

### 评论 #24 (作者: PN88168, 时间: 10个月前)

I tried USING the latest API but encountered errors of missing files ...what could have done wrong my fellow geniuses?

---

### 评论 #25 (作者: TP19085, 时间: 10个月前)

Using the browser’s Developer Tools—especially the Network tab—is a hands-on way to see how BRAIN’s API calls function. By inspecting requests, you can uncover details like URLs, headers, payloads, and parameters such as  `max_trade`  that may not be fully documented. For example, adding  `max_trade="OFF"`  in the alpha generation loop shows how you can programmatically customize simulation behavior.

Keep in mind that some parameters, including  `max_trade` , are only supported in newer API versions. If a parameter isn’t recognized, check your API version and consult the official documentation or BRAIN support. Improper use can lead to issues, like simulation failures or resets in your Max Simulation Streak.

Have others discovered hidden parameters or flags that meaningfully impact alpha simulations? Sharing these can help the community optimize workflows and avoid unexpected pitfalls.

---

