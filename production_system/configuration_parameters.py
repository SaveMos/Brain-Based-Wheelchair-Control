from jsonschema.benchmarks.useless_keywords import schema

from production_system.json_validation import JsonHandler
import json

class ConfigurationParameters:
    """
    Class that manage the configuration .
    """
    GLOBAL_NETCONF_PATH = "../global_netconf.json"
    PREPARATION_SYSTEM_IP = None
    DEVELOP_SYSTEM_IP = None
    EVALUATION_SYSTEM_IP = None
    EVALUATION_SYSTEM_PORT = None
    SERVICE_CLASS_IP = None
    SERVICE_CLASS_PORT = None
    MESSAGING_SYSTEM_IP = None
    MESSAGING_SYSTEM_PORT = None


    def __init__(self):
        self._evaluation_phase = False



    @property
    def evaluation_phase(self) -> bool:
        """
        Get the evaluation_phase parameter

        Returns:
            bool: return the value of evaluation_phase parameter
        """

        return self.evaluation_phase

    @evaluation_phase.setter
    def evaluation_phase(self, param: bool):
        """
        Set the evaluation_phase parameter
        Args:
            param: value to assign to evaluation_phase parameter

        """


        self._evaluation_phase = param

    def get_config_params(self) :
        """
        Get the configuration parameter from json file

        Returns:
            bool: True if there aren't error, False otherwise

        """
        handler = JsonHandler()
        path = "configuration/prod_sys_conf.json"
        prod_sys_conf = handler.read_json_file(path)
        schema_path = "production_schema/configSchema.json"
        if handler.validate_json(prod_sys_conf, schema_path):
            return False

        self._evaluation_phase = prod_sys_conf['evaluation_phase']

        data = handler.read_json_file(ConfigurationParameters.GLOBAL_NETCONF_PATH)
        ConfigurationParameters.PREPARATION_SYSTEM_IP = data["Preparation System"]["ip"]
        ConfigurationParameters.DEVELOP_SYSTEM_IP = data["Develop System"]["ip"]
        ConfigurationParameters.EVALUATION_SYSTEM_IP = data["Evaluation System"]["ip"]
        ConfigurationParameters.EVALUATION_SYSTEM_PORT = data["Evaluation System"]["port"]
        ConfigurationParameters.SERVICE_CLASS_IP = data["Service Class"]["ip"]
        ConfigurationParameters.SERVICE_CLASS_PORT = data["Service Class"]["port"]
        ConfigurationParameters.MESSAGING_SYSTEM_IP = data["Messaging System"]["ip"]
        ConfigurationParameters.MESSAGING_SYSTEM_PORT = data["Messaging System"]["port"]

        return True

    def start_config(self):

        configuration = {
            "configuration": "start production"
        }

        return configuration