from __future__ import annotations

import argparse
import sys
import threading
import time
import webbrowser
from pathlib import Path


import socket

GUI_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = GUI_ROOT.parent
SRC_ROOT = PROJECT_ROOT / "src"

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def get_local_ip() -> str:
    """获取本机的局域网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


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

    try:
        from app.logging_config import configure_logging
        configure_logging()
    except Exception:
        pass

    local_ip = get_local_ip()
    
    # 动态确定要打开的链接
    if args.host == "0.0.0.0":
        url = f"http://{local_ip}:{args.port}"
        print(f"\n============================================================")
        print(f"  服务已绑定至 0.0.0.0，您可以通过以下链接进行访问:")
        print(f"  -> 本地回环: http://127.0.0.1:{args.port}")
        print(f"  -> 局域网/公网 IP: http://{local_ip}:{args.port}")
        print(f"============================================================\n")
    else:
        url = f"http://{args.host}:{args.port}"
        print(f"\n============================================================")
        print(f"  服务已启动，您可以通过以下链接进行访问:")
        print(f"  -> 访问地址: {url}")
        if args.host == "127.0.0.1":
            print(f"  -> 提示: 如需局域网或远程访问，请使用 --host 0.0.0.0 启动")
        print(f"============================================================\n")

    if not args.no_browser:
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()

