from flask import Flask, render_template, request
import yfinance as yf
import json

app = Flask(__name__)

# List of common Indian stock ticker symbols
indian_stocks = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "SBIN": "SBIN.NS",
    "AXISBANK": "AXISBANK.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
    "ITC": "ITC.NS",
}

@app.route('/')
def home():
    return render_template("index.html", stocks=indian_stocks.keys())

@app.route('/stock', methods=['POST'])
def stock():
    stock_name = request.form.get("stock_name").upper()
    ticker_symbol = indian_stocks.get(stock_name)

    if ticker_symbol:
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            todays_data = stock.history(period="1d")
            current_price = todays_data["Close"].iloc[-1]
            todays_high = todays_data["High"].iloc[-1]
            todays_low = todays_data["Low"].iloc[-1]

            # Dummy shareholding pattern (use an actual API if needed)
            shareholding_pattern = {
                "Promoters": 50.1,
                "FIIs": 20.2,
                "DIIs": 15.3,
                "Public": 14.4,
            }

            # Preparing data for the template
            stock_data = {
                "name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "enterprise_value": info.get("enterpriseValue", "N/A"),
                "high_52": info.get("fiftyTwoWeekHigh", "N/A"),
                "low_52": info.get("fiftyTwoWeekLow", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "pb_ratio": info.get("priceToBook", "N/A"),
                "todays_high": todays_high,
                "todays_low": todays_low,
                "current_price": current_price,
                "shareholding": json.dumps(shareholding_pattern),
            }
            return render_template("stock.html", stock_data=stock_data)
        except Exception as e:
            return f"Error fetching data: {e}", 500
    else:
        return "Stock not found. Please go back and try again.", 404

if __name__ == '__main__':
    app.run(debug=True)
