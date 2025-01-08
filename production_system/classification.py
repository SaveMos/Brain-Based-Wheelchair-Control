"""
Author: Alessandro Ascani
"""
import joblib
import pandas as pd
from sklearn.neural_network import MLPClassifier
from production_system.label import Label




class Classification:
    """
     Class that managing the classifier executing the deployment and classification operation

    """
    def __init__(self):
        self._classifier: MLPClassifier or None = None



    def classify(self, prepared_session):
        """
        Method that execute classify operation based on received prepared_session and classifier
        Args:
            prepared_session: prepared session that must be classified

        Returns:
            label: aN object of label class representing the label obtained from classify operation

        """

        # convert prepared session json in python object
        if self._classifier is None:
            self._classifier = joblib.load("model/classifier.sav")

        label_mapping = {"turnRight":0, "turnLeft":1, "move":2}
        environment_mapping = {"slippery":0, "plain":1, "slope":2, "house":3, "track":4}
        activity_mapping = {"shopping":0, "sport":1, "cooking":2, "relax":3, "gaming":4}

        # convert features in Data Frame
        features_struct = {
            'PSD_alpha_band': prepared_session['PSD_alpha_band'],
            'PSD_beta_band': prepared_session['PSD_beta_band'],
            'PSD_theta_band': prepared_session['PSD_theta_band'],
            'PSD_delta_band': prepared_session['PSD_delta_band'],
            'activity': activity_mapping.get(prepared_session['activity']),
            'environment': environment_mapping.get(prepared_session['environment']),
            'label': label_mapping.get(prepared_session['label'])
        }

        features_DF = pd.DataFrame([features_struct])

        movement = self._classifier.predict(features_DF)
        print(movement)
        label = Label(prepared_session['uuid'], movement)


        return label


