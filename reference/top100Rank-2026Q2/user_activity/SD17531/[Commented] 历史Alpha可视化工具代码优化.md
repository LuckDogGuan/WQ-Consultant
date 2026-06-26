# 历史Alpha可视化工具代码优化

- **链接**: [Commented] 历史Alpha可视化工具代码优化.md
- **作者**: LQ99002
- **发布时间/热度**: 1年前, 得票: 12

## 帖子正文

来自研究小组的Alpha统计分析工具。

```
# %% [markdown]# # 登录# %%def sign_in():    import requests    from time import sleep    # Initialize variables to hold the username and password    #--------------------WARNING--------------------    username = "xxxxx@xxxxx.com"  # NEVER SHARE YOUR USERNAME AND PASSWORD    password = "xxxxxxxxxxxxxx"   # NEVER SHARE YOUR USERNAME AND PASSWORD    #--------------------WARNING--------------------    # Create a session to persistently store the headers    s = requests.Session()    # Save credentials into the session    s.auth = (username, password)    while True:        try:            # Send a POST request to the /authentication API            response = s.post('https://api.worldquantbrain.com/authentication')            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx            print("Authentication successful.")            break  # Exit the loop on success        except requests.HTTPError as e:            print(f"HTTP error occurred: {e}. Retrying...")  # Provide more specific error message            sleep(10)        except Exception as e:            print(f"Error during authentication: {e}. Trying to login again.")            sleep(10)    return ssession = sign_in()# %% [markdown]# # 下载历史表现# %%# Function to fetch a specific number of IS alphas (`total_alphas`) using pagination.def get_n_os_alphas(session, total_alphas, limit=100):    fetched_alphas = []    offset = 0    # Keep fetching alphas until the required number of alphas is reached or no more alphas are available.    while len(fetched_alphas) < total_alphas:        response = session.get(            f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}"        )        alphas = response.json()["results"]        fetched_alphas.extend(alphas)        if len(alphas) < limit:            break        offset += limit    return fetched_alphas[:total_alphas]alpha_list_submitted = get_n_os_alphas(session, 3000)# %%# dump the alpha list to a JSON fileimport jsonwith open('alpha_list_submitted.json', 'w') as f:    json.dump(alpha_list_submitted, f, indent=4)# %%len(alpha_list_submitted)# make it to a dataframeimport pandas as pddf_alpha_list_submitted = pd.DataFrame(alpha_list_submitted)# save the# %% [markdown]# # 分析1：Alpha分布图# %%# 对于每一个region，我们画出一个直方图，展示Sharpe, turnover, return, margin, fitness# 每个region画一个大图，里面由相应的小图组成import matplotlib.pyplot as pltimport seaborn as snsimport numpy as npimport matplotlib.gridspec as gridspecimport matplotlib.cm as cmimport matplotlib.colors as mcolorsimport matplotlib.ticker as tickerimport matplotlib.patches as mpatches# each alpha is a row in the dataframe, and we can get the region from the settings column Index seetings, where it is a dic and there is a key value for 'region'# for each alpha, we can have performance in IS and OS, we look at the IS performance firstdef get_region(alpha_list_submitted, region):    # filter the alpha_list_submitted dataframe by region    df_region = alpha_list_submitted[alpha_list_submitted['settings'].apply(lambda x: x['region'] == region)]    return df_regiondef get_performance(df_region, performance_type):    # filter the performance type from the dataframe    df_performance = df_region[performance_type]    return df_performancedef get_performance_metrics(df_performance):    # extract the performance metrics from the dataframe    sharpe = df_performance.apply(lambda x: x.get('sharpe', np.nan))    turnover = df_performance.apply(lambda x: x.get('turnover', np.nan))    returns = df_performance.apply(lambda x: x.get('returns', np.nan))    margin = df_performance.apply(lambda x: x.get('margin', np.nan))    fitness = df_performance.apply(lambda x: x.get('fitness', np.nan))    return sharpe, turnover, returns, margin, fitnessdef plot_performance_metrics(sharpe, turnover, returns, margin, fitness, region):    # set up the figure and axes for the subplots    fig = plt.figure(figsize=(15, 10))    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[1, 1])    ax0 = fig.add_subplot(gs[0, 0])    ax1 = fig.add_subplot(gs[0, 1])    ax2 = fig.add_subplot(gs[1, 0])    ax3 = fig.add_subplot(gs[1, 1])    ax4 = fig.add_subplot(gs[2, :])    # plot the histograms for each metric    sns.histplot(sharpe, bins=20, kde=True, ax=ax0)    sns.histplot(turnover, bins=20, kde=True, ax=ax1)    sns.histplot(returns, bins=20, kde=True, ax=ax2)    sns.histplot(margin, bins=20, kde=True, ax=ax3)    sns.histplot(fitness, bins=20, kde=True, ax=ax4)    # set titles and labels for each subplot    ax0.set_title(f'Sharpe Ratio Distribution in {region}')    ax1.set_title(f'Turnover Distribution in {region}')    ax2.set_title(f'Returns Distribution in {region}')    ax3.set_title(f'Margin Distribution in {region}')    ax4.set_title(f'Fitness Distribution in {region}')    plt.tight_layout()    plt.show()def plot_is_os_performance_matrix(df_is_performance, df_os_performance, region):    # extract the performance metrics for IS and OS    sharpe_is, turnover_is, returns_is, margin_is, fitness_is = get_performance_metrics(df_is_performance)    sharpe_os, turnover_os, returns_os, margin_os, fitness_os = get_performance_metrics(df_os_performance)    # for the same histpolot, we will put the IS and OS performance in the same histogram, we can use different color for the IS and OS performance    # set up the figure and axes for the subplots    fig = plt.figure(figsize=(15, 10))    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[1, 1])    ax0 = fig.add_subplot(gs[0, 0])    ax1 = fig.add_subplot(gs[0, 1])    ax2 = fig.add_subplot(gs[1, 0])    ax3 = fig.add_subplot(gs[1, 1])    ax4 = fig.add_subplot(gs[2, :])    # plot the histograms for each metric    sns.histplot(sharpe_is, bins=20, kde=True, ax=ax0, color='blue', label='IS')    sns.histplot(sharpe_os, bins=20, kde=True, ax=ax0, color='orange', label='OS')    # set the x-label to be the same for both IS and OS    ax0.set_xlabel('Sharpe Ratio')    ax0.legend()    sns.histplot(turnover_is, bins=20, kde=True, ax=ax1, color='blue', label='IS')    sns.histplot(turnover_os, bins=20, kde=True, ax=ax1, color='orange', label='OS')    ax1.set_xlabel('Turnover')    ax1.legend()    sns.histplot(returns_is, bins=20, kde=True, ax=ax2, color='blue', label='IS')    sns.histplot(returns_os, bins=20, kde=True, ax=ax2, color='orange', label='OS')    ax2.set_xlabel('Returns')    ax2.legend()    sns.histplot(margin_is, bins=20, kde=True, ax=ax3, color='blue', label='IS')    sns.histplot(margin_os, bins=20, kde=True, ax=ax3, color='orange', label='OS')    ax3.set_xlabel('Margin')    ax3.legend()    sns.histplot(fitness_is, bins=20, kde=True, ax=ax4, color='blue', label='IS')    sns.histplot(fitness_os, bins=20, kde=True, ax=ax4, color='orange', label='OS')    ax4.set_xlabel('Fitness')    ax4.legend()       # set titles and labels for each subplot    ax0.set_title(f'Sharpe Ratio Distribution in {region}')    ax1.set_title(f'Turnover Distribution in {region}')    ax2.set_title(f'Returns Distribution in {region}')    ax3.set_title(f'Margin Distribution in {region}')    ax4.set_title(f'Fitness Distribution in {region}')    plt.tight_layout()    plt.show()# 获取不同region，并画出不同region的performanceregions = df_alpha_list_submitted['settings'].apply(lambda x: x['region']).unique()for region in regions:    df_region = get_region(df_alpha_list_submitted, region)    df_is_performance = get_performance(df_region, 'is')    df_os_performance = get_performance(df_region, 'os')    sharpe_os, turnover_os, returns_os, margin_os, fitness_os = get_performance_metrics(df_os_performance)    sharpe_is, turnover_is, returns_is, margin_is, fitness_is = get_performance_metrics(df_is_performance)    plot_is_os_performance_matrix(df_is_performance, df_os_performance, region)# %% [markdown]# # 分析2：Alpha趋势分布图# %%# 画出一个不同matric跟Sharpe的散点图，并拟合出一条线，展示不同的performance跟Sharpe的关系import matplotlib.pyplot as pltimport seaborn as snsimport numpy as npimport matplotlib.gridspec as gridspecimport matplotlib.cm as cmregion = 'USA'df_region = get_region(df_alpha_list_submitted, region)df_is_performance = get_performance(df_region, 'is')df_os_performance = get_performance(df_region, 'os')sharpe_os, turnover_os, returns_os, margin_os, fitness_os = get_performance_metrics(df_os_performance)sharpe_is, turnover_is, returns_is, margin_is, fitness_is = get_performance_metrics(df_is_performance)# define a function, the take in is the sharpe_os, turnover_os, returns_os, margin_os, fitness_os; sharpe_is, turnover_is, returns_is, margin_is, fitness_is# there should be 5 subplots, and each subplot should be a scatter plot, and the x-axis is the sharpe, and the y-axis is the other performance metrics# for each subplot, show both IS and OS performance, and use different color for IS and OS performancedef plot_sharpe_vs_performance(sharpe_os, turnover_os, returns_os, margin_os, fitness_os, sharpe_is, turnover_is, returns_is, margin_is, fitness_is,region):    # set up the figure and axes for the subplots    fig = plt.figure(figsize=(15, 10))    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[1, 1])    ax0 = fig.add_subplot(gs[0, 0])    ax1 = fig.add_subplot(gs[0, 1])    ax2 = fig.add_subplot(gs[1, 0])    ax3 = fig.add_subplot(gs[1, 1])    ax4 = fig.add_subplot(gs[2, :])    # plot the scatter plots for each metric    sns.scatterplot(x=sharpe_os, y=turnover_os, ax=ax0, color='orange', label='OS')    sns.scatterplot(x=sharpe_is, y=turnover_is, ax=ax0, color='blue', label='IS')    sns.regplot(x=sharpe_os, y=turnover_os, ax=ax0, scatter=False, color='orange')    sns.regplot(x=sharpe_is, y=turnover_is, ax=ax0, scatter=False, color='blue')    ax0.set_xlabel('Sharpe Ratio')    ax0.set_ylabel('Turnover')    ax0.legend()    ax0.set_title(f'Sharpe Ratio vs Turnover in {region}')    sns.scatterplot(x=sharpe_os, y=returns_os, ax=ax1, color='orange', label='OS')    sns.scatterplot(x=sharpe_is, y=returns_is, ax=ax1, color='blue', label='IS')    sns.regplot(x=sharpe_os, y=returns_os, ax=ax1, scatter=False, color='orange')    sns.regplot(x=sharpe_is, y=returns_is, ax=ax1, scatter=False, color='blue')    ax1.set_xlabel('Sharpe Ratio')    ax1.set_ylabel('Returns')    ax1.legend()    ax1.set_title(f'Sharpe Ratio vs Returns in {region}')       sns.scatterplot(x=sharpe_os, y=margin_os, ax=ax2, color='orange', label='OS')    sns.scatterplot(x=sharpe_is, y=margin_is, ax=ax2, color='blue', label='IS')    sns.regplot(x=sharpe_os, y=margin_os, ax=ax2, scatter=False, color='orange')    sns.regplot(x=sharpe_is, y=margin_is, ax=ax2, scatter=False, color='blue')    ax2.set_xlabel('Sharpe Ratio')    ax2.set_ylabel('Margin')    ax2.legend()    ax2.set_title(f'Sharpe Ratio vs Margin in {region}')    sns.scatterplot(x=sharpe_os, y=fitness_os, ax=ax3, color='orange', label='OS')    sns.scatterplot(x=sharpe_is, y=fitness_is, ax=ax3, color='blue', label='IS')    sns.regplot(x=sharpe_os, y=fitness_os, ax=ax3, scatter=False, color='orange')    sns.regplot(x=sharpe_is, y=fitness_is, ax=ax3, scatter=False, color='blue')    ax3.set_xlabel('Sharpe Ratio')    ax3.set_ylabel('Fitness')    ax3.legend()    ax3.set_title(f'Sharpe Ratio vs Fitness in {region}')    sns.scatterplot(x=sharpe_os, y=sharpe_is, ax=ax4, color='orange', label='OS')    sns.scatterplot(x=sharpe_is, y=sharpe_is, ax=ax4, color='blue', label='IS')    sns.regplot(x=sharpe_os, y=sharpe_is, ax=ax4, scatter=False, color='orange')    sns.regplot(x=sharpe_is, y=sharpe_is, ax=ax4, scatter=False, color='blue')    ax4.set_xlabel('Sharpe Ratio OS')    ax4.set_ylabel('Sharpe Ratio IS')    ax4.legend()    ax4.set_title(f'Sharpe Ratio OS vs Sharpe Ratio IS in {region}')    plt.tight_layout()    plt.show()# Example usage# region = 'USA'# plot_sharpe_vs_performance(sharpe_os, turnover_os, returns_os, margin_os, fitness_os, sharpe_is, turnover_is, returns_is, margin_is, fitness_is, region)# 获取不同region，并画出不同region的performanceregions = df_alpha_list_submitted['settings'].apply(lambda x: x['region']).unique()for region in regions:    df_region = get_region(df_alpha_list_submitted, region)    df_is_performance = get_performance(df_region, 'is')    df_os_performance = get_performance(df_region, 'os')    sharpe_os, turnover_os, returns_os, margin_os, fitness_os = get_performance_metrics(df_os_performance)    sharpe_is, turnover_is, returns_is, margin_is, fitness_is = get_performance_metrics(df_is_performance)    plot_sharpe_vs_performance(sharpe_os, turnover_os, returns_os, margin_os, fitness_os, sharpe_is, turnover_is, returns_is, margin_is, fitness_is, region)# %% [markdown]# # 分析3：数据字段使用情况（分区域图）# %% [markdown]# ![image.png](attachment:image.png)# %% [markdown]# ![image.png](attachment:image.png)# %% [markdown]# ![image.png](attachment:image.png)# %% [markdown]# # 总结反思
```

