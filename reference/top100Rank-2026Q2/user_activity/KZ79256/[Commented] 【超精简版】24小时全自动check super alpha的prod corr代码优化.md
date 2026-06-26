# 【超精简版】24小时全自动check super alpha的prod corr代码优化

- **链接**: [Commented] 【超精简版】24小时全自动check super alpha的prod corr代码优化.md
- **作者**: HW93328
- **发布时间/热度**: 10个月前, 得票: 97

## 帖子正文

省流：该代码用于check super alpha的prod cor，根据prod值为每一个sa添加颜色标签和修改name，同时检查结果将会保存在csv文件中。

论坛中之前也有大佬发过该功能的代码，但是我在学习的时候感觉功能比较“复杂”，对于“萌新”可能一下子看不懂也用不来，所以我将其中最核心的部分抽取出来，做到复制-粘贴即可快速使用。

```
from machine_lib import login,set_alpha_propertiesimport timefrom requests.exceptions import Timeout,HTTPError,RequestExceptionimport pandas as pdfrom datetime import datetimeimport csv# 获取到sa数据def get_super_alphas(start_date, end_date, sharpe_th, fitness_th, delay, alpha_num, tag: str = '', s=None):    if s is None:        s = login()    alpha_list = []    # 3E large 3C less    # 正的    i = 0    while True:        url_e = (f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}"                 f"&is.sharpe%3E={sharpe_th}&is.fitness%3E={fitness_th}"                 f"&status=UNSUBMITTED&dateCreated%3E={start_date}"                 f"T00:00:00-04:00&dateCreated%3C{end_date}T00:00:00-04:00"                 f"&settings.delay={delay}&order=-is.sharpe&hidden=false&type=SUPER")        response = s.get(url_e)        try:            i += 100            count = response.json()["count"]            print("已经获取到的原始数量count: %d" % count)            alpha_list.extend(response.json()["results"])            if i >= count or i == 9900:                break            time.sleep(0.01)        except Exception as e:            print(f"Failed to get alphas: {e}")            i -= 100            time.sleep(5)            s = login()            print("%d finished re-login" % i)    if len(alpha_list) == 0:        return []    alpha_id_list = []    for j in range(len(alpha_list)):        alpha_id = alpha_list[j]["id"]        alpha_id_list.append(alpha_id)    return alpha_id_listdef my_get(url,timeout=None):    retries=0    max_retries=3    global s    while retries < max_retries:        try:            # 发送请求（使用当前 session）            response = s.get(url,timeout=timeout)            try:                response.raise_for_status()                return response            except HTTPError as http_err:                status_code = response.status_code if response else None                if status_code ==401:                    try:                        new_session = login()                        if new_session !=None:                            s = new_session                    except Exception as e:                        print(f"登录失败: {str(e)}")                        retries += 1                    continue                elif status_code ==403:                    print(f"status code:{status_code} Forbidden 无权限访问（认证成功但权限不足）,{response.content},break")                    return None                elif response.status_code in [429,500,502,503,504]:                    wait = 2 ** retries  # 指数退避                    print(f"status code: {response.status_code} ,{response.content} ,sleep 5 and retry" )                    time.sleep(wait)                    retries += 1                else:                    raise http_err        except Timeout as e:            print(f"timeout err {e}, sleep 30 and retry")            retries += 1            time.sleep(5)        except RequestException as e:            print(f"请求失败: {str(e)}")            retries += 1            time.sleep(5)        except Exception as e:            print(f"error err {e} ,exit get request")            print(f"未知错误: {str(e)}")            retries += 1            time.sleep(5)            # return None, current_session    print(f"达到最大重试次数 {max_retries}，放弃请求")    return Noneif __name__ == '__main__':    s = login()    delay = 1    sharpe = 4.5    fitness = 5.0    start_date = "2025-07-24"    end_date = "2029-12-31"    alpha_id_list = get_super_alphas(start_date=start_date, end_date=end_date,                                     sharpe_th=sharpe, fitness_th=fitness,                                     delay=1, alpha_num=500, s=s)    # 创建CSV文件并写入表头    csv_filename = f"superalpha_prod_checkeddata.csv"    # 读取已checked的alpha id    checked_alpha_ids = set()    try:        with open(csv_filename, mode='r', newline='', encoding='utf-8') as csv_file:            reader = csv.DictReader(csv_file)            for row in reader:                checked_alpha_ids.add(row['alpha_id'])        print(f"已从 {csv_filename} 中读取 {len(checked_alpha_ids)} 个已检查的 alpha_id")    except FileNotFoundError:        print(f"文件 {csv_filename} 不存在，将创建新文件")    # 过滤掉已经检查过的 alpha_id    filtered_alpha_id_list = [alpha_id for alpha_id in alpha_id_list if alpha_id not in checked_alpha_ids]    print(f"过滤后剩余 {len(filtered_alpha_id_list)} 个未检查的 alpha_id")    for alpha_id in filtered_alpha_id_list:        # 外层循环，如果内层5次都失败则等待10分钟后重新开始        outer_retry_count = 0        max_outer_retries = 1000  # 外层最大重试次数        while outer_retry_count < max_outer_retries:            # 循环获取response，直到获取到有效内容            max_retries = 5  # 最大重试次数            retry_count = 0            success = False  # 标记是否成功获取数据            while retry_count < max_retries:                response = my_get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod")                print(f"第{retry_count + 1}次尝试获取response")                print(response)                # print(response.content)                # 添加响应验证                if response is None:                    print("请求失败，无法获取响应")                    retry_count += 1                    if retry_count < max_retries:                        print(f"等待60秒后重试...")                        time.sleep(120)                    continue                # 检查响应内容                if not response.content:                    print("响应内容为空")                    retry_count += 1                    if retry_count < max_retries:                        print(f"等待60秒后重试...")                        time.sleep(120)                    continue                # 检查响应状态码                if response.status_code != 200:                    print(f"请求失败，状态码: {response.status_code}")                    print(f"响应内容: {response.text}")                    retry_count += 1                    if retry_count < max_retries:                        print(f"等待60秒后重试...")                        time.sleep(120)                    continue                # 尝试解析JSON                try:                    res=response.json()                    success = True                    print(res)                    break                except ValueError as e:                    print(f"JSON解析失败: {e}")                    print(f"响应内容: {response.text}")                    retry_count += 1                    if retry_count < max_retries:                        print(f"等待60秒后重试...")                        time.sleep(120)                    continue            # 检查内层循环是否成功获取数据            if success:                print("成功获取并解析数据，继续执行后续逻辑")                break  # 成功获取数据，跳出外层循环            else:                # 内层5次都失败了                outer_retry_count += 1                if outer_retry_count < max_outer_retries:                    print(f"本轮5次尝试均失败，等待10分钟({600}秒)后重新开始...")                    time.sleep(600)  # 等待10分钟(600秒)                else:                    print(f"已达到最大轮次 {max_outer_retries}，放弃请求")                    exit(1)        prod = res["max"]        prod = float(prod)        print(prod)        name = 'sa'+str(prod)        # color None, RED, YELLOW, GREEN, BLUE, PURPLE        if prod>0.7:            color = 'RED'        elif prod>0.6:            color = 'BLUE'        elif prod>0.5:            color = 'GREEN'        else:            color = 'PURPLE'        set_alpha_properties(s,                             alpha_id,                             name=name,                             color=color,                             selection_desc="1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",                             combo_desc="1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"                             )        print(f'{alpha_id}prod检验完成')        # 将数据写入CSV文件        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:            fieldnames = ['alpha_id', 'prod', 'write_time']            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)            # 只有在文件为空（新创建）时才写入表头            if csv_file.tell() == 0:                writer.writeheader()            writer.writerow({                'alpha_id': alpha_id,                'prod': prod,                'write_time': current_time            })        print(f"已将 alpha_id: {alpha_id}, prod: {prod}, 时间: {current_time} 写入CSV文件")
```

![图片](images/img_b2fa46caac.png)

 ![图片](images/img_7dc67d3505.png)

---

## 讨论与评论 (6)

### 评论 #1 (作者: KZ79256, 时间: 10个月前)

佬,你的代码怎么复制上来的哇,还有高亮

======================================冲冲冲======================================

---

### 评论 #2 (作者: YZ34957, 时间: 10个月前)

up主您好，请问这个是线上的获取还是本地计算

---

### 评论 #3 (作者: LL88284, 时间: 10个月前)

感谢大佬的分享！，请问有没有完整代码文件可供下载的，git或者其他云盘

---

### 评论 #4 (作者: CC85858, 时间: 8个月前)

---------------------------------------------------------------------------------------------------------------------------------感谢大佬分享，代码非常好用，和全自动super alpha代码简直是神配合                                                           ----------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #5 (作者: DC54828, 时间: 7个月前)

大佬，用你的代码我运行不了，check出来是估计值

---

### 评论 #6 (作者: CL86067, 时间: 7个月前)

奇怪，一直请求码200，响应失败，不知道大家成功运行了吗？

---

