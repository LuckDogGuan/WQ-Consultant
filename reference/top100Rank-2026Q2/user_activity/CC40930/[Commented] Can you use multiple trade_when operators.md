# Can you use multiple trade_when operators?

- **链接**: [Commented] Can you use multiple trade_when operators.md
- **作者**: IH10395
- **发布时间/热度**: 2年前, 得票: 5

## 帖子正文

Just a simple example I won't actually use. Let's say I decide to go long when volume is above average:

trade_when(volume>adv20, 1, -1)

And go short where the close is lower than the open:

trade_when(close<open, -1, -1)

It doesn't seem to me the second expression has any effect. How do I do this?

---

## 讨论与评论 (15)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi!

Try using if-else here instead of trade_when:

>>Go long when volume is above average:

volume>adv20 ? 1 : -1

>>Go short where the close is lower than the open:

close<open ? -1 : 1

But this two conditions can happen at the same time. So you need to come up with idea how to combine two conditions.

Trade when works differently, please check out this post:  [[BRAIN TIPS] Using trade_when for Event Alphas and Low Turnover Alphas](/hc/en-us/community/posts/8360363631127)

---

### 评论 #2 (作者: AT56452, 时间: 1年前)

[AG20578](/hc/en-us/profiles/12243980162327-AG20578)  - So, can we use two if_else operators together in one alpha here then?

---

### 评论 #3 (作者: YW42946, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  Yes you can, but the more condition you set the more likely you are overfitting.

---

### 评论 #4 (作者: DK20528, 时间: 1年前)

Yes, you can use multiple  `trade_when`  operators in your strategy, but it depends on the specific platform you're using and how you're structuring your code. Here’s how this typically works and how to apply it:

### General Concept of  `trade_when` :

- The  `trade_when`  operator is typically used to specify conditions under which a trade should occur, based on certain alpha signals or market factors.
- You can apply different  `trade_when`  operators to define various trading conditions, allowing more flexible control over the strategy's execution.

### Possible Ways to Use Multiple  `trade_when`  Operators:

1. **Multiple Conditional Trades:**  You can define separate conditions for entering and exiting trades and use multiple  `trade_when`  operators in a sequence. This allows you to create more complex strategies with different triggers for entering long or short positions.
   Example:
   python
   Copy code
   `# Define your trade conditions
   triggerTradeLong = (rank(volume) > 0.5)
   triggerTradeShort = (rank(volume) <= 0.5)
   # Define your alpha expressions
   AlphaLong = "long_strategy_expression"
   AlphaShort = "short_strategy_expression"
   # Execute the trades using multiple trade_when
   trade_when(triggerTradeLong, AlphaLong)
   trade_when(triggerTradeShort, AlphaShort)
   `
2. **Combining Multiple Trade Conditions in One  `trade_when` :**  You can combine multiple conditions into a single  `trade_when`  by using logical operators like  `and` ,  `or` , or  `not`  to create more complex conditions for executing trades.
   Example:
   python
   Copy code
   `triggerTrade = (rank(volume) > 0.5) and (momentum > 0.2)
   Alpha = "long_strategy_expression"
   trade_when(triggerTrade, Alpha)
   `
3. **Sequential or Different Conditions for Entry and Exit:**  You might want to separate the logic for entering and exiting trades. In this case, you would define different conditions for entering and exiting positions and use separate  `trade_when`  operators.
   Example:
   python
   Copy code
   `triggerEntry = (rank(volume) > 0.5) and (momentum > 0.2)
   triggerExit = (rank(volume) <= 0.5) or (momentum < 0)
   Alpha = "strategy_expression"
   # Execute entry when the triggerEntry condition is met
   trade_when(triggerEntry, Alpha)
   # Execute exit when the triggerExit condition is met
   trade_when(triggerExit, Alpha)
   `

### Key Considerations:

- **Order of Execution:**  Make sure the conditions you are specifying make sense logically. For example, if you have two  `trade_when`  operators for both entry and exit signals, ensure that they don’t conflict with each other. If an entry signal occurs but the exit condition is immediately true, the position might be closed right after it’s opened.
- **Overriding and Conflict:**  Using multiple  `trade_when`  operators might cause conflicts if they are not set up properly. For example, if one condition triggers a long position and another triggers a short position at the same time, it could lead to unexpected behavior.
- **Efficiency:**  Ensure that the strategy remains efficient, as adding too many  `trade_when`  conditions could potentially slow down execution, especially if the conditions are complex or involve large datasets.

### Example: Two Trade Conditions

If you want to use two separate  `trade_when`  operators to handle different entry and exit conditions (e.g., based on volume and momentum), you can structure it like this:

