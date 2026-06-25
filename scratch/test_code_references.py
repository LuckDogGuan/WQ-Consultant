import os
import sys
import py_compile
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch

# Ensure project root is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_expression_pruner():
    print("=== Testing Expression Pruner ===")
    from reference.code.pruning.expression_pruner import prune_expressions
    
    # Construct a mock dataframe with similar factor structures but different parameters
    mock_data = pd.DataFrame([
        # Group 1: Group neutralize ts_rank of close
        {"regular": "group_neutralize(ts_rank(close, 20), sector)", "sharpe": 1.5, "fitness": 1.2},
        {"regular": "group_neutralize(ts_rank(close, 10), sector)", "sharpe": 1.8, "fitness": 1.4}, # Best in group 1
        {"regular": "group_neutralize(ts_rank(close, 30), sector)", "sharpe": 1.2, "fitness": 0.9},
        
        # Group 2: ts_decay_linear of rank close
        {"regular": "ts_decay_linear(rank(close), 5)", "sharpe": 2.0, "fitness": 1.6}, # Best in group 2
        {"regular": "ts_decay_linear(rank(close), 10)", "sharpe": 1.7, "fitness": 1.3},
        
        # Group 3: A trade_when expression
        {"regular": "trade_when(volume > 1000, ts_rank(close, 20), sector)", "sharpe": 2.1, "fitness": 1.8}
    ])
    
    print("Original factors:")
    print(mock_data[["regular", "sharpe", "fitness"]])
    
    pruned_df = prune_expressions(mock_data)
    print("\nPruned factors:")
    print(pruned_df[["regular", "sharpe", "fitness"]])
    
    # Assertions
    # We should have exactly 3 rows remaining (one for each structural group)
    assert len(pruned_df) == 3, f"Expected 3 rows, got {len(pruned_df)}"
    
    # The best close rank should be 10 days
    assert "group_neutralize(ts_rank(close, 10), sector)" in pruned_df["regular"].values
    assert "group_neutralize(ts_rank(close, 20), sector)" not in pruned_df["regular"].values
    
    # The best decay close rank should be 5 days
    assert "ts_decay_linear(rank(close), 5)" in pruned_df["regular"].values
    assert "ts_decay_linear(rank(close), 10)" not in pruned_df["regular"].values
    
    print("Expression pruner test PASSED!\n")

def test_correlation_pruner():
    print("=== Testing Correlation Pruner ===")
    from reference.code.pruning.correlation_pruner import prune_by_correlation
    
    # Construct a mock correlation matrix for three alphas: A, B, C
    # A and B are highly correlated (0.8), A and C are low (0.2), B and C are low (0.3)
    corr_matrix = pd.DataFrame(
        [
            [1.0, 0.8, 0.2],
            [0.8, 1.0, 0.3],
            [0.2, 0.3, 1.0]
        ],
        index=["alpha_A", "alpha_B", "alpha_C"],
        columns=["alpha_A", "alpha_B", "alpha_C"]
    )
    
    # A has higher score/sharpe, B has slightly lower, C is lower
    alpha_list = [
        {"alpha_id": "alpha_A", "sharpe": 2.0, "fitness": 1.8, "margin": "5.0%"},  # Score = 0.5 * 1.8 + 0.5 * 5.0 = 3.4
        {"alpha_id": "alpha_B", "sharpe": 1.9, "fitness": 1.7, "margin": 4.0},     # Score = 0.5 * 1.7 + 0.5 * 4.0 = 2.85
        {"alpha_id": "alpha_C", "sharpe": 1.5, "fitness": 1.2, "margin": 3.0}      # Score = 0.5 * 1.2 + 0.5 * 3.0 = 2.1
    ]
    
    # Running greedy prune with correlation threshold 0.7
    selected_alphas = prune_by_correlation(corr_matrix, alpha_list, corr_threshold=0.7)
    print("Selected Alphas:", selected_alphas)
    
    # A is selected first because of higher score
    # B conflicts with A (0.8 >= 0.7), so B is skipped
    # C does not conflict with A (0.2 < 0.7), so C is selected
    assert "alpha_A" in selected_alphas
    assert "alpha_B" not in selected_alphas
    assert "alpha_C" in selected_alphas
    assert len(selected_alphas) == 2
    
    print("Correlation pruner test PASSED!\n")

def test_fast_pnl_downloader():
    print("=== Testing Fast PnL Downloader (Mocked) ===")
    from reference.code.analysis.fast_pnl_downloader import get_pnl_via_competition
    
    # Mock WQ session and response
    mock_session = MagicMock()
    
    # Mock competition response
    mock_comp_resp = MagicMock()
    mock_comp_resp.status_code = 200
    mock_comp_resp.json.return_value = {"results": [{"id": "MAPC2025"}]}
    
    # Mock PnL performance response
    mock_perf_resp = MagicMock()
    mock_perf_resp.status_code = 200
    mock_perf_resp.json.return_value = {
        "pnl": {
            "schema": {
                "name": "beforeAndAfterPnN",
                "properties": [
                    {"name": "date", "type": "date"},
                    {"name": "afterPnL", "type": "amount"}
                ]
            },
            "records": [
                ["2025-01-01", 123.45],
                ["2025-01-02", 125.60],
                ["2025-01-03", 128.90]
            ]
        }
    }
    
    # Configure session.get mock side effects
    def mock_get(url, *args, **kwargs):
        if "/competitions" in url and "MAPC2025" not in url:
            return mock_comp_resp
        elif "before-and-after-performance" in url:
            return mock_perf_resp
        return MagicMock(status_code=404)
        
    mock_session.get.side_effect = mock_get
    
    # Execute downloader
    pnl_df = get_pnl_via_competition(mock_session, "alpha_test")
    
    print("Downloaded PnL shape:", pnl_df.shape)
    print(pnl_df)
    
    assert not pnl_df.empty
    assert "Date" in pnl_df.columns
    assert "alpha_test" in pnl_df.columns
    assert len(pnl_df) == 3
    assert pnl_df.loc[0, "alpha_test"] == 123.45
    
    print("Fast PnL downloader mock test PASSED!\n")

