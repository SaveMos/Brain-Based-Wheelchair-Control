from development_system import training_orchestrator
from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.jsonIO import JsonHandler
from development_system.development_system_message_broker import DevelopmentSystemMessageBroker
from development_system.learning_plot_model import LearningPlotModel
from development_system.learning_plot_view import LearningPlotView
from development_system.training_orchestrator import TrainingOrchestrator
from development_system.validation_orchestrator import ValidationOrchestrator


class DevelopmentSystemOrchestrator:
    """Orchestrates the development system process."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.testing = None
        self.json_handler = JsonHandler()
        self.config_params = ConfigurationParameters() #instance of ConfigurationParameters class
        #self.dev_mess_broker = DevelopmentSystemMessageBroker()  # instance of DevelopmentSystemMessageBroker class
        self.training_orchestrator = TrainingOrchestrator()
        self.validation_orchestrator = ValidationOrchestrator()
        self.classifier = Classifier()

        #self.plot_model = LearningPlotModel()
        #self.plot_view = LearningPlotView()

    def set_testing(self, value):
        """Set the minimum number of layers."""
        self.testing = value

    def get_testing(self):
        """Get the minimum number of layers."""
        return self.testing

    def develop(self):
        """Handle development logic."""

        json_handler = JsonHandler()
        # Read the responses of the user for the stop and go
        user_responses = json_handler.read_json_file("responses/user.json")
        print("Start: ", user_responses["Start"])

        # Definition of the stop&go structure
        # The user must insert only a value equal to 1 in the JSON file, the only considered value 0 is the testNotOK
        if user_responses["Start"] == 1:
            print("Start")
            # Load configurations directly from ConfigurationParameters
            self.config_params.load_configuration()
            # Test the access to loaded configuration parameters
            print("Min Layers:", orchestrator.config_params.min_layers)

            # Create a MessageBroker instance and start the server
            # dev_mess_broker = DevelopmentSystemMessageBroker(host='0.0.0.0', port=5002)
            # dev_mess_broker.start_server()

            # message = dev_mess_broker.rcv_learning_set()
            # if message:
            # print("Message received:", message)

            # Simulation of the reception of the learning set, to change in future
            json_handler1 = JsonHandler()

            learning_set = json_handler1.create_learning_set_from_json("intermediate_results/dataset_split.json")


            # SET AVERAGE HYPERPARAMETERS
            set_average_hyperparams = True #in this case at the start, the average hyperparams must be setted
            self.training_orchestrator.train_classifier(set_average_hyperparams)
            # stop for setting #iterations

        elif user_responses["ClassifierCheck"] == 1:
            print("ClassifierCheck")
            # SET AVERAGE HYPERPARAMETERS
            # stop for setting #iterations
        elif user_responses["IterationCheck"] == 1:
            print("IterationCheck")
            # set_num_iterations   (questo probabilmente rimosso, train() legge direttamente il json)
            # TRAIN
                # GENERATE LEARNING REPORT
                # CHECK LEARNING PLOT
            set_average_hyperparams = False  # in this case, the average hyperparams are already setted
            self.training_orchestrator.train_classifier(set_average_hyperparams)

        elif user_responses["Validation"] == 1:
            print("Validation")
            # SET HYPERPARAMETERS (loop)
            # TRAIN               (loop)
                # GENERATE VALIDATION REPORT
                # CHECK VALIDATION RESULT
            self.validation_orchestrator.validation()

        elif user_responses["GenerateTest"] == 1:
            print("GenerateTest")
            # GENERATE TEST REPORT
            # CHECK TEST RESULT
        elif user_responses["TestOK"] == 0:
            print("TestNotOK")
            # SEND CONFIGURATION
        elif user_responses["TestOK"] == 1:
            print("TestOK")
            # send classifier

if __name__ == "__main__":

    orchestrator = DevelopmentSystemOrchestrator()
    orchestrator.develop()
