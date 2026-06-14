import json
import tempfile
import unittest
from pathlib import Path

from consultant_core.machine_lib import load_webdatascope_info


class WebDataScopeCacheTests(unittest.TestCase):
    def test_load_webdatascope_info_prefers_saved_json_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_path = root / "webdatascope_info.json"
            cache_path.write_text(json.dumps({"USA_1": {"ok": True}}), encoding="utf-8")

            data = load_webdatascope_info(root, node_executable="node-does-not-exist")

        self.assertEqual(data, {"USA_1": {"ok": True}})


if __name__ == "__main__":
    unittest.main()
