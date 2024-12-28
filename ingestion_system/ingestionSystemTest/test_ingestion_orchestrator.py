import json
import logging
from multiprocessing import Process
import time

from clientSideSystem.client import ClientSideOrchestrator
from ingestion_system.SessionAndRecordExchanger import SessionAndRecordExchanger
from ingestion_system.ingestion_system_orchestrator import IngestionSystemOrchestrator

logger = logging.getLogger()
logger.level = logging.INFO

def run_orchestrator():
    orchestrator = IngestionSystemOrchestrator(False)
    orchestrator.ingestion()


def run_client():
    client = ClientSideOrchestrator("dataTest/")
    client.run(5, True)


def test_ingestion_system_orchestrator():
    # create receiver
    receiver = SessionAndRecordExchanger(host='127.0.0.1', port=5012)
    label_receiver = SessionAndRecordExchanger(host='127.0.0.1', port=5013)
    receiver.start_server()
    label_receiver.start_server()

    # Run the orchestrator
    ingestion_system = Process(target=run_orchestrator, args=())
    ingestion_system.start()

    time.sleep(1)

    # Run client
    client_system = Process(target=run_client)
    client_system.start()

    raw_sessions = []
    labels = []
    num_sessions = 14
    num_labels = 14
    # waits for the sessions
    for i in range(num_sessions):
        message = receiver.get_message()
        #print("io preparation messaggio ricevuto dall'ingestion: ", message)
        raw_session = json.loads(message['message']) #convert to dictionary
        #print("io preparation messaggio trasformato: ", message)
        raw_sessions.append(raw_session)
    # waits for labels
    for i in range(num_labels):
        message = label_receiver.get_message()
        label = json.loads(message['message'])
        labels.append(label)

    ingestion_system.terminate()
    client_system.terminate()
    assert len(raw_sessions) == num_sessions
    assert len(labels) == 14

if __name__ == "__main__":
    test_ingestion_system_orchestrator()
