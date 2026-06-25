import os
import sys
import json
import logging
import requests
import pandas as pd
from typing import Optional, List

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BRAIN_API_URL = os.environ.get("BRAIN_API_URL", "https://api.worldquantbrain.com")

def login():
    """
    Authenticate with WQ Brain API.
    Loads credentials dynamically from user_config.json or user_info.txt.
    """
    from pathlib import Path
    possible_paths = [
        Path("user_config.json"),
        Path("../user_config.json"),
        Path("../../user_config.json"),
        Path(os.path.expanduser("~")) / ".config" / "AiWorkFlow" / "user_config.json",
        Path("D:/SoftWare/AiWorkFlow/user_config.json")
    ]
    config_file = r"D:\SoftWare\AiWorkFlow\user_config.json"
    for p in possible_paths:
        if p.exists():
            config_file = str(p)
            break

    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            credentials = config_data.get("credentials", {})
            username = credentials.get("email")
            password = credentials.get("password")
            if username and password:
                logger.info(f"Loaded credentials from {config_file}")
        except Exception as e:
            logger.error(f"Error loading credentials from user_config.json: {e}")

    if not username or not password:
        txt_file = 'user_info.txt'
        try:
            with open(txt_file, 'r') as f:
                data = f.read().strip().split('\n')
                data = {line.split(': ')[0]: line.split(': ')[1] for line in data}
            username = data['username'].strip("'\" ")
            password = data['password'].strip("'\" ")
            logger.info(f"Loaded credentials from {txt_file}")
        except FileNotFoundError:
            logger.error(f"Credentials not found. Please setup {config_file} or create {txt_file}.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading credentials from user_info.txt: {e}")
            sys.exit(1)

    s = requests.Session()
    s.auth = (username, password)
    try:
        response = s.post(f'{BRAIN_API_URL}/authentication')
        if response.status_code in [200, 201]:
            logger.info("Login successful.")
            return s
        else:
            logger.error(f"Authentication failed: {response.status_code} - {response.text}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Authentication exception: {e}")
        sys.exit(1)

def get_competitions(session) -> List[str]:
    """
    Fetch available competition IDs from WQ Brain.
    """
    url = f"{BRAIN_API_URL}/competitions"
    try:
        resp = session.get(url)
        if resp.status_code == 200:
            comps = resp.json().get("results", [])
            # Return competition IDs, sorted by date or ID descending
            comp_ids = [c["id"] for c in comps if "id" in c]
            logger.info(f"Found WQ competitions: {comp_ids}")
            return comp_ids
    except Exception as e:
        logger.error(f"Failed to fetch competitions list: {e}")
    return []

def get_pnl_via_competition(session, alpha_id: str, comp_ids: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Attempt to fetch PnL via competition before-and-after performance API to bypass the 2000-per-hour limit.
    Falls back to the standard PnL API if competition endpoints fail or return no data.
    """
    if not comp_ids:
        # Default or fallback list of recent/active competition IDs
        comp_ids = get_competitions(session)
        if not comp_ids:
            # Hardcoded fallbacks if API is down
            comp_ids = ["MAPC2025", "SAC2025", "MAPC2026"]

    # Try each competition endpoint
    for comp_id in comp_ids:
        url = f"{BRAIN_API_URL}/competitions/{comp_id}/alphas/{alpha_id}/before-and-after-performance"
        try:
            logger.info(f"Trying to fetch PnL for {alpha_id} via competition {comp_id}...")
            resp = session.get(url)
            if resp.status_code == 200:
                data = resp.json()
                pnl_section = data.get("pnl", {})
                records = pnl_section.get("records", [])
                schema_props = pnl_section.get("schema", {}).get("properties", [])
                
                if records and schema_props:
                    cols = [prop["name"] for prop in schema_props]
                    df = pd.DataFrame(records, columns=cols)
                    # The column is usually 'afterPnL' or 'beforePnL' or 'pnl'
                    pnl_col = next((c for c in df.columns if c != "date"), df.columns[1])
                    df = df.rename(columns={"date": "Date", pnl_col: alpha_id})
                    logger.info(f"Successfully retrieved PnL for {alpha_id} via competition {comp_id} API.")
                    return df[["Date", alpha_id]]
            elif resp.status_code == 404:
                # Alpha might not belong to this competition, try next
                continue
            elif resp.status_code == 429:
                # Rate limited on competition endpoint
                logger.warning(f"Rate limited on competition {comp_id} endpoint.")
                break
        except Exception as e:
            logger.error(f"Error fetching PnL from competition {comp_id}: {e}")

    # Fallback to standard PnL API
    logger.info(f"Falling back to standard PnL API for {alpha_id}...")
    url = f"{BRAIN_API_URL}/alphas/{alpha_id}/recordsets/pnl"
    try:
        resp = session.get(url)
        if resp.status_code == 200:
            pnl_data = resp.json()
            cols = [item['name'] for item in pnl_data['schema']['properties']]
            df = pd.DataFrame(pnl_data['records'], columns=cols)
            df = df.rename(columns={'date': 'Date', 'pnl': alpha_id})
            logger.info(f"Successfully retrieved PnL for {alpha_id} via standard API.")
            return df[['Date', alpha_id]]
        else:
            logger.error(f"Standard PnL API failed for {alpha_id}: {resp.status_code} - {resp.text}")
    except Exception as e:
        logger.error(f"Exception fetching PnL from standard API: {e}")

    return pd.DataFrame()

def main():
    if len(sys.argv) < 2:
        print("Usage: python fast_pnl_downloader.py <alpha_id> [output_csv]")
        sys.exit(1)
        
    alpha_id = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) > 2 else f"{alpha_id}_pnl.csv"
    
    session = login()
    df = get_pnl_via_competition(session, alpha_id)
    if not df.empty:
        df.to_csv(output_csv, index=False)
        print(f"PnL saved to {output_csv}. Shape: {df.shape}")
    else:
        print(f"Failed to fetch PnL for {alpha_id}")

if __name__ == "__main__":
    main()
