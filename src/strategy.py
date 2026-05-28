"""
STEP 3: Signal Generation
==========================

Why this matters:
You convert features → trading decisions.

CRITICAL CONCEPT: Signal Shifting
==================================

Suppose today (Tuesday) you calculate a signal.
Can you trade using today's closing price?

NO. Here's why:

You only know today's close AFTER the market closes.
So you can only ACT on the signal tomorrow.

This is called LOOK-AHEAD BIAS.
Most beginner strategies fail because they ignore this.

Correct workflow:
- Day 1 (Tuesday): Market closes, signal generated
- Day 2 (Wednesday): Trade based on yesterday's signal

In code:
strategy_return = signal.shift(1) * returns

This shift(1) is CRITICAL for realistic backtesting.
"""

import pandas as pd
import numpy as np


def generate_momentum_signal(features, momentum_threshold=0.02):
    """
    Generate trading signals based on momentum.
    
    Signal Rule (Simple):
    if momentum > threshold:
        signal = 1 (go long, buy)
    else:
        signal = 0 (stay in cash, don't buy)
    
    Args:
        features (pd.DataFrame): Feature matrix with 'Momentum' column
        momentum_threshold (float): Threshold for momentum signal
                                  0.02 = 2% threshold
    
    Returns:
        pd.Series: Trading signals (1 = long, 0 = no position)
    
    Why this signal?
    ================
    Momentum is one of the oldest and most studied market anomalies.
    
    Logic:
    - If market gained >2% over 10 days, trend is up
    - Go long (buy), expect continuation
    - If not, stay out
    
    This is NOT prediction.
    This is trend-following.
    """
    
    # Generate signal
    signal = (features['Momentum'] > momentum_threshold).astype(int)
    
    print(f"\n" + "="*60)
    print("SIGNAL GENERATION")
    print("="*60)
    print(f"\nSignal Rule:")
    print(f"  if Momentum > {momentum_threshold:.2%}: signal = 1 (long)")
    print(f"  else: signal = 0 (no position)")
    
    # Statistics
    long_days = (signal == 1).sum()
    no_position_days = (signal == 0).sum()
    pct_long = long_days / len(signal) * 100
    
    print(f"\nSignal Statistics:")
    print(f"  Days in long: {long_days} ({pct_long:.1f}%)")
    print(f"  Days in no position: {no_position_days} ({100-pct_long:.1f}%)")
    
    return signal


def calculate_strategy_returns(features, signal, transaction_cost=0.0005):
    """
    Calculate strategy returns (INCLUDING SIGNAL SHIFT).
    
    This is where most beginners make mistakes.
    
    CRITICAL: signal.shift(1)
    ========================
    
    Why shift?
    - Signal generated today → Trade executed tomorrow
    - Uses today's signal + tomorrow's return
    
    Without shift:
    - Uses today's signal + today's return
    - LOOK-AHEAD BIAS (you can't trade the same day)
    
    Formula:
    strategy_return_t = signal_{t-1} * return_t - transaction_cost
    
    Transaction Cost:
    - 0.05% per trade is realistic for large institutional trades
    - Includes: brokerage, slippage, impact
    - Shows why overtrading destroys profits
    
    Args:
        features (pd.DataFrame): Feature matrix with returns
        signal (pd.Series): Trading signals (1 or 0)
        transaction_cost (float): Per-trade cost (0.0005 = 0.05%)
    
    Returns:
        pd.DataFrame: DataFrame with returns and cumulative returns
    """
    
    # CRITICAL: Shift signal by 1 day
    # This ensures we trade based on yesterday's signal with today's return
    signal_shifted = signal.shift(1)
    
    # Calculate raw strategy returns
    # signal_shifted * return: only collect returns when signal = 1
    strategy_return = signal_shifted * features['Return']
    
    # Subtract transaction costs only when signal changes
    # Why only when it changes?
    # - Entering a trade costs transaction_cost
    # - Holding costs nothing
    # - Exiting a trade costs transaction_cost
    signal_change = signal_shifted.diff().abs()
    
    # Apply transaction cost when entering/exiting positions
    strategy_return = strategy_return - (signal_change * transaction_cost)
    
    print(f"\n" + "="*60)
    print("STRATEGY RETURNS (WITH SIGNAL SHIFT & TRANSACTION COSTS)")
    print("="*60)
    print(f"\nLook-Ahead Bias Prevention:")
    print(f"  ✓ Signal shifted by 1 day")
    print(f"  ✓ Trades executed day after signal generation")
    print(f"\nTransaction Costs:")
    print(f"  {transaction_cost:.4%} per trade")
    print(f"  Total trades (entries): {signal_change.sum():.0f}")
    
    # Build results dataframe
    results = pd.DataFrame(index=features.index)
    results['Signal'] = signal
    results['Signal_Shifted'] = signal_shifted
    results['Return'] = features['Return']
    results['Strategy_Return'] = strategy_return
    results['Cumulative_Return'] = (1 + strategy_return).cumprod() - 1
    results['Buy_Hold_Return'] = features['Return']
    results['Cumulative_BuyHold'] = (1 + features['Return']).cumprod() - 1
    
    # Remove NaN from signal shift
    results = results.dropna()
    
    print(f"\nPerformance Summary:")
    print(f"  Strategy Cumulative Return: {results['Cumulative_Return'].iloc[-1]:.2%}")
    print(f"  Buy & Hold Cumulative Return: {results['Cumulative_BuyHold'].iloc[-1]:.2%}")
    print(f"  Strategy Mean Daily Return: {results['Strategy_Return'].mean():.4%}")
    print(f"  Buy & Hold Mean Daily Return: {results['Buy_Hold_Return'].mean():.4%}")
    
    return results


if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from load_data import load_nifty_data
    from features import engineer_features
    
    data = load_nifty_data()
    features = engineer_features(data)
    signal = generate_momentum_signal(features, momentum_threshold=0.02)
    results = calculate_strategy_returns(features, signal, transaction_cost=0.0005)
    
    print("\n" + "="*60)
    print("First 10 rows of strategy results:")
    print(results.head(10))