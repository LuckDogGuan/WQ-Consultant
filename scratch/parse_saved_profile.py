from bs4 import BeautifulSoup
from pathlib import Path

html_path = Path("scratch/profile_page.html")
if not html_path.exists():
    print(f"Error: {html_path} does not exist.")
    exit(1)

soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), 'html.parser')

comments_ul = soup.select_one('ul.profile-comments')
if comments_ul:
    items = comments_ul.select('li.profile-contribution')
    print(f"Found {len(items)} items of class 'profile-contribution' inside ul.profile-comments!")
    for idx, li in enumerate(items[:5]):
        print(f"\n--- Item #{idx} ---")
        print(li.prettify())
else:
    print("Could not find ul.profile-comments.")
