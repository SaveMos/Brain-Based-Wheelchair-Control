from development_system.jsonIO import JsonHandler


class ValidationReportView:
    """Shows the validation report"""

    def __init__(self):
        """ """
        self.json_handler = JsonHandler()

    def show_validation_report(self, validation_report):
        """ """
        self.json_handler.write_json_file(validation_report, "results/validation_report.json")