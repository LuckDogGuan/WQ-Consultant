# Question: How many years does a data field require for IS and OS separately?

- **链接**: [Commented] Question How many years does a data field require for IS and OS separately.md
- **作者**: WC30696
- **发布时间/热度**: 3个月前, 得票: 10

## 帖子正文

Following the spec  [https://support.worldquantbrain.com/hc/en-us/articles/38469828154135-How-will-my-submissions-be-scored-in-DCC](https://support.worldquantbrain.com/hc/en-us/articles/38469828154135-How-will-my-submissions-be-scored-in-DCC) , it has IS and OS.

In API samples, it downloads data within the periods 2021-01-01 to 2022-12-31, 2021-01-01 to 2021-06-30, 2021-01-01 to 2021-12-31.

Question: How many years does a data field require for IS and OS separately?

If it just requires 2 years for IS, how will the platform calculate the OS score of each alpha?

---

## 讨论与评论 (7)

### 评论 #1 (作者: LD27384, 时间: 3个月前)

From what I know so far, the API only provides data for 2021–2022 (two full years). The IS requires a minimum of two years of data, and for the OS, remember to use the  `create_dataframe`  function in your code—it will help WorldQuant study and explore your dataframe later.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #2 (作者: WC30696, 时间: 3个月前)

If we need to use the `create_dataframe` function, I assume all data fields will be re-ran to generate more data for the OS score calculation, so, if we submit multiple data fields, all these data fields must be reproducible, right? If so, will we have a submission template including notebook, code, ppt templates later?

---

### 评论 #3 (作者: JN96079, 时间: 3个月前)

Yeah, sure thing as to what  [LD2738](/hc/en-us/profiles/34336234869655-LD27384)  claims. A 2-year period is needed, specifically 2021-2022, and the most important part is the "create_dataframe" function in the code!

^^JN

---

### 评论 #4 (作者: DB89987, 时间: 3个月前)

The two year restriction is by design. Although I have no information about the OS period. Good Question.

---

### 评论 #5 (作者: WL13229, 时间: 3个月前)

you need to build a 2-year DataFrame

---

### 评论 #6 (作者: WL13229, 时间: 3个月前)

[WC30696](/hc/en-us/profiles/28973900425367-WC30696)

only one notebook would be count

---

### 评论 #7 (作者: AR98193, 时间: 3个月前)

I do not think we are allowed by the RavenPack api to access more than 2 years of data

---

