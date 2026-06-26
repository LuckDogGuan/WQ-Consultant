# 分享一个超好用的genius排行分析工具代码优化

- **链接**: [Commented] 分享一个超好用的genius排行分析工具代码优化.md
- **作者**: XX42289
- **发布时间/热度**: 1年前, 得票: 37

## 帖子正文

我们都知道genius项目有多个等级，分为gold，expert，master和grand master
但是事实上达成了条件，也并不意味着你能当上那个等级的，因为grand master只有2%的名额，master只有8%，
所以你需要在leaderboard上各项排名排名靠前。
所以今天分享的工具可以很好地帮助你了解你目前每个模块处于哪个位置，才能知道应该往哪个方向努力。

代码如下，别忘记替换你的用户名和密码，也别忘了安装matplotlib库：

```
import timeimport requestsimport pandas as pdimport matplotlib.pyplot as pltusername = "username"password = "password"s = requests.Session()s.auth = (username, password)response = s.post('https://api.worldquantbrain.com/authentication')print(response.content)# API的基本信息base_url = "https://api.worldquantbrain.com/consultant/boards/genius"# 1. 遍历分页 API，收集所有用户数据def fetch_all_data(s):    offset = 0    limit = 30    all_data = []    while True:        response = s.get(f"{base_url}?limit={limit}&offset={offset}&order%3D-fieldAvg&aggregate=user",)        data = response.json()        if "results" in data:            all_data.extend(data["results"])            offset += limit            print(f"Fetched {offset} records")            if offset >= data["count"]:                break        else:            print("Error fetching data")            break        time.sleep(1)    # 保存为CSV文件    df = pd.DataFrame(all_data)    df.to_csv("all_users_data.csv", index=False)    print("Data saved to all_users_data.csv")    return df# 2. 获取自己的用户数据中的leaderboard部分def fetch_self_data(s):    response = s.get("https://api.worldquantbrain.com/users/self/consultant/summary")    self_data = response.json().get("leaderboard", {})    return self_data# 3. 绘制直方图并高亮自己所在位置def plot_histogram(df, self_data, col):    # 获取 fieldAvg 数据    field_avg_data = df[col].dropna()    # 绘制直方图    plt.figure(figsize=(10, 6))    n, bins, patches = plt.hist(field_avg_data, bins=20, color="blue", edgecolor="black", alpha=0.7)    # 确定自己在哪个柱子中    self_field_avg = self_data.get("fieldAvg")    for i in range(len(bins) - 1):        if bins[i] <= self_field_avg < bins[i + 1]:            patches[i].set_facecolor("red")            break    # 图表设置    plt.xlabel(f"{col}")    plt.ylabel("Frequency")    plt.title(f"Distribution of {col} with Self Highlighted")    plt.show()# 执行步骤df = fetch_all_data(s)self_data = fetch_self_data(s)plot_histogram(df, self_data, "alphaCount")plot_histogram(df, self_data, "fieldAvg")
```

该代码会直接绘制两张图，第一张图是你的alpha数量的排名，红色意味着你的位置，如果越靠后说明越好。
我是一个新手顾问，刚加入顾问团队，所以我的位置是在最差的一档。

![图片](images/img_8e067013c8.png)

第二张图是你的fieldAvg的排名，同样红色意味着你的位置，如果越靠前说明越好。
我这里的排名还算可以，中等水平，但是还有很大的提升空间。

![图片](images/img_591e992e5e.png)

最后，
希望大家都能在genius项目中取得好成绩，加油！

---

## 讨论与评论 (16)

### 评论 #1 (作者: XX42289, 时间: 1年前)

大家可以修改plot_histogram这个函数的最后一个传入的参数，是列名的意思。就可以绘制不同参数的排行了。

---

### 评论 #2 (作者: FL11741, 时间: 1年前)

[XX42289](/hc/en-us/profiles/14187300941847-XX42289) 
没想到BRAIN的API里真的提供了相应的数据接口，并且也给予了consultant权限。这下我之前写的爬虫脚本就非常多余了LOL。我希望能够在我的帖子下引用您提供的fetch_all_data代码段以对之前的工具进行补充，并附上这篇帖子的链接以及您的User ID，以方便其他顾问查看学习和参考。

---

### 评论 #3 (作者: XX42289, 时间: 1年前)

升级了一下代码，大家更换fetch_all_data以下的全部代码，就可以体验自动计算排名了

