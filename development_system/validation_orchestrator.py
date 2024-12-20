import copy
import itertools

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.trainer import Trainer
from development_system.validation_report_model import ValidationReportModel
from development_system.validation_report_view import ValidationReportView


class ValidationOrchestrator:
    """Orchestrator of the validation"""

    def __init__(self):
        """ """
        self.classifiers = []
        self.validation_report = None
        self.validation_report_model = ValidationReportModel()
        self.validation_report_view = ValidationReportView()
        self.config_params = ConfigurationParameters()

    def validation(self):    # It performs the grid search and generates the validation report
        """ """
        # Grid Search
        classifier_trainer = Trainer()
        iterations = classifier_trainer.read_number_iterations()
        #classifier_trainer.set_num_iterations(num_iterations)

        #load the configurations
        self.config_params.load_configuration()

        # Compute all possible combinations of hyperparameters
        layers = []

        for i in range(ConfigurationParameters.min_layers, ConfigurationParameters.max_layers + 1,
                       ConfigurationParameters.step_layers):
            layers.append(i)

        neurons = []

        for i in range(ConfigurationParameters.min_neurons, ConfigurationParameters.max_neurons + 1,
                       ConfigurationParameters.step_neurons):
            neurons.append(i)

        grid_search = list(itertools.product(layers, neurons))

        for (num_layers, num_neurons) in grid_search:
            # SET HYPERPARAMETERS
            classifier_trainer.set_hyperparameters(num_layers, num_neurons)
            # TRAIN
            classifier = classifier_trainer.train(iterations, validation=True)
            #append the clasifier into the classifiers list
            self.classifiers.append(copy.deepcopy(classifier))

        # GENERATE VALIDATION REPORT
        self.validation_report =  self.validation_report_model.generate_validation_report(self.classifiers)

        print("validation report =", self.validation_report)
        # CHECK VALIDATION RESULT
        self.validation_report_view.show_validation_report(self.validation_report)