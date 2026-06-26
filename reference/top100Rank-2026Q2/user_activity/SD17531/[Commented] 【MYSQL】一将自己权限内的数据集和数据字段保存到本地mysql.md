# 【MYSQL】（一）将自己权限内的数据集和数据字段保存到本地mysql

- **链接**: [Commented] 【MYSQL】一将自己权限内的数据集和数据字段保存到本地mysql.md
- **作者**: JG15244
- **发布时间/热度**: 1年前, 得票: 8

## 帖子正文

> 这篇帖子主打一个开箱即用，复制建表语句执行后，直接执行对应的方法即可
> 之前在论坛里也借鉴过很多大佬的方法，但有些地方因为配置不同所以会有问题
> 这里已经将每个模块尽可能的独立出来了

## 1. 保存自己权限内的数据集datasets

### （1）数据集表

这里的保存逻辑是id、region、delay、universe按一条数据来算。

```
CREATE TABLE `datasets` (  `id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'id',  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'name',  `description` text COLLATE utf8_unicode_ci COMMENT '详细描述',  `category` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '类别',  `subcategory` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '子类别',  `region` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'region',  `delay` int(11) DEFAULT NULL COMMENT 'delay',  `universe` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'universe',  `coverage` double DEFAULT NULL COMMENT '覆盖率',  `valueScore` double DEFAULT NULL COMMENT '价值分',  `userCount` int(11) DEFAULT NULL COMMENT '用户数量',  `alphaCount` int(11) DEFAULT NULL COMMENT 'Alpha 数量',  `fieldCount` int(11) DEFAULT NULL COMMENT '字段数量',  `pyramidMultiplier` double DEFAULT NULL COMMENT 'pyramid 倍数',  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间，自动更新',  UNIQUE KEY `idx_unique_dataset` (`id`,`region`,`delay`,`universe`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='数据集';
```

### （2）保存方法

```
region_values = ["USA", "GLB", "EUR", "ASI"]delay_values = {    "USA": [0, 1],    "GLB": [1],    "EUR": [0, 1],    "ASI": [1]}universe_values = {    "USA": ["TOP3000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500"],    "GLB": ["TOP3000", "MINVOL1M"],    "EUR": ["TOP1200", "TOP800", "TOP400", "ILLIQUID_MINVOL1M"],    "ASI": ["MINVOL1M", "ILLIQUID_MINVOL1M"]}DB_CONFIG = {    'host': '',    'user': '',    'password': '',    'database': '',    'charset': 'utf8'}def save_datasets():    url = "https://api.worldquantbrain.com/data-sets"    connection = pymysql.connect(**DB_CONFIG)    cursor = connection.cursor()    total_num = 0    for region in region_values:        for delay in delay_values[region]:            for universe in universe_values[region]:                params = {                    "region": region,                    "delay": delay,                    "universe": universe,                    "instrumentType": "EQUITY",                }                response = s.get(url, params=params)                data = response.json().get('results', [])                if not data:                    continue                for item in data:                    id = item.get('id')                    name = item.get('name')                    description = item.get('description')                    category_id = item.get('category', {}).get('id')                    subcategory_id = item.get('subcategory', {}).get('id')                    region = item.get('region')                    delay = item.get('delay')                    universe = item.get('universe')                    coverage = item.get('coverage')                    value_score = item.get('valueScore')                    user_count = item.get('userCount')                    alpha_count = item.get('alphaCount')                    field_count = item.get('fieldCount')                    pyramid_multiplier = item.get('pyramidMultiplier')                    sql = """                    INSERT INTO datasets (                        id, name, description, category, subcategory, region, delay, universe,                         coverage, valueScore, userCount, alphaCount, fieldCount, pyramidMultiplier                    ) VALUES (                        %s, %s, %s, %s, %s, %s, %s, %s,                         %s, %s, %s, %s, %s, %s                    )                    ON DUPLICATE KEY UPDATE                         name = VALUES(name),                        description = VALUES(description),                        category = VALUES(category),                        subcategory = VALUES(subcategory),                        region = VALUES(region),                        delay = VALUES(delay),                        universe = VALUES(universe),                        coverage = VALUES(coverage),                        valueScore = VALUES(valueScore),                        userCount = VALUES(userCount),                        alphaCount = VALUES(alphaCount),                        fieldCount = VALUES(fieldCount),                        pyramidMultiplier = VALUES(pyramidMultiplier)                    """                    cursor.execute(sql, (                        id, name, description, category_id, subcategory_id, region, delay, universe,                         coverage, value_score, user_count, alpha_count, field_count, pyramid_multiplier                    ))                connection.commit()                print(f"成功保存{region} {delay} {universe}的数据集: {len(data)}条")                total_num += len(data)    cursor.close()    connection.close()    print(f"共保存 {total_num} 条数据集")
```

### （3）自行根据json扩展

```
{  "count": 52,  "results": [    {      "id": "analyst11",      "name": "ESG scores",      "description": "Environmental Social Governance scores that exhibit significance with respect to financial metrics - different scores according to grouping and weighing.",      "category": { "id": "analyst", "name": "Analyst" },      "subcategory": { "id": "analyst-esg", "name": "ESG" },      "region": "USA",      "delay": 0,      "universe": "TOP3000",      "coverage": 0.6818,      "valueScore": 3.0,      "userCount": 11,      "alphaCount": 17,      "fieldCount": 197,      "pyramidMultiplier": 1.7,      "themes": [],      "researchPapers": [        {          "type": "discussion",          "title": "Getting started with Analyst Datasets",          "url": "../CC40930/[Commented] Getting started with Analyst DatasetsResearch.md"        }      ]    },    ...    ...  ]}
```

## 2. 保存自己权限内的数据字段data_fields

### （1）数据字段表

保存逻辑同数据集表

```
CREATE TABLE `datafields` (  `id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '主键 ID',  `description` text COLLATE utf8_unicode_ci COMMENT 'KPI 描述',  `dataset` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '数据集 ID',  `category` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '类别 ID',  `subcategory` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '子类别 ID',  `region` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'region',  `delay` int(11) DEFAULT NULL COMMENT 'delay',  `universe` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'universe',  `type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '矩阵类型',  `coverage` double DEFAULT NULL COMMENT '覆盖率',  `user_count` int(11) DEFAULT NULL COMMENT '用户数量',  `alpha_count` int(11) DEFAULT NULL COMMENT 'Alpha 数量',  `pyramid_multiplier` double DEFAULT NULL COMMENT 'pyramid 倍数',  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间，自动更新',  UNIQUE KEY `idx_unique_dataset` (`id`,`region`,`delay`,`universe`,`dataset`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='字段表';
```

### （2）保存方法

```
def save_data_fields():    url = "https://api.worldquantbrain.com/data-fields"    connection = pymysql.connect(**DB_CONFIG)    cursor = connection.cursor()    total_num = 0    sql_query = """        SELECT id, region, delay, universe        FROM datasets;    """    cursor.execute(sql_query)    results = cursor.fetchall()    for row in results:        params = {            "dataset.id": row[0],      # Dataset ID            "region": row[1],          # Region            "delay": row[2],           # Delay            "universe": row[3],        # Universe            "instrumentType": "EQUITY",  # 固定值            "limit": 50,               # 固定值            "offset": 0                # 固定值        }        count = s.get(url, params=params).json()['count']        for offset in range(0, count, 50):            params['offset'] = offset            response = s.get(url, params=params)            data = response.json().get('results', [])            if not data:                continue            batch_values = []            for item in data:                batch_values.append((                    item.get('id'),                    item.get('description'),                    item.get('dataset', {}).get('id'),                    item.get('category', {}).get('id'),                    item.get('subcategory', {}).get('id'),                    item.get('region'),                    item.get('delay'),                    item.get('universe'),                    item.get('type'),                    item.get('coverage'),                    item.get('userCount'),                    item.get('alphaCount'),                    item.get('pyramidMultiplier')                ))            sql = """                INSERT INTO datafields (                    id, description, dataset, category, subcategory,                     region, delay, universe, type, coverage, user_count,                     alpha_count, pyramid_multiplier                ) VALUES (                    %s, %s, %s, %s, %s,                     %s, %s, %s, %s, %s, %s,                     %s, %s                )                ON DUPLICATE KEY UPDATE                    description = VALUES(description),                    dataset = VALUES(dataset),                    category = VALUES(category),                    subcategory = VALUES(subcategory),                    region = VALUES(region),                    delay = VALUES(delay),                    universe = VALUES(universe),                    type = VALUES(type),                    coverage = VALUES(coverage),                    user_count = VALUES(user_count),                    alpha_count = VALUES(alpha_count),                    pyramid_multiplier = VALUES(pyramid_multiplier);            """            cursor.executemany(sql, batch_values)            connection.commit()            total_num += count        print(f"成功保存{params['dataset.id']} {params['region']} {params['delay']} {params['universe']}的数据字段: {count}条")    cursor.close()    connection.close()    print(f"共保存 {total_num} 条数据字段")
```

### （3）自行根据json扩展

```
{  "count": 197,  "results": [    {      "id": "anl11_1e",      "description": "Aggregate KPI for Pollution Prevention & Environmental Remediation",      "dataset": { "id": "analyst11", "name": "ESG scores" },      "category": { "id": "analyst", "name": "Analyst" },      "subcategory": { "id": "analyst-esg", "name": "ESG" },      "region": "USA",      "delay": 0,      "universe": "TOP3000",      "type": "MATRIX",      "coverage": 0.6396,      "userCount": 1,      "alphaCount": 1,      "pyramidMultiplier": 1.7,      "themes": []    },    ...    ...  ]}
```

> 后续计划：
> 目标：开箱可用，每隔功能模块尽可能独立。
> IMPORTANT：
> 1. 优化顾问的一二三阶模板，这会将全部代码最后放到最后一篇帖子中。
> 2. 构建模板填充模板：将自己的alpha模板已经需要遍历的数据集或字段填充好，程序将自行运行。
> POINT：
> 1. 定时任务，保证云服务器上账号始终保持登录状态。
> 2. 独立的check方法，24小时不停的check新提交过的alpha已经已经check过的alpha，并将其结果保存到mysql数据库中。
> 3. 优化 multi_simulate 方法，暂时想的是多线程提交以及保存提交记录。
> 4. 消息推送：报错推送、任务完成（simulate、check）推送。
> 5. AI 方面还在研究...

---

## 讨论与评论 (3)

### 评论 #1 (作者: SD17531, 时间: 1年前)

感谢大佬的代码,已经按照您的代码下载所有datafields到本地数据库.

顺便分享一下遇到的问题和解决的思路:

1.两个函数都需要复制到自己的代码里面,两个建表语句需要先执行.

2.需要先试用wqb或者machine_lib的login()获取session,然后赋值slogin()之类的.

3.下载datasets的数据量不大,不担心遇到网络波动之类的问题.但是下载datafields有几十万条数据,需要一两小时的时间,所以网络不是很稳定的情况下,建议把index打出来或者其他处理方式.我下载过程中中断了,处理了一下传入的列表,进行续下载.一个简单的思路如下:

```
def save_data_fields():    url = "https://api.worldquantbrain.com/data-fields"    connection = pymysql.connect(**DB_CONFIG)    cursor = connection.cursor()    total_num = 0    sql_query = """        SELECT id, region, delay, universe        FROM datasets;    """    cursor.execute(sql_query)    results = cursor.fetchall()    # for index,row in enumerate(results):      # 这里可以根据你已经下载好最后一个dataset_id来定位你的整个results需要从哪里开始下载    #     if 'pv30' == row[0]:    #         print(index)    #         break           for row in results[1342:]:         # 我这里是重新从results的第1342个元素开始下载        params = {            "dataset.id": row[0],      # Dataset ID            "region": row[1],          # Region            "delay": row[2],           # Delay            "universe": row[3],        # Universe            "instrumentType": "EQUITY",  # 固定值            "limit": 50,               # 固定值            "offset": 0                # 固定值        }
```

4.下载完的数据如下: ![图片](images/img_3206a6b4c4.png)

---

### 评论 #2 (作者: CG48008, 时间: 1年前)

大佬的代码好用，容易上手。将全部的fields爬下来可以做很多事，比如搭建自己的rag知识库，或许可以找到有信号的alpha

---

### 评论 #3 (作者: WS55742, 时间: 1年前)

非常感谢！很有帮助！谢谢！

---

