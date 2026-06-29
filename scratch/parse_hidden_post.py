from bs4 import BeautifulSoup
from pathlib import Path

html_path = Path("scratch/post_31978925276823.html")
if not html_path.exists():
    print(f"Error: {html_path} does not exist.")
    exit(1)

soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), 'html.parser')

print("Page Title:", soup.title.get_text(strip=True) if soup.title else "None")

# Search for any divs or headings that could represent the main message
main_content = soup.select_one('main') or soup.select_one('.main-layout')
if main_content:
    print("\n--- Main Content Text ---")
    print(main_content.get_text(separator="\n", strip=True)[:1000])
else:
    print("No <main> or .main-layout found.")
    print("Page body text:")
    print(soup.body.get_text(separator="\n", strip=True)[:1000] if soup.body else "No Body")
