import unittest
from unittest.mock import MagicMock, patch
import json
import pandas as pd
 
from app.storage import connect, init_db, upsert_alpha
from app.services.background_inspector import BackgroundInspector
 
class BackgroundInspectorTests(unittest.TestCase):
    def setUp(self):
        init_db()
        # Clean table
        with connect() as conn:
            conn.execute("DELETE FROM alpha_records")
            conn.execute("DELETE FROM check_results")
            conn.execute("DELETE FROM settings")
            
        # Put WQ credentials in Settings
        with connect() as conn:
            conn.execute("INSERT INTO settings (key, value, updated_at) VALUES ('wq_username', 'test_user', datetime('now'))")
            conn.execute("INSERT INTO settings (key, value, updated_at) VALUES ('wq_password', 'test_pass', datetime('now'))")
            conn.execute("INSERT INTO settings (key, value, updated_at) VALUES ('region', 'USA', datetime('now'))")
 
    @patch("app.services.background_inspector.login_with_credentials")
    def test_process_candidates_empty_db(self, mock_login):
        inspector = BackgroundInspector()
        inspector._process_candidates("test_user", "test_pass")
        mock_login.assert_not_called()
 
    @patch("app.services.background_inspector.login_with_credentials")
    @patch("app.services.background_inspector.download_correlation_data")
    @patch("app.services.background_inspector.load_correlation_data")
    @patch("app.services.background_inspector.get_alpha_pnl")
    @patch("app.services.background_inspector.calc_self_corr_local")
    @patch("app.services.background_inspector.retire_wq_alpha")
    def test_process_candidates_autocorrelation_workflow(
        self, mock_retire, mock_calc_self_corr, mock_get_pnl, mock_load_corr, mock_download, mock_login
    ):
        # Insert an alpha with no prod_corr (value is 0.0 or NULL)
        upsert_alpha({
            "alpha_id": "A11111",
            "alpha_type": "PPA",
            "name": "Alpha 1",
            "region": "USA",
            "universe": "TOP3000",
            "sharpe": 1.6,
            "fitness": 1.1,
            "margin": 0.0015,
            "prod_corr": 0.0,
            "ppa_corr": 0.0,
            "status": "UNSUBMITTED",
            "source": "test_src"
        })
 
        session_mock = MagicMock()
        mock_login.return_value = session_mock
        mock_load_corr.return_value = ({}, pd.DataFrame())
        
        # Mock PnL
        pnl_df = pd.DataFrame({"Date": ["2026-01-01", "2026-01-02"], "A11111": [1.0, 1.05]})
        mock_get_pnl.return_value = pnl_df
        
        # Mock correlation output
        mock_calc_self_corr.return_value = 0.25
        
        inspector = BackgroundInspector()
        inspector._process_candidates("test_user", "test_pass")
        
        mock_login.assert_called_once_with("test_user", "test_pass")
        mock_download.assert_called_once_with(session_mock, flag_increment=True)
        
        # Check that it updated the database with calculated correlation and grade
        with connect() as conn:
            row = conn.execute("SELECT * FROM alpha_records WHERE alpha_id = ?", ("A11111",)).fetchone()
            
        self.assertIsNotNone(row)
        self.assertEqual(row["prod_corr"], 0.25)
        self.assertEqual(row["ppa_corr"], 0.25)
        # S-grade criteria met (Sharpe >= 1.58, Fitness >= 1.0, Margin >= 0.0010, correlation <= 0.68)
        self.assertEqual(row["alpha_type"], "S")
 
    @patch("app.services.background_inspector.login_with_credentials")
    @patch("app.services.background_inspector.check_alpha_remotely")
    @patch("app.services.background_inspector.add_check_result")
    @patch("app.services.background_inspector.retire_wq_alpha")
    def test_process_candidates_check_submit_workflow(
        self, mock_retire, mock_add_check, mock_check_remotely, mock_login
    ):
        # Insert an alpha that has good metrics (would be graded S/A/B),
        # status 'UNSUBMITTED', has prod_corr set, but lacks check_results
        upsert_alpha({
            "alpha_id": "A22222",
            "alpha_type": "B",  # Already initialized to B grade
            "name": "Alpha 2",
            "region": "USA",
            "universe": "TOP3000",
            "sharpe": 1.6,
            "fitness": 1.1,
            "margin": 0.0015,
            "prod_corr": 0.35,
            "ppa_corr": 0.25,
            "status": "UNSUBMITTED",
            "source": "test_src"
        })
 
        session_mock = MagicMock()
        mock_login.return_value = session_mock
        mock_check_remotely.return_value = ("PASS", 0.35, "", {"is": {"checks": [{"name": "PROD_CORRELATION", "value": 0.35, "result": "PASS"}]}})
        
        # Stub the fetch details inside _run_check_submit to avoid deep mocking
        with patch.object(BackgroundInspector, "_run_fetch_pnl_details") as mock_fetch:
            inspector = BackgroundInspector()
            inspector._process_candidates("test_user", "test_pass")
            
            mock_login.assert_called_once()
            mock_check_remotely.assert_called_once_with(session_mock, "A22222")
            mock_add_check.assert_called_once()
            mock_fetch.assert_called_once()
 
 
if __name__ == "__main__":
    unittest.main()
