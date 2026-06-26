# [工程优化]增强版mult_simulation分享

- **链接**: [Commented] [工程优化]增强版mult_simulation分享.md
- **作者**: ZL35633
- **发布时间/热度**: 1年前, 得票: 10

## 帖子正文

* 支持断点续跑

* 支持卡槽分配

* 支持完成时间预估

* 优化提交效率 [速度+15%]

* 基础语法+单线程实现

* 兼容旧版本接口

```
import osimport jsonimport timeimport hashlibimport datetimeimport wqbAPI_SIMULATION_URL = "https://api.worldquantbrain.com/simulations"API_SIMULATION_MSG_URL = "https://api.worldquantbrain.com/simulations/{task_id}"def _generate_payload(task):    payload = []    for code, decay in task['alpha_list']:        item = {            'type': 'REGULAR',            'settings': {                'instrumentType': 'EQUITY',                'region': task['region'],                'universe': task['universe'],                'delay': 1,                'decay': decay,                'neutralization': task['neutralization'],                'truncation': 0.08,                'pasteurization': 'ON',                'testPeriod': 'P2Y',                'unitHandling': 'VERIFY',                'nanHandling': 'ON',                'language': 'FASTEXPR',                'visualization': False,            },            'regular': code        }        payload.append(item)    return payloaddef _is_slot_available(session, slot):    if not slot:        return True    try:        now = time.time()        if slot.get('check_time', 0) > now:            return False        response = session.get(slot['progress_url'], timeout=60)        retry_after = response.headers.get("Retry-After", 0)                if retry_after != 0:            slot['check_time'] = now + float(retry_after)        else:            slot['cost'] = float(now - slot['start_time'])            data = response.json()                        if data.get("status") == "COMPLETE":                slot['complete'] = True                print(f"Task {slot['task_id']} complete, Cost: {int(slot['cost'])} s")            else:                print(f"Task {slot['task_id']} fail, Cost: {int(slot['cost'])} s")                print(slot['task'])                for task_id in data.get('children', []):                    msg = session.get(API_SIMULATION_MSG_URL.format(task_id=task_id), timeout=60).json()                    print(json.dumps(msg, indent=2))            return True    except Exception as e:        import traceback        traceback.print_exc()    return Falsedef _submit_task(session, slot, task):    if not task:        return False    slot['task'] = task    slot['task_id'] = task['task_id']    slot['alpha_list'] = task['alpha_list']    slot['start_time'] = time.time()    slot['complete'] = False    slot['check_time'] = 0        try:        payload = _generate_payload(task)        response = session.post(API_SIMULATION_URL, json=payload)        slot['progress_url'] = response.headers['Location']        return True    except Exception as e:        print(f"Error submitting task: {e}, http_code: {response.status_code}")        print(payload)        time.sleep(600)    return Falsedef _gen_signature(alpha, region, universe, neutralization):    code, decay = alpha    plaintext = f"{region}{universe}{neutralization}{decay}{code}"    sign = hashlib.md5(plaintext.encode()).hexdigest()    return sign        def _make_task(neutralization, region, universe, task_id, alpha_list, signature_list):    task = {        'task_id': task_id,        'alpha_list': alpha_list,        'region': region,        'universe': universe,        'neutralization': neutralization,        'signature_list': signature_list    }        return taskdef _initialize_tasks(alphas, signature_set, neutralization, region, universe):    tasks = list()        alpha_list = list()    signature_list = list()        cnt = 0        for alpha in alphas:        sign = _gen_signature(alpha, region, universe, neutralization)        if sign in signature_set:            print(f'Skip alpha, {alpha}')            continue                alpha_list.append(alpha)        signature_list.append(sign)                if len(alpha_list) >= 10:            task = _make_task(neutralization, region, universe, cnt, alpha_list, signature_list)            tasks.append(task)            cnt += 1            alpha_list = list()            signature_list = list()                if len(alpha_list) > 1:        task = _make_task(neutralization, region, universe, cnt, alpha_list, signature_list)        tasks.append(task)    elif len(alpha_list) == 1:        print(f"Invalid Task: {alpha_list}")                            print(f"Total Tasks: {len(tasks)}")        return tasksdef _estimate_completion(n_task, n_slot, avg_cost):    estimated_time = datetime.datetime.fromtimestamp(time.time() + (avg_cost * n_task / n_slot))    return estimated_time.strftime("%Y-%m-%d %H:%M:%S")def _save_checkpoint(file_path, task):    with open(file_path, 'a') as fp:        for sign in task['signature_list']:            fp.write(f'{sign}\n')            fp.flush()def _load_checkpoint(checkpoint_file):    signature_set = set()    if not os.path.exists(checkpoint_file):        with open(checkpoint_file, 'w') as _:            pass    with open(checkpoint_file) as fp:        for sign in fp:            signature_set.add(sign.strip())     return signature_setdef _cost_avg():    cost_list = list()    def add_cost(cost):        nonlocal cost_list        cost_list.append(float(cost))        return sum(cost_list)/len(cost_list)    return add_costdef run_simulations(session, alphas, neutralization, region, universe, slot_num=9, checkpoint_file='./simulation.ckpt'):    slots = [dict() for _ in range(slot_num)]    signature_set = _load_checkpoint(checkpoint_file)    tasks = _initialize_tasks(alphas, signature_set, neutralization, region, universe)        cost_avg = _cost_avg()    while tasks:        for slot in slots:            time.sleep(0.1)            if _is_slot_available(session, slot):                                task = tasks.pop(0)                                if slot.get('complete', False):                    _save_checkpoint(checkpoint_file, slot['task'])                    print(f"Estimated completion: {_estimate_completion(len(tasks), len(slots), cost_avg(slot['cost']))}")                                if _submit_task(session, slot, task):                    print(f"Task {slot['task_id']} submitted")                print("Simulation complete")def multi_simulate(alpha_pools, neut, region, universe, start):    wqs = wqb.WQBSession(('<email>', '<password>'))    alphas = list()    for pool in alpha_pools:        for batch in pool:            for alpha in batch:                alphas.append(alpha)    run_simulations(        wqs, alphas, neut, region, universe,         slot_num=10, checkpoint_file='./simulation.ckpt'    )
```

