# 【Pyramid时间窗口可视化APP，助你VF1.0！】WEB_UI一键启动！即刻显化三个月内的Pyramid分布代码优化

- **链接**: [Commented] 【Pyramid时间窗口可视化APP助你VF10】WEB_UI一键启动即刻显化三个月内的Pyramid分布代码优化.md
- **作者**: LH44620
- **发布时间/热度**: 5个月前, 得票: 21

## 帖子正文

**【BUG修正：之前单个alpha多pyramid时只计算一次，更新后的代码修改了这个bug，与平台统计口径保持一致。**

**新特征：增加了时间窗口内，已提交的SA分区数量统计】**

**一、简介**

**Pyramid是因子多样化的可视化表现，因子的多样化则是World Quant平台一个十分重要的指标。直接影响你的因子组合性能的好坏与其稳定性。**

当前，平台只能显示一个赛季季度内的Pyramid分布。可是，VF是滑动的三个月。故而，对于掌握在每个VF窗口期内的因子分布来说十分不便。

于是，在此痛点上，开发了这款具有web_ui可视化界面的Pyramid分布APP。助力你精准把握每个时间窗口内的投资组合！（Pyramid分布）

**二、代码&使用说明**

**【代码已更新】**

```
import streamlit as stimport pandas as pdimport requestsimport jsonimport osimport timefrom datetime import datetime, timedelta# === 新增：加密库 ===try:    from cryptography.fernet import Fernetexcept ImportError:    st.error("缺少依赖库！请运行: pip install cryptography")    st.stop()# ==========================================# 1. 基础配置与缓存管理# ==========================================CACHE_FILE = "alpha_cache.json"CREDENTIALS_FILE = "credentials.json"KEY_FILE = "secret.key"# --- 密钥与凭证管理模块 ---def load_key():    """加载或生成加密密钥"""    if not os.path.exists(KEY_FILE):        key = Fernet.generate_key()        with open(KEY_FILE, "wb") as key_file:            key_file.write(key)    else:        with open(KEY_FILE, "rb") as key_file:            key = key_file.read()    return keydef save_credentials_encrypted(email, password):    """加密保存凭证"""    key = load_key()    cipher_suite = Fernet(key)       data = {"email": email, "password": password}    json_data = json.dumps(data).encode('utf-8')    encrypted_data = cipher_suite.encrypt(json_data)       with open(CREDENTIALS_FILE, "wb") as f:        f.write(encrypted_data)def load_credentials_encrypted():    """解密读取凭证"""    if not os.path.exists(CREDENTIALS_FILE) or not os.path.exists(KEY_FILE):        return None, None           try:        key = load_key()        cipher_suite = Fernet(key)               with open(CREDENTIALS_FILE, "rb") as f:            encrypted_data = f.read()                   decrypted_data = cipher_suite.decrypt(encrypted_data)        data = json.loads(decrypted_data.decode('utf-8'))        return data.get("email"), data.get("password")    except Exception as e:        # 如果解密失败（比如key文件丢失），返回空让用户重新输入        return None, Nonedef clear_credentials():    """清除本地凭证"""    if os.path.exists(CREDENTIALS_FILE):        os.remove(CREDENTIALS_FILE)    st.toast("已清除本地保存的密码", icon="🗑️")# --- 数据缓存模块 ---def load_cache():    if os.path.exists(CACHE_FILE):        try:            with open(CACHE_FILE, 'r', encoding='utf-8') as f:                return json.load(f)        except Exception:            return []    return []def save_cache(data):    try:        with open(CACHE_FILE, 'w', encoding='utf-8') as f:            json.dump(data, f)    except Exception as e:        st.error(f"缓存保存失败: {e}")# ==========================================# 2. 核心逻辑：登录与数据获取# ==========================================def login(email, password):    try:        s = requests.Session()        s.auth = (email, password)        response = s.post('https://api.worldquantbrain.com/authentication')        if response.status_code in [200, 201]:            return s        else:            return None    except Exception as e:        st.error(f"连接异常: {str(e)}")        return Nonedef fetch_submitted_alphas(session, start_date, end_date, max_offset=9900):    alpha_list = []    offset = 0    status_text = st.empty()    progress_bar = st.progress(0)    while True:        url = (            f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={offset}"            "&status!=UNSUBMITTED%1FIS_FAIL"            f"&dateSubmitted%3E={start_date}T00:00:00-04:00"            f"&dateSubmitted%3C={end_date}T00:00:00-04:00"            "&order=-is.sharpe&hidden=false"        )        try:            status_text.text(f"Fetching data... Offset: {offset}")            response = session.get(url)                       if response.status_code != 200:                status_text.error(f"API Error: {response.status_code}")                break                           response_data = response.json()            total_count = response_data.get("count", 0)                       if total_count > 0:                progress = min(offset / total_count, 1.0)                progress_bar.progress(progress)            if "results" in response_data:                alpha_list.extend(response_data["results"])            offset += 100            if offset >= total_count or offset > max_offset:                progress_bar.progress(1.0)                status_text.success(f"Done! Fetched {len(alpha_list)} alphas.")                time.sleep(1)                status_text.empty()                progress_bar.empty()                break            time.sleep(0.3)        except Exception as e:            status_text.error(f"Fetch Error: {str(e)}")            time.sleep(3)            break    return alpha_list# ==========================================# 3. 数据处理 (核心修复部分)# ==========================================def parse_pyramid_structure(pyramid_name):    try:        parts = pyramid_name.split('/')        if len(parts) >= 3:            return parts[0], parts[2]        elif len(parts) == 1:            return "UNKNOWN", parts[0]        else:            return "UNKNOWN", "UNKNOWN"    except:        return "ERROR", "ERROR"def get_pyramid_distribution(alpha_records, view_start_date, view_end_date):    """    修复版：    1. 支持单个 Alpha 属于多个 Pyramid 的情况 (Loop append)    2. 支持 Super Alpha (SA) 的统计    3. 过滤解析错误的 Pyramid    """    data_points = []       start_dt = pd.to_datetime(view_start_date)    end_dt = pd.to_datetime(view_end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)    for alpha in alpha_records:        # 1. 时间过滤        date_str = alpha.get("dateSubmitted")        if not date_str: continue        try:            alpha_date = pd.to_datetime(date_str)            if alpha_date.tzinfo is not None:                alpha_date = alpha_date.tz_localize(None)            if not (start_dt <= alpha_date <= end_dt):                continue        except: continue        # 2. 提取 Pyramid 信息        is_metrics = alpha.get("is", {})        checks = is_metrics.get("checks", [])        pyramid_check = next((item for item in checks if item.get("name") == "MATCHES_PYRAMID"), None)               found_any_pyramid = False        if pyramid_check and "pyramids" in pyramid_check:            # 遍历所有 pyramids，修复“只统计一个”的问题            for p in pyramid_check["pyramids"]:                p_name = p.get("name", "")                region, category = parse_pyramid_structure(p_name)                               # 过滤掉 ERROR 或 UNKNOWN，确保数据干净                if region != "ERROR" and category != "ERROR":                    data_points.append({"Category": category, "Region": region, "Count": 1})                    found_any_pyramid = True               # 3. 如果没有找到任何 Pyramid (说明是 Super Alpha 或其他)，尝试用 settings.region 归类为 SA        if not found_any_pyramid:            r = alpha.get("settings", {}).get("region")            if r:                data_points.append({"Category": "SA", "Region": r, "Count": 1})    if not data_points: return pd.DataFrame()    df = pd.DataFrame(data_points)    pivot_df = df.pivot_table(index="Category", columns="Region", values="Count", aggfunc="count", fill_value=0)       # === 优化：将 SA 行移到底部 ===    rows = list(pivot_df.index)    if "SA" in rows:        rows.remove("SA")     # 先移除        rows.sort()           # 其他类别按字母排序        rows.append("SA")     # 再把 SA 加到最后        pivot_df = pivot_df.reindex(rows) # 重建索引    return pivot_df# ==========================================# 4. Streamlit UI 主程序# ==========================================st.set_page_config(page_title="Pyramid Alpha Dashboard", layout="wide")st.markdown("""<style>    .stApp { background-color: #0e1117; color: white; }    div.stButton > button { background-color: #262730; color: white; border: 1px solid #4e535e; }    div.stButton > button:hover { border-color: #0078d7; color: #0078d7; }</style>""", unsafe_allow_html=True)st.title("Pyramid Alpha Distribution Dashboard")# --- 初始化状态 ---if 'alpha_data' not in st.session_state:    cached_data = load_cache()    if cached_data:        st.session_state['alpha_data'] = cached_data        st.toast(f"Local cache loaded: {len(cached_data)} records", icon="📂")    else:        st.session_state['alpha_data'] = []if 'view_start' not in st.session_state:    today = datetime.now().date()    st.session_state.view_start = (today.replace(day=1) - pd.DateOffset(months=2)).date()if 'view_end' not in st.session_state:    st.session_state.view_end = datetime.now().date()# --- 侧边栏：API 设置 ---st.sidebar.header("1. WQBrain Data Fetch")# 尝试自动加载凭证saved_email, saved_password = load_credentials_encrypted()with st.sidebar.form("login_form"):    st.caption("Enter your WQBrain credentials to fetch new data.")       # 如果有保存的密码，自动填入 default_value    email_val = saved_email if saved_email else ""    pass_val = saved_password if saved_password else ""       email = st.text_input("Email", value=email_val)    password = st.text_input("Password", value=pass_val, type="password")       # 记住密码复选框 (如果有保存的，默认勾选)    remember = st.checkbox("Remember Me (Encrypted Locally)", value=(True if saved_email else False))       st.markdown("---")       default_start = datetime(2024, 1, 1).date()    default_end = datetime.now().date() + timedelta(days=1)       fetch_start = st.date_input("Fetch Start (API)", value=default_start)    fetch_end = st.date_input("Fetch End (API)", value=default_end)       submitted = st.form_submit_button("Login & Fetch Alphas")# 如果用户想清除密码if saved_email:    if st.sidebar.button("Forget Password"):        clear_credentials()        st.rerun()if submitted:    if not email or not password:        st.sidebar.error("Please enter both email and password.")    else:        with st.spinner("Logging in..."):            sess = login(email, password)            if sess:                st.sidebar.success("Login Successful!")                               # === 核心修改：处理密码保存 ===                if remember:                    save_credentials_encrypted(email, password)                else:                    clear_credentials() # 如果用户取消勾选，则删除旧凭证                               # 开始抓取                alphas = fetch_submitted_alphas(sess, str(fetch_start), str(fetch_end))                               if alphas:                    st.session_state['alpha_data'] = alphas                    save_cache(alphas)                    st.success(f"Fetched and saved {len(alphas)} alphas.")                    time.sleep(1)                    st.rerun()                else:                    st.warning("No alphas found in this date range.")            else:                st.sidebar.error("Login failed. Check your credentials.")# --- 主界面：可视化 ---if st.session_state['alpha_data']:    total = len(st.session_state['alpha_data'])    st.write(f"💾 **Data Source:** {total} records loaded.")    st.markdown("---")       st.subheader("2. Visualization Window")    c1, c2, c3, c4 = st.columns([1, 1, 3, 1])       if c1.button("◀ Prev Month"):        st.session_state.view_start = (pd.to_datetime(st.session_state.view_start) - pd.DateOffset(months=1)).date()        st.session_state.view_end = (pd.to_datetime(st.session_state.view_end) - pd.DateOffset(months=1)).date()        st.rerun()    if c2.button("Next Month ▶"):        st.session_state.view_start = (pd.to_datetime(st.session_state.view_start) + pd.DateOffset(months=1)).date()        st.session_state.view_end = (pd.to_datetime(st.session_state.view_end) + pd.DateOffset(months=1)).date()        st.rerun()    if c4.button("Reset to Last 3M"):        today = datetime.now().date()        st.session_state.view_end = today        start_of_current_month = today.replace(day=1)        st.session_state.view_start = (start_of_current_month - pd.DateOffset(months=2)).date()        st.rerun()    with c3:        col_d1, col_d2 = st.columns(2)        new_s = col_d1.date_input("Start", value=st.session_state.view_start, label_visibility="collapsed")        new_e = col_d2.date_input("End", value=st.session_state.view_end, label_visibility="collapsed")               if new_s != st.session_state.view_start or new_e != st.session_state.view_end:            st.session_state.view_start = new_s            st.session_state.view_end = new_e            st.rerun()    st.caption(f"Viewing Window: **{st.session_state.view_start}** to **{st.session_state.view_end}**")    # 计算分布    df_result = get_pyramid_distribution(        st.session_state['alpha_data'],        st.session_state.view_start,        st.session_state.view_end    )       if not df_result.empty:        desired_order = ['USA', 'GLB', 'EUR', 'ASI', 'CHN', 'KOR', 'TWN', 'HKG', 'JPN', 'AMR', 'IND']        existing_cols = [c for c in desired_order if c in df_result.columns]        remaining_cols = [c for c in df_result.columns if c not in desired_order]        df_result = df_result[existing_cols + remaining_cols]        styled_df = df_result.style.background_gradient(            cmap='Greens', axis=None        ).format(            lambda x: f"{x:.0f}" if x > 0 else ""        )        st.subheader("Pyramid Heatmap (with SA)")               col_l, col_c, col_r = st.columns([1, 8, 1])        with col_c:            st.dataframe(                styled_df,                use_container_width=True,                height=600            )               # 显示统计信息        sa_count = df_result.loc["SA"].sum() if "SA" in df_result.index else 0        st.info(f"Total Counts: {df_result.sum().sum()} | Included SA: {int(sa_count)}")    else:        st.warning("No alphas found in the selected viewing window.")else:    st.info("👈 Please login on the sidebar to fetch your alpha data.")
```

