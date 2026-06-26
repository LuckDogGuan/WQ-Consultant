# 【全自动搜索字段】语义搜索可用字段代码优化

- **链接**: [Commented] 【全自动搜索字段】语义搜索可用字段代码优化.md
- **作者**: LA79055
- **发布时间/热度**: 1年前, 得票: 46

## 帖子正文

还在为找不到公式中的相关名称字段而担忧吗？

语义搜索它来了！ **先赞后看哦 ~**

利用金融领域预训练好的模型，输入你想要的描述，自动输出相关的字段名称！！

### 提前将WorldQuant平台的字段转为程序可读的向量数据

```
# 获得地区信息current_dir = os.getcwd()operator_datafields_dir = os.path.join(current_dir, 'OperatorAndDataFields')datafields_excel_path = os.path.join(operator_datafields_dir, 'datafields_GLB_1_TOP3000.csv')usa_analyst7_datafields = pd.read_csv(datafields_excel_path)usa_analyst7_datafields = usa_analyst7_datafields[    (usa_analyst7_datafields['type'] != 'GROUP')]usa_analyst7_datafields = usa_analyst7_datafields[usa_analyst7_datafields['coverage'] >= 0.5]usa_analyst7_datafields = usa_analyst7_datafields[usa_analyst7_datafields['userCount'] > 2]usa_analyst7_datafields = usa_analyst7_datafields[usa_analyst7_datafields['alphaCount'] > 2]usa_analyst7_datafields.reset_index(drop=True, inplace=True)model = SentenceTransformer('FinLang/finance-embeddings-investopedia')# 获取所有description内容，去除缺失值descriptions = usa_analyst7_datafields['description'].dropna().tolist()# 生成所有description的向量description_embeddings = model.encode(descriptions, show_progress_bar=True)# 保存向量到Semantic_Embeddings_Data文件夹embeddings_dir = os.path.join(current_dir, 'Semantic_Embeddings_Data')os.makedirs(embeddings_dir, exist_ok=True)embeddings_path = os.path.join(embeddings_dir, 'datafields_GLB_1_TOP3000' + '_embeddings.npy')np.save(embeddings_path, description_embeddings)print(f"已保存description_embeddings到 {embeddings_path}")
```

① 预训练模型读入：model = SentenceTransformer('FinLang/finance-embeddings-investopedia')

② 将字段描述丢入预训练模型中获取特征向量：description_embeddings = model.encode(descriptions, show_progress_bar=True)

③ 保存字段向量以便随时读出：np.save(embeddings_path, description_embeddings)

### 搜索高关联字段

以 sentiment 和 volatility 为例搜索高关联字段。

```
sentences = ["sentiment", "volatility"]sentence_embeddings = model.encode(sentences)# 获取前10个最相似的描述top_n = 10      # 筛选多少个近似描述 idalpha = 0.7     # 相似度评分占比beta = 0.5      # 关键词覆盖率评分占比all_top_ids = []all_top_descriptions = []# ... existing code ...for idx, (sentence, sent_emb) in enumerate(zip(sentences, sentence_embeddings)):    # 计算近似度    similarities = cosine_similarity([sent_emb], description_embeddings)[0]    query_words = set(sentence.lower().split())    coverage_scores = [len(query_words & desc_words) / len(query_words) for desc_words in desc_words_list]    # 计算相似度和关键字最终得分    final_scores = alpha * similarities + beta * np.array(coverage_scores)    # 针对 dataset.id 包含 fundamental 的行加分    fundamental_bonus = (usa_analyst7_datafields['dataset.id'].astype(str) == 'fundamental6').astype(float) * 0.2    pv_bonus = (usa_analyst7_datafields['dataset.id'].astype(str) == 'pv1').astype(float) * 0.2    final_scores += fundamental_bonus.values + pv_bonus    # 根据最终得分筛选出前 top_n 的字段    top_indices = final_scores.argsort()[-top_n:][::-1]    description_index = usa_analyst7_datafields['description'].dropna().index    # 获取最相似的id和描述    top_ids = usa_analyst7_datafields.loc[description_index[top_indices], 'id'].tolist()    top_descriptions = usa_analyst7_datafields.loc[description_index[top_indices], 'description'].tolist()    # 保留每个重复描述最多2个，同时同步top_ids    desc_count = {}    filtered_top_descriptions = []    filtered_top_ids = []    for id, desc in zip(top_ids, top_descriptions):        desc_count[desc] = desc_count.get(desc, 0) + 1        # 如果描述出现次数小于等于2，则保留        if desc_count[desc] <= 2:            filtered_top_descriptions.append(desc)            filtered_top_ids.append(id)    top_descriptions = filtered_top_descriptions    top_ids = filtered_top_ids    all_top_ids.append(top_ids)    all_top_descriptions.append(top_descriptions)    print(f"\n句子：{sentence}")    for id, desc in zip(top_ids, top_descriptions):        print(f"最相似的id：{id}，描述：{desc}")
```

① 计算余弦相似度：

```
similarities = cosine_similarity([sent_emb], description_embeddings)[0]
```

② 计算关键词覆盖率：

```
coverage_scores = [len(query_words & desc_words) / len(query_words) for desc_words in desc_words_list]
```

③ 给基础字段增加权重：

```
fundamental_bonus = (usa_analyst7_datafields['dataset.id'].astype(str) == 'fundamental6').astype(float) * 0.2
```

针对 sentiment 和 volatility 的输出结果如下。

![图片](images/img_07d370e8bd.png)

---

## 讨论与评论 (2)

### 评论 #1 (作者: KZ79256, 时间: 1年前)

看这查询貌似是当个单词,如果是两个不想关单词的话,能不能解决哇

---

### 评论 #2 (作者: LA79055, 时间: 1年前)

[KZ79256](/hc/en-us/profiles/13609593802263-KZ79256)

针对你的提问，我认为我当前提出的语义搜索模型更多的是给大家一个启发性的效果。至于能否搜索两个不相同但语义近似的单词，我认为是可以的，因为金融模型是提前训练好的，因此近似的金融单词应当有近似的词向量产生，但是当前代码筛选的效果是不够的。仍然需要通过一些统计学以及可视化手段观察是否有数值近似的词向量产生，以及如何将这些词向量筛选出来。

---

