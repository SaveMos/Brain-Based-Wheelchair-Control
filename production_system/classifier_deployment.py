"""
Author: Alessandro Ascani
"""
import joblib
from production_system.classifier import Classifier

class ClassifierDeployment:
    """
    class that deploy the provided classifier .
    """
    @staticmethod
    def deploy(classifier):
        """
        Saves the provided classifier in a .sav file
        Args:
            classifier: model of classifier to save
        """
        joblib.dump(classifier, "model/classifier.sav")


if __name__ == "__main__":
    data = { "num_iteration" : 500, "num_layers": 4, "num_neurons": 30, "test_error": 5, "validation_error": 2, "training_error": 3}
    classifier = Classifier(data['num_iteration'], data['num_layers'], data['num_neurons'], data['test_error'], data['validation_error'], data['training_error'])
    instance = ClassifierDeployment()
    instance.deploy(classifier)
