# 【Community Leader - 因子构造】[缘分一道桥]Alpha 变体生成执行记录与自相关分析工具

- **链接**: 【Community Leader - 因子构造】[缘分一道桥]Alpha 变体生成执行记录与自相关分析工具.md
- **作者**: JX79797
- **发布时间/热度**: 6个月前, 得票: 93

## 帖子正文

**整体介绍**

`run_yuanfen.py` 是一个功能强大的独立 Python 脚本，旨在帮助 WorldQuant BRAIN 平台的用户更高效地探索和管理他们的 Alpha。它主要提供两种核心模式：**变体生成 (Variant)** 和 **Alpha 下载与自相关分析 (Download)**，并支持一个方便的**交互式 (Interactive)** 菜单驱动模式。

****主要功能：****

*   **Alpha 变体生成：** 基于现有 Alpha（特别是已提交的 OS Alpha），自动识别并生成其在不同市场设置（如区域、延迟、Universe）下的有效变体。用户可以选择性地对这些变体进行模拟，并自动记录模拟历史，避免重复工作。新生成的 Alpha 会被打上特定标签并可自定义名称。
*   **Alpha 下载与自相关分析：** 能够根据特定标签（默认为 `run_yuanfen`）下载用户已提交的 Alpha。脚本会计算这些 Alpha 与用户所有 OS Alpha 之间的自相关性（包括与 PPAC Alpha 的相关性），并将结果保存为 CSV 文件。这有助于用户评估 Alpha 的独特性和多样性，优化投资组合。
*   **交互式模式：** 提供一个友好的命令行菜单，引导用户选择功能并输入必要的参数，简化了操作流程。

这个工具对于希望扩展现有 Alpha 覆盖范围、探索新市场机会，以及持续优化 Alpha 组合以提高多样性和降低冗余度的研究员来说，是不可多得的助手。

**依赖环境和文件**

**Python 库依赖：**

您需要安装以下 Python 库：

```
pip install requests numpy pandas beautifulsoup4 lxml pathlib pickle-mixin tqdm
```

****其他依赖：****

*   **`user_info.txt` (可选):** 包含 BRAIN 平台登录凭据的文件（格式：`username: ' [your_email@example.com](mailto:your_email@example.com) '` 和 `password: 'your_password'`）。如果文件不存在或信息不完整，脚本会提示用户在运行时输入。
*   **`alphas/` 目录 (自动创建):** 用于缓存 OS Alpha 的 PnL 数据和 ID 信息，以加速后续的下载和相关性计算。
*   **`submit/` 目录 (自动创建):** 用于存储下载模式下生成的 CSV 结果文件。
*   **`records/yuanfen_history.csv` (自动创建):** 在变体生成模式下，用于记录已模拟的 Alpha 变体历史，防止重复模拟。

**使用说明**

`run_yuanfen.py` 支持交互式和命令行两种使用方式。

**交互式模式 (推荐)**

直接运行脚本，它会提供一个菜单引导您操作：

```
```bashpython run_yuanfen.py -i# 或python run_yuanfen.py # 如果没有指定 --mode 参数，默认进入交互模式```
```

脚本会提示您选择功能（Find Variants 或 Download Tagged Alphas）并输入相应的参数。

**命令行模式**

您可以直接通过命令行参数指定操作模式和详细设置。

****1. 变体生成模式 (`--mode variant`)****

此模式用于查找并模拟现有 Alpha 的变体。

```
*   **通过日期范围查找 Alpha：**    python run_yuanfen.py --mode variant --date-range "2023-01-01" "2023-01-31" --target-region "EUR" --simulate --record-file "records/my_variants_history.csv" --output-file "my_eur_variants.json"    ```    *   `--date-range "START" "END"`：指定 Alpha 的提交日期范围。    *   `--target-region "REGION"`：可选，筛选特定区域的变体。    *   `--simulate`：如果包含此参数，脚本将对找到的变体进行模拟。    *   `--record-file "PATH"`：指定模拟历史记录文件的路径（默认为 `records/yuanfen_history.csv`）。    *   `--output-file "PATH"`：指定变体分析结果输出的 JSON 文件路径（默认为 `yuanfen_results.json`）。
```

```
   **通过 Alpha ID 列表查找 Alpha：**    ```bash    python run_yuanfen.py --mode variant --alpha-ids "alphaId1,alphaId2,alphaId3" --simulate --target-region "USA"    ```    *   `--alpha-ids "ID1,ID2,..."`：逗号分隔的 Alpha ID 列表。
```

****2. 下载模式 (`--mode download`)****

此模式用于下载特定标签的 Alpha 并计算自相关性。

```
```bashpython run_yuanfen.py --mode download --tag "my_custom_tag" --target-region "USA"```*   `--tag "TAG_NAME"`：指定要下载的 Alpha 标签（默认为 `run_yuanfen`）。*   `--target-region "REGION"`：可选，筛选特定区域的 Alpha。
```

**示例**

**![图片](images/img_ad4e65678d.png)**

**登录凭据：**

脚本会尝试从 `user_info.txt` 文件中读取您的 BRAIN 平台用户名和密码。如果读取失败或文件不存在，它将提示您在命令行中输入。

**代码分享**