```
# 1. 遍历分页 API，收集所有用户数据def fetch_all_data(s):    offset = 0    limit = 30    all_data = []    while True:        response = s.get(f"{base_url}?limit={limit}&offset={offset}&order%3D-fieldAvg&aggregate=user",)        data = response.json()        if "results" in data:            all_data.extend(data["results"])            offset += limit            print(f"Fetched {offset} records")            if offset >= data["count"]:                break        else:            print("Error fetching data")            break        time.sleep(1)    # 保存为CSV文件    df = pd.DataFrame(all_data)    df.to_csv("all_users_data.csv", index=False)    print("Data saved to all_users_data.csv")    return df# 2. 获取自己的用户数据中的leaderboard部分def fetch_self_data(s):    response = s.get("https://api.worldquantbrain.com/users/self/consultant/summary")    self_data = response.json().get("leaderboard", {})    return self_data# 3. 绘制直方图并高亮自己所在位置def plot_histogram(df, self_data, col):    # 获取 fieldAvg 数据    field_avg_data = df[col].dropna()    # 绘制直方图    plt.figure(figsize=(10, 6))    n, bins, patches = plt.hist(field_avg_data, bins=30, color="blue", edgecolor="black", alpha=0.7)    # 确定自己在哪个柱子中    self_field_avg = self_data.get(col)    for i in range(len(bins) - 1):        if bins[i] <= self_field_avg < bins[i + 1]:            patches[i].set_facecolor("red")            break    # 图表设置    plt.xlabel(f"{col}")    plt.ylabel("Frequency")    plt.title(f"Distribution of {col} with Self Highlighted")    plt.show()def rank(df, self_data, cols):    # 计算自己的排名    self_rank = {}    for col in cols:        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            self_val = self_data.get(col)            rank = (df[col] > self_val).sum() + 1            self_rank[col] = str(int(rank / len(df) * 100))+'%'  # 转换为百分比        elif col in ["operatorAvg", "fieldAvg"]:            self_val = self_data.get(col)            rank = (df[col] < self_val).sum() + 1            self_rank[col] = str(int(rank / len(df) * 100))+'%'    return self_rank# ['rank', 'user', 'currentLevel', 'bestLevel', 'alphaCount', 'pyramidCount', 'combinedAlphaPerformance', 'combinedSelectedAlphaPerformance', 'operatorCount', 'operatorAvg', 'fieldCount', 'fieldAvg', 'communityActivity', 'completedReferrals', 'maxSimulationStreak', 'country']# 执行步骤df = fetch_all_data(s)df = df[df['alphaCount'] > 0]df.reset_index(drop=True, inplace=True)self_data = fetch_self_data(s)plot_histogram(df, self_data, "operatorCount")plot_histogram(df, self_data, "operatorAvg")plot_histogram(df, self_data, "fieldCount")plot_histogram(df, self_data, "fieldAvg")plot_histogram(df, self_data, "communityActivity")plot_histogram(df, self_data, "completedReferrals")plot_histogram(df, self_data, "maxSimulationStreak")# 再计算一下自己每个标签的百分比排名my_rank = rank(df, self_data, ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals", "maxSimulationStreak"])print("总人数:", len(df))for k, v in my_rank.items():    print(f"{k}: {v}, 越小越好")
```

---

### 评论 #4 (作者: XX42289, 时间: 1年前)

升级了代码，更直观更方便，只需要设置几个参数就可以选择要不要图片，要不要print内容。

