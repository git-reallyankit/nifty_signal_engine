"""
STEP 4 & 5: Backtesting & Performance Metrics
==============================================

Backtesting != Proof of Profitability
======================================

What backtesting does:
- Answers: "What would have happened historically?"
- Shows if logic works in past data
- Identifies problems before real trading

What backtesting DOESN'T do:
- Prove future profitability
- Account for slippage changes
- Account for regime changes
- Prove causation (correlation ≠ causation)

Key Metrics for Strategy Evaluation:
====================================

1. Cumulative Return
   - Total growth of capital
   - Simple but doesn't account for risk

2. Sharpe Ratio ⭐ MOST IMPORTANT
   - return per unit of risk
   - Higher = smoother returns
   - >1.0 is good, >2.0 is excellent

3. Drawdown
   - Largest peak-to-trough decline
   - Important psychologically
   - Shows if strategy is bearable

4. Win Rate
   - Percentage of profitable days
   - Less important than Sharpe
   - But good for intuition
"""

import pandas as pd
import numpy as np
from datetime import datetime


def compute_sharpe_ratio(returns, risk_free_rate=0.05, periods_per_year=252):
    """
    Compute Sharpe Ratio.
    
    Formula:
    Sharpe = (mean_return - risk_free_rate) / std_return * sqrt(252)
    
    Interpretation:
    - Measures excess return per unit of risk
    - Higher = better risk-adjusted returns
    - >1.0 is good for hedge funds
    - >2.0 is excellent (rare)
    - <0.5 is weak
    
    Why sqrt(252)?
    - Annualization factor
    - 252 trading days per year
    - Scales daily metric to annual
    
    Args:
        returns (pd.Series): Daily returns
        risk_free_rate (float): Annual risk-free rate (5% = 0.05)
        periods_per_year (int): 252 for daily data
    
    Returns:
        float: Annual Sharpe ratio
    """
    
    # Convert annual risk-free rate to daily
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1
    
    # Excess daily returns
    excess_returns = returns - daily_rf
    
    # Sharpe ratio
    sharpe = excess_returns.mean() / excess_returns.std() * np.sqrt(periods_per_year)
    
    return sharpe


def compute_maximum_drawdown(cumulative_returns):
    """
    Compute maximum drawdown.
    
    Intuition:
    - Worst peak-to-trough decline
    - Shows largest loss from peak
    - Important psychologically (can you handle -30%?)
    
    Formula:
    Drawdown = (Low - Peak) / Peak
    Peak = max value seen so far
    
    Args:
        cumulative_returns (pd.Series): Cumulative returns (decimal form)
    
    Returns:
        float: Maximum drawdown (as negative decimal)
    """
    
    # Convert returns to wealth (1 = starting capital)
    wealth = 1 + cumulative_returns
    
    # Running maximum (peak so far)
    running_max = wealth.expanding().max()
    
    # Drawdown at each point
    drawdown = (wealth - running_max) / running_max
    
    # Maximum drawdown (most negative)
    max_dd = drawdown.min()
    
    return max_dd


def compute_win_rate(returns):
    """
    Compute percentage of profitable days.
    
    Note:
    - Win rate is less important than Sharpe
    - But useful for intuition
    - A strategy can have 40% win rate but positive expectancy
    
    Args:
        returns (pd.Series): Daily returns
    
    Returns:
        float: Percentage of days with positive returns
    """
    positive_days = (returns > 0).sum()
    total_days = len(returns)
    return positive_days / total_days


