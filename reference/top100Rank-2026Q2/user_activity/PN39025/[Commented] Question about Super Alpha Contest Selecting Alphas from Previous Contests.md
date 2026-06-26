# Question about Super Alpha Contest: Selecting Alphas from Previous Contests

- **链接**: [Commented] Question about Super Alpha Contest Selecting Alphas from Previous Contests.md
- **作者**: DV64461
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

Hi everyone,

I'm participating in the Super Alpha contest and had a couple of questions:

1. **Alpha Source Requirement** : Do  *all*  the alphas used to construct the Super Alpha need to be created through previous contests, or is it sufficient if  *some*  are from past contests?
2. **Selecting Alphas from Past Contests** : I'm not sure how to efficiently select alphas that were created during previous contests. I noticed that if I manually tag them during the contests, I can later filter using the tag tool in the Selection Expression—but this feels quite inconvenient. Is there a better or official method to do this?

Would really appreciate any tips or guidance from those with experience. If you're wondering the same, feel free to like this post to help boost visibility!

Thanks and good luck to everyone!

---

## 讨论与评论 (11)

### 评论 #1 (作者: NS94943, 时间: 1年前)

Hi,

I think the categories ATOM and SIMPLE and RISK NEUTRALIZED need not be from past competitions. And to answer your second question, just use

```
own * in(classifications,"<Category>")
```

or

```
  own * (neutralization=="<neutralization>")
```

or

```
own * in(competitions,"<competition>")
```

as the case may be, in your selection expression If you are trying to get your own alphas, omit the "own" otherwise. And then you can apply more conditions to the selection expression to narrow your list of alphas.

Cheers!

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

Hello, the super alpha competition is similar to the old SAC competition, but with one more thing, the alphas participating in the competition are selected from past competitions. Don't worry too much if your alpha number is small because with genius, you can choose alphas from the same school, the same country, or other people's world. Focus on alpha performance.

---

### 评论 #3 (作者: RS70387, 时间: 1年前)

Hi  [DV64461](/hc/en-us/profiles/14750991135255-DV64461) ,
For ACE and HCAC, the alphas selected in SuperAlphas will typically come from those specific competitions. However, for ATOM, SIMPLE, RISK NEUTRALIZED, and POWER POOL categories, the alphas can be from any submission period, they don’t have to be from a past contest. Also, for the Super Alpha Competition 2025, all consultants have access to the weekly group category alphas submitted by all participants, so you’re not limited to just your own alphas when constructing SuperAlphas.

---

### 评论 #4 (作者: TP18957, 时间: 1年前)

Great questions about the Super Alpha Contest! Regarding the alpha source, it’s important to note that while some categories like ATOM, SIMPLE, and RISK NEUTRALIZED don’t require alphas from past contests specifically, for others you do need to leverage previously created alphas. To efficiently select alphas from past contests, the selection expression language is your friend. You can filter using  `in(competitions, "<competition_name>")`  to include only alphas created during particular contests. For example,  `own * in(competitions, "SuperAlphaContest2023")`  will select your alphas from that contest. Similarly, you can filter by neutralization or classification using  `neutralization == "<type>"`  or  `in(classifications, "<category>")` . Tagging can work but is cumbersome at scale; using these built-in filters is much more effective and flexible. Combining multiple filters can help you quickly find and optimize your alpha selection for the contest.

---

### 评论 #5 (作者: SP39437, 时间: 1年前)

Turnover measures how frequently the positions in an alpha strategy are changed over a specific period, typically daily or annually. While high turnover can sometimes enhance returns, it also introduces several risks and challenges.

Negative effects of high turnover include increased transaction costs — such as commissions, slippage, and bid-ask spreads — which reduce net profitability. Frequent trading can also create market impact, where large trades influence prices, especially in illiquid stocks. High-turnover strategies tend to have lower scalability, making them harder to execute at large volumes. Furthermore, they may suffer from overfitting, where the alpha captures noise rather than true market signals, leading to poor performance in out-of-sample tests.

That said, high turnover can offer advantages if carefully managed, such as reacting swiftly to short-term opportunities and capturing rapid market inefficiencies.

My main challenge is finding a balance — building alpha strategies that maintain strong performance while keeping turnover at a manageable level.

---

### 评论 #6 (作者: TP85668, 时间: 1年前)

No,  **not all alphas in a Super Alpha need to be from previous contests** , but  **at least some must be**  if the contest requires it (check the contest rules).

✅  **For selecting contest alphas efficiently** :

- The best method is to  **use tags during the contest**  (e.g.,  `contest_march2025` ).
- Then, in the Super Alpha Selection Expression, filter by tag:
  ini
  Sao chépChỉnh sửa
  `tag = "contest_march2025"
  `
- Currently,  **manual tagging is the recommended approach** . There's no automatic filter for “created during contest” unless tagged.

---

### 评论 #7 (作者: SK90981, 时间: 1年前)

Tagging is helpful but can be tedious—an official filtering tool for past contest alphas would really streamline the process.

---

### 评论 #8 (作者: AG14039, 时间: 1年前)

Great questions! For Super Alpha construction, not  *all*  alphas need to be from past contests—but to be eligible for contest scoring, at least some must come from previous SAC submissions. As for selecting them efficiently, you're right that tagging during the contest helps, but another useful method is to use filters like  `CreatedAt`  in your selection expression (e.g.,  `CreatedAt >= 2024-01-01` ) to target a specific time range. It’s not perfect, but it does make things more manageable. Hopefully, future updates will streamline this process even more. Good luck building your Super Alpha!

---

### 评论 #9 (作者: RP41479, 时间: 1年前)

Hello! The Super Alpha Competition is like the old SAC but adds a twist—alphas are chosen from past competitions. Even with fewer alphas, Genius lets you pick from your school, country, or others globally. Just focus on alpha performance!

---

### 评论 #10 (作者: VS18359, 时间: 1年前)

Hi all,
What is the selection expression to select alphas with the classification 'SIMPLE'? Please suggest some ideas?

---

### 评论 #11 (作者: NS94943, 时间: 1年前)

Hi  [VS18359](/hc/en-us/profiles/4730368641431-VS18359) ,

You can start with

```
in(classifications, "SIMPLE") && (<other selection conditions here>)
```

For example, to select SIMPLE classified alphas from the price-volume category, you could use:

```
in(classifications,"SIMPLE") && (in(datacategories,"PV"))
```

Cheers!

---

