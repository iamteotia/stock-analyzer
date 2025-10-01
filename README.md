# Indian Stock Market Analyzer

🚀 **Live Stock Analysis Tool for NSE/BSE** - Quantitative analysis for long-term investment

## ✨ Features

- **10 Quantitative Parameters** scored 0-10 with weighted analysis
- **Real-time NSE/BSE data** via yfinance
- **Interactive price & volume charts** with moving averages
- **Multiple time periods** (1 month to 10 years)
- **Modern animated UI** with particle effects
- **Investment recommendations** based on comprehensive scoring

## 📊 Quantitative Parameters

1. **P/E Ratio** (Weight: 1.2) - Ideal: 15-25
2. **P/B Ratio** (Weight: 1.0) - Ideal: 1-3
3. **ROE** (Weight: 1.5) - Target: >15%
4. **Debt/Equity** (Weight: 1.3) - Ideal: <1.0
5. **Current Ratio** (Weight: 0.8) - Ideal: >1.5
6. **Profit Margin** (Weight: 1.2) - Target: >10%
7. **Dividend Yield** (Weight: 0.9) - Ideal: >2%
8. **Revenue Growth** (Weight: 1.1) - Target: >10%
9. **EPS** (Weight: 1.0) - Higher is better
10. **Beta** (Weight: 0.7) - Ideal: 0.8-1.2

### Scoring:
- **8-10**: 🟢 STRONG BUY
- **6.5-8**: 🟢 BUY
- **5-6.5**: 🟡 HOLD
- **3-5**: 🟠 WEAK
- **0-3**: 🔴 AVOID

---

## 🛠️ Technologies

- Flask + Python 3.11
- yfinance (Yahoo Finance API)
- pandas, numpy, matplotlib
- Gunicorn (Production server)
- Render (Free hosting)

---

## 📝 Author

**Created by Vivek Teotia**

## ⚖️ Disclaimer

Educational purposes only. Consult financial advisors before investing.

---

## 📄 License

MIT License
