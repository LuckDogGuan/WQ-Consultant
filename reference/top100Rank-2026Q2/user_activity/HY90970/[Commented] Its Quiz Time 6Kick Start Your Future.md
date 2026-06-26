# It's Quiz Time 6Kick Start Your Future

- **链接**: [Commented] Its Quiz Time 6Kick Start Your Future.md
- **作者**: DD47096
- **发布时间/热度**: 2年前, 得票: 5

## 帖子正文

![图片](images/img_6120249394.png)

---

## 讨论与评论 (20)

### 评论 #1 (作者: DD47096, 时间: 2年前)

Hey everyone! Well done!

> Correct answer - GM-C-GM

---

### 评论 #2 (作者: YZ73957, 时间: 2年前)

EDIT: There seems to be a misunderstanding with many of the other solutions there. The question says that you need to win 2 CONSECUTIVE games for the match to count as a win. It is not a typical "best of 3" series where you can win 2 games in any order. So the idea is that having a tougher opponent (the GM) in the middle game has a higher chance of breaking up your "2-game-winstreak" and hurts your chances more than intution suggests.

Tl-dr: 
GM-C-GM maximizes the probability of winning the match.

Elaboration: 
Define the following probabilities:

P(winning against colleague) = x 
P(winning against GM) = y 
The problem definition says that x > y.

Suppose we play all 3 games to the end. Then, there are 8 possible win-loss sequences:

1. WWW 
2. WWL 
3. WLW 
4. LWW 
5. LLW 
6. LWL 
7. WLL 
8. LLL

Notice that only sequences 1, 2, and 4 results in us winning the match. So we calculate the probability any of those sequences happening, for C-GM-C and GM-C-GM cases. We assume the probability of winning each game is independent.

C-GM-C: 
P(WWW) = x . y . x (where . denotes multiplication) 
P(WWL) = x . y . (1-x) 
P(LWW) = (1-x) . y . x 
Total: x . y . (2-x)

GM-C-GM: 
P(WWW) = y . x . y 
P(WWL) = y . x . (1-y) 
P(LWW) = (1-y) . x . y 
Total: x . y . (2-y)

Since x > y, it is clear that the total in the GM-C-GM case is greater, so this is the sequence of play we should be choosing to maximize our probability of winning.

---

### 评论 #3 (作者: TN48752, 时间: 2年前)

Here’s how to analyze the two possibilities:

- **C-GM-C:**
  - You have a high probability of winning the first game against your colleague (C).
  - You then have a lower probability of winning the second game against the grandmaster (GM).
  - Even if you win the first two games, you still need to win one more game to secure victory. In this scenario, your third and final game would be against your colleague (C), which again gives you a high probability of winning.
- **GM-C-GM:**
  - You have a lower probability of winning the first game against the grandmaster (GM).
  - If you win the first game, you then have a high probability of winning the second game against your colleague (C).
  - However, if you lose the first game, you then need to win the next two games to win the match. This means defeating both the grandmaster (GM) and your colleague (C), which is statistically less likely than the first scenario (C-GM-C).

Therefore, the schedule that maximizes the probability of winning the match is  **C-GM-C** . This is because you start with a high probability win and even if you lose the second game, you still have a good chance of winning the third game against your colleague (C).

---

### 评论 #4 (作者: GD59214, 时间: 2年前)

Better if you do C-GM-C

---

### 评论 #5 (作者: NG20776, 时间: 2年前)

We love any tips

---

### 评论 #6 (作者: GD59214, 时间: 2年前)

**Explanation of my answer :**

To decide between the two possible schedules for a chess match C-GM-C and GM-C-GM you need to calculate the probability of winning at least two consecutive games in each scenario. Both schedules yield the same probability formula, 2pq−pq^2, where p is the probability of winning against your colleague (C) and q is the probability of winning against the grandmaster (GM). Since p>q, you typically have a better chance with Schedule 1 (C-GM-C). This schedule leverages the higher probability of winning against your colleague in two games instead of just one, maximizing your overall chances to win the match.

