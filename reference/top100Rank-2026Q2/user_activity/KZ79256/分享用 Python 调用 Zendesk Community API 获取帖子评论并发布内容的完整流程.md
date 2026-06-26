# 分享：用 Python 调用 Zendesk Community API 获取帖子、评论并发布内容的完整流程

- **链接**: 分享用 Python 调用 Zendesk Community API 获取帖子评论并发布内容的完整流程.md
- **作者**: KZ79256
- **发布时间/热度**: 1个月前, 得票: 23

## 帖子正文

分享：用 Python 调用 Zendesk Community API 获取帖子、评论并发布内容的完整流程最近我整理了一套用 Python 访问 Zendesk Community 的方法，包括读取论坛 topic 下的帖子、获取帖子详情、批量获取评论、保存数据，以及在有权限的情况下通过 API 发布新帖子。这里把完整流程记录下来，供需要做内容整理、论坛检索或个人知识归档的同学参考。本文只讨论官方 API 和正常登录态下的使用方式。实际能否读取、评论或发帖，取决于当前账号权限、目标 topic 的权限设置，以及 Zendesk Help Center session 是否有效。一、常用 Community API 总览Zendesk Community 常用接口主要包括 topic、post、comment 三类。功能接口获取所有 topicsGET /api/v2/community/topics.json获取指定 topic 信息GET /api/v2/community/topics/{topic_id}.json获取指定 topic 下的帖子GET /api/v2/community/topics/{topic_id}/posts.json获取单个帖子详情GET /api/v2/community/posts/{post_id}.json获取某个帖子的评论GET /api/v2/community/posts/{post_id}/comments.json搜索社区帖子GET /api/v2/help_center/community_posts/search.json获取当前 Help Center sessionGET /api/v2/help_center/sessions.json创建新帖子POST /api/v2/community/posts.json其中，读取内容主要用 GET；发布内容主要用 POST。使用 cookie session 发 POST 请求时，通常还需要从/api/v2/help_center/sessions.json获取 CSRF token。二、建立登录 session首先需要完成 WorldQuant Brain 登录，然后通过 support authentication 链路进入 Zendesk Help Center。示例代码如下：import os
import httpx

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

