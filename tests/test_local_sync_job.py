import unittest
from unittest.mock import MagicMock, patch
import json
import os
os.environ["WQ_DB_NAME"] = "test_gui.db"
import pandas as pd

from app.storage import connect, init_db, upsert_alpha, create_job
from app.services.sync_service import run_refresh_correlation_job

class LocalSyncJobTests(unittest.TestCase):
    def setUp(self):
        init_db()
        with connect() as conn:
            conn.execute("DELETE FROM alpha_records")
            conn.execute("DELETE FROM check_results")
            conn.execute("DELETE FROM settings")
            conn.execute("DELETE FROM jobs")
            
        with connect() as conn:
            conn.execute("INSERT INTO settings (key, value, updated_at) VALUES ('wq_username', 'test_user', datetime('now'))")
            conn.execute("INSERT INTO settings (key, value, updated_at) VALUES ('wq_password', 'test_pass', datetime('now'))")
            conn.execute("INSERT INTO settings (key, value, updated_at) VALUES ('region', 'USA', datetime('now'))")

    @patch("app.services.sync_service.login_with_credentials")
    @patch("app.services.background_inspector.download_correlation_data")
    @patch("app.services.background_inspector.BackgroundInspector")
    def test_run_refresh_correlation_job_success(self, mock_inspector_cls, mock_download_corr, mock_login):
        # Insert a local alpha that should be processed (grade S, not garbage)
        upsert_alpha({
            "alpha_id": "LOC123",
            "alpha_type": "S",
            "name": "Alpha Local",
            "region": "USA",
            "universe": "TOP3000",
            "sharpe": 1.5,
            "fitness": 1.0,
            "margin": 0.001,
            "prod_corr": 0.0,
            "ppa_corr": 0.0,
            "status": "CHECKED_PASS",
            "source": "test_src"
        })

        session_mock = MagicMock()
        mock_login.return_value = session_mock
        
        inspector_mock = MagicMock()
        mock_inspector_cls.return_value = inspector_mock

        job_id = create_job("refresh_correlation", "Refresh correlation", {})
        
        run_refresh_correlation_job(job_id, {})
        
        # Verify login was called
        mock_login.assert_called_once_with("test_user", "test_pass")
        # Verify correlation data download was triggered
        mock_download_corr.assert_called_once_with(session_mock, flag_increment=True)
        # Verify _run_autocorrelation was called for the alpha
        inspector_mock._run_autocorrelation.assert_called_once()
        
        # Verify job is marked as completed
        with connect() as conn:
            job = conn.execute("SELECT status FROM jobs WHERE id = ?", (job_id,)).fetchone()
            self.assertEqual(job["status"], "completed")

    @patch("app.services.sync_service.login_with_credentials")
    def test_run_refresh_correlation_job_no_candidates(self, mock_login):
        # No candidate alphas in DB
        job_id = create_job("refresh_correlation", "Refresh empty", {})
        run_refresh_correlation_job(job_id, {})
        
        mock_login.assert_not_called()
        
        with connect() as conn:
            job = conn.execute("SELECT status FROM jobs WHERE id = ?", (job_id,)).fetchone()
            self.assertEqual(job["status"], "completed")
