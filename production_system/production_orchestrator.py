"""
    Orchestrator of production system

    Author: Alessandro Ascani
"""
import sys
from production_system.configuration_parameters import ConfigurationParameters
from production_system.production_system_communication import ProductionSystemIO
from production_system.classifier_controller import ClassifierController
from production_system.json_validation import JsonHandler
from production_system.classifier import Classifier
from production_system.prepared_session import PreparedSession






class ProductionOrchestrator:
    """
        Production system orchestrator.
    """
    def __init__(self, testing: bool):

        self._testing = testing

        self._configuration = ConfigurationParameters()
        self._prod_sys_io = ProductionSystemIO()
        self._classifier_controller = ClassifierController()

        # configure parameters
        result = self._configuration.get_config_params()

        # json isn't valid
        if result is False:
            sys.exit(0)



    def production(self):
        """
        Start production process.

        """

        while True:
            # receive classifier or prepared session
            message = self._prod_sys_io.get_last_message()
            handler = JsonHandler()


            if message['ip'] == "Develop" :
                #deploy operation
                print("Classifier received")
                #convert json message in object class
                msg_json = message['message']
                classifier = Classifier(msg_json['num_iteration'], msg_json['num_layers'], msg_json['num_neurons'], msg_json['test_error'], msg_json['validation_error'], msg_json['training_error'])
                self._classifier_controller.deploy(classifier)

                # send start configuration to messaging system
                print("Send start configuration")
                config = self._configuration.start_config()
                self._prod_sys_io.send_configuration(config)

            elif message['ip'] == "Preparation" :
                #classify operation
                print("Prepared session received")
                ps_json = message['message']
                # validation of json schema
                schemas_path = "production_schema/PreparedSessionSchema.json"
                result = handler.validate_json(ps_json, schemas_path)
                if result is False:
                    continue

                ps_features = [ps_json['psd_alpha_band'], ps_json['psd_beta_band'], ps_json['psd_tetha_band'], ps_json['psd_delta_band'], ps_json['activity'], ps_json['environment']]
                #convert prepared session json in python object
                prepared_session = PreparedSession(ps_json['uuid'], ps_features)

                label = self._classifier_controller.classify(prepared_session)

                #if evaluation phase parameter is true label is sent also to Evaluation System
                if self._configuration.evaluation_phase:
                    eval_sys_ip = ConfigurationParameters.EVALUATION_SYSTEM_IP
                    eval_sys_port = ConfigurationParameters.EVALUATION_SYSTEM_PORT
                    print("Send label to evaluate session")
                    self._prod_sys_io.send_label(eval_sys_ip, eval_sys_port, label)

                # Send label to client
                serv_cl_ip = ConfigurationParameters.SERVICE_CLASS_IP
                serv_cl_port = ConfigurationParameters.SERVICE_CLASS_PORT
                print("Send label to service class")
                self._prod_sys_io.send_label(serv_cl_ip, serv_cl_port, label)

if __name__ == "__main__":
    prod = ProductionOrchestrator(False)
    prod.production()
