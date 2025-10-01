"""
Stock Analyzer Module
Performs quantitative analysis on Indian stocks from NSE/BSE
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64
import time
import requests

class StockAnalyzer:
    """
    Comprehensive stock analyzer based on quantitative parameters
    for long-term investment in Indian markets
    """
    
    def __init__(self, symbol):
        """
        Initialize with stock symbol (e.g., 'RELIANCE.NS' for NSE or 'RELIANCE.BO' for BSE)
        """
        self.symbol = symbol
        
        # Create session with headers to avoid rate limiting
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        time.sleep(1.5)  # Rate limiting delay
        
        try:
            self.stock = yf.Ticker(symbol, session=session)
            time.sleep(1)
            self.info = self.stock.info
        except Exception as e:
            print(f"Error initializing: {e}")
            self.stock = yf.Ticker(symbol)
            self.info = {}
        
    def get_financial_data(self):
        """Fetch key financial data with error handling"""
        try:
            # Fallback values if data is missing
            safe_get = lambda key, default=0: self.info.get(key, default) if self.info.get(key) not in [None, 'None', ''] else default
            
            return {
                'pe_ratio': safe_get('trailingPE', 0),
                'forward_pe': safe_get('forwardPE', 0),
                'pb_ratio': safe_get('priceToBook', 0),
                'roe': safe_get('returnOnEquity', 0),
                'roa': safe_get('returnOnAssets', 0),
                'debt_to_equity': safe_get('debtToEquity', 0),
                'current_ratio': safe_get('currentRatio', 0),
                'profit_margin': safe_get('profitMargins', 0),
                'operating_margin': safe_get('operatingMargins', 0),
                'eps': safe_get('trailingEps', 0),
                'dividend_yield': (safe_get('dividendYield', 0) * 100) if safe_get('dividendYield', 0) else 0,
                'peg_ratio': safe_get('pegRatio', 0),
                'revenue_growth': safe_get('revenueGrowth', 0),
                'earnings_growth': safe_get('earningsGrowth', 0),
                'market_cap': safe_get('marketCap', 0),
                'beta': safe_get('beta', 1),
            }
        except Exception as e:
            print(f"Error fetching financial data: {e}")
            return {key: 0 for key in ['pe_ratio', 'pb_ratio', 'roe', 'debt_to_equity', 
                                        'current_ratio', 'profit_margin', 'dividend_yield', 
                                        'revenue_growth', 'eps', 'beta']}
    
    def calculate_score(self, value, thresholds, reverse=False):
        """Calculate score (0-10) based on value and thresholds"""
        if value is None or value == 0:
            return 5  # Default middle score instead of 0
        
        try:
            value = float(value)
        except:
            return 5
        
        if reverse:
            if value >= thresholds[4]: return 0
            elif value >= thresholds[3]: return 2
            elif value >= thresholds[2]: return 4
            elif value >= thresholds[1]: return 7
            else: return 10
        else:
            if value <= thresholds[0]: return 0
            elif value <= thresholds[1]: return 2
            elif value <= thresholds[2]: return 4
            elif value <= thresholds[3]: return 7
            else: return 10
    
    def analyze_parameters(self):
        """Analyze all parameters and assign scores (0-10)"""
        data = self.get_financial_data()
        scores = {}
        
        # 1. P/E Ratio
        pe = data.get('pe_ratio', 0)
        scores['pe_ratio'] = {
            'value': pe,
            'score': self.calculate_score(pe, [0, 15, 25, 35, 50], reverse=True),
            'weight': 1.2
        }
        
        # 2. P/B Ratio
        pb = data.get('pb_ratio', 0)
        scores['pb_ratio'] = {
            'value': pb,
            'score': self.calculate_score(pb, [0, 1, 3, 5, 10], reverse=True),
            'weight': 1.0
        }
        
        # 3. ROE
        roe = data.get('roe', 0) * 100 if data.get('roe') else 0
        scores['roe'] = {
            'value': roe,
            'score': self.calculate_score(roe, [0, 10, 15, 20, 25]),
            'weight': 1.5
        }
        
        # 4. Debt to Equity
        de = data.get('debt_to_equity', 0) / 100 if data.get('debt_to_equity') else 0
        scores['debt_to_equity'] = {
            'value': de,
            'score': self.calculate_score(de, [0, 0.5, 1.0, 2.0, 3.0], reverse=True),
            'weight': 1.3
        }
        
        # 5. Current Ratio
        cr = data.get('current_ratio', 0)
        scores['current_ratio'] = {
            'value': cr,
            'score': self.calculate_score(cr, [0, 1.0, 1.5, 2.0, 2.5]),
            'weight': 0.8
        }
        
        # 6. Profit Margin
        pm = data.get('profit_margin', 0) * 100 if data.get('profit_margin') else 0
        scores['profit_margin'] = {
            'value': pm,
            'score': self.calculate_score(pm, [0, 5, 10, 15, 20]),
            'weight': 1.2
        }
        
        # 7. Dividend Yield
        dy = data.get('dividend_yield', 0)
        scores['dividend_yield'] = {
            'value': dy,
            'score': self.calculate_score(dy, [0, 1, 2, 3, 4]),
            'weight': 0.9
        }
        
        # 8. Revenue Growth
        rg = data.get('revenue_growth', 0) * 100 if data.get('revenue_growth') else 0
        scores['revenue_growth'] = {
            'value': rg,
            'score': self.calculate_score(rg, [-10, 5, 10, 15, 20]),
            'weight': 1.1
        }
        
        # 9. EPS
        eps = data.get('eps', 0)
        scores['eps'] = {
            'value': eps,
            'score': self.calculate_score(eps, [0, 5, 10, 20, 30]),
            'weight': 1.0
        }
        
        # 10. Beta
        beta = data.get('beta', 1)
        beta_score = 10 if 0.8 <= beta <= 1.2 else (7 if 0.5 <= beta <= 1.5 else 5)
        scores['beta'] = {
            'value': beta,
            'score': beta_score,
            'weight': 0.7
        }
        
        return scores, data
    
    def calculate_overall_score(self, scores):
        """Calculate weighted overall score"""
        total_weighted_score = 0
        total_weight = 0
        
        for param, details in scores.items():
            total_weighted_score += details['score'] * details['weight']
            total_weight += details['weight']
        
        overall_score = total_weighted_score / total_weight if total_weight > 0 else 5
        return round(overall_score, 2)
    
    def get_historical_data(self, period='5y'):
        """Fetch historical stock data with retry"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                time.sleep(1.5)
                hist = self.stock.history(period=period)
                if not hist.empty:
                    return hist
                time.sleep(2)
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(3 * (attempt + 1))
                    continue
        return pd.DataFrame()
    
    def generate_price_chart(self, period='5y'):
        """Generate price chart for given period"""
        hist = self.get_historical_data(period)
        
        if hist.empty:
            return None
        
        plt.figure(figsize=(12, 6))
        plt.style.use('dark_background')
        
        plt.plot(hist.index, hist['Close'], color='#00ff88', linewidth=2, label='Close Price')
        plt.fill_between(hist.index, hist['Close'], alpha=0.3, color='#00ff88')
        
        if len(hist) > 50:
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            plt.plot(hist.index, hist['MA50'], color='#ffaa00', linewidth=1.5, label='50-Day MA', alpha=0.7)
        
        if len(hist) > 200:
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
            plt.plot(hist.index, hist['MA200'], color='#ff0088', linewidth=1.5, label='200-Day MA', alpha=0.7)
        
        plt.title(f'{self.symbol} - Price History ({period})', fontsize=16, color='white', pad=20)
        plt.xlabel('Date', fontsize=12, color='white')
        plt.ylabel('Price (₹)', fontsize=12, color='white')
        plt.legend(loc='best', framealpha=0.9)
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, facecolor='#000000', edgecolor='none')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()
    
    def generate_volume_chart(self, period='5y'):
        """Generate volume chart"""
        hist = self.get_historical_data(period)
        
        if hist.empty:
            return None
        
        plt.figure(figsize=(12, 4))
        plt.style.use('dark_background')
        plt.bar(hist.index, hist['Volume'], color='#00aaff', alpha=0.6, width=5)
        plt.title(f'{self.symbol} - Volume History ({period})', fontsize=16, color='white', pad=20)
        plt.xlabel('Date', fontsize=12, color='white')
        plt.ylabel('Volume', fontsize=12, color='white')
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, facecolor='#000000', edgecolor='none')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()
    
    def get_recommendation(self, overall_score):
        """Get investment recommendation based on overall score"""
        if overall_score >= 8:
            return "STRONG BUY", "Excellent fundamentals for long-term investment"
        elif overall_score >= 6.5:
            return "BUY", "Good fundamentals, suitable for long-term"
        elif overall_score >= 5:
            return "HOLD", "Average fundamentals, monitor closely"
        elif overall_score >= 3:
            return "WEAK", "Below average fundamentals, risky for long-term"
        else:
            return "AVOID", "Poor fundamentals, not recommended"
    
    def get_company_info(self):
        """Get basic company information"""
        return {
            'name': self.info.get('longName', 'N/A'),
            'sector': self.info.get('sector', 'N/A'),
            'industry': self.info.get('industry', 'N/A'),
            'website': self.info.get('website', 'N/A'),
            'summary': self.info.get('longBusinessSummary', 'N/A')[:500] if self.info.get('longBusinessSummary') else 'N/A',
            'employees': self.info.get('fullTimeEmployees', 'N/A'),
            'city': self.info.get('city', 'N/A'),
            'country': self.info.get('country', 'N/A'),
        }