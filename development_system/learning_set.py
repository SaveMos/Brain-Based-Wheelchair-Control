class LearningSet:
    """Class representing the learning set."""

    def __init__(self):
        """Initialize the learning set."""
        self.training_set = None
        self.validation_set = None
        self.test_set = None

    # Setters and Getters
    def set_training_set(self, data):
        """Set the training set."""
        self.training_set = data

    def get_training_set(self):
        """Get the training set."""
        return self.training_set

    def set_validation_set(self, data):
        """Set the validation set."""
        self.validation_set = data

    def get_validation_set(self):
        """Get the validation set."""
        return self.validation_set

    def set_test_set(self, data):
        """Set the test set."""
        self.test_set = data

    def get_test_set(self):
        """Get the test set."""
        return self.test_set