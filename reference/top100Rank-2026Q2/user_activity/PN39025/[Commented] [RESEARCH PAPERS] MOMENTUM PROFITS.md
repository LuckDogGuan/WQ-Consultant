# [RESEARCH PAPERS] MOMENTUM PROFITS

- **链接**: [Commented] [RESEARCH PAPERS] MOMENTUM PROFITS.md
- **作者**: PH82915
- **发布时间/热度**: 1年前, 得票: 57

## 帖子正文

Hi everyone! A classic paper I recommend for new users is  **"Momentum Profits"**  by Jegadeesh and Titman. This paper sparked my interest in momentum strategies when I started working on alphas.

**Abstract:** 
The authors find that stocks with strong performance in the past 3-12 months tend to continue outperforming, suggesting a simple yet powerful momentum factor for predicting returns.

**Idea:**

- **Momentum Alpha:**  Build a signal based on past returns (e.g., 6-month return).
- **Reversal:**  Explore the limits of momentum by testing long-term reversal patterns.

**Data on WQBrain:**

- Use rolling returns over different periods to create momentum-based alphas (e.g., ts_delta or ts_sum for price data).

This paper is perfect for brainstorming your first momentum alpha.

**Link:**   [https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf)

---

## 讨论与评论 (35)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi  [PH82915](/hc/en-us/profiles/1532005543462-PH82915) ,

Thanks so much for the detailed feedback and suggestions! I really appreciate you taking the time to share your expertise. Thanks again for your guidance.

---

### 评论 #2 (作者: TD17989, 时间: 1年前)

That’s an excellent recommendation! The paper "Momentum Profits" by Jegadeesh and Titman is indeed a foundational read for anyone interested in momentum-based strategies. Your insights on how the authors suggest that past winners tend to keep winning and the idea of using past returns to predict future performance are spot-on.

---

### 评论 #3 (作者: TN51777, 时间: 1年前)

For reversal idea, it can implement easily on websim, we can try example idea alpha, or using -return with high decay, or (high - low)/ close, or using MA and MACD and RSI in technical indicator to build alpha.

---

### 评论 #4 (作者: TN51777, 时间: 1年前)

However momentum idea is harder, in websim it take longer period for momentum idea working. In my experience, you should try momentum idea for years, by setting time-series operators to 252 or 500 days to find a robust signal

---

### 评论 #5 (作者: AK98027, 时间: 1年前)

The paper "Momentum Profits" by Jegadeesh and Titman is indeed foundational for understanding momentum-based strategies. It establishes that buying past winners and selling past losers can yield significant risk-adjusted excess returns. Key insights from their research include:

- **Persistence of Winners** : The authors found that stocks that performed well in the past tend to continue performing well in the future, supporting the idea of momentum in stock prices.
- **Market Efficiency Challenge** : Their findings challenge the notion of weak-form market efficiency, as the ability to predict future performance based on past returns contradicts the efficient market hypothesis.
- **Empirical Support** : Subsequent studies have replicated their results across various markets and asset classes, reinforcing the robustness of momentum strategies.

Overall, Jegadeesh and Titman's work has sparked extensive research into momentum, highlighting its significance in asset pricing and investment strategies.

---

### 评论 #6 (作者: TN48752, 时间: 1年前)

The idea of building a momentum alpha based on past returns is both simple and powerful. By looking at metrics like the 6-month return, you can create a signal that captures momentum. Additionally, testing long-term reversal patterns is an interesting extension, allowing for further refinement of momentum strategies by exploring when momentum might reverse after an extended period.

---

### 评论 #7 (作者: PH82915, 时间: 1年前)

@TN51777 Why is the momentum idea more challenging to implement, and why does it take a longer period, such as 252 or 500 days, for it to work effectively in websim? How can setting time-series operators to these extended periods help in finding a more robust momentum signal?

---

### 评论 #8 (作者: AK98027, 时间: 1年前)

That’s an excellent recommendation! The paper "Momentum Profits" by Jegadeesh and Titman is indeed a foundational read for anyone interested in momentum-based strategies. Your insights on how the authors suggest that past winners tend to keep winning and the idea of using past returns to predict future performance are spot-on.

