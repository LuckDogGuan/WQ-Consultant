import json
import traceback
from datetime import datetime, timezone
from pathlib import Path


RUN_DIR = Path("runs") / "alpha_machine"
DEFAULT_NOTEBOOK_PATH = Path("notebooks") / "Alpha Machine copy.ipynb"


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_sentiment_option_templates(sent_fields, option_fields):
    alpha_list = []
    for sent_field in sent_fields:
        for opt_field in option_fields:
            alpha_list.append(
                "log(1+sigmoid(ts_zscore(%s,30))*sigmoid(ts_zscore(%s,30)))"
                % (sent_field, opt_field)
            )
    return alpha_list


class AlphaMachineRunRecorder:
    def __init__(self, notebook_path, run_dir=RUN_DIR):
        self.notebook_path = Path(notebook_path)
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        stem = self.notebook_path.stem.replace(" ", "_")
        self.events_path = self.run_dir / f"{stem}.jsonl"
        self.state_path = self.run_dir / f"{stem}.state.json"

    def read_state(self):
        if not self.state_path.exists():
            return {}
        with self.state_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def append_event(self, event_type, **payload):
        event = {
            "time": utc_now_iso(),
            "notebook": str(self.notebook_path),
            "event": event_type,
            **payload,
        }
        with self.events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def mark_started(self):
        state = {
            "notebook": str(self.notebook_path),
            "started_at": utc_now_iso(),
            "updated_at": utc_now_iso(),
            "status": "running",
            "completed_cells": [],
        }
        self._write_state(state)
        return self.append_event("run_started")

    def mark_cell_started(self, cell_index, cell_label=None):
        state = self.read_state()
        state.update(
            {
                "updated_at": utc_now_iso(),
                "status": "running",
                "current_cell": cell_index,
                "current_label": cell_label,
            }
        )
        self._write_state(state)
        return self.append_event("cell_started", cell_index=cell_index, cell_label=cell_label)

    def mark_cell_succeeded(self, cell_index, cell_label=None):
        state = self.read_state()
        completed = state.get("completed_cells", [])
        if cell_index not in completed:
            completed.append(cell_index)
        state.update(
            {
                "updated_at": utc_now_iso(),
                "status": "running",
                "last_successful_cell": cell_index,
                "last_successful_label": cell_label,
                "completed_cells": completed,
            }
        )
        self._write_state(state)
        return self.append_event("cell_succeeded", cell_index=cell_index, cell_label=cell_label)

    def mark_cell_failed(self, cell_index, cell_label, exc):
        state = self.read_state()
        state.update(
            {
                "updated_at": utc_now_iso(),
                "status": "failed",
                "failed_cell": cell_index,
                "failed_label": cell_label,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
        self._write_state(state)
        return self.append_event(
            "cell_failed",
            cell_index=cell_index,
            cell_label=cell_label,
            error_type=type(exc).__name__,
            error=str(exc),
            traceback=traceback.format_exc(),
        )

    def mark_completed(self):
        state = self.read_state()
        state.update({"updated_at": utc_now_iso(), "status": "completed"})
        self._write_state(state)
        return self.append_event("run_completed")

    def mark_interrupted(self, reason="interrupted"):
        state = self.read_state()
        for key in ("failed_cell", "failed_label", "error_type", "error"):
            state.pop(key, None)
        state.update(
            {
                "updated_at": utc_now_iso(),
                "status": "interrupted",
                "interrupt_reason": reason,
            }
        )
        self._write_state(state)
        return self.append_event(
            "run_interrupted",
            current_cell=state.get("current_cell"),
            current_label=state.get("current_label"),
            reason=reason,
        )

    def resume_summary(self):
        state = self.read_state()
        if not state:
            return "No previous Alpha Machine run record found."
        status = state.get("status", "unknown")
        current_cell = state.get("current_cell")
        last_cell = state.get("last_successful_cell")
        failed_cell = state.get("failed_cell")
        if status == "failed":
            return (
                f"Previous run failed at cell {failed_cell}: "
                f"{state.get('error_type', 'Error')} {state.get('error', '')}"
            ).strip()
        if status == "running" and current_cell is not None:
            return f"Previous run was interrupted or still running at cell {current_cell}."
        if status == "interrupted" and current_cell is not None:
            return f"Previous run was interrupted at cell {current_cell}."
        if last_cell is not None:
            return f"Previous run status: {status}; last successful cell: {last_cell}."
        return f"Previous run status: {status}."

    def _write_state(self, state):
        tmp_path = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        tmp_path.replace(self.state_path)


def start_alpha_machine_run(notebook_path=DEFAULT_NOTEBOOK_PATH, run_dir=RUN_DIR):
    recorder = AlphaMachineRunRecorder(notebook_path, run_dir)
    recorder.mark_started()
    return recorder


def notebook_cell_label(cell):
    source = "".join(cell.get("source", []))
    for line in source.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:120]
    return ""


def execute_notebook_with_record(notebook_path=DEFAULT_NOTEBOOK_PATH, timeout=1200):
    import nbformat
    from nbclient import NotebookClient

    notebook_path = Path(notebook_path)
    recorder = start_alpha_machine_run(notebook_path)
    nb = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3")
    client.create_kernel_manager()

    try:
        with client.setup_kernel():
            for index, cell in enumerate(nb.cells):
                if cell.get("cell_type") != "code":
                    continue
                label = notebook_cell_label(cell)
                recorder.mark_cell_started(index, label)
                try:
                    client.execute_cell(cell, index)
                except Exception as exc:
                    recorder.mark_cell_failed(index, label, exc)
                    nbformat.write(nb, notebook_path)
                    raise
                recorder.mark_cell_succeeded(index, label)
        recorder.mark_completed()
        nbformat.write(nb, notebook_path)
    except Exception:
        raise
    return recorder
