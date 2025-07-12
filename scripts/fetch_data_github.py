"""
Script để fetch dữ liệu tài chính cho GitHub Actions
"""

import json
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from financial_data_fetcher import FinancialDataFetcher
from financial_data_fetcher.utils import create_summary_report, get_data_quality_score

def main():
    """Fetch dữ liệu và lưu vào file JSON"""
    
    print("Starting financial data fetch for GitHub Pages...")
    
    # Tạo thư mục docs nếu chưa có
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    data_dir = os.path.join(docs_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Khởi tạo fetcher
    fetcher = FinancialDataFetcher()
    
    try:
        # Fetch dữ liệu
        print("Fetching financial data...")
        data = fetcher.fetch_all_data()
        
        # Lưu dữ liệu chi tiết
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        detailed_file = os.path.join(data_dir, f"financial_data_{timestamp}.json")
        
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Lưu dữ liệu mới nhất (overwrite)
        latest_file = os.path.join(data_dir, "latest_data.json")
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Tạo summary data cho website
        summary_data = create_summary_data(data)
        summary_file = os.path.join(data_dir, "summary_data.json")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {detailed_file}")
        print(f"Latest data saved to {latest_file}")
        print(f"Summary data saved to {summary_file}")
        
        # Tạo báo cáo text
        report = create_summary_report(data)
        report_file = os.path.join(docs_dir, "latest_report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report saved to {report_file}")
        
        # Cập nhật historical data
        update_historical_data(data)
        
        print("Financial data fetch completed successfully!")
        
    except Exception as e:
        print(f"Error fetching financial data: {str(e)}")
        raise

def create_summary_data(data):
    """Tạo dữ liệu summary cho website"""
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "data_quality": get_data_quality_score(data),
        "assets": {}
    }
    
    # Precious Metals
    if 'precious_metals' in data:
        metals = data['precious_metals']
        
        if 'gold' in metals and 'current_price' in metals['gold']:
            summary["assets"]["gold"] = {
                "name": "Gold",
                "price": metals['gold']['current_price'],
                "change": metals['gold'].get('change', 0),
                "change_percent": metals['gold'].get('change_percent', 0),
                "currency": "USD",
                "unit": "oz"
            }
        
        if 'silver' in metals and 'current_price' in metals['silver']:
            summary["assets"]["silver"] = {
                "name": "Silver",
                "price": metals['silver']['current_price'],
                "change": metals['silver'].get('change', 0),
                "change_percent": metals['silver'].get('change_percent', 0),
                "currency": "USD",
                "unit": "oz"
            }
    
    # Stock Indices
    if 'stock_indices' in data:
        indices = data['stock_indices']
        
        if 'dow_jones' in indices and 'current_price' in indices['dow_jones']:
            summary["assets"]["dow_jones"] = {
                "name": "Dow Jones",
                "price": indices['dow_jones']['current_price'],
                "change": indices['dow_jones'].get('change', 0),
                "change_percent": indices['dow_jones'].get('change_percent', 0),
                "currency": "USD",
                "unit": "points"
            }
        
        if 'vn_index' in indices and 'current_price' in indices['vn_index']:
            summary["assets"]["vn_index"] = {
                "name": "VN Index",
                "price": indices['vn_index']['current_price'],
                "change": indices['vn_index'].get('change', 0),
                "change_percent": indices['vn_index'].get('change_percent', 0),
                "currency": "VND",
                "unit": "points"
            }
    
    # Bond Yields
    if 'bond_yields' in data:
        bonds = data['bond_yields']
        
        if 'us_10y_bond_yahoo' in bonds and 'current_price' in bonds['us_10y_bond_yahoo']:
            summary["assets"]["us_10y_bond"] = {
                "name": "US 10Y Treasury",
                "price": bonds['us_10y_bond_yahoo']['current_price'],
                "change": bonds['us_10y_bond_yahoo'].get('change', 0),
                "change_percent": bonds['us_10y_bond_yahoo'].get('change_percent', 0),
                "currency": "USD",
                "unit": "%"
            }
    
    # FX Rates
    if 'fx' in data:
        fx = data['fx']
        
        if 'usd_vnd' in fx and 'current_price' in fx['usd_vnd']:
            summary["assets"]["usd_vnd"] = {
                "name": "USD/VND",
                "price": fx['usd_vnd']['current_price'],
                "change": fx['usd_vnd'].get('change', 0),
                "change_percent": fx['usd_vnd'].get('change_percent', 0),
                "currency": "VND",
                "unit": "rate"
            }
        
        if 'eur_usd' in fx and 'current_price' in fx['eur_usd']:
            summary["assets"]["eur_usd"] = {
                "name": "EUR/USD",
                "price": fx['eur_usd']['current_price'],
                "change": fx['eur_usd'].get('change', 0),
                "change_percent": fx['eur_usd'].get('change_percent', 0),
                "currency": "USD",
                "unit": "rate"
            }
    
    return summary

def update_historical_data(current_data):
    """Cập nhật dữ liệu lịch sử"""
    
    historical_file = os.path.join("docs", "data", "historical_data.json")
    
    # Đọc dữ liệu lịch sử hiện tại
    historical_data = []
    if os.path.exists(historical_file):
        try:
            with open(historical_file, 'r', encoding='utf-8') as f:
                historical_data = json.load(f)
        except Exception as e:
            print(f"Error reading historical data: {e}")
            historical_data = []
    
    # Tạo entry mới
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "data": create_summary_data(current_data)
    }
    
    # Thêm entry mới
    historical_data.append(new_entry)
    
    # Giữ lại 90 ngày gần nhất
    historical_data = historical_data[-90:]
    
    # Lưu lại
    with open(historical_file, 'w', encoding='utf-8') as f:
        json.dump(historical_data, f, indent=2, ensure_ascii=False)
    
    print(f"Historical data updated with {len(historical_data)} entries")

if __name__ == "__main__":
    main()
