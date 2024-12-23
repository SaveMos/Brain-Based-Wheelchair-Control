"""
    Orchestrator of production system

    Author: Alessandro Ascani
"""
import sys
import json

from production_system.configuration_parameters import ConfigurationParameters
from production_system.classifier_deployment import ClassifierDeployment
from production_system.production_system_communication import ProductionSystemIO
from production_system.classification import Classification
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
        self._classification = Classification()

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
                deployment = ClassifierDeployment()
                deployment.deploy(classifier)

                # send start configuration to messaging system
                print("Send start configuration")
                msg_sys_ip = self._configuration.MESSAGING_SYSTEM_IP
                msg_sys_port = self._configuration.MESSAGING_SYSTEM_PORT
                config = self._configuration.start_config()
                self._prod_sys_io.send_message(msg_sys_ip, msg_sys_port, config)

            elif message['ip'] == "Preparation" :
                #classify operation
                print("Prepared session received")
                prepared_session_json = message['message']
                # validation of json schema
                schemas_path = "production_schema/PreparedSessionSchema.json"
                result = handler.validate_json(prepared_session_json, schemas_path)
                if result is False:
                    continue

                #convert prepared session json in python object
                prepared_session = PreparedSession(prepared_session_json['uuid'], prepared_session_json['features'])

                label = self._classification.classify(prepared_session)

                #convert label into json
                label_dict = label.to_dictionary()

                label_json = json.dumps(label_dict)


                #if evaluation phase parameter is true label is sent also to Evaluation System
                if self._configuration.evaluation_phase:
                    eval_sys_ip = ConfigurationParameters.EVALUATION_SYSTEM_IP
                    eval_sys_port = ConfigurationParameters.EVALUATION_SYSTEM_PORT
                    print("Send label to evaluate session")
                    self._prod_sys_io.send_message(eval_sys_ip, eval_sys_port, label_json)

                # Send label to client
                serv_cl_ip = ConfigurationParameters.SERVICE_CLASS_IP
                serv_cl_port = ConfigurationParameters.SERVICE_CLASS_PORT
                print("Send label to service class")
                self._prod_sys_io.send_message(serv_cl_ip, serv_cl_port, label_json)
