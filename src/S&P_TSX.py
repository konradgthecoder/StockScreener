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
import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle 
import requests
import time 

URL = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
URL_END = "&culture=en-CA&region=CAN&order=asc&r=581263"

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.replace(".", "-").strip()
        print(ticker)
        
        tickers.append(ticker)
    
    with open("sptsxtickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
        
    print(tickers)
    
    return tickers

# save_sp500_tickers()

def get_data_from_morningstar(reload_sptsxtickers=False):
    if reload_sptsxtickers:
        tickers = save_sp500_tickers()
    else:
        with open("sptsxtickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('key_ratios/{}.csv'.format(ticker)):
            try:
                df = URL + ("{}".format(ticker)) + URL_END
                response = requests.get(df, allow_redirects=True)
                open("key_ratios/{}_key_ratios.csv".format(ticker), 'wb').write(response.content)
                time.sleep(30)
                
            except:
                df = URL + ("{}.TO".format(ticker)) + URL_END
                response = requests.get(df, allow_redirects=True)
                open("key_ratios/{}-TO_key_ratios.csv".format(ticker), 'wb').write(response.content)
                time.sleep(30)
                
        else:
            print("Already have {}".format(ticker))
            
# get_data_from_morningstar()

def compile_data():
    with open("sptsxtickers.pickle", "rb") as f:
        tickers = pickle.load(f)
        
    main_df = pd.DataFrame()
    
   
    df = pd.read_csv('key_ratios/AAV_key_ratios.csv', skiprows=2, nrows=10)
    df.rename(columns={'Unnamed: 0': "AAV Dates"}, inplace=True)
    for i in range(9):
        if i!=5 and i!=9:
            df.drop([i], inplace=True)
    df = df.reset_index(drop=True)
    df.set_index('AAV Dates', inplace=True)
    print(df)
    print()
    for column in df:
        print(df[column])
        print()
#         df.set_index('Date', inplace=True)
        
#         df.rename(columns = {'Adj Close': ticker}, inplace=True)
#         df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        
#         if main_df.empty:
#             main_df = df 
#         else:
#             main_df = main_df.join(df, how='outer')
#              
#         if count % 10 == 0:
#             print(count)
#          
#         print(main_df.head())
#         main_df.to_csv('sptsx_data.csv')
        
compile_data()

def visualize_data():
    df = pd.read_csv('sptsx_joined_closes.csv')
#     df['ACB'].plot()
#     plt.show()
    df_corr = df.corr()
    
    print(df_corr.head)
    
    data = df_corr.values 
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()


# visualize_data()

    