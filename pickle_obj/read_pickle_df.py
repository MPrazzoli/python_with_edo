# Imported packages
import os
import pandas as pd
import time

# Project's imports
from moduls.stock_dataframe_class import StockClass, StockListClass


def read_available_ticker_from_pickle():
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/pickle_obj/stock_dataframes'
    # Retrieving process and computation of tickers that are into our DB
    available_ticker_list = os.listdir(data_path)

    for i, file in enumerate(available_ticker_list):
        available_ticker_list[i] = file.rsplit('.', 1)[0]

    return available_ticker_list


def read_not_found_from_pickle(max_not_found_record):
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/pickle_obj/not_found_records'
    ticker_list_object = StockListClass(ticker_list=os.listdir(data_path))

    # Retrieving process and computation of tickers that are already into our DB but we want excluded
    # cause they do not give a data response since the limit we fix in variable max_not_found_record
    not_found_over_limit_list = []

    for file in ticker_list_object.ticker_list:
        df = pd.read_pickle(project_root + '/pickle_obj/not_found_records/' + file)
        if len(df.index) > max_not_found_record:
            not_found_over_limit_list.append(file.rsplit('.', 1)[0])

    return not_found_over_limit_list


def read_from_pickle(ticker_list_object):
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))

    stock_object_dictionary_read_from_pickle = {'{0}'.format(ticker): StockClass(ticker=ticker) for ticker in
                                                ticker_list_object.ticker_list}

    for ticker in ticker_list_object.ticker_list:
        try:
            stock_object_dictionary_read_from_pickle['{0}'.format(ticker)].pickle = pd.read_pickle(
                project_root + '/pickle_obj/stock_dataframes/' + ticker + '.pkl')

        except:
            pass

    return stock_object_dictionary_read_from_pickle


def read_data_for_analysis_linearInterp_for_nan(max_not_found_record, start, end): # other interpolation types https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html
    i = time.time()
    available_tickers = read_available_ticker_from_pickle()
    not_found_tickers = read_not_found_from_pickle(max_not_found_record=max_not_found_record)
    available_tickers = pd.DataFrame(available_tickers)
    available_tickers.set_index(0, inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns
    available_tickers.drop(not_found_tickers, inplace=True)
    ticker_list_object = StockListClass(ticker_list=list(available_tickers.index))

    # Retrieving process from our DB
    stock_object_dictionary_for_analysis = read_from_pickle(ticker_list_object)
    print(time.time() - i)

    log_ticker_list = []  # tracking of tickers which had issues during the storage process from pickle to history
    all_nan_list = []  # tracking of all matrix NaN dataframe

    # Selecting the period of time for the analysis
    for ticker in ticker_list_object.ticker_list:
        try:
            stock_object_dictionary_for_analysis['{0}'.format(ticker)].history = stock_object_dictionary_for_analysis[
                                                                                     '{0}'.format(ticker)].pickle.loc[
                                                                                 start:end]

            if stock_object_dictionary_for_analysis['{0}'.format(ticker)].history.isnull().values.any():
                if len(stock_object_dictionary_for_analysis['{0}'.format(ticker)].history) * len(
                            stock_object_dictionary_for_analysis['{0}'.format(ticker)].history.columns) \
                            == stock_object_dictionary_for_analysis['{0}'.format(ticker)].history.isnull().sum().sum():

                    all_nan_list.append(ticker)

                else:
                    stock_object_dictionary_for_analysis['{0}'.format(ticker)].history.interpolate(method='linear',
                                                                                                   limit_direction='forward',
                                                                                                   axis=0, inplace=True)
                    stock_object_dictionary_for_analysis['{0}'.format(ticker)].history.interpolate(method='linear',
                                                                                               limit_direction='backward',
                                                                                               axis=0, inplace=True)

        except:
            log_ticker_list.append(ticker)
            continue

    if all_nan_list or log_ticker_list:
        for element in stock_object_dictionary_for_analysis.copy():
            if element in all_nan_list or element in log_ticker_list:
                stock_object_dictionary_for_analysis.pop(element)

    print('--- time to read from pickle in seconds --- ',time.time() - i)
    print('--- list of all nan tickers --- ', all_nan_list)
    print('--- list of logged tickers --- ', log_ticker_list)

    return stock_object_dictionary_for_analysis
