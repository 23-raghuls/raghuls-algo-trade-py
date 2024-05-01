import requests
import sys

def get_stock_data(api_key, symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    # API_key - 2000 Free Reads/day
    api_key = "IMP4V0N54KCVCU3Y"
    symbol = sys.argv[1]
    stock_data = get_stock_data(api_key, symbol)
    
    if "Global Quote" in stock_data:
        global_quote = stock_data["Global Quote"]
        print("Stock Symbol:", global_quote["01. symbol"])
        print("Open Price:", global_quote["02. open"])
        print("High Price:", global_quote["03. high"])
        print("Low Price:", global_quote["04. low"])
        print("Current Price:", global_quote["05. price"])
        print("Volume:", global_quote["06. volume"])
        print("Latest Trading Day:", global_quote["07. latest trading day"])
        print("Previous Close:", global_quote["08. previous close"])
        print("Change:", global_quote["09. change"])
        print("Change Percent:", global_quote["10. change percent"])

if __name__ == "__main__":
    main()

