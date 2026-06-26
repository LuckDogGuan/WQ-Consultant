# [会议总结]GLB因子的回测技法及抛砖引玉

- **链接**: [Commented] [会议总结]GLB因子的回测技法及抛砖引玉.md
- **作者**: SY86571
- **发布时间/热度**: 9个月前, 得票: 16

## 帖子正文

2025.9.26晚10:30 小组会议讨论了 GLB MAPC 比赛中回测和提交阿尔法的方法，以及针对参会者提出的各类问题进行解答，具体如下：

- **GLB Alpha回测与提交主要是以下三个技法：**
  - **利用已提交alpha进行回测** ：将其他地区已提交阿尔法对应的相同或相似数据字段在 GLB 上重新回测并提交，可通过搜索数据字段名或描述来查找。
  - **选择回测区域：** 若觉得 GLB回测慢，可选择回测快的区域（如 USA 或AMR或别的region），回测与 Global 有相同数据字段的内容，找到阿尔法后再放到 GLB 上回测。
  - **利用Brain Lab进行回测：** 在 Brain Lab 中获取所有数据字段的 data frame，编写 group_rank 或rank 并与 returns 计算相关性，相关性高则可在平台上回测。

会议要点就以上三点,以下是一些问题的回答:

- **SA 选择问题解答** ：
  - **选择数量影响** ：选择 SA 的数量多少影响较大，越多越稳定，但关键是提交者的初衷，初衷不好提交效果就不佳。
  - **表现差异情况** ：选择数量多（如五六百个或 800 多个）与数量少（如三四百个或一两百个）表现差异不显著属正常现象。
- **GLB 字段组合问题解答** ：
  - **是否为 super Alpha** ：在 GLB 里用相同字段组合的 Alpha 不是 super Alpha，它是线性叠加，而 super Alpha 是非线性叠加。
  - **思路互换** ：提交 GLB 后可将相同数据字段拿到 ASI、Eur 等region再回测，提高多样性。
- **GLB 做 Ra 问题解答** ：
  - **地区表现不均处理** ：若 GLB 上阿尔法在三个地区中两个表现好一个表现不好，可去表现好的地区搜索该数据字段并回测提交；也可在neutralization的group condition 处下功夫，但提升效率可能不大。
  - **转换思路** ：若某地区总是弄不出好的阿尔法，可先在该地区回测找到好的阿尔法再回到 GLB 回测。
- **信号指标操作问题解答** ：
  - **加噪音操作** ：在优秀信号指标上加类似噪音的操作不可取，会降低收入，Power pool 阿尔法强调信号纯粹。
  - **不同类型阿尔法取舍** ：取舍 PC 不同的 Ra 和 PPA 时，应选择赚钱多的阿尔法，且该选择因人而异。
- **Asia news 数据集问题解答** ：
  - **业内常用方法** ：业内常见直接用 news 数据与公司涨跌幅做回归，但这种方法不适合提交 Power pool 阿尔法。
  - **解决办法** ：可降低 news 数据的频率，如用 ts_sum 结合过去一段时间或指数加权平均，使低 return 可接受。

下面是抛砖引玉环节:

针对技法1, 本人实现代码片段如下:

![图片](images/img_7aeaaaa185.png)

步骤:

1.先获取所有已提交的alpha: 代码里的ActiveAlphas, 我用的是redis做本地存储,结构保持原本json不变;

2.在IsAlphaRegularCorr中判断alpha表达式是否与当前回测region相匹配(字段是否存在与当前GLB region/delay);

3.根据配置获取MAPC2025所有中性化设置项,逐一进行设置构建新alpha加入再回测列表;

后续的回测流程与其他无异

针对技法2, 之前研究数据集及其字段, 发现维度存在region delay universe 然后就是 data category, dataset 才到datafield, 简简单单就六维, 维度之间的联系变得很难洞见, 遂考虑将之降维处理, 且称之为"二向化",实现如下:

1.通过 [https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY®ion={region}&delay={delay}&universe={universe}&limit=50&offset={offset}接口获取指定region所有数据集,存于AllDataSets,如下图:](https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY%C2%AEion={region}&delay={delay}&universe={universe}&limit=50&offset={offset}%E6%8E%A5%E5%8F%A3%E8%8E%B7%E5%8F%96%E6%8C%87%E5%AE%9Aregion%E6%89%80%E6%9C%89%E6%95%B0%E6%8D%AE%E9%9B%86,%E5%AD%98%E4%BA%8EAllDataSets,%E5%A6%82%E4%B8%8B%E5%9B%BE:)

![图片](images/img_ded3ef9c22.png)

