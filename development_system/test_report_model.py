from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.test_report import TestReport


class TestReportModel:
    """Generates the report for the test"""

    def __init__(self):
        """ """
        self.config_params = ConfigurationParameters()

    def generate_test_report(self, classifier: Classifier):
        """ """
        self.config_params.load_configuration()
        test_report = TestReport()
        test_report.set_generalization_tolerance(ConfigurationParameters.generalization_tolerance)
        test_report.set_validation_error(classifier.get_validation_error())
        test_report.set_test_error(classifier.get_test_error())
        test_report.set_difference(classifier.get_valid_test_error_difference())
        print("difference = ", test_report.get_difference())
        return test_report

        #return {'generalization_tolerance': ConfigurationParameters.generalization_tolerance,
        #        'validation_error': classifier.get_validation_error(),
        #        'test_error': classifier.get_test_error(),
        #        'difference': classifier.get_valid_test_error_difference()}