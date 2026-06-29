import os
import sys
import json
import asyncio
import re
import importlib.util
import shutil
import uuid
import base64
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def download_image_via_page(page, img_url: str, output_path: Path) -> bool:
    try:
        if img_url.startswith("data:"):
            if "," in img_url:
                header, encoded = img_url.split(",", 1)
                data = base64.b64decode(encoded)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(data)
                return True
            return False

        # Run fetch in the browser context to get the image as a base64 string
        # This will automatically use the browser's cookies and session!
        js_code = """
        async (url) => {
            const response = await fetch(url);
            const blob = await response.blob();
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(blob);
            });
        }
        """
        base64_data = await page.evaluate(js_code, img_url)
        if "," in base64_data:
            header, encoded = base64_data.split(",", 1)
            data = base64.b64decode(encoded)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(data)
            return True
    except Exception as e:
        print(f"Error downloading image {img_url} via browser: {e}")
    return False

async def preprocess_html_to_markdown(page, element, output_dir: Path, download_images: bool = True, img_dir_name: str = "images") -> str:
    if not element:
        return ""
        
    async def convert_node(node) -> str:
        if isinstance(node, str):
            return node
            
        if not hasattr(node, 'name') or node.name is None:
            return str(node)
            
        tag_name = node.name.lower()
        
        if tag_name == 'br':
            return "\n"
            
        if tag_name in ['p', 'div']:
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            return f"\n\n{child_text.strip()}\n\n"
            
        if tag_name in ['strong', 'b']:
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            stripped = child_text.strip()
            if stripped:
                return f" **{stripped}** "
            return child_text
            
        if tag_name in ['em', 'i']:
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            stripped = child_text.strip()
            if stripped:
                return f" *{stripped}* "
            return child_text
            
        if tag_name == 'code':
            parent_name = node.parent.name.lower() if node.parent else ""
            child_text = node.get_text()
            if parent_name == 'pre':
                return child_text
            else:
                return f" `{child_text}` "
                
        if tag_name == 'pre':
            code_el = node.find('code')
            code_text = code_el.get_text() if code_el else node.get_text()
            return f"\n```\n{code_text}\n```\n"
            
        if tag_name == 'a':
            href = node.get('href', '')
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            child_text = child_text.strip()
            if href and child_text:
                return f" [{child_text}]({href}) "
            elif href:
                return f" {href} "
            else:
                return child_text
                
        if tag_name == 'img':
            src = node.get('src', '')
            alt = node.get('alt', '图片')
            if src:
                full_src = src if src.startswith('http') else f"https://support.worldquantbrain.com{src}"
                if not download_images:
                    return f" ![{alt}]({full_src}) "
                
                ext = ".png"
                clean_url = src.split('?')[0].split('#')[0]
                url_ext = Path(clean_url).suffix.lower()
                if url_ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
                    ext = url_ext
                
                img_uuid = uuid.uuid4().hex[:10]
                img_name = f"img_{img_uuid}{ext}"
                img_path = output_dir / img_dir_name / img_name
                
                print(f"Downloading image from {full_src} to {img_path}...")
                success = await download_image_via_page(page, full_src, img_path)
                if success:
                    return f" ![{alt}]({img_dir_name}/{img_name}) "
                else:
                    return f" ![{alt}]({full_src}) "
            return ""
            
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag_name[1])
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            return f"\n\n{'#' * level} {child_text.strip()}\n\n"
            
        if tag_name == 'blockquote':
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            lines = [line.strip() for line in child_text.strip().split('\n') if line.strip()]
            if lines:
                return "\n" + "\n".join([f"> {line}" for line in lines]) + "\n"
            return ""

        if tag_name == 'ul':
            child_text = ""
            for child in node.children:
                if hasattr(child, 'name') and child.name and child.name.lower() == 'li':
                    li_text = await convert_node(child)
                    li_lines = [line.strip() for line in li_text.strip().split('\n') if line.strip()]
                    if li_lines:
                        child_text += f"\n- {li_lines[0]}"
                        for line in li_lines[1:]:
                            child_text += f"\n  {line}"
            return f"\n{child_text}\n"
            
        if tag_name == 'ol':
            child_text = ""
            idx = 1
            for child in node.children:
                if hasattr(child, 'name') and child.name and child.name.lower() == 'li':
                    li_text = await convert_node(child)
                    li_lines = [line.strip() for line in li_text.strip().split('\n') if line.strip()]
                    if li_lines:
                        child_text += f"\n{idx}. {li_lines[0]}"
                        for line in li_lines[1:]:
                            child_text += f"\n   {line}"
                        idx += 1
            return f"\n{child_text}\n"
            
        if tag_name == 'li':
            child_text = ""
            for child in node.children:
                child_text += await convert_node(child)
            return child_text
            
        child_text = ""
        for child in node.children:
            child_text += await convert_node(child)
        return child_text

    text = await convert_node(element)
    
    lines = text.split('\n')
    cleaned_lines = []
    prev_was_empty = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_was_empty:
                cleaned_lines.append("")
                prev_was_empty = True
        else:
            cleaned_lines.append(line)
            prev_was_empty = False
            
    return "\n".join(cleaned_lines).strip()

def copy_referenced_images(source_md_path: Path, dest_md_path: Path):
    try:
        content = source_md_path.read_text(encoding="utf-8")
        img_refs = re.findall(r'!\[.*?\]\((images/[^)]+)\)', content)
        if img_refs:
            source_img_dir = source_md_path.parent / "images"
            dest_img_dir = dest_md_path.parent / "images"
            dest_img_dir.mkdir(parents=True, exist_ok=True)
            for img_rel_path in img_refs:
                img_name = Path(img_rel_path).name
                src_img = source_img_dir / img_name
                dest_img = dest_img_dir / img_name
                if src_img.exists() and not dest_img.exists():
                    shutil.copy2(src_img, dest_img)
                    print(f"Copied image {img_name} from {source_md_path.parent.name} to {dest_md_path.parent.name}")
    except Exception as e:
        print(f"Error copying referenced images: {e}")

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

# Now we can import ForumClient
from forum_functions import ForumClient

