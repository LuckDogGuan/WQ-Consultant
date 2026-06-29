import json
import re
import sys
from pathlib import Path

# Set stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load the 182 comments from profile
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

# Group profile comments by post_id
profile_by_post = {}
for c in profile_comments:
    post_id = extract_post_id(c["post_url"])
    if not post_id:
        print(f"Could not extract post ID from: {c['post_url']}")
        continue
    if post_id not in profile_by_post:
        profile_by_post[post_id] = []
    profile_by_post[post_id].append(c)

print(f"Profile: 182 comments are distributed across {len(profile_by_post)} unique posts.")

# Now check local directory
adv_id = "ZS59763"
adv_dir = Path(r"d:\code\WorldQuant Brain\consultant\gui\reference\top100Rank-2026Q2\user_activity\ZS59763")
local_files = list(adv_dir.glob("*.md"))

# Map local files by post_id
local_by_post = {}
for f in local_files:
    if f.name.startswith("[L2]"):
        continue
    m = re.search(r'_(\d+)\.md$', f.name)
    if m:
        local_by_post[m.group(1)] = f

print(f"Local: Found {len(local_by_post)} local files (excluding [L2]).")

# Perform comparison
missing_posts = []
mismatched_comments = []

for post_id, p_comms in profile_by_post.items():
    expected_count = len(p_comms)
    
    if post_id not in local_by_post:
        missing_posts.append((post_id, p_comms[0]["title"], expected_count))
        continue
        
    # Read local file and count comments by adv_id
    f_path = local_by_post[post_id]
    try:
        content = f_path.read_text(encoding="utf-8")
        # Match pattern like: ### 评论 #1 (作者: ZS59763, 时间: ...)
        comment_pattern = rf'### 评论 #\d+ \(作者:\s*{adv_id}\b'
        matches = re.findall(comment_pattern, content)
        actual_count = len(matches)
        
        if actual_count != expected_count:
            mismatched_comments.append({
                "post_id": post_id,
                "file_name": f_path.name,
                "expected": expected_count,
                "actual": actual_count,
                "profile_snippets": [c["snippet"][:60] for c in p_comms]
            })
    except Exception as e:
        print(f"Error reading local file {f_path.name}: {e}")

print("\n=== Missing Posts ===")
print(f"Total {len(missing_posts)} posts found in profile but missing locally:")
for pid, title, count in missing_posts:
    print(f"  - Post ID: {pid}, Title: '{title}', Expected Comments: {count}")

print("\n=== Mismatched Comments (Expected vs Actual) ===")
print(f"Total {len(mismatched_comments)} files have mismatch in comment count:")
for m in mismatched_comments:
    print(f"  - File: {m['file_name']}")
    print(f"    Expected comments from profile: {m['expected']}, Actual in local file: {m['actual']}")
    print(f"    Snippets of expected comments:")
    for snip in m['profile_snippets']:
        print(f"      * {snip}...")
