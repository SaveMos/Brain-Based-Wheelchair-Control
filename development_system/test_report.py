import joblib

from development_system.classifier import Classifier


class TestReport:
    """Class representing the test report."""

    def __init__(self, classifier_index):
        """Initialize the test report."""
        #self.winner_network = None
        self.winner_network: Classifier = joblib.load("data/classifier" + str(classifier_index) + ".sav")

    # Setters and Getters
    def set_winner_network(self, network):
        """Set the winner network."""
        self.winner_network = network

    def get_winner_network(self):
        """Get the winner network."""
        return self.winner_network