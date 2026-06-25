# 【新人向-RA的本地self+ppac自相关】复制即用！代码优化

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwiXJhVeXCA6D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAc9odHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzU1ODEwODc1MjQ1MDMtLSVFNiU5NiVCMCVFNCVCQSVCQSVFNSU5MCU5MS1SQSVFNyU5QSU4NCVFNiU5QyVBQyVFNSU5QyVCMHNlbGYtcHBhYyVFOCU4NyVBQSVFNyU5QiVCOCVFNSU4NSVCMy0lRTUlQTQlOEQlRTUlODglQjYlRTUlOEQlQjMlRTclOTQlQTgGOwhUOg5zZWFyY2hfaWRJIik3NDMzNDQ0MC02ODk0LTRlYjUtODZjYy0zOWIwODJiZDZjYzcGOwhGOglyYW5raQc6C2xvY2FsZUkiCnpoLWNuBjsIVDoKcXVlcnlJIg7oh6rnm7jlhbMGOwhUOhJyZXN1bHRzX2NvdW50aQLoAw%3D%3D--7b8e293910f1532485670bf36284d271d0fae789
- **作者**: LX57490
- **发布时间/热度**: 6个月前, 得票: 113

## 帖子正文

本帖子展示了如何将两位前辈（KZ79256和BW14163）贡献的两个本地自相关计算代码整合成一个统一、易用的解决方案！下一期我们提供在此代码输出基础上检测PROD的代码！一、登录在代码447行输入账号密码。def main():# 配置参数class cfg:username = ""password = ""data_path = Path('.')二、配置在代码开头这部分，我们可以看到参数配置，有几点注意事项：START_DATE = "10-11"  # 起始日期（MM-DD格式）END_DATE = "10-12"  # 结束日期SHARPE_THRESHOLD = 1.58  # 夏普比率阈值FITNESS_THRESHOLD = 1.5  # 适应度阈值REGION = "EUR"  # 区域ALPHA_NUM = 2000  # Alpha数量1. 日期不要写错哦！注意中午12点分割线！比如说现在是13号中午14点（已过12点），你要筛选12号的，开始10-12，结束10-13，这样12号一整天的alpha都能计算在内。但是你设置，开始10-13，结束10-14，只会有13号12点~14点的alpha。2. Sharpe，Finess可以自行设定阀值，或者自行添加别的条件，选取你想要的alpha！3. 选取数量，会从高到低选取，所以新人前期一般2000也够了，不过注意的一点：数据好以及想跑很多天的顾问们注意，查询次数一万两万+会导致停顿，无法继续查询，所以非必要一天一天查询，最多一小时一万阀值，或者加大筛选条件！4.跑多地区的时候不要忘记换地区哦！三、输出样式输出为.xlsx文件。如下图所示：alpha_id    exp   check_status    Rank    sharpe    self_correlation    ppac_correlation    turnover    fitness    margin    dateCreated    longCount    shortCount    decay    neutralization    neutralization_nameJjjEoVQW   if_else...   Check OK    1    1.99    0.59319975    0.372963776    7.03%    1.57    22.12‱    2025-10-11T13:41:42-04:00    787    766    6    SUBINDUSTRY    SubindustryWjjQ3qeZ   if_else...   Check OK    2    1.98    0.599714359    0.398041108    7.87%    1.57    20.09‱    2025-10-11T13:42:17-04:00    781    772    6    SUBINDUSTRY    Subindustry这里的排序只用了Sharpe从高到低，所以大家对于自己的alpha质量有一个标准判断得分的话，可以自行修改def rank_alphas_by_sharpe(alpha_data)函数，自己设置一个alpha质量标准。这地方我们可以看到我们进行检测后的数据：1. alpha_id：新手配合下方连接食用最好哦，进阶可以接入Alpha lists查询组内相关性。2. exp：咱的alpha也会一并输出。3. check_status：只有check成功的才会放到这上面哦！4. 后面的基础数据就不必多说了，要是想多看到更多的数据添加即可！注：不是PPA也会计算PPAC！四、效果展示PS:本人不知道为什么上传30kb的png不可以，就手打一下，大家凑活看吧！PSS：新来的顾问用跑出来的alpha_id复制到这个网址的后缀就能查看该alpha了！https://platform.worldquantbrain.com/alpha/eg:https://platform.worldquantbrain.com/alpha/JjjEoVQW和前面的xlsx的本地自测相同！CorrelationSelf CorrelationMaximum   Minimum  Last Run: Sun, 10/12/2025, 11:21 PM0.5932    -0.2051Power Pool CorrelationMaximum   Minimum  Last Run: Sun, 10/12/2025, 11:21 PM0.3730    -0.2051五、完整代码最后祝各位顾问月月VF1.0！RA60刀！SA60！日日120刀！！！！高筑墙！广积粮！缓称王！import requestsimport pandas as pdimport loggingimport timeimport picklefrom collections import defaultdictimport numpy as npfrom tqdm import tqdmfrom pathlib import Pathfrom concurrent.futures import ThreadPoolExecutor, as_completedimport jsonimport osimport sysfrom datetime import datetimefrom typing import Optional, Tuple, Dict, List, Unionfrom requests import Response# ===== 参数设置 =====# 第一个算法的参数START_DATE = "10-11"  # 起始日期（MM-DD格式）END_DATE = "10-12"  # 结束日期SHARPE_THRESHOLD = 1.58  # 夏普比率阈值FITNESS_THRESHOLD = 1.5  # 适应度阈值REGION = "EUR"  # 区域ALPHA_NUM = 2000  # Alpha数量# 第二个算法的参数SELF_CORR_TAG = 'SelfCorr'  # 自相关性计算模式PPAC_CORR_TAG = 'PPAC'  # PPAC自相关性计算模式MAX_WORKERS_SELF_CORR = 5  # 自相关性计算的最大线程数# 动态生成输出文件名OUTPUT_FILE = f"alpha_results_{START_DATE}_{REGION}.xlsx"  # 改为Excel格式# ===== 登录函数 =====def sign_in(username, password):s = requests.Session()s.auth = (username, password)try:response = s.post('https://api.worldquantbrain.com/authentication')response.raise_for_status()logging.info("Successfully signed in")return sexcept requests.exceptions.RequestException as e:logging.error(f"Login failed: {e}")return None# ===== 第一个算法的函数 =====def get_submit_alphas(session, start_date, end_date, sharpe_th, fitness_th, region, alpha_num, tag=None):"""获取可以提交的Alpha信息"""output = []  # 用于存储符合条件的Alpha记录count = 0  # 用于统计处理的Alpha数量# 分页获取数据，每次获取100条for i in range(0, alpha_num, 100):print(f"处理偏移量: {i}")# 构造API请求URLbase_url = f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2025-{start_date}T00:00:00-04:00&dateCreated%3C=2025-{end_date}T00:00:00-04:00&is.fitness%3E={fitness_th}&is.sharpe%3E={sharpe_th}&settings.region={region}&order=-is.sharpe&hidden=false&type!=SUPER"# 添加标签筛选条件if tag:base_url += f"&tags={tag}"url = base_urltry:response = session.get(url)  # 发送GET请求if response.status_code == 200:  # 如果请求成功alpha_list = response.json().get("results", [])  # 获取返回的Alpha列表for alpha in alpha_list:# 提取Alpha的各项信息alpha_id = alpha.get("id")name = alpha.get("name")dateCreated = alpha.get("dateCreated")sharpe = alpha.get("is", {}).get("sharpe")fitness = alpha.get("is", {}).get("fitness")turnover = alpha.get("is", {}).get("turnover")margin = alpha.get("is", {}).get("margin")longCount = alpha.get("is", {}).get("longCount")shortCount = alpha.get("is", {}).get("shortCount")decay = alpha.get("settings", {}).get("decay")exp = alpha.get("regular", {}).get("code")# 新增：提取中性化设置neutralization = alpha.get("settings", {}).get("neutralization", "NONE")# 将中性化代码转换为可读名称neutralization_map = {"SUBINDUSTRY": "Subindustry","STATISTICAL": "Statistical","SLOW": "Slow Factors","SLOW_AND_FAST": "Slow + Fast Factors","SECTOR": "Sector","NONE": "None","MARKET": "Market","INDUSTRY": "Industry","FAST": "Fast Factors","CROWDING": "Crowding Factors","COUNTRY": "Country/Region"}neutralization_name = neutralization_map.get(neutralization, neutralization)count += 1  # 增加处理计数# 检查是否可以通过检查checks = alpha.get("is", {}).get("checks", [])checks_df = pd.DataFrame(checks)check_status = "Check FAIL"  # 默认检查状态为失败# 如果存在检查项if not checks_df.empty:if "result" in checks_df.columns:# 如果所有检查项都通过且longCount + shortCount > 100，则标记为Check OKif not any(checks_df["result"].eq("FAIL")) and ((longCount or 0) + (shortCount or 0) > 100):check_status = "Check OK"# 构造记录字典rec = {"alpha_id": alpha_id,"check_status": check_status,"sharpe": sharpe,"turnover": f"{turnover:.2%}" if turnover is not None else None,"fitness": fitness,"margin": f"{margin * 10000:.2f}‱" if margin is not None else None,  # 转换为万分比显示"longCount": longCount,"shortCount": shortCount,"dateCreated": dateCreated,"decay": decay,"exp": exp,"neutralization": neutralization,  # 添加中性化代码"neutralization_name": neutralization_name  # 添加中性化可读名称}# 只有标记为 "Check OK" 的记录才会被保存到输出列表中if check_status == "Check OK":output.append(rec)else:# 如果请求失败，打印错误信息并尝试重新登录print(f"请求失败，状态码: {response.status_code}")print(f"响应内容: {response.text}")except Exception as e:# 捕获异常并打印错误信息print(f"处理偏移量 {i} 时出错: {e}")print(f"总计处理 Alpha 数量: {count}")  # 打印处理总数print(f"符合条件的 Alpha 数量: {len(output)}")return output# ===== 基于夏普比率的排名函数 =====def rank_alphas_by_sharpe(alpha_data):"""根据夏普比率对Alpha进行排名"""if not alpha_data:print("没有符合条件的Alpha数据，无法进行排名")return pd.DataFrame()df = pd.DataFrame(alpha_data)# 按照夏普比率降序排序df = df.sort_values(by='sharpe', ascending=False)# 添加排名列df['Rank'] = range(1, len(df) + 1)# 重新排列列顺序columns_order = ["exp", "check_status", "alpha_id", "Rank", "sharpe", "turnover","fitness", "margin", "dateCreated", "longCount", "shortCount", "decay","neutralization", "neutralization_name"]df = df[columns_order]return df# ===== 第二个算法的函数 =====def save_obj(obj: object, name: str) -> None:with open(name + '.pickle', 'wb') as f:pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)def load_obj(name: str) -> object:with open(name + '.pickle', 'rb') as f:return pickle.load(f)def wait_get(session, url: str, max_retries: int = 10) -> "Response":retries = 0while retries < max_retries:while True:simulation_progress = session.get(url)if simulation_progress.headers.get("Retry-After", 0) == 0:breaktime.sleep(float(simulation_progress.headers["Retry-After"]))if simulation_progress.status_code < 400:breakelse:time.sleep(2 ** retries)retries += 1return simulation_progressdef _get_alpha_pnl(session, alpha_id: str) -> pd.DataFrame:pnl = wait_get(session, "https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl").json()df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])df = df.rename(columns={'date': 'Date', 'pnl': alpha_id})df = df[['Date', alpha_id]]return dfdef get_alpha_pnls(session,alphas: list[dict],alpha_pnls: Optional[pd.DataFrame] = None,alpha_ids: Optional[dict[str, list]] = None) -> Tuple[dict[str, list], pd.DataFrame]:if alpha_ids is None:alpha_ids = defaultdict(list)if alpha_pnls is None:alpha_pnls = pd.DataFrame()new_alphas = [item for item in alphas if item['id'] not in alpha_pnls.columns]if not new_alphas:return alpha_ids, alpha_pnlsfor item_alpha in new_alphas:alpha_ids[item_alpha['settings']['region']].append(item_alpha['id'])fetch_pnl_func = lambda alpha_id: _get_alpha_pnl(session, alpha_id).set_index('Date')with ThreadPoolExecutor(max_workers=10) as executor:results = executor.map(fetch_pnl_func, [item['id'] for item in new_alphas])alpha_pnls = pd.concat([alpha_pnls] + list(results), axis=1)alpha_pnls.sort_index(inplace=True)return alpha_ids, alpha_pnlsdef get_os_alphas(session, limit: int = 100, get_first: bool = False) -> List[Dict]:fetched_alphas = []offset = 0retries = 0total_alphas = 100while len(fetched_alphas) < total_alphas:print(f"Fetching alphas from offset {offset} to {offset + limit}")url = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}&order=-dateSubmitted"res = wait_get(session, url).json()if offset == 0:total_alphas = res['count']alphas = res["results"]fetched_alphas.extend(alphas)if len(alphas) < limit:breakoffset += limitif get_first:breakreturn fetched_alphas[:total_alphas]def calc_self_corr(session,alpha_id: str,os_alpha_rets: pd.DataFrame | None = None,os_alpha_ids: dict[str, str] | None = None,alpha_result: dict | None = None,return_alpha_pnls: bool = False,alpha_pnls: pd.DataFrame | None = None) -> float | tuple[float, pd.DataFrame]:if alpha_result is None:alpha_result = wait_get(session, f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()if alpha_pnls is not None:if len(alpha_pnls) == 0:alpha_pnls = Noneif alpha_pnls is None:_, alpha_pnls = get_alpha_pnls(session, [alpha_result])alpha_pnls = alpha_pnls[alpha_id]alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index) > pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)]self_corr = os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets).max()if np.isnan(self_corr):self_corr = 0return self_corrdef download_data(session, data_path: Path, flag_increment=True):if flag_increment:try:os_alpha_ids = load_obj(str(data_path / 'os_alpha_ids'))os_alpha_pnls = load_obj(str(data_path / 'os_alpha_pnls'))ppac_alpha_ids = load_obj(str(data_path / 'ppac_alpha_ids'))exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]except Exception as e:logging.error(f"Failed to load existing data: {e}")os_alpha_ids = Noneos_alpha_pnls = Noneexist_alpha = []ppac_alpha_ids = []else:os_alpha_ids = Noneos_alpha_pnls = Noneexist_alpha = []ppac_alpha_ids = []if os_alpha_ids is None:alphas = get_os_alphas(session, limit=100, get_first=False)else:alphas = get_os_alphas(session, limit=30, get_first=True)alphas = [item for item in alphas if item['id'] not in exist_alpha]ppac_alpha_ids += [item['id'] for item in alphas for item_match in item['classifications'] ifitem_match['name'] == 'Power Pool Alpha']os_alpha_ids, os_alpha_pnls = get_alpha_pnls(session, alphas, alpha_pnls=os_alpha_pnls, alpha_ids=os_alpha_ids)save_obj(os_alpha_ids, str(data_path / 'os_alpha_ids'))save_obj(os_alpha_pnls, str(data_path / 'os_alpha_pnls'))save_obj(ppac_alpha_ids, str(data_path / 'ppac_alpha_ids'))print(f'新下载的alpha数量: {len(alphas)}, 目前总共alpha数量: {os_alpha_pnls.shape[1]}')return os_alpha_ids, os_alpha_pnlsdef load_data(data_path: Path, tag='PPAC'):os_alpha_ids = load_obj(str(data_path / 'os_alpha_ids'))os_alpha_pnls = load_obj(str(data_path / 'os_alpha_pnls'))ppac_alpha_ids = load_obj(str(data_path / 'ppac_alpha_ids'))if tag == 'PPAC':for item in os_alpha_ids:os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha in ppac_alpha_ids]elif tag == 'SelfCorr':for item in os_alpha_ids:os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha not in ppac_alpha_ids]else:os_alpha_ids = os_alpha_idsexist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]os_alpha_pnls = os_alpha_pnls[exist_alpha]os_alpha_rets = os_alpha_pnls - os_alpha_pnls.ffill().shift(1)os_alpha_rets = os_alpha_rets[pd.to_datetime(os_alpha_rets.index) > pd.to_datetime(os_alpha_rets.index).max() - pd.DateOffset(years=4)]return os_alpha_ids, os_alpha_rets# ===== 新增函数：计算PPAC自相关性 =====def calculate_ppac_correlation_for_alphas(session, data_path, alpha_df, tag=PPAC_CORR_TAG,max_workers=MAX_WORKERS_SELF_CORR):"""为Alpha列表计算PPAC自相关性"""# 下载并加载PPAC自相关性计算所需的基础数据print("\n下载PPAC自相关性计算所需的基础数据...")download_data(session, data_path, flag_increment=True)print("\n加载PPAC自相关性计算数据...")os_alpha_ids, os_alpha_rets = load_data(data_path, tag=tag)# 为每个Alpha计算PPAC自相关性print(f"\n为 {len(alpha_df)} 个Alpha计算PPAC自相关性...")alpha_ids = alpha_df['alpha_id'].tolist()ppac_corr_results = []def process_alpha(alpha_id):try:ppac_corr = calc_self_corr(session=session,alpha_id=alpha_id,os_alpha_rets=os_alpha_rets,os_alpha_ids=os_alpha_ids)return alpha_id, ppac_correxcept Exception as e:print(f"计算Alpha {alpha_id} PPAC自相关性失败: {e}")return alpha_id, None# 使用线程池并行处理with ThreadPoolExecutor(max_workers=max_workers) as executor:futures = [executor.submit(process_alpha, alpha_id) for alpha_id in alpha_ids]for future in tqdm(as_completed(futures), total=len(futures), desc="计算PPAC自相关性"):alpha_id, ppac_corr = future.result()if ppac_corr is not None:ppac_corr_results.append({"alpha_id": alpha_id, "ppac_correlation": ppac_corr})# 创建结果DataFrameppac_corr_df = pd.DataFrame(ppac_corr_results)# 合并到原始DataFrameresult_df = alpha_df.merge(ppac_corr_df, on='alpha_id', how='left')return result_df# ===== 整合函数 =====def calculate_self_correlation_for_alphas(session, data_path, alpha_df, tag=SELF_CORR_TAG,max_workers=MAX_WORKERS_SELF_CORR):"""为Alpha列表计算自相关性"""# 下载并加载自相关性计算所需的基础数据print("\n下载自相关性计算所需的基础数据...")download_data(session, data_path, flag_increment=True)print("\n加载自相关性计算数据...")os_alpha_ids, os_alpha_rets = load_data(data_path, tag=tag)# 为每个Alpha计算自相关性print(f"\n为 {len(alpha_df)} 个Alpha计算自相关性...")alpha_ids = alpha_df['alpha_id'].tolist()self_corr_results = []def process_alpha(alpha_id):try:self_corr = calc_self_corr(session=session,alpha_id=alpha_id,os_alpha_rets=os_alpha_rets,os_alpha_ids=os_alpha_ids)return alpha_id, self_correxcept Exception as e:print(f"计算Alpha {alpha_id} 自相关性失败: {e}")return alpha_id, None# 使用线程池并行处理with ThreadPoolExecutor(max_workers=max_workers) as executor:futures = [executor.submit(process_alpha, alpha_id) for alpha_id in alpha_ids]for future in tqdm(as_completed(futures), total=len(futures), desc="计算自相关性"):alpha_id, self_corr = future.result()if self_corr is not None:self_corr_results.append({"alpha_id": alpha_id, "self_correlation": self_corr})# 创建结果DataFrameself_corr_df = pd.DataFrame(self_corr_results)# 合并到原始DataFrameresult_df = alpha_df.merge(self_corr_df, on='alpha_id', how='left')return result_df# ===== 主函数 =====def main():# 配置参数class cfg:username = ""password = ""data_path = Path('.')# 登录print("登录WorldQuant Brain...")session = sign_in(cfg.username, cfg.password)if not session:print("登录失败，请检查用户名和密码")return# 第一步：获取符合条件的Alphaprint("\n获取符合条件的Alpha...")alpha_data = get_submit_alphas(session=session,start_date=START_DATE,end_date=END_DATE,sharpe_th=SHARPE_THRESHOLD,fitness_th=FITNESS_THRESHOLD,region=REGION,alpha_num=ALPHA_NUM,)if not alpha_data:print("没有找到符合条件的Alpha")return# 第二步：基于夏普比率进行排名print("\n基于夏普比率进行排名...")alpha_df = rank_alphas_by_sharpe(alpha_data)if alpha_df.empty:print("没有找到符合条件的Alpha")return# 第三步：为这些Alpha计算普通自相关性result_df = calculate_self_correlation_for_alphas(session=session,data_path=cfg.data_path,alpha_df=alpha_df,tag=SELF_CORR_TAG)# 第四步：为这些Alpha计算PPAC自相关性result_df = calculate_ppac_correlation_for_alphas(session=session,data_path=cfg.data_path,alpha_df=result_df,  # 使用上一步的结果tag=PPAC_CORR_TAG)# 第五步：保存结果到Excel# 选择需要输出的列output_columns = ["alpha_id", "exp", "check_status", "Rank", "sharpe","self_correlation", "ppac_correlation", "turnover", "fitness", "margin","dateCreated", "longCount", "shortCount", "decay","neutralization", "neutralization_name"]# 确保所有列都存在available_columns = [col for col in output_columns if col in result_df.columns]result_df = result_df[available_columns]# 保存到Excelwith pd.ExcelWriter(OUTPUT_FILE) as writer:result_df.to_excel(writer, sheet_name='Alpha Results', index=False)print(f"\n结果已保存到: {OUTPUT_FILE}")# 打印前10个结果print("\n前10个Alpha的结果:")print(result_df.head(10).to_string(index=False))# 打印统计信息print("\n统计信息:")print(f"Alpha总数: {len(result_df)}")if 'self_correlation' in result_df.columns:print(f"平均自相关性: {result_df['self_correlation'].mean():.4f}")print(f"最大自相关性: {result_df['self_correlation'].max():.4f}")print(f"最小自相关性: {result_df['self_correlation'].min():.4f}")if 'ppac_correlation' in result_df.columns:print(f"平均PPAC自相关性: {result_df['ppac_correlation'].mean():.4f}")print(f"最大PPAC自相关性: {result_df['ppac_correlation'].max():.4f}")print(f"最小PPAC自相关性: {result_df['ppac_correlation'].min():.4f}")# 中性化设置分布统计if 'neutralization_name' in result_df.columns:print("\n中性化设置分布:")print(result_df['neutralization_name'].value_counts())if __name__ == "__main__":main()

