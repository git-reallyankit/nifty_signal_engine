# NIFTY Signal Research Engine - Phase 1

A professional **market research pipeline** teaching quantitative finance fundamentals.

**This is NOT:** A profitable trading bot, HFT engine, or prediction model.

**This IS:** How real quants structure research. The foundation for advanced ML-based strategies.

---

## 🎯 What You'll Learn

### 1. How Financial Data Behaves
- Market data is noisy, sequential, time-dependent, non-stationary
- Think in returns, volatility, trends, risk-adjusted metrics
- NOT in absolute prices

### 2. How Quants Structure Research
Real quant workflow:
```
Data → Features → Signal → Backtest → Metrics → Improve
```

### 3. How ML Connects to Markets
Before ML: you need clean data, engineered features, realistic evaluation.
Otherwise ML becomes useless noise-fitting.

---

## 🏗️ Architecture

```
NIFTY Data
    ↓
Feature Engineering (Returns, MA, Volatility, Momentum)
    ↓
Signal Generation (Momentum > 2% → Buy)
    ↓
Backtesting (Simulate historical performance)
    ↓
Performance Metrics (Sharpe, Drawdown, Win Rate)
    ↓
Visualization (Build intuition)
```

---

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
cd src
python main.py
```

This will:
1. Download 5 years of NIFTY historical data
2. Compute features (returns, moving averages, volatility, momentum)
3. Generate trading signals based on momentum
4. Backtest the strategy with transaction costs
5. Calculate performance metrics (Sharpe, drawdown, etc)
6. Generate 5 visualization plots

---

## 📖 Detailed Components

### STEP 1: Load Data (`load_data.py`)

**Why?** You cannot build without data. It's your raw research material.

```python
from load_data import download_nifty_data
data = download_nifty_data()  # 5 years of NIFTY history
```

**Output:**
- Date, Open, High, Low, Close, Volume
- 1200+ trading days of data

---

### STEP 2: Feature Engineering (`features.py`)

**Why?** ML models cannot understand raw prices. Convert prices → interpretable quantities.

#### Feature 1: Returns
```
Return_t = (P_t - P_{t-1}) / P_{t-1}
```
- Normalizes price movement
- Move from 100→101 and 1000→1001 both have different % returns
- Essential for understanding volatility structure

#### Feature 2: Moving Averages
- MA5: 5-day average (quick reaction)
- MA20: 20-day average (smooth trend)
- Used for trend detection and crossover signals

#### Feature 3: Volatility
```
Rolling standard deviation of returns (20-day window)
```
- Measures "how violently prices move"
- NOT direction, NOT profitability
- One of the MOST important concepts in finance

#### Feature 4: Momentum
```
Momentum_t = (P_t / P_{t-10}) - 1
```
- Measures recent market strength
- Oldest and most reliable market anomaly
- Used in momentum-following strategies

---

### STEP 3: Signal Generation (`strategy.py`)

**Why?** Convert features into trading logic.

Simple rule:
```python
if momentum > 0.02:  # > 2% over 10 days
    signal = 1       # Go long
else:
    signal = 0       # Stay in cash
