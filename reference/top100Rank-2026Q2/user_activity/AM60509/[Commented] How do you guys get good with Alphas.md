# How do you guys get good with Alphas?

- **链接**: [Commented] How do you guys get good with Alphas.md
- **作者**: JP51577
- **发布时间/热度**: 2年前, 得票: 16

## 帖子正文

Hi guys! I just wanted to ask about the best way about learning about Alphas. I've been actively on the platform for a few days, but so far I've only managed to submit 1 Alpha, with a few of my unsubmitted ones very close to passing all tests (usually it's the sharpe that's super close to the threshold). I've watched the training videos, and also read the documents, been to the forums, but I don't seem to understand them much as well to apply them into my Alpha simulations, even the super beginner ones.

To those who've managed to consistently submit Alphas, reached silver/gold level, or managed to understand how Alphas work and are able to consistently apply the skills to improving your Alphas - how did you guys do it?

I would love to have some tips and tricks as I'm feeling super lost and demotivated. Thank you!

---

## 讨论与评论 (17)

### 评论 #1 (作者: KE15584, 时间: 2年前)

Hello,

I have been active on this platform for a few months now, and would like to share the approach I took to generate some good Alpha ideas -

1. To start off, I focused on a single equity market - US. I read up as much as possible on the various indexes (S&P 500, Nasdaq etc..) and took some time to understand the kind of companies that are listed on the indexes

2. I then moved on to Fundamental Analysis. There are numerous online resources to learn fundamental analysis of stocks, and the time spent on this will be well worth it as you can generate some really good alphas using fundamental information. To be specific, you need to have some basic knowledge about the Income Statement, Balance Sheet and Cash Flow Statement of a listed company, and the various financial ratios (profitability, leverage, liquidity etc..)

3. I then explored + analyzed the fundamental datasets available on the Brain platform and correlated each datafield to the corresponding financial / fundamental information I had learnt earlier. I simulated quite a few datafields and noted the Turnover + other test parameters to choose the best performing datafields for my Alphas

4. Next, I went through the detailed operator descriptions on the platform, several times. A good understanding of all the available operators is imperative in Alpha generation and hard work is the only way through this. It is quite important to understand cross-sectional and time-series operators, and which one to use when for best results

5. I then moved on to Technical Analysis with a focus on Price Action + Volume Analysis. I have not looked much into technical indicators yet as I have been focused only on statistical analysis of price + volume so far. This type of analysis helps me in coming up with ideas for short-term reversion signals, and so far this approach has worked for me

6. I have set apart some amount of my time daily to study Microeconomics + Quantitative Finance, all within the context of equity research (both these subjects are vast and many topics might not be immediately relevant to equity research + trading)

