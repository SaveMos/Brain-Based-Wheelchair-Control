from development_system.configuration_parameters import ConfigurationParameters
from development_system.jsonIO import JsonHandler
from development_system.test_report import TestReport


class TestReportView:
    """Shows the test report"""

    def __init__(self):
        """ """
        self.json_handler = JsonHandler()

    def show_test_report(self, test_report: TestReport):
        """ """
        report = {'generalization_tolerance': ConfigurationParameters.generalization_tolerance,
                'validation_error': test_report.get_validation_error(),
                'test_error': test_report.get_test_error(),
                'difference': test_report.get_difference(),}

        self.json_handler.write_json_file(report, "results/test_report.json")