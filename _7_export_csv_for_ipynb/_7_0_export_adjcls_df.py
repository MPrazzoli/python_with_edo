# Imported packages
import numpy as np
import os
import pandas as pd
from datetime import date, timedelta
import time
import networkx as nx
from collections import Counter

# Project's imports
from _2_api_moduls._2_0_stock_dataframe_class import StockListClass
from _3_pickle_obj._3_0_read_pickle_df import read_available_ticker_from_pickle, read_not_found_from_pickle, \
    read_data_for_analysis_linearInterp_for_nan
# from analysis_functions.correlation import cross_correlation_function


def stock_analysis():
    start_date = (date.today() - timedelta(365)).strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')
    stock_object_dictionary = read_data_for_analysis_linearInterp_for_nan(max_not_found_record=5, start=start_date,
                                                                          end=end_date)
    ticker_list = []
    for element in stock_object_dictionary:
        ticker_list.append(element)

    # construction of the open prices
    open_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Open'] for element in
                            stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    # construction of the high prices
    high_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['High'] for element in
                            stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    # construction of the low prices
    low_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Low'] for element in
                        stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    # construction of the adjusted close prices
    adjclose_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Adj Close'] for element in
                                stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    volume_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Volume'] for element in
                                stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/_8_jupyter_notebooks/_8_0_exported_dataframe/open_' + start_date + '_' + end_date + '_' + str(len(ticker_list))
    open_df.to_csv(data_path, index=True)

    data_path = project_root + '/_8_jupyter_notebooks/_8_0_exported_dataframe/high_' + start_date + '_' + end_date + '_' + str(len(ticker_list))
    high_df.to_csv(data_path, index=True)

    data_path = project_root + '/_8_jupyter_notebooks/_8_0_exported_dataframe/low_' + start_date + '_' + end_date + '_' + str(len(ticker_list))
    low_df.to_csv(data_path, index=True)

    data_path = project_root + '/_8_jupyter_notebooks/_8_0_exported_dataframe/adjclose_' + start_date + '_' + end_date + '_' + str(len(ticker_list))
    adjclose_df.to_csv(data_path, index=True)

    data_path = project_root + '/_8_jupyter_notebooks/_8_0_exported_dataframe/volume_' + start_date + '_' + end_date + '_' + str(len(ticker_list))
    volume_df.to_csv(data_path, index=True)


def main():
    stock_analysis()


if __name__ == "__main__":
    main()