# Imported packages
import os
import pandas as pd
import time
from datetime import datetime
from QuantLib import *
import warnings


# Set of the project path to find also data path where the tickers list is stored in your computer
project_root = os.path.dirname(os.path.dirname(__file__))
data_path = project_root + '/static/data'

# Getting the list of all tickers we are interested in from the ticker_isin_file.xlsx excel file,
# then a StockListClass instance is initialize to store the list of tickers and the list
# of isin which we insert in our excel file
ticker_python = pd.read_excel(data_path + '/ticker_isin_file.xlsx', sheet_name='new-to-update-period')
ticker_python.set_index('ticker', inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns

for ticker in ticker_python.index:
    try:
        os.remove(project_root + '/pickle_obj/stock_dataframes/' + ticker + '.pkl')
    except:continue