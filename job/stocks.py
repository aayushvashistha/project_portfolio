# stocks.py

import pandas as pd
import datetime as dt
import time
import yfinance as yf

def main():
    stocks = ["TSLA", "TD", "AMZN", "AMC", "GOOG", "INFY"]  # Add/Remove stocks as required
    # cryptocurrencies = ['BTC-CAD', 'ETH-CAD']

    count = 0
    data = pd.DataFrame()

    while True:  # Adjust the number of iterations as needed
        count += 1
        print(f"\n\nScript is executing {count} time")

        for ticker in stocks:
            data[ticker] = yf.download(ticker, period="1d", interval="1m")[['Adj Close']]

        # print("\n", data[stocks].iloc[-1])
        # countdown(5)  # Adjust the countdown time as needed
        result_dict = {ticker: data[ticker].iloc[-1] for ticker in stocks}
        return result_dict  # Return the data from the main function

# def countdown(t):
#     while t:
#         mins, secs = divmod(t, 60)
#         timer = '{:02d}'.format(secs)
#         print(f"Refreshing in {timer} seconds", end="\r")
#         time.sleep(1)
#         t -= 1

if __name__ == "__main__":
    result = main()
    print(result)  # Print the result for verification
