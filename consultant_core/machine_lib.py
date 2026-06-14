import requests
from os import environ
from time import sleep
import os
import time
import json
import re
import subprocess
import math
import pandas as pd
import random
import pickle
from pathlib import Path
from urllib.parse import urljoin
from datetime import date, datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from itertools import product
from itertools import combinations
from collections import defaultdict
import pickle
 
 
 
basic_ops = ["reverse", "inverse", "rank", "zscore", "quantile", "normalize"]
 
ts_ops = ["ts_rank", "ts_zscore", "ts_delta",  "ts_sum", "ts_delay", 
          "ts_std_dev", "ts_mean",  "ts_arg_min", "ts_arg_max","ts_scale", "ts_quantile"]
 
ops_set = basic_ops + ts_ops 

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GUI_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIMULATION_PROGRESS_LOG = PROJECT_ROOT / "runs" / "alpha_machine" / "simulation_progress.jsonl"
DEFAULT_SUBMISSION_LOG = PROJECT_ROOT / "runs" / "submissions" / "submission_log.jsonl"
DEFAULT_SUBMISSION_TIMEZONE = "Asia/Shanghai"
DEFAULT_SUBMISSION_POLL_SECONDS = 20 * 60
DEFAULT_WEBDATASCOPE_DIR = GUI_ROOT / "data" / "webdatascope"
LEGACY_WEBDATASCOPE_DIR = PROJECT_ROOT / "data" / "webdatascope"
DEFAULT_NEUTRALIZATION_FALLBACK_CYCLE = ["MARKET", "SECTOR", "INDUSTRY", "SUBINDUSTRY"]


def write_simulation_log(log_path, event):
    if log_path is None:
        return

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(event)
    record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_submission_log(log_path, event):
    if log_path is None:
        return

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(event)
    record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def next_simulation_start(log_path=DEFAULT_SIMULATION_PROGRESS_LOG):
    path = Path(log_path)
    if not path.exists():
        return 0

    completed_pools = set()
    error_events = {"task_post_error", "simulation_poll_error", "simulation_not_complete"}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except ValueError:
                continue
            pool_index = record.get("pool_index")
            if pool_index is None:
                continue
            if record.get("event") == "pool_complete":
                completed_pools.add(pool_index)
            elif record.get("event") in error_events:
                completed_pools.discard(pool_index)

    start = 0
    while start in completed_pools:
        start += 1
    return start


def _response_content_text(response):
    if response is None:
        return ""
    content = getattr(response, "content", b"")
    if isinstance(content, bytes):
        return content.decode("utf-8", errors="replace")
    return str(content)


def load_credentials(credentials_path=None):
    if credentials_path is None:
        credentials_path = PROJECT_ROOT / "credentials.json"
    else:
        credentials_path = Path(credentials_path)

    with credentials_path.open("r", encoding="utf-8") as f:
        credentials = json.load(f)

    username = credentials.get("email") or credentials.get("username")
    password = credentials.get("password")
    if not username or not password:
        raise RuntimeError(f"Missing email/username or password in {credentials_path}")

    return username, password


def _response_message(response):
    try:
        payload = response.json()
    except ValueError:
        return response.text[:500]

    if isinstance(payload, dict):
        return payload.get("message") or payload.get("detail") or payload.get("error") or str(payload)
    return str(payload)


def _json_with_results(response, url):
    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"WorldQuant API returned non-JSON response for {url}: "
            f"status={response.status_code}, text={response.text[:500]}"
        ) from exc

    if response.status_code != requests.codes.ok:
        raise RuntimeError(
            f"WorldQuant API request failed for {url}: "
            f"status={response.status_code}, message={_response_message(response)}"
        )

    if "results" not in payload:
        raise RuntimeError(
            f"WorldQuant API response for {url} did not include 'results': "
            f"status={response.status_code}, keys={list(payload.keys())}, "
            f"message={_response_message(response)}"
        )

    return payload


def _get_json_with_results(session, url, max_retries=5):
    response = None
    for attempt in range(max_retries + 1):
        response = session.get(url)
        if response.status_code != 429:
            return _json_with_results(response, url)

        if attempt == max_retries:
            return _json_with_results(response, url)

        retry_after = response.headers.get("Retry-After")
        if retry_after:
            sleep_seconds = float(retry_after)
        else:
            sleep_seconds = min(60, 5 * (attempt + 1))
        sleep(sleep_seconds)

    if response is None:
        raise RuntimeError(f"WorldQuant request was not sent: {url}")
    return _json_with_results(response, url)


def _json_payload(response, url):
    if response.status_code != requests.codes.ok:
        raise RuntimeError(
            f"WorldQuant API request failed for {url}: "
            f"status={response.status_code}, message={_response_message(response)}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"WorldQuant API returned non-JSON response for {url}: "
            f"status={response.status_code}, text={response.text[:500]}"
        ) from exc


def _get_json_payload(session, url, max_retries=2, retry_sleep=2):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = session.get(url)
            return _json_payload(response, url)
        except (requests.exceptions.RequestException, RuntimeError) as exc:
            last_error = exc
            if attempt == max_retries:
                break
            sleep(retry_sleep)

    raise RuntimeError(f"WorldQuant API request failed after retries for {url}: {last_error}") from last_error


def login():
    
    username, password = load_credentials()

    if not username or not password:
        raise RuntimeError("Missing WorldQuant Brain credentials")
 
    # Create a session to persistently store the headers
    s = requests.Session()
    s.trust_env = False
 
    # Save credentials into session
    s.auth = (username, password)
 
    # Send a POST request to the /authentication API
    response = s.post('https://api.worldquantbrain.com/authentication', timeout=60)
    if response.status_code not in (requests.codes.created, requests.codes.ok):
        raise RuntimeError(
            f"WorldQuant authentication failed: "
            f"status={response.status_code}, message={_response_message(response)}"
        )
    return s  


def reconnect_login_after_disconnect(
    reconnect_count=0,
    short_reconnects=2,
    short_sleep=300,
    long_sleep=3600,
):
    while True:
        reconnect_count += 1
        wait_seconds = submission_reconnect_sleep_seconds(
            reconnect_count,
            short_reconnects=short_reconnects,
            short_sleep=short_sleep,
            long_sleep=long_sleep,
        )
        print(f"platform disconnected; wait {wait_seconds} seconds before reconnect")
        sleep(wait_seconds)
        try:
            return login(), reconnect_count
        except (requests.exceptions.RequestException, OSError) as exc:
            print(f"login connection error: {exc}")


def get_datasets(
    s,
    instrument_type: str = 'EQUITY',
    region: str = 'USA',
    delay: int = 1,
    universe: str = 'TOP3000'
):
    url = "https://api.worldquantbrain.com/data-sets?" +\
        f"instrumentType={instrument_type}&region={region}&delay={str(delay)}&universe={universe}"
    datasets_df = pd.DataFrame(_get_json_with_results(s, url)['results'])
    return datasets_df


def get_datafield_count(
    s,
    instrument_type: str = 'EQUITY',
    region: str = 'USA',
    delay: int = 1,
    universe: str = 'TOP3000',
    dataset_id: str = '',
    search: str = ''
):
    url = "https://api.worldquantbrain.com/data-fields?" +\
        f"&instrumentType={instrument_type}" +\
        f"&region={region}&delay={str(delay)}&universe={universe}&limit=1"
    if dataset_id:
        url += f"&dataset.id={dataset_id}"
    if search:
        url += f"&search={search}"
    url += "&offset=0"
    payload = _get_json_with_results(s, url)
    return payload.get('count', len(payload['results']))


def get_datafields(
    s,
    instrument_type: str = 'EQUITY',
    region: str = 'USA',
    delay: int = 1,
    universe: str = 'TOP3000',
    dataset_id: str = '',
    search: str = ''
):
    has_search = bool(search)
    first_results = []
    if not has_search:
        url_template = "https://api.worldquantbrain.com/data-fields?" +\
            f"&instrumentType={instrument_type}" +\
            f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" +\
            "&offset={x}"
        first_url = url_template.format(x=0)
        count_payload = _get_json_with_results(s, first_url)
        first_results = count_payload['results']
        count = count_payload.get('count', len(first_results))
        
    else:
        url_template = "https://api.worldquantbrain.com/data-fields?" +\
            f"&instrumentType={instrument_type}" +\
            f"&region={region}&delay={str(delay)}&universe={universe}&limit=50" +\
            f"&search={search}" +\
            "&offset={x}"
        count = 100
    
    datafields_list = []
    start_offset = 0
    if first_results:
        datafields_list.append(first_results)
        start_offset = 50

    for x in range(start_offset, count, 50):
        url = url_template.format(x=x)
        datafields_list.append(_get_json_with_results(s, url)['results'])
 
    datafields_list_flat = [item for sublist in datafields_list for item in sublist]
 
    datafields_df = pd.DataFrame(datafields_list_flat)
    return datafields_df

