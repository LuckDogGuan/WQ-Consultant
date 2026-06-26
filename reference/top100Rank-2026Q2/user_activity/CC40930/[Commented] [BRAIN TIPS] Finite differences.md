# [BRAIN TIPS] Finite differences

- **链接**: [Commented] [BRAIN TIPS] Finite differences.md
- **作者**: NL41370
- **发布时间/热度**: 3年前, 得票: 24

## 帖子正文

The world of derivatives is vast and full of wonders.

Let's try to adapt some mathematical concepts and formulas to the expression language. Here we will calculate the approximation of first and second order derivative of sales as a function of time using finite differences method.

**First order derivatives.**

The  **derivative**  dy/dx of the function y=f(x) at the point x0 is the  **rate of change**  of the variable y with respect to the variable x at the specified point.

As a first example, let's consider first order derivative of sales(s) over the time(t) and construct its differential approximation on a uniform grid with step(h):

(forward)dsdt=s(t+h)−s(t)h

(backward)dsdt=(s(t)−s(t−h))h

(central)dsdt=12⋅(forward+backward)=(s(t+h)−s(t−h))2h

Where s(t)− is sales at day t (for ex. today),

s(t+h)− is sales at day t+h (for ex. tomorrow, if h=1 day),

s(t−h)− is sales at day t−h (for ex. yesterday, if h=1 day).

As we can't base our stock predictions on the future data - only backward type derivative calculation suits for us.

If t - the day of prediction, the formula can be implemented on BRAIN platform as

sales(t)−sales(t−h)h=sales−ts_delay(sales,h)h=ts_delta(sales,h)h

ts_delta(sales,63)/63 - first order derivative of sales, where h=63days≈1quarter. We can omit division by h, because everything will be normalized. But if you will compare different derivatives, h should be stated.

So far, we have used only two points to calculate derivative of sales: (1)at the day of prediction, (2)after a quarter.

Guess what, we can use three!

The formula of three points first order derivative:

dsdt=s(t−2⋅h)−4⋅s(t−h)+3⋅s(t)2⋅h

In expression it will look accordingly:

ts_delay(sales,2⋅h)−4⋅ts_delay(sales,h)+3⋅sales)2⋅h where h=63 (for example).

Wait for it...

We can calculate four-point derivative!

dsdt=(−2s(t−3h)+9s(t−2h)−18s(t−h)+11s(t))6h

Expression implementation:

(−2⋅ts_delay(sales,3⋅h)+9⋅ts_delay(sales,2⋅h)−18⋅ts_delay(sales,h)+11⋅sales)6⋅h

In our case h=63 days period, a quarter. In formula, 3 quarter period doesn't have much economic sense. You can take periods of: today (0), 1 quarter ago (-1), 2 quarters ago (half a year) (-2) , 4 quarters ago (a year) (-4). The coefficients can be calculated using any on-line finite difference coefficients calculator, for example  [https://web.media.mit.edu/~crtaylor/calculator.html](https://web.media.mit.edu/~crtaylor/calculator.html) . There you need to input sampled points as -4,-2,-1,0, the derivative order is 1.

**Second-order derivatives.**

Now we will proceed to second-order derivatives.

The second-order derivative is the rate of change of the first-order derivative.

We'll start from three points, you can't calculate second order derivative for <3 points:

dsdt=(s(t)−2⋅s(t−h)+s(t−2h))h2

Expression implementation:

(sales−2⋅ts_delay(sales,h)+ts_delay(sales,2⋅h))h2

Very often, for calculating second-order derivative, one can use following expression:

ts_delta(ts_delta(sales,h),h)

And - you know it -, we can use four-point formula to calculate second-order derivative. (Please, calculate it by yourself).

**Conclusion.**

You can see that here we calculated all derivatives in one dimension - time. As you know, our world has more than 1 dimension, so we advise to try your ideas of derivatives also in 2D or even in 3D. Another thing, that you'll be delighted to discover - not only integer-order derivatives can be calculated. There is evidence of the existence of fractional order derivatives - you can find the application of finite differences method for it too.

**Links.**

[https://web.media.mit.edu/~crtaylor/calculator.html](https://web.media.mit.edu/~crtaylor/calculator.html)  - calculator for coefficients

[https://www.researchgate.net/publication/230582754_Finite_difference_methods_for_fractional_differential_equations](https://www.researchgate.net/publication/230582754_Finite_difference_methods_for_fractional_differential_equations)  - Finite difference methods for fractional differential equations

[http://web.mit.edu/16.90/BackUp/www/pdfs/Chapter12.pdf](http://web.mit.edu/16.90/BackUp/www/pdfs/Chapter12.pdf)  - In general about the method + Finite Difference Approximations in 2D

[https://en.wikipedia.org/wiki/Finite_difference#Calculus_of_finite_differences](https://en.wikipedia.org/wiki/Finite_difference#Calculus_of_finite_differences)  - useful Wikipedia link

---

## 讨论与评论 (8)

### 评论 #1 (作者: RK42336, 时间: 3年前)

Can you please elaborate further on this with some possible examples to depict typical use cases and scenarios of applying this mathematical tool in the financial markets space? It will help in gaining a better understanding and perspective.

Thank you!

---

### 评论 #2 (作者: AG20578, 时间: 3年前)

Hi!

Derivatives are often used in financial models, because it is a basic mathematical operation. 
It helps to calculate rate of different financial indicators.

For example, if you ever used ts_delta operator in your alphas (which is first order one-point derivative approximation of some variable), now you can try to use two or three or more point approximation.

Also, you can try these approximations with different financial ratios or technical indicators.

---

### 评论 #3 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

Thank you so much for the detailed and insightful post on derivatives and their applications in financial analysis. The concepts of finite difference methods, especially the first and second-order derivative calculations, not only expand our understanding of mathematical models but also have practical applications in time-series analysis and market prediction.

---

### 评论 #5 (作者: TD17989, 时间: 1年前)

Hi, I hope Brain will share more research articles explaining how to deploy alpha through derivative financial models

---

### 评论 #6 (作者: TL60820, 时间: 1年前)

Thank you for the detailed and insightful post on derivatives and their role in financial analysis. The explanation of finite difference methods, particularly for first and second-order derivative calculations, enhances our understanding of mathematical models and their practical applications, especially in time-series analysis and market prediction.

---

### 评论 #7 (作者: ND68030, 时间: 1年前)

Thank you for sharing this valuable information! The finite difference method is a powerful approach for approximating first- and second-order derivatives, particularly useful for problems involving discrete data, such as predicting sales over time. Using formulas offers varying levels of accuracy depending on the analysis needs. However, it’s worth noting that increasing the number of points also increases computational complexity. Additionally, extending this method to higher dimensions or fractional-order derivatives can unlock even greater potential applications in fields such as economics, engineering, and data science.

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

The world of derivatives is indeed vast, and understanding how to apply finite difference methods to approximate derivatives can be crucial in quantitative analysis. By using finite difference formulas, we can calculate the first and second-order derivatives of sales with respect to time, utilizing past data points. For example, the first-order derivative can be approximated using two, three, or even four points, providing more precision as we increase the number of points. Similarly, the second-order derivative, representing the rate of change of the first-order derivative, can be computed using similar principles. This approach helps us understand the rate of change in variables over time, which can be useful in financial modeling and forecasting.

---

