"""
Author: Saverio Mosti
Creation Date: 2024-12-06
"""
import json
import os


class SegregationSystemConfiguration:
    """
    Represents the configuration for the segregation system, including settings
    for collected sessions, tolerance intervals, and dataset percentages.

    Attributes:
        minimum_number_of_collected_sessions (int): The minimum number of collected sessions required.
        tolerance_interval (float): The tolerance interval used in calculations.
        training_set_percentage (float): The percentage of data allocated to the training set.
        validation_set_percentage (float): The percentage of data allocated to the validation set.
        number_of_training_sessions (int): The number of training sessions configured.

    Author: Saverio Mosti

    Creation Date: 2024-12-06
    """

    def __init__(self):
        self.minimum_number_of_collected_sessions = 0
        self.tolerance_interval = 0
        self.training_set_percentage = 0
        self.validation_set_percentage = 0
        self.number_of_training_sessions = 0
        self.number_of_validation_sessions = 0

    # Getter and setter for minimum_number_of_collected_sessions
    @property
    def minimum_number_of_collected_sessions(self) -> int:
        """
        Gets the minimum number of collected sessions.

        Returns:
            int: The minimum number of collected sessions.
        """
        return self.minimum_number_of_collected_sessions

    @minimum_number_of_collected_sessions.setter
    def minimum_number_of_collected_sessions(self, value: int):
        """
        Sets the minimum number of collected sessions.

        Args:
            value (int): The new minimum number of collected sessions.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("minimum_number_of_collected_sessions must be a positive integer.")
        self.minimum_number_of_collected_sessions = value

    # Getter and setter for tolerance_interval
    @property
    def tolerance_interval(self) -> float:
        """
        Gets the tolerance interval.

        Returns:
            float: The tolerance interval.
        """
        return self.tolerance_interval

    @tolerance_interval.setter
    def tolerance_interval(self, value: float):
        """
        Sets the tolerance interval.

        Args:
            value (float): The new tolerance interval.

        Raises:
            ValueError: If the value is not a positive number.
        """
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("tolerance_interval must be a positive number.")
        self.tolerance_interval = float(value)

    # Getter and setter for training_set_percentage
    @property
    def training_set_percentage(self) -> float:
        """
        Gets the percentage of data allocated to the training set.

        Returns:
            float: The training set percentage.
        """
        return self.training_set_percentage

    @training_set_percentage.setter
    def training_set_percentage(self, value: float):
        """
        Sets the percentage of data allocated to the training set.

        Args:
            value (float): The new training set percentage.

        Raises:
            ValueError: If the value is not between 0 and 100.
        """
        if not isinstance(value, (float, int)) or not 0 <= value <= 100:
            raise ValueError("training_set_percentage must be between 0 and 100.")
        self.training_set_percentage = float(value)

    # Getter and setter for validation_set_percentage
    @property
    def validation_set_percentage(self) -> float:
        """
        Gets the percentage of data allocated to the validation set.

        Returns:
            float: The validation set percentage.
        """
        return self.validation_set_percentage

    @validation_set_percentage.setter
    def validation_set_percentage(self, value: float):
        """
        Sets the percentage of data allocated to the validation set.

        Args:
            value (float): The new validation set percentage.

        Raises:
            ValueError: If the value is not between 0 and 100.
        """
        if not isinstance(value, (float, int)) or not 0 <= value <= 100:
            raise ValueError("validation_set_percentage must be between 0 and 100.")
        self.validation_set_percentage = float(value)

    # Getter and setter for number_of_training_sessions
    @property
    def number_of_training_sessions(self) -> int:
        """
        Gets the number of training sessions configured.

        Returns:
            int: The number of training sessions.
        """
        return self.number_of_training_sessions

    @number_of_training_sessions.setter
    def number_of_training_sessions(self, value: int):
        """
        Sets the number of training sessions.

        Args:
            value (int): The new number of training sessions.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("number_of_training_sessions must be a positive integer.")
        self.number_of_training_sessions = value

    def configure_parameters(self):
        """
         Initializes a new instance of the `SegregationSystemConfiguration` class.
         Loads configuration values from a default JSON file.

         Raises:
         FileNotFoundError: If the configuration file does not exist.
         KeyError: If any required key is missing in the JSON file.
         """
        # Default path to the configuration file
        file_path = "conf/segregation_system_configuration.json"

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The configuration file '{file_path}' does not exist.")

        # Load the JSON data
        with open(file_path, 'r') as json_file:
            config_data = json.load(json_file)

        # Extract and assign values to instance variables
        try:
            self.minimum_number_of_collected_sessions = config_data['minimum_number_of_collected_sessions']
            self.tolerance_interval = config_data['tolerance_interval']
            self.training_set_percentage = config_data['training_set_percentage']
            self.validation_set_percentage = config_data['validation_set_percentage']
            self.number_of_training_sessions = config_data['number_of_training_sessions']
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
