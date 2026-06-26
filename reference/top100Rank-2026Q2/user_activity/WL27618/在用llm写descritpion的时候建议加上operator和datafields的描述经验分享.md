# 在用llm写descritpion的时候建议加上operator和datafields的描述经验分享

- **链接**: 在用llm写descritpion的时候建议加上operator和datafields的描述经验分享.md
- **作者**: WL27618
- **发布时间/热度**: 11个月前, 得票: 61

## 帖子正文

如题.

不要只给llm提供表达式, 因为很多字段没法望文生义的. 加上描述之后效果好了很多, 已经算是(我觉得) 人类能阅读的范畴了.

```
signal = group_neutralize(ts_regression(ts_zscore(fnd31_milliq,252),ts_zscore(cap,252),252,rettype=0),industry);ts_target_tvr_decay(signal,target_tvr=0.1)Idea: Exploit mean reversion in illiquidity-adjusted returns after controlling for market capitalization and industry effects.Rationale for data used: Illiquidity captures price pressure, market capitalization reflects size effects, and industry accounts for sectoral biases.Rationale for operators used: ts_regression isolates the illiquidity effect net of market capitalization; group_neutralize removes industry biases.-ts_mean(ts_backfill(vec_sum(scl15_d1_conflict),22), 66)Idea: Identify stocks with recent increases in disagreement/conflict compared to their longer-term average.Rationale for data used: `scl15_d1_conflict` directly measures conflict levels.Rationale for operators used: `ts_mean` calculates the average conflict over different lookback periods. `ts_backfill` handles any missing values in the conflict data.signal= group_neutralize(ts_mean(-vec_avg(rsk60_offer), 22),sector);trade_when(vec_sum(rsk60_crowding)>-5,signal,-1)Idea: Fade the mean reversion of shorting offer rates when crowding is low.Rationale for data used: rsk60_offer reflects shorting costs; sector controls for industry bias; rsk60_crowding indicates market sentiment.Rationale for operators used: group_neutralize removes sector bias; trade_when conditions trading on crowding levels.
```

operator和datafields都可以从表达式ast解析出来. 然后平时存在本地的数据库(或者其他任何形式的文件), 从数据库把描述加进prompt. 我现在用的prompt是这样.

```
regular_alpha_fill:- role: usercontent: |You are a professional quantitative analyst. Given the following alpha expression and related information:Alpha Expression:<alpha>{alpha_regular}</alpha>Operators Used:{operator_info}Datafields Used:{datafields_info}Please complete the following analysis:- Refine the core idea of the alpha: summarize the main concept of the quantitative strategy.- Give concise reasons for using the datafields.- Give concise reasons for using the most important one or two operators.Then generate a structured output using this format (without blank lines):Idea: [fill in core idea]Rationale for data used: [concise explanation without unnecessary words]Rationale for operators used: [concise explanation of key operators]Do not include any extra commentary or formatting.
```

强调了很多次要concise .

接下来应该要让llm自动修改alpha name, 和选择提交alpha的category. 因为平时只会改tag, 这两项我都没有利用起来.

---

## 讨论与评论 (4)

### 评论 #1 (作者: DS48533, 时间: 11个月前)

haha，我是让AI在生成表达式的时候，就带有描述，用alpha#描述的方式生成

然后写了个程序，可以传入alpha#描述，解析出来平台需要的description

---

### 评论 #2 (作者: WL27618, 时间: 11个月前)

是每个回测表达式都带描述吗? 这么硬核

---

### 评论 #3 (作者: WL27618, 时间: 10个月前)

regular_alpha_fill:
  - role: user
    content: |
      You are a professional quantitative analyst. Given the following alpha expression and related information:

Alpha Expression:
      <alpha>
      {alpha_regular}
      </alpha>

Operators Used:
      {operator_info}

Datafields Used:
      {datafields_info}

Please complete the following analysis:

- Refine the core idea of the alpha: summarize the main concept of the quantitative strategy.
      - Give concise reasons for using the datafields.
      - Give concise reasons for using the most important one or two operators.

Then generate a structured description text using this format (without blank lines):

Idea: [fill in core idea] \nRationale for data used: [concise explanation without unnecessary words] \nRationale for operators used: [concise explanation of key operators]

      Do not include any extra commentary or formatting.

Then return a JSON object with:
      {
        "name": "[the most important datafield used in the alpha]",
        "description": "[the full description text exactly as above]",
        "category": "[one of PRICE_REVERSION, PRICE_MOMENTUM, VOLUME, FUNDAMENTAL, ANALYST, PRICE_VOLUME, RELATION, SENTIMENT, or empty string]"
      }

Keep the "description" exactly in the current format.  
      "category" must be chosen strictly from the allowed list or left empty.  
      Output only the JSON object without extra commentary.

重新修改了一下, 自动选择category. 不过我观察生成的category, 感觉很不准确...

---

### 评论 #4 (作者: WL27618, 时间: 10个月前)

今天把全部提交的alpha都检查一遍. 发现, 生成的description还是不聪明. 好像没法理解表达式, 只是机械的找一些关健词. 比如
a = datafield1; ts_zscore(b,252)

我的llm就没能识别到第一句是误导, 表达式实际和a无关. name也会去选择a. 
还有category似乎也只是根据我提供的description的关键词区分. 我用的是gemini api.

====================================================================================

---

