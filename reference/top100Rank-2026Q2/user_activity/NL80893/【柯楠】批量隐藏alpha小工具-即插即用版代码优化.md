# 【柯楠】批量隐藏alpha小工具-即插即用版代码优化

- **链接**: 【柯楠】批量隐藏alpha小工具-即插即用版代码优化.md
- **作者**: NL80893
- **发布时间/热度**: 8个月前, 得票: 92

## 帖子正文

hello~小伙伴们，相信大家在筛选alpha时都会遇到一个小问题，就是alpha的量太大！筛选起来困难重重。虽然有些同学会使用color等小工具进行设置，但不隐藏或者手动隐藏会十分的废手+废鼠标+费时间。柯楠经过测试了之后，给大家开发了一个小工具，即可以用代码实现批量隐藏alpha，但此代码只针对color的设置哦，如果你需要用其他的隐藏条件，可以自己修改哈。以下是代码正文及测试截图，支持自定义时间及颜色的选择，登录在终端交互就可以啦~import osimport requestsimport timeimport jsonfrom datetime import datetimefrom getpass import getpassfrom requests.adapters import HTTPAdapterfrom urllib3.util.retry import Retry# -------------------------- 基础配置 --------------------------brain_api_url = os.environ.get("BRAIN_API_URL", "https://api.worldquantbrain.com")INITIAL_REQUEST_INTERVAL = 1.0  # 初始请求间隔（秒）MAX_REQUEST_INTERVAL = 10.0     # 最大请求间隔（秒）LOGIN_RETRY_TIMES = 5           # 登录重试次数HIDE_RETRY_TIMES = 3            # 单个Alpha隐藏操作的重试次数# -------------------------- 筛选配置（可自定义修改） --------------------------TARGET_COLOR = "RED"  # 要隐藏的Alpha颜色，可改为"BLUE"、"GREEN"等# 时间范围配置（格式：YYYY-MM-DD，留空则不限制）START_DATE = "2025-01-01"  # 起始时间：隐藏≥该时间创建的AlphaEND_DATE = "2025-12-31"    # 结束时间：隐藏≤该时间创建的Alpha# 示例：隐藏所有蓝色Alpha → TARGET_COLOR="BLUE"，START_DATE=""，END_DATE=""# -------------------------- 工具函数 --------------------------def create_session_with_retries():"""创建带有自动重试机制的会话"""session = requests.Session()# 配置重试策略retry_strategy = Retry(total=3,backoff_factor=1,status_forcelist=[429, 500, 502, 503, 504],allowed_methods=["GET", "POST", "PATCH"])adapter = HTTPAdapter(max_retries=retry_strategy)session.mount("https://", adapter)session.mount("http://", adapter)session.timeout = 30  # 30秒超时return sessiondef login():"""交互式输入账号密码并登录"""print("\n请输入登录信息：")username = input("用户名：").strip()password = getpass("密码：").strip()if not username or not password:print("❌ 用户名和密码不能为空！")raise ValueError("用户名和密码不能为空")session = create_session_with_retries()for retry in range(LOGIN_RETRY_TIMES):try:session.auth = (username, password)response = session.post(f"{brain_api_url}/authentication")if response.status_code == 429:retry_after = int(response.headers.get('Retry-After', 5))print(f"⚠️ 登录请求被限流，将在{retry_after}秒后重试...")time.sleep(retry_after)continueresponse.raise_for_status()print(f"✅ 登录成功！")return sessionexcept requests.exceptions.HTTPError as e:if response.status_code == 401:print(f"⚠️ 第{retry+1}次登录失败：用户名或密码错误")else:print(f"⚠️ 第{retry+1}次登录失败：{str(e)}")except Exception as e:print(f"⚠️ 第{retry+1}次登录失败：{str(e)}")if retry < LOGIN_RETRY_TIMES - 1:sleep_time = min(INITIAL_REQUEST_INTERVAL * (2 ** retry), MAX_REQUEST_INTERVAL)print(f"将在{sleep_time:.1f}秒后重试...")time.sleep(sleep_time)else:print(f"❌ 登录重试{LOGIN_RETRY_TIMES}次均失败")raisedef get_target_color_alphas(session, target_color, start_date="", end_date=""):"""筛选指定颜色和时间范围内的未隐藏Alpha"""target_alphas = []offset = 0limit = 100current_interval = INITIAL_REQUEST_INTERVALprint(f"\n🔍 开始筛选 {target_color} 色Alpha（时间范围：{start_date if start_date else '不限'} 至 {end_date if end_date else '不限'}）...")# 构建时间筛选参数time_filters = ""if start_date:try:datetime.strptime(start_date, "%Y-%m-%d")time_filters += f"&dateCreated%3E={start_date}T00:00:00-04:00"except ValueError:print(f"❌ 起始时间格式错误：{start_date}，请使用YYYY-MM-DD格式")raiseif end_date:try:datetime.strptime(end_date, "%Y-%m-%d")time_filters += f"&dateCreated%3C={end_date}T23:59:59-04:00"except ValueError:print(f"❌ 结束时间格式错误：{end_date}，请使用YYYY-MM-DD格式")raisewhile True:url = (f"{brain_api_url}/users/self/alphas"f"?limit={limit}&offset={offset}"f"&color={target_color}&hidden=false&type=REGULAR"f"{time_filters}"f"&order=-dateCreated")try:response = session.get(url)if response.status_code == 429:retry_after = int(response.headers.get('Retry-After', 5))print(f"⚠️ 筛选请求被限流，将在{retry_after}秒后重试...")time.sleep(retry_after)continueif response.status_code == 504:print(f"⚠️ 网关超时，将在{current_interval}秒后重试...")time.sleep(current_interval)current_interval = min(current_interval * 2, MAX_REQUEST_INTERVAL)continueresponse.raise_for_status()data = response.json()total_count = data.get("count", 0)current_alphas = data.get("results", [])for alpha in current_alphas:target_alphas.append({"id": alpha["id"],"name": alpha.get("name", "未命名Alpha"),"create_time": alpha.get("dateCreated", "未知时间")})processed = min(offset + limit, total_count)latest_time = current_alphas[0]['dateCreated'][:10] if current_alphas else '无'print(f"   已筛选：{processed}/{total_count} 个（最新创建时间：{latest_time}）")current_interval = INITIAL_REQUEST_INTERVALif offset + limit >= total_count:breakoffset += limittime.sleep(current_interval)except Exception as e:error_msg = str(e)print(f"⚠️ 筛选出错（offset={offset}）：{error_msg}")current_interval = min(current_interval * 2, MAX_REQUEST_INTERVAL)print(f"将在{current_interval}秒后重试...")time.sleep(current_interval)continueprint(f"✅ 筛选完成！共找到 {len(target_alphas)} 个符合条件的{target_color}色Alpha")return target_alphasdef hide_alpha(session, alpha_id, alpha_name, alpha_create_time, color):"""隐藏单个Alpha"""url = f"{brain_api_url}/alphas/{alpha_id}"update_params = {"hidden": True}current_interval = INITIAL_REQUEST_INTERVALfor retry in range(HIDE_RETRY_TIMES):try:response = session.patch(url, json=update_params)if response.status_code == 429:retry_after = int(response.headers.get('Retry-After', 5))print(f"⚠️ 隐藏请求被限流，将在{retry_after}秒后重试...")time.sleep(retry_after)continueif response.status_code == 504:print(f"⚠️ 网关超时，将在{current_interval}秒后重试...")time.sleep(current_interval)current_interval = min(current_interval * 2, MAX_REQUEST_INTERVAL)continueresponse.raise_for_status()# 验证隐藏结果verify_response = session.get(url)if verify_response.status_code == 429:retry_after = int(verify_response.headers.get('Retry-After', 5))print(f"⚠️ 验证请求被限流，将在{retry_after}秒后重试...")time.sleep(retry_after)continueverify_data = verify_response.json()if verify_data.get("hidden", False):print(f"✅ 隐藏成功：{alpha_name}（ID：{alpha_id}，创建时间：{alpha_create_time[:10]}，颜色：{color}）")return Trueelse:raise Exception("修改后hidden仍为False")except Exception as e:error_msg = str(e)if retry < HIDE_RETRY_TIMES - 1:current_interval = min(current_interval * 2, MAX_REQUEST_INTERVAL)print(f"⚠️ 第{retry+1}次隐藏失败：{alpha_name}（ID：{alpha_id}），错误：{error_msg}，将在{current_interval}秒后重试...")time.sleep(current_interval)else:print(f"❌ 隐藏失败：{alpha_name}（ID：{alpha_id}），错误：{error_msg}")return Falsedef batch_hide_alphas_by_color(target_color, start_date="", end_date=""):"""主流程：登录→筛选指定颜色Alpha→批量隐藏"""print("=" * 70)print(f"📌 WorldQuant Brain 批量隐藏Alpha小工具")print("=" * 70)# 1. 登录获取会话session = login()# 2. 筛选指定颜色和时间范围的Alphatarget_alphas = get_target_color_alphas(session, target_color, start_date, end_date)if not target_alphas:print(f"\n🎉 没有找到需要隐藏的Alpha，程序结束！")return# 3. 批量执行隐藏操作print(f"\n🚀 开始批量隐藏（共{len(target_alphas)}个{target_color}色Alpha）...")success_count = 0fail_count = 0fail_ids = []current_interval = INITIAL_REQUEST_INTERVALfor idx, alpha in enumerate(target_alphas, 1):alpha_id = alpha["id"]alpha_name = alpha["name"]alpha_create_time = alpha["create_time"]print(f"\n[{idx}/{len(target_alphas)}] 处理：{alpha_name}（ID：{alpha_id}）")if hide_alpha(session, alpha_id, alpha_name, alpha_create_time, target_color):success_count += 1current_interval = INITIAL_REQUEST_INTERVALelse:fail_count += 1fail_ids.append((alpha_id, alpha_name, alpha_create_time[:10]))current_interval = min(current_interval * 1.5, MAX_REQUEST_INTERVAL)time.sleep(current_interval)# 4. 输出统计结果print("\n" + "=" * 70)print(f"📊 批量隐藏完成（{target_color}色，时间范围：{start_date if start_date else '不限'} 至 {end_date if end_date else '不限'}）：")print(f"   总数量：{len(target_alphas)} 个")print(f"   成功隐藏：{success_count} 个")print(f"   隐藏失败：{fail_count} 个")if fail_ids:print(f"\n❌ 隐藏失败的{target_color}色Alpha列表（建议稍后重试）：")for fail_id, fail_name, fail_time in fail_ids:print(f"     - ID：{fail_id}，名称：{fail_name}，创建时间：{fail_time}")print("=" * 70)# -------------------------- 程序入口 --------------------------if __name__ == "__main__":try:# 使用配置中的颜色和时间参数batch_hide_alphas_by_color(target_color=TARGET_COLOR,start_date=START_DATE,end_date=END_DATE)except Exception as e:print(f"\n❌ 程序异常终止：{str(e)}")

