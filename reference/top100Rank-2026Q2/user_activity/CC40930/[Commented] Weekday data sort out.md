# Weekday data sort out.

- **链接**: [Commented] Weekday data sort out.md
- **作者**: DD55723
- **发布时间/热度**: 2年前, 得票: 2

## 帖子正文

Today is Monday and I want to sort out all returns of previous Mondays in the year.

1. What operator should be used to sort out returns from previous Mondays?

2. Tomorrow is Tuesday, will keeping the operator help sort out data from previous Tuesdays in the year?

Thank you for reading and replying me.

---

## 讨论与评论 (7)

### 评论 #1 (作者: HT66349, 时间: 2年前)

Hi,

Currently, we generally do not support date fields, so there is no direct method to filter data from a specific day or a day of the week.

---

### 评论 #2 (作者: DK20528, 时间: 1年前)

To address your questions, let's break down both points:

### 1.  **Sorting Out Returns from Previous Mondays:**

To filter or sort out returns specifically from previous Mondays, you will need to check the  **day of the week**  for each date in your dataset. You can use a time-based operator to check for the days of the week and filter the returns accordingly.

In Python, the  `weekday()`  function is typically used to identify the day of the week, where:

- **0**  = Monday
- **1**  = Tuesday
- **2**  = Wednesday
- **3**  = Thursday
- **4**  = Friday
- **5**  = Saturday
- **6**  = Sunday

You can use a conditional check based on this to filter for  **previous Mondays** .

### Example (assuming you have time-series data):

python

Copy code

`import pandas as pd

# Example dataset with dates and returns
data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=365, freq='D'),
    'return': [0.01] * 365 # Example returns for simplicity
})

# Filter out returns from Mondays (0 = Monday)
data['weekday'] = data['date'].dt.weekday
previous_mondays_returns = data[data['weekday'] == 0]
`

This will give you  **all returns from Mondays**  in the dataset.

If you're using a platform like  **WorldQuant's BRAIN**  or a similar backtesting tool, you would typically use built-in time-based filters to achieve this. Look for operators like  `weekday()`  or  `dayofweek`  in the documentation, which can be used to filter or select data based on the day of the week.

### 2.  **Will Keeping the Operator Help Sort Out Data from Previous Tuesdays (Tomorrow being Tuesday)?**

No, simply keeping the operator that sorts data based on Monday (i.e., filtering using  `weekday() == 0` ) will  **not**  automatically adjust for Tuesdays when the day changes to Tuesday. The filter specifically targets  **Mondays**  based on the  `weekday() == 0`  condition. If tomorrow is Tuesday, and you want to filter data from  **previous Tuesdays** , you will need to modify the condition or logic accordingly.

For example:

- If you want to sort out returns from previous Tuesdays when tomorrow is Tuesday, you would change the condition to  `weekday() == 1`  (since Tuesday corresponds to 1).

### Example (for previous Tuesdays):

python

Copy code

`# Filter out returns from Tuesdays (1 = Tuesday)
previous_tuesdays_returns = data[data['weekday'] == 1]
`

This change in the condition ensures you're filtering for Tuesdays when the current day is Tuesday.

### Summary:

- To filter out returns from  **previous Mondays** , you should use an operator that identifies the  **weekday**  as Monday (i.e.,  `weekday() == 0` ).
- If tomorrow is Tuesday and you want to filter for  **previous Tuesdays** , you will need to adjust the condition to target Tuesday ( `weekday() == 1` ), not keep the Monday condition.

Would you like an example in a specific language or platform (like WorldQuant BRAIN) to illustrate this further?

---

### 评论 #3 (作者: MK58212, 时间: 1年前)

Thanks

---

### 评论 #4 (作者: RK48711, 时间: 1年前)

Thank you for the thorough analysis and suggestions! I see now that relying solely on open-close differences might oversimplify the strategy. I'll focus on incorporating additional indicators, improving risk management, and accounting for transaction costs and market conditions. Your point about testing across different environments and reducing trade frequency makes a lot of sense—I’ll work on refining these aspects. Thanks again for the valuable insights!

---

### 评论 #5 (作者: SJ17125, 时间: 1年前)

To filter returns from previous Mondays, check the day of the week using a function like  `weekday()` . For Mondays, filter where  `weekday() == 0` . Example in Python:

python

Copy code

`data['weekday'] = data['date'].dt.weekday
previous_mondays_returns = data[data['weekday'] == 0]
`

If tomorrow is Tuesday and you need previous Tuesday's data, adjust the condition to  `weekday() == 1` . The filter for Mondays won’t adapt automatically to Tuesdays without modification. Always update the condition to match your target day.

---

### 评论 #6 (作者: XL31477, 时间: 1年前)

**Hey! I agree with what's been said above. To sort out returns from a specific weekday like previous Mondays, indeed use an operator like weekday() and set it to 0. And as others pointed out, when it comes to a different day like tomorrow being Tuesday, you gotta change the condition to weekday() == 1 for previous Tuesdays' data. Make sure to adjust that condition based on the target weekday each time for accurate filtering.**

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

- For Mondays, you would use an operator like  `date_filter`  with  `weekday == 0` .
- For Tuesdays, you would adjust the filter to  `weekday == 1` .

You can keep the operator for Monday and later adjust it for other days of the week as necessary by changing the weekday condition.

---

