class LearningPlot:
    """Class representing the learning plot."""

    def __init__(self):
        """Initialize learning plot parameters."""
        self.max_number_iterations = None
        self.mse = []  # Mean squared error for each iteration.

    # Setters and Getters
    def set_max_number_iterations(self, value):
        """Set the maximum number of iterations."""
        self.max_number_iterations = value

    def get_max_number_iterations(self):
        """Get the maximum number of iterations."""
        return self.max_number_iterations

    def set_mse(self, mse_list):
        """Set the mean squared error list."""
        self.mse = mse_list

    def get_mse(self):
        """Get the mean squared error list."""
        return self.mse