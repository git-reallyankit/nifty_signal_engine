"""
STEP 2: Feature Engineering
============================

Why this matters:
ML models cannot understand raw prices.
You must convert prices → numerical features that represent market behavior.

Features we'll build:
1. Returns: percentage daily movement
2. Moving Averages: trend detection
3. Volatility: risk/uncertainty measurement
4. Momentum: recent market strength
"""

import pandas as pd
import numpy as np


def compute_returns(data, column='Close'):
    """
    Compute daily returns.
    
    Formula:
    Return_t = (P_t - P_{t-1}) / P_{t-1}
    
    Why returns instead of prices?
    - Price 100→101 vs Price 1000→1001 both move by 1
    - But only 1% vs 0.1% return
    - Returns are normalized and comparable across different price levels
    
    Args:
        data (pd.DataFrame): OHLCV data
        column (str): Which column to use (usually 'Close')
    
    Returns:
        pd.Series: Daily returns (decimal form, e.g., 0.02 = 2%)
    """
    returns = data[column].pct_change()
    print(f"✓ Computed returns")
    print(f"  Mean daily return: {returns.mean():.4%}")
    print(f"  Std daily return: {returns.std():.4%}")
    return returns


def compute_moving_averages(data, windows=[5, 20], column='Close'):
    """
    Compute simple moving averages (SMA).
    
    MA_5: 5-day average (reacts quickly to recent prices)
    MA_20: 20-day average (smoother, shows longer trend)
    
    Why useful?
    - MA5 > MA20: Uptrend
    - MA5 < MA20: Downtrend
    - Used in trend-following strategies
    
    Args:
        data (pd.DataFrame): OHLCV data
        windows (list): Window sizes for moving averages
        column (str): Which column to use
    
    Returns:
        pd.DataFrame: DataFrame with MA columns
    """
    features = pd.DataFrame(index=data.index)
    
    for window in windows:
        ma_col = f'MA{window}'
        features[ma_col] = data[column].rolling(window=window).mean()
        print(f"✓ Computed {ma_col}")
    
    return features


def compute_volatility(returns, window=20):
    """
    Compute rolling volatility (standard deviation of returns).
    
    Formula:
    Volatility_t = std(returns[t-window:t])
    
    Why volatility matters?
    - High volatility = large price swings = higher risk AND opportunity
    - Low volatility = stable prices = predictable but less profitable
    - Used in risk management and signal filtering
    
    Key insight:
    Volatility is ONE OF THE MOST IMPORTANT concepts in quantitative finance.
    
    Args:
        returns (pd.Series): Daily returns
        window (int): Rolling window size (usually 20 days ≈ 1 month)
    
    Returns:
        pd.Series: Rolling volatility
    """
    volatility = returns.rolling(window=window).std()
    print(f"✓ Computed volatility")
    print(f"  Mean volatility: {volatility.mean():.4%}")
    print(f"  Max volatility: {volatility.max():.4%}")
    return volatility


def compute_momentum(data, window=10, column='Close'):
    """
    Compute momentum.
    
    Formula:
    Momentum_t = (P_t / P_{t-window}) - 1
    
    Intuition:
    - Measures how strongly price has moved recently
    - Positive: upward movement, negative: downward movement
    - One of the oldest and most reliable market anomalies
    
    Why 10 days?
    - Long enough to capture trend, short enough to react to changes
    - Different time horizons suit different strategies
    
    Args:
        data (pd.DataFrame): OHLCV data
        window (int): Lookback period (in days)
        column (str): Which column to use
    
    Returns:
        pd.Series: Momentum values
    """
    momentum = (data[column] / data[column].shift(window)) - 1
    print(f"✓ Computed momentum (window={window})")
    print(f"  Mean momentum: {momentum.mean():.4%}")
    return momentum


def engineer_features(data):
    """
    Compute all features for the dataset.
    
    This is the master function that creates your feature matrix.
    
    Returns a single DataFrame with all features aligned.
    """
    print("\n" + "="*60)
    print("FEATURE ENGINEERING")
    print("="*60 + "\n")
    
    features = pd.DataFrame(index=data.index)
    
    # Feature 1: Returns
    features['Return'] = compute_returns(data)
    
    # Feature 2: Moving Averages
    ma_features = compute_moving_averages(data, windows=[5, 20])
    features = features.join(ma_features)
    
    # Feature 3: Volatility
    features['Volatility'] = compute_volatility(features['Return'], window=20)
    
    # Feature 4: Momentum
    features['Momentum'] = compute_momentum(data, window=10)
    
    # Drop rows with NaN (due to rolling calculations)
    print(f"\nRemoving {features.isnull().sum().sum()} NaN values from rolling calculations...")
    features = features.dropna()
    
    print(f"\n✓ Feature engineering complete!")
    print(f"  Final dataset: {len(features)} days")
    print(f"\nFeature Summary:")
    print(features.describe())
    
    return features


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append('.')
    from load_data import load_nifty_data
    
    data = load_nifty_data()
    features = engineer_features(data)
    print("\n" + "="*60)
    print("First 5 rows of features:")
    print(features.head())