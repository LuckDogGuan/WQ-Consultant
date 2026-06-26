# 【构建自己的代码框架系列】第01篇--用MySQL完美保存全部回测过的alpha

- **链接**: [Commented] 【构建自己的代码框架系列】第01篇--用MySQL完美保存全部回测过的alpha.md
- **作者**: XM75236
- **发布时间/热度**: 1年前, 得票: 22

## 帖子正文

### 一.原有痛点

1.网页端速度慢,灵活性差,字段不全或不可自定义(比如看最后两年sharpe或low_2_year_shape等),不便筛选

2.一二三阶段那种跑批同时进行的时候,最好打tag,api打tag影响回测速率

3.alpha之间互相对比困难,例如来自相同核心field的筛选问题

### 二.解决方案

使用数据库,本方案采用的结构化数据库MySQL,也有同学使用的Mongo等非结构化的,这个我抛砖引玉,欢迎讨论

我这边独特的字段如下

1.tags,自己打标签.multi_simulate的时候,可以获取到progress_urls,把这些url和应该打的标签在代码中存起来推到redis中,另起一个任务专门负责根据这些url获取其alpha的id,进而和tag建立关系,再转存到MySQL中

2.check_status.接口获取信息到的check信息中,存在fail的,这个字段就为fail,否则就是pending,只有pending的alpha才需要后面check

3.low_2y_sharpe.这个字段是single的dataset独有,能获取到就赋值,获取不到就补1.不是补0,因为为0的需要将check_status变为fail

4.is_ladder_sharpe,不是single的dataset,则有这个字段,同样的,能获取到就赋值,获取不到就补1.不是补0,因为为0的需要将check_status变为fail

5.is_submit.记录是否提交的信息.0未提交,1已提交.值得注意的是,这个字段还能解决如何科学存货.按自己的提交标准,check完以后把is_submit字段赋值为2-10之间的数值.比如我,2为优秀10为垃圾,中间酌情.

### 三.核心代码

api代码在下一条评论,这里似乎放不下

MySQL表结构如下:

-- worldquant.alpha_data definition