---

### 评论 #9 (作者: NH84459, 时间: 1年前)

Momentum strategies are built on the idea that securities that have performed well in the recent past (e.g., the last 3-12 months) tend to continue outperforming in the short-term. The key steps for constructing a momentum alpha are:

1. **Define the Lookback Period:**
   - Momentum is usually measured by price performance over a fixed time horizon, such as 6 months. You can use a  **6-month return**  or adapt it to other timeframes based on your research.

---

### 评论 #10 (作者: AC63290, 时间: 1年前)

In finance, investors often track sentiment through various tools like sentiment analysis on news and social media, investor surveys, or market indicators like the VIX (Volatility Index). These tools help paint a picture of how market participants are feeling, whether that’s a sense of fear (which could drive a sell-off) or optimism (which could push prices higher).

---

### 评论 #11 (作者: DP11917, 时间: 1年前)

Fama and French’s paper emphasizes that these factors—size and value—can explain much of the variation in expected returns, and integrating them into a strategy can offer opportunities to enhance returns and build effective alpha.

---

### 评论 #12 (作者: PH82915, 时间: 1年前)

Bài nghiên cứu kinh điển "Momentum Profits" do Jegadeesh và Titman thực hiện đã khởi nguồn nhiều chiến lược giao dịch momentum trong thị trường tài chính. Nghiên cứu cho thấy các cổ phiếu có hiệu suất tốt trong 3-12 tháng qua thường tiếp tục tăng giá trong tương lai. Ngược lại, hiện tượng đảo chiều (reversal) sau thời gian dài cũng có thể xảy ra.

---

### 评论 #13 (作者: PH82915, 时间: 1年前)

Ý tưởng chính trong bài nghiên cứu

1. Momentum Alpha: Xây dựng tín hiệu dựa trên hiệu suất quá khứ (ví dụ: lợi nhuận 6 tháng trước).

2. Reversal: Khám phá giới hạn của momentum bằng cách kiểm tra các mô hình đảo chiều trong dài hạn.

---

### 评论 #14 (作者: PH82915, 时间: 1年前)

Ứng dụng trong xây dựng Alpha trên WorldQuant Brain

1. Sử dụng các hàm tính lợi nhuận rolling: 
Trên WQ Brain, hãy khai thác các hàm như ts_delta() hoặc ts_sum() để tính toán lợi nhuận qua các khung thời gian khác nhau.

Ví dụ:

alpha = ts_delta(close, 20)  # Tín hiệu momentum dựa trên biến động giá trong 20 ngày qua

2. Làm mượt tín hiệu:
Việc dùng trung bình trượt như sma() hoặc ewma() có thể làm giảm ảnh hưởng của nhiễu.

Ví dụ:

alpha = ts_delta(sma(close, 10), 5)  # Trung bình trượt 10 ngày kết hợp momentum 5 ngày

3. Thử nghiệm chiều ngược (Reversal):
Kiểm tra hiện tượng đảo chiều bằng các khung thời gian dài hơn.

Ví dụ:

alpha = -ts_delta(close, 120)  # Biểu hiện đảo chiều sau 120 ngày

4. Kết hợp khối lượng giao dịch:
Tín hiệu momentum có thể được cải thiện khi xem xét khối lượng giao dịch.

Ví dụ:

alpha = ts_delta(close, 20) * rank(volume)  # Kết hợp khối lượng giao dịch

5. Khai thác nhiều khung thời gian:
Để đảm bảo chiến lược đa dạng và hiệu quả, hãy xây dựng nhiều alpha trên các khung thời gian khác nhau (ngắn hạn và dài hạn).

---

### 评论 #15 (作者: PH82915, 时间: 1年前)

Chiến lược momentum được chứng minh là đường hướng hiệu quả trong nghiên cứu tài chính. Việc ứng dụng các kỹ thuật như momentum và reversal trên nền tảng WorldQuant Brain không chỉ giúp tăng khả năng tìm kiếm alpha tín hiệu mạnh mà còn giúp vận dụng để ứng dụng trong phân tích kỹ thuật thực chiến

