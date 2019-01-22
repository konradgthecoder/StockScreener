"""
-------------------------------------------------------
[file name]
[program description]
-------------------------------------------------------
Author:  Konrad Gapinski
ID:     160713100
Email:   gapi3100@mylaurier.ca
__updated__ = "2019-01-21"
-------------------------------------------------------
"""
URL = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
TICKERS = ["ACB", "FB", "JE"]
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import csv 
import requests

def csvGetter():
    for ticker in TICKERS:
        urlParsed = URL + ticker 
        response = requests.get(urlParsed, allow_redirects=True)
        open("/future_value/{}_key_ratios.csv".format(ticker), 'wb').write(response.content)
        print(response)
        
def csvEditor():
    

style.use('ggplot')

start = dt.datetime(2009, 1, 1)
end = dt.datetime.now()
# 
df = web.DataReader('RNW.TO', 'yahoo', start, end)
# print(df.head)
# df.to_csv('tsla.csv')
# df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

# df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()
df_ohlc.reset_index(inplace=True) 

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

# print(df_ohlc.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g', colordown='r', alpha=0.75)
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
# plt.show()