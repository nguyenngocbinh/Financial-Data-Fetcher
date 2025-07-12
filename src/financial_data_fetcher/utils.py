"""
Utility functions for Financial Data Fetcher
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os

def format_currency(value: float, currency: str = "USD") -> str:
    """
    Format currency value with proper symbol and formatting
    
    Args:
        value: The numeric value
        currency: Currency code (USD, VND, EUR, etc.)
    
    Returns:
        Formatted currency string
    """
    currency_symbols = {
        "USD": "$",
        "VND": "₫",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    if currency == "VND":
        return f"{value:,.0f} {symbol}"
    else:
        return f"{symbol}{value:,.2f}"

def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format percentage value with proper sign and formatting
    
    Args:
        value: The percentage value
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    return f"{value:+.{decimals}f}%"

def calculate_change(current: float, previous: float) -> Dict[str, float]:
    """
    Calculate absolute and percentage change
    
    Args:
        current: Current value
        previous: Previous value
    
    Returns:
        Dict with absolute and percentage change
    """
    if previous == 0:
        return {"absolute": 0, "percentage": 0}
    
    absolute_change = current - previous
    percentage_change = (absolute_change / previous) * 100
    
    return {
        "absolute": absolute_change,
        "percentage": percentage_change
    }

def is_market_open(market: str = "US") -> bool:
    """
    Check if market is currently open
    
    Args:
        market: Market code (US, VN, EU, etc.)
    
    Returns:
        Boolean indicating if market is open
    """
    now = datetime.now()
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    
    if market == "US":
        # US market: Monday-Friday, 9:30 AM - 4:00 PM ET
        if weekday >= 5:  # Weekend
            return False
        
        # Simplified check (ignoring timezone for now)
        hour = now.hour
        return 9 <= hour <= 16
    
    elif market == "VN":
        # Vietnam market: Monday-Friday, 9:00 AM - 3:00 PM ICT
        if weekday >= 5:  # Weekend
            return False
        
        hour = now.hour
        return 9 <= hour <= 15
    
    # Default to always open for other markets
    return True

def get_market_status(market: str = "US") -> Dict[str, Any]:
    """
    Get detailed market status
    
    Args:
        market: Market code
    
    Returns:
        Dict with market status information
    """
    is_open = is_market_open(market)
    now = datetime.now()
    
    return {
        "market": market,
        "is_open": is_open,
        "current_time": now.isoformat(),
        "weekday": now.strftime("%A"),
        "status": "Open" if is_open else "Closed"
    }

def clean_financial_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and validate financial data
    
    Args:
        data: Raw financial data
    
    Returns:
        Cleaned financial data
    """
    cleaned = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            cleaned[key] = clean_financial_data(value)
        elif isinstance(value, (int, float)):
            # Remove NaN and infinity values
            if np.isnan(value) or np.isinf(value):
                cleaned[key] = None
            else:
                cleaned[key] = value
        else:
            cleaned[key] = value
    
    return cleaned

