# Regarding the turnover.

- **链接**: [Commented] Regarding the turnover.md
- **作者**: PT88153
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

Hey Community, can anyone suggest what are best bracket for the  **turnover** is best ?

---

## 讨论与评论 (50)

### 评论 #1 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #2 (作者: NL78692, 时间: 1年前)

Hey there! When discussing the best bracket for turnover, it generally depends on the specific strategy and operational capacity of your trading algorithm (Alpha). However, as per common guidelines and the industry benchmarks mentioned, a good turnover bracket for an Alpha is typically below 40%. B/c of some reasons:

1. **Lower Transaction Costs** : Keeping turnover under 40% usually implies lower transaction costs because you're trading less frequently. This can enhance net returns as frequent trading can eat into profits due to fees and slippage.
2. **Manageability** : Alphas with lower turnover are often easier to manage and can be more resilient to varying market conditions. High turnover strategies might require constant monitoring and quick decision-making, which could be demanding.
3. **Real-world Feasibility** : Strategies with lower turnover are more likely to be implementable in real-world trading environments where transaction costs and market impact play significant roles.

---

### 评论 #3 (作者: PP87148, 时间: 1年前)

Hi,

It is a good practice to keep the turnover  **below 30%** . So you can keep your turnover window between  **10% to 30%.**

---

### 评论 #4 (作者: TN48752, 时间: 1年前)

Hi, the best turnover range should be from 10% - 25%, too small and alpha will be almost non-trading, too large and after cost will be bad

---

### 评论 #5 (作者: HN91473, 时间: 1年前)

For the best turnover bracket, aiming for around 12-15% can be ideal. Keeping your turnover within this range helps balance the frequency of trades with transaction costs, maintaining efficiency without overly frequent adjustments. This range tends to work well for many strategies, optimizing performance while keeping costs manageable.

---

### 评论 #6 (作者: PN39025, 时间: 1年前)

Hi  [PT88153](/hc/en-us/profiles/20369380952343-PT88153) ,

If you want low revenue, I recommend you use fundamental dataset, but if you want high revenue, use price volume. Good luck!

---

### 评论 #7 (作者: VV63697, 时间: 1年前)

I think the best range for turnover is between 10 to 30 percent , above 30 percent transaction costs are also high below 10 percent is like there are very few trades that are happening(it may still still have a good OS performance though)

---

### 评论 #8 (作者: DL53864, 时间: 1年前)

A good turnover rate is likely around 15–25%. Depending on the region setting, I adjust my turnover preferences accordingly. For the USA, I can accept a slightly higher turnover, such as 20–30%.

---

### 评论 #9 (作者: SK72105, 时间: 1年前)

[PT88153](/hc/en-us/profiles/20369380952343-PT88153)  It depends on the number of datafields you use, the kind of data fields you use, and your alpha idea! The rule of thumb is to have turnover < 30%, and margin > 5%. However I think for 75% or more of your alphas you should keep turnover less than 17.5%! For categories like fundamental - you can easily achieve a turnover less than 10; while for categories like sentiment/option/pv it is sometimes hard to achieve a turnover below 15; for analyst data it truly depends on your idea - but we can again get a turnover less than 10 for it.

---

### 评论 #10 (作者: SR82953, 时间: 1年前)

Hi PT88153,

When creating an alpha, one of the most crucial factors to consider is how the submission criteria will impact the out-of-sample (OS) Sharpe performance of the alpha.

![图片](images/img_97003198c0.png)

The stats above show that alphas submitted with higher turnover rates (above 20%) tend to yield better OS Sharpe performance. However, submitting alphas with such high turnover is not generally recommended. High turnover significantly increases the number of trades, which can adversely affect the after-cost analysis of combined alpha performance—a factor that will soon play a critical role in ongoing genius programme.

Therefore, it is advisable to create alphas within a turnover range that strikes a balance between achieving decent OS Sharpe performance and managing the trading costs associated with the alpha.

---

### 评论 #11 (作者: VA36844, 时间: 1年前)

In my opinion, a suitable turnover range would be between 10% and 30%. I often use some datafields with high variability and good coverage, such as  `pv1` . Then, I reduce turnover by increasing the decay or using the  `trade_when()`  function.

