# Getting started as a new consultant to make alphas

- **链接**: [Commented] Getting started as a new consultant to make alphas.md
- **作者**: VV63697
- **发布时间/热度**: 1年前, 得票: 8

## 帖子正文

Here are a few tips that might me helpful if you are yet to submit an alpha or have just started to submit a few (feel free to add more points in comments plus correct me wherever i might be wrong)-

1) Get your basics strong , you can read about fundamental ratios and the inferences you can make from them and at least know the basic technical indicators to begin with . With more time going forward we can go into more complex stuff related to algo trading strategies or ml models(not required at the beginning ) .

2) Watch all the videos in the learn section plus read the documentation page a few times there is almost everything that you require to start out.

3) Use the alpha examples in the documentation and read the logic behind them now you can start out with improving the signal by using the hints provided in the examples. Once you are able to do this much and get a submittable signal out of the examples then we can move forward to finding similar ideas to those in examples but now by ourself.

4) Now assuming that you are able to at least come up with an idea now this one is my personal advice might not be correct but I find it hard to get started with the USA region because of high correlation so i would suggest to start out with GLB or ASI region ( I think US , ASI , GLB , EUR have the same weightage ) .

5) So in GLB or ASI region we can start with using the most basic operators zscore , ts_zscore , rank , ts_rank which was told to me during one of the session in consultant competitions this makes it easy to recognise which fields you can use for your alpha . Use MINVOL1M to start with you get better signals here compared to TOP3000 .

6) Neutralisations - now risk handled neutralizations might be better to use for your alphas and i think we were told to use them to reduce correlation as well but as of now i find the niche neutralizations to have lower prod correlation might be due to a lot of submissions in the risk handled ones plus the niche neutralizations take comparatively way less time to run (for me).

7) Before submitting any alphas make sure you have the test period on and at least have 2 years of testing data to affirm whether your alpha performs well or not there . You can refer to more tests here -  [../CC40930/[Commented] Robustness Test.md](../CC40930/[Commented] Robustness Test.md)

8) Whenever you choose any data field to work with you can see what's the coverage for that data field . If you are working with low coverage data fields you can use ts_backfill or other related operators . More info here -  [https://support.worldquantbrain.com/hc/en-us/articles/19248385997719-Weight-Coverage-common-issues-and-advice](/hc/en-us/articles/19248385997719-Weight-Coverage-common-issues-and-advice)

9) When you add two datafields make sure to scale them down to similar limits .

10) Try to avoid overfitting the alphas to pass the tests or add noise to reduce correlation as it might affect your OS performance.

11) Ask any doubts you have in this forum or any other forum , your advisor and other consultants will be more than happy to help you with your doubts.

This might me sufficient enough to get started with your journey as a fellow consultant . I might add more points below if required.

Happy learning !

---

## 讨论与评论 (34)

### 评论 #1 (作者: CH36668, 时间: 1年前)

This is an incredibly well-structured and insightful guide for anyone starting their alpha journey. The level of detail and thoughtfulness you’ve put into covering all the key aspects—from building a solid foundation to advanced strategies like neutralization and avoiding overfitting—is truly commendable. Your emphasis on learning, experimentation, and seeking help from the community fosters a supportive and collaborative spirit, which is essential for success.

Thank you for sharing such a comprehensive resource! It’s not just a starting point but also a roadmap for continuous improvement and learning. Your effort to help others navigate this challenging yet rewarding journey is deeply appreciated. Wishing everyone great success and happy learning, indeed!

---

### 评论 #2 (作者: SC43474, 时间: 1年前)

This guide is a goldmine for anyone starting their alpha journey! The focus on mastering the basics—like ratios, indicators, and starting with simpler regions—is spot on. Using operators like zscore and ts_zscore to identify signals is a smart strategy.

A key tip: always check your data’s quality and freshness. Even small discrepancies can skew results. Also, don’t overlook the power of experimenting with different neutralization strategies—small tweaks can drastically improve your alpha's performance.

Alpha development is all about iteration. Embrace the trial and error process, as that's where breakthroughs happen.

Amazing work here—can’t wait to see more! Keep it up!

---

