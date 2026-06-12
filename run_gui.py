from __future__ import annotations

import argparse
import sys
import threading
import time
import webbrowser
from pathlib import Path


GUI_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = GUI_ROOT.parent
SRC_ROOT = PROJECT_ROOT / "src"

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="启动 WorldQuant Consultant GUI")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址；远程部署可用 0.0.0.0")
    parser.add_argument("--port", type=int, default=8765, help="监听端口")
    parser.add_argument("--no-browser", action="store_true", help="启动后不自动打开浏览器")
    return parser.parse_args()


def open_browser(url: str) -> None:
    time.sleep(1.2)
    webbrowser.open(url)


def main() -> None:
    args = parse_args()
    try:
        import uvicorn
    except ModuleNotFoundError:
        print("缺少 GUI 依赖，请先运行：python -m pip install -r gui/requirements.txt")
        raise

    url = f"http://127.0.0.1:{args.port}"
    if not args.no_browser:
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()

