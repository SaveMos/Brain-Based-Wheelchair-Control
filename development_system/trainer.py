import math

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters

class Trainer:
    """Class responsible for training a classifier."""

    def __init__(self):
        """Initialize trainer parameters."""
        self.classifier = Classifier()


    def set_number_iterations(self):
        """Set the number of iterations."""

    def set_average_hyperparameters(self):
        """Set the average hyperparameters."""
        avg_neurons = math.ceil((ConfigurationParameters.max_neurons + ConfigurationParameters.min_neurons) / 2)
        avg_layers = math.ceil((ConfigurationParameters.max_layers + ConfigurationParameters.min_layers) / 2)
        print("avg_neurons: ", avg_neurons)
        self.classifier.set_num_neurons(avg_neurons)
        self.classifier.set_num_layers(avg_layers)

    def set_hyperparameters(self):
        """Set the average hyperparameters."""

    def train(self):
        """Train the classifier."""