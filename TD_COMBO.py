import os, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pandas_datareader import data as pdr
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings('ignore')


def identify_price_flips(df):
    df['Price Flip'] = False
    df['Trend'] = None  # To record the trend at each price flip

    for i in range(4, len(df) - 1):
        # Identify uptrend flips
        if df['Close'].iloc[i] > df['Close'].iloc[i - 4] and df['Close'].iloc[i + 1] < df['Close'].iloc[i - 4]:
            df.at[df.index[i + 1], 'Price Flip'] = True
            df.at[df.index[i + 1], 'Trend'] = 'uptrend'

        # Identify downtrend flips
        elif df['Close'].iloc[i] < df['Close'].iloc[i - 4] and df['Close'].iloc[i + 1] > df['Close'].iloc[i - 4]:
            df.at[df.index[i + 1], 'Price Flip'] = True
            df.at[df.index[i + 1], 'Trend'] = 'downtrend'

    return df


def identify_setups_and_countdown(df):
    df['Buy Setup'] = 0
    df['Sell Setup'] = 0
    df['Perfected'] = None  # To track 'Perfected Buy' or 'Perfected Sell'
    df['Countdown'] = 0
    active_setup = None
    setup_count = 0
    countdown = 0

    for i in range(4, len(df)):
        if df['Price Flip'].iloc[i]:
            active_setup = None
            setup_count = 0
            countdown = 0

        if active_setup == 'Buy' and df['Close'].iloc[i] < df['Close'].iloc[i - 4]:
            setup_count += 1
        elif active_setup == 'Sell' and df['Close'].iloc[i] > df['Close'].iloc[i - 4]:
            setup_count += 1
        else:
            active_setup = None
            setup_count = 0

        if setup_count == 0:
            if df['Close'].iloc[i] < df['Close'].iloc[i - 4]:
                active_setup = 'Buy'
                setup_count = 1
            elif df['Close'].iloc[i] > df['Close'].iloc[i - 4]:
                active_setup = 'Sell'
                setup_count = 1

        if setup_count == 9:
            if active_setup == 'Buy':
                df.at[df.index[i], 'Buy Setup'] = 9
                if check_perfected_buy(df, i):
                    df.at[df.index[i], 'Perfected'] = 'Perfected Buy'
            elif active_setup == 'Sell':
                df.at[df.index[i], 'Sell Setup'] = 9
                if check_perfected_sell(df, i):
                    df.at[df.index[i], 'Perfected'] = 'Perfected Sell'

        if df['Perfected'].iloc[i] and countdown == 0:
            countdown = 1

        if countdown > 0:
            df.at[df.index[i], 'Countdown'] = countdown
            if (active_setup == 'Buy' and df['Close'].iloc[i] < df['Low'].iloc[i - 2]) or \
                    (active_setup == 'Sell' and df['Close'].iloc[i] > df['High'].iloc[i - 2]):
                countdown += 1
            if countdown > 13:
                countdown = 0

    return df

def identify_setups_and_countdown(df):
    df['Buy Setup'] = 0
    df['Sell Setup'] = 0
    df['Perfected'] = None  # To track 'Perfected Buy' or 'Perfected Sell'
    df['Countdown'] = 0

    active_setup = None
    setup_count = 0
    countdown = 0

    for i in range(4, len(df)):
        if df['Price Flip'].iloc[i]:
            # Reset everything on a price flip
            active_setup = None
            setup_count = 0
            countdown = 0

        # Only continue if there is an active setup
        if active_setup:
            if active_setup == 'Buy' and df['Close'].iloc[i] < df['Close'].iloc[i - 4]:
                setup_count += 1
            elif active_setup == 'Sell' and df['Close'].iloc[i] > df['Close'].iloc[i - 4]:
                setup_count += 1
            else:
                # If the setup does not continue, reset the count
                setup_count = 0
                active_setup = None

        # Start a new setup if there isn't one active
        if setup_count == 0:
            if df['Close'].iloc[i] < df['Close'].iloc[i - 4]:
                active_setup = 'Buy'
                setup_count = 1
            elif df['Close'].iloc[i] > df['Close'].iloc[i - 4]:
                active_setup = 'Sell'
                setup_count = 1

        # When a setup reaches 9, check for perfection
        if setup_count == 9:
            df.at[df.index[i], f'{active_setup} Setup'] = 9
            if active_setup == 'Buy' and check_perfected_buy(df, i):
                df.at[df.index[i], 'Perfected'] = 'Perfected Buy'
            elif active_setup == 'Sell' and check_perfected_sell(df, i):
                df.at[df.index[i], 'Perfected'] = 'Perfected Sell'
            # Reset setup count after a full sequence
            setup_count = 0

        # Start or continue countdown after a perfected setup
        if df['Perfected'].iloc[i] and countdown == 0:
            countdown = 1  # Start countdown after perfection

        # Execute countdown logic
        if countdown > 0:
            df.at[df.index[i], 'Countdown'] = countdown
            if active_setup == 'Buy' and df['Close'].iloc[i] < df['Low'].iloc[i - 2]:
                countdown += 1
            elif active_setup == 'Sell' and df['Close'].iloc[i] > df['High'].iloc[i - 2]:
                countdown += 1

            # Reset countdown after 13 counts
            if countdown > 13:
                countdown = 0

    return df