python

Copy code

`# Entry Condition 1: High volume
triggerEntry1 = (rank(volume) > 0.7)

# Entry Condition 2: Positive momentum
triggerEntry2 = (momentum > 0.2)

# Combine entry conditions
triggerEntry = triggerEntry1 and triggerEntry2

# Exit Condition: Low volume
triggerExit = (rank(volume) <= 0.3)

# Define Alpha (your alpha expression)
Alpha = "strategy_expression"
# Apply trade_when for Entry and Exit
trade_when(triggerEntry, Alpha)    # When entry condition is met
trade_when(triggerExit, Alpha)     # When exit condition is met
`

This approach allows for greater flexibility in managing the timing and criteria of your trades.

### Conclusion:

Using multiple  `trade_when`  operators is certainly possible, and it allows for more control over when and how trades are executed. Just ensure that you clearly define the conditions, avoid conflicts between them, and make sure the logic flows as intended in your strategy.

---

### 评论 #5 (作者: MK58212, 时间: 1年前)

Thanks for this valuable information

---

### 评论 #6 (作者: RK48711, 时间: 1年前)

You can use multiple  `trade_when`  operators to structure complex strategies with different trade conditions for entry and exit. For instance, separate  `trade_when`  operators can handle long and short signals or combined entry conditions using logical operators like  `and`  or  `or` . Ensure logical consistency to avoid conflicts, such as simultaneous opposing signals or inefficient execution. This flexibility allows for greater control over timing and criteria for trades, enhancing strategy precision.

---

### 评论 #7 (作者: SG76464, 时间: 1年前)

Thanks for this information about these operators it is concise and to the point

---

### 评论 #8 (作者: TN48752, 时间: 1年前)

I would like to ask what is the difference between if_else and trade_when? I tried to apply these 2 operators to the same alpha idea but got different results.

---

### 评论 #9 (作者: XL31477, 时间: 1年前)

**Well, the difference between if_else and trade_when is that if_else is mainly for setting up conditional expressions to decide values directly. While trade_when is focused on defining conditions for when trades should happen based on certain signals. They work in different ways in a strategy. Sometimes they might seem similar in simple cases but can lead to different results when used in more complex setups. You gotta understand their functions clearly to use them right in your alphas.**

---

### 评论 #10 (作者: LK29993, 时间: 1年前)

For if_else, there is one condition, and two alpha expressions. If the condition is true, it uses the first alpha expression; if the condition is false, it uses the second alpha expression.

For trade_when, there are two conditions, and one alpha expression. The first condition is like the "on" switch to switch on the alpha expression, while the second condition is like the "off" switch to switch off the alpha expression. There are more details to how the trade_when operator works though, you can find out more in the operator section.

---

### 评论 #11 (作者: CC40930, 时间: 1年前)

By ensuring that each  `trade_when`  is exclusive in what it’s doing (long, short, or hold), you can ensure that the short condition works independently and has an effect.

If this approach still doesn't work as expected, you might also want to check whether the dataset you're using has the appropriate values and that the conditions are not conflicting based on the market’s behavior during those periods.

---

### 评论 #12 (作者: AM60509, 时间: 1年前)

You can use multiple  `trade_when`  operators to structure complex strategies with different trade conditions for entry and exit. For instance, separate  `trade_when`  operators can handle long and short signals or combined entry conditions using logical operators like  `and`  or  `or` . Ensure logical consistency to avoid conflicts, such as simultaneous opposing signals or inefficient execution. I would suggest not using multiple trade_when as it might result in overfitting

---

### 评论 #13 (作者: KS69567, 时间: 1年前)

You're right that the second expression doesn't have any effect in your code because both the long and short positions are set to  `-1` , which means both conditions are instructing the system to take a short position. To resolve this, you should set a long position (e.g.,  `1` ) for when the conditions for buying are met and a short position (e.g.,  `-1` ) when the conditions for selling are met.

---

### 评论 #14 (作者: KS69567, 时间: 1年前)

- The first condition  `volume > adv20`  will trigger a long position (1) when the volume is above average and a neutral position (0) otherwise.
- The second condition  `close < open`  will trigger a short position (-1) when the close is lower than the open and a neutral position (0) otherwise.

This way, the second condition will indeed have an effect by taking short positions when the close is less than the open.

---

### 评论 #15 (作者: AG73209, 时间: 1年前)

Because both the long and short positions are set to -1, which indicates that both conditions are telling the system to adopt a short position, you are correct that the second expression in your code has no effect. This can be fixed by setting a long position (e.g., 1) for when the buying conditions are satisfied and a short position (e.g., -1) for when the selling conditions are satisfied.

---

