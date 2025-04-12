# stocks.py

import requests

def get_finnhub_price(symbol, api_key):
    url = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and "c" in data and data["c"] != 0:
            return data["c"]
        else:
            print(f"No valid price data for {symbol}")
            return None
    except requests.RequestException as e:
        print(f"Request error for {symbol}: {e}")
        return None

def get_multiple_prices(symbols, api_key):
    result = {}
    for symbol in symbols:
        price = get_finnhub_price(symbol, api_key)
        if price is not None:
            result[symbol] = price
    return result

if __name__ == "__main__":
    API_KEY = "cvst7ohr01qhup0su340cvst7ohr01qhup0su34g"
    symbols = ["AAPL", "TSLA", "TD", "NVDA", "GOOGL", "AMZN"]
    prices = get_multiple_prices(symbols, API_KEY)
    print(prices)
