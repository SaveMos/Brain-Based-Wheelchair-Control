import pandas as pd
import random
import copy


class RecordDispenser:
    """
    Class used to retrieve csv files with records
    Creates a list of records from different sources shuffled
    """

    def __init__(self, csv_files: list, path: str):
        """
        Initializes the individual dataframes
        :param csv_files: list of csv files containing the records
        """
        self.csv_files = csv_files
        self.first_indices_to_read = [0] * len(self.csv_files)
        self.original_lenght = 0

        # creates paths from csv names
        paths = []
        for csv_name in self.csv_files:
            paths.append(path + csv_name + ".csv")

        # saves all the csv in dataframes to have easy access and not open them everytime
        self.dataframes = []
        self.df_lenghs = []
        for csv_path in paths:
            df = pd.read_csv(csv_path)
            self.dataframes.append(df)
            self.df_lenghs.append(df.shape[0])

        self.record_list = []
        return

    def get_row_batch(self, max_rows: int) -> None:
        """
        gets a batch of rows from a random dataframe and adds them to the record list
        """
        # Choose a random number of rows (between 1 and 10)
        rand_rows = random.randint(1, max_rows)
        random_file = random.randint(0, len(self.dataframes) - 1)

        # checks that rand_rows is not too big
        num_rows = min(rand_rows, self.df_lenghs[random_file] - self.first_indices_to_read[random_file])

        # Iterates over the batch of rows and creates the message for the ingestion system
        start_index = self.first_indices_to_read[random_file]
        end_index = start_index + num_rows
        for _, row in self.dataframes[random_file].iloc[start_index:end_index].iterrows():
            message = {"source": self.csv_files[random_file], "value": row.to_dict()}
            self.record_list.append(message)

        # Update the last_row_index for the selected file
        self.first_indices_to_read[random_file] = end_index
        return

    def prepare_record_list(self, max_rows: int) -> None:
        """
        Puts together batches from each dataframe, until all records are added
        """
        while True:
            if all(x >= y for x, y in zip(self.first_indices_to_read, self.df_lenghs)):
                break
            self.get_row_batch(max_rows)

        self.original_lenght = len(self.record_list)

    def extend_list(self) -> None:
        """
        Extends the list with new ids (The lenght added is the original one to avoid conflicts on id)
        """
        #get last element UUID
        last_uuid = self.record_list[len(self.record_list) - 1]["value"]["UUID"]

        # Split the UUID string into prefix and suffix
        prefix, suffix = last_uuid.split('-', 1)

        # Increment the numerical part of the prefix
        new_prefix = 'a' + str(int(prefix[1:]) + 1)

        new_list = []

        for i in range(self.original_lenght):
            copied_dict = copy.deepcopy(self.record_list[i])

            # Split the UUID string into prefix and suffix
            prefix, suffix = copied_dict["value"]["UUID"].split('-', 1)

            # Concatenate the parts back together
            new_uuid_string = new_prefix + '-' + suffix
            copied_dict["value"]["UUID"] = new_uuid_string

            new_list.append(copied_dict)

        self.record_list.extend(new_list)