2.通过 [https://api.worldquantbrain.com//data-fields?instrumentType='EQUITY'&region={region}&delay={delay}&universe={universe}&dataset.id={dataset_id}&limit=50&offset={offset}接口获取所有数据集及对应的所有数据字段相关信息,存于redis如上如列表所示,每个数据集信息里增加所包含的数据字段如图:](https://api.worldquantbrain.com//data-fields?instrumentType='EQUITY'&region={region}&delay={delay}&universe={universe}&dataset.id={dataset_id}&limit=50&offset={offset}%E6%8E%A5%E5%8F%A3%E8%8E%B7%E5%8F%96%E6%89%80%E6%9C%89%E6%95%B0%E6%8D%AE%E9%9B%86%E5%8F%8A%E5%AF%B9%E5%BA%94%E7%9A%84%E6%89%80%E6%9C%89%E6%95%B0%E6%8D%AE%E5%AD%97%E6%AE%B5%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF,%E5%AD%98%E4%BA%8Eredis%E5%A6%82%E4%B8%8A%E5%A6%82%E5%88%97%E8%A1%A8%E6%89%80%E7%A4%BA,%E6%AF%8F%E4%B8%AA%E6%95%B0%E6%8D%AE%E9%9B%86%E4%BF%A1%E6%81%AF%E9%87%8C%E5%A2%9E%E5%8A%A0%E6%89%80%E5%8C%85%E5%90%AB%E7%9A%84%E6%95%B0%E6%8D%AE%E5%AD%97%E6%AE%B5%E5%A6%82%E5%9B%BE:)

![图片](images/img_af2e551cba.png)

每个数据字段信息可通过 [api.worldquantbrain.com/data-fields/{datafieldid}](https://api.worldquantbrain.com/data-fields/assets) 接口获取,其中data项包含了该数据字段所有region相关信息如下图:

![图片](images/img_8696563883.png)

至此,所有数据集及字段都被二向化到了redis的一个DB里,如何实现获取同时存在于GLB ASI EUR 的所有字段呢? 以下是我的实现:

![图片](images/img_ca5f58a167.png)

当回测region是区域级别的,如GLB EUR ASI等, 设置目标region集合为['GLB', 'EUR', 'ASI'],调用get_sorted_fields_by_regions获取同时存在于目标region集合的所有字段,该方法实现如下:

```
def get_sorted_fields_by_regions(self, brain, Types=['MATRIX', 'VECTOR'], target_regions=['GLB', 'EUR', 'ASI']):        """        获取所有'MATRIX'和'VECTOR'类型字段，选取其属性data下region有'GLB'、'EUR'和'ASI'的字段        按总的pyramidMultiplier进行排序输出字段id列表        Args:            brain: 包含storageDatafieldAndOperator的redis对象        Returns:            list: 按pyramidMultiplier排序的字段id列表        """        try:            # 筛选符合条件的字段            filtered_fields = []            # 获取所有字段            cursor = 0            Cnt = 0            while True:                cursor, keys = brain.storageDatafieldAndOperator.redis.scan(cursor=cursor, match='*', count=1000)                for key in keys:                    fieldinfo = brain.storageDatafieldAndOperator.get(key)                    if not isinstance(fieldinfo, dict) or fieldinfo.get('dataset') is None or fieldinfo['type'] not in Types:                        continue                                        if not all(region in {x['region'] for x in fieldinfo['data']} for region in target_regions):                        continue                    # 计算总pyramidMultiplier                    total_pyramidMultiplier = 0                    for region in target_regions:                        for x in fieldinfo['data']:                            if x['region'] != region:                                continue                            total_pyramidMultiplier += x['pyramidMultiplier']                    # 添加到筛选列表                    filtered_fields.append({                        'id': key,                        'pyramidMultiplier': total_pyramidMultiplier                    })                Cnt += len(keys)                print(f"已处理 {Cnt} 个键...", end='\r')                if cursor == 0:                      break                 print(f"\n✅ 成功处理了 {Cnt} 个键")            # 按total_pyramidMultiplier降序排序            sorted_fields = sorted(filtered_fields, key=lambda x: x['pyramidMultiplier'], reverse=True)            # 提取排序后的字段id列表            result = [field['id'] for field in sorted_fields]            return result        except Exception as e:            print(f"❌获取排序字段失败: {str(e)}")            import traceback            Error = {"ERROR": f"❌获取排序字段失败: {str(e)}", "traceback": f"{traceback.format_exc()}"}            brain.storageError.save(f"{brain.Instance}_get_sorted_fields_by_regions", Error)            return []
```

以下是获取到的存在于三大region的字段片段:

![图片](images/img_bc19ec32b1.png)

后续就是原有的对字段进行加工回测的流程,不再赘诉

技法3待开发,以上是抛的砖头,希望能引出技法3的相关实现, 有用请点赞哦!

---

## 讨论与评论 (7)

### 评论 #1 (作者: SJ65808, 时间: 9个月前)

不亏是大佬，执行力这块没的说

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #2 (作者: SY86571, 时间: 8个月前)

还是小兵一名，佬之名担不起，因为之前就已实现，没想到确是老师提到的技法，纯属路过路过

---

### 评论 #3 (作者: SZ20589, 时间: 8个月前)

感谢大佬分享，我学会了

1. 从 USA 或 Asia 开始，快速挖掘有效 Alpha：速度要快，但要有深度，不要蜻蜓点水

2. 对有效的alpha 放在 GLB 区域再次回测：不止GLB，只要是共用字段，都有机会；

3. 运用相似字段替换的方法进行扩展： 不错的方法，建议在不同的区域使用，同一区域类似字段是同频的，高度相关；

=============================================================================

=============================== HOPE HIGH VF ==================================

=============================================================================

---

### 评论 #4 (作者: AM12075, 时间: 8个月前)

思路完整，尤其是技法1、2在实践中可行性高。建议几点：一是 `get_sorted_fields_by_regions` 可增加缓存层，减少重复scan；二是二向化过程若能存储字段与dataset的映射索引，后续跨region匹配效率会更高；三是建议技法3（Brain Lab回测）可补充范例，如以group_rank和returns计算IC的代码片段，方便参照与验证。整体结构清晰，具推广价值。

---

### 评论 #5 (作者: JX14975, 时间: 8个月前)

优秀的思路，你的代码很有实用价值。我用weijie老师的思路确实出了不少alpha，诸位同僚也可以多试试这些思路。

=============================================================================

========================== HOPE HIGH CONMBINE ===============================

=============================================================================

---

### 评论 #6 (作者: MY82844, 时间: 8个月前)

需用像EUR那样对group_cartesian_product(country, x)做group_neutralize吗

---

### 评论 #7 (作者: SY86571, 时间: 8个月前)

@ [MY82844](/hc/en-us/profiles/32294661710743-MY82844)  像EUR GLB ASI这些大区都可以优先group_cartesian_product(country, x)搞一下

---