def evaluate_strategy(results):
    """
    Comprehensive strategy evaluation.
    
    Compares strategy vs buy-and-hold benchmark.
    """
    
    print("\n" + "="*60)
    print("BACKTEST RESULTS & PERFORMANCE METRICS")
    print("="*60)
    
    # Extract returns
    strategy_returns = results['Strategy_Return']
    buyhold_returns = results['Buy_Hold_Return']
    
    # Extract cumulative returns
    strategy_cumulative = results['Cumulative_Return']
    buyhold_cumulative = results['Cumulative_BuyHold']
    
    # ============== STRATEGY METRICS ==============
    print("\n" + "-"*60)
    print("STRATEGY PERFORMANCE")
    print("-"*60)
    
    strategy_sharpe = compute_sharpe_ratio(strategy_returns)
    strategy_dd = compute_maximum_drawdown(strategy_cumulative)
    strategy_wr = compute_win_rate(strategy_returns)
    
    print(f"\nCumulative Return: {strategy_cumulative.iloc[-1]:.2%}")
    print(f"Mean Daily Return: {strategy_returns.mean():.4%}")
    print(f"Std Daily Return: {strategy_returns.std():.4%}")
    print(f"Sharpe Ratio: {strategy_sharpe:.3f}")
    print(f"Maximum Drawdown: {strategy_dd:.2%}")
    print(f"Win Rate: {strategy_wr:.1%} of days profitable")
    
    # ============== BUY & HOLD BENCHMARK ==============
    print("\n" + "-"*60)
    print("BUY & HOLD BENCHMARK")
    print("-"*60)
    
    buyhold_sharpe = compute_sharpe_ratio(buyhold_returns)
    buyhold_dd = compute_maximum_drawdown(buyhold_cumulative)
    buyhold_wr = compute_win_rate(buyhold_returns)
    
    print(f"\nCumulative Return: {buyhold_cumulative.iloc[-1]:.2%}")
    print(f"Mean Daily Return: {buyhold_returns.mean():.4%}")
    print(f"Std Daily Return: {buyhold_returns.std():.4%}")
    print(f"Sharpe Ratio: {buyhold_sharpe:.3f}")
    print(f"Maximum Drawdown: {buyhold_dd:.2%}")
    print(f"Win Rate: {buyhold_wr:.1%} of days profitable")
    
    # ============== COMPARISON ==============
    print("\n" + "-"*60)
    print("COMPARISON (Strategy - BuyHold)")
    print("-"*60)
    
    return_advantage = strategy_cumulative.iloc[-1] - buyhold_cumulative.iloc[-1]
    sharpe_advantage = strategy_sharpe - buyhold_sharpe
    dd_advantage = strategy_dd - buyhold_dd  # Less negative is better
    
    print(f"\nReturn Advantage: {return_advantage:.2%}")
    print(f"Sharpe Advantage: {sharpe_advantage:.3f}")
    print(f"Drawdown Advantage: {dd_advantage:.2%} (less negative = better)")
    
    # ============== INTERPRETATION ==============
    print("\n" + "="*60)
    print("INTERPRETATION")
    print("="*60)
    
    print(f"\n⚠️ REALITY CHECK:")
    print(f"\nShould you trade this strategy?")
    
    if strategy_sharpe < 0.5:
        print(f"❌ NO. Sharpe {strategy_sharpe:.2f} < 0.5 (too weak)")
    elif strategy_sharpe < 1.0:
        print(f"⚠️ MAYBE. Sharpe {strategy_sharpe:.2f} is acceptable but not great")
    elif strategy_sharpe < 2.0:
        print(f"✓ GOOD. Sharpe {strategy_sharpe:.2f} is solid")
    else:
        print(f"✓✓ EXCELLENT. Sharpe {strategy_sharpe:.2f} is very strong")
    
    print(f"\n⚠️ CAVEATS:")
    print(f"• This is HISTORICAL backtest, not future prediction")
    print(f"• Markets change (regime shift)")
    print(f"• Slippage, fees, impact may be larger in real trading")
    print(f"• Curve-fitting risk (parameters optimized to past)")
    
    print(f"\n📊 WHAT THIS TEACHES:")
    print(f"• How quants structure research")
    print(f"• Why transaction costs matter")
    print(f"• Why signal shifting matters")
    print(f"• The foundation for ML-based strategies")
    
    return {
        'strategy_sharpe': strategy_sharpe,
        'strategy_drawdown': strategy_dd,
        'strategy_cumulative_return': strategy_cumulative.iloc[-1],
        'buyhold_sharpe': buyhold_sharpe,
        'buyhold_drawdown': buyhold_dd,
        'buyhold_cumulative_return': buyhold_cumulative.iloc[-1],
    }


if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from load_data import load_nifty_data
    from features import engineer_features
    from strategy import generate_momentum_signal, calculate_strategy_returns
    
    data = load_nifty_data()
    features = engineer_features(data)
    signal = generate_momentum_signal(features, momentum_threshold=0.02)
    results = calculate_strategy_returns(features, signal, transaction_cost=0.0005)
    metrics = evaluate_strategy(results)