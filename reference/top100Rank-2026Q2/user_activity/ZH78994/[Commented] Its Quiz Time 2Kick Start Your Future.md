# It's Quiz Time 2Kick Start Your Future

- **链接**: [Commented] Its Quiz Time 2Kick Start Your Future.md
- **作者**: NG20776
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

New Quiz.

![图片](images/img_a8c70d6ff2.png)

---

## 讨论与评论 (20)

### 评论 #1 (作者: DD47096, 时间: 2年前)

Wow! Many of you did it right this time, congratulations! We are pleased to see different approaches to the problem.

> **Correct answer - 27/32 = 54/64 = 0.84375**

---

### 评论 #2 (作者: Osca Kipkurui(OK99740), 时间: 2年前)

3/4

---

### 评论 #3 (作者: NG20776, 时间: 2年前)

Can you give me any pointers?

---

### 评论 #4 (作者: AJ93287, 时间: 2年前)

Let 'T' denote a correct decision being made.

Let 'F' denote an incorrect decision being made.

Then, the combinations that result in an incorrect decision are:

T, F, F with a probability of 3/4 x 1/4 x 1/4 = 3/64

F, F, T with a probability of 1/4 x 1/4 x 3/4 = 3/64

F, T, F with a probability of 1/4 x 3/4 x 1/4 = 3/64

F, F, F with a probability of 1/4 x 1/4 x 1/4 = 1/64

So, the probability of an incorrect decision is 3/64 + 3/64 + 3/64 + 1/64 = 10/64

At this stage, we can deduce that the probability of a correct decision is:

1 - 10/64 = 54/64

But, let's validate the answer by considering the combinations that lead to a correct decision:

T, T, T with a probability of 3/4 x 3/4 x 3/4 = 27/64

T, T, F with a probability of 3/4 x 3/4 x 1/4 = 9/64

T, F, T with a probability of 3/4 x 1/4 x 3/4 = 9/64

F, T, T with a probability of 1/4 x 3/4 x 3/4 = 9/64

So, the probability of a correct decision is 27/64 + 9/64 + 9/64 + 9/64 = 54/64

which confirms our earlier answer.

Final answer:  the probability that the jury makes the correct decision is 54/64.

---

### 评论 #5 (作者: NG20776, 时间: 2年前)

Any other ideas?

---

### 评论 #6 (作者: DC11952, 时间: 2年前)

Another way to solve this problem, we can use the binomial distribution (with n=3, p=3/4) to look at the cases where the jury makes the correct decision based on majority voting. There are two ways they can arrive at a majority correct decision:

1. All three jurors make the correct decision.
2. Two jurors make the correct decision and one does not.

Probability of case 1 = PMF(X=3) = 3C3*(3/4)**3

Probability of case 2 (TTF, TFT, FTT) = PMF(X=2) = 3C2*(3/4)**2*(1/4)

Overall Probability = (3/4)**3 + 3*(3/4)**2*(1/4) = 0.84375

---

### 评论 #7 (作者: NG20776, 时间: 2年前)

All of you have quite different answers

---

### 评论 #8 (作者: NG40937, 时间: 2年前)

Probability of all jurors making the correct decision is (0.75)^3

Probability of exactly two making the correct decision - 3*(0.75)^3

and probability of this occurring is 0.25.Hence the probability is - 3*(0.75)^3*0.25

Summing these probabilities- (0.75)^3 + 3*(0.75)^3*0.25 = 0.84375

---

### 评论 #9 (作者: SK51905, 时间: 2年前)

P(correct decision)= 1- P(wrong decision)

P(wrong decision) = either all are wrong or just one guy is correct

P(wrong decision) = 3C3*(1/4)*(1/4)*(1/4) + 3C1*(3/4)*(1/4)*(1/4)

= (1/64)+ (9/64) = 10/64

P(correct decision)= 1-(10/64) = 54/64 = 0.84375

---

### 评论 #10 (作者: SM22750, 时间: 2年前)

3/7

---

### 评论 #11 (作者: DC79919, 时间: 2年前)

27/32 is the probability of the jury making the correct decision.

---

### 评论 #12 (作者: LK23809, 时间: 2年前)

Imagine we have a jury of three people. Each juror has a chance of making the correct decision, and that chance is like flipping a fair coin 25% (or 1/4). Now, when they vote, the final decision is based on what most of them choose.

Here’s the interesting part: If each juror is more likely to be right than wrong (meaning their chance of being correct is greater than 50%), then adding more jurors increases the likelihood that the majority decision will be correct. It’s like having more heads in a coin toss.

However, if each juror is more likely to be wrong (their chance of being correct is less than 50%), adding more jurors actually makes things worse. In this case, the best scenario is having just one juror—a single coin flip.

In our situation, where each juror’s accuracy is only 25%, the overall probability of the jury making the correct decision remains at 25%. So, it’s not very promising. But hey, at least we’re not relying on a single coin flip! 😄

---

### 评论 #13 (作者: AK35548, 时间: 2年前)

54/64

---

### 评论 #14 (作者: HT42353, 时间: 2年前)

To find the probability of the jury making the correct decision, we can analyze the different scenarios:

1. All three jurors make the correct decision.
2. Two jurors make the correct decision and one makes the incorrect decision.

