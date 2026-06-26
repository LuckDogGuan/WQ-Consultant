# What is Sharpe ratio?

- **链接**: [Commented] What is Sharpe ratio.md
- **作者**: SO32451
- **发布时间/热度**: 3个月前, 得票: 3

## 帖子正文

Sharpe ratio refers to the critical, annualized metric assessing a trading strategy's risk-adjusted return by dividing the annualized excess return by the strategy's volatility.

---

## 讨论与评论 (2)

### 评论 #1 (作者: BK68311, 时间: 3个月前)

import numpy as np

def sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate annualized Sharpe ratio.

    Parameters:
    returns (array-like): Periodic returns (e.g., daily or monthly)
    risk_free_rate (float): Annual risk-free rate (default 2%)

    Returns:
    float: Sharpe ratio
    """
    # Convert to numpy array
    returns = np.array(returns)

    # Average periodic return
    mean_return = np.mean(returns)

    # Volatility (standard deviation of returns)
    volatility = np.std(returns)

    # Annualization factor (assuming daily returns, ~252 trading days)
    annual_factor = 252  

    # Annualized return and volatility
    annual_return = mean_return * annual_factor
    annual_volatility = volatility * np.sqrt(annual_factor)

    # Sharpe ratio
    sharpe = (annual_return - risk_free_rate) / annual_volatility
    return sharpe

# Example usage:
daily_returns = [0.001, -0.002, 0.003, 0.0015, -0.0005]  # sample daily returns
print("Sharpe Ratio:", sharpe_ratio(daily_returns))

---

### 评论 #2 (作者: FZ60707, 时间: 2个月前)

Well said. To add a nuance: the Sharpe ratio is most meaningful when comparing strategies with similar return distributions, as it assumes normality and penalizes both upside and downside volatility equally. Still, it remains an essential first filter for risk-adjusted performance.

---

