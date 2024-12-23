from production_system.label import Label
from production_system.prepared_session import PreparedSession
import joblib


class Classification:
    """
     Class that executes the classify operation

    """
    def __init__(self):
        self._classifier = None

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

        movement = self._classifier.predict(prepared_session.features)
        label = Label(prepared_session.uuid, movement)

        return label
