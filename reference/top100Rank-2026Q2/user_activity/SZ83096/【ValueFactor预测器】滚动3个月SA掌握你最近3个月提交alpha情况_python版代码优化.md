# 【ValueFactor预测器】滚动3个月SA，掌握你最近3个月提交alpha情况_python版代码优化

- **链接**: 【ValueFactor预测器】滚动3个月SA掌握你最近3个月提交alpha情况_python版代码优化.md
- **作者**: SZ83096
- **发布时间/热度**: 11 months ago, 得票: 87

## 帖子正文

首先感谢weijie老师提出的idea:

选择你最近3个月提交的alpha 组SA，根据SA的表现衡量你过去3个月提交的alpha的质量，sa的表现可以视作value factor的预告。之后，你提交的alpah，需要和过去3个月组合的sa的相关性低。

那么如何滚动3个月的alpha组合sa呢？

根据alpha提交的时间，添加年份-月份的tags，然后在组sa的时候，选择tags是指定月份的alpha，进行回测，根据sa的表现，衡量你最近3个月提交的sa质量，代码如下：

```
import jsonimport sysimport timefrom datetime import datetimefrom time import sleepimport requestsfrom requests.adapters import HTTPAdapterfrom requests.packages.urllib3.util.retry import Retrydef load_config(file_path):    """从指定路径f加载JSON配置文件，并处理可能的异常"""    try:        with open(file_path, 'r') as file:            config = json.load(file)        return config    except FileNotFoundError:        print(f"Error: Config file '{file_path}' not found.")        sys.exit(1)    except json.JSONDecodeError as e:        print(f"Error: Failed to parse JSON from '{file_path}': {e}")        sys.exit(1)config_file = 'config.json'config = load_config(config_file)user=config["user"]passwd=config["password"]def login():    username = user    password =  passwd    retry_strategy = Retry(        total=3,  # 总共重试次数        backoff_factor=1,  # 每次重试之间的延迟时间（秒）        status_forcelist=[500, 502, 503, 504]  # 遇到这些HTTP状态码时重试    )    adapter = HTTPAdapter(max_retries=retry_strategy)    s = requests.Session()    s.mount("https://", adapter)    s.mount("http://", adapter)    s.auth = (username, password)    max_try = 3    retry=0    while True:        try:            response = s.post('https://api.worldquantbrain.com/authentication')            if response.status_code  in [200,201]:                print(f"login success")                return s        except Exception as e:            print(f"login err :{e}")            print(f"login failed ,sleep 5 ,try again")            sleep(5)        retry +=1        if retry > max_try:            break    return Nonedef get_submited_alphas_three_month(s,start_date,end_date,region,only_ppa=True):    # only_ppa 设置是否只获取ppa的alpha设置tags，后续组sa时根据tags值的年份月份筛选    print(f"正在获取{start_date}到{end_date}内，{region}地区的ppa alpha")    url=f"https://api.worldquantbrain.com/users/self/alphas?limit=10&offset=0&status!=UNSUBMITTED%1FIS-FAIL&dateSubmitted%3E{start_date}T04:00:00.000Z&dateSubmitted%3C{end_date}T04:00:00.000Z&type=REGULAR&settings.region={region}&order=-dateSubmitted&hidden=false"    count=0    print(url)    count=s.get(url).json()['count']    print(count)    alpha_list=[]    for i in range(0,count,100):        url=f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}&status!=UNSUBMITTED%1FIS-FAIL&dateSubmitted%3E{start_date}T04:00:00.000Z&dateSubmitted%3C{end_date}T04:00:00.000Z&type=REGULAR&settings.region={region}&order=-dateSubmitted&hidden=false"        response=s.get(url).json()        for alpha in response['results']:            if only_ppa:                flag=0                for item in alpha["classifications"]:                    if item['name']=='Power Pool Alpha':                        flag=1                        break                if flag==1:                    alpha_list.append(alpha)            else:                alpha_list.append(alpha)    print(f"在时间范围{start_date}到{end_date}内，{region}地区，获取了 {len(alpha_list)}个ppa alpha")    return alpha_list# 对所有alpha 在原有tags列表上增加年份+月份的tags，如2025-05def set_alpha_property_list(s,alpha_list):    count = 0    for alpha in alpha_list:        alpha_id=alpha['id']        print(f"正在设置第{count}个alpha 的属性,{alpha_id}; 总alpha数量{len(alpha_list)}")        tags=alpha['tags']        name=alpha['name']        date_created=alpha['dateCreated']        color=alpha['color']        description=alpha['regular']['description']        dt = datetime.fromisoformat(date_created.replace('Z', '+00:00'))        year_month = dt.strftime('%Y-%m')  # "2025-07"        print(year_month)        if year_month in tags:            continue        else:            tags.append(year_month)        category=alpha['category']        if category is None:            category=None        if color is None:            color=None        if name is None:            name=None        print(tags)        params = {        "color": color,        "name": name,        "tags": tags,        "category": None,        "regular": {"description": description},        "combo": {"description": description},        "selection": {"description": description}}        response = s.patch( "https://api.worldquantbrain.com/alphas/" + alpha_id, json=params)        # print(response.json())        sleep(1)        count+=1    return Truedef make_simulation_data(select,combo,region,universe,delay,decay,neut_,select_handle,select_num,maxtrade):    simulation_data={    "type": "SUPER",    "settings": {        "maxTrade": maxtrade,        "nanHandling": "ON",        "instrumentType": "EQUITY",        "delay": delay,        "universe": universe,        "truncation": 0.08,        "unitHandling": "VERIFY",        "selectionLimit": select_num,        "selectionHandling": select_handle,        "testPeriod": "P0D",        "componentActivation": "IS",        "pasteurization": "ON",        "region": region,        "language": "FASTEXPR",        "decay": decay,        "neutralization": neut_,        "visualization": False    },    "combo": str(combo),    "selection": select}    return simulation_datadef simulate_sa(s,simulation_data):    brain_api_url = 'https://api.worldquantbrain.com'    try:        simulation_response=s.post(f'{brain_api_url}/simulations',json=simulation_data)        # print(simulation_response.json())    except Exception as e:        print(f"模拟sa失败:{e}")        return None    simulation_progress_url = simulation_response.headers['Location']    print(simulation_progress_url)    while True:        simulation_progress_response=s.get(simulation_progress_url)        retry_after = simulation_progress_response.headers.get("Retry-After", 0)        if str(retry_after) == '0':            status = simulation_progress_response.json().get("status", "not_found")            if status == "COMPLETE":                res_=simulation_progress_response.json()                alpha_id=res_["alpha"]                print(f"最近3个月的ppa组成的sa模拟完成,alpha_id:{alpha_id}")                break        else:            print(f"processing,begin sleep {float(retry_after)}")            time.sleep(float(retry_after))    return alpha_id# 对指定日期范围内的ppa 设置年月标签来确认是否是指定时间范围的ppas = login()#设置你想滚动组合sa的月份start_date='2025-04-01'end_date='2025-06-30'data_range=['2025-04','2025-05','2025-06']# 地区，universeregion='USA'universe='TOP3000'delay=1decay=0select_handle='POSITIVE'select_num=300maxtrade='ON'alpha_list=get_submited_alphas_three_month(s,start_date,end_date,region)print(f"在时间范围{start_date}到{end_date}内，提交了 {len(alpha_list)}个ppa alpha")print(alpha_list[0]['id'],)set_alpha_property_list(s,alpha_list)select=f'(own) && ((in(tags,"{data_range[0]}")) || (in(tags,"{data_range[1]}"))|| (in(tags,"{data_range[2]}")))'print(select)combo=1alpha_ids=[]for decay in  [0]:    ##可根据需要对多种neut回测查看sa表现    for neut_ in  ["CROWDING","REVERSION_AND_MOMENTUM"]:        simulation_data=make_simulation_data(select,combo,region,universe,delay,decay,neut_,select_handle,select_num,maxtrade)        alpha_id=simulate_sa(s,simulation_data)        alpha_ids.append(alpha_id)print(f"完成回测,alpha_id如下")print(alpha_ids)print(f"最近3个月， {region} 提交的ppa 组合的sa表现如下")for alpha_id in alpha_ids:    res=s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}")    res_json=res.json()    sharpe=res_json['is']['sharpe']    fitness=res_json['is']['fitness']    return_=res_json['is']['returns']    drawdown=res_json['is']['drawdown']    margin=res_json['is']['margin']    turnover=res_json['is']['turnover']    neut=res_json['settings']['neutralization']    decay=res_json['settings']['decay']    print(f"{alpha_id}: sharpe: {sharpe}, fitness: {fitness}, return: {return_}, drawdown: {drawdown}, margin: {margin}, turnover: {turnover}, neut: {neut},decay: {decay}")
```

