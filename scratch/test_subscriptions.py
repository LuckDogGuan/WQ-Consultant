import os
import sys
import asyncio
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


from forum_functions import ForumClient
from playwright.async_api import async_playwright
import json

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

async def test_sub():
    email, password = load_credentials()
    client = ForumClient()
    
    async with async_playwright() as p:
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        
        target_url = "https://support.worldquantbrain.com/hc/en-us/subscriptions"
        print(f"Navigating to {target_url}...")
        await page.goto(target_url, wait_until="networkidle")
        
        # 保存页面 HTML 便于观察
        html_content = await page.content()
        Path("scratch/subscriptions_temp.html").write_text(html_content, encoding="utf-8")
        print("Saved HTML to scratch/subscriptions_temp.html")
        
        # 简单解析一下页面上的链接
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 寻找订阅列表链接
        # 常见 Zendesk subscriptions 结构类似 table.subscriptions-table 或 a[href*="/community/posts/"]
        links = []
        for a in soup.select("a"):
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if "/community/posts/" in href or "/articles/" in href:
                links.append((text, href))
                
        print(f"Found {len(links)} potential subscription links:")
        for idx, (txt, href) in enumerate(links, 1):
            print(f"{idx}. [{txt}] -> {href}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_sub())
