# [BRAIN TIPS] Troubleshooting common error messages

- **链接**: [Commented] [BRAIN TIPS] Troubleshooting common error messages.md
- **作者**: NL41370
- **发布时间/热度**: 5个月前, 得票: 4

## 帖子正文

Here are the list of frequently encountered error messages on the Simulate page. Along with the likely cause and resolutions.

**Error message**

**Likely cause & resolution**

Attempted to use unknown variable

An unavailable variable was included within the expression. Check if your variable has a typo or if you are using the right region in the settings. Tip: Font color of data fields and operators show up as blue text, if used correctly in the expression.

Unexpected end of input

A common syntax error usually comes from missing parentheses or missing semi-colon. 
Example: "rank(sales/assets" would raise this error

Expression cannot be empty

This error is often raised when users assign their alpha to a variable without actually calling it afterwards.
Example: "alpha = -ts_delta(close,5);" would raise the error but "alpha = -ts_delta(close,5); alpha" would not.

Illegal group index value, cannot exceed number of elements

To ensure high performance of platform, a check is made on group indices' values during simulation. Index values should not exceed amount of elements belonging to all indexed groups. If an error message is raised, it is likely that groups' index used in one of operators is not dense (not dense index looks like [0, 5, 8, 26, 107]). In this case, using "densify(group)" instead of "group" will help.

Illegal group index value, cannot be negative

We don't allow negative values for group index, to resolve this problem, try using densify operator.

Got invalid value for attribute "lookback", must be constant or string

This error is raised when you try to use a non-constant or string for "lookback" field of an operator. Or when you place your parameters in the wrong order.
Example: "ts_rank(sales/assets, days_from_last_change(sales))" would raise the error

Grouping data used outside of group operator

Grouping data are meant to be used in group operator only. This error is raised if you try to use the group data somewhere else.
Example: "ts_delta(industry, 5)" would raise the error

Cumulative lookback of expression exceeds available history

Due to limited data history, if you try to lookback further than we can provide, this error is raised. Notice that the cumulative lookback is considered the highest lookback used in the expression.
Example: ts_rank(ts_mean(close,20),20) would have the cumulative lookback of 40.

You have reached the limit of concurrent simulations. Please wait for previous simulations to finish

You can only simulate a limited amount of alphas at once so if you try to simulate more than that, this error will be raised. You have to wait until one of your previous simulations to finish to continue.

Invalid number of inputs: X, should be exactly Y input(s)

This error is raised when you provide more or less number of inputs than required.
Example: Both "group_mean(sales/assets, market)" and "group_mean(sales/assets, 1, market, 1)" would raise this error. The correct expression would be: "group_mean(sales/assets, 1, market)"

At least 10 component alphas are required for SuperAlpha Competition

Try to increase the number of selected Alphas - change the selection expression to ensure at least 10 Alphas are used in your SuperAlpha.

Your simulation has been running too long. If you are running simulations in batch, consider to reduce the number of concurrent simulation.
Please refer to  [this article](/hc/en-us/articles/18216481207575-What-is-Your-simulation-has-been-running-too-long-If-you-are-running-simulations-in-batch-consider-to-reduce-the-number-of-concurrent-simulations-error-and-how-to-resolve-it)  for more information.

Invalid data field "XXX"
The error indicates one of your component Alphas is using a DECM data field. You can exclude that particular Alpha from the selection list by adding this condition "not(in(datafields, "datafield_name"))"

"XXX" is not a valid choice
This error mostly happens when using API to simulate Alphas with wrong value of some settings. Please refer to the simulation UI to see what values are valid.

Your simulation probably took too much resource

The error happens when there are too many or large operators or datasets, even if the expression seems simple. To fix this, make your Alpha simpler or use fewer operators or datasets.

Besides, you are advised to check the data type in your Alpha expression. If you use a vector data without a vector operator, such error would also occur.

Please check if you are using vector data field correctly
If you are a using a vector operator or a vector dataset:
Do NOT using Matrix dataset on vector operators. Or vice versa
Do NOT combine Vector data field with Matrix data field, unless you first perform a vector operation on the Vector data field. Do not perform vector operation on Matrix data field
Use a Vector data field only if you have first converted it to a matrix data field using a vector operator

Max Trade option must be ON for region
Turn on Max Trade option when simulating or submitting Alphas in ASI, JPN, HKG, KOR or TW regions.

Found unused variables/ data fields/ operators "b", "a", "c"

Before submitting the Alpha, remove unused variables, operators or data fields from the expression or comment out the lines that mention the unused variables or data fields 

Incompatible unit for input at index … expected …  found …

This warning appears when you try to perform arithmetic operations (like addition or multiplication) on fields with different units. To resolve the warning,  **rank the fields involved**  so they become unitless. E.g. Instead of close + adv20, use rank(close) + rank(adv20).

Required attribute "lookback" must have a value

Please specify the lookback period: the number of past data points (days, typically) over which the operator calculates its result.

Got invalid input at index 1, expected a date in format "YYYY-MM-DD"

Provide date as a string in the format YYYY-MM-DD.

Operator … does not support event inputs

This happens when a vector field is fed into an operator that’s designed to work on matrix data. Use a vector operator like vec_avg() to convert the data to a matrix format before applying any operators like rank().

Daily simulation limit reached. Please try tomorrow (EST time zone).

Users have a daily limit on simulations based on platform traffic, though the number is high and may vary. Consultants have a higher limit than regular users.

Simulation length is below cutoff of 500 days

The alpha must have a minimum length of 500 days after the first non-zero holding value

Power Pool submissions reached quota of 1 for daily quota
You are only allowed to submit one Pure Power Pool Alpha per day (EST time zone). Please try tomorrow or submit a Power Pool Alpha that also meets Atom or regular submission criteria

Power Pool monthly submissions reached quota of 10 for monthly quota
You are only allowed to submit 10 Pure Power Pool Alphas per calendar month in one leaderboard

The simulation does not match the current IS period. Please clone this alpha and re-simulate.
Periodically, the dates in the In-sample (IS) period on BRAIN are moved forward. To resolve this error, click "Clone" on the Alpha under the Alphas page and re-simulate the cloned Alpha.

---

## 讨论与评论 (5)

### 评论 #1 (作者: PL40597, 时间: 1年前)

“SIMULATION_LIMIT_EXCEEDED” --->  do you know about this error? thanks - it happens sometimes even there is only 5 concurrent multi-simulation running.

---

### 评论 #2 (作者: YW42946, 时间: 1年前)

[PL40597](/hc/en-us/profiles/26581959673879-PL40597)  The simulation limit is a global limit on Brain server. So, if you are using multiple processes, or didn't delete request from killed processes, you may hit the limit without knowing this.

---

### 评论 #3 (作者: PL40597, 时间: 1年前)

thanks  [YW42946](/hc/en-us/profiles/12485882527255-YW42946)  - I did use multiple processes, but each only use 3 slots in the code level. so usually 6 slots are used. but there might be possible left session at server side, I guess.

thanks anyway, and the other info this above error is that it will disappear after several retries.

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

How can you prevent errors related to negative group indices, and what is the best approach to using the 'densify' operator in your expressions?

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

These are some great insights on improving alpha research and handling errors in simulations. Managing correlations between alphas, adjusting parameters dynamically, and avoiding overfitting are crucial for creating strong signals. It's also important to focus on logical consistency and to address potential losses upfront with thoughtful risk management strategies. Keep up the great work!

---