---

### 评论 #16 (作者: deleted user, 时间: 1年前)

**Fundamentals Data (Real-Time):**  Use  **fundamental data**  such as  **revenue growth, P/E ratios,**  and  **debt ratios**  of companies listed in China. Combining these fundamentals with technical or sentiment signals can increase sharpness and fitness.

---

### 评论 #17 (作者: JK98819, 时间: 1年前)

- **Great suggestion!**  The "Momentum Profits" paper is a great starting point for learning how stocks that performed well in the past may continue to do well.
- **Interesting point!**  Momentum strategies work over months, but it’s worth testing how long they stay effective. Have you tried comparing short-term vs. long-term trends?
- **Good idea!**  Using tools like moving averages and MACD along with momentum might make signals more reliable. Have you tested this approach?
- **Nice thought!**  Checking if momentum eventually reverses is smart. Maybe combining this with company fundamentals (like earnings growth) could make it even better?
- **Well said!**  Momentum strategies need time to work. Testing different timeframes, like 6 months vs. 1 year, could help find the best approach.

---

### 评论 #18 (作者: RB25229, 时间: 1年前)

Your insights on how the authors suggest that past winners tend to keep winning and the idea of using past returns to predict future performance are spot-on.

---

### 评论 #19 (作者: AS16039, 时间: 1年前)

It looks like the "Momentum Profits" paper by Jegadeesh and Titman is a foundational resource for developing momentum-based alphas.

1. **Momentum Alpha:**  Use past returns (e.g.,  `ts_delta(close, 20)` ) to capture trends.
2. **Reversal Testing:**  Analyze longer periods ( `ts_delta(close, 120)` ) to detect reversals.
3. **Smoothing:**  Apply moving averages ( `sma()`  or  `ewma()` ) to reduce noise.
4. **Volume Integration:**  Rank-adjusted momentum ( `ts_delta(close, 20) * rank(volume)` ) can enhance signals.
5. **Multi-Timeframe Analysis:**  Combining short and long lookback periods increases robustness.

---

### 评论 #20 (作者: PT55616, 时间: 1年前)

Momentum idea makes alpha high turnover, I tried to reduce turnover by increase decay, or truncate, but it lose signal of alpha, can you tell me how can you reduce turnover?

---

### 评论 #21 (作者: UN28170, 时间: 1年前)

The paper "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency" by Jegadeesh and Titman (1993) examines momentum strategies in stock markets. The authors find that stocks with high past returns continue to perform well, while those with poor past returns underperform over 3- to 12-month periods. This momentum effect is not due to systematic risk or delayed reactions to common factors. However, some abnormal returns dissipate over the next two years. The findings challenge contrarian strategies and suggest that markets do not fully adjust to new information, impacting stock price efficiency and investment strategies.

---

### 评论 #22 (作者: GO84876, 时间: 1年前)

Jegadeesh and Titman’s ‘Momentum Profits’ is a foundational paper in momentum investing, offering strong empirical evidence that past winners continue to outperform over intermediate time horizons. The study’s findings remain relevant today, influencing trading strategies and quantitative finance research. The idea of momentum-based alphas using rolling returns is particularly insightful, and I’m interested in exploring how different lookback periods impact performance across various market conditions. Additionally, the interplay between momentum and long-term reversal raises intriguing questions about optimal holding periods and risk management strategies. This paper provides a great starting point for developing systematic trading signals.

---

### 评论 #23 (作者: UN28170, 时间: 1年前)

The paper  *"Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency"*  by Jegadeesh and Titman (1993) examines momentum trading strategies. It finds that stocks with strong past performance continue to outperform those with weak past performance over 3- to 12-month horizons, generating abnormal returns. These returns are not fully explained by systematic risk or delayed reactions to market-wide factors. However, momentum profits partially reverse after two years, suggesting that price overreaction plays a role. The study challenges weak-form market efficiency, indicating that stock prices do not fully reflect available information in the short-to-medium term.

---

### 评论 #24 (作者: DK30003, 时间: 1年前)

