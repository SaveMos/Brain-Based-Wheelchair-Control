from development_system.jsonIO import JsonHandler


class TestReportView:
    """Shows the test report"""

    def __init__(self):
        """ """
        self.json_handler = JsonHandler()

    def show_test_report(self, test_report):
        """ """
        self.json_handler.write_json_file(test_report, "results/test_report.json")