### 评论 #3 (作者: LY88401, 时间: 1年前)

A comprehensive guide for Alpha beginners, offering clear, actionable steps to build strong foundations, refine signals, and ensure robust performance. Emphasizing practical strategies and community support, it’s an essential roadmap for new consultants. 🚀Thank you very much!

---

### 评论 #4 (作者: RP41479, 时间: 1年前)

This is an excellent guide for anyone starting their alpha journey! Thank you for sharing such a thoughtful and detailed resource—it’s both inspiring and highly appreciated.

---

### 评论 #5 (作者: HY45205, 时间: 1年前)

This guide is truly outstanding! You've done an excellent job covering all the essential steps for new consultants to start their alpha journey with confidence. The detailed breakdown of concepts, tools, and strategies—from building foundational knowledge to implementing robust testing and neutralization techniques—offers a clear roadmap for success.

I particularly appreciate how you've emphasized the importance of continuous learning, experimenting with different ideas, and leveraging community support. Your insights into starting with regions like GLB or ASI, choosing appropriate operators, and managing overfitting are incredibly practical and valuable.

Thank you for sharing such a comprehensive and thoughtful guide. It's a fantastic resource not only for beginners but also for those looking to refine their approach. Wishing everyone the best in their alpha creation journey, and kudos to you for fostering a spirit of collaboration and growth!

---

### 评论 #6 (作者: DK20528, 时间: 1年前)

This is a great and detailed guide for anyone just starting out with alpha submissions or working on their first few! I especially like the focus on starting with strong fundamentals and the advice on avoiding overfitting.

A couple of additional thoughts:

- It might be helpful to mention the importance of  **keeping track of performance metrics**  like Sharpe ratio, alpha, and beta when evaluating your alpha’s success. These are crucial to understanding how your alpha behaves in various market conditions.
- It could also be useful to  **experiment with different data sources**  or  **feature engineering**  techniques over time. Once you're comfortable with the basics, trying different ways to transform your features can uncover new patterns and improve alpha performance.
- **Collaboration**  is key. Sharing ideas or asking for feedback in the community can sometimes provide a fresh perspective and help identify areas you might have missed.

But overall, great tips for anyone getting started. Best of luck to all!

---

### 评论 #7 (作者: TN48752, 时间: 1年前)

Thanks for sharing the detailed roadmap. I realized I have been on the same journey since I started alpha on Brain.

---

### 评论 #8 (作者: LN92324, 时间: 1年前)

Your sharing is really helpful for new consultants. When I first joined Brain, I also had many difficulties due to lack of experience. At that time, when I found an alpha that could be submitted, I usually submitted it right away. Now, I think new consultants can start with Fundamental and Model datasets. Once they have experience, then when they decide to move on to more difficult datasets, it will be easier for them.

---

### 评论 #9 (作者: DN41247, 时间: 1年前)

Thank you for this comprehensive and practical guide for beginners! The step-by-step approach, especially the emphasis on building a strong foundation, leveraging examples, and region-specific strategies, is incredibly useful. Your insights on neutralizations and robustness testing are particularly valuable. Great job creating such an encouraging resource for newcomers!

---

### 评论 #10 (作者: TT55495, 时间: 1年前)

Thanks for sharing. Starting with the basics and building from there will help beginners get off on the right foot. Keep experimenting, testing, and learning—this iterative process is key to growing successful alphas. Good luck!

---

### 评论 #11 (作者: MY83791, 时间: 1年前)

Thank you for sharing such an incredibly detailed and insightful guide for beginners on their alpha journey! The emphasis on building strong fundamentals, leveraging documentation and examples, and progressing to advanced techniques like neutralizations and robustness testing is commendable. Your step-by-step approach not only simplifies the learning curve but also encourages collaboration and continuous improvement.

Your efforts to provide this roadmap reflect a genuine intent to support the community, and it’s deeply appreciated. Wishing everyone success as they implement these valuable tips!

---

### 评论 #12 (作者: QG16026, 时间: 1年前)

Thank you for this detailed and practical guide for beginners! The clear, step-by-step approach, especially the focus on establishing a strong foundation, using examples, and applying region-specific strategies is incredibly helpful. Excellent work creating such an encouraging resource for newcomers!

