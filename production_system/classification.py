"""
Author: Alessandro Ascani
"""
import joblib
import pandas as pd
from sklearn.neural_network import MLPClassifier
from production_system.label import Label
from production_system.prepared_session import PreparedSession



class Classification:
    """
     Class that managing the classifier executing the deployment and classification operation

    """
    def __init__(self):
        self._classifier: MLPClassifier or None = None



    def classify(self, prepared_session: PreparedSession):
        """
        Method that execute classify operation based on received prepared_session and classifier
        Args:
            prepared_session: prepared session that must be classified

        Returns:
            label: aN object of label class representing the label obtained from classify operation

        """

        if self._classifier is None:
            self._classifier = joblib.load("model/classifier.sav")

        # convert features in Data Frame
        features_struct = {
            'PSD_alpha_band': [prepared_session.features[0]],
            'PSD_beta_band': [prepared_session.features[1]],
            'PSD_theta_band': [prepared_session.features[2]],
            'PSD_delta_band': [prepared_session.features[3]]
        }

        features = pd.DataFrame(features_struct)

        movement = self._classifier.predict(features)
        label = Label(prepared_session.uuid, movement)

        return label

if __name__ == "__main__":
    data = {"uuid": "001", "PSD_alpha_band": 0.8, "PSD_beta_band": 0.7, "PSD_theta_band": 0.9, "PSD_delta_band": 0.6,
            "activity": 4, "environment": 2}
    features = [data["PSD_alpha_band"], data["PSD_beta_band"], data["PSD_theta_band"], data["PSD_delta_band"]]
    ps = PreparedSession(data['uuid'], features)

    instance = Classification()
    result = instance.classify(ps)
    print(result.uuid)
    print(result.movements)
