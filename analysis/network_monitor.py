# Imported packages
import numpy as np
import pandas as pd
from datetime import date, timedelta
import time
import networkx as nx
from collections import Counter

# Project's imports
from api_moduls.stock_dataframe_class import StockListClass
from pickle_obj.read_pickle_df import read_available_ticker_from_pickle, read_not_found_from_pickle, \
    read_data_for_analysis_linearInterp_for_nan
# from analysis_functions.correlation import cross_correlation_function


def network_monitor_function():
    start_date = (date.today() - timedelta(180)).strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')
    stock_object_dictionary = read_data_for_analysis_linearInterp_for_nan(max_not_found_record=5, start=start_date,
                                                                          end=end_date)
    ticker_list = []
    for element in stock_object_dictionary:
        ticker_list.append(element)

    # construction of the open prices
    # open_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Open'] for element in
    #                         stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    # construction of the high prices
    # high_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['High'] for element in
    #                         stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    # construction of the low prices
    # low_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Low'] for element in
    #                         stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose()

    # construction of the adjusted close prices
    adjclose_df = pd.DataFrame([stock_object_dictionary['{0}'.format(element)].history['Adj Close'] for element in
                                stock_object_dictionary.copy()], index=list(stock_object_dictionary.keys())).transpose().astype('float32')

    # manage nan value and take off (in the read module) those series with too many nan, or with observation that are not at least the 60% of the total analysis period
    corr_matrix_adjclose = np.corrcoef(adjclose_df.transpose().to_numpy()).astype('float32')    # int64arr = ones((1024, 1024), dtype=np.uint64)
    # corr_matrix_adjclose = adjclose_df.corr(method='pearson').astype('float32')
    upper_trin_corr_matrix = np.triu(corr_matrix_adjclose, 1).astype('float32')
    upper_trin_corr_matrix = np.where(upper_trin_corr_matrix <= 0.000001, np.nan, upper_trin_corr_matrix) # mettere intervallo intorno a zero se si vogliono tenere le incorrelate
    quantile = np.nanquantile(upper_trin_corr_matrix, 0.75).astype('float32')
    corr_matrix_adjclose = np.where(corr_matrix_adjclose <= quantile, 0, corr_matrix_adjclose)
    corr_matrix_adjclose = np.triu(corr_matrix_adjclose, 1).astype('float32') # keeping just the upper triangle matrix

    # np.savetxt("test2CorrMatrix.csv", corr_matrix_adjclose, delimiter=",")
    # correlation method: pearson, kendall, spearman and callable
    # corr_matrix_adjclose = adjclose_df.corr(method='pearson').astype('float16')

    '''numpy.core._exceptions.MemoryError: Unable to allocate 197. MiB for an array with shape (1, 25786084) and data type float64'''

    del stock_object_dictionary

    corr_matrix_adjclose_df = pd.DataFrame(corr_matrix_adjclose, index=[i for i in ticker_list], columns=[i for i in ticker_list], dtype=np.float32)
    corr_matrix_adjclose_df = corr_matrix_adjclose_df.where(np.triu(np.ones(corr_matrix_adjclose_df.shape), 1).astype(np.bool))
    corr_matrix_adjclose_df = corr_matrix_adjclose_df.stack().reset_index()
    corr_matrix_adjclose_df.columns = ['Source', 'Target', 'Weight']
    corr_matrix_adjclose_df = corr_matrix_adjclose_df[corr_matrix_adjclose_df['Weight'] != 0]
    corr_matrix_adjclose_df.reset_index(drop=True, inplace=True)
    zipper = list(zip(corr_matrix_adjclose_df['Source'], corr_matrix_adjclose_df['Target']))
    graph = nx.Graph((x, y, {'weight': corr_matrix_adjclose_df.Weight[zipper.index((x, y))]}) for (x, y), v in
                       Counter(zipper).items())








    for (x, y), v in Counter(zipper).items():
        graph.add_edge(x, y, weight=corr_matrix_adjclose_df.Weight[zipper.index((x, y))])

    graph = nx.DiGraph((x, y, {'weight': corr_matrix_adjclose_df.Weight[zipper.index((x, y))]}) for (x, y), v in Counter(zipper).items())

    g = nx.DiGraph((x, y, {'weight': df.Value[Ed.index((x, y))]}) for (x, y), v in Counter(Ed).items())





    df = pd.DataFrame(np.where(np.triu(np.ones(corr_matrix_adjclose.shape), 1).astype(np.bool)))
    df2 = pd.DataFrame(df, columns=["A", "B"])

    G = nx.from_numpy_matrix(corr_matrix_adjclose)

    quantile = corr_matrix_adjclose.melt().value.quantile(0.75).astype('float16')

    corr_matrix_adjclose.apply(lambda x: [y if y >= quantile else 0 for y in x])
    # numpy compute corr in horizontal, it is necessary to convert the transposed dataframe (example adjclose_df.transpose())
    # to numpy (from dataframe to array) and then compute the correlation matrix as num = np.corrcoef(adjclose_df.transpose())
    # trin = np.triu(num, 1) prendo solamente il triangolo sopra la diagonale e il resto lo metto a zero
    # np.where(trin <= 0.000001, np.nan, trin) sostituisco tutti i valori di trin che sono prossimi a zerocon nan
    # quantile = np.nanquantile(ok, 0.75)  calcolo il quantile che voglio escludendo i nan
    # np.where(num <= quantile, 0, num) metto tutti le correlazioni inferiori alla soglia determinata pari a zero e così
    # la mia matrice di correlazione diventa un' adjacency matrix


     # poi costruire il network con 

    ######## Not useful anymore np.fill_diagonal(num2, np.nan)
    # quantile np.quantile(num, 0.75)
    # np.fill_diagonal(num2, np.nan)
    print(corr_matrix_adjclose)

    '''
    #############################################################################
    ###   corr_matrix_adjclose.describe().transpose() # to get Series stats   ###
    #############################################################################
    '''

    column_headers_list = corr_matrix_adjclose.columns.values.tolist()

    # TODO: la prossima riga dovrebbe impiantarsi e dare errore di memoria prova a bloccare l'esecuzione alla
    #  prossima riga e  lanciarla dal Terminal, nel caso non dovesse darti problemi, prova ad eseguire anche la riga successiva
    #  sempre dal terminal ... itera questa operazione fino a riscontrare un problema di memoria

    # corr_matrix_one_lag = np.zeros((len(column_headers_list), len(column_headers_list)))

    # corr_matrix_two_lag = np.zeros((len(column_headers_list), len(column_headers_list)))

    # Computation of log return of each stock over adjusted close prices
    # if you want there is also the method --> df['pct_change'] = df.price.pct_change()
    # and it compute percentage change







    log_return_adjclose_df = pd.DataFrame()
    for i, col in enumerate(column_headers_list):
        log_return_adjclose_df[col] = np.log(adjclose_df[col]) - np.log(adjclose_df[col].shift(-1))

    """
    ## Corr Adjustment ##
    # input of a rule to choose the most fittable correlation to the model (in this case it is chosen the .7 quant)
    # to erase those correlation that do not achive the chosen threshold
    """

    del stock_object_dictionary

    tempo = time.time()
    corr_matrix_lag = pd.DataFrame()
    i = 0
    for element in column_headers_list:
        df = log_return_adjclose_df
        df[element] = df[element].shift(1)
        corr_matrix_lag = corr_matrix_lag.append(df.corr()[element])
        print("row: ", i, "--- %s seconds ---" % (tempo - time.time()))
        i += 1

    print('arrivati')

    lag = 1

    # we need a faster method to compute the cross-correlation matrix of 5000 stocks

    for i, col in enumerate(column_headers_list):
        for j, col in enumerate(column_headers_list):
            if i != j:
                # to measure the effect of i on j
                corr_matrix_one_lag[i][j] = \
                    log_return_adjclose_df[column_headers_list[j]].corr(
                        log_return_adjclose_df[column_headers_list[i]].shift(lag))

            if (i % 50) == 0 and (j % 50) == 0: print('row: ', i, ', column: ', j,
                                                      " --- %s seconds ---" % (tempo - time.time()))
    # https://riptutorial.com/pandas/example/9812/using-hdfstore
    # https://stackoverflow.com/questions/33171413/cross-correlation-time-lag-correlation-with-pandas/55490747
    print('arrivati')

    # it is done in this way because the library networkx does (Notes: it is the opposite way of the theory of the book "Networks: An Introduction")

    # then insert the efficient performance on the lagged i.e. try different lag periods
    ### for col in db_adj.columns:
    ###     xycorr = [crosscorr(db_adj[col], db_adj[col], lag=i) for i in range(12)] # call function for lagged correlation between two Series
    ###

    print(corr_matrix)


