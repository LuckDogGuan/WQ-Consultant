# 【Lab使用经验】查看Vector类型数据：取均值及判断更新频率代码优化

- **链接**: [Commented] 【Lab使用经验】查看Vector类型数据取均值及判断更新频率代码优化.md
- **作者**: LL87164
- **发布时间/热度**: 11个月前, 得票: 10

## 帖子正文

**Vector** 类型数据字段在Lab里显示如下： ![图片](images/img_ce43b3d923.png)

取一个样本判断其类型： **numpy.ndarray**

![图片](images/img_c13805529a.png)

判断类型是为了下一步取均值的操作

采用类似平台的Vector操作符来取 **均值** ：

![图片](images/img_c41fdb0747.png)

注：应该使用  **np.nanmean**  函数来对 Vector 字段取均值，避免列表中有一个 NaN 时返回值是 NaN。

更新频率图示及代码参见另一个帖子里的评论： [https://support.worldquantbrain.com/hc/en-us/community/posts/33247252289943/comments/33263818275607](/hc/en-us/community/posts/33247252289943/comments/33263818275607)

备注：

1. 图中使用的字段  `anl44_2_epsr_value`  代表 "reported earnings per share"（报告每股收益）。

---

## 讨论与评论 (5)

### 评论 #1 (作者: YQ51506, 时间: 1年前)

因为 vector字段元素这里是个列表，因此我是以这个列表为基础，取出其最大值，最小值，均值等，进行处理，构建为matrix的dataframe格式，实现了vector_operator的效果，不知道准不准确

---

### 评论 #2 (作者: LL87164, 时间: 11个月前)

[YQ51506](/hc/en-us/profiles/27706511330455-YQ51506)

**Vector** 数据字段是数组： **numpy.ndarray。** 用python函数 np.nanmean(arr) 取均值，避免列表中有一个 NaN 时返回值是 NaN。

---

### 评论 #3 (作者: FZ60707, 时间: 1年前)

感谢大佬分享，正愁着vector数据看不了呢，一直报错

---

### 评论 #4 (作者: YW93864, 时间: 1年前)

我记得可以使用dataframe的.map操作，比如取均值df.map(np.nanmean)

=======================================================================================================================================================================

---

### 评论 #5 (作者: LL87164, 时间: 11个月前)

[YW93864](/hc/en-us/profiles/14096946892439-YW93864)

不好意思，没及时回复。多谢提醒！您说的对，应该是用这个 np.nanmean。也是最近才发现： Vector 字段的列表里如果有一个是 NaN，用标准函数的话返回的也是 NaN。已更新正文中截屏内容。

补充两组函数的对比：

标准函数
功能
nan-Safe 版本

np.max()
最大值
np.nanmax()

np.min()
最小值
np.nanmin()

np.quantile()
分位数
np.nanquantile()

np.percentile()
百分位数
np.nanpercentile()

np.sum()
求和
np.nansum()

np.std()
标准差
np.nanstd()

---

