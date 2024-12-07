
from configuration_parameters import ConfigurationParameters

class ProductionOrchestrator:
    """
    Production system orchestrator.
    """
    def __init__(self):
        self.configuration_parameters = ConfigurationParameters()

    def run(self):
        """
        Start production process.
        """
        self.configuration_parameters.configure_parameters("example_parameters")


