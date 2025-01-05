"""
    Orchestrator of production system

    Author: Alessandro Ascani
"""

import time
from production_system.configuration_parameters import ConfigurationParameters
from production_system.production_system_communication import ProductionSystemIO
from production_system.classification import Classification
from production_system.deployment import Deployment
from production_system.json_validation import JsonHandler







class ProductionOrchestrator:
    """
        Production system orchestrator.
    """
    def __init__(self, testing: bool):

        self._testing = testing

        self._configuration = ConfigurationParameters()
        self._evaluation_phase = self._configuration.parameters['evaluation_phase']
        self._prod_sys_io = ProductionSystemIO()
        self._session_counter = 0
        self._test_counter = 0




    def production(self):
        """
        Start production process.

        """
        print("Start production process")
        while True:
            # receive classifier or prepared session
            message = self._prod_sys_io.get_last_message()




            if self._testing:
                print("Send start message to service class")
                self._prod_sys_io.send_timestamp(time.time(), "start")


            handler = JsonHandler()



            #develop session
            if message['ip'] == self._configuration.DEVELOP_SYSTEM_IP :
                #deploy operation
                print("Classifier received")
                #convert json message in object class
                classifier_json = message['message']
                cl_schemas_path = "production_schema/ClassifierSchema.json"
                result = handler.validate_json(classifier_json, cl_schemas_path)
                if result is False:
                    print("classifier not valid")
                    break

                deployment = Deployment()
                deployment.deploy(classifier_json)

                if self._testing:
                    print("Send end message to Service Class")
                    self._prod_sys_io.send_timestamp(time.time(), "end")


                # send start configuration to messaging system
                print("Send start configuration")
                self._prod_sys_io.send_configuration()

                if self._testing:
                    return



            # classify session
            elif message['ip'] == self._configuration.PREPARATION_SYSTEM_IP :
                #classify operation
                print("Prepared session received")
                ps_json = message['message']
                # validation of json schema
                schemas_path = "production_schema/PreparedSessionSchema.json"
                result = handler.validate_json(ps_json, schemas_path)
                if result is False:
                    print("prepared session not valid")
                    break

                classification = Classification()
                label = classification.classify(ps_json)

                #if evaluation phase parameter is true label is sent also to Evaluation System
                if self._evaluation_phase:
                    eval_sys_ip = self._configuration.EVALUATION_SYSTEM_IP
                    eval_sys_port = self._configuration.EVALUATION_SYSTEM_PORT
                    print("Send label to evaluate session")
                    self._prod_sys_io.send_label(eval_sys_ip, eval_sys_port, label)

                # Send label to client
                serv_cl_ip = self._configuration.SERVICE_CLASS_IP
                serv_cl_port = self._configuration.SERVICE_CLASS_PORT
                print("Send label to service class")
                self._prod_sys_io.send_label(serv_cl_ip, serv_cl_port, label)

                if self._testing:
                    print("Send end message to Service Class")
                    self._prod_sys_io.send_timestamp(time.time(), "end")


                if self._evaluation_phase and self._session_counter == self._configuration.parameters['max_session_evaluation']:
                    self._session_counter = 0
                    self._evaluation_phase = False

                elif not self._evaluation_phase and self._session_counter == self._configuration.parameters['max_session_production']:
                    self._session_counter = 0
                    self._evaluation_phase = True

                if self._testing:
                    return

            else:
                print("sender unknown")
                if self._testing:
                    print("Send end message to Service Class")
                    self._prod_sys_io.send_timestamp(time.time(), "end")
                    return



if __name__ == "__main__":

    production_system_orchestrator = ProductionOrchestrator(False)
    production_system_orchestrator.production()
