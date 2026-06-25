# WorldQuant Consultant GUI

一个基于 FastAPI + Jinja2 的本地 Web 界面，用于辅助管理 WorldQuant Brain 因子开发流程。

## 🎯 核心功能

1. **仪表盘 (Dashboard)**: 展示系统状态与基本统计。
2. **回测任务 (Backtest)**: 支持多数据集回测、自动过滤与检查。
3. **优化规划 (Optimization)**: 提供因子 Error 诊断与优化建议。
4. **Alpha 记录 (Alphas)**: 记录与管理本地因子，支持批量提交。
5. **设置 (Settings)**: 账号配置与系统参数设置。
6. **日志 (Logs)**: 实时系统日志查看与导出。

## ⚙️ 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **环境自检**
   ```bash
   python check_env.py
   ```

3. **启动服务**
   ```bash
   python run_gui.py
   ```

4. **运行测试**
   ```bash
   python -m pytest
   ```

---

## 📂 项目目录结构 (Directory Structure)

为了便于理解和独立开发，仓库结构已简化并进行模块化整理，布局如下：

* **[app/](file:///d:/code/WorldQuant%20Brain/consultant/gui/app)**：Web 应用程序代码库，包含 FastAPI 路由、服务逻辑、Jinja2 网页模板及静态前端样式。
* **[consultant_core/](file:///d:/code/WorldQuant%20Brain/consultant/gui/consultant_core)**：系统底层核心连接封装库，负责处理 WQ Brain 接口调用、Session 维护与数据抓取逻辑。
* **[doc/](file:///d:/code/WorldQuant%20Brain/consultant/gui/doc)**：文档中心，保存系统架构更新记录、因子开发入门指南与集成规划书（已合并原 `todo_list`）。
* **[reference/](file:///d:/code/WorldQuant%20Brain/consultant/gui/reference)**：**受保护的只读参考库**（严禁修改，修改/实验请复制至 `scratch/` 进行）：
  * **[code/](file:///d:/code/WorldQuant%20Brain/consultant/gui/reference/code)**：已清洗验证的模块化 Python 参考脚本（包含去重剪枝 `pruning/`、参数寻优 `optimization/`、自相关分析与快速 PnL 下载 `analysis/`）。
  * **[notebook/](file:///d:/code/WorldQuant%20Brain/consultant/gui/reference/notebook)**：用于回测的核心 Jupyter Notebook 笔记本（包含主生产线 `alpha_generation_pipeline.ipynb` 及 `archive/` 历史备份）。
  * **[unverified/](file:///d:/code/WorldQuant%20Brain/consultant/gui/reference/unverified)**：收集自论坛的原始经验帖子原文（未做任何修改）。
  * **[official_paper/](file:///d:/code/WorldQuant%20Brain/consultant/gui/reference/official_paper)**：官方标准与考核指标说明文档。
  * **[reference_report.md](file:///d:/code/WorldQuant%20Brain/consultant/gui/reference/reference_report.md)**：论坛帖子的本地代码验证报告与操作经验提炼。
* **[scratch/](file:///d:/code/WorldQuant%20Brain/consultant/gui/scratch)**：临时草稿、猜想验证与本地单元测试（包含验证参考代码用例的 `test_code_references.py`）。
* **[tests/](file:///d:/code/WorldQuant%20Brain/consultant/gui/tests)**：Web 服务后端接口与数据处理的系统自动化测试用例。

