# How to start making alphas for new consultants(after Power Pool update)

- **链接**: [Commented] How to start making alphas for new consultantsafter Power Pool update.md
- **作者**: VV63697
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

This is my 3rd post in the same series each one has slightly different tips based on the changing nature of the Brain platform.

Here are a few tips that might me helpful if you are yet to submit an alpha or have just started to submit a few -

1) Get your basics strong , you can read about fundamental ratios and the inferences you can make from them and at least know the basic technical indicators to begin with . With more time going forward we can go into more complex stuff related to algo trading strategies or ml models(not required at the beginning ) .

2) Watch all the videos in the learn section plus read the documentation page a few times there is almost everything that you require to start out.

3) Use the alpha examples in the documentation and read the logic behind them now you can start out with improving the signal by using the hints provided in the examples. Once you are able to do this much and get a submittable signal out of the examples then we can move forward to finding similar ideas to those in examples but now by ourself.

4) Now assuming that you are able to at least come up with an idea now since the launch of Powerpool alphas it is quite easy to make alpha in any of the 4 regions where Powerpool alphas are allowed ( USA,EUR,ASI,GLB) so you can pick anyone you find the best for you and start.

5) So in GLB or ASI region we can start with using the most basic operators zscore , ts_zscore , rank , ts_rank which was told to me during one of the session in consultant competitions this makes it easy to recognise which fields you can use for your alpha . Use MINVOL1M to start with you get better signals here compared to TOP3000 .

6) Neutralisations - now risk handled neutralizations might be better to use for your alphas and i think we were told to use them to reduce correlation as well but as of now i find the niche neutralizations to have lower prod correlation might be due to a lot of submissions in the risk handled ones plus the niche neutralizations take comparatively way less time to run also with the launch of the Max Trade option it can help to improve after cost performance and lower correlation as well.

7) Before submitting any alphas make sure you have the test period on and at least have 2 years of testing data to affirm whether your alpha performs well or not there . You can refer to more tests here -  [../CC40930/[Commented] Robustness Test.md](../CC40930/[Commented] Robustness Test.md)

8) Make sure to not have turnover more than 30% from what i have learnt from a lot of consultants and my advisor it has a big role on your OS performance. Also try the Max Trade setting

9) You can check for after cost sharpe IS in the illiquid universe if that is available , it would be helpful going forward from now in genius program as well

10) Whenever you choose any data field to work with you can see what's the coverage for that data field . If you are working with low coverage data fields you can use ts_backfill or other related operators . More info here -  [https://support.worldquantbrain.com/hc/en-us/articles/19248385997719-Weight-Coverage-common-issues-and-advice](/hc/en-us/articles/19248385997719-Weight-Coverage-common-issues-and-advice)

11) When you add two datafields make sure to scale them down to similar limits .

12) Try to avoid overfitting the alphas to pass the tests or add noise to reduce correlation as it might affect your OS performance anyways there is no need to do so since the PPAC.

13) Ask any doubts you have in this forum or any other forum , your advisor and other consultants will be more than happy to help you with your doubts.

This might me sufficient enough to get started with your journey as a fellow consultant . I might add more points when i learn more in the months to come .

Happy learning !

---

## 讨论与评论 (2)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Thank you for sharing about power pool. Can you explain more clearly how to optimize power pool performance with a small number of operators? I see that because the dataset is used less, the number of operators must increase.

---

### 评论 #2 (作者: JO96892, 时间: 1年前)

This is really an eye-opener

---

