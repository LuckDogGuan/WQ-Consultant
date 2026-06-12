# WorldQuant Consultant GUI Standalone Project

这是一个独立的 WorldQuant Consultant GUI 交互系统，提供完备的可视化操作界面，用于阿尔法模拟、回测、提交前检查、相关性计算以及本地数据目录的管理。

## Git 初始化与项目独立说明

根据安全规范，本项目已作为独立的 Git 仓库进行管理。请在操作 Git 时遵循以下步骤：

### 1. 初始化 Git 仓库
进入 `consultant/gui` 文件夹，并运行初始化命令：
```bash
git init
```

### 2. 检查 .gitignore 配置
为保证安全，避免将缓存数据库、任务日志以及个人敏感信息提交至代码库，项目根目录下已配置 `.gitignore`。
其忽略规则如下：
```text
# 忽略本地 SQLite 数据库与数据目录快照
data/

# 忽略系统后台运行产生的日志
logs/

# 忽略 Python 字节码缓存与运行环境
__pycache__/
*.pyc
.venv/
venv/
```
在执行代码提交前，请先使用 `git status` 检查，确保无多余的本地缓存或敏感信息泄露。

### 3. 代码提交指引
请仅提交代码改动，严禁使用 `git add -A` 或 `git add .`。
推荐提交步骤：
```bash
# 查看本地变动文件
git status

# 仅暂存指定修改的文件
git add app/static/style.css app/templates/settings.html

# 提交至本地仓库
git commit -m "feat: optimize settings cascade with day1 scope mapping"
```

---

## 快速启动指南

### 1. 安装依赖
确保已安装运行本项目所需的第三方库：
```bash
pip install -r requirements.txt
```

### 2. 配置 WorldQuant Brain 凭据
启动服务后，直接在浏览器中访问“系统设置”页面：
- 在 WQ 凭据配置中输入您的 WorldQuant Brain 账户和密码并点击保存（密码已支持明密文切换）。
- 也可点击“一键从 credentials.json 导入”从外部快速读取。

### 3. 运行 GUI 服务
直接在 `gui/` 目录下运行：
```bash
python run_gui.py
```
或在顾问项目根目录下运行：
```bash
python gui/run_gui.py
```
启动后在浏览器打开链接：`http://127.0.0.1:8765`。

### 4. 数据目录初始化
初次使用时，本系统会自动从全局 `data_catalog` 目录克隆所需的数据子集进行隔离运行。
您也可以直接在“数据目录”页面选择特定的地区与股票池，一键发起“刷新同步该地区数据”任务，后台将自动连接 WQ API 拉取最新数据集并建立索引。