```
# 1. 遍历分页 API，收集所有用户数据import os.pathdef fetch_all_data(s):    offset = 0    limit = 30    all_data = []    while True:        response = s.get(f"{base_url}?limit={limit}&offset={offset}&order%3D-fieldAvg&aggregate=user",)        data = response.json()        if "results" in data:            all_data.extend(data["results"])            offset += limit            print(f"Fetched {offset} records")            if offset >= data["count"]:                break        else:            print("Error fetching data")            break        time.sleep(1)    # 保存为CSV文件    df = pd.DataFrame(all_data)    df.to_csv("all_users_data.csv", index=False)    print("Data saved to all_users_data.csv")    return df# 2. 获取自己的用户数据中的leaderboard部分def fetch_self_data(s):    response = s.get("https://api.worldquantbrain.com/users/self/consultant/summary")    self_data = response.json().get("leaderboard", {})    return self_data# 3. 绘制直方图并高亮自己所在位置def plot_histogram(df, self_data, col):    # 获取 fieldAvg 数据    field_avg_data = df[col].dropna()    # 绘制直方图    plt.figure(figsize=(10, 6))    n, bins, patches = plt.hist(field_avg_data, bins=30, color="blue", edgecolor="black", alpha=0.7)    # 确定自己在哪个柱子中    self_field_avg = self_data.get(col)    for i in range(len(bins) - 1):        if bins[i] <= self_field_avg < bins[i + 1]:            patches[i].set_facecolor("red")            break    # 图表设置    plt.xlabel(f"{col}")    plt.ylabel("Frequency")    plt.title(f"Distribution of {col} with Self Highlighted")    plt.show()def rank(df, self_data, cols):    # 计算自己的排名    self_rank = {}    tt_rk = 0    for col in cols:        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            self_val = self_data.get(col)            rank = (df[col] > self_val).sum() + 1            self_rank[col] = str(int(rank))        elif col in ["operatorAvg", "fieldAvg"]:            self_val = self_data.get(col)            rank = (df[col] < self_val).sum() + 1            self_rank[col] = str(int(rank))        tt_rk += rank    self_rank["total_rank"] = tt_rk    return self_rankdef calculate_ranks(df, cols):    # 创建一个新的DataFrame来存储排名    rank_df = pd.DataFrame(index=df.index, columns=cols)    # 遍历每一列    for col in cols:        # 计算排名，对于数值越大越好的列，使用df[col].rank(method='max', ascending=False)        # 对于数值越小越好的列，使用df[col].rank(method='min', ascending=True)        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            rank_df[col] = df[col].rank(method='min', ascending=False).apply(lambda x: int(x))        elif col in ["operatorAvg", "fieldAvg"]:            rank_df[col] = df[col].rank(method='min', ascending=True).apply(lambda x: int(x))    rank_df['total_rank'] = rank_df.sum(axis=1)    return rank_dfif __name__ == '__main__':    import json    import time    import numpy as np    import requests    import pandas as pd    import matplotlib.pyplot as plt    pd.set_option('expand_frame_repr', False)    pd.set_option('display.max_rows', 50000)    # 参数设置    username = "user_name"    password = "password"    mode = 'expert'    draw_plots = False  # 是否画图    print_info = True  # 是否打印信息    s = requests.Session()    s.auth = (username, password)    response = s.post('https://api.worldquantbrain.com/authentication')    response_content = response.content    response_str = response_content.decode('utf-8')    response_dict = json.loads(response_str)    user_id = response_dict['user']['id']    # API的基本信息    base_url = "https://api.worldquantbrain.com/consultant/boards/genius"    # 执行步骤    if os.path.exists("all_users_data.csv"):        df = pd.read_csv("all_users_data.csv")    else:        df = fetch_all_data(s)    # df = pd.read_csv("all_users_data.csv")    df.reset_index(drop=True, inplace=True)    self_data = fetch_self_data(s)    if draw_plots:        plot_histogram(df, self_data, "operatorCount")        plot_histogram(df, self_data, "operatorAvg")        plot_histogram(df, self_data, "fieldCount")        plot_histogram(df, self_data, "fieldAvg")        plot_histogram(df, self_data, "communityActivity")        plot_histogram(df, self_data, "completedReferrals")        plot_histogram(df, self_data, "maxSimulationStreak")    # 再计算一下自己每个标签的百分比排名    my_rank = rank(df, self_data,                   ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",                    "maxSimulationStreak"])    if print_info:        print("GOLD总人数:", len(df))        print("以下是你各项的排名:")        for k, v in my_rank.items():            print(f"{k}: {v}, 越小越好")    cols = ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",            "maxSimulationStreak"]    rank_df = calculate_ranks(df.set_index('user'), cols)    rank_df = pd.merge(rank_df, df[['user', 'alphaCount', 'pyramidCount', 'combinedAlphaPerformance', 'combinedSelectedAlphaPerformance']], on='user', how='left')    if mode == 'expert':        rank_df = rank_df[rank_df['alphaCount'] >= 20]        rank_df = rank_df[rank_df['pyramidCount'] >= 10]        rank_df = rank_df[(rank_df['combinedAlphaPerformance'] >= 0.5) | (rank_df['combinedSelectedAlphaPerformance'] >= 0.5)]    elif mode == 'master':        rank_df = rank_df[rank_df['alphaCount'] >= 120]        rank_df = rank_df[rank_df['pyramidCount'] >= 30]        rank_df = rank_df[(rank_df['combinedAlphaPerformance'] >= 1) | (rank_df['combinedSelectedAlphaPerformance'] >= 1)]    elif mode == 'grandmaster':        rank_df = rank_df[rank_df['alphaCount'] >= 220]        rank_df = rank_df[rank_df['pyramidCount'] >= 60]        rank_df = rank_df[(rank_df['combinedAlphaPerformance'] >= 2) | (rank_df['combinedSelectedAlphaPerformance'] >= 2)]    my_total_rank = (rank_df['total_rank'] < my_rank['total_rank']).sum()   if print_info:        print(user_id)        print("我的排名:", my_total_rank)        print(f"满足{mode}条件的总人数:", len(rank_df))        if mode == 'grandmaster':            print(f'你想成为【{mode}】', "至少要排名在:", threshold:=int(len(df)*0.02))        elif mode == 'master':            print(f'你想成为【{mode}】', "至少要排名在:", threshold:=int(len(df)*0.10))        elif mode == 'expert':            print(f'你想成为【{mode}】', "至少要排名在:", threshold:=int(len(df)*0.30))        if my_total_rank < threshold:            print(f"恭喜你大概率可以成为【{mode}】")
```

---

### 评论 #5 (作者: XX42289, 时间: 1年前)

再次更新代码，现在更清晰了。

![图片](images/img_fe3ff64f47.png)

