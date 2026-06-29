import unittest
from unittest.mock import MagicMock

from app.services.alpha_remote_validator import (
    detect_flat_pnl,
    compute_remote_validation_score,
    run_remote_validation,
)


class AlphaRemoteValidatorTests(unittest.TestCase):
    def test_detect_flat_pnl_all_zeros(self):
        # 1. 全零 PNL
        pnl = [0.0] * 1000
        self.assertTrue(detect_flat_pnl(pnl))

    def test_detect_flat_pnl_insufficient_length(self):
        # 2. 交易日数不足 3 年 (756天)
        pnl = [1.2] * 500
        self.assertTrue(detect_flat_pnl(pnl))

    def test_detect_flat_pnl_end_stale(self):
        # 3. 末端绝对静止 (最后 250 天相同值)
        # 前 600 天是变化的，后 250 天是固定的 1.5
        pnl = [float(i) for i in range(600)] + [1.5] * 250
        self.assertTrue(detect_flat_pnl(pnl))

    def test_detect_flat_pnl_mid_stale(self):
        # 4. 中途非零冻结 (中途连续 250 天相同非零值)
        pnl = [float(i) for i in range(300)] + [10.5] * 250 + [float(i) for i in range(300)]
        self.assertTrue(detect_flat_pnl(pnl))

    def test_detect_flat_pnl_zero_streak(self):
        # 5. 长周期零值断带 (连续 756 天零值)
        pnl = [1.0] * 100 + [0.0] * 760 + [1.0] * 100
        self.assertTrue(detect_flat_pnl(pnl))

    def test_detect_flat_pnl_healthy(self):
        # 6. 健康的 PNL 序列 (没有连续相同值)
        pnl = [float(i % 50 + 1) for i in range(1000)]
        self.assertFalse(detect_flat_pnl(pnl))

    def test_compute_remote_validation_score_insufficient_years(self):
        # 1. 年份数量不足 3 年
        yearly_stats = [
            {"year": "2022", "sharpe": 1.5, "returns": 0.05, "turnover": 0.12},
            {"year": "2023", "sharpe": 1.6, "returns": 0.06, "turnover": 0.13},
        ]
        res = compute_remote_validation_score(yearly_stats)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["grade_adjustment"], "D")
        self.assertIn("insufficient_years", res["issues"])

    def test_compute_remote_validation_score_dead_year(self):
        # 2. 单年零换手 + 零收益
        yearly_stats = [
            {"year": "2021", "sharpe": 1.5, "returns": 0.05, "turnover": 0.12},
            {"year": "2022", "sharpe": 1.6, "returns": 0.06, "turnover": 0.13},
            {"year": "2023", "sharpe": 0.0, "returns": 0.0, "turnover": 0.0},
        ]
        res = compute_remote_validation_score(yearly_stats)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["grade_adjustment"], "D")
        self.assertIn("DEAD_ALPHA_RISK", res["issues"])

    def test_compute_remote_validation_score_zero_years_ratio(self):
        # 3. 零值年份占比超过 40% (例如 5 年中有 3 年是零值)
        yearly_stats = [
            {"year": "2019", "sharpe": 1.5, "returns": 0.05, "turnover": 0.12},
            {"year": "2020", "sharpe": 1.6, "returns": 0.06, "turnover": 0.13},
            {"year": "2021", "sharpe": 0.0, "returns": 0.0, "turnover": 0.0},
            {"year": "2022", "sharpe": 0.0, "returns": 0.0, "turnover": 0.0},
            {"year": "2023", "sharpe": 0.0, "returns": 0.0, "turnover": 0.0},
        ]
        res = compute_remote_validation_score(yearly_stats)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["grade_adjustment"], "D")
        self.assertIn("DEAD_ALPHA_RISK", res["issues"])

    def test_compute_remote_validation_score_recent_zero_sharpe(self):
        # 4. 近两年平均 Sharpe 极低 (< 0.10) 或包含 0.0
        yearly_stats = [
            {"year": "2021", "sharpe": 1.5, "returns": 0.05, "turnover": 0.12},
            {"year": "2022", "sharpe": 0.05, "returns": 0.01, "turnover": 0.08},
            {"year": "2023", "sharpe": 0.0, "returns": 0.02, "turnover": 0.05},
        ]
        res = compute_remote_validation_score(yearly_stats)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["grade_adjustment"], "D")
        self.assertIn("DEAD_ALPHA_RISK_RECENT", res["issues"])

    def test_compute_remote_validation_score_pos_years_ratio(self):
        # 5. 正收益年份占比不足 50%
        # 4 年中仅 1 年正收益
        yearly_stats = [
            {"year": "2020", "sharpe": 1.5, "returns": 0.05, "turnover": 0.12},
            {"year": "2021", "sharpe": -0.5, "returns": -0.02, "turnover": 0.08},
            {"year": "2022", "sharpe": -0.8, "returns": -0.03, "turnover": 0.05},
            {"year": "2023", "sharpe": -0.1, "returns": -0.01, "turnover": 0.05},
        ]
        res = compute_remote_validation_score(yearly_stats)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["grade_adjustment"], "D")
        self.assertIn("unstable_returns", res["issues"])

    def test_compute_remote_validation_score_healthy_keep(self):
        # 6. 健康因子的正常评级保持 (keep)
        yearly_stats = [
            {"year": "2021", "sharpe": 1.5, "returns": 0.05, "turnover": 0.12},
            {"year": "2022", "sharpe": 1.6, "returns": 0.06, "turnover": 0.13},
            {"year": "2023", "sharpe": 1.7, "returns": 0.07, "turnover": 0.14},
        ]
        res = compute_remote_validation_score(yearly_stats, is_sharpe=1.6, is_fitness=2.0)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["grade_adjustment"], "keep")
        self.assertEqual(len(res["issues"]), 0)


if __name__ == "__main__":
    unittest.main()
