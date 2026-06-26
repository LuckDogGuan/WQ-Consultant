# 基于wqb+MongoDB的边回测边储存alpha_info和pnl方案

- **链接**: 基于wqbMongoDB的边回测边储存alpha_info和pnl方案.md
- **作者**: MZ45384
- **发布时间/热度**: 10个月前, 得票: 12

## 帖子正文

随着回测数量不断增加，提交前的准备工作也在复杂化，例如检查厂型alpha和相关性剪枝等等，而这些工作都需要pnl或alpha details。由于我本人有每提交一个alpha就重新检查可提交alpha的习惯，因此需要大量调用api，而api调用次数每小时限流，因此使用数据库来储存调用出来的信息一边后续直接从数据库中读取是最优解，论坛里不少前辈都用sqlite, mysql或oracle来储存，不过也有用mongoDB的， 综合来看，我认为后者操作更简单也更符合json格式；而wqb的concurrent_simulate刚好提供了可操作的回调函数。于是我采用了wqb+mongoDB的方式，代码如下：import requestsimport timeimport pymongoclient = pymongo.MongoClient('localhost', 27017)alpha_db = client.alpha_dbalphas_cl = alpha_db.alphaspnls_cl = alpha_db.pnlsdef login():     # 登录平台username = "3323438320@qq.com"password = "UCkingdom0102"# Create a session to persistently store the headerss = requests.Session()# Save credentials into sessions.auth = (username, password)# Send a POST request to the /authentication APIresponse = s.post('https://api.worldquantbrain.com/authentication')print(response.text)return ss = login()def wait_get(sess, url: str, max_retries: int = 10) -> "Response":retries = 0while retries < max_retries:while True:simulation_progress = sess.get(url)if simulation_progress.headers.get("Retry-After", 0) == 0:breaktime.sleep(float(simulation_progress.headers["Retry-After"]))if simulation_progress.status_code < 400:breakelse:time.sleep(2 ** retries)retries += 1return simulation_progressdef save_alpha_from_children(n, resp, wqbs):   # 储存部分global sif resp.status_code != 200:print(f'{n}, {resp}')returnchildren = resp.json()['children']count = 0for url in children:while True:try:data = wait_get(s, 'https://api.worldquantbrain.com/simulations/'+url).json()if data['status'] == 'ERROR':print(n, 'irregular alpha:', data['message'])breakelif data['status'] == "COMPLETE" or data['status'] == "WARNING":alpha_id = data["alpha"]alpha = wait_get(s, f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()if abs(alpha["is"]["sharpe"]) < 1 or abs(alpha["is"]["fitness"]) < 0.7:   # 选择满足一定标准的进行储存，标准因人而异breakcount += 1alphas_cl.insert_one(alpha)pnl = wait_get(s, 'https://api.worldquantbrain.com/alphas/' + alpha_id + '/recordsets/pnl').json()pnl['alpha_id'] = alpha_idpnls_cl.insert_one(pnl)breakelse:print(n, data['status'])breakexcept Exception as e:print(f'{n}, Error: {e}')time.sleep(100)s = login()continueprint(f'{n}, {resp}, {count} alpha and pnl saved successfully')这段代码可以直接放到machine_lib.py里或者单独放一个py文件，然后在回测部分插入：multi_alphas_2 = wqb.to_multi_alphas(sim_data_list_2, 10)concurrency = 8start = 0resps = await wqbs.concurrent_simulate(multi_alphas_2,concurrency,start_point = start,on_start=lambda vars: print(f'{vars['idx']}, {vars['url']}'),on_success=lambda vars: save_alpha_from_children(vars['idx'], vars['resp'], wqbs),on_failure=lambda vars: print(f'{vars['idx']}, {vars['resp']}'),)效果如下

---

## 讨论与评论 (2)

### 评论 #1 (作者: MY49971, 时间: 9个月前)

大哥，注意你的账户啊~========================================================================================================================================================================

---

### 评论 #2 (作者: JX14975, 时间: 9个月前)

大佬，有测试过这样是否会影响回测速度吗？我不清楚wqb库的on_success输入是否会与接下来的异步回测抢时间（貌似在回测完后改颜色与名字是会的）？另外，在跑GLB等地区可能会出现回测仍然在平台上进行但wqb库已经超时了的情况，这又是如何处理的？

---

