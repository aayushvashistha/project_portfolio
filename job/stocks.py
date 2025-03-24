import yfinance as yf

stocks = ["AAPL", "GOOG"]  # Test multiple tickers
data = {}

for ticker in stocks:
    try:
        print(f"Downloading data for {ticker}...")
        stock_data = yf.download(ticker, period="1d", interval="1m")
        
        # Check if data is returned
        if stock_data.empty:
            print(f"No data returned for {ticker}")
        else:
            data[ticker] = stock_data['Adj Close']
        
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")

# Print out the results
print("Data retrieved: ", data)