### 🛠️ 安装与运行

**1. 环境准备**  需要安装 Python 以及以下依赖库：

Bash

```
pip install streamlit pandas requests cryptography

```

**2. 运行 App**  将附件代码保存为  `app.py` ，在终端运行：

Bash

```
streamlit run app.py

```

### 📖 用户界面使用说明 (WebUI Guide)

进入网页后，界面分为左侧的  **“设置区”**  和右侧的  **“可视化区”** 。

![图片](images/img_95fb3b15fc.png)

#### 1. 左侧侧边栏：数据获取与登录

这里是数据的入口，负责从 WQBrain 服务器拉取数据到本地。

- **Credentials (凭证)** ：
  - 输入你的 Email 和 Password。
  - **Remember Me** ：勾选后，密码会被加密保存到本地的  `credentials.json`  文件中。下次打开 App 会自动填充，无需再次输入。
  - *注：如果想清除保存的密码，只需取消勾选或点击出现的 "Forget Password" 按钮。*
- **Fetch Date Range (API 抓取范围)** ：
  - 这是向服务器请求数据的范围。
  - **建议** ： `Start`  设为今年年初（如 2024/01/01）， `End`  设为明天（因为 API 默认不包含结束当天）。
  - 点击  **"Login & Fetch Alphas"**  按钮开始抓取。完成后数据会自动存入本地缓存。

