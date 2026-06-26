# 如何利用可视化来筛选更好的数据集？代码优化

- **链接**: [Commented] 如何利用可视化来筛选更好的数据集代码优化.md
- **作者**: XX42289
- **发布时间/热度**: 1年前, 得票: 31

## 帖子正文

## 如何利用可视化来筛选更好的数据集？

我们都知道World Quant提供了大量的数据集，如analyst16, model26等等。
然而，面对大量的数据集，我们如何判断一个数据集的质量呢？
这里我将分享一种我自己在用的简单而有效的方法：通过可视化来筛选数据集，特别是利用直方图来分析alpha各种指标的分布。

## 为什么使用直方图？

直方图是一种能够显示数据分布情况的图表。通过观察直方图，我们可以快速了解数据的集中趋势、离散程度以及可能存在的异常值。在金融数据分析中，alpha因子的表现至关重要，通过绘制alpha的多个指标（如Sharpe Ratio、Turnover、Fitness等）的直方图，可以直观地看到这些指标的分布情况。

### 代码实现

以下Python代码，该代码展示了如何利用`matplotlib`和`seaborn`库绘制alpha指标的直方图。
但是一定要注意，光炒代码是无法运行的，你需要先准备好alpha指标的数据集，然后将其传入到下面的代码中。
你的df一定要有的列是：'sharpe', 'turnover', 'fitness', 'margin', 'longCount', 'shortCount'
你可以通过api来批量获取这些信息

```
import pandas as pdimport numpy as npimport matplotlib.pyplot as pltimport seaborn as snsdef plot_histogram(df, column_name, plot_title, bins):    sns.set(style="whitegrid")    plt.figure(figsize=(10, 6))    sns.histplot(df[column_name], bins=bins, kde=False, color='skyblue', edgecolor='black')    plt.title(plot_title, fontsize=16)    plt.xlabel(column_name, fontsize=14)    plt.ylabel('Frequency', fontsize=14)    plt.tight_layout()    plt.show()
```

```
# 在这之前，需要先准备好alpha指标的数据集，我这里用一个示例数据集来演示，# 其中一定要有'sharpe', 'turnover', 'fitness', 'margin', 'longCount', 'shortCount'这几列才行，否则会报错df = pd.DataFrame(alphas, columns=['alpha_id', 'exp', 'sharpe', 'turnover', 'fitness', 'margin', 'longCount', 'shortCount', 'dateCreated', 'decay'])sharp_bins = np.arange(-3, 3.1, 0.1).round(2)turnover_bins = np.arange(0, 1.05, 0.05).round(2)fitness_bins = np.arange(-2, 2.05, 0.05).round(2)longCount_bins = np.arange(0, 1500, 100)shortCount_bins = np.arange(0, 1500, 100)plot_histogram(df, 'sharpe', 'Distribution of Sharpe Ratio', bins=sharp_bins)plot_histogram(df, 'turnover', 'Distribution of Turnover', bins=turnover_bins)plot_histogram(df, 'fitness', 'Distribution of Fitness', bins=fitness_bins)plot_histogram(df, 'longCount', 'Distribution of Long Count', bins=longCount_bins)plot_histogram(df, 'shortCount', 'Distribution of Short Count', bins=shortCount_bins)
```

### 如何解读直方图？

通过上述代码，可以生成多个alpha指标的直方图。特别地，如果发现更多的alpha落在高Sharpe Ratio的区域，说明这个数据集可能具有更好的质量。
解下来我以一个例子来解释一下。
region:USA
delay:1
instrumentType:EQUITY
universe:TOP3000
datasest_id:analyst14

我一共在analyst14这个数据集中回测了20000个alpha，可以看到analyst14这个数据集的Sharpe Ratio的直方图，大部分的比率集中在0附近，但是是明显右边部分更多，也就是说analyst14这个数据集有更多的正alpha，而且在sharpe为1的附近是有不少alpha的，所以这个数据集质量还行。

![图片](images/img_fe605b66d4.png) 
再看turnover的直方图，可以看到大部分的alpha的turnover都在0.2以下，这说明这个数据集的alpha的turnover都比较低，这也是比较好的。

![图片](images/img_916170b968.png) 
再看fitness的直方图，和sharpe的直方图有点类似，大部分的alpha的fitness都在0附近，但是右边部分更多，但是集中在0.5附近，并不满足1的条件，说明analyst14的fitness是一般的。

![图片](images/img_7bb570c891.png) 
再看Long Count和Short Count的直方图，可以看到有一半的alpha的long count和short count都是小于500的，这说明analyst14这个数据集一般，可能coverage不够，大部分的回测可能会导制concentration risk。

![图片](images/img_b1aae20820.png)

![图片](images/img_c269938a3b.png)

那么总体概括一下的话，这个数据集可能会导制很多无效的回测，fitness表现不够好，long count和short count都不太符合。所以跑二阶段或者三阶段的时候，产出会比较低（不是说没有）。
你可能跑了10000个一阶段之后，就可以大概得出结论，然后马上切换另一个数据集**（及时止损）**。

## 总结

希望本贴的直方图案例可以帮助你快速筛选出更优质的数据集。
当然不局限于直方图，你甚至可以画一些其他的图来帮助筛选。

---

## 讨论与评论 (4)

### 评论 #1 (作者: SY90356, 时间: 1年前)

谢谢！感谢您得分享

---

### 评论 #2 (作者: MZ45384, 时间: 1年前)

非常有用

---

### 评论 #3 (作者: XX81632, 时间: 8个月前)

请问一下这里需要传入的是已经回测过的有各类指标的alpha，是这么理解吗，那么一个数据集下如analyst14下所有字段ID当中我需要回测多少alpha来绘图呢

---

### 评论 #4 (作者: JQ70858, 时间: 5个月前)

重新用AI写了一个代码，实现这个功能，对于小白来说，有图会更容易理解一些数据。我个人认为这是筛选数据集的很好的很高效的方法之一。但是我不懂代码，不知道如何更高效的获取某个数据集更多的字段信息，我的意思是字段的质量。希望有人帮我解答一下。谢谢分享。

---

