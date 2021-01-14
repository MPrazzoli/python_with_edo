# Imported packages
import pandas as pd

# Project's imports
from moduls.stock_dataframe_class import StockListClass
from pickle_obj.read_pickle_df import read_available_ticker_from_pickle, read_not_found_from_pickle, read_data_for_analysis

'''
do not make the big df just recall df from dictionary and use the dateindex to recall data

df3.loc['2018-01-12':'2018-01-20'] 
'''


def main():
    available_tickers = read_available_ticker_from_pickle()
    not_found_tickers = read_not_found_from_pickle(max_not_found_record=100)
    available_tickers = pd.DataFrame(available_tickers)
    available_tickers.set_index(0, inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns
    available_tickers.drop(not_found_tickers, inplace=True)
    ticker_list_object = StockListClass(ticker_list=list(available_tickers.index))
    start_date = '2021-01-01'
    end_date = '2021-01-07'
    stock_object_dictionary = read_data_for_analysis(ticker_list_object, start=start_date, end=end_date)

    print(5)


if __name__ == '__main__':
    main()

