# WorldQuant Consultant GUI v0.1

这是一个为 WorldQuant Brain 工作流设计的本地 Web 交互图形界面（基于 FastAPI + Jinja2 + Vanilla CSS），旨在提供可视化回测任务调度、相关性评定改名以及 check_submission 三线程检查等辅助工具。

## 功能特性

- **安全单用户登录**：支持管理员密码加盐 SHA256 哈希认证。支持从 `credentials.json` 自动导入 WorldQuant 凭据及通过环境变量 `WQ_GUI_ADMIN_PASSWORD` 重置初始密码。
- **本地优先数据目录**：首次启动自动克隆外部 `data_catalog` 与相关性 pickle 缓存，与外部环境物理隔离。本地缓存满 7 天时页面友好提示。
- **三阶段回测串行调度**：输入多个数据集 ID，系统自动串行运行各阶段（一阶 FO、二阶 SO、三阶 TH），前缀自动推导与剪枝 Prune，自动推荐 neutralization 效率评分最高项，且支持断点续跑。
- **限额限时挂起拦截**：在每个 pool 回测及 check 提交 POST 前校验当前额度（4500 限额）和禁用时间窗口，达到限制后自动切换至挂起等待状态，不强行中断任务。
- **相关性诊断改名**：对比平台 OS 历史因子 Returns 缓存，智能计算 PPA/RA/ATOM 因子指标并自动命名，在页面提供二次改名确认。
- **三线程 check_submission**：自动构建包含回测、相关性优秀候选及手动粘贴的待检队列，多线程并发执行，结果写入数据库并分页直观查看。
- **任务隔离日志**：系统采用 Thread-local 机制将并发任务各自的 `stdout/stderr` 输出隔离重定向至 `logs/job_{job_id}.log`，支持前台 AJAX 异步实时滚动显示。

---

## 环境要求

请确保以下 Python 依赖库已成功安装：
```powershell
python -m pip install -r gui/requirements.txt
```

*(如果需要进行测试，可运行 `python -m pip install pytest` 安装测试框架)*

---

## 快速运行

进入项目根目录 `consultant` 下，运行启动入口：

```powershell
python gui/run_gui.py
```

- **访问链接**：[http://127.0.0.1:8765](http://127.0.0.1:8765)
- **初始管理员密码**：`admin`

*注：如果您希望禁止启动后自动打开浏览器（例如在 Linux 服务器上远程运行），可使用参数：*
```powershell
python gui/run_gui.py --no-browser
```

---

## 目录及存储结构

- **代码存放**：`gui/app/`
- **数据库路径**：`gui/data/gui.db` (保存所有系统参数设置、任务进度状态、已判定 Alpha 归档、check 结果等)
- **快照缓存**：`gui/data/catalog/` 与 `gui/data/correlation/`
- **日志路径**：
  - 系统日志：`gui/logs/gui.log`
  - 任务日志：`gui/logs/job_{job_id}.log`