---

### 评论 #13 (作者: AR10676, 时间: 1年前)

Thank you so much VV63697 for a comprehensive article , it is really helpful for the new consultants to create alphas , I will say that new consultants should bring innovation in their ideas for creating alphas with better results

---

### 评论 #14 (作者: ZH78994, 时间: 1年前)

1) **Strengthen Your Basics**: Start by familiarizing yourself with fundamental ratios (like P/E, P/B, ROE) and what insights they provide about a company's financial health. Also, learn the basic technical indicators (like moving averages, RSI, MACD) to understand price action. As you progress, you can delve into more advanced topics like algorithmic trading strategies and machine learning models, but focus on the fundamentals first.

2) **Utilize Learning Resources**: Watch all the videos in the "Learn" section and read the documentation carefully. These resources cover essential concepts and tools you'll need to get started. Revisit the documentation a few times to reinforce your understanding and ensure you have a solid foundation before diving deeper.

---

### 评论 #15 (作者: YC82708, 时间: 1年前)

This is an excellent guide for those starting out with alpha submission, offering practical tips and clear advice for building a solid foundation in the field. I especially appreciate your emphasis on understanding the basics of fundamental ratios and technical indicators, as well as the importance of reading through documentation and learning materials.

Your advice about starting with regions like GLB or ASI to avoid high correlation is insightful, as is the suggestion to use basic operators like  `zscore`  and  `ts_zscore`  for a more manageable starting point. The tips on neutralizations and scaling data fields are also highly relevant for those looking to refine their signals and minimize correlation.

Your recommendation to test alphas over at least two years of data to ensure robustness is a key practice for validation. It’s also great that you’ve highlighted the importance of avoiding overfitting and the value of asking questions in the community for support.

Overall, this guide provides a clear, actionable path for those looking to dive into alpha strategy development. It’s a fantastic starting point for both beginners and those looking to improve their submissions. Happy learning indeed!

---

### 评论 #16 (作者: CC40930, 时间: 1年前)

Great tips for anyone starting their journey as a consultant! I particularly like your advice on focusing on the basics, like fundamental ratios and basic technical indicators, before diving into complex strategies. It’s also crucial to start with regions like GLB or ASI to avoid the high correlation of the US market. I agree with your point about neutralizations too—niche ones can often offer better results with lower correlation and quicker run times. Additionally, using a solid testing period with 2+ years of data and ensuring proper data coverage are essential steps for reliable alphas. Thanks for sharing these insights!

---

### 评论 #17 (作者: DD24306, 时间: 1年前)

Thank you for taking the time to share such a detailed and thoughtful guide for those starting out on their alpha journey! Your tips on building a strong foundation, leveraging learning resources, and strategically navigating regions and datasets are incredibly practical and actionable. I especially appreciate the emphasis on understanding neutralization strategies, scaling data fields, and avoiding overfitting—critical advice for creating robust and sustainable alphas. The encouragement to seek help from the community and advisors highlights the collaborative spirit that drives progress. Your insights and willingness to guide others are truly inspiring. Thank you for helping us all grow together!

---

### 评论 #18 (作者: KS24487, 时间: 1年前)

> Great tips for anyone starting their journey as a consultant! I particularly like your advice on focusing on the basics, like fundamental ratios and basic technical indicators, before diving into c...

Very true.

---

### 评论 #19 (作者: CT68712, 时间: 1年前)

This guide is incredibly helpful for those of us who are just diving into alpha creation! I totally agree with the emphasis on strengthening our basics—having a good grasp of fundamental ratios and basic technical indicators is key. It's also smart to start with regions like GLB or ASI to avoid getting tangled in the high correlation of the US market. The advice to utilize neutralizations to manage risk is super valuable too.

Don't forget about testing your alphas over a decent period—at least two years of data is crucial for validation! Overall, these tips create a solid roadmap for anyone eager to learn and grow in this field. Thanks for putting this together; it’s a fantastic resource for us all!

---

### 评论 #20 (作者: DL53864, 时间: 1年前)

