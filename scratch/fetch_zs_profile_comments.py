import asyncio
import json
import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Add untracked path for ForumClient
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
        
        user_id = "26858512793111"
        adv_id = "ZS59763"
        
        current_url = f"https://support.worldquantbrain.com/hc/zh-cn/profiles/{user_id}-{adv_id}?filter_by=comments&sort_by=recent_user_activity"
        page_num = 1
        all_profile_comments = []
        
        while current_url:
            print(f"Fetching page {page_num}: {current_url}")
            await page.goto(current_url, wait_until="domcontentloaded")
            try:
                await page.wait_for_selector('ul.profile-comments', timeout=5000)
            except Exception as e:
                print(f"Timeout waiting for profile comments on page {page_num}: {e}")
                break
                
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            comments_ul = soup.select_one('ul.profile-comments')
            if not comments_ul:
                print("Could not find ul.profile-comments on this page.")
                break
                
            items = comments_ul.select('li.profile-contribution')
            print(f"Found {len(items)} profile-contribution items on page {page_num}")
            
            for item in items:
                # Find comment-link
                comment_a = item.select_one('a.comment-link')
                comment_href = comment_a.get('href', '') if comment_a else ""
                
                # Find post link
                breadcrumbs = item.select('.profile-contribution-breadcrumbs a')
                post_href = breadcrumbs[-1].get('href', '') if breadcrumbs else ""
                
                # Find title
                title_li = breadcrumbs[-1] if breadcrumbs else None
                title = title_li.get('title', '') if title_li else ""
                if not title and title_li:
                    title = title_li.get_text(strip=True)
                
                # Body snippet
                body_p = item.select_one('.profile-contribution-body')
                body_text = body_p.get_text(strip=True) if body_p else ""
                
                all_profile_comments.append({
                    "title": title,
                    "post_url": post_href,
                    "comment_url": comment_href,
                    "snippet": body_text
                })
                
            next_a = soup.select_one('a.pagination-next-link')
            if next_a and next_a.get('href'):
                next_href = next_a.get('href')
                current_url = next_href if next_href.startswith('http') else f"https://support.worldquantbrain.com{next_href}"
                page_num += 1
            else:
                current_url = None
                
        print(f"\nTotal profile comments parsed: {len(all_profile_comments)}")
        
        # Save to json file for analysis
        out_file = Path("scratch/zs_profile_comments.json")
        out_file.write_text(json.dumps(all_profile_comments, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved to {out_file}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
