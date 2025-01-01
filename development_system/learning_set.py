from typing import List
from segregation_system.prepared_session import PreparedSession

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
