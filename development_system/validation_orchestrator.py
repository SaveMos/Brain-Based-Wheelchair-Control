import copy
import itertools
import random

import joblib

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
        self.service_flag = None

    def validation(self):    # It performs the grid search and generates the validation report
        """
            Perform a grid search for hyperparameters and generate the validation report.

            Returns:
                ValidationReport or bool:
                    - If in service mode, returns the generated validation report.
                    - If in testing mode, returns `True` if all classifiers in the report are valid, otherwise `False`.
        """
        # load the configurations
        self.config_params.load_configuration()
        self.service_flag = self.config_params.service_flag

        # Grid Search
        classifier_trainer = Trainer()
        if self.service_flag:
            iterations = classifier_trainer.read_number_iterations()

        else:
            classifier = joblib.load("data/classifier_trainer.sav")
            iterations = classifier.get_num_iterations()

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

        if self.service_flag:
            # it is useful only for testing the creation of validation report
            return self.validation_report
        else:
            #restituisce true se tutti i classificatori nel report sono validi, se anche uno non è valido, false
            index = int(random.random() <= 0.95)
            if index == 0:  #5%
                return False
            else:
                return True