import os
import sys
import json
import asyncio
from pathlib import Path
import importlib.util

sys.path.insert(0, r"C:\Program Files\Python312\Lib\site-packages\cnhkmcp\untracked")
sys.path.insert(0, r"C:\Users\31186\AppData\Roaming\Python\Python312\site-packages\cnhkmcp\untracked")

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
    return None, None

async def main():
    email, password = load_credentials()
    if not email:
        print("Credentials not found")
        return
        
    # Import platform_functions and print its path
    import platform_functions
    print(f"platform_functions path: {platform_functions.__file__}")
    from platform_functions import brain_client
    
    await brain_client.authenticate(email, password)
    # Ensure support session is active
    csrf_token = await brain_client._ensure_support_session()
    print(f"Support session established. CSRF token: {csrf_token}")
    
    # Test user: ZS59763 -> 26858512793111
    user_id = "26858512793111"
    
    # Try posts API
    print(f"Testing ZS59763 posts...")
    posts_url = f"/api/v2/community/users/{user_id}/posts.json"
    try:
        response = await brain_client._support_get(posts_url)
        print(f"Posts API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('posts', []))} posts")
            for post in data.get('posts', [])[:3]:
                print(f"  - Post ID: {post.get('id')}, Title: {post.get('title')}")
    except Exception as e:
        print(f"Error testing posts: {e}")
        
    # Try comments API
    print(f"Testing ZS59763 comments...")
    comments_url = f"/api/v2/community/users/{user_id}/comments.json"
    try:
        response = await brain_client._support_get(comments_url)
        print(f"Comments API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('comments', []))} comments")
            for comment in data.get('comments', [])[:3]:
                print(f"  - Comment ID: {comment.get('id')}, Post ID: {comment.get('post_id')}, Body (partial): {comment.get('body')[:50]}")
    except Exception as e:
        print(f"Error testing comments: {e}")

if __name__ == "__main__":
    asyncio.run(main())
