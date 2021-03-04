# Necessary Libraries
import os
import yfinance as yf, pandas as pd, shutil, os, time, glob
import numpy as np
import requests
# from get_all_tickers import get_tickers as gt
from statistics import mean
from datetime import date, timedelta

# our packages
from _3_pickle_obj._3_0_read_pickle_df import read_data_for_analysis_linearInterp_for_nan

def std_rsi_function(lag=365, period=14): # try also 9 and 22

    start_time = time.time()
    # Set of the project path to find also data path where the tickers list is stored in your computer
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = project_root + '/_6_analysis/rsi/'

    start_date = (date.today() - timedelta(lag)).strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')
    stock_object_dictionary = read_data_for_analysis_linearInterp_for_nan(max_not_found_record=5, start=start_date,
                                                                              end=end_date)
    ticker_list = []
    for element in stock_object_dictionary:
        ticker_list.append(element)

    # Create the dataframe that we will be adding the final _6_analysis of each stock to
    Compare_Stocks = pd.DataFrame(columns=["Company", "Days_Observed", "Crosses", "True_Positive", "False_Positive", "True_Negative", "False_Negative", "Sensitivity",
    "Specificity", "Accuracy", "TPR", "FPR"])

    # To keep tracking the api process
    j = 0

    # While loop to cycle through the stock paths
    for ticker in ticker_list:
        prices = list(stock_object_dictionary['{0}'.format(ticker)].history['Adj Close'])
        # Dataframe to hold the historical data of the stock we are interested in.
        prices_df = pd.DataFrame(prices)

        # The author of the code removes less than 2 dollars prices
        # # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
        # while c < len(Hist_data):
        #     if Hist_data.iloc[c,4] > float(2.00):  # Check that the closing price for this day is greater than $2.00
        #         prices.append(Hist_data.iloc[c,4])
        #     c += 1
        # prices_df = pd.DataFrame(prices)  # Make a dataframe from the prices list

        upPrices=[]
        downPrices=[]
        #  Loop to hold up and down price movements
        for i in range(len(prices)):
            if i == 0:
                upPrices.append(0)
                downPrices.append(0)
            else:
                if (prices[i]-prices[i-1])>0:
                    upPrices.append(prices[i]-prices[i-1])  # ABSOLUTE DIFFERENCE VALUE INSTEAD OF RELATIVE RETURN
                    downPrices.append(0)
                else:
                    downPrices.append(prices[i]-prices[i-1])  # ABSOLUTE DIFFERENCE VALUE INSTEAD OF RELATIVE RETURN
                    upPrices.append(0)

        avg_gain = []
        avg_loss = []
        #  Loop to calculate the average gain and loss
        for x in range(len(upPrices)):
            if x < period+1:
                avg_gain.append(0)
                avg_loss.append(0)
            else:
                sumGain = 0
                sumLoss = 0
                y = x-period
                while y<=x:
                    sumGain += upPrices[y]
                    sumLoss += downPrices[y]
                    y += 1
                avg_gain.append(sumGain/period)
                avg_loss.append(abs(sumLoss/period))

        RS = []
        RSI = []
        #  Loop to calculate RSI and RS
        for p in range(len(prices)):
            if p < period+1:
                RS.append(0)
                RSI.append(0)
            else:
                RSvalue = (avg_gain[p]/avg_loss[p])
                RS.append(RSvalue)
                RSI.append(100 - (100/(1+RSvalue)))

        #  Creates the csv for each stock's RSI and price movements
        df_dict = {
            'Prices' : prices,
            'upPrices' : upPrices,
            'downPrices' : downPrices,
            'AvgGain' : avg_gain,
            'AvgLoss' : avg_loss,
            'RS' : RS,
            'RSI' : RSI
        }

        stock_object_dictionary['{0}'.format(ticker)].rsi = pd.DataFrame(df_dict, columns = ['Prices', 'upPrices', 'downPrices', 'AvgGain','AvgLoss', 'RS', "RSI"])
        stock_object_dictionary['{0}'.format(ticker)].rsi.index = stock_object_dictionary['{0}'.format(ticker)].history.index

        if (j % 50) == 0: print(j, "--- %s seconds ---" % (time.time() - start_time))
        j += 1

    print("--- time of api: %s seconds ---" % (time.time() - start_time))
    return(stock_object_dictionary)


def main():
    dict = std_rsi_function()


if __name__ == "__main__":
    main()