def export_to_csv(data: Dict[str, Any], filename: str = "financial_data.csv"):
    """
    Export financial data to CSV
    
    Args:
        data: Financial data to export
        filename: Output filename
    """
    try:
        # Flatten the data structure
        flattened = flatten_dict(data)
        
        # Create DataFrame
        df = pd.DataFrame([flattened])
        
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
        
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nested keys
        sep: Separator for nested keys
    
    Returns:
        Flattened dictionary
    """
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)

def calculate_technical_indicators(prices: List[float], window: int = 20) -> Dict[str, float]:
    """
    Calculate basic technical indicators
    
    Args:
        prices: List of price values
        window: Window size for moving average
    
    Returns:
        Dict with technical indicators
    """
    if len(prices) < window:
        return {"error": f"Not enough data points. Need at least {window}"}
    
    prices_array = np.array(prices)
    
    # Simple Moving Average
    sma = np.mean(prices_array[-window:])
    
    # Exponential Moving Average
    ema = pd.Series(prices).ewm(span=window).mean().iloc[-1]
    
    # Volatility (standard deviation)
    volatility = np.std(prices_array[-window:])
    
    # RSI (simplified)
    deltas = np.diff(prices_array)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gains = np.mean(gains[-window:])
    avg_losses = np.mean(losses[-window:])
    
    if avg_losses == 0:
        rsi = 100
    else:
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
    
    return {
        "sma": float(sma),
        "ema": float(ema),
        "volatility": float(volatility),
        "rsi": float(rsi)
    }

def get_data_quality_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate data quality score
    
    Args:
        data: Financial data to evaluate
    
    Returns:
        Dict with quality metrics
    """
    total_fields = 0
    valid_fields = 0
    error_fields = 0
    
    def check_value(value):
        nonlocal total_fields, valid_fields, error_fields
        total_fields += 1
        
        if value is None:
            error_fields += 1
        elif isinstance(value, str) and "error" in value.lower():
            error_fields += 1
        elif isinstance(value, (int, float)) and (np.isnan(value) or np.isinf(value)):
            error_fields += 1
        else:
            valid_fields += 1
    
    def traverse(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                if isinstance(value, dict):
                    traverse(value)
                else:
                    check_value(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
        else:
            check_value(obj)
    
    traverse(data)
    
    quality_score = (valid_fields / total_fields * 100) if total_fields > 0 else 0
    
    return {
        "total_fields": total_fields,
        "valid_fields": valid_fields,
        "error_fields": error_fields,
        "quality_score": quality_score,
        "quality_grade": get_quality_grade(quality_score)
    }

def get_quality_grade(score: float) -> str:
    """
    Get quality grade based on score
    
    Args:
        score: Quality score (0-100)
    
    Returns:
        Quality grade (A, B, C, D, F)
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def create_summary_report(data: Dict[str, Any]) -> str:
    """
    Create a summary report of the financial data
    
    Args:
        data: Financial data
    
    Returns:
        Formatted summary report
    """
    report = []
    report.append("=== FINANCIAL DATA SUMMARY REPORT ===")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Data Quality
    quality = get_data_quality_score(data)
    report.append(f"Data Quality Score: {quality['quality_score']:.1f}% (Grade: {quality['quality_grade']})")
    report.append(f"Valid Fields: {quality['valid_fields']}/{quality['total_fields']}")
    report.append("")
    
    # Market Status
    us_status = get_market_status("US")
    vn_status = get_market_status("VN")
    report.append(f"US Market Status: {us_status['status']}")
    report.append(f"VN Market Status: {vn_status['status']}")
    report.append("")
    
    # Key Metrics
    if 'precious_metals' in data:
        report.append("PRECIOUS METALS:")
        metals = data['precious_metals']
        if 'gold' in metals and 'current_price' in metals['gold']:
            report.append(f"  Gold: {format_currency(metals['gold']['current_price'])}")
        if 'silver' in metals and 'current_price' in metals['silver']:
            report.append(f"  Silver: {format_currency(metals['silver']['current_price'])}")
        report.append("")
    
    if 'stock_indices' in data:
        report.append("STOCK INDICES:")
        indices = data['stock_indices']
        if 'dow_jones' in indices and 'current_price' in indices['dow_jones']:
            report.append(f"  Dow Jones: {indices['dow_jones']['current_price']:,.2f}")
        if 'vn_index' in indices and 'current_price' in indices['vn_index']:
            report.append(f"  VN Index: {indices['vn_index']['current_price']:,.2f}")
        report.append("")
    
    if 'fx' in data:
        report.append("FOREIGN EXCHANGE:")
        fx = data['fx']
        if 'usd_vnd' in fx and 'current_price' in fx['usd_vnd']:
            report.append(f"  USD/VND: {format_currency(fx['usd_vnd']['current_price'], 'VND')}")
        if 'eur_usd' in fx and 'current_price' in fx['eur_usd']:
            report.append(f"  EUR/USD: {fx['eur_usd']['current_price']:.4f}")
        report.append("")
    
    report.append("=" * 50)
    
    return "\n".join(report)

# Example usage
if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test currency formatting
    print(f"USD: {format_currency(1234.56, 'USD')}")
    print(f"VND: {format_currency(25000, 'VND')}")
    print(f"EUR: {format_currency(1234.56, 'EUR')}")
    
    # Test percentage formatting
    print(f"Percentage: {format_percentage(2.34)}")
    print(f"Percentage: {format_percentage(-1.23)}")
    
    # Test change calculation
    change = calculate_change(105, 100)
    print(f"Change: {change}")
    
    # Test market status
    us_status = get_market_status("US")
    print(f"US Market: {us_status}")
    
    # Test technical indicators
    prices = [100, 101, 102, 101, 103, 105, 104, 106, 107, 105, 108, 110, 109, 111, 112]
    indicators = calculate_technical_indicators(prices, window=10)
    print(f"Technical indicators: {indicators}")
    
    print("Utility functions test completed!")