```
# -*- coding: utf-8 -*-"""Standalone script for BRAIN Alpha Variant Generation ("Yuanfen Yidao Qiao")and downloading tagged alphas with self-correlation.This script provides a command-line interface for two main modes:1. 'variant': Finds and optionally simulates new alpha variants based on an existing alpha.2. 'download': Fetches alphas with a specific tag, calculates their self-correlation,and saves them to a sorted CSV file.3. 'interactive': A menu-driven interactive mode to guide the user.Features:- Login with email/password from user_info.txt or prompt.- Mode 'variant':- Fetch submitted OS alphas by date range or by specific IDs.- Find all possible setting variants for each alpha.- Filter variants for a specific target region.- Optionally, run simulations for the filtered variants.- Record simulation history to avoid re-running.- Set name and tags for newly created alphas.- Mode 'download':- Fetch all alphas with the 'run_yuanfen' tag.- Optionally filter by a specific region.- Calculate self-correlation for each alpha against all other OS alphas.- Save results to a CSV file in the `submit/` directory.- Sort the CSV by region, then by self-correlation (ascending).Example Usage:# --- Interactive Mode ---python run_yuanfen.py# --- Variant Mode (Command Line) ---python run_yuanfen.py --mode variant --alpha-ids "alphaId1,alphaId2" \--target-region "EUR" --simulate# --- Download Mode (Command Line) ---python run_yuanfen.py --mode download --target-region "USA""""from __future__ import annotationsimport argparseimport getpassimport jsonimport loggingimport osimport reimport sysimport threadingimport timeimport picklefrom collections import defaultdictfrom datetime import datetime, timedeltafrom typing import Dict, List, Optional, Sequence, Tuple, Unionfrom urllib.parse import urljoinfrom concurrent.futures import ThreadPoolExecutorimport copy # 导入 copy 模块import numpy as npimport pandas as pdimport requestsfrom pathlib import Path # 导入 Path# For get_platform_setting_options and validate_settingfrom itertools import product# --- Start of Combined Lib ---logger = logging.getLogger("yuanfen_standalone")class SingleSession(requests.Session):_instance=None_lock=threading.Lock()def__new__(cls, *args, **kwargs):ifcls._instanceisNone:withcls._lock:ifcls._instanceisNone:cls._instance=super().__new__(cls)returncls._instancebrain_api_url = os.environ.get("BRAIN_API_URL", "https://api.worldquantbrain.com")def wait_get(sess, url: str, params: Optional[Dict] = None, max_retries: int = 1000) -> Optional[requests.Response]:"""Performs a GET request with retry logic and exponential backoff.Returns None if all retries fail, instead of raising an error."""forattemptinrange(max_retries):try:response=sess.get(url, params=params)if"Retry-After"inresponse.headers:sleep_time=float(response.headers["Retry-After"])time.sleep(sleep_time)continueresponse.raise_for_status() # Raise for HTTP errors, but allow 404 to be handled by callerreturnresponseexceptrequests.exceptions.HTTPErrorase:ife.response.status_code==404: # Special handling for 404slogger.warning(f"Request to {url} returned 404 (Not Found). Attempt {attempt+1}/{max_retries}. Returning response for caller to handle.")returne.response# Return the 404 responseelse:logger.warning(f"Request to {url} failed with HTTP error {e.response.status_code} (attempt {attempt+1}/{max_retries}): {e}")exceptrequests.exceptions.RequestExceptionase:logger.warning(f"Request to {url} failed (attempt {attempt+1}/{max_retries}): {e}")# Exponential backoff for retriestime.sleep(2**attempt)logger.error(f"Failed to get URL {url} after {max_retries} retries. Returning None.")returnNone# Return None after all retries faildef start_simulation(s: SingleSession, simulate_data: Union[list[dict], dict]) -> requests.Response:returns.post(f"{brain_api_url}/simulations", json=simulate_data)def get_simulation_result_json(s: requests.Session, alpha_id: str) -> dict:ifnotalpha_id: return {}resp=wait_get(s, f"{brain_api_url}/alphas/{alpha_id}")ifrespisNoneorresp.status_code==404: return {} # Handle 404 specifically for alpha details or None responsereturnresp.json()def simulation_progress(s: SingleSession, simulate_response: requests.Response) -> dict:ifsimulate_response.status_code//100!=2:logger.warning(f'Simulation start failed: {simulate_response.status_code} - {simulate_response.text}')return {"completed": False, "message": f"Start failed: {simulate_response.status_code} - {simulate_response.text}"}progress_url=simulate_response.headers["Location"]whileTrue:progress_resp=wait_get(s, progress_url)ifprogress_respisNone: # wait_get failed after all retrieslogger.error(f"Simulation progress URL {progress_url} failed to respond after multiple retries. Assuming simulation failed.")return {"completed": False, "message": "Simulation progress not found after multiple retries."}ifprogress_resp.status_code==404: # Handle 404 for progress URLlogger.error(f"Simulation progress URL {progress_url} returned 404. Assuming simulation failed.")return {"completed": False, "message": "Simulation progress not found."}progress_json=progress_resp.json()ifprogress_json.get("status") in ("COMPLETE", "ERROR"):ifprogress_json.get("status") =="ERROR":logger.error(f"Simulation failed: {progress_json}")return {"completed": False, "message": json.dumps(progress_json)}alpha_id=progress_json.get("alpha")ifnotalpha_id:logger.warning(f"Simulation completed but no alpha ID found: {progress_json}")return {"completed": False, "message": "Simulation completed but no alpha ID."}final_result=get_simulation_result_json(s, alpha_id)return {"completed": True, "result": final_result} iffinal_resultelse {"completed": False, "message": "Failed to retrieve final result."}else:# If status is not COMPLETE or ERROR, continue pollinglogger.info(f"Simulation {progress_url} is still {progress_json.get('status', 'processing')}. Retrying after a short delay.")time.sleep(5) # Poll every 5 seconds# --- Start of self_corr_checkV3 logic (copied) ---def save_obj(obj: object, name: str) -> None:"""保存对象到文件中，以 pickle 格式序列化。Args:obj (object): 需要保存的对象。name (str): 文件名（不包含扩展名），保存的文件将以 '.pickle' 为扩展名。Returns:None: 此函数无返回值。Raises:pickle.PickleError: 如果序列化过程中发生错误。IOError: 如果文件写入过程中发生 I/O 错误。"""os.makedirs(os.path.dirname(name), exist_ok=True)withopen(name+'.pickle', 'wb') asf:pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)def load_obj(name: str) -> object:"""加载指定名称的 pickle 文件并返回其内容。此函数会打开一个以 `.pickle` 为扩展名的文件，并使用 `pickle` 模块加载其内容。Args:name (str): 不带扩展名的文件名称。Returns:object: 从 pickle 文件中加载的 Python 对象。Raises:FileNotFoundError: 如果指定的文件不存在。pickle.UnpicklingError: 如果文件内容无法被正确反序列化。"""withopen(name+'.pickle', 'rb') asf:returnpickle.load(f)def _get_alpha_pnl(sess,alpha_id: str) -> pd.DataFrame:"""获取指定 alpha 的 PnL数据，并返回一个包含日期和 PnL 的 DataFrame。此函数通过调用 WorldQuant Brain API 获取指定 alpha 的 PnL 数据，并将其转换为 pandas DataFrame 格式，方便后续数据处理。Args:alpha_id (str): Alpha 的唯一标识符。Returns:pd.DataFrame: 包含日期和对应 PnL 数据的 DataFrame，列名为 'Date' 和 alpha_id。"""pnl=wait_get(sess, "https://api.worldquantbrain.com/alphas/"+alpha_id+"/recordsets/pnl").json()df=pd.DataFrame(pnl['records'], columns=[item['name'] foriteminpnl['schema']['properties']])# 立即转换日期格式df['date'] =pd.to_datetime(df['date']).dt.normalize()df=df.rename(columns={'date':'Date', 'pnl':alpha_id})df=df[['Date', alpha_id]]returndfdef get_alpha_pnls(sess,alphas: list[dict],alpha_pnls: Optional[pd.DataFrame] =None,alpha_ids: Optional[dict[str, list]] =None) -> Tuple[dict[str, list], pd.DataFrame]:"""获取 alpha 的 PnL 数据，并按区域分类 alpha 的 ID。Args:alphas (list[dict]): 包含 alpha 信息的列表，每个元素是一个字典，包含 alpha 的 ID 和设置等信息。alpha_pnls (Optional[pd.DataFrame], 可选): 已有的 alpha PnL 数据，默认为空的 DataFrame。alpha_ids (Optional[dict[str, list]], 可选): 按区域分类的 alpha ID 字典，默认为空字典。Returns:Tuple[dict[str, list], pd.DataFrame]:- 按区域分类的 alpha ID 字典。- 包含所有 alpha 的 PnL 数据的 DataFrame。"""ifalpha_idsisNone:alpha_ids=defaultdict(list)ifalpha_pnlsisNone:alpha_pnls=pd.DataFrame()new_alphas= [itemforiteminalphasifitem['id'] notinalpha_pnls.columns]ifnotnew_alphas:returnalpha_ids, alpha_pnlsforitem_alphainnew_alphas:alpha_ids[item_alpha['settings']['region']].append(item_alpha['id'])fetch_pnl_func=lambdaalpha_id: _get_alpha_pnl(sess, alpha_id).set_index('Date')withThreadPoolExecutor(max_workers=10) asexecutor:results=executor.map(fetch_pnl_func, [item['id'] foriteminnew_alphas])alpha_pnls=pd.concat([alpha_pnls] +list(results), axis=1)# 确保索引是 datetime 类型alpha_pnls.index=pd.to_datetime(alpha_pnls.index).normalize()alpha_pnls.sort_index(inplace=True)returnalpha_ids, alpha_pnlsclass cfg:# 使用示例username=""password=""data_path=Path('alphas')_data_cache = {}_cache_lock = threading.RLock()def load_data(tag=None):"""加载数据并缓存，减少重复加载。线程安全版本。"""# 使用缓存加速重复调用cache_key=str(tag)with_cache_lock:ifcache_keyin_data_cache:# 返回缓存数据的深拷贝，避免多线程修改共享对象returncopy.deepcopy(_data_cache[cache_key][0]), _data_cache[cache_key][1].copy()os_alpha_ids=load_obj(str(cfg.data_path/'os_alpha_ids'))os_alpha_pnls=load_obj(str(cfg.data_path/'os_alpha_pnls'))ppac_alpha_ids=load_obj(str(cfg.data_path/'ppac_alpha_ids'))iftag=='PPAC':foriteminos_alpha_ids:os_alpha_ids[item] = [alphaforalphainos_alpha_ids[item] ifalphainppac_alpha_ids]eliftag=='SelfCorr':foriteminos_alpha_ids:os_alpha_ids[item] = [alphaforalphainos_alpha_ids[item] ifalphanotinppac_alpha_ids]else:os_alpha_ids=os_alpha_ids# 不指定tag时使用全量数据# 处理数据...(原有代码)exist_alpha= [alphaforidsinos_alpha_ids.values() foralphainids]os_alpha_pnls=os_alpha_pnls[exist_alpha]os_alpha_pnls.columns =os_alpha_pnls.columns.astype(str)# 确保加载的 pnl 数据索引是标准化的 datetimeos_alpha_pnls.index =pd.to_datetime(os_alpha_pnls.index).normalize()os_alpha_rets=os_alpha_pnls-os_alpha_pnls.ffill().shift(1)os_alpha_rets=os_alpha_rets[pd.to_datetime(os_alpha_rets.index)>pd.to_datetime(os_alpha_rets.index).max() -pd.DateOffset(years=4)]# 缓存结果的副本，避免后续修改影响缓存# 将 defaultdict 转换为 dict 再缓存，以避免 unhashable type 错误_data_cache[cache_key] = (dict(copy.deepcopy(os_alpha_ids)), os_alpha_rets.copy())# 返回原始数据的副本# 确保返回的是 dict 而不是 defaultdictreturncopy.deepcopy(_data_cache[cache_key][0]), _data_cache[cache_key][1].copy()def calc_self_corr(sess, alpha_id, os_alpha_rets=None, os_alpha_ids=None, alpha_result=None, return_alpha_pnls=False, alpha_pnls=None):ifalpha_resultisNone:alpha_result=wait_get(sess, f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()ifalpha_pnlsisnotNone:iflen(alpha_pnls) ==0:alpha_pnls=Noneifalpha_pnlsisNone:_, alpha_pnls_df=get_alpha_pnls(sess, [alpha_result])ifalpha_idinalpha_pnls_df.columns:alpha_pnls=alpha_pnls_df[alpha_id]else:alpha_pnls=pd.Series(dtype='float64') # Or handle error appropriately# 确保传入的 alpha_pnls 索引是标准化的 datetimeifnotisinstance(alpha_pnls.index, pd.DatetimeIndex):alpha_pnls.index=pd.to_datetime(alpha_pnls.index).normalize()alpha_rets=alpha_pnls-alpha_pnls.ffill().shift(1)alpha_rets=alpha_rets.replace(0, 1e-14) # 替换零值为极小正数（新增）alpha_rets=alpha_rets.dropna() # 移除缺失值（新增）# 新增：确保 alpha_rets 也只使用最近四年的数据alpha_rets=alpha_rets[pd.to_datetime(alpha_rets.index) >pd.to_datetime(alpha_rets.index).max() -pd.DateOffset(years=4)]region=alpha_result['settings']['region']# 新增：清洗 os_alpha_rets（删除含 NaN 的列，过滤标准差过小的列）ifos_alpha_retsisnotNone:os_alpha_rets_clean=os_alpha_rets[os_alpha_ids[region]].dropna(axis=1, thresh=len(os_alpha_rets)*0.7)# 新增：检查筛选后的数据是否为空ifos_alpha_rets_clean.empty:print(f"警告：region={region} 筛选后无有效数据，原始ID数量={len(os_alpha_ids[region])}")valid_columns=os_alpha_ids[region]else:std_devs=os_alpha_rets_clean.std()valid_columns=std_devs.index # 保留所有列# 仅在DataFrame非空时执行列筛选os_alpha_rets_clean=os_alpha_rets_clean[valid_columns]# 更新 os_alpha_ids 为有效列对应的 alpha_id（假设 os_alpha_ids 结构为 {region: [alpha_ids]}）# 新增：打印ID匹配情况existing_columns=set(os_alpha_rets.columns)missing_ids= [alphaforalphainos_alpha_ids[region] ifalphanotinexisting_columns]os_alpha_ids[region] = [alphaforalphainos_alpha_ids[region] ifalphainvalid_columns]else:os_alpha_rets_clean=pd.DataFrame()# 新增：检查有效数据是否存在ifos_alpha_rets_clean.empty:print(f"已提交为空，无有效参考数据或自身收益率数据，相关性无法计算，默认0.01")max_corr_id=Nonemax_corr_value=np.nan_to_num(0.01, nan=0.0) # 确保默认值不为NaNelifalpha_rets.empty:print(f"警告：{alpha_id} 无有效参考数据或自身收益率数据，相关性无法计算")max_corr_id=Nonemax_corr_value=np.nan_to_num(0, nan=0.0) # 确保默认值不为NaNelse:# 计算重叠日期common_dates=os_alpha_rets_clean.index.intersection(alpha_rets.index)iflen(common_dates) ==0:print(f"警告：{alpha_id} 与参考数据无重叠日期，相关性无法计算")max_corr_id=Nonemax_corr_value=np.nan_to_num(0, nan=0.0) # 确保默认值不为NaNelse:# 使用清洗后的数据计算相关系数os_alpha_rets_aligned, alpha_rets_aligned=os_alpha_rets_clean.align(alpha_rets, join='inner', axis=0)corr_series=os_alpha_rets_aligned.corrwith(alpha_rets_aligned)# 处理全 NA 情况ifcorr_series.isna().all():print(f"警告：{alpha_id} 相关系数序列全为 NA，无最大值")max_corr_id=Nonemax_corr_value=np.nan_to_num(0, nan=0.0) # 确保默认值不为NaNelse:# 显式跳过 NA 以避免 FutureWarningmax_corr_id=corr_series.idxmax(skipna=True)max_corr_value=np.nan_to_num(corr_series.max(), nan=0.0) # 确保最大值不为NaN# 打印最大相关性的 alpha_id 和值ifmax_corr_idisNone:print(f"与 {alpha_id} 最大相关性的 alpha_id 是 {max_corr_id}，相关性值为 {max_corr_value}")ifalpha_resultandalpha_result['settings']['region'] inos_alpha_idsandnotos_alpha_rets.empty andnotalpha_rets.empty:try:debug_corr_series=os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets)print(debug_corr_series.sort_values(ascending=False).round(4).head(1))exceptExceptionase:print(f"Debug print error: {e}")self_corr=max_corr_value# 确保 self_corr 最终不是 NaN，将其替换为 0self_corr=np.nan_to_num(self_corr, nan=0.0)ifreturn_alpha_pnls:returnself_corr, alpha_pnlselse:returnself_corr# --- Start of main script logic ---BASE_URL = "https://api.worldquantbrain.com"def brain_login(username: str, password: str, max_retries: int = 3) -> requests.Session:session=SingleSession()session.auth= (username, password)forattemptinrange(1, max_retries+1):try:response=session.post(f"{BASE_URL}/authentication")ifresponse.status_code==requests.codes.unauthorized:ifresponse.headers.get("WWW-Authenticate") =="persona":location=response.headers.get("Location", "")print(f"Biometric authentication required. Please open this URL, complete login, then re-run: {urljoin(response.url, location)}")sys.exit(1)raiseRuntimeError("Invalid username or password.")response.raise_for_status()logger.info("Authentication successful.")returnsessionexceptrequests.HTTPErrorasexc:ifattempt>=max_retries: raiseexctime.sleep(2)raiseRuntimeError("Authentication failed after retries.")def get_platform_setting_options(session: requests.Session) -> pd.DataFrame:"""Retrieves and organizes instrument type, region, and delay data into a DataFrame."""settings_options=session.options(f"{BASE_URL}/simulations").json()['actions']['POST']['settings']['children']data= [{settings_options[key]['label']: settings_options[key]['choices']}forkeyinsettings_options.keys()ifsettings_options[key]['type'] =='choice']instrument_type_data= {}region_data= {}universe_data= {}delay_data= {}neutralization_data= {}foritemindata:if'Instrument type'initem:instrument_type_data=item['Instrument type']elif'Region'initem:region_data=item['Region']['instrumentType']elif'Universe'initem:universe_data=item['Universe']['instrumentType']elif'Delay'initem:delay_data=item['Delay']['instrumentType']elif'Neutralization'initem:neutralization_data=item['Neutralization']['instrumentType']data_list= []forinstrument_typeininstrument_type_data:forregioninregion_data[instrument_type['value']]:fordelayindelay_data[instrument_type['value']]['region'][region['value']]:row= {'InstrumentType': instrument_type['value'], 'Region': region['value'], 'Delay': delay['value']}row['Universe'] = [item['value'] foriteminuniverse_data[instrument_type['value']]['region'][region['value']]]row['Neutralization'] = [item['value'] foriteminneutralization_data[instrument_type['value']]['region'][region['value']]]data_list.append(row)df=pd.DataFrame(data_list).sort_values(by=['InstrumentType', 'Region', 'Delay'], ascending=False, ignore_index=True)returndfdef validate_setting(setting: Dict, options_df: Optional[pd.DataFrame]) -> bool:"""Check if a setting combination is valid according to simulation options."""ifoptions_dfisNoneoroptions_df.empty:returnTrue# Skip validation if options not availableinst_type=setting.get("instrumentType", "EQUITY")region=setting.get("region")delay=setting.get("delay")universe=setting.get("universe")try:delay=int(delay)except (ValueError, TypeError):pass# Iterate to find matchfor_, rowinoptions_df.iterrows():row_inst=row.get('InstrumentType')row_region=row.get('Region')row_delay=row.get('Delay')try:row_delay=int(row_delay)except (ValueError, TypeError):passifrow_inst==inst_typeandrow_region==regionandrow_delay==delay:# Check universevalid_universes=row.get('Universe', [])ifisinstance(valid_universes, list) anduniverseinvalid_universes:returnTruereturnFalsedef get_all_user_alphas(session: requests.Session) -> List[Dict]:all_alphas, offset, limit= [], 0, 100logger.info("Fetching all OS alphas for correlation reference...")whileTrue:try:resp=wait_get(session, f"{BASE_URL}/users/self/alphas", params={"stage": "OS", "limit": limit, "offset": offset})data=resp.json() # FIX: Assign resp.json() to data firstresults=data.get("results", [])ifnotresults: breakall_alphas.extend(results)offset+=len(results)logger.info(f"Fetched {len(all_alphas)} OS alphas so far...")iflen(results) <limit: breakexceptExceptionase:logger.error(f"Failed to fetch alphas at offset {offset}: {e}")breakreturnall_alphas# 复制自 machine_lib.py 的 get_alphas 函数，并重命名def _get_unsubmitted_alphas_from_api(s, start_date, end_date, sharpe_th, fitness_th, usage, tag: str = '', color_exclude='', region=None):alpha_list= []next_alphas= []start_date_str=start_date.strftime('%Y-%m-%d') ifhasattr(start_date, 'strftime') elsestart_dateend_date_str=end_date.strftime('%Y-%m-%d') ifhasattr(end_date, 'strftime') elseend_datecommon_params= {"limit": 100,"tag": tag,"status": "UNSUBMITTED","dateCreated>": f"{start_date_str}T00:00:00-04:00","dateCreated<": f"{end_date_str}T00:00:00-04:00","color!": color_exclude,"order": "-is.sharpe","hidden": "false"}ifregion:common_params["settings.region"] =region# Positive alphasi=0whileTrue:params_positive= {**common_params, "offset": i, "is.sharpe>": sharpe_th, "is.fitness>": fitness_th}response=s.get(f"https://api.worldquantbrain.com/users/self/alphas", params=params_positive)try:response.raise_for_status()logger.info(f"Fetching positive alphas (offset {i}): {response.url}")i+=100json_response=response.json()ifnotisinstance(json_response, dict) or"count"notinjson_response:raiseValueError(f"Unexpected API response format: {json_response}")count=json_response["count"]logger.info(f"count: {count}")results=json_response.get("results", [])ifnotresults:logger.info(f"No positive alphas found for tag={tag}, region={region}, sharpe>={sharpe_th}, fitness>={fitness_th}")alpha_list.extend(results)ifi>=countori==9900:breaktime.sleep(0.01)exceptExceptionase:logger.error(f"Failed to get positive alphas: {e}")i-=100s=brain_login(s.auth[0], s.auth[1])# Negative alphasifusage!="submit":i=0whileTrue:params_negative= {**common_params, "offset": i, "is.sharpe<": -sharpe_th, "is.fitness<": -fitness_th}response=s.get(f"https://api.worldquantbrain.com/users/self/alphas", params=params_negative)try:response.raise_for_status()logger.info(f"Fetching negative alphas (offset {i}): {response.url}")json_response=response.json()ifnotisinstance(json_response, dict) or"count"notinjson_response:raiseValueError(f"Unexpected API response format: {json_response}")count=json_response["count"]results=json_response.get("results", [])ifnotresults:logger.info(f"No negative alphas found for tag={tag}, region={region}, sharpe<=-{sharpe_th}, fitness<=-{fitness_th}")ifi>=countori==9900:breakalpha_list.extend(results)i+=100exceptExceptionase:logger.error(f"Failed to get negative alphas: {e}")s=brain_login(s.auth[0], s.auth[1])ifnotalpha_list:logger.info(f"No alphas found in total for tag={tag}, region={region}. Returning empty lists.")return {"next": []}ifusage!="submit":forjinrange(len(alpha_list)):alpha_id=alpha_list[j]["id"]# name = alpha_list[j]["name"] # 'name' is not used in rec, so commented out# dateCreated = alpha_list[j]["dateCreated"] # 'dateCreated' is not used in rec, so commented outsharpe=alpha_list[j]["is"]["sharpe"]fitness=alpha_list[j]["is"]["fitness"]turnover=alpha_list[j]["is"]["turnover"]margin=alpha_list[j]["is"]["margin"]longCount=alpha_list[j]["is"]["longCount"]shortCount=alpha_list[j]["is"]["shortCount"]decay=alpha_list[j]["settings"]["decay"]# region = alpha_list[j]["settings"]["region"] # 'region' is not used in rec, so commented outif'regular'inalpha_list[j]:exp=alpha_list[j]['regular']['code']elif'combo'inalpha_list[j]:exp=alpha_list[j]['combo']['code']else:exp=""rec= [alpha_id, exp, sharpe, turnover, fitness, margin, longCount, shortCount, alpha_list[j]["dateCreated"], decay]next_alphas.append(rec)output_dict= {"next": next_alphas}logger.info(f"count: {len(next_alphas)}")returnoutput_dictdef _get_unsubmitted_alphas_details(session: requests.Session, tag: str, target_region: Optional[str], cached_alphas_details: Optional[Dict[str, Dict]] = None) -> Tuple[List[Dict], Dict[str, Dict]]:logger.info(f"Fetching unsubmitted alphas with tag: '{tag}' for region '{target_regioniftarget_regionelse'ALL'}'...")ifcached_alphas_detailsisNone:cached_alphas_details= {}all_unsubmitted_alphas_details= []days=30sharpe=0.9fitness=0.5today=datetime.now().date()start_date=today-timedelta(days=days)end_date=today+timedelta(days=1)for_per=_get_unsubmitted_alphas_from_api(session, start_date, end_date,sharpe, fitness,"track", tag=tag, color_exclude="RED", region=target_region)alpha_id_list= [item[0] foriteminfor_per.get('next', [])] # Removed 'decay'foralpha_idinalpha_id_list:ifalpha_idincached_alphas_details:full_details=cached_alphas_details[alpha_id]else:full_details=get_simulation_result_json(session, alpha_id)iffull_details:cached_alphas_details[alpha_id] =full_detailsiffull_details:alpha_tags=full_details.get('tags', [])alpha_region_from_details=full_details.get('settings', {}).get('region')iftaginalpha_tagsand (target_regionisNoneoralpha_region_from_details==target_region):all_unsubmitted_alphas_details.append(full_details)logger.info(f"Found {len(all_unsubmitted_alphas_details)} unsubmitted alphas with tag '{tag}' for region '{target_regioniftarget_regionelse'ALL'}'.")returnall_unsubmitted_alphas_details, cached_alphas_detailsdef fetch_alphas_by_date_range(session: requests.Session, start_date: str, end_date: str) -> List[Dict]:logger.info(f"Fetching alphas from {start_date} to {end_date}...")start_iso, end_iso=f"{start_date}T00:00:00Z", f"{end_date}T23:59:59Z"all_alphas, offset, limit= [], 0, 100whileTrue:params= {"stage": "OS", "order": "-dateSubmitted", "dateSubmitted>": start_iso, "dateSubmitted<": end_iso, "limit": limit, "offset": offset}resp=wait_get(session, f"{BASE_URL}/users/self/alphas", params=params)data=resp.json() # FIX: Assign resp.json() to data firstresults=data.get("results", [])ifnotresults: breakall_alphas.extend(results)offset+=len(results)iflen(results) <limit: breakreturnall_alphasdef fetch_alphas_by_ids(session: requests.Session, alpha_ids: List[str]) -> List[Dict]:logger.info(f"Fetching {len(alpha_ids)} alphas by ID...")return [get_simulation_result_json(session, alpha_id.strip()) foralpha_idinalpha_idsifalpha_id.strip()]def fetch_operators(session: requests.Session) -> List[Dict]:returnwait_get(session, f"{BASE_URL}/operators").json()def _dedupe(seq: Sequence[str]) -> List[str]:returnlist(dict.fromkeys(seq))def _extract_expression(alpha: Dict) -> Optional[str]:forkeyin ("regular", "combo", "selection"):if (block:=alpha.get(key)) andisinstance(block, dict):ifexpr:=block.get("expression") orblock.get("code"):returnexprreturnNonedef parse_expression(expression: str, operator_names: Sequence[str]) -> Tuple[List[str], List[str]]:"""Split an expression into operators and datafields using a token scan."""# Remove C-style comments /* ... */expression=re.sub(r"/\*[\s\S]*?\*/", "", expression)# Remove Python-style comments # ...expression=re.sub(r"#.*", "", expression)operator_set=set(operator_names)tokens=re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression)found_ops: List[str] = []found_fields: List[str] = []# Add known built-in keywords/variables to skip_tokens# These are often part of the expression language itself, not queryable datafieldsskip_tokens= {"if", "else", "true", "false", "nan", "inf", "alpha", "percentage", "p", "limit_volume","factor","longscale","value"}fortokenintokens:iftokeninskip_tokens:continueiftokeninoperator_set:found_ops.append(token)else:found_fields.append(token)logger.info(f"Parsed expression. Found operators: {_dedupe(found_ops)}, Datafields: {_dedupe(found_fields)}")return_dedupe(found_ops), _dedupe(found_fields)def get_datafield_availability(session: requests.Session, field_name: str) -> Dict:"""Fetch detail for a datafield and summarize other available settings."""resp=wait_get(session, f"{BASE_URL}/data-fields/{field_name}")ifrespisNoneorresp.status_code==404: # Handle 404 specifically for datafield availability or None responselogger.warning(f"Datafield '{field_name}' not found (404). Returning empty availability.")info_result= {"detail": {}, "availability": [], "error": "Datafield not found."}logger.info(f"Availability info for field '{field_name}': {info_result.get('availability')}")returninfo_resulttry:detail=resp.json()availability_candidates= []forkeyin ("availability","availabilities","availableSettings","availabilityList","regionAvailability","settings","data",):value=detail.get(key)ifisinstance(value, list):availability_candidates.extend(value)elifisinstance(value, dict):nested=value.get("availability") orvalue.get("items") orvalue.get("list")ifisinstance(nested, list):availability_candidates.extend(nested)def_pick(d, keys, default_val=None):forkinkeys:val=d.get(k)ifvalisnotNone:returnvalreturndefault_valnormalized_items= []foriteminavailability_candidates:ifnotisinstance(item, dict):continuenormalized_items.append({"instrumentType": _pick(item, ["instrumentType", "instrument_type"], "EQUITY"), # 默认设置为 EQUITY"region": _pick(item, ["region", "regionCode"]),"delay": _pick(item, ["delay", "lag"]),"universe": _pick(item, ["universe", "universeName"]),})# Deduplicate normalized combos.normalized_json_strings=_dedupe([json.dumps(x, sort_keys=True) for x in normalized_items if any(x.values())])combos= [json.loads(s) forsinnormalized_json_strings]info_result= {"detail": detail, "availability": combos}logger.info(f"Availability info for field '{field_name}': {info_result.get('availability')}")returninfo_resultexceptExceptionase:logger.error(f"Error parsing datafield availability for '{field_name}': {e}", exc_info=True)info_result= {"availability": [], "error": "Datafield not found or error parsing."}logger.info(f"Availability info for field '{field_name}': {info_result.get('availability')}")returninfo_resultdef find_common_availabilities(session: requests.Session, datafields: List[str]) -> List[Dict]:ifnotdatafields:logger.info("No datafields provided to find common availabilities.")return []common_settings=Noneforfieldindatafields:info=get_datafield_availability(session, field)ifinfo.get("error") ornotinfo.get("availability"):logger.warning(f"Field '{field}' has no availability info (likely local var). Skipping constraint.")continuecurrent_settings=set()foritemininfo["availability"]:normalized_item= {"instrumentType": item.get("instrumentType"),"region": item.get("region"),"delay": item.get("delay"),"universe": item.get("universe"),}current_settings.add(json.dumps(normalized_item, sort_keys=True))ifcommon_settingsisNone:common_settings=current_settingselse:common_settings=common_settings.intersection(current_settings)ifnotcommon_settings:logger.info(f"Intersection empty after checking field '{field}'.")break# Optimized: if intersection is empty, no need to check further fieldsifcommon_settingsisNone:logger.info("No common settings found across all valid datafields.")return []result= [json.loads(s) forsincommon_settings]logger.info(f"Final common availabilities: {result}")result.sort(key=lambdax: (x.get("region", ""), x.get("universe", ""), x.get("delay", 0)))returnresultdef get_alpha_variants(session: requests.Session, alpha: Dict, operators: List[Dict], simulation_options: Optional[pd.DataFrame] = None, target_region: Optional[str] = None) -> Dict:alpha_id=alpha.get("id", "Unknown")alpha_type=alpha.get("type")ifalpha_type!="REGULAR":return {"id": alpha_id, "valid": False, "reason": "Not REGULAR type", "variants": []}expr=_extract_expression(alpha)ifnotexpr:return {"id": alpha_id, "valid": False, "reason": "No expression found", "variants": []}operator_names= [op.get("name", "") foropinoperators]_, fields=parse_expression(expr, operator_names)ifnotfields:return {"id": alpha_id, "valid": False, "reason": "No datafields found", "variants": []}common_settings=find_common_availabilities(session, fields)ifnotcommon_settings:return {"id": alpha_id, "valid": False, "reason": "No common settings", "variants": []}original_settings=alpha.get("settings", {})valid_variants= []fornew_settingincommon_settings:# Validate against simulation options if providedifsimulation_optionsisnotNone:ifnotvalidate_setting(new_setting, simulation_options):logger.info(f" Skipping: Invalid simulation setting combination ({new_setting.get('region')}/{new_setting.get('universe')}).")continueiftarget_regionandnew_setting.get("region") !=target_region:continueis_duplicate=Trueforkeyin ["region", "universe", "delay", "instrumentType"]:val_orig=str(original_settings.get(key, ""))val_new=str(new_setting.get(key, ""))ifval_orig!=val_new:is_duplicate=Falsebreakifnotis_duplicate:merged_settings=original_settings.copy()merged_settings.update(new_setting)if"language"notinmerged_settings:merged_settings["language"] ="FASTEXPR"ifmerged_settings.get("region") in ["ASI", "JPN", "HKG", "KOR", "TWN"]:merged_settings["maxTrade"] ="ON"payload= {"type": "REGULAR","settings": merged_settings,"regular": expr,}valid_variants.append({"diff_settings": new_setting,"simulation_payload": payload})return {"id": alpha_id,"dateSubmitted": alpha.get("dateSubmitted"),"expression": expr,"valid": True,"variants": valid_variants,"original_settings": original_settings}def set_alpha_properties(session: requests.Session, alpha_id: str, name: Optional[str] = None, tags: Optional[list[str]] = None):params= {k: vfork, vin [("name", name), ("tags", tags)] ifv}ifnotparams: returnresponse=session.patch(f"{brain_api_url}/alphas/{alpha_id}", json=params)ifresponse.ok: logger.info(f"Successfully set properties for alpha {alpha_id} (name='{name}', tags={tags}).")else: logger.warning(f"Failed to set properties for alpha {alpha_id}: {response.text}")def run_simulation_payload(session: requests.Session, payload: Dict) -> Tuple[bool, Union[Dict, str]]:settings=payload.get("settings", {})logger.info(f" -> Submitting simulation for {settings.get('region')}/{settings.get('universe')}...")retry_delay=2# 重试间隔2秒whileTrue: # 无限循环重试try:resp=start_simulation(session, payload)# 检查是否是并发错误（例如HTTP 429 Too Many Requests）ifresp.status_code==429or (resp.status_code==400and"concurrent"inresp.text.lower()):logger.warning(f" -> Concurrent error detected for {settings.get('region')}/{settings.get('universe')}. Retrying in {retry_delay} seconds.")time.sleep(retry_delay)continue# 重试resp.raise_for_status() # 对其他HTTP错误抛出异常result=simulation_progress(session, resp)return (True, result.get("result")) ifresult.get("completed") else (False, result.get("message", "Simulation failed."))exceptrequests.exceptions.RequestExceptionase:# 捕获 requests 相关的异常。这里将其视为非并发错误，直接返回失败，让上层继续处理下一个alpha。logger.error(f" -> Request error during simulation for {settings.get('region')}/{settings.get('universe')}: {e}", exc_info=True)returnFalse, str(e)exceptExceptionase:# 捕获其他未知异常。这里将其视为非并发错误，直接返回失败，让上层继续处理下一个alpha。logger.error(f" -> Unexpected error during simulation for {settings.get('region')}/{settings.get('universe')}: {e}", exc_info=True)returnFalse, str(e)def setup_logging():logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # 将日志级别改为 DEBUGdef get_credentials_from_file(file_path: str = 'user_info.txt') -> tuple[Optional[str], Optional[str]]:try:withopen(file_path, 'r', encoding='utf-8') asf: data=f.read().strip().split('\n')user_data= {line.split(': ')[0]: line.split(': ')[1] forlineindataif': 'inline}username=user_data.get('username', "''")[1:-1]password=user_data.get('password', "''")[1:-1]ifnotusernameornotpassword:logger.warning(f"Username or password not found/empty in {file_path}.")returnNone, Nonereturnusername, passwordexceptFileNotFoundError:returnNone, NoneexceptExceptionase:logger.error(f"Error parsing {file_path}: {e}")returnNone, Nonedef run_variant_mode(session, date_range, alpha_ids, target_region, simulate, record_file, output_file):logger.info("--- Running in Variant Generation Mode ---")os.makedirs(os.path.dirname(record_file), exist_ok=True)processed_variants=set()ifos.path.exists(record_file):try:history_df=pd.read_csv(record_file)if'variant_key'inhistory_df.columns:processed_variants=set(history_df['variant_key'].dropna())logger.info(f"Loaded {len(processed_variants)} previously simulated variants.")exceptExceptionase:logger.warning(f"Could not read record file {record_file}: {e}.")ifdate_range:alphas_to_process=fetch_alphas_by_date_range(session, date_range[0], date_range[1])elifalpha_ids:alphas_to_process=fetch_alphas_by_ids(session, alpha_ids)else:logger.error("For 'variant' mode, either --date-range or --alpha-ids must be provided.")returnifnotalphas_to_process:logger.info("No alphas found to process. Exiting.")returnlogger.info(f"Found {len(alphas_to_process)} alpha(s) to process.")operators=fetch_operators(session)logger.info("Fetching platform setting options...")simulation_options=Nonetry:simulation_options=get_platform_setting_options(session)logger.info("Platform setting options fetched successfully.")exceptExceptionase:logger.warning(f"Failed to fetch platform setting options: {e}")all_results= []foralphainalphas_to_process:original_alpha_id=alpha.get('id')logger.info(f"\n--- Analyzing Alpha: {original_alpha_id} ---")analysis_result=get_alpha_variants(session, alpha, operators, simulation_options, target_region)ifnotanalysis_result.get("valid") ornotanalysis_result.get("variants"):logger.info(f"No valid variants found for alpha {original_alpha_id}.")continuelogger.info(f"Found {len(analysis_result['variants'])} variant(s) for alpha {original_alpha_id}"+ (f" in region {target_region}"iftarget_regionelse""))ifsimulate:fori, variantinenumerate(analysis_result['variants']):variant_key=f"{original_alpha_id}::{json.dumps(variant['diff_settings'], sort_keys=True)}"ifvariant_keyinprocessed_variants:logger.info(f" Skipping variant {i+1}/{len(analysis_result['variants'])} (already processed).")continuelogger.info(f" Simulating variant {i+1}/{len(analysis_result['variants'])}...")success, result_or_msg=run_simulation_payload(session, variant['simulation_payload'])ifsuccessand (new_alpha_id:=result_or_msg.get("id")):set_alpha_properties(session, new_alpha_id, name=original_alpha_id, tags=['run_yuanfen'])record= {'timestamp': datetime.now().isoformat(), 'variant_key': variant_key, 'original_alpha_id': original_alpha_id, 'new_alpha_id': new_alpha_id, 'settings': json.dumps(variant['simulation_payload']['settings']), 'expression': variant['simulation_payload']['regular']}pd.DataFrame([record]).to_csv(record_file, mode='a', header=notos.path.exists(record_file), index=False)processed_variants.add(variant_key)all_results.append(analysis_result)ifall_results:withopen(output_fileor"yuanfen_results.json", 'w', encoding='utf-8') asf: json.dump(all_results, f, indent=2)logger.info(f"Processing complete. Results saved to {output_fileor'yuanfen_results.json'}.")else:logger.info("Processing complete. No valid variants were found.")def run_download_mode(session, tag, target_region):logger.info("--- Running in Download Mode ---")os_alphas_cache_path='cache/os_alphas'os_pnls_cache_path='cache/os_pnls'os_alpha_ids_cache_path='cache/os_alpha_ids'unsubmitted_alphas_details_cache_path='cache/unsubmitted_alphas_details'target_pnl_cache_path='cache/target_pnl_cache'os.makedirs('cache', exist_ok=True)# 初始加载 OS alpha 缓存cached_all_os_alphas= []cached_os_alpha_pnls=pd.DataFrame()cached_os_alpha_ids_by_region=defaultdict(list)ifos.path.exists(os_alphas_cache_path+'.pickle') and \os.path.exists(os_pnls_cache_path+'.pickle') and \os.path.exists(os_alpha_ids_cache_path+'.pickle'):logger.info("Loading OS alphas, PnLs, and regional IDs from cache...")cached_all_os_alphas=load_obj(os_alphas_cache_path)cached_os_alpha_pnls=load_obj(os_pnls_cache_path)cached_os_alpha_ids_by_region=load_obj(os_alpha_ids_cache_path)# 确保加载的缓存类型正确ifnotisinstance(cached_os_alpha_pnls, pd.DataFrame):logger.warning(f"Cached PnLs at {os_pnls_cache_path}.pickle is not a DataFrame, resetting.")cached_os_alpha_pnls=pd.DataFrame()ifnotisinstance(cached_os_alpha_ids_by_region, defaultdict):logger.warning(f"Cached alpha IDs at {os_alpha_ids_cache_path}.pickle is not a defaultdict, resetting.")cached_os_alpha_ids_by_region=defaultdict(list)# 获取最新的所有 OS alphalatest_all_os_alphas=get_all_user_alphas(session)# 找出新的 OS alphacached_os_alpha_ids_set= {alpha['id'] foralphaincached_all_os_alphasif'id'inalpha}new_os_alphas_to_process= [alphaforalphainlatest_all_os_alphasifalpha['id'] notincached_os_alpha_ids_set]ifnew_os_alphas_to_process:logger.info(f"Found {len(new_os_alphas_to_process)} new OS alphas. Fetching their PnLs and updating cache...")updated_os_alpha_pnls, updated_os_alpha_ids_by_region=get_alpha_pnls(session, new_os_alphas_to_process,alpha_pnls=cached_os_alpha_pnls,alpha_ids=cached_os_alpha_ids_by_region)# 更新总的 OS alpha 列表all_os_alphas=latest_all_os_alphas# 使用最新的所有 alphaos_alpha_pnls=updated_os_alpha_pnlsos_alpha_ids_by_region=updated_os_alpha_ids_by_region# 保存更新后的 OS alpha 缓存save_obj(all_os_alphas, os_alphas_cache_path)save_obj(os_alpha_pnls, os_pnls_cache_path)save_obj(os_alpha_ids_by_region, os_alpha_ids_cache_path)else:logger.info("No new OS alphas found. Using existing cached data for OS alphas.")all_os_alphas=cached_all_os_alphasos_alpha_pnls=cached_os_alpha_pnlsos_alpha_ids_by_region=cached_os_alpha_ids_by_region# 初始加载未提交 alpha 详情缓存cached_unsubmitted_alphas_details= {}ifos.path.exists(unsubmitted_alphas_details_cache_path+'.pickle'):logger.info("Loading unsubmitted alphas details from cache...")cached_unsubmitted_alphas_details=load_obj(unsubmitted_alphas_details_cache_path)# 模拟 get_alphas_by_days 中的 sharpe 和 fitness 逻辑sharpe=0.9fitness=0.5days=30# 默认获取最近30天的alphatoday=datetime.now().date()start_date=today-timedelta(days=days)end_date=today+timedelta(days=1)# 获取未提交的 alphatarget_alphas, updated_unsubmitted_alphas_details=_get_unsubmitted_alphas_details(session, tag=tag, target_region=target_region, cached_alphas_details=cached_unsubmitted_alphas_details)# 保存更新后的未提交 alpha 详情缓存save_obj(updated_unsubmitted_alphas_details, unsubmitted_alphas_details_cache_path)ifnottarget_alphas: returnlogger.info("No alphas with specified tag found.")# 初始加载 target PnL 缓存cached_target_pnls= {}ifos.path.exists(target_pnl_cache_path+'.pickle'):logger.info("Loading target PnLs from cache...")cached_target_pnls=load_obj(target_pnl_cache_path)# 加载 SelfCorr 和 PPAC 的参考数据os_alpha_ids_selfcorr, os_alpha_rets_selfcorr=load_data(tag='SelfCorr')ppac_alpha_ids, ppac_alpha_rets=load_data(tag='PPAC')processed_data= []foralphaintarget_alphas:alpha_id=alpha.get('id')full_details=alphaalpha_region=full_details.get('settings', {}).get('region')iftarget_regionandalpha_region!=target_region: continuelogger.info(f"Processing alpha {alpha_id} in region {alpha_region}...")# 使用 _get_alpha_pnl 获取 PnLtarget_pnl=Noneifalpha_idincached_target_pnls:target_pnl=cached_target_pnls[alpha_id]logger.info(f"Loaded PnL for {alpha_id} from cache.")else:try:target_pnl_df=_get_alpha_pnl(session, alpha_id)ifnottarget_pnl_df.empty:target_pnl=target_pnl_df.set_index('Date')[alpha_id]cached_target_pnls[alpha_id] =target_pnl# 更新缓存logger.info(f"Fetched PnL for {alpha_id} and added to cache.")else:logger.warning(f"Empty PnL for {alpha_id}. Skipping.")continueexceptExceptionase:logger.error(f"Could not get PnL for {alpha_id}: {e}. Skipping.")continue# 确保 target_pnl 不是 None 且不为空iftarget_pnlisNoneortarget_pnl.empty:logger.warning(f"Target PnL for {alpha_id} is empty after caching check. Skipping.")continue# 计算 self_corrself_corr=calc_self_corr(session, alpha_id, os_alpha_rets=os_alpha_rets_selfcorr, os_alpha_ids=os_alpha_ids_selfcorr, alpha_result=full_details, alpha_pnls=target_pnl)# 计算 ppac_sorrppac_sorr=calc_self_corr(session, alpha_id, os_alpha_rets=ppac_alpha_rets, os_alpha_ids=ppac_alpha_ids, alpha_result=full_details, alpha_pnls=target_pnl)processed_data.append({'id': alpha_id,'parent_id': full_details.get('name', alpha_id), # 新增 parent_id 字段，如果 name 缺失则使用 alpha_id'region': alpha_region,'is_selfCorrelation': round(self_corr, 2),'ppac_sorr': round(ppac_sorr, 2),'expression': _extract_expression(full_details),'sharpe': full_details.get('is', {}).get('sharpe'),'fitness': full_details.get('is', {}).get('fitness'),'turnover': full_details.get('is', {}).get('turnover') *100,'margin': full_details.get('is', {}).get('margin') *10000,'pyramids': ' '.join([p.get('name', '') forpinnext((checkforcheckinfull_details.get('is', {}).get('checks', []) ifcheck.get('name') =='MATCHES_PYRAMID'), {}).get('pyramids', [])])})# 保存更新后的 target PnL 缓存save_obj(cached_target_pnls, target_pnl_cache_path)ifnotprocessed_data: returnlogger.info("No data to save after processing.")output_df=pd.DataFrame(processed_data).sort_values(by=['region', 'is_selfCorrelation'], ascending=[True, True])# 确保 is_selfCorrelation 和 ppac_sorr 列是数值类型，然后格式化为两位小数的字符串output_df['is_selfCorrelation'] =output_df['is_selfCorrelation'].apply(lambdax: f"{x:.2f}")output_df['ppac_sorr'] =output_df['ppac_sorr'].apply(lambdax: f"{x:.2f}")filename=f"run_yuanfen_{target_region}_candidates.csv"iftarget_regionelse"run_yuanfen_ALL_candidates.csv"output_path=os.path.join("submit", filename)os.makedirs("submit", exist_ok=True)output_df.to_csv(output_path, index=False, encoding='utf-8')logger.info(f"Successfully saved {len(output_df)} alphas to {output_path}")def run_interactive_mode(session):whileTrue:print("\n--- Interactive Mode ---")print("1. Find Variants")print("2. Download Tagged Alphas")print("3. Exit")choice=input("Select an option (1-3): ")ifchoice=='1':sub_choice=input(" Fetch by (1) Date Range or (2) Alpha IDs? ")date_range, ids=None, Noneifsub_choice=='1':start=input(" Enter start date (YYYY-MM-DD): ")end=input(" Enter end date (YYYY-MM-DD): ")date_range= [start, end]elifsub_choice=='2':ids_str=input(" Enter comma-separated Alpha IDs: ")ids= [s.strip() forsinids_str.split(',')]else:print(" Invalid choice.")continueregion=input(" Enter target region (or leave blank for all): ")simulate=input(" Run simulations? (y/n): ").lower() =='y'output=input(" Enter output JSON file name (default: yuanfen_results.json): ")run_variant_mode(session, date_range, ids, regionorNone, simulate, "records/yuanfen_history.csv", output)elifchoice=='2':tag=input(" Enter tag to download (default: run_yuanfen): ") or"run_yuanfen"region=input(" Enter target region (or leave blank for all): ")run_download_mode(session, tag, regionorNone)elifchoice=='3':breakelse:print("Invalid option, please try again.")def main():setup_logging()parser=argparse.ArgumentParser(description="Standalone BRAIN Alpha Tool.", formatter_class=argparse.RawTextHelpFormatter)parser.add_argument('-i', '--interactive', action='store_true', help="Run in interactive mode.")parser.add_argument("--mode", required=False, choices=['variant', 'download'], help="Mode: 'variant' or 'download'. Required if not in interactive mode.")variant_group=parser.add_argument_group('Variant Mode')variant_group.add_argument("--date-range", nargs=2, metavar=('START', 'END'), help="Date range for 'variant' mode.")variant_group.add_argument("--alpha-ids", help="Comma-separated IDs for 'variant' mode.")variant_group.add_argument("--simulate", action='store_true', help="Run simulations for found variants.")variant_group.add_argument("--record-file", default="records/yuanfen_history.csv", help="History file for simulations.")download_group=parser.add_argument_group('Download Mode')download_group.add_argument("--tag", default="run_yuanfen", help="Tag to filter alphas.")parser.add_argument("--target-region", help="Optional: Filter by region.")parser.add_argument("--output-file", help="Output file (for variant mode).")args=parser.parse_args()username, password=get_credentials_from_file()ifnotusernameornotpassword:logger.info("Could not load credentials from file, prompting.")username=input("Enter BRAIN Username (Email): ")password=getpass.getpass("Enter BRAIN Password: ")try:session=brain_login(username, password)exceptExceptionase:logger.error(f"Login failed: {e}")sys.exit(1)ifargs.interactive ornotargs.mode:run_interactive_mode(session)elifargs.mode =='variant':run_variant_mode(session, args.date_range, [s.strip() forsinargs.alpha_ids.split(',')] ifargs.alpha_ids elseNone, args.target_region, args.simulate, args.record_file, args.output_file)elifargs.mode =='download':run_download_mode(session, args.tag, args.target_region)if __name__ == "__main__":main()
```

