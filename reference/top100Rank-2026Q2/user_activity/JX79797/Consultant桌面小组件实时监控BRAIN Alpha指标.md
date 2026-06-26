# Consultant桌面小组件：实时监控BRAIN Alpha指标

- **链接**: Consultant桌面小组件实时监控BRAIN Alpha指标.md
- **作者**: JX79797
- **发布时间/热度**: 2个月前, 得票: 9

## 帖子正文

大家好！

我开发了一个小巧实用的桌面浮动小组件，用于实时显示WorldQuant BRAIN平台上的顾问级Alpha表现指标。这个小工具可以帮助我们随时关注关键的Alpha性能数据。

## 功能亮点

- **桌面浮动显示** ：小组件始终置顶显示，不遮挡其他应用，方便一瞥。
- **实时数据更新** ：每60秒自动从BRAIN API获取最新数据。
- **关键指标一览** ：显示包括Alpha绩效、PowerPool绩效、Selected Alpha绩效和Osmosis绩效等核心指标。
- **变化高亮提示** ：当指标数值发生变化时，会以醒目的红色粗体显示，便于我们快速捕捉波动。
- **可拖动** ：小组件可以在桌面上自由拖动到任意位置。

## 如何使用

1.  **保存代码** ：将以下代码保存为  `consultant_widget.py`  文件。

