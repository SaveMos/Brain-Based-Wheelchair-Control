from development_system.classifier import Classifier
from development_system.learning_error import LearningError


class LearningPlotModel:
    """Generates the report for the learning plot"""

    def __init__(self):
        """ """

    def generate_learning_report(self, classifier: Classifier):
        """ """
        learning_report = LearningError(classifier.get_loss_curve())
        return learning_report
