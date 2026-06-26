# How to get different alpha stats for custom time period by using ACE API?

- **链接**: [Commented] How to get different alpha stats for custom time period by using ACE API.md
- **作者**: VS62595
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

When we simulate an alpha we got the IS stats for 10 years but I want to get the stats for let say last 3 years or 5 years for my alpha research.

How can we use that in ACE API?

---

## 讨论与评论 (11)

### 评论 #1 (作者: PL15523, 时间: 1年前)

Hi, you can refer to my code:

```
def calculate_selfos(stats_df):    selected_rows = stats_df[stats_df['year'].isin(['2019', '2020', '2021'])]    isSharpe = selected_rows['sharpe'].mean()    selected_rows_all_years = stats_df[stats_df['year'].isin(['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'])]    osSharpe = selected_rows_all_years['sharpe'].mean()    selfos = isSharpe / osSharpe    return selfos
```

---

### 评论 #2 (作者: HY45205, 时间: 1年前)

Hi VS62595,

Great question about customizing the time period for alpha stats using the ACE API! Tailoring the analysis period is indeed crucial for nuanced alpha research.

`def calculate_alpha_stats(stats_df, start_year, end_year):
    # Filter data for the desired time period
    selected_rows = stats_df[(stats_df['year'] >= start_year) & (stats_df['year'] <= end_year)]

    # Calculate required stats
    avg_sharpe = selected_rows['sharpe'].mean()  # Example metric
    avg_drawdown = selected_rows['drawdown'].mean()  # Add other metrics if needed
return {
        "Average Sharpe": avg_sharpe,
        "Average Drawdown": avg_drawdown
    }

# Example usage
stats = calculate_alpha_stats(stats_df, 2019, 2021)
print(stats)
`

1. **Alternative Approach:**  If the stats are embedded in simulation outputs, you can directly subset the results post-simulation. For example, extracting IS or OS stats for the last 3 years from the results CSV.
2. **Direct API Query:**  If you’re fetching data from ACE API using specific endpoints, you could use  `filters`  like:
   `response = ace_api.get_alpha_stats(alpha_id, start_date="2019-01-01", end_date="2021-12-31")
   `

If you need more assistance implementing this or additional help understanding the ACE API parameters, feel free to ask. Good luck with your alpha research!

---

### 评论 #3 (作者: DP11917, 时间: 1年前)

You can use train and test directly on Brain, get this feature API to code Python on your automation framework

---

### 评论 #4 (作者: PN39025, 时间: 1年前)

You can get it from api record and then get the last elements of the array. Good luck!

---

### 评论 #5 (作者: TD84322, 时间: 1年前)

Thank you for the helpful responses and code examples! The code you shared is exactly what I needed to filter the alpha stats for a custom time period. I also appreciate the alternative approaches and insights on using the ACE API. Your help will make my project much easier to complete. Thanks again!

---

### 评论 #6 (作者: ZH78994, 时间: 1年前)

To get performance stats for the last 3 or 5 years for your alpha research, use a rolling time window or custom backtesting period that focuses on recent years. This allows you to better understand how your alpha performs under current market conditions and ensures you’re working with relevant, up-to-date data. Always make sure to adjust your evaluation metrics accordingly, as these shorter periods may provide different insights than using the full 10 years of data.

---

### 评论 #7 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #8 (作者: AC63290, 时间: 1年前)

To get IS stats for a specific time period using the ACE API, you can modify the  `testperiod`  parameter in the  `generate_alpha()`  function. Here's how to do it:

```
# For last 3 years
alpha_list = [ace.generate_alpha(x, 
                               region="GLB", 
                               universe="MINVOL", 
                               neutralization="STATISTICAL",
                               decay=0,
                               testperiod="P3Y") for x in alpha_expressions]

# For last 5 years
alpha_list = [ace.generate_alpha(x, 
                               region="GLB", 
                               universe="MINVOL", 
                               neutralization="STATISTICAL",
                               decay=0,
                               testperiod="P5Y") for x in alpha_expressions]

```

Key points:

- Use "P3Y" for 3 years
- Use "P5Y" for 5 years
- The "P" prefix indicates period
- "Y" suffix indicates years

Note: I noticed there was a typo in your error message where "testperied" was used instead of "testperiod". Make sure to use the correct parameter name "testperiod" to avoid the TypeError.

---

### 评论 #9 (作者: PT27687, 时间: 1年前)

It sounds like you're looking for a more tailored analysis for your research, which is a valuable approach. Have you looked into the specific functions within the ACE API that deal with time frames? It could be beneficial to dive into the documentation or any available user guides. Understanding how to manipulate the parameters for your time period could yield the results you need!

---

### 评论 #10 (作者: AK40989, 时间: 1年前)

Customizing alpha stats for specific time periods using the ACE API is a great way to refine your research. The code snippets shared provide a solid foundation for filtering data based on your desired years. Have you considered how varying the time frame might impact the robustness of your findings? Exploring different periods could reveal trends or anomalies that might not be apparent in a longer-term analysis, enhancing your overall insights.

---

### 评论 #11 (作者: RK48711, 时间: 1年前)

Great question! In ACE API, you can specify the in-sample (IS) period for your alpha analysis by adjusting the date range in your simulation request. If the API allows custom time frames, you may need to filter the IS stats for the last 3 or 5 years after retrieving the full 10-year data.

Check if ACE API provides parameters for defining custom IS periods—if not, a workaround could be processing the returned data to extract only the desired timeframe. Have you checked the documentation for any built-in filtering options?"**

This keeps it informative while encouraging further discussion. Let me know if you’d like a more technical response!

---

