from segregation_system.SegregationSystemJsonHandler import SegregationSystemJsonHandler
from segregation_system.balancing_report_model import BalancingReportModel
from segregation_system.coverage_report_model import CoverageReportModel
from segregation_system.learning_set_splitter import LearningSetSplitter
from segregation_system.prepared_session import PreparedSession
from segregation_system.segregation_system_configuration import SegregationSystemConfiguration
from segregation_system.segregation_database_manager.segregation_system_database_controller import SegregationSystemDatabaseController
from segregation_system.session_receiver_and_configuration_sender import SessionReceiverAndConfigurationSender


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
        json_handler = SegregationSystemJsonHandler()
        execution_state_file_path = "user/user_responses.json"

        number_of_session_status = json_handler.read_field_from_json(execution_state_file_path, "number_of_collected_sessions")
        balancing_report_status = json_handler.read_field_from_json(execution_state_file_path, "balancing_report")
        coverage_report_status = json_handler.read_field_from_json(execution_state_file_path, "coverage_report")

        if (number_of_session_status == "-" or balancing_report_status == "-") or self.get_testing():
            # Create a Configuration object, to load the system configuration.
            config = SegregationSystemConfiguration()
            # Configure the system parameters from the configuration file.
            config.configure_parameters()

            # Create a MessageBroker instance to send and receive messages.
            message_broker = SessionReceiverAndConfigurationSender()
            # Create an instance of database controller.
            db = SegregationSystemDatabaseController()

            while db.get_number_of_prepared_session_stored() < config.minimum_number_of_collected_sessions:
                # Receive the prepared session from the preparation system, and cast it into a PreparedSession object.
                new_prepared_session = PreparedSession.from_dictionary(message_broker.get_last_message())

                # Store the new prepared session in the database.
                db.store_prepared_session(new_prepared_session.to_dictionary())

            json_handler.write_field_to_json(execution_state_file_path, "number_of_collected_sessions",
                                                     "OK")  # Register this, so we do not have to make the check again.

            # Get all the prepared sessions in the database.
            all_prepared_sessions = db.get_all_prepared_sessions()

            print("Generating the balancing report...")
            report_model = BalancingReportModel(all_prepared_sessions,
                                                        config)  # Create the BalancingReportModel Object.
            report_model.generateBalancingReport()  # Generate the Balancing Report.
            print("Balancing report generated!")

        if coverage_report_status == "-" and balancing_report_status == "NOT OK" and not self.get_testing():
            db = SegregationSystemDatabaseController()
            db.reset_session_database()
            message_broker = SessionReceiverAndConfigurationSender()
            message_broker.send_configuration()
            self.reset_execution_state()

        if (coverage_report_status == "-" and balancing_report_status == "OK") or self.get_testing():
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

        if coverage_report_status == "NOT OK" and balancing_report_status == "OK" and not self.get_testing():
            db = SegregationSystemDatabaseController()
            db.reset_session_database()
            message_broker = SessionReceiverAndConfigurationSender()
            message_broker.send_configuration()
            self.reset_execution_state()

        if (coverage_report_status == "OK" and balancing_report_status == "OK" and number_of_session_status == "OK") or self.get_testing():
            # The final phase.
            # Create a Configuration object, to load the system configuration.
            config = SegregationSystemConfiguration()

            # Configure the system parameters from the configuration file.
            config.configure_parameters()

            # Create an instance of database controller.
            db = SegregationSystemDatabaseController()

            # Get all the prepared sessions in the database.
            all_prepared_sessions = db.get_all_prepared_sessions()

            report_model = LearningSetSplitter(config)
            learning_sets = report_model.generateLearningSets(all_prepared_sessions)

            # Create a MessageBroker instance to send and receive messages.
            message_broker = SessionReceiverAndConfigurationSender()

            # Get development IP.
            network_info = json_handler.get_system_address("../global_netconf.json", "Development System")

            # Send the learning sets to the Development System.
            message_broker.send_message(network_info.get("ip"), network_info.get("port"), SegregationSystemJsonHandler.dict_to_string(learning_sets.to_dict()))

            db.reset_session_database()
            self.reset_execution_state()


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

    def reset_execution_state(self):
        json_handler = SegregationSystemJsonHandler()
        execution_state_file_path = "user/user_responses.json"
        json_handler.write_field_to_json(execution_state_file_path, "number_of_collected_sessions" , "-")
        json_handler.write_field_to_json(execution_state_file_path, "balancing_report", "-")
        json_handler.write_field_to_json(execution_state_file_path, "coverage_report", "-")


# Example to test the class
if __name__ == "__main__":
    orchestrator = SegregationSystemOrchestrator(True)
    orchestrator.reset_execution_state()
    orchestrator.run()
