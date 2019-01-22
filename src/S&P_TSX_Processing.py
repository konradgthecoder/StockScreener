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
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import numpy as np
import pandas as pd
import pickle 
from sklearn import svm, model_selection as cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

style.use('ggplot')

day_range = input("Day_range = ")

def process_data_for_labels(ticker, day_range):
    hm_days = day_range
    hm_days = int(hm_days)
    df = pd.read_csv('sptsx_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    
    for i in range(1, (hm_days+1)):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
        
    df.fillna(0, inplace=True) 
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.04
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0
    
def extract_featuresets(ticker, day_range): 
    tickers, df = process_data_for_labels(ticker, day_range)
    
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker, i)] for i in range(1, (int(day_range)+1))]))    
    
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))
    df.fillna(0, inplace=True)
    
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X, y, df

def do_ml(ticker):
    X, y, df = extract_featuresets(ticker, day_range)
    
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,
                                                                       y,
                                                                       test_size = 0.75)
    
#     clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
    
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy:', confidence)
    predictions = clf.predict(X_test)
    print('Predicted spread:', Counter(predictions))
    df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), parse_dates=True, index_col=0)
#     df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()  
    df_ohlc.reset_index(inplace=True) 
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g', colordown='r', alpha=0.75)
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    plt.show()
    
    return confidence 


do_ml('RNW')
    
    
    
    
    
    