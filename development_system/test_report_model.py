from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.test_report import TestReport


class TestReportModel:
    """Generates the report for the test"""

    def __init__(self):
        """ """

    @staticmethod
    def generate_test_report(classifier: Classifier):
        """
            Generates a test report for the given classifier.

            This method configures the system, retrieves the relevant metrics from the
            provided classifier, and creates a `TestReport` instance populated with these values.
            It also prints the difference between validation and test errors for reference.

            Args:
                classifier (Classifier): An instance of a classifier that provides
                validation and test error metrics.

            Returns:
                TestReport: An instance of `TestReport` containing the generalization
                tolerance, validation error, test error, and the difference between
                validation and test errors.
        """

        # the configurations are loaded only in case of stop and go
        #if ConfigurationParameters.params is None:
            #ConfigurationParameters.load_configuration()

        test_report = TestReport()
        test_report.set_generalization_tolerance(ConfigurationParameters.params['generalization_tolerance'])
        test_report.set_validation_error(classifier.get_validation_error())
        test_report.set_test_error(classifier.get_test_error())
        test_report.set_difference(classifier.get_valid_test_error_difference())
        return test_report