```
# 1. 遍历分页 API，收集所有用户数据import os.pathdef fetch_all_data(s):    offset = 0    limit = 30    all_data = []    while True:        response = s.get(f"{base_url}?limit={limit}&offset={offset}&order%3D-fieldAvg&aggregate=user", )        data = response.json()        if "results" in data:            all_data.extend(data["results"])            offset += limit            print(f"Fetched {offset} records")            if offset >= data["count"]:                break        else:            print("Error fetching data")            break        time.sleep(0)    # 保存为CSV文件    df = pd.DataFrame(all_data)    df.to_csv("all_users_data.csv", index=False)    print("Data saved to all_users_data.csv")    return df# 2. 获取自己的用户数据中的leaderboard部分def fetch_self_data(s):    response = s.get("https://api.worldquantbrain.com/users/self/consultant/summary")    self_data = response.json().get("leaderboard", {})    return self_data# 3. 绘制直方图并高亮自己所在位置def plot_histogram(df, self_data, col):    # 获取 fieldAvg 数据    field_avg_data = df[col].dropna()    # 绘制直方图    plt.figure(figsize=(10, 6))    n, bins, patches = plt.hist(field_avg_data, bins=30, color="blue", edgecolor="black", alpha=0.7)    # 确定自己在哪个柱子中    self_field_avg = self_data.get(col)    for i in range(len(bins) - 1):        if bins[i] <= self_field_avg < bins[i + 1]:            patches[i].set_facecolor("red")            break    # 图表设置    plt.xlabel(f"{col}")    plt.ylabel("Frequency")    plt.title(f"Distribution of {col} with Self Highlighted")    plt.show()def rank(df, self_data, cols):    # 计算自己的排名    self_rank = {}    tt_rk = 0    for col in cols:        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            self_val = self_data.get(col)            rank = (df[col] > self_val).sum() + 1            self_rank[col] = str(int(rank))        elif col in ["operatorAvg", "fieldAvg"]:            self_val = self_data.get(col)            rank = (df[col] < self_val).sum() + 1            self_rank[col] = str(int(rank))        tt_rk += rank    self_rank["total_rank"] = tt_rk    return self_rankdef calculate_ranks(df, cols):    # 创建一个新的DataFrame来存储排名    rank_df = pd.DataFrame(index=df.index, columns=cols)    # 遍历每一列    for col in cols:        # 计算排名，对于数值越大越好的列，使用df[col].rank(method='max', ascending=False)        # 对于数值越小越好的列，使用df[col].rank(method='min', ascending=True)        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            rank_df[col] = df[col].rank(method='min', ascending=False).apply(lambda x: int(x))        elif col in ["operatorAvg", "fieldAvg"]:            rank_df[col] = df[col].rank(method='min', ascending=True).apply(lambda x: int(x))    rank_df['total_rank'] = rank_df.sum(axis=1)    return rank_dfif __name__ == '__main__':    import json    import time    import numpy as np    import requests    import pandas as pd    import matplotlib.pyplot as plt    pd.set_option('expand_frame_repr', False)    pd.set_option('display.max_rows', 50000)    # 参数设置    username = "username"    password = "password"    mode = 'grandmaster'  # 'expert', 'master', 'grandmaster'    draw_plots = False  # 是否画图    print_info = True  # 是否打印信息    s = requests.Session()    s.auth = (username, password)    response = s.post('https://api.worldquantbrain.com/authentication')    response_content = response.content    response_str = response_content.decode('utf-8')    response_dict = json.loads(response_str)    user_id = response_dict['user']['id']    # API的基本信息    base_url = "https://api.worldquantbrain.com/consultant/boards/genius"    # 执行步骤    # if os.path.exists("all_users_data.csv"):    #     df = pd.read_csv("all_users_data.csv")    # else:    df = fetch_all_data(s)    df.reset_index(drop=True, inplace=True)    self_data = fetch_self_data(s)    if draw_plots:        plot_histogram(df, self_data, "operatorCount")        plot_histogram(df, self_data, "operatorAvg")        plot_histogram(df, self_data, "fieldCount")        plot_histogram(df, self_data, "fieldAvg")        plot_histogram(df, self_data, "communityActivity")        plot_histogram(df, self_data, "completedReferrals")        plot_histogram(df, self_data, "maxSimulationStreak")    # 再计算一下自己每个标签的百分比排名    my_rank = rank(df, self_data,                   ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",                    "maxSimulationStreak"])    if print_info:        print("GOLD总人数:", len(df))        print("以下是你各项的排名:")        for k, v in my_rank.items():            print(f"{k}: {v}, 越小越好")    cols = ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",            "maxSimulationStreak"]    rank_df = calculate_ranks(df.set_index('user'), cols)    rank_df = pd.merge(rank_df, df[        ['user', 'alphaCount', 'pyramidCount', 'combinedAlphaPerformance', 'combinedSelectedAlphaPerformance']],                       on='user', how='left')    if mode == 'expert':        rank_df = rank_df[rank_df['alphaCount'] >= 20]        rank_df = rank_df[rank_df['pyramidCount'] >= 10]        rank_df = rank_df[            (rank_df['combinedAlphaPerformance'] >= 0.5) | (rank_df['combinedSelectedAlphaPerformance'] >= 0.5)]    elif mode == 'master':        rank_df = rank_df[rank_df['alphaCount'] >= 120]        rank_df = rank_df[rank_df['pyramidCount'] >= 30]        rank_df = rank_df[            (rank_df['combinedAlphaPerformance'] >= 1) | (rank_df['combinedSelectedAlphaPerformance'] >= 1)]    elif mode == 'grandmaster':        rank_df = rank_df[rank_df['alphaCount'] >= 220]        rank_df = rank_df[rank_df['pyramidCount'] >= 60]        rank_df = rank_df[            (rank_df['combinedAlphaPerformance'] >= 2) | (rank_df['combinedSelectedAlphaPerformance'] >= 2)]    my_total_rank = (rank_df['total_rank'] < my_rank['total_rank']).sum()    if print_info:        print(user_id)        print("我的排名:", my_total_rank)        print(f"满足{mode}条件的总人数:", len(rank_df))        if mode == 'grandmaster':            print(f'你想成为【{mode}】', "至少要排名在:", threshold := int(len(df) * 0.02))        elif mode == 'master':            print(f'你想成为【{mode}】', "至少要排名在:", threshold := int(len(df) * 0.10))        elif mode == 'expert':            print(f'你想成为【{mode}】', "至少要排名在:", threshold := int(len(df) * 0.30))        my_alphaCount = self_data.get('alphaCount')        my_pyramidCount = self_data.get('pyramidCount')        my_combinedAlphaPerformance = self_data.get('combinedAlphaPerformance')        my_combinedSelectedAlphaPerformance = self_data.get('combinedSelectedAlphaPerformance')        alphaCount_tag, pyramidCount_tag, combinedAlphaPerformance_tag, total_rank_tag = False, False, False, False        if mode == 'grandmaster':            if my_alphaCount >= 220:                alphaCount_tag = True            if my_pyramidCount >= 60:                pyramidCount_tag = True            if my_combinedAlphaPerformance >= 2 or my_combinedSelectedAlphaPerformance >= 2:                combinedAlphaPerformance_tag = True            if my_total_rank < threshold:                total_rank_tag = True        elif mode == 'master':            if my_alphaCount >= 120:                alphaCount_tag = True            if my_pyramidCount >= 30:                pyramidCount_tag = True            if my_combinedAlphaPerformance >= 1 or my_combinedSelectedAlphaPerformance >= 1:                combinedAlphaPerformance_tag = True            if my_total_rank < threshold:                total_rank_tag = True        elif mode == 'expert':            if my_alphaCount >= 20:                alphaCount_tag = True            if my_pyramidCount >= 10:                pyramidCount_tag = True            if my_combinedAlphaPerformance >= 0.5 or my_combinedSelectedAlphaPerformance >= 0.5:                combinedAlphaPerformance_tag = True            if my_total_rank < threshold:                total_rank_tag = True        if alphaCount_tag and pyramidCount_tag and combinedAlphaPerformance_tag and total_rank_tag:            print(f"恭喜你大概率可以成为【{mode}】")        else:            if not alphaCount_tag:                print(f"你的alphaCount为{my_alphaCount}, 未达到{mode}标准")            if not pyramidCount_tag:                print(f"你的pyramidCount为{my_pyramidCount}, 未达到{mode}标准")            if not combinedAlphaPerformance_tag:                print(                    f"你的combinedAlphaPerformance为{max(my_combinedAlphaPerformance, my_combinedSelectedAlphaPerformance)}, 未达到{mode}标准")            if not total_rank_tag:                print(f"你的总排名为{my_total_rank}, 未达到{mode}标准")            print("同志还需努力！！！")
```

