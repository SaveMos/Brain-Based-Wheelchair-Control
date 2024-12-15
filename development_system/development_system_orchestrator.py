from development_system.configuration_parameters import ConfigurationParameters


class DevelopmentSystemOrchestrator:
    """Orchestrates the development system process."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.testing = None
        self.develop = None
        self.config_params = ConfigurationParameters() #instance of ConfigurationParameters class

    def set_testing(self, value):
        """Set the minimum number of layers."""
        self.testing = value

    def get_testing(self):
        """Get the minimum number of layers."""
        return self.testing

    def develop(self):
        """Handle development logic."""
        pass  # Logic for development.

if __name__ == "__main__":
    orchestrator = DevelopmentSystemOrchestrator()

    # Load configurations directly from ConfigurationParameters
    orchestrator.config_params.load_configuration()
    # Test the access to loaded configuration parameters
    #print("Min Layers:", orchestrator.config_params.min_layers)
    #print("Max Layers:", orchestrator.config_params.max_layers)
    #print("Step Layers:", orchestrator.config_params.step_layers)
    #print("Min Neurons:", orchestrator.config_params.min_neurons)
    #print("Max Neurons:", orchestrator.config_params.max_neurons)
    #print("Step Neurons:", orchestrator.config_params.step_neurons)
    #print("Overfitting Tolerance:", orchestrator.config_params.overfitting_tolerance)
    #print("Generalization Tolerance:", orchestrator.config_params.generalization_tolerance)