---

## 讨论与评论 (9)

### 评论 #1 (作者: JB71859, 时间: 1年前)

怎么用呢

---

### 评论 #2 (作者: ZL35633, 时间: 1年前)

@ [JB71859](/hc/en-us/profiles/26720563911063-JB71859)  抱歉，有几处错误已经修改，帖子已经更新等待审核。

1.pip install wqb， 因为代码里使用了 [HD44583](/hc/en-us/profiles/27705611217687-HD44583) 大佬的session。

2.注释掉machine_lib里的multi_simulate函数

3.将代码粘贴到machine_lib里

4.修改multi_simulate里的用户名和密码。

---

### 评论 #3 (作者: JM61824, 时间: 1年前)

为什么会提示
Error submitting task: 'location'

---

### 评论 #4 (作者: JL16510, 时间: 1年前)

出现Error submitting task: 'location'一般是参数有问题。

---

### 评论 #5 (作者: ZS59763, 时间: 1年前)

location一般是：你槽已经跑满了，或者入参有问题（建议检查alpha的表达式是否正确）

---

### 评论 #6 (作者: SH51829, 时间: 1年前)

```
# - HTTP 400 错误表示客户端发送的请求存在错误，无法被服务器理解和接受。常见原因包括请求参数错误、请求头设置不当、Cookie问题、客户端软件错误等。# 解决方案：# 1. 首先检查函数调用那里传参的填写内容格式是否正确（如调用 multi_simulate 函数那里的第二个参数应该是`SECTOR`而非`Sector`）# 2. 还有报错 400 ，post 的代码尝试改造如下（理论上应该是参数错误，你看看是不是有个批量槽只送了一个 alpha ）if len(sim_data_list)== 1:    simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=sim_data_list[0])else:    simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=sim_data_list)
```

---

### 评论 #7 (作者: SH51829, 时间: 1年前)