def check_perfected_buy(df, index):
    day_9_high = df['High'].iloc[index]
    day_6_high = df['High'].iloc[index - 3]
    day_7_high = df['High'].iloc[index - 2]
    return day_6_high > day_9_high and day_7_high > day_9_high


def check_perfected_sell(df, index):
    day_9_low = df['Low'].iloc[index]
    day_6_low = df['Low'].iloc[index - 3]
    day_7_low = df['Low'].iloc[index - 2]
    return day_6_low < day_9_low and day_7_low < day_9_low


def backtest_strategy(df):
    df['Position Type'] = None
    df['Position'] = 0
    df['Portfolio Value'] = 0.0
    df['Daily Return'] = df['Close'].pct_change()  # Compute daily returns

    for i in range(1, len(df)):
        # Check for buy signals based on trends
        if df['Perfected'].iloc[i] == 'Perfected Buy':
            df.at[df.index[i], 'Position Type'] = 'buy'
            df.at[df.index[i], 'Position'] = 1
            print(f"Buying at {df.index[i]}, price: {df['Close'].iloc[i]}")

        # Check for sell signals based on trends
        elif df['Perfected'].iloc[i] == 'Perfected Sell':
            df.at[df.index[i], 'Position Type'] = 'sell'
            df.at[df.index[i], 'Position'] = -1
            print(f"Selling at {df.index[i]}, price: {df['Close'].iloc[i]}")

        # Calculate returns for positions
        if df['Position'].iloc[i] != 0:
            if df['Position'].iloc[i - 1] == 1:
                df.at[df.index[i], 'Portfolio Value'] = df['Daily Return'].iloc[i]
            elif df['Position'].iloc[i - 1] == -1:
                df.at[df.index[i], 'Portfolio Value'] = -df['Daily Return'].iloc[i]

        # Handle closing positions based on price flips and trend
        if df['Price Flip'].iloc[i]:
            df.at[df.index[i], 'Position Type'] = None
            df.at[df.index[i], 'Position'] = 0
            print(f"Closing position at {df.index[i]}, price: {df['Close'].iloc[i]}")

    # Calculate cumulative returns from strategy
    df['Cumulative Return'] = (1 + df['Portfolio Value']).cumprod() - 1
    df['Cumulative Return'].fillna(0, inplace=True)  # Replace NaN with 0 for non-trading days

    return df





data_sp = pd.read_excel('C:\BoyanLAB\Quant Research\Elvis_Projekt/S&Pdata_OHCL.xlsx')
data_sp = data_sp.set_index("Date")

data_sp = pd.read_excel('C:\BoyanLAB\Quant Research\Elvis_Projekt/S&Pdata_OHCL_daily_1999.xlsx')
data_sp = data_sp.set_index("Date")

df = identify_price_flips(data_sp)
df = identify_setups_and_countdown(df)
df_back = backtest_strategy(df)

# Visualization
plt.figure(figsize=(14, 7))
plt.plot(df_back.index, df_back['Close'], label='Close Price', color='lightgray')
plt.plot(df_back.index, df_back['Cumulative Return'], label='Portfolio Value', color='blue')
buy_signals = df_back[df_back['Position Type'] == 'buy']
sell_signals = df_back[df_back['Position Type'] == 'sell']
plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', alpha=1)
plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', alpha=1)
plt.title('Backtest Performance and Close Price')
plt.xlabel('Date')
plt.ylabel('Price/Portfolio Value')
plt.legend()
plt.grid(True)
plt.show(block = True)