"""
Author: Alessandro Ascani
"""

class Label:
    """
    Data Object class to represent a Label created in Production System.
    """

    def __init__(self, uuid: str, movements: int):
        """
        Initialize the Label with uuid and movements fields.

        Args:
            uuid (str): The unique identifier for the label.
            movements (int): Integer label associated to the movements.
        """
        self._uuid = uuid
        self._movements = movements

    @property
    def uuid(self) -> str:
        """
        Get the uuid of the label.

        Returns:
            str: The uuid of the label.
        """
        return self._uuid

    @uuid.setter
    def uuid(self, value: str):
        """
        Set the uuid of the label.

        Args:
            value (str): The new uuid of the label.
        """
        self._uuid = value

    @property
    def movements(self) -> int:
        """
        Get the movements label.

        Returns:
            int: The movements label.
        """
        return self._movements

    @movements.setter
    def movements(self, value: int):
        """
        Set the movements label.

        Args:
            value (int): The new movements label.
        """
        self._movements = value
