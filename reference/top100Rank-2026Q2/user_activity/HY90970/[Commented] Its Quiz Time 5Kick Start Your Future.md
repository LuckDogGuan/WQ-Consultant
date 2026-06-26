# It's Quiz Time 5Kick Start Your Future

- **链接**: [Commented] Its Quiz Time 5Kick Start Your Future.md
- **作者**: DD47096
- **发布时间/热度**: 2年前, 得票: 5

## 帖子正文

New Quiz from Researchers life. ![图片](images/img_827ce0cf2a.png)

---

## 讨论与评论 (12)

### 评论 #1 (作者: DD47096, 时间: 2年前)

It was a hard one.

Correct answer

> Using geometric probability calculation in 3D. The arrival times are in a [0,7]x[0,7]x[0,7] cube. Consider a<b<c, so the total probability is of volume (7^3)/6. The part we need is when a+1>c. This resulting object can be cut in two by the a=6 plane, so we get a triangular prism of volume 3 and a tetrahedron of volume 1/6.
> **Hence the solution is (3+1/6)/(343/6)=19/343**

---

### 评论 #2 (作者: AB39149, 时间: 2年前)

If they decide independently, so we can say:

Probability of Adam =1/8

Probability of Bill =1/8

Probability of Christoph =1/8

Probability of all three meeting during particular hour presentation : (1/8)*(1/8)*(1/8) =>1/512

We have 8 hr they can meet any of hr:

=>8/512

=>1/64

---

### 评论 #3 (作者: TN48752, 时间: 2年前)

Here's how to solve the probability of Adam, Bill, and Christopher meeting during a presentation:

1. **Total number of possibilities:**  There are 8 hours of presentations (from 9am to 5pm). Each person can choose one of these 8 hours independently. So, the total number of possibilities for their choices is 8 * 8 * 8 = 512 (each person chooses 1 out of 8 options).
2. **Favorable cases:**  We only care about the scenario where all three attend the same presentation. There are 8 possible hours for this to happen (any of the 8 hours).
3. **Probability:**  The probability is the number of favorable cases divided by the total number of possibilities: Probability = (Number of favorable cases) / (Total number of possibilities) = 8 / 512 = 1 / 64

Therefore, the probability of Adam, Bill, and Christopher all meeting during a presentation is 1/64.

---

### 评论 #4 (作者: HD75519, 时间: 2年前)

1/64

---

### 评论 #5 (作者: LL97982, 时间: 2年前)

let X,Y,Z be iid U(0,1) RV that represents the arrival times of Adam, Bill and Christoph.

approach 1: joint distribution of max & min

let M = max(X,Y,Z), N = min(X,Y,Z), the probability of interest is P(0 < N < 7/8, N < M < N+1/8) + P(7/8 < N < 1, N < M < 1)

by order statistics, the joint CDF P(M<m, N<n) = m^3 (1 - ((m-n)/m)^3) for 0<n<1, n<m<1

the joint PDF f(m,n) = 6(m-n) for 0<n<1, n<m<1, 0 otherwise

using f(m,n) to compute P(0 < N < 7/8, N < M < N+1/8) + P(7/8 < N < 1, N < M < 1) gives 11/256

approach 2: inclusion exclusion of the complement

let E1, E2, E3 denote the events |X-Y| > 1/8, |Y-Z| > 1/8, |Z-X| > 1/8 respectively

we are interested in P(E1^c and E2^c and E3^c) = 1 - P(E1 or E2 or E3)

by inclusion exclusion, P(E1 or E2 or E3) = P(E1) + P(E2) + P(E3) - P(E1 and E2) - P(E2 and E3) - P(E3 and E1) + P(E1 and E2 and E3) = 3P(E1) - 3P(E1 and E2) + P(E1 and E2 and E3) by symmetry

P(E1) = (7/8)^2 as E1 is analogous to the event where X and Y are in (0,7/8), then "insert" the remaining 1/8 between X and Y

P(E1 and E2) = P(1/8<Y<7/8, X,Z are not in (Y - 1/8, Y + 1/8)) + 2P(0<Y<1/8, Y+1/8<X,Z<1) = 451/768

P(E1 and E2 and E3) = (6/8)^3 as it is analogous to the event where X,Y,Z are in (0,6/8) and "insert" the remaining 1/8 between 2 smaller number and 1/8 between 2 larger number

3P(E1) - 3P(E1 and E2) + P(E1 and E2 and E3) gives 245/256, hence the probability of interest is 11/256

approach 3: volume method