---

## 讨论与评论 (13)

### 评论 #1 (作者: CM48632, 时间: 8个月前)

工具太实用啦，必须点赞

---

### 评论 #2 (作者: MY41727, 时间: 8个月前)

若把一阶段的alpha都隐藏了，会影响到二阶段获取吗

---

### 评论 #3 (作者: SZ20589, 时间: 8个月前)

感谢大佬分享，大佬提供了一种思路，可以用代码实现批量隐藏alpha，只针对color的设置，如果需要用其他的隐藏条件，需要再修改。alpha被隐藏的话，怎么样把它再找回来呢？如果一个alpha被隐藏了，下次再运行模板怎么样避免重复相同的因子回测呢？=====================================================================================Genius is one percent inspiration and ninety-nine percent perspiration.===========================================================================================

---

### 评论 #4 (作者: JY20282, 时间: 8个月前)

试用了一下，感觉确实不错，一下就清晰起来了

---

### 评论 #5 (作者: AH18340, 时间: 8个月前)

感谢大佬分享，对于没有使用数据库的顾问确实挺好的思路，但是如果你使用了数据库，我相信筛选alpha不是个问题=============================================================================The best time to plant a tree is 20 years ago. The second-best time is now.=============================================================================

---

### 评论 #6 (作者: JX39934, 时间: 8个月前)

