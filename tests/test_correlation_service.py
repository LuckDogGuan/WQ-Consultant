import unittest
from pathlib import Path
import tempfile
import pandas as pd
from unittest.mock import patch, MagicMock

class CorrelationServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "gui.db"
        
        # Patch paths and storage database
        patcher = patch("app.paths.DB_PATH", self.db_path)
        self.addCleanup(patcher.stop)
        patcher.start()

        storage_patcher = patch("app.storage.DB_PATH", self.db_path)
        self.addCleanup(storage_patcher.stop)
        storage_patcher.start()

        from app.storage import init_db
        init_db()

    def tearDown(self):
        self.tmp.cleanup()

    @patch("app.services.correlation_service.download_correlation_data")
    @patch("app.services.correlation_service.load_correlation_data")
    @patch("app.services.correlation_service.get_alpha_pnl")
    @patch("app.services.correlation_service.calc_self_corr_local")
    def test_run_inline_correlation_check_stages(
        self, mock_calc, mock_pnl, mock_load, mock_download
    ):
        from app.storage import connect, upsert_alpha, update_settings
        from app.services.correlation_service import run_inline_correlation_check

        # Setup database settings
        update_settings({
            "fo_corr_sharpe_th": "1.0",
            "fo_max_prod_corr": "0.7",
            "so_corr_sharpe_th": "1.2",
            "so_max_prod_corr": "0.6",
            "th_corr_sharpe_th": "1.5",
            "th_max_prod_corr": "0.5",
        })

        # Insert some alphas to check
        # We need to insert alphas with different Sharpes to see how different stages treat them
        # Alpha 1: Sharpe=1.1, ProdCorr=0.55
        # Alpha 2: Sharpe=1.4, ProdCorr=0.55
        upsert_alpha({
            "alpha_id": "alpha_1",
            "sharpe": 1.1,
            "fitness": 0.8,
            "status": "CHECKED_PASS"
        })
        upsert_alpha({
            "alpha_id": "alpha_2",
            "sharpe": 1.4,
            "fitness": 1.1,
            "status": "CHECKED_PASS"
        })

        # Mock dependencies
        mock_download.return_value = None
        mock_load.return_value = ({"USA": ["alpha_ref"]}, pd.DataFrame())
        
        # PNL mock
        pnl_df = pd.DataFrame({
            "Date": ["2026-06-01", "2026-06-02"],
            "alpha_1": [10.0, 10.5],
            "alpha_2": [10.0, 10.5]
        })
        mock_pnl.return_value = pnl_df

        # Correlation mock: returns 0.55
        mock_calc.return_value = 0.55

        session = MagicMock()

        # 1. Check FO stage
        # FO stage limits: sharpe >= 1.0, corr <= 0.7.
        # Both alpha_1 (Sharpe=1.1) and alpha_2 (Sharpe=1.4) should PASS (RA) because:
        # alpha_1: 1.1 >= 1.0 and 0.55 <= 0.7 -> PASS (RA)
        # alpha_2: 1.4 >= 1.0 and 0.55 <= 0.7 -> PASS (RA)
        run_inline_correlation_check(session, ["alpha_1", "alpha_2"], job_id=999, stage="FO")

        with connect() as conn:
            row_1 = conn.execute("SELECT alpha_type, name, prod_corr FROM alpha_records WHERE alpha_id = 'alpha_1'").fetchone()
            row_2 = conn.execute("SELECT alpha_type, name, prod_corr FROM alpha_records WHERE alpha_id = 'alpha_2'").fetchone()
        
        self.assertEqual(row_1["alpha_type"], "RA")
        self.assertEqual(row_2["alpha_type"], "RA")
        self.assertAlmostEqual(row_1["prod_corr"], 0.55)
        self.assertAlmostEqual(row_2["prod_corr"], 0.55)

        # 2. Check SO stage
        # SO stage limits: sharpe >= 1.2, corr <= 0.6.
        # alpha_1: 1.1 < 1.2 -> SKIP
        # alpha_2: 1.4 >= 1.2 and 0.55 <= 0.6 -> PASS (RA)
        run_inline_correlation_check(session, ["alpha_1", "alpha_2"], job_id=999, stage="SO")

        with connect() as conn:
            row_1 = conn.execute("SELECT alpha_type, name FROM alpha_records WHERE alpha_id = 'alpha_1'").fetchone()
            row_2 = conn.execute("SELECT alpha_type, name FROM alpha_records WHERE alpha_id = 'alpha_2'").fetchone()

        self.assertEqual(row_1["alpha_type"], "SKIP")
        self.assertEqual(row_2["alpha_type"], "RA")

        # 3. Check TH stage
        # TH stage limits: sharpe >= 1.5, corr <= 0.5.
        # alpha_2: 1.4 < 1.5 -> SKIP
        run_inline_correlation_check(session, ["alpha_2"], job_id=999, stage="TH")

        with connect() as conn:
            row_2 = conn.execute("SELECT alpha_type, name FROM alpha_records WHERE alpha_id = 'alpha_2'").fetchone()

        self.assertEqual(row_2["alpha_type"], "SKIP")

if __name__ == "__main__":
    unittest.main()