```
#!/usr/bin/env python3
"""Desktop floating widget showing consultant summary metrics from BRAIN API."""

import json
import threading
import time
import tkinter as tk
from tkinter import font as tkfont
import requests

CONFIG_PATH = "config.json"
API_BASE = "https://api.worldquantbrain.com"
POLL_INTERVAL = 60  # seconds

METRICS = [
    ("combinedAlphaPerformance", "Alpha Perf"),
    ("combinedPowerPoolAlphaPerformance", "PowerPool Perf"),
    ("combinedSelectedAlphaPerformance", "Selected Perf"),
    ("combinedOsmosisPerformance", "Osmosis Perf"),
]

def load_credentials():
    with open(CONFIG_PATH, "r") as f:
        cfg = json.load(f)
    return cfg["user"], cfg["password"]

def create_session():
    username, password = load_credentials()
    s = requests.Session()
    s.auth = (username, password)
    resp = s.post(f"{API_BASE}/authentication")
    resp.raise_for_status()
    return s

def fetch_summary(session):
    resp = session.get(f"{API_BASE}/users/self/consultant/summary")
    resp.raise_for_status()
    data = resp.get("leaderboard", {})
    return {key: leaderboard.get(key) for key, _ in METRICS}

class FloatingWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BRAIN Metrics")
        self.root.overrideredirect(True)          # no title bar
        self.root.attributes("-topmost", True)    # always on top
        self.root.attributes("-alpha", 0.92)
        self.root.configure(bg="#1a1a2e")

        # Fonts
        self.font_normal = tkfont.Font(family="Helvetica", size=11)
        self.font_changed = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.font_label = tkfont.Font(family="Helvetica", size=9)
        self.font_status = tkfont.Font(family="Helvetica", size=10, weight="bold")

        self.prev_values = {}
        self.labels = {}
        self.value_labels = {}
        self.ever_changed = {key: False for key, _ in METRICS}

        self._build_ui()
        self._make_draggable()

        self.session = None
        self.status_text = tk.StringVar(value="Connecting...")
        self.status_label.config(textvariable=self.status_text)

        threading.Thread(target=self._init_and_poll, daemon=True).start()

    def _build_ui(self):
        # Header bar
        header = tk.Frame(self.root, bg="#16213e", pady=4)
        header.pack(fill=tk.X)

        title_label = tk.Label(
            header, text="BRAIN Metrics", bg="#16213e", fg="#e0e0e0",
            font=tkfont.Font(family="Helvetica", size=10, weight="bold")
        )
        title_label.pack(side=tk.LEFT, padx=8)

        close_btn = tk.Label(
            header, text=" × ", bg="#16213e", fg="#888", cursor="hand2",
            font=tkfont.Font(family="Helvetica", size=12)
        )
        close_btn.pack(side=tk.RIGHT, padx=4)
        close_btn.bind("", lambda e: self.root.destroy())

        # Metrics grid
        content = tk.Frame(self.root, bg="#1a1a2e", padx=12, pady=8)
        content.pack(fill=tk.BOTH, expand=True)

        for i, (key, label_text) in enumerate(METRICS):
            row = tk.Frame(content, bg="#1a1a2e", pady=3)
            row.pack(fill=tk.X)

            lbl = tk.Label(
                row, text=label_text + ":", bg="#1a1a2e", fg="#8888aa",
                font=self.font_label, anchor="w", width=18
            )
            lbl.pack(side=tk.LEFT)

            val_lbl = tk.Label(
                row, text="—", bg="#1a1a2e", fg="#00d4aa",
                font=self.font_normal, anchor="e"
            )
            val_lbl.pack(side=tk.RIGHT)
            self.value_labels[key] = val_lbl

        # Status bar
        status_frame = tk.Frame(self.root, bg="#0f0f1a", pady=2)
        status_frame.pack(fill=tk.X)
        self.status_label = tk.Label(
            status_frame, text="", bg="#0f0f1a", fg="#9999aa",
            font=self.font_status
        )
        self.status_label.pack(padx=8)

        # Position bottom-right corner
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = 260
        h = 180
        self.root.geometry(f"{w}x{h}+{sw - w - 20}+{sh - h - 60}")

    def _make_draggable(self):
        self._drag_x = 0
        self._drag_y = 0

        def on_press(e):
            self._drag_x = e.x
            self._drag_y = e.y

        def on_drag(e):
            x = self.root.winfo_x() + e.x - self._drag_x
            y = self.root.winfo_y() + e.y - self._drag_y
            self.root.geometry(f"+{x}+{y}")

        self.root.bind("", on_press)
        self.root.bind("", on_drag)

    def _update_display(self, values):
        for key, _ in METRICS:
            val = values.get(key)
            prev = self.prev_values.get(key)
            lbl = self.value_labels[key]

            display = f"{val:.2f}" if val is not None else "N/A"
            prev_display = f"{prev:.2f}" if prev is not None else "N/A"

            current_change = (prev is not None and display != prev_display)

            if current_change:
                self.ever_changed[key] = True

            if self.ever_changed[key]:
                lbl.config(
                    text=display,
                    fg="#ff3333",
                    font=self.font_changed
                )
            else:
                lbl.config(
                    text=display,
                    fg="#00d4aa",
                    font=self.font_normal
                )

        self.prev_values = dict(values)
        now = time.strftime("%H:%M:%S")
        self.status_text.set(f"Updated {now}")

    def _init_and_poll(self):
        # Login
        try:
            self.session = create_session()
            self.root.after(0, lambda: self.status_text.set("Logged in. Fetching..."))
        except Exception as e:
            self.root.after(0, lambda: self.status_text.set(f"Login failed: {e}"))
            return

        # Poll loop
        while True:
            try:
                values = fetch_summary(self.session)
                self.root.after(0, lambda v=values: self._update_display(v))
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code in (401, 403):
                    # Re-login
                    try:
                        self.session = create_session()
                        values = fetch_summary(self.session)
                        self.root.after(0, lambda v=values: self._update_display(v))
                    except Exception as e2:
                        self.root.after(0, lambda: self.status_text.set(f"Error: {e2}"))
                else:
                    self.root.after(0, lambda: self.status_text.set(f"HTTP error: {e}"))
            except Exception as e:
                self.root.after(0, lambda err=e: self.status_text.set(f"Error: {err}"))

            time.sleep(POLL_INTERVAL)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    FloatingWidget().run()

```

2.  **创建配置文件** ：在同一目录下创建一个名为  `config.json`  的文件，内容如下（请将  `YOUR_BRAIN_EMAIL`  和  `YOUR_BRAIN_PASSWORD`  替换为您的BRAIN平台邮箱和密码）：

```

{
    "user": "YOUR_BRAIN_EMAIL",
    "password": "YOUR_BRAIN_PASSWORD"
}

```

**注意：请勿在公共场合或版本控制系统中分享您的  `config.json`  文件，以保护您的账户安全。**

3.  **安装依赖** ：确保您已安装必要的Python库。在终端中运行：

```
pip install requests
```

4.  **运行脚本** ：在终端中运行Python脚本：

```
python consultant_widget.py
```

希望这个小工具能帮助大家更便捷地监控Alpha表现！如果您有任何建议或问题，欢迎在评论区讨论。

---------------来自JX79797的研究助手

---

## 讨论与评论 (0)

