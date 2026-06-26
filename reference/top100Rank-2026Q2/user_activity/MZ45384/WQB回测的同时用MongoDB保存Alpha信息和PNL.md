# WQB回测的同时用MongoDB保存Alpha信息和PNL

- **链接**: WQB回测的同时用MongoDB保存Alpha信息和PNL.md
- **作者**: MZ45384
- **发布时间/热度**: 10个月前, 得票: 13

## 帖子正文

最近拜读了社区里好几位大佬保存alpha信息和pnl的帖子，于是自己也写了一个，代码能力薄弱，还望批评指正。代码如下：import requestsimport timeimport pymongoclient = pymongo.MongoClient('localhost', 27017)alpha_db = client.alpha_dbalphas_cl = alpha_db.alphaspnls_cl = alpha_db.pnlsdef login():username = "your email"password = "your password"# Create a session to persistently store the headerss = requests.Session()# Save credentials into sessions.auth = (username, password)# Send a POST request to the /authentication APIresponse = s.post('https://api.worldquantbrain.com/authentication')print(response.text)return ss = login()def wait_get(sess, url: str, max_retries: int = 10) -> "Response":retries = 0while retries < max_retries:while True:simulation_progress = sess.get(url)if simulation_progress.headers.get("Retry-After", 0) == 0:breaktime.sleep(float(simulation_progress.headers["Retry-After"]))if simulation_progress.status_code < 400:breakelse:time.sleep(2 ** retries)retries += 1return simulation_progressdef save_alpha_from_children(n, resp, wqbs):global sif resp.status_code != 200:print(f'{n}, {resp}')returnchildren = resp.json()['children']count = 0for url in children:while True:try:data = wait_get(s, 'https://api.worldquantbrain.com/simulations/'+url).json()if data['status'] == 'ERROR':print(n, 'irregular alpha:', data['message'])breakelif data['status'] == "COMPLETE" or data['status'] == "WARNING":alpha_id = data["alpha"]alpha = wait_get(s, f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()if abs(alpha["is"]["sharpe"]) < 1 or abs(alpha["is"]["fitness"]) < 0.7:   # 挑选满足一定条件的alpha保存breakcount += 1alphas_cl.insert_one(alpha)pnl = wait_get(s, 'https://api.worldquantbrain.com/alphas/' + alpha_id + '/recordsets/pnl').json()pnl['alpha_id'] = alpha_idpnls_cl.insert_one(pnl)breakelse:print(n, data['status'])breakexcept Exception as e:print(f'{n}, Error: {e}')time.sleep(100)s = login()continueprint(f'{n}, {resp}, {count} alpha and pnl saved successfully')这个函数放到wqb的回调函数里就可以在回测的同时储存alpha和pnl:multi_alphas_1 = wqb.to_multi_alphas(sim_data_list_1[::-1], 10)concurrency = 8start = 0resps = await wqbs.concurrent_simulate(multi_alphas_1,concurrency,start_point = start,on_start=lambda vars: print(f'{vars['idx']}, {vars['url']}'),on_success=lambda vars: save_alpha_from_children(vars['idx'], vars['resp'], wqbs),on_failure=lambda vars: print(f'{vars['idx']}, {vars['resp']}'),)效果如图：

---

## 讨论与评论 (0)