---

### 评论 #6 (作者: XH93773, 时间: 1年前)

点赞是对创作者最大的敬意，respect！！！

---

### 评论 #7 (作者: XX42289, 时间: 1年前)

```
# 1. 遍历分页 API，收集所有用户数据import os.pathdef fetch_all_data(s):    offset = 0    limit = 30    all_data = []    while True:        response = s.get(f"{base_url}?limit={limit}&offset={offset}&order%3D-fieldAvg&aggregate=user", )        data = response.json()        if "results" in data:            all_data.extend(data["results"])            offset += limit            print(f"Fetched {offset} records")            if offset >= data["count"]:                break        else:            print("Error fetching data")            break        time.sleep(0)    # 保存为CSV文件    df = pd.DataFrame(all_data)    df.to_csv("all_users_data.csv", index=False)    print("Data saved to all_users_data.csv")    return df# 2. 获取自己的用户数据中的leaderboard部分def fetch_self_data(s):    response = s.get("https://api.worldquantbrain.com/users/self/consultant/summary")    self_data = response.json().get("leaderboard", {})    return self_data# 3. 绘制直方图并高亮自己所在位置def plot_histogram(df, self_data, col):    # 获取 fieldAvg 数据    field_avg_data = df[col].dropna()    # 绘制直方图    plt.figure(figsize=(10, 6))    n, bins, patches = plt.hist(field_avg_data, bins=30, color="blue", edgecolor="black", alpha=0.7)    # 确定自己在哪个柱子中    self_field_avg = self_data.get(col)    for i in range(len(bins) - 1):        if bins[i] <= self_field_avg < bins[i + 1]:            patches[i].set_facecolor("red")            break    # 图表设置    plt.xlabel(f"{col}")    plt.ylabel("Frequency")    plt.title(f"Distribution of {col} with Self Highlighted")    plt.show()def rank(df, self_data, cols):    # 计算自己的排名    self_rank = {}    tt_rk = 0    for col in cols:        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            self_val = self_data.get(col)            rank = (df[col] > self_val).sum() + 1            self_rank[col] = str(int(rank))        elif col in ["operatorAvg", "fieldAvg"]:            self_val = self_data.get(col)            rank = (df[col] < self_val).sum() + 1            self_rank[col] = str(int(rank))        tt_rk += rank    self_rank["total_rank"] = tt_rk    return self_rankdef calculate_ranks(df, cols):    # 创建一个新的DataFrame来存储排名    rank_df = pd.DataFrame(index=df.index, columns=cols)    # 遍历每一列    for col in cols:        # 计算排名，对于数值越大越好的列，使用df[col].rank(method='max', ascending=False)        # 对于数值越小越好的列，使用df[col].rank(method='min', ascending=True)        if col in ["operatorCount", "fieldCount", "communityActivity", "completedReferrals", "maxSimulationStreak"]:            rank_df[f"{col}_rank"] = df[col].rank(method='min', ascending=False).apply(lambda x: int(x))        elif col in ["operatorAvg", "fieldAvg"]:            rank_df[f"{col}_rank"] = df[col].rank(method='min', ascending=True).apply(lambda x: int(x))        del rank_df[col]    rank_df['total_rank'] = rank_df.sum(axis=1)    return rank_dfif __name__ == '__main__':    import json    import time    import numpy as np    import requests    import pandas as pd    import matplotlib.pyplot as plt    pd.set_option('expand_frame_repr', False)    pd.set_option('display.max_rows', 50000)    # 参数设置    user_id = 'XX12345'  # 你的ID    username = "user"    password = "password"    mode = 'grandmaster'  # 'expert', 'master', 'grandmaster'    draw_plots = False  # 是否画图    print_info = True  # 是否打印信息    quarter_pay_num = 40  # 假设满足季度奖励的人需要交满40个    s = requests.Session()    s.auth = (username, password)    response = s.post('https://api.worldquantbrain.com/authentication')    response_content = response.content    response_str = response_content.decode('utf-8')    response_dict = json.loads(response_str)    # user_id = response_dict['user']['id']    # API的基本信息    base_url = "https://api.worldquantbrain.com/consultant/boards/genius"    # 执行步骤    if os.path.exists("all_users_data.csv"):        df = pd.read_csv("all_users_data.csv")    else:        df = fetch_all_data(s)    # df = fetch_all_data(s)    df.reset_index(drop=True, inplace=True)    # self_data = fetch_self_data(s)    self_data = df.loc[df['user']==user_id].to_dict(orient='records')[0]    print(self_data)    if draw_plots:        plot_histogram(df, self_data, "operatorCount")        plot_histogram(df, self_data, "operatorAvg")        plot_histogram(df, self_data, "fieldCount")        plot_histogram(df, self_data, "fieldAvg")        plot_histogram(df, self_data, "communityActivity")        plot_histogram(df, self_data, "completedReferrals")        plot_histogram(df, self_data, "maxSimulationStreak")    # 再计算一下自己每个标签的百分比排名    my_rank = rank(df, self_data,                   ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",                    "maxSimulationStreak"])    if print_info:        print("GOLD总人数:", len(df))        print(f"可能满足季度奖金的总人数（交满{quarter_pay_num}个）:", len(df[df['alphaCount']>quarter_pay_num]))        print("以下是你各项的排名:")        for k, v in my_rank.items():            print(f"{k}: {v}, 越小越好")    cols = ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",            "maxSimulationStreak"]    rank_df = calculate_ranks(df.set_index('user'), cols)    rank_df = pd.merge(rank_df, df[        ['user', 'alphaCount', 'pyramidCount', 'combinedAlphaPerformance', 'combinedSelectedAlphaPerformance', "operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals", 'maxSimulationStreak']],                       on='user', how='left')    rank_df['预测排名（不准，以官方为准）'] = rank_df['total_rank'].rank(method='min', ascending=True).apply(lambda x: int(x))    rank_df[['user', '预测排名（不准，以官方为准）', 'alphaCount', 'pyramidCount', "operatorAvg", "fieldAvg"]].to_csv('temp/rank预计排名（非官方，仅供参考）.csv', index=False, encoding='gbk')    if mode == 'expert':        rank_df = rank_df[rank_df['alphaCount'] >= 20]        rank_df = rank_df[rank_df['pyramidCount'] >= 10]        rank_df = rank_df[            (rank_df['combinedAlphaPerformance'] >= 0.5) | (rank_df['combinedSelectedAlphaPerformance'] >= 0.5)]    elif mode == 'master':        rank_df = rank_df[rank_df['alphaCount'] >= 120]        rank_df = rank_df[rank_df['pyramidCount'] >= 30]        rank_df = rank_df[            (rank_df['combinedAlphaPerformance'] >= 1) | (rank_df['combinedSelectedAlphaPerformance'] >= 1)]    elif mode == 'grandmaster':        rank_df = rank_df[rank_df['alphaCount'] >= 220]        rank_df = rank_df[rank_df['pyramidCount'] >= 60]        rank_df = rank_df[            (rank_df['combinedAlphaPerformance'] >= 2) | (rank_df['combinedSelectedAlphaPerformance'] >= 2)]    rank_df[['user', '预测排名（不准，以官方为准）', 'alphaCount', 'pyramidCount', "operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",                    "maxSimulationStreak"]].to_csv('temp/rank预计排名（非官方，仅供参考）.csv', index=False, encoding='gbk')    my_total_rank = (rank_df['total_rank'] < my_rank['total_rank']).sum()    if print_info:        print("|+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+|")        print("|+=+==+=+=以下是按照gold为universe计算的排名=+==+=+==+=+|")        print("|+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+|")        print(user_id)        print("我的排名:", my_total_rank)        print(f"满足{mode}条件的总人数:", len(rank_df))        if mode == 'grandmaster':            print(f'你想成为【{mode}】', "至少要排名在:", threshold := int(len(df[df['alphaCount']>40]) * 0.02))        elif mode == 'master':            print(f'你想成为【{mode}】', "至少要排名在:", threshold := int(len(df[df['alphaCount']>40]) * 0.08))        elif mode == 'expert':            print(f'你想成为【{mode}】', "至少要排名在:", threshold := int(len(df[df['alphaCount']>40]) * 0.20))        my_alphaCount = self_data.get('alphaCount')        my_pyramidCount = self_data.get('pyramidCount')        my_combinedAlphaPerformance = self_data.get('combinedAlphaPerformance')        my_combinedSelectedAlphaPerformance = self_data.get('combinedSelectedAlphaPerformance')        alphaCount_tag, pyramidCount_tag, combinedAlphaPerformance_tag, total_rank_tag = False, False, False, False        if mode == 'grandmaster':            if my_alphaCount >= 220:                alphaCount_tag = True            if my_pyramidCount >= 60:                pyramidCount_tag = True            if my_combinedAlphaPerformance >= 2 or my_combinedSelectedAlphaPerformance >= 2:                combinedAlphaPerformance_tag = True            if my_total_rank < threshold:                total_rank_tag = True        elif mode == 'master':            if my_alphaCount >= 120:                alphaCount_tag = True            if my_pyramidCount >= 30:                pyramidCount_tag = True            if my_combinedAlphaPerformance >= 1 or my_combinedSelectedAlphaPerformance >= 1:                combinedAlphaPerformance_tag = True            if my_total_rank < threshold:                total_rank_tag = True        elif mode == 'expert':            if my_alphaCount >= 20:                alphaCount_tag = True            if my_pyramidCount >= 10:                pyramidCount_tag = True            if my_combinedAlphaPerformance >= 0.5 or my_combinedSelectedAlphaPerformance >= 0.5:                combinedAlphaPerformance_tag = True            if my_total_rank < threshold:                total_rank_tag = True        if alphaCount_tag and pyramidCount_tag and combinedAlphaPerformance_tag and total_rank_tag:            print(f"恭喜你大概率可以成为【{mode}】")        else:            if not alphaCount_tag:                print(f"你的alphaCount为{my_alphaCount}, 未达到{mode}标准")            if not pyramidCount_tag:                print(f"你的pyramidCount为{my_pyramidCount}, 未达到{mode}标准")            if not combinedAlphaPerformance_tag:                print(                    f"你的combinedAlphaPerformance为{max(my_combinedAlphaPerformance, my_combinedSelectedAlphaPerformance)}, 未达到{mode}标准")            if not total_rank_tag:                print(f"你的总排名为{my_total_rank}, 未达到{mode}标准")            print("同志还需努力！！！")    rank_df = calculate_ranks(rank_df.set_index('user'), cols)    rank_df = pd.merge(rank_df, df[        ['user', 'alphaCount', 'pyramidCount', 'combinedAlphaPerformance', 'combinedSelectedAlphaPerformance',         "operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",         'maxSimulationStreak']],                       on='user', how='left')    # 再计算一下自己每个标签的百分比排名    my_rank = rank(rank_df, self_data,                   ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",                    "maxSimulationStreak"])    rank_df['预测排名（不准，以官方为准）'] = rank_df['total_rank'].rank(method='min', ascending=True).apply(        lambda x: int(x))    rank_df[['user', '预测排名（不准，以官方为准）', 'alphaCount', 'pyramidCount', "operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",                    "maxSimulationStreak"]].to_csv(        f'temp/rank相对等级{mode}.csv', index=False, encoding='gbk')    my_total_rank = (rank_df['total_rank'] < my_rank['total_rank']).sum()    if print_info:        print("|+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+|")        print(f"|+=+==+=+=以下是按照{mode}为universe计算的排名=+==+=+==+=+|")        print("|+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+=+==+|")        print(user_id)        print(f"满足{mode}总人数:", len(rank_df))        print(f"以下是你在{mode}池子里的各项的排名:")        for k, v in my_rank.items():            print(f"{k}: {v}, 越小越好")        print(f"以{mode}作为池子的总排名：", my_total_rank)
```