```

**NOT prediction.** Just trend-following logic.

---

### CRITICAL: Signal Shifting

⚠️ **Most beginner strategies fail here.**

```
Day 1 (Tuesday): Calculate signal at market close
Day 2 (Wednesday): Execute trade based on yesterday's signal
```

Why? You only know today's close AFTER market close.

**Code:**
```python
strategy_return = signal.shift(1) * return - transaction_cost
```

This prevents **look-ahead bias** (using future information).

---

### STEP 4: Backtesting (`strategy.py`)

Simulate historical strategy performance.

**Important:** Backtesting shows "what would have happened historically," NOT proof of future profitability.

---

### STEP 5: Performance Metrics (`metrics.py`)

#### Cumulative Return
Simple total growth. Doesn't account for risk.

#### Sharpe Ratio ⭐ MOST IMPORTANT
```
Sharpe = (mean_return - risk_free_rate) / std_return * √252
```
- Measures return per unit of risk
- Higher = smoother returns
- \>1.0 is good, >2.0 is excellent

#### Maximum Drawdown
Largest peak-to-trough decline.
- Psychologically important
- Shows if strategy is bearable

#### Win Rate
% of profitable days. Less important than Sharpe.

---

### STEP 6: Visualization (`plots.py`)

5 plots generated:

1. **Price + Moving Averages**: See trends
2. **Volatility**: Identify spikes and quiet periods
3. **Momentum & Signals**: Trading logic visualization
4. **Cumulative Returns**: Strategy vs Buy & Hold
5. **Drawdown**: Risk visualization

---

## ⚠️ Common Mistakes to Avoid

### ❌ Trying ML immediately
No. ML comes AFTER: data, features, clean backtesting.

### ❌ Using future information
Very common. Always shift signals.

### ❌ Optimizing parameters endlessly
No endless grid search. Keep it simple.

### ❌ Obsessing over profits
You're learning infrastructure, not becoming profitable this week.

---

## 🧠 What You Should Understand

NOT: "My strategy made money."

BUT:
- ✅ What returns are and why they matter
- ✅ Why volatility is critical in finance
- ✅ Why signal shifting prevents look-ahead bias
- ✅ Why transaction costs destroy naive strategies
- ✅ How quants structure research pipelines
- ✅ Why proper backtesting methodology matters
- ✅ The connection between risk and return

---

## 📊 Expected Results

This momentum strategy typically shows:
- **Cumulative Return:** Variable (depends on market regime)
- **Sharpe Ratio:** 0.3 - 0.8 (modest, not great)
- **Buy & Hold Sharpe:** Often better! (market has been trending up)
- **Max Drawdown:** Similar or slightly better than buy-and-hold

**Key insight:** Simple strategies often don't beat the market. But they teach you the infrastructure.

---

## 🚀 What Happens Next Week

Once this foundation works, add:
- Logistic regression classifier
- Binary prediction targets (up/down days)
- Train/test split for realistic evaluation
- Feature importance analysis
- Confusion matrix and classification metrics

Then your project becomes interview-worthy ML + finance work.

---

## 📂 Project Structure

```
nifty_signal_engine/
├── data/
│   └── nifty.csv              # Downloaded NIFTY data
├── src/
│   ├── load_data.py           # Data download/loading
│   ├── features.py            # Feature engineering
│   ├── strategy.py            # Signal generation & returns
│   ├── metrics.py             # Performance evaluation
│   ├── plots.py               # Visualization
│   └── main.py                # Master script
├── plots/                      # Generated visualization plots
│   ├── 01_price_and_moving_averages.png
│   ├── 02_volatility.png
│   ├── 03_momentum_and_signals.png
│   ├── 04_cumulative_returns.png
│   └── 05_drawdown.png
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Troubleshooting

### "No module named yfinance"
```bash
pip install yfinance
```

### Data download fails
- Check internet connection
- yfinance servers may be temporarily down
- Try again in a few minutes

### No data directory
```bash
mkdir data
```

### Plots not saving
```bash
mkdir plots
```

---

## 📚 Key Concepts Summary

| Concept | Why It Matters |
|---------|----------------|
| Returns | Normalize price movement; enable comparability |
| Volatility | Measure risk/uncertainty; key for position sizing |
| Momentum | Market anomaly; trend-following signal |
| Signal Shifting | Prevent look-ahead bias; realistic backtesting |
| Transaction Costs | Real-world constraint; destroy naive strategies |
| Sharpe Ratio | Risk-adjusted performance; industry standard |
| Drawdown | Psychological impact; risk management |
| Backtesting | Historical validation; not future prediction |

---

## 📖 References

- Sharpe Ratio: https://en.wikipedia.org/wiki/Sharpe_ratio
- Momentum Anomaly: "The Cross-Section of Expected Stock Returns" (Fama & French)
- Backtesting Best Practices: "Designing Backtests" (Pardo)

---

## ⚖️ Disclaimer

**Past performance is not indicative of future results.**

This is educational material. Do not trade real money based on this strategy without:
- Proper risk management
- Realistic slippage/cost assumptions
- Forward testing on new data
- Professional financial advice

---

## 🎯 Success Criteria for Week 1

✅ Data loads correctly  
✅ Features computed correctly  
✅ Strategy returns computed correctly  
✅ Sharpe ratio computed  
✅ Transaction cost added  
✅ At least 5 plots generated  
✅ **Most importantly:** You understand WHY each step exists  

---

## 📧 Questions?

Read the comments in each module. They explain the "why" behind every line.

Real quant work is NOT "follow tutorials." It's understanding each step deeply.

**Build carefully.**

---

*NIFTY Signal Research Engine - Phase 1*  
*Foundation layer of a hybrid quant + ML system*  
*Last updated: 2024*