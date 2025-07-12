# Configuration file for Financial Data Fetcher

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (optional - most data sources work without API keys)
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
FRED_API_KEY = os.getenv("FRED_API_KEY", "")

# Data sources - Using Python libraries instead of direct API calls
# Primary: yfinance (Yahoo Finance) - most reliable
# Secondary: fredapi (FRED API) - requires free API key
# Tertiary: investpy (investing.com) - backup option
DATA_SOURCES = {
    "primary": "yfinance",      # Yahoo Finance via yfinance library
    "secondary": "fredapi",     # FRED API via fredapi library  
    "tertiary": "investpy"      # Investing.com via investpy library
}

# Symbols and tickers for yfinance (Yahoo Finance)
YFINANCE_SYMBOLS = {
    "gold": "GC=F",          # Gold futures
    "silver": "SI=F",        # Silver futures
    "dow_jones": "^DJI",     # Dow Jones Industrial Average
    "us_10y_bond": "^TNX",   # 10-Year Treasury Note Yield
    "usd_vnd": "USDVND=X",   # USD/VND exchange rate
    "eur_usd": "EURUSD=X",   # EUR/USD exchange rate
    "oil": "CL=F",           # Crude Oil futures
    "bitcoin": "BTC-USD",    # Bitcoin
    "ethereum": "ETH-USD",   # Ethereum
    "sp500": "^GSPC",        # S&P 500
    "nasdaq": "^IXIC"        # NASDAQ
}

# Vietnamese market symbols (alternative sources)
VN_SYMBOLS = {
    "vn_index": "^VNI",      # Vietnam Index (may not work in yfinance)
    "vn30": "^VN30"          # VN30 Index
}

# Alternative data sources for Vietnamese market
VN_DATA_SOURCES = {
    "vndirect": "https://dchart-api.vndirect.com.vn/dchart/history",
    "investing": "vietnam-indices"  # For investpy library
}

# FRED series IDs (requires free API key from FRED)
FRED_SERIES = {
    "us_10y_bond": "DGS10",           # 10-Year Treasury Constant Maturity Rate
    "housing_index": "CSUSHPISA",     # Case-Shiller U.S. National Home Price Index
    "unemployment_rate": "UNRATE",    # Unemployment Rate
    "inflation_rate": "CPIAUCSL",     # Consumer Price Index
    "gdp": "GDP",                     # Gross Domestic Product
    "federal_funds_rate": "FEDFUNDS"  # Federal Funds Rate
}

# Required Python libraries
REQUIRED_LIBRARIES = {
    "yfinance": ">=0.2.10",          # Yahoo Finance data
    "fredapi": ">=0.5.0",            # FRED API wrapper
    "pandas": ">=1.3.0",             # Data manipulation
    "numpy": ">=1.21.0",             # Numerical computing
    "requests": ">=2.25.0",          # HTTP requests
    "python-dotenv": ">=0.19.0"      # Environment variables
}

# Optional libraries for enhanced functionality
OPTIONAL_LIBRARIES = {
    "investpy": ">=1.0.8",           # Investing.com data
    "plotly": ">=5.0.0",             # Interactive charts
    "dash": ">=2.0.0",               # Web dashboard
    "beautifulsoup4": ">=4.9.0",     # Web scraping
    "lxml": ">=4.6.0"                # XML/HTML parser
}

# Update intervals (in minutes)
UPDATE_INTERVALS = {
    "real_time": 5,         # Every 5 minutes
    "hourly": 60,           # Every hour
    "daily": 1440,          # Every day
    "weekly": 10080         # Every week
}

# Data retrieval settings
DATA_SETTINGS = {
    "period": "1y",         # Default period for historical data
    "interval": "1d",       # Default interval (1d, 1h, 5m, etc.)
    "auto_adjust": True,    # Auto-adjust prices for splits/dividends
    "prepost": True,        # Include pre/post market data
    "threads": True         # Use threading for multiple symbol downloads
}

# Error handling and retry settings
ERROR_HANDLING = {
    "max_retries": 3,       # Maximum number of retry attempts
    "retry_delay": 5,       # Delay between retries (seconds)
    "timeout": 30,          # Request timeout (seconds)
    "fallback_enabled": True # Enable fallback data sources
}

# Data storage
DATA_DIR = "data"
DATABASE_FILE = "financial_data.db"
CACHE_DURATION = 300        # Cache duration in seconds (5 minutes)

# Dashboard settings
DASHBOARD_PORT = 8050
DASHBOARD_HOST = "127.0.0.1"
DEBUG_MODE = True

# Backward compatibility - keep old attribute names for existing code
SYMBOLS = YFINANCE_SYMBOLS  # Alias for backward compatibility

# Backward compatibility - keep old URL constants
YAHOO_FINANCE_BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
VN_INDEX_URL = "https://www.cophieu68.vn/export/stockprice.php"