---

### 评论 #8 (作者: ZL80407, 时间: 1年前)

手动点赞，兼送膝盖！XX大佬！

---

### 评论 #9 (作者: LL87164, 时间: 1年前)

operatorCount:  为什么是越小越好？这跟鼓励分散鼓励多用的不同Operator不是相违背吗？

operatorAvg: 这个是指单个alpha里的Operator越少越好对吗？

fieldCount: 为什么是越小越好？这跟鼓励分散鼓励多用的不同field不是相违背吗？

fieldAvg: 这个是指单个alpha里的field越少越好对吗？

communityActivity: 这个是什么意思？论坛积极度吗？为什么也是越小越好

completedReferrals: 这个是什么意思？为什么是越小越好

maxSimulationStreak: 这个是什么意思？为什么是越小越好

---

### 评论 #10 (作者: KZ79256, 时间: 1年前)

[LL87164](/hc/en-us/profiles/28834270391959-LL87164)

operatorCount是越大越好，不过课代表的代码把其改成排名，越大排名越小，所以最后是排名越小越好

operatorAvg是指单个alpha里的Operator越少越好

fieldCount也是越大越好，和operatorCount同理

fieldAvg是指单个alpha里的field越少越好

communityActivity：指的是论坛活跃度，别人点赞你的评论或post，你可以增加活跃度，同样也是越大越好

