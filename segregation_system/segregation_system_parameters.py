import json
import jsonschema


from segregation_system.SegregationSystemJsonHandler import SegregationSystemJsonHandler


class SegregationSystemConfiguration:
    # Local parameters
    LOCAL_PARAMETERS_PATH = "conf/segregation_system_configuration.json"
    LOCAL_PARAMETERS_SCHEMA_PATH = "schemas/segregationSystemConfigurationSchema.json"
    LOCAL_PARAMETERS = {} # A Dict object.

    # Global parameters
    GLOBAL_PARAMETERS_PATH = "../global_netconf.json"
    GLOBAL_PARAMETERS_SCHEMA_PATH = "../global_netconf_schema.json"
    GLOBAL_PARAMETERS = {} # A Dict object.

    @staticmethod
    def configure_parameters(local_file_path = LOCAL_PARAMETERS_PATH , global_file_path = GLOBAL_PARAMETERS_PATH) -> None:
        """
        Initializes the `SegregationSystemConfiguration` instance with configuration values from a JSON file.

        Args:
            file_path (str): The path to the JSON configuration file. Defaults to "conf/segregation_system_configuration.json".

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            KeyError: If any required key is missing in the JSON file.
            ValueError: If any value type is incorrect.
        """

        # Initialize JsonHandler to read the JSON file
        json_handler = SegregationSystemJsonHandler()

        # Extract and assign values to instance variables
        try:
            SegregationSystemConfiguration.LOCAL_PARAMETERS = json_handler.read_json_file(local_file_path)
            SegregationSystemConfiguration.GLOBAL_PARAMETERS = json_handler.read_json_file(global_file_path)
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
        except ValueError:
            raise ValueError("One or more values in the configuration file are of the wrong type.")

    @staticmethod
    def validate_json(json_parameters: dict, param_type: str, basedir: str = ".") -> bool:
        """
        Validate JSON parameters read from a file.

        :param json_parameters: The JSON parameters to validate.
        :param param_type: The type of the parameters (local or global).
        :param basedir: The base directory from which to look for the different parameters files.
        :return: True if the JSON parameters are valid, False otherwise.
        """

        if param_type == "local":
            schema_path = f"{basedir}/{SegregationSystemConfiguration.LOCAL_PARAMETERS_SCHEMA_PATH}"
        elif param_type == "global":
            schema_path = f"{basedir}/{SegregationSystemConfiguration.GLOBAL_PARAMETERS_SCHEMA_PATH}"
        else:
            return False
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        try:
            jsonschema.validate(json_parameters, schema)
            return True
        except jsonschema.ValidationError as e:
            if param_type == "local":
                print(f"Invalid local parameters: {e}")
            elif param_type == "global":
                print(f"Invalid global parameters: {e}")
            return False