However momentum idea is harder, in websim it take longer period for momentum idea working. In my experience, you should try momentum idea for years, by setting time-series operators to 252 or 500 days to find a robust signal

---

### 评论 #25 (作者: HH28380, 时间: 1年前)

The idea of building a momentum alpha based on past returns is both simple and powerful. By looking at metrics like the 6-month return, you can create a signal that captures momentum. 
Additionally, testing long-term reversal patterns is an interesting extension, allowing for further refinement of momentum strategies by exploring when momentum might reverse after an extended period.

---

### 评论 #26 (作者: PY62071, 时间: 1年前)

Key Aspects of Momentum Profit in Quant Finance

Momentum Strategies

1.Time-Series (Absolute) Momentum: If an asset has had positive returns over a past period, it is expected to continue rising, and vice versa.

Cross-Sectional (Relative) Momentum: Ranks assets based on past performance and goes long on top-performing assets while shorting underperformers.

2.Factors Driving Momentum Profitability

Behavioral Biases: Investor overreaction, underreaction, and herding behavior.

Market Microstructure: Slow information diffusion and liquidity constraints.

Risk-based Theories: Higher returns compensate for higher risks.

3.Challenges & Risks

Momentum Crashes: Sudden trend reversals cause losses.

Transaction Costs: High turnover strategies incur costs.

Market Regimes: Works well in trending markets but struggles in mean-reverting ones.

---

### 评论 #27 (作者: XD81759, 时间: 1年前)

Hey there! This "Momentum Profits" paper is a great pick. Momentum factor, as it says, uses past returns to predict future performance. Building a signal from 6 - month return is a solid start. For reversal, look at long - term price trends. On WQBrain, using functions like ts_delta or ts_sum for price data to get rolling returns is key. It helps create momentum - based alphas. Thanks for sharing this valuable resource, just like our forum would do!

---

### 评论 #28 (作者: SK84434, 时间: 1年前)

Valuble and very insightful knowledge!

---

### 评论 #29 (作者: TD37298, 时间: 1年前)

The concept of building momentum alpha based on past returns is both straightforward and powerful. By considering metrics like 6-month returns, you can generate signals that capture momentum. Furthermore, examining long-term reversal patterns is an interesting extension, allowing for further refinement of momentum strategies by exploring when momentum might reverse after an extended period.

---

### 评论 #30 (作者: GN51437, 时间: 1年前)

In practical terms, how significant are transaction costs and market impact when implementing momentum strategies, and could these factors substantially diminish the alpha described?

---

### 评论 #31 (作者: NH16784, 时间: 1年前)

Thanks  [PH82915](/hc/en-us/profiles/1532005543462-PH82915)  for your information, I am having trouble with when to use momentum and when to use reversal, can you help me with this?

---

### 评论 #32 (作者: IW96661, 时间: 1年前)

Great pick! Jegadeesh and Titman's momentum paper is a true classic — simple, intuitive, and still highly relevant for alpha generation. Your breakdown is super clear, especially the link between short-term momentum and longer-term reversal exploration. Also love the practical tip on using  `ts_delta`  and  `ts_sum`  in WQ Brain — perfect starting points for new users testing momentum ideas. Thanks for sharing!

---

### 评论 #33 (作者: SY65468, 时间: 1年前)

Consider enhancing the basic momentum approach by integrating short-term momentum (e.g., 3–6 months) with long-term reversal effects (e.g., 3–5 years) into a composite signal. Additionally, applying cross-sectional ranking can help differentiate relative outperformers from underperformers more effectively. For further refinement, you may also explore risk-adjusting the momentum signal using measures such as volatility or beta to improve the robustness and reliability of the alpha.

---

### 评论 #34 (作者: CW99271, 时间: 10个月前)

这是一个很好的推荐！Jegadeesh 和 Titman 的论文“动量利润”对于任何对基于动量的策略感兴趣的人来说确实是一本基础读物。您对作者如何表明过去的赢家往往会继续获胜以及使用过去的回报来预测未来表现的想法的见解是正确的。

---

### 评论 #35 (作者: KU30147, 时间: 6个月前)

Very informative and helpfull.

---

