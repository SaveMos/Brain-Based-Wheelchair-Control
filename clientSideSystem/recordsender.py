"""
Module: recordsender
Send records to ingestion system gathering them from csv files.

Author: Francesco Taverna
"""

import random
import pandas as pd


class RecordSender:
    """
    Class used to retrieve csv files with records
    Creates a list of records from different sources shuffled
    """

    def __init__(self, path: str):
        """
        Initializes the individual dataframes
        :param path: path to csv files containing the records
        """
        #list of the 4 csv files
        self.csv_files = ["calendar", "environment","helmet","labels"]
        #list to count how many records are read from each csv
        self.first_indices_to_read = [0] * len(self.csv_files)
        #total lenght of combined records
        self.original_lenght = 0

        # creates paths from csv names
        paths = []
        for csv_name in self.csv_files:
            paths.append(path + csv_name + ".csv")

        # saves all the csv in dataframes to have easy access and not open them everytime
        self.dataframes = []
        self.df_lenghs = []
        for csv_path in paths:
            #read and save in a dataframe df
            df = pd.read_csv(csv_path)
            #add to the dataframe list
            self.dataframes.append(df)
            #save the number of rows of the csv file
            self.df_lenghs.append(df.shape[0])

        #record list to save records from dataframes
        self.record_list = []

    def get_row_batch(self, max_rows: int) -> None:
        """
        gets a batch of rows from a random dataframe and adds them to the record list
        """
        # Choose a random number of rows (between 1 and max_rows)
        rand_rows = random.randint(1, max_rows)
        # Choose a random dataframe, random_file contains the index of the chosen df
        random_file = random.randint(0, len(self.dataframes) - 1)

        # checks that rand_rows is not too big:
        #minimun between random row number to read and the available readble rows
        num_rows = min(rand_rows, self.df_lenghs[random_file] - self.first_indices_to_read[random_file])

        # Iterates over the batch of rows and creates the message for the ingestion system
        #interval of rows to read:
        start_index = self.first_indices_to_read[random_file]
        end_index = start_index + num_rows #final row not included

        #iteration over dataframe rows in that interval
        for _, row in self.dataframes[random_file].iloc[start_index:end_index].iterrows():
            #convert a row to a dictionary and create a message with two values:
            #source is the csv file name from which the row is extracted
            #value is the row data as dictionary
            message = {"source": self.csv_files[random_file], "value": row.to_dict()}
            """
            example:
            [
                {
                 "source": "helmet",
                 "value": {"UUID": xxxx, "VAR2": xxxx
                 },
                 ...
            ]
            """
            #each message is added to the list
            self.record_list.append(message)

        # Update the last_row_index for the selected file
        self.first_indices_to_read[random_file] = end_index

    def prepare_record_list(self, max_rows: int) -> None:
        """
        Puts together batches from each dataframe, until all records are added
        """
        while True:
            #check if all rows in each file have been read:
            #each index has to be greater than the csv row number
            if all(x >= y for x, y in zip(self.first_indices_to_read, self.df_lenghs)):
                break
            #create messages reading rows from csv
            self.get_row_batch(max_rows)
        #total number or records read
        self.original_lenght = len(self.record_list)
        return