# 全局内存缓存，防止单次执行中对同一个帖子重复发起网络请求
network_cache = {}

# Zendesk ID 与 顾问ID 的本地对照表路径
MAP_FILE = Path("reference/top100Rank-2026Q2/user_activity/advisor_zendesk_map.json")

def load_advisor_zendesk_map() -> dict:
    if MAP_FILE.exists():
        try:
            return json.loads(MAP_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_advisor_zendesk_map(m: dict):
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        MAP_FILE.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"Error saving map file: {e}")

def sniff_profiles_from_html(html_content: str):
    """从 HTML 文本中嗅探所有个人主页链接，并持久化更新到 JSON 对照表"""
    m = load_advisor_zendesk_map()
    # 匹配形如 /profiles/14187300941847-XX42289 的链接
    pattern = r'/profiles/(\d+)-([A-Z]{2}\d{5})'
    matches = re.findall(pattern, html_content, re.IGNORECASE)
    
    updated = False
    for num_id, adv_id in matches:
        adv_id = adv_id.upper()
        if m.get(adv_id) != num_id:
            m[adv_id] = num_id
            print(f"[嗅探发现] 匹配关联: {adv_id} -> {num_id}")
            updated = True
            
    if updated:
        save_advisor_zendesk_map(m)

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

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        credentials = config_data.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if email and password:
            return email, password
    print("Error: Credentials not found in user_config.json.")
    sys.exit(1)

def extract_forum_links(text: str) -> list[str]:
    # 匹配论坛帖子链接
    pattern = r'https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/\d+(?:-[a-zA-Z0-9%-]+)?'
    links = re.findall(pattern, text)
    
    # 匹配相对路径链接
    relative_pattern = r'/hc/[a-zA-Z-]+/community/posts/\d+(?:-[a-zA-Z0-9%-]+)?'
    rel_links = re.findall(relative_pattern, text)
    for rl in rel_links:
        links.append(f"https://support.worldquantbrain.com{rl}")
        
    normalized_links = []
    for link in links:
        match = re.match(r'(https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/\d+)', link)
        if match:
            normalized_links.append(match.group(1))
    return list(set(normalized_links))

def extract_post_id(url: str) -> str:
    if not url:
        return ""
    match = re.search(r'/community/posts/(\d+)', url)
    if match:
        return match.group(1)
    match = re.search(r'/articles/(\d+)', url)
    if match:
        return match.group(1)
    if isinstance(url, str) and url.isdigit():
        return url
    return ""