def get_vec_fields(fields):

    # 请在此处添加获得权限的Vector操作符
    vec_ops = ["vec_avg", "vec_sum"]
    vec_fields = []
 
    for field in fields:
        for vec_op in vec_ops:
            if vec_op == "vec_choose":
                vec_fields.append("%s(%s, nth=-1)"%(vec_op, field))
                vec_fields.append("%s(%s, nth=0)"%(vec_op, field))
            else:
                vec_fields.append("%s(%s)"%(vec_op, field))
 
    return(vec_fields)

def processed_datafield_records(df):
    records = []
    for field_id in df[df['type'] == "MATRIX"]["id"].tolist():
        records.append(
            {
                "field_id": field_id,
                "expression": "winsorize(ts_backfill(%s, 120), std=4)" % field_id,
            }
        )
    for field_id in df[df['type'] == "VECTOR"]["id"].tolist():
        for vec_op in ["vec_avg", "vec_sum"]:
            expression = "%s(%s)" % (vec_op, field_id)
            records.append(
                {
                    "field_id": field_id,
                    "expression": "winsorize(ts_backfill(%s, 120), std=4)" % expression,
                }
            )
    return records

def process_datafields(df):

    datafields = []
    datafields += df[df['type'] == "MATRIX"]["id"].tolist()
    datafields += get_vec_fields(df[df['type'] == "VECTOR"]["id"].tolist())
    return ["winsorize(ts_backfill(%s, 120), std=4)"%field for field in datafields]


def _webdatascope_scope_key(region="USA", delay=1):
    return f"{str(region).upper()}_{int(delay)}"


def _coerce_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _select_webdatascope_neutralization(
    item_data,
    min_sharpe=0.35,
    min_osis_count=20,
):
    if not item_data:
        return None

    candidates = []
    for neut, stats in item_data.items():
        if not isinstance(stats, dict):
            continue
        count = stats.get("count")
        try:
            count_value = int(count)
        except (TypeError, ValueError):
            count_value = 0
        sharpe = _coerce_float(stats.get("sharpe_ratio"))
        osis_count = stats.get("osis_count")
        try:
            osis_count_value = int(osis_count)
        except (TypeError, ValueError):
            osis_count_value = count_value
        score = None
        if sharpe is not None:
            score = sharpe * math.log(osis_count_value + 1)
        candidates.append(
            {
                "neutralization": str(neut).upper(),
                "count": count_value,
                "sharpe_ratio": sharpe,
                "osis_count": osis_count_value,
                "score": score,
            }
        )
    if not candidates:
        return None

    qualified = [
        item
        for item in candidates
        if item["sharpe_ratio"] is not None
        and item["sharpe_ratio"] >= min_sharpe
        and item["osis_count"] >= min_osis_count
    ]
    ranking_pool = qualified or candidates
    ranking_pool.sort(
        key=lambda item: (
            item["score"] if item["score"] is not None else float("-inf"),
            item["count"],
            item["neutralization"],
        ),
        reverse=True,
    )
    selected = ranking_pool[0]
    total_count = sum(item["count"] for item in candidates)
    selected["percentage"] = (selected["count"] / total_count * 100) if total_count else 0
    selected["selection_rule"] = "efficiency_score" if qualified else "unqualified_score_fallback"
    return selected


def recommended_neutralization_table(
    df,
    data_info,
    dataset_id,
    region="USA",
    universe="TOP3000",
    delay=1,
    fallback_cycle=None,
    min_sharpe=0.35,
    min_osis_count=20,
):
    fallback_cycle = fallback_cycle or DEFAULT_NEUTRALIZATION_FALLBACK_CYCLE
    scope = (data_info or {}).get(_webdatascope_scope_key(region, delay), {})
    neutralization_stats = scope.get("neutralization") or {}
    field_stats = neutralization_stats.get("datafield") or {}
    dataset_stats = neutralization_stats.get("dataset") or {}

    rows = []
    fallback_index = 0
    for field_id in df["id"].tolist():
        source = "webdatascope_datafield"
        selected = _select_webdatascope_neutralization(
            field_stats.get(field_id),
            min_sharpe=min_sharpe,
            min_osis_count=min_osis_count,
        )
        if not selected:
            source = "webdatascope_dataset"
            selected = _select_webdatascope_neutralization(
                dataset_stats.get(dataset_id),
                min_sharpe=min_sharpe,
                min_osis_count=min_osis_count,
            )
        if selected:
            rows.append(
                {
                    "field_id": field_id,
                    "dataset_id": dataset_id,
                    "region": region,
                    "universe": universe,
                    "delay": delay,
                    "recommended_neutralization": selected["neutralization"],
                    "recommendation_source": source,
                    "selection_rule": selected["selection_rule"],
                    "count": selected["count"],
                    "percentage": selected["percentage"],
                    "sharpe_ratio": selected["sharpe_ratio"],
                    "osis_count": selected["osis_count"],
                    "score": selected["score"],
                }
            )
            continue

        neutralization = fallback_cycle[fallback_index % len(fallback_cycle)]
        fallback_index += 1
        rows.append(
            {
                "field_id": field_id,
                "dataset_id": dataset_id,
                "region": region,
                "universe": universe,
                "delay": delay,
                "recommended_neutralization": neutralization,
                "recommendation_source": "fallback_cycle",
                "selection_rule": "fallback_cycle",
                "count": None,
                "percentage": None,
                "sharpe_ratio": None,
                "osis_count": None,
                "score": None,
            }
        )

    return pd.DataFrame(rows)


def split_processed_datafields_by_neutralization(df, recommendations):
    recommendation_map = dict(
        zip(recommendations["field_id"], recommendations["recommended_neutralization"])
    )
    grouped = defaultdict(list)
    for record in processed_datafield_records(df):
        neut = recommendation_map.get(record["field_id"], "SUBINDUSTRY")
        grouped[neut].append(record["expression"])
    return dict(grouped)


