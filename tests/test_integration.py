"""
Comprehensive test suite for Financial Data Fetcher
"""

import os
import json
import subprocess
import sys
from datetime import datetime
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from financial_data_fetcher import config

def test_basic_functionality():
    """Test basic data fetching functionality"""
    
    print("=== TESTING BASIC FUNCTIONALITY ===\n")
    
    try:
        from financial_data_fetcher import FinancialDataFetcher
        
        fetcher = FinancialDataFetcher()
        
        # Test precious metals
        print("1. Testing precious metals data...")
        metals_data = fetcher.fetch_precious_metals_data()
        
        if 'gold' in metals_data and 'current_price' in metals_data.get('gold', {}):
            print(f"✅ Gold price: ${metals_data['gold']['current_price']:.2f}")
        else:
            print("⚠️ Gold data not available")
        
        # Test stock indices
        print("\n2. Testing stock indices data...")
        indices_data = fetcher.fetch_stock_indices_data()
        
        if 'dow_jones' in indices_data and 'current_price' in indices_data.get('dow_jones', {}):
            print(f"✅ Dow Jones: {indices_data['dow_jones']['current_price']:,.2f}")
        else:
            print("⚠️ Dow Jones data not available")
        
        # Test FX data
        print("\n3. Testing FX data...")
        fx_data = fetcher.fetch_fx_data()
        
        if 'usd_vnd' in fx_data and 'current_price' in fx_data.get('usd_vnd', {}):
            print(f"✅ USD/VND: {fx_data['usd_vnd']['current_price']:,.0f}")
        else:
            print("⚠️ USD/VND data not available")
        
        print("\n✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False

def test_fred_api():
    """Test FRED API connection"""
    
    print("\n=== TESTING FRED API ===\n")
    
    # Check API key
    if not config.FRED_API_KEY or config.FRED_API_KEY == "your_fred_api_key":
        print("⚠️ FRED API key not configured")
        print("📋 To get a FREE API key:")
        print("1. Go to https://fred.stlouisfed.org/")
        print("2. Create free account")
        print("3. Get API key from My Account → API Keys")
        print("4. Add to .env file: FRED_API_KEY=your_key_here")
        return False
    
    print(f"✅ API key configured: {config.FRED_API_KEY[:8]}...")
    
    # Test API connection
    try:
        url = config.FRED_BASE_URL
        params = {
            "series_id": "DGS10",
            "api_key": config.FRED_API_KEY,
            "file_type": "json",
            "limit": 1,
            "sort_order": "desc"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data and data['observations']:
                observation = data['observations'][0]
                value = observation.get('value', 'N/A')
                print(f"✅ 10-Year Treasury Rate: {value}%")
                return True
        
        print(f"❌ FRED API test failed: HTTP {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ FRED API test failed: {str(e)}")
        return False

def test_github_pages_setup():
    """Test GitHub Pages setup"""
    
    print("\n=== TESTING GITHUB PAGES SETUP ===\n")
    
    # Test 1: Generate data
    print("1. Testing data generation...")
    try:
        # Import scripts from scripts directory
        scripts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
        sys.path.insert(0, scripts_path)
        
        from fetch_data_github import main as fetch_main
        from generate_html_report import main as generate_main
        
        fetch_main()
        generate_main()
        print("✅ Data generation successful!")
    except Exception as e:
        print(f"❌ Data generation failed: {e}")
        return False
    
    # Test 2: Check required files
    print("\n2. Checking required files...")
    required_files = [
        "docs/index.html",
        "docs/data/latest_data.json",
        "docs/data/summary_data.json"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 0:
                print(f"✅ {file_path} ({size} bytes)")
            else:
                print(f"❌ {file_path} is empty")
                return False
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Test 3: Validate JSON
    print("\n3. Validating JSON data...")
    try:
        with open("docs/data/summary_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "assets" in data and data["assets"]:
            print(f"✅ JSON data valid with {len(data['assets'])} assets")
        else:
            print("❌ JSON data invalid or empty")
            return False
    except Exception as e:
        print(f"❌ JSON validation failed: {e}")
        return False
    
    print("\n✅ GitHub Pages setup test passed!")
    return True

def test_deployment_readiness():
    """Test deployment readiness"""
    
    print("\n=== TESTING DEPLOYMENT READINESS ===\n")
    
    # Test git availability
    print("1. Checking git availability...")
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Git available: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git not available")
        return False
    
    # Test git repository
    print("\n2. Checking git repository...")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        print("✅ Git repository ready")
    except subprocess.CalledProcessError:
        print("❌ Not a git repository")
        return False
    
    # Test workflow files
    print("\n3. Checking workflow files...")
    workflow_files = [
        ".github/workflows/update-data.yml"
    ]
    
    for file_path in workflow_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("\n✅ Deployment readiness test passed!")
    return True

def run_all_tests():
    """Run all tests"""
    
    print("🚀 RUNNING COMPREHENSIVE TESTS FOR FINANCIAL DATA FETCHER\n")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("FRED API", test_fred_api),
        ("GitHub Pages Setup", test_github_pages_setup),
        ("Deployment Readiness", test_deployment_readiness)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"RUNNING: {test_name}")
        print('='*60)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print('='*60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Project is ready for deployment!")
        show_next_steps()
    else:
        print("⚠️ Some tests failed. Please fix the issues before deployment.")
        show_troubleshooting()

def show_next_steps():
    """Show next steps after successful tests"""
    
    print("\n🎯 NEXT STEPS:")
    print("1. Create GitHub repository (public)")
    print("2. Upload all files to repository")
    print("3. Enable GitHub Pages in Settings")
    print("4. Enable GitHub Actions with read/write permissions")
    print("5. Run workflow manually for first time")
    print("\n📖 See GITHUB_PAGES_SETUP.md for detailed instructions")

def show_troubleshooting():
    """Show troubleshooting tips"""
    
    print("\n🔧 TROUBLESHOOTING:")
    print("1. Check internet connection")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Get FRED API key (free) from https://fred.stlouisfed.org/")
    print("4. Check GitHub Actions permissions")
    print("5. Verify all files are present")

if __name__ == "__main__":
    run_all_tests()
