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
    match = re.search(r'/community/posts/(\d+)', url)
    if match:
        return match.group(1)
    match = re.search(r'/articles/(\d+)', url)
    if match:
        return match.group(1)
    return url

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
    clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
    filename = output_dir / f"{prefix}{clean_title}.md"
    
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
                
        # 检查是否有多页评论 (在分页导航中是否存在 page=2 链接)
        has_more_pages = any('page=2' in a.get('href', '') for a in soup.select('.pagination a'))
        
        if has_more_pages and max_comment_pages > 1:
            page_num = 2
            while page_num <= max_comment_pages:
                comment_url = f"{base_url}?page={page_num}#comments"
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
                    
                # 检查是否还有下一页，避免不必要的访问
                has_next = any(f'page={page_num + 1}' in a.get('href', '') for a in comment_soup.select('.pagination a'))
                if not has_next:
                    break
                    
                page_num += 1

    return {
        "success": True,
        "post": post_data,
        "comments": comments,
        "total_comments": len(comments)
    }

async def fetch_links_from_profile_page(page, user_id: str, adv_id: str) -> list[str]:
    """通过顾问的 Zendesk 个人主页获取其发表的所有发帖和回帖链接 (支持 Cursor 分页)"""
    links = []
    seen = set()
    
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
            
    return links


