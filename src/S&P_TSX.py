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
from copy import deepcopy
from builtins import input
from yahoo_fin import stock_info as si

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Morningstar export CSV key ratios URL                                                                                                                   #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
URL = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
URL_END = "&culture=en-CA&region=CAN&order=asc&r=581263"

style.use('ggplot')

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Function saves list of tickers to a file called sptsxtickers.pickle.                                                                                    #
#     returns:    tickers Saves tickers into sptsxtickers.pickle.                                                                                         #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def save_sp500_tickers():
    # Search through list of Wikipedia tickers
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    # Isolates HTML table on Wikipedia for tickers section
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.replace(".", "-").strip()
        print(ticker)
        
        tickers.append(ticker)
    # Dumps the tickers to our file
    with open("sptsxtickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
        
    print(tickers)
    
    return tickers



#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Function gets CSV key ratio data from Morningstar for all our TSX SP tickers.                                                                           #
#     returns:    Saves tickers into individual CSV files located in key_ratios package.                                                                  #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def get_data_from_morningstar(reload_sptsxtickers=False):
    if reload_sptsxtickers:
        tickers = save_sp500_tickers()
    else:
        with open("sptsxtickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    
    for ticker in tickers:
        ticker = ticker.replace('-', '.')
        print(ticker)
        if not os.path.exists('key_ratios/{}_key_ratios.csv'.format(ticker)):
            try:
                df = URL + ("{}".format(ticker)) + URL_END
                response = requests.get(df, allow_redirects=True)
                open("key_ratios/{}_key_ratios.csv".format(ticker), 'wb').write(response.content)
                time.sleep(2)
                
            except:
                df = URL + ("{}.TO".format(ticker)) + URL_END
                response = requests.get(df, allow_redirects=True)
                open("key_ratios/{}-TO_key_ratios.csv".format(ticker), 'wb').write(response.content)
                time.sleep(15)
                
        else:
            print("Already have {}".format(ticker))
            

def get_data_from_yahoo(reload_sptsxtickers=False):
        if reload_sptsxtickers:
            tickers = save_sp500_tickers()
        else:
            with open("sptsxtickers.pickle", "rb") as f:
                tickers = pickle.load(f)
        if not os.path.exists('stock_dfs'):
            os.makedirs('stock_dfs')
        
        start = dt.datetime(2009, 1, 1)
        end = dt.datetime.now()
        
        for ticker in tickers:
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                try:
                    df = web.DataReader(ticker, 'yahoo', start, end)
                    df.to_csv('stock_dfs/{}.csv'.format(ticker))
                except:
                    df = web.DataReader(ticker + '.TO', 'yahoo', start, end)
                    df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Function compiles data into two lists.                                                                                                                  #
#     returns:    BPS list                                                                                                                                #
#                 Dividend list                                                                                                                           #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def compile_data(ticker): 
    # Reading ticker key ratios csv, dropping all unnecessary data and isolating dividends and book values
    df = pd.read_csv('key_ratios/{}_key_ratios.csv'.format(ticker), skiprows=2, nrows=10)
    df.rename(columns={'Unnamed: 0': "{} Dates".format(ticker)}, inplace=True)
    for i in range(10):
        if (i!=9 and i!=6):
            df.drop([i], inplace=True)
    
    # Setting indices for easy data selection
    df = df.reset_index(drop=True)
    df.set_index('{} Dates'.format(ticker), inplace=True)
    dd = deepcopy(df)
    try:
        dd.drop('Book Value Per Share * CAD', inplace=True)
    except:
        dd.drop('Book Value Per Share * USD', inplace=True)
    
    try:
        df.drop('Dividends CAD', inplace=True)
    except:
        df.drop('Dividends USD', inplace=True)
    
    # Creating various lists for storing book value and dividend prices
    book_value_per_share = []
    BV_share = []
    # Final book value per share list
    BPS = []
    dividenda = []
    dividendb = []
    # Final dividend list
    dividend = []
    
    # Looping through columns in numpy array
    for col in df:
        book_value_per_share.append(df[col].values)
    # Looping through lists in list array
    for x in book_value_per_share:
        BV_share.append((x.tolist()))
    # Appending float data to list
    for x in BV_share:
        for y in x:
            if (str(y) != 'nan' and str(y) != 'NaN' and str(y) != 'nAn'):
                BPS.append(y)
    # Looping through columns in numpy array
    for col in dd:
        dividenda.append(dd[col].values)
    # Looping through lists in list array
    for x in dividenda:
        dividendb.append((x.tolist()))
    # Appending float data to list
    for x in dividendb:
        for y in x:
            
            dividend.append(y)
                
    return BPS, dividend
        
def compile_closing_prices():
    with open("sptsxtickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    main_df = pd.DataFrame()
    
    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csb'.format(ticker)) 
        df.set_index('Date', inplace=True)
        
        df.rename(columns = {'Adj Close':ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'] ,1, inplace=True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
            
        if count % 10 == 0:
            print(count)
        
        main_df.to_csv('sptsx_joined_closes.csv')
        
        
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Function calculates intrinsic value of specified ticker using Buffet's formula.                                                                         #
#     returns:    c - The intrinsic value of our chosen ticker.                                                                                           #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
def calculate_intrinsic_value_BPS(bps, dividend, years, federal_note):
    # Time period between old and new book values
    time_period_years = len(bps)
    time_period_years -= 2
    # Current book value per share
    TTM_BPS = bps[-1]
    TTM_BPS = float(TTM_BPS)
    k=1
    # Not interested in dying companies
    if TTM_BPS <= 0:
        return None
    while (TTM_BPS <= 0 or TTM_BPS == None):
        TTM_BPS = float(TTM_BPS)
        TTM_BPS = bps[-k]
        TTM_BPS = float(TTM_BPS)
        k += 1
        time_period_years -= 1
    # Current dividend payout ratio converted to 0.0 if not found
    TTM_dividend = dividend[-1]
    if (str(TTM_dividend) != 'nan'):
        TTM_dividend = TTM_dividend
        TTM_dividend = float(TTM_dividend)
    else:
        TTM_dividend = 0.0
    
    # Ignoring TTM BPS, only counting yearly BPS
    bps = bps[:-1]
    start_BPS = bps[0]
    i=1
    start_BPS = float(start_BPS)
    while start_BPS <= 0:
        start_BPS = float(start_BPS)
        start_BPS = bps[i]
        start_BPS = float(start_BPS)
        i+=1
        time_period_years -= 1
    
    if (len(bps) < 3 or time_period_years < 3):
        return None
    
    start_BPS = float(start_BPS)
    end_BPS = bps[-1]
    end_BPS = float(end_BPS)
    average_BPS_per_year = (((end_BPS/start_BPS)**(1/time_period_years))-1)*100
    
    print("Average BPS:    {}".format(average_BPS_per_year))
    print("TTM Dividend:   {}".format(TTM_dividend))

    # Calculate Intrinsic Value
    perc = (1+average_BPS_per_year/100)
    base = perc ** years
    parr = TTM_BPS * base
    r = federal_note / 100
    extra = (1 + r) ** years

    # Formula for Intrinsic Value
    c = TTM_dividend * (1-(1/extra))/r+parr/extra
 
    return c
    
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Function gets all intrinsic values on our ticker list.                                                                                                  #
#     returns:    Saves beautiful CSV of intrinsic values                                                                                                 #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#        
def get_intrinsic_value_list():
    # Opening our ticker list
    with open("sptsxtickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    main_df = pd.DataFrame()
        
    
    # Asking for federal interest rate and time period
    time_period = input("What is the time period you are looking to cover? \n(Note that the time period you choose must be consistent with the time period of the Federal Rate)")
    time_period = int(time_period)
    
    federal_rate = input("What is the {} year federal interest rate? \n(Enter as a regular percentage. Ex. 3% = 3)".format(time_period))
    federal_rate = float(federal_rate)
    
    # Looping through tickers, calling calculate_intrinsic_value_BPS() to get all ticker prices, saving them into a table
    not_found_count = 0
    not_found_tickers = []
    
    main_df = pd.DataFrame(columns=['Ticker', 'Intrinsic Value', 'Actual Value', 'Percent Undervalued', 'Percent Overvalued'])  
    main_df.set_index('Ticker')


    for ticker in tickers:
        
        ticker = ticker.replace('-', '.')
        print(ticker)
        # Call compile_data to get BPS and dividend data
        try:
            BPS, dividend = compile_data(ticker)
        except:
            print("CSV File Not Found!")
            not_found_count += 1
            not_found_tickers.append(ticker)
            print()
            continue
        # Call calculate_intrinsic_value_BPS for specified ticker
        c = calculate_intrinsic_value_BPS(BPS, dividend, time_period, federal_rate)
        print(c)
        
        # Ignore extremely small intrinsic values, don't care about these...
        if c!= None:
            c = float(c)
        if (c != None and c < 0.1):
            continue
        # Get recent stock price of ticker
        ticker = ticker.replace('.', '-')
        try:
            stock_price = si.get_live_price(ticker + ".TO")
        except:
            stock_price = si.get_live_price(ticker)
            
        if c!=None:
            undervalued_percentage = ((c - stock_price) / stock_price) * 100
            overvalued_percentage = ((stock_price - c) / c) * 100
            
        else:
            continue
             
        
#         main_df = main_df.join(df, how='outer', lsuffix='_left', rsuffix='_right')
        main_df = main_df.append({'Ticker' : ticker, 'Intrinsic Value' : c, 'Actual Value' : stock_price, 'Percent Undervalued' : undervalued_percentage, 'Percent Overvalued' : overvalued_percentage}, ignore_index=True)
        
        main_df = main_df.round(2)
        print(main_df)
        print()
    main_df.to_csv('intrinsic_value_list.csv', )
    print(main_df)
    print("{} tickers were missing CSV's.".format(not_found_count))
    print("List of tickers missing:\n", not_found_tickers)


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                         #
# Function neatly visualizes our data into a matplotlib pyplot.                                                                                           #
#     returns:    Shwos plot of stock                                                                                                                     #
#                                                                                                                                                         #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
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

# UNCOMMENT TO GET SPTSX TICKERS
# save_sp500_tickers()
# UNCOMMENT TO REFRESH STOCK DATA
get_data_from_morningstar()
# UNCOMMENT TO VISUALIZE DATA
# visualize_data()
get_intrinsic_value_list()

    