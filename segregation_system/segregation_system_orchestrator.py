

from segregation_system.SegregationSystemJsonHandler import SegregationSystemJsonHandler
from segregation_system.balancing_report_model import BalancingReportModel
from segregation_system.coverage_report_model import CoverageReportModel
from segregation_system.learning_set_splitter import LearningSetSplitter
from segregation_system.segregation_database_manager.segregation_system_database_controller import \
    SegregationSystemDatabaseController
from segregation_system.segregation_system_parameters import SegregationSystemConfiguration
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
        self.db = SegregationSystemDatabaseController()
        self.message_broker = SessionReceiverAndConfigurationSender()

    def run(self):
        """
        Executes the segregation system by loading configuration parameters and initializing components.

        This method initializes a `SegregationSystemConfiguration` object to load system parameters
        from the configuration file and sets up the required subsystems.
        """
        SegregationSystemConfiguration.configure_parameters()
        execution_state_file_path = "user/user_responses.json"
        number_of_session_status = SegregationSystemJsonHandler.read_field_from_json(execution_state_file_path, "number_of_collected_sessions")
        balancing_report_status = SegregationSystemJsonHandler.read_field_from_json(execution_state_file_path, "balancing_report")
        coverage_report_status = SegregationSystemJsonHandler.read_field_from_json(execution_state_file_path, "coverage_report")

        if (number_of_session_status == "-" and balancing_report_status == "-") or self.get_testing():
            # Create a Configuration object, to load the system configuration.

            # Configure the system parameters from the configuration file.
            self.message_broker.start_server()
            print("Waiting for a message")

            while self.db.get_number_of_prepared_session_stored() < SegregationSystemConfiguration.LOCAL_PARAMETERS['minimum_number_of_collected_sessions']:
                # Receive the prepared session from the preparation system, and cast it into a PreparedSession object.
                message = self.message_broker.get_last_message()
                self.message_broker.send_timestamp("start")

                print("Prepared Session received!")
                message = SegregationSystemJsonHandler.string_to_dict(message['message'])

                if SegregationSystemJsonHandler.validate_json( message , "schemas/preparedSessionSchema.json"):
                    print("Prepared Session Valid!")
                    try:
                        # Validation of the prepared session.
                        #new_prepared_session = PreparedSession.from_dictionary(message)
                        #print("Prepared Session Valid! (class)")

                        # Store the new prepared session in the database.
                        self.db.store_prepared_session(message)
                    except Exception:
                        print("Prepared Session NOT Valid!")

                self.message_broker.send_timestamp("end")

            print("Enough prepared session stored!")
            SegregationSystemJsonHandler.write_field_to_json(execution_state_file_path, "number_of_collected_sessions",
                                                     "OK")  # Register this, so we do not have to make the check again.

            # Get all the prepared sessions in the database.
            all_prepared_sessions = self.db.get_all_prepared_sessions()

            print("Generating the balancing report...")
            #report_model = BalancingReportModel(all_prepared_sessions)  # Create the BalancingReportModel Object.
            #report_model.generateBalancingReport()  # Generate the Balancing Report.
            print("Balancing report generated!")

        if coverage_report_status == "-" and balancing_report_status == "NOT OK" and number_of_session_status == "OK":
            self.db.reset_session_database()
            self.message_broker.send_configuration("unbalanced_classes")
            self.reset_execution_state()

        if (coverage_report_status == "-" and balancing_report_status == "OK") or self.get_testing():
            # Get all the prepared sessions in the database.
            all_prepared_sessions = self.db.get_all_prepared_sessions()

            print("Generating the input coverage report...")
            # Create the BalancingReportModel Object.
            #report_model = CoverageReportModel(all_prepared_sessions)
            # Generate the Balancing Report.
            #report_model.generateCoverageReport()
            print("Input coverage report generated!")


        if coverage_report_status == "NOT OK" and balancing_report_status == "OK" and number_of_session_status == "OK":
            self.db.reset_session_database()
            self.message_broker.send_configuration("coverage_not_satisfied")
            self.reset_execution_state()

        if (coverage_report_status == "OK" and balancing_report_status == "OK" and number_of_session_status == "OK") or self.get_testing():
            # The final phase.
            # Create an instance of database controller.

            # Get all the prepared sessions in the database.
            all_prepared_sessions = self.db.get_all_prepared_sessions()

            report_model = LearningSetSplitter()
            learning_sets = report_model.generateLearningSets(all_prepared_sessions)


            network_info = SegregationSystemConfiguration.GLOBAL_PARAMETERS["Development System"]

            # Send the learning sets to the Development System.
            self.message_broker.send_message(network_info['ip'], network_info['port'], SegregationSystemJsonHandler.dict_to_string(learning_sets.to_dict()))
            self.db.reset_session_database()
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
        """
        Reset the execution state for a fresh-new stop&go interaction.
        """
        execution_state_file_path = "user/user_responses.json"
        SegregationSystemJsonHandler.write_field_to_json(execution_state_file_path, "number_of_collected_sessions" , "-")
        SegregationSystemJsonHandler.write_field_to_json(execution_state_file_path, "balancing_report", "-")
        SegregationSystemJsonHandler.write_field_to_json(execution_state_file_path, "coverage_report", "-")


# Example to test the class
if __name__ == "__main__":
    SegregationSystemConfiguration.configure_parameters()
    orchestrator = SegregationSystemOrchestrator(True)

    orchestrator.reset_execution_state()
    db = SegregationSystemDatabaseController()
    db.reset_session_database()

    orchestrator.run()
