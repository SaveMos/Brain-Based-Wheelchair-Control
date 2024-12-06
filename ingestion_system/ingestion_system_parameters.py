"""
Module: ingestion_system_parameters
Loads and manages configuration parameters for the ingestion system.
"""

import json

class IngestionSystemParameters:
    """
    Loads and stores configuration parameters for the ingestion system.
    """

    # Default parameters
    number_of_records_to_store = 4
    missing_samples_threshold_interval = 2
    evaluation_phase = False

    @staticmethod
    def load_parameters(filepath="config.json"):
        """
        Load parameters from a JSON configuration file.

        Args:
            filepath (str): Path to the configuration file. Defaults to 'config.json'.
        """
        try:
            with open(filepath, "r") as file:
                config = json.load(file)
                IngestionSystemParameters.number_of_records_to_store = config.get("number_of_records_to_store", 4)
                IngestionSystemParameters.missing_samples_threshold_interval = config.get(
                    "missing_samples_threshold_interval", 2
                )
                IngestionSystemParameters.evaluation_phase = config.get("evaluation_phase", False)
        except FileNotFoundError:
            print("Configuration file not found. Using default parameters.")