输出结果如下：

```
完成回测,alpha_id如下['12Q7xez', 'E2XGKG0']最近3个月提交的ppa USA 组合的sa表现如下12Q7xez: sharpe: 3.71, fitness: 5.36, return: 0.2609, drawdown: 0.0647, margin: 0.00873, turnover: 0.0598, neut: CROWDING,decay: 0E2XGKG0: sharpe: 4.11, fitness: 5.85, return: 0.2533, drawdown: 0.0429, margin: 0.006105, turnover: 0.083, neut: REVERSION_AND_MOMENTUM,decay: 0
```

---

## 讨论与评论 (9)

### 评论 #1 (作者: WL13229, 时间: 11 months ago)

请补充图片实例

---

### 评论 #2 (作者: SZ83096, 时间: 11 months ago)

修改下最后部分的代码，并补充代码最后输出的结果图

```
s = login()start_date='2025-04-01'end_date='2025-06-30'data_range=['2025-04','2025-05','2025-06']# region='ASI'# universe='MINVOL1M'regions=[['ASI','MINVOL1M'],['USA','TOP3000'],['EUR','TOP2500']]delay=1select_handle='POSITIVE'select_num=300maxtrade='ON'result_mess=[]for region,universe in regions:    alpha_list=get_submited_alphas_three_month(s,start_date,end_date,region)    print(f"在时间范围{start_date}到{end_date}内，提交了 {len(alpha_list)}个ppa alpha")    print(alpha_list[0]['id'])    set_alpha_property_list(s,alpha_list)    select=f'(own) && ((in(tags,"{data_range[0]}")) || (in(tags,"{data_range[1]}"))|| (in(tags,"{data_range[2]}")))'    print(select)    combo=1    alpha_ids=[]    for decay in  [0]:        ##可根据需要对多种neut回测查看sa表现        for neut_ in  ["CROWDING","REVERSION_AND_MOMENTUM"]:            simulation_data=make_simulation_data(select,combo,region,universe,delay,decay,neut_,select_handle,select_num,maxtrade)            alpha_id=simulate_sa(s,simulation_data)            alpha_ids.append(alpha_id)    # print(f"完成回测,alpha_id如下")    # print(alpha_ids)    # print(f"最近3个月 {region}地区 提交的ppa 组合的sa表现如下")    result_mess.append(f"最近3个月 {region}地区 提交了  {len(alpha_list)} 个 ppa alpha, ppa 组合的sa表现如下")    for alpha_id in alpha_ids:        res=s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}")        res_json=res.json()        sharpe=res_json['is']['sharpe']        fitness=res_json['is']['fitness']        return_=res_json['is']['returns']        drawdown=res_json['is']['drawdown']        margin=res_json['is']['margin']        turnover=res_json['is']['turnover']        neut=res_json['settings']['neutralization']        decay=res_json['settings']['decay']        mess=f"region: {region} {alpha_id}: sharpe: {sharpe}, fitness: {fitness}, return: {return_}, drawdown: {drawdown}, margin: {margin}, turnover: {turnover}, neut: {neut},decay: {decay}"        # print(mess)        result_mess.append(mess)for item in result_mess:    print(item)
```

