import pytest
from pathlib import Path
import app.storage
import app.paths

# Force test database isolation
TEST_DB_PATH = app.paths.DATA_DIR / "test_gui.db"
app.storage.DB_PATH = TEST_DB_PATH
app.paths.DB_PATH = TEST_DB_PATH

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    # Clean up test DB file if exists to ensure clean run
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass
    app.storage.init_db()
    yield
    # Clean up after session
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass
