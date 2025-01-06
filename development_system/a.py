import time

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.json_validator_reader_and_writer import JsonValidatorReaderAndWriter
from development_system.learning_set import LearningSet
from development_system.learning_set_receiver_and_classifier_sender import LearningSetReceiverAndClassifierSender
from development_system.testing_orchestrator import TestingOrchestrator
from development_system.training_orchestrator import TrainingOrchestrator
from development_system.validation_orchestrator import ValidationOrchestrator


class DevelopmentSystemOrchestrator:
    """Orchestrates the development system process."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.service = None
        self.json_handler = JsonValidatorReaderAndWriter()
        self.dev_mess_broker = LearningSetReceiverAndClassifierSender(host='0.0.0.0',
                                                                      port=5004)  # instance of DevelopmentSystemMessageBroker class
        self.training_orchestrator = TrainingOrchestrator()
        self.validation_orchestrator = ValidationOrchestrator()
        self.testing_orchestrator = TestingOrchestrator()
        self.classifier = Classifier()
        self.learning_set = LearningSet([], [], [])
        ConfigurationParameters.load_configuration()

    def set_testing(self, value):
        """Set the service flag value.
            Args:
               value: new service flag value.
            Returns:
               None
        """
        self.service = value

    def get_testing(self):
        """Get the service flag value."""
        return self.service

    def develop(self):
        """Handle development logic."""

        json_handler = JsonValidatorReaderAndWriter()
        # Read the responses of the user for the stop and go and the value to start the continuous execution
        json_handler.validate_json("responses/user_responses.json", "schemas/user_responses_schema.json")
        user_responses = json_handler.read_json_file("responses/user_responses.json")
        # assign the value of the service flag to testing

        orchestrator.set_testing(ConfigurationParameters.params['service_flag'])
        print("Service Flag: ", self.service)

        # loop for the non-stop-and-go execution
        if self.service:
            # Create a MessageBroker instance and start the server
            # self.dev_mess_broker.start_server()
            # response = self.dev_mess_broker.send_timestamp(time.time(), "start")
            print("Start timestamp sent")
            # print("Response from Module Production System:", response)

        while True:
            # Definition of the stop&go structure
            # The user must insert only a value equal to 1 in the JSON file, the only considered value 0 is the testNotOK
            if user_responses["Start"] == 1 or user_responses["ClassifierCheck"] == 1:

                if user_responses["Start"] == 1:
                    print("Start")

                    if self.service:
                        print("waiting for learning set")
                        message = self.dev_mess_broker.rcv_learning_set()
                        if message:
                            print("Learning set received:", message)

                        learning_set = LearningSet.from_dict(JsonValidatorReaderAndWriter.string_to_dict(message['message']))

                        # save the three type of sets in a different Json file
                        self.learning_set.save_learning_set(learning_set)

                # SET AVERAGE HYPERPARAMETERS
                set_average_hyperparams = True  # in this case at the start, the average hyperparams must be set
                self.training_orchestrator.train_classifier(set_average_hyperparams)
                print("Average hyperparameters set")
                # if service flag is true, ends. If it is false, go to the next step
                if self.service:
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
                if self.service:
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
                if self.service:
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
                if self.service:
                    for key in user_responses.keys():
                        user_responses[key] = 0
                    if result:
                        user_responses["TestOK"] = 1

            elif user_responses["TestOK"] == 0:
                print("TestNotOK")
                # SEND CONFIGURATION
                if self.service:
                    print("send configuration")
                    response = self.dev_mess_broker.send_configuration()
                    print("Response from Module Messaging System:", response)
                # exit the loop
                break

            elif user_responses["TestOK"] == 1:
                print("TestOK")
                # SEND CLASSIFIER
                if self.service:
                    print("send classifier")
                    response = self.dev_mess_broker.send_classifier()
                    print("Response from Module Production System:", response)
                # exit the loop
                break

            # if testing is false, the loop must end
            if not self.service:
                break

        if self.service:
            print("End timestamp sent")
            # Create a MessageBroker instance and start the server
            # self.dev_mess_broker.start_server()
            # response = self.dev_mess_broker.send_timestamp(time.time(), "end")
            # print("Response from Module Production System:", response)


if __name__ == "__main__":
    orchestrator = DevelopmentSystemOrchestrator()
    orchestrator.develop()
