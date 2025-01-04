"""
Module: PreparationSystemParameters
Loads and manages configuration parameters for the preparation system.

Author: Francesco Taverna

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
        self.sampling_frequency = 100.0
        self.development_phase = True
        self.bandwidths = {
                             "psd_alpha_band": [8, 12],
                             "psd_beta_band": [12, 30],
                             "psd_theta_band": [1, 4],
                             "psd_delta_band": [4, 8]
                          }


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
        self.sampling_frequency = configuration["sampling_frequency"]
        self.bandwidths = configuration["bandwidths"]