Thank you for your great contribution. For new consultants, it can be challenging to decide which dataset to use for each region. I would like to add some advice: try using the Data page feature. Create filters to select datasets that have been used moderately (too low may be hard to work with, too high could lead to production correlation being too high). Once you have gained stability, you can then research more challenging datasets.

---

### 评论 #21 (作者: NS62681, 时间: 1年前)

Your insights are truly valuable for new consultants! When I first joined Brain, I also faced many challenges due to my lack of experience. Back then, whenever I found an alpha that seemed submit-worthy, I would submit it immediately. Now, I believe new consultants can benefit from starting with Fundamental and Model datasets, as they provide a solid foundation for understanding and developing effective alphas.

---

### 评论 #22 (作者: NT34170, 时间: 1年前)

This is a brilliant roadmap for anyone diving into the world of trading strategies! Your detailed steps not only outline a strong foundation but also guide on progressively tackling more complex aspects. The insights on regional focus and the nuances of risk neutralization are especially valuable.

---

### 评论 #23 (作者: VP87972, 时间: 1年前)

These tips are incredibly structured and insightful for anyone stepping into the realm of algo trading and model building. It's great to see such a thoughtful and detailed roadmap laid out for beginners.

---

### 评论 #24 (作者: RB98150, 时间: 1年前)

Great guide! Solid foundation, testing rigor, and avoiding overfitting are key. Will refine my approach!

---

### 评论 #25 (作者: PT27687, 时间: 1年前)

This is an excellent guide filled with practical advice for newcomers. Your emphasis on mastering the basics before diving into complex strategies resonates well. It’s interesting how you recommend starting with specific regions to avoid correlation issues; I'm curious if you have suggestions on how to effectively test these initial ideas? Happy learning to you too!

---

### 评论 #26 (作者: TK30888, 时间: 1年前)

This is a comprehensive and structured approach for anyone new in the field. Your effort to delineate each step clearly is truly helpful in navigating through what can be a complex process. The varied advice on regions to focus on and specific strategies for starting out provide a great foundation.

---

### 评论 #27 (作者: NH69517, 时间: 1年前)

These insights provide a clear and structured approach for newcomers. Engaging with the documentation, examples, and global regions systematically seems like a practical strategy to gain valuable experiences in developing better alphas.

---

### 评论 #28 (作者: BV82369, 时间: 1年前)

These points provide a structured approach for beginners to navigate alpha submissions efficiently. Emphasizing fundamental concepts initially and gradually progressing toward complex techniques like ML models is a logical roadmap.

---

### 评论 #29 (作者: AK40989, 时间: 1年前)

This guide is awesome for anyone starting with alphas! I like how you focus on getting the basics right with fundamental ratios and starting in simpler regions like GLB or ASI. Using operators like zscore is a good move too.

---

### 评论 #30 (作者: DK30003, 时间: 1年前)

I particularly appreciate how you've emphasized the importance of continuous learning, experimenting with different ideas, and leveraging community support. Your insights into starting with regions like GLB or ASI, choosing appropriate operators, and managing overfitting are incredibly practical and valuable.

---

### 评论 #31 (作者: HN80189, 时间: 1年前)

This is a well-structured and detailed guideline for newcomers. Breaking down the learning process into progressive steps makes entry into the field approachable.

---

### 评论 #32 (作者: QN13195, 时间: 1年前)

This is a well-structured and practical guide for newcomers. The emphasis on gradual progression from fundamentals to more advanced concepts should be particularly useful for those starting out. Providing direct references to existing documentation ensures better accessibility for learning materials.

---

### 评论 #33 (作者: TN33707, 时间: 1年前)

These are some solid and practical insights for getting started with submitting alphas. The suggestions on building strong fundamentals and progressively working towards complex strategies provide a good learning path.

---

### 评论 #34 (作者: TN41146, 时间: 1年前)

Your insights are incredibly helpful for new consultants. When I first joined Brain, I also struggled a lot due to my lack of experience. Back then, I would often submit any alpha I found that could be submitted right away. Now, I believe new consultants should start with the Fundamental and Model datasets. As they gain more experience, transitioning to more challenging datasets will become much smoother.

---

