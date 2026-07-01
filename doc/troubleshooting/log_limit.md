# 日志管理与大小限制设计文档

为防止系统日志文件（如 `gui.log`）无限增长导致磁盘占用过高或在 GUI 界面读取日志时产生卡顿，系统引入了**日志文件自动滚动限制**以及**低内存占用的多文件滚动读取与 Log Tail 读取优化**。

## 1. 日志大小限制与回滚配置

在 `app/logging_config.py` 中，原有的 `FileHandler` 被替换为了标准库的 `RotatingFileHandler`：

*   **单个日志文件大小上限** (`maxBytes`)：`5 MB` (5 * 1024 * 1024 字节)。
*   **历史备份数量** (`backupCount`)：最多保留 `3` 个历史日志备份文件（如 `gui.log.1`, `gui.log.2`, `gui.log.3`）。
*   当系统向 `gui.log` 写入数据导致文件超过 5MB 时，它会自动被重命名为备份，并建立新的 `gui.log` 开始写入。这从源头上杜绝了日志文件无限制膨胀至数十或数百兆的问题。

```python
from logging.handlers import RotatingFileHandler
log_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
```

---

## 2. 支持滚动日志多文件流式读取 (`filter_gui_log`)

在导出日志或过滤日志时，如果只读取 `gui.log`，会导致已被滚动到 `gui.log.1`、`gui.log.2` 的历史日志遗失。为此，我们重构了 `filter_gui_log`：
*   **自动扫描备份**：依次寻找 `gui.log.3` (最旧), `gui.log.2`, `gui.log.1`, 最后是 `gui.log` (最新)。
*   **时序流输出**：从最旧到最新依次流式打开并迭代行记录，确保导出的日志具有完美的连续时序性，且不遗漏历史日志。

```python
    log_files = []
    for i in range(3, 0, -1):
        back_file = LOG_DIR / f"gui.log.{i}"
        if back_file.exists():
            log_files.append(back_file)
    log_file = get_gui_log_path()
    if log_file.exists():
        log_files.append(log_file)
```

---

## 3. 读取尾部日志的内存与 CPU 优化 (`read_log_tail`)

为防止读取尾部日志（如在前端终端日志查看页面）因为日志文件巨大而卡死，我们设计了**基于生成器与 C 级滑窗双端队列 (`collections.deque`) 且支持跨文件回溯的方案**：

```python
def read_log_tail(path: Path, max_lines: int = 200) -> list[str]:
    # 收集需要读取的文件，从最新到最旧（用于支持 RotatingFileHandler 滚动日志读取）
    files_to_read = [path]
    for i in range(1, 4):
        back_file = path.parent / f"{path.name}.{i}"
        if back_file.exists():
            files_to_read.append(back_file)

    accumulated_lines = []
    import collections
    
    for f_path in files_to_read:
        if len(accumulated_lines) >= max_lines:
            break
        if not f_path.exists():
            continue
        try:
            needed = max_lines - len(accumulated_lines)
            with open(f_path, "r", encoding="utf-8", errors="replace") as f:
                file_tail = list(collections.deque(f, maxlen=needed))
            # 最新文件的尾部排在最前面，最旧的排在最后面
            accumulated_lines = file_tail + accumulated_lines
        except Exception:
            pass
            
    return accumulated_lines[-max_lines:]
```

### 优化特点：
1.  **自动跨文件回溯**：如果最新文件中的日志行数少于所请求的 `max_lines`，它会自动回溯至 `gui.log.1`、`gui.log.2`，拼装出足够行数的历史日志进行返回。
2.  **极低内存占用**：通过在文件迭代器 `f` 上直接进行迭代读取，只在滑窗内保留需要的行数，单次操作内存占用为常数级 $O(\text{max\_lines})$，完全免去了加载整包巨型日志文件的延迟和 OOM 崩溃隐患。
