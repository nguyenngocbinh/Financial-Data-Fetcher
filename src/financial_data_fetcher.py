import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional, Any
import config

class FinancialDataFetcher:
    """
    Lớp chính để lấy dữ liệu tài chính từ nhiều nguồn khác nhau
    """
    
    def __init__(self):
        self.symbols = config.SYMBOLS
        self.fred_series = config.FRED_SERIES
        self.data_dir = config.DATA_DIR
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Tạo thư mục data nếu chưa tồn tại"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def fetch_yahoo_finance_data(self, symbol: str, period: str = "1d") -> Dict[str, Any]:
        """
        Lấy dữ liệu từ Yahoo Finance
        
        Args:
            symbol: Mã chứng khoán (VD: "GC=F" cho vàng)
            period: Khoảng thời gian ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
        
        Returns:
            Dict chứa thông tin giá và metadata
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"error": f"No data found for {symbol}"}
            
            current_price = hist['Close'].iloc[-1]
            change = current_price - hist['Close'].iloc[-2] if len(hist) > 1 else 0
            change_percent = (change / hist['Close'].iloc[-2] * 100) if len(hist) > 1 and hist['Close'].iloc[-2] != 0 else 0
            
            return {
                "symbol": symbol,
                "current_price": float(current_price),
                "change": float(change),
                "change_percent": float(change_percent),
                "high": float(hist['High'].iloc[-1]),
                "low": float(hist['Low'].iloc[-1]),
                "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                "timestamp": datetime.now().isoformat(),
                "historical_data": hist.to_dict('records')
            }
            
        except Exception as e:
            return {"error": f"Error fetching data for {symbol}: {str(e)}"}
    
    def fetch_fred_data(self, series_id: str, limit: int = 1) -> Dict[str, Any]:
        """
        Lấy dữ liệu từ FRED (Federal Reserve Economic Data)
        
        Args:
            series_id: ID của series dữ liệu
            limit: Số lượng điểm dữ liệu mới nhất
        
        Returns:
            Dict chứa dữ liệu từ FRED
        """
        try:
            if not config.FRED_API_KEY or config.FRED_API_KEY == "your_fred_api_key":
                return {"error": "FRED API key not configured"}
            
            url = f"{config.FRED_BASE_URL}"
            params = {
                "series_id": series_id,
                "api_key": config.FRED_API_KEY,
                "file_type": "json",
                "limit": limit,
                "sort_order": "desc"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'observations' in data and data['observations']:
                latest = data['observations'][0]
                return {
                    "series_id": series_id,
                    "value": float(latest['value']) if latest['value'] != '.' else None,
                    "date": latest['date'],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": f"No data found for series {series_id}"}
                
        except Exception as e:
            return {"error": f"Error fetching FRED data for {series_id}: {str(e)}"}
    
    def fetch_vn_index_data(self) -> Dict[str, Any]:
        """
        Lấy dữ liệu VN Index
        Lưu ý: Đây là ví dụ cơ bản, có thể cần điều chỉnh tùy theo API thực tế
        """
        try:
            # Sử dụng Yahoo Finance cho VN Index
            return self.fetch_yahoo_finance_data("^VNI")
            
        except Exception as e:
            return {"error": f"Error fetching VN Index data: {str(e)}"}
    
    def fetch_currency_data(self, currency_pair: str) -> Dict[str, Any]:
        """
        Lấy dữ liệu tỷ giá hối đoái
        
        Args:
            currency_pair: Cặp tiền tệ (VD: "USDVND=X")
        
        Returns:
            Dict chứa thông tin tỷ giá
        """
        return self.fetch_yahoo_finance_data(currency_pair)
    
    def fetch_precious_metals_data(self) -> Dict[str, Any]:
        """
        Lấy dữ liệu kim loại quý (vàng, bạc)
        
        Returns:
            Dict chứa giá vàng và bạc
        """
        gold_data = self.fetch_yahoo_finance_data(self.symbols["gold"])
        silver_data = self.fetch_yahoo_finance_data(self.symbols["silver"])
        
        return {
            "gold": gold_data,
            "silver": silver_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def fetch_stock_indices_data(self) -> Dict[str, Any]:
        """
        Lấy dữ liệu các chỉ số chứng khoán
        
        Returns:
            Dict chứa dữ liệu các chỉ số
        """
        dow_jones_data = self.fetch_yahoo_finance_data(self.symbols["dow_jones"])
        vn_index_data = self.fetch_vn_index_data()
        
        return {
            "dow_jones": dow_jones_data,
            "vn_index": vn_index_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def fetch_bond_yields_data(self) -> Dict[str, Any]:
        """
        Lấy dữ liệu lợi suất trái phiếu
        
        Returns:
            Dict chứa lợi suất trái phiếu 10 năm Mỹ
        """
        # Thử lấy từ Yahoo Finance trước
        yahoo_data = self.fetch_yahoo_finance_data(self.symbols["us_10y_bond"])
        
        # Thử lấy từ FRED nếu cần
        fred_data = self.fetch_fred_data(self.fred_series["us_10y_bond"])
        
        return {
            "us_10y_bond_yahoo": yahoo_data,
            "us_10y_bond_fred": fred_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def fetch_housing_data(self) -> Dict[str, Any]:
        """
        Lấy dữ liệu chỉ số giá nhà
        
        Returns:
            Dict chứa chỉ số giá nhà
        """
        return self.fetch_fred_data(self.fred_series["housing_index"])
    
    def fetch_fx_data(self) -> Dict[str, Any]:
        """
        Lấy dữ liệu tỷ giá ngoại tệ
        
        Returns:
            Dict chứa các tỷ giá chính
        """
        usd_vnd_data = self.fetch_currency_data(self.symbols["usd_vnd"])
        eur_usd_data = self.fetch_currency_data(self.symbols["eur_usd"])
        
        return {
            "usd_vnd": usd_vnd_data,
            "eur_usd": eur_usd_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """
        Lấy tất cả dữ liệu tài chính
        
        Returns:
            Dict chứa tất cả dữ liệu
        """
        all_data = {
            "precious_metals": self.fetch_precious_metals_data(),
            "stock_indices": self.fetch_stock_indices_data(),
            "bond_yields": self.fetch_bond_yields_data(),
            "housing": self.fetch_housing_data(),
            "fx": self.fetch_fx_data(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Lưu dữ liệu vào file
        self.save_data_to_file(all_data)
        
        return all_data
    
    def save_data_to_file(self, data: Dict[str, Any], filename: Optional[str] = None):
        """
        Lưu dữ liệu vào file JSON
        
        Args:
            data: Dữ liệu cần lưu
            filename: Tên file (nếu không có sẽ tự động tạo theo timestamp)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_data_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {filepath}")
    
    def load_data_from_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Đọc dữ liệu từ file
        
        Args:
            filename: Tên file cần đọc
            
        Returns:
            Dict chứa dữ liệu hoặc None nếu lỗi
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data from {filepath}: {str(e)}")
            return None

# Ví dụ sử dụng
if __name__ == "__main__":
    fetcher = FinancialDataFetcher()
    
    print("Fetching financial data...")
    data = fetcher.fetch_all_data()
    
    print("\n=== PRECIOUS METALS ===")
    print(f"Gold: ${data['precious_metals']['gold'].get('current_price', 'N/A')}")
    print(f"Silver: ${data['precious_metals']['silver'].get('current_price', 'N/A')}")
    
    print("\n=== STOCK INDICES ===")
    print(f"Dow Jones: {data['stock_indices']['dow_jones'].get('current_price', 'N/A')}")
    print(f"VN Index: {data['stock_indices']['vn_index'].get('current_price', 'N/A')}")
    
    print("\n=== BOND YIELDS ===")
    print(f"US 10Y Bond (Yahoo): {data['bond_yields']['us_10y_bond_yahoo'].get('current_price', 'N/A')}%")
    
    print("\n=== FX RATES ===")
    print(f"USD/VND: {data['fx']['usd_vnd'].get('current_price', 'N/A')}")
    print(f"EUR/USD: {data['fx']['eur_usd'].get('current_price', 'N/A')}")
    
    print(f"\nData saved at: {data['timestamp']}")