def load_advisor_list() -> list[str]:
    """从 user_rank.md 解析前100名顾问 ID"""
    advisors = []
    rank_file = Path("reference/top100Rank-2026Q2/user_rank.md")
    if not rank_file.exists():
        print(f"Error: {rank_file} not found.")
        sys.exit(1)
        
    with open(rank_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines[1:]: # 跳过标题行
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            advisor_id = parts[1].strip()
            # 过滤只包含合法格式的 ID
            if re.match(r'^[A-Z]{2}\d{5}$', advisor_id):
                advisors.append(advisor_id)
    return advisors

def scan_all_local_posts(output_base_dir: Path) -> dict[str, Path]:
    """扫描所有已下载的帖子，建立 post_id 到本地文件路径的映射，用于极速去重和断点续传"""
    post_id_to_path = {}
    if not output_base_dir.exists():
        return post_id_to_path
    for root, dirs, files in os.walk(output_base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding="utf-8")
                    url_match = re.search(r'- \*\*链接\*\*: (https://[^\s\n]+)', content)
                    if url_match:
                        url = url_match.group(1)
                        post_id = extract_post_id(url)
                        if post_id:
                            if post_id not in post_id_to_path or "[L2]" in post_id_to_path[post_id].name:
                                post_id_to_path[post_id] = file_path
                except Exception:
                    pass
    return post_id_to_path

def save_post_content_to_file(url, title, body, comments, post_data, output_dir, prefix) -> Path:
    """统一的文件写入辅助函数"""
    post_id = extract_post_id(url)
    clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
    filename = output_dir / f"{prefix}{clean_title}_{post_id}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"- **链接**: {url}\n")
        f.write(f"- **作者**: {post_data.get('author', 'Unknown')}\n")
        f.write(f"- **发布时间/热度**: {post_data.get('details', {}).get('date', 'Unknown')}, 得票: {post_data.get('details', {}).get('votes', '0')}\n\n")
        f.write("## 帖子正文\n\n")
        f.write(f"{body}\n\n")
        f.write("---\n\n")
        f.write(f"## 讨论与评论 ({len(comments)})\n\n")
        for idx, c in enumerate(comments, 1):
            f.write(f"### 评论 #{idx} (作者: {c.get('author')}, 时间: {c.get('date')})\n\n")
            f.write(f"{c.get('body', '')}\n\n---\n\n")
            
    print(f"Saved successfully to: {filename.relative_to(output_dir.parent.parent)}")
    return filename

async def search_forum_posts_custom(page, search_query: str, max_results: int = 30) -> list[str]:
    """自定义快速搜索，如果在 4 秒内没有找到结果列表，说明已到尾页或无结果，直接退出"""
    search_results = []
    page_num = 1
    seen_urls = set()
    
    while len(search_results) < max_results:
        search_url = f"https://support.worldquantbrain.com/hc/zh-cn/search?page={page_num}&query={search_query}#results"
        print(f"Navigating to search page: {search_url} (Page {page_num})")
        
        try:
            response = await page.goto(search_url, wait_until="domcontentloaded")
            if response and response.status == 404:
                break
                
            await page.wait_for_selector('ul.search-results-list', timeout=4000)
        except Exception:
            break
            
        content = await page.content()
        # 顺便从搜索结果的页面中嗅探 profiles 链接
        sniff_profiles_from_html(content)
        
        soup = BeautifulSoup(content, 'html.parser')
        results_on_page = soup.select('li.search-result-list-item')
        if not results_on_page:
            break
            
        new_items = 0
        for result in results_on_page:
            title_element = result.select_one('h2.search-result-title a')
            if title_element:
                link = title_element.get('href')
                if link:
                    full_link = link if link.startswith('http') else f"https://support.worldquantbrain.com{link}"
                    post_id = extract_post_id(full_link)
                    if post_id and post_id not in seen_urls:
                        seen_urls.add(post_id)
                        search_results.append(full_link)
                        new_items += 1
                        
        if new_items == 0:
            break
            
        if len(results_on_page) < 10:
            break
            
        page_num += 1
        
    return search_results

async def read_full_forum_post_custom(page, post_url_or_id: str, output_dir: Path, include_comments: bool = True, max_comment_pages: int = 20, download_images: bool = True) -> dict:
    """自定义的高效读取帖子和评论的函数，并将评论等待超时缩短到 3 秒，避免 60 秒卡顿"""
    if post_url_or_id.startswith('http'):
        initial_url = post_url_or_id
    else:
        initial_url = f"https://support.worldquantbrain.com/hc/zh-cn/community/posts/{post_url_or_id}"

    # 1. 导航到主贴
    print(f"Navigating to initial URL: {initial_url}")
    await page.goto(initial_url, wait_until="domcontentloaded")
    await page.wait_for_selector('.post-body, .article-body', timeout=5000)
    
    base_url = re.sub(r'(\?|&)page=\d+', '', page.url).split('#')[0]
    
    content = await page.content()
    # 嗅探本主帖页面的 profiles 链接以匹配 Zendesk ID
    sniff_profiles_from_html(content)
    
    soup = BeautifulSoup(content, 'html.parser')

    post_data = {}
    title_element = soup.select_one('.post-title, h1.article-title, .article__title')
    post_data['title'] = title_element.get_text(strip=True) if title_element else 'Unknown Title'

    author_span = soup.select_one('.post-author span[title]')
    post_data['author'] = author_span['title'] if author_span else 'Unknown Author'

    body_element = soup.select_one('.post-body, .article-body')
    if body_element:
        post_data['body'] = await preprocess_html_to_markdown(page, body_element, output_dir, download_images=download_images)
    else:
        post_data['body'] = 'Body not found'
    
    votes_element = soup.select_one('.vote-sum')
    date_element = soup.select_one('.post-meta .meta-data')
    post_data['details'] = {
        'votes': votes_element.get_text(strip=True) if votes_element else '0',
        'date': date_element.get_text(strip=True) if date_element else 'Unknown Date'
    }

    # 2. 抓取评论
    comments = []
    if include_comments:
        # 页面1的评论已在 initial_url 加载时一同返回，直接解析即可，避免二次请求
        comment_elements = soup.select('.comment')
        for comment_element in comment_elements:
            author_span = comment_element.select_one('.comment-author span[title]')
            author_id = author_span['title'] if author_span else 'Unknown'
            body_element = comment_element.select_one('.comment-body')
            date_element = comment_element.select_one('.comment-meta .meta-data')
            
            if body_element:
                comment_body = await preprocess_html_to_markdown(page, body_element, output_dir, download_images=download_images)
            else:
                comment_body = ''

            comment_data = {
                'author': author_id,
                'body': comment_body,
                'date': date_element.get_text(strip=True) if date_element else 'Unknown Date'
            }
            if comment_data not in comments:
                comments.append(comment_data)
                
        # 检查是否有多页评论 (通过是否存在下一页链接判断)
        next_a = soup.select_one('a.pagination-next-link')
        page_num = 2
        while next_a and page_num <= max_comment_pages:
            next_href = next_a.get('href', '')
            if not next_href:
                break
            comment_url = next_href if next_href.startswith('http') else f"https://support.worldquantbrain.com{next_href}"
            print(f"Navigating to comment page: {comment_url}")
            
            try:
                response = await page.goto(comment_url, wait_until="domcontentloaded")
                if response and response.status == 404:
                    break
                await page.wait_for_selector('.comment-list', timeout=3000, state="visible")
            except Exception:
                break

            comment_html = await page.content()
            sniff_profiles_from_html(comment_html)
            
            comment_soup = BeautifulSoup(comment_html, 'html.parser')
            comment_elements = comment_soup.select('.comment')

            if not comment_elements:
                break
            
            new_comments_found = 0
            for comment_element in comment_elements:
                author_span = comment_element.select_one('.comment-author span[title]')
                author_id = author_span['title'] if author_span else 'Unknown'

                body_element = comment_element.select_one('.comment-body')
                date_element = comment_element.select_one('.comment-meta .meta-data')
                
                if body_element:
                    comment_body = await preprocess_html_to_markdown(page, body_element, output_dir, download_images=download_images)
                else:
                    comment_body = ''

                comment_data = {
                    'author': author_id,
                    'body': comment_body,
                    'date': date_element.get_text(strip=True) if date_element else 'Unknown Date'
                }
                
                if comment_data not in comments:
                    comments.append(comment_data)
                    new_comments_found += 1

            if new_comments_found == 0:
                break
                
            next_a = comment_soup.select_one('a.pagination-next-link')
            page_num += 1

    return {
        "success": True,
        "post": post_data,
        "comments": comments,
        "total_comments": len(comments)
    }

async def fetch_links_from_profile_page(page, user_id: str, adv_id: str) -> tuple[list[str], int, int]:
    """通过顾问的 Zendesk 个人主页获取其发表的所有发帖和回帖链接 (支持 Cursor 分页)"""
    links = []
    seen = set()
    expected_posts = 0
    expected_comments = 0
    
    # 1. 抓取他发表的主帖 (Posts)
    current_url = f"https://support.worldquantbrain.com/hc/zh-cn/profiles/{user_id}-{adv_id}?filter_by=posts&sort_by=recent_user_activity"
    page_num = 1
    while current_url:
        print(f"Navigating to profile posts: {current_url} (Page {page_num})")
        try:
            await page.goto(current_url, wait_until="domcontentloaded")
            try:
                await page.wait_for_selector('.profile-section', timeout=4000)
            except Exception:
                break
                
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Parse expected counts on the very first page load
            if page_num == 1:
                try:
                    for a in soup.find_all('a'):
                        href = a.get('href', '')
                        tab_text = a.get_text(strip=True)
                        if 'filter_by=posts' in href:
                            posts_m = re.search(r'(?:帖子|posts)[（(]\s*(\d+)\s*[）)]', tab_text, re.IGNORECASE)
                            if posts_m:
                                expected_posts = int(posts_m.group(1))
                        elif 'filter_by=comments' in href:
                            comments_m = re.search(r'(?:评论|comments)[（(]\s*(\d+)\s*[）)]', tab_text, re.IGNORECASE)
                            if comments_m:
                                expected_comments = int(comments_m.group(1))
                    print(f"[{adv_id}] 解析到期望数据量 - 帖子: {expected_posts}, 评论: {expected_comments}")
                except Exception as e:
                    print(f"Failed to parse expected counts: {e}")
            
            new_links_found = 0
            for a in soup.select("a"):
                href = a.get("href", "")
                if "/community/posts/" in href or "/articles/" in href:
                    clean_href = href.split('#')[0]
                    full_url = clean_href if clean_href.startswith("http") else f"https://support.worldquantbrain.com{clean_href}"
                    post_id = extract_post_id(full_url)
                    if post_id and post_id not in seen:
                        seen.add(post_id)
                        links.append(full_url)
                        new_links_found += 1
            
            print(f"Page {page_num} posts: found {new_links_found} new links.")
            
            # Find next page url
            next_a = soup.select_one('a.pagination-next-link')
            if next_a and next_a.get('href'):
                next_href = next_a.get('href')
                current_url = next_href if next_href.startswith('http') else f"https://support.worldquantbrain.com{next_href}"
                page_num += 1
            else:
                current_url = None
        except Exception as e:
            print(f"Failed to fetch profile posts: {e}")
            break
            
    # 2. 抓取他发表的评论 (Comments)
    current_url = f"https://support.worldquantbrain.com/hc/zh-cn/profiles/{user_id}-{adv_id}?filter_by=comments&sort_by=recent_user_activity"
    page_num = 1
    while current_url:
        print(f"Navigating to profile comments: {current_url} (Page {page_num})")
        try:
            await page.goto(current_url, wait_until="domcontentloaded")
            try:
                await page.wait_for_selector('.profile-section', timeout=4000)
            except Exception:
                break
                
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            new_links_found = 0
            for a in soup.select("a"):
                href = a.get("href", "")
                if "/community/posts/" in href or "/articles/" in href:
                    clean_href = href.split('#')[0]
                    full_url = clean_href if clean_href.startswith("http") else f"https://support.worldquantbrain.com{clean_href}"
                    post_id = extract_post_id(full_url)
                    if post_id and post_id not in seen:
                        seen.add(post_id)
                        links.append(full_url)
                        new_links_found += 1
                        
            print(f"Page {page_num} comments: found {new_links_found} new links.")
            
            next_a = soup.select_one('a.pagination-next-link')
            if next_a and next_a.get('href'):
                next_href = next_a.get('href')
                current_url = next_href if next_href.startswith('http') else f"https://support.worldquantbrain.com{next_href}"
                page_num += 1
            else:
                current_url = None
        except Exception as e:
            print(f"Failed to fetch profile comments: {e}")
            break
            
    return links, expected_posts, expected_comments


async def fetch_post_with_cache(page, email, password, url, output_dir, prefix="", global_local_posts=None, max_comment_pages: int = 20, download_images: bool = True, force: bool = False) -> tuple[bool, str, list[str], dict | None, list | None, str]:
    """
    带有多级缓存的帖子拉取函数：
    1. 检查目标顾问目录下是否已存在。
    2. 检查全局其他顾问目录下是否存在（若存在则直接复制）。
    3. 检查内存缓存。
    4. 发起网络请求下载，并写入内存缓存与当前顾问目录。
    """
    post_id = extract_post_id(url)
    global_local_posts = global_local_posts or {}
    
    # 1. 检查目标目录与全局缓存是否已存在
    if not force and post_id in global_local_posts:
        source_path = global_local_posts[post_id]
        if source_path.exists():
            # 如果它已经存在于当前顾问目录中
            if source_path.parent == output_dir:
                try:
                    content = source_path.read_text(encoding="utf-8")
                    if "hc/user_images/" not in content:
                        title_match = re.match(r'# (.*)', content)
                        title = title_match.group(1) if title_match else source_path.stem
                        print(f"Skipping download (already exists in target folder): {title} ({source_path.name})")
                        extracted_links = extract_forum_links(content)
                        mock_post = {"author": "Local", "details": {"date": "Local", "votes": "0"}}
                        return True, title, extracted_links, mock_post, [], post_id
                    else:
                        print(f"File {source_path.name} contains un-localized images. Re-downloading to localize images...")
                except Exception:
                    pass
            # 如果它存在于其他顾问的目录中，则复制过来
            else:
                try:
                    content = source_path.read_text(encoding="utf-8")
                    if "hc/user_images/" not in content:
                        print(f"Copying local cache from: {source_path.relative_to(source_path.parent.parent.parent)}")
                        title_match = re.match(r'# (.*)', content)
                        title = title_match.group(1) if title_match else source_path.stem
                        extracted_links = extract_forum_links(content)
                        clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                        dest_path = output_dir / f"{prefix}{clean_title}_{post_id}.md"
                        shutil.copy2(source_path, dest_path)
                        copy_referenced_images(source_path, dest_path)
                        global_local_posts[post_id] = dest_path
                        return True, title, extracted_links, {"author": "Local"}, [], post_id
                    else:
                        print(f"Local cache for post {post_id} contains un-localized images. Will re-fetch from web to localize.")
                except Exception as e:
                    print(f"Failed to copy local cache: {e}")

    # 3. 检查内存缓存
    if not force and post_id in network_cache:
        print(f"Using memory cache for post_id: {post_id}")
        cached_data = network_cache[post_id]
        if cached_data["success"]:
            dest_file = save_post_content_to_file(url, cached_data["title"], cached_data["body"], cached_data["comments"], cached_data["post"], output_dir, prefix)
            
            # Copy images if they exist in global_local_posts and the file exists
            if post_id in global_local_posts:
                src_p = global_local_posts[post_id]
                if src_p.exists():
                    copy_referenced_images(src_p, dest_file)
                
            extracted_links = extract_forum_links(cached_data["body"] + "\n" + "\n".join([c.get("body", "") for c in cached_data["comments"]]))
            return True, cached_data["title"], extracted_links, cached_data["post"], cached_data["comments"], post_id
        else:
            return False, "", [], None, None, post_id

    # 4. 网络拉取
    try:
        post_detail = await read_full_forum_post_custom(page, url, output_dir, include_comments=True, max_comment_pages=max_comment_pages, download_images=download_images)
        if not post_detail.get("success"):
            print(f"Failed to fetch content for URL: {url}")
            network_cache[post_id] = {"success": False}
            return False, "", [], None, None, post_id
        
        post = post_detail.get("post", {})
        comments = post_detail.get("comments", [])
        title = post.get("title", "Unknown Title")
        body = post.get("body", "")
        
        network_cache[post_id] = {
            "success": True,
            "title": title,
            "body": body,
            "comments": comments,
            "post": post
        }
        
        saved_path = save_post_content_to_file(url, title, body, comments, post, output_dir, prefix)
        
        # Update global_local_posts so that subsequent cache hits can find it
        global_local_posts[post_id] = saved_path
        
        content_to_scan = body + "\n" + "\n".join([c.get("body", "") for c in comments])
        extracted_links = extract_forum_links(content_to_scan)
        
        resolved_post_id = extract_post_id(page.url)
        if not resolved_post_id:
            resolved_post_id = post_id
            
        return True, title, extracted_links, post, comments, resolved_post_id
    except Exception as e:
        print(f"Exception extracting post '{url}': {e}")
        network_cache[post_id] = {"success": False}
        return False, "", [], None, None, post_id

async def main():
    email, password = load_credentials()
    client = ForumClient()
    
    # 加载 100 顾问列表
    advisors = load_advisor_list()
    print(f"Loaded {len(advisors)} advisors to process.")
    
def migrate_old_filenames(output_base_dir: Path):
    """
    将旧版没有包含 post_id 的文件名迁移到新版格式：
    如 2024Q4薪资分享.md -> 2024Q4薪资分享_41063717088919.md
    """
    print("\n================== 正在进行旧文件名迁移 ==================")
    migrated_count = 0
    deleted_count = 0
    for root, dirs, files in os.walk(output_base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                name_stem = file_path.stem
                
                # 如果文件名已经是以 _数字 结尾，说明已经是新格式，跳过
                if re.search(r'_\d{5,}$', name_stem):
                    continue
                
                try:
                    content = file_path.read_text(encoding="utf-8")
                    url_match = re.search(r'- \*\*链接\*\*: (https://[^\s\n]+)', content)
                    if url_match:
                        url = url_match.group(1)
                        post_id = extract_post_id(url)
                        if post_id:
                            # 构造新文件名
                            new_name = f"{name_stem}_{post_id}.md"
                            new_path = file_path.parent / new_name
                            
                            if new_path.exists():
                                # 如果新格式已存在，说明是重复的旧文件，直接删除旧的
                                file_path.unlink()
                                deleted_count += 1
                            else:
                                file_path.rename(new_path)
                                migrated_count += 1
                except Exception as e:
                    print(f"Error migrating file {file_path}: {e}")
                    
    print(f"文件名迁移完成：已迁移 {migrated_count} 个文件，清理 {deleted_count} 个重复旧文件。\n")

def count_local_activity(adv_dir: Path, adv_id: str) -> tuple[int, int]:
    """
    计算本地已保存的顾问 activity 数量：
    1. 属于该顾问的主帖数 (文件名不含 [Commented] 和 [L2])
    2. 该顾问在所有本地文件中的评论数总和
    """
    local_posts = 0
    local_comments = 0
    for p_file in adv_dir.glob("*.md"):
        if p_file.name.startswith("[L2]"):
            continue
        try:
            content = p_file.read_text(encoding="utf-8")
            
            # 判断是否为主贴作者
            if not p_file.name.startswith("[Commented]"):
                local_posts += 1
                
            # 计算该顾问在当前文件中的评论数
            # 匹配格式如：### 评论 #1 (作者: ZS59763, 时间: ...)
            comment_pattern = rf'### 评论 #\d+ \(作者:\s*{adv_id}\b'
            comments_found = len(re.findall(comment_pattern, content))
            local_comments += comments_found
        except Exception:
            pass
    return local_posts, local_comments

async def main():
    email, password = load_credentials()
    client = ForumClient()
    
    # 加载 100 顾问列表
    advisors = load_advisor_list()
    print(f"Loaded {len(advisors)} advisors to process.")
    
    # 优先抓取 ZS59763
    if "ZS59763" in advisors:
        advisors.remove("ZS59763")
        target_advisors = ["ZS59763"] + advisors
    else:
        target_advisors = advisors
    
    output_base_dir = Path("reference/top100Rank-2026Q2/user_activity")
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    # 执行旧文件名迁移，防止重名覆盖以及校验失败
    migrate_old_filenames(output_base_dir)
    
    # 全局本地已下载文件扫描，用于秒级断点续传
    global_local_posts = scan_all_local_posts(output_base_dir)
    print(f"Scanned {len(global_local_posts)} posts already present in local folders.")
    
    async with async_playwright() as p:
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        
        # 必须先触发 SSO 登录流程，使浏览器在 support.worldquantbrain.com 域名下也处于登录状态
        # 否则匿名状态下访问个人主页会看到“发贴(0)”或“回复(0)”的空页面，导致无法抓取
        signin_url = "https://support.worldquantbrain.com/hc/zh-cn/signin"
        print(f"Triggering SSO Sign-in by navigating to {signin_url}...")
        try:
            await page.goto(signin_url, wait_until="networkidle")
            print("SSO login succeeded. Current URL:", page.url)
        except Exception as e:
            print(f"SSO login navigation timed out or failed: {e}, continuing...")
        
        # 0. 并发解析缺失的 Zendesk ID (使用信号量进行并发控制)
        concurrency_sem = asyncio.Semaphore(5)
        m = load_advisor_zendesk_map()
        missing_advisors = [adv for adv in target_advisors if adv not in m]
        if missing_advisors:
            print(f"\n================== 正在并发解析 {len(missing_advisors)} 个缺失的 Zendesk ID ==================")
            
            async def resolve_advisor_id(adv_id):
                current_map = load_advisor_zendesk_map()
                if adv_id in current_map:
                    return True
                    
                async with concurrency_sem:
                    item_page = await client._new_page(context)
                    try:
                        print(f"正在并发搜索顾问: {adv_id} 的 Zendesk ID...")
                        search_links = await search_forum_posts_custom(item_page, adv_id, max_results=5)
                        
                        # 检查在加载搜索页时是否有 sniff 成功
                        current_map = load_advisor_zendesk_map()
                        if adv_id in current_map:
                            return True
                            
                        if not search_links:
                            return False
                            
                        # 遍历前 3 个帖子以嗅探 ID
                        adv_dir = output_base_dir / adv_id
                        adv_dir.mkdir(parents=True, exist_ok=True)
                        for s_url in search_links[:3]:
                            await read_full_forum_post_custom(
                                item_page, s_url, adv_dir, include_comments=True, max_comment_pages=1, download_images=False
                            )
                            current_map = load_advisor_zendesk_map()
                            if adv_id in current_map:
                                return True
                    except Exception as e:
                        print(f"Error resolving ID for {adv_id}: {e}")
                    finally:
                        await item_page.close()
                return False
                
            await asyncio.gather(*(resolve_advisor_id(adv) for adv in missing_advisors))
            print("Zendesk ID 并发解析完成！当前映射表已更新。\n")
        
        for adv_id in target_advisors:
            print(f"\n>>>>>>> 正在检索顾问: {adv_id} <<<<<<<")
            adv_dir = output_base_dir / adv_id
            adv_dir.mkdir(parents=True, exist_ok=True)
            
            results = []
            expected_posts = 0
            expected_comments = 0
            
            # 1. 从已有的 map 中获取 User ID 爬取个人主页
            m = load_advisor_zendesk_map()
            if adv_id in m:
                user_id = m[adv_id]
                print(f"Found Zendesk User ID: {user_id} for {adv_id}. Fetching directly from personal profile page...")
                profile_links, expected_posts, expected_comments = await fetch_links_from_profile_page(page, user_id, adv_id)
                results.extend(profile_links)
                print(f"Found {len(profile_links)} links from profile page.")
            else:
                # 兜底：如果实在没搜到 ID，则通过搜索关键字兜底
                print(f"Warning: Could not resolve Zendesk ID for {adv_id}. Falling back to search results...")
                try:
                    search_links = await search_forum_posts_custom(page, adv_id, max_results=30)
                    results.extend(search_links)
                except Exception as e:
                    print(f"Search fallback failed for {adv_id}: {e}")
                
            # 去重
            unique_results = []
            seen_ids = set()
            for r in results:
                p_id = extract_post_id(r)
                if p_id and p_id not in seen_ids:
                    seen_ids.add(p_id)
                    unique_results.append(r)
                    
            print(f"Total unique links to process for {adv_id}: {len(unique_results)}")
            
            level2_links_queue = []
            l1_success_count = 0
            
            # 并发控制信号量，限制最大同时打开5个页面 (即相当于5线程)
            concurrency_sem = asyncio.Semaphore(5)
            
            # Level 1: 并发下载任务定义
            async def process_l1_item(url, idx):
                post_id = extract_post_id(url)
                
                # 1. 检查本地是否已存在
                target_exists = False
                for p_file in adv_dir.glob("*.md"):
                    if post_id in p_file.name:
                        target_exists = True
                        try:
                            file_content = p_file.read_text(encoding="utf-8")
                            l2_links = extract_forum_links(file_content)
                            return True, (p_file.name, p_file.name, {"author": "Local"}, []), l2_links, "local"
                        except Exception:
                            pass
                        break
                
                if target_exists:
                    return False, None, [], "skipped"
                
                # 2. 从缓存或网络下载 (使用信号量进行流量控制)
                async with concurrency_sem:
                    item_page = await client._new_page(context)
                    try:
                        print(f"[Level 1] Concurrently fetching {idx}/{len(unique_results)}: {url}")
                        success, title, l2_links, post_data, comments, resolved_post_id = await fetch_post_with_cache(
                            item_page, email, password, url, adv_dir, prefix="", global_local_posts=global_local_posts
                        )
                        if success:
                            return True, (title, resolved_post_id, post_data, comments), l2_links, "downloaded"
                        return False, None, [], "failed"
                    except Exception as e:
                        print(f"Error fetching {url}: {e}")
                        return False, None, [], "error"
                    finally:
                        await item_page.close()

            # 并发执行 Level 1
            tasks_l1 = [process_l1_item(url, idx) for idx, url in enumerate(unique_results, 1)]
            l1_results = await asyncio.gather(*tasks_l1)
            
            # 下载完毕后，回到单线程环境下进行重命名、筛选以及主贴身份校验 (线程安全)
            level2_links_queue = []
            l1_success_count = 0
            for idx, (success, payload, l2_links, status) in enumerate(l1_results, 1):
                url = unique_results[idx - 1]
                post_id = extract_post_id(url)
                if not success:
                    continue
                    
                if status == "local":
                    level2_links_queue.extend(l2_links)
                    l1_success_count += 1
                    continue
                    
                title, resolved_post_id, post_data, comments = payload
                is_author = False
                is_commenter = False
                
                # 寻找磁盘上已下载的以 _{resolved_post_id}.md 结尾的所有文件
                matched_files = list(adv_dir.glob(f"*_{resolved_post_id}.md"))
                file_content = ""
                if matched_files:
                    for f in matched_files:
                        try:
                            file_content = f.read_text(encoding="utf-8")
                            break
                        except Exception:
                            pass
                            
                if file_content:
                    try:
                        author_match = re.search(r'- \*\*作者\*\*: ([^\n]+)', file_content)
                        if author_match and author_match.group(1).strip() == adv_id:
                            is_author = True
                                
                        comment_author_pattern = rf'### 评论 #\d+ \(作者:\s*{adv_id}\b'
                        if re.search(comment_author_pattern, file_content):
                            is_commenter = True
                    except Exception as e:
                        print(f"Error checking author identity: {e}")
                else:
                    if post_data and post_data.get("author") == adv_id:
                        is_author = True
                    if comments:
                        for c in comments:
                            if c.get("author") == adv_id:
                                is_commenter = True
                                break
                                
                if is_author or is_commenter:
                    l1_success_count += 1
                    level2_links_queue.extend(l2_links)
                    
                    prefix = "" if is_author else "[Commented] "
                    clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                    target_file = adv_dir / f"{prefix}{clean_title}_{resolved_post_id}.md"
                    
                    # 合并与去重磁盘文件，确保仅保留 target_file
                    target_exists = target_file.exists()
                    for f in matched_files:
                        if f.resolve() == target_file.resolve():
                            continue
                        if target_exists:
                            try:
                                f.unlink()
                            except Exception:
                                pass
                        else:
                            try:
                                f.rename(target_file)
                                target_exists = True
                            except Exception as e:
                                print(f"Rename failed: {e}")
                                
                    if not target_file.exists() and post_data:
                        save_post_content_to_file(url, title, post_data.get('body', ''), comments, post_data, adv_dir, prefix)
                        
                    print(f"Match: Post belongs to advisor {adv_id} (IsAuthor: {is_author}, IsCommenter: {is_commenter})")
                else:
                    # 丢弃非本顾问活动帖子
                    for f in matched_files:
                        try:
                            f.unlink()
                        except Exception:
                            pass
                    print(f"Filtered: Post does not belong to {adv_id} (just mentioned). Deleted from advisor folder.")
            
            print(f"[Level 1 Done] Concurrently processed Level 1. Successfully matched {l1_success_count} valid posts for {adv_id}.")
            
            # ====== 数据校验与自愈逻辑 (Verification & Self-healing) ======
            if expected_posts > 0 or expected_comments > 0:
                local_posts, local_comments = count_local_activity(adv_dir, adv_id)
                print(f"[首次校验] 本地帖子数: {local_posts} (期望: {expected_posts}), 本地评论数: {local_comments} (期望: {expected_comments})")
                
                # 1. 补齐缺失的主帖 (并发拉取)
                if local_posts < expected_posts:
                    print(f"[自愈触发] 主帖数不足，开始强制补拉缺失主帖...")
                    
                    missing_urls = []
                    for url in results:
                        p_id = extract_post_id(url)
                        found = False
                        for f in adv_dir.glob("*.md"):
                            if f"_{p_id}.md" in f.name and not f.name.startswith("[Commented]") and not f.name.startswith("[L2]"):
                                found = True
                                break
                        if not found:
                            missing_urls.append(url)
                            
                    async def fetch_missing_post(url):
                        async with concurrency_sem:
                            item_page = await client._new_page(context)
                            try:
                                print(f"强制重新拉取可能的主帖: {url} ...")
                                await fetch_post_with_cache(
                                    item_page, email, password, url, adv_dir, prefix="", global_local_posts=global_local_posts, force=True
                                )
                            except Exception as e:
                                print(f"Error self-healing missing post {url}: {e}")
                            finally:
                                await item_page.close()
                                
                    if missing_urls:
                        await asyncio.gather(*(fetch_missing_post(url) for url in missing_urls))
                        
                    # 重新评估 author 状态并改名 (主帖)
                    for f in adv_dir.glob("*.md"):
                        if not f.name.startswith("[L2]") and "_" in f.name:
                            try:
                                content = f.read_text(encoding="utf-8")
                                author_match = re.search(r'- \*\*作者\*\*: ([^\n]+)', content)
                                if author_match and author_match.group(1).strip() == adv_id:
                                    if f.name.startswith("[Commented]"):
                                        new_name = f.name.replace("[Commented] ", "")
                                        target_p = f.parent / new_name
                                        if target_p.exists():
                                            f.unlink()
                                        else:
                                            f.rename(target_p)
                            except Exception:
                                pass
                                
                    local_posts, local_comments = count_local_activity(adv_dir, adv_id)
                    
                # 2. 补齐缺失的评论 (并发拉取)
                if local_comments < expected_comments:
                    print(f"[自愈触发] 评论数不足，开始强制拉取/更新所有相关帖子的评论分页...")
                    urls_to_refresh = []
                    for f in adv_dir.glob("*.md"):
                        if not f.name.startswith("[L2]"):
                            try:
                                content = f.read_text(encoding="utf-8")
                                url_match = re.search(r'- \*\*链接\*\*: (https://[^\s\n]+)', content)
                                if url_match:
                                    urls_to_refresh.append(url_match.group(1))
                            except Exception:
                                pass
                                
                    async def refresh_comment_post(url):
                        async with concurrency_sem:
                            item_page = await client._new_page(context)
                            try:
                                print(f"强制更新帖子评论: {url} ...")
                                await fetch_post_with_cache(
                                    item_page, email, password, url, adv_dir, prefix="", global_local_posts=global_local_posts, force=True
                                )
                            except Exception as e:
                                print(f"Error self-healing comments on {url}: {e}")
                            finally:
                                await item_page.close()
                                
                    if urls_to_refresh:
                        await asyncio.gather(*(refresh_comment_post(url) for url in urls_to_refresh))
                        
                    # 重新判定是否属于 is_author / is_commenter (顺序重命名)
                    for url in urls_to_refresh:
                        p_id = extract_post_id(url)
                        matched_files = list(adv_dir.glob(f"*_{p_id}.md"))
                        if not matched_files:
                            continue
                            
                        content = ""
                        for f in matched_files:
                            try:
                                content = f.read_text(encoding="utf-8")
                                break
                            except Exception:
                                pass
                                
                        if not content:
                            continue
                            
                        try:
                            is_author = False
                            is_commenter = False
                            author_match = re.search(r'- \*\*作者\*\*: ([^\n]+)', content)
                            if author_match and author_match.group(1).strip() == adv_id:
                                is_author = True
                            comment_author_pattern = rf'### 评论 #\d+ \(作者:\s*{adv_id}\b'
                            if re.search(comment_author_pattern, content):
                                is_commenter = True
                                
                            if is_author or is_commenter:
                                prefix = "" if is_author else "[Commented] "
                                title_match = re.match(r'# (.*)', content)
                                title = title_match.group(1) if title_match else matched_files[0].stem
                                clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                                
                                target_name = f"{prefix}{clean_title}_{p_id}.md"
                                target_path = adv_dir / target_name
                                
                                target_exists = target_path.exists()
                                for f in matched_files:
                                    if f.resolve() == target_path.resolve():
                                        continue
                                    if target_exists:
                                        try:
                                            f.unlink()
                                        except Exception:
                                            pass
                                    else:
                                        try:
                                            f.rename(target_path)
                                            target_exists = True
                                        except Exception as e:
                                            print(f"Rename in heal failed: {e}")
                            else:
                                for f in matched_files:
                                    try:
                                        f.unlink()
                                    except Exception:
                                        pass
                        except Exception as e:
                            print(f"Error in self-healing check for post {p_id}: {e}")
                                
                    local_posts, local_comments = count_local_activity(adv_dir, adv_id)
                    print(f"[最终校验] 本地帖子数: {local_posts} (期望: {expected_posts}), 本地评论数: {local_comments} (期望: {expected_comments})")
            
            # Level 2: 抓取二级链接 (并发拉取)
            level2_links_queue = list(set(level2_links_queue))
            print(f"Found {len(level2_links_queue)} unique potential Level 2 links for {adv_id}.")
            
            async def process_l2_item(l2_url, l2_idx):
                l2_id = extract_post_id(l2_url)
                l1_exists = False
                for p_file in adv_dir.glob("*.md"):
                    if l2_id in p_file.name and "[L2]" not in p_file.name:
                        l1_exists = True
                        break
                if l1_exists:
                    return False
                    
                async with concurrency_sem:
                    item_page = await client._new_page(context)
                    try:
                        print(f"[Level 2] Concurrently fetching {l2_idx}/{len(level2_links_queue)}: {l2_url}...")
                        success, _, _, _, _, _ = await fetch_post_with_cache(
                            item_page, email, password, l2_url, adv_dir, prefix="[L2] ", global_local_posts=global_local_posts
                        )
                        return success
                    except Exception as e:
                        print(f"Error fetching Level 2 post {l2_url}: {e}")
                        return False
                    finally:
                        await item_page.close()
            
            tasks_l2 = [process_l2_item(l2_url, l2_idx) for l2_idx, l2_url in enumerate(level2_links_queue, 1)]
            l2_results = await asyncio.gather(*tasks_l2)
            l2_success_count = sum(1 for r in l2_results if r)
            print(f"[Level 2 Done] Concurrently fetched {l2_success_count} Level 2 posts for {adv_id}.")
            
        await browser.close()
        
    # 3. 建立本地文章引用关联
    build_local_relationships(output_base_dir)
    print("\n================== 任务全部完成！ ==================")

def build_local_relationships(output_base_dir: Path):
    """扫描所有已下载的帖子，将内嵌的 WQ 论坛链接替换为指向本地文件的相对路径，建立引用关联"""
    print("\n================== 阶段 3: 建立本地帖子引用关联 ==================")
    
    post_id_to_paths = {}
    
    # 收集已下载的所有 .md 文件
    for root, dirs, files in os.walk(output_base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding="utf-8")
                    url_match = re.search(r'- \*\*链接\*\*: (https://[^\s\n]+)', content)
                    if url_match:
                        url = url_match.group(1)
                        post_id = extract_post_id(url)
                        if post_id:
                            if post_id not in post_id_to_paths:
                                post_id_to_paths[post_id] = []
                            post_id_to_paths[post_id].append(file_path)
                except Exception as e:
                    print(f"Error reading file {file_path.name} for link: {e}")
                    
    print(f"Found {len(post_id_to_paths)} unique local posts indexed for reference links.")
    
    # 遍历更新文件内链
    updated_files = 0
    for root, dirs, files in os.walk(output_base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding="utf-8")
                    original_content = content
                    
                    pattern = r'https://support\.worldquantbrain\.com/hc/[a-zA-Z-]+/community/posts/(\d+)(?:-[a-zA-Z0-9%-]+)?'
                    rel_pattern = r'/hc/[a-zA-Z-]+/community/posts/(\d+)(?:-[a-zA-Z0-9%-]+)?'
                    
                    def replacer(match):
                        # Avoid replacing the main link line
                        start_idx = match.start()
                        context_before = content[max(0, start_idx - 25):start_idx]
                        if "- **链接**:" in context_before:
                            return match.group(0)

                        post_id = match.group(1)
                        if post_id in post_id_to_paths:
                            paths = post_id_to_paths[post_id]
                            dest_path = None
                            for p in paths:
                                if p.parent == file_path.parent:
                                    dest_path = p
                                    break
                            if not dest_path:
                                non_l2_paths = [p for p in paths if "[L2]" not in p.name]
                                dest_path = non_l2_paths[0] if non_l2_paths else paths[0]
                            
                            rel_path = os.path.relpath(dest_path, start=file_path.parent)
                            rel_path = rel_path.replace('\\', '/')
                            return rel_path
                        return match.group(0)
                        
                    content = re.sub(pattern, replacer, content)
                    content = re.sub(rel_pattern, replacer, content)
                    
                    if content != original_content:
                        file_path.write_text(content, encoding="utf-8")
                        print(f"Linked reference updated for: {file_path.relative_to(output_base_dir)}")
                        updated_files += 1
                except Exception as e:
                    print(f"Error building links for file {file_path.name}: {e}")
                    
    print(f"Done! Successfully updated {updated_files} files with local relationships.")

if __name__ == "__main__":
    asyncio.run(main())