---

### 评论 #7 (作者: MA44638, 时间: 2年前)

Intuition says there is more chance to win the match in C-GM-C schedule as we have to play against GM only once. But in reality, we will have higher chance of winning in GM-C-GM schedule as: we can win against C with high probability, let suppose we will surely win against C Now we have to win against GM only once in order to win the match. But in C-GM-C, if we lose against GM there is no possible chance to win the match. Hence, I will choose GM-C-GM schedule to play.

---

### 评论 #8 (作者: AJ93287, 时间: 2年前)

Play the grandmaster first, because if we win that match, we update the prior distribution for our ability and hence markedly increase the probability of beating our colleague.  (In contrast, we learn little by playing and beating our colleague first, so we would fail to significantly update the probability of next beating the grandmaster).

---

### 评论 #9 (作者: SV11672, 时间: 2年前)

As per probability of winning over colleague is higher than the probability of winning over the grandmaster,

Than the probability of winning  in schedule C-GM-C

Will be higher than the schedule  GM-C-GM .

---

### 评论 #10 (作者: TN67143, 时间: 2年前)

My answer is quite counter intuitive, but in my humble opinion, the probability of winning the match is equal in each possible schedule.

The necessary condition for the player to win is winning two consecutive matches.

Firstly, following C-GM-C schedule, in order to win the match, the player need to at least win (C-GM) or (GM-C), so the probability of winning in the first schedule is P(C->GM) + P(GM->C). Since order matters in this context, so maybe P(C->GM) != P(GM->C).

Secondly, following GM-C-GM schedule, in order to win the match, the player need to at least win (GM-C) or (C-GM), yeilding the probability of winning is P(GM->C) + P(C->GM).

Applying the associate rule of probability, we have P(C->GM)+P(GM->C) = P(GM->C)+P(C->GM).

Therefore, the probability of winning is equal in both schedule.

Hope to hear from your feedback and answer soon!

---

### 评论 #11 (作者: HY98874, 时间: 2年前)

probability of winning  in schedule C-GM-C

Will be higher than the schedule  GM-C-GM .

---

### 评论 #12 (作者: YZ73957, 时间: 2年前)

There seems to be a misunderstanding with many of the other solutions there. The question says that you need to win 2 CONSECUTIVE games for the match to count as a win. It is not a typical "best of 3" series where you can win 2 games in any order. So the idea is that having a tougher opponent (the GM) in the middle game has a higher chance of breaking up your "2-game-winstreak" and hurts your chances more than intution suggests.

Tl-dr:
GM-C-GM maximizes the probability of winning the match.

Elaboration:
Define the following probabilities:

P(winning against colleague) = x
P(winning against GM) = y
The problem definition says that x > y.

Suppose we play all 3 games to the end. Then, there are 8 possible win-loss sequences:

1. WWW
2. WWL
3. WLW
4. LWW
5. LLW
6. LWL
7. WLL
8. LLL

Notice that only sequences 1, 2, and 4 results in us winning the match. So we calculate the probability any of those sequences happening, for C-GM-C and GM-C-GM cases. We assume the probability of winning each game is independent.

C-GM-C:
P(WWW) = x . y . x (where . denotes multiplication)
P(WWL) = x . y . (1-x)
P(LWW) = (1-x) . y . x
Total: x . y . (2-x)

GM-C-GM:
P(WWW) = y . x . y
P(WWL) = y . x . (1-y)
P(LWW) = (1-y) . x . y
Total: x . y . (2-y)

Since x > y, it is clear that the total in the GM-C-GM case is greater, so this is the sequence of play we should be choosing to maximize our probability of winning.

---

### 评论 #13 (作者: LI36776, 时间: 2年前)

Saw this question before from problem 2 in  *Frederick Mosteller - Fifty Challenging Problems in Probability with Solutions* . The answer is GM-C-GM, It helps if you substitute in numbers like P(beat C) = 1, P(beat GM) = 0.01

