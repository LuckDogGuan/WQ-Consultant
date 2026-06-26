import os
import sys
import json
import asyncio
import re
import importlib.util
from pathlib import Path

# 动态寻找和查找所有可能的 cnhkmcp/untracked 路径，并验证 forum_functions.py 是否存在
possible_untracked_paths = []
spec = importlib.util.find_spec("cnhkmcp")
if spec and spec.submodule_search_locations:
    for loc in spec.submodule_search_locations:
        possible_untracked_paths.append(Path(loc) / "untracked")

possible_untracked_paths.extend([
    Path(r"C:\Program Files\Python312\Lib\site-packages\cnhkmcp\untracked"),
    Path(r"C:\Users\31186\AppData\Roaming\Python\Python312\site-packages\cnhkmcp\untracked")
])

cnhkmcp_untracked = None
for path in possible_untracked_paths:
    if path.exists() and (path / "forum_functions.py").exists():
        cnhkmcp_untracked = str(path)
        break

if cnhkmcp_untracked:
    if cnhkmcp_untracked not in sys.path:
        sys.path.insert(0, cnhkmcp_untracked)
else:
    print("Warning: Could not find untracked directory containing forum_functions.py")


# Now we can import ForumClient
from forum_functions import ForumClient

def load_credentials():
    possible_paths = [
        Path("user_config.json"),
        Path("../user_config.json"),
        Path("../../user_config.json"),
        Path(os.path.expanduser("~")) / ".config" / "AiWorkFlow" / "user_config.json",
        Path("D:/SoftWare/AiWorkFlow/user_config.json")
    ]
    config_file = None
    for p in possible_paths:
        if p.exists():
            config_file = str(p)
            break
    if not config_file:
        config_file = r"D:\SoftWare\AiWorkFlow\user_config.json"

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        credentials = config_data.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if email and password:
            return email, password
    print("Error: Credentials not found in user_config.json.")
    sys.exit(1)

def extract_forum_links(text: str) -> list[str]:
    # 匹配论坛帖子的链接模式
    pattern = r'https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/\d+(?:-[a-zA-Z0-9%-]+)?'
    links = re.findall(pattern, text)
    normalized_links = []
    for link in links:
        # 提取到 id 部分进行去重
        match = re.match(r'(https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/\d+)', link)
        if match:
            normalized_links.append(match.group(1))
    return list(set(normalized_links))

async def fetch_and_save_post(client, email, password, url, output_dir, prefix="") -> tuple[bool, str, list[str]]:
    """抓取帖子并保存，同时提取其中的论坛链接"""
    try:
        post_detail = await client.read_full_forum_post(email, password, url, include_comments=True)
        if not post_detail.get("success"):
            print(f"Failed to fetch content for URL: {url}")
            return False, "", []
        
        post = post_detail.get("post", {})
        comments = post_detail.get("comments", [])
        title = post.get("title", "Unknown Title")
        body = post.get("body", "")
        
        # 提取文章正文和评论中的所有链接
        content_to_scan = body + "\n" + "\n".join([c.get("body", "") for c in comments])
        extracted_links = extract_forum_links(content_to_scan)
        
        # 清理文件名
        clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
        filename = output_dir / f"{prefix}{clean_title}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"- **链接**: {url}\n")
            f.write(f"- **作者**: {post.get('author', 'Unknown')}\n")
            f.write(f"- **发布时间/热度**: {post.get('details', {}).get('date', 'Unknown')}, 得票: {post.get('details', {}).get('votes', '0')}\n\n")
            f.write("## 帖子正文\n\n")
            f.write(f"{body}\n\n")
            f.write("---\n\n")
            f.write(f"## 讨论与评论 ({len(comments)})\n\n")
            for idx, c in enumerate(comments, 1):
                f.write(f"### 评论 #{idx} (作者: {c.get('author')}, 时间: {c.get('date')})\n\n")
                f.write(f"{c.get('body', '')}\n\n---\n\n")
                
        print(f"Saved successfully to: {filename}")
        return True, title, extracted_links
    except Exception as e:
        print(f"Exception extracting post '{url}': {e}")
        return False, "", []

async def main():
    email, password = load_credentials()
    client = ForumClient()
    
    search_tasks = [
        ("\u964d\u4f4e\u76f8\u5173\u6027", "zh-cn"),  # 降低相关性
        ("\u81ea\u76f8\u5173", "zh-cn"),        # 自相关
        ("reduce self-correlation", "en-us"),
        ("lower correlation", "en-us"),
        ("correlation too high", "en-us"),
        ("reduce correlation", "en-us")
    ]
    
    all_posts = []
    seen_links = set()
    
    for query, locale in search_tasks:
        print(f"Searching WQ forum ({locale}) for: '{query}'...")
        try:
            res = await client.search_forum_posts(email, password, query, max_results=8, locale=locale)
            if res.get("success"):
                for r in res.get("results", []):
                    link = r.get("link")
                    if link and link not in seen_links:
                        seen_links.add(link)
                        all_posts.append(r)
        except Exception as e:
            print(f"Error searching WQ forum: {e}")
            
    # 按 votes / comments 排序
    all_posts.sort(key=lambda x: (x.get("votes", 0), x.get("comments", 0)), reverse=True)
    
    # 筛选关键词
    relevant_posts = []
    keywords = ["相关", "correlation", "self-corr", "sc", "pnl", "优化", "prun", "reduce", "lower"]
    for post in all_posts:
        title_lower = post.get("title", "").lower()
        snippet_lower = post.get("snippet", "").lower()
        if any(kw in title_lower or kw in snippet_lower for kw in keywords):
            relevant_posts.append(post)
            
    if not relevant_posts:
        relevant_posts = all_posts[:3]
        
    print(f"Found {len(relevant_posts)} relevant posts. Fetching top 3 posts as Level 1...")
    
    output_dir = Path("./reference/unverified")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存已成功抓取的标准 URL 以便 Level 2 去重
    processed_urls = set()
    
    level2_links_queue = []
    extracted_l1_count = 0
    
    # Level 1 抓取
    for post_info in relevant_posts[:3]:
        title = post_info.get("title", "Unknown Title")
        url = post_info.get("link")
        
        print(f"\n[Level 1] Fetching: {title} ({url})...")
        success, final_title, l2_links = await fetch_and_save_post(client, email, password, url, output_dir, prefix="")
        if success:
            extracted_l1_count += 1
            processed_urls.add(url)
            for l2_link in l2_links:
                if l2_link not in processed_urls:
                    level2_links_queue.append(l2_link)
                    
    print(f"\nLevel 1 done. Successfully fetched {extracted_l1_count} posts.")
    print(f"Found {len(level2_links_queue)} unique potential Level 2 links inside Level 1 posts.")
    
    # 去重
    level2_links_queue = list(set(level2_links_queue))
    
    # Level 2 抓取 (深度限制为 2)
    extracted_l2_count = 0
    for idx, l2_url in enumerate(level2_links_queue, 1):
        if l2_url in processed_urls:
            continue
        
        print(f"\n[Level 2] Fetching link {idx}/{len(level2_links_queue)}: {l2_url}...")
        success, final_title, _ = await fetch_and_save_post(client, email, password, l2_url, output_dir, prefix="[L2] ")
        if success:
            processed_urls.add(l2_url)
            extracted_l2_count += 1
            
    print(f"\nDone! Level 1: {extracted_l1_count} posts, Level 2: {extracted_l2_count} posts saved to {output_dir}.")

if __name__ == "__main__":
    asyncio.run(main())
