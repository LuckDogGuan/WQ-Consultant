# OSMOSIS 分数分配策略 by TIGER：big head 分配法代码优化

- **链接**: [Commented] OSMOSIS 分数分配策略 by TIGERbig head 分配法代码优化.md
- **作者**: ZZ13271
- **发布时间/热度**: 4个月前, 得票: 66

## 帖子正文

```
策略说明：适用于量少且质量不佳的小地区，把权重尽可能分配给表现相对较好的因子使用说明：只需要填上用户密码和region即可import requestsfrom time import sleepimport jsonimport randomREGION = 'CHN'  # Can be changed to other regions like 'APAC', 'EMEA', etc.def login():    username = ""    password = ""    # Create a session to persistently store the headers    s = requests.Session()    # Save credentials into session    s.auth = (username, password)    # Send a POST request to the /authentication API    response = s.post('https://api.worldquantbrain.com/authentication')    print(f"Login response: {response.content}")    print('consultant lib')    return sdef get_alphas(session, region, limit=100):    """Get alphas for the specified region"""    url = f'https://api.worldquantbrain.com/users/self/alphas?limit={limit}&offset=0&status!=UNSUBMITTED%1FIS-FAIL&type=REGULAR&settings.region={region}&order=-os.sharpe&hidden=false'    response = session.get(url)        if response.status_code != 200:        print(f"Error getting alphas: {response.status_code}")        return []        try:        data = response.json()        # The API returns 'results' key, not 'items'        alphas = data.get('results', [])        print(f"Retrieved {len(alphas)} alphas for region {region}")        return alphas    except json.JSONDecodeError as e:        print(f"Error parsing JSON response: {e}")        return []def set_alpha_osmosis_score(session, alpha_id, score):    """Set osmosis score for a specific alpha"""    alpha_url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'        # Generate a random name for the alpha    random_suffix = str(random.randint(1000, 9999))    data = {        "color": None,        "name": f"{REGION.lower()}_scored_{random_suffix}",        "tags": ["ace_tag"],        "category": None,        "regular": {"description": None},        "osmosisPoints": score    }        response = session.patch(alpha_url, json=data)    return responsedef generate_scores(num_alphas):    """Generate scores according to the specified rules - Total must be 100,000"""    scores = []        if num_alphas == 0:        return scores        # Special case: only 1 alpha    if num_alphas == 1:        return [100000]        # Special case: only 2 alphas    if num_alphas == 2:        return [50000, 50000]  # Both get equal share        # General case: 3 or more alphas    # First two alphas get high scores (but we'll adjust later to make total exact)    scores.append(50000)  # First alpha    scores.append(40000)  # Second alpha        remaining_total = 10000  # Remaining points to distribute    remaining_count = num_alphas - 2        # For small numbers of alphas, reduce the first two scores to allow more reasonable distribution    if num_alphas <= 6:        # Redistribute some points from first two to remaining alphas        redistribution = min(20000, 5000 * (6 - num_alphas))  # More redistribution for fewer alphas        scores[0] -= redistribution // 2        scores[1] -= redistribution // 2        remaining_total += redistribution        if num_alphas >= 7:  # Have enough alphas for full pattern        # Last 5 alphas get single digit scores (descending)        last_five = [9, 7, 5, 3, 1]  # Fixed descending pattern        remaining_total -= sum(last_five)  # Deduct last 5 scores        remaining_count -= 5  # Remove last 5 from remaining count                if remaining_count > 0:  # Have middle section            # Middle section: descending from high to low            middle_total = remaining_total                        # Create descending scores for middle section            middle_scores = []            if remaining_count == 1:                middle_scores.append(middle_total)            else:                # Distribute middle_total across remaining_count scores, descending                # First middle score gets largest share                first_middle = int(middle_total * 0.5)  # First gets ~50%                remaining_middle = middle_total - first_middle                                middle_scores.append(first_middle)                                # Distribute the rest descending                for i in range(1, remaining_count):                    if remaining_middle <= 0:                        middle_scores.append(10)  # Minimum                    else:                        ratio = i / (remaining_count - 1) if remaining_count > 1 else 0                        score = int(remaining_middle * (1 - ratio) / (remaining_count - 1))                        middle_scores.append(max(score, 10))                        scores.extend(middle_scores)                scores.extend(last_five)            else:  # 3-6 alphas: only first 2 + some single digits        # Remaining alphas get single digit scores (descending)        for i in range(remaining_count):            score = max(9 - i * 2, 1)            scores.append(score)        # Final adjustment to ensure total is exactly 100,000    current_total = sum(scores)    difference = 100000 - current_total        if difference != 0:        # Adjust the most flexible score (usually a middle score)        if num_alphas >= 7 and len(scores) > 7:  # Have middle section            # Adjust the last middle score            adjust_index = -6            scores[adjust_index] += difference            scores[adjust_index] = max(scores[adjust_index], 10)  # Ensure minimum        elif num_alphas >= 3:  # Adjust third score            scores[2] += difference            scores[2] = max(scores[2], 1)  # Ensure minimum        return scoresdef main():    """Main function to score alphas"""    print(f"Starting alpha scoring for region: {REGION}")        # Login and create session    session = login()        # Get alphas for the specified region    alphas = get_alphas(session, REGION)        if not alphas:        print("No alphas found or error retrieving alphas")        return        print(f"Found {len(alphas)} alphas")        # Generate scores according to rules    scores = generate_scores(len(alphas))        print("Generated scores:")    for i, score in enumerate(scores):        print(f"  Alpha {i+1}: {score}")        # Set osmosis scores for each alpha    for i, (alpha, score) in enumerate(zip(alphas, scores)):        alpha_id = alpha.get('id')        if not alpha_id:            print(f"Warning: Alpha {i} has no ID, skipping")            continue                print(f"Setting score {score} for alpha {alpha_id} (alpha {i+1})")                response = set_alpha_osmosis_score(session, alpha_id, score)                if response.status_code == 200:            print(f"  Successfully set score for alpha {alpha_id}")        else:            print(f"  Failed to set score for alpha {alpha_id}: {response.status_code}")            print(f"  Response: {response.text}")                # Add small delay to avoid rate limiting        sleep(0.5)        print("Alpha scoring completed!")if __name__ == "__main__":    main()
```