def main():
    network_monitor_function()


if __name__ == "__main__":
    main()

# # Imported packages
# import os
# import numpy as np
# import pandas as pd
# from QuantLib import *
# import datetime
#
# # Network package
# import networkx as nx
#
# # Project's imports
# from pickle_obj.read_pickle_df import read_data_for_analysis
# from moduls.stock_dataframe_class import StockClass, AnalysisDatesClass


from datetime import date, timedelta


# import matplotlib.pyplot as plt
#     import networkx as nx
#     import pandas as pd
#     import yfinance as yf
# import yfinance as yf
# from datetime import date
# import tkinter as tk
# from tkinter import filedialog
#
# from datetime import *
# from QuantLib import *
#
# import matplotlib.pyplot  as plt


# Beginning of the period_app script
# if __name__ == "__main__":
#     main()


def network_function(stock_object_dictionary, ticker_list_object, important_dates):
    # construction of the headers and sub-headers of the big DF of all stocks and their market information
    header = [np.array(ticker_list_object.ticker_list),
              np.array(len(ticker_list_object.ticker_list) * ['Date_Time', 'OpenPrice', 'HighPrice',
                                                              'LowPrice', 'ClosePrice', 'AdjClose',
                                                              'Volume', 'Dividends', 'StockSplits'])]
    # setting of the number of observations used for the analysis
    obs = str(200)  # number of observations to use for the analysis
    # setting of the sub-headers array
    sub_headers = np.array(['OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice',
                            'AdjClose', 'Volume', 'Dividends', 'StockSplits'])

    # setting of the trading day
    # right now it set with the day observations of the first stock in the ticker_list_object i.e. American Express
    days = stock_object_dictionary['AXP_object'].history.index

    header = [np.array(['TimeStamp']), np.array(['Date_Time'])]
    db = pd.DataFrame(days, index=days, columns=header)

    # for cycle to clean dataset in Sql
    for i, ticker in enumerate(ticker_list_object.ticker_list):
        # construction of the header and sub-headers of the big Table/Database
        header = [np.array(len(sub_headers) * [ticker.lower()]), sub_headers]
        # converting the stock_object_dictionary history DataFrame into an array
        historical_series = np.array(stock_object_dictionary['{0}_object'.format(ticker)].history)
        # creating an adjusted df for the fetched serie to attach to the db
        adj_historical_series = pd.DataFrame(historical_series, index=days, columns=header)
        db = db.join(adj_historical_series)  # construction of the final database
    db = db.drop('TimeStamp', axis=1)
    project_root = os.path.dirname(os.path.dirname(__file__))
    db_path = project_root + '\static\data\dbFianle10days.xlsx'
    db.to_excel(db_path, index=True, header=True)

    ##############################################################################
    ### Vedi se riesci a fare una funzione per tutti questi passaggi ############
    ##############################################################################
    ### soprattutto prova a fare correlazione e segui l'andamento della stock  ###
    ############# dalla chiusura precedente all'apertura seguente ################
    ##############################################################################

    db_adj = db.filter(like='AdjClose')

    db_adj.columns = db_adj.columns.droplevel(-1)  # to drop the underlevel header

    db_adj = db_adj.apply(
        pd.to_numeric)  # to convert from object to float64 (numeric)...Otherwise I cannot apply corr function
    # oppure DataFrame.convert_dtypes(infer_objects=True, convert_string=True, convert_integer=True, convert_boolean=True)

    corr_db_adj = db_adj.corr(method='pearson')

    # corr_db_adj.describe().transpose() # for Series stats

    colheaderslist = db_adj.columns.values.tolist()

    corr_matrix = np.zeros((len(colheaderslist), len(colheaderslist)))

    # computation of log return of each stock
    # if you want there is also the method --> df['pct_change'] = df.price.pct_change()
    db_adj_lnReturndf = pd.DataFrame()
    for i, col in enumerate(colheaderslist):
        db_adj_lnReturndf[col] = np.log(db_adj[col]) - np.log(db_adj[col].shift(-1))

    """
    ## Corr Adjustment ##
    # input of a rule to choose the most fittable correlation to the model (in this case it is chosen the .7 quant)
    # to erase those correlation that do not achive the chosen threshold
    """
    for i, col in enumerate(colheaderslist):
        for j, col in enumerate(colheaderslist):
            if i != j:
                corr_matrix[i][j] = crosscorr(db_adj_lnReturndf[colheaderslist[i]],
                                              db_adj_lnReturndf[colheaderslist[j]],
                                              lag=1)  # to measure the effect of i on j
                # it is done in this way because the library networkx does (Notes: it is the opposite way of the theory of the book "Networks: An Introduction")

                # then insert the efficient performance on the lagged i.e. try different lag periods
                ### for col in db_adj.columns:
                ###     xycorr = [crosscorr(db_adj[col], db_adj[col], lag=i) for i in range(12)] # call function for lagged correlation between two Series
                ###

    print(corr_matrix)

    ticker_list_modified = list(map(str.lower, [ele.replace('.', '_') for ele in
                                                ticker_list]))  # it save the list of all retrieved tickers in lower case and
    # it replaces "." with "_"

    ddbb = pd.DataFrame(corr_matrix)  # convert corr_matrix (array) to dataframe type
    ddbb.index = ticker_list_modified  # to rename indices of the dataframe
    ddbb.columns = ticker_list_modified  # to rename columns of the dataframe

    """
    BEGINING TO BUILD THE GRAPH (NETWORK)  
    """

    # https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_directed.html

    ##for col in db_adj.columns:
    # xycorr = [crosscorr(db_adj[col], db_adj[col], lag=i) for i in range(12)] # call function for lagged correlation between two Series
    ###
    ##for col in dfdf.columns:
    ##    print(dfdf[col].iloc[:])
    # per creare il network dalla adjacency matrix
    ##A = np.array([[1, 1], [2, 1]])
    ##G = nx.from_numpy_matrix(A)
    ###

    # db['a2a_mi','OpenPrice']['2020-09-11'] # to access single elements

    # idx = pd.IndexSlice
    # db.to_excel(r'dbFinale2.xlsx', index = True)
    # db['a2a_mi','OpenPrice'].loc[idx[days[2]]]

    # ################### to access data into the dataframe #####################

    # df = pd.DataFrame({ 'Date': rng, 'Val': np.random.randn(len(rng)) })
    # finalDF22 = DateDFdf.join(adjserie)
    # idx = pd.IndexSlice

    # df['location','S1'].loc[idx['a']]

    # df.loc(axis=1)[:,'S1']
    # df['location','S1']

    # graph = nx.karate_club_graph()

    # plt.figure(figsize =(30, 30))
    # nx.draw_networkx(graph, with_labels = True)

    # writer1 = pd.ExcelWriter('nodes.xlsx', engine='xlsxwriter')
    # dfnodes = pd.DataFrame(graph.nodes())

    # dfnodes.to_excel(writer1, sheet_name='Foglio1')

    # writer2 = pd.ExcelWriter('edges.xlsx', engine='xlsxwriter')
    # dfedges = pd.DataFrame(graph.edges())

    # dfedges.to_excel(writer2, sheet_name='Foglio1')

    # writer1.save()
    # writer2.save()

    # bet_centrality = nx.betweenness_centrality(graph, normalized = True,
    #                                               endpoints = False)

    # close_centrality = nx.closeness_centrality(graph)

    # deg_centrality = nx.degree_centrality(graph)

    # # #define the ticker symbol
    # tickerSymbol = 'BET.MI'

    # # #get data on this ticker
    # tickerData = yf.Ticker(tickerSymbol)

    # # #get the historical prices for this ticker
    # tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-5-31') #‘1d’ (daily), ‘1mo’ (monthly), ‘1y’ (yearly)

    # # #see your data that is a Pandas dataframe
    # tickerDf

    # # #define the ticker symbol
    # # tickerSymbol = 'BET.MI'

    # # #get data on this ticker
    # # tickerData = yf.Ticker(tickerSymbol)

    # # #info on the company
    # tickerData.info

    # # #https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

# def main():
#     # Setting of Start date and End date of our retrieving period
#     arctic = ArcticDatesClass(start='2020-11-01', end='2020-12-01')
#     stock_object_dictionary, ticker_list_object = arctic_retrieve_function(start_date=arctic.start_date, end_date=arctic.end_date)
#     date_entry1 = input('Enter the start date for the analysis in YYYY-MM-DD format')
#     date_entry2 = input('Enter the end date for the analysis in YYYY-MM-DD format')
#     year1, month1, day1 = map(int, date_entry1.split('-'))
#     year2, month2, day2 = map(int, date_entry2.split('-'))
#     analysis = AnalysisDatesClass(start=datetime.datetime(year1,month1, day1), end=datetime.datetime(year2,month2, day2))
#
#     # Call of the network analysis function
#     network_function(stock_object_dictionary, ticker_list_object, analysis)
#
#
# # Beginning of the period_app script
# if __name__ == "__main__":
#     main()
#
