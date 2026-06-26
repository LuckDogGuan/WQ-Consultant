# [BRAIN TIPS] Improve your alphas with Custom Neutralization

- **链接**: [Commented] [BRAIN TIPS] Improve your alphas with Custom Neutralization.md
- **作者**: KA64574
- **发布时间/热度**: 3年前, 得票: 22

## 帖子正文

**What is neutralization?** Neutralization is a risk reduction technique that allocates capital equally on long and short position to neutralize the effect of events that drive prices of stocks within the selected group. For detailed explanation of how neutralization work, you can refer to  [**this post**]([Commented] [BRAIN TIPS] How to use the operator densify and how to use it along with other group operators like group_neutralize.md) .

**Usual neutralization method:** Since no neutralization alphas are strongly discouraged, you may already notice that your alphas are neutralized by default with neutralization options of "MARKET", "SECTOR", "INDUSTRY" and "SUBINDUSTRY".

**Custom Neutralization:** In addition to those common options, you can also use "group_neutralize()” operator to neutralize your alpha on a self-defined group instead.

***Example of custom neutralization:***

CUSTOM_GROUP = floor(rank(cap)*4.99);

group_neutralize(alpha, CUSTOM_GROUP)

**Idea explanation:**

- You first make “rank(cap)” vector of the instruments scale from 0 to 1.
- Multiply by 4.99 to expand the scale from 0 to 4.99.
- Divide all instruments into 5 buckets by using floor() operator, scaling form 0 to 4. Since we used floor() operator, all vectors are integers now. Now we have made quantile groups, based on market cap.
- The rationale behind this procedure is that, you assume there are some risks related to a company’s market capitalization thus stocks with similar size would bear the same risk. By neutralizing on the group, we mitigate that risk factor from our alpha.

**Double Neutralization:** In some cases, we may want to neutralize our alphas with multiple risk factors. In order to achieve that, we can use a technique called "Double Neutralization".

***Example of double neutralization:***

NEW_GROUP = bucket(rank(rel_num_comp), range=”0.1,1,0.1”);

CUSTOM_GROUP = (INDUSTRY+1)*1000 + NEW_GROUP;

group_neutralize(alpha, densify(group))

Idea explanation:

- First, we create a new group using “bucket” operator using “rel_num_comp” which represents the number of the instrument’s competitors. A new group is created such that instruments with the number of competitors that fall into the same decile will get assigned the same value.
- Next, by multiplying the "INDUSTRY" value with fairly large constant then adding " NEW_GROUP ", only stocks with the same industry AND with similar number of competitors would have the similar final results and get neutralized (companies that are doing business in the same industry with similar number of competitors are highly likely to be competitors).
- So in this case, we are neutralizing our alphas on companies that produce the same product, which in turn bear the same risk related to that product.

It's also worth noting that densify operator needs to be used for faster calculation, more information on densify operator can be found on  [**this post** .]([Commented] [BRAIN TIPS] How to use the operator densify and how to use it along with other group operators like group_neutralize.md)

**Tips to do well:**  Try different grouping methods and decide what suit your alphas best. Here are some example grouping methods in addition to well-known ones:

+ COUNTRY

+ EXCHANGE

+ Relationship data

+ Statistical groups

+ Create own groups with bucket operator

---

## 讨论与评论 (9)

### 评论 #1 (作者: HW98276, 时间: 1年前)

CUSTOM_GROUP = (INDUSTRY+1)*1000 + NEW_GROUP

Why would you add 1 to the INDUSTRY grouping? What does the underlying data look like for these GROUP type datafields? Would you please elaborate more on that?

Thanks!

---

### 评论 #2 (作者: YW42946, 时间: 1年前)

[HW98276](/hc/en-us/profiles/25690648092055-HW98276)  Now instead of playing with maximum and get confused. You can try out the new group_cartesian_product(g1, g2) operator to combine two group together!

---

### 评论 #3 (作者: PL15523, 时间: 1年前)

Hi, I hope there will be a webinar that guides how to build custom groups in detail. I mostly just know how to use rank(factor) for groups without any specific meaning.

---

### 评论 #4 (作者: AC63290, 时间: 1年前)

Neutralization is a risk-reduction technique that balances long and short positions to minimize group-specific risks. Standard methods include neutralizing by market, sector, or industry, while custom neutralization uses the  `group_neutralize()`  operator to create self-defined groups based on factors like market capitalization or competitor count. For example, dividing stocks into quantiles based on market cap or combining factors like industry and competition allows targeted risk mitigation. Double neutralization extends this concept by neutralizing on multiple risk factors, ensuring robust Alpha performance. Experiment with grouping methods, such as country, exchange, or statistical relationships, to refine Alphas while maintaining their core intent.

---

### 评论 #5 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #6 (作者: SK72105, 时间: 1年前)

I am encountering an warning that says

"Incompatible unit for input of "densify" at index 0, expected "Unit[Group:1]", found "Unit[]"

This warning is prevalent for all grouping datafields in pv13,pv29,pv30. I am using group_neutralize along with densify. Am I doing something incorrectly?

---

### 评论 #7 (作者: TT55495, 时间: 1年前)

Thank you for the comprehensive explanation about neutralization and its various methods! I appreciate the clear examples illustrating both custom and double neutralization techniques.

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

Neutralization is a technique used to reduce the impact of external risk factors by allocating capital equally between long and short positions within a selected group. This helps in mitigating the influence of price-driving events that affect stocks.

---

### 评论 #9 (作者: CT68712, 时间: 1年前)

I really appreciate this detailed explanation on neutralization techniques! As a newbie in quantitative trading, I'm trying to grasp these concepts better. The distinction between standard methods like sector or industry neutralization and custom approaches is especially enlightening. The example with market cap quantiles makes it clearer how we can create custom groups to manage risks effectively. I would love to see more practical applications of these techniques, especially for someone who's just starting out in this complex yet fascinating field. Thanks for sharing this valuable knowledge!

---

