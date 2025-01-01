import random
import joblib

from sklearn.metrics import log_loss

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.jsonIO import JsonHandler
from development_system.test_report_model import TestReportModel
from development_system.test_report_view import TestReportView
from utility.utils import Utils


class TestingOrchestrator:
    """Orchestrator of the testing"""

    def __init__(self):
        """ """
        self.json_handler = JsonHandler()
        self.winner_network = None
        self.test_report = None
        self.test_report_model = TestReportModel()
        self.test_report_view = TestReportView()
        self.file_manager = Utils()
        ConfigurationParameters.load_configuration()
        self.service_flag: bool = ConfigurationParameters.service_flag

    def test(self):
        """
            Executes the testing phase for the classifier and generates a test report.

            This method performs several tasks in the testing phase:
            - Validates and reads necessary JSON files to determine the classifier index
              or selects one randomly.
            - Loads the classifier model and validates the test dataset schema.
            - Extracts features and labels from the test data, processes them for evaluation,
              and calculates the test error using the log loss function.
            - Generates and displays a test report.
            - Removes all saved classifiers and re-saves the winning network with the
              updated test error.
            - Depending on the `service_flag`, either returns the test report or a boolean
              indicating whether the test passed.

            Returns:
                Union[TestReport, bool]: The test report (if `service_flag` is True) or
                a boolean indicating the test result (if `service_flag` is False).
        """
        if self.service_flag:
            self.json_handler.validate_json("intermediate_results/winner_network.json", "schemas/winner_network_schema.json")
            data = self.json_handler.read_json_file("intermediate_results/winner_network.json")
            classifier_index = data["index"]
        else:
            classifier_index = random.randint(1, 5)

        self.winner_network: Classifier = joblib.load("data/classifier" + str(classifier_index ) + ".sav")


        self.json_handler.validate_json("data/test_set.json","schemas/generic_set_schema.json")
        test_data = self.json_handler.read_json_file("data/test_set.json")

        result = self.json_handler.extract_features_and_labels(test_data, "test_set")

        test_features = result[0]
        test_labels = result[1]

        true_labels = []
        for label in test_labels:
            if label == 1.0:
                true_labels.append([1.0, 0])
            else:
                true_labels.append([0, 1.0])

        self.winner_network.set_test_error(log_loss(true_labels, self.winner_network.predict_proba(test_features)))

        # GENERATE TEST REPORT
        self.test_report = self.test_report_model.generate_test_report(self.winner_network)
        print("test report generated\n")
        print("test error =", self.test_report.get_test_error())

        #remove all saved classifiers
        self.file_manager.delete_files_pattern("data/classifier*.sav")

        # save winner network (we have to save again it because, now the test_error is updated)
        joblib.dump(self.winner_network, "data/classifier.sav")

        # CHECK TEST RESULT
        self.test_report_view.show_test_report(self.test_report)


        if self.service_flag:
            # useful only for the test of the test report format
            return self.test_report
        else:
            # true if the test is passed, false otherwise
            index = int(random.random() <= 0.99)
            if index == 1:
                return True
            else:
                return False