for key in ["http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]:
    os.environ.pop(key, None)

os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12"

auth = (username, password)

client = httpx.Client(
    follow_redirects=False,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
)

r = client.post("https://api.worldquantbrain.com/authentication", auth=auth)
print("login:", r.status_code, r.url)

r = client.get(
    "https://api.worldquantbrain.com/authentication/support"
    "?return_to=https%3A%2F%2Fsupport.worldquantbrain.com%2Fhc%2Fen-us%2Fcommunity%2Ftopics"
)

print("support redirect:", r.status_code, r.headers.get("location"))

while r.status_code in (301, 302, 303, 307, 308):
    location = r.headers.get("location")
    if not location:
        break
    r = client.get(location)
    print("redirect:", r.status_code, r.url, r.headers.get("location"))

print(r.status_code)
print(r.text[:1000])如果最后返回真实论坛页面，说明 session 可能已经建立成功。如果返回Just a moment...、challenges.cloudflare.com或Enable JavaScript and cookies to continue，说明请求被 Cloudflare challenge 拦截，当前不是目标内容。三、获取 topic 下的帖子列表假设已经知道 topic id，可以直接获取该 topic 下的帖子。TOPIC_ID = 32983704970903

r = client.get(
    f"https://support.worldquantbrain.com/api/v2/community/topics/{TOPIC_ID}/posts.json",
    params={
        "page[size]": 10,
        "sort_by": "recent_activity"
    }
)

print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print(r.text[:2000])如果请求成功，返回 JSON 中通常包含posts字段。每个 post 里会包含帖子 id、标题、正文、作者、创建时间、更新时间、评论数、投票数等信息。可以这样提取基础字段：data = r.json()
posts = data.get("posts", [])

for post in posts:
    print("=" * 80)
    print("id:", post.get("id"))
    print("title:", post.get("title"))
    print("html_url:", post.get("html_url"))
    print("created_at:", post.get("created_at"))
    print("updated_at:", post.get("updated_at"))
    print("comment_count:", post.get("comment_count"))
    print("vote_sum:", post.get("vote_sum"))四、处理分页：获取 topic 下所有帖子Zendesk API 可能会分页返回结果。如果帖子很多，不能只请求第一页，需要检查meta.has_more和links.next。def fetch_all_topic_posts(client, topic_id, page_size=100):
    url = f"https://support.worldquantbrain.com/api/v2/community/topics/{topic_id}/posts.json"
    params = {
        "page[size]": page_size,
        "sort_by": "recent_activity"
    }

    all_posts = []

    while url:
        r = client.get(url, params=params)
        print("GET:", r.status_code, r.url)

        head = r.text[:500]

        if "Just a moment" in head or "challenges.cloudflare.com" in head:
            raise RuntimeError("请求被 Cloudflare challenge 拦截。")

        if "<html" in head.lower():
            raise RuntimeError("返回了 HTML 页面，可能未登录或被跳转到 access 页面。")

        r.raise_for_status()
        data = r.json()

        posts = data.get("posts", [])
        all_posts.extend(posts)

        meta = data.get("meta") or {}
        links = data.get("links") or {}

        if meta.get("has_more"):
            url = links.get("next")
            params = None
        else:
            url = None

    return all_posts


posts = fetch_all_topic_posts(client, TOPIC_ID)
print("total posts:", len(posts))五、获取单个帖子详情如果已经知道 post id，可以读取单个帖子详情。POST_ID = 40373405530647

r = client.get(
    f"https://support.worldquantbrain.com/api/v2/community/posts/{POST_ID}.json"
)

print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print(r.text[:2000])

data = r.json()
post = data.get("post", {})

print("title:", post.get("title"))
print("details:", post.get("details"))
print("html_url:", post.get("html_url"))注意：details字段通常是 HTML。如果想转成纯文本，可以用 BeautifulSoup。from bs4 import BeautifulSoup

html = post.get("details") or ""
text = BeautifulSoup(html, "html.parser").get_text("\\n", strip=True)

print(text)六、获取某个帖子的评论评论接口是：GET /api/v2/community/posts/{post_id}/comments.json示例：POST_ID = 40373405530647

r = client.get(
    f"https://support.worldquantbrain.com/api/v2/community/posts/{POST_ID}/comments.json",
    params={
        "page[size]": 100,
        "include": "users"
    }
)

print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print(r.text[:2000])如果成功，返回 JSON 通常包含comments字段。可以这样解析：data = r.json()
comments = data.get("comments", [])
users = data.get("users", [])

user_map = {u.get("id"): u for u in users}

for c in comments:
    author = user_map.get(c.get("author_id"), {})
    print("=" * 80)
    print("comment id:", c.get("id"))
    print("author:", author.get("name") or c.get("author_id"))
    print("created_at:", c.get("created_at"))
    print("updated_at:", c.get("updated_at"))
    print("body:", c.get("body"))评论正文通常也可能是 HTML，可以继续用 BeautifulSoup 转为纯文本。from bs4 import BeautifulSoup

for c in comments:
    html = c.get("body") or ""
    text = BeautifulSoup(html, "html.parser").get_text("\\n", strip=True)
    print(text)七、分页获取某个帖子的所有评论如果一个帖子评论很多，也需要分页。def fetch_all_post_comments(client, post_id, page_size=100):
    url = f"https://support.worldquantbrain.com/api/v2/community/posts/{post_id}/comments.json"
    params = {
        "page[size]": page_size,
        "include": "users"
    }

    all_comments = []
    all_users = {}

    while url:
        r = client.get(url, params=params)
        print("GET:", r.status_code, r.url)

        head = r.text[:500]

        if "Just a moment" in head or "challenges.cloudflare.com" in head:
            raise RuntimeError("请求被 Cloudflare challenge 拦截。")

        if "<html" in head.lower():
            raise RuntimeError("返回了 HTML 页面，可能未登录或被跳转到 access 页面。")

        r.raise_for_status()
        data = r.json()

        for u in data.get("users", []):
            all_users[u.get("id")] = u

        all_comments.extend(data.get("comments", []))

        meta = data.get("meta") or {}
        links = data.get("links") or {}

        if meta.get("has_more"):
            url = links.get("next")
            params = None
        else:
            url = None

    return all_comments, all_users


comments, users = fetch_all_post_comments(client, POST_ID)
print("total comments:", len(comments))八、批量获取某个 topic 下所有帖子和评论如果想把一个 topic 下的所有帖子和评论都保存下来，可以先获取所有帖子，再逐个获取评论。from bs4 import BeautifulSoup

def html_to_text(html):
    return BeautifulSoup(html or "", "html.parser").get_text("\\n", strip=True)


def collect_topic_posts_with_comments(client, topic_id):
    posts = fetch_all_topic_posts(client, topic_id)

    result = []

    for index, post in enumerate(posts, start=1):
        post_id = post.get("id")
        print(f"[{index}/{len(posts)}] fetching comments for post:", post_id)

        comments, users = fetch_all_post_comments(client, post_id)

        user_map = {uid: user for uid, user in users.items()}

        item = {
            "post_id": post_id,
            "title": post.get("title"),
            "html_url": post.get("html_url"),
            "created_at": post.get("created_at"),
            "updated_at": post.get("updated_at"),
            "vote_sum": post.get("vote_sum"),
            "comment_count": post.get("comment_count"),
            "details_html": post.get("details"),
            "details_text": html_to_text(post.get("details")),
            "comments": []
        }

        for c in comments:
            author = user_map.get(c.get("author_id"), {})
            item["comments"].append({
                "comment_id": c.get("id"),
                "author_id": c.get("author_id"),
                "author_name": author.get("name"),
                "created_at": c.get("created_at"),
                "updated_at": c.get("updated_at"),
                "body_html": c.get("body"),
                "body_text": html_to_text(c.get("body")),
            })

        result.append(item)

    return result


dataset = collect_topic_posts_with_comments(client, TOPIC_ID)
print("posts collected:", len(dataset))九、保存为 JSONJSON 适合保留完整结构，包括每个帖子下面的评论列表。import json

with open("zendesk_topic_posts_with_comments.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("saved to zendesk_topic_posts_with_comments.json")十、保存为 CSVCSV 更适合用 Excel 或 pandas 查看。可以把每一条评论展开成一行。如果某个帖子没有评论，也保留一行帖子信息。import csv

with open("zendesk_topic_posts_with_comments.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "post_id",
            "title",
            "html_url",
            "post_created_at",
            "post_updated_at",
            "vote_sum",
            "comment_count",
            "post_text",
            "comment_id",
            "comment_author_name",
            "comment_created_at",
            "comment_updated_at",
            "comment_text",
        ]
    )

    writer.writeheader()

    for post in dataset:
        comments = post.get("comments") or []

        if not comments:
            writer.writerow({
                "post_id": post.get("post_id"),
                "title": post.get("title"),
                "html_url": post.get("html_url"),
                "post_created_at": post.get("created_at"),
                "post_updated_at": post.get("updated_at"),
                "vote_sum": post.get("vote_sum"),
                "comment_count": post.get("comment_count"),
                "post_text": post.get("details_text"),
                "comment_id": "",
                "comment_author_name": "",
                "comment_created_at": "",
                "comment_updated_at": "",
                "comment_text": "",
            })
        else:
            for c in comments:
                writer.writerow({
                    "post_id": post.get("post_id"),
                    "title": post.get("title"),
                    "html_url": post.get("html_url"),
                    "post_created_at": post.get("created_at"),
                    "post_updated_at": post.get("updated_at"),
                    "vote_sum": post.get("vote_sum"),
                    "comment_count": post.get("comment_count"),
                    "post_text": post.get("details_text"),
                    "comment_id": c.get("comment_id"),
                    "comment_author_name": c.get("author_name"),
                    "comment_created_at": c.get("created_at"),
                    "comment_updated_at": c.get("updated_at"),
                    "comment_text": c.get("body_text"),
                })

print("saved to zendesk_topic_posts_with_comments.csv")十一、搜索社区帖子除了遍历 topic，也可以直接用搜索接口查关键词。例如搜索某个 topic 内包含 alpha 的帖子：r = client.get(
    "https://support.worldquantbrain.com/api/v2/help_center/community_posts/search.json",
    params={
        "query": "alpha",
        "topic": TOPIC_ID,
    }
)

print(r.status_code)
print(r.headers.get("content-type"))
print(r.text[:2000])这个方式适合查找某个关键词相关的历史讨论，比如 alpha 表达式、operator、simulation、submission、decay、neutralization 等。十二、发布新帖子发帖前建议先获取 CSRF token。session_r = client.get("https://support.worldquantbrain.com/api/v2/help_center/sessions.json")

print(session_r.status_code)
print(session_r.headers.get("content-type"))
print(session_r.text[:1000])

session_r.raise_for_status()
csrf = session_r.json()["current_session"]["csrf_token"]然后构造请求头和 payload。headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-CSRF-Token": csrf,
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"https://support.worldquantbrain.com/hc/en-us/community/topics/{TOPIC_ID}",
    "Origin": "https://support.worldquantbrain.com",
}

