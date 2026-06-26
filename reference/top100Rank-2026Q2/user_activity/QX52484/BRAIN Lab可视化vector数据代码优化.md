# BRAIN Lab可视化vector数据代码优化

- **链接**: BRAIN Lab可视化vector数据代码优化.md
- **作者**: QX52484
- **发布时间/热度**: 11个月前, 得票: 54

## 帖子正文

周知,lab中通过修改可以直接查看anl14_actvalue_ebit_fp0 这样的matridx数据。
但如果改为vector数据会导致报错。
因为vector数据是三维的，不能直接通过lab中的visualizations.plot绘制二维图像。
lab中的使用的visualizations.plot系列应该是lab平台中自定义封装的函数。
因此在尽量少改动的情况下，将vector数据转变为matridx数据即可进行查看。
处理思路参考wqb平台的vec_avg vec_max等操作符即可。
下为参考代码: (lab网页不能CV外部代码，推荐使用utools等软件截图悬浮功能或放副屏进行手
敲)
 ![图片](images/img_614263d9e8.png)

实操结果如下：

![图片](images/img_10845f2ecc.png)

---

## 讨论与评论 (11)

### 评论 #1 (作者: JZ81222, 时间: 11个月前)

但是brain lab用起来真的好慢 怎么样能够快一点

---

### 评论 #2 (作者: CW62372, 时间: 11个月前)

这是单只股票的图像对吗

---

### 评论 #3 (作者: WF37935, 时间: 11个月前)

```
# vector求和df.map(lambda x: np.sum(x) if isinstance(x, np.ndarray) else x)# vector求均值df.map(lambda x: np.mean(x) if isinstance(x, np.ndarray) else x)# vector求个数df.map(lambda x: len(x) if isinstance(x, np.ndarray) else x)
```

---

### 评论 #4 (作者: LW17399, 时间: 11个月前)

正好我也遇到这个问题了，谢谢分享！

---

### 评论 #5 (作者: CM48632, 时间: 11个月前)

这个链接  [../JL16510/[Commented] 向BRAIN Labs里粘贴代码的一个方法代码优化.md](../JL16510/[Commented] 向BRAIN Labs里粘贴代码的一个方法代码优化.md)  可以不用手敲

---

### 评论 #6 (作者: QX52484, 时间: 11个月前)

[CM48632](/hc/en-us/profiles/29138831896343-CM48632)

感谢分享，学习到了

今天看到了WW31730大佬的分享 也放在这里

有段代码可以参考，集成了wq的operator

# Robust vector flattener
def flatten_vector(x):
    if isinstance(x, (list, np.ndarray)):
        return np.ravel(x).tolist()
    if pd.isna(x):
        return []
    return []

# All vector functions
def vec_avg(x):
    x = flatten_vector(x)
    return np.mean(x) if x else np.nan

def vec_sum(x):
    x = flatten_vector(x)
    return np.sum(x)

def vec_max(x):
    x = flatten_vector(x)
    return max(x) if x else np.nan

def vec_min(x):
    x = flatten_vector(x)
    return min(x) if x else np.nan

def vec_range(x):
    x = flatten_vector(x)
    return max(x) - min(x) if x else np.nan

def vec_count(x):
    x = flatten_vector(x)
    return len(x)

def vec_skewness(x):
    x = flatten_vector(x)
    if len(x) < 3:
        return np.nan
    x = np.array(x)
    std = np.std(x)
    return np.mean(((x - np.mean(x)) / std) ** 3) if std != 0 else 0

def vec_kurtosis(x):
    x = flatten_vector(x)
    if len(x) < 4:
        return np.nan
    x = np.array(x)
    std = np.std(x)
    return np.mean(((x - np.mean(x)) / std) ** 4) - 3 if std != 0 else -3

# Mapping of function names
vec_ops = {
    'vec_avg': vec_avg,
    'vec_sum': vec_sum,
    'vec_max': vec_max,
    'vec_min': vec_min,
    'vec_range': vec_range,
    'vec_count': vec_count,
    'vec_skewness': vec_skewness,
    'vec_kurtosis': vec_kurtosis
}

# Main function
def df_vector_stat(df, func_name):
    """
    Apply a vector operation to each column of a DataFrame where each cell is a list.

Args:
        df (pd.DataFrame): DataFrame with list-like cells
        func_name (str): Vector operation name, e.g., 'vec_sum'

Returns:
        pd.DataFrame: A new DataFrame with one column per original column
    """
    if func_name not in vec_ops:
        raise ValueError(f"Unsupported function: {func_name}. Choose from: {list(vec_ops.keys())}")

    func = vec_ops[func_name]

    result_df = df.apply(lambda col: col.map(func))
    result_df.columns = [f"{col}_{func_name}" for col in df.columns]
    return result_df

---

### 评论 #7 (作者: QX52484, 时间: 11个月前)

[JZ81222](/hc/en-us/profiles/30476699099159-JZ81222)

据说用新加坡的节点访问会好一点，lab界面卡的话。。按老师的说法就只能忍忍了，也不常用。

---

### 评论 #8 (作者: QX52484, 时间: 11个月前)

[CW62372](/hc/en-us/profiles/28847429562135-CW62372)

是的，单只股票的。

可以参考learn中的内容

Vector类型数据集是一种不固定大小的数据字段类型。在这种类型的数据字段中，每个金融工具每天记录的事件数量不同，因此它们通常存储在vector中。一个vector字段在一天内报告单个金融工具的多个新闻事件。

scl15_d1_sentiment是一个字段，它给出了一天内各种事件的情绪得分。由于我们每个金融工具只能采取一个头寸，因此作为输入，我们只需要一个情绪值。对于AAPL的某个日期，如果有5个情绪得分，我们只需使用所有这些得分的平均值，通常可以合理地代表该整天的情绪。因此，为将此情绪向量转换为矩阵字段，我们将使用vec_avg（scl15_d1_sentiment）。如果您认为中位数可能是更好的代表，则可以使用vec_median（scl15_d1_sentiment）代替。下面再次是vec_avg字段的平均值和换手率图。平均值密集地在15,000左右，换手率在130％左右。在此处，您也需要使用ts_rank或ts_decay降低换手率，以在Alpha表达式中使用它.

---

### 评论 #9 (作者: WS46709, 时间: 11个月前)

谢谢分享！

---

### 评论 #10 (作者: CG34705, 时间: 11个月前)

你好，请问用这个方法可以看到分组数据图吗，如果可以请问具体怎么做到呢？我尝试了你的方法，成功看到了分布图，但是试图看分组图却报了以下错误：
no artists with labels found to put in legend, not that artists whoes label start with an underscore are ignored when legend() is called with no argument. plt.legend(title="Groups) ，这是为什么呢？

---

### 评论 #11 (作者: SW66069, 时间: 11个月前)

感谢分享，受益颇多！

---

