import joblib

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
