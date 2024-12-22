from development_system.classifier import Classifier
from development_system.learning_plot import LearningPlot


class LearningPlotModel:
    """Generates the report for the learning plot"""

    def __init__(self):
        """ """

    def generate_learning_report(self, classifier: Classifier):
        """ """
        learning_report = LearningPlot(classifier.get_loss_curve())
        return learning_report
