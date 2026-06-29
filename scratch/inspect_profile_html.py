import asyncio
import json
import os
import sys
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
        print("Launching browser...")
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        
        # Sign in
        signin_url = "https://support.worldquantbrain.com/hc/zh-cn/signin"
        print(f"Navigating to signin: {signin_url}")
        await page.goto(signin_url, wait_until="domcontentloaded")
        print("SSO Login completed.")
        
        user_id = "26858512793111"
        adv_id = "ZS59763"
        
        current_url = f"https://support.worldquantbrain.com/hc/zh-cn/profiles/{user_id}-{adv_id}?filter_by=comments&sort_by=recent_user_activity"
        print(f"Navigating to profile comments page: {current_url}")
        await page.goto(current_url, wait_until="domcontentloaded")
        print("Navigation to profile comments page done.")
        
        try:
            print("Waiting for .profile-section to load...")
            await page.wait_for_selector('.profile-section', timeout=8000)
            print(".profile-section loaded successfully.")
        except Exception as e:
            print(f"wait_for_selector failed: {e}")
            
        content = await page.content()
        Path("scratch/profile_page.html").write_text(content, encoding="utf-8")
        print("Saved profile page HTML to scratch/profile_page.html")
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for elements
        print("Checking lists and elements:")
        ul_elems = soup.find_all('ul')
        print(f"Total <ul> tags: {len(ul_elems)}")
        for idx, ul in enumerate(ul_elems[:10]):
            ul_class = ul.get('class', [])
            print(f"  ul #{idx}: class={ul_class}")
            
        # Print tab text and link
        print("\nChecking tabs/navigation links:")
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if 'filter_by=' in href or 'profiles' in href:
                print(f"  Link text: '{a.get_text(strip=True)}', href: '{href}'")
                
        # Let's inspect profile-activity list
        print("\nChecking items with 'profile' classes:")
        for el in soup.find_all(class_=re.compile("profile")):
            print(f"  Tag: {el.name}, Class: {el.get('class')}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
