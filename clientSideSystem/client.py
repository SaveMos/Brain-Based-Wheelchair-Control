import time
import json
from threading import Thread

from .recordSender import RecordSender
from utility.message_broker.message_broker import MessageBroker


def client_receiver(communication: MessageBroker) -> None:
    TIME_END_PATH_PROD = "../nonElasticity/end_time_prod.txt"
    while True:
        message = communication.get_last_message()
        print(message)

        ending_time = time.time()
        with open(TIME_END_PATH_PROD, "a") as my_file:
            my_file.write(str(ending_time) + "\n")
            my_file.close()


class ClientSideOrchestrator:

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.communication = MessageBroker(host='client side ip', port=5001)
        self.testing = True  #da parametrizzare?
        self.time_period = 0.1 # delay between messages to ingestion
        self.uuid_list = []
        return

    def _send_one_row(self, current_row: dict) -> None:
        """
        sends a raw to the ingestion System
        :param current_row: row to send
        """
        json_row = json.dumps(current_row)

        self.communication.send_message(target_ip='ingestion ip', target_port=5002, message=json_row)
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

        TIME_START_PATH_PROD = "../nonElasticity/start_time_prod.txt"
        TIME_START_PATH_DEV = "../nonElasticity/start_time_dev.txt"

        print("SENDING")

        #iterate over each record in the record_list
        for i, record in enumerate(record_sender.record_list):

            #check if the UUID has been already sent
            if record["value"]["UUID"] not in self.uuid_list:
                #if it's new, it is added to uuid_list
                self.uuid_list.append(record["value"]["UUID"])

                #if in the production testing phase
                if self.testing is True:
                    #save timestamp
                    starting_time_prod = time.time()
                    #save time in a specific file
                    with open(TIME_START_PATH_PROD, "a") as my_file:
                        my_file.write(str(starting_time_prod) + "\n")
                        my_file.close()

                #otherwise we are in development phase
                else:
                    #save timestamp every 100 UUID
                    if len(self.uuid_list) % 100 == 1:
                        starting_time_dev = time.time()

                        # save time in a another specific file
                        with open(TIME_START_PATH_DEV, "a") as my_file:
                            my_file.write(str(starting_time_dev) + "\n")
                            my_file.close()

            #send record to ingestion system
            self._send_one_row(record)
            time.sleep(self.time_period)

        #if it's not testing, wait for the end of receiving thread
        if not testing:
            receiver.join()
