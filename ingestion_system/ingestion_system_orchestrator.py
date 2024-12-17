"""
Module: ingestion_system_orchestrator
Orchestrates the ingestion system workflow.
"""

#import classes
import json

from .ingestion_json_handler.json_handler import JsonHandler
from .record_buffer_controller import RecordBufferController
from .raw_session_preparation import RawSessionPreparation
from .ingestion_system_parameters import IngestionSystemParameters
from .SessionAndRecordExchanger import SessionAndRecordExchanger


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

        #IO configuration
        self.json_io = SessionAndRecordExchanger(host='0.0.0.0', port=5001) #parameters of Ingestion server
        self.json_io.start_server()
        self.Number_of_missing_samples = 0

        #testing or not?
        self.testing = testing

        print("INGESTION ORCHESTRATOR INITIALIZED")


    def ingestion(self, record):
        """
        Process a record through the ingestion workflow.

        Args:
            record (dict): Record to process.
        """
        while True: #receive records iteratively
            message = self.json_io.get_last_message()['message'] #get record message

            new_record = json.load(message) #convert json in python dict
            # stores record
            self.buffer_controller.store_record(new_record)

            # retrieve records
            stored_records = self.buffer_controller.get_records(new_record["value"]["UUID"])

            # if there is at least one None: not enough records
            if None in stored_records:
                continue

            # creates raw session
            raw_session = self.session_preparation.create_raw_session(stored_records)

            # removes records
            self.buffer_controller.remove_records(new_record["value"]["UUID"])

            # marks missing samples with "None" and checks the number
            self.Number_of_missing_samples, marked_raw_session = self.session_preparation.mark_missing_samples(raw_session, None)
            if self.Number_of_missing_samples >= self.parameters.missing_samples_threshold_interval:
                continue #do not send anything

            # if in evaluation phase, sends labels to evaluation system
            handler = JsonHandler()
            if self.parameters.evaluation_phase:
                label = {
                    "uuid": marked_raw_session["uuid"],
                    "label": marked_raw_session["label"]
                }

                json_label = handler.convert_dictionary_to_json(label)
                self.json_io.send_message(target_ip='ip evaluation system', target_port=5002, message=json_label)

            # sends raw sessions
            json_raw_session = handler.convert_dictionary_to_json(marked_raw_session)
            self.json_io.send_message(target_ip='ip preparation system', target_port=5002, message=json_raw_session)
            #self._update_session()
