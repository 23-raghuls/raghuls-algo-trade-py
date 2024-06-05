import yfinance as yf
import pandas as pd
import numpy as np

# Define the stock symbol
symbol = 'AAPL'

# Fetch the stock data
stock = yf.Ticker(symbol)

# Get the current stock price
current_price = stock.history(period='1d')['Close'][0]
print(f"Current Price: {current_price}")

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

# Find the call and put options with the smallest strike_diff
best_call = data[(data['type'] == 'call')].loc[data['strike_diff'].idxmin()]
best_put = data[(data['type'] == 'put')].loc[data['strike_diff'].idxmin()]

print("\nBest Call Option based on Strike Price:")
print(best_call)

print("\nBest Put Option based on Strike Price:")
print(best_put)

