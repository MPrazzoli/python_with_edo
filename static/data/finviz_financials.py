import os
import time
import numpy as np
import pandas as pd
from finvizfinance.quote import finvizfinance
from pickle_obj.read_pickle_df import read_available_ticker_from_pickle

'''
This script to fetch periodically finviz data of our stocks which are in the ticker_isin_file.xlsx

Info fetched:
'Sector': 'Industrials',
'Industry': 'Trucking',
'Country': 'China',
'P/E': '-', 42.57
'EPS (ttm)': '-0.86',
'Insider Own': '20.61%',
'Shs Outstand': '246.62M',
'Shs Float': '51.47M',
'Market Cap': '936.51M',
'Income': '-208.10M',
'Sales': '5.16B',
'Book/sh': '1.48',
'P/B': '1.53',
'ROA': '-6.90%',
'Target Price': '-',
'ROE': '-43.00%',
'ROI': '-4.40%',
'Employees': '8423',
'Debt/Eq': '2.44',
'''

# Set of the project path to find also data path where the tickers list is stored in your computer
project_root = os.path.dirname(os.path.dirname(__file__))
data_path = project_root + '/data'

# Getting the list of all tickers we are interested in from the ticker_isin_file.xlsx excel file,
# then a StockListClass instance is initialize to store the list of tickers and the list
# of isin which we insert in our excel file
ticker_python = pd.read_excel(data_path + '/ticker_isin_file.xlsx', sheet_name='American')
ticker_python.set_index('ticker', inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns

ticker_python['Sector'] = ''
ticker_python['Industry'] = ''
ticker_python['Country'] = ''
ticker_python['P/E'] = ''
ticker_python['EPS (ttm)'] = ''
ticker_python['Insider Own'] = ''
ticker_python['Shs Outstand'] = ''
ticker_python['Shs Float'] = ''
ticker_python['Market Cap'] = ''
ticker_python['Income'] = ''
ticker_python['Sales'] = ''
ticker_python['Book/sh'] = ''
ticker_python['P/B'] = ''
ticker_python['ROA'] = ''
ticker_python['Target Price'] = ''
ticker_python['ROE'] = ''
ticker_python['ROI'] = ''
ticker_python['Employees'] = ''
ticker_python['Debt/Eq'] = ''

start_time = time.time()

# To keep tracking the api process
j = 0

for i, ticker in enumerate(ticker_python.index):

    try:
        stock = finvizfinance(ticker)
    except:continue

    try:
        ticker_python.at[ticker_python.index[i], 'Sector'] = stock.TickerFundament()['Sector']
    except:
        ticker_python.at[ticker_python.index[i], 'Sector'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'Industry'] = stock.TickerFundament()['Industry']
    except:
        ticker_python.at[ticker_python.index[i], 'Industry'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'Country'] = stock.TickerFundament()['Country']
    except:
        ticker_python.at[ticker_python.index[i], 'Country'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'P/E'] = float(stock.TickerFundament()['P/E'])
    except:
        ticker_python.at[ticker_python.index[i], 'P/E'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'EPS (ttm)'] = float(stock.TickerFundament()['EPS (ttm)'])
    except:
        ticker_python.at[ticker_python.index[i], 'EPS (ttm)'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'Insider Own'] = float(
            stock.TickerFundament()['Insider Own'][:-1]) / 100
    except:
        ticker_python.at[ticker_python.index[i], 'Insider Own'] = ''

    ticker_python.at[ticker_python.index[i], 'Shs Outstand'] = stock.TickerFundament()['Shs Outstand']
    if ticker_python.at[ticker_python.index[i], 'Shs Outstand'][-1] == 'M':
        ticker_python.at[ticker_python.index[i], 'Shs Outstand'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Outstand'][:-1]) * 1000000
    elif ticker_python.at[ticker_python.index[i], 'Shs Outstand'][-1] == 'B':
        ticker_python.at[ticker_python.index[i], 'Shs Outstand'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Outstand'][:-1]) * 1000000000
    elif ticker_python.at[ticker_python.index[i], 'Shs Outstand'][-1] == 'T':
        ticker_python.at[ticker_python.index[i], 'Shs Outstand'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Outstand'][:-1]) * 1000000000000
    elif ticker_python.at[ticker_python.index[i], 'Shs Outstand'][-1] == 'K':
        ticker_python.at[ticker_python.index[i], 'Shs Outstand'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Outstand'][:-1]) * 1000

    ticker_python.at[ticker_python.index[i], 'Shs Float'] = stock.TickerFundament()['Shs Float']
    if ticker_python.at[ticker_python.index[i], 'Shs Float'][-1] == 'M':
        ticker_python.at[ticker_python.index[i], 'Shs Float'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Float'][:-1]) * 1000000
    elif ticker_python.at[ticker_python.index[i], 'Shs Float'][-1] == 'B':
        ticker_python.at[ticker_python.index[i], 'Shs Float'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Float'][:-1]) * 1000000000
    elif ticker_python.at[ticker_python.index[i], 'Shs Float'][-1] == 'T':
        ticker_python.at[ticker_python.index[i], 'Shs Float'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Float'][:-1]) * 1000000000000
    elif ticker_python.at[ticker_python.index[i], 'Shs Float'][-1] == 'K':
        ticker_python.at[ticker_python.index[i], 'Shs Float'] = float(
            ticker_python.at[ticker_python.index[i], 'Shs Float'][:-1]) * 1000

    ticker_python.at[ticker_python.index[i], 'Market Cap'] = stock.TickerFundament()['Market Cap']
    if ticker_python.at[ticker_python.index[i], 'Market Cap'][-1] == 'M':
        ticker_python.at[ticker_python.index[i], 'Market Cap'] = float(
            ticker_python.at[ticker_python.index[i], 'Market Cap'][:-1]) * 1000000
    elif ticker_python.at[ticker_python.index[i], 'Market Cap'][-1] == 'B':
        ticker_python.at[ticker_python.index[i], 'Market Cap'] = float(
            ticker_python.at[ticker_python.index[i], 'Market Cap'][:-1]) * 1000000000
    elif ticker_python.at[ticker_python.index[i], 'Market Cap'][-1] == 'T':
        ticker_python.at[ticker_python.index[i], 'Market Cap'] = float(
            ticker_python.at[ticker_python.index[i], 'Market Cap'][:-1]) * 1000000000000
    elif ticker_python.at[ticker_python.index[i], 'Market Cap'][-1] == 'K':
        ticker_python.at[ticker_python.index[i], 'Market Cap'] = float(
            ticker_python.at[ticker_python.index[i], 'Market Cap'][:-1]) * 1000

    ticker_python.at[ticker_python.index[i], 'Income'] = stock.TickerFundament()['Income']
    if ticker_python.at[ticker_python.index[i], 'Income'][-1] == 'M':
        ticker_python.at[ticker_python.index[i], 'Income'] = float(
            ticker_python.at[ticker_python.index[i], 'Income'][:-1]) * 1000000
    elif ticker_python.at[ticker_python.index[i], 'Income'][-1] == 'B':
        ticker_python.at[ticker_python.index[i], 'Income'] = float(
            ticker_python.at[ticker_python.index[i], 'Income'][:-1]) * 1000000000
    elif ticker_python.at[ticker_python.index[i], 'Income'][-1] == 'T':
        ticker_python.at[ticker_python.index[i], 'Income'] = float(
            ticker_python.at[ticker_python.index[i], 'Income'][:-1]) * 1000000000000
    elif ticker_python.at[ticker_python.index[i], 'Income'][-1] == 'K':
        ticker_python.at[ticker_python.index[i], 'Income'] = float(
            ticker_python.at[ticker_python.index[i], 'Income'][:-1]) * 1000

    ticker_python.at[ticker_python.index[i], 'Sales'] = stock.TickerFundament()['Sales']
    if ticker_python.at[ticker_python.index[i], 'Sales'][-1] == 'M':
        ticker_python.at[ticker_python.index[i], 'Sales'] = float(
            ticker_python.at[ticker_python.index[i], 'Sales'][:-1]) * 1000000
    elif ticker_python.at[ticker_python.index[i], 'Sales'][-1] == 'B':
        ticker_python.at[ticker_python.index[i], 'Sales'] = float(
            ticker_python.at[ticker_python.index[i], 'Sales'][:-1]) * 1000000000
    elif ticker_python.at[ticker_python.index[i], 'Sales'][-1] == 'T':
        ticker_python.at[ticker_python.index[i], 'Sales'] = float(
            ticker_python.at[ticker_python.index[i], 'Sales'][:-1]) * 1000000000000
    elif ticker_python.at[ticker_python.index[i], 'Sales'][-1] == 'K':
        ticker_python.at[ticker_python.index[i], 'Sales'] = float(
            ticker_python.at[ticker_python.index[i], 'Sales'][:-1]) * 1000

    try:
        ticker_python.at[ticker_python.index[i], 'Book/sh'] = float(stock.TickerFundament()['Book/sh'])
    except:
        ticker_python.at[ticker_python.index[i], 'Book/sh'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'P/B'] = float(stock.TickerFundament()['P/B'])
    except:
        ticker_python.at[ticker_python.index[i], 'P/B'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'ROA'] = float(stock.TickerFundament()['ROA'][:-1]) / 100
    except:
        ticker_python.at[ticker_python.index[i], 'ROA'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'Target Price'] = float(stock.TickerFundament()['Target Price'])
    except:
        ticker_python.at[ticker_python.index[i], 'Target Price'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'ROE'] = float(stock.TickerFundament()['ROE'][:-1]) / 100
    except:
        ticker_python.at[ticker_python.index[i], 'ROE'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'ROI'] = float(stock.TickerFundament()['ROI'][:-1]) / 100
    except:
        ticker_python.at[ticker_python.index[i], 'ROI'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'Employees'] = int(stock.TickerFundament()['Employees'])
    except:
        ticker_python.at[ticker_python.index[i], 'Employees'] = ''

    try:
        ticker_python.at[ticker_python.index[i], 'Debt/Eq'] = float(stock.TickerFundament()['Debt/Eq'])
    except:
        ticker_python.at[ticker_python.index[i], 'Debt/Eq'] = ''

    if (j % 50) == 0: print(j, "--- %s seconds ---" % (time.time() - start_time))
    j += 1

ticker_python.reset_index(level=0, inplace=True)
ticker_python.to_excel(r'ticker_isin_file.xlsx', sheet_name='AmericanFinancials', index=False)
