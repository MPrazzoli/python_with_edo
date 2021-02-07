from analysis.filter_for_financials import mkt_cap_filter_shsout, mkt_cap_filter_shsfloat

# Funzione per creare indici di mercato in base alla capitalizzazione per outstanding shares oppure floattante


def main():
    stock_object_dictionary, ticker_list, mkt_cap_quantiles = mkt_cap_filter_shsout(lag=180, shsout=True, num_of_quantiles=10)
    stock_object_dictionary, ticker_list, mkt_cap_quantiles = mkt_cap_filter_shsout(lag=180, shsfloat=True, num_of_quantiles=10)

    print(0)


if __name__ == '__main__':
    main()

