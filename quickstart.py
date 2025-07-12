#!/usr/bin/env python3
"""
Quick start script for Financial Data Fetcher - Updated Version
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from financial_data_fetcher import FinancialDataFetcher
import config

def main():
    """Quick demo using updated configuration"""
    print("🚀 Financial Data Fetcher - Quick Start (Updated)")
    print("=" * 50)
    
    fetcher = FinancialDataFetcher()
    
    # Quick test with new config
    print("\n📊 Fetching sample data...")
    try:
        # Test gold price using new config
        gold_data = fetcher.fetch_yahoo_finance_data(config.YFINANCE_SYMBOLS["gold"])
        
        if "error" not in gold_data:
            print("✅ Gold data fetched successfully!")
            print(f"� Gold Price: ${gold_data['current_price']:.2f}")
            print(f"📈 Change: {gold_data['change_percent']:+.2f}%")
        else:
            print(f"⚠️ Error: {gold_data['error']}")
            
        # Test another symbol
        btc_data = fetcher.fetch_yahoo_finance_data(config.YFINANCE_SYMBOLS["bitcoin"])
        if "error" not in btc_data:
            print(f"₿ Bitcoin Price: ${btc_data['current_price']:.2f}")
            print(f"📈 Change: {btc_data['change_percent']:+.2f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Next steps:")
    print("1. Run: python scripts/example.py")
    print("2. Or use: python run.bat (Windows)")
    print("3. Or use: make demo (Linux/macOS)")

if __name__ == "__main__":
    main()
