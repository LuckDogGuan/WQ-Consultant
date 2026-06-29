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
        print(f"Navigating to post: {post_url}")
        try:
            response = await page.goto(post_url, wait_until="domcontentloaded")
            print(f"Response status: {response.status if response else 'No Response'}")
            print(f"Current page URL: {page.url}")
            
            # Wait for content
            await page.wait_for_selector('.post-body, .article-body, .error-page', timeout=5000)
            content = await page.content()
            
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.select_one('.post-title, h1.article-title, .article__title')
            print(f"Title: {title.get_text(strip=True) if title else 'None'}")
            
            body = soup.select_one('.post-body, .article-body')
            print(f"Body found: {body is not None}")
            
            error_msg = soup.select_one('.error-message, .error-page')
            if error_msg:
                print(f"Error element text: {error_msg.get_text(strip=True)}")
                
        except Exception as e:
            print(f"Error fetching post: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
