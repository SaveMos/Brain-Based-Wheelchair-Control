"""
Module: PreparationSystemParameters
Loads and manages configuration parameters for the preparation system.
"""
from ingestion_system.ingestion_json_handler.json_handler import JsonHandler
from preparation_system import ING_MAN_CONFIG_FILE_PATH


class PreparationSystemParameters:
    """
    Loads and stores configuration parameters for the preparation system.
    """

    def __init__(self):
        """
        Initialize parameters with default values or load from a configuration file.
        """

        self.testing = False
        self.upper_bound = 0.99
        self.lower_bound = 0.01
        self.missing_samples_correction = "interpolate"
        self.development_phase = True


    def load_parameters(self):
        """
        Load parameters from a JSON configuration file.
        """
        filepath = ING_MAN_CONFIG_FILE_PATH

        jsonhandler = JsonHandler() #initializing Json class
        configuration = jsonhandler.read_json_file(filepath) # trasforming Json to a Python dictionary

        #reading configuration parameters from dictionary
        self.development_phase = configuration["development_phase"]
        self.testing = configuration["testing"]
        self.upper_bound = configuration["upper_bound"]
        self.lower_bound = configuration["lower_bound"]
        self.missing_samples_correction = configuration["missing_samples_correction"]


