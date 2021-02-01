# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time
from datetime import date, timedelta

# our packages
from pickle_obj.read_pickle_df import read_data_for_analysis_linearInterp_for_nan
from analysis.exchange_id import exchangeId_dict_StockClass

def mark_minervini_screener(lag=365, quantile_value=.7, exchangeid_filter=True, exchangeid=None):

    if not exchangeid_filter:
        start_date = (date.today() - timedelta(lag)).strftime('%Y-%m-%d')
        end_date = date.today().strftime('%Y-%m-%d')
        stock_object_dictionary = read_data_for_analysis_linearInterp_for_nan(max_not_found_record=5, start=start_date,
                                                                              end=end_date)
        ticker_list = []

        for element in stock_object_dictionary:
            ticker_list.append(element)

    else:
        stock_object_dictionary, ticker_list = exchangeId_dict_StockClass(lag=lag, id=exchangeid)

    yf.pdr_override()

    # Variables
    # tickers = ['A', 'AA', 'AAL', 'AACQ', 'AAIC', 'AACG']  # si.tickers_sp500()
    # tickers = [item.replace('.', '-') for item in tickers] # Yahoo Finance uses dashes instead of dots

    # index_name_dj30 = '^ DJI'  # DOW JONES INDUSTRIAL AVERAGE
    index_name_sp500 = '^GSPC'  # S&P 500
    index_name_nasdaq = '^IXIC'  # NASDAQ
    index_name_russell2000 = '^RUT'  # RUSSELL 2000

    start_date = datetime.datetime.now() - datetime.timedelta(days=lag)
    end_date = datetime.date.today()
    exportList = pd.DataFrame(columns=['Stock', 'RS_Rating', '50 Day MA', '150 Day Ma', '200 Day MA', '52 Week Low', '52 week High'])
    returns_multiples = []

    # Index Returns S&P500
    index_sp500_df = pdr.get_data_yahoo(index_name_sp500, start_date, end_date)
    index_sp500_df['Percent Change'] = index_sp500_df['Adj Close'].pct_change()
    index_sp500_return = (index_sp500_df['Percent Change'] + 1).cumprod()[-1] # think to use log return instead of regular return --> segmentation for index of market or invented indeces
                                                                # example, construct your personal indeces per mkt capitalization or other financials
    # Index Returns NASDAQ
    index_nasdaq_df = pdr.get_data_yahoo(index_name_nasdaq, start_date, end_date)
    index_nasdaq_df['Percent Change'] = index_nasdaq_df['Adj Close'].pct_change()
    index_nasdaq_return = (index_nasdaq_df['Percent Change'] + 1).cumprod()[-1]

    # Index Returns RUSSELL2000
    index_russell2000_df = pdr.get_data_yahoo(index_name_russell2000, start_date, end_date)
    index_russell2000_df['Percent Change'] = index_russell2000_df['Adj Close'].pct_change()
    index_russell2000_return = (index_russell2000_df['Percent Change'] + 1).cumprod()[-1]

    # Find top 30% performing stocks (relative to the S&P 500)
    for ticker in ticker_list:
        # Download historical data as CSV for each stock (makes the process faster)
        # df = pdr.get_data_yahoo(ticker, start_date, end_date)
        # df.to_csv(f'{ticker}.csv')
        d = {'Adj Close': stock_object_dictionary['{0}'.format(ticker)].history['Adj Close']}
        df = pd.DataFrame(data=d, index=stock_object_dictionary['{0}'.format(ticker)].history.index)

        # Calculating returns relative to the market (returns multiple)
        df['Percent Change'] = df['Adj Close'].pct_change()
        stock_return = (df['Percent Change'] + 1).cumprod()[-1]
        if stock_object_dictionary['{0}'.format(ticker)].exchangeid == 676:
            index_return = index_sp500_return
        elif stock_object_dictionary['{0}'.format(ticker)].exchangeid == 663:
            index_return = index_nasdaq_return
        elif stock_object_dictionary['{0}'.format(ticker)].exchangeid == 650:
            index_return = index_russell2000_return

        returns_multiple = round((stock_return / index_return), 2)
        returns_multiples.extend([returns_multiple])

        # print(f'Ticker: {ticker}; Returns Multiple against S&P 500: {returns_multiple}\n')
        # time.sleep(1)

    # Creating dataframe of only top 30%
    rs_df = pd.DataFrame(list(zip(ticker_list, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
    rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
    rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(quantile_value)]

    # Checking Minervini conditions of top 30% of stocks in given list
    rs_stocks = rs_df['Ticker']
    for stock in rs_stocks:
        try:
            d = {'Adj Close': stock_object_dictionary['{0}'.format(stock)].history['Adj Close']}
            df = pd.DataFrame(data=d, index=stock_object_dictionary['{0}'.format(stock)].history.index)
            sma = [50, 150, 200]
            for x in sma:
                df['SMA_' + str(x)] = round(df['Adj Close'].rolling(window=x).mean(), 2)

            # Storing required values
            currentClose = df['Adj Close'][-1]
            moving_average_50 = df['SMA_50'][-1]
            moving_average_150 = df['SMA_150'][-1]
            moving_average_200 = df['SMA_200'][-1]
            low_of_52week = round(min(df['Adj Close'][-260:]), 2)
            high_of_52week = round(max(df['Adj Close'][-260:]), 2)
            RS_Rating = round(rs_df[rs_df['Ticker'] == stock].RS_Rating.tolist()[0])

            try:
                moving_average_200_20 = df['SMA_200'][-20]
            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            # condition_1 = currentClose > moving_average_150 > moving_average_200
            condition_1 = (currentClose > moving_average_150) and (currentClose > moving_average_200)

            # Condition 2: 150 SMA and > 200 SMA
            condition_2 = moving_average_150 > moving_average_200

            # Condition 3: 200 SMA trending up for at least 1 month (preferably 4-5 months minimum in most cases)
            condition_3 = moving_average_200 > moving_average_200_20

            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            # condition_4 = moving_average_50 > moving_average_150 > moving_average_200
            condition_4 = (moving_average_50 > moving_average_150) and (moving_average_50 > moving_average_200)

            # Condition 5: Current Price > 50 SMA
            condition_5 = currentClose > moving_average_50

            # Condition 6: Current Price is at least 25% - 30% above 52 week low
            condition_6 = currentClose >= (1.3 * low_of_52week)

            # Condition 7: Current Price is within 25% of 52 week high
            # condition_7 = currentClose >= (.75 * high_of_52week)
            condition_7 = currentClose <= (.75 * high_of_52week)

            # If all conditions above are true, add stock to exportList
            if (condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7):
                exportList = exportList.append({'Stock': stock, 'RS_Rating': RS_Rating, '50 Day MA': moving_average_50,
                                                '150 Day Ma': moving_average_150, '200 Day MA': moving_average_200,
                                                '52 Week Low': low_of_52week, '52 week High': high_of_52week},
                                               ignore_index=True)
                # print(stock + ' made the Minervini requirements')
        except Exception as e:
            print(e)
            print(f'Could not gather data on {stock}')

    exportList = exportList.sort_values(by='RS_Rating', ascending=False)
    print('\n', exportList)
    file_name = 'ScreenOutput' + date.today().strftime('%Y-%m-%d') + '_lag_' + str(lag) + '_quant_' + str(quantile_value) + '.xlsx'
    writer = ExcelWriter(file_name)
    exportList.to_excel(writer, 'Sheet1')
    writer.save()


def main():
    mark_minervini_screener(lag=365, quantile_value=.7, exchangeid_filter=True, exchangeid=None)


if __name__ == '__main__':
    main()
