import joblib

from development_system.classifier import Classifier


class TestReport:
    """Class representing the test report."""

    def __init__(self):
        """Initialize the test report."""
        self.generalization_tolerance = None
        self.validation_error = None
        self.test_error = None
        self.difference = None

    # Getter and Setter for generalization_tolerance
    def set_generalization_tolerance(self, generalization_tolerance):
        """Set the generalization tolerance."""
        self.generalization_tolerance = generalization_tolerance

    def get_generalization_tolerance(self):
        """Get the generalization tolerance."""
        return self.generalization_tolerance

    # Getter and Setter for validation_error
    def set_validation_error(self, validation_error):
        """Set the validation error."""
        self.validation_error = validation_error

    def get_validation_error(self):
        """Get the validation error."""
        return self.validation_error

    # Getter and Setter for test_error
    def set_test_error(self, test_error):
        """Set the test error."""
        self.test_error = test_error

    def get_test_error(self):
        """Get the test error."""
        return self.test_error

    # Getter and Setter for difference
    def set_difference(self, difference):
        """Set the difference."""
        self.difference = difference

    def get_difference(self):
        """Get the difference."""
        return self.difference