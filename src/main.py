"""
NIFTY Signal Research Engine - Phase 1
========================================

Master script that orchestrates the entire pipeline:

1. Load Data
2. Feature Engineering
3. Signal Generation
4. Backtesting & Metrics
5. Visualization

Run this to execute the complete analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from load_data import download_nifty_data, load_nifty_data
from features import engineer_features
from strategy import generate_momentum_signal, calculate_strategy_returns
from metrics import evaluate_strategy
from plots import generate_all_plots


def main():
    """
    Main execution function.
    """
    
    print("\n" + "="*80)
    print(" "*20 + "NIFTY SIGNAL RESEARCH ENGINE - PHASE 1")
    print("="*80)
    print("\nGoal: Build the foundation layer of a hybrid quant + ML system")
    print("You are NOT building a profitable trading bot.")
    print("You ARE building a market research pipeline.")
    print("\n" + "="*80 + "\n")
    
    # ========== STEP 1: DATA ==========
    print("STEP 1: DOWNLOADING & LOADING DATA")
    print("-" * 80)
    
    try:
        data = load_nifty_data()
    except FileNotFoundError:
        print("\nData not found. Downloading from yfinance...")
        data = download_nifty_data()
    
    # ========== STEP 2: FEATURES ==========
    print("\n\nSTEP 2: FEATURE ENGINEERING")
    print("-" * 80)
    
    features = engineer_features(data)
    
    # ========== STEP 3: SIGNALS ==========
    print("\n\nSTEP 3: SIGNAL GENERATION")
    print("-" * 80)
    
    signal = generate_momentum_signal(features, momentum_threshold=0.02)
    
    # ========== STEP 4 & 5: STRATEGY & METRICS ==========
    print("\n\nSTEP 4: CALCULATE STRATEGY RETURNS")
    print("-" * 80)
    
    results = calculate_strategy_returns(features, signal, transaction_cost=0.0005)
    
    print("\n\nSTEP 5: EVALUATE BACKTEST RESULTS")
    print("-" * 80)
    
    metrics = evaluate_strategy(results)
    
    # ========== STEP 6: VISUALIZATION ==========
    print("\n\nSTEP 6: GENERATE VISUALIZATIONS")
    print("-" * 80)
    
    generate_all_plots(data, features, signal, results)
    
    # ========== FINAL SUMMARY ==========
    print("\n" + "="*80)
    print("EXECUTION COMPLETE")
    print("="*80)
    print("\n📊 Generated Files:")
    print("  Data: data/nifty.csv")
    print("  Plots: plots/01_*.png through 05_*.png")
    print("\n✅ Week 1 Success Checklist:")
    print("  ✓ Data loads correctly")
    print("  ✓ Features computed correctly")
    print("  ✓ Strategy returns computed correctly")
    print("  ✓ Sharpe ratio computed")
    print("  ✓ Transaction cost added")
    print("  ✓ Plots generated")
    print("  ✓ You understand WHY each step exists")
    print("\n📚 Key Learnings:")
    print("  • Returns normalize price movement")
    print("  • Moving averages detect trends")
    print("  • Volatility measures risk/uncertainty")
    print("  • Momentum is a market anomaly")
    print("  • Signal shifting prevents look-ahead bias")
    print("  • Transaction costs destroy naive strategies")
    print("  • Sharpe ratio measures risk-adjusted returns")
    print("  • Visualization builds market intuition")
    print("\n🚀 Next Week:")
    print("  • Add logistic regression classifier")
    print("  • Create prediction targets (binary: up/down)")
    print("  • Train/test split for realistic evaluation")
    print("  • Feature importance analysis")
    print("  • Confusion matrix and classification metrics")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()