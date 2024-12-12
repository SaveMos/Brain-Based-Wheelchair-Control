
from utility.json_handler.json_handler import JsonHandler

class ProductionOrchestrator:
    """
    Production system orchestrator.
    """
    def __init__(self):
        self.configuration_parameters = JsonHandler.read_json_file()

    def run(self):
        """
        Start production process.
        """



