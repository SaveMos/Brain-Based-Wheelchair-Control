
import sys
from production_system.json_validation import JsonHandler


class ConfigurationParameters:
    """
    Class that manage the configuration .
    """
    def __init__(self):
        GLOBAL_NETCONF_PATH = "../global_netconf.json"

        handler = JsonHandler()
        path = "configuration/prod_sys_conf.json"
        prod_sys_conf = handler.read_json_file(path)
        schema_path = "production_schema/configSchema.json"
        if handler.validate_json(prod_sys_conf, schema_path):
            print("json non valido")
            sys.exit(0)

        self.parameters = prod_sys_conf

        data = handler.read_json_file(GLOBAL_NETCONF_PATH)
        self.PREPARATION_SYSTEM_IP = data["Preparation System"]["ip"]
        self.DEVELOP_SYSTEM_IP = data["Develop System"]["ip"]
        self.EVALUATION_SYSTEM_IP = data["Evaluation System"]["ip"]
        self.EVALUATION_SYSTEM_PORT = data["Evaluation System"]["port"]
        self.SERVICE_CLASS_IP = data["Service Class"]["ip"]
        self.SERVICE_CLASS_PORT = data["Service Class"]["port"]
        self.MESSAGING_SYSTEM_IP = data["Messaging System"]["ip"]
        self.MESSAGING_SYSTEM_PORT = data["Messaging System"]["port"]


    def start_config(self):
        """

        Returns:

        """

        configuration = {
            "configuration": "production"
        }

        return configuration