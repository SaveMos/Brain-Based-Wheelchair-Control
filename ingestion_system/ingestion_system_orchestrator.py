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
        while True:  # receive records iteratively
            try:
                print("ricevo record")
                message = self.json_io.get_last_message()  # Get record message
                print("record ricevuto dall'ingestion proveniente dal client:", message)

                if not message:
                    print("No message received.")
                    continue

                # Debug: Verifica la struttura del messaggio
                print(f"Message structure: {type(message)}, Content: {message}")

                if isinstance(message, str):
                    # Prova a caricare il JSON se è una stringa
                    try:
                        message = json.loads(message)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON message: {e}")
                        continue

                # Debug: Verifica il contenuto del messaggio
                print(f"Decoded message: {message}")

                # Accedi alla chiave 'message'
                if 'message' not in message:
                    print("Key 'message' not found in message.")
                    continue

                record_message = message['message']
                print("Processed record_message:", record_message)

                handler = JsonHandler()

                # Converte il JSON in dizionario
                try:
                    new_record = json.loads(record_message)
                except Exception as e:
                    print(f"Error converting record_message to dictionary: {e}")
                    continue

                print("Converted record to dictionary:", new_record)

                # Valida il record
                is_valid = handler.validate_json(new_record, RECORD_SCHEMA_FILE_PATH)
                if not is_valid:
                    print(f"Invalid record received: {record_message}")
                    continue

                # stores record
                self.buffer_controller.store_record(new_record)

                # retrieve records
                stored_records = self.buffer_controller.get_records(new_record["value"]["UUID"])
                print("Stored records:", stored_records)

                # if there is at least one None: not enough records
                if None in stored_records:
                    continue

                # creates raw session
                raw_session = self.session_preparation.create_raw_session(stored_records)

                # removes records
                self.buffer_controller.remove_records(new_record["value"]["UUID"])

                # marks missing samples with "None" and checks the number
                self.number_of_missing_samples, marked_raw_session = self.session_preparation.mark_missing_samples(
                    raw_session, None)
                if self.number_of_missing_samples >= self.parameters.missing_samples_threshold_interval:
                    continue  # do not send anything

                # if in evaluation phase, sends labels to evaluation system
                if self.parameters.evaluation_phase:
                    label = {
                        "uuid": marked_raw_session.uuid,
                        "label": marked_raw_session.label
                    }

                    json_label = handler.convert_dictionary_to_json(label)
                    print("json_label da inviare al test ingestion: ", json_label)
                    self.json_io.send_message(target_ip="127.0.0.1", target_port=5003, message=json_label)

                # sends raw sessions
                json_raw_session = handler.convert_dictionary_to_json(vars(marked_raw_session))
                print("json_raw_session da inviare al test ingestion: ", json_raw_session)
                self.json_io.send_message(target_ip="127.0.0.1", target_port=5002, message=json_raw_session)

            except Exception as e:
                print(f"Error during ingestion: {e}")
