import yfinance as yf
import pandas as pd
import numpy as np

# Define a list of stocks to consider
stock_list = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'PYPL', 'INTC']

# Heuristic: Use historical volatility and volume to find best stocks for intraday trading
def get_intraday_trade_signals(ticker, period='1mo', interval='1d'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    
    # Ensure there is enough data to compute rolling statistics
    if hist.shape[0] < 5:
        return None
    
    # Calculate historical volatility
    hist['Returns'] = hist['Close'].pct_change()
    hist['Volatility'] = hist['Returns'].rolling(window=5).std()
    
    # Calculate average volume
    hist['Average Volume'] = hist['Volume'].rolling(window=5).mean()
    
    # Drop NaN values
    hist = hist.dropna()
    
    # Check if we have enough rows after dropping NaN values
    if hist.empty:
        return None
    
    # Simplified heuristic: High volatility and high volume
    avg_volatility = hist['Volatility'].mean()
    avg_volume = hist['Average Volume'].mean()
    
    # Define buy, sell, and stop-loss based on some simplified rules
    current_price = hist['Close'].iloc[-1]
    buy_price = current_price * 0.995  # 0.5% below the current price
    sell_price = current_price * 1.02  # 2% above the current price
    stop_loss = current_price * 0.98   # 2% below the current price
    
    return {
        'Ticker': ticker,
        'Average Volatility': avg_volatility,
        'Average Volume': avg_volume,
        'Buy Price': buy_price,
        'Sell Price': sell_price,
        'Stop Loss': stop_loss
    }

# Collect data for all stocks
stock_data = [get_intraday_trade_signals(ticker) for ticker in stock_list]

# Filter out None values
stock_data = [data for data in stock_data if data is not None]

# Convert to DataFrame for easy manipulation
df = pd.DataFrame(stock_data)

# Ensure we have data before proceeding
if not df.empty:
    # Sort by average volatility and volume (descending)
    df = df.sort_values(by=['Average Volatility', 'Average Volume'], ascending=False)
    
    # Select top 2 stocks
    top_stocks = df.head(2)
    
    # Display the results
    print(top_stocks)
else:
    print("Not enough data to determine the top stocks for intraday trading.")
