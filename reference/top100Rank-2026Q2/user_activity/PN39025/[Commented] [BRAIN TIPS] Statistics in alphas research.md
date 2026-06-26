# [BRAIN TIPS] Statistics in alphas research

- **链接**: [Commented] [BRAIN TIPS] Statistics in alphas research.md
- **作者**: NL41370
- **发布时间/热度**: 3年前, 得票: 18

## 帖子正文

The field of statistics has played an important role in many aspects of our lives and, you guessed it, understanding statistics is an important stepping stone on your journey of becoming a great quant. In this post, we will be discussing some basic terminologies that you will – or may already – frequently encounter.

**A)**   **Moments:**

In statistics, moments are generally used to describe the characteristics of a distribution of a random variable. The following four are the most commonly used:

**1. The first moment – Mean:**  The mean, or the expected value, is a very common metric which is represented by the arithmetic mean of all sample values drawn of the population (sample mean) or the entire population (population mean).

![image](images/img_39225ccd28.png)

**2. The second moment – Variance:**  While the mean refers to the average distance between observations and 0, the variance is a measure of dispersion of a set of values from its mean. The higher the variance , the more spread out data points are from the mean.

![image](images/img_bd513122eb.png)

The graph above shows probability density functions (PDFs) of four normally distributed variables. We notice that with a low variance variable, there will be more occurrences near its mean than its tails. Also, variables with similar variances but different means and the same type of distribution will have the same dispersion from their means thus yielding similar looking PDFs but in different places.

Common usages of variance in alpha research is calculating the historical volatility of a given stock (standard deviation of historical returns) or the consensus among analysts (variance of target prices for a given stock).

**3. The third moment – Skewness:** Sometimes, the distribution of a random variable may not be asymmetrical but “skewed” towards one side and the level of that asymmetry is measured by Skewness.

![image](images/img_1fd3657a65.png)

![image](images/img_d6e19be494.png)

A distribution is either distributed symmetrically (Skew(X)=0), negatively skewed (Skew(X)<0)  or positively skewed (Skew(X)>0). For interpretation, a negatively skewed distribution is the distribution with the mode (most frequently observed value) higher than its mean but with a greater chance of extreme negative outcomes. On the other hand, a positively skewed distribution’s mode is below its mean and extreme positive outcomes are also more likely.

**4. The fourth moment – Kurtosis:** Kurtosis is usually referred as the measurement of the “tailedness” of a distribution with the higher kurtosis means the fatter or thicker the tails of the distribution. Since the normal distribution’s kurtosis is equal to 3, we usually use excess kurtosis (kurtosis – 3) instead.

![image](images/img_74f0092528.png)

![image](images/img_c8ec6d4c33.png)

There are three types of kurtosis:

+ Mesokurtic - Kurt(X) = 0: A distribution with the same kurtosis as the normal distribution is called mesokurtic.

+ Leptokurtic - Kurt(X) > 0: A distribution with positive kurtosis would have fatter tails which suggest higher chance to observe extreme outcomes.

+ Platykurtic - Kurt(X) < 0: A distribution with negative kurtosis would have thinner tails or lower probability of extreme outcomes

Kurtosis and skewness can be combined when analyzing stock returns. Stocks with positive kurtosis and negatively skewed returns distribution may indicate higher probability of extreme drawdown.

**B) Joint variability between multiple random variables:**

Covariance is a measure of direction between two random variables. With positive covariance, greater value observed on one variable usually correspond with the observation of greater values of the other variable and vice versa. Negative covariance indicates that greater value on one variable would mainly correspond with lesser value on the other. The sign of the covariance, therefore, refers to the tendency in the linear relationship between those two variables and the magnitude provides the information of how strong the relationship is. Formulaically, covariance is defined as:

![image](images/img_ec25592d52.png)

