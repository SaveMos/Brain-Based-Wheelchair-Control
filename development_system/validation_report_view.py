from development_system.jsonIO import JsonHandler
from development_system.validation_report import ValidationReport

class ValidationReportView:
    """Shows the validation report"""

    def __init__(self):
        """ """
        self.json_handler = JsonHandler()

    def show_validation_report(self, validation_report: ValidationReport):
        """ """
        report = {'report': validation_report.get_validation_report(),
                             'overfitting_tolerance': validation_report.get_overfitting_tolerance(),}

        self.json_handler.write_json_file(report, "results/validation_report.json")