---

### 评论 #14 (作者: VM83936, 时间: 2年前)

C-GM-C

---

### 评论 #15 (作者: TN67143, 时间: 2年前)

Interesting viewpoints.

If we don't use the tool and language of probability, we could look at this question in the following perspective: should we do the hard and challenging things first (winning the GM with low probability of winning) or do the easier thing first (with higher probability of winning).

In scenario 1, if we choose to accept some risk and do the hard things first (try to win GM), we may learn to build muscle and grow, making it easier to succeed later on (win C). In the case we are capable, this may be a good move. But if we set a little too high expectations of our capabilities, the first failure with the GM would potentially lead to other failure later on as a domino effects. As the first encounter with the GM would cost us time, energy, and resources, and they could potentially demotivate us in the following work if we are not in the similar level of GM. We have a very high probability of failure if we are not fully aware of our ability and set a higher expectations than our current level of chess mastery. In this scenario, I think it quite similar to big win or big loss. Either you win totally, or you lose totally (high risk, high returns). There are quite many real life examples of this phenomenon, where many people succeed earlier on life but gradually failing behind as time passes. 

In scenario 2, If we choose to do the easier things first (play with C), it would help us to gradually grow and build muscles. The higher probability of winning would also motivate us to continue. The reasonable expectation we set earlier on would help us to choose the right level of training with our own capabilities. Also, the quick win would also show us concrete evidences of our capabilities, motivate us to gradually and reasonably take more calculated risks and challenges, leading to a higher potential of winning and succeeding in the following and increasingly hard opponents (play with GM). It is similar to gradually and increasingly challenging tasks may help us grow and learn more reasonably than a very challenging tasks in the beginning. We have the probability of winning C higher, make it easier for us to win at least 1 match. Event if we lose in the second game with GM, we would still gain some achievements, rather than high probability of losing completely later on as in scenario 1.

Here are some of my opinions. What is your perspectives on this problems?

---

### 评论 #16 (作者: PD93606, 时间: 2年前)

It does sound counter-intuitive when we say that playing a GM twice over the colleague (C) increases the odds of winning, but this is true in this case because of the rules.
Let's think about this logically. Let's say we are so bad that we will, guaranteed, lose all the matches with the GM. Then, it wouldn't matter what order the matches are because we'll not be winning two consecutive games anytime. 
But let's say we have a small chance of winning against the GM (we'll call it x). Then for the C-GM-C matchup, we have that very small chance x of winning against the GM and the match in general (winning against the GM is the bottleneck here). However, going GM-C-GM, you have to defeat the GM one out of the two times to win, which will be more probable than playing the GM once.

Let the probability of the player winning against the GM is 1/x (x>1). This logically means that in an ideal scenario, the player will win one game out of x games. So, the more the amount of GM games, the more the chance of the player winning at least once, thereby sealing the victory.

(This is assuming defeating C is not that big of a deal, as given in the question)

---

### 评论 #17 (作者: UV28925, 时间: 2年前)

really enjoyed this discussion

---

### 评论 #18 (作者: HY90970, 时间: 2年前)

let, c be the probability of winning against C.

g be the probability of winning against GM.

c>g.

match is won implies one of the following game sequence:

WWL, LWW,WWW.

therefore,

for,

1.C-GM-C p(match is won)= 2cg(1-c)+c^2g=2cg - c^2g

2. GM-C-GM p(match is won)= 2cg - g^2c

since c>g

c^2g>g^2c

-c^2g<-g^2c

2cg-c^2g<2cg-g^2c

therefore, GM-C-GM maximizes the probability.

---

### 评论 #19 (作者: MC63847, 时间: 1年前)

suppose a is the probability to win C, b is the probability to win GM. For C-GM-C, the probability to win is ab+(1-a)ba=2ab-a^2*b. For GM-C-GM, the probability to win is ba+(1-b)ab=2ab-ab^2. So the GM-C-GM is better.

---

### 评论 #20 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