completedReferrals：是完成推荐的人数，越大越好，同理operatorCount

maxSimulationStreak：是指最长的联系回测时间，越大越好，同理operatorCount

建议认真看一下genius的QA。。。

---

### 评论 #11 (作者: JH44290, 时间: 1年前)

感谢大佬，我运行了这个帖子最新的那个代码版本，出现这个报错，应该怎样做呢？

---------------------------------------------------------------------------

KeyError Traceback (most recent call last) File c:\Python\Python312\Lib\site-packages\pandas\core\indexes\base.py:3805, in Index.get_loc(self, key)

3804 try:

-> 3805 return self._engine.get_loc(casted_key)

3806 except KeyError as err:

File index.pyx:167, in pandas._libs.index.IndexEngine.get_loc()

File index.pyx:196, in pandas._libs.index.IndexEngine.get_loc()

File pandas\_libs\hashtable_class_helper.pxi:7081, in pandas._libs.hashtable.PyObjectHashTable.get_item()

File pandas\_libs\hashtable_class_helper.pxi:7089, in pandas._libs.hashtable.PyObjectHashTable.get_item()

KeyError: 'completedReferrals'

The above exception was the direct cause of the following exception:

KeyError Traceback (most recent call last)

Cell In[1], line 153

150 plot_histogram(df, self_data, "maxSimulationStreak")

