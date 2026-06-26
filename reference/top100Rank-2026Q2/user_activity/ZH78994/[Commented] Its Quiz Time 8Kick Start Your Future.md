# It's Quiz Time 8Kick Start Your Future

- **链接**: [Commented] Its Quiz Time 8Kick Start Your Future.md
- **作者**: DD47096
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

![图片](images/img_3ab63288a9.png)

---

## 讨论与评论 (7)

### 评论 #1 (作者: DD47096, 时间: 2年前)

It was a hard question, but we have a correct answer in comments.

> Correct answer - Such number is 1034482758620689655172413793 and has length of 28 digits.

---

### 评论 #2 (作者: TN48752, 时间: 2年前)

To solve this problem, we need to identify the smallest positive integer N that triples in value when its rightmost digit is shifted to the leftmost position. Let's denote the integer as N and its digit length as ddd.

When the rightmost digit aaa of N is shifted to the leftmost position, the new number becomes a*10^(d−1)+(N−a)/10. According to the problem, this new number is equal to 3N.

=> N = a*(10^d-1)/29

where N must be an integer, meaning a(10^d - 1) must be divisible by 29. The digit aaa can only be a value from 1 to 9 (since it's a digit), and we need to find the smallest ddd such that 10^d - 1 is divisible by 29.

To solve this, let's find the smallest ddd for which 10^d≡1 (mod 29). This means finding the order of 10 modulo 29.

Here, we see that 10^17≡1 (mod 29). Therefore, d=17.

Hence, the digit length of the smallest number N is 17.

---

### 评论 #3 (作者: AA74657, 时间: 2年前)

I am able to reduce this problem to N*29=z*((10^d)-1)
And hence ((10^d)-1) should be a multiple of 29 as z belongs to [1,9].
which means 10^d should leave remainder 1 when divided by 29 and smallest such value of d is 28.

---

### 评论 #4 (作者: TN67143, 时间: 2年前)

First, let suppose our original number is a1a2...a(n-1)a(n), of length n, called x.

Then, If we put the last digit to become the first one, we have a(n)a1...a(n-2)a(n-1), called x_transform.

Looking at the first condition, x_transform = 3*x,

We have: a(n)a1a2....a(n-2)a(n-1) = 3*a1a2...a(n-1)a(n).

Next, if we notice, the above equation have similar part of a1a2...a(n-1), just difference that, the left side, they are of factor 1, but the right side, they are of factor 30. Therefore, we may wish to use this insight to solve our problem.

If we multiply both part with 10, then adding a(n), we shall have:

10*a(n)a1a2...a(n-2)a(n-1) + a(n) = 30*a1a2....a(n-1)a(n) + a(n)

Leading to: a(n)a1a2...a(n-1)a(n) = 30*x + a(n)

If we separate the a(n) in the first digit and the rest of a1a2...a(n-1)a(n), we have:

a(n)*10^(n+1) + x = 30*x + a(n)

If we take a(n) and x on each side, we have:

a(n) * (10^(n+1) - 1) = 29*x,

Therefore, x = a(n) * (10^(n+1)-1)/29.

Since x is a positive integer and a(n) is a digit number in [1;9], we need to have 29|(10^(n+1)-1).

Here, since (10, 29) = 1 and 29 is a prime number, then if we apply Euler theorem (or Fermat little theorem in general case:  [https://crypto.stanford.edu/pbc/notes/numbertheory/order.html](https://crypto.stanford.edu/pbc/notes/numbertheory/order.html) ), we shall have: 29|(10^(29-1)-1) or 29|(10^28-1).

If we try n=27 and n+1 = 28, we shall see they they satisfy the condition x_transform = 3*x with many value of a(n) in [1;9].

If we assume m is the smallest length of x, then we should have 1<=m<=27.

From here we can try out different approach to find m.

The first one could be trying out each value of m in [1; 27] to find m. This one may work when the range is relatively small. If our initial factor increase, then manual approach may cost us many time trying.

The second approach could be ask for computer power to help. We may need a divisable module to test the divisibility and a while loop to find m.

The third approach may work using group theory. If we can prove (a,a^2,...,a^(p-1)) is equivalent to (1,2,...,p-1) modulo p, with (a, p) = 1 and p is a prime number, then there doesn't exist a positive number k in the range [1, p-1] such that a^(p-1) is equeivalent to a^k modulo p. Therefore, p-1 is the smallest positive integer such that a^(p-1) is equivalent to 1 modulo p. Here, a = 10, and p = 29. So m = p-2 = 27. This theory-based approach may work for some specific class and condition with the generalize problem of x_transform = f*x when 10*f-1 is a prime number.

To conclude, the value we need to find is 27.

What do you think about my solution and approach?

Thanks!

Best regards.

---

### 评论 #5 (作者: MC63847, 时间: 1年前)

suppose that the number form is 'Az'. A is a number with length d-1, z is a number with length 1. So 'Az' means its value is 10A+z. Such that, shifted number form is 'zA'. Its value is 10^(d-1)z+A, which should be equal to 3(10A+z). So we get (10^(d-1)-3)z=29A. It means that 10^(d-1)-3 should be a multiple of 29. By program, we can get the smallest d=28, z=3, A=3448275862068965517241379. The smallest number is 34482758620689655172413793 with length=28.

---

### 评论 #6 (作者: AC63290, 时间: 1年前)

This puzzle asks for the smallest positive integer that triples in value when its rightmost digit is shifted to become the leftmost digit.

Let the number be denoted by NNN. If the number has ddd digits, we can represent it as N=10k+xN = 10k + xN=10k+x, where:

- kkk is the number formed by removing the rightmost digit (i.e., the number without the last digit),
- xxx is the rightmost digit.

---

### 评论 #7 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

