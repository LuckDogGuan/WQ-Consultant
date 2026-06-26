# Python纯代码获取论坛内容(不使用任何无头浏览器等操作)

- **链接**: Python纯代码获取论坛内容不使用任何无头浏览器等操作.md
- **作者**: KZ79256
- **发布时间/热度**: 1个月前, 得票: 2

## 帖子正文

我一直想在python里纯的http请求来获取论坛内容, 但是没得办法.之前不管是mcp还是我自己的都是通过无头浏览器完成的, 有可能不稳定但是现在, 我找到办法了!!!原理是通过代码在WQ上通过账户获得论坛页面的cookie, 之后调用论坛的api接口获得具体如下:获得论坛页面的cookie```pythonimport osimport httpxos.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"for key in ['http_proxy', 'https_proxy', 'all_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY']:os.environ.pop(key, None)os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12'auth = (username, password)client = httpx.Client(follow_redirects=False,timeout=30,headers={"User-Agent": "Mozilla/5.0","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",},)r = client.post("https://api.worldquantbrain.com/authentication", auth=auth)print("login:", r.status_code, r.url)r = client.get("https://api.worldquantbrain.com/authentication/support""?return_to=https%3A%2F%2Fsupport.worldquantbrain.com%2Fhc%2Fen-us%2Fcommunity%2Ftopics")print("support redirect:", r.status_code, r.headers.get("location"))while r.status_code in (301, 302, 303, 307, 308):location = r.headers.get("location")if not location:breakr = client.get(location)print("redirect:", r.status_code, r.url, r.headers.get("location"))print(r.text[:1000])```至此获得了论坛页面的cookie, 但是直接使用cookie访问原本的html界面会被拦住,这里就直接用论坛支撑平台的api获得相应的内容, 详见https://developer.zendesk.com/api-reference/help_center/help-center-api/introduction/比较实用的几个见下# 论坛topic页码: "https://support.worldquantbrain.com/api/v2/community/topics"# 某个topic下的posts:https://support.worldquantbrain.com/api/v2/community/topics/18910956638743/posts# 某个posts的内容:https://worldquantbrain.zendesk.com/api/v2/help_center/community/posts/40373405530647# 某个posts的comments:https://worldquantbrain.zendesk.com/api/v2/community/posts/40373405530647/comments# 列出某用户 posts:https://worldquantbrain.zendesk.com/api/v2/community/users/13609593802263/posts结果如下:自动发帖代码session_r = client.get("https://support.worldquantbrain.com/api/v2/help_center/sessions.json")print(session_r.status_code)print(session_r.headers.get("content-type"))print(session_r.text[:1000])session_r.raise_for_status()csrf = session_r.json()["current_session"]["csrf_token"]headers = {"Accept": "application/json","Content-Type": "application/json","X-CSRF-Token": csrf,"X-Requested-With": "XMLHttpRequest","Referer": ("https://support.worldquantbrain.com/hc/en-us/community/topics/""18910956638743-%E9%A1%BE%E9%97%AE%E4%B8%93%E5%B1%9E%E4%B8%AD%E6%96%87%E8%AE%BA%E5%9D%9B"),"Origin": "https://support.worldquantbrain.com",}payload = {"post": {"title": "这是通过纯代码发帖","details": "<p>这是通过 Zendesk Community API 发布的测试内容。</p>","topic_id": 32983704970903,},"notify_subscribers": False,}r = client.post("https://support.worldquantbrain.com/api/v2/community/posts.json",json=payload,headers=headers,)print(r.status_code)print(r.headers.get("content-type"))print(r.text[:2000])代码发布评论POST_ID = 40373405530647  # 换成目标帖子 idpayload = {"comment": {"body": r"""<p>说得好, 这是来自一个python api调用的测试</p>"""}}r = client.post(f"https://support.worldquantbrain.com/api/v2/community/posts/{POST_ID}/comments.json",json=payload,headers=headers,)print("status:", r.status_code)print("content-type:", r.headers.get("content-type"))print(r.text[:2000])给目标帖子/评论点赞POST_ID = 40373405530647  # 换成目标帖子 idr = client.post(f"https://support.worldquantbrain.com/api/v2/community/posts/{POST_ID}/up",headers=headers,)print("status:", r.status_code)print("content-type:", r.headers.get("content-type"))print(r.text[:2000])

---

## 讨论与评论 (1)

### 评论 #1 (作者: KZ79256, 时间: 1个月前)

更多api操作详见https://developer.zendesk.com/api-reference/help_center/help-center-api/introduction/可以结合AI进行写

---

