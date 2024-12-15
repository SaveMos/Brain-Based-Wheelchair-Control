

class EvaluationSystemParameters:
    """
    This class is used to represent the configuration parameters of the Evaluation System.
    """
    MAX_CONSECUTIVE_ERRORS = None
    MAX_ERRORS = None
    MIN_LABELS = None
    SERVICE_FLAG = None
    EVALUATION_IP = None
    EVALUATION_PORT = None
    MESSAGING_IP = None
    MESSAGING_PORT = None
    SERVICE_IP = None
    SERVICE_PORT = None

    # Inserire anche Indirizzi IP e porte di Ingestion e Production Systems
    # TODO
    INGESTION_SYSTEM_IP = None
    PRODUCTION_SYSTEM_IP = None

    @staticmethod
    def initialize_config_params():
        """
        This method is used to initialize the configuration parameters. It's a static method
        and all the attributes initialized are static.
        """
        eval_sys_io = EvaluationJsonIO.get_instance()
        json_params, json_global_params = eval_sys_io.recv_config_params()

        ConfigurationParameters.MAX_ERRORS = json_params['MAX_ERRORS']
        ConfigurationParameters.MAX_CONSECUTIVE_ERRORS = json_params['MAX_CONSECUTIVE_ERRORS']
        ConfigurationParameters.MIN_LABELS = json_params['MIN_LABELS']
        ConfigurationParameters.SERVICE_FLAG = json_params['SERVICE_FLAG']
        ConfigurationParameters.EVALUATION_IP = json_global_params['Evaluation System']['ip']
        ConfigurationParameters.EVALUATION_PORT = json_global_params['Evaluation System']['port']
        ConfigurationParameters.MESSAGING_IP = json_global_params['Messaging System']['ip']
        ConfigurationParameters.MESSAGING_PORT = json_global_params['Messaging System']['port']
        ConfigurationParameters.SERVICE_IP = json_global_params['Service Class']['ip']
        ConfigurationParameters.SERVICE_PORT = json_global_params['Service Class']['port']