---

### 评论 #12 (作者: KS69567, 时间: 1年前)

Balance between high-turnover and moderate/low-turnover strategies to reduce risk and smooth returns.

---

### 评论 #13 (作者: ST37368, 时间: 1年前)

Hello  [PT88153](/hc/en-us/profiles/20369380952343-PT88153)

Nothing is best here, last year WQ launched a theme for low turnover alphas, where you will get a higher multiplier when you submit alpha with below 10 turnover.

Then, a couple of days later we got another theme of the higher multiplier, there we had to submit alpha above 30 turnover.

With my experience the dataset that you are working on matters the most :)

---

### 评论 #14 (作者: MY83791, 时间: 1年前)

The turnover margin measures how much the alpha actually earns relative to its trading; it is defined as profit divided by total trade value. A good turnover is one that maximizes this ratio between the profit/Sharpe and the turnover.

So it's advicable to keep the turnover somewhere between 15-30 % 
Any further inputs are welcomed.

---

### 评论 #15 (作者: YC48839, 时间: 1年前)

我认为对于交易策略的换手率（turnover）来说，最佳的bracket取决于具体的交易目标和市场条件。然而，通常来说，换手率的合理范围可以是每天的交易量占总仓位的10-30%。当然，这也取决于你的交易频率和风险承受能力。例如，如果你是日内交易者，可能需要更高的换手率；而如果你是长期投资者，可能需要更低的换手率。有没有其他社区成员对这个问题有经验可以分享？

---

### 评论 #16 (作者: YC48839, 时间: 1年前)

作为一个量化交易爱好者，我也曾经在探索最佳的换手率范围时遇到过困惑。个人认为，YC48839 的观点是比较合理的，换手率的选择确实需要依据具体的交易目标和市场条件。例如，如果你是使用高频交易策略，可能需要更高的换手率来追求利润；而如果你是使用长期投资策略，可能需要更低的换手率来控制风险。

在我的实践中，我曾经尝试过不同的换手率，发现对于日内交易来说，20-40% 的换手率是一个比较合理的范围；而对于长期投资来说，5-15% 的换手率可能更为合适。当然，这也需要依据你的交易风格和风险承受能力来调整。

我想问一下社区的其他成员，你们在选择换手率时，有什么样的经验和心得可以分享呢？

---

### 评论 #17 (作者: SV11672, 时间: 1年前)

Hi, NL78692

"That's a great point! You're absolutely right that the ideal turnover bracket for an Alpha depends on the specific strategy and operational capacity."

---

### 评论 #18 (作者: QG16026, 时间: 1年前)

Thank you all for sharing such valuable insights about the ideal turnover bracket. It's clear that the best range depends heavily on the strategy, dataset, and trading objectives. The suggestions to aim for a range of 10-30%, balancing transaction costs and performance, are especially helpful.

---

### 评论 #19 (作者: RP41479, 时间: 1年前)

An optimal turnover range is 10-30%: above 30%, transaction costs rise; below 10%, trades are minimal, though out-of-sample performance might still be strong.

---

### 评论 #20 (作者: TL60820, 时间: 1年前)

Based on my experience, maintaining a turnover rate between 15% and 25% is ideal. This range strikes a balance, as excessively high turnover can lead to excessive transaction costs, which reduce the weight of your alpha. When turnover surpasses this threshold, the benefits of alpha may be overshadowed by the associated costs, diminishing overall performance. Additionally, it is crucial to pay close attention to the margin ratio. Properly managing both turnover and margin ensures that your strategy remains efficient and that alpha generation retains its intended impact, contributing to sustainable and effective outcomes.

---

### 评论 #21 (作者: NT63388, 时间: 1年前)

I believe Turnover should ideally range between 8% and 30%. However, Alphas with very low or extremely high Turnovers are not necessarily unsuitable for submission. To increase diversity, you could aim for the following distribution:
Turnover 8%-30%: 80%
Others: 20%
This balance allows for flexibility while maintaining focus on the most promising ranges.

---

### 评论 #22 (作者: SK95162, 时间: 1年前)

From my experience, an ideal turnover typically falls within the range of 10–25% and should remain below 30% for optimal performance.

