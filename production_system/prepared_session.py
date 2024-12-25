"""
 Author: Alessandro Ascani
"""
from typing import List



class PreparedSession:
    """
        Data object class to represent the prepared session used by production system
    """
    def __init__(self, uuid: str, features: List[float]):
        self._uuid = uuid
        self._features = features

    @property
    def uuid(self) -> str:
        """
        Get the uuid of the prepared session.

        Returns:
            str: The uuid of the prepared session.
        """
        return self._uuid

    @uuid.setter
    def uuid(self, value: str):
        """
        Set the uuid of the prepared session.

        Args:
            value (str): The new uuid of the prepared session.
        """
        self._uuid = value

    @property
    def features(self) -> List[float]:
        """
        Get the features of prepared session.

        Returns:
            List[float]: The features.
        """
        return self._features

    @features.setter
    def features(self, value: List[float]):
        """
        Set the movements label.

        Args:
            value (List[float]): The new list of features.
        """
        self._features = value

if __name__ == "__main__":
    data = {"uuid": "001", "PSD_alpha_band": 1.5, "PSD_beta_band": 0.5, "PSD_theta_band": 0.25, "PSD_delta_band": 2.25, "activity": 4, "enviroment": 2}
    features = [data["PSD_alpha_band"], data["PSD_beta_band"], data["PSD_theta_band"], data["PSD_delta_band"], data["activity"], data["enviroment"]]
    ps = PreparedSession(data['uuid'], features)
    print(ps.uuid)
    print(ps.features)
