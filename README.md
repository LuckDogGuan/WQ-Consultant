# WorldQuant Consultant GUI

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org)

这是一个为 WorldQuant Brain 工作流设计的本地 Web 交互图形界面（基于 FastAPI + Jinja2 + Vanilla CSS），提供可视化模拟回测任务调度、相关性诊断与自动命名、提交前三线程多并发校验等核心辅助工具，旨在极大提升 Alpha 挖掘与提交流程的效率。

---

## 🎯 核心功能特性

*   🔐 **安全单用户登录**
    *   采用管理员密码加盐 SHA256 哈希安全认证。
    *   支持一键从 `credentials.json` 自动导入 WorldQuant 凭据。
    *   可通过环境变量 `WQ_GUI_ADMIN_PASSWORD` 在部署时灵活重置或指定初始密码。
*   📂 **本地隔离数据目录**
    *   首次启动时自动克隆所需的 `data_catalog` 与相关性缓存（与全局物理隔离，避免冲突）。
    *   自带过期机制：本地缓存满 7 天时，页面将提供友好的同步/更新提醒。
*   🔄 **三阶段回测串行调度**
    *   支持输入多个数据集 ID，自动串行运行一阶 FO、二阶 SO、三阶 TH 阶段回测。
    *   自带前缀自动推导与剪枝（Prune）逻辑，智能推荐 Neutralization 效率评分最高项，且支持断点续跑。
*   🛑 **限额限时挂起拦截**
    *   在每个 Pool 回测和提交前的 API 请求中，自动校验当前额度（4500 限额限制）和系统禁用时间窗口。
    *   达到限制后自动切换至挂起（Pending）状态，避免强行中断任务导致数据丢失。
*   🏷️ **相关性诊断与智能重命名**
    *   自动对比平台 OS 历史因子 Returns 缓存，智能计算 PPA / RA / ATOM 因子相关性指标。
    *   基于相关性表现自动推荐符合规范的因子命名，并在界面提供二次确认与手动微调。
*   🧵 **三线程并发校验 (Check Submission)**
    *   自动从“回测结果”、“相关性优秀候选”以及“手动粘贴”中构建待检队列。
    *   采用多线程并发执行向 WQ Brain 提交前检查，检测结果持久化写入 SQLite，并支持直观的分页与过滤查看。
*   📝 **任务隔离日志输出**
    *   采用 Thread-local 机制将并发任务各自的 `stdout`/`stderr` 重定向至独立日志文件 `logs/job_{job_id}.log`。
    *   前端支持通过 AJAX 异步实时滚动获取并展示日志信息，互不干扰。

---

## 📂 目录及存储结构

```text
gui/
├── app/                  # Web 服务核心代码目录
│   ├── auth.py          # 登录认证与 Session 校验逻辑
│   ├── main.py          # FastAPI 路由、页面渲染与 API 定义
│   ├── job_runner.py    # 任务调度与 Thread-local 日志重定向
│   ├── storage.py       # 本地 SQLite 数据访问层
│   └── templates/       # HTML 界面模板 (Jinja2)
├── consultant_core/      # 核心回测与相关性算法库
├── data/                 # 本地持久化数据 (Git 已忽略)
│   ├── gui.db           # SQLite 数据库 (保存设置、任务进度、Alpha 归档、check 结果等)
│   ├── catalog/         # 本地克隆的数据目录快照
│   └── correlation/     # 相关性计算本地缓存目录
├── logs/                 # 日志记录目录 (Git 已忽略)
│   ├── gui.log          # 系统运行主日志
│   └── job_*.log        # 各后台异步任务的独立日志
├── requirements.txt      # 依赖包列表
├── check_env.py          # 部署环境检测脚本
└── run_gui.py            # GUI 启动入口脚本
```

---

## ⚙️ 环境准备与一键检测

### 1. 安装项目依赖

确保安装了运行本项目所需的第三方库：

```powershell
python -m pip install -r requirements.txt
```

*(如果需要运行测试用例，可额外安装 `pytest`)*

### 1.1 本地 webdatascope 数据读取说明

GUI 主程序使用 Python 运行。`data/webdatascope/` 下的 `info_data.bin` 是压缩的 msgpack 数据，首次解析需要本机可用 `node`，用于执行同目录保留的 `pako.min.js` 与 `msgpack.min.js` 解码库。解析成功后会生成 `data/webdatascope/webdatascope_info.json` 缓存；后续 Python 会优先直接读取这个 JSON 缓存，原始 `.bin` 和 `.js` 文件不会删除。

