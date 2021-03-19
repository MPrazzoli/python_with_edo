# Imported packages
from datetime import date, timedelta

# Project's imports
from _2_api_moduls._2_1_api import api_function
from _3_pickle_obj._3_0_read_pickle_df import read_from_pickle, read_not_found_from_pickle
from _3_pickle_obj._3_1_write_pickle_df import write_to_pickle, write_not_found_from_pickle
from _7_export_csv_for_ipynb._7_0_export_adjcls_df import export_csv

#TODO: aggiungi un file pkl per tenere traccia dell'ultimo giorno osservato e salvato per poi fare un retrieving da quella data ultima osservata ad oggi +1 gg per yahoo finance
def main():
    # Setting of Start date and End date of our retrieving period
    start_date = date.today() - timedelta(15)
    end_date = date.today() + timedelta(1)

    try:
        # Retrieving process and computation of tickers that are already into our DB but we want excluded
        # cause they do not give a data response since the limit we fix in variable max_not_found_record

        pickle_not_found_tickers_list = read_not_found_from_pickle(max_not_found_record=100)

    except:
        pickle_not_found_tickers_list = []

    # Function call to run the retrieving process and store market data in a dictionary of StockClass instances
    # (take a look at _2_0_stock_dataframe_class.py for more information)
    # application variable is used to tell which script is calling api_function (daily app as this variable set to
    # zero, whereas period app has it set to one)
    stock_object_dictionary, ticker_list_object = \
        api_function(start=start_date, end=end_date, not_found_tickers=pickle_not_found_tickers_list, daily_app=0)

    write_not_found_from_pickle(stock_object_dictionary=stock_object_dictionary, ticker_list_object=ticker_list_object)

    # Read from pickle the stock dictionary object of stock dataframes to update it
    # .pkl files are used cause they guarantee better performance in retrieving process time
    stock_object_dictionary_pickle = read_from_pickle(ticker_list_object)

    for ticker in ticker_list_object.ticker_list:
        try:
            stock_object_dictionary_pickle['{0}'.format(ticker)].pickle =\
                stock_object_dictionary_pickle['{0}'.format(ticker)].pickle.append(
                    stock_object_dictionary['{0}'.format(ticker)].history)

        except:
            stock_object_dictionary_pickle['{0}'.format(ticker)].pickle = stock_object_dictionary[
                '{0}'.format(ticker)].history

        try:
            stock_object_dictionary_pickle['{0}'.format(ticker)].pickle = stock_object_dictionary_pickle[
                '{0}'.format(ticker)].pickle.groupby(level=0).last()
        except:
            print('check error in last price for group by pickle --', ticker)

    write_to_pickle(stock_object_dictionary_pickle, ticker_list_object)

    start_date_for_export = (date.today() - timedelta(600)).strftime('%Y-%m-%d')
    end_date_for_export = date.today().strftime('%Y-%m-%d')

    export_csv(start_date_for_export, end_date_for_export)

    print('the end')


# Beginning of the period_app script
if __name__ == "__main__":
    main()
