# Updated Brain API Settings for Alpha Research

- **链接**: [Commented] Updated Brain API Settings for Alpha Research.md
- **作者**: SC43474
- **发布时间/热度**: 1年前, 得票: 23

## 帖子正文

Hello Brain Community,

To help you optimize your alpha research across different markets, here is the latest compilation of Brain API settings, incorporating recent additions to Universes and Neutralization options. Having these parameters clearly laid out will ensure your API calls are configured correctly for each region, improving both efficiency and research accuracy.

### USA

- **Universe:**  TOP3000, TOP1000, TOP500, TOP200, ILLIQUID_MINVOL1M, TOPSP500
- **Delay:**  0, 1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, STATISTICAL, CROWDING

### Europe (EUR)

- **Universe:**  TOP2500, TOP1200, TOP800, TOP400, ILLIQUID_MINVOL1M
- **Delay:**  0, 1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, COUNTRY, STATISTICAL, CROWDING

### Global (GLB)

- **Universe:**  TOP3000, MINVOL1M
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, COUNTRY, STATISTICAL, CROWDING

### Asia (ASI)

- **Universe:**  MINVOL1M, ILLIQUID_MINVOL1M
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, COUNTRY, CROWDING, STATISTICAL

### China (CHN)

- **Universe:**  TOP2000U
- **Delay:**  0, 1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, CROWDING

### Korea (KOR)

- **Universe:**  TOP600
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

### Taiwan (TWN)

- **Universe:**  TOP500, TOP100
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

### Hong Kong (HKG)

- **Universe:**  TOP800, TOP500
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

### Japan (JPN)

- **Universe:**  TOP1600, TOP1200
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

### Americas (AMR)

- **Universe:**  TOP600
- **Delay:**  1
- **Neutralization:**  MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY

This updated overview consolidates key Brain API parameters to help you configure your strategies effectively across regions. Keep this guide handy to ensure your research workflows remain precise and efficient.

---

## 讨论与评论 (20)

### 评论 #1 (作者: US66925, 时间: 1年前)

Hi  [SC43474,](/hc/en-us/profiles/5163496266135-SC43474)

This is an incredibly valuable resource for anyone working with Brain API to streamline and enhance their alpha research across various regions. Having a well-organized and up-to-date overview of the available  **Universes** ,  **Delays** , and  **Neutralization options**  by region is crucial for building robust, region-specific signals and avoiding common pitfalls like misalignment in factor exposures or inappropriate benchmarking. I especially appreciate the detailed breakdown for each region—from the Global and US  to more nuanced regional setups like Taiwan, Korea, and China. The inclusion of neutralization techniques such as  **SLOW** ,  **FAST** , and  **CROWDING**  adds another layer of granularity, enabling more tailored factor isolation. For consultants working across multiple regions, this post serves as a quick-reference operational playbook to maintain consistency and accuracy in API setup. Thanks for compiling and sharing this—it’s a real time-saver and will definitely help avoid errors in API setup.

---

### 评论 #2 (作者: IK32530, 时间: 1年前)

Thank you for organizing everything clearly. Has the recently updated RAM Neutralization not been applied yet? I’m asking because, in the documentation, I think it was saved in a dictionary format under the name Reversion and Momentum.

---

### 评论 #3 (作者: VP21767, 时间: 1年前)

This is a good topic for all consultants. Moreover, there is a new neutralize call REVERSION_AND_MOMENTUM which is added to 4 big regions. Goodluck to you and all consultants

---

### 评论 #4 (作者: TP18957, 时间: 1年前)

This is an excellent consolidation of the Brain API settings across regions — having this level of granularity outlined helps reduce ambiguity when aligning universe definitions with neutralization schemes. It’s particularly helpful to see the inclusion of  `ILLiquid_MINVOL1M`  across multiple regions, especially for strategies relying on liquidity-aware factor design. One follow-up: will there be consistency checks or guidelines when using overlapping universes like  `TOP500`  across markets such as HKG, TWN, and the USA? Moreover, with the addition of complex neutralization methods like  `SLOW_AND_FAST`  and  `STATISTICAL` , it might be useful to include practical examples in the API documentation that show the implications of each setting on factor scores. Thanks again for compiling this in one place.

---

### 评论 #5 (作者: TP18957, 时间: 1年前)

Thank you for taking the time to compile and share this thorough and clearly formatted update. Having region-specific Brain API configurations laid out side by side is incredibly helpful — especially for those of us working across multiple markets simultaneously. It saves us time and ensures we’re not making assumptions that could lead to discrepancies in model outputs. I also appreciate the inclusion of both established and newer neutralization options like  `CROWDING`  and  `SLOW_AND_FAST` , which are often underutilized but offer powerful adjustments to factor construction. Great job putting this together for the community — it’s a valuable reference I’ll definitely keep close at hand.

---

### 评论 #6 (作者: CT69120, 时间: 1年前)

