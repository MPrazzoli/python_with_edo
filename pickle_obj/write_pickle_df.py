# Imported packages
import os
import pandas as pd


def write_not_found_from_pickle(stock_object_dictionary, ticker_list_object):
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/pickle_obj/not_found_records/'

    for ticker in ticker_list_object.ticker_list:
        try:
            if isinstance(stock_object_dictionary['{0}'.format(ticker)].not_found, pd.DataFrame):
                try:
                    df = pd.read_pickle(data_path + ticker + '.pkl')
                    frames = [df, stock_object_dictionary['{0}'.format(ticker)].not_found]
                    not_found_df = pd.concat(frames)

                except:
                    not_found_df = stock_object_dictionary['{0}'.format(ticker)].not_found

                not_found_df.to_pickle(data_path + ticker + '.pkl')

        except:
            pass


def write_to_pickle(stock_object_dictionary_to_write, ticker_list_object):
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/pickle_obj/stock_dataframes/'

    for ticker in ticker_list_object.ticker_list:
        try:
            stock_object_dictionary_to_write['{0}'.format(ticker)].pickle.to_pickle(data_path + ticker + '.pkl')

        except:
            pass