---

## 讨论与评论 (6)

### 评论 #1 (作者: HZ99685, 时间: 6个月前)

复制的代码没有缩进。。。。。苦

---

### 评论 #2 (作者: LL62621, 时间: 6个月前)

这个是对桥的补充嘛

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

日拱一卒

---

### 评论 #3 (作者: JX79797, 时间: 6个月前)

[HZ99685](/hc/en-us/profiles/32603557750935-HZ99685)  那肯定用上ai啊

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #4 (作者: JX79797, 时间: 6个月前)

更新分组并发版本

# -*- coding: utf-8 -*-
"""
Standalone script for BRAIN Alpha Variant Generation ("Yuanfen Yidao Qiao")
and downloading tagged alphas with self-correlation.

This script provides a command-line interface for two main modes:
1. 'variant': Finds and optionally simulates new alpha variants based on an existing alpha.
2. 'download': Fetches alphas with a specific tag, calculates their self-correlation,
   and saves them to a sorted CSV file.
3. 'interactive': A menu-driven interactive mode to guide the user.

Features:
- Login with email/password from user_info.txt or prompt.
- Mode 'variant':
    - Fetch submitted OS alphas by date range or by specific IDs.
    - Find all possible setting variants for each alpha.
    - Filter variants for a specific target region.
    - Optionally, run simulations for the filtered variants.
    - Record simulation history to avoid re-running.
    - Set name and tags for newly created alphas.
- Mode 'download':
    - Fetch all alphas with the 'run_yuanfen' tag.
    - Optionally filter by a specific region.
    - Calculate self-correlation for each alpha against all other OS alphas.
    - Save results to a CSV file in the `submit/` directory.
    - Sort the CSV by region, then by self-correlation (ascending).

Example Usage:

# --- Interactive Mode ---
python run_yuanfen.py

# --- Variant Mode (Command Line) ---
python run_yuanfen.py --mode variant --alpha-ids "alphaId1,alphaId2" \
    --target-region "EUR" --simulate

# --- Download Mode (Command Line) ---
python run_yuanfen.py --mode download --target-region "USA"
"""

