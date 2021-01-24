import numpy as np
import pandas as pd
from QuantLib import *


class StockClass(object):

    # Initialization of the StockClass object with the ticker symbol which is use to construct a yf.Ticker object
    def __init__(self, ticker, isin=None, exchangeId=None):
        self.name = ticker
        self.isin = isin
        self.exchangeId = exchangeId
        # self.history is the method of the SotckClass object to store data in DataFrame format
        self.history = pd.DataFrame
        self.investing = pd.DataFrame
        self.pickle = pd.DataFrame
        self.not_found = np.array([['date', 'ticker']])
        self.nanDiv = False
        self.nanSplit = False

class StockListClass(object):

    # Initialization of the StockListClass object with ticker symbol and isin code of all stocks we are interested in
    def __init__(self, ticker_list, isin_list=None, exchangeId_list=None):
        self.ticker_list = ticker_list
        self.isin_list = isin_list
        self.exchangeId_list = exchangeId_list


class ImportantDatesClass(object):

    # Initialization of the ImportantDatesClass object and setting each date in the right format for
    # each specific retrieving package
    def __init__(self, calendar, start, end):
        self.start_date = start
        self.start_date_yahoofinance = str(self.start_date.year) + '-' + str(self.start_date.month) + '-' + str(
            self.start_date.day)
        self.start_date_investingcom = str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(
            self.start_date.year)
        self.start_date_quantlib = Date(int(self.start_date_yahoofinance.split('-')[2]),
                                        int(self.start_date_yahoofinance.split('-')[1]),
                                        int(self.start_date_yahoofinance.split('-')[0]))
        self.end_date = end
        self.end_date_yahoofinance = str(self.end_date.year) + '-' + str(self.end_date.month) + '-' + str(
            self.end_date.day)
        self.end_date_investingcom = str(self.end_date.day) + '/' + str(self.end_date.month) + '/' + str(
            self.end_date.year)
        self.end_date_quantlib = Date(int(self.end_date_yahoofinance.split('-')[2]),
                                      int(self.end_date_yahoofinance.split('-')[1]),
                                      int(self.end_date_yahoofinance.split('-')[0]))
        self.calendar = calendar
        self.trading_day_list = []
        self.trading_day_list_of_dates = None
        self.trading_day_list_formatted = None
        self.trading_day_dataframe = None

    # This method is used to compute the right trading calendar (non-holiday) and its output is a dataframe
    # of those dates which are found thanks QuantLib package
    def trading_day_list_method(self):
        day = self.start_date_quantlib
        while day <= self.end_date_quantlib:
            if not self.calendar.isHoliday(day) and not self.calendar.isWeekend(day.weekday()):
                self.trading_day_list.append(day)
            day = day + Period(1, Days)
        self.trading_day_list_of_dates = [day.to_date() for day in self.trading_day_list]
        self.trading_day_timestamp_of_dates = [pd.Timestamp(l) for l in self.trading_day_list_of_dates]
        d = {'date': self.trading_day_timestamp_of_dates,
             'date': self.trading_day_timestamp_of_dates}
        self.trading_day_dataframe = pd.DataFrame(d).set_index('date')


class AnalysisDatesClass(object):

    # Initialization of the AnalysisDatesClass object and setting dates of the analysis period
    def __init__(self, start, end):
        self.start_date = start
        self.end_date = end

# Not used function
# def difference_between_list(list1, list2):
#     return list(list(set(list1) - set(list2)) + list(set(list2) - set(list1)))


# Not used method/function
# def mongodb_retrieve_data_method(self, start, end):
#     try:
#         self.history = self.ticker_object.history(period='1d', start=start, end=end, auto_adjust=False)
#         # setting index name of the DateFrame already retrieved with the name 'Date_Time' and the columns with the
#         # Open Price ... Close Price ... 'StockSplits' which are columns of the DataFrame already retrieved
#         self.history.index.names = ['Date_Time']
#         self.history.columns = ['OpenPrice',
#                                 'HighPrice',
#                                 'LowPrice',
#                                 'ClosePrice',
#                                 'AdjClose',
#                                 'Volume',
#                                 'Dividends',
#                                 'StockSplits']
#         self.index_list_formatted = [int(x.strftime(format='%Y%m%d')) for x in self.history.index.tolist()]
#     except:
#         pass
#
# class ArcticDatesClass(object):
#
#     # Initialization of the ArcticDatesClass object and setting dates of the retrieving period
#     def __init__(self, start, end):
#         self.start_date = start
#         self.end_date = end
