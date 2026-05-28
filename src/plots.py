"""
STEP 6: Visualization
=====================

Why visualize?
==============

Raw numbers don't build intuition.

You need to SEE:
• Price trends
• Volatility spikes
• Strategy behavior
• When it works, when it fails
• Drawdown periods

This is critical for understanding what's happening.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def plot_price_and_moving_averages(data, features, figsize=(14, 6)):
    """
    Plot price with moving averages.
    
    Shows:
    - Close price (black)
    - 5-day MA (orange, fast, reactive)
    - 20-day MA (blue, slow, smooth)
    
    Signals:
    - Price above MA20: uptrend
    - Price below MA20: downtrend
    - MA5 crossing MA20: momentum shift
    """
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot price
    ax.plot(data.index, data['Close'], label='Close Price', 
            color='black', linewidth=1.5, alpha=0.8)
    
    # Plot moving averages
    ax.plot(features.index, features['MA5'], label='MA5 (5-day)', 
            color='orange', linewidth=1.5, alpha=0.7)
    ax.plot(features.index, features['MA20'], label='MA20 (20-day)', 
            color='blue', linewidth=1.5, alpha=0.7)
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Price (₹)', fontsize=12, fontweight='bold')
    ax.set_title('NIFTY Price with Moving Averages', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Date formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('../plots/01_price_and_moving_averages.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: plots/01_price_and_moving_averages.png")
    plt.close()


def plot_volatility(features, figsize=(14, 5)):
    """
    Plot rolling volatility over time.
    
    Shows:
    - High volatility spikes (red zones)
    - Low volatility periods (stable)
    - Relation to market stress events
    """
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot volatility
    ax.fill_between(features.index, features['Volatility'], alpha=0.3, color='red')
    ax.plot(features.index, features['Volatility'], color='darkred', linewidth=1.5)
    
    # Add mean line
    mean_vol = features['Volatility'].mean()
    ax.axhline(y=mean_vol, color='green', linestyle='--', alpha=0.5, 
               label=f'Mean Volatility: {mean_vol:.4%}')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Volatility (Std Dev of Returns)', fontsize=12, fontweight='bold')
    ax.set_title('NIFTY 20-Day Rolling Volatility', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Date formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('../plots/02_volatility.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: plots/02_volatility.png")
    plt.close()


def plot_momentum(features, signal, figsize=(14, 6)):
    """
    Plot momentum and trading signals.
    
    Shows:
    - Momentum line (oscillates around 0)
    - Signal threshold (horizontal line)
    - Buy signals (green dots where signal turns on)
    - Position status (background shading)
    """
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot momentum
    ax.plot(features.index, features['Momentum'], label='Momentum', 
            color='blue', linewidth=1, alpha=0.7)
    
    # Add threshold line
    threshold = 0.02
    ax.axhline(y=threshold, color='green', linestyle='--', linewidth=2, 
               label=f'Threshold ({threshold:.2%})')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Shade buy regions (where signal = 1)
    for i in range(len(signal)-1):
        if signal.iloc[i] == 1:
            ax.axvspan(signal.index[i], signal.index[i+1], alpha=0.1, color='green')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Momentum', fontsize=12, fontweight='bold')
    ax.set_title('Momentum and Trading Signals', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Date formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('../plots/03_momentum_and_signals.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: plots/03_momentum_and_signals.png")
    plt.close()


def plot_cumulative_returns(results, figsize=(14, 7)):
    """
    Plot cumulative returns: Strategy vs Buy & Hold.
    
    This is the most important plot.
    Shows if strategy outperforms buy-and-hold.
    
    Visual indicators:
    - Strategy above buy-hold: strategy winning
    - Strategy below buy-hold: strategy losing
    - Sharp drops: maximum drawdown periods
    """
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot cumulative returns
    ax.plot(results.index, results['Cumulative_Return'] * 100, 
            label='Strategy', color='green', linewidth=2.5, alpha=0.8)
    ax.plot(results.index, results['Cumulative_BuyHold'] * 100, 
            label='Buy & Hold (Benchmark)', color='blue', linewidth=2.5, alpha=0.8)
    
    # Fill between for visualization
    ax.fill_between(results.index, 
                     results['Cumulative_Return'] * 100,
                     results['Cumulative_BuyHold'] * 100,
                     where=(results['Cumulative_Return'] > results['Cumulative_BuyHold']),
                     alpha=0.2, color='green', label='Strategy Outperforming')
    ax.fill_between(results.index,
                     results['Cumulative_Return'] * 100,
                     results['Cumulative_BuyHold'] * 100,
                     where=(results['Cumulative_Return'] <= results['Cumulative_BuyHold']),
                     alpha=0.2, color='red', label='Buy & Hold Outperforming')
    
    # Add zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Return (%)', fontsize=12, fontweight='bold')
    ax.set_title('Strategy vs Buy & Hold Cumulative Returns', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Date formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('../plots/04_cumulative_returns.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: plots/04_cumulative_returns.png")
    plt.close()


def plot_drawdown(results, figsize=(14, 6)):
    """
    Plot drawdown over time.
    
    Shows:
    - Worst peak-to-trough losses
    - Psychological impact of strategy
    - Risk management need
    """
    
    def compute_drawdown(cumulative_returns):
        wealth = 1 + cumulative_returns
        running_max = wealth.expanding().max()
        drawdown = (wealth - running_max) / running_max * 100
        return drawdown
    
    strategy_dd = compute_drawdown(results['Cumulative_Return'])
    buyhold_dd = compute_drawdown(results['Cumulative_BuyHold'])
    
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.fill_between(results.index, strategy_dd, alpha=0.3, color='green', label='Strategy')
    ax.plot(results.index, strategy_dd, color='darkgreen', linewidth=1.5)
    
    ax.fill_between(results.index, buyhold_dd, alpha=0.3, color='blue', label='Buy & Hold')
    ax.plot(results.index, buyhold_dd, color='darkblue', linewidth=1.5)
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Drawdown (%)', fontsize=12, fontweight='bold')
    ax.set_title('Drawdown Comparison: Strategy vs Buy & Hold', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Date formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('../plots/05_drawdown.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: plots/05_drawdown.png")
    plt.close()


def generate_all_plots(data, features, signal, results):
    """
    Generate all visualizations.
    """
    import os
    
    # Create plots directory
    os.makedirs('../plots', exist_ok=True)
    
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60 + "\n")
    
    plot_price_and_moving_averages(data, features)
    plot_volatility(features)
    plot_momentum(features, signal)
    plot_cumulative_returns(results)
    plot_drawdown(results)
    
    print(f"\n✓ All plots saved to plots/ directory")


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
    
    generate_all_plots(data, features, signal, results)