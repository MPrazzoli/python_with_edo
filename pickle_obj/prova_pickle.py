# Imported packages
import os
import pandas as pd


def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    all_data_df = pd.read_pickle(project_root + '/pickle_obj/stock_dataframes/AAPL.pkl')
    print(project_root)
    print(all_data_df)
    # df_filtered = all_data_df.loc['2020-07-19':'2021-01-15']

if __name__ == "__main__":
    main()