#### 2. 右侧主界面：可视化分析

当数据加载完成后（无论是从 API 新抓取的，还是从本地缓存读取的），右侧会显示分析面板。

- **数据源状态** ：
  - 顶部会显示  `💾 Data Source: X records loaded` ，让你知道当前分析的是基于多少条 Alpha 数据。
- **可视化时间窗口 (Visualization Window)** ：
  - 这是本工具的精髓。你可以在不重新请求 API 的情况下，随意调整查看的时间段。
  - **◀ Prev Month / Next Month ▶** ：按月向前或向后滑动窗口（开始月和结束月会同时+1或者-1），方便复盘历史分布演变。
  - **Reset to Last 3M** ：一键将窗口重置为  **“最近 3 个月”** （从当前月倒推的完整 3 个月周期），这是最常用的复盘VF的窗口。
  - **Start / End 日期选择器** ：你也可以手动微调具体的日期。
- **Pyramid Heatmap (热力图)** ：
  - 表格已做居中处理，适配宽屏显示。
  - **颜色含义** ：颜色越深，代表该 Pyramid 下的 Alpha 数量越多。空白格代表数量为 0。
  - 底部会显示当前视图内的 Alpha 总数统计。

### 🔒 关于安全性

本工具生成的  `credentials.json`  文件使用了  `Fernet`  对称加密算法。即使该文件被他人获取，在没有  `secret.key` （首次运行自动生成）的情况下也无法解密出你的密码，请放心使用。

