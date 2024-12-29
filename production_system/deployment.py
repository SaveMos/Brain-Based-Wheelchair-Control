"""
Author: Alessandro Ascani
"""
import joblib


class Deployment:
    """
     Class that execute deployment operation
    """

    @staticmethod
    def deploy(classifier):
        """
        Saves the provided classifier in a .sav file
        Args:
            classifier: model of classifier to save
        """
        joblib.dump(classifier, "model/classifier.sav")