from __future__ import annotations

import argparse
import getpass
import json
import logging
import os
import re
import sys
import threading
import time
import pickle
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple, Union
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import copy # 导入 copy 模块

import numpy as np
import pandas as pd
import requests
from pathlib import Path # 导入 Path

# For get_platform_setting_options and validate_setting
from itertools import product

# --- Start of Combined Lib ---
logger = logging.getLogger("yuanfen_standalone")

class SingleSession(requests.Session):
    _instance = None
    _lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

class SessionManager:
    def __init__(self, session, start_time, expiry_time):
        self.session = session
        self.start_time = start_time
        self.expiry_time = expiry_time
        self.lock = threading.Lock()  # 添加线程锁保护session刷新

def refresh_session(self):
        with self.lock:  # 使用线程锁保护session刷新过程
            logger.info("Session expired, logging in again...")
            if self.session:
                self.session.close()
            # Use brain_login from run_yuanfen.py
            # Assuming brain_login takes username and password, which are not directly available here.
            # For now, I'll assume the session object itself can be refreshed or a new one created.
            # A more robust solution would pass credentials to SessionManager or make brain_login accessible.
            # For this context, I'll call brain_login without args, assuming it can get credentials.
            # If brain_login requires explicit username/password, this will need further adjustment.
            self.session = brain_login(self.session.auth[0], self.session.auth[1]) # Re-authenticate with existing credentials
            self.start_time = time.time()

brain_api_url = os.environ.get("BRAIN_API_URL", " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) ")

def wait_get(sess, url: str, params: Optional[Dict] = None, max_retries: int = 1000) -> Optional[requests.Response]:
    """
    Performs a GET request with retry logic and exponential backoff.
    Returns None if all retries fail, instead of raising an error.
    """
    for attempt in range(max_retries):
        try:
            response = sess.get(url, params=params)
            if "Retry-After" in response.headers:
                sleep_time = float(response.headers["Retry-After"])
                time.sleep(sleep_time)
                continue
            response.raise_for_status() # Raise for HTTP errors, but allow 404 to be handled by caller
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404: # Special handling for 404s
                logger.warning(f"Request to {url} returned 404 (Not Found). Attempt {attempt + 1}/{max_retries}. Returning response for caller to handle.")
                return e.response # Return the 404 response
            else:
                logger.warning(f"Request to {url} failed with HTTP error {e.response.status_code} (attempt {attempt + 1}/{max_retries}): {e}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request to {url} failed (attempt {attempt + 1}/{max_retries}): {e}")

        # Exponential backoff for retries
        time.sleep(2)

    logger.error(f"Failed to get URL {url} after {max_retries} retries. Returning None.")
    return None # Return None after all retries fail

def start_simulation(s: SingleSession, simulate_data: Union[list[dict], dict]) -> requests.Response:
    return s.post(f"{brain_api_url}/simulations", json=simulate_data)

def get_simulation_result_json(s: requests.Session, alpha_id: str) -> dict:
    if not alpha_id: return {}
    resp = wait_get(s, f"{brain_api_url}/alphas/{alpha_id}")
    if resp is None or resp.status_code == 404: return {} # Handle 404 specifically for alpha details or None response
    return resp.json()

def simulation_progress(s: SingleSession, simulate_response: requests.Response) -> dict:
    if simulate_response.status_code // 100 != 2:
        logger.warning(f'Simulation start failed: {simulate_response.status_code} - {simulate_response.text}')
        return {"completed": False, "message": f"Start failed: {simulate_response.status_code} - {simulate_response.text}"}

    progress_url = simulate_response.headers["Location"]

    # Add a timeout for polling simulation progress (e.g., 20 minutes as in optimizeAlpha.py)
    polling_start_time = time.time()
    polling_timeout = 1200 # seconds (20 minutes)

    while True:
        if time.time() - polling_start_time > polling_timeout:
            logger.error(f"Simulation progress check timed out after {polling_timeout / 60} minutes for URL: {progress_url}. Assuming simulation failed.")
            return {"completed": False, "message": f"Simulation progress check timed out."}

progress_resp = wait_get(s, progress_url)

        if progress_resp is None:
            logger.error(f"Simulation progress URL {progress_url} failed to respond after multiple retries. Assuming simulation failed.")
            return {"completed": False, "message": "Simulation progress not found after multiple retries."}

if progress_resp.status_code == 404:
            logger.error(f"Simulation progress URL {progress_url} returned 404. Assuming simulation failed.")
            return {"completed": False, "message": "Simulation progress not found."}

progress_json = progress_resp.json()
        status = progress_json.get("status")

if status == "COMPLETE":
            alpha_id = progress_json.get("alpha")
            if not alpha_id:
                logger.warning(f"Simulation completed but no alpha ID found: {progress_json}")
                return {"completed": False, "message": "Simulation completed but no alpha ID."}
            final_result = get_simulation_result_json(s, alpha_id)
            return {"completed": True, "result": final_result} if final_result else {"completed": False, "message": "Failed to retrieve final result."}
        elif status in ("ERROR", "FAIL"): # Treat "ERROR" and "FAIL" as definitive failures for this attempt
            logger.error(f"Simulation failed with status '{status}': {progress_json}")
            return {"completed": False, "message": json.dumps(progress_json)}
        elif status == "WARNING": # Treat "WARNING" as completed with a warning
            alpha_id = progress_json.get("alpha")
            if not alpha_id:
                logger.warning(f"Simulation completed with WARNING but no alpha ID found: {progress_json}")
                return {"completed": False, "message": "Simulation completed with WARNING but no alpha ID."}
            final_result = get_simulation_result_json(s, alpha_id)
            return {"completed": True, "result": final_result, "warning": json.dumps(progress_json)} if final_result else {"completed": False, "message": "Failed to retrieve final result with WARNING."}
        else:
            # If status is not COMPLETE, ERROR, FAIL, or WARNING, continue polling
            logger.info(f"Simulation {progress_url} is still {status}. Retrying after a short delay.")
            time.sleep(5) # Poll every 5 seconds

# --- Start of self_corr_checkV3 logic (copied) ---
def save_obj(obj: object, name: str) -> None:
    """
    保存对象到文件中，以 pickle 格式序列化。

Args:
        obj (object): 需要保存的对象。
        name (str): 文件名（不包含扩展名），保存的文件将以 '.pickle' 为扩展名。

Returns:
        None: 此函数无返回值。

Raises:
        pickle.PickleError: 如果序列化过程中发生错误。
        IOError: 如果文件写入过程中发生 I/O 错误。
    """
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name: str) -> object:
    """
    加载指定名称的 pickle 文件并返回其内容。

此函数会打开一个以 `.pickle` 为扩展名的文件，并使用 `pickle` 模块加载其内容。

Args:
        name (str): 不带扩展名的文件名称。

Returns:
        object: 从 pickle 文件中加载的 Python 对象。

Raises:
        FileNotFoundError: 如果指定的文件不存在。
        pickle.UnpicklingError: 如果文件内容无法被正确反序列化。
    """
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)

def _get_alpha_pnl(sess,alpha_id: str) -> pd.DataFrame:
    """
    获取指定 alpha 的 PnL数据，并返回一个包含日期和 PnL 的 DataFrame。

此函数通过调用 WorldQuant Brain API 获取指定 alpha 的 PnL 数据，
    并将其转换为 pandas DataFrame 格式，方便后续数据处理。

Args:
        alpha_id (str): Alpha 的唯一标识符。

Returns:
        pd.DataFrame: 包含日期和对应 PnL 数据的 DataFrame，列名为 'Date' 和 alpha_id。
    """
    pnl = wait_get(sess, " [https://api.worldquantbrain.com/alphas/](https://api.worldquantbrain.com/alphas/) " + alpha_id + "/recordsets/pnl").json()
    df = pd.DataFrame(pnl['records'], columns=[item['name'] for item in pnl['schema']['properties']])
    # 立即转换日期格式
    df['date'] = pd.to_datetime(df['date']).dt.normalize()
    df = df.rename(columns={'date':'Date', 'pnl':alpha_id})
    df = df[['Date', alpha_id]]
    return df

def get_alpha_pnls(
    sess,
    alphas: list[dict], 
    alpha_pnls: Optional[pd.DataFrame] = None, 
    alpha_ids: Optional[dict[str, list]] = None
) -> Tuple[dict[str, list], pd.DataFrame]:
    """
    获取 alpha 的 PnL 数据，并按区域分类 alpha 的 ID。

Args:
        alphas (list[dict]): 包含 alpha 信息的列表，每个元素是一个字典，包含 alpha 的 ID 和设置等信息。
        alpha_pnls (Optional[pd.DataFrame], 可选): 已有的 alpha PnL 数据，默认为空的 DataFrame。
        alpha_ids (Optional[dict[str, list]], 可选): 按区域分类的 alpha ID 字典，默认为空字典。

Returns:
        Tuple[dict[str, list], pd.DataFrame]: 
            - 按区域分类的 alpha ID 字典。
            - 包含所有 alpha 的 PnL 数据的 DataFrame。
    """

if alpha_ids is None:
        alpha_ids = defaultdict(list)
    if alpha_pnls is None:
        alpha_pnls = pd.DataFrame()

    new_alphas = [item for item in alphas if item['id'] not in alpha_pnls.columns]
    if not new_alphas:
        return alpha_ids, alpha_pnls

    for item_alpha in new_alphas:
        alpha_ids[item_alpha['settings']['region']].append(item_alpha['id'])