payload = {
    "post": {
        "title": "测试发帖：API 连通性检查",
        "details": "<p>这是通过 Zendesk Community API 发布的测试内容。</p>",
        "topic_id": TOPIC_ID,
    },
    "notify_subscribers": False,
}

r = client.post(
    "https://support.worldquantbrain.com/api/v2/community/posts.json",
    json=payload,
    headers=headers,
)

print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print(r.text[:2000])成功时一般返回201 Created，响应里会包含新帖子的id和html_url。十三、回复帖子评论如果账号有评论权限，也可以通过 API 给帖子添加评论。评论接口通常是：POST /api/v2/community/posts/{post_id}/comments.json示例：POST_ID = 40373405530647

payload = {
    "comment": {
        "body": "<p>这是通过 API 发布的一条测试评论。</p>"
    }
}

r = client.post(
    f"https://support.worldquantbrain.com/api/v2/community/posts/{POST_ID}/comments.json",
    json=payload,
    headers=headers,
)

print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print(r.text[:2000])如果返回201，说明评论发布成功。如果返回403，通常表示当前账号没有评论权限、CSRF/session 不完整，或者目标帖子不允许评论。十四、常见状态码含义状态码常见含义200GET 请求成功，正常返回数据。201POST 创建成功，例如成功发帖或成功评论。401未认证，当前请求没有有效登录态。403已被拒绝，常见原因是账号无权限、CSRF 缺失、session 不完整或 topic/post 不允许操作。404资源不存在，或者当前账号无权看到该资源。422请求格式不合法，例如 title 为空、details 不合法、topic_id 不可用。429请求过快，触发 rate limit，需要降低频率。十五、排查 403 的建议遇到403 Forbidden时，不要只看状态码，建议把响应内容也打印出来。print("status:", r.status_code)
print("final url:", r.url)
print("content-type:", r.headers.get("content-type"))
print("headers:", dict(r.headers))
print("body head:", r.text[:2000])可以按下面几种情况判断：如果返回 JSON，并明确写着 forbidden 或 not allowed，大概率是账号或 topic 权限不足。如果返回 HTML，并且是 access/login 页面，说明 support session 没有建立成功。如果返回Just a moment...或challenges.cloudflare.com，说明请求被 Cloudflare challenge 拦截。如果 GET 能成功但 POST 失败，优先检查 CSRF token、Origin、Referer 和账号发帖权限。如果同一个账号在浏览器里也看不到发帖或评论入口，那么 API 通常也不会允许发帖或评论。十六、推荐的完整封装下面是一个更完整的工具类写法，适合后续复用。import json
import csv
from bs4 import BeautifulSoup


