from segregation_system.balancing_report_model import BalancingReportModel
from segregation_system.coverage_report_model import CoverageReportModel
from segregation_system.learning_set_splitter import LearningSetSplitter
from segregation_system.prepared_session import PreparedSession
from segregation_system.segregation_system_configuration import SegregationSystemConfiguration
from segregation_system.segregation_system_database_controller import SegregationSystemDatabaseController

from utility.json_handler.json_handler import JsonHandler
from utility.message_broker.message_broker import MessageBroker


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
        self.testing = testing  # Set the testing attribute.
        self.run()  # Launch the application.

    def run(self):
        """
        Executes the segregation system by loading configuration parameters and initializing components.

        This method initializes a `SegregationSystemConfiguration` object to load system parameters
        from the configuration file and sets up the required subsystems.

        Example:
            orchestrator.run()
        """
        json_handler = JsonHandler()
        execution_state_file_path = "data/execution_state_file.json"

        number_of_session_status = json_handler.read_field_from_json(execution_state_file_path, "number_of_collected_sessions")
        balancing_report_status = json_handler.read_field_from_json(execution_state_file_path, "balancing_report")
        coverage_report_status = json_handler.read_field_from_json(execution_state_file_path, "coverage_report")

        if number_of_session_status != "OK" or balancing_report_status != "OK"or self.get_testing():
            # The first phase must be done.

            # Create a Configuration object, to load the system configuration.
            config = SegregationSystemConfiguration()
            # Configure the system parameters from the configuration file.
            config.configure_parameters()

            # Create a MessageBroker instance to send and receive messages.
            message_broker = MessageBroker()

            new_prepared_session = PreparedSession(0, [], "")
            # Receive the prepared session from the preparation system, and cast it into a PreparedSession object.
            new_prepared_session.from_dict(message_broker.get_last_message())

            # Create an instance of database controller.
            db = SegregationSystemDatabaseController()

            # Store the new prepared session in the database.
            db.store_prepared_session(new_prepared_session.to_dictionary())

            # OPTIMIZATION
            # If the check has already been passed, it is not necessary to do another read from the database.
            if number_of_session_status == "OK":
                # Assign the minimum number to pass the test.
                number_of_prepared_sessions_stored = config.minimum_number_of_collected_sessions
            else:
                # Get the number of stored prepared sessions in the database.
                number_of_prepared_sessions_stored = db.get_number_of_prepared_session_stored()

            if number_of_prepared_sessions_stored >= config.minimum_number_of_collected_sessions or self.get_testing():
                # The number is sufficient, we can continue.
                json_handler.write_field_to_json(execution_state_file_path, "number_of_collected_sessions",
                                                 "OK")  # Register this, so we do not have to make the check again.

                # Get all the prepared sessions in the database.
                all_prepared_sessions = db.get_all_prepared_sessions()

                print("Generating the balancing report...")
                report_model = BalancingReportModel(all_prepared_sessions,
                                                    config)  # Create the BalancingReportModel Object.
                report_model.generateBalancingReport()  # Generate the Balancing Report.
                print("Balancing report generated!")

                #wait_for_input("Press Enter to launch the BalancingReport application...")  # Wait the user response.

                #report_view = BalancingReportView()
                #report_view.open_balancing_report()  # Open the balancing report with the Windows default application.

                # The image will be open in the default viewer but the application will terminate here.

                #resp = wait_for_input("Response? 'OK' or 'NOT OK'?")  # Wait the user response.

                #json_handler.write_field_to_json(execution_state_file_path, "balancing_report", resp)  # Register the response.

            else:
                pass
                #json_handler.write_field_to_json(execution_state_file_path, "number_of_collected_sessions","NOT OK")  # Register this.


        elif coverage_report_status != "OK" or self.get_testing():
            # Create an instance of database controller.
            db = SegregationSystemDatabaseController()

            # Get all the prepared sessions in the database.
            all_prepared_sessions = db.get_all_prepared_sessions()

            print("Generating the input coverage report...")
            # Create the BalancingReportModel Object.
            report_model = CoverageReportModel(all_prepared_sessions)
            # Generate the Balancing Report.
            report_model.generateCoverageReport()
            print("Input coverage report generated!")

            #wait_for_input( "Press Enter to launch the Input Coverage Report application...")  # Wait the user response.

            #report_view = CoverageReportView()
            #report_view.open_coverage_report()  # Open the balancing report with the Windows default application.

            # The image will be open in the default viewer but the application will terminate here.

            #resp = wait_for_input("Response? 'OK' or 'NOT OK'?")  # Wait the user response.

            #json_handler.write_field_to_json(execution_state_file_path, "coverage_report", resp)  # Register the response.

        elif (coverage_report_status == "OK" and balancing_report_status == "OK" and number_of_session_status == "OK") or self.get_testing():
            # The final phase.
            # Create a Configuration object, to load the system configuration.
            config = SegregationSystemConfiguration()

            # Configure the system parameters from the configuration file.
            config.configure_parameters()

            # Create an instance of database controller.
            db = SegregationSystemDatabaseController()

            # Get all the prepared sessions in the database.
            all_prepared_sessions = db.get_all_prepared_sessions()

            report_model = LearningSetSplitter()
            learning_sets = report_model.generateLearningSets(all_prepared_sessions, config)

            # Create a MessageBroker instance to send and receive messages.
            message_broker = MessageBroker()

            # Get development IP
            network_info = json_handler.get_system_address("../global_netconf.json", "Development System")

            # Send the learning sets to the Development System.
            message_broker.send_message(network_info.get("ip"), network_info.get("port"), learning_sets)



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
