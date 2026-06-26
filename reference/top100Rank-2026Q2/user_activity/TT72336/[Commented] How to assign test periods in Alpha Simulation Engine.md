# How to assign test periods in Alpha Simulation Engine?

- **链接**: [Commented] How to assign test periods in Alpha Simulation Engine.md
- **作者**: JS35015
- **发布时间/热度**: 1年前, 得票: 1

## 帖子正文

I was using ACE for simulating in USA then I got error as I had not assigned 2 years for test.
How to overcome it?

---

## 讨论与评论 (15)

### 评论 #1 (作者: AG20578, 时间: 1年前)

Hi!
you should specify in generate_alpha function test_period parameter:

ace.generate_alpha(x, region= "USA", universe = "TOP3000", **test_period='P2Y'** )

Please check the  [documentation](https://platform.worldquantbrain.com/learn/documentation/brain-api/ace-2023-doc#:~:text=generate_alpha(regular%3A%20str,visualization%3A%20bool%20%3D%20False)) .

---

### 评论 #2 (作者: DL53864, 时间: 1年前)

During the HCAC competition, for simulated Alphas in the GLB or USA regions, you need to set the  **test_period**  to  **P2Y**  in order to run them successfully.

---

### 评论 #3 (作者: NM53870, 时间: 1年前)

You should sent request with settings `test_period='P2Y'`, USA and GLB must be settings  `test_period='P2Y'` during HCA competition

---

### 评论 #4 (作者: DK30003, 时间: 1年前)

you should specify in generate_alpha function test_period parameter:

ace.generate_alpha(x, region= "USA", universe = "TOP3000", **test_period='P2Y0D'** )

---

### 评论 #5 (作者: AJ93287, 时间: 1年前)

You can edit the ace_lib.py file as follows:

![图片](images/img_31d1349e17.png)

---

### 评论 #6 (作者: SY65468, 时间: 1年前)

Hii  [JS35015](/hc/en-us/profiles/25681312737175-JS35015)

Requests must include  `test_period='P2Y'` . During the HCA competition, both USA and GLB must also use  `test_period='P2Y'` .

---

### 评论 #7 (作者: HN71281, 时间: 1年前)

You need to specify the  `test_period`  parameter when using the  `generate_alpha`  function in ACE. Try setting  `test_period='P2Y'`  like this:

```
ace.generate_alpha(x, region="USA", universe="TOP3000", test_period="P2Y")

```

This ensures your simulation runs correctly. Also, refer to the documentation for more details.

---

### 评论 #8 (作者: PP87148, 时间: 1年前)

you can use below expression

ace.generate_alpha(x, region= region1, universe = universe1, decay = decay1 ,neutralization = neut , truncation = trunc, test_period= 'P2Y')

---

### 评论 #9 (作者: NT29269, 时间: 1年前)

Search for the function  `generate_alpha`  first and add or adjust the  `test_period`  parameter to enable simulation. Currently, for the two regions GLB and USA,  `test_period`  should be set to  `'P2Y'` .

---

### 评论 #10 (作者: TN33707, 时间: 1年前)

It seems like the duration assignment was missed initially which led to the error. You can rectify this by going back into your setup configurations and ensuring that you specify a 2-year period for the test.

---

### 评论 #11 (作者: TT72336, 时间: 1年前)

If you use the API to simulate, add the option  `testPeriod: "P2Y"`  to the request payload. If you use the platform interface, set the  **Test Period**  to  **2 Years 0 Months**  to simulate successfully.

---

### 评论 #12 (作者: MA97359, 时间: 1年前)

Use  `test_period='P2Y'`  while generating alpha; assign the test period accordingly to ensure proper backtesting and evaluation over a two-year horizon

---

### 评论 #13 (作者: LH71010, 时间: 1年前)

For web approach, you can change it in your setting window, by setting test period = 2.

For API approach, there is an option that testPeriod: "P2Y", you need to add it to your sim API.

---

### 评论 #14 (作者: HD25387, 时间: 1年前)

To assign test periods in the Alpha Simulation Engine, you need to specify the  `test_period`  parameter in the  `generate_alpha`  function. For example, if you are simulating in the USA region, set it as follows:

`ace.generate_alpha(x, region="USA", universe="TOP3000", test_period="P2Y")
`

This ensures that your simulation includes the required 2-year test period. This setting is necessary for running simulations in regions like  **USA**  and  **GLB** , especially during competitions like HCAC. Always refer to the documentation for any updates.

---

### 评论 #15 (作者: LO56106, 时间: 1年前)

To resolve the errors that occur during ACE simulation, you need to specify the test period parameter in the `generate_alpha` function. For example, for the US region, you can set it like this: `ace.generate_alpha(x, region="USA", universe="TOP3000", test_period="P2Y")`. Make sure your simulation includes the required two-year test period.

---

