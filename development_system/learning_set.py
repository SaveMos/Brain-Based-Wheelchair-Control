import json
from typing import List

import pandas as pd

from development_system.prepared_session import PreparedSession

class LearningSet:
    """
    Represents a collection of datasets used in machine learning, including
    training, validation, and test sets.

    Attributes:
        training_set (List[PreparedSession]): A list of `PreparedSession` objects used for training.
        validation_set (List[PreparedSession]): A list of `PreparedSession` objects used for validation.
        test_set (List[PreparedSession]): A list of `PreparedSession` objects used for testing.

    """

    def __init__(self,
        training_set: List[PreparedSession],
        validation_set: List[PreparedSession],
        test_set: List[PreparedSession]):
        """
        Initializes a new instance of the `LearningSet` class.

        Args:
            training_set (List[PreparedSession]): Training dataset as a list of `PreparedSession` objects.
            validation_set (List[PreparedSession]): Validation dataset as a list of `PreparedSession` objects.
            test_set (List[PreparedSession]): Test dataset as a list of `PreparedSession` objects.
        """
        self._training_set = training_set
        self._validation_set = validation_set
        self._test_set = test_set

    @staticmethod
    def extract_features_and_labels(data_set, set_type):
        """
        Extracts features and labels from a set of data.

        Args:
            data_set (dict): A dictionary which contains a set of data (ex. "test_set").
            set_type (str): Type of dictionary that contains a set.

        Returns:
            list: A list containing two elements:
                  - features (pd.DataFrame): A DataFrame with the characteristics.
                  - labels (pd.Series): Series with the labels.
        """

        activity_mapping = {"shopping": 0, "sport": 1, "cooking": 2, "relax": 3, "gaming": 4}

        environment_mapping = {"slippery": 0, "plain": 1, "slope": 2, "house": 3, "track": 4}

        current_set = data_set[set_type]

        current_data = pd.DataFrame([
            {
                "psd_alpha_band": record["psd_alpha_band"],
                "psd_beta_band": record["psd_beta_band"],
                "psd_theta_band": record["psd_theta_band"],
                "psd_delta_band": record["psd_delta_band"],
                "activity": activity_mapping.get(record["activity"], -1),  # Default value -1 if doesn't find
                "environment": environment_mapping.get(record["environment"], -1),  # Default value -1 if doesn't find
                "label": record["label"]
            }
            for record in current_set
        ])

        # Separation of the features and labels
        # features = pd.DataFrame(data["features"].to_list())
        features = current_data.drop(columns=["label"])
        labels = current_data["label"]

        return [features, labels]

    @property
    def training_set(self) -> List[PreparedSession]:
        """
        Gets the training dataset.

        Returns:
            List[PreparedSession]: The training dataset.
        """
        return self._training_set

    @training_set.setter
    def training_set(self, value: List[PreparedSession]):
        """
        Sets the training dataset.

        Args:
            value (List[PreparedSession]): A new list of `PreparedSession` objects for training.

        Raises:
            ValueError: If the input is not a list of `PreparedSession` objects.
        """
        if not isinstance(value, list) or not all(isinstance(item, PreparedSession) for item in value):
            raise ValueError("training_set must be a list of PreparedSession objects.")
        self._training_set = value

    @property
    def validation_set(self) -> List[PreparedSession]:
        """
        Gets the validation dataset.

        Returns:
            List[PreparedSession]: The validation dataset.
        """
        return self._validation_set

    @validation_set.setter
    def validation_set(self, value: List[PreparedSession]):
        """
        Sets the validation dataset.

        Args:
            value (List[PreparedSession]): A new list of `PreparedSession` objects for validation.

        Raises:
            ValueError: If the input is not a list of `PreparedSession` objects.
        """
        if not isinstance(value, list) or not all(isinstance(item, PreparedSession) for item in value):
            raise ValueError("validation_set must be a list of PreparedSession objects.")
        self._validation_set = value

    @property
    def test_set(self) -> List[PreparedSession]:
        """
        Gets the test dataset.

        Returns:
            List[PreparedSession]: The test dataset.
        """
        return self._test_set

    @test_set.setter
    def test_set(self, value: List[PreparedSession]):
        """
        Sets the test dataset.

        Args:
            value (List[PreparedSession]): A new list of `PreparedSession` objects for testing.

        Raises:
            ValueError: If the input is not a list of `PreparedSession` objects.
        """
        if not isinstance(value, list) or not all(isinstance(item, PreparedSession) for item in value):
            raise ValueError("test_set must be a list of PreparedSession objects.")
        self._test_set = value


    @staticmethod
    def create_learning_set_from_json(json_file_path: str):
        """
        Converts a JSON file to a LearningSet object.

        Args:
            json_file_path (str): Path to the JSON file containing the data.

        Returns:
            LearningSet: An instance of the LearningSet class populated with the data from the JSON file.

        Raises:
            FileNotFoundError: If the JSON file does not exist.
            KeyError: If required keys are missing in the JSON data.
            ValueError: If the data types do not match the expected structure.
        """
        try:
            # Carica i dati dal file JSON
            with open(json_file_path, 'r') as file:
                current_data = json.load(file)
        except FileNotFoundError as ex:
            raise FileNotFoundError(f"File not found: {ex}")
        except json.JSONDecodeError as ex:
            raise ValueError(f"Error decoding JSON: {ex}")

        # Converti ciascun set nel JSON in una lista di oggetti PreparedSession
        training_set = [PreparedSession.from_dictionary(session) for session in current_data.get('training_set', [])]
        validation_set = [PreparedSession.from_dictionary(session) for session in
                          current_data.get('validation_set', [])]
        test_set = [PreparedSession.from_dictionary(session) for session in current_data.get('test_set', [])]

        # Crea e restituisci l'oggetto LearningSet
        return LearningSet(training_set=training_set, validation_set=validation_set, test_set=test_set)


    @staticmethod
    def save_learning_set(learning_set):
        """
        Saves the training, validation, and test sets of a LearningSet instance to JSON files.

        Args:
            learning_set (LearningSet): An instance containing training, validation, and test sets.

        Returns:
            None
        """
        # Converte i dati utilizzando il metodo to_dictionary
        training_data = [session.to_dictionary() for session in learning_set.training_set]
        validation_data = [session.to_dictionary() for session in learning_set.validation_set]
        test_data = [session.to_dictionary() for session in learning_set.test_set]

        # Salva i dati nei rispettivi file JSON
        with open('data/training_set.json', 'w') as f:
            json.dump({"training_set": training_data}, f, indent=4)

        with open('data/validation_set.json', 'w') as f:
            json.dump({"validation_set": validation_data}, f, indent=4)

        with open('data/test_set.json', 'w') as f:
            json.dump({"test_set": test_data}, f, indent=4)

