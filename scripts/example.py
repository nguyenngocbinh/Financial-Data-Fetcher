"""
Ví dụ sử dụng Financial Data Fetcher
"""

import time
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from financial_data_fetcher import FinancialDataFetcher

def main():
    """Hàm chính để demo các tính năng"""
    
    print("=== FINANCIAL DATA FETCHER DEMO ===\n")
    
    # Khởi tạo fetcher
    fetcher = FinancialDataFetcher()
    
    # 1. Lấy dữ liệu kim loại quý
    print("1. Fetching precious metals data...")
    metals_data = fetcher.fetch_precious_metals_data()
    
    print("Gold Data:")
    if 'gold' in metals_data and 'current_price' in metals_data['gold']:
        gold = metals_data['gold']
        print(f"  Price: ${gold['current_price']:.2f}")
        print(f"  Change: {gold.get('change', 0):.2f} ({gold.get('change_percent', 0):+.2f}%)")
        print(f"  High: ${gold.get('high', 0):.2f}")
        print(f"  Low: ${gold.get('low', 0):.2f}")
    else:
        print("  No data available")
    
    print("\nSilver Data:")
    if 'silver' in metals_data and 'current_price' in metals_data['silver']:
        silver = metals_data['silver']
        print(f"  Price: ${silver['current_price']:.2f}")
        print(f"  Change: {silver.get('change', 0):.2f} ({silver.get('change_percent', 0):+.2f}%)")
        print(f"  High: ${silver.get('high', 0):.2f}")
        print(f"  Low: ${silver.get('low', 0):.2f}")
    else:
        print("  No data available")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Lấy dữ liệu chỉ số chứng khoán
    print("2. Fetching stock indices data...")
    indices_data = fetcher.fetch_stock_indices_data()
    
    print("Dow Jones Data:")
    if 'dow_jones' in indices_data and 'current_price' in indices_data['dow_jones']:
        dow = indices_data['dow_jones']
        print(f"  Index: {dow['current_price']:,.2f}")
        print(f"  Change: {dow.get('change', 0):.2f} ({dow.get('change_percent', 0):+.2f}%)")
        print(f"  High: {dow.get('high', 0):,.2f}")
        print(f"  Low: {dow.get('low', 0):,.2f}")
    else:
        print("  No data available")
    
    print("\nVN Index Data:")
    if 'vn_index' in indices_data and 'current_price' in indices_data['vn_index']:
        vn = indices_data['vn_index']
        print(f"  Index: {vn['current_price']:,.2f}")
        print(f"  Change: {vn.get('change', 0):.2f} ({vn.get('change_percent', 0):+.2f}%)")
        print(f"  High: {vn.get('high', 0):,.2f}")
        print(f"  Low: {vn.get('low', 0):,.2f}")
    else:
        print("  No data available")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Lấy dữ liệu trái phiếu
    print("3. Fetching bond yields data...")
    bond_data = fetcher.fetch_bond_yields_data()
    
    print("US 10Y Treasury Bond:")
    if 'us_10y_bond_yahoo' in bond_data and 'current_price' in bond_data['us_10y_bond_yahoo']:
        bond = bond_data['us_10y_bond_yahoo']
        print(f"  Yield: {bond['current_price']:.2f}%")
        print(f"  Change: {bond.get('change', 0):.2f} ({bond.get('change_percent', 0):+.2f}%)")
    else:
        print("  No data available")
    
    print("\n" + "="*50 + "\n")
    
    # 4. Lấy dữ liệu tỷ giá
    print("4. Fetching FX data...")
    fx_data = fetcher.fetch_fx_data()
    
    print("USD/VND Rate:")
    if 'usd_vnd' in fx_data and 'current_price' in fx_data['usd_vnd']:
        usd_vnd = fx_data['usd_vnd']
        print(f"  Rate: {usd_vnd['current_price']:,.0f}")
        print(f"  Change: {usd_vnd.get('change', 0):.2f} ({usd_vnd.get('change_percent', 0):+.2f}%)")
    else:
        print("  No data available")
    
    print("\nEUR/USD Rate:")
    if 'eur_usd' in fx_data and 'current_price' in fx_data['eur_usd']:
        eur_usd = fx_data['eur_usd']
        print(f"  Rate: {eur_usd['current_price']:.4f}")
        print(f"  Change: {eur_usd.get('change', 0):.4f} ({eur_usd.get('change_percent', 0):+.2f}%)")
    else:
        print("  No data available")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Lấy tất cả dữ liệu
    print("5. Fetching all data...")
    all_data = fetcher.fetch_all_data()
    
    print("All data fetched and saved!")
    print(f"Timestamp: {all_data.get('timestamp', 'N/A')}")
    
    # 6. Demo real-time monitoring
    print("\n6. Real-time monitoring (5 updates, 10 seconds apart)...")
    for i in range(5):
        print(f"\nUpdate {i+1}/5:")
        
        # Lấy giá vàng
        gold_data = fetcher.fetch_yahoo_finance_data(fetcher.symbols["gold"])
        if 'current_price' in gold_data:
            print(f"  Gold: ${gold_data['current_price']:.2f}")
        
        # Lấy Dow Jones
        dow_data = fetcher.fetch_yahoo_finance_data(fetcher.symbols["dow_jones"])
        if 'current_price' in dow_data:
            print(f"  Dow Jones: {dow_data['current_price']:,.2f}")
        
        # Lấy USD/VND
        usd_vnd_data = fetcher.fetch_yahoo_finance_data(fetcher.symbols["usd_vnd"])
        if 'current_price' in usd_vnd_data:
            print(f"  USD/VND: {usd_vnd_data['current_price']:,.0f}")
        
        if i < 4:  # Không delay ở lần cuối
            time.sleep(10)
    
    print("\n" + "="*50)
    print("Demo completed!")

def demo_json_export():
    """Demo xuất dữ liệu ra JSON"""
    print("\n=== JSON EXPORT DEMO ===")
    
    fetcher = FinancialDataFetcher()
    data = fetcher.fetch_all_data()
    
    # Xuất ra file JSON đẹp
    with open('demo_financial_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Data exported to demo_financial_data.json")
    
    # Hiển thị một phần dữ liệu
    print("\nSample data structure:")
    print(json.dumps({
        "timestamp": data.get('timestamp'),
        "precious_metals": {
            "gold": data.get('precious_metals', {}).get('gold', {}).get('current_price', 'N/A'),
            "silver": data.get('precious_metals', {}).get('silver', {}).get('current_price', 'N/A')
        },
        "stock_indices": {
            "dow_jones": data.get('stock_indices', {}).get('dow_jones', {}).get('current_price', 'N/A'),
            "vn_index": data.get('stock_indices', {}).get('vn_index', {}).get('current_price', 'N/A')
        }
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
        demo_json_export()
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
    except Exception as e:
        print(f"\nError in demo: {str(e)}")
        print("Make sure you have internet connection and all dependencies installed")
