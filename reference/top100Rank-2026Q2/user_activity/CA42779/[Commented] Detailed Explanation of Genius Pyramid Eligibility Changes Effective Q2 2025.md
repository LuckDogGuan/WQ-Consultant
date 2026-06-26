# Detailed Explanation of Genius Pyramid Eligibility Changes Effective Q2 2025

- **链接**: [Commented] Detailed Explanation of Genius Pyramid Eligibility Changes Effective Q2 2025.md
- **作者**: DD24306
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

### 1. Key Changes in Pyramid Limits per Alpha

Before Q2 2025:

- A single Alpha could belong to an unlimited number of Pyramids.
- *Example* : The Alpha "Momentum_RSI" using Price, Volume, and Earnings data could simultaneously belong to Price Volume, Earnings, and Model Pyramids.

Starting Q2 2025:

- Each Alpha can only contribute to a maximum of 2 Pyramids.
- If an Alpha belongs to >2 Pyramids → It will not count toward any Pyramid in Genius rankings.
- *Note* :
  - The Alpha still qualifies for Base Payment and other metrics (e.g., signal count, Combined Alpha performance).
  - Neutralization fields (currency, sector, etc.) do not count as extra Pyramids.

Illustrative Examples:

- Alpha "MA_Crossover" belongs to 3 Pyramids (Price Volume, Model, Fundamental) → 0 Pyramids in Genius.
- Alpha "EPS_Growth" belongs to 2 Pyramids (Earnings, Fundamental) → Still counts as 2 Pyramids.

### 2. Reasons for the Change

- Alignment with Power Pool/Atom Alphas: These Alpha types are simpler (fewer data fields), so Genius is adapting for fairness.
- Focus on Quality: The system now prioritizes Alphas that meet core eligibility criteria (e.g., high Sharpe Ratio) over quantity.
- Avoid Redundancy: Prevents Alphas from exploiting multiple Pyramids to inflate scores.

Neutralization Example:

- Alpha "Sector_Neutral_Momentum" uses 2 Pyramids (Price Volume, Model) + sector neutralization → Still only counts as 2 Pyramids.

### 3. Implementation Details

- Effective Date: April 1, 2025 (Q2 2025).
- Leaderboard Update: By April 25, 2025.
- Unaffected Metrics:
  - Base Pyramid Multipliers: Existing multipliers remain unchanged.
  - Accrued Payments: Cumulative payments are not impacted.
- New Community Score: Upcoming metric for forum activity, referrals, and BRAIN event participation.

### 4. Practical Examples from Your Data

Assume you have 3 Alphas:

1. Alpha X:
   - Belongs to 3 Pyramids (Earnings, Fundamental, Price Volume).
   - Result: 0 Pyramids (exceeds limit).
2. Alpha Y:
   - Belongs to 2 Pyramids (News, Sentiment) + currency neutralization.
   - Result: 2 Pyramids (neutralization ignored).
3. Alpha Z:
   - Belongs to 1 Pyramid (Macro).
   - Result: 1 Pyramid.

→ Total Pyramids after adjustment: 2 (Alpha Y) + 1 (Alpha Z) = 3 Pyramids (sharp drop from 81).

### 5. Optimization Strategies

- Step 1: Audit your Pyramid Distribution for Alphas with >2 Pyramids.
  - For overqualified Alphas, remove less critical Pyramids.
- Step 2: Prioritize retaining the strongest Pyramids (e.g., those with the best backtest results).
- Step 3: Split complex Alphas into multiple standalone Alphas if needed.

Example:

- Alpha "MultiFactor" (4 Pyramids) → Split into:
  - "MultiFactor_A" (2 Pyramids).
  - "MultiFactor_B" (2 Pyramids).

### Key Takeaways

- Goal: Reduce Pyramid spam and emphasize high-quality Alphas.
- Action Items:
  - Review Alphas exceeding the 2-Pyramid limit.
  - Leverage neutralization fields to preserve Pyramid slots.
  - Monitor Community Score for additional ranking benefits.

---

## 讨论与评论 (7)

### 评论 #1 (作者: TN48242, 时间: 1年前)

This article provides a very clear and logical explanation of the changes to the Genius Pyramid rules starting from Q2 2025. Limiting each Alpha to contributing to a maximum of 2 Pyramids helps better reflect the true contribution of each Alpha and prevents situations where a single Alpha artificially inflates leaderboard scores by participating in too many Pyramids. I really appreciate the optimization strategies suggested, such as splitting complex Alphas or carefully selecting the strongest Pyramids. However, I have one question: If an Alpha belongs to more than 2 Pyramids and therefore is excluded from all Pyramid counting for the leaderboard, will it still qualify for the multipliers applied to its base payment? I would love to hear a clarification on this point, as it directly affects the reward structure for contributors.

---

### 评论 #2 (作者: KK81152, 时间: 1年前)

the new restriction on pyramid limits per alpha starting in  **Q2 2025**  requires a shift in how alphas are allocated across pyramids. The key to success will be carefully managing alpha placement to avoid exceeding the two-pyramid limit, while still maintaining diversity and performance in your pyramids. Start reviewing your alpha usage now to ensure you comply with the new rules and optimize your rankings for the upcoming quarter.

---

### 评论 #3 (作者: CA42779, 时间: 1年前)

Big shift ahead with the 2-Pyramid cap—this change rightly puts more emphasis on alpha clarity, originality, and performance over structural overlap. I'm revisiting my current Pyramid mappings to streamline exposure and split overly broad alphas where needed. Prioritizing pyramids with the strongest historical Sharpe and persistence, while using neutralization fields smartly to conserve slots. This will not only optimize Genius scores but push us all toward cleaner, more targeted alpha design. Looking forward to how others are adapting their strategies under the new rules.

---

### 评论 #4 (作者: MG13458, 时间: 1年前)

The new  **2-Pyramid limit**  is definitely going to change the way we think about Alpha distribution. It’s a good move to prioritize quality over quantity, but it’s going to make strategic planning even more important

---

### 评论 #5 (作者: ML46209, 时间: 1年前)

Thanks for the clear breakdown and actionable tips! The 2-Pyramid limit really pushes us to focus on quality and smart allocation. Looking forward to optimizing my alphas accordingly.

---

### 评论 #6 (作者: SK90981, 时间: 1年前)

New pyramid rules from Q2 2025: Max 2 pyramids per Alpha. Exceeding this means 0 pyramid credit in Genius. Focus now shifts to quality over quantity.

---

### 评论 #7 (作者: TP18957, 时间: 1年前)

This policy update introduces a critical optimization constraint for anyone working with multi-Pyramid alphas. While limiting each alpha to a maximum of two Pyramids simplifies the scoring logic and discourages redundancy, it also forces us to rethink how we design and categorize multi-factor strategies. A useful approach would be to audit your current alpha-Pyramid associations using the  `get_alpha_info()`  or  `get_alpha_pyramids()`  API endpoints. For any alphas that exceed the 2-Pyramid limit, consider breaking them into modular variants, each tailored for specific Pyramid themes while preserving core logic. Also, leverage neutralization (sector, region, etc.) instead of structural overlaps to maintain diversity without inflating Pyramid count. This change rewards intentional, high-quality construction over broad-spectrum alpha tagging.

---

