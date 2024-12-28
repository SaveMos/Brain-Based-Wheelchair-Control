import os
import time
import json
from threading import Thread

from ingestion_system.SessionAndRecordExchanger import SessionAndRecordExchanger
from . import TIME_START_PATH_PROD, TIME_START_PATH_DEV, TIME_END_PATH_PROD
from .recordsender import RecordSender



def client_receiver(communication: SessionAndRecordExchanger) -> None:
    #waits for receiving messages from the ingestion system
    while True:
        message = communication.get_message()
        print(message)

        ending_time = time.time()
        with open(TIME_END_PATH_PROD, "a") as my_file:
            #save timestamp
            my_file.write(str(ending_time) + "\n")
            my_file.close()


class ClientSideOrchestrator:
    """
    Manage sending records to the ingestion system.
    Coordinate recording of timestamps to monitor response times (Responsiveness).
    Start a separate thread to receive messages from the ingestion system.
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.communication = SessionAndRecordExchanger(host='127.0.0.1', port=5000)
        self.is_testing_production = True  #da parametrizzare?
        self.time_period = 0.1 # delay between messages to ingestion
        self.uuid_list = []
        return

    def _send_one_row(self, current_row: dict) -> None:
        """
        sends a raw to the ingestion System
        :param current_row: row to send
        """
        #print("il record prima dell'invio all'ingestion è:", current_row)
        print("mando una row")
        json_row = json.dumps(current_row)
        #print("il record modificato prima dell'invio all'ingestion: ", json_row)

        response = self.communication.send_message(target_ip='127.0.0.1', target_port=5001, message=json_row)
        if response is None:
            print("Failed to send the message. Retrying...")
            time.sleep(1)
        return

    def run(self, max_rows: int, testing: bool = False) -> None:

        # prepares records
        record_sender = RecordSender(self.csv_path)
        record_sender.prepare_record_list(max_rows)

        #PER COSA???????? forse per: è responsabile della ricezione di
        # messaggi o conferme dal sistema di ingestione.
        # creates receiving thread
        receiver = Thread(target=client_receiver, args=(self.communication, ))
        receiver.start()


        print("SENDING")
        #iterate over each record in the record_list
        for i, record in enumerate(record_sender.record_list):
            #check if the UUID has been already sent
            if record["value"]["UUID"] not in self.uuid_list:
                #if it's new, it is added to uuid_list
                self.uuid_list.append(record["value"]["UUID"])

                #if in the production testing phase
                if self.is_testing_production is True:
                    #save timestamp of when the row is sent (to measure responsiveness)
                    starting_time_prod = time.time()
                    #save time in a specific file
                    with open(TIME_START_PATH_PROD, "a") as my_file:
                        my_file.write(str(starting_time_prod) + "\n")
                        my_file.close()

                #otherwise we are in development phase
                else:
                    #save timestamp every 100 UUID because in dev phase we monitor just a subset of record
                    #to avoid an excessive overhead
                    if len(self.uuid_list) % 100 == 1:
                        starting_time_dev = time.time()

                        # save time in a another specific file
                        with open(TIME_START_PATH_DEV, "a") as my_file:
                            my_file.write(str(starting_time_dev) + "\n")
                            my_file.close()

            #send record to ingestion system
            self._send_one_row(record)
            time.sleep(self.time_period)

        print("ho finito di inviare i dati all'ingestion")
        #if it's not testing, wait for the end of receiving thread
        if not testing:
            receiver.join()
