from production_system.configuration_parameters import ConfigurationParameters
from production_system.classifier_deployment import ClassifierDeployment
from production_system.production_system_jsonio import ProductionSystemJSONIO
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

        #receive classifier
        prod_sys_io = ProductionSystemJSONIO()
        classifier = prod_sys_io.receive_classifier()

        deployment = ClassifierDeployment()
        deployment.deploy(classifier)

        #receive prepared session
        prod_sys_io = ProductionSystemJSONIO()
        prepared_session = prod_sys_io.receive_prepared_session()

        #classify operation
        classification = Classification()
        label = classification.classify(prepared_session)

        #if evaluation phase parameter is true label is sent also to Evaluation System
        prod_sys_io = ProductionSystemJSONIO()
        if configuration.evaluation_phase:
            configuration.evaluation_phase = False
            prod_sys_io.send_label(label) #da sistemare

        # Send label to client
        prod_sys_io.send_label(label) # da sistemare
