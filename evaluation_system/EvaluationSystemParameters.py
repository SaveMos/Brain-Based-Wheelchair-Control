"""
Author: Giovanni Ligato
"""


import json

class EvaluationSystemParameters:
    """
    This class is used to store the parameters of the Evaluation System.
    """

    # Local parameters
    LOCAL_PARAMETERS_PATH = "parameters/evaluation_system_parameters.json"
    MINIMUM_NUMBER_LABELS = None
    TOTAL_ERRORS = None
    MAX_CONSECUTIVE_ERRORS = None
    TESTING = None

    # Global parameters
    GLOBAL_PARAMETERS_PATH = "../global_netconf.json"
    INGESTION_SYSTEM_IP = None
    PRODUCTION_SYSTEM_IP = None
    MESSAGING_SYSTEM_IP = None
    MESSAGING_SYSTEM_PORT = None
    TESTING_SYSTEM_IP = None
    TESTING_SYSTEM_PORT = None


    @staticmethod
    def loadParameters():
        """
        This method is used to load the parameters of the Evaluation System.
        """

        try:
            with open(EvaluationSystemParameters.LOCAL_PARAMETERS_PATH, "r") as local_parameters:
                data = json.load(local_parameters)
                EvaluationSystemParameters.MINIMUM_NUMBER_LABELS = data["minimum_number_labels"]
                EvaluationSystemParameters.TOTAL_ERRORS = data["total_errors"]
                EvaluationSystemParameters.MAX_CONSECUTIVE_ERRORS = data["max_consecutive_errors"]
                EvaluationSystemParameters.TESTING = data["testing"]

            with open(EvaluationSystemParameters.GLOBAL_PARAMETERS_PATH, "r") as global_parameters:
                data = json.load(global_parameters)
                EvaluationSystemParameters.INGESTION_SYSTEM_IP = data["Ingestion System"]["ip"]
                EvaluationSystemParameters.PRODUCTION_SYSTEM_IP = data["Production System"]["ip"]
                EvaluationSystemParameters.MESSAGING_SYSTEM_IP = data["Messaging System"]["ip"]
                EvaluationSystemParameters.MESSAGING_SYSTEM_PORT = data["Messaging System"]["port"]
                EvaluationSystemParameters.TESTING_SYSTEM_IP = data["Testing System"]["ip"]
                EvaluationSystemParameters.TESTING_SYSTEM_PORT = data["Testing System"]["port"]
        except Exception as e:
            print(f"Error loading parameters: {e}")