For scenario 1:
The probability of all three jurors making the correct decision is (3/4)^3, since each juror has a probability of 3/4 of making the correct decision.

For scenario 2:
There are three possible ways in which two jurors can make the correct decision and one makes the incorrect decision (assuming the incorrect decision is the minority opinion):
- Two jurors in positions 1 and 2 are correct, and the third juror is incorrect.
- Two jurors in positions 1 and 3 are correct, and the second juror is incorrect.
- Two jurors in positions 2 and 3 are correct, and the first juror is incorrect.

Each of these scenarios has a probability of (3/4)^2 * 1/4, since two jurors make the correct decision with probability (3/4)^2 and the third juror makes the incorrect decision with probability 1/4.

So, the total probability of scenario 2 occurring is 3 * ((3/4)^2 * 1/4).

Now, to find the overall probability of the jury making the correct decision, we add the probabilities of scenario 1 and scenario 2:

(3/4)^3 + 3 * ((3/4)^2 * 1/4)

Let's calculate this:

(3/4)^3 + 3 * ((3/4)^2 * 1/4) = (27/64) + 3 * ((9/16) * (1/4)) = (27/64) + (27/64) = 27/32

So, the probability of the jury making the correct decision is  **27/32** .

---

### 评论 #15 (作者: CM69671, 时间: 2年前)

The probability of the Jury making the correct decision is dependent on 3 possible scenarios.

1st scenario is if all 3 Jurors make correct decision.That is if Juror 1 and Juror 2 and Juror make correct decision.

That will be 3/4×3/4×3/4 =27/64

Or the second scenario is if;

(i) Juror 1 and Juror 2 make correct decision and  Juror 3 make the wrong decision.That is;

3/4×3/4×1/4=9/64

(ii)Or if Juror 1 and Juror3 make correct decision and Juror 2 make wrong decision.That will be;

3/4×1/4×3/4=9/64

(iii)Or Juror 2 and Juror 3 make the correct decision while Juror 1 makes wrong decision.That is ;

1/4×3/4×3/4 =9/64

In total ,scenario 2 consists of 9/64 + 9/64+9/64=27/64.

Or third scenario is if,out of the three Jurors one makes the correct decision.This is possible because with one correct decision of 3/4 it overrules 2 wrong decision.one correct decision carries 75% of the vote which is a majority.Therefore

(i) Juror 1 and Juror 2 can make wrong decisions while Juror 3 make correct decision;That is 

1/4 ×1/4 ×3/4 =3/64 

(ii)Or If Juror 1 and Juror 3 make wrong decisions and Juror 2 makes correct decision.

1/4×3/4×1/4 =3/64 

(iii)Or If  Juror 2 and Juror 3 make wrong decisions and Juror 1 makes correct decision.That will be

3/4× 1/4×1/4 =3/64

The 3 rd scenario consists of total;

3/64+3/64+3/64=9/64

Therefore the probability of the Jurors making the correct decision will be if scenario 1 or scenario 2 or scenario 3 occurs.That is;

27/64 +27/64+9/64= 63/64.

ANSWER: Possibility of Jurors making the correct decision is 63/64

---

### 评论 #16 (作者: GD59214, 时间: 2年前)

I created a more general question solver using Python which would allow for you to work out the probability of the jury being correct at any probability of each juror being correct. Below is my coded solution along with my final answer for this question. Note that # are comments explaining my thought process for each step :

**from sympy import Rational**

# Probability of each juror making the correct decision

**p_correct = Rational(3, 4)**

# Probability of each juror making the incorrect decision

**p_incorrect = 1 - p_correct**

# Since the final decision is made by majority voting, the jury makes the correct decision if:

1. All three jurors make the correct decision, or

2. Any two jurors make the correct decision and the third makes the incorrect decision. Now we calculate the probability for each of these scenarios:

# All three make correct decision

**p_all_correct = p_correct * p_correct * p_correct**

# Two make correct decision and one incorrect

**p_two_correct_one_incorrect = p_correct * p_correct * p_incorrect**

# Since there are three different jurors that could be the one incorrect, multiply by 3

**p_majority_correct = 3 * p_two_correct_one_incorrect**

# Total probability that the jury makes the correct decision

**p_jury_correct = p_all_correct + p_majority_correct p_jury_correct.evalf()**

Final answer : 0.843750000000000

---

### 评论 #17 (作者: PS80322, 时间: 2年前)

54/64 = 27/32

p(correct) = (p(2 out of 3 correct) + p(all are correct))/ (total probability of all outcomes)

p(t) = p(3 are correct) + p(2 are correct) + p(1 is correct) + p(0 are correct)

solving with p(individual of being correct) = 3/4

we get 54/64

---

### 评论 #18 (作者: MC63847, 时间: 1年前)

p(2 jurors right)=3*(3/4)^2*(1/4)=27/64

p(3 jurors right)=(3/4)^3=27/64

p(final right)=p(2 jurors right)+p(3 jurors right)=54/64=27/32

---

### 评论 #19 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #20 (作者: AK98027, 时间: 1年前)

54/64 = 27/32

p(correct) = (p(2 out of 3 correct) + p(all are correct))/ (total probability of all outcomes)

p(t) = p(3 are correct) + p(2 are correct) + p(1 is correct) + p(0 are correct)

solving with p(individual of being correct) = 3/4

we get 54/64

---

