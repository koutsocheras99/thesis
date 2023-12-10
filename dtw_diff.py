import csv
import pandas as pd
import os
import numpy as np
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis

def diff_checks(pair_level_folder, column_to_examine):
    '''
    iterate the pair folder and
    append for every pair the stocks data
    and their specfied column in order to
    be later examined
    '''
    for root, dirs, files in os.walk(pairs_folder):
        dataframes = []
        for directory in dirs:
            pair_level_folder = os.path.join(root, directory)
            # print(f"Pair folder: {pair_level_folder}") # pairs_1w/cvx_xom

            csv_files = [file for file in os.listdir(pair_level_folder) if file.endswith('.csv')]
            # print(csv_files) # ['T.csv', 'TMUS.csv', 'VZ.csv']

            # read each CSV file and extract the specified column
            for file in csv_files:
                file_path = os.path.join(pair_level_folder, file)
                df = pd.read_csv(file_path)
                dataframes.append(df[column_to_examine])


            # create a new file (if it does not already exist)
            f = open(f'{pair_level_folder}/dtw_results.txt', 'w')
            f.close()

            # perform comparisons between columns of different CSV files
            for i in range(len(dataframes)):
                for j in range(i + 1, len(dataframes)):
                    try:
                        print(f'Comparing {csv_files[i]} and {csv_files[j]}:')
                        stock_a = pd.read_csv(f'{pair_level_folder}/{csv_files[i]}', index_col=0, parse_dates = True)
                        stock_b = pd.read_csv(f'{pair_level_folder}/{csv_files[j]}', index_col=0, parse_dates = True)

                        stock_a_pct_change = stock_a[column_to_examine].dropna()
                        stock_b_pct_change = stock_b[column_to_examine].dropna()

                        # print(stock_a_pct_change)
                        # print(stock_b_pct_change)

                        distance_default_window = dtw.distance(stock_a_pct_change, stock_b_pct_change)
                        print(f' Default window {distance_default_window}')

                        # below are worst returns than above
                        # distance_20_window = dtw.distance(stock_a_pct_change, stock_b_pct_change, window=20)
                        # print(f' Window set to 20 shifts maximum {distance_20_window}')

                        # distance_20_window_with_max_step = dtw.distance(stock_a_pct_change, stock_b_pct_change, window=20, max_step=40)
                        # print(f' Window set to 20 shifts maximum with step set {distance_20_window_with_max_step}')

                        f = open(f'{pair_level_folder}/dtw_results.txt', 'a')
                        f.write(f'Comparing {csv_files[i]} and {csv_files[j]}:\n')
                        f.write(f'Dynamic Time Warping Distance: {distance_default_window} \n')
                        f.close()

                    except Exception as e: # list index out of range when only 2 pairs
                        # print(e)
                        continue


if __name__ == "__main__":
    pairs_folder = 'pairs_1w/'
    general_folder = 'sp500_1w_max_period/'

    diff_checks(pairs_folder, column_to_examine='close_pct_change')


    # pairs_folder = 'pairs_1d/'
    # general_folder = 'sp500_1d_max_period/'
