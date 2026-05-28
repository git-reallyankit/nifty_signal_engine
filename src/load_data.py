"""
STEP 1: Load Market Data
========================

Why this matters:
- You cannot build a quant system without data
- This is your raw research material
- yfinance is reliable for NIFTY data

What this does:
- Downloads historical NIFTY data (^NSEI ticker)
- Saves to CSV for reproducibility
- Validates data integrity
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os


def download_nifty_data(ticker="^NSEI", years=5, save_path="../data/nifty.csv"):
    """
    Download historical NIFTY data from yfinance.
    
    Args:
        ticker (str): Yahoo Finance ticker for NIFTY index
        years (int): Number of years of historical data to fetch
        save_path (str): Path to save the CSV file
    
    Returns:
        pd.DataFrame: DataFrame with OHLCV data
    
    Key insight:
    - We download 5 years as a good balance between:
      * enough data for meaningful statistics
      * not too old (market behavior changes)
    """
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    
    print(f"Downloading NIFTY data from {start_date.date()} to {end_date.date()}...")
    
    # Download data
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        progress=False
    )
    
    print(f"✓ Downloaded {len(data)} trading days")
    print(f"\nData Info:")
    print(f"Start Date: {data.index[0].date()}")
    print(f"End Date: {data.index[-1].date()}")
    print(f"Columns: {list(data.columns)}")
    
    # Validate data
    if data.isnull().sum().sum() > 0:
        print(f"\n Warning: {data.isnull().sum().sum()} null values found")
        print("Dropping rows with nulls...")
        data = data.dropna()

    # After downloading/loading data
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)  # Keep only 'Close', 'High', etc.
    
    # Create parent directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save to CSV
    data.to_csv(save_path)
    print(f"\n Data saved to {save_path}")
    
    # Show first few rows
    print("\nFirst 5 rows of data:")
    print(data.head())
    
    return data


def load_nifty_data(csv_path="../data/nifty.csv"):
    """
    Load NIFTY data from CSV.
    
    Used when data is already downloaded and saved.
    """
    data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    print(f"✓ Loaded {len(data)} trading days from {csv_path}")
    return data


if __name__ == "__main__":
    # Download and save data
    nifty_data = download_nifty_data()