we have P(interested) = 2P(interested, X<Y) = 2 volume(interested, X < Y) by symmetry

volume(interested, X<Y) comes from the following solids:

1. 1/8<x<7/8, x<y<x+1/8, y-1/8<z<x+1/8

2. 0<x<1/8, 1/8<y<x+1/8, y-1/8<z<x+1/8

3. 0<x<1/8, x<y<1/8, 0<z<x+1/8

4. 7/8<x<1, x<y<1, y-1/8<z<1

computing the volume gives 11/512, hence the probability of interest is 11/256

---

### 评论 #6 (作者: AJ93287, 时间: 2年前)

The approach I've taken is to run a Monte Carlo simulation where each trial consists of each researcher starting a presentation in the continuous time period running from time 0 to time 7 hours.  This is because each researcher attends for exactly 1 hour and the total time period is 8 hours.

The result for 100,000 trials is obtained using the following code:

import numpy as np

np.random.seed(123)

flag_list = [ ]

for i in range(100000):

    #print(i)

    flag = None

    start_time_1 = np.random.uniform(low=0, high=7, size=1)
    start_time_2 = np.random.uniform(low=0, high=7, size=1)
    start_time_3 = np.random.uniform(low=0, high=7, size=1)

    #print(start_time_1)
    #print(start_time_2)
    #print(start_time_3)

    if (start_time_2 + 1 < start_time_1):
        #print("2 arrives and leaves before 1")
        flag = 0
    elif (start_time_2 > start_time_1 + 1):
        #print("1 arrives and leaves before 2")
        flag = 0
    elif ((start_time_3 + 1 < start_time_1) and (start_time_3 + 1 < start_time_2)):
        #print("3 arrives and leaves before 1 and 2")
        flag = 0
    elif ((start_time_3 > start_time_1 + 1) and (start_time_3 > start_time_2 + 1)):
        #print("1 and 2 arrive and leave before 3")
        flag = 0
    else:
        #print("All three meet")
        flag = 1

    flag_list.append(flag)

prob = sum(flag_list) / len(flag_list)

print(f'The probability all three meet = {round(prob, 3)} to 3 decimal places.')

Running the code above yields the probability all three meet = 0.088 to 3 decimal places.

---

### 评论 #7 (作者: NG40937, 时间: 2年前)

it would be 1/64

---

### 评论 #8 (作者: Digamber Deshmukh(DD22608), 时间: 2年前)

Probability of meeting - 1/64

---

### 评论 #9 (作者: HY90970, 时间: 2年前)

Let, a, b, c be the time points of arrival of Adam, Bill and Cristoph respectively.

0<=a, b, c <=7  -(1)

Condition of their meet can be written as

|a-b|<=1

|b-c|<=1

|c-a|<=1  -(2) 

(1) and (2) combined give region of interscetion which is

One triangular prism of height 5√3 and base edge=√2

And 2 small triangular pyramids of base edge √2 and 3 edges of 1.

Vol of triangular prism=√3a*a*h/4 

=√3 2*5√3/4=30/4=7.5

Vol of 2 pyramids=1

So, 

Probability= (7.5+1) /343=0.0248

---

### 评论 #10 (作者: MC63847, 时间: 1年前)

suppose they are a,b,c, then they all follow U[0,7]. a,b,c should satisfy some conditions, so that they will meet together. We can only consider a<b<c and finally multiply the result by 6. So, the condition will be b<a+1 and c<a+1. We can write the integral: ![图片](images/img_8ce3a6d63b.jpeg)

it means that when a<6, the b and c should satisfy b<a+1 and c<a+1; when a>=6, the upper bound for b and c is not a+1 but 7.

The result of the integral is 6*1/343*[3+1/6]=19/343

---

### 评论 #11 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #12 (作者: AK98027, 时间: 1年前)

Here's how to solve the probability of Adam, Bill, and Christopher meeting during a presentation:

1. **Total number of possibilities:**  There are 8 hours of presentations (from 9am to 5pm). Each person can choose one of these 8 hours independently. So, the total number of possibilities for their choices is 8 * 8 * 8 = 512 (each person chooses 1 out of 8 options).
2. **Favorable cases:**  We only care about the scenario where all three attend the same presentation. There are 8 possible hours for this to happen (any of the 8 hours).
3. **Probability:**  The probability is the number of favorable cases divided by the total number of possibilities: Probability = (Number of favorable cases) / (Total number of possibilities) = 8 / 512 = 1 / 64

Therefore, the probability of Adam, Bill, and Christopher all meeting during a presentation is 1/64.

---