fetch_pnl_func = lambda alpha_id: _get_alpha_pnl(sess, alpha_id).set_index('Date')
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_pnl_func, [item['id'] for item in new_alphas])
    alpha_pnls = pd.concat([alpha_pnls] + list(results), axis=1)
    # 确保索引是 datetime 类型
    alpha_pnls.index = pd.to_datetime(alpha_pnls.index).normalize()
    alpha_pnls.sort_index(inplace=True)

return alpha_ids, alpha_pnls

class cfg:
    # 使用示例
    username = ""
    password = ""
    data_path = Path('alphas')

_data_cache = {}
_cache_lock = threading.RLock()

def load_data(tag=None):
    """加载数据并缓存，减少重复加载。线程安全版本。"""
    # 使用缓存加速重复调用
    cache_key = str(tag)
    with _cache_lock:
        if cache_key in _data_cache:
            # 返回缓存数据的深拷贝，避免多线程修改共享对象
            return copy.deepcopy(_data_cache[cache_key][0]), _data_cache[cache_key][1].copy()

        os_alpha_ids = load_obj(str(cfg.data_path / 'os_alpha_ids'))
        os_alpha_pnls = load_obj(str(cfg.data_path / 'os_alpha_pnls'))
        ppac_alpha_ids = load_obj(str(cfg.data_path / 'ppac_alpha_ids'))

if tag=='PPAC':
            for item in os_alpha_ids:
                os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha in ppac_alpha_ids]
        elif tag=='SelfCorr':
            for item in os_alpha_ids:
                os_alpha_ids[item] = [alpha for alpha in os_alpha_ids[item] if alpha not in ppac_alpha_ids]
        else:
            os_alpha_ids = os_alpha_ids  # 不指定tag时使用全量数据

# 处理数据...(原有代码)
        exist_alpha = [alpha for ids in os_alpha_ids.values() for alpha in ids]
        os_alpha_pnls = os_alpha_pnls[exist_alpha]
        os_alpha_pnls.columns = os_alpha_pnls.columns.astype(str)
        # 确保加载的 pnl 数据索引是标准化的 datetime
        os_alpha_pnls.index = pd.to_datetime(os_alpha_pnls.index).normalize()
        os_alpha_rets = os_alpha_pnls - os_alpha_pnls.ffill().shift(1)
        os_alpha_rets = os_alpha_rets[pd.to_datetime(os_alpha_rets.index)>pd.to_datetime(os_alpha_rets.index).max() - pd.DateOffset(years=4)]

        # 缓存结果的副本，避免后续修改影响缓存
        # 将 defaultdict 转换为 dict 再缓存，以避免 unhashable type 错误
        _data_cache[cache_key] = (dict(copy.deepcopy(os_alpha_ids)), os_alpha_rets.copy())

    # 返回原始数据的副本
    # 确保返回的是 dict 而不是 defaultdict
    return copy.deepcopy(_data_cache[cache_key][0]), _data_cache[cache_key][1].copy()

def calc_self_corr(sess, alpha_id, os_alpha_rets=None, os_alpha_ids=None, alpha_result=None, return_alpha_pnls=False, alpha_pnls=None):
    if alpha_result is None:
        alpha_result = wait_get(sess, f" [https://api.worldquantbrain.com/alphas/{alpha_id}").json(](https://api.worldquantbrain.com/alphas/{alpha_id}%22).json() )

if alpha_pnls is not None:
        if len(alpha_pnls) == 0:
            alpha_pnls = None
    if alpha_pnls is None:
        _, alpha_pnls_df = get_alpha_pnls(sess, [alpha_result])
        if alpha_id in alpha_pnls_df.columns:
            alpha_pnls = alpha_pnls_df[alpha_id]
        else:
            alpha_pnls = pd.Series(dtype='float64') # Or handle error appropriately

    # 确保传入的 alpha_pnls 索引是标准化的 datetime
    if not isinstance(alpha_pnls.index, pd.DatetimeIndex):
        alpha_pnls.index = pd.to_datetime(alpha_pnls.index).normalize()

alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)
    alpha_rets = alpha_rets.replace(0, 1e-14)  # 替换零值为极小正数（新增）
    alpha_rets = alpha_rets.dropna()  # 移除缺失值（新增）
    # 新增：确保 alpha_rets 也只使用最近四年的数据
    alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index) > pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)]

region = alpha_result['settings']['region']
    # 新增：清洗 os_alpha_rets（删除含 NaN 的列，过滤标准差过小的列）
    if os_alpha_rets is not None:
        # 添加对 region 键的检查
        if region in os_alpha_ids:
            os_alpha_rets_clean = os_alpha_rets[os_alpha_ids[region]].dropna(axis=1, thresh=len(os_alpha_rets)*0.7)
            # 新增：检查筛选后的数据是否为空
            if os_alpha_rets_clean.empty:
                print(f"警告：region={region} 筛选后无有效数据，原始ID数量={len(os_alpha_ids[region])}")
                valid_columns = [] # 如果没有有效数据，则有效列为空
            else:
                std_devs = os_alpha_rets_clean.std()
                valid_columns = std_devs.index  # 保留所有列
                # 仅在DataFrame非空时执行列筛选
                os_alpha_rets_clean = os_alpha_rets_clean[valid_columns]
            # 更新 os_alpha_ids 为有效列对应的 alpha_id（假设 os_alpha_ids 结构为 {region: [alpha_ids]}）
            # 新增：打印ID匹配情况
            existing_columns = set(os_alpha_rets.columns)
            missing_ids = [alpha for alpha in os_alpha_ids[region] if alpha not in existing_columns]
            os_alpha_ids[region] = [alpha for alpha in os_alpha_ids[region] if alpha in valid_columns]
        else:
            # 如果 region 不在 os_alpha_ids 中，则 os_alpha_rets_clean 为空 DataFrame
            print(f"警告：区域 '{region}' 不在 os_alpha_ids 中。")
            os_alpha_rets_clean = pd.DataFrame()
    else:
        os_alpha_rets_clean = pd.DataFrame()

# 新增：检查有效数据是否存在
    if os_alpha_rets_clean.empty:
        print(f"已提交为空，无有效参考数据或自身收益率数据，相关性无法计算，默认0.01")
        max_corr_id = None
        max_corr_value = np.nan_to_num(0.01, nan=0.0) # 确保默认值不为NaN
    elif alpha_rets.empty:
        print(f"警告：{alpha_id} 无有效参考数据或自身收益率数据，相关性无法计算")
        max_corr_id = None
        max_corr_value = np.nan_to_num(0, nan=0.0) # 确保默认值不为NaN
    else:
        # 计算重叠日期
        common_dates = os_alpha_rets_clean.index.intersection(alpha_rets.index)
        if len(common_dates) == 0:
            print(f"警告：{alpha_id} 与参考数据无重叠日期，相关性无法计算")
            max_corr_id = None
            max_corr_value = np.nan_to_num(0, nan=0.0) # 确保默认值不为NaN
        else:
            # 使用清洗后的数据计算相关系数
            os_alpha_rets_aligned, alpha_rets_aligned = os_alpha_rets_clean.align(alpha_rets, join='inner', axis=0)
            corr_series = os_alpha_rets_aligned.corrwith(alpha_rets_aligned)
            # 处理全 NA 情况
            if corr_series.isna().all():
                print(f"警告：{alpha_id} 相关系数序列全为 NA，无最大值")
                max_corr_id = None
                max_corr_value = np.nan_to_num(0, nan=0.0) # 确保默认值不为NaN
            else:
                # 显式跳过 NA 以避免 FutureWarning
                max_corr_id = corr_series.idxmax(skipna=True)
                max_corr_value = np.nan_to_num(corr_series.max(), nan=0.0) # 确保最大值不为NaN

# 打印最大相关性的 alpha_id 和值
    if max_corr_id is None:
        print(f"与 {alpha_id} 最大相关性的 alpha_id 是 {max_corr_id}，相关性值为 {max_corr_value}")
        if alpha_result and alpha_result['settings']['region'] in os_alpha_ids and not os_alpha_rets.empty and not alpha_rets.empty:
            try:
                debug_corr_series = os_alpha_rets[os_alpha_ids[alpha_result['settings']['region']]].corrwith(alpha_rets)
                print(debug_corr_series.sort_values(ascending=False).round(4).head(1))
            except Exception as e:
                print(f"Debug print error: {e}")

self_corr = max_corr_value
    # 确保 self_corr 最终不是 NaN，将其替换为 0
    self_corr = np.nan_to_num(self_corr, nan=0.0)

if return_alpha_pnls:
        return self_corr, alpha_pnls
    else:
        return self_corr

# --- Start of main script logic ---
BASE_URL = " [https://api.worldquantbrain.com](https://api.worldquantbrain.com) "

def brain_login(username: str = None, password: str = None, max_retries: int = 3) -> requests.Session:
    if username is None or password is None:
        # Try to get credentials from file if not provided
        file_username, file_password = get_credentials_from_file()
        if file_username and file_password:
            username = file_username
            password = file_password
        else:
            # If still no credentials, raise error instead of prompting
            raise RuntimeError("Authentication credentials (username/password) not provided and not found in file.")

session = SingleSession()
    session.auth = (username, password)
    for attempt in range(1, max_retries + 1):
        try:
            response = session.post(f"{BASE_URL}/authentication")
            if response.status_code == requests.codes.unauthorized:
                if response.headers.get("WWW-Authenticate") == "persona":
                    location = response.headers.get("Location", "")
                    logger.error(f"Biometric authentication required. Please open this URL, complete login, then re-run: {urljoin(response.url, location)}")
                    sys.exit(1)
                raise RuntimeError("Invalid username or password.")
            response.raise_for_status()
            logger.info("Authentication successful.")
            return session
        except requests.HTTPError as exc:
            if attempt >= max_retries: raise exc
            time.sleep(2)
    raise RuntimeError("Authentication failed after retries.")

def get_platform_setting_options(session: requests.Session) -> pd.DataFrame:
    """
    Retrieves and organizes instrument type, region, and delay data into a DataFrame.
    """
    settings_options = session.options(f"{BASE_URL}/simulations").json()['actions']['POST']['settings']['children']

    data = [
        {settings_options[key]['label']: settings_options[key]['choices']}
        for key in settings_options.keys()
        if settings_options[key]['type'] == 'choice'
    ]

instrument_type_data = {}
    region_data = {}
    universe_data = {}
    delay_data = {}
    neutralization_data = {}

for item in data:
        if 'Instrument type' in item:
            instrument_type_data = item['Instrument type']
        elif 'Region' in item:
            region_data = item['Region']['instrumentType']
        elif 'Universe' in item:
            universe_data = item['Universe']['instrumentType']
        elif 'Delay' in item:
            delay_data = item['Delay']['instrumentType']
        elif 'Neutralization' in item:
            neutralization_data = item['Neutralization']['instrumentType']

data_list = []

for instrument_type in instrument_type_data:
        for region in region_data[instrument_type['value']]:
            for delay in delay_data[instrument_type['value']]['region'][region['value']]:
                row = {'InstrumentType': instrument_type['value'], 'Region': region['value'], 'Delay': delay['value']}
                row['Universe'] = [
                    item['value'] for item in universe_data[instrument_type['value']]['region'][region['value']]
                ]
                row['Neutralization'] = [
                    item['value'] for item in neutralization_data[instrument_type['value']]['region'][region['value']]
                ]
                data_list.append(row)

df = pd.DataFrame(data_list).sort_values(
        by=['InstrumentType', 'Region', 'Delay'], ascending=False, ignore_index=True
    )
    return df

def validate_setting(setting: Dict, options_df: Optional[pd.DataFrame]) -> bool:
    """Check if a setting combination is valid according to simulation options."""
    if options_df is None or options_df.empty:
        return True # Skip validation if options not available

    inst_type = setting.get("instrumentType", "EQUITY")
    region = setting.get("region")
    delay = setting.get("delay")
    universe = setting.get("universe")

    try:
        delay = int(delay)
    except (ValueError, TypeError):
        pass

# Iterate to find match
    for _, row in options_df.iterrows():
        row_inst = row.get('InstrumentType')
        row_region = row.get('Region')
        row_delay = row.get('Delay')

        try:
            row_delay = int(row_delay)
        except (ValueError, TypeError):
            pass

        if row_inst == inst_type and row_region == region and row_delay == delay:
            # Check universe
            valid_universes = row.get('Universe', [])
            if isinstance(valid_universes, list) and universe in valid_universes:
                return True

    return False

def get_all_user_alphas(session: requests.Session) -> List[Dict]:
    all_alphas, offset, limit = [], 0, 100
    logger.info("Fetching all OS alphas for correlation reference...")
    while True:
        try:
            resp = wait_get(session, f"{BASE_URL}/users/self/alphas", params={"stage": "OS", "limit": limit, "offset": offset})
            data = resp.json() # FIX: Assign resp.json() to data first
            results = data.get("results", [])
            if not results: break
            all_alphas.extend(results)
            offset += len(results)
            logger.info(f"Fetched {len(all_alphas)} OS alphas so far...")
            if len(results) < limit: break
        except Exception as e:
            logger.error(f"Failed to fetch alphas at offset {offset}: {e}")
            break
    return all_alphas

# 复制自 machine_lib.py 的 get_alphas 函数，并重命名
def _get_unsubmitted_alphas_from_api(s, start_date, end_date, sharpe_th, fitness_th, usage, tag: str = '', color_exclude='', region=None):
    alpha_list = []
    next_alphas = []

    start_date_str = start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date
    end_date_str = end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date

common_params = {
        "limit": 100,
        "tag": tag,
        "status": "UNSUBMITTED",
        "dateCreated>": f"{start_date_str}T00:00:00-04:00",
        "dateCreated<": f"{end_date_str}T00:00:00-04:00",
        "color!": color_exclude,
        "order": "-is.sharpe",
        "hidden": "false"
    }
    if region:
        common_params["settings.region"] = region