---

## 讨论与评论 (16)

### 评论 #1 (作者: LR93609, 时间: 7个月前)

感谢分享，确实不错，开箱即用。如果能够配合GPU使用就更好了。我在user阶段使用过sc的计算，当时电脑一般，计算效率太低了，我总以为是算法问题，现在看来是我狭隘了，这么好的算法，让我浪费太多精力在手动调试上面了。希望后面更多创新和创意。

---

### 评论 #2 (作者: YH25030, 时间: 7个月前)

谢谢分享。这个帖子对新人帮助很大，检测PPAC的相关性节省了不少提交检查时间。

---

### 评论 #3 (作者: CY96125, 时间: 6个月前)

谢谢分享，我个人在此基础上修改拓展出了SA的检测

---

### 评论 #4 (作者: BJ65592, 时间: 6个月前)

谢谢分享，受益良多感觉可以把这些输出的ppac再次互相进行自相关性检测，然后根据总相关性由低到高排名输出，这样应该能避免提交一次之后，因子库更新导致好多因子相关性高交不上，然后需要重新计算一遍相关性的尴尬。

---

### 评论 #5 (作者: ZL15100, 时间: 6个月前)

好用，传参tags要改为tag

---

### 评论 #6 (作者: XG98059, 时间: 6个月前)

