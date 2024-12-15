class ValidationReport:
    """Class representing the validation report."""

    def __init__(self):
        """Initialize the validation report."""
        self.top_5_networks = []


    # Setters and Getters
    def set_top_5_networks(self, networks):
        """Set the top 5 networks."""
        self.top_5_networks = networks

    def get_top_5_networks(self):
        """Get the top 5 networks."""
        return self.top_5_networks