7. For motivation, I would suggest that you try and get all the Alpha examples given in the documentation to a 'Submittable' state (If you haven't already). This exercise is a great confidence-booster as most of the Alpha examples are based on fundamental data, and are good starting points for creating advanced Alphas

Hope this helps. Good luck !

---

### 评论 #2 (作者: KP54912, 时间: 2年前)

Hello guys am new here wanting to know how it works out

---

### 评论 #3 (作者: NL41370, 时间: 2年前)

Hi  [KP54912](/hc/en-us/profiles/23228016118039-KP54912)

We would recommend you go through  [*Read this First * - Starter Pack](https://platform.worldquantbrain.com/learn/documentation/discover-brain/read-first-starter-pack)  post first, then go through  [Learning section](https://platform.worldquantbrain.com/learn)  for better understanding. You can go through FAQs or this community for further questions.

---

### 评论 #4 (作者: AT56452, 时间: 1年前)

I would suggest you go through all the fundamental analysis ratios on investopedia. Make alphas using those.

Then, also go through the learning section given on the platform. That's extremely helpful in understanding what kind of data is available on the platform and how to tackle it.

Understand thoroughly the operators you're using. Go through the time series ones first.

---

### 评论 #5 (作者: AT56452, 时间: 1年前)

Also, attend every webinar and advisory session that is held. If you get an opportunity to attend the in person meet-ups, attend those too. You get to learn a lot in these sessions.

Then, go through the getting started series on community forum. That series is very helpful in making alphas and understanding datasets.

---

### 评论 #6 (作者: AM60509, 时间: 1年前)

Go through the Videos and documentation given on the learn section and also go through the articles.Focus on one region say USA initially to make your alphas and start with simpler datasets like price/volume and fundamental

---

### 评论 #7 (作者: DK20528, 时间: 1年前)

It sounds like you're on the right track by watching the training videos, reading documentation, and engaging with the community, but it's normal to feel overwhelmed, especially in the early stages of learning. Here are some tips to help you progress in building Alphas:

1. **Start Small & Build Gradually** : Try starting with very simple models. Even if your first Alphas don’t perform well, it’s a great way to get a feel for the process and the tools. Don't worry too much about complex strategies initially; focus on basic concepts like simple moving averages, or basic momentum indicators.
2. **Work on Improving Sharpe Ratio** : Since your Alphas are close to passing but struggle with Sharpe, try to focus on reducing the variance and optimizing your risk-return profile. You can experiment with different risk management techniques, such as adjusting the position size or adding a volatility filter.
3. **Test, Test, and Test** : Run simulations with various parameters, and be systematic about testing and iterating. Take small steps in modifying one parameter at a time and observe how it impacts performance.
4. **Focus on Features & Data** : Alphas rely heavily on the features (signals) and data quality. Make sure your data inputs are solid and that your features are statistically significant. Keep iterating on how you process data or combine multiple signals to find patterns.
5. **Understand the Core Metrics** : Dive deeper into understanding key metrics like Sharpe ratio, drawdowns, and risk-adjusted returns. Knowing exactly how they are calculated and how they influence performance can give you better intuition for designing Alphas.
6. **Engage with the Community** : Keep asking questions on the forums and discussing your Alphas with others who are further along in the process. Often, they’ll have valuable insights into issues you're facing.
7. **Look for Simple Patterns** : Early on, avoid overfitting. Stick with simpler models that capture basic market patterns. For example, basic trend-following or mean-reversion strategies can be good starting points.
8. **Leverage the Tutorials and Challenges** : Participate in challenges and analyze the solutions shared by others. These often contain useful strategies, code snippets, and model setups that can help you learn faster.
9. **Stay Consistent** : The key to learning is persistence. As you test and optimize, you’ll start to see patterns emerge, and things will click into place over time. It’s normal to feel lost at first, but consistent practice will lead to improvements.
10. **Track Your Progress** : Make sure you track what’s working and what’s not. This can help you identify trends in your performance and make adjustments more effectively.

Lastly, it's important to be patient and not get discouraged. Everyone starts somewhere, and building successful Alphas takes time and continuous improvement. Keep experimenting and refining your strategies. You'll gain more clarity and expertise with each iteration!

---

### 评论 #8 (作者: RK48711, 时间: 1年前)

It’s great that you’re engaging with training videos, documentation, and the community—feeling overwhelmed at first is normal. Start with simple models to grasp the basics, and focus on improving Sharpe ratio by reducing variance and optimizing risk-return profiles. Test systematically, experimenting with parameters one at a time. Ensure your data and features are solid, statistically significant, and well-processed. Dive into key metrics like Sharpe, drawdowns, and risk-adjusted returns to develop better intuition. Engage actively with the community for insights, avoid overfitting by sticking to simple patterns, and participate in challenges to learn faster. Stay consistent, track your progress, and be patient—improvement comes with persistence and practice.

---

### 评论 #9 (作者: MK58212, 时间: 1年前)

Thank you for the thoughtful and encouraging advice! Your insights and practical tips make the learning process feel more approachable and structured. I truly appreciate the support and guidance as I work to improve my skills. 🙏

---

### 评论 #10 (作者: SJ17125, 时间: 1年前)

It’s fantastic that you’re exploring training videos, documentation, and engaging with the community—feeling overwhelmed initially is completely normal. Start with simple models to build a strong foundation, and focus on improving the Sharpe ratio by minimizing variance and optimizing risk-adjusted returns. Systematically test your ideas by tweaking one parameter at a time and ensure your data is clean, statistically significant, and robust. Prioritize understanding metrics like Sharpe, drawdowns, and alpha decay to develop better judgment over time.

Leverage community discussions to gain new perspectives, and avoid overfitting by focusing on clear, interpretable patterns. Participate in challenges to gain practical experience and benchmark your progress. Consistently document your experiments, learn from failures, and iterate. Remember, persistence and patience are key—every step forward strengthens your expertise in creating impactful strategies. Don’t hesitate to explore emerging techniques like alternative data integration and automation to stay ahead in your journey!

---

### 评论 #11 (作者: SG76464, 时间: 1年前)

Thanks for this amazing guide to explore learning section

---

### 评论 #12 (作者: XL31477, 时间: 1年前)

**Hey  [JP51577](/hc/en-us/profiles/8712376578327-JP51577) ! I feel you. First, start simple with basic models like simple moving averages. Then, focus on improving Sharpe by reducing variance, say adjusting position size. Test systematically, changing one parameter at a time. Make sure data's good and features are significant. Understand metrics well. Engage with the community, avoid overfitting with simple patterns. Also, participate in challenges. Keep at it and be patient. You'll improve gradually.**

---

### 评论 #13 (作者: JP51577, 时间: 1年前)

Hi everyone! Thank you all for the tips and advice. I actually haven’t been to this site for a while because it was too difficult for me to understand, but I’m now more motivated to start again.

I think for now what I would need help is knowing how to use the functions to manipulate the data sets to make it submittable. I’m not really sure how to use those functions even after watching videos and reading documents. How did you guys learn to use the functions?

---

### 评论 #14 (作者: CC40930, 时间: 1年前)

Hi there! It sounds like you're on the right track, but you're feeling stuck, which is completely normal when you're learning something as complex as alpha strategy development. Here are some tips and approaches that might help you move forward and become more confident in applying and improving your alphas.

---

### 评论 #15 (作者: PL51876, 时间: 1年前)

Hi  [JP51577](/hc/en-us/profiles/8712376578327-JP51577) , you can look at  [https://platform.worldquantbrain.com/learn/operators](https://platform.worldquantbrain.com/learn/operators)  page for the meaning behind each operators. And  [../CH36668/[Commented] 【Alpha Template Collections】- Continuously UpdatePinnedAlpha Template.md](../CH36668/[Commented] 【Alpha Template Collections】- Continuously UpdatePinnedAlpha Template.md)  for some actual usage, try to replicate some ideas from the original authors and see how different operator change the output performance.

---

### 评论 #16 (作者: KS69567, 时间: 1年前)

1. **Start Simple** : Begin with basic models and intuitive operators to build confidence.
2. **Sharpe Optimization** : Minimize variance with neutralization and filters; enhance returns with risk management.
3. **Systematic Testing** : Adjust one parameter at a time and validate results step-by-step.
4. **Metrics Focus** : Prioritize understanding Sharpe ratio, drawdowns, and alpha decay for better judgment.
5. **Engage & Learn** : Leverage training, documentation, and community support to grow steadily.

---

### 评论 #17 (作者: KS69567, 时间: 1年前)

Absolutely, feeling overwhelmed is part of the learning process! Focus on small, manageable steps:

1. **Training Videos & Docs** : Absorb key concepts at your own pace.
2. **Simple Models** : Start with basic strategies to build confidence.
3. **Community** : Ask questions and share experiences—learning together makes it easier.
4. **Stay Patient** : Progress takes time; every small win adds up.

---