没想到我也能用上这么好的东西。

---

### 评论 #7 (作者: YC59838, 时间: 6个月前)

感谢大佬，很好用

---

### 评论 #8 (作者: RL71875, 时间: 5个月前)

好东西啊

---

### 评论 #9 (作者: JQ70858, 时间: 5个月前)

使用原有的check代码，我叫它“一次性check”，但我一直琢磨着，check完达标的因子，你交了一个，实际上有一堆都挂掉了，这个时候人力去辨别就有点浪费时间了，所以如果能做个check按照某些指标（比如自相关）把因子分类，那么这一类交了一个自然就pass了，这绝对能提高工作效率。当然如果能整合pro cor是最好不过的了。感谢作者分享，我这边在用着，check2000个，但是卡在78%半个小时不动了，不知道啥问题。

---

### 评论 #10 (作者: FF65210, 时间: 5个月前)

感谢大佬，我赶紧用上这个提高效率，祝大佬早日GM。

---

### 评论 #11 (作者: HY20507, 时间: 4个月前)

感谢大佬，开箱即用

---

### 评论 #12 (作者: YW86963, 时间: 3个月前)

感谢大佬，帮助节省不少时间

---

### 评论 #13 (作者: HH34943, 时间: 3个月前)

这个自相关检验代码，运行后在本地产生.pickle缓存文件。需要根据region把data path区分开吗，生成data_USA，data_EUR这样的子文件。不然会不会导致当从USA切换到EUR时，代码会读取本地缓存的USA alpha id去匹配EUR的Pnl数据，导致计算的自相关性错误？

---

### 评论 #14 (作者: LX57490, 时间: 3个月前)

@HH34943你上面有你的邮箱，建议删除上个回复，避免其他问题影响你的账号！！！！地区只需要更改你选择  "EUR"   "USA"  就可以了 CSV会携带地区和日期，以及对应PNL，每个地区的自相关都是单独的，所以不必担心这个问题！可能在PPA的相关性上面略有误差，这个是现在无法避免的小误差！！！！

---

### 评论 #15 (作者: HH34943, 时间: 3个月前)

信息有延迟，刚刚才在邮箱收到您的信息，好的感谢解答和提醒

---

### 评论 #16 (作者: YL17960, 时间: 26天前)

非常非常感谢

---

