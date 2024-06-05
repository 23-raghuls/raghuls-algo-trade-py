import yfinance as yf
import pandas as pd
import numpy as np

# Define the stock symbol
symbol = 'MSFT'

# Fetch the stock data
stock = yf.Ticker(symbol)

# Get the current stock price
current_price = stock.history(period='1d')['Close'][0]
print(f"Current Price: {current_price}")

# Fetch historical data to calculate moving averages
hist_data = stock.history(period='1y')  # Fetch 1 year of data
hist_data['SMA50'] = hist_data['Close'].rolling(window=50).mean()
hist_data['SMA200'] = hist_data['Close'].rolling(window=200).mean()

# Determine if we should consider calls or puts based on moving averages
recent_data = hist_data.dropna().tail(1)  # Get the most recent data after dropping NaNs
if recent_data['SMA50'].values[0] > recent_data['SMA200'].values[0]:
    option_type = 'call'
    print("Heuristic Decision: Consider Call Options")
else:
    option_type = 'put'
    print("Heuristic Decision: Consider Put Options")

# Get the expiration dates for the options
expirations = stock.options

# Define a function to fetch options data and create features
def get_options_data(expiration_date):
    options_chain = stock.option_chain(expiration_date)
    calls = options_chain.calls
    puts = options_chain.puts
    calls['type'] = 'call'
    puts['type'] = 'put'
    return pd.concat([calls, puts])

# Fetch options data for multiple expiration dates to create a dataset
data = pd.DataFrame()
for expiration_date in expirations[:3]:  # Limiting to first 3 expiration dates for this example
    options_data = get_options_data(expiration_date)
    options_data['expirationDate'] = expiration_date
    data = pd.concat([data, options_data])

# Calculate the difference between the strike price and the current stock price
data['strike_diff'] = np.abs(data['strike'] - current_price)

# Find the best option of the decided type based on the smallest strike_diff
best_option = data[(data['type'] == option_type)].loc[data['strike_diff'].idxmin()]

print(f"\nBest {option_type.capitalize()} Option based on Strike Price:")
print(best_option)
