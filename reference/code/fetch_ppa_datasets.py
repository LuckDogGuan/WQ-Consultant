import os
import re
import yaml
import requests
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# 载入配置
config_path = os.path.join(BASE_DIR, 'config.yaml')
if not os.path.exists(config_path):
    raise FileNotFoundError("config.yaml not found. Please create config.yaml in the same directory.")

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

def login():
    s = requests.Session()
    s.auth = (config['username'], config['password'])
    response = s.post(f"{config['api_base_url']}/authentication")
    print("登录状态:", response.status_code)
    if response.status_code != 201:
        raise RuntimeError(f"Login failed: status code {response.status_code}")
    return s

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=10, max=60),
    retry=retry_if_exception_type(requests.exceptions.RequestException)
)
def get_theme_datasets(s, region, delay, universe, limit=50, offset=0):
    url = (
        f"{config['api_base_url']}/data-sets"
        f"?delay={delay}&instrumentType=EQUITY&limit={limit}&offset={offset}"
        f"&region={region}&theme=true&universe={universe}"
    )
    headers = {
        'Accept': 'application/json',
        'Referer': (
            f"{config['platform_url']}/data/data-sets"
            f"?delay={delay}&instrumentType=EQUITY&limit={limit}&offset={offset}"
            f"&region={region}&theme=true&universe={universe}"
        ),
    }
    response = s.get(url, headers=headers, timeout=180)
    response.raise_for_status()
    return response.json()

def fetch_all(s, region, delay, universe):
    all_results = []
    offset = 0
    limit = 50
    while True:
        data = get_theme_datasets(s, region, delay, universe, limit=limit, offset=offset)
        results = data.get('results', [])
        total = data.get('count', 0)
        all_results.extend(results)
        print(f"已拉取 {len(all_results)}/{total}")
        if len(all_results) >= total or not results:
            break
        offset += limit
    return all_results

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=10, max=60),
    retry=retry_if_exception_type(requests.exceptions.RequestException)
)
def get_datafields_page(s, dataset_id, region, delay, universe, limit=50, offset=0):
    url = (
        f"{config['api_base_url']}/data-fields"
        f"?dataset.id={dataset_id}&instrumentType=EQUITY"
        f"&region={region}&delay={delay}&universe={universe}"
        f"&limit={limit}&offset={offset}"
    )
    response = s.get(url, timeout=180)
    response.raise_for_status()
    return response.json()

def fetch_dataset_fields(s, dataset_id, region, delay, universe):
    all_fields = []
    offset = 0
    limit = 50
    while True:
        data = get_datafields_page(s, dataset_id, region, delay, universe, limit=limit, offset=offset)
        results = data.get('results', [])
        total = data.get('count', 0)
        all_fields.extend(results)
        if len(all_fields) >= total or not results:
            break
        offset += limit
    return all_fields

def safe_filename(name):
    return re.sub(r'[\\/:*?"<>|]+', '_', name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch PPA theme datasets and fields from WorldQuant Brain")
    parser.add_argument("--region", type=str, default="USA", help="Region (default: USA)")
    parser.add_argument("--delay", type=int, default=1, help="Delay (default: 1)")
    parser.add_argument("--universe", type=str, default="TOP3000", help="Universe (default: TOP3000)")
    args = parser.parse_args()

    s = login()
    region = args.region
    delay = args.delay
    universe = args.universe
    results = fetch_all(s, region, delay, universe)
    rows = []
    for item in results:
        category = item.get('category') or {}
        subcategory = item.get('subcategory') or {}
        rows.append({
            'id': item.get('id'),
            'name': item.get('name'),
            'description': item.get('description'),
            'category.id': category.get('id'),
            'category.name': category.get('name'),
            'subcategory.id': subcategory.get('id'),
            'subcategory.name': subcategory.get('name'),
            'region': item.get('region'),
            'delay': item.get('delay'),
            'universe': item.get('universe'),
            'coverage': item.get('coverage'),
            'valueScore': item.get('valueScore'),
            'userCount': item.get('userCount'),
            'alphaCount': item.get('alphaCount'),
            'fieldCount': item.get('fieldCount'),
            'themed': item.get('themed'),
            'pyramidMultiplier': item.get('pyramidMultiplier'),
        })
    df = pd.DataFrame(rows)
    out = f"theme_datasets_{region}_{delay}_{universe}.csv"
    df.to_csv(out, index=False, encoding='utf-8-sig')
    print(f"已保存 {len(df)} 个数据集到 {out}")
    fields_dir = f"theme_fields_{region}_{delay}_{universe}"
    os.makedirs(fields_dir, exist_ok=True)
    all_fields_rows = []
    # 这里我们只处理前几个，用于验证；如果想完全拉取也可以，但为了快速验证且防频限，我们做完整的遍历或者前两个。
    # 既然用户需要验证，我们为了让验证快速完成且成功，可以先遍历全部，或者限制拉取的条数。
    # 我们先完整遍历，如果数据集很多，我们可以打印进度。
    for i, item in enumerate(results, 1):
        ds_id = item.get('id')
        ds_name = item.get('name')
        print(f"[{i}/{len(results)}] 拉取字段: {ds_id} - {ds_name}")
        try:
            fields = fetch_dataset_fields(s, ds_id, region, delay, universe)
        except Exception as e:
            print(f"  失败: {e}")
            continue
        ds_rows = []
        for f in fields:
            cat = f.get('category') or {}
            sub = f.get('subcategory') or {}
            ds = f.get('dataset') or {}
            ds_rows.append({
                'dataset.id': ds.get('id') or ds_id,
                'dataset.name': ds.get('name') or ds_name,
                'id': f.get('id'),
                'description': f.get('description'),
                'type': f.get('type'),
                'region': f.get('region'),
                'delay': f.get('delay'),
                'universe': f.get('universe'),
                'category.id': cat.get('id'),
                'category.name': cat.get('name'),
                'subcategory.id': sub.get('id'),
                'subcategory.name': sub.get('name'),
                'coverage': f.get('coverage'),
                'userCount': f.get('userCount'),
                'alphaCount': f.get('alphaCount'),
                'themed': f.get('themed'),
                'pyramidMultiplier': f.get('pyramidMultiplier'),
            })
        if ds_rows:
            df_ds = pd.DataFrame(ds_rows)
            ds_file = os.path.join(fields_dir, f"{safe_filename(ds_id)}.csv")
            df_ds.to_csv(ds_file, index=False, encoding='utf-8-sig')
            all_fields_rows.extend(ds_rows)
            print(f"  {len(ds_rows)} 个字段")
    if all_fields_rows:
        df_all = pd.DataFrame(all_fields_rows)
        all_out = f"theme_fields_all_{region}_{delay}_{universe}.csv"
        df_all.to_csv(all_out, index=False, encoding='utf-8-sig')
        print(f"已汇总 {len(df_all)} 条字段到 {all_out}")
