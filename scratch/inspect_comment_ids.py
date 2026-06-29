import asyncio
import json
import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

possible_untracked_paths = [
    Path(r"C:\Program Files\Python312\Lib\site-packages\cnhkmcp\untracked"),
    Path(r"C:\Users\31186\AppData\Roaming\Python\Python312\site-packages\cnhkmcp\untracked")
]
for p in possible_untracked_paths:
    if p.exists() and (p / "forum_functions.py").exists():
        sys.path.insert(0, str(p))
        break

from forum_functions import ForumClient

def load_credentials():
    config_file = r"D:\SoftWare\AiWorkFlow\user_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        credentials = config_data.get("credentials", {})
        return credentials.get("email"), credentials.get("password")
    return None, None

async def main():
    email, password = load_credentials()
    client = ForumClient()
    
    async with async_playwright() as p:
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        
        # Sign in
        signin_url = "https://support.worldquantbrain.com/hc/zh-cn/signin"
        await page.goto(signin_url, wait_until="domcontentloaded")
        
        post_url = "https://support.worldquantbrain.com/hc/zh-cn/community/posts/32988918972183-ATOM%E6%A8%A1%E6%9D%BF%E5%88%86%E4%BA%AB"
        await page.goto(post_url, wait_until="domcontentloaded")
        
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        comments = soup.select('.comment')
        print(f"Found {len(comments)} comment elements in HTML.")
        
        for idx, comment in enumerate(comments[:3]):
            print(f"\n--- Comment #{idx} ---")
            print(f"Attributes: {comment.attrs}")
            # Look for permalink or id
            comment_id = comment.get('id', '')
            print(f"ID attribute: {comment_id}")
            
            # Find any links inside the comment that might contain comment IDs
            links = comment.select('a')
            for a in links:
                href = a.get('href', '')
                if 'comment' in href or 'permalink' in a.get('class', []):
                    print(f"  Link: text='{a.get_text(strip=True)}', href='{href}', class={a.get('class')}")
                    
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
