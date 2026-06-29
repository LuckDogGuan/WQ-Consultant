import sys
from bs4 import BeautifulSoup
from pathlib import Path

# Set stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

html_path = Path("scratch/profile_page.html")
if not html_path.exists():
    print(f"Error: {html_path} does not exist.")
    exit(1)

soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), 'html.parser')

comments_ul = soup.select_one('ul.profile-comments')
if comments_ul:
    items = comments_ul.select('li.profile-contribution')
    print(f"Found {len(items)} profile-contribution items on the page.")
    
    unique_post_ids = set()
    for idx, li in enumerate(items):
        # Try to find comment-link
        comment_a = li.select_one('a.comment-link')
        comment_href = comment_a.get('href', '') if comment_a else ""
        
        # Try to find post link in breadcrumbs
        breadcrumbs = li.select('.profile-contribution-breadcrumbs a')
        post_href = ""
        if breadcrumbs:
            # The last link in breadcrumbs should be the post link
            post_href = breadcrumbs[-1].get('href', '')
            
        print(f"Item #{idx}:")
        print(f"  Post link: {post_href}")
        print(f"  Comment link: {comment_href}")
        
        # Extract post ID
        import re
        m = re.search(r'/community/posts/(\d+)', post_href)
        if m:
            unique_post_ids.add(m.group(1))
            
    print(f"\nUnique post IDs found: {len(unique_post_ids)}")
else:
    print("Could not find ul.profile-comments.")
