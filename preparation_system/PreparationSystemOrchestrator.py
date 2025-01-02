import json
import sys

from ingestion_system.ingestion_json_handler.json_handler import JsonHandler
from preparation_system import ING_MAN_CONFIG_FILE_PATH, PREP_MAN_CONFIG_SCHEMA_FILE_PATH, RAW_SESS_SCHEMA_FILE_PATH
from preparation_system.PreparationSystemParameters import PreparationSystemParameters
from preparation_system.RawSessionReceiver_and_PreparedSessionSender import RawSessionReceiver_and_PrepareSessionSender
from preparation_system.SessionPreparation import SessionPreparation


class PreparationSystemOrchestrator:
    def __init__(self):
        print("-- PREPARATION SYSTEM STARTED --")
        handler = JsonHandler()
        #read configuration file
        configuration = handler.read_json_file(ING_MAN_CONFIG_FILE_PATH)
        #validate configuration file schema
        is_valid = handler.validate_json(configuration, PREP_MAN_CONFIG_SCHEMA_FILE_PATH)
        if is_valid is False:
            sys.exit(0)

        self.parameters = PreparationSystemParameters()

        #instantiate message exchanger
        self.communication = RawSessionReceiver_and_PrepareSessionSender(host='127.0.0.1', port=5015)
        self.communication.start_server()
        #prepare SessionPreparation istance with all configuration parameters
        self.session_preparation = SessionPreparation(configuration) #da modificare

        print("-- PREPARATION SYSTEM INITIALIZED --")

    def run(self) -> None:
        while True:
            # receive message
            message = self.communication.get_message()
            new_raw_session = json.loads(message["message"])

            # validate json
            handler = JsonHandler()
            is_valid = handler.validate_json(new_raw_session, RAW_SESS_SCHEMA_FILE_PATH)
            if is_valid is False:
                continue

            # correct raw session
            raw_session_corrected = self.session_preparation.correct_missing_samples(new_raw_session, None)
            raw_session_corrected = self.session_preparation.correct_outliers(raw_session_corrected)

            # create prepared session
            prepared_session = self.session_preparation.create_prepared_session(raw_session_corrected)
            json_prepared_session = handler.convert_dictionary_to_json(prepared_session)

            # send prepared session
            if self.parameters.development_phase:
                #send to segregation system
                self.communication.send_message('127.0.0.1', 5041, json_prepared_session)
            else: #commentare per il test
                #send to production system
                self.communication.send_message('127.0.0.1', 5045, json_prepared_session)