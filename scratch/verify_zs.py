import os
import re
from pathlib import Path

adv_id = "ZS59763"
adv_dir = Path(r"d:\code\WorldQuant Brain\consultant\gui\reference\top100Rank-2026Q2\user_activity\ZS59763")

if not adv_dir.exists():
    print(f"Error: {adv_dir} does not exist.")
    exit(1)

files = list(adv_dir.glob("*.md"))
print(f"Total markdown files found: {len(files)}")

local_posts = []
local_commented_files = []
l2_files = []
other_files = []

for f in files:
    if f.name.startswith("[L2]"):
        l2_files.append(f)
    elif f.name.startswith("[Commented]"):
        local_commented_files.append(f)
    else:
        # Check if it starts with anything else, but is not L2/Commented
        local_posts.append(f)

print(f"L2 files count: {len(l2_files)}")
print(f"Files starting with [Commented] count: {len(local_commented_files)}")
print(f"Other files (assumed posts authored by ZS59763) count: {len(local_posts)}")

# Let's count how many total comments ZS59763 authored in all files (excluding L2)
total_comments_by_zs = 0
comments_per_file = {}

for f in files:
    if f.name.startswith("[L2]"):
        continue
    try:
        content = f.read_text(encoding="utf-8")
        # Match pattern like: ### 评论 #1 (作者: ZS59763, 时间: ...)
        comment_pattern = rf'### 评论 #\d+ \(作者:\s*{adv_id}\b'
        matches = re.findall(comment_pattern, content)
        if matches:
            comments_per_file[f.name] = len(matches)
            total_comments_by_zs += len(matches)
    except Exception as e:
        print(f"Error reading {f.name}: {e}")

print(f"\nTotal comments authored by {adv_id} found in local files: {total_comments_by_zs}")
print(f"Number of files containing comments by {adv_id}: {len(comments_per_file)}")

# Print files containing multiple comments by ZS59763
multiple_comments = {k: v for k, v in comments_per_file.items() if v > 1}
if multiple_comments:
    print(f"\nFiles with multiple comments by {adv_id}:")
    for k, v in sorted(multiple_comments.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {k}: {v} comments")
