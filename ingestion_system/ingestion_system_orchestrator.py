"""
Module: ingestion_system_orchestrator
This module orchestrates the ingestion system workflow by interacting with other components.
"""

from record_buffer_controller import RecordBufferController
from raw_session_preparation import RawSessionPreparation
from ingestion_system_parameters import IngestionSystemParameters
from ingestion_system_json_io import IngestionSystemJSONIO

class IngestionSystemOrchestrator:
    """
    Orchestrator for the ingestion system workflow. Acts as a controller to call other components.
    """

    @staticmethod
    def ingestion(record):
        """
        Process a record through the ingestion workflow.

        Args:
            record (dict): Record to process.
        """
        # Load parameters from the configuration json
        IngestionSystemParameters.load_parameters()

        # Store record in buffer
        RecordBufferController.store_record(record)

        # Check if sufficient records are available
        records = RecordBufferController.get_records()
        if len(records) >= IngestionSystemParameters.number_of_records_to_store:
            # Create a raw session
            raw_session = RawSessionPreparation.create_raw_session(records)

            # Remove processed records
            RecordBufferController.remove_records()

            # Mark missing samples
            RawSessionPreparation.mark_missing_samples(raw_session)

            # Handle raw session based on its validity and evaluation phase
            if raw_session is not None:
                if IngestionSystemParameters.evaluation_phase:
                    IngestionSystemJSONIO.send_label_to_evaluation_system(raw_session)
                else:
                    IngestionSystemJSONIO.send_raw_session(raw_session)
