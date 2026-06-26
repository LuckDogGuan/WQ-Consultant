# It's Quiz Time 10Kick Start Your Future

- **链接**: [Commented] Its Quiz Time 10Kick Start Your Future.md
- **作者**: DD47096
- **发布时间/热度**: 2年前, 得票: 6

## 帖子正文

![图片](images/img_2f516f56c6.png)

---

## 讨论与评论 (10)

### 评论 #1 (作者: DD47096, 时间: 1年前)

Hey everyone! We release the correct answer now

> The largest possible value for B can be  **1638**

---

### 评论 #2 (作者: TN48752, 时间: 2年前)

- Since we have 100 distinct integers, the numbers can be arranged from smallest to largest, and each integer will be unique. The four smallest integers can be assumed to be close to zero to maximize their sum.
- The smallest integers can be 1, 2, 3, and 4. Thus:
  B=1+2+3+4=10
  Therefore, the largest possible value for B given that A=2024 is 10.

---

### 评论 #3 (作者: AB80462, 时间: 2年前)

The  **largest possible value for B is 1638** , which is accomplished when the four smallest integers in the set are 408, 409, 410, and 411.

**Further explanation:**

I think the smallest 4 integers (and their sum) in a set of 100 distinct integers is maximized, when the smallest value of the 4 largest integers is maximized. To do so, the 4 largest integers have to be as consecutive as possible. To this extent, I found that the smallest among the 4 largest numbers is maximized at 504, with the sum of four largest numbers then being:

504 + 505 + 506 + 509 = 2024

(505 doesn't work because 2024 - 505 - 506 - 507 = 506 (i.e. 506 would have to repeat))

---

Once we know this, we can fill the remaining 96 integers consecutively below 504 (making 504 the 97th element of this set). This would make the set start from 408, and the 100 distinct integers would be:
408, 409, 410, 411, .... 504, 505, 506, 509

- Then, the sum of 4 smallest integers become 408 + 409 + 410 + 411 = 1638

---

### 评论 #4 (作者: JC85226, 时间: 2年前)

2024 divide 4 is 506. The mean of the four largest numbers is 506.

The four largest numbers is 504, 505, 507, 508. If we use smaller number in this combination, it will reduce the space we can put the other 96 distinct integers.

Assume the every difference between the other integers is 1, to maximize the smallest numbers.

504 - (96-4) = 412.

The 4 smallest numbers will be 412, 411, 410, 409. Sum of them is 1642.

As a result, the largest possible value for B given that A=2024 is 1642.

---

### 评论 #5 (作者: AV29962, 时间: 2年前)

We need to find the maximum possible sum of the least 4 integers. Basically the scenario in which the least four numbers are the largest possible given the constraint that the sum of the largest four numbers is 2024. 
If you give it some thought, we essentially need to figure out 4 numbers that add to 2024 such that the least one among them is largest possible, by hit and trial the minimum of such four numbers would be 504. If you assume 505 as the minimum the least sum would be 505+506+507+508=2026 hence 504. Now 504 is the 4th largest of 100 distinct numbers, so the least four having the maximum sum can be obtained by the assuming the largest possible values for every other no. so 5th largest is 503, 6th is 502 and so on. 
The least 4 numbers would be 408,409,410,411 and the max sum possible is 1638. B= 1638

---

### 评论 #6 (作者: TN67143, 时间: 2年前)

Hi,

To solve this problem, first, let's assume the 100 distinct integers, sorted from smallest to largest is: a1, a2,..., a100. (a1 < a2 <...< a100, ai is in Z).

Since the sum of four largest integer is A = 2024, we have A = a97 + a98 + a99 + a100 = 2024.

We need to find the maximum of B = a1 + a2 + a3 + a4, the sum of 4 smallest ones.

Since the integers are distinct and sorted from smallest to largest, we have: a1 <= a2 - 1 <= a3 - 2 <= ... <= a97 - 96.

Similarly, we have a2 <= a98-96, a3 <= a99-96, a4 <= a100-96.

Therefore, when we add then altogether, we have:

B = a1 + a2 + a3 + a4 <= a97 - 96 + a98 - 96 + a99 - 96 + a100 - 96 = (a97 + a98 + a99 + a100) - 4*96 = A - 384 = 1640.

The equality happens when the a1 = a2-1 = a3-2 = a4-3 = ... = a100-99. Then we have A = a97 + a98 + a99 + a100 = a1 + 96 + a1 + 97 + a1 + 98 + a1 + 99 = 4*a1 + 96 + 97 + 98 + 99 = 4*a1 + 390 = 2024.

Then a1 = 408.5, not an integer.

Therefore, B < 1640. We can try out different value of B to find the maximum (that is close to 1639.)

Thank you.

---

### 评论 #7 (作者: HD75519, 时间: 1年前)

Given a sequence of 100 distinct integers, and the sum of the largest 4 numbers is 2024. To find the maximum possible value of the sum of the smallest 4 numbers.

Let us arrange the numbers in ascending order: x1, x2, x3, ... , x100 (xj > xi, if j > i)

Point 1: To maximize the smallest numbers in the sequence, the difference between 2 consecutive numbers should be minimum -> since the numbers are integers, the minimum difference is therefore 1.

Point 2: Finding x97, x98, x99, x100: Let us write them as a, a+1, a+2, a+3 since they are consecutive integers. 4a+6 = 2024 => solving for a gives 504.5 which is not an integer. So 4 consecutive numbers cannot give a sum of 2024. So, let us just increase the largest number by some value so that we get integers for the greatest 4 numbers. For this we need the combination of a, a+1, a+2, a+5 = 4a+8, giving a as 504.

Now x97 - x1 = 96 (since they are consecutive) => x1 = 408.

x1 + x2  + x3 + x4 = 408 + 409 + 410 + 411 = 1638

---

### 评论 #8 (作者: MC63847, 时间: 1年前)

to make the last four numbers as large as possible, we should try to make the fourth largest number as large as possible. Suppose that the largest number is a, then the second, third and fourth largest number should be a-1, a-3, a-4, such that they meet the condition that they sum up to 2024. So, we can get that a=508. Next, we can get the last four number are 408, 409, 410, 411. They sum up to 1638

---

### 评论 #9 (作者: SP72209, 时间: 1年前)

So taking the Largest number be x

then the other three large nos will be x-1,x-2,x-3

so the sum must allign to 2024.

x+x-1+x-2+x-3=2024

solving for x we get x= 508.

so the smallest can be 100 less so 408 followed by 409,410,411

This sums up to 1638.

---

### 评论 #10 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

