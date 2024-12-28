"""
Module: ingestion_system_orchestrator
Orchestrates the ingestion system workflow.
"""

# import classes
import json
import sys

from . import ING_MAN_CONFIG_SCHEMA_FILE_PATH, ING_MAN_CONFIG_FILE_PATH, RECORD_SCHEMA_FILE_PATH
from .ingestion_json_handler.json_handler import JsonHandler
from .record_buffer_controller import RecordBufferController
from .raw_session_preparation import RawSessionPreparation
from .ingestion_system_parameters import Parameters
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
        handler = JsonHandler()
        # validate schema of configuration json
        configuration = handler.read_json_file(ING_MAN_CONFIG_FILE_PATH)
        is_valid = handler.validate_json(configuration, ING_MAN_CONFIG_SCHEMA_FILE_PATH)
        if is_valid is False:
            sys.exit(0)  # exit if not correct

        # parameters class configuration
        self.parameters = Parameters()

        # buffer class configuration
        self.buffer_controller = RecordBufferController()

        # raw session configuration
        self.session_preparation = RawSessionPreparation()

        # IO configuration
        self.json_io = SessionAndRecordExchanger(host='127.0.0.1', port=5001)  # parameters of Ingestion server
        self.json_io.start_server()
        self.number_of_missing_samples = 0

        # testing or not?
        self.testing = testing

        print("INGESTION ORCHESTRATOR INITIALIZED")

    def ingestion(self):
        """
        Process a record through the ingestion workflow.
        """
        i = 1
        while True:  # receive records iteratively
            try:
                print(i)
                i = i+1
                message = self.json_io.get_last_message()  # Get record message
                #print("record ricevuto dall'ingestion proveniente dal client:", message)

                # Debug: Verifica la struttura del messaggio
                #print(f"Message structure: {type(message)}, Content: {message}")

                record_message = message['message'] #json
                handler = JsonHandler()

                new_record = json.loads(record_message) #dictionary

                is_valid = handler.validate_json(new_record, RECORD_SCHEMA_FILE_PATH)
                if not is_valid:
                    continue

                # stores record
                self.buffer_controller.store_record(new_record)

                # retrieve records
                stored_records = self.buffer_controller.get_records(new_record["value"]["UUID"])

                # if there is at least one None: not enough records
                if None in stored_records:
                    continue
                print("OK RAW SESSION COMPLETA")

                # creates raw session
                raw_session = self.session_preparation.create_raw_session(stored_records)

                # removes records
                self.buffer_controller.remove_records(new_record["value"]["UUID"])

                # marks missing samples with "None" and checks the number
                self.number_of_missing_samples, marked_raw_session = self.session_preparation.mark_missing_samples(
                    raw_session, None)
                if self.number_of_missing_samples >= self.parameters.missing_samples_threshold_interval:
                    print("MANCANZA DI SAMPLES")
                    continue  # do not send anything

                # if in evaluation phase, sends labels to evaluation system
                if self.parameters.evaluation_phase:
                    label = {
                        "uuid": marked_raw_session.uuid,
                        "label": marked_raw_session.label
                    }
                    #print("json_label prima della conversione da dizionario a json ", label)
                    json_label = handler.convert_dictionary_to_json(label) #json
                    print("invio al client il label")
                    self.json_io.send_message(target_ip="127.0.0.1", target_port=5013, message=json_label)

                # sends raw sessions
                json_raw_session = marked_raw_session.to_json()
                print("invio al client la raw session")
                self.json_io.send_message(target_ip="127.0.0.1", target_port=5012, message=json_raw_session)

            except Exception as e:
                print(f"Error during ingestion: {e}")
