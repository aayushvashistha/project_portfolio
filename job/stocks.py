# stocks.py

import pandas as pd
import yfinance as yf

def main():
    stocks = ["AAPL"] #, "AAPL", "GOOG", "TD", "AMZN", "NVDA"]  # Add/Remove stocks as required
    data = pd.DataFrame()

    for ticker in stocks:
        data[ticker] = yf.download(ticker, period="1d", interval="1m")[['Close']]

    result_dict = {ticker: data[ticker].iloc[-1] for ticker in stocks}
    return result_dict  # Return the data from the main function

if __name__ == "__main__":
    result = main()
    print(result)