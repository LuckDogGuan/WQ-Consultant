import os
import sys
import json
import asyncio
import re
import importlib.util
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

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
    # 匹配论坛帖子及文章的链接模式
    pattern = r'https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/\d+(?:-[a-zA-Z0-9%-]+)?'
    links = re.findall(pattern, text)
    
    # 同时也匹配相对路径的 /hc/.../community/posts/... 链接
    relative_pattern = r'/hc/[a-zA-Z-]+/community/posts/\d+(?:-[a-zA-Z0-9%-]+)?'
    rel_links = re.findall(relative_pattern, text)
    for rl in rel_links:
        links.append(f"https://support.worldquantbrain.com{rl}")
        
    normalized_links = []
    for link in links:
        match = re.match(r'(https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/\d+)', link)
        if match:
            normalized_links.append(match.group(1))
    return list(set(normalized_links))

def extract_post_id(url: str) -> str:
    match = re.search(r'/community/posts/(\d+)', url)
    if match:
        return match.group(1)
    match = re.search(r'/articles/(\d+)', url)
    if match:
        return match.group(1)
    return url

async def fetch_and_save_post(client, email, password, url, output_dir, prefix="") -> tuple[bool, str, list[str]]:
    """抓取帖子并保存，同时提取其中的论坛链接"""
    # 断点续传：扫描本地已下载文件，若包含此 URL 则直接提取链接并跳过网络请求
    post_id = extract_post_id(url)
    for p in output_dir.glob("*.md"):
        try:
            content = p.read_text(encoding="utf-8")
            if url in content or (post_id and post_id in content):
                # 提取标题
                title_match = re.match(r'# (.*)', content)
                title = title_match.group(1) if title_match else p.stem
                print(f"Skipping download (already exists locally): {title} ({p.name})")
                extracted_links = extract_forum_links(content)
                return True, title, extracted_links
        except Exception:
            pass

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
        
        # 清理文件名防止系统字符冲突
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
    
    output_dir = Path("./reference/unverified")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    level1_subscriptions = []
    seen_ids = set()
    
    # 第一步：访问 Subscriptions 列表并解析
    async with async_playwright() as p:
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        
        target_url = "https://support.worldquantbrain.com/hc/en-us/subscriptions"
        print(f"Navigating to {target_url}...")
        await page.goto(target_url, wait_until="networkidle")
        
        html_content = await page.content()
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 提取订阅的文章/帖子链接
        for a in soup.select("a"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if "/community/posts/" in href or "/articles/" in href:
                full_url = href if href.startswith("http") else f"https://support.worldquantbrain.com{href}"
                post_id = extract_post_id(full_url)
                if post_id not in seen_ids:
                    seen_ids.add(post_id)
                    level1_subscriptions.append((title, full_url))
        
        await browser.close()
        
    print(f"\nFound {len(level1_subscriptions)} unique subscription links from the list.")
    
    processed_urls = set()
    level2_links_queue = []
    extracted_l1_count = 0
    
    # 第二步：抓取 Level 1 订阅帖子
    for idx, (title, url) in enumerate(level1_subscriptions, 1):
        print(f"\n[Level 1] Fetching {idx}/{len(level1_subscriptions)}: {title} ({url})...")
        success, final_title, l2_links = await fetch_and_save_post(client, email, password, url, output_dir, prefix="")
        if success:
            extracted_l1_count += 1
            processed_urls.add(url)
            for l2_link in l2_links:
                if l2_link not in processed_urls:
                    level2_links_queue.append(l2_link)
                    
    print(f"\nLevel 1 done. Successfully fetched {extracted_l1_count} subscription posts.")
    print(f"Found {len(level2_links_queue)} unique potential Level 2 links inside Level 1 posts.")
    
    # 去重
    level2_links_queue = list(set(level2_links_queue))
    
    # 第三步：抓取 Level 2 链接（最多二层）
    extracted_l2_count = 0
    for idx, l2_url in enumerate(level2_links_queue, 1):
        l2_id = extract_post_id(l2_url)
        # 检查是否已包含在 Level 1 或已抓取过的列表里
        if l2_id in seen_ids or l2_url in processed_urls:
            continue
            
        print(f"\n[Level 2] Fetching link {idx}/{len(level2_links_queue)}: {l2_url}...")
        success, final_title, _ = await fetch_and_save_post(client, email, password, l2_url, output_dir, prefix="[L2] ")
        if success:
            processed_urls.add(l2_url)
            seen_ids.add(l2_id)
            extracted_l2_count += 1
            
    print(f"\nDone! Level 1: {extracted_l1_count} posts, Level 2: {extracted_l2_count} posts saved to {output_dir}.")

if __name__ == "__main__":
    asyncio.run(main())
