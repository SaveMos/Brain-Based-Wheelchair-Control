"""
Module: ingestion_system_parameters
Loads and manages configuration parameters for the ingestion system.

Author: Francesco Taverna

"""
from ingestion_system import ING_MAN_CONFIG_FILE_PATH
from ingestion_system.ingestion_json_handler.json_handler import JsonHandler


class Parameters:
    """
    Loads and stores configuration parameters for the ingestion system.
    """

    def __init__(self):
        """
        Initialize parameters with default values or load from a configuration file.
        """

        self.missing_samples_threshold_interval = 10

        self.evaluation_phase = True #if True send label to evaluation system

        self.load_parameters()  #try to load parameters from json


    def load_parameters(self):
        """
        Load parameters from a JSON configuration file.
        """
        filepath = ING_MAN_CONFIG_FILE_PATH

        self.jsonhandler = JsonHandler() #initializing Json class
        configuration = self.jsonhandler.read_json_file(filepath) # trasforming Json to a Python dictionary

        #reading configuration parameters from dictionary
        #self.number_of_records_to_store = configuration["number_of_records_to_store"]
        self.missing_samples_threshold_interval = configuration["missing_samples_threshold_interval"]
        self.evaluation_phase = configuration["evaluation_phase"]


