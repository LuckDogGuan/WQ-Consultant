import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

profile_comments_path = Path("scratch/zs_profile_comments.json")
if not profile_comments_path.exists():
    print("Error: scratch/zs_profile_comments.json not found.")
    exit(1)
    
profile_comments = json.loads(profile_comments_path.read_text(encoding="utf-8"))

def extract_post_id(url: str) -> str:
    if not url:
        return ""
    m = re.search(r'/posts/(\d+)', url)
    if m:
        return m.group(1)
    m = re.search(r'/articles/(\d+)', url)
    if m:
        return m.group(1)
    return ""

profile_by_post = {}
for c in profile_comments:
    post_id = extract_post_id(c["post_url"])
    if not post_id:
        continue
    if post_id not in profile_by_post:
        profile_by_post[post_id] = []
    profile_by_post[post_id].append(c)

adv_id = "ZS59763"
adv_dir = Path(r"d:\code\WorldQuant Brain\consultant\gui\reference\top100Rank-2026Q2\user_activity\ZS59763")
local_files = list(adv_dir.glob("*.md"))

local_by_post = {}
for f in local_files:
    if f.name.startswith("[L2]"):
        continue
    m = re.search(r'_(\d+)\.md$', f.name)
    if m:
        local_by_post[m.group(1)] = f

print(f"Profile: 182 comments across {len(profile_by_post)} unique posts.")
print(f"Local: {len(local_by_post)} files (excluding [L2]).")

missing_posts = []
mismatched_comments = []

for post_id, p_comms in profile_by_post.items():
    expected_count = len(p_comms)
    if post_id not in local_by_post:
        missing_posts.append((post_id, p_comms[0]["title"], expected_count))
        continue
        
    f_path = local_by_post[post_id]
    try:
        content = f_path.read_text(encoding="utf-8")
        comment_pattern = rf'### 评论 #\d+ \(作者:\s*{adv_id}\b'
        matches = re.findall(comment_pattern, content)
        actual_count = len(matches)
        
        if actual_count != expected_count:
            mismatched_comments.append({
                "post_id": post_id,
                "file_name": f_path.name,
                "expected": expected_count,
                "actual": actual_count
            })
    except Exception as e:
        print(f"Error reading local file {f_path.name}: {e}")

print("\n=== Summary ===")
print(f"Total unique posts from profile: {len(profile_by_post)}")
print(f"Total local post files: {len(local_by_post)}")
print(f"Total missing posts: {len(missing_posts)}")
print(f"Total mismatched comment count posts: {len(mismatched_comments)}")

if missing_posts:
    print("\n=== Missing Posts ===")
    for pid, title, count in missing_posts:
        print(f"  - Post ID: {pid}, Title: '{title}', Expected Comments: {count}")

if mismatched_comments:
    print("\n=== Mismatched Comments ===")
    for m in mismatched_comments:
        print(f"  - File: {m['file_name']}, Expected: {m['expected']}, Actual: {m['actual']}")
