from cgitb import handler

from production_system.configuration_parameters import ConfigurationParameters
from production_system.classifier_deployment import ClassifierDeployment
from production_system.production_system_communication import ProductionSystemIO
from production_system.classification import Classification
from production_system.json_handler import JsonHandler
from production_system.classifier import Classifier
from production_system.label import Label
import sys
import json

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



    def run(self):
        """
        Start production process.

        """

        while True:
            # receive classifier or prepared session
            message = self._prod_sys_io.get_last_message()
            handler = JsonHandler()


            if message['ip'] == "Develop" :

                msg_json = message['message']
                classifier = Classifier(msg_json['num_iteration'], msg_json['num_layers'], msg_json['num_neurons'], msg_json['test_error'], msg_json['validation_error'], msg_json['training_error'])
                deployment = ClassifierDeployment()
                deployment.deploy(classifier)

            elif message['ip'] == "Preparation" :
                #classify operation
                prepared_session_json = message['message']
                schemas_path = "production_schema/PreparedSessionSchema.json"
                result = handler.validate_json(prepared_session_json, schemas_path)
                if result is False:
                    continue

                #convert prepared session json in python object
                prepared_session = PreparedSession(prepared_session_json['uuid'], prepared_session_json['features'])

                label = self._classification.classify(prepared_session)

                #convert label into json
                label_dict = {
                    'uuid': label.uuid,
                    'movement': label.movements
                }

                label_json = json.dumps(label_dict)


                #if evaluation phase parameter is true label is sent also to Evaluation System
                if self._configuration.evaluation_phase:
                    target_ip = ConfigurationParameters.EVALUATION_SYSTEM_IP
                    target_port = ConfigurationParameters.EVALUATION_SYSTEM_PORT
                    self._prod_sys_io.send_message(target_ip, target_port, label_json)

                # Send label to client
                #prod_sys_io.send_message(label)
