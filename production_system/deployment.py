"""
Author: Alessandro Ascani
"""
import joblib
from production_system.classifier import Classifier


class Deployment:
    """
     Class that execute deployment operation
    """

    @staticmethod
    def deploy(classifier_json):
        """
        Saves the provided classifier in a .sav file
        Args:
            classifier_json: file json of classifier to save
        """
        classifier = Classifier(classifier_json['num_iteration'], classifier_json['num_layers'], classifier_json['num_neurons'],
                                classifier_json['test_error'], classifier_json['validation_error'], classifier_json['training_error'])
        joblib.dump(classifier, "model/classifier.sav")