async def fetch_post_with_cache(page, email, password, url, output_dir, prefix="", global_local_posts=None, max_comment_pages: int = 20, download_images: bool = True) -> tuple[bool, str, list[str], dict | None, list | None]:
    """
    带有多级缓存的帖子拉取函数：
    1. 检查目标顾问目录下是否已存在。
    2. 检查全局其他顾问目录下是否存在（若存在则直接复制）。
    3. 检查内存缓存。
    4. 发起网络请求下载，并写入内存缓存与当前顾问目录。
    """
    post_id = extract_post_id(url)
    global_local_posts = global_local_posts or {}
    
    # 1. 检查目标目录是否已存在
    for p in output_dir.glob("*.md"):
        try:
            content = p.read_text(encoding="utf-8")
            if url in content or (post_id and post_id in content):
                # 检查是否存在未本地化的图片链接
                if "hc/user_images/" in content:
                    print(f"File {p.name} contains un-localized images. Re-downloading to localize images...")
                    break
                
                title_match = re.match(r'# (.*)', content)
                title = title_match.group(1) if title_match else p.stem
                print(f"Skipping download (already exists in target folder): {title} ({p.name})")
                extracted_links = extract_forum_links(content)
                mock_post = {"author": "Local", "details": {"date": "Local", "votes": "0"}}
                return True, title, extracted_links, mock_post, []
        except Exception:
            pass

    # 2. 检查全局本地已下载映射
    if post_id in global_local_posts:
        source_path = global_local_posts[post_id]
        if source_path.exists():
            try:
                content = source_path.read_text(encoding="utf-8")
                # 仅在源缓存文件不含有未本地化图片时，才直接拷贝缓存
                if "hc/user_images/" not in content:
                    print(f"Copying local cache from: {source_path.relative_to(source_path.parent.parent.parent)}")
                    title_match = re.match(r'# (.*)', content)
                    title = title_match.group(1) if title_match else source_path.stem
                    
                    extracted_links = extract_forum_links(content)
                    
                    clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                    dest_path = output_dir / f"{prefix}{clean_title}.md"
                    shutil.copy2(source_path, dest_path)
                    
                    # Copy images referenced in the markdown
                    copy_referenced_images(source_path, dest_path)
                    
                    return True, title, extracted_links, {"author": "Local"}, []
                else:
                    print(f"Local cache for post {post_id} contains un-localized images. Will re-fetch from web to localize.")
            except Exception as e:
                print(f"Failed to copy local cache: {e}")

    # 3. 检查内存缓存
    if post_id in network_cache:
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
            return True, cached_data["title"], extracted_links, cached_data["post"], cached_data["comments"]
        else:
            return False, "", [], None, None

    # 4. 网络拉取
    try:
        post_detail = await read_full_forum_post_custom(page, url, output_dir, include_comments=True, max_comment_pages=max_comment_pages, download_images=download_images)
        if not post_detail.get("success"):
            print(f"Failed to fetch content for URL: {url}")
            network_cache[post_id] = {"success": False}
            return False, "", [], None, None
        
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
        
        return True, title, extracted_links, post, comments
    except Exception as e:
        print(f"Exception extracting post '{url}': {e}")
        network_cache[post_id] = {"success": False}
        return False, "", [], None, None

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
    
    # 全局本地已下载文件扫描，用于秒级断点续传
    global_local_posts = scan_all_local_posts(output_base_dir)
    print(f"Scanned {len(global_local_posts)} posts already present in local folders.")
    
    async with async_playwright() as p:
        browser, context = await client._get_browser_context(p, email, password)
        page = await client._new_page(context)
        
        for adv_id in target_advisors:
            print(f"\n>>>>>>> 正在检索顾问: {adv_id} <<<<<<<")
            adv_dir = output_base_dir / adv_id
            adv_dir.mkdir(parents=True, exist_ok=True)
            
            results = []
            
            # 1. 尝试从本地已累积的 zendesk 映射文件中查找，实现直爬个人主页
            m = load_advisor_zendesk_map()
            has_profile = False
            if adv_id in m:
                user_id = m[adv_id]
                print(f"Found Zendesk User ID: {user_id} for {adv_id}. Fetching directly from personal profile page...")
                profile_links = await fetch_links_from_profile_page(page, user_id, adv_id)
                results.extend(profile_links)
                print(f"Found {len(profile_links)} links from profile page.")
                has_profile = True
            
            # 2. 如果没有在映射表中，则使用关键字全局搜索来寻找该顾问的个人主页 ID
            if not has_profile:
                search_query = adv_id
                print(f"Searching forum for keyword: '{search_query}'...")
                try:
                    search_links = await search_forum_posts_custom(page, search_query, max_results=30)
                    print(f"Found {len(search_links)} search results for {adv_id}.")
                    
                    # 遍历搜索结果，直到嗅探到该顾问的 Zendesk ID
                    for s_url in search_links:
                        # 仅加载第一页以嗅探 ID，用 temp_ 前缀写入以避免冲突，并将 max_comment_pages 设为 1
                        success, title, _, _, _ = await fetch_post_with_cache(
                            page, email, password, s_url, adv_dir, prefix="temp_", global_local_posts=global_local_posts, max_comment_pages=1, download_images=False
                        )
                        # 清理临时文件
                        if success:
                            clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                            for f_temp in [adv_dir / f"temp_{clean_title}.md", adv_dir / f"[Commented] temp_{clean_title}.md"]:
                                if f_temp.exists():
                                    f_temp.unlink()
                                
                        # 检查是否成功嗅探到了 ID
                        m = load_advisor_zendesk_map()
                        if adv_id in m:
                            user_id = m[adv_id]
                            print(f"[成功激活] 嗅探到 {adv_id} 的 Zendesk ID: {user_id}。立即切换到个人主页抓取！")
                            profile_links = await fetch_links_from_profile_page(page, user_id, adv_id)
                            results.extend(profile_links)
                            has_profile = True
                            break
                            
                    # 如果仍未嗅探到 ID，则使用原有的搜索结果兜底
                    if not has_profile:
                        print(f"Warning: Could not sniff Zendesk ID for {adv_id}. Using search results as fallback.")
                        results.extend(search_links)
                except Exception as e:
                    print(f"Search failed for {adv_id}: {e}")
                
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
            
            # Level 1: 拉取并根据作者过滤
            for idx, url in enumerate(unique_results, 1):
                post_id = extract_post_id(url)
                print(f"[Level 1] Checking result {idx}/{len(unique_results)}: {url}")
                
                target_exists = False
                for p_file in adv_dir.glob("*.md"):
                    if post_id in p_file.name:
                        target_exists = True
                        try:
                            file_content = p_file.read_text(encoding="utf-8")
                            l2_links = extract_forum_links(file_content)
                            level2_links_queue.extend(l2_links)
                            l1_success_count += 1
                        except Exception:
                            pass
                        break
                
                if target_exists:
                    print(f"Already processed locally for advisor {adv_id}. Skipping.")
                    continue
                
                # 调用带缓存的拉取函数 (传入复用的 page 避免反复初始化浏览器)
                success, title, l2_links, post_data, comments = await fetch_post_with_cache(
                    page, email, password, url, adv_dir, prefix="", global_local_posts=global_local_posts
                )
                
                if success:
                    is_author = False
                    is_commenter = False
                    
                    clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                    written_file = adv_dir / f"{clean_title}.md"
                    
                    if written_file.exists():
                        try:
                            file_content = written_file.read_text(encoding="utf-8")
                            author_match = re.search(r'- \*\*作者\*\*: ([^\n]+)', file_content)
                            if author_match:
                                author_name = author_match.group(1).strip()
                                if author_name == adv_id:
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
                                    
                    # 校验：是否是该顾问本人的帖子或发言？
                    if is_author or is_commenter:
                        l1_success_count += 1
                        level2_links_queue.extend(l2_links)
                        
                        prefix = "" if is_author else "[Commented] "
                        current_file = adv_dir / f"{clean_title}.md"
                        target_file = adv_dir / f"{prefix}{clean_title}.md"
                        
                        if current_file.exists() and prefix != "":
                            if target_file.exists():
                                current_file.unlink()
                            else:
                                current_file.rename(target_file)
                        print(f"Match: Post belongs to advisor {adv_id} (IsAuthor: {is_author}, IsCommenter: {is_commenter})")
                    else:
                        # 丢弃非本顾问活动帖子
                        clean_title = "".join(c for c in title if c.isalnum() or c in " -_[]【】").strip()
                        for f_del in [adv_dir / f"{clean_title}.md", adv_dir / f"[Commented] {clean_title}.md"]:
                            if f_del.exists():
                                f_del.unlink()
                        print(f"Filtered: Post does not belong to {adv_id} (just mentioned). Deleted from advisor folder.")
            
            print(f"[Level 1 Done] Successfully fetched {l1_success_count} valid posts for {adv_id}.")
            
            # Level 2: 抓取二级链接
            level2_links_queue = list(set(level2_links_queue))
            print(f"Found {len(level2_links_queue)} unique potential Level 2 links for {adv_id}.")
            
            l2_success_count = 0
            for idx, l2_url in enumerate(level2_links_queue, 1):
                l2_id = extract_post_id(l2_url)
                l1_exists = False
                for p_file in adv_dir.glob("*.md"):
                    if l2_id in p_file.name and "[L2]" not in p_file.name:
                        l1_exists = True
                        break
                if l1_exists:
                    continue
                    
                print(f"[Level 2] Fetching {idx}/{len(level2_links_queue)}: {l2_url}...")
                success, _, _, _, _ = await fetch_post_with_cache(
                    page, email, password, l2_url, adv_dir, prefix="[L2] ", global_local_posts=global_local_posts
                )
                if success:
                    l2_success_count += 1
            print(f"[Level 2 Done] Successfully fetched {l2_success_count} Level 2 posts for {adv_id}.")
            
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
