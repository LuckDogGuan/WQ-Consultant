# 【代码分享】获取Documentation里的内容 简易版

- **链接**: 【代码分享】获取Documentation里的内容 简易版.md
- **作者**: FD69320
- **发布时间/热度**: 10个月前, 得票: 25

## 帖子正文

简易版代码分享""""""import httpxBRAIN_API_HOST          = 'https://api.worldquantbrain.com'BRAIN_API_AUTH          = '/authentication'BRAIN_API_TUTORIAL      = '/tutorials'BRAIN_API_CONTENT       = '/tutorial-pages/'WQ_USER_NAME            = ''WQ_PASSWORD             = ''def login():"""Create and authenticate a new session with the Brain API.Returns:httpx.Client: Authenticated session object.Raises:httpx.HTTPError: If authentication fails."""session = httpx.Client(timeout=30)try:auth_response = session.post(url=f"{BRAIN_API_HOST}{BRAIN_API_AUTH}",auth=(WQ_USER_NAME, WQ_PASSWORD))auth_response.raise_for_status()auth_token = auth_response.headers.get('Authorization')if auth_token:session.headers.update({'Authorization': auth_token})return sessionexcept httpx.HTTPError as exc:session.close()raise httpx.HTTPError(f"Authentication failed: {exc}") from excdef get_all_tutorials(session: httpx.Client):"""Get all tutorials from the WorldQuant API."""url = f'{BRAIN_API_HOST}{BRAIN_API_TUTORIAL}'response = session.get(url)return response.json()def get_content_by_id(session: httpx.Client, tutorial_id: str):"""Get a tutorial from the WorldQuant API by its ID."""url = f'{BRAIN_API_HOST}{BRAIN_API_CONTENT}{tutorial_id}'response = session.get(url)return response.json()if __name__ == '__main__':session = login()tutorials = get_all_tutorials(session)for tutorial in tutorials['results']:for page in tutorial['pages']:page_content = get_content_by_id(session, page['id'])print(page_content)

---

## 讨论与评论 (0)

