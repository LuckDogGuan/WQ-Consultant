# 【LLM agent】构建全流程的大模型交易agent——第一步：构建数据库

- **链接**: [Commented] 【LLM agent】构建全流程的大模型交易agent第一步构建数据库.md
- **作者**: YK53163
- **发布时间/热度**: 1年前, 得票: 13

## 帖子正文

### Intro：

最近发现大模型虽然有很强的功能，能够对论文提取因子或者进行撰写表达式，但是过程过于繁琐，没有能够很好的兼容到平台的内容，比如fast expression，dataset等等。。基于此开一个小的专题，主要用来构建BRAIN的一个llm agent，开发平台采用langchain或者llamaindex都可以，如果想要简单的一点的话coze或者camel ai也可以实现（后者集成比较复杂）

### 数据集准备

首先需要准备数据集，第一个是平台上的数据，参考了一下平台给的api接口和论坛的帖子加以改进

step 1 数据表达式，下面是所有的genius给的图提取出来的数据，有些数据未来可能不可用，但是这里是为了构建数据库而准备的

```
DATA_DICT = {    "region": {        "USA": {            "universe": ["TOP3000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500"],            "category": ["analyst", "earnings", "fundamental", "imbalance", "insiders", "institutions", "macro", "model", "news", "option", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "GLB": {            "universe": ["TOP3000", "MINVOL1M"],            "category": ["analyst", "earnings", "fundamental", "macro", "model", "news", "option", "other", "price_volume", "risk", "short_interest", "social_media"]        },        "EUR": {            "universe": ["TOP1200", "TOP800", "TOP400", "ILLIQUID_MINVOL1M"],            "category": ["analyst", "earnings", "fundamental", "insiders", "institutions", "macro", "model", "news", "option", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]},        "ASI": {            "universe": ["MINVOL1M", "ILLIQUID_MINVOL1M"],            "category": ["analyst", "earnings", "fundamental", "insiders", "institutions", "model", "news", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "CHN": {            "universe": ["TOP2000U"],            "category": ["analyst", "earnings", "fundamental", "model", "news", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "KOR": {            "universe": ["TOP600"],            "category": ["analyst", "earnings", "fundamental", "insiders", "model", "option", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "TWN": {            "universe": ["TOP500", "TOP100"],            "category": ["analyst", "earnings", "fundamental", "insiders", "model", "news", "option", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "HKG": {            "universe": ["TOP800", "TOP500"],            "category": ["analyst", "earnings", "fundamental", "insiders", "model", "news", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "JPN": {            "universe": ["TOP1600", "TOP1200"],            "category": ["analyst", "earnings", "fundamental", "insiders", "institutions", "model", "news", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        },        "AMR": {            "universe": ["TOP600"],            "category": ["analyst", "earnings", "fundamental", "insiders", "institutions", "macro", "model", "news", "option", "other", "price_volume", "risk", "sentiment", "short_interest", "social_media"]        }    }}
```

step 2 提取所有的数据

```
import pandas as pddef process_datasets(region, universe, delay, category):    """    Process datasets for the given region, universe, delay, and category.    """    try:        datasets_df = get_datasets(s, region=region, delay=delay, universe=universe)        selected_datasets_df = datasets_df[            (datasets_df["delay"] ==delay) &            (datasets_df["coverage"] >0.5) & (datasets_df["coverage"] <=1) &            (datasets_df["fieldCount"] > 0) & (datasets_df["fieldCount"] < 2000) &            (datasets_df["region"] ==region) & (datasets_df["universe"] ==universe) &            (datasets_df["userCount"] >0) & (datasets_df["userCount"] <100) &            (datasets_df["valueScore"] > 1) & (datasets_df["valueScore"] < 10) &            (datasets_df["category"].apply(lambda x: x.get("id") if isinstance(x, dict) else None) == category)        ].sort_values(by=['valueScore'], ascending=False)        print(f"Region: {region}, Universe: {universe}, Delay: {delay}, Category: {category}")        print(selected_datasets_df)          global data        if 'data' not in globals():            data = []        for dataset_id in selected_datasets_df['id']:            data = get_datafields(s, dataset_id=dataset_id, region=region, universe=universe, delay=delay)            data_matrix = data[data['type'] == 'MATRIX']            data_vector = data[data['type'] == 'VECTOR']            if len(data_matrix) > 0:                matrix_fields_1 = process_datafields(data, "matrix")                data.extend(matrix_fields_1)            if len(data_vector) > 0:                vector_fields_1 = process_datafields(data, "vector")                data.extend(vector_fields_1)            print(f"Processing dataset {dataset_id}")        print(f"Total data length for Region: {region}, Universe: {universe}, Delay: {delay}, Category: {category}: {len(data)}")    except Exception as e:        print(f"Error processing datasets for Region: {region}, Universe: {universe}, Delay: {delay}, Category: {category}. Error: {e}")
```

运行

```
for region, details in DATA_DICT["region"].items():    for universe in details["universe"]:        for delay in DELAY_LIST:            for category in details["category"]:              process_datasets(region, universe, delay, category)
```

step 3 存储到数据库

```
from sqlalchemy import create_engineengine = create_engine('sqlite:///processed_data.db')  # 使用SQLite数据库def store_data_in_sql(data_df, table_name):    """    将处理后的数据存储到SQL数据库中。    """    try:        data_df.to_sql(table_name, con=engine, if_exists='append', index=False)        print(f"Data successfully inserted into {table_name} table.")    except Exception as e:        print(f"Error inserting data into SQL: {e}")
```

```
data_df = pd.DataFrame(data)table_name = "" #自己填store_data_in_sql(data_df, table_name)
```

### 

### *Final: Prompt*

考虑到这里需要写各种各样的prompt，这里先提供一个初步的选择地区的prompt，在其中需要考虑的是要把地区选择和数据集选择分开，由于fast expression对于编写非常重要，这个或作为system prompt写进里面

```
Fast Expression is a proprietary programming language used in WorldQuant BRAIN to simplify the creation and testing of financial models. It can be seen as a form of pseudocode that uses natural language and simple programming structures to express the logic of algorithms. The main features of Fast Expression include: \n\n- Block comments can be created using /*, and comments are terminated with */. The comments consist of explanatory text that helps in understanding the functionality of the code. \n- The semicolon (;) is used to separate statements, marking the end of one sentence and the beginning of another. However, the final line of code (line 13) does not require a semicolon. \n- The last statement of the entire expression is the Alpha expression used by the BRAIN simulator to compute the positions of stocks. \n- Fast Expression does not include classes, objects, pointers, or functions.\n\nAdditionally, Fast Expression allows you to select a region from the following list of options: ['USA', 'GLB', 'EUR', 'ASI', 'CHN', 'KOR', 'TWN', 'JPN', 'HKG', 'AMR'] for your financial model.
```

tbd：后续更新具体agent的方案

---

## 讨论与评论 (2)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Your article is so good, this is what I was looking for to help the research process go faster. Thank you very much.

---

### 评论 #2 (作者: DL97892, 时间: 1年前)

棒啊，佬！

---