```
"""感谢分享！以下是本人对楼主代码的 _is_slot_available 函数和 run_simulations 函数以及 multi_simulate 函数进行一些改动 ~ 欢迎补充交流 ~ 改动位置已用`# [x]`注释标明！"""
```

```
def _is_slot_available(session, slot):    if not slot:        return True     # 空槽位直接标记为可用    # [x] 🔍 新增关键检查：如果progress_url不存在，说明是未使用的空槽    if 'progress_url' not in slot:        return True     # 空槽位直接标记为可用    try:        # 其余代码不变        now = time.time()        # ……
```

```
def run_simulations(session, alphas, neutralization, region, universe, slot_num=9, checkpoint_file='./simulation.ckpt'):    slots = [dict() for _ in range(slot_num)]    signature_set = _load_checkpoint(checkpoint_file)    tasks = _initialize_tasks(alphas, signature_set, neutralization, region, universe)    cost_avg = _cost_avg()    while tasks:        for slot in slots:            time.sleep(0.1)            if _is_slot_available(session, slot):                # """                # task = tasks.pop(0)                # if slot.get('complete', False):                #     _save_checkpoint(checkpoint_file, slot['task'])                #     print(f"Estimated completion: {_estimate_completion(len(tasks), len(slots), cost_avg(slot['cost']))}")                # [x] [工程优化]增强版mult_simulation分享-V6 解决函数 multi_simulate 调用报错  IndexError: pop from empty list                  task = None                if tasks:                    task = tasks.pop(0)                if slot.get('complete', False):                    _save_checkpoint(checkpoint_file, slot['task'])                    print(f"Estimated completion: {_estimate_completion(len(tasks), len(slots), cost_avg(slot['cost']))}")                # """                if _submit_task(session, slot, task):                    print(f"Task {slot['task_id']} submitted")    # print("Simulation complete")    # [x] [工程优化]增强版mult_simulation分享-V10-250311 完善代码任务完成检查逻辑    # 等待所有槽位任务完成    while True:        all_complete = True        for slot in slots:            if not _is_slot_available(session, slot):                all_complete = False                break        if all_complete:            break        time.sleep(120)  # 每120秒检查一次        print("Simulation complete")  # 确保这是最后一行    
```

```
def multi_simulate(alpha_pools, neut, region, universe, start):    # wqs = wqb.WQBSession(('<email>', '<password>'))    # [x] 调用目录下其它文件获取账号密码代替上面直接输入的方法    # """    with open(expanduser("brain_credentials.txt")) as f:    # txt文件内容为["这里填写邮箱", "这里填写密码"]        credentials = json.load(f)    username, password  =  credentials    wqs = wqb.WQBSession((username, password))    # """    alphas = list()    for pool in alpha_pools:        for batch in pool:            for alpha in batch:                alphas.append(alpha)    run_simulations(        wqs, alphas, neut, region, universe,         slot_num=10, checkpoint_file='./simulation.ckpt'    )
```

---

### 评论 #8 (作者: ZL35633, 时间: 1年前)

@ [SH51829](/hc/en-us/profiles/27031967893015-SH51829)  感谢！

---

### 评论 #9 (作者: ZZ44620, 时间: 1年前)

[ZL35633](/hc/en-us/profiles/28828582941975-ZL35633) ， [SH51829](/hc/en-us/profiles/27031967893015-SH51829)

下面我运行出现的情况，如果最后一组任务提交完成之后，会一直出现无规则complete(因为我需要遍历中性化，所以一直卡在这，到不了下一个任务), 而且这种complete不是之前提交后的，例如Task 174 complete出现了三次

Task 184 submitted
Task 174 complete, Cost: 376 s
Task 174 complete, Cost: 497 s
Task 183 complete, Cost: 257 s
Task 184 complete, Cost: 245 s
Task 174 complete, Cost: 619 s
Task 183 complete, Cost: 379 s
Task 184 complete, Cost: 368 s
Task 178 complete, Cost: 415 s
Task 168 complete, Cost: 626 s
Task 182 complete, Cost: 394 s
Task 179 complete, Cost: 414 s
Task 174 complete, Cost: 742 s
Task 183 complete, Cost: 502 s
Task 184 complete, Cost: 490 s
Task 178 complete, Cost: 538 s
Task 168 complete, Cost: 750 s
Task 182 complete, Cost: 517 s
Task 179 complete, Cost: 537 s
Task 174 complete, Cost: 865 s
Task 183 complete, Cost: 625 s
Task 184 complete, Cost: 613 s
Task 178 complete, Cost: 661 s

然后我问ai修改了一下函数(我使用[x] new标记新的修改)

```
def _is_slot_available(session, slot):    if not slot:        return True     # 空槽位直接标记为可用    # [x] 🔍 新增关键检查：如果progress_url不存在，说明是未使用的空槽    if 'progress_url' not in slot:        return True     # 空槽位直接标记为可用           # [x] new 关键修复：如果任务已被标记为完成，直接返回True    if slot.get('complete', False):        return True
```

和

```
def run_simulations(session, alphas, neutralization, region, universe, slot_num=9, checkpoint_file='./simulation.ckpt'):    slots = [dict() for _ in range(slot_num)]    signature_set = _load_checkpoint(checkpoint_file)    tasks = _initialize_tasks(alphas, signature_set, neutralization, region, universe)    cost_avg = _cost_avg()    while tasks:         # 这里一样           # [x] new 等待所有槽位任务完成     print("等待所有任务完成...")    last_status_change = time.time()    last_complete_count = 0    while True:        all_complete = True        complete_count = 0        for slot in slots:            if slot and 'progress_url' in slot and not slot.get('complete', False):                all_complete = False            elif slot and slot.get('complete', False):                complete_count += 1        # 如果任务完成数量变化，更新状态变化时间        if complete_count != last_complete_count:            last_status_change = time.time()            last_complete_count = complete_count        # 检测异常情况：30分钟内没有任何新任务完成，可能陷入循环        if not all_complete and time.time() - last_status_change > 1800:  # 30分钟            print("警告：30分钟内没有新任务完成，可能存在问题。强制退出等待。")            break        if all_complete:            break        print(f"进度：已完成{complete_count}/{len(slots)}个任务，继续等待...")        time.sleep(120)  # 每120秒检查一次    print("Simulation complete")    
```

然后输出现在变成了：

Task 184 submitted

等待所有任务完成...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

进度：已完成0/10个任务，继续等待...

警告：30分钟内没有新任务完成，可能存在问题。强制退出等待。

Simulation complete

我对于代码理解不是很深，所以这个解决方案是结合ai的比较牵强的方案，希望和大家交流讨论一下。

---

