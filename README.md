# Financial Data Fetcher - GitHub Pages

🌟 **Live Demo**: [https://nguyenngocbinh.github.io/financial-data-fetcher/](https://nguyenngocbinh.github.io/financial-data-fetcher/)

## Overview

Automated financial data dashboard that updates daily via GitHub Actions and displays on GitHub Pages.

### Data Sources (All FREE)
- 🥇 **Gold & Silver** prices (Yahoo Finance)
- 📈 **Stock Indices** (Dow Jones, VN Index)
- 🏦 **US 10Y Treasury** bond yields (FRED API)
- 💱 **Foreign Exchange** rates (USD/VND, EUR/USD)

### Features
- ✅ **Auto-updates** twice daily (9 AM & 1 PM UTC)
- ✅ **Responsive** design for mobile & desktop
- ✅ **Data quality** monitoring
- ✅ **Historical data** tracking (90 days)
- ✅ **Error handling** and fallbacks

## Quick Start

### Option 1: Quick Demo
```bash
python quickstart.py
```

### Option 2: Full Example
```bash
python scripts/example.py
```

### Option 3: Windows Menu
```batch
run.bat
```

### Option 4: Run Tests
```bash
python -m pytest tests/ -v
```

## GitHub Pages Deployment

### Option 1: GitHub Pro ($4/month) - Private Source
1. Create **private repository**
2. Upload files
3. Enable GitHub Pages
4. Enable GitHub Actions

### Option 2: Public Repository (Free)
1. Create **public repository**
2. Upload files  
3. Enable GitHub Pages
4. Enable GitHub Actions

## API Keys (FREE)

### FRED API Key
1. Go to [fred.stlouisfed.org](https://fred.stlouisfed.org/)
2. Create free account
3. Get API key
4. Add to repository secrets: `FRED_API_KEY`

## 📁 Project Structure

This is a well-organized Python package for fetching and analyzing financial data with the following structure:

```
financial_data_fetcher/
├── 📁 src/financial_data_fetcher/      # Main package source code
│   ├── __init__.py                    # Package initialization
│   ├── financial_data_fetcher.py      # Main data fetching logic
│   ├── dashboard.py                   # Web dashboard
│   ├── scheduler.py                   # Task scheduling
│   ├── utils.py                       # Utility functions
│   └── config.py                      # Configuration settings
│
├── 📁 scripts/                        # Executable scripts
│   ├── __init__.py                    # Scripts package init
│   ├── example.py                     # Usage examples
│   ├── fetch_data_github.py           # GitHub-specific data fetching
│   ├── generate_html_report.py        # HTML report generation
│   └── clean.py                       # Cleanup utility
│
├── 📁 tests/                          # Test suite
│   ├── __init__.py                    # Test package init
│   ├── test_financial_data_fetcher.py # Unit tests
│   └── test_integration.py            # Integration tests
│
├── 📁 data/                           # Data directory
│   └── README.md                      # Data documentation
│
├── 📁 docs/                           # Documentation
│   └── index.html                     # Website template
│
├── 📁 .github/workflows/              # GitHub Actions
│   ├── ci-cd.yml                      # CI/CD pipeline
│   └── update-data.yml                # Data update workflow
│
├── 📄 Root Files
│   ├── quickstart.py                  # Quick start script
│   ├── run.bat                        # Windows batch script
│   ├── Makefile                       # Build automation
│   └── README.md                      # Main documentation
│
├── 📄 Configuration Files
│   ├── requirements.txt               # Production dependencies
│   ├── requirements-dev.txt           # Development dependencies
│   ├── .env.example                   # Environment variables template
│   ├── pyproject.toml                 # Modern Python project config
│   ├── setup.py                       # Package setup (legacy)
│   └── tox.ini                        # Testing across Python versions
│
├── 📁 Documentation
│   ├── COMPLETE_GUIDE.md              # Comprehensive guide
│   ├── PRIVATE_TO_PUBLIC_GUIDE.md     # Privacy guide
│   └── LICENSE                        # MIT license
│
└── 📁 Build & Distribution
    ├── MANIFEST.in                    # Package manifest
    └── .gitignore                     # Git ignore rules
```

### 🏗️ Package Features

#### ✅ Production Ready
- **Proper Python Package Structure**: Follows PEP standards
- **Dependency Management**: Separate prod/dev requirements
- **Configuration Management**: Environment-based config
- **Error Handling**: Comprehensive error handling
- **Logging**: Structured logging throughout

#### ✅ Development Tools
- **Testing**: Unit tests + integration tests
- **Code Quality**: Black formatting, flake8 linting
- **Type Checking**: MyPy static type checking
- **CI/CD**: GitHub Actions workflows
- **Cross-platform**: Works on Windows, macOS, Linux

#### ✅ Distribution
- **PyPI Ready**: Can be published to PyPI
- **Docker Support**: Can be containerized
- **GitHub Pages**: Automated web deployment
- **Documentation**: Comprehensive guides

### 🧪 Testing

#### Run All Tests
```bash
pytest tests/ -v
```

#### Run with Coverage
```bash
pytest tests/ -v --cov=financial_data_fetcher --cov-report=html
```

#### Test Multiple Python Versions
```bash
tox
```

### 🏗️ Building

#### Build Package
```bash
python -m build
```

#### Install Locally
```bash
pip install -e .
```

### 🧹 Cleanup

#### Clean Cache & Temp Files
```bash
python clean.py
```

#### Clean Everything
```bash
make clean
```

### 📊 What's Included

- **Financial Data Sources**: Yahoo Finance, FRED API
- **Data Types**: Stocks, bonds, commodities, FX, indices
- **Visualization**: Plotly charts, web dashboard
- **Automation**: Scheduling, GitHub Actions
- **Documentation**: Complete guides and examples

### 🔧 Removed/Optimized

The project has been optimized by:
- ✅ Removing duplicate files
- ✅ Consolidating test files
- ✅ Organizing into proper package structure
- ✅ Adding proper configuration files
- ✅ Including build and distribution tools
- ✅ Creating comprehensive documentation

This is now a professional, production-ready Python package! 🎉

## Documentation

- **📖 Complete Guide**: See `COMPLETE_GUIDE.md` for detailed instructions
- **🔒 Private Setup**: See `PRIVATE_TO_PUBLIC_GUIDE.md` for private source code
- **⚙️ Configuration**: Edit `config.py` for customization

## Testing

```bash
# Run comprehensive tests
python test_all.py

# Or use batch file (Windows)
run.bat
```

## URLs After Deployment

- **Main page**: `https://username.github.io/financial-data-fetcher/`
- **API data**: `https://username.github.io/financial-data-fetcher/data/latest_data.json`

## Troubleshooting

1. **Run tests**: `python test_all.py`
2. **Check logs**: GitHub Actions tab
3. **Verify API keys**: Repository secrets
4. **Read guides**: `COMPLETE_GUIDE.md`

## Disclaimer

⚠️ **For informational purposes only. Not financial advice.**

## License

MIT License - Free for personal and commercial use.
