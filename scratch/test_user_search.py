import os
import sys
import asyncio
import importlib.util
from pathlib import Path
import json

# 动态引入 cnhkmcp
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


from forum_functions import ForumClient
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

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

    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    credentials = config_data.get("credentials", {})
    return credentials.get("email"), credentials.get("password")

async def test_search():
    email, password = load_credentials()
    client = ForumClient()
    
    # 比如我们搜索一个活跃顾问：KZ79256
    query = "KZ79256"
    print(f"Searching for user: {query}...")
    
    res = await client.search_forum_posts(email, password, query, max_results=5, locale="zh-cn")
    if res.get("success"):
        results = res.get("results", [])
        print(f"Found {len(results)} results:")
        for idx, r in enumerate(results, 1):
            print(f"{idx}. [{r.get('title')}] -> {r.get('link')} (Author: {r.get('author')})")
            
        # 我们随机访问一个搜索到的帖子，寻找 KZ79256 的个人主页链接
        if results:
            target_post_url = results[0].get("link")
            print(f"\nNavigating to post to look for user profiles: {target_post_url}")
            async with async_playwright() as p:
                browser, context = await client._get_browser_context(p, email, password)
                page = await client._new_page(context)
                await page.goto(target_post_url, wait_until="networkidle")
                
                html_content = await page.content()
                soup = BeautifulSoup(html_content, "html.parser")
                
                # 寻找形如 /profiles/ 或 /users/ 的链接
                profile_links = []
                for a in soup.select("a"):
                    href = a.get("href", "")
                    text = a.get_text(strip=True)
                    if "/profiles/" in href:
                        profile_links.append((text, href))
                        
                print(f"\nFound {len(profile_links)} profile links in the page:")
                for txt, href in profile_links[:10]:
                    print(f"- [{txt}] -> {href}")
                    
                await browser.close()
    else:
        print("Search failed.")

if __name__ == "__main__":
    asyncio.run(test_search())
