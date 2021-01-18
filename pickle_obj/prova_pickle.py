# Imported packages
import os
import pandas as pd


def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    df = pd.read_pickle(project_root + '/pickle_obj/stock_dataframes/SVA.pkl')
    print(project_root)
    print(df)
    df1 = df.loc['2020-07-19':'2021-01-15']

if __name__ == "__main__":
    main()