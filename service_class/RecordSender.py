
import pandas as pd
import requests

from service_class.UniqueRandomGenerator import UniqueRandomGenerator
from service_class.ServiceClassParameters import ServiceClassParameters

class RecordSender:

    def __init__(self, basedir: str = "."):
        """
        Initialize the RecordSender class by reading all the data from the CSV files.

        :param basedir: Base directory of Record Sender.
        """

        self.base_dir = basedir

        # Read the data from the CSV files
        self.calendar = RecordSender.csv_reader(f"{basedir}/../data/calendar.csv")
        self.environment = RecordSender.csv_reader(f"{basedir}/../data/environment.csv")
        self.helmet = RecordSender.csv_reader(f"{basedir}/../data/helmet.csv")
        self.labels = RecordSender.csv_reader(f"{basedir}/../data/labels.csv")

        # UniqueRandomGenerator instance
        self.unique_random_generator = UniqueRandomGenerator(0, 96)


    @staticmethod
    def csv_reader(csv_path: str):
        """
        Read a CSV file into a pandas DataFrame.

        :param csv_path: The path to the CSV file.
        :return: A pandas DataFrame containing the CSV data.
        """

        return pd.read_csv(csv_path)


    def send_session(self) -> bool:
        """
        Send a random session to the Ingestion System.

        :return: True if the session was sent successfully, False otherwise.
        """

        # Get a random index
        index = self.unique_random_generator.generate()

        calendar = self.calendar.iloc[index]
        environment = self.environment.iloc[index]
        helmet = self.helmet.iloc[index]
        label = self.labels.iloc[index]

        # Preparing the records to send
        calendar_record = {
            "source": "calendar",
            "value": calendar.to_dict()
        }
        environment_record = {
            "source": "environment",
            "value": environment.to_dict()
        }
        helmet_record = {
            "source": "helmet",
            "value": helmet.to_dict()
        }
        label_record = {
            "source": "labels",
            "value": label.to_dict()
        }

        # Send the records to the Ingestion System
        url = f"http://{ServiceClassParameters.INGESTION_SYSTEM_IP}:\
              {ServiceClassParameters.INGESTION_SYSTEM_PORT}/IngestionSystem"

        try:
            response = requests.post(url, json=calendar_record)
            if response.status_code != 200:
                return False
            response = requests.post(url, json=environment_record)
            if response.status_code != 200:
                return False
            response = requests.post(url, json=helmet_record)
            if response.status_code != 200:
                return False

            # if ServiceClassParameters.DEVELOPMENT_PHASE:
                # Label is sent only during the development phase
                # response = requests.post(url, json=label_record)
                # if response.status_code != 200:
                    # return False

            # Label has to be sent also in the evaluation phase
            response = requests.post(url, json=label_record)
            if response.status_code != 200:
                return False

        except requests.RequestException as e:
            print(f"Error sending session: {e}")
            return False
        return True


if __name__ == "__main__":
    # Test the RecordSender class
    rs = RecordSender()