---

### 评论 #23 (作者: KK61864, 时间: 1年前)

[PT88153](/hc/en-us/profiles/20369380952343-PT88153)    Keep the turnover somewhere between 10-25 % .above 25 percent transaction costs are also high below 10 percent is like there are very few trades that are happening, it may still still have a good OS performance though!  Any further inputs are welcomed.

---

### 评论 #24 (作者: AB15407, 时间: 1年前)

Based on my experience, turnover should ideally be in the range of 10–30%. If turnover exceeds 30%, my Sharpe ratio must be exceptionally strong; only then would I still consider it.

---

### 评论 #25 (作者: LN62753, 时间: 1年前)

The optimal turnover range is likely around 10–30%. It shouldn't be too low, as this indicates that the alpha has few trades and may struggle to capture market trends. On the other hand, if the turnover is too high, transaction costs will increase significantly.

---

### 评论 #26 (作者: CC40930, 时间: 1年前)

Turnover optimization is definitely key to building effective alphas! Striking the right balance can make a huge difference. 🚀

---

### 评论 #27 (作者: RS70387, 时间: 1年前)

For optimal turnover, aim for a range between 10% and 30%. This balance ensures sufficient trading activity to capture market trends while minimizing transaction costs. If turnover exceeds 30%, transaction costs may outweigh the benefits, but if it's below 10%, the alpha may lack sufficient trades to perform well.

---

### 评论 #28 (作者: KK76363, 时间: 1年前)

Normally I work with 20% turnover and most of the time I try to keep turnover under 30%. If we want to reduce turnover we can use decay as well.

---

### 评论 #29 (作者: SB24011, 时间: 1年前)

Hello, the ideal turnover range typically falls between 10% and 25%. If the turnover is too low, it may result in minimal trading activity, which can significantly reduce alpha, as there won’t be enough trades to generate meaningful returns. On the other hand, if the turnover is too high, transaction costs and slippage can erode the potential gains, leading to poor overall performance after accounting for these expenses. Balancing turnover within this range helps optimize both trade frequency and cost-efficiency, which is crucial for maximizing alpha

---

### 评论 #30 (作者: RB20756, 时间: 1年前)

The ideal turnover range varies by strategy, but generally, 10-30% works well, balancing trade frequency and transaction costs. Aiming for 12-15% often provides a good trade-off, with flexibility for regions like the USA where 20-30% can still be effective.

---

### 评论 #31 (作者: BS20926, 时间: 1年前)

Hi, the best optimal turnover range is around 15-25%. turnover within this range balances the frequency of trades and the transaction costs. The turnover should not be too low or too high.

---

### 评论 #32 (作者: AM60509, 时间: 1年前)

It is a good practice to keep the turnover  **below 30%** . So you can keep your turnover window between  **10% to 30%.One can use trade_when operator to reduce turnover .Use of ts_target_tvr_hump can also be employed to reduce turnover to the desired range**

---

### 评论 #33 (作者: SG76464, 时间: 1年前)

Based on my knowledge the optimal turnover should be 15 percent to 25-27 percent above 30 percent cost will rise.  The turnover percent calculates how much the alpha earns relative to its trading it is defined as profit divided by total trade value

---

### 评论 #34 (作者: AS34048, 时间: 1年前)

For optimal turnover ,It should be in between the range of 10% to 30 % , but for High Capacity Alphas Competition (HCAC), you shpuld keep the turnover below 10% .

---

### 评论 #35 (作者: AG73209, 时间: 1年前)

As per my point of view, Keeping turnover between 10% and 25% for the best results. This range captures market trends while keeping transaction costs low. Too high (above 30%) increases costs, and too low (below 10%) may not generate enough trades for strong performance.

---

### 评论 #36 (作者: KS72509, 时间: 1年前)

I try to keep my turnover between 10 to 25 percent , too less turnover-less trades will be there, turnover above 25- transaction costs will be high.

---

### 评论 #37 (作者: NM98411, 时间: 1年前)

Did you employ wavelet transforms to decompose time-series data into multiple frequency components for improved signal extraction and noise reduction?

---

