"""
Author: Saverio Mosti
Creation Date: 2024-12-06
"""

from typing import List

class PreparedSession:
    """
    The `PreparedSession` class represents a prepared session for a data segregation system.

    Attributes:
        sessionID (int): The unique ID of the session.
        features (List[Features]): A list of `Features` objects representing the characteristics of the session.
        labels (str): The label associated with the prepared session.
    Author: Saverio Mosti

    Creation Date: 2024-12-06
    """

    def __init__(self, sessionID: int, features: List[float], label : str):
        """
        Initializes a new instance of the `PreparedSession` class.

        Args:
            sessionID (int): The unique ID of the session.
            features (List[Features]): A list of features associated with the session.
            label (str): A label associated with the session.
        """
        self._sessionID = sessionID
        self._features = features
        self._labels = label

    # Getter and setter for sessionID
    @property
    def sessionID(self) -> int:
        """Returns the session ID."""
        return self._sessionID

    @sessionID.setter
    def sessionID(self, value: int):
        """Sets a new value for the session ID."""
        if not isinstance(value, int):
            raise ValueError("sessionID must be an integer.")
        self._sessionID = value

    # Getter and setter for features
    @property
    def features(self) -> List[float]:
        """Returns the list of features for the session."""
        return self._features

    @features.setter
    def features(self, value: List[float]):
        """Sets a new list of features for the session."""
        if not isinstance(value, list):
            raise ValueError("features must be a list.")
        self._features = value

    # Getter and setter for labels
    @property
    def label(self) -> str:
        """Returns the list of labels for the session."""
        return self._labels

    @label.setter
    def label(self, value: str):
        """Sets a new list of labels for the session."""
        self._labels = value

    def from_dict(self, data: dict):
        """
        Take the values from a dictionary and put them into the Object.

        Args:
            data (dict): A dictionary containing keys `sessionID`, `features`, and `label`.

        Returns:
            Nothing.

        Raises:
            KeyError: If required keys are missing in the dictionary.
            ValueError: If the data types of values do not match the expected types.
        """
        try:
            self._sessionID = data['sessionID']
            self._features = data['features']
            self._labels = data['label']
        except KeyError as e:
            raise KeyError(f"Missing key in input dictionary: {e}")

        # Validate the types
        if not isinstance(self._session_id, int):
            raise ValueError("sessionID must be an integer.")
        if not isinstance(self._features, list) or not all(isinstance(f, (float, int)) for f in features):
            raise ValueError("features must be a list of numbers.")
        if not isinstance(self._label, str):
            raise ValueError("label must be a string.")

    def to_dictionary(self) -> dict:
        """
        Converts the `PreparedSession` object into a dictionary.

        Returns:
            dict: A dictionary representation of the `PreparedSession` object,
            with keys `sessionID`, `features`, and `label`.
        """
        return {
            'sessionID': self._sessionID,
            'features': self._features,
            'label': self._labels
        }

