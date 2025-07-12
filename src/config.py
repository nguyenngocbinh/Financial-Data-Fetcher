# Configuration file for Financial Data Fetcher

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (add your own keys)
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "your_alpha_vantage_api_key")
FRED_API_KEY = os.getenv("FRED_API_KEY", "your_fred_api_key")

# Data sources URLs
YAHOO_FINANCE_BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
VN_INDEX_URL = "https://www.cophieu68.vn/export/stockprice.php"

# Symbols and tickers
SYMBOLS = {
    "gold": "GC=F",  # Gold futures
    "silver": "SI=F",  # Silver futures
    "dow_jones": "^DJI",  # Dow Jones Industrial Average
    "us_10y_bond": "^TNX",  # 10-Year Treasury Note Yield
    "vn_index": "^VNI",  # Vietnam Index
    "usd_vnd": "USDVND=X",  # USD/VND exchange rate
    "eur_usd": "EURUSD=X",  # EUR/USD exchange rate
    "housing_index": "CSUSHPISA"  # Case-Shiller U.S. National Home Price Index
}

# FRED series IDs
FRED_SERIES = {
    "us_10y_bond": "DGS10",
    "housing_index": "CSUSHPISA",
    "unemployment_rate": "UNRATE",
    "inflation_rate": "CPIAUCSL"
}

# Update intervals (in minutes)
UPDATE_INTERVALS = {
    "real_time": 5,
    "hourly": 60,
    "daily": 1440
}

# Data storage
DATA_DIR = "data"
DATABASE_FILE = "financial_data.db"

# Dashboard settings
DASHBOARD_PORT = 8050
DASHBOARD_HOST = "127.0.0.1"