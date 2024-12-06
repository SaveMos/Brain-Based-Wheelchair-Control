from typing import List
from segregation_system.features import Features

class PreparedSession:
    """
    The `PreparedSession` class represents a prepared session for a data segregation system.

    Attributes:
        sessionID (int): The unique ID of the session.
        features (List[Features]): A list of `Features` objects representing the characteristics of the session.
        labels (List[str]): A list of labels associated with the session.
    """

    def __init__(self, sessionID: int, features: List[Features], labels: List[str]):
        """
        Initializes a new instance of the `PreparedSession` class.

        Args:
            sessionID (int): The unique ID of the session.
            features (List[Features]): A list of features associated with the session.
            labels (List[str]): A list of labels associated with the session.
        """
        self._sessionID = sessionID
        self._features = features
        self._labels = labels

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
    def features(self) -> List[Features]:
        """Returns the list of features for the session."""
        return self._features

    @features.setter
    def features(self, value: List[Features]):
        """Sets a new list of features for the session."""
        if not isinstance(value, list):
            raise ValueError("features must be a list.")
        self._features = value

    # Getter and setter for labels
    @property
    def labels(self) -> List[str]:
        """Returns the list of labels for the session."""
        return self._labels

    @labels.setter
    def labels(self, value: List[str]):
        """Sets a new list of labels for the session."""
        if not isinstance(value, list):
            raise ValueError("labels must be a list of strings.")
        if not all(isinstance(label, str) for label in value):
            raise ValueError("All elements of labels must be strings.")
        self._labels = value
