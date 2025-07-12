#!/usr/bin/env python3
"""
Quick start script for Financial Data Fetcher
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from financial_data_fetcher import FinancialDataFetcher

def main():
    """Quick demo"""
    print("🚀 Financial Data Fetcher - Quick Start")
    print("=" * 50)
    
    fetcher = FinancialDataFetcher()
    
    # Quick test
    print("\n📊 Fetching sample data...")
    try:
        data = fetcher.fetch_precious_metals_data()
        if data:
            print("✅ Data fetched successfully!")
            print(f"📈 Sample: {list(data.keys())[:3]}")
        else:
            print("⚠️ No data available")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Next steps:")
    print("1. Run: python scripts/example.py")
    print("2. Or use: python run.bat (Windows)")
    print("3. Or use: make demo (Linux/macOS)")

if __name__ == "__main__":
    main()
