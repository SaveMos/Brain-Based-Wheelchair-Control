"""
Author: Giovanni Ligato
"""


import json
import jsonschema


class EvaluationSystemParameters:
    """
    This class is used to store the parameters of the Evaluation System.
    """

    # Local parameters
    LOCAL_PARAMETERS_PATH = "parameters/evaluation_system_parameters.json"
    LOCAL_PARAMETERS_SCHEMA_PATH = "schemas/evaluation_system_parameters_schema.json"
    MINIMUM_NUMBER_LABELS = None
    TOTAL_ERRORS = None
    MAX_CONSECUTIVE_ERRORS = None
    TESTING = None

    # Global parameters
    GLOBAL_PARAMETERS_PATH = "../global_netconf.json"
    GLOBAL_PARAMETERS_SCHEMA_PATH = "../global_netconf_schema.json"
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

                if EvaluationSystemParameters._validate_json(data, "local"):
                    EvaluationSystemParameters.MINIMUM_NUMBER_LABELS = data["minimum_number_labels"]
                    EvaluationSystemParameters.TOTAL_ERRORS = data["total_errors"]
                    EvaluationSystemParameters.MAX_CONSECUTIVE_ERRORS = data["max_consecutive_errors"]
                    EvaluationSystemParameters.TESTING = data["testing"]
                else:
                    print("Invalid local parameters.")

            with open(EvaluationSystemParameters.GLOBAL_PARAMETERS_PATH, "r") as global_parameters:
                data = json.load(global_parameters)

                if EvaluationSystemParameters._validate_json(data, "global"):
                    EvaluationSystemParameters.INGESTION_SYSTEM_IP = data["Ingestion System"]["ip"]
                    EvaluationSystemParameters.PRODUCTION_SYSTEM_IP = data["Production System"]["ip"]
                    EvaluationSystemParameters.MESSAGING_SYSTEM_IP = data["Messaging System"]["ip"]
                    EvaluationSystemParameters.MESSAGING_SYSTEM_PORT = data["Messaging System"]["port"]
                    EvaluationSystemParameters.TESTING_SYSTEM_IP = data["Testing System"]["ip"]
                    EvaluationSystemParameters.TESTING_SYSTEM_PORT = data["Testing System"]["port"]
                else:
                    print("Invalid global parameters.")

        except Exception as e:
            print(f"Error loading parameters: {e}")

    def _validate_json(self, json_parameters: Dict, type: str) -> bool:
        """
        Validate JSON parameters read from a file.

        :param json_parameters: The JSON parameters to validate.
        :param type: The type of the parameters (local or global).
        :return: True if the JSON parameters are valid, False otherwise.
        """

        if type == "local":
            schema_path = EvaluationSystemParameters.LOCAL_PARAMETERS_SCHEMA_PATH
        elif type == "global":
            schema_path = EvaluationSystemParameters.GLOBAL_PARAMETERS_SCHEMA_PATH
        else:
            return False

        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        try:
            jsonschema.validate(json_parameters, schema)
            return True
        except jsonschema.ValidationError as e:
            if type == "local":
                print(f"Invalid local parameters: {e}")
            elif type == "global":
                print(f"Invalid global parameters: {e}")
            return False