---

## 讨论与评论 (9)

### 评论 #1 (作者: HG61318, 时间: 3个月前)

方法不错,学习了

##################################################################
摸摸后缀
##################################################################

---

### 评论 #2 (作者: HL10684, 时间: 3个月前)

```
策略说明：适用于量少且质量不佳的小地区，把权重尽可能分配给表现相对较好的因子
```

楼主是如何判断表现相对较好的因子，代码好像没有对因子好差进行判断诶🤔

==================================================================================

所遇皆为我师，望不吝赐教

==================================================================================

---

### 评论 #3 (作者: LK39823, 时间: 3个月前)

大佬试过后用着怎么样，os表现稳定吗？

================================================================================

我之前一直手工分配，感觉不是很稳一会儿0.8，一会儿0.2

===================================================================================

---

### 评论 #4 (作者: MZ45384, 时间: 3个月前)

又有新的osmisis分配方法了。但是Big head这种只够前面几个分配大头的会不会不太鲁棒。已经一个月了可以展示一下对应的os rank吗，这对我很重要。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #5 (作者: JC87908, 时间: 3个月前)

非常实用的工具，感谢无私分享！

---

### 评论 #6 (作者: SJ65808, 时间: 3个月前)

OS更新一个月了，虎哥表现如何？？

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #7 (作者: MY49971, 时间: 3个月前)

效果如何呢，大佬

==================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #8 (作者: ZZ81910, 时间: 3个月前)

-------------------------------------------------------------------------------------------------------------

我还没做过小地区，不过作为新手我总体数量本就不多，不知道适不适用这个

-----------------------------------------------------------------------------------------------------------

---

### 评论 #9 (作者: PX70901, 时间: 1个月前)

效果如何？

---