![图片](images/img_3088a5bb0f.png)

---

### 评论 #3 (作者: ML42552, 时间: 11 months ago)

太强了橘子姐，马上用上了，虽然经过3-5月和4-6月的比对看不出什么，但是把自己的和橘子姐的对比一下就很明显了。

62xXrP5: sharpe: 2.52, fitness: 2.8, return: 0.1545, drawdown: 0.0615, margin: 0.004116, turnover: 0.0751, neut: CROWDING,decay: 0
vo0RPaA: sharpe: 2.64, fitness: 2.86, return: 0.1463, drawdown: 0.0527, margin: 0.002861, turnover: 0.1023, neut: REVERSION_AND_MOMENTUM,decay: 0

全方面的碾压，难怪橘子姐的vf能这么高，对未来的提交标准有了一定的认知了

感谢橘子姐！！！

---

### 评论 #4 (作者: YC62305, 时间: 10 months ago)

```
config_file = 'config.json'
```

这块如何配置

---

### 评论 #5 (作者: SZ83096, 时间: 10 months ago)

[YC62305](/hc/en-us/profiles/28856294144279-YC62305)

在运行这个脚本的相同目录下，创建个config.json文件，然后文件内容如下：wq的账号密码

```
{    "user": "xxxx",    "password": "zzzz"}
```

---

### 评论 #6 (作者: HW54322, 时间: 10 months ago)

自动回测VF，mark一下

---

### 评论 #7 (作者: KH92677, 时间: 10 months ago)

这段代码是不是要交过SA才会有VF的预测结果？

---

### 评论 #8 (作者: ZJ47021, 时间: 9 months ago)

这个怎么用呀？

---

### 评论 #9 (作者: HH61427, 时间: 8 months ago)

这个跑出来的结果是怎么影响vf的，或者说和标题的关联是什么

---

