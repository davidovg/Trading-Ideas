import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import momentum_utils as au
from quant_utils import *


df_equities = pd.DataFrame()
stocks = ['AAPL', 'AMZN', 'GOOG']

for stock in stocks:
    stock = yf.Ticker(stock)
    df_equity = stock.history(interval="1d", period="max")['Close']
    df_equity = pd.DataFrame(df_equity, index=df_equity.index)
    df_equities = pd.concat((df_equities, df_equity), axis=1)

df_equities.dropna(inplace=True)


mom_lag = 3  # business days before end of month

categories_lag_months = [9, 3]
smoothing_intervals = 2

# CAT MOMENTUM
def compute_mom(data, categories_lag_months):
    data_mom = None
    for mom_len in categories_lag_months:
        m = data.apply(au.get_momentum, axis=0, raw=True,


                   args=(mom_len * 22, smoothing_intervals)) * 12 / mom_len / len(categories_lag_months)
    data_mom = m if data_mom is None else data_mom + m
    data_mom = data_mom.dropna()
    return data_mom


data_mom = compute_mom(df_equities, categories_lag_months)


#RSI
symbol = yf.Ticker('^GDAXI')
df_dax = symbol.history(interval="1d",period="max")


# Filter the data by date
df_dax = df_dax[df_dax.index > "2017-01-01"]
df_dax = df_dax[df_dax.index < "2023-02-03"]

# Print the result
print(df_dax)
del df_dax["Dividends"]
del df_dax["Stock Splits"]

change = df_dax["Close"].diff()
change.dropna(inplace=True)


def rsi(df,n):
    change_up = df.copy()
    change_down = df.copy()
    change_up[change_up<0] = 0
    change_down[change_down>0] = 0
    change.equals(change_up+change_down)

    # Calculate the rolling average of average up and average down
    avg_up = change_up.rolling(n).mean()
    avg_down = change_down.rolling(n).mean().abs()
    #if avg_up == 0:
     #   return 0
    #elif avg_down == 0:
     #   return 100
    #else:
    return 100 * avg_up / (avg_up + avg_down)

# Take a look at the 20 oldest datapoints
rsix = rsi(change,14)



# Set the theme of our chart
plt.style.use('fivethirtyeight')

# Make our resulting figure much bigger
plt.rcParams['figure.figsize'] = (20, 20)

# Create two charts on the same figure.
ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

# First chart:
# Plot the closing price on the first chart
ax1.plot(df_dax['Close'], linewidth=2)
ax1.set_title('Close Price')

# Second chart
# Plot the RSI
ax2.set_title('Relative Strength Index')
ax2.plot(rsix, color='orange', linewidth=1)
# Add two horizontal lines, signalling the buy and sell ranges.
# Oversold
ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
# Overbought
ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