class ZendeskCommunityClient:
    def __init__(self, client, base_url="https://support.worldquantbrain.com"):
        self.client = client
        self.base_url = base_url.rstrip("/")

    def _check_response(self, r):
        head = r.text[:500]

        if "Just a moment" in head or "challenges.cloudflare.com" in head:
            raise RuntimeError("请求被 Cloudflare challenge 拦截。")

        if "<html" in head.lower():
            raise RuntimeError("返回了 HTML 页面，可能未登录或被跳转到 access 页面。")

        r.raise_for_status()
        return r

    def html_to_text(self, html):
        return BeautifulSoup(html or "", "html.parser").get_text("\\n", strip=True)

    def get_csrf_token(self):
        r = self.client.get(f"{self.base_url}/api/v2/help_center/sessions.json")
        self._check_response(r)
        return r.json()["current_session"]["csrf_token"]

    def get_topic_posts(self, topic_id, page_size=100):
        url = f"{self.base_url}/api/v2/community/topics/{topic_id}/posts.json"
        params = {
            "page[size]": page_size,
            "sort_by": "recent_activity"
        }

        all_posts = []

        while url:
            r = self.client.get(url, params=params)
            self._check_response(r)

            data = r.json()
            all_posts.extend(data.get("posts", []))

            meta = data.get("meta") or {}
            links = data.get("links") or {}

            if meta.get("has_more"):
                url = links.get("next")
                params = None
            else:
                url = None

        return all_posts

    def get_post_comments(self, post_id, page_size=100):
        url = f"{self.base_url}/api/v2/community/posts/{post_id}/comments.json"
        params = {
            "page[size]": page_size,
            "include": "users"
        }

        all_comments = []
        users = {}

        while url:
            r = self.client.get(url, params=params)
            self._check_response(r)

            data = r.json()

            all_comments.extend(data.get("comments", []))

            for user in data.get("users", []):
                users[user.get("id")] = user

            meta = data.get("meta") or {}
            links = data.get("links") or {}

            if meta.get("has_more"):
                url = links.get("next")
                params = None
            else:
                url = None

        return all_comments, users

    def collect_topic(self, topic_id):
        posts = self.get_topic_posts(topic_id)
        result = []

        for i, post in enumerate(posts, start=1):
            post_id = post.get("id")
            print(f"[{i}/{len(posts)}] post_id={post_id}")

            comments, users = self.get_post_comments(post_id)

            result.append({
                "post_id": post_id,
                "title": post.get("title"),
                "html_url": post.get("html_url"),
                "created_at": post.get("created_at"),
                "updated_at": post.get("updated_at"),
                "vote_sum": post.get("vote_sum"),
                "comment_count": post.get("comment_count"),
                "details_html": post.get("details"),
                "details_text": self.html_to_text(post.get("details")),
                "comments": [
                    {
                        "comment_id": c.get("id"),
                        "author_id": c.get("author_id"),
                        "author_name": (users.get(c.get("author_id")) or {}).get("name"),
                        "created_at": c.get("created_at"),
                        "updated_at": c.get("updated_at"),
                        "body_html": c.get("body"),
                        "body_text": self.html_to_text(c.get("body")),
                    }
                    for c in comments
                ],
            })

        return result

    def create_post(self, topic_id, title, html_details, notify_subscribers=False):
        csrf = self.get_csrf_token()

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"{self.base_url}/hc/en-us/community/topics/{topic_id}",
            "Origin": self.base_url,
        }

        payload = {
            "post": {
                "title": title,
                "details": html_details,
                "topic_id": int(topic_id),
            },
            "notify_subscribers": notify_subscribers,
        }

        r = self.client.post(
            f"{self.base_url}/api/v2/community/posts.json",
            json=payload,
            headers=headers,
        )

        self._check_response(r)
        return r.json().get("post")

    def create_comment(self, post_id, html_body):
        csrf = self.get_csrf_token()

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.base_url,
        }

        payload = {
            "comment": {
                "body": html_body
            }
        }

        r = self.client.post(
            f"{self.base_url}/api/v2/community/posts/{post_id}/comments.json",
            json=payload,
            headers=headers,
        )

        self._check_response(r)
        return r.json().get("comment")


zc = ZendeskCommunityClient(client)

dataset = zc.collect_topic(32983704970903)

with open("topic_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)十七、使用建议只保存自己有权限访问的内容。不要公开用户名、密码、cookie、CSRF token 或 session 信息。批量获取时建议降低请求频率，不要对论坛造成压力。如果需要长期归档，建议保存 JSON，因为 JSON 能保留帖子与评论的层级关系。如果需要人工分析，建议额外导出 CSV，方便用 Excel、pandas 或数据库处理。发帖或评论前，建议先用一条简短测试内容确认权限。整体来说，读取论坛内容的核心是 topic、post、comment 三层结构；发帖和评论的核心是有效登录态、CSRF token 和目标板块权限。只要这三点满足，使用官方 API 对论坛内容进行整理和发布会比较直接。

---

## 讨论与评论 (1)

### 评论 #1 (作者: JX14975, 时间: 25天前)

感谢分享这套完善的 Zendesk API 流程！想请教一下，和之前基于 cnhkmcp 的 Playwright 方案相比，直接调用 Zendesk Community API 在绕过 Cloudflare、session 稳定性以及其它方面上具体有哪些优势？

---

