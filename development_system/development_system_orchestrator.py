from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.jsonIO import JsonHandler
from development_system.label_receiver_and_classifier_sender import LabelReceiverAndClassifierSender
from development_system.testing_orchestrator import TestingOrchestrator
from development_system.training_orchestrator import TrainingOrchestrator
from development_system.validation_orchestrator import ValidationOrchestrator

class DevelopmentSystemOrchestrator:
    """Orchestrates the development system process."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.testing = None
        self.json_handler = JsonHandler()
        self.config_params = ConfigurationParameters() #instance of ConfigurationParameters class
        #self.dev_mess_broker = DevelopmentSystemMessageBroker(host='0.0.0.0', port=5002)  # instance of DevelopmentSystemMessageBroker class
        self.training_orchestrator = TrainingOrchestrator()
        self.validation_orchestrator = ValidationOrchestrator()
        self.testing_orchestrator = TestingOrchestrator()
        self.classifier = Classifier()


    def set_testing(self, value):
        """Set the service flag value.
            Args:
               value: new service flag value.
            Returns:
               None
        """
        self.testing = value

    def get_testing(self):
        """Get the service flag value."""
        return self.testing

    def develop(self):
        """Handle development logic."""

        json_handler = JsonHandler()
        # Read the responses of the user for the stop and go and the value to start the continuous execution
        json_handler.validate_json("responses/user_responses.json", "schemas/user_responses_schema.json")
        user_responses = json_handler.read_json_file("responses/user_responses.json")
        #load the configurations and assign the value of the service flag to testing
        self.config_params.load_configuration()
        orchestrator.set_testing(self.config_params.service_flag)
        print("Service Flag: ", self.testing)
        #loop for the non-stop-and-go execution
        while True:

            # Definition of the stop&go structure
            # The user must insert only a value equal to 1 in the JSON file, the only considered value 0 is the testNotOK
            if user_responses["Start"] == 1 or user_responses["ClassifierCheck"] == 1:


                if user_responses["Start"] == 1:
                    print("Start")

                    # Create a MessageBroker instance and start the server
                    # self.dev_mess_broker.start_server()

                    # message = self.dev_mess_broker.rcv_learning_set()
                    # if message:
                    # print("Message received:", message)

                    # Simulation of the reception of the learning set, to change in future
                    json_handler1 = JsonHandler()
                    json_handler1.validate_json("intermediate_results/dataset_split.json", "schemas/dataset_split_schema.json")
                    # returns a learning set object read from a Json file
                    learning_set = json_handler1.create_learning_set_from_json("intermediate_results/dataset_split.json")
                    #print the sets received
                    #json_handler1.print_learning_set(learning_set)
                    # save the three type of sets in a different Json file
                    json_handler1.save_learning_set(learning_set)

                # SET AVERAGE HYPERPARAMETERS
                set_average_hyperparams = True #in this case at the start, the average hyperparams must be set
                self.classifier = self.training_orchestrator.train_classifier(set_average_hyperparams)
                print("Average hyperparameters set")
                #if service flag is true, ends. If it is false, go to the next step
                if not orchestrator.get_testing():
                    for key in user_responses.keys():
                        user_responses[key] = 0
                    user_responses["IterationCheck"] = 1

            elif user_responses["IterationCheck"] == 1:
                print("Iteration Check Phase")
                # SET NUMBER ITERATIONS
                # TRAIN
                    # GENERATE LEARNING REPORT
                    # CHECK LEARNING PLOT
                set_average_hyperparams = False  # in this case, the average hyperparams are already set
                self.training_orchestrator.train_classifier(set_average_hyperparams)
                print("Number of iterations set")
                # if the testing is false, go to the validation phase
                if not orchestrator.get_testing():
                    for key in user_responses.keys():
                        user_responses[key] = 0
                    user_responses["Validation"] = 1

            elif user_responses["Validation"] == 1:
                print("Validation phase")
                # SET HYPERPARAMETERS (loop)
                # TRAIN               (loop)
                    # GENERATE VALIDATION REPORT
                    # CHECK VALIDATION RESULT
                result = self.validation_orchestrator.validation()
                print("Validation phase done")
                # if the testing is false and the validation is correct, go to the test phase.
                # if the testing is false and the validation is not correct, go at the beginning.
                if not orchestrator.get_testing():
                    for key in user_responses.keys():
                        user_responses[key] = 0
                    if result:
                        user_responses["GenerateTest"] = 1
                    else:
                        user_responses["ClassifierCheck"] = 1

            elif user_responses["GenerateTest"] == 1:
                print("Test phase")
                # GENERATE TEST REPORT
                # CHECK TEST RESULT
                result = self.testing_orchestrator.test()
                print("Test phase done")
                # if the testing is false and the test is correct, send the classifier to production system.
                # if the testing is false and the test is not correct, send the configuration to messaging system.
                if not orchestrator.get_testing():
                    for key in user_responses.keys():
                        user_responses[key] = 0
                    if result:
                        user_responses["TestOK"] = 1

            elif user_responses["TestOK"] == 0:
                print("TestNotOK")
                # SEND CONFIGURATION

                # Retrieve ip address and port of the target system
                self.json_handler.validate_json("../global_netconf.json", "../global_netconf_schema.json")
                endpoint = self.json_handler.get_system_address("../global_netconf.json", "Production System")

                # Create a MessageBroker instance and start the server
                #self.dev_mess_broker.start_server()
                #self.response = dev_mess_broker.send_configuration(target_ip=endpoint["ip"], target_port=endpoint["port"])
                #self.print("Response from Module Production System:", response)
                # exit the loop
                break

            elif user_responses["TestOK"] == 1:
                print("TestOK")
                # SEND CLASSIFIER

                # Retrieve ip address and port of the target system
                self.json_handler.validate_json("../global_netconf.json", "../global_netconf_schema.json")
                endpoint = self.json_handler.get_system_address("../global_netconf.json", "Production System")

                # Create a MessageBroker instance and start the server
                #self.dev_mess_broker.start_server()
                #response = self.dev_mess_broker.send_classifier(target_ip=endpoint["ip"], target_port=endpoint["port"], classifier_file="data/classifier.sav")
                #print("Response from Module Production System:", response)
                # exit the loop
                break

            # if testing is true, the loop must end
            if self.testing:
                break


if __name__ == "__main__":

    orchestrator = DevelopmentSystemOrchestrator()
    orchestrator.develop()
