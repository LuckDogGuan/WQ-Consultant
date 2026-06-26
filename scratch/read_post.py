import os
import sys
import json
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import importlib.util

# Setup untracked path for forum_functions
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

from forum_functions import ForumClient

def load_credentials():
    possible_paths = [
        Path("user_config.json"),
        Path("../user_config.json"),
        Path("../../user_config.json"),
        Path(os.path.expanduser("~")) / ".config" / "AiWorkFlow" / "user_config.json",
        Path("D:/SoftWare/AiWorkFlow/user_config.json")
    ]
    for p in possible_paths:
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            credentials = config_data.get("credentials", {})
            return credentials.get("email"), credentials.get("password")
    print("Credentials not found")
    sys.exit(1)

async def main():
    email, password = load_credentials()
    client = ForumClient()
    url = "https://support.worldquantbrain.com/hc/en-us/community/posts/41065497021335--%E5%90%B9%E5%93%A8%E4%BA%BA-%E4%B8%8D%E5%86%8D%E6%B0%B4%E8%B4%B4-%E6%9C%80%E6%96%B0-MCP-%E8%87%AA%E5%B8%A6-brain-forum-browse-Skill-%E5%AF%B9-AI-%E8%AF%B4-%E9%80%9B%E4%B8%80%E9%80%9B%E8%AE%BA%E5%9D%9B-%E5%8D%B3%E5%8F%AF%E8%87%AA%E5%8A%A8%E9%80%9B%E8%AE%BA%E5%9D%9B"
    
    async with async_playwright() as p:
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        print(f"Navigating to {url}")
        await page.goto(url, wait_until="domcontentloaded")
        try:
            await page.wait_for_selector('.post-body, .article-body', timeout=10000)
        except Exception as e:
            print("Failed to find post body selector:", e)
            
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        title = soup.select_one('.post-title, h1.article-title')
        body = soup.select_one('.post-body, .article-body')
        
        print("\n=== TITLE ===")
        print(title.get_text(strip=True) if title else "No Title")
        print("\n=== BODY ===")
        print(body.get_text(strip=True) if body else "No Body")
        
        # Comments
        comments = soup.select('.comment')
        print(f"\n=== COMMENTS ({len(comments)}) ===")
        for idx, comment in enumerate(comments, 1):
            author_span = comment.select_one('.comment-author span[title]')
            author_id = author_span['title'] if author_span else 'Unknown'
            body_element = comment.select_one('.comment-body')
            body_text = body_element.get_text(strip=True) if body_element else ''
            print(f"#{idx} Author: {author_id}")
            print(body_text)
            print("-" * 20)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
