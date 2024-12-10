"""
Author: Saverio Mosti
Creation Date: 2024-12-06
"""


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

    def __init__(self,
                 minimum_number_of_collected_sessions: int,
                 tolerance_interval: float,
                 training_set_percentage: float,
                 validation_set_percentage: float,
                 number_of_training_sessions: int):
        """
        Initializes a new instance of the `SegregationSystemConfiguration` class.

        Args:
            minimum_number_of_collected_sessions (int): Minimum number of collected sessions.
            tolerance_interval (float): Tolerance interval for the system.
            training_set_percentage (float): Percentage for training set.
            validation_set_percentage (float): Percentage for validation set.
            number_of_training_sessions (int): Number of training sessions.
        """
        self._minimum_number_of_collected_sessions = minimum_number_of_collected_sessions
        self._tolerance_interval = tolerance_interval
        self._training_set_percentage = training_set_percentage
        self._validation_set_percentage = validation_set_percentage
        self._number_of_training_sessions = number_of_training_sessions

    # Getter and setter for minimum_number_of_collected_sessions
    @property
    def minimum_number_of_collected_sessions(self) -> int:
        """
        Gets the minimum number of collected sessions.

        Returns:
            int: The minimum number of collected sessions.
        """
        return self._minimum_number_of_collected_sessions

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
        self._minimum_number_of_collected_sessions = value

    # Getter and setter for tolerance_interval
    @property
    def tolerance_interval(self) -> float:
        """
        Gets the tolerance interval.

        Returns:
            float: The tolerance interval.
        """
        return self._tolerance_interval

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
        self._tolerance_interval = float(value)

    # Getter and setter for training_set_percentage
    @property
    def training_set_percentage(self) -> float:
        """
        Gets the percentage of data allocated to the training set.

        Returns:
            float: The training set percentage.
        """
        return self._training_set_percentage

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
        self._training_set_percentage = float(value)

    # Getter and setter for validation_set_percentage
    @property
    def validation_set_percentage(self) -> float:
        """
        Gets the percentage of data allocated to the validation set.

        Returns:
            float: The validation set percentage.
        """
        return self._validation_set_percentage

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
        self._validation_set_percentage = float(value)

    # Getter and setter for number_of_training_sessions
    @property
    def number_of_training_sessions(self) -> int:
        """
        Gets the number of training sessions configured.

        Returns:
            int: The number of training sessions.
        """
        return self._number_of_training_sessions

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
        self._number_of_training_sessions = value

    def configure_parameters(self,
                             min_sessions: int,
                             tolerance: float,
                             training_percentage: float,
                             validation_percentage: float,
                             training_sessions: int):
        """
        Configures the parameters of the segregation system.

        Args:
            min_sessions (int): Minimum number of collected sessions.
            tolerance (float): Tolerance interval.
            training_percentage (float): Training set percentage.
            validation_percentage (float): Validation set percentage.
            training_sessions (int): Number of training sessions.
        """
        self.minimum_number_of_collected_sessions = min_sessions
        self.tolerance_interval = tolerance
        self.training_set_percentage = training_percentage
        self.validation_set_percentage = validation_percentage
        self.number_of_training_sessions = training_sessions