CREATE TABLE `alpha_data` (

`id` varchar(10) NOT NULL DEFAULT '',

`exp` varchar(2000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,

`original_field` varchar(100) DEFAULT NULL,

`dateCreated` datetime DEFAULT NULL,

`region` varchar(10) DEFAULT NULL,

`universe` varchar(50) DEFAULT NULL,

`sharpe` float DEFAULT NULL,

`fitness` float DEFAULT NULL,

`turnover` float DEFAULT NULL,

`longCount` int DEFAULT NULL,

`shortCount` int DEFAULT NULL,

`returns` float DEFAULT NULL,

`drawdown` float DEFAULT NULL,

`margin` float DEFAULT NULL,

`delay` int DEFAULT NULL,

`decay` int DEFAULT NULL,

`neutralization` varchar(20) DEFAULT NULL,

`truncation` float DEFAULT NULL,

`pasteurization` varchar(10) DEFAULT NULL,

`unitHandling` varchar(10) DEFAULT NULL,

`visualization` varchar(10) DEFAULT NULL,

`tags` varchar(100) DEFAULT NULL,

`check_status` varchar(20) DEFAULT NULL,

`is_submit` tinyint DEFAULT NULL,

`low_2y_sharpe` float DEFAULT NULL,

`is_ladder_sharpe` float DEFAULT NULL,

PRIMARY KEY (`id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

ARSET=utf8mb3;

---

## 讨论与评论 (8)

### 评论 #1 (作者: XM75236, 时间: 1年前)

def alpha_info_to_mysql():    
    s = login()
    from datetime import datetime, timedelta

    # 从MySQL获取最近的一次获取时间
    with pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_db, charset='utf8') as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT log_value FROM worldquant.logs WHERE log_type='get_alpha_info' LIMIT 1")
            date_begin = cursor.fetchone()[0]

all_field_list = {}
    for table_name in table_names:
        region  = table_name.split('_')[0]      
        # 从worldquant.ASI_DELAY1里面获取所有的field值变成list存为field_list
        with pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_db, charset='utf8') as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT field FROM worldquant.{region}_DELAY1")
                field_list = [i[0] for i in cursor.fetchall()]
                all_field_list[region] = field_list

# 从api获取alpha的信息
    base_url = " [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) "
    total_count = 0
    ids = []
    with pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_db, charset='utf8') as conn:
        # 从上次获取时间开始,每次获取1小时的数据,直到当前时间
        # date_now = datetime.now(pytz.utc) 这个带了毫秒,不好用,死循环,使得date_begin_dt永远小于date_now
        date_now = datetime.now().replace(microsecond=0).astimezone(pytz.utc)
        while True:
            date_begin_dt = datetime.fromisoformat(date_begin).astimezone(pytz.utc)
            # print(f"date_begin_dt: {date_begin_dt}")
            # print(f"date_now: {date_now}")
            # 打印北京时间
            cst_timezone = pytz.timezone('Asia/Shanghai')
            print(f"date_begin: {date_begin_dt.astimezone(cst_timezone)}")
            print(f"date_now: {date_now.astimezone(cst_timezone)}")
            if date_begin_dt >= date_now:
                break
            # 结束时间为开始时间+1小时,且为北京时间格式
            date_end = (datetime.fromisoformat(date_begin) + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S+08:00')

            print(f"Getting data from {date_begin} to {date_end}")
            # 参数
            params = {
                "limit": 100,  # 每页100个,这是接口允许的最大值
                "dateCreated>": date_begin,
                "dateCreated<": date_end,
                "order": "dateCreated",  # 日期排序,按创建日期最早->最晚
            }
            count = s.get(base_url, params=params).json()['count']
            print(f"count: {count}")
            total_count += count
            # count值类似有2000个alpha,每页100个,则有20页,咱们挨个提取
            for offset in range(0, count, 100):  # 从0开始,每次提取100个
                # params中增加offset参数,每次提取100个
                params['offset'] = offset
                results = s.get(base_url, params=params).json()["results"]
                for result in results:
                    id = result['id']
                    if 'regular' in result:
                        exp = result['regular']['code']
                    else:
                        continue

                    ids.append(id)
                    settings = result['settings']

                    # 时间格式需要转换,因为数据库中的时间格式是datetime
                    dateCreatedTmp = result['dateCreated']
                    dateCreated_dt = datetime.fromisoformat(dateCreatedTmp).astimezone(pytz.utc) # 这是UTC时间,时间格式
                    dateCreated = (dateCreated_dt + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') # 转换为北京时间,字符串格式

                    # 以下是alpha的模拟数据
                    alpha_info = result['is']
                    longCount = alpha_info['longCount']
                    shortCount = alpha_info['shortCount']
                    turnover = alpha_info['turnover']
                    returns = alpha_info['returns']
                    drawdown = alpha_info['drawdown']
                    margin = alpha_info['margin']
                    fitness = alpha_info['fitness']
                    if (fitness is None) or (fitness == 'null') or (fitness == 'None'):
                        fitness = 0
                    sharpe = alpha_info['sharpe']

                    # 以下是alpha的配置信息
                    region = settings['region']
                    universe = settings['universe']
                    delay = settings['delay']
                    decay = settings['decay']
                    neutralization = settings['neutralization']
                    truncation = settings['truncation']
                    pasteurization = settings['pasteurization']
                    unitHandling = settings['unitHandling']
                    visualization = settings['visualization']

# 从all_field_list中找到exp这个长字符串包含的field
                    field_list = all_field_list[region]
                    matches = [field for field in field_list if field in exp]
                    if matches:
                        original_field = max(matches, key=len)
                        if f"-ts" in exp:
                            original_field = f"-{original_field}"
                    else:
                        original_field = None  # 或者处理没有匹配的情况

                    checks = result['is']['checks']
                    # 如果checks的任意一个子元素的result值为FAIL,则check的值就是FAIL,如果不是，还需要判定sharpe_2022
                    if any([c['result'] == 'FAIL' for c in checks]):
                        check_status = 'FAIL'
                    else:
                        sharpe_2022 = get_sharpe_2022(s, id)
                        if sharpe_2022 is None:
                            check_status = 'PENDING'
                        elif sharpe_2022 < 1:
                            check_status = 'FAIL'
                        else:
                            check_status = 'PENDING'
                    # 获取low_2y_sharpe值,为0的没有后续处理的必要
                    for item in checks:
                        if item['name'] == 'LOW_2Y_SHARPE':
                            low_2y_sharpe = item['value']
                            break
                    else:
                        low_2y_sharpe = 1  # 如果没有找到(有时候前面fail以后这个就没有),则默认为1 TODO: 这个值需要确认
                    # 获取is_ladder_sharpe，为0的没有后续处理的必要
                    for item in checks:
                        if item['name'] == 'IS_LADDER_SHARPE':
                            is_ladder_sharpe = item.get('value', 1)
                            break
                    else:
                        is_ladder_sharpe = 1  # 如果没有找到(有时候前面fail以后这个就没有),则默认1 TODO: 这个值需要确认

                    sql = """
                        INSERT INTO worldquant.alpha_data (
                            id, dateCreated, longCount, shortCount, turnover,
                            returns, drawdown, margin, fitness, sharpe,
                            region, universe, delay, decay, neutralization,
                            truncation, pasteurization, unitHandling, visualization,exp,
                            check_status, original_field, low_2y_sharpe, is_ladder_sharpe
                        ) VALUES (
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s
                        )
                        ON DUPLICATE KEY UPDATE
                            dateCreated=%s, longCount=%s, shortCount=%s, turnover=%s,
                            returns=%s, drawdown=%s, margin=%s, fitness=%s, sharpe=%s,
                            region=%s, universe=%s, delay=%s, decay=%s, neutralization=%s,
                            truncation=%s, pasteurization=%s, unitHandling=%s, visualization=%s,exp=%s,
                            check_status=%s, original_field=%s, low_2y_sharpe=%s, is_ladder_sharpe=%s
                    """
                    sql_params = (
                        id, dateCreated, longCount, shortCount, turnover,
                        returns, drawdown, margin, fitness, sharpe,
                        region, universe, delay, decay, neutralization,
                        truncation, pasteurization, unitHandling, visualization,exp,
                        check_status, original_field, low_2y_sharpe, is_ladder_sharpe,

                        dateCreated, longCount, shortCount, turnover,
                        returns, drawdown, margin, fitness, sharpe,
                        region, universe, delay, decay, neutralization,
                        truncation, pasteurization, unitHandling, visualization,exp,
                        check_status, original_field, low_2y_sharpe, is_ladder_sharpe,
                    )
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(sql, sql_params)
                    except Exception as e:
                        print(f"Error: {e}")
                        print(f"SQL: {sql}")
                conn.commit()

                time.sleep(0.5)  # 为了不给服务器太大压力,每次请求间隔0.5秒
            # 更新最新的获取时间,特别的,如果date_end>当前时间,则记录结束时间为当前时间(北京时间)
            if datetime.fromisoformat(date_end).astimezone(pytz.utc) > date_now:
                cst_timezone = pytz.timezone('Asia/Shanghai')
                date_end = date_now.astimezone(cst_timezone).strftime('%Y-%m-%dT%H:%M:%S+08:00')
            with conn.cursor() as cursor:
                log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 更新最新的获取时间,设置为开始时间,而不是结束时间的原因是,while循环的退出条件是结束时间>当前时间,如果设置为结束时间,则会导致最后一次获取的数据不完整
                cursor.execute(f"UPDATE worldquant.logs SET log_value='{date_end}',log_time='{log_time}' WHERE log_type='get_alpha_info'")
            conn.commit()
            # 开始时间更新为结束时间,继续下一次循环
            date_begin = date_end

    print(f"Total count: {total_count}")

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

照着操作了,可以麻烦补充一下

table_names = ["ASI_DELAY1", ]这些表的创建语句及对应的从worldquant拉取数据字段的函数方法吗?

还有sharpe_2022 = get_sharpe_2022(s, id),这个get_sharpe_2022(s, id)函数能否补充一下?

谢谢.

---

### 评论 #3 (作者: XM75236, 时间: 1年前)

### 表

-- worldquant.asi_delay1 definition

CREATE TABLE `asi_delay1` (
  `field` varchar(100) NOT NULL,
  `region` varchar(100) DEFAULT NULL,
  `delay` char(1) DEFAULT NULL,
  `universe` varchar(100) DEFAULT NULL,
  `datasets` varchar(100) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `coverage` float DEFAULT NULL,
  `userCount` int DEFAULT NULL,
  `alphaCount` int DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`field`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

### 拉取字段(获取到后自己用pymysql往数据库存)

```
def get_fields(s, dataset_id, region, delay, universe):    """    给定data_sets的id,以及参数region,delay,universe,返回符合条件的data_sets里面的fields    :param s: requests.session()    :param dataset_id: data_sets的id    :param region: region    :param delay: delay    :param universe: universe    :return: fields,每个field是一个dict,包含field_type和field_id    """    url_template = (        "https://api.worldquantbrain.com/data-fields?"        f"&instrumentType=EQUITY"        f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50"        "&offset={x}"    )    result = s.get(url_template.format(x=0)).json()    # 如果result中没有count字段,则打印result并报错,为了找到错误原因    if 'count' not in result:        print(result)        raise ValueError("No count field in result")    count = result['count']    datafields_list = []    for x in range(0, count, 50):        results = s.get(url_template.format(x=x)).json()['results']        for result in results:            field_type = result['type']            field_id = result['id']            description = result['description']            coverage = result['coverage']            userCount = result['userCount']            alphaCount = result['alphaCount']            datafields_list.append({'field_type': field_type, 'field_id': field_id, 'description': description,'coverage': coverage, 'userCount': userCount, 'alphaCount': alphaCount})    return datafields_list
```

### get_sharpe_2022

def get_sharpe_2022(s, alpha_id):

result = s.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats](https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats) ")

while True:

if "retry-after" in result.headers:

# print('retrying in', result.headers["retry-after"], 'seconds')

time.sleep(float(result.headers["retry-after"]))

result = s.get(f" [https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats](https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats) ")

else:

break

try:

response_json = result.json()

sharpe_2022 = response_json["records"][-1][6]

print(f"alpha_id: {alpha_id}, sharpe_2022: {sharpe_2022}")

return float(sharpe_2022)

except json.decoder.JSONDecodeError:

print(result.text)

print("JSONDecodeError: No valid JSON object could be decoded from the string.")

return None

except Exception as e:

print(f"when get sharpe_2022 for alpha_id: {alpha_id}, error: {e}")

print(result.text)

return None

---

### 评论 #4 (作者: WL56882, 时间: 1年前)

get_sharpe_2022是干啥的

---

### 评论 #5 (作者: SD17531, 时间: 1年前)

谢谢大佬,希望尽快出现 **第02篇** .

---

### 评论 #6 (作者: ST25014, 时间: 1年前)

感谢分享

---

### 评论 #7 (作者: XM75236, 时间: 1年前)

get_sharpe_2022是2022也就是最近一年的sharpe,看这个是为了筛选信号明显衰减的alpha.

只是粗犷的筛选,如果你觉得放入完整的P/L信息更好也可以自己加入一些字段.

另外预告下,第二篇写的是redis建立等待模拟的alpha池子的方式,实现永不停歇的读取池子进行模拟的任务,和自由推送模拟任务的解耦.

> 如果有问题解决不了,那就加一层中间层.如果还解决不了,那就再加一层.

---

### 评论 #8 (作者: TQ88961, 时间: 1年前)

随着回测次数达到几十万上百万，数据库会膨胀到多大？

---

