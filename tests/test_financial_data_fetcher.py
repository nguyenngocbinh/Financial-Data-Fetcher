"""
Unit tests for financial_data_fetcher module
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import tempfile
import json

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from financial_data_fetcher import FinancialDataFetcher
from financial_data_fetcher.config import SYMBOLS, FRED_SYMBOLS


class TestFinancialDataFetcher:
    """Test cases for FinancialDataFetcher class"""

    def setup_method(self):
        """Setup test environment"""
        self.fetcher = FinancialDataFetcher()

    def test_init(self):
        """Test FinancialDataFetcher initialization"""
        assert self.fetcher is not None
        assert hasattr(self.fetcher, 'fred_api_key')

    @patch('yfinance.download')
    def test_fetch_yahoo_data(self, mock_download):
        """Test fetching data from Yahoo Finance"""
        # Mock data
        mock_data = pd.DataFrame({
            'Close': [100, 101, 102],
            'Volume': [1000, 1100, 1200]
        })
        mock_download.return_value = mock_data
        
        result = self.fetcher.fetch_yahoo_data(['AAPL'], period='1mo')
        
        assert isinstance(result, dict)
        mock_download.assert_called_once()

    @patch('fredapi.Fred')
    def test_fetch_fred_data(self, mock_fred):
        """Test fetching data from FRED API"""
        # Mock FRED API
        mock_fred_instance = MagicMock()
        mock_fred_instance.get_series.return_value = pd.Series([1.5, 1.6, 1.7])
        mock_fred.return_value = mock_fred_instance
        
        result = self.fetcher.fetch_fred_data(['DGS10'], period='1mo')
        
        assert isinstance(result, dict)
        mock_fred.assert_called_once()

    def test_config_symbols(self):
        """Test that configuration symbols are properly defined"""
        assert isinstance(SYMBOLS, dict)
        assert isinstance(FRED_SYMBOLS, dict)
        assert len(SYMBOLS) > 0
        assert len(FRED_SYMBOLS) > 0

    def test_save_data(self):
        """Test saving data to file"""
        test_data = {"test": {"Close": [100, 101, 102]}}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.fetcher.save_data(test_data, temp_file)
            
            # Check if file was created and contains data
            assert os.path.exists(temp_file)
            
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)
                assert loaded_data == test_data
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_load_data(self):
        """Test loading data from file"""
        test_data = {"test": {"Close": [100, 101, 102]}}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            json.dump(test_data, f)
        
        try:
            loaded_data = self.fetcher.load_data(temp_file)
            assert loaded_data == test_data
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_load_nonexistent_file(self):
        """Test loading data from non-existent file"""
        result = self.fetcher.load_data("nonexistent_file.json")
        assert result is None


if __name__ == '__main__':
    pytest.main([__file__])