---

## 讨论与评论 (15)

### 评论 #1 (作者: RL71875, 时间: 6个月前)

感谢大佬分享

---

### 评论 #2 (作者: LG87838, 时间: 6个月前)

距离图形化/0代码编程的时间窗口越来越近了。

感谢大佬的分享。

------------------------------------------------------------------------------------------------------------------------------------

慢慢来，相信时间的力量

------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #3 (作者: KK88739, 时间: 6个月前)

似乎有bug哦，显示的图标不正确

---

### 评论 #4 (作者: YQ84572, 时间: 6个月前)

很好用的工具，可以可视化的查看自己的alpha分布，和mcp中的vf预测器有点像
====================================================================================
祝大佬base多多，vf高高，分享更多工具
====================================================================================

---

### 评论 #5 (作者: LH44620, 时间: 6个月前)

[KK88739](/hc/en-us/profiles/29207120111639-KK88739) 可以请发一下bug的图吗？

---

### 评论 #6 (作者: HL81191, 时间: 6个月前)

新环境的话还得再  **pip install matplotlib，** 另外我觉得

> ### 🔒 关于安全性
> 本工具生成的  `credentials.json`  文件使用了  `Fernet`  对称加密算法。即使该文件被他人获取，在没有  `secret.key` （首次运行自动生成）的情况下也无法解密出你的密码，请放心使用。

