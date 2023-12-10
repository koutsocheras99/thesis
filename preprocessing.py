from datetime import datetime, time
import pandas as pd
import csv
import os
import shutil

def transfer_stock_data_to_pair_folders(pairs_folder, general_folder):
    '''
    copy the stock csv files from the general folder
    directory (sp500_1w_max_period/) to their specific 
    pairs folder (pairs_1w/cvx_xom/)
    '''
    for root, dirs, files in os.walk(pairs_folder):
        for directory in dirs:
            list_of_pair_stocks_uppercase = [stock.upper() for stock in directory.split('_')]
            # print(f"Folder name: {directory}")
            # print(f"Split names: {list_of_pair_stocks_uppercase}")
            for symbol in list_of_pair_stocks_uppercase:
                source_file_path = os.path.join(general_folder, f"{symbol}.csv")
                # print(source_file_path)
                if os.path.exists(source_file_path):
                    destination_file_path = os.path.join(f"{pairs_folder}/{directory}", f"{symbol}.csv")
                    shutil.copy(source_file_path, destination_file_path)
                    print(f"File '{symbol}.csv' copied successfully.")
                else:
                    print(f"File '{symbol}.csv' not found in {general_folder}")


def keep_only_oldest_common_dates(pair_level_folder, oldest_common_starting_date_in_the_pair):
    '''
    read the csv files inside the pair folder
    compare the lines with the oldest common date
    and keep only the common dates
    '''
    for stock_file in os.listdir(pair_level_folder):
        # read the content of the file
        with open(pair_level_folder+"/"+stock_file, 'r') as csvfile:
            lines = csvfile.readlines()
            first_line = [lines[0]]  # keep the first line
            # from the second line (not the header) and below compare the dates
            filtered_lines = [line for line in lines[1:] if datetime.strptime(line.split(',')[0].split()[0], "%Y-%m-%d") >= oldest_common_starting_date_in_the_pair]

        # write the filtered lines back to the file
        with open(pair_level_folder+"/"+stock_file, 'w') as csvfile:
            csvfile.writelines(first_line)
            csvfile.writelines(filtered_lines)


def retrieve_oldest_common_start_date_between_a_pair(pair_level_folder):
    '''
    inside the pair folder
    check the first row/column of each pair csv file
    and get the oldest common date
    '''
    oldest_start_dates_list = []
    for stock_file in os.listdir(pair_level_folder):
        if os.path.isfile(os.path.join(pair_level_folder, stock_file)):
            # print(f"CSV stock file inside the pair folder: {stock_file}") # CVX.csv, XOM.csv

            with open(pair_level_folder+"/"+stock_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # skip the header row
                first_row = next(reader)  # get the first row after the header

                # print(first_row[0])
                date_string = first_row[0]
                date_object = datetime.strptime(date_string.split()[0], '%Y-%m-%d')
                oldest_start_dates_list.append(date_object)

    oldest_common_starting_date_in_a_pair = max(oldest_start_dates_list)
    keep_only_oldest_common_dates(pair_level_folder, oldest_common_starting_date_in_a_pair)
    # print(oldest_start_dates_list)
    # print(oldest_common_starting_date_in_a_pair)

    print(f"The older common start date between pair in folder {pair_level_folder} has been retrieved successfully.\n")


def retrieve_oldest_common_start_date_between_all_pairs(pairs_folder):
    for root, dirs, files in os.walk(pairs_folder):
        for directory in dirs:
            pair_level_folder = os.path.join(root, directory)
            # print(f"Pair folder: {pair_level_folder}") # pairs_1w/cvx_xom
            retrieve_oldest_common_start_date_between_a_pair(pair_level_folder)

    print("The older common start date between all pairs has been retrieved successfully.\n")


def apply_percentage_changes_to_columns(pairs_folder):
    for root, dirs, files in os.walk(pairs_folder):
        for directory in dirs:
            pair_level_folder = os.path.join(root, directory)
            for stock_file in os.listdir(pair_level_folder):
                df = pd.read_csv(pair_level_folder+"/"+stock_file)
                df[['open_pct_change', 'high_pct_change', 'low_pct_change', 'close_pct_change']] = df[['Open', 'High', 'Low', 'Close']].pct_change().mul(100)
                df.to_csv(pair_level_folder+"/"+stock_file, index=False)

    print("Percentage change columns have been added successfully.\n")


if __name__ == "__main__":
    pairs_folder = 'pairs_1w/'
    general_folder = 'sp500_1w_max_period/'

    # pairs_folder = 'pairs_1d/'
    # general_folder = 'sp500_1d_max_period/'

    transfer_stock_data_to_pair_folders(pairs_folder, general_folder)
    retrieve_oldest_common_start_date_between_all_pairs(pairs_folder)
    apply_percentage_changes_to_columns(pairs_folder)

    '''
    for root, dirs, files in os.walk(pairs_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
    print("CSV files deleted in the folder:", pairs_folder)
    '''