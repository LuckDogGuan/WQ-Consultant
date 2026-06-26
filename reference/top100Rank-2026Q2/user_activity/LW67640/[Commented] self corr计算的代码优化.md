# self corr计算的代码优化

- **链接**: [Commented] self corr计算的代码优化.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 54

## 帖子正文

感恩大佬发布了准确计算self corr的代码

经过长时间的使用, 对于自己经常需要用的功能,我也补充了一些进入到代码里面, 分享给各位朋友参考.

1.优化打印逻辑, 原先的代码里面会打印出多个corr来,实际上我更关心的是最大的corr数值,所以修改了.

2.除了最大的corr,实际上我还关心最小的corr,因为在实际情况中,有时候我们需要一下reverse,把原先的负数sharpe变为正数,所以我会看一下sharpe为负数时,最小的corr数值是多少.

参考实现如下:

```
def calc_self_corr(    alpha_id: str,    os_alpha_rets: pd.DataFrame | None = None,    os_alpha_ids: dict[str, str] | None = None,    alpha_result: dict | None = None,    return_alpha_pnls: bool = False,    alpha_pnls: pd.DataFrame | None = None) -> float | tuple[float, pd.DataFrame]:    """    计算指定 alpha 与其他 alpha 的最大自相关性。    Args:        alpha_id (str): 目标 alpha 的唯一标识符。        os_alpha_rets (pd.DataFrame | None, optional): 其他 alpha 的收益率数据，默认为 None。        os_alpha_ids (dict[str, str] | None, optional): 其他 alpha 的标识符映射，默认为 None。        alpha_result (dict | None, optional): 目标 alpha 的详细信息，默认为 None。        return_alpha_pnls (bool, optional): 是否返回 alpha 的 PnL 数据，默认为 False。        alpha_pnls (pd.DataFrame | None, optional): 目标 alpha 的 PnL 数据，默认为 None。    Returns:        float | tuple[float, pd.DataFrame]: 如果 `return_alpha_pnls` 为 False，返回最大自相关性值；            如果 `return_alpha_pnls` 为 True，返回包含最大自相关性值和 alpha PnL 数据的元组。    """    if alpha_result is None:        alpha_result = wait_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()    if alpha_pnls is not None:        if len(alpha_pnls) == 0:            alpha_pnls = None    if alpha_pnls is None:        _, alpha_pnls = get_alpha_pnls([alpha_result])        alpha_pnls = alpha_pnls[alpha_id]    alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)    alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index)>pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)]    # os_alpha_rets = os_alpha_rets.replace(0, np.nan)    # alpha_rets = alpha_rets.replace(0, np.nan)    # 找到相关性序列    correlation_series = os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets).sort_values(ascending=False).round(4)    # 获取最大的相关性数值    max_correlation = correlation_series.iloc[0]    min_correlation = correlation_series.iloc[-1]    # 打印最大的相关性数值    print('max_correlation: '+ str(max_correlation))    print('min_correlation: '+ str(min_correlation))    os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets).sort_values(ascending=False).round(4).to_csv(str(cfg.data_path / 'os_alpha_corr.csv'))    self_corr = os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets).max()    if np.isnan(self_corr):        self_corr = 0    if return_alpha_pnls:        return self_corr, alpha_pnls    else:        return self_corr
```

3.因为每次交完alpha以后,原先计算过self corr的需要进行更新,每次才能跟服务器下载PNL会花很多时间,所以我把PNL数据直接存储本地了.实现代码如下:

