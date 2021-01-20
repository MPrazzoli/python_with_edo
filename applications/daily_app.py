# Imported packages
from datetime import date, timedelta

# Project's imports
from api_moduls.api import api_function
from pickle_obj.read_pickle_df import read_from_pickle, read_not_found_from_pickle
from pickle_obj.write_pickle_df import write_to_pickle, write_not_found_from_pickle


def main():
    # Setting of Start date and End date of our retrieving period
    start_date = date.today() - timedelta(2)
    end_date = date.today() + timedelta(1)

    try:
        # Retrieving process and computation of tickers that are already into our DB but we want excluded
        # cause they do not give a data response since the limit we fix in variable max_not_found_record

        pickle_not_found_tickers_list = read_not_found_from_pickle(max_not_found_record=100)

    except:
        pickle_not_found_tickers_list = []

        # Function call to run the retrieving process and store market data in a dictionary of StockClass instances
        # (take a look at stock_dataframe_class.py for more information)
        # application variable is used to tell which script is calling api_function (daily app as this variable set to
        # zero, whereas period app has it set to one)
    stock_object_dictionary, ticker_list_object = \
        api_function(start=start_date, end=end_date, not_found_tickers=pickle_not_found_tickers_list, daily_app=1)

    write_not_found_from_pickle(stock_object_dictionary=stock_object_dictionary, ticker_list_object=ticker_list_object)

    # Read from pickle the stock dictionary object of stock dataframes to update it
    # .pkl files are used cause they guarantee better performance in retrieving process time
    stock_object_dictionary_pickle = read_from_pickle(ticker_list_object)

    for ticker in ticker_list_object.ticker_list:
        try:
            stock_object_dictionary_pickle['{0}'.format(ticker)].pickle = \
                stock_object_dictionary_pickle['{0}'.format(ticker)].pickle.append(
                    stock_object_dictionary['{0}'.format(ticker)].history)

        except:
            stock_object_dictionary_pickle['{0}'.format(ticker)].pickle = stock_object_dictionary[
                '{0}'.format(ticker)].history

        try:
            stock_object_dictionary_pickle['{0}'.format(ticker)].pickle = stock_object_dictionary_pickle[
                '{0}'.format(ticker)].pickle.groupby(level=0).last()
        except:
            print(ticker)

    write_to_pickle(stock_object_dictionary_pickle, ticker_list_object)
    print('the end')


# Beginning of the period_app script
if __name__ == "__main__":
    main()