### 评论 #38 (作者: SK26283, 时间: 1年前)

The ideal turnover percentage depends on the specific trading goals, risk tolerance, and investment horizon. It's essential to analyse the strategy and consider the costs and benefits of different turnover rates.I normally work with turnover of about 15-20% but in some cases where performance is good I try to keep it just below 30%.

---

### 评论 #39 (作者: PT82759, 时间: 1年前)

The ideal turnover range is typically  **10%-30%** . If turnover is too low (below 10%), there won't be enough trades to generate meaningful returns, while turnover that's too high (above 30%) increases transaction costs, impacting overall performance. It's best to keep turnover between  **15%-25%**  to optimize both trade frequency and costs.

---

### 评论 #40 (作者: CT68712, 时间: 1年前)

Hi everyone! As a newcomer to quantitative trading, I've been diving into the discussions on turnover rates. It's fascinating to see the varied opinions on what's optimal. I appreciate the insight that keeping turnover below 30% can help minimize transaction costs, which is crucial for maximizing returns. I'm personally aiming for a target of about 15% as it seems to strike a good balance between trading frequency and cost efficiency. I'd love to hear more about how seasoned traders manage their turnover while optimizing their alpha. Looking forward to learning more from the community!

---

### 评论 #41 (作者: AK40989, 时间: 1年前)

The discussion around turnover is quite insightful, especially regarding the ideal range for optimizing alpha performance. Many seem to agree that keeping turnover between 10% and 30% strikes a good balance between managing transaction costs and ensuring sufficient trading activity. Have any of you experimented with turnover rates outside this range, and what were the impacts on your alpha's performance? Sharing those experiences could provide valuable lessons for others navigating this aspect of alpha development!

---

### 评论 #42 (作者: ND68030, 时间: 1年前)

Other factors to consider when deciding on turnover include market liquidity, transaction costs, and risk management capability. In markets with low liquidity or high volatility, high turnover can lead to greater risk and increased transaction costs. Effective risk management will help adjust turnover appropriately and optimize profits

---

### 评论 #43 (作者: NG78013, 时间: 1年前)

Turnover optimization is definitely key to building effective alphas! Striking the right balance can make a huge difference.

---

### 评论 #44 (作者: NG78013, 时间: 1年前)

Hi, the best optimal turnover range is around 15-20%. turnover within this range balances the frequency of trades and the transaction costs. The turnover should not be too low or too high.

---

### 评论 #45 (作者: VG25185, 时间: 1年前)

As pointed out, turnover preferences vary by market and region. In highly liquid markets like the US, higher turnover (20–30%) can be sustainable. However, in emerging markets where spreads are wider and liquidity is lower, a lower-turnover approach (10–20%) is often preferred.

---

### 评论 #46 (作者: PT27687, 时间: 1年前)

It would be helpful to clarify what type of turnover you're referring to—are you discussing revenue, employee turnover, or perhaps something else? Understanding the specific context can help us provide more tailored suggestions for the best brackets. Looking forward to learning more about your needs!

---

### 评论 #47 (作者: VN28696, 时间: 1年前)

It depends on your strategy and execution costs. Lower turnover (e.g., <5%) works well for longer-term alphas, reducing transaction costs, while higher turnover (e.g., 20-40%) can capture short-term inefficiencies but needs tight execution. What’s your focus—short-term or long-term signals?

---

### 评论 #48 (作者: SK90981, 时间: 1年前)

The ideal turnover range is between 10% and 25%; if it is too little, alpha will essentially not trade, and if it is too great, after-cost will be poor.

---

### 评论 #49 (作者: AK40989, 时间: 1年前)

Your insights on turnover are spot on, especially the emphasis on keeping it below 40% to manage costs and enhance net returns. This balance is crucial for maintaining a sustainable trading strategy. Considering the operational challenges of high turnover strategies, how do you think traders can effectively adapt their approaches to maintain performance while minimizing turnover in volatile market conditions?

---

### 评论 #50 (作者: DK30003, 时间: 1年前)

I believe Turnover should ideally range between 8% and 30%. However, Alphas with very low or extremely high Turnovers are not necessarily unsuitable for submission. To increase diversity, you could aim for the following distribution:

---

