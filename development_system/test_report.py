class TestReport:
    """Class representing the test report."""

    def __init__(self):
        """Initialize the test report."""
        self.winner_network = None

    # Setters and Getters
    def set_winner_network(self, network):
        """Set the winner network."""
        self.winner_network = network

    def get_winner_network(self):
        """Get the winner network."""
        return self.winner_network