# Positive alphas
    i = 0
    while True:
        params_positive = {**common_params, "offset": i, "is.sharpe>": sharpe_th, "is.fitness>": fitness_th}
        response = s.get(f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ", params=params_positive)
        try:
            response.raise_for_status()
            logger.info(f"Fetching positive alphas (offset {i}): {response.url}")
            i += 100
            json_response = response.json()
            if not isinstance(json_response, dict) or "count" not in json_response:
                raise ValueError(f"Unexpected API response format: {json_response}")
            count = json_response["count"]
            logger.info(f"count: {count}")
            results = json_response.get("results", [])
            if not results:
                logger.info(f"No positive alphas found for tag={tag}, region={region}, sharpe>={sharpe_th}, fitness>={fitness_th}")
            alpha_list.extend(results)
            if i >= count or i == 9900:
                break
            time.sleep(0.01)
        except Exception as e:
            logger.error(f"Failed to get positive alphas: {e}")
            i -= 100
            s = brain_login(s.auth[0], s.auth[1])

# Negative alphas
    if usage != "submit":
        i = 0
        while True:
            params_negative = {**common_params, "offset": i, "is.sharpe<": -sharpe_th, "is.fitness<": -fitness_th}
            response = s.get(f" [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ", params=params_negative)
            try:
                response.raise_for_status()
                logger.info(f"Fetching negative alphas (offset {i}): {response.url}")
                json_response = response.json()
                if not isinstance(json_response, dict) or "count" not in json_response:
                    raise ValueError(f"Unexpected API response format: {json_response}")
                count = json_response["count"]
                results = json_response.get("results", [])
                if not results:
                    logger.info(f"No negative alphas found for tag={tag}, region={region}, sharpe<=-{sharpe_th}, fitness<=-{fitness_th}")
                if i >= count or i == 9900:
                    break
                alpha_list.extend(results)
                i += 100
            except Exception as e:
                logger.error(f"Failed to get negative alphas: {e}")
                s = brain_login(s.auth[0], s.auth[1])

if not alpha_list:
        logger.info(f"No alphas found in total for tag={tag}, region={region}. Returning empty lists.")
        return {"next": []}

if usage != "submit":
        for j in range(len(alpha_list)):
            alpha_id = alpha_list[j]["id"]
            # name = alpha_list[j]["name"] # 'name' is not used in rec, so commented out
            # dateCreated = alpha_list[j]["dateCreated"] # 'dateCreated' is not used in rec, so commented out
            sharpe = alpha_list[j]["is"]["sharpe"]
            fitness = alpha_list[j]["is"]["fitness"]
            turnover = alpha_list[j]["is"]["turnover"]
            margin = alpha_list[j]["is"]["margin"]
            longCount = alpha_list[j]["is"]["longCount"]
            shortCount = alpha_list[j]["is"]["shortCount"]
            decay = alpha_list[j]["settings"]["decay"]
            # region = alpha_list[j]["settings"]["region"] # 'region' is not used in rec, so commented out

            if 'regular' in alpha_list[j]:
                exp = alpha_list[j]['regular']['code']
            elif 'combo' in alpha_list[j]:
                exp = alpha_list[j]['combo']['code']
            else:
                exp = ""

            rec = [alpha_id, exp, sharpe, turnover, fitness, margin, longCount, shortCount, alpha_list[j]["dateCreated"], decay]
            next_alphas.append(rec)           
        output_dict = {"next": next_alphas}
        logger.info(f"count: {len(next_alphas)}")
    return output_dict

def _get_unsubmitted_alphas_details(session: requests.Session, tag: str, target_region: Optional[str], cached_alphas_details: Optional[Dict[str, Dict]] = None) -> Tuple[List[Dict], Dict[str, Dict]]:
    logger.info(f"Fetching unsubmitted alphas with tag: '{tag}' for region '{target_region if target_region else 'ALL'}'...")

    if cached_alphas_details is None:
        cached_alphas_details = {}

all_unsubmitted_alphas_details = []

    days = 30
    sharpe = 0.9
    fitness = 0.5

today = datetime.now().date()
    start_date = today - timedelta(days=days)
    end_date = today + timedelta(days=1)

for_per = _get_unsubmitted_alphas_from_api(session, start_date, end_date,
                            sharpe, fitness,
                            "track", tag=tag, color_exclude="RED", region=target_region)

    alpha_id_list = [item[0] for item in for_per.get('next', [])] # Removed 'decay'

    for alpha_id in alpha_id_list:
        if alpha_id in cached_alphas_details:
            full_details = cached_alphas_details[alpha_id]
        else:
            full_details = get_simulation_result_json(session, alpha_id)
            if full_details:
                cached_alphas_details[alpha_id] = full_details

        if full_details:
            alpha_tags = full_details.get('tags', [])
            alpha_region_from_details = full_details.get('settings', {}).get('region')

if tag in alpha_tags and (target_region is None or alpha_region_from_details == target_region):
                all_unsubmitted_alphas_details.append(full_details)

logger.info(f"Found {len(all_unsubmitted_alphas_details)} unsubmitted alphas with tag '{tag}' for region '{target_region if target_region else 'ALL'}'.")
    return all_unsubmitted_alphas_details, cached_alphas_details

def fetch_alphas_by_date_range(session: requests.Session, start_date: str, end_date: str) -> List[Dict]:
    logger.info(f"Fetching alphas from {start_date} to {end_date}...")
    start_iso, end_iso = f"{start_date}T00:00:00Z", f"{end_date}T23:59:59Z"
    all_alphas, offset, limit = [], 0, 100
    while True:
        params = {"stage": "OS", "order": "-dateSubmitted", "dateSubmitted>": start_iso, "dateSubmitted<": end_iso, "limit": limit, "offset": offset}
        resp = wait_get(session, f"{BASE_URL}/users/self/alphas", params=params)
        data = resp.json() # FIX: Assign resp.json() to data first
        results = data.get("results", [])
        if not results: break
        all_alphas.extend(results)
        offset += len(results)
        if len(results) < limit: break
    return all_alphas

def fetch_alphas_by_ids(session: requests.Session, alpha_ids: List[str]) -> List[Dict]:
    logger.info(f"Fetching {len(alpha_ids)} alphas by ID...")
    return [get_simulation_result_json(session, alpha_id.strip()) for alpha_id in alpha_ids if alpha_id.strip()]

def fetch_operators(session: requests.Session) -> List[Dict]:
    return wait_get(session, f"{BASE_URL}/operators").json()

def _dedupe(seq: Sequence[str]) -> List[str]:
    return list(dict.fromkeys(seq))

def _extract_expression(alpha: Dict) -> Optional[str]:
    for key in ("regular", "combo", "selection"):
        if (block := alpha.get(key)) and isinstance(block, dict):
            if expr := block.get("expression") or block.get("code"):
                return expr
    return None

def parse_expression(expression: str, operator_names: Sequence[str]) -> Tuple[List[str], List[str]]:
    """Split an expression into operators and datafields using a token scan."""
    # Remove C-style comments /* ... */
    expression = re.sub(r"/\*[\s\S]*?\*/", "", expression)
    # Remove Python-style comments # ...
    expression = re.sub(r"#.*", "", expression)

operator_set = set(operator_names)
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression)

found_ops: List[str] = []
    found_fields: List[str] = []

# Add known built-in keywords/variables to skip_tokens
    # These are often part of the expression language itself, not queryable datafields
    skip_tokens = {"if", "else", "true", "false", "nan", "inf", "alpha", "percentage", "p", "limit_volume","factor","longscale","value"}

for token in tokens:
        if token in skip_tokens:
            continue
        if token in operator_set:
            found_ops.append(token)
        else:
            found_fields.append(token)

logger.info(f"Parsed expression. Found operators: {_dedupe(found_ops)}, Datafields: {_dedupe(found_fields)}")
    return _dedupe(found_ops), _dedupe(found_fields)

def get_datafield_availability(session: requests.Session, field_name: str) -> Dict:
    """Fetch detail for a datafield and summarize other available settings."""
    resp = wait_get(session, f"{BASE_URL}/data-fields/{field_name}")
    if resp is None or resp.status_code == 404:  # Handle 404 specifically for datafield availability or None response
        logger.warning(f"Datafield '{field_name}' not found (404). Returning empty availability.")
        info_result = {"detail": {}, "availability": [], "error": "Datafield not found."}
        logger.info(f"Availability info for field '{field_name}': {info_result.get('availability')}")
        return info_result

try:
        detail = resp.json()

        availability_candidates = []
        for key in (
            "availability",
            "availabilities",
            "availableSettings",
            "availabilityList",
            "regionAvailability",
            "settings",
            "data",
        ):
            value = detail.get(key)
            if isinstance(value, list):
                availability_candidates.extend(value)
            elif isinstance(value, dict):
                nested = value.get("availability") or value.get("items") or value.get("list")
                if isinstance(nested, list):
                    availability_candidates.extend(nested)

def _pick(d, keys, default_val=None):
            for k in keys:
                val = d.get(k)
                if val is not None:
                    return val
            return default_val

normalized_items = []
        for item in availability_candidates:
            if not isinstance(item, dict):
                continue
            normalized_items.append(
                {
                    "instrumentType": _pick(item, ["instrumentType", "instrument_type"], "EQUITY"), # 默认设置为 EQUITY
                    "region": _pick(item, ["region", "regionCode"]),
                    "delay": _pick(item, ["delay", "lag"]),
                    "universe": _pick(item, ["universe", "universeName"]),
                }
            )

# Deduplicate normalized combos.
        normalized_json_strings = _dedupe(
            [json.dumps(x, sort_keys=True) for x in normalized_items if any(x.values())]
        )
        combos = [json.loads(s) for s in normalized_json_strings]
        info_result = {"detail": detail, "availability": combos}
        logger.info(f"Availability info for field '{field_name}': {info_result.get('availability')}")
        return info_result
    except Exception as e:
        logger.error(f"Error parsing datafield availability for '{field_name}': {e}", exc_info=True)
        info_result = {"availability": [], "error": "Datafield not found or error parsing."}
        logger.info(f"Availability info for field '{field_name}': {info_result.get('availability')}")
        return info_result

def find_common_availabilities(session: requests.Session, datafields: List[str]) -> List[Dict]:
    if not datafields:
        logger.info("No datafields provided to find common availabilities.")
        return []

common_settings = None

for field in datafields:
        info = get_datafield_availability(session, field)

        if info.get("error") or not info.get("availability"):
            logger.warning(f"Field '{field}' has no availability info (likely local var). Skipping constraint.")
            continue

current_settings = set()
        for item in info["availability"]:
            normalized_item = {
                "instrumentType": item.get("instrumentType"),
                "region": item.get("region"),
                "delay": item.get("delay"),
                "universe": item.get("universe"),
            }
            current_settings.add(json.dumps(normalized_item, sort_keys=True))

if common_settings is None:
            common_settings = current_settings
        else:
            common_settings = common_settings.intersection(current_settings)

        if not common_settings:
            logger.info(f"Intersection empty after checking field '{field}'.")
            break # Optimized: if intersection is empty, no need to check further fields

if common_settings is None:
        logger.info("No common settings found across all valid datafields.")
        return []

result = [json.loads(s) for s in common_settings]
    logger.info(f"Final common availabilities: {result}")

    result.sort(key=lambda x: (x.get("region", ""), x.get("universe", ""), x.get("delay", 0)))

    return result

def get_alpha_variants(session: requests.Session, alpha: Dict, operators: List[Dict], simulation_options: Optional[pd.DataFrame] = None, target_region: Optional[str] = None) -> Dict:
    alpha_id = alpha.get("id", "Unknown")
    alpha_type = alpha.get("type")

    if alpha_type != "REGULAR":
        return {"id": alpha_id, "valid": False, "reason": "Not REGULAR type", "variants": []}

expr = _extract_expression(alpha)
    if not expr:
        return {"id": alpha_id, "valid": False, "reason": "No expression found", "variants": []}

operator_names = [op.get("name", "") for op in operators]
    _, fields = parse_expression(expr, operator_names)

    if not fields:
        return {"id": alpha_id, "valid": False, "reason": "No datafields found", "variants": []}

common_settings = find_common_availabilities(session, fields)

    if not common_settings:
        return {"id": alpha_id, "valid": False, "reason": "No common settings", "variants": []}

original_settings = alpha.get("settings", {})
    valid_variants = []

    for new_setting in common_settings:
        # Validate against simulation options if provided
        if simulation_options is not None:
            if not validate_setting(new_setting, simulation_options):
                logger.info(f"  Skipping: Invalid simulation setting combination ({new_setting.get('region')}/{new_setting.get('universe')}).")
                continue

if target_region and new_setting.get("region") != target_region:
            continue

is_duplicate = True
        for key in ["region", "universe", "delay", "instrumentType"]:
            val_orig = str(original_settings.get(key, ""))
            val_new = str(new_setting.get(key, ""))
            if val_orig != val_new:
                is_duplicate = False
                break

        if not is_duplicate:
            merged_settings = original_settings.copy()
            merged_settings.update(new_setting)

            if "language" not in merged_settings:
                merged_settings["language"] = "FASTEXPR"

if merged_settings.get("region") in ["ASI", "JPN", "HKG", "KOR", "TWN"]:
                merged_settings["maxTrade"] = "ON"

            payload = {
                "type": "REGULAR",
                "settings": merged_settings,
                "regular": expr,
            }

            valid_variants.append({
                "diff_settings": new_setting,
                "simulation_payload": payload
            })

    return {
        "id": alpha_id,
        "dateSubmitted": alpha.get("dateSubmitted"),
        "expression": expr,
        "valid": True,
        "variants": valid_variants,
        "original_settings": original_settings
    }

def set_alpha_properties(session: requests.Session, alpha_id: str, name: Optional[str] = None, tags: Optional[list[str]] = None):
    params = {k: v for k, v in [("name", name), ("tags", tags)] if v}
    if not params: return
    response = session.patch(f"{brain_api_url}/alphas/{alpha_id}", json=params)
    if response.ok: logger.info(f"Successfully set properties for alpha {alpha_id} (name='{name}', tags={tags}).")
    else: logger.warning(f"Failed to set properties for alpha {alpha_id}: {response.text}")

# Helper function: to_multi_alphas
def to_multi_alphas(alpha_list, batch_size=10):
    return [alpha_list[i:i + batch_size] for i in range(0, len(alpha_list), batch_size)]

# Modified simulate_multis function
def simulate_multis(session_manager, alphas_with_metadata_batch, name, tags):
    """
    模拟多个alpha表达式对应的某个地区的信息
    Modified to return structured results for each alpha in the batch.
    alphas_with_metadata_batch: A list of tuples, each containing (simulation_payload, variant_key, original_alpha_id, settings, expression).
    """
    if session_manager.session is None:
        session_manager.refresh_session()
    if time.time() - session_manager.start_time > session_manager.expiry_time:
        session_manager.refresh_session()

structured_results = []

    if not alphas_with_metadata_batch:
        return structured_results

# Extract only the alpha payloads for the API call
    simulation_data_for_post = [item[0] for item in alphas_with_metadata_batch]

    # Create a temporary map from alpha payload (by its 'regular' expression) to its variant_key
    # This is needed to re-associate variant_key with the results from the API
    payload_expr_to_variant_key_map = {
        item[0]['regular']: item[1] # Map expression to variant_key
        for item in alphas_with_metadata_batch
    }

simulation_progress_url = None
    while True:
        try:
            resp = session_manager.session.post(f"{brain_api_url}/simulations", json=simulation_data_for_post)
            simulation_progress_url = resp.headers.get('Location', None)
            if simulation_progress_url is None:
                json_data = resp.json()
                logger.error(f"Multi-sim start failed, no Location header. Response: {json_data}")
                # If multi-sim submission fails, all alphas in the batch fail
                for alpha_payload in simulation_data_for_post: # Iterate over submitted payloads
                    expr = alpha_payload['regular']
                    variant_key = payload_expr_to_variant_key_map.get(expr, "UNKNOWN_VARIANT_KEY")
                    structured_results.append({
                        'expression': expr,
                        'variant_key': variant_key,
                        'alpha_id': None,
                        'status': 'ERROR',
                        'message': f"Multi-sim submission failed: {json_data.get('detail', str(json_data))}"
                    })
                return structured_results
            else:
                logger.info(f'Multi-sim submission successful. Progress URL: {simulation_progress_url}')
                break
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during multi-sim submission: {e}", exc_info=True)
            time.sleep(60) # Wait before retrying submission
        except Exception as e:
            logger.error(f"An unexpected error occurred during multi-sim submission: {e}", exc_info=True)
            time.sleep(60) # Wait before retrying submission

# Check progress for the multi-sim
    get_start_time = time.time()
    polling_timeout = 1200 # 20 minutes

    while True:
        if time.time() - get_start_time > polling_timeout:
            logger.error(f"Multi-sim progress check timed out after {polling_timeout / 60} minutes for URL: {simulation_progress_url}. Assuming all alphas in batch failed.")
            for alpha_payload in simulation_data_for_post: # Iterate over submitted payloads
                expr = alpha_payload['regular']
                variant_key = payload_expr_to_variant_key_map.get(expr, "UNKNOWN_VARIANT_KEY")
                structured_results.append({
                    'expression': expr,
                    'variant_key': variant_key,
                    'alpha_id': None,
                    'status': 'ERROR',
                    'message': "Multi-sim progress check timed out."
                })
            return structured_results

try:
            resps = session_manager.session.get(simulation_progress_url)
            json_data = resps.json()
            headers = resps.headers
            retry_after = headers.get('Retry-After', 0)

if retry_after == 0:
                status = json_data.get("status")
                if status == 'COMPLETE':
                    logger.info(f'Multi-sim completed: {simulation_progress_url}')
                    break
                elif status == 'ERROR':
                    logger.error(f"Error in multi-sim: {simulation_progress_url}. Response: {json_data}")
                    # If multi-sim itself errors out, all children might be affected
                    for alpha_payload in simulation_data_for_post: # Iterate over submitted payloads
                        expr = alpha_payload['regular']
                        variant_key = payload_expr_to_variant_key_map.get(expr, "UNKNOWN_VARIANT_KEY")
                        structured_results.append({
                            'expression': expr,
                            'variant_key': variant_key,
                            'alpha_id': None,
                            'status': 'ERROR',
                            'message': f"Multi-sim failed with status ERROR: {json_data.get('detail', str(json_data))}"
                        })
                    return structured_results
                else:
                    logger.info(f"Multi-sim not complete yet (status: {status}): {simulation_progress_url}. Retrying after a short delay.")
                    time.sleep(5) # Poll every 5 seconds
            else:
                time.sleep(float(retry_after))
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during multi-sim progress check: {e}", exc_info=True)
            time.sleep(30) # Wait before retrying progress check
        except Exception as e:
            logger.error(f"An unexpected error occurred during multi-sim progress check: {e}", exc_info=True)
            time.sleep(30) # Wait before retrying progress check

    # Process individual alpha results from the multi-sim response
    children = json_data.get("children", [])
    if len(children) != len(simulation_data_for_post): # Compare with actual submitted payloads
        logger.warning(f"Number of children ({len(children)}) does not match number of submitted alphas ({len(simulation_data_for_post)}). This might indicate partial failure or an API issue.")

for i, alpha_payload in enumerate(simulation_data_for_post): # Iterate over submitted payloads
        expr = alpha_payload['regular']
        variant_key = payload_expr_to_variant_key_map.get(expr, "UNKNOWN_VARIANT_KEY") # Get variant_key using expression

        child_alpha_id = None
        child_status = 'ERROR'
        child_message = 'Unknown error or not processed.'

if i < len(children):
            child_url = f"{brain_api_url}/simulations/{children[i]}"
            try:
                child_progress_resp = session_manager.session.get(child_url)
                child_json_data = child_progress_resp.json()

                child_alpha_id = child_json_data.get("alpha")
                child_status = child_json_data.get("status")
                child_message = child_json_data.get("message", "")

if child_status == "COMPLETE":
                    logger.info(f"  -> Child alpha for expression '{expr}' (variant: {variant_key}) completed successfully with ID: {child_alpha_id}")
                    # Removed: set_alpha_properties call from here.
                    # Alpha properties will be set by run_batched_simulations.
                else:
                    logger.warning(f"  -> Child alpha for expression '{expr}' (variant: {variant_key}) failed (status: {child_status}, message: {child_message}).")

