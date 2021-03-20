# Imported packages
import os
import pandas as pd


def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    all_data_df = pd.read_pickle(project_root + '/_3_pickle_obj/_3^1_stock_dataframes/AAPL.pkl')
    print(all_data_df.head(5))
    print(all_data_df.loc['2020-12-01':'2021-03-05'])
    df_filtered = all_data_df.loc['2020-07-19':'2025-01-15']

if __name__ == "__main__":
    main()































































