这个东西很好很安全，因为我之前账号认证信息都是明文写在代码里或文件里，想过设置环境变量引用，但是初次在虚拟环境尝试失败就没再尝试了，安全性很差。

---

### 评论 #7 (作者: MZ45384, 时间: 6个月前)

强力工具加一，感谢大佬的可视化分析pyramids代码，效果不错，我找到了EUR和USA的fundamental被封的原因了。

![图片](images/img_47ac2bb998.png)

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

### 评论 #8 (作者: WF37935, 时间: 5个月前)

感谢分享！不过获取指定时间pyramid的话，可以直接把genius接口的起止日期改改就行了。 [https://api.worldquantbrain.com/users/self/activities/pyramid-alphas?startDate={startDate}&endDate={endDate}](https://api.worldquantbrain.com/users/self/activities/pyramid-alphas?startDate={startDate}&endDate={endDate})

---

### 评论 #9 (作者: ML43675, 时间: 5个月前)

感谢大佬分享！！！正好是我需要的工具，强迫症想均匀的点满每一个塔(～￣▽￣)～

---

### 评论 #10 (作者: LX57490, 时间: 5个月前)

### **感谢前辈无私分享，祝愿前辈次次GM，月月VF1.0，weight猛猛涨！！！！**

大佬开发的Pyramid可视化工具，精准命中VF周期管理的痛点需求。

其技术亮点有三：

一、是通过 `cryptography` 实现凭证加密存储；

二、是独创双时间轴设计——API抓取范围与可视化窗口分离，避免重复请求；

三、是核心算法升级，既修复“单因子多金字塔”统计漏洞，又创新识别Super Alpha区域分布。

此工具将分散的Pyramid数据转化为直观战场沙盘，堪称因子组合优化的“战术目镜”！

#### **注：使用win+R调用CMD的同学们，记得cd跳转到你代码位置后再streamlit run app.py！！！！**

---

### 评论 #11 (作者: HW93328, 时间: 5个月前)

============================HW93328============================

很新颖的ui工具，可以可视化的查看自己的alpha分布，针对distrbution的一些问题进行直观的发现，感谢大佬分享！！

============================HW93328============================

---

### 评论 #12 (作者: GC81559, 时间: 4个月前)

终于找到我想要的工具了，超级有帮助

---

### 评论 #13 (作者: LK39823, 时间: 3个月前)

==================================================================================

什么时候大佬能出一个统计自己做过哪些数据集的一个可视化系统？总是搞不清自己做过哪些数据集

===================================================================================

感谢大佬的分享，争取gm

---

### 评论 #14 (作者: DZ31817, 时间: 3个月前)

20260316

------------------------------------------------------------------------------------------

感谢分享，运行成功了。该工具可视化不同vf窗口下的点塔情况，再结合不同vf窗口下的sharpe、fitness等统计，应该能更好地控制自己的vf变化了。

---

### 评论 #15 (作者: WL58980, 时间: 2个月前)

大佬的帖子太有用了，受益匪浅呀！！！感谢！！！

============================================================================

Study hard — quality over quantity, no room for mediocrity. Cherish every learning opportunity, stay focused, and learn from the experts. Keep pushing!

============================================================================

---