except requests.exceptions.RequestException as e:
                child_message = f"Request error fetching child sim details: {e}"
                logger.error(f"  -> {child_message}", exc_info=True)
            except Exception as e:
                child_message = f"Unexpected error fetching child sim details: {e}"
                logger.error(f"  -> {child_message}", exc_info=True)
        else:
            child_message = "No child simulation URL found for this alpha in multi-sim response."
            logger.warning(f"  -> {child_message} for expression '{expr}' (variant: {variant_key}).")

structured_results.append({
            'expression': expr,
            'variant_key': variant_key, # Add variant_key to the result
            'alpha_id': child_alpha_id,
            'status': child_status,
            'message': child_message
        })

    return structured_results

def _submit_single_simulation_with_retries(
    session: requests.Session, 
    payload: Dict,
    variant_key: str,
    original_alpha_id: str,
    hard_fail_attempts_in_memory: defaultdict,
    skipped_in_current_run: set,
    record_file: str 
) -> Tuple[bool, Union[Dict, str]]:
    """Helper to submit a single simulation with retry logic."""
    settings = payload.get("settings", {})

    # Check if this variant is already permanently failed in the current run
    if variant_key in skipped_in_current_run:
        logger.info(f"  -> Skipping variant {variant_key} (permanently failed in current run).")
        return False, "Permanently failed in current run."

max_submission_retries = 1000 
    initial_retry_delay = 2

for attempt in range(1, max_submission_retries + 1):
        try:
            resp = start_simulation(session, payload)

            if resp.status_code == 429 or (resp.status_code == 400 and "concurrent" in resp.text.lower()):
                logger.warning(f"  -> Concurrent error detected for {settings.get('region')}/{settings.get('universe')}. Retrying in 2 seconds (attempt {attempt}/{max_submission_retries}).")
                time.sleep(2) 
                continue 

            resp.raise_for_status() 

            result = simulation_progress(session, resp)
            success = result.get("completed")

            if not success:
                message = result.get("message", "Unknown simulation failure.")
                if "ERROR" in message.upper() or "FAIL" in message.upper() or "timed out" in message.lower():
                    hard_fail_attempts_in_memory[variant_key] += 1
                    logger.warning(f"  -> Hard failure detected for {variant_key}. Attempt {hard_fail_attempts_in_memory[variant_key]}/{3}.")

                    if hard_fail_attempts_in_memory[variant_key] >= 3:
                        logger.error(f"  -> Variant {variant_key} permanently failed after 3 hard attempts. Aborting all retries for this variant.")
                        skipped_in_current_run.add(variant_key) 

                        record = {
                            'timestamp': datetime.now().isoformat(),
                            'variant_key': variant_key,
                            'original_alpha_id': original_alpha_id,
                            'new_alpha_id': '', 
                            'settings': json.dumps(payload['settings']),
                            'expression': payload['regular'],
                            'status': 'PERMANENTLY_FAILED',
                            'message': f"Permanently failed after 3 ERROR/FAIL attempts: {message}"
                        }
                        try:
                            write_header = not os.path.exists(record_file) or os.stat(record_file).st_size == 0
                            pd.DataFrame([record]).to_csv(record_file, mode='a', header=write_header, index=False)
                        except Exception as csv_e:
                            logger.error(f"Failed to write permanent failure to record file: {csv_e}")
                        return False, f"Permanently failed after 3 ERROR/FAIL attempts: {message}"

                logger.warning(f"  -> Simulation for {settings.get('region')}/{settings.get('universe')} failed (transient or non-hard failure): {message}. Retrying in 2 seconds (attempt {attempt}/{max_submission_retries}).")
                time.sleep(2) 
                continue 

            return (True, result.get("result")) if success else (True, result.get("warning"))

        except requests.exceptions.RequestException as e:
            logger.warning(f"  -> Request error during simulation for {settings.get('region')}/{settings.get('universe')}: {e}. Retrying in 2 seconds (attempt {attempt}/{max_submission_retries}).", exc_info=True)
            time.sleep(2) 
            continue 
        except Exception as e:
            logger.error(f"  -> Unexpected error during simulation for {settings.get('region')}/{settings.get('universe')}: {e}", exc_info=True)
            return False, str(e)

    logger.error(f"  -> Failed to submit simulation for {settings.get('region')}/{settings.get('universe')} after {max_submission_retries} retries.")
    return False, f"Failed to submit simulation after {max_submission_retries} retries."

def run_batched_simulations(
    session: requests.Session, 
    payloads_with_metadata: List[Tuple[Dict, str, str, Dict, str]], 
    hard_fail_attempts_in_memory: defaultdict,
    skipped_in_current_run: set,
    record_file: str 
) -> List[Tuple[bool, Union[Dict, str], str, str, Dict, str]]:
    """
    Submits multiple simulation payloads in batches using the adapted simulate_multis function.

    Args:
        session: The requests session.
        payloads_with_metadata: A list of tuples, each containing (simulation_payload, variant_key, original_alpha_id, settings, expression).
        hard_fail_attempts_in_memory: Dictionary to track hard failures.
        skipped_in_current_run: Set to track variants permanently skipped in this run.
        record_file: Path to the record file for permanent failures.

    Returns:
        A list of tuples, where each tuple contains (success_status, result_or_message, variant_key, original_alpha_id, simulation_settings, simulation_expression) for each payload.
    """
    if not payloads_with_metadata:
        return []

all_results = []

    # Initialize SessionManager for simulate_multis
    session_start_time = time.time()
    # The session passed here is `requests.Session` from `run_yuanfen.py`'s main logic
    # It already has auth set up from brain_login.
    session_expiry_time = 3 * 60 * 60  # 3 hours
    session_manager = SessionManager(session, session_start_time, session_expiry_time)

# Filter out already skipped variants and prepare for batching
    active_payloads_with_metadata = []
    for payload, variant_key, original_alpha_id, simulation_settings, simulation_expression in payloads_with_metadata:
        if variant_key in skipped_in_current_run:
            logger.info(f"  -> Skipping variant {variant_key} (permanently failed in current run) before batching.")
            all_results.append((False, "Permanently failed in current run.", variant_key, original_alpha_id, simulation_settings, simulation_expression))
            continue
        active_payloads_with_metadata.append((payload, variant_key, original_alpha_id, simulation_settings, simulation_expression))

if not active_payloads_with_metadata:
        return all_results # All were skipped

batches_of_alpha_payloads_with_metadata = to_multi_alphas(active_payloads_with_metadata, batch_size=5)

# Create a reverse map from variant_key to its full metadata
    # This is needed because simulate_multis will now return variant_key in its structured results.
    expression_to_metadata_map = {
        item[1]: (item[0], item[1], item[2], item[3], item[4]) # item[1] is variant_key
        for item in active_payloads_with_metadata
    }

logger.info(f"  -> Submitting {len(active_payloads_with_metadata)} simulations in {len(batches_of_alpha_payloads_with_metadata)} batches using simulate_multis.")

for batch_idx, batch_alpha_payloads in enumerate(batches_of_alpha_payloads_with_metadata):
        logger.info(f"  -> Processing batch {batch_idx + 1}/{len(batches_of_alpha_payloads_with_metadata)} with {len(batch_alpha_payloads)} alphas.")

        try:
            # Call simulate_multis
            # The 'name' and 'tags' arguments for simulate_multis are used for setting alpha properties.
            # I'll use a generic name and the 'run_yuanfen' tag.
            multi_sim_structured_results = simulate_multis(
                session_manager, 
                batch_alpha_payloads, 
                name="yuanfen_batch_sim", 
                tags=['run_yuanfen']
            )

