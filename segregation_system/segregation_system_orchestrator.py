from segregation_system.balancing_report_model import BalancingReportModel
from segregation_system.balancing_report_view import BalancingReportView
from segregation_system.coverage_report_model import CoverageReportModel
from segregation_system.coverage_report_view import CoverageReportView
from segregation_system.learning_set_splitter import LearningSetSplitter
from segregation_system.segregation_system_configuration import SegregationSystemConfiguration
from segregation_system.segregation_system_database_controller import SegregationSystemDatabaseController


class SegregationSystemOrchestrator:
    """
    Orchestrates the segregation system by initializing and running its various components.

    This class is responsible for managing the overall flow of the segregation system.
    It initializes with a testing mode to determine the behavior of the system during execution
    (e.g., running in a simulated or production environment).

    Attributes:
        testing (bool): A flag indicating whether the system is in testing mode. If True,
                        the system runs in a simulated environment; otherwise, it operates in production mode.
    """

    def __init__(self, testing: bool):
        """
        Initializes the SegregationSystemOrchestrator object and runs the system.

        Args:
            testing (bool): A flag to specify if the system is in testing mode.

        Example:
            orchestrator = SegregationSystemOrchestrator(testing=True)
        """
        self.testing = testing
        self.run() # Launch the application.

    def run(self):
        """
        Executes the segregation system by loading configuration parameters and initializing components.

        This method initializes a `SegregationSystemConfiguration` object to load system parameters
        from the configuration file and sets up the required subsystems.

        Example:
            orchestrator.run()
        """
        config = SegregationSystemConfiguration()
        config.configure_parameters()  # Configure the system parameters from the file

        # receive the session from the preparation system.

        db = SegregationSystemDatabaseController("brain")

        # store the session in the database.

        # get the number of stored sessions.
        number = 10
        if number > config.minimum_number_of_collected_sessions:
            # Number sufficient.

            # get all the prepared sessions
            sessions = []

            report_model = BalancingReportModel(sessions, config) # Create the BalancingReportModel Object.
            report_model.generateBalancingReport() # Generate the Balancing Report.

            wait_for_input("Press Enter to launch the BalancingReport application...")  # Wait the user response.

            report_view = BalancingReportView()
            report_view.open_balancing_report() # Open the balancing report.

            resp = wait_for_input("Response? 'OK' or 'NOT OK'?")  # Wait the user response.
            if resp == "OK":
                report_model = CoverageReportModel(sessions)  # Create the BalancingReportModel Object.
                report_model.generateCoverageReport() # Generate the Balancing Report.

                wait_for_input("Press Enter to launch the CoverageReport application...")  # Wait the user response.

                report_view = CoverageReportView()
                report_view.open_coverage_report()  # Open the balancing report.

                resp = wait_for_input("Response? 'OK' or 'NOT OK'?")  # Wait the user response.

                if resp == "OK":
                    report_model = LearningSetSplitter()
                    learning_sets = report_model.generateLearningSets(sessions , config)

                    # send learning sets

                else:
                    # Send configuration.
                    return

            else:
                # Send configuration.
                return
        else:
            return

    # Getter for testing
    def get_testing(self) -> bool:
        """
        Retrieves the current testing mode status.

        Returns:
            bool: The current value of the testing mode flag.
        """
        return self.testing

    # Setter for testing
    def set_testing(self, testing: bool):
        """
        Updates the testing mode status.

        Args:
            testing (bool): The new value for the testing mode flag.

        Example:
            orchestrator.set_testing(False)
        """
        if not isinstance(testing, bool):
            raise ValueError("Testing mode must be a boolean value.")
        self.testing = testing


def wait_for_input(prompt: str = "Press Enter to continue or provide a value: ") -> str:
    """
    Waits for user input from the keyboard.

    Args:
        prompt (str): The message displayed to the user while waiting for input.

    Returns:
        str: The input provided by the user. Returns an empty string if no input is provided.

    Handles:
        KeyboardInterrupt: If the user presses Ctrl+C, a message is printed, and an empty string is returned.
    """
    try:
        # Display the prompt and wait for user input
        user_input = input(prompt)
        return user_input
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully and avoid crashing the program
        print("\nKeyboard interruption detected. Exiting.")
        return ""

