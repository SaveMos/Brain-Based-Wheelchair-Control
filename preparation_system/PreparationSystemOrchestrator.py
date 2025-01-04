"""

Module: PreparationSystemOrchestrator
Orchestrates the preparation system workflow.

Author: Francesco Taverna
"""


from preparation_system.preparation_json_handler.json_handler import JsonHandler
from preparation_system.PreparationSystemParameters import PreparationSystemParameters
from preparation_system.RawSessionReceiver_and_PreparedSessionSender import RawSessionReceiver_and_PrepareSessionSender
from preparation_system.SessionPreparation import SessionPreparation


class PreparationSystemOrchestrator:
    def __init__(self):
        print("-- PREPARATION SYSTEM STARTED --")


        self.parameters = PreparationSystemParameters()

        #instantiate message exchanger
        self.communication = RawSessionReceiver_and_PrepareSessionSender(host=self.parameters.configuration["ip_preparation"],
                                                                         port=self.parameters.configuration["port_preparation"])
        self.communication.start_server()
        #prepare SessionPreparation istance with all configuration parameters
        self.session_preparation = SessionPreparation()

        print("-- PREPARATION SYSTEM INITIALIZED --")

    def run(self) -> None:
        while True:
            # receive message
            boo, new_raw_session = self.communication.get_message()
            if boo:
                continue
            handler = JsonHandler()
            # correct raw session
            raw_session_corrected = self.session_preparation.correct_missing_samples(new_raw_session, None)
            raw_session_corrected = self.session_preparation.correct_outliers(raw_session_corrected)

            # create prepared session
            prepared_session = self.session_preparation.create_prepared_session(raw_session_corrected)
            json_prepared_session = handler.convert_dictionary_to_json(prepared_session)

            # send prepared session
            if self.parameters.configuration["development"]:
                #send to segregation system
                self.communication.send_message(self.parameters.configuration["ip_segregation"],
                                                self.parameters.configuration["port_segregation"], json_prepared_session)
            else: #to comment for the preparation test
                #send to production system
                self.communication.send_message(self.parameters.configuration["ip_production"],
                                                self.parameters.configuration["port_production"], json_prepared_session)