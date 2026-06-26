# Getting started with Research

- **链接**: [Commented] Getting started with Research.md
- **作者**: EN37804
- **发布时间/热度**: 4个月前, 得票: 3

## 帖子正文

Getting started with quantitative research at WorldQuant is a journey of turning raw data into predictive signals known as  **Alphas** . Whether you are a student, an engineer, a data enthusiast or someone interested in quantitative finance the WorldQuant BRAIN platform is designed for you it lets you simulate and test these ideas using institutional-grade data.

Here is a guide to help you navigate your first steps in the WorldQuant community.

## 1. The Core Concept: What is an Alpha?

In the WorldQuant ecosystem, an  **Alpha**  is a mathematical expression used to predict the relative performance of a set of financial instruments.

## 2. Your First 3 Steps on BRAIN

### Step 1: Onboarding & Training

Before writing code, head to the  **Learn**  section on the  [WorldQuant BRAIN platform](https://platform.worldquantbrain.com/) .

- **Learn2Quant Series:**  Watch the beginner videos hosted by WorldQuant experts.
- **Operator Documentation:**  Familiarize yourself with functions like  `rank()` ,  `ts_sum()` , and  `correlation()` .
- **Data Explorer:**  Browse the thousands of data fields available, from standard price-volume to news sentiment datasets.

### Step 2: Building in the Simulation Environment

Use the  **Simulate**  tab to write and test your first Alpha.

- **Universe:**  Start with  `TOP3000`  (the most liquid stocks).
- **Neutralization:**  you can apply  `Subindustry`  or  `Sector`  neutralization to ensure your Alpha is betting on specific stock movements rather than broad market trends.
- **Decay:**  Use a decay (e.g.,  `decay=3` ) to smooth out your trades and reduce turnover costs.

### Step 3: Passing the "Alpha Tests"

For an Alpha to be submittable, it must pass several automated checks:

- **Sharpe Ratio:**  Needs to show consistent risk-adjusted returns (usually > 1.25).
- **Turnover:**  Should be within a range that makes the strategy tradable (usually >= 1 x <= 70%).
- **Fitness:**  A proprietary metric combining Sharpe and returns.

---

## 讨论与评论 (1)

### 评论 #1 (作者: RM79380, 时间: 4个月前)

This is a clear and beginner-friendly guide to getting started on WorldQuant BRAIN. I like how it walks newcomers from understanding Alphas to onboarding, simulation, and passing key Alpha tests. Emphasizing neutralization, decay, and starting with a liquid universe makes it especially practical for first-time researchers.

---

