# stocks.py

import pandas as pd
import yfinance as yf

def main():
    stocks = ["TSLA", "AAPL", "GOOG", "TD", "AMZN", "INFY"]  # Add/Remove stocks as required
    data = pd.DataFrame()

    for ticker in stocks:
        data[ticker] = yf.download(ticker, period="1d", interval="1m")[['Adj Close']]

    result_dict = {ticker: data[ticker].iloc[-1] for ticker in stocks}
    return result_dict  # Return the data from the main function

if __name__ == "__main__":
    result = main()
    print(result)