Recently, new documentation about neutralizing RAM has been added. You can refer to it and consider including it in this article—thank you very much!
 [https://platform.worldquantbrain.com/learn/documentation/advanced-topics/getting-started-ram-risk-neutralized-alphas#how-to-simulate-ram-risk-neutralized-alphas](https://platform.worldquantbrain.com/learn/documentation/advanced-topics/getting-started-ram-risk-neutralized-alphas#how-to-simulate-ram-risk-neutralized-alphas)

---

### 评论 #7 (作者: AK98027, 时间: 1年前)

Appreciate the systematic organization of this update! The regional API parameter documentation significantly enhances strategy configuration efficiency and research methodology precision. Valuable reference material for the community.

---

### 评论 #8 (作者: NT32626, 时间: 1年前)

Thank you for the helpful information you provided. Additionally, I’d like to add that you can open the Network tab in the browser's Console to observe the APIs being called during your interactions with the website. This can help you identify the necessary APIs and payloads.

---

### 评论 #9 (作者: DJ40095, 时间: 1年前)

Thanks for the detailed update! Could you explain how the newer neutralization options like STATISTICAL and CROWDING differ in their methodology or impact from traditional options like SECTOR or INDUSTRY? Are there specific cases where using these would be more advantageous in improving Alpha robustness or SuperAlpha performance?

---

### 评论 #10 (作者: AK40989, 时间: 1年前)

Just to add, what’s missing here is the new neutralization string for the API which is  **REVERSION_AND_MOMENTUM**

---

### 评论 #11 (作者: PY62071, 时间: 1年前)

This organized API settings breakdown by region is incredibly beneficial! It's a fantastic resource for the community, significantly aiding in optimizing strategy configurations and boosting research precision.

---

### 评论 #12 (作者: SK55888, 时间: 1年前)

Thank you for organizing everything clearly. Has the recently updated RAM Neutralization not been applied yet? I’m asking because, in the documentation.

---

### 评论 #13 (作者: DK20528, 时间: 1年前)

Appreciate the clear and structured update! Laying out the API settings by region like this makes it much easier to fine-tune strategies and sharpen research accuracy. A really valuable reference point for everyone in the community!

---

### 评论 #14 (作者: AK52014, 时间: 1年前)

Thanks for compiling this clear, detailed update! Side-by-side Brain API configurations by region are incredibly useful for multi-market work. Including lesser-used neutralizers like CROWDING and SLOW_AND_FAST adds real value—this will be a go-to reference.

---

### 评论 #15 (作者: SZ83096, 时间: 1年前)

Excellent consolidation of region-specific parameters! 🚀 This will save countless hours in cross-market alpha testing. Three key observations for optimization:**

1. **Neutralization Asymmetry**  

   - US notably lacks `COUNTRY` neutralization (vs. EUR/GLB/ASI), suggesting domestic factors dominate.  

   - China/Korea/TW/HK/Japan omit `STATISTICAL` neutralization – is this due to data constraints or strategy design?

2. **Liquidity Thresholds**  

   `ILLIQUID_MINVOL1M` appears in US/EUR/ASI but not emerging markets. Critical for small-cap strategies!

3. **Actionable Tips**  

   ```python  

   # Pro optimization: Chain neutralizations for crowded regions (e.g. EUROPE)  

   neutralize(["SECTOR", "STATISTICAL", "CROWDING"], inplace=True)  

   ```

---

### 评论 #16 (作者: JK98819, 时间: 1年前)

- **Genius Program** :
  - **Rule** : Repeated operators are  **not**  counted.
  - **Example** : If the expression uses the same operator (e.g.,  `+` ) multiple times, it is only counted  **once** .
  - **Resulting Operator Count** :  **2**
- **Power Pool Alpha** :
  - **Rule** : Repeated operators  **are**  counted.
  - **Example** : If an expression uses  `+` ,  `+` , and  `-` , all three are counted individually.
  - **Resulting Operator Count** :  **3**

---

### 评论 #17 (作者: SP39437, 时间: 1年前)

This is an excellent summary of Brain API settings across different regions — having this level of clarity helps eliminate ambiguity when aligning universe definitions with neutralization strategies. The inclusion of universes like  `ILLIQUID_MINVOL1M`  across multiple markets is particularly helpful for those building  **liquidity-sensitive factor models** . One question I had: will there be any  **guidelines or consistency checks**  for overlapping universes such as  `TOP500`  in regions like HKG, TWN, and the USA?

Also, the addition of advanced neutralization types like  `SLOW_AND_FAST`  and  `STATISTICAL`  is great to see. It would be valuable if the documentation included  **practical examples**  showing how these impact factor scores in real use cases.

Overall, having all these configurations clearly laid out side by side is incredibly useful — especially for those of us developing cross-regional strategies. Thanks again for compiling this. It’s a fantastic reference I’ll be keeping close as part of my research workflow.

---

### 评论 #18 (作者: TP19085, 时间: 1年前)

Thank you for putting together such a clear and comprehensive update. Having side-by-side Brain API configurations for each region is incredibly useful, especially for those of us developing strategies across multiple markets. This format minimizes the risk of oversight and helps ensure our models are aligned correctly with region-specific parameters. I also appreciate your inclusion of newer neutralization options like  `CROWDING`  and  `SLOW_AND_FAST`  — they’re often overlooked but offer powerful levers for refining factor construction. This reference is definitely one I’ll keep handy.

Your inclusion of universes like  `ILLIQUID_MINVOL1M`  across different regions is particularly helpful for those designing liquidity-aware models. One follow-up: are there plans to standardize universe usage when overlapping sets like  `TOP500`  are used in HKG, TWN, and USA? Also, it would be great if the API documentation included concrete examples showing how advanced neutralizations like  `SLOW_AND_FAST`  or  `STATISTICAL`  impact output. Thanks again for sharing this valuable resource.

---

### 评论 #19 (作者: NS62681, 时间: 1年前)

Really appreciate the clarity and structure in this update! Breaking down API settings by region makes strategy tweaking much easier and sharpens research focus. Super helpful for everyone involved.

---

### 评论 #20 (作者: SM36732, 时间: 1年前)

thanks for the update

---