---

## 讨论与评论 (8)

### 评论 #1 (作者: WL13229, 时间: 1年前)

从多元化的角度来说，用户需要尽可能像俄罗斯方块消消乐一样，把自己蓝色的柱子变成一个平均的情况，即不要集中在某种turnover或者fitness中

---

### 评论 #2 (作者: WL13229, 时间: 1年前)

![图片](images/img_079c09f822.png)

---

### 评论 #3 (作者: WL13229, 时间: 1年前)

发帖请带示例图

---

### 评论 #4 (作者: MG88592, 时间: 1年前)

==============================================================================
==============================================================================
非常好用的一个功能，可以分地区多指标的呈现出历史的alpha信息，希望大家都配置起来，提升效率。
==============================================================================

---

### 评论 #5 (作者: BW14163, 时间: 1年前)

感谢大佬分享，先收藏了

---

### 评论 #6 (作者: SD17531, 时间: 1年前)

工具很好用,但是需要注意.

这个工具能够给我们看到的数据是OS更新了半年的数据,比如2024年7月-2025年1月提交的alpha, 他的OS从2022年7月份开始是我们看不到的, 在WQ更新了OS数据以后,就可以在网页上看到你的alpha在2022年7月-2023年1月的数据表现了.所以这只是半年的数据, 用这半年的数据,来判断你的alpha是否表现好,是不足够的.

但是依旧能够给我们带来很多的启发, 比如查看自己的PNL发现,在样本内的表现sharpe都是正的,但是更新给你了半年的OS以后,又出现负数,或者是很大的负数,那么这个alpha多半有问题,不应该出现巨大偏差,可能是过拟合了或者因子失效了.

然后, 即使在网页上看到的OS数据,表现还可以了,依旧无法确认这个alpha是否OS稳定,因为还有2年的OS是无法看到的.

按照群友的说法,OS sharpe / IS sharpe > 0.5,这个因子就已经比较好了

希望大家都能挖到好因子

---

### 评论 #7 (作者: FL39657, 时间: 1年前)

很好用，可以帮助自己分析自己的alpha

---

### 评论 #8 (作者: XC66172, 时间: 1年前)

这个必须要收藏~ 可以看到提交因子的IS OS指标分布的工具太好了。

不过现在是我参加的第一个赛季，估计还看不到OS数据，等有了OS数据就可以进一步分析什么样的IS因子更容易拿到好的OS了。

WEIJIE老师的示例图也很有借鉴意义，SHARPE的OS相比IS整体左移，可以看到大多数的因子SHARPE表现都会衰退..

=====================================

每天睡醒就搓搓因子，总有一个是好的

=====================================

---

