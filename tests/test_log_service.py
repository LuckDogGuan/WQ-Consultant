import pytest
from pathlib import Path
from unittest.mock import patch
from app.services.log_service import filter_gui_log, get_job_log_path, get_gui_log_path

def test_get_paths():
    assert get_job_log_path(123).name == "job_123.log"
    assert get_gui_log_path().name == "gui.log"

def test_filter_gui_log():
    # 使用项目根目录下的临时文件，以避开 AppData/Temp 的权限限制
    mock_log_file = Path("test_gui.log").resolve()
    mock_log_content = (
        "2026-06-24 12:00:00 - INFO - line 1\n"
        "2026-06-24 12:05:00 - INFO - line 2\n"
        "  multiline extra trace\n"
        "2026-06-24 12:10:00 - INFO - line 3\n"
    )
    try:
        mock_log_file.write_text(mock_log_content, encoding="utf-8")

        with patch("app.services.log_service.get_gui_log_path", return_value=mock_log_file):
            # 1. Test no filter
            lines = list(filter_gui_log())
            assert len(lines) == 4
            assert "line 1" in lines[0]

            # 2. Test start filter
            lines = list(filter_gui_log(start_time="2026-06-24 12:03:00"))
            assert len(lines) == 3  # lines 2, multiline, and 3
            assert "line 2" in lines[0]
            assert "line 1" not in "".join(lines)

            # 3. Test end filter
            lines = list(filter_gui_log(end_time="2026-06-24 12:08:00"))
            assert len(lines) == 3  # lines 1, 2, and multiline
            assert "line 3" not in "".join(lines)

            # 4. Test start & end filter
            lines = list(filter_gui_log(start_time="2026-06-24 12:01:00", end_time="2026-06-24 12:09:00"))
            assert len(lines) == 2  # line 2 and multiline
            assert "line 2" in lines[0]
            assert "line 1" not in "".join(lines)
            assert "line 3" not in "".join(lines)
    finally:
        if mock_log_file.exists():
            mock_log_file.unlink()
