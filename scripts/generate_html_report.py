"""
Script để generate HTML report cho GitHub Pages
"""

import json
import os
import sys
from datetime import datetime
from jinja2 import Template
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def main():
    """Generate HTML report"""
    
    print("Generating HTML report for GitHub Pages...")
    
    # Đọc dữ liệu
    try:
        with open("docs/data/summary_data.json", 'r', encoding='utf-8') as f:
            summary_data = json.load(f)
    except Exception as e:
        print(f"Error reading summary data: {e}")
        return
    
    # Tạo HTML
    html_content = generate_html_page(summary_data)
    
    # Lưu HTML
    with open("docs/index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML report generated successfully!")
    
    # Tạo charts
    generate_charts(summary_data)

def generate_html_page(data):
    """Generate HTML page với dữ liệu tài chính"""
    
    template_str = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Data Dashboard - Daily Update</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .update-time {
            color: #7f8c8d;
            font-size: 1.1em;
        }
        
        .quality-score {
            background: #27ae60;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 10px;
            font-weight: bold;
        }
        
        .assets-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .asset-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .asset-card:hover {
            transform: translateY(-5px);
        }
        
        .asset-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .asset-price {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .asset-change {
            font-size: 1.1em;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
        }
        
        .positive {
            background-color: #d4edda;
            color: #155724;
        }
        
        .negative {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .neutral {
            background-color: #e2e3e5;
            color: #383d41;
        }
        
        .precious-metals .asset-card {
            border-left: 5px solid #f39c12;
        }
        
        .stock-indices .asset-card {
            border-left: 5px solid #3498db;
        }
        
        .bonds .asset-card {
            border-left: 5px solid #27ae60;
        }
        
        .fx .asset-card {
            border-left: 5px solid #e74c3c;
        }
        
        .section-title {
            font-size: 1.8em;
            color: white;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        
        .footer {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-top: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .footer p {
            color: #7f8c8d;
            margin-bottom: 10px;
        }
        
        .github-link {
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }
        
        .github-link:hover {
            text-decoration: underline;
        }
        
        .charts-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .chart-container {
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            .assets-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .asset-price {
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Financial Data Dashboard</h1>
            <p class="update-time">Last Update: {{ data.update_time }}</p>
            <div class="quality-score">
                Data Quality: {{ "%.1f"|format(data.data_quality.quality_score) }}% ({{ data.data_quality.quality_grade }})
            </div>
        </div>
        
        <!-- Precious Metals Section -->
        <div class="precious-metals">
            <h2 class="section-title">🥇 Precious Metals</h2>
            <div class="assets-grid">
                {% if data.assets.gold %}
                <div class="asset-card">
                    <div class="asset-name">Gold ({{ data.assets.gold.unit }})</div>
                    <div class="asset-price">${{ "%.2f"|format(data.assets.gold.price) }}</div>
                    <div class="asset-change {{ 'positive' if data.assets.gold.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.gold.change_percent) }}%
                        ({{ "{:+.2f}".format(data.assets.gold.change) }})
                    </div>
                </div>
                {% endif %}
                
                {% if data.assets.silver %}
                <div class="asset-card">
                    <div class="asset-name">Silver ({{ data.assets.silver.unit }})</div>
                    <div class="asset-price">${{ "%.2f"|format(data.assets.silver.price) }}</div>
                    <div class="asset-change {{ 'positive' if data.assets.silver.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.silver.change_percent) }}%
                        ({{ "{:+.2f}".format(data.assets.silver.change) }})
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Stock Indices Section -->
        <div class="stock-indices">
            <h2 class="section-title">📈 Stock Indices</h2>
            <div class="assets-grid">
                {% if data.assets.dow_jones %}
                <div class="asset-card">
                    <div class="asset-name">{{ data.assets.dow_jones.name }}</div>
                    <div class="asset-price">{{ "{:,.2f}".format(data.assets.dow_jones.price) }}</div>
                    <div class="asset-change {{ 'positive' if data.assets.dow_jones.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.dow_jones.change_percent) }}%
                        ({{ "{:+.2f}".format(data.assets.dow_jones.change) }})
                    </div>
                </div>
                {% endif %}
                
                {% if data.assets.vn_index %}
                <div class="asset-card">
                    <div class="asset-name">{{ data.assets.vn_index.name }}</div>
                    <div class="asset-price">{{ "{:,.2f}".format(data.assets.vn_index.price) }}</div>
                    <div class="asset-change {{ 'positive' if data.assets.vn_index.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.vn_index.change_percent) }}%
                        ({{ "{:+.2f}".format(data.assets.vn_index.change) }})
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Bonds Section -->
        <div class="bonds">
            <h2 class="section-title">🏦 Bond Yields</h2>
            <div class="assets-grid">
                {% if data.assets.us_10y_bond %}
                <div class="asset-card">
                    <div class="asset-name">{{ data.assets.us_10y_bond.name }}</div>
                    <div class="asset-price">{{ "%.2f"|format(data.assets.us_10y_bond.price) }}%</div>
                    <div class="asset-change {{ 'positive' if data.assets.us_10y_bond.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.us_10y_bond.change_percent) }}%
                        ({{ "{:+.2f}".format(data.assets.us_10y_bond.change) }})
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- FX Section -->
        <div class="fx">
            <h2 class="section-title">💱 Foreign Exchange</h2>
            <div class="assets-grid">
                {% if data.assets.usd_vnd %}
                <div class="asset-card">
                    <div class="asset-name">{{ data.assets.usd_vnd.name }}</div>
                    <div class="asset-price">{{ "{:,.0f}".format(data.assets.usd_vnd.price) }}</div>
                    <div class="asset-change {{ 'positive' if data.assets.usd_vnd.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.usd_vnd.change_percent) }}%
                        ({{ "{:+.2f}".format(data.assets.usd_vnd.change) }})
                    </div>
                </div>
                {% endif %}
                
                {% if data.assets.eur_usd %}
                <div class="asset-card">
                    <div class="asset-name">{{ data.assets.eur_usd.name }}</div>
                    <div class="asset-price">{{ "%.4f"|format(data.assets.eur_usd.price) }}</div>
                    <div class="asset-change {{ 'positive' if data.assets.eur_usd.change_percent >= 0 else 'negative' }}">
                        {{ "{:+.2f}".format(data.assets.eur_usd.change_percent) }}%
                        ({{ "{:+.4f}".format(data.assets.eur_usd.change) }})
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Charts Section -->
        <div class="charts-section">
            <h2 class="section-title" style="color: #2c3e50;">📊 Price Charts</h2>
            <div class="chart-container">
                <div id="price-chart"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 Automatically updated by GitHub Actions</p>
            <p>📊 Data sources: Yahoo Finance, FRED API</p>
            <p>⚠️ For informational purposes only. Not financial advice.</p>
            <p>
                <a href="https://github.com/your-username/financial-data-fetcher" class="github-link">
                    View on GitHub
                </a>
            </p>
        </div>
    </div>
    
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        // Add interactive charts here if needed
        console.log('Financial Data Dashboard loaded successfully!');
    </script>
</body>
</html>"""
    
    template = Template(template_str)
    return template.render(data=data)

def generate_charts(data):
    """Generate charts for the website"""
    
    # Create a simple price comparison chart
    assets = []
    prices = []
    changes = []
    
    for asset_key, asset_data in data['assets'].items():
        if asset_key not in ['usd_vnd', 'us_10y_bond']:  # Skip currency and bond for comparison
            assets.append(asset_data['name'])
            prices.append(asset_data['price'])
            changes.append(asset_data['change_percent'])
    
    if assets:
        # Create bar chart
        fig = go.Figure()
        
        colors = ['green' if x >= 0 else 'red' for x in changes]
        
        fig.add_trace(go.Bar(
            x=assets,
            y=changes,
            marker_color=colors,
            text=[f"{x:+.2f}%" for x in changes],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Daily Price Changes (%)",
            xaxis_title="Assets",
            yaxis_title="Change (%)",
            template="plotly_white",
            height=400
        )
        
        # Save chart as HTML
        fig.write_html("docs/data/price_chart.html")
        
        print("Price chart generated successfully!")

if __name__ == "__main__":
    # Install jinja2 if not available
    try:
        from jinja2 import Template
    except ImportError:
        print("Installing jinja2...")
        os.system("pip install jinja2")
        from jinja2 import Template
    
    main()
