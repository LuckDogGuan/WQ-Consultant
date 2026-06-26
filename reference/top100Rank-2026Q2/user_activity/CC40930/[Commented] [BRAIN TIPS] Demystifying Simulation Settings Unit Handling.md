# [BRAIN TIPS] Demystifying Simulation Settings: Unit Handling

- **链接**: [Commented] [BRAIN TIPS] Demystifying Simulation Settings Unit Handling.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

**What is Unit Handling?**

While developing an Alpha, standardizing units is crucial for accurate calculations. BRAIN  provides an automated "Unit Handling" feature. It detects and warns about incompatible units used within operators.

**Unit Handling in BRAIN**

Click the "Settings" button on the upper left of the simulation page. In the fourth line, you'll find the "UNIT HANDLING" section. By default, it's set to "Verify", and no other options are available. This feature only generates warning messages and doesn't affect the testing process.

![图片](images/img_ecaa73634f.png)

**When does a warning message pop up?**  **🚨**

A warning message surfaces when an expression uses incompatible data fields. For instance, if we try to calculate the sum of the close price and volume of the stock:

*close + volume*

This equation won't make sense as the units of these data fields are incompatible for direct addition.

**Keep in Mind**

The "Unit Handling" option detects potential mistakes in unit handling, but it might not spot all errors. For example, if we try to calculate the sum of ranked value and powered ranked value:

*rank(returns)^2+rank(cap)*

Here, the rank operator transforms all values from 0 to 1, skewing the distribution for the powered ranked value. As BRAIN's Unit Handling relies on the unit labels to detect inconsistencies, it can't identify this mismatch.

---

## 讨论与评论 (7)

### 评论 #1 (作者: QG16026, 时间: 1年前)

I would like to ask if there are other options for setting instrument equity? Or is Brain currently only allowing alpha on this type of asset?

---

### 评论 #2 (作者: deleted user, 时间: 1年前)

Hi, I would like to ask when should I use functions like power or sqrt, is this a signal enhancement technique?

---

### 评论 #3 (作者: LK29993, 时间: 1年前)

Yes, currently the only instrument type available on BRAIN is Equity.

---

### 评论 #4 (作者: LK29993, 时间: 1年前)

Power and square root are data transformation techniques commonly used to handle skewed data.

Square or other power transformations help to reduce skewness by spreading out the data.

Square root transformations help to reduce skewness by compressing outliers.

---

### 评论 #5 (作者: TT55495, 时间: 1年前)

How can we improve the detection of mismatched units or inconsistent data fields in Alpha models, especially in cases where the 'Unit Handling' option might miss issues, like when combining ranked values with powered ranked values? What strategies can be employed to ensure better compatibility between different data fields in these types of expressions?

---

### 评论 #6 (作者: CC40930, 时间: 1年前)

In summary,  **Unit Handling**  helps in preventing basic unit incompatibilities in calculations, but it's important to remain vigilant for more complex issues that might not be flagged.

---

### 评论 #7 (作者: ND68030, 时间: 1年前)

**Unit Handling**  refers to the systematic management and standardization of measurement units within computational models and algorithms. In the context of developing an Alpha (a trading strategy or signal), unit handling ensures that all numerical inputs and operations are dimensionally consistent. This consistency is vital for accurate calculations, meaningful comparisons, and reliable performance metrics.

---

