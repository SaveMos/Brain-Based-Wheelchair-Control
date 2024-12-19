from production_system.json_handler import JsonHandler
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

    def get_config_params(self):
        """
        Get the configuration parameter from json file

        """
        path = "configuration/prod_sys_conf.json"
        prod_sys_conf = JsonHandler.read_json_file(path)

        self._evaluation_phase = prod_sys_conf['evaluation_phase']

        with open(ConfigurationParameters.GLOBAL_NETCONF_PATH, "r") as global_netconf:
            data = json.load(global_netconf)
            ConfigurationParameters.PREPARATION_SYSTEM_IP = data["Preparation System"]["ip"]
            ConfigurationParameters.DEVELOP_SYSTEM_IP = data["Develop System"]["ip"]
            ConfigurationParameters.EVALUATION_SYSTEM_IP = data["Evaluation System"]["ip"]
            ConfigurationParameters.EVALUATION_SYSTEM_PORT = data["Evaluation System"]["port"]