def load_webdatascope_info(
    webdatascope_dir=DEFAULT_WEBDATASCOPE_DIR,
    info_data_path=None,
    node_executable="node",
):
    webdatascope_dir = Path(webdatascope_dir)
    if webdatascope_dir == DEFAULT_WEBDATASCOPE_DIR and not webdatascope_dir.exists() and LEGACY_WEBDATASCOPE_DIR.exists():
        webdatascope_dir = LEGACY_WEBDATASCOPE_DIR
    info_data_path = Path(info_data_path) if info_data_path else webdatascope_dir / "info_data.bin"
    cache_path = webdatascope_dir / "webdatascope_info.json"
    if cache_path.exists():
        with cache_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    pako_path = webdatascope_dir / "pako.min.js"
    msgpack_path = webdatascope_dir / "msgpack.min.js"
    script = (
        "const fs=require('fs');"
        "const pako=require(process.argv[1]);"
        "const msgpack=require(process.argv[2]);"
        "const raw=fs.readFileSync(process.argv[3]);"
        "const data=msgpack.decode(pako.inflate(new Uint8Array(raw)));"
        "process.stdout.write(JSON.stringify(data));"
    )
    result = subprocess.run(
        [node_executable, "-e", script, str(pako_path), str(msgpack_path), str(info_data_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    data = json.loads(result.stdout)
    webdatascope_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = cache_path.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    tmp_path.replace(cache_path)
    return data

def ts_factory(op, field):
    output = []
    #days = [3, 5, 10, 20, 60, 120, 240]
    days = [5, 22, 66, 120, 240]
    
    for day in days:
    
        alpha = "%s(%s, %d)"%(op, field, day)
        output.append(alpha)
    
    return output

def first_order_factory(fields, ops_set):
    alpha_set = []
    #for field in fields:
    for field in fields:
        #reverse op does the work
        alpha_set.append(field)
        #alpha_set.append("-%s"%field)
        for op in ops_set:
 
            if op == "ts_percentage":
 
                alpha_set += ts_comp_factory(op, field, "percentage", [0.5])
 
            elif op == "ts_decay_exp_window":
 
                alpha_set += ts_comp_factory(op, field, "factor", [0.5])
 
            elif op == "ts_moment":
 
                alpha_set += ts_comp_factory(op, field, "k", [2, 3, 4])
 
            elif op == "ts_entropy":
 
                alpha_set += ts_comp_factory(op, field, "buckets", [10])
 
            elif op.startswith("ts_") or op == "inst_tvr":
 
                alpha_set += ts_factory(op, field)
 
            elif op.startswith("vector"):
 
                alpha_set += vector_factory(op, field)
 
            elif op == "signed_power":
 
                alpha = "%s(%s, 2)"%(op, field)
                alpha_set.append(alpha)
 
            else:
                alpha = "%s(%s)"%(op, field)
                alpha_set.append(alpha)
 
    return alpha_set


def load_task_pool(alpha_list, limit_of_children_simulations, limit_of_multi_simulations):
    '''
    Input:
        alpha_list : list of (alpha, decay) tuples
        limit_of_multi_simulations : number of children simulation in a multi-simulation
        limit_of_multi_simulations : number of simultaneous multi-simulations
    Output:
        task : [10 * (alpha, decay)] for a multi-simulation
        pool : [10 * [10 * (alpha, decay)]] for simultaneous multi-simulations
        pools : [[10 * [10 * (alpha, decay)]]]

    '''
    tasks = [alpha_list[i:i + limit_of_children_simulations] for i in range(0, len(alpha_list), limit_of_children_simulations)]
    pools = [tasks[i:i + limit_of_multi_simulations] for i in range(0, len(tasks), limit_of_multi_simulations)]
    return pools

def multi_simulate(
    alpha_pools,
    neut,
    region,
    universe,
    start=0,
    log_path=DEFAULT_SIMULATION_PROGRESS_LOG,
):

    s = login()
    reconnect_count = 0

    brain_api_url = 'https://api.worldquantbrain.com'
    write_simulation_log(
        log_path,
        {
            "event": "simulation_run_start",
            "start": start,
            "pool_count": len(alpha_pools),
            "neutralization": neut,
            "region": region,
            "universe": universe,
        },
    )

    for x, pool in enumerate(alpha_pools):
        if x < start: continue
        pool_failed = False
        write_simulation_log(log_path, {"event": "pool_start", "pool_index": x, "task_count": len(pool)})
        progress_urls = []
        y = -1
        for y, task in enumerate(pool):
            # 10 tasks, 10 alpha in each task
            sim_data_list = generate_sim_data(task, region, universe, neut)
            simulation_response = None
            write_simulation_log(
                log_path,
                {
                    "event": "task_post_start",
                    "pool_index": x,
                    "task_index": y,
                    "alpha_count": len(task),
                },
            )
            try:
                simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=sim_data_list)
                simulation_progress_url = simulation_response.headers['Location']
                progress_urls.append(simulation_progress_url)
                write_simulation_log(
                    log_path,
                    {
                        "event": "task_post_submitted",
                        "pool_index": x,
                        "task_index": y,
                        "progress_url": simulation_progress_url,
                    },
                )
            except Exception as exc:
                pool_failed = True
                content = _response_content_text(simulation_response)
                write_simulation_log(
                    log_path,
                    {
                        "event": "task_post_error",
                        "pool_index": x,
                        "task_index": y,
                        "status_code": getattr(simulation_response, "status_code", None),
                        "message": content,
                        "exception": repr(exc),
                    },
                )
                print("location key error: %s"%content)
                if isinstance(exc, (requests.exceptions.RequestException, OSError)):
                    s, reconnect_count = reconnect_login_after_disconnect(reconnect_count)
                else:
                    sleep(600)
                    s = login()

        print("pool %d task %d post done"%(x,y))

        j = -1
        for j, progress in enumerate(progress_urls):
            try:
                simulation_progress = None
                while True:
                    simulation_progress = s.get(progress)
                    retry_after = float(simulation_progress.headers.get("Retry-After", 0))
                    if retry_after == 0:
                        break
                    # 将回测的检查间隔从5秒变成20秒
                    sleep_time = max(20.0, retry_after)
                    sleep(sleep_time)

                status = simulation_progress.json().get("status", 0)
                if status != "COMPLETE":
                    pool_failed = True
                    write_simulation_log(
                        log_path,
                        {
                            "event": "simulation_not_complete",
                            "pool_index": x,
                            "progress_index": j,
                            "progress_url": progress,
                            "status": status,
                        },
                    )
                    print("Not complete : %s"%(progress))
                else:
                    write_simulation_log(
                        log_path,
                        {
                            "event": "simulation_complete",
                            "pool_index": x,
                            "progress_index": j,
                            "progress_url": progress,
                        },
                    )

                """
                #alpha_id = simulation_progress.json()["alpha"]
                children = simulation_progress.json().get("children", 0)
                children_list = []
                for child in children:
                    child_progress = s.get(brain_api_url + "/simulations/" + child)
                    alpha_id = child_progress.json()["alpha"]

                    set_alpha_properties(s,
                            alpha_id,
                            name = "%s"%name,
                            color = None,)
                """
            except KeyError:
                pool_failed = True
                write_simulation_log(
                    log_path,
                    {
                        "event": "simulation_poll_error",
                        "pool_index": x,
                        "progress_index": j,
                        "progress_url": progress,
                        "exception": "KeyError",
                    },
                )
                print("look into: %s"%progress)
            except Exception as e:
                pool_failed = True
                write_simulation_log(
                    log_path,
                    {
                        "event": "simulation_poll_error",
                        "pool_index": x,
                        "progress_index": j,
                        "progress_url": progress,
                        "exception": repr(e),
                    },
                )
                print(f"other error: {e}")


        print("pool %d task %d simulate done"%(x, j))
        if not pool_failed:
            write_simulation_log(log_path, {"event": "pool_complete", "pool_index": x})
    
    print("Simulate done")
    write_simulation_log(log_path, {"event": "simulation_run_complete"})

def generate_sim_data(alpha_list, region, uni, neut):
    sim_data_list = []
    for alpha, decay in alpha_list:
        simulation_data = {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': region,
                'universe': uni,
                'delay': 1,
                'decay': decay,
                'neutralization': neut,
                'truncation': 0.08,
                'pasteurization': 'ON',
                'testPeriod': 'P0Y',
                'unitHandling': 'VERIFY',
                'nanHandling': 'ON',
                'language': 'FASTEXPR', #  FASTEXPR 快速表达式，PYTHON Python语言回测
                'visualization': False,
            },
            'regular': alpha}

        sim_data_list.append(simulation_data)
    return sim_data_list

def set_alpha_properties(
    s,
    alpha_id,
    name: str | None = None,
    color: str | None = None,
    selection_desc: str = "None",
    combo_desc: str = "None",
    tags: str = ["ace_tag"],
):
    """
    Function changes alpha's description parameters
    """
 
    params = {
        "color": color,
        "name": name,
        "tags": tags,
        "category": None,
        "regular": {"description": None},
        "combo": {"description": combo_desc},
        "selection": {"description": selection_desc},
    }
    response = s.patch(
        "https://api.worldquantbrain.com/alphas/" + alpha_id, json=params
    )


def parse_renamed_alpha_log(text):
    """Extract alpha ids and target names from rename log lines."""
    records = []
    seen = set()
    pattern = re.compile(r"\bRenaming\s+([A-Za-z0-9]+)\s+to\s+(\S+)")
    for line in str(text).splitlines():
        match = pattern.search(line)
        if not match:
            continue
        alpha_id, target_name = match.groups()
        if alpha_id in seen:
            continue
        seen.add(alpha_id)
        records.append({"alpha_id": alpha_id, "target_name": target_name})
    return records


def _submission_date_text(value=None):
    if value is None:
        return date.today().isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _read_submission_log(log_path=DEFAULT_SUBMISSION_LOG):
    path = Path(log_path)
    if not path.exists():
        return []

    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except ValueError:
                continue
    return records


def _successful_submission_ids(log_path=DEFAULT_SUBMISSION_LOG):
    return {
        record.get("alpha_id")
        for record in _read_submission_log(log_path)
        if record.get("event") == "alpha_submit_success" and record.get("alpha_id")
    }


def submitted_count_for_date(submission_date=None, log_path=DEFAULT_SUBMISSION_LOG):
    target_date = _submission_date_text(submission_date)
    return sum(
        1
        for record in _read_submission_log(log_path)
        if record.get("event") == "alpha_submit_success"
        and record.get("submission_date") == target_date
    )


def _parse_hhmm(value):
    if value is None:
        return None

    parts = str(value).strip().split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Expected HH:MM time, got {value!r}")
    hour = int(parts[0])
    minute = int(parts[1])
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Expected HH:MM time, got {value!r}")
    return hour, minute


def _ensure_timezone(value, timezone_name=DEFAULT_SUBMISSION_TIMEZONE):
    tz = ZoneInfo(timezone_name)
    if value.tzinfo is None:
        return value.replace(tzinfo=tz)
    return value.astimezone(tz)


def _now_in_timezone(timezone_name=DEFAULT_SUBMISSION_TIMEZONE):
    return datetime.now(ZoneInfo(timezone_name))


def _minutes_since_midnight(value):
    return value.hour * 60 + value.minute


def _is_blocked_submission_time(
    now,
    blocked_start=None,
    blocked_end=None,
    timezone_name=DEFAULT_SUBMISSION_TIMEZONE,
):
    if not blocked_start or not blocked_end:
        return False

    local_now = _ensure_timezone(now, timezone_name)
    start_hour, start_minute = _parse_hhmm(blocked_start)
    end_hour, end_minute = _parse_hhmm(blocked_end)
    start = start_hour * 60 + start_minute
    end = end_hour * 60 + end_minute
    current = _minutes_since_midnight(local_now)

    if start == end:
        return True
    if start < end:
        return start <= current < end
    return current >= start or current < end


def _normalize_alpha_submit_record(record):
    if isinstance(record, str):
        return {"alpha_id": record, "target_name": None}
    if isinstance(record, dict):
        alpha_id = record.get("alpha_id") or record.get("id")
        return {"alpha_id": alpha_id, "target_name": record.get("target_name") or record.get("name")}
    if isinstance(record, (list, tuple)) and record:
        alpha_id = record[0]
        target_name = record[1] if len(record) > 1 else None
        return {"alpha_id": alpha_id, "target_name": target_name}
    raise ValueError(f"Unsupported alpha submit record: {record!r}")


def submit_alpha(s, alpha_id, max_retries=2, retry_sleep=5, max_submit_polls=20):
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit"
    last_response = None
    for attempt in range(max_retries + 1):
        response = s.post(url)
        submit_polls = 0
        while True:
            last_response = response
            retry_after = response.headers.get("Retry-After") or response.headers.get("retry-after")
            if not retry_after:
                break
            submit_polls += 1
            if submit_polls > max_submit_polls:
                break
            sleep(float(retry_after))
            response = s.get(url)

        if last_response.status_code in (requests.codes.ok, requests.codes.created, requests.codes.accepted):
            return last_response

        if last_response.status_code == 429 and attempt < max_retries:
            sleep(retry_sleep)
            continue
        if last_response.status_code >= 500 and attempt < max_retries:
            sleep(retry_sleep)
            continue
        break

    raise RuntimeError(
        f"WorldQuant alpha submit failed for {alpha_id}: "
        f"status={last_response.status_code}, message={_response_message(last_response)}"
    )


def submit_alpha_queue(
    records,
    session=None,
    log_path=DEFAULT_SUBMISSION_LOG,
    max_per_day=4,
    today=None,
    dry_run=False,
    submit_max_retries=2,
    submit_retry_sleep=60,
    pause_between_submits=0,
):
    submission_date = _submission_date_text(today)
    already_submitted = _successful_submission_ids(log_path)
    daily_count = submitted_count_for_date(submission_date, log_path=log_path)
    daily_remaining = max(0, max_per_day - daily_count)
    summary = {
        "submission_date": submission_date,
        "daily_limit": max_per_day,
        "daily_success_before_run": daily_count,
        "daily_remaining_before_run": daily_remaining,
        "submitted": [],
        "dry_run": [],
        "failed": [],
        "skipped_existing": [],
        "skipped_limit": [],
    }
    s = session if session is not None or dry_run else login()

    seen = set()
    for raw_record in records:
        record = _normalize_alpha_submit_record(raw_record)
        alpha_id = record.get("alpha_id")
        if not alpha_id:
            continue
        if alpha_id in seen:
            continue
        seen.add(alpha_id)
        target_name = record.get("target_name")

        if alpha_id in already_submitted:
            summary["skipped_existing"].append(alpha_id)
            continue
        if daily_remaining <= 0:
            summary["skipped_limit"].append(alpha_id)
            continue

        base_event = {
            "alpha_id": alpha_id,
            "target_name": target_name,
            "submission_date": submission_date,
        }
        if dry_run:
            summary["dry_run"].append(alpha_id)
            write_submission_log(log_path, {"event": "alpha_submit_dry_run", **base_event})
            daily_remaining -= 1
            continue

        try:
            write_submission_log(log_path, {"event": "alpha_submit_started", **base_event})
            response = submit_alpha(
                s,
                alpha_id,
                max_retries=submit_max_retries,
                retry_sleep=submit_retry_sleep,
            )
        except Exception as exc:
            summary["failed"].append({"alpha_id": alpha_id, "message": str(exc)})
            write_submission_log(
                log_path,
                {"event": "alpha_submit_error", "message": str(exc), **base_event},
            )
            if pause_between_submits:
                sleep(pause_between_submits)
            continue

        summary["submitted"].append(alpha_id)
        already_submitted.add(alpha_id)
        daily_remaining -= 1
        write_submission_log(
            log_path,
            {
                "event": "alpha_submit_success",
                "status_code": response.status_code,
                "message": _response_message(response),
                **base_event,
            },
        )
        if pause_between_submits and daily_remaining > 0:
            sleep(pause_between_submits)

    summary["daily_remaining_after_run"] = daily_remaining
    return summary


def _remove_finished_submit_records(records, summary, retry_failed=False):
    finished = set(summary.get("submitted", []))
    finished.update(summary.get("dry_run", []))
    finished.update(summary.get("skipped_existing", []))
    if not retry_failed:
        finished.update(item.get("alpha_id") for item in summary.get("failed", []) if item.get("alpha_id"))

    pending = []
    for record in records:
        alpha_id = _normalize_alpha_submit_record(record).get("alpha_id")
        if alpha_id and alpha_id in finished:
            continue
        pending.append(record)
    return pending


def submit_alpha_queue_until_limit(
    records,
    session=None,
    log_path=DEFAULT_SUBMISSION_LOG,
    daily_limit=4,
    poll_seconds=DEFAULT_SUBMISSION_POLL_SECONDS,
    blocked_start=None,
    blocked_end=None,
    timezone_name=DEFAULT_SUBMISSION_TIMEZONE,
    max_cycles=None,
    now_func=None,
    sleep_func=None,
    retry_failed=False,
    dry_run=False,
    submit_max_retries=2,
    submit_retry_sleep=60,
    pause_between_submits=0,
):
    """
    Keep submitting pending alphas while daily capacity is available.

    The daily count is read from the local submission log every cycle. If the
    daily limit has been reached, or the China-time blocked window is active,
    this waits `poll_seconds` before checking again.
    """
    pending = list(records)
    get_now = now_func or (lambda: _now_in_timezone(timezone_name))
    sleeper = sleep_func or sleep
    summary = {
        "daily_limit": daily_limit,
        "poll_seconds": poll_seconds,
        "blocked_window": (
            {"start": blocked_start, "end": blocked_end, "timezone": timezone_name}
            if blocked_start and blocked_end
            else None
        ),
        "submitted": [],
        "dry_run": [],
        "failed": [],
        "skipped_existing": [],
        "skipped_limit": [],
        "cycles": [],
    }

    cycles = 0
    while pending:
        if max_cycles is not None and cycles >= max_cycles:
            break
        cycles += 1

        now = _ensure_timezone(get_now(), timezone_name)
        submission_date = now.date().isoformat()
        submitted_today = submitted_count_for_date(submission_date, log_path=log_path)

        if _is_blocked_submission_time(now, blocked_start, blocked_end, timezone_name):
            summary["cycles"].append(
                {
                    "event": "blocked_submission_window",
                    "submission_date": submission_date,
                    "submitted_today": submitted_today,
                    "pending_count": len(pending),
                }
            )
            sleeper(poll_seconds)
            continue

        if submitted_today >= daily_limit:
            summary["cycles"].append(
                {
                    "event": "daily_limit_reached",
                    "submission_date": submission_date,
                    "submitted_today": submitted_today,
                    "pending_count": len(pending),
                }
            )
            sleeper(poll_seconds)
            continue

        run_summary = submit_alpha_queue(
            pending,
            session=session,
            log_path=log_path,
            max_per_day=daily_limit,
            today=submission_date,
            dry_run=dry_run,
            submit_max_retries=submit_max_retries,
            submit_retry_sleep=submit_retry_sleep,
            pause_between_submits=pause_between_submits,
        )
        summary["cycles"].append(
            {
                "event": "submit_attempt",
                "submission_date": submission_date,
                "submitted_today": submitted_today,
                "pending_count": len(pending),
                "result": run_summary,
            }
        )
        for key in ("submitted", "dry_run", "failed", "skipped_existing", "skipped_limit"):
            summary[key].extend(run_summary.get(key, []))

        pending = _remove_finished_submit_records(pending, run_summary, retry_failed=retry_failed)

    summary["pending_count"] = len(pending)
    return summary


def _format_alpha_date(value, year=None):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()

    text = str(value).strip()
    if not text:
        return None
    if len(text) == 5 and text[2] == "-":
        return f"{year or datetime.now().year}-{text}"
    return text


def _alpha_next_decay(turnover, decay):
    if turnover is None or decay is None:
        return None
    if turnover > 0.7:
        return decay * 4
    if turnover > 0.6:
        return decay * 3 + 3
    if turnover > 0.5:
        return decay * 3
    if turnover > 0.4:
        return decay * 2
    if turnover > 0.35:
        return decay + 4
    if turnover > 0.3:
        return decay + 2
    return decay


def _alpha_query_url(
    offset,
    page_size,
    start_date=None,
    end_date=None,
    sharpe_th=None,
    fitness_th=None,
    region=None,
    order="-is.sharpe",
    direction="positive",
    status="UNSUBMITTED%1FIS_FAIL",
    year=None,
):
    url = f"https://api.worldquantbrain.com/users/self/alphas?limit={page_size}&offset={offset}"
    if status:
        url += f"&status={status}"

    start = _format_alpha_date(start_date, year=year)
    end = _format_alpha_date(end_date, year=year)
    if start:
        url += f"&dateCreated%3E={start}T00:00:00-04:00"
    if end:
        url += f"&dateCreated%3C{end}T00:00:00-04:00"

    if fitness_th is not None:
        sign = "%3C-" if direction == "negative" else "%3E"
        url += f"&is.fitness{sign}{fitness_th}"
    if sharpe_th is not None:
        sign = "%3C-" if direction == "negative" else "%3E"
        url += f"&is.sharpe{sign}{sharpe_th}"
    if region:
        url += f"&settings.region={region}"
    url += f"&order={order}&hidden=false&type!=SUPER"
    return url


def _alpha_row(alpha, direction="positive"):
    metrics = alpha.get("is") or {}
    settings = alpha.get("settings") or {}
    regular = alpha.get("regular") or {}
    sharpe = metrics.get("sharpe")
    fitness = metrics.get("fitness")
    turnover = metrics.get("turnover")
    margin = metrics.get("margin")
    long_count = metrics.get("longCount")
    short_count = metrics.get("shortCount")
    decay = settings.get("decay")
    expression = regular.get("code")
    if direction == "negative" and expression:
        expression = f"-{expression}"

    return {
        "alpha_id": alpha.get("id"),
        "name": alpha.get("name"),
        "dateCreated": alpha.get("dateCreated"),
        "expression": expression,
        "sharpe": sharpe,
        "fitness": fitness,
        "turnover": turnover,
        "margin": margin,
        "returns": metrics.get("returns"),
        "drawdown": metrics.get("drawdown"),
        "longCount": long_count,
        "shortCount": short_count,
        "instrumentCount": (long_count or 0) + (short_count or 0),
        "decay": decay,
        "next_decay": _alpha_next_decay(turnover, decay),
        "region": settings.get("region"),
        "universe": settings.get("universe"),
        "neutralization": settings.get("neutralization"),
        "direction": direction,
        "status": alpha.get("status"),
    }


def get_alpha_detail(alpha_id, session=None, max_retries=2, retry_sleep=2):
    s = session or login()
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
    return _get_json_payload(s, url, max_retries=max_retries, retry_sleep=retry_sleep)


def get_alpha_recordsets(alpha_id, session=None, max_retries=2, retry_sleep=2):
    s = session or login()
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets"
    return _get_json_payload(s, url, max_retries=max_retries, retry_sleep=retry_sleep)


def alpha_recordset_to_frame(payload):
    schema = payload.get("schema") or {}
    properties = schema.get("properties") or []
    columns = [item.get("name") for item in properties]
    records = payload.get("records") or []
    df = pd.DataFrame(records, columns=columns)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def get_alpha_recordset(alpha_id, recordset_name, session=None, max_retries=2, retry_sleep=2):
    s = session or login()
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/{recordset_name}"
    return alpha_recordset_to_frame(
        _get_json_payload(s, url, max_retries=max_retries, retry_sleep=retry_sleep)
    )


def get_alphas_full(
    start_date=None,
    end_date=None,
    sharpe_th=None,
    fitness_th=None,
    region="USA",
    limit=None,
    usage="track",
    include_negative=None,
    session=None,
    page_size=100,
    year=None,
    min_instrument_count=0,
    order="-is.sharpe",
    status="UNSUBMITTED%1FIS_FAIL",
):
    """Fetch alpha records as a DataFrame with explicit metric columns.

    Dates can be full ``YYYY-MM-DD`` strings, ``datetime/date`` objects, or
    short ``MM-DD`` strings with ``year=2026``. Omit dates to fetch all pages
    matching the remaining filters.
    """
    s = session or login()
    include_negative = usage != "submit" if include_negative is None else include_negative
    directions = [("positive", order)]
    if include_negative:
        negative_order = "is.sharpe" if order == "-is.sharpe" else order
        directions.append(("negative", negative_order))

    rows = []
    for direction, order in directions:
        offset = 0
        fetched = 0
        retries = 0
        while True:
            if limit is not None and fetched >= limit:
                break
            current_page_size = min(page_size, limit - fetched) if limit is not None else page_size
            url = _alpha_query_url(
                offset,
                current_page_size,
                start_date=start_date,
                end_date=end_date,
                sharpe_th=sharpe_th,
                fitness_th=fitness_th,
                region=region,
                order=order,
                direction=direction,
                year=year,
                status=status,
            )
            response = s.get(url)
            try:
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    print(f"Rate limited. Sleeping for {retry_after}s.")
                    time.sleep(retry_after)
                    continue
                alpha_list = response.json().get("results", [])
                retries = 0 # reset retries on success
            except Exception as e:
                retries += 1
                print(f"Offset {offset} error {e}, status {response.status_code}. Retrying ({retries}/5)...")
                time.sleep(2 ** retries)
                if retries > 5:
                    print("Max retries exceeded, skipping this page.")
                    break
                s = login()
                continue

            for alpha in alpha_list:
                row = _alpha_row(alpha, direction=direction)
                if row["instrumentCount"] >= min_instrument_count:
                    rows.append(row)

            fetched += len(alpha_list)
            if len(alpha_list) < current_page_size:
                break
            offset += current_page_size

    return pd.DataFrame(rows)


def get_alphas(start_date, end_date, sharpe_th, fitness_th, region, alpha_num, usage):
    df = get_alphas_full(
        start_date=start_date,
        end_date=end_date,
        sharpe_th=sharpe_th,
        fitness_th=fitness_th,
        region=region,
        limit=alpha_num,
        usage=usage,
        year=datetime.now().year,
        min_instrument_count=101,
    )
    return _alpha_frame_to_legacy_records(df)


def recent_alpha_date_range(lookback_days, timezone_name=DEFAULT_SUBMISSION_TIMEZONE, now=None):
    """返回最近 N 天 alpha 查询窗口，格式为完整 YYYY-MM-DD 日期。"""
    if now is None:
        today = datetime.now(ZoneInfo(timezone_name)).date()
    elif isinstance(now, datetime):
        today = _ensure_timezone(now, timezone_name).date()
    elif isinstance(now, date):
        today = now
    else:
        today = _ensure_timezone(datetime.fromisoformat(str(now)), timezone_name).date()
    start = today - timedelta(days=lookback_days)
    return start.isoformat(), today.isoformat()


def daily_alpha_date_range(timezone_name=DEFAULT_SUBMISSION_TIMEZONE, now=None):
    """返回当天 alpha 查询窗口；结束日期用明天，因为 API 的结束时间是开区间。"""
    if now is None:
        today = datetime.now(ZoneInfo(timezone_name)).date()
    elif isinstance(now, datetime):
        today = _ensure_timezone(now, timezone_name).date()
    elif isinstance(now, date):
        today = now
    else:
        today = _ensure_timezone(datetime.fromisoformat(str(now)), timezone_name).date()
    tomorrow = today + timedelta(days=1)
    return today.isoformat(), tomorrow.isoformat()


def _alpha_frame_to_legacy_records(df, verbose=True):
    output = []
    for _, row in df.iterrows():
        rec = [
            row["alpha_id"],
            row["expression"],
            row["sharpe"],
            row["turnover"],
            row["fitness"],
            row["margin"],
            row["dateCreated"],
            row["decay"],
        ]
        if row["next_decay"] != row["decay"]:
            rec.append(row["next_decay"])
        if verbose:
            print(rec)
        output.append(rec)

    if verbose:
        print("count: %d"%len(output))
    return output


def get_recent_alphas(
    lookback_days,
    sharpe_th,
    fitness_th,
    region,
    universe,
    alpha_num,
    usage,
    timezone_name=DEFAULT_SUBMISSION_TIMEZONE,
    fetch_limit_multiplier=3,
    session=None,
    now=None,
    verbose=True,
):
    """拉取最近 alpha 候选，并保留指定 region/universe 的结果。

    WorldQuant 的 alpha 列表接口可以直接按 region 查询；universe 会在
    alpha settings 中返回，因此这里先拉取，再按 universe 二次过滤。
    """
    start_date, end_date = recent_alpha_date_range(
        lookback_days,
        timezone_name=timezone_name,
        now=now,
    )
    fetch_limit = max(alpha_num, alpha_num * fetch_limit_multiplier)
    if verbose:
        print(
            f"Fetching {usage} alphas from {start_date} to {end_date}, "
            f"region={region}, universe={universe}, sharpe>={sharpe_th}, fitness>={fitness_th}"
        )
    alpha_df = get_alphas_full(
        start_date=start_date,
        end_date=end_date,
        sharpe_th=sharpe_th,
        fitness_th=fitness_th,
        region=region,
        limit=fetch_limit,
        usage=usage,
        session=session,
        min_instrument_count=101,
    )
    if alpha_df.empty:
        if verbose:
            print("count: 0")
        return []
    if "universe" in alpha_df.columns:
        alpha_df = alpha_df[alpha_df["universe"] == universe]
    alpha_df = alpha_df.head(alpha_num)
    return _alpha_frame_to_legacy_records(alpha_df, verbose=verbose)


def get_daily_alpha_count(
    alpha_num=4500,
    usage="track",
    timezone_name=DEFAULT_SUBMISSION_TIMEZONE,
    session=None,
    now=None,
    status="UNSUBMITTED%1FIS_FAIL",
    min_instrument_count=0,
):
    """统计当天 alpha 数量；默认不限制 region，用于和每日生成上限比较。"""
    start_date, end_date = daily_alpha_date_range(timezone_name=timezone_name, now=now)
    alpha_df = get_alphas_full(
        start_date=start_date,
        end_date=end_date,
        sharpe_th=None,
        fitness_th=None,
        region=None,
        limit=alpha_num,
        usage=usage,
        session=session,
        min_instrument_count=min_instrument_count,
        status=status,
        include_negative=False,
        order="-dateCreated",
    )
    return len(alpha_df)


def prune(next_alpha_recs, prefix, keep_num):
    # prefix is the datafield prefix, fnd6, mdl175 ...
    # keep_num is the num of top sharpe same-datafield alpha
    output = []
    num_dict = defaultdict(int)
    for rec in next_alpha_recs:
        exp = rec[1]
        field = exp.split(prefix)[-1].split(",")[0]
        sharpe = rec[2]
        if sharpe < 0:
            field = "-%s"%field
        if num_dict[field] < keep_num:
            num_dict[field] += 1
            decay = rec[-1]
            exp = rec[1]
            output.append([exp,decay])
    return output

def get_group_second_order_factory(first_order, group_ops, region):
    second_order = []
    for fo in first_order:
        for group_op in group_ops:
            second_order += group_factory(group_op, fo, region)
    return second_order


def group_factory(op, field, region):
    output = []
    vectors = ["cap"] 
    
    chn_group_13 = ['pv13_h_min2_sector', 'pv13_di_6l', 'pv13_rcsed_6l', 'pv13_di_5l', 'pv13_di_4l', 
                        'pv13_di_3l', 'pv13_di_2l', 'pv13_di_1l', 'pv13_parent', 'pv13_level']
    
    
    chn_group_1 = ['sta1_top3000c30','sta1_top3000c20','sta1_top3000c10','sta1_top3000c2','sta1_top3000c5']
    
    chn_group_2 = ['sta2_top3000_fact4_c10','sta2_top2000_fact4_c50','sta2_top3000_fact3_c20']
    
    hkg_group_13 = ['pv13_10_f3_g2_minvol_1m_sector', 'pv13_10_minvol_1m_sector', 'pv13_20_minvol_1m_sector', 
                    'pv13_2_minvol_1m_sector', 'pv13_5_minvol_1m_sector', 'pv13_1l_scibr', 'pv13_3l_scibr',
                    'pv13_2l_scibr', 'pv13_4l_scibr', 'pv13_5l_scibr']
    
    hkg_group_1 = ['sta1_allc50','sta1_allc5','sta1_allxjp_513_c20','sta1_top2000xjp_513_c5']
    
    hkg_group_2 = ['sta2_all_xjp_513_all_fact4_c10','sta2_top2000_xjp_513_top2000_fact3_c10',
                   'sta2_allfactor_xjp_513_13','sta2_top2000_xjp_513_top2000_fact3_c20']
    
    twn_group_13 = ['pv13_2_minvol_1m_sector','pv13_20_minvol_1m_sector','pv13_10_minvol_1m_sector',
                    'pv13_5_minvol_1m_sector','pv13_10_f3_g2_minvol_1m_sector','pv13_5_f3_g2_minvol_1m_sector',
                    'pv13_2_f4_g3_minvol_1m_sector']
    
    twn_group_1 = ['sta1_allc50','sta1_allxjp_513_c50','sta1_allxjp_513_c20','sta1_allxjp_513_c2',
                   'sta1_allc20','sta1_allxjp_513_c5','sta1_allxjp_513_c10','sta1_allc2','sta1_allc5']
    
    twn_group_2 = ['sta2_allfactor_xjp_513_0','sta2_all_xjp_513_all_fact3_c20',
                   'sta2_all_xjp_513_all_fact4_c20','sta2_all_xjp_513_all_fact4_c50']
    
    usa_group_13 = ['pv13_h_min2_3000_sector','pv13_r2_min20_3000_sector','pv13_r2_min2_3000_sector',
                    'pv13_r2_min2_3000_sector', 'pv13_h_min2_focused_pureplay_3000_sector']
    
    usa_group_1 = ['sta1_top3000c50','sta1_allc20','sta1_allc10','sta1_top3000c20','sta1_allc5']
    
    usa_group_2 = ['sta2_top3000_fact3_c50','sta2_top3000_fact4_c20','sta2_top3000_fact4_c10']
    
    usa_group_6 = ['mdl10_group_name']
    
    asi_group_13 = ['pv13_20_minvol_1m_sector', 'pv13_5_f3_g2_minvol_1m_sector', 'pv13_10_f3_g2_minvol_1m_sector',
                    'pv13_2_f4_g3_minvol_1m_sector', 'pv13_10_minvol_1m_sector', 'pv13_5_minvol_1m_sector']
    
    asi_group_1 = ['sta1_allc50', 'sta1_allc10', 'sta1_minvol1mc50','sta1_minvol1mc20',
                   'sta1_minvol1m_normc20', 'sta1_minvol1m_normc50']
    
    jpn_group_1 = ['sta1_alljpn_513_c5', 'sta1_alljpn_513_c50', 'sta1_alljpn_513_c2', 'sta1_alljpn_513_c20']
    
    jpn_group_2 = ['sta2_top2000_jpn_513_top2000_fact3_c20', 'sta2_all_jpn_513_all_fact1_c5',
                   'sta2_allfactor_jpn_513_9', 'sta2_all_jpn_513_all_fact1_c10']
    
    jpn_group_13 = ['pv13_2_minvol_1m_sector', 'pv13_2_f4_g3_minvol_1m_sector', 'pv13_10_minvol_1m_sector',
                    'pv13_10_f3_g2_minvol_1m_sector', 'pv13_all_delay_1_parent', 'pv13_all_delay_1_level']
    
    kor_group_13 = ['pv13_10_f3_g2_minvol_1m_sector', 'pv13_5_minvol_1m_sector', 'pv13_5_f3_g2_minvol_1m_sector',
                    'pv13_2_minvol_1m_sector', 'pv13_20_minvol_1m_sector', 'pv13_2_f4_g3_minvol_1m_sector']
    
    kor_group_1 = ['sta1_allc20','sta1_allc50','sta1_allc2','sta1_allc10','sta1_minvol1mc50',
                   'sta1_allxjp_513_c10', 'sta1_top2000xjp_513_c50']
    
    kor_group_2 =['sta2_all_xjp_513_all_fact1_c50','sta2_top2000_xjp_513_top2000_fact2_c50',
                  'sta2_all_xjp_513_all_fact4_c50','sta2_all_xjp_513_all_fact4_c5']
    
    eur_group_13 = ['pv13_5_sector', 'pv13_2_sector', 'pv13_v3_3l_scibr', 'pv13_v3_2l_scibr', 'pv13_2l_scibr',
                    'pv13_52_sector', 'pv13_v3_6l_scibr', 'pv13_v3_4l_scibr', 'pv13_v3_1l_scibr']
    
    eur_group_1 = ['sta1_allc10', 'sta1_allc2', 'sta1_top1200c2', 'sta1_allc20', 'sta1_top1200c10']
    
    eur_group_2 = ['sta2_top1200_fact3_c50','sta2_top1200_fact3_c20','sta2_top1200_fact4_c50']
    
    glb_group_13 = ["pv13_10_f2_g3_sector", "pv13_2_f3_g2_sector", "pv13_2_sector", "pv13_52_all_delay_1_sector"]
        
    glb_group_1 = ['sta1_allc20', 'sta1_allc10', 'sta1_allc50', 'sta1_allc5']
    
    glb_group_2 = ['sta2_all_fact4_c50', 'sta2_all_fact4_c20', 'sta2_all_fact3_c20', 'sta2_all_fact4_c10']
    
    glb_group_13 = ['pv13_2_sector', 'pv13_10_sector', 'pv13_3l_scibr', 'pv13_2l_scibr', 'pv13_1l_scibr',
                    'pv13_52_minvol_1m_all_delay_1_sector','pv13_52_minvol_1m_sector','pv13_52_minvol_1m_sector'] 
    
    amr_group_13 = ['pv13_4l_scibr', 'pv13_1l_scibr', 'pv13_hierarchy_min51_f1_sector',
                    'pv13_hierarchy_min2_600_sector', 'pv13_r2_min2_sector', 'pv13_h_min20_600_sector']
    
    #bps_group = "bucket(rank(fnd28_value_05480), range='0.1, 1, 0.1')"
    #pb_group = "bucket(rank(close/fnd28_value_05480), range='0.1, 1, 0.1')"
    cap_group = "bucket(rank(cap), range='0.1, 1, 0.1')"
    asset_group = "bucket(rank(assets),range='0.1, 1, 0.1')"
    sector_cap_group = "bucket(group_rank(cap, sector),range='0.1, 1, 0.1')"
    sector_asset_group = "bucket(group_rank(assets, sector),range='0.1, 1, 0.1')"

    vol_group = "bucket(rank(ts_std_dev(returns,20)),range = '0.1, 1, 0.1')"

    liquidity_group = "bucket(rank(close*volume),range = '0.1, 1, 0.1')"

    groups = ["market","sector", "industry", "subindustry",
            cap_group, asset_group, sector_cap_group, sector_asset_group, vol_group, liquidity_group]

    if region == "CHN":
        groups += chn_group_13 + chn_group_1 + chn_group_2  
    if region == "TWN":
        groups += twn_group_13 + twn_group_1 + twn_group_2 
    if region == "ASI":
        groups += asi_group_13 + asi_group_1 
    if region == "USA":
        groups += usa_group_13 + usa_group_1 + usa_group_2  
    if region == "HKG":
        groups += hkg_group_13 + hkg_group_1 + hkg_group_2 
    if region == "KOR":
        groups += kor_group_13 + kor_group_1 + kor_group_2 
    if region == "EUR": 
        groups += eur_group_13 + eur_group_1 + eur_group_2 
    if region == "GLB":
        groups += glb_group_13 + glb_group_1 + glb_group_2
    if region == "AMR":
        groups += amr_group_13 
    if region == "JPN":
        groups += jpn_group_1 + jpn_group_2 + jpn_group_13 
        
    for group in groups:
        if op.startswith("group_vector"):
            for vector in vectors:
                alpha = "%s(%s,%s,densify(%s))"%(op, field, vector, group)
                output.append(alpha)
        elif op.startswith("group_percentage"):
            alpha = "%s(%s,densify(%s),percentage=0.5)"%(op, field, group)
            output.append(alpha)
        else:
            alpha = "%s(%s,densify(%s))"%(op, field, group)
            output.append(alpha)
        
    return output


def trade_when_factory(op,field,region):
    output = []
    open_events = ["ts_arg_max(volume, 5) == 0", "ts_corr(close, volume, 20) < 0",
                   "ts_corr(close, volume, 5) < 0", "ts_mean(volume,10)>ts_mean(volume,60)",
                   "group_rank(ts_std_dev(returns,60), sector) > 0.7", "ts_zscore(returns,60) > 2",
                   "ts_arg_min(volume, 5) > 3",
                   "ts_std_dev(returns, 5) > ts_std_dev(returns, 20)",
                   "ts_arg_max(close, 5) == 0", "ts_arg_max(close, 20) == 0",
                   "ts_corr(close, volume, 5) > 0", "ts_corr(close, volume, 5) > 0.3", "ts_corr(close, volume, 5) > 0.5",
                   "ts_corr(close, volume, 20) > 0", "ts_corr(close, volume, 20) > 0.3", "ts_corr(close, volume, 20) > 0.5",
                   "ts_regression(returns, %s, 5, lag = 0, rettype = 2) > 0"%field,
                   "ts_regression(returns, %s, 20, lag = 0, rettype = 2) > 0"%field,
                   "ts_regression(returns, ts_step(20), 20, lag = 0, rettype = 2) > 0",
                   "ts_regression(returns, ts_step(5), 5, lag = 0, rettype = 2) > 0"]

    exit_events = ["abs(returns) > 0.1", "-1"]

    usa_events = ["rank(rp_css_business) > 0.8", "ts_rank(rp_css_business, 22) > 0.8", "rank(vec_avg(mws82_sentiment)) > 0.8",
                  "ts_rank(vec_avg(mws82_sentiment),22) > 0.8", "rank(vec_avg(nws48_ssc)) > 0.8",
                  "ts_rank(vec_avg(nws48_ssc),22) > 0.8", "rank(vec_avg(mws50_ssc)) > 0.8", "ts_rank(vec_avg(mws50_ssc),22) > 0.8",
                  "ts_rank(vec_sum(scl12_alltype_buzzvec),22) > 0.9", "pcr_oi_270 < 1", "pcr_oi_270 > 1",]

    asi_events = ["rank(vec_avg(mws38_score)) > 0.8", "ts_rank(vec_avg(mws38_score),22) > 0.8"]

    eur_events = ["rank(rp_css_business) > 0.8", "ts_rank(rp_css_business, 22) > 0.8",
                  "rank(vec_avg(oth429_research_reports_fundamental_keywords_4_method_2_pos)) > 0.8",
                  "ts_rank(vec_avg(oth429_research_reports_fundamental_keywords_4_method_2_pos),22) > 0.8",
                  "rank(vec_avg(mws84_sentiment)) > 0.8", "ts_rank(vec_avg(mws84_sentiment),22) > 0.8",
                  "rank(vec_avg(mws85_sentiment)) > 0.8", "ts_rank(vec_avg(mws85_sentiment),22) > 0.8",
                  "rank(mdl110_analyst_sentiment) > 0.8", "ts_rank(mdl110_analyst_sentiment, 22) > 0.8",
                  "rank(vec_avg(nws3_scores_posnormscr)) > 0.8",
                  "ts_rank(vec_avg(nws3_scores_posnormscr),22) > 0.8",
                  "rank(vec_avg(mws36_sentiment_words_positive)) > 0.8",
                  "ts_rank(vec_avg(mws36_sentiment_words_positive),22) > 0.8"]

    glb_events = ["rank(vec_avg(mdl109_news_sent_1m)) > 0.8",
                  "ts_rank(vec_avg(mdl109_news_sent_1m),22) > 0.8",
                  "rank(vec_avg(nws20_ssc)) > 0.8",
                  "ts_rank(vec_avg(nws20_ssc),22) > 0.8",
                  "vec_avg(nws20_ssc) > 0",
                  "rank(vec_avg(nws20_bee)) > 0.8",
                  "ts_rank(vec_avg(nws20_bee),22) > 0.8",
                  "rank(vec_avg(nws20_qmb)) > 0.8",
                  "ts_rank(vec_avg(nws20_qmb),22) > 0.8"]

    chn_events = ["rank(vec_avg(oth111_xueqiunaturaldaybasicdivisionstat_senti_conform)) > 0.8",
                  "ts_rank(vec_avg(oth111_xueqiunaturaldaybasicdivisionstat_senti_conform),22) > 0.8",
                  "rank(vec_avg(oth111_gubanaturaldaydevicedivisionstat_senti_conform)) > 0.8",
                  "ts_rank(vec_avg(oth111_gubanaturaldaydevicedivisionstat_senti_conform),22) > 0.8",
                  "rank(vec_avg(oth111_baragedivisionstat_regi_senti_conform)) > 0.8",
                  "ts_rank(vec_avg(oth111_baragedivisionstat_regi_senti_conform),22) > 0.8"]

    kor_events = ["rank(vec_avg(mdl110_analyst_sentiment)) > 0.8",
                  "ts_rank(vec_avg(mdl110_analyst_sentiment),22) > 0.8",
                  "rank(vec_avg(mws38_score)) > 0.8",
                  "ts_rank(vec_avg(mws38_score),22) > 0.8"]

    twn_events = ["rank(vec_avg(mdl109_news_sent_1m)) > 0.8",
                  "ts_rank(vec_avg(mdl109_news_sent_1m),22) > 0.8",
                  "rank(rp_ess_business) > 0.8",
                  "ts_rank(rp_ess_business,22) > 0.8"]

    for oe in open_events:
        for ee in exit_events:
            alpha = "%s(%s, %s, %s)"%(op, oe, field, ee)
            output.append(alpha)
    return output


def submission_reconnect_sleep_seconds(reconnect_count, short_reconnects=2, short_sleep=300, long_sleep=3600):
    if reconnect_count <= short_reconnects:
        return short_sleep
    return long_sleep


def check_submission(
    alpha_bag,
    gold_bag,
    start,
    short_reconnects=2,
    short_sleep=300,
    long_sleep=3600,
):
    depot = []
    s = login()
    reconnect_count = 0
    for idx, g in enumerate(alpha_bag):
        if idx < start:
            continue
        if idx % 5 == 0:
            print(idx)
        if idx > 0 and idx % 200 == 0:
            s = login()
        #print(idx)
        pc = get_check_submission(s, g)
        if pc == "sleep":
            reconnect_count += 1
            wait_seconds = submission_reconnect_sleep_seconds(
                reconnect_count,
                short_reconnects=short_reconnects,
                short_sleep=short_sleep,
                long_sleep=long_sleep,
            )
            print(f"platform disconnected; wait {wait_seconds} seconds before reconnect")
            sleep(wait_seconds)
            s = login()
            alpha_bag.append(g)
        elif pc != pc:
            # pc is nan
            print("check self-corrlation error")
            reconnect_count += 1
            wait_seconds = submission_reconnect_sleep_seconds(
                reconnect_count,
                short_reconnects=short_reconnects,
                short_sleep=short_sleep,
                long_sleep=long_sleep,
            )
            sleep(wait_seconds)
            s = login()
            alpha_bag.append(g)
        elif pc == "fail":
            continue
        elif pc == "error":
            depot.append(g)
        else:
            print(g)
            gold_bag.append((g, pc))
    print(depot)
    return gold_bag

def get_check_submission(s, alpha_id, max_retries=3, retry_sleep=5):
    attempts = 0
    while True:
        try:
            result = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/check")
        except (requests.exceptions.RequestException, OSError) as exc:
            attempts += 1
            print(f"check connection error for {alpha_id}: {exc}; retry {attempts}/{max_retries}")
            if attempts >= max_retries:
                return "sleep"
            time.sleep(retry_sleep)
            continue

        if "retry-after" in result.headers:
            time.sleep(float(result.headers["Retry-After"]))
        else:
            break
    try:
        if result.json().get("is", 0) == 0:
            print("logged out")
            return "sleep"
        checks_df = pd.DataFrame(
                result.json()["is"]["checks"]
        )
        pc = checks_df[checks_df.name == "PROD_CORRELATION"]["value"].values[0]
        if not any(checks_df["result"] == "FAIL"):
            return pc
        else:
            return "fail"
    except:
        print("catch: %s"%(alpha_id))
        return "error"
    

def view_alphas(gold_bag):
    s = login()
    sharp_list = []
    for gold, pc in gold_bag:

        triple = locate_alpha(s, gold)
        info = [triple[0], triple[2], triple[3], triple[4], triple[5], triple[6], triple[1]]
        info.append(pc)
        sharp_list.append(info)

    sharp_list.sort(reverse=True, key = lambda x : x[1])
    for i in sharp_list:
        print(i)
 
def locate_alpha(s, alpha_id):
    while True:
        alpha = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id)
        if "retry-after" in alpha.headers:
            time.sleep(float(alpha.headers["Retry-After"]))
        else:
            break
    string = alpha.content.decode('utf-8')
    metrics = json.loads(string)
    #print(metrics["regular"]["code"])
    
    dateCreated = metrics["dateCreated"]
    sharpe = metrics["is"]["sharpe"]
    fitness = metrics["is"]["fitness"]
    turnover = metrics["is"]["turnover"]
    margin = metrics["is"]["margin"]
    decay = metrics["settings"]["decay"]
    exp = metrics['regular']['code']
    
    triple = [alpha_id, exp, sharpe, turnover, fitness, margin, dateCreated, decay]
    return triple



