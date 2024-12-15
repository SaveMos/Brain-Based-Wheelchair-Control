from development_system.jsonIO import JsonHandler


class ConfigurationParameters:
    """Class representing configuration parameters."""

    def __init__(self):
        """Initialize configuration parameters with default values."""
        self.min_layers = None
        self.max_layers = None
        self.step_layers = None
        self.min_neurons = None
        self.max_neurons = None
        self.step_neurons = None
        self.overfitting_tolerance = None
        self.generalization_tolerance = None
        self.read_conf = JsonHandler()  # instance of JsonHandler class

    # Setters and Getters
    def set_min_layers(self, value):
        """Set the minimum number of layers."""
        self.min_layers = value

    def get_min_layers(self):
        """Get the minimum number of layers."""
        return self.min_layers

    def set_max_layers(self, value):
        """Set the minimum number of layers."""
        self.max_layers = value

    def get_max_layers(self):
        """Get the minimum number of layers."""
        return self.max_layers

    def set_step_layers(self, value):
        """Set the minimum number of layers."""
        self.step_layers = value

    def get_step_layers(self):
        """Get the minimum number of layers."""
        return self.step_layers
    def set_min_neurons(self, value):
        """Set the minimum number of layers."""
        self.min_neurons = value

    def get_min_neurons(self):
        """Get the minimum number of layers."""
        return self.min_neurons

    def set_max_neurons(self, value):
        """Set the minimum number of layers."""
        self.max_neurons = value

    def get_max_neurons(self):
        """Get the minimum number of layers."""
        return self.max_neurons

    def set_step_neurons(self, value):
        """Set the minimum number of layers."""
        self.step_layers = value

    def get_step_neurons(self):
        """Get the minimum number of layers."""
        return self.step_layers
    def set_overfitting_tolerance(self, value):
        """Set the minimum number of layers."""
        self.overfitting_tolerance = value

    def get_overfitting_tolerance(self):
        """Get the minimum number of layers."""
        return self.overfitting_tolerance

    def set_generalization_tolerance(self, value):
        """Set the minimum number of layers."""
        self.generalization_tolerance = value

    def get_generalization_tolerance(self):
        """Get the minimum number of layers."""
        return self.generalization_tolerance

    def load_configuration(self):
        """Load configuration parameters from a JSON file."""
        filepath = "development_parameters.json"
        params = {}
        params = self.read_conf.read_configuration_parameters(filepath)

        self.min_layers = params["min_layers"]
        self.max_layers = params["max_layers"]
        self.step_layers = params['step_layers']
        self.min_neurons = params['min_neurons']
        self.max_neurons = params['max_neurons']
        self.step_neurons = params['step_neurons']
        self.overfitting_tolerance = params['overfitting_tolerance']
        self.generalization_tolerance = params['generalization_tolerance']

