"""
Author: Giovanni Ligato
"""


import json
import jsonschema


class ServiceClassParameters:
    """
    This class is used to store the parameters of the Service Class.
    """

    # Local parameters
    LOCAL_PARAMETERS_PATH = "parameters/service_class_parameters.json"
    LOCAL_PARAMETERS_SCHEMA_PATH = "schemas/service_class_parameters_schema.json"
    DEVELOPMENT_PHASE = None
    DEVELOPMENT_SESSIONS = None
    PRODUCTION_SESSIONS = None
    EVALUATION_SESSIONS = None

    # Global parameters
    GLOBAL_PARAMETERS_PATH = "../global_netconf.json"
    GLOBAL_PARAMETERS_SCHEMA_PATH = "../global_netconf_schema.json"
    INGESTION_SYSTEM_IP = None
    INGESTION_SYSTEM_PORT = None
    MESSAGING_SYSTEM_PORT = None
    SERVICE_CLASS_PORT = None

    @staticmethod
    def loadParameters(basedir: str = "."):
        """
        This method is used to load the parameters of the Service Class.

        :param basedir: The base directory from which to look for the different parameters files.
        """

        try:
            with open(f"{basedir}/{ServiceClassParameters.LOCAL_PARAMETERS_PATH}", "r") as local_parameters:
                data = json.load(local_parameters)

                if ServiceClassParameters._validate_json(data, "local", basedir):
                    ServiceClassParameters.DEVELOPMENT_PHASE = data["development_phase"]
                    ServiceClassParameters.DEVELOPMENT_SESSIONS = data["development_sessions"]
                    ServiceClassParameters.PRODUCTION_SESSIONS = data["production_sessions"]
                    ServiceClassParameters.EVALUATION_SESSIONS = data["evaluation_sessions"]
                else:
                    print("Invalid local parameters.")

                with open(f"{basedir}/{ServiceClassParameters.GLOBAL_PARAMETERS_PATH}", "r") as global_parameters:
                    data = json.load(global_parameters)

                    if ServiceClassParameters._validate_json(data, "global", basedir):
                        ServiceClassParameters.INGESTION_SYSTEM_IP = data["Ingestion System"]["ip"]
                        ServiceClassParameters.INGESTION_SYSTEM_PORT = data["Ingestion System"]["port"]
                        ServiceClassParameters.MESSAGING_SYSTEM_PORT = data["Messaging System"]["port"]
                        ServiceClassParameters.SERVICE_CLASS_PORT = data["Service Class"]["port"]
                    else:
                        print("Invalid global parameters.")

        except Exception as e:
            print(f"Error loading parameters: {e}")

    # noinspection DuplicatedCode
    @staticmethod
    def _validate_json(json_parameters: dict, param_type: str, basedir: str = ".") -> bool:
        """
        Validate JSON parameters read from a file.

        :param json_parameters: The JSON parameters to validate.
        :param param_type: The type of parameters to validate (local or global).
        :param basedir: The base directory from which to look for the different parameters files.
        :return: True if the JSON parameters are valid, False otherwise.
        """

        if param_type == "local":
            schema_path = f"{basedir}/{ServiceClassParameters.LOCAL_PARAMETERS_SCHEMA_PATH}"
        elif param_type == "global":
            schema_path = f"{basedir}/{ServiceClassParameters.GLOBAL_PARAMETERS_SCHEMA_PATH}"
        else:
            return False
        
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        try:
            jsonschema.validate(json_parameters, schema)
            return True
        except jsonschema.ValidationError as e:
            if param_type == "local":
                print(f"Invalid JSON local parameters: {e}")
            elif param_type == "global":
                print(f"Invalid JSON global parameters: {e}")
            return False
