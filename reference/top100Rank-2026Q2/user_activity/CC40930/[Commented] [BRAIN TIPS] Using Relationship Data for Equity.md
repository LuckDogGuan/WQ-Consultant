# [BRAIN TIPS] Using Relationship Data for Equity

- **链接**: [Commented] [BRAIN TIPS] Using Relationship Data for Equity.md
- **作者**: KA64574
- **发布时间/热度**: 3年前, 得票: 8

## 帖子正文

The relationship data for equity dataset outputs various classifications and grouping of instruments based on company connections. There are 2 common ways in which we can use relationship data, and that depend on the type of the datafield, whether it is in group form or matrix form.

**For Group Form**

We can apply what we have learnt in custom neutralization, read more about it  [here]([Commented] [BRAIN TIPS] Improve your alphas with Custom Neutralization.md)

Custom neutralization allows you to neutralize your alpha on a self-defined group with the expression:  **group_neutralize(alpha, group)**

Most of grouping fields are  [sparse](https://www.pinecone.io/learn/roughly-explained/sparse-vector/#:~:text=A%20sparse%20vector%20is%20a,it%20is%20a%20sparse%20vector.) , thus we suggest using the densify function such as  **group_neutralize(alpha, densify(group))**  to avoid error while using group operators.

For example, we can take  **group_neutralize(ts_delay(close,2), densify(pv13_h2_sector))** .

**For Matrix Form**

Rel_num_comp is an example of a relationship data given in matrix form, with each row representing one data and each column representing one stock. Rel_num_comp measures the total number of companies conducting similar business to the subject company.

Example of Hypothesis: If the ratio of the company’s sales to the number of competitors is growing, then the stock price should increase.

Following the above steps an alpha could be:  **rank(sales/rel_num_comp)**

---

## 讨论与评论 (6)

### 评论 #1 (作者: TN48752, 时间: 1年前)

I haven't really seen a change when using densify and not using this operator in a group, maybe the simulation speed when using densify will be faster?

---

### 评论 #2 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #3 (作者: SK72105, 时间: 1年前)

I am encountering an warning that says

"Incompatible unit for input of "densify" at index 0, expected "Unit[Group:1]", found "Unit[]"

This warning is prevalent for all grouping datafields in pv13,pv29,pv30. I am using group_neutralize along with densify. Am I doing something incorrectly?

![图片](images/img_3415e45c27.png)  ![图片](images/img_8e43cd7d68.png)  ![图片](images/img_3ca154e87e.png)

---

### 评论 #4 (作者: deleted user, 时间: 1年前)

Try removing the densify operator in alpha to see if the error persists. I understand that densify will split the group into multiple ranges and speed up the simulation a bit, but it won't improve alpha.

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

Using relationship data for equity can be beneficial depending on whether it's in group or matrix form. In group form, custom neutralization techniques like  `group_neutralize(alpha, densify(group))`  can be applied to neutralize alphas within groups. In matrix form, data like  `rel_num_comp`  can be used to compare sales against competitors, allowing for the creation of alphas such as  `rank(sales/rel_num_comp)` .

---

### 评论 #6 (作者: deleted user, 时间: 1年前)

- **Group Form**  data is often categorical, where instruments (such as stocks) are grouped based on certain attributes or relationships, such as industry, sector, or geographic region.
- **Neutralization with Groups** : To reduce exposure to specific factors (like sectors, industries, or regions), you can  **neutralize**  your alpha within these groups. Neutralization helps ensure that your alpha doesn't have unwanted biases towards specific groups.

---

