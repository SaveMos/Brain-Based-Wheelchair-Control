"""
Module: ingestion_system_orchestrator
Orchestrates the ingestion system workflow.
"""

#import classes
from .record_buffer_controller import RecordBufferController
from .raw_session_preparation import RawSessionPreparation
from .ingestion_system_parameters import IngestionSystemParameters
from .ingestion_system_json_io import IngestionSystemJSONIO


class IngestionSystemOrchestrator:
    """
    Orchestrator for the ingestion system workflow.
    Manages instances of system components.
    """

    def __init__(self, testing: bool):
        """
        Initializes the IngestionSystemOrchestrator object.

        Args:
            testing (bool): A flag to specify if the system is in testing mode.

        Example:
            orchestrator = IngestionSystemOrchestrator(testing=True)
        """

        print("INGESTION ORCHESTRATOR INITIALIZATION")

        #parameters class configuration
        self.parameters = IngestionSystemParameters()

        #buffer class configuration
        self.buffer_controller = RecordBufferController()

        #raw session configuration
        self.session_preparation = RawSessionPreparation()

        self.json_io = IngestionSystemJSONIO()

        #testing or not?
        self.testing = testing

        print("INGESTION ORCHESTRATOR INITIALIZED")


    def ingestion(self, record):
        """
        Process a record through the ingestion workflow.

        Args:
            record (dict): Record to process.
        """
        self.buffer_controller.store_record(record)
        records = self.buffer_controller.get_records()

        if len(records) >= self.parameters.number_of_records_to_store:
            raw_session = self.session_preparation.create_raw_session(records)
            self.buffer_controller.remove_records()
            self.session_preparation.mark_missing_samples(raw_session)

            if self.parameters.evaluation_phase:
                self.json_io.send_label_to_evaluation_system(raw_session)
            else:
                self.json_io.send_raw_session(raw_session)
