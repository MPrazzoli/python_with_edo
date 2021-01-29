# Imported packages
import os
import time
import pandas as pd
import numpy as np
from QuantLib import *
from datetime import datetime

# Imported packages for market data retrieving
import yfinance as yf
# from yahoo_fin.stock_info import get_data
import investpy

# Project's imports
from api_moduls.stock_dataframe_class import StockClass, StockListClass, ImportantDatesClass

'''
In this project all stock market data are retrieve from Yahoo Finance API or alternatively from Investing.com API.
Both methods required the list of tickers to retrieve, the period of time (start date and end date) and the time frequency 
of the data (daily, weekly, monthly ... data). At the moment we use just daily data retrieve.
'''


def api_function(start, end, not_found_tickers, daily_app):
    """
    :param start: datetime.date
                Download start date
    :param end: datetime.date
            Download end date
    :param not_found_tickers: list
                            Not found tickers we want to exclude from the retrieving process
    :param daily_app: int
                    1 for daily app and zero for period app
    :return: stock_object_dictionary, ticker_list_object
    """

    start_time = time.time()  # To compute code execution time for each retrieve

    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/static/data'

    # Getting the list of all tickers we are interested in from the ticker_isin_file.xlsx excel file,
    # then a StockListClass instance is initialize to store the list of tickers and the list
    # of isin which we insert in our excel file
    ticker_python = pd.read_excel(data_path + '/ticker_isin_file.xlsx', sheet_name='American') # new-to-update-period
    ticker_python.set_index('ticker', inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns

    ticker_python.drop(not_found_tickers, inplace=True)
    ticker_list_object = StockListClass(ticker_list=list(ticker_python.index),
                                        isin_list=list(ticker_python.values[:, 0]),
                                        exchangeId_list=list(ticker_python.values[:, 1]))

    # Retrieve the DataFrame which contains all American stocks listed on Investpy package excel file.
    # This step it is made because we begin to retrieve stock's data from Yahoo Finance API,
    # but when we have an error or missing data from Yahoo Finance during the retrieving process
    # we try to get those date from Investing.com.
    # Sometimes Investing.com use different tickers from the original ones which are used in Yahoo Finance instead,
    # for this reason we begin from the ticker in which we found an issue during the retrieving process and with the isin
    # that is linked to that ticker we begin searching the same isin in the investing_stocks_dataframe to find
    # the ticker which is assign to that stock in Investing.com.
    investing_stocks_dataframe = pd.read_excel(data_path + '/stocksInvesting(onlyUSstocks).xlsx',
                                               sheet_name='investing')

    # We initialize an instance of ImportantDate class to store the Start date and the End date
    # of our analysis period ( UnitedStates calendar is the Quanlib object to manage trading days and
    # the parameter = 1 tells QuanLib to use the NYSE calendar cause we want to trade American stocks in this case)
    # (take a look at stock_dataframe_class.py for more information)
    important_dates = ImportantDatesClass(calendar=UnitedStates(1), start=start, end=end)
    important_dates.trading_day_list_method()

    # Definition of a dictionary to store stock as StockClass instances and for each stock get attribute
    # (take a look at stock_dataframe_class.py for more information)
    stock_object_dictionary = {'{0}'.format(ticker): StockClass(ticker=ticker, isin=ticker_list_object.isin_list[i], exchangeid=ticker_list_object.exchangeId_list[i]) for i, ticker in enumerate(ticker_list_object.ticker_list)}

    # Definition of our QuantLib market
    market = 'United States'
    market.lower()

    # To keep tracking the api process
    j = 0

    for ticker in ticker_list_object.ticker_list:

        try:
            stock_object_dictionary['{0}'.format(ticker)].history = yf.Ticker(ticker).history(period='1d',
                                                                                              start=important_dates.start_date_yahoofinance,
                                                                                              end=important_dates.end_date_yahoofinance,
                                                                                              auto_adjust=False)
            stock_object_dictionary['{0}'.format(ticker)].history = stock_object_dictionary[
                '{0}'.format(ticker)].history.groupby(level=0).last()  # get rid of duplicates
            if stock_object_dictionary['{0}'.format(ticker)].history.empty:
                if not('Dividends' in stock_object_dictionary['{0}'.format(ticker)].history):
                    stock_object_dictionary['{0}'.format(ticker)].nanDiv = True
                if not('Stock Splits' in stock_object_dictionary['{0}'.format(ticker)].history):
                    stock_object_dictionary['{0}'.format(ticker)].nanSplit = True

                if daily_app:

                    try:
                        stock_info_dataframe = investing_stocks_dataframe[
                            investing_stocks_dataframe['country'] == market.lower()]  # filter for 'united states'
                        stock_info_dataframe = stock_info_dataframe[
                            stock_info_dataframe['isin'] == ticker_python['isin'][ticker]]
                        investing_symbol = stock_info_dataframe['symbol'].values[0]
                        stock_object_dictionary['{0}'.format(ticker)].investing = investpy.get_stock_historical_data(
                            stock=investing_symbol, country=market, from_date=important_dates.start_date_investingcom,
                            to_date=important_dates.end_date_investingcom)
                        stock_object_dictionary['{0}'.format(ticker)].investing['Adj Close'] = \
                            stock_object_dictionary['{0}'.format(ticker)].investing['Close']
                        stock_object_dictionary['{0}'.format(ticker)].investing['Dividends'] = np.nan
                        stock_object_dictionary['{0}'.format(ticker)].investing['Stock Splits'] = np.nan

                    except:
                        stock_object_dictionary['{0}'.format(ticker)].not_found = \
                            np.append(stock_object_dictionary['{0}'.format(ticker)].not_found,
                                      np.array([[datetime.now(), ticker]]), axis=0)
                        stock_object_dictionary['{0}'.format(ticker)].not_found = \
                            pd.DataFrame({'date': stock_object_dictionary['{0}'.format(ticker)].not_found[1:, 0],
                                          'ticker': stock_object_dictionary['{0}'.format(ticker)].not_found[1:,
                                                    1]}).set_index('date')
        except:
            if daily_app:
                try:
                    stock_info_dataframe = investing_stocks_dataframe[
                        investing_stocks_dataframe['country'] == market.lower()]  # filter for 'united states'
                    stock_info_dataframe = stock_info_dataframe[
                        stock_info_dataframe['isin'] == ticker_python['isin'][ticker]]
                    investing_symbol = stock_info_dataframe['symbol'].values[0]
                    stock_object_dictionary['{0}'.format(ticker)].investing = investpy.get_stock_historical_data(
                        stock=investing_symbol, country=market, from_date=important_dates.start_date_investingcom,
                        to_date=important_dates.end_date_investingcom)
                    stock_object_dictionary['{0}'.format(ticker)].investing['Adj Close'] = \
                        stock_object_dictionary['{0}'.format(ticker)].investing['Close']
                    stock_object_dictionary['{0}'.format(ticker)].investing['Dividends'] = np.nan
                    stock_object_dictionary['{0}'.format(ticker)].investing['Stock Splits'] = np.nan

                except:
                    stock_object_dictionary['{0}'.format(ticker)].not_found = \
                        np.append(stock_object_dictionary['{0}'.format(ticker)].not_found,
                                  np.array([[datetime.now(), ticker]]), axis=0)
                    stock_object_dictionary['{0}'.format(ticker)].not_found = \
                        pd.DataFrame({'date': stock_object_dictionary['{0}'.format(ticker)].not_found[1:, 0],
                                      'ticker': stock_object_dictionary['{0}'.format(ticker)].not_found[1:,
                                                1]}).set_index('date')

        # try:
        #     stock_object_dictionary['{0}'.format(ticker)].get_data = get_data(ticker,
        #                                                                       start_date=important_dates.start_date_investingcom,
        #                                                                       end_date=important_dates.end_date_investingcom)
        #     stock_object_dictionary['{0}'.format(ticker)].get_data.drop(['ticker'], axis=1, inplace=True)
        #     stock_object_dictionary['{0}'.format(ticker)].get_data.rename(
        #         columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'adjclose': 'Adj Close',
        #                  'volume': 'Volume'})
        #     stock_object_dictionary['{0}'.format(ticker)].get_data['Dividends'] = np.nan
        #     stock_object_dictionary['{0}'.format(ticker)].get_data['Stock Splits'] = np.nan
        #
        # except:
        #     pass

        if daily_app == 0:
            try:
                stock_info_dataframe = investing_stocks_dataframe[
                    investing_stocks_dataframe['country'] == market.lower()]  # filter 'united states' stocks
                stock_info_dataframe = stock_info_dataframe[
                    stock_info_dataframe['isin'] == ticker_python['isin'][ticker]]
                investing_symbol = stock_info_dataframe['symbol'].values[0]
                stock_object_dictionary['{0}'.format(ticker)].investing = investpy.get_stock_historical_data(
                    stock=investing_symbol, country=market, from_date=important_dates.start_date_investingcom,
                    to_date=important_dates.end_date_investingcom)
                stock_object_dictionary['{0}'.format(ticker)].investing['Adj Close'] = \
                    stock_object_dictionary['{0}'.format(ticker)].investing['Close']
                stock_object_dictionary['{0}'.format(ticker)].investing['Dividends'] = np.nan
                stock_object_dictionary['{0}'.format(ticker)].investing['Stock Splits'] = np.nan

            except:
                if stock_object_dictionary['{0}'.format(ticker)].history.empty:
                    stock_object_dictionary['{0}'.format(ticker)].not_found = \
                        np.append(stock_object_dictionary['{0}'.format(ticker)].not_found,
                                  np.array([[datetime.now(), ticker]]), axis=0)
                    stock_object_dictionary['{0}'.format(ticker)].not_found = \
                        pd.DataFrame({'date': stock_object_dictionary['{0}'.format(ticker)].not_found[1:, 0],
                                      'ticker': stock_object_dictionary['{0}'.format(ticker)].not_found[1:,
                                                1]}).set_index('date')
                else:
                    pass

        try:

            stock_object_dictionary['{0}'.format(ticker)].history = important_dates.trading_day_dataframe.join(
                stock_object_dictionary['{0}'.format(ticker)].history)

            if stock_object_dictionary['{0}'.format(ticker)].nanDiv:
                stock_object_dictionary['{0}'.format(ticker)].history['Dividends'] = np.nan
            if stock_object_dictionary['{0}'.format(ticker)].nanSplit:
                stock_object_dictionary['{0}'.format(ticker)].history['Stock Splits'] = np.nan

            try:
                stock_object_dictionary['{0}'.format(ticker)].history.fillna(
                    stock_object_dictionary['{0}'.format(ticker)].investing, inplace=True)

            except:
                pass

        except:
            pass

        if (j % 50) == 0: print(j, "--- %s seconds ---" % (time.time() - start_time))
        j += 1

    print("--- time of api: %s seconds ---" % (time.time() - start_time))

    return stock_object_dictionary, ticker_list_object
