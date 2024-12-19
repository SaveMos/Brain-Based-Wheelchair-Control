from development_system.jsonIO import JsonHandler


class SegregationSystemConfiguration:
    """
    Represents the configuration for the segregation system, including settings
    for collected sessions, tolerance intervals, and dataset percentages.

    Author: Saverio Mosti

    Creation Date: 2024-12-19

    Attributes:
        minimum_number_of_collected_sessions (int): The minimum number of collected sessions required.
        tolerance_interval (float): The tolerance interval used in calculations.
        training_set_percentage (float): The percentage of data allocated to the training set.
        validation_set_percentage (float): The percentage of data allocated to the validation set.
        number_of_training_sessions (int): The number of training sessions configured.
    """

    def __init__(self):
        self._minimum_number_of_collected_sessions: int = 0
        self._tolerance_interval: float = 0.0
        self._training_set_percentage: float = 0.0
        self._validation_set_percentage: float = 0.0
        self._number_of_training_sessions: int = 0

    # Getter and setter for minimum_number_of_collected_sessions
    @property
    def minimum_number_of_collected_sessions(self) -> int:
        """ Gets the minimum number of collected sessions. """
        return self._minimum_number_of_collected_sessions

    @minimum_number_of_collected_sessions.setter
    def minimum_number_of_collected_sessions(self, value: int):
        """ Sets the minimum number of collected sessions. """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("minimum_number_of_collected_sessions must be a positive integer.")
        self._minimum_number_of_collected_sessions = value

    # Getter and setter for tolerance_interval
    @property
    def tolerance_interval(self) -> float:
        """ Gets the tolerance interval. """
        return self._tolerance_interval

    @tolerance_interval.setter
    def tolerance_interval(self, value: float):
        """ Sets the tolerance interval. """
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("tolerance_interval must be a positive number.")
        self._tolerance_interval = float(value)

    # Getter and setter for training_set_percentage
    @property
    def training_set_percentage(self) -> float:
        """ Gets the percentage of data allocated to the training set. """
        return self._training_set_percentage

    @training_set_percentage.setter
    def training_set_percentage(self, value: float):
        """ Sets the percentage of data allocated to the training set. """
        if not isinstance(value, (float, int)) or not 0 <= value <= 100:
            raise ValueError("training_set_percentage must be between 0 and 100.")
        self._training_set_percentage = float(value)

    # Getter and setter for validation_set_percentage
    @property
    def validation_set_percentage(self) -> float:
        """ Gets the percentage of data allocated to the validation set. """
        return self._validation_set_percentage

    @validation_set_percentage.setter
    def validation_set_percentage(self, value: float):
        """ Sets the percentage of data allocated to the validation set. """
        if not isinstance(value, (float, int)) or not 0 <= value <= 100:
            raise ValueError("validation_set_percentage must be between 0 and 100.")
        self._validation_set_percentage = float(value)

    # Getter and setter for number_of_training_sessions
    @property
    def number_of_training_sessions(self) -> int:
        """ Gets the number of training sessions configured. """
        return self._number_of_training_sessions

    @number_of_training_sessions.setter
    def number_of_training_sessions(self, value: int):
        """ Sets the number of training sessions. """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("number_of_training_sessions must be a positive integer.")
        self._number_of_training_sessions = value


    def configure_parameters(self, file_path: str = "conf/segregation_system_configuration.json") -> None:
        """
        Initializes the `SegregationSystemConfiguration` instance with configuration values from a JSON file.

        Args:
            file_path (str): The path to the JSON configuration file. Defaults to "conf/segregation_system_configuration.json".

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            KeyError: If any required key is missing in the JSON file.
            ValueError: If any value type is incorrect.
        """

        # Initialize JsonHandler to read the JSON file
        json_handler = JsonHandler()
        config_data = json_handler.read_json_file(file_path)

        # Extract and assign values to instance variables
        try:
            self.minimum_number_of_collected_sessions = int(config_data['minimum_number_of_collected_sessions'])
            self.tolerance_interval = float(config_data['tolerance_interval'])
            self.training_set_percentage = float(config_data['training_set_percentage'])
            self.validation_set_percentage = float(config_data['validation_set_percentage'])
            self.number_of_training_sessions = int(config_data['number_of_training_sessions'])
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
        except ValueError:
            raise ValueError("One or more values in the configuration file are of the wrong type.")