### 2. 运行一键检测脚本 🛡️

项目内置了环境自检程序 [check_env.py](file:///D:/code/WorldQuant%20Brain/consultant/gui/check_env.py)，在首次运行或部署至服务器前，强烈建议运行此脚本进行一键体检：

```powershell
python check_env.py
```

该脚本将自动帮您检测以下项目：
- Python 版本（建议 $\ge 3.8$）
- 各第三方依赖项（`fastapi`, `pandas`, `requests` 等）的安装完整性
- 核心算法包 [consultant_core](file:///D:/code/WorldQuant%20Brain/consultant/gui/consultant_core) 的导入状态
- 数据目录 `data/` 和日志目录 `logs/` 的创建与读写权限
- 与 WorldQuant Brain 官网 API (`api.worldquantbrain.com`) 的网络延迟及代理配置
- 数据库或外部文件中的 WQ Brain 凭据状态
- 安全环境变量设置（是否配置了管理员初始密码环境变量）

---

## 🚀 快速运行与使用说明

### 1. 启动服务

直接在当前目录下运行启动入口脚本 [run_gui.py](file:///D:/code/WorldQuant%20Brain/consultant/gui/run_gui.py)：

```powershell
python run_gui.py
```

*   **默认访问链接**：[http://127.0.0.1:8765](http://127.0.0.1:8765)
*   **初始管理员登录密码**：`admin`

### 2. 常用启动参数

启动脚本支持以下命令行参数，便于在不同场景下部署：

```powershell
# 1. 仅启动服务，禁止自动拉起本地浏览器（适合 Linux / SSH 远程部署）
python run_gui.py --no-browser

# 2. 绑定到指定端口（例如 9000）
python run_gui.py --port 9000

# 3. 开启局域网/外网访问
python run_gui.py --host 0.0.0.0
```

### 3. 配置 WorldQuant 凭据

成功登录后，系统会自动引导或在左侧导航进入 **“系统设置”** 页面：
- **手动输入**：在 WQ 凭证配置区输入您的 WorldQuant Brain 账号（Email）与密码，支持明密文切换。
- **一键导入**：如果在父项目根目录下已配置过 `credentials.json`，可点击 **“一键从 credentials.json 导入”** 按钮实现秒级自动同步。

---

## 🔒 独立 Git 仓库管理与提交流程

根据安全规范，本项目作为独立的 Git 仓库进行管理。**为避免将敏感凭据、缓存数据库、大型快照数据及大量本地日志误提交至公共代码库**，请在操作 Git 时务必遵循以下步骤：

### 1. 遵守 `.gitignore` 过滤规则

根目录下的 `.gitignore` 已配置以下过滤策略：
- `data/`（过滤 SQLite 数据库与数据目录快照，防止本地凭证与敏感 Alpha 泄露）
- `logs/`（过滤运行日志与并发任务日志）
- `__pycache__/` 及其他 Python 编译缓存文件
- 虚拟环境目录（`.venv/`, `venv/` 等）

### 2. 严禁粗暴提交

**严禁** 在根目录下直接运行 `git add -A` 或 `git add .`。请使用显式、精确的暂存指令。

推荐的标准提交提交流程：
```bash
# 1. 查看本地变动的文件
git status

# 2. 仅手动暂存需要修改的业务代码
git add app/static/style.css app/templates/settings.html

# 3. 提交描述需清晰规范
git commit -m "feat: optimize settings cascade with day1 scope mapping"
```

---

## 🛠️ 生产环境部署建议

1.  **修改初始密码**：在服务器部署前，强烈建议设置环境变量 `WQ_GUI_ADMIN_PASSWORD` 写入强密码，系统检测到该变量后会抛弃默认密码 `admin`。
2.  **配置反向代理与 HTTPS**：推荐使用 Nginx 作为反向代理，并配置 SSL/TLS 证书。系统已自带安全保护：在 HTTPS 访问下，Session Cookie 会自动被标记为 `Secure`。
3.  **进程守候**：使用 Systemd、PM2 或 Docker 容器托管运行，以实现崩溃自启与后台持久运行：
    ```bash
    # Systemd 运行示例命令行
    python run_gui.py --host 0.0.0.0 --port 8765 --no-browser
    ```
