from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters


class TestReportModel:
    """Generates the report for the test"""

    def __init__(self):
        """ """
        self.config_params = ConfigurationParameters()

    def generate_test_report(self, classifier: Classifier):
        """ """
        self.config_params.load_configuration()
        return {'generalization_tolerance': ConfigurationParameters.generalization_tolerance,
                'validation_error': classifier.get_validation_error(),
                'test_error': classifier.get_test_error(),
                'difference': classifier.get_valid_test_error_difference()}