感谢楠姐的分享。通过你这个脚本成功把用户阶段标记的无用因子干掉了，阿里嘎多三Q思密达=============================================================================The only thing permanent is change. What we need to do is to constantly improve ourselves.=============================================================================

---

### 评论 #7 (作者: JW16084, 时间: 8个月前)

工具真好用，一直头痛，刷新因子的的好办法，每次都是设置时间，去卡因子，现在有这工具，可以不用烦恼拉。太赞了，感谢楠姐分享呀

---

### 评论 #8 (作者: CL64349, 时间: 8个月前)

感谢大佬的分享，非常实用的工具。点赞.......................

---

### 评论 #9 (作者: YW45434, 时间: 8个月前)

感谢楠楠老师分享，点赞

---

### 评论 #10 (作者: YW65763, 时间: 8个月前)

感谢楠楠老师分享，楠姐出品，必属精品。

---

### 评论 #11 (作者: ZT46009, 时间: 7个月前)

===============================================================================================================================================================================================================================================非常感谢楠楠大佬的无私分享！这些实用内容真的帮我解决不少问题，再次由衷致谢！===============================================================================================================================================================================================================================================

---

### 评论 #12 (作者: MY49971, 时间: 6个月前)

感谢大佬分享，很有用的功能======================================================================================================Talk is cheap,show me the alpha=================================

---

### 评论 #13 (作者: QM70930, 时间: 6个月前)

感谢，挺有用的

---