```
def _get_alpha_pnl(alpha_id: str) -> pd.DataFrame:    """    获取指定 alpha 的 PnL数据，并返回一个包含日期和 PnL 的 DataFrame。    此函数通过调用 WorldQuant Brain API 获取指定 alpha 的 PnL 数据，    并将其转换为 pandas DataFrame 格式，方便后续数据处理。    Args:        alpha_id (str): Alpha 的唯一标识符。    Returns:        pd.DataFrame: 包含日期和对应 PnL 数据的 DataFrame，列名为 'Date' 和 alpha_id。    """    pnl = wait_get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl").json()    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])    df = df.rename(columns={'date':'Date', 'pnl':alpha_id})    df = df[['Date', alpha_id]]    return dfdef _get_alpha_pnl(alpha_id: str) -> pd.DataFrame:    """带数据库缓存的PNL获取函数"""    # 先尝试从数据库获取    db_data = get_pnl_from_db(alpha_id)    if db_data:        pnl_dict = json.loads(db_data["pnl_data"])        df = pd.DataFrame(pnl_dict['records'],                         columns=[item['name'] for item in pnl_dict['schema']['properties']])    else:        # 从API获取        pnl = wait_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl").json()        # 存储到数据库        region = wait_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()['settings']['region']        if not save_pnl_to_db(alpha_id, region, pnl):            logging.warning(f"Failed to save PNL data for {alpha_id} to DB")               df = pd.DataFrame(pnl['records'],                         columns=[item['name'] for item in pnl['schema']['properties']])       df = df.rename(columns={'date':'Date', 'pnl':alpha_id})    return df[['Date', alpha_id]]def _get_alpha_pnl(alpha_id: str) -> pd.DataFrame:    """带数据库缓存的PNL获取函数"""    # 先尝试从数据库获取    if check_alpha_exists(alpha_id):        conn = get_db_conn()        try:            with conn.cursor() as cursor:                sql = "SELECT pnl_data FROM alpha_pnl WHERE alpha_id = %s"                cursor.execute(sql, (alpha_id,))                result = cursor.fetchone()                pnl = json.loads(result['pnl_data'])        finally:            conn.close()    else:        # 从API获取并保存到数据库        pnl = wait_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl").json()        region = wait_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()['settings']['region']        save_alpha_pnl(alpha_id, pnl, region)       # 保持原有处理逻辑不变    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])    df = df.rename(columns={'date':'Date', 'pnl':alpha_id})    return df[['Date', alpha_id]]
```

4.因为我的alpha数据也是直接存在了本地服务器,所以在打印alpha的时候,我希望能够直观地打印出alpha的表达式和sharpe,fitness等数据,针对自己的数据库数据格式,采用了打印的方式,部分代码如下:

```
def print_dict_info(data):    print("exp:")    print(data['exp'])    headers = [        'sharpe',        'fitness',        'returns',        'margin',        'turnover',        'drawdown',        'longCount',        'shortCount',        'first_datafield'    ]    values = [        data['sharpe'],        data['fitness'],        f"{data['returns'] * 100:.2f}%",        f"{data['margin'] * 10000:.2f}‱",        f"{data['turnover'] * 100:.2f}%",        f"{data['drawdown'] * 100:.2f}%",        data['longCount'],        data['shortCount'],        data['first_datafield']    ]    row = " | ".join([f"{header}: {value}" for header, value in zip(headers, values)])    print(row)
```

大概的打印内容如下:

```
Fetching alphas from offset 0 to 30新下载的alpha数量: 0, 目前总共alpha数量: 359max_correlation: 0.1373min_correlation: -0.047536e****** self_corr: 0.13729466200741886exp:#ASI_1******s1;process1 = ts_z*****************4), 22);sharpe: 5.18 | fitness: 2.61 | returns: 12.40% | margin: 5.08‱ | turnover: 48.84% | drawdown: 2.04% | longCount: 1611 | shortCount: 1616 | first_datafield: None
```

5.这部分满足相关性要求的alphaid,如果数量很多的话,我会单独打印出来,然后使用navicat进行查看.

6.有时候下载的数据量是巨大的,那么中断的情况不在少数,jupyter里面打印会有问题,导致打印界面中断.所以我在确保代码稳定运行的情况下,直接忽略了报错,使用以下代码:

```
import warningswarnings.filterwarnings('ignore')
```

7.其实还有很多可以优化的地方,比如可以直接根据alpha的sharpe大于还是小于0,来判断符合corr标准的alpha.当sharpe小于0 时,需要获取的是最小corr,而不是最大corr.但是太懒了,就没有怎么写这些新的逻辑实现.

希望以上思路能够给大家提供一点点帮助.

---

## 讨论与评论 (2)

### 评论 #1 (作者: LW67640, 时间: 1年前)

感谢分享，也感谢华子哥打好的基础，顾问必备的好工具。

在Pnl查询和比对的时候，可以增加一个统计pnl为0，或者去重的检查，可以在一定程度上检查出厂字的alpha。

-------------------------------------------

不混信号是需要有自制力的。

--------------------------------------------

---

### 评论 #2 (作者: MG88592, 时间: 1年前)

感谢小虎哥的分享，自己目前配置本地计算还存在一些问题，一直懒得去优化，下个季度得好好上心。

============================================================================
============================================================================

---

