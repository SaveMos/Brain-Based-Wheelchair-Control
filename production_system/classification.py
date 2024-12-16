
import joblib


class Classification:
    """
     Class that executes the classify operation

    """
    def __init__(self):
        self._classifier = None

    def classify(self, prepared_session):
        """
        Method that execute classify operation based on received prepared_session and classifier
        Args:
            prepared_session: prepared session that must be classified
            classifier: classifier used in operation

        Returns:
            label

        """

        if self._classifier is None:
            self._classifier = joblib.load("model/classifier.sav")

        label = self._classifier.predict(prepared_session)
        return label


