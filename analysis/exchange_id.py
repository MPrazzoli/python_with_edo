# Imported packages
import os
import time
import numpy as np
import pandas as pd
from datetime import date, timedelta

# Project's imports
from pickle_obj.read_pickle_df import read_available_ticker_from_pickle, read_data_for_analysis_linearInterp_for_nan


def exchangeId_dict_StockClass(lag, id=None):
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/static/data'

    # Getting the list of all tickers we are interested in from the ticker_isin_file.xlsx excel file,
    # then a StockListClass instance is initialize to store the list of tickers and the list
    # of isin which we insert in our excel file
    ticker_python = pd.read_excel(data_path + '/ticker_isin_file.xlsx', sheet_name='American')
    ticker_python.set_index('ticker', inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns

    start_date = (date.today() - timedelta(lag)).strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')
    stock_object_dictionary = read_data_for_analysis_linearInterp_for_nan(max_not_found_record=5, start=start_date,
                                                                          end=end_date)

    start_time = time.time()  # To compute code execution time for each retrieve

    ticker_list = []
    for element in stock_object_dictionary.copy():
        if id is None:
            try:
                stock_object_dictionary['{0}'.format(element)].exchangeid =\
                ticker_python.loc[element]['exchange_id']
                ticker_list.append(element)

            except:
                pass

        else:
            try:
                if ticker_python.loc[element]['exchange_id']==id:
                    stock_object_dictionary['{0}'.format(element)].exchangeid = \
                        ticker_python.loc[element]['exchange_id']
                    ticker_list.append(element)
                else:
                    stock_object_dictionary.pop(element)

            except:
                pass

    print("--- %s seconds ---" % (time.time() - start_time))
    return stock_object_dictionary, ticker_list


def exchangeId_ticker_list(id=None):
    available_tickers = read_available_ticker_from_pickle()
    available_tickers = pd.DataFrame(available_tickers, columns=['ticker'])
    available_tickers.set_index('ticker', inplace=True)
    available_tickers['exchange_id'] = np.nan
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/static/data'

    # Getting the list of all tickers we are interested in from the ticker_isin_file.xlsx excel file,
    # then a StockListClass instance is initialize to store the list of tickers and the list
    # of isin which we insert in our excel file
    ticker_python = pd.read_excel(data_path + '/ticker_isin_file.xlsx', sheet_name='American')
    ticker_python.set_index('ticker', inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns

    start_time = time.time()  # To compute code execution time for each retrieve

    ticker_list = []
    for element in available_tickers.index:
        if id is not None:
            try:
                if ticker_python.loc[element]['exchange_id']==id:
                    ticker_list.append(element)
                else:
                    continue

            except:
                pass

        else:
            try:
                return (list(available_tickers.index))

            except:
                pass

    print("--- %s seconds ---" % (time.time() - start_time))

    return ticker_list




def main():
    ticker_list = exchangeId_ticker_list(676)
    stock_object_dictionary, ticker_list = exchangeId_dict_StockClass(180, 676)
    print(0)


if __name__ == "__main__":
    main()