# Imported packages
import os
import time
import pandas as pd
from datetime import date, timedelta
from yahoofinancials import YahooFinancials

# Project's imports
from pickle_obj.read_pickle_df import read_data_for_analysis_linearInterp_for_nan


def financials_dict_StockClass(lag, exchangeid=None, sector=None, industry=None, country=None, pe=None, eps=None,
                               insiderown=None, shsout=None, shsfloat=None, mktcap=None, income=None, sales=None,
                               bookh=None, pb=None, roa=None, tp=None, roe=None, roi=None, employees=None, debteq=None):

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

    ticker_python2 = pd.read_excel(data_path + '/ticker_isin_file.xlsx', sheet_name='AmericanFinancials')
    final_df = pd.concat([ticker_python2['ticker'], ticker_python2['isin']], axis=1, keys=['ticker', 'isin'])

    if exchangeid is not None:
        final_df['exchangeid'] = ticker_python2['exchange_id']

    if sector is not None:
        final_df['sector'] = ticker_python2['Sector']

    if industry is not None:
        final_df['industry'] = ticker_python2['Industry']

    if country is not None:
        final_df['country'] = ticker_python2['Country']

    if pe is not None:
        final_df['pe'] = ticker_python2['P/E']

    if eps is not None:
        final_df['eps'] = ticker_python2['EPS (ttm)']

    if insiderown is not None:
        final_df['insiderown'] = ticker_python2['Insider Own']

    if shsout is not None:
        final_df['shsout'] = ticker_python2['Shs Outstand']

    if shsfloat is not None:
        final_df['shsfloat'] = ticker_python2['Shs Float']

    if mktcap is not None:
        final_df['mktcap'] = ticker_python2['Market Cap']

    if income is not None:
        final_df['income'] = ticker_python2['Income']

    if sales is not None:
        final_df['sales'] = ticker_python2['Sales']

    if bookh is not None:
        final_df['bookh'] = ticker_python2['Book/sh']

    if pb is not None:
        final_df['pb'] = ticker_python2['P/B']

    if roa is not None:
        final_df['roa'] = ticker_python2['ROA']

    if tp is not None:
        final_df['tp'] = ticker_python2['Target Price']

    if roe is not None:
        final_df['roe'] = ticker_python2['ROE']

    if roi is not None:
        final_df['roi'] = ticker_python2['ROI']

    if employees is not None:
        final_df['employees'] = ticker_python2['Employees']

    if debteq is not None:
        final_df['debteq'] = ticker_python2['Debt/Eq']

    final_df.set_index('ticker', inplace=True)  # Setting the index of ticker_python DataFrame with Tickers columns

    headers = list(final_df.columns)
    headers.remove('isin')
    headers.remove('exchangeid')

    final_df.dropna(subset=headers, how='all', inplace=True)

    del ticker_python2

    start_time = time.time()  # To compute code execution time for each retrieve

    # To keep tracking the api process
    j = 0

    ticker_list = list(final_df)
    for element in stock_object_dictionary.copy():
        try:
            for column in final_df.columns:
                setattr(stock_object_dictionary['{0}'.format(element)], column, final_df.loc[element][column])

        except:
            stock_object_dictionary.pop(element)

        if (j % 50) == 0: print(j, "--- %s seconds ---" % (time.time() - start_time))
        j += 1

    print("--- time of financial filter: %s seconds ---" % (time.time() - start_time))
    return stock_object_dictionary, ticker_list


def main():
    stock_object_dictionary, ticker_list = financials_dict_StockClass(180, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                                      1, 1, 1, 1, 1)
    print(0)


if __name__ == "__main__":
    main()