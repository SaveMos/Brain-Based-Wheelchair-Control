import numpy as np
from sklearn.neural_network import MLPClassifier

class Classifier(MLPClassifier):
    """Class representing a classifier."""

    def __init__(self):
        super(Classifier, self).__init__()
        """Initialize classifier attributes."""
        self.num_iterations = None
        self.num_layers = None
        self.num_neurons = None
        self.training_error = None
        self.validation_error = None
        self.test_error = None

    def get_error_difference(self):
        """Calculate the error difference between validation and training."""
        return abs(self.validation_error - self.training_error)

    # Setters and Getters
    def set_num_iterations(self, value):
        """Set the number of iterations."""
        self.num_iterations = value

    def get_num_iterations(self):
        """Get the number of iterations."""
        return self.num_iterations

    def set_num_layers(self, value):
        """Set the number of layers."""
        self.num_layers = value

    def get_num_layers(self):
        """Get the number of layers."""
        return self.num_layers

    def set_num_neurons(self, value):
        """Set the number of neurons."""
        self.num_neurons = value

    def get_num_neurons(self):
        """Get the number of neurons."""
        return self.num_neurons

    def set_training_error(self, value):
        """Set the training error."""
        self.training_error = value

    def get_training_error(self):
        """Get the training error."""
        return self.training_error

    def set_validation_error(self, value):
        """Set the validation error."""
        self.validation_error = value

    def get_validation_error(self):
        """Get the validation error."""
        return self.validation_error

    def set_test_error(self, value):
        """Set the test error."""
        self.test_error = value

    def get_test_error(self):
        """Get the test error."""
        return self.test_error

    def fit(self, x, y):
        self.hidden_layer_sizes = np.full((self.num_layers,), self.num_neurons, dtype=int)
        super().fit(x, y)
