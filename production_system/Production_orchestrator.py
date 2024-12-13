from production_system.Configuration_parameters import ConfigurationParameters
from production_system.Classifier_deployment import ClassifierDeployment
from production_system.Production_system_JSONIO import ProductionSystemJSONIO
from production_system.Classification import Classification


class ProductionOrchestrator:
    """
    Production system orchestrator.
    """
    def __init__(self, testing: bool):
        self._testing = testing
        self.run()

    def run(self):
        """
        Start production process.

        """
        # parameters configuration
        configuration = ConfigurationParameters()
        configuration.get_config_params()

        #receive classifier
        classifier = ProductionSystemJSONIO.receive_classifier()

        ClassifierDeployment.deploy(classifier)

        #receive prepared session
        prepared_session = ProductionSystemJSONIO.receive_prepared_session()

        #classify operation
        label = Classification.classify(prepared_session, classifier)

        #if evaluation phase parameter is true label is sent also to Evaluation System
        if configuration.evaluation_phase:
            configuration.evaluation_phase = False

            ProductionSystemJSONIO.send_label(label) #da sistemare

        # Send label to client
            ProductionSystemJSONIO.send_label(label) # da sistemare