# some factory for other operators 
def vector_factory(op, field):
    output = []
    vectors = ["cap"]
    
    for vector in vectors:
    
        alpha = "%s(%s, %s)"%(op, field, vector)
        output.append(alpha)
    
    return output
 
 
def ts_comp_factory(op, field, factor, paras):
    output = []
    #l1, l2 = [3, 5, 10, 20, 60, 120, 240], paras
    l1, l2 = [5, 22, 66, 240], paras
    comb = list(product(l1, l2))
    
    for day,para in comb:
        alpha = ""
        if type(para) == float:
            alpha = "%s(%s, %d, %s=%.1f)"%(op, field, day, factor, para)
        elif type(para) == int:
            alpha = "%s(%s, %d, %s=%d)"%(op, field, day, factor, para)
            
        output.append(alpha)
    
    return output
 
def twin_field_factory(op, field, fields):
    
    output = []
    #days = [3, 5, 10, 20, 60, 120, 240]
    days = [5, 22, 66, 240]
    outset = list(set(fields) - set([field]))
    
    for day in days:
        for counterpart in outset:
            alpha = "%s(%s, %s, %d)"%(op, field, counterpart, day)
            output.append(alpha)
    
    return output
 
def login_hk():
    """Backward-compatible alias for the standard WorldQuant login.

    Older notebooks used this name for a separate environment-variable login
    path. The project now uses ``credentials.json`` through ``login()`` so all
    sessions share the same credential loading, proxy handling, and error path.
    """
    return login()


def refresh_data_catalog(s, **kwargs):
    from .catalog_cache import refresh_catalog

    return refresh_catalog(s, **kwargs)


if __name__ == "__main__":
    login()
