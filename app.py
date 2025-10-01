"""
Flask Web Application for Stock Analysis
Production-ready version for Render deployment
"""

from flask import Flask, render_template, request, jsonify
from analyzer import StockAnalyzer
import traceback
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vivek-stock-analyzer-2025-default-key')

@app.route('/')
def index():
    """Render homepage"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze stock based on user input"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        period = data.get('period', '5y')
        
        if not symbol:
            return jsonify({'error': 'Please enter a stock symbol'}), 400
        
        # Add .NS for NSE if not specified
        if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
            symbol += '.NS'
        
        # Initialize analyzer
        analyzer = StockAnalyzer(symbol)
        
        # Get analysis
        scores, financial_data = analyzer.analyze_parameters()
        overall_score = analyzer.calculate_overall_score(scores)
        recommendation, reason = analyzer.get_recommendation(overall_score)
        company_info = analyzer.get_company_info()
        
        # Generate charts
        price_chart = analyzer.generate_price_chart(period)
        volume_chart = analyzer.generate_volume_chart(period)
        
        # Prepare parameter display names
        param_names = {
            'pe_ratio': 'P/E Ratio',
            'pb_ratio': 'P/B Ratio',
            'roe': 'Return on Equity (ROE)',
            'debt_to_equity': 'Debt to Equity',
            'current_ratio': 'Current Ratio',
            'profit_margin': 'Profit Margin',
            'dividend_yield': 'Dividend Yield',
            'revenue_growth': 'Revenue Growth',
            'eps': 'Earnings Per Share (EPS)',
            'beta': 'Beta (Volatility)'
        }
        
        # Format scores for display
        formatted_scores = {}
        for key, value in scores.items():
            formatted_scores[param_names.get(key, key)] = {
                'value': round(value['value'], 2),
                'score': value['score'],
                'weight': value['weight']
            }
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'company_info': company_info,
            'scores': formatted_scores,
            'overall_score': overall_score,
            'recommendation': recommendation,
            'reason': reason,
            'price_chart': price_chart,
            'volume_chart': volume_chart,
            'financial_data': financial_data
        })
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Error analyzing stock: {str(e)}. Please check the symbol and try again.'
        }), 500

@app.route('/results')
def results():
    """Render results page"""
    return render_template('results.html')

if __name__ == '__main__':
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
