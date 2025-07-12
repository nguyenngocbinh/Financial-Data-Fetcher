import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime, timedelta
import os
from financial_data_fetcher import FinancialDataFetcher
import config

class FinancialDashboard:
    """
    Dashboard web để hiển thị dữ liệu tài chính real-time
    """
    
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.fetcher = FinancialDataFetcher()
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Thiết lập giao diện dashboard"""
        self.app.layout = html.Div([
            html.H1("Financial Data Dashboard", 
                   style={'text-align': 'center', 'margin-bottom': '30px'}),
            
            # Controls
            html.Div([
                html.Button("Refresh Data", id="refresh-btn", n_clicks=0,
                           style={'margin': '10px', 'padding': '10px 20px'}),
                html.Div(id="last-update", style={'margin': '10px'})
            ], style={'text-align': 'center'}),
            
            # Precious Metals Section
            html.Div([
                html.H2("Precious Metals", style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.H3("Gold", style={'color': '#FFD700'}),
                        html.Div(id="gold-price", style={'font-size': '24px', 'font-weight': 'bold'}),
                        html.Div(id="gold-change", style={'font-size': '16px'})
                    ], className="metric-box", style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                    
                    html.Div([
                        html.H3("Silver", style={'color': '#C0C0C0'}),
                        html.Div(id="silver-price", style={'font-size': '24px', 'font-weight': 'bold'}),
                        html.Div(id="silver-change", style={'font-size': '16px'})
                    ], className="metric-box", style={'width': '48%', 'display': 'inline-block', 'margin': '1%'})
                ])
            ], style={'margin': '20px 0'}),
            
            # Stock Indices Section
            html.Div([
                html.H2("Stock Indices", style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.H3("Dow Jones", style={'color': '#1f77b4'}),
                        html.Div(id="dow-price", style={'font-size': '24px', 'font-weight': 'bold'}),
                        html.Div(id="dow-change", style={'font-size': '16px'})
                    ], className="metric-box", style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                    
                    html.Div([
                        html.H3("VN Index", style={'color': '#ff7f0e'}),
                        html.Div(id="vn-price", style={'font-size': '24px', 'font-weight': 'bold'}),
                        html.Div(id="vn-change", style={'font-size': '16px'})
                    ], className="metric-box", style={'width': '48%', 'display': 'inline-block', 'margin': '1%'})
                ])
            ], style={'margin': '20px 0'}),
            
            # Bond Yields Section
            html.Div([
                html.H2("Bond Yields", style={'text-align': 'center'}),
                html.Div([
                    html.H3("US 10Y Treasury", style={'color': '#2ca02c'}),
                    html.Div(id="bond-yield", style={'font-size': '24px', 'font-weight': 'bold'}),
                    html.Div(id="bond-change", style={'font-size': '16px'})
                ], className="metric-box", style={'width': '48%', 'margin': '1% auto', 'display': 'block'})
            ], style={'margin': '20px 0'}),
            
            # FX Section
            html.Div([
                html.H2("Foreign Exchange", style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.H3("USD/VND", style={'color': '#d62728'}),
                        html.Div(id="usdvnd-rate", style={'font-size': '24px', 'font-weight': 'bold'}),
                        html.Div(id="usdvnd-change", style={'font-size': '16px'})
                    ], className="metric-box", style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                    
                    html.Div([
                        html.H3("EUR/USD", style={'color': '#9467bd'}),
                        html.Div(id="eurusd-rate", style={'font-size': '24px', 'font-weight': 'bold'}),
                        html.Div(id="eurusd-change", style={'font-size': '16px'})
                    ], className="metric-box", style={'width': '48%', 'display': 'inline-block', 'margin': '1%'})
                ])
            ], style={'margin': '20px 0'}),
            
            # Chart Section
            html.Div([
                html.H2("Price Charts", style={'text-align': 'center'}),
                dcc.Dropdown(
                    id='chart-selector',
                    options=[
                        {'label': 'Gold', 'value': 'gold'},
                        {'label': 'Silver', 'value': 'silver'},
                        {'label': 'Dow Jones', 'value': 'dow_jones'},
                        {'label': 'VN Index', 'value': 'vn_index'},
                        {'label': 'US 10Y Bond', 'value': 'us_10y_bond'},
                        {'label': 'USD/VND', 'value': 'usd_vnd'},
                        {'label': 'EUR/USD', 'value': 'eur_usd'}
                    ],
                    value='gold',
                    style={'margin': '10px'}
                ),
                dcc.Graph(id='price-chart')
            ], style={'margin': '20px 0'}),
            
            # Auto-refresh interval
            dcc.Interval(
                id='interval-component',
                interval=5*60*1000,  # 5 minutes
                n_intervals=0
            ),
            
            # Store for data
            dcc.Store(id='financial-data-store')
        ])
    
    def setup_callbacks(self):
        """Thiết lập callbacks cho dashboard"""
        
        @callback(
            [Output('financial-data-store', 'data'),
             Output('last-update', 'children')],
            [Input('refresh-btn', 'n_clicks'),
             Input('interval-component', 'n_intervals')]
        )
        def update_financial_data(n_clicks, n_intervals):
            """Cập nhật dữ liệu tài chính"""
            try:
                data = self.fetcher.fetch_all_data()
                update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return data, f"Last updated: {update_time}"
            except Exception as e:
                return {}, f"Error updating data: {str(e)}"
        
        @callback(
            [Output('gold-price', 'children'),
             Output('gold-change', 'children'),
             Output('silver-price', 'children'),
             Output('silver-change', 'children')],
            [Input('financial-data-store', 'data')]
        )
        def update_precious_metals(data):
            """Cập nhật giá kim loại quý"""
            if not data or 'precious_metals' not in data:
                return "N/A", "N/A", "N/A", "N/A"
            
            metals = data['precious_metals']
            
            # Gold
            gold_price = "N/A"
            gold_change = "N/A"
            if 'gold' in metals and 'current_price' in metals['gold']:
                gold_price = f"${metals['gold']['current_price']:.2f}"
                if 'change_percent' in metals['gold']:
                    change_pct = metals['gold']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    gold_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            # Silver
            silver_price = "N/A"
            silver_change = "N/A"
            if 'silver' in metals and 'current_price' in metals['silver']:
                silver_price = f"${metals['silver']['current_price']:.2f}"
                if 'change_percent' in metals['silver']:
                    change_pct = metals['silver']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    silver_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            return gold_price, gold_change, silver_price, silver_change
        
        @callback(
            [Output('dow-price', 'children'),
             Output('dow-change', 'children'),
             Output('vn-price', 'children'),
             Output('vn-change', 'children')],
            [Input('financial-data-store', 'data')]
        )
        def update_stock_indices(data):
            """Cập nhật chỉ số chứng khoán"""
            if not data or 'stock_indices' not in data:
                return "N/A", "N/A", "N/A", "N/A"
            
            indices = data['stock_indices']
            
            # Dow Jones
            dow_price = "N/A"
            dow_change = "N/A"
            if 'dow_jones' in indices and 'current_price' in indices['dow_jones']:
                dow_price = f"{indices['dow_jones']['current_price']:,.2f}"
                if 'change_percent' in indices['dow_jones']:
                    change_pct = indices['dow_jones']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    dow_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            # VN Index
            vn_price = "N/A"
            vn_change = "N/A"
            if 'vn_index' in indices and 'current_price' in indices['vn_index']:
                vn_price = f"{indices['vn_index']['current_price']:,.2f}"
                if 'change_percent' in indices['vn_index']:
                    change_pct = indices['vn_index']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    vn_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            return dow_price, dow_change, vn_price, vn_change
        
        @callback(
            [Output('bond-yield', 'children'),
             Output('bond-change', 'children')],
            [Input('financial-data-store', 'data')]
        )
        def update_bond_yields(data):
            """Cập nhật lợi suất trái phiếu"""
            if not data or 'bond_yields' not in data:
                return "N/A", "N/A"
            
            bonds = data['bond_yields']
            
            # US 10Y Bond
            bond_yield = "N/A"
            bond_change = "N/A"
            if 'us_10y_bond_yahoo' in bonds and 'current_price' in bonds['us_10y_bond_yahoo']:
                bond_yield = f"{bonds['us_10y_bond_yahoo']['current_price']:.2f}%"
                if 'change_percent' in bonds['us_10y_bond_yahoo']:
                    change_pct = bonds['us_10y_bond_yahoo']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    bond_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            return bond_yield, bond_change
        
        @callback(
            [Output('usdvnd-rate', 'children'),
             Output('usdvnd-change', 'children'),
             Output('eurusd-rate', 'children'),
             Output('eurusd-change', 'children')],
            [Input('financial-data-store', 'data')]
        )
        def update_fx_rates(data):
            """Cập nhật tỷ giá ngoại tệ"""
            if not data or 'fx' not in data:
                return "N/A", "N/A", "N/A", "N/A"
            
            fx = data['fx']
            
            # USD/VND
            usdvnd_rate = "N/A"
            usdvnd_change = "N/A"
            if 'usd_vnd' in fx and 'current_price' in fx['usd_vnd']:
                usdvnd_rate = f"{fx['usd_vnd']['current_price']:,.0f}"
                if 'change_percent' in fx['usd_vnd']:
                    change_pct = fx['usd_vnd']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    usdvnd_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            # EUR/USD
            eurusd_rate = "N/A"
            eurusd_change = "N/A"
            if 'eur_usd' in fx and 'current_price' in fx['eur_usd']:
                eurusd_rate = f"{fx['eur_usd']['current_price']:.4f}"
                if 'change_percent' in fx['eur_usd']:
                    change_pct = fx['eur_usd']['change_percent']
                    color = 'green' if change_pct >= 0 else 'red'
                    eurusd_change = html.Span(f"{change_pct:+.2f}%", style={'color': color})
            
            return usdvnd_rate, usdvnd_change, eurusd_rate, eurusd_change
        
        @callback(
            Output('price-chart', 'figure'),
            [Input('chart-selector', 'value'),
             Input('financial-data-store', 'data')]
        )
        def update_chart(selected_asset, data):
            """Cập nhật biểu đồ giá"""
            if not data:
                return go.Figure()
            
            try:
                # Lấy dữ liệu lịch sử cho asset được chọn
                symbol_map = {
                    'gold': config.SYMBOLS['gold'],
                    'silver': config.SYMBOLS['silver'],
                    'dow_jones': config.SYMBOLS['dow_jones'],
                    'vn_index': config.SYMBOLS['vn_index'],
                    'us_10y_bond': config.SYMBOLS['us_10y_bond'],
                    'usd_vnd': config.SYMBOLS['usd_vnd'],
                    'eur_usd': config.SYMBOLS['eur_usd']
                }
                
                symbol = symbol_map.get(selected_asset, config.SYMBOLS['gold'])
                hist_data = self.fetcher.fetch_yahoo_finance_data(symbol, period="1mo")
                
                if 'historical_data' in hist_data and hist_data['historical_data']:
                    df = pd.DataFrame(hist_data['historical_data'])
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['Close'],
                        mode='lines',
                        name=selected_asset.replace('_', ' ').title(),
                        line=dict(width=2)
                    ))
                    
                    fig.update_layout(
                        title=f"{selected_asset.replace('_', ' ').title()} Price Chart (1 Month)",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        height=400
                    )
                    
                    return fig
                else:
                    return go.Figure().add_annotation(
                        text="No historical data available",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, showarrow=False
                    )
                    
            except Exception as e:
                return go.Figure().add_annotation(
                    text=f"Error loading chart: {str(e)}",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
    
    def run(self, debug=True):
        """Chạy dashboard"""
        self.app.run_server(
            debug=debug,
            host=config.DASHBOARD_HOST,
            port=config.DASHBOARD_PORT
        )

# CSS styles
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

if __name__ == "__main__":
    dashboard = FinancialDashboard()
    print(f"Starting dashboard at http://{config.DASHBOARD_HOST}:{config.DASHBOARD_PORT}")
    dashboard.run(debug=True)