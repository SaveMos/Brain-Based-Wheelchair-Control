import numpy as np
from sklearn.neural_network import MLPClassifier

class Classifier(MLPClassifier):
    """Class representing a classifier."""

    def __init__(self):
        super(Classifier, self).__init__()
        """Initialize classifier attributes."""
        #self.num_iterations = None
        self.num_layers = None
        self.num_neurons = None
        self.training_error = None
        self.validation_error = None
        self.test_error = None
        self.early_stopping = False #it prevents the classifier to stop before the number of iterations

    def get_train_valid_error_difference(self):
        if self.get_validation_error() == 0:
            return 1
        return (self.get_validation_error() - self.get_training_error()) / self.get_validation_error()

    def get_valid_test_error_difference(self):
        if self.get_test_error() == 0:
            return 1
        return (self.get_test_error() - self.get_validation_error()) / self.get_test_error()

    # Setters and Getters

    def set_num_iterations(self, num_iterations: int):
        """Set the number of iterations."""
        self.max_iter = num_iterations      # #iterations of MLPClassifier

    def get_num_iterations(self):
        """Get the number of iterations."""
        return self.max_iter                # #iterations of MLPClassifier

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

    def set_training_error(self, training_error = 0):
        #"""Set the training error."""
        if training_error == 0:
            self.training_error = self.loss_
        else:
            self.training_error = training_error

    #def get_training_error(self):
        #"""Get the training error."""
        #return self.training_error

    def get_training_error(self):
        """Get the training error."""
        return self.loss_

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

    def classifier_report(self):
        return {'num_iterations': self.get_num_iterations(),
                'validation_error': self.get_validation_error(),
                'training_error': self.get_training_error(),
                'difference': self.get_train_valid_error_difference(),
                'num_layers': self.get_num_layers(),
                'num_neurons': self.get_num_neurons(),
                'network_complexity': self.get_num_layers() * self.get_num_neurons()
                }

    def fit(self, x, y):
        self.hidden_layer_sizes = np.full((self.num_layers,), self.num_neurons, dtype=int)
        super().fit(x, y)

    #curve to show in the learning report view
    def get_loss_curve(self):
        return self.loss_curve_