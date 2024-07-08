import os, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime,timedelta
from yahoo_fin import options
yf.pdr_override()


ff_data = pd.read_excel("C://Users/david/FF_daily.xlsx")
ff_data = ff_data.set_index("Date")
bab_data = pd.read_excel("C://Users/david/BaB_daily.xlsx")
df_bab = bab_data.set_index("Date")

date_dt = pd.to_datetime(df_bab.index, format='%m/%d/%Y')  # Convert string to datetime
df_bab.index = date_dt.strftime('%Y%m%d')
df_bab.index = df_bab.index.astype(int)

# Merge the two datasets again, correctly this time
df = ff_data.merge(df_bab, left_index=True, right_index=True, how='inner')

df_indices = (df + 1).cumprod(axis=0)*100

def compute_zscore(df, rol_window=250):
    rolling_mean = df.rolling(rol_window).mean()
    rolling_std = df.rolling(rol_window).std()
    return (df - rolling_mean) / rolling_std

# Compute ratios with respect to "Mkt-RF"
df_ratios = df_indices.div(df_indices["Mkt-RF"], axis=0)
df_ratios.drop(["Mkt-RF", "RF"], axis=1, inplace=True)  # Remove the "Mkt-RF" column to avoid dividing by itself

# Compute Z-scores for the ratios
ratios_zscores = compute_zscore(df_ratios)

# Plotting
fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(15, 15))

# List of column names for iteration
columns = ratios_zscores.columns

for ax, col in zip(axs.flat, columns):
    ax.plot(ratios_zscores.index, ratios_zscores[col], label=f'Z-score of {col}/Mkt-RF')
    ax.set_title(f'Z-score of {col}/Mkt-RF')
    ax.set_xlabel('Date')
    ax.set_ylabel('Z-score')
    ax.legend()
    ax.grid(True)

# Adjust layout
plt.tight_layout()
plt.show()

ratios_zscores.columns = ['Zscore_Size', 'Zscore_Value','Zscore_Quality','Zscore_MoM','Zscore_BaB']
ratios_zscores = ratios_zscores.dropna()
# Merge the two datasets again, correctly this time
df_signals = ratios_zscores.merge(df[['Mkt-RF','Size','Value','Quality','MoM','BaB']], left_index=True, right_index=True, how='inner')



# Initialize strategy variables
position = None  # None, 'Size', or 'Mkt-RF'
total_returns = [1.0]  # Initial returns, represented multiplicatively

# Lists to store trade logs
trades = []

# Simulate the trading strategy
for date, row in df_signals.iterrows():
    if position == 'Size':
        total_returns.append(total_returns[-1] * (1 + row['Size']))  # Accumulate returns from holding 'Size'
        if row['Zscore_Size'] >= 2:
            # Switch from Size to Mkt-RF
            trades.append((date, 'Switch from Size to Mkt-RF', row['Mkt-RF']))
            position = 'Mkt-RF'
    elif position == 'Mkt-RF':
        total_returns.append(total_returns[-1] * (1 + row['Mkt-RF']))  # Accumulate returns from holding 'Mkt-RF'
        # Example condition to switch back to Size, let's assume if Z-score Size goes below -2 again
        if row['Zscore_Size'] <= -2:
            trades.append((date, 'Switch from Mkt-RF to Size', row['Size']))
            position = 'Size'
    else:
        total_returns.append(total_returns[-1])  # No change in returns
        if row['Zscore_Size'] <= -2:
            # Buy Size
            position = 'Size'
            trades.append((date, 'Buy Size', row['Size']))

# Display trades
trade_log = pd.DataFrame(trades, columns=['Date', 'Action', 'Price at Action'])
print(trade_log)
print("Total returns from strategy: ", total_returns[-1])

total_returns = total_returns[1:]

# Plot the total returns
plt.figure(figsize=(10, 5))
plt.plot(df_signals.index, total_returns, label='Cumulative Returns')
plt.title('Strategy Cumulative Returns Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid(True)
plt.show()


def simulate_trading_strategy(df, factor_name, zscore_column):
    # Initialize strategy variables
    position = None  # None, 'Size', or 'Mkt-RF'
    total_returns = [1.0]  # Initial returns, represented multiplicatively
    trades = []  # To store trade logs

    # Simulate the trading strategy
    for date, row in df.iterrows():
        if position == factor_name:
            total_returns.append(
                total_returns[-1] * (1 + row[factor_name]))  # Accumulate returns from holding the factor
            if row[zscore_column] >= 2:
                # Switch from factor to Mkt-RF
                trades.append((date, f'Switch from {factor_name} to Mkt-RF', row['Mkt-RF']))
                position = 'Mkt-RF'
        elif position == 'Mkt-RF':
            total_returns.append(total_returns[-1] * (1 + row['Mkt-RF']))  # Accumulate returns from holding 'Mkt-RF'
            # Example condition to switch back to the factor
            if row[zscore_column] <= -2:
                trades.append((date, f'Switch from Mkt-RF to {factor_name}', row[factor_name]))
                position = factor_name
        else:
            total_returns.append(total_returns[-1])  # No change in returns
            if row[zscore_column] <= -2:
                # Buy the factor
                position = factor_name
                trades.append((date, f'Buy {factor_name}', row[factor_name]))

    # Display trades
    trade_log = pd.DataFrame(trades, columns=['Date', 'Action', 'Price at Action'])
    print(trade_log)
    print("Total returns from strategy: ", total_returns[-1])

    total_returns = total_returns[1:]  # Adjust the list to remove the initial 1.0

    # Plot the total returns
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, total_returns, label='Cumulative Returns')
    plt.title(f'Strategy Cumulative Returns Over Time for {factor_name}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.show()

    return trade_log, total_returns

# Example usage:
# df should be your full DataFrame with all necessary columns
# 'Size' is the example factor, and 'Zscore_Size' is its Z-score column
simulate_trading_strategy(df_signals, 'Size', 'Zscore_Size')

