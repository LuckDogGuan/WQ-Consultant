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
            conn.execute("DELETE FROM sync_chunks")
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
            "status": "CHECKED_PASS",
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

    @patch("app.job_runner.JobRunner")
    @patch("app.storage.create_job")
    def test_sync_alphas_endpoint(self, mock_create_job, mock_job_runner):
        from fastapi.testclient import TestClient
        from app.main import app, get_current_admin
        
        app.dependency_overrides[get_current_admin] = lambda: "admin"
        client = TestClient(app)
        
        mock_create_job.return_value = 888
        runner_instance = MagicMock()
        mock_job_runner.return_value = runner_instance
        
        try:
            response = client.post("/api/alphas/sync")
            self.assertEqual(response.status_code, 200)
            self.assertIn("同步任务已成功启动", response.json()["message"])
            self.assertEqual(response.json()["job_id"], 888)
            
            mock_create_job.assert_called_once_with(
                kind="sync_alphas",
                title="同步云端因子 (最近 30 天)",
                params={"lookback_days": 30}
            )
            runner_instance.start_job.assert_called_once_with(888, "sync_alphas", {"lookback_days": 30})
        finally:
            app.dependency_overrides.clear()

    @patch("app.services.sync_service.login_with_credentials")
    @patch("app.services.sync_service.get_alphas_full")
    @patch("app.services.sync_service.create_job")
    @patch("app.services.sync_service.JobRunner")
    def test_run_sync_alphas_job(self, mock_job_runner, mock_create_job, mock_get_alphas, mock_login):
        from app.services.sync_service import run_sync_alphas_job
        
        session_mock = MagicMock()
        mock_login.return_value = session_mock
        
        # Cloud returned A_NEW_1 and A_CLOUD_1 (which is already in DB)
        mock_df = pd.DataFrame([
            {
                "alpha_id": "A_NEW_1",
                "name": "New Alpha 1",
                "sharpe": 1.65,
                "fitness": 1.2,
                "margin": 0.0018,
                "returns": 0.15,
                "drawdown": 0.08,
                "status": "UNSUBMITTED",
                "universe": "TOP3000"
            },
            {
                "alpha_id": "A_CLOUD_1",
                "name": "Cloud Alpha 1",
                "sharpe": 1.45,
                "fitness": 1.0,
                "margin": 0.0012,
                "returns": 0.12,
                "drawdown": 0.07,
                "status": "UNSUBMITTED",
                "universe": "TOP3000"
            }
        ])
        mock_get_alphas.return_value = mock_df
        
        # Pre-insert A_CLOUD_1 to test filtering duplicate
        upsert_alpha({
            "alpha_id": "A_CLOUD_1",
            "alpha_type": "B",
            "name": "Cloud Alpha 1",
            "region": "USA",
            "universe": "TOP3000",
            "sharpe": 1.45,
            "fitness": 1.0,
            "margin": 0.0012,
            "status": "UNSUBMITTED",
            "source": "manual"
        })
        
        mock_create_job.return_value = 999
        runner_instance = MagicMock()
        mock_job_runner.return_value = runner_instance
        
        # Create a job in DB
        with connect() as conn:
            conn.execute("INSERT INTO jobs (id, kind, status, title, params, progress_current, progress_total, message, created_at, updated_at) VALUES (888, 'sync_alphas', 'queued', 'test', '{}', 0, 100, '', datetime('now'), datetime('now'))")
            
        run_sync_alphas_job(888, {"lookback_days": 30})
        
        # Verify that only A_NEW_1 was added (since A_CLOUD_1 already existed)
        with connect() as conn:
            rows = conn.execute("SELECT alpha_id, source FROM alpha_records").fetchall()
            ids = {r["alpha_id"]: r["source"] for r in rows}
            
        self.assertIn("A_NEW_1", ids)
        self.assertEqual(ids["A_NEW_1"], "wq_sync")
        self.assertEqual(ids["A_CLOUD_1"], "manual") # Source should not change
        
        # Verify that alpha_inspection job was triggered
        mock_create_job.assert_called_once()
        runner_instance.start_job.assert_called_once_with(999, "alpha_inspection", {"only_new": True})

    @patch("app.services.sync_service.login_with_credentials")
    @patch("app.services.sync_service.get_alphas_full")
    def test_run_sync_alphas_job_skips_successful_day_chunks(self, mock_get_alphas, mock_login):
        from datetime import datetime, timedelta
        from app.services.sync_service import run_sync_alphas_job

        session_mock = MagicMock()
        mock_login.return_value = session_mock
        mock_get_alphas.return_value = pd.DataFrame()

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        with connect() as conn:
            conn.execute("INSERT INTO jobs (id, kind, status, title, params, progress_current, progress_total, message, created_at, updated_at) VALUES (889, 'sync_alphas', 'queued', 'test', '{}', 0, 100, '', datetime('now'), datetime('now'))")
            conn.execute(
                """
                INSERT INTO sync_chunks(kind, region, chunk_start, chunk_end, status, fetched_count, error, updated_at)
                VALUES ('wq_sync', 'USA', ?, ?, 'success', 0, '', datetime('now'))
                """,
                (yesterday.isoformat(), today.isoformat()),
            )

        run_sync_alphas_job(889, {"lookback_days": 1})

        self.assertEqual(mock_get_alphas.call_count, 1)

    @patch("app.services.sync_service.login_with_credentials")
    @patch("app.services.sync_service.get_alphas_full")
    def test_run_sync_alphas_job_records_failed_day_for_retry(self, mock_get_alphas, mock_login):
        from app.services.sync_service import run_sync_alphas_job

        session_mock = MagicMock()
        mock_login.return_value = session_mock
        mock_get_alphas.side_effect = RuntimeError("temporary disconnect")

        with connect() as conn:
            conn.execute("INSERT INTO jobs (id, kind, status, title, params, progress_current, progress_total, message, created_at, updated_at) VALUES (890, 'sync_alphas', 'queued', 'test', '{}', 0, 100, '', datetime('now'), datetime('now'))")

        with self.assertRaises(RuntimeError):
            run_sync_alphas_job(890, {"lookback_days": 0})

        with connect() as conn:
            row = conn.execute("SELECT status, error FROM sync_chunks WHERE kind = 'wq_sync' AND region = 'USA'").fetchone()

        self.assertEqual(row["status"], "failed")
        self.assertIn("temporary disconnect", row["error"])

    @patch("app.services.sync_service.login_with_credentials")
    @patch("app.services.background_inspector.BackgroundInspector._run_autocorrelation")
    def test_run_alpha_inspection_job(self, mock_run_auto, mock_login):
        from app.services.sync_service import run_alpha_inspection_job
        
        session_mock = MagicMock()
        mock_login.return_value = session_mock
        
        # Pre-insert one alpha with missing correlation
        upsert_alpha({
            "alpha_id": "A_INSP_1",
            "alpha_type": "",
            "name": "Inspection Alpha 1",
            "region": "USA",
            "universe": "TOP3000",
            "sharpe": 1.45,
            "fitness": 1.0,
            "margin": 0.0012,
            "prod_corr": 0.0,
            "status": "CHECKED_PASS",
            "source": "wq_sync"
        })
        
        # Create job in DB
        with connect() as conn:
            conn.execute("INSERT INTO jobs (id, kind, status, title, params, progress_current, progress_total, message, created_at, updated_at) VALUES (777, 'alpha_inspection', 'queued', 'test', '{}', 0, 100, '', datetime('now'), datetime('now'))")
            
        run_alpha_inspection_job(777, {})
        
        # Verify that autocorrelation run was triggered for A_INSP_1
        mock_run_auto.assert_called_once()
        self.assertEqual(mock_run_auto.call_args[0][1], "A_INSP_1")


if __name__ == "__main__":
    unittest.main()