152 # 再计算一下自己每个标签的百分比排名

--> 153 my_rank = rank(df, self_data,

154 ["operatorCount", "operatorAvg", "fieldCount", "fieldAvg", "communityActivity", "completedReferrals",

...

3815 # InvalidIndexError. Otherwise we fall through and re-raise

3816 # the TypeError.

3817 self._check_indexing_error(key)

KeyError: 'completedReferrals'

---

### 评论 #12 (作者: KZ79256, 时间: 1年前)

[JH44290](/hc/en-us/profiles/28903565485847-JH44290)  因为新的Q2赛季没有completedReferrals这个维度了，如果你想查看Q1的成绩不如等到明天就公布了，Q2的成绩现在查看没有意义，大家还没把代码debug好。
=========================================================================

---

### 评论 #13 (作者: XH86688, 时间: 1年前)

感谢鑫佬，想请问下现在这个API是不再能访问到user id了吗，出现这个报错，改怎么操作呢？

---

### 评论 #14 (作者: YW10763, 时间: 1年前)

这边建议提交一点数量的alpha之后再来跑课代表的代码， 不然有偶然性

---

### 评论 #15 (作者: CW99271, 时间: 10个月前)

这排名结果的样式看起来很熟悉，仔细看看，原来这个作者是鑫鑫大神呀

---

### 评论 #16 (作者: TK25060, 时间: 7个月前)

我的表一是横轴alphacount,纵轴是frequency，这张表怎么理解呢

---