However, the covariance is sensitive to the size of its variables so it may be difficult to compare the relationship between two different sets of variables. The correlation coefficient was, therefore, used to normalize the covariance by dividing it by the geometric mean of the two variables’ variance. As a result, correlation of two variables always range between -1 and 1, with 1 referring to perfect positive correlation and -1 perfect negative correlation.

![image](images/img_fbb49ebf04.png)

![image](images/img_92163b0453.png)

The analysis of correlation between variables can also be used in alpha research. For example, high revenue growth alone would not illustrate the full picture. A company with high revenue growth but low or negative correlation between revenue growth and net income growth may imply an ongoing cash burn period for rapid growth.

---

## 讨论与评论 (11)

### 评论 #1 (作者: NH84459, 时间: 1年前)

Hi, I haven't been able to apply much of the 3rd and 4th order moments (skewness and kurtosis) to alpha research. Could you provide some ideas on using these moments?

---

### 评论 #2 (作者: PL15523, 时间: 1年前)

Can you explain how co kurtosis and co skewness work? Are there higher order co_moment functions? And why aren't there co_mean and co_std?

---

### 评论 #3 (作者: PN39025, 时间: 1年前)

[NL41370](/hc/en-us/profiles/11433604068887-NL41370)  I found your article quite interesting. But I still don't understand how to use skewness and kurtosis, co_mean effectively.

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

Given that kurtosis can indicate the likelihood of extreme events, how would you adapt your alpha models to account for stocks with leptokurtic distributions?

---

### 评论 #5 (作者: LK29993, 时间: 1年前)

Hi NH84459! For skewness, you can look into creating alphas using option data for a start, especially looking into volatility smile/skew/smirk strategies. For kurtosis, you can try working with price volume data first.

---

### 评论 #6 (作者: LK29993, 时间: 1年前)

Hi PL15523!

The ts_co_skewness(y,x,d) operator measures the extent to which the two variables y and x experience asymmetry in their distribution. Positive value means both variables exhibit positive deviations from their means at the same time, while negative value means both variables exhibit negative deviations from their means at the same time.

The ts_co_kurtosis(y,x,d) operator measures the extent to which the two variables y and x experience extremity or tailedness in their distribution. High level of cokurtosis means the two variables tend to undergo extreme positive and negative deviations from the mean at the same time.

There is no co_std, but there is ts_covariance(y, x, d) though.

To compare the means of two variables, you can use subtract one mean from the other or divide one mean by the other, but do take note to put them in the same scale and handle for potential zero denominators.

---

### 评论 #7 (作者: LK29993, 时间: 1年前)

Hi PN39025! Could you share more about which aspects you do not understand?

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

Statistics play a vital role in quant finance, and understanding moments, covariance, and correlation is key to building effective models. Moments, like mean, variance, skewness, and kurtosis, help describe the distribution of a random variable. Covariance and correlation allow us to understand the relationships between multiple variables. In alpha research, these concepts can be used to assess volatility, growth patterns, and the strength of relationships between financial metrics, aiding in the development of robust trading strategies.

---

### 评论 #9 (作者: CT68712, 时间: 1年前)

As a 台大電機資工的學生, I find the discussion on moments and their applications in quant finance fascinating. Understanding skewness and kurtosis can really enhance our alpha research. For example, stocks with high kurtosis could indicate a higher probability of extreme outcomes, which is crucial for developing robust trading strategies. I’ve been experimenting with applying these concepts to historical stock data to gauge potential volatility and trends. Would love to hear more thoughts on practical ways to integrate these statistical measures into our models! Any tips or resources for diving deeper into this would be greatly appreciated!

---

### 评论 #10 (作者: SV11672, 时间: 1年前)

"Hi LK29993 

Great explanation of the ts_co_skewness and ts_co_kurtosis operators! It's helpful to understand how these measures can capture the asymmetry and extremity of two variables' distributions."

---

### 评论 #11 (作者: TN74933, 时间: 1年前)

Hi, can you help how to know a data is left or right skew in brain? I have some troubles with it, thanks a lot!

---

