"""
Financial Data Fetcher Package
=============================

A Python package for fetching and analyzing financial data including:
- Gold prices
- Silver prices
- US 10-year Treasury yield
- Dow Jones index
- VN Index
- US Housing Price Index
- FX rates

Author: Your Name
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main modules
from .financial_data_fetcher import FinancialDataFetcher
from .dashboard import Dashboard
from .scheduler import Scheduler
from . import utils
from . import config

__all__ = [
    "FinancialDataFetcher",
    "Dashboard", 
    "Scheduler",
    "config",
    "utils"
]