def test_super_alpha_correlation():
    print("=== Testing SuperAlpha Correlation Calculation (Mocked) ===")
    from reference.code.analysis.super_alpha_correlation import calc_self_corr
    
    mock_session = MagicMock()
    
    # Construct mock historical returns for OS baseline alphas in region IND
    date_index = pd.date_range(start="2025-01-01", periods=5)
    os_alpha_rets = pd.DataFrame(
        [
            [0.01, -0.005],
            [-0.012, 0.008],
            [0.005, -0.002],
            [0.003, 0.011],
            [-0.002, -0.004]
        ],
        index=date_index,
        columns=["OS_ALPHA_1", "OS_ALPHA_2"]
    )
    
    os_alpha_ids = {"IND": ["OS_ALPHA_1", "OS_ALPHA_2"]}
    
    # Mock target alpha's detail response
    alpha_result = {
        "id": "target_alpha",
        "type": "SUPER",
        "settings": {"region": "IND"}
    }
    
    # Mock target alpha's PnL dataframe (running returns = diff of cumulative PnLs)
    # Target returns: [NaN, 0.009 (10.009-10), -0.011 (9.998-10.009), 0.006 (10.004-9.998), 0.004 (10.008-10.004)]
    mock_pnl_df = pd.DataFrame({
        "Date": date_index,
        "target_alpha": [10.0, 10.009, 9.998, 10.004, 10.008]
    })
    
    # Patch the _get_alpha_pnl helper to bypass network
    with patch("reference.code.analysis.super_alpha_correlation._get_alpha_pnl", return_value=mock_pnl_df):
        corr_val = calc_self_corr(
            session=mock_session,
            alpha_id="target_alpha",
            os_alpha_rets=os_alpha_rets,
            os_alpha_ids=os_alpha_ids,
            alpha_result=alpha_result
        )
        
    print(f"Calculated maximum correlation: {corr_val:.4f}")
    assert isinstance(corr_val, float)
    assert -1.0 <= corr_val <= 1.0
    
    print("SuperAlpha correlation mock test PASSED!\n")

def test_robust_sharpe_optimizer():
    print("=== Testing Robust Sharpe Optimizer Functions ===")
    from reference.code.optimization.robust_sharpe_optimizer import modify_alpha_expression
    
    # Test expression mutation logic
    cases = [
        # TS Backfill
        ("ts_backfill(close, 10)", "time_backfill_ts", 90, "ts_backfill(close, 90)"),
        ("close", "time_backfill_ts", 90, "ts_backfill(close, 90)"),
        
        # Add Winsorize
        ("close", "add_winsorize", 3, "winsorize(close, std=3)"),
        
        # Add Signed Power
        ("close", "add_signed_power", 0.5, "signed_power(close, 0.5)"),
        
        # Add Group Zscore
        ("close", "add_group_zscore", "sector", "group_zscore(close, sector)"),
        
        # Modify Winsorize std
        ("winsorize(close, std=2)", "winsorize_std", 5, "winsorize(close, std=5)")
    ]
    
    for expr, mod_type, val, expected in cases:
        result = modify_alpha_expression(expr, mod_type, val)
        print(f"Expr: {expr} + {mod_type}({val}) -> {result}")
        assert result == expected, f"Expected {expected}, got {result}"
        
    print("Robust Sharpe optimizer mutation logic test PASSED!\n")

def test_syntax_compilation():
    print("=== Testing Syntax Compilation ===")
    
    modules_to_test = [
        "reference/code/pruning/expression_pruner.py",
        "reference/code/pruning/correlation_pruner.py",
        "reference/code/optimization/robust_sharpe_optimizer.py",
        "reference/code/analysis/super_alpha_correlation.py",
        "reference/code/analysis/fast_pnl_downloader.py"
    ]
    
    for relative_path in modules_to_test:
        abs_path = os.path.join(project_root, relative_path)
        print(f"Compiling {relative_path}...")
        try:
            py_compile.compile(abs_path, doraise=True)
            print(f"-> {relative_path} compiled successfully.")
        except py_compile.PyCompileError as e:
            print(f"-> ERROR compiling {relative_path}: {e}")
            sys.exit(1)
            
    print("Syntax compilation test PASSED!\n")

def main():
    test_expression_pruner()
    test_correlation_pruner()
    test_fast_pnl_downloader()
    test_super_alpha_correlation()
    test_robust_sharpe_optimizer()
    test_syntax_compilation()
    print("All tests completed successfully!")

if __name__ == "__main__":
    main()
