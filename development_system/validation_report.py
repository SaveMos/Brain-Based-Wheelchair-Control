class ValidationReport:
    """Class representing the validation report."""

    def __init__(self):
        """Initialize the validation report."""
        self.top_5_networks = []

    def get_top_5_networks(self):
        """Get the top 5 networks."""
        return self.top_5_networks