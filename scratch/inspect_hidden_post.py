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
        
        post_url = "https://support.worldquantbrain.com/hc/zh-cn/community/posts/31978925276823"
        await page.goto(post_url, wait_until="domcontentloaded")
        
        content = await page.content()
        Path("scratch/post_31978925276823.html").write_text(content, encoding="utf-8")
        print("Saved html to scratch/post_31978925276823.html")
        
        soup = BeautifulSoup(content, 'html.parser')
        # Check elements
        print(f"Title element: {soup.select_one('.post-title')}")
        print(f"Post body element class/style: {soup.select_one('.post-body')}")
        print(f"Error elements: {soup.select('.error-page, .error-message')}")
        
        # Check if we can find any text about "您没有权限" (You don't have permission) or similar
        print(f"Page text length: {len(soup.get_text())}")
        if "没有权限" in content or "not authorized" in content.lower() or "登入" in content or "登录" in content:
            print("Detected permission/authorization words in page!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
