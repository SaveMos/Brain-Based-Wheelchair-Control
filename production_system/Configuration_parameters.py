from production_system.Production_system_JSONIO import ProductionSystemJSONIO
from utility.json_handler.json_handler import JsonHandler
class ConfigurationParameters:
    """
    Class that manage the configuration .
    """
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
        # l'inizializzazione tramite file json deve passare per il production JSON IO?
        path = "configuration/prod_sys_conf.json"
        prod_sys_conf = JsonHandler.read_json_file(path)

        self._evaluation_phase = prod_sys_conf['evaluation_phase']
