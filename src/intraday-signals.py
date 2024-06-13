import yfinance as yf
from datetime import datetime
import pandas as pd

def get_best_stocks():
    # Define the list of stocks you want to analyze
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']
    
    best_stocks = {}
    
    for stock in stocks:
        # Fetch historical data for the stock
        data = yf.download(stock, start=datetime.now().strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
        
        # Calculate SMA5 and SMA20
        data['SMA5'] = data['Close'].rolling(window=5).mean()
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        
        # Check for SMA crossover
        if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1] and data['SMA5'].iloc[-2] < data['SMA20'].iloc[-2]:
            entry_price = data['Close'].iloc[-1]
            target = entry_price * 1.02  # 2% target
            stop_loss = entry_price * 0.98  # 2% stop-loss
            
            best_stocks[stock] = {'entry_price': entry_price, 'target': target, 'stop_loss': stop_loss}
    
    return best_stocks

def main():
    # Get the best stocks for intraday
    best_stocks = get_best_stocks()
    
    if best_stocks:
        print("Best stocks for intraday trading:")
        for stock, details in best_stocks.items():
            print(f"Stock: {stock}, Entry Price: {details['entry_price']}, Target: {details['target']}, Stop-loss: {details['stop_loss']}")
    else:
        print("No stocks found for intraday trading.")

if __name__ == "__main__":
    # Execute the script at 9 AM
    current_time = datetime.now().time()
    if current_time.hour == 9 and current_time.minute == 0:
        main()
