from production_system.configuration_parameters import ConfigurationParameters
from production_system.classifier_deployment import ClassifierDeployment
from production_system.production_system_io import ProductionSystemIO
from production_system.classification import Classification


class ProductionOrchestrator:
    """
    Production system orchestrator.
    """
    def __init__(self, testing: bool):
        self._testing = testing
        self.run()

    @staticmethod
    def run():
        """
        Start production process.

        """
        # parameters configuration
        configuration = ConfigurationParameters()
        configuration.get_config_params()

        # receive classifier or prepared session
        prod_sys_io = ProductionSystemIO()
        sender, message = prod_sys_io.get_last_message()

        if sender == "Develop" :
            classifier = message
            deployment = ClassifierDeployment()
            deployment.deploy(classifier)

        elif sender == "Preparation" :
            #classify operation
            prepared_session = message
            classification = Classification()
            label = classification.classify(prepared_session)

        #if evaluation phase parameter is true label is sent also to Evaluation System
        prod_sys_io = ProductionSystemIO()
        if configuration.evaluation_phase:
            configuration.evaluation_phase = False
            target_ip = ConfigurationParameters.EVALUATION_SYSTEM_IP
            target_port = ConfigurationParameters.EVALUATION_SYSTEM_PORT
            prod_sys_io.send_message(target_ip, target_port, label)

        # Send label to client
        #prod_sys_io.send_message(label) # da sistemare