if not multi_sim_structured_results:
                logger.error(f"simulate_multis returned empty results for batch {batch_idx + 1}.")
                # If simulate_multis returns empty, treat all in batch as failed
                for alpha_payload in batch_alpha_payloads:
                    expr = alpha_payload['regular']
                    _, variant_key, original_alpha_id, simulation_settings, simulation_expression = expression_to_metadata_map[expr]

                    hard_fail_attempts_in_memory[variant_key] += 1
                    logger.warning(f"  -> Batch failure for alpha {variant_key}. Attempt {hard_fail_attempts_in_memory[variant_key]}/{3}.")

                    if variant_key in skipped_in_current_run:
                        all_results.append((False, "Permanently failed in current run.", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                        continue

if hard_fail_attempts_in_memory[variant_key] >= 3:
                        logger.error(f"  -> Variant {variant_key} permanently failed after 3 hard attempts due to batch error. Aborting all retries for this variant.")
                        skipped_in_current_run.add(variant_key)
                        record = {
                            'timestamp': datetime.now().isoformat(),
                            'variant_key': variant_key,
                            'original_alpha_id': original_alpha_id,
                            'new_alpha_id': '', 
                            'settings': json.dumps(simulation_settings),
                            'expression': simulation_expression,
                            'status': 'PERMANENTLY_FAILED',
                            'message': "Batch failed: simulate_multis returned empty results."
                        }
                        try:
                            write_header = not os.path.exists(record_file) or os.stat(record_file).st_size == 0
                            pd.DataFrame([record]).to_csv(record_file, mode='a', header=write_header, index=False)
                        except Exception as csv_e:
                            logger.error(f"Failed to write permanent failure to record file: {csv_e}")
                        all_results.append((False, "Permanently failed after 3 ERROR/FAIL attempts due to batch error.", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                    else:
                        all_results.append((False, "Batch failed: simulate_multis returned empty results.", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                continue # Move to next batch

# Process individual alpha results from the multi-sim response
            for individual_result in multi_sim_structured_results:
                variant_key = individual_result.get('variant_key') # Get variant_key directly from result
                new_alpha_id = individual_result.get('alpha_id')
                status = individual_result.get('status')
                message = individual_result.get('message', '')

# Retrieve original metadata using the variant_key
                original_payload, _, original_alpha_id, simulation_settings, simulation_expression = expression_to_metadata_map.get(variant_key, (None, None, None, None, None))

                # If variant_key is not found in map (should not happen if map is correctly built)
                if variant_key is None or original_alpha_id is None:
                    logger.error(f"  -> Could not find original metadata for variant_key {variant_key} from simulate_multis result. Skipping result.")
                    continue

if status == "COMPLETE":
                    logger.info(f"  -> Multi-sim alpha {variant_key} completed successfully with new ID: {new_alpha_id}.")
                    all_results.append((True, {"id": new_alpha_id}, variant_key, original_alpha_id, simulation_settings, simulation_expression))
                else:
                    # This is an individual alpha failure within a multi-sim
                    hard_fail_attempts_in_memory[variant_key] += 1
                    logger.warning(f"  -> Multi-sim alpha {variant_key} failed (status: {status}, message: {message}). Attempt {hard_fail_attempts_in_memory[variant_key]}/{3}.")

                    if variant_key in skipped_in_current_run: # Already permanently failed
                        all_results.append((False, "Permanently failed in current run.", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                        continue

if hard_fail_attempts_in_memory[variant_key] >= 3:
                        logger.error(f"  -> Variant {variant_key} permanently failed after 3 hard attempts. Aborting all retries for this variant.")
                        skipped_in_current_run.add(variant_key)

                        record = {
                            'timestamp': datetime.now().isoformat(),
                            'variant_key': variant_key,
                            'original_alpha_id': original_alpha_id,
                            'new_alpha_id': '', 
                            'settings': json.dumps(simulation_settings),
                            'expression': simulation_expression,
                            'status': 'PERMANENTLY_FAILED',
                            'message': f"Permanently failed after 3 ERROR/FAIL attempts: {message}"
                        }
                        try:
                            write_header = not os.path.exists(record_file) or os.stat(record_file).st_size == 0
                            pd.DataFrame([record]).to_csv(record_file, mode='a', header=write_header, index=False)
                        except Exception as csv_e:
                            logger.error(f"Failed to write permanent failure to record file: {csv_e}")
                        all_results.append((False, f"Permanently failed after 3 ERROR/FAIL attempts: {message}", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                    else:
                        all_results.append((False, message, variant_key, original_alpha_id, simulation_settings, simulation_expression))

except Exception as exc:
            logger.error(f"  -> Exception during simulate_multis for batch {batch_idx + 1}: {exc}", exc_info=True)
            # If the entire multi-sim call fails, all alphas in the batch are affected
            for item in batch_alpha_payloads_with_metadata[batch_idx]: # Iterate over the original items in the batch
                _, variant_key, original_alpha_id, simulation_settings, simulation_expression = item # Unpack the item

                hard_fail_attempts_in_memory[variant_key] += 1
                logger.warning(f"  -> Batch failure for alpha {variant_key}. Attempt {hard_fail_attempts_in_memory[variant_key]}/{3}.")

                if variant_key in skipped_in_current_run: # Already permanently failed
                    all_results.append((False, "Permanently failed in current run.", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                    continue

if hard_fail_attempts_in_memory[variant_key] >= 3:
                    logger.error(f"  -> Variant {variant_key} permanently failed after 3 hard attempts due to batch error. Aborting all retries for this variant.")
                    skipped_in_current_run.add(variant_key)

                    record = {
                        'timestamp': datetime.now().isoformat(),
                        'variant_key': variant_key,
                        'original_alpha_id': original_alpha_id,
                        'new_alpha_id': '', 
                        'settings': json.dumps(simulation_settings),
                        'expression': simulation_expression,
                        'status': 'PERMANENTLY_FAILED',
                        'message': f"Permanently failed after 3 ERROR/FAIL attempts due to batch error: {exc}"
                    }
                    try:
                        write_header = not os.path.exists(record_file) or os.stat(record_file).st_size == 0
                        pd.DataFrame([record]).to_csv(record_file, mode='a', header=write_header, index=False)
                    except Exception as csv_e:
                        logger.error(f"Failed to write permanent failure to record file: {csv_e}")
                    all_results.append((False, f"Permanently failed after 3 ERROR/FAIL attempts due to batch error: {exc}", variant_key, original_alpha_id, simulation_settings, simulation_expression))
                else:
                    all_results.append((False, str(exc), variant_key, original_alpha_id, simulation_settings, simulation_expression))

    return all_results

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # 将日志级别改为 DEBUG

def get_credentials_from_file(file_path: str = 'user_info.txt') -> tuple[Optional[str], Optional[str]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f: data = f.read().strip().split('\n')
        user_data = {line.split(': ')[0]: line.split(': ')[1] for line in data if ': ' in line}
        username = user_data.get('username', "''")[1:-1]
        password = user_data.get('password', "''")[1:-1]
        if not username or not password:
            logger.warning(f"Username or password not found/empty in {file_path}.")
            return None, None
        return username, password
    except FileNotFoundError:
        return None, None
    except Exception as e:
        logger.error(f"Error parsing {file_path}: {e}")
        return None, None

def run_variant_mode(session, date_range, alpha_ids, target_region, simulate, record_file, output_file):
    logger.info("--- Running in Variant Generation Mode ---")
    os.makedirs(os.path.dirname(record_file), exist_ok=True)

    processed_variants = set() 
    permanently_failed_variants = set() 

    hard_fail_attempts_in_memory = defaultdict(int)
    skipped_in_current_run = set()

record_file_headers = ['timestamp', 'variant_key', 'original_alpha_id', 'new_alpha_id', 'settings', 'expression', 'status', 'message']
    if os.path.exists(record_file):
        try:
            history_df = pd.read_csv(record_file)
            if all(header in history_df.columns for header in ['variant_key', 'status']):
                successful_records = history_df[history_df['status'] == 'SUCCESS']
                processed_variants = set(successful_records['variant_key'].dropna())
                logger.info(f"Loaded {len(processed_variants)} previously successful variants from '{record_file}'.")

failed_records = history_df[history_df['status'] == 'PERMANENTLY_FAILED']
                permanently_failed_variants = set(failed_records['variant_key'].dropna())
                logger.info(f"Loaded {len(permanently_failed_variants)} previously permanently failed variants from '{record_file}'.")
            else:
                logger.warning(f"'{record_file}' exists but missing expected columns. Starting with empty history.")
                pd.DataFrame(columns=record_file_headers).to_csv(record_file, index=False)
        except Exception as e:
            logger.warning(f"Could not read record file {record_file}: {e}. Starting with empty history.")
            pd.DataFrame(columns=record_file_headers).to_csv(record_file, index=False)
    else:
        logger.info(f"Record file '{record_file}' not found. Creating a new one with headers.")
        pd.DataFrame(columns=record_file_headers).to_csv(record_file, index=False)

if date_range:
        alphas_to_process = fetch_alphas_by_date_range(session, date_range[0], date_range[1])
    elif alpha_ids:
        alphas_to_process = fetch_alphas_by_ids(session, alpha_ids)
    else:
        logger.error("For 'variant' mode, either --date-range or --alpha-ids must be provided.")
        return

if not alphas_to_process:
        logger.info("No alphas found to process. Exiting.")
        return

logger.info(f"Found {len(alphas_to_process)} alpha(s) to process.")
    operators = fetch_operators(session)

    logger.info("Fetching platform setting options...")
    simulation_options = None
    try:
        simulation_options = get_platform_setting_options(session)
        logger.info("Platform setting options fetched successfully.")
    except Exception as e:
        logger.warning(f"Failed to fetch platform setting options: {e}")

all_collected_variants = []
    for alpha in alphas_to_process:
        original_alpha_id = alpha.get('id')
        logger.info(f"\n--- Analyzing Alpha: {original_alpha_id} ---")
        analysis_result = get_alpha_variants(session, alpha, operators, simulation_options, target_region)

        if not analysis_result.get("valid") or not analysis_result.get("variants"):
            logger.info(f"No valid variants found for alpha {original_alpha_id}.")
            continue

logger.info(f"Found {len(analysis_result['variants'])} variant(s) for alpha {original_alpha_id}" + (f" in region {target_region}" if target_region else ""))

        for variant in analysis_result['variants']:
            variant_key = f"{original_alpha_id}::{json.dumps(variant['diff_settings'], sort_keys=True)}"

            if variant_key in processed_variants:
                logger.info(f"  Skipping variant (already processed): {variant_key}")
                skipped_in_current_run.add(variant_key) 
                continue
            if variant_key in permanently_failed_variants:
                logger.info(f"  Skipping variant (permanently failed from history): {variant_key}")
                skipped_in_current_run.add(variant_key) 
                continue
            if variant_key in skipped_in_current_run: 
                logger.info(f"  Skipping variant (permanently failed in current run): {variant_key}")
                continue

            variant['original_alpha_id'] = original_alpha_id
            variant['variant_key'] = variant_key
            all_collected_variants.append(variant)

if not simulate or not all_collected_variants:
        logger.info("No variants to simulate or simulate flag is false. Exiting variant mode.")
        if all_collected_variants: 
            final_analysis_results = [v for v in all_collected_variants if v['variant_key'] not in skipped_in_current_run]
            if final_analysis_results:
                with open(output_file or "yuanfen_results.json", 'w', encoding='utf-8') as f: json.dump(final_analysis_results, f, indent=2)
                logger.info(f"Analysis complete. Results saved to {output_file or 'yuanfen_results.json'}.")
        return

grouped_variants = defaultdict(list)
    for variant in all_collected_variants:
        settings = variant['simulation_payload']['settings']
        group_key = (
            settings.get('region'),
            settings.get('instrumentType', 'EQUITY'),
            settings.get('universe', 'TOP3000'),
            settings.get('delay', 1)
        )
        grouped_variants[group_key].append(variant)

logger.info(f"Starting batched simulations for {len(all_collected_variants)} variants across {len(grouped_variants)} groups.")

    all_simulation_results = [] 
    for group_key, variants_in_group in grouped_variants.items():
        region, inst_type, universe, delay = group_key
        logger.info(f"\n--- Processing batch for Region: {region}, InstType: {inst_type}, Universe: {universe}, Delay: {delay} ({len(variants_in_group)} variants) ---")

        payloads_for_batch_with_metadata = [
            (v['simulation_payload'], v['variant_key'], v['original_alpha_id'], v['simulation_payload']['settings'], v['simulation_payload']['regular'])
            for v in variants_in_group
        ]

        batch_results = run_batched_simulations(
            session, 
            payloads_for_batch_with_metadata,
            hard_fail_attempts_in_memory,
            skipped_in_current_run,
            record_file 
        )

        for success, result_or_msg, variant_key, original_alpha_id, simulation_settings, simulation_expression in batch_results:
            if success and (new_alpha_id := result_or_msg.get("id")):
                set_alpha_properties(session, new_alpha_id, name=original_alpha_id, tags=['run_yuanfen'])
                record = {
                    'timestamp': datetime.now().isoformat(),
                    'variant_key': variant_key,
                    'original_alpha_id': original_alpha_id,
                    'new_alpha_id': new_alpha_id,
                    'settings': json.dumps(simulation_settings),
                    'expression': simulation_expression,
                    'status': 'SUCCESS',
                    'message': 'Simulation completed successfully.'
                }
                write_header = not os.path.exists(record_file) or os.stat(record_file).st_size == 0
                pd.DataFrame([record]).to_csv(record_file, mode='a', header=write_header, index=False)
                processed_variants.add(variant_key) 

                matched_variant = {
                    'original_alpha_id': original_alpha_id,
                    'variant_key': variant_key,
                    'new_alpha_id': new_alpha_id,
                    'simulation_payload': {
                        'settings': simulation_settings,
                        'regular': simulation_expression
                    }
                }
                all_simulation_results.append(matched_variant)
            else:
                if variant_key not in skipped_in_current_run: 
                     logger.error(f"  -> Batched simulation for variant {variant_key} failed: {result_or_msg}")

    if all_simulation_results:
        with open(output_file or "yuanfen_results.json", 'w', encoding='utf-8') as f: json.dump(all_simulation_results, f, indent=2)
        logger.info(f"Processing complete. Results saved to {output_file or 'yuanfen_results.json'}.")
    else:
        logger.info("Processing complete. No valid variants were found or simulated.")

def run_download_mode(session, tag, target_region):
    logger.info("--- Running in Download Mode ---")
    os_alphas_cache_path = 'cache/os_alphas'
    os_pnls_cache_path = 'cache/os_pnls'
    os_alpha_ids_cache_path = 'cache/os_alpha_ids'
    unsubmitted_alphas_details_cache_path = 'cache/unsubmitted_alphas_details'
    target_pnl_cache_path = 'cache/target_pnl_cache'
    os.makedirs('cache', exist_ok=True)

# 初始加载 OS alpha 缓存
    cached_all_os_alphas = []
    cached_os_alpha_pnls = pd.DataFrame()
    cached_os_alpha_ids_by_region = defaultdict(list)

if os.path.exists(os_alphas_cache_path + '.pickle') and \
       os.path.exists(os_pnls_cache_path + '.pickle') and \
       os.path.exists(os_alpha_ids_cache_path + '.pickle'):
        logger.info("Loading OS alphas, PnLs, and regional IDs from cache...")
        cached_all_os_alphas = load_obj(os_alphas_cache_path)
        cached_os_alpha_pnls = load_obj(os_pnls_cache_path)
        cached_os_alpha_ids_by_region = load_obj(os_alpha_ids_cache_path)

# 确保加载的缓存类型正确
        if not isinstance(cached_os_alpha_pnls, pd.DataFrame):
            logger.warning(f"Cached PnLs at {os_pnls_cache_path}.pickle is not a DataFrame, resetting.")
            cached_os_alpha_pnls = pd.DataFrame()
        if not isinstance(cached_os_alpha_ids_by_region, defaultdict):
            logger.warning(f"Cached alpha IDs at {os_alpha_ids_cache_path}.pickle is not a defaultdict, resetting.")
            cached_os_alpha_ids_by_region = defaultdict(list)

    # 获取最新的所有 OS alpha
    latest_all_os_alphas = get_all_user_alphas(session)

# 找出新的 OS alpha
    cached_os_alpha_ids_set = {alpha['id'] for alpha in cached_all_os_alphas if 'id' in alpha}
    new_os_alphas_to_process = [alpha for alpha in latest_all_os_alphas if alpha['id'] not in cached_os_alpha_ids_set]

if new_os_alphas_to_process:
        logger.info(f"Found {len(new_os_alphas_to_process)} new OS alphas. Fetching their PnLs and updating cache...")
        updated_os_alpha_pnls, updated_os_alpha_ids_by_region = get_alpha_pnls(session, new_os_alphas_to_process, 
                                                                              alpha_pnls=cached_os_alpha_pnls, 
                                                                              alpha_ids=cached_os_alpha_ids_by_region)

        # 更新总的 OS alpha 列表
        all_os_alphas = latest_all_os_alphas # 使用最新的所有 alpha
        os_alpha_pnls = updated_os_alpha_pnls
        os_alpha_ids_by_region = updated_os_alpha_ids_by_region

# 保存更新后的 OS alpha 缓存
        save_obj(all_os_alphas, os_alphas_cache_path)
        save_obj(os_alpha_pnls, os_pnls_cache_path)
        save_obj(os_alpha_ids_by_region, os_alpha_ids_cache_path)
    else:
        logger.info("No new OS alphas found. Using existing cached data for OS alphas.")
        all_os_alphas = cached_all_os_alphas
        os_alpha_pnls = cached_os_alpha_pnls
        os_alpha_ids_by_region = cached_os_alpha_ids_by_region

    # 初始加载未提交 alpha 详情缓存
    cached_unsubmitted_alphas_details = {}
    if os.path.exists(unsubmitted_alphas_details_cache_path + '.pickle'):
        logger.info("Loading unsubmitted alphas details from cache...")
        cached_unsubmitted_alphas_details = load_obj(unsubmitted_alphas_details_cache_path)

# 模拟 get_alphas_by_days 中的 sharpe 和 fitness 逻辑
    sharpe = 0.9
    fitness = 0.5
    days = 30 # 默认获取最近30天的alpha

today = datetime.now().date()
    start_date = today - timedelta(days=days)
    end_date = today + timedelta(days=1)

# 获取未提交的 alpha
    target_alphas, updated_unsubmitted_alphas_details = _get_unsubmitted_alphas_details(session, tag=tag, target_region=target_region, cached_alphas_details=cached_unsubmitted_alphas_details)

    # 保存更新后的未提交 alpha 详情缓存
    save_obj(updated_unsubmitted_alphas_details, unsubmitted_alphas_details_cache_path)

if not target_alphas: return logger.info("No alphas with specified tag found.")

# 初始加载 target PnL 缓存
    cached_target_pnls = {}
    if os.path.exists(target_pnl_cache_path + '.pickle'):
        logger.info("Loading target PnLs from cache...")
        cached_target_pnls = load_obj(target_pnl_cache_path)

# 加载 SelfCorr 和 PPAC 的参考数据
    os_alpha_ids_selfcorr, os_alpha_rets_selfcorr = load_data(tag='SelfCorr')
    ppac_alpha_ids, ppac_alpha_rets = load_data(tag='PPAC')

processed_data = []
    for alpha in target_alphas:
        alpha_id = alpha.get('id')
        full_details = alpha 

        alpha_region = full_details.get('settings', {}).get('region')
        if target_region and alpha_region != target_region: continue

        logger.info(f"Processing alpha {alpha_id} in region {alpha_region}...")

# 使用 _get_alpha_pnl 获取 PnL
        target_pnl = None
        if alpha_id in cached_target_pnls:
            target_pnl = cached_target_pnls[alpha_id]
            logger.info(f"Loaded PnL for {alpha_id} from cache.")
        else:
            try:
                target_pnl_df = _get_alpha_pnl(session, alpha_id) 
                if not target_pnl_df.empty:
                    target_pnl = target_pnl_df.set_index('Date')[alpha_id]
                    cached_target_pnls[alpha_id] = target_pnl # 更新缓存
                    logger.info(f"Fetched PnL for {alpha_id} and added to cache.")
                else:
                    logger.warning(f"Empty PnL for {alpha_id}. Skipping.")
                    continue
            except Exception as e:
                logger.error(f"Could not get PnL for {alpha_id}: {e}. Skipping.")
                continue

        # 确保 target_pnl 不是 None 且不为空
        if target_pnl is None or target_pnl.empty:
            logger.warning(f"Target PnL for {alpha_id} is empty after caching check. Skipping.")
            continue

# 计算 self_corr
        self_corr = calc_self_corr(session, alpha_id, os_alpha_rets=os_alpha_rets_selfcorr, os_alpha_ids=os_alpha_ids_selfcorr, alpha_result=full_details, alpha_pnls=target_pnl)

        # 计算 ppac_sorr
        ppac_sorr = calc_self_corr(session, alpha_id, os_alpha_rets=ppac_alpha_rets, os_alpha_ids=ppac_alpha_ids, alpha_result=full_details, alpha_pnls=target_pnl)

        processed_data.append({
            'id': alpha_id,
            'parent_id': full_details.get('name', alpha_id), # 新增 parent_id 字段，如果 name 缺失则使用 alpha_id
            'region': alpha_region,
            'is_selfCorrelation': round(self_corr, 2),
            'ppac_sorr': round(ppac_sorr, 2),
            'expression': _extract_expression(full_details),
            'sharpe': full_details.get('is', {}).get('sharpe'),
            'fitness': full_details.get('is', {}).get('fitness'),
            'turnover': full_details.get('is', {}).get('turnover') * 100,
            'margin': full_details.get('is', {}).get('margin') * 10000,
            'pyramids': ' '.join([p.get('name', '') for p in next((check for check in full_details.get('is', {}).get('checks', []) if check.get('name') == 'MATCHES_PYRAMID'), {}).get('pyramids', [])])
        })

# 保存更新后的 target PnL 缓存
    save_obj(cached_target_pnls, target_pnl_cache_path)

if not processed_data: return logger.info("No data to save after processing.")
    output_df = pd.DataFrame(processed_data).sort_values(by=['region', 'is_selfCorrelation'], ascending=[True, True])

    # 确保 is_selfCorrelation 和 ppac_sorr 列是数值类型，然后格式化为两位小数的字符串
    output_df['is_selfCorrelation'] = output_df['is_selfCorrelation'].apply(lambda x: f"{x:.2f}")
    output_df['ppac_sorr'] = output_df['ppac_sorr'].apply(lambda x: f"{x:.2f}")

filename = f"run_yuanfen_{target_region}_candidates.csv" if target_region else "run_yuanfen_ALL_candidates.csv"
    output_path = os.path.join("submit", filename)
    os.makedirs("submit", exist_ok=True)
    output_df.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"Successfully saved {len(output_df)} alphas to {output_path}")

def run_interactive_mode(session):
    while True:
        print("\n--- Interactive Mode ---")
        print("1. Find Variants")
        print("2. Download Tagged Alphas")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

if choice == '1':
            sub_choice = input("  Fetch by (1) Date Range or (2) Alpha IDs? ")
            date_range, ids = None, None
            if sub_choice == '1':
                start = input("  Enter start date (YYYY-MM-DD): ")
                end = input("  Enter end date (YYYY-MM-DD): ")
                date_range = [start, end]
            elif sub_choice == '2':
                ids_str = input("  Enter comma-separated Alpha IDs: ")
                ids = [s.strip() for s in ids_str.split(',')]
            else:
                print("  Invalid choice.")
                continue

            region = input("  Enter target region (or leave blank for all): ")
            simulate = input("  Run simulations? (y/n): ").lower() == 'y'
            output = input("  Enter output JSON file name (default: yuanfen_results.json): ")

            run_variant_mode(session, date_range, ids, region or None, simulate, "records/yuanfen_history.csv", output)

elif choice == '2':
            tag = input("  Enter tag to download (default: run_yuanfen): ") or "run_yuanfen"
            region = input("  Enter target region (or leave blank for all): ")
            run_download_mode(session, tag, region or None)

elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Standalone BRAIN Alpha Tool.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interactive', action='store_true', help="Run in interactive mode.")
    parser.add_argument("--mode", required=False, choices=['variant', 'download'], help="Mode: 'variant' or 'download'. Required if not in interactive mode.")

    variant_group = parser.add_argument_group('Variant Mode')
    variant_group.add_argument("--date-range", nargs=2, metavar=('START', 'END'), help="Date range for 'variant' mode.")
    variant_group.add_argument("--alpha-ids", help="Comma-separated IDs for 'variant' mode.")
    variant_group.add_argument("--simulate", action='store_true', help="Run simulations for found variants.")
    variant_group.add_argument("--record-file", default="records/yuanfen_history.csv", help="History file for simulations.")

download_group = parser.add_argument_group('Download Mode')
    download_group.add_argument("--tag", default="run_yuanfen", help="Tag to filter alphas.")

parser.add_argument("--target-region", help="Optional: Filter by region.")
    parser.add_argument("--output-file", help="Output file (for variant mode).")

    args = parser.parse_args()

username, password = get_credentials_from_file()
    if not username or not password:
        logger.info("Could not load credentials from file, prompting.")
        username = input("Enter BRAIN Username (Email): ")
        password = getpass.getpass("Enter BRAIN Password: ")

try:
        session = brain_login(username, password)
    except Exception as e:
        logger.error(f"Login failed: {e}")
        sys.exit(1)

if args.interactive or not args.mode:
        run_interactive_mode(session)
    elif args.mode == 'variant':
        run_variant_mode(session, args.date_range, [s.strip() for s in args.alpha_ids.split(',')] if args.alpha_ids else None, args.target_region, args.simulate, args.record_file, args.output_file)
    elif args.mode == 'download':
        run_download_mode(session, args.tag, args.target_region)

if __name__ == "__main__":
    main()

---

### 评论 #5 (作者: YQ84572, 时间: 6个月前)

很详细的分享，可以监控变体生成的数据和自相关，很方便做研究和筛选
====================================================================================
祝大佬base多多，vf高高，分享更多小妙招～～
====================================================================================

---

### 评论 #6 (作者: MZ45384, 时间: 6个月前)

wow，真是巨大的工程量，大佬的代码能力可见一斑，但是能介绍一些变体案列吗，还是跟app中的缘分一道桥一样。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

