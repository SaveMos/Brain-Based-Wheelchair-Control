import json
import logging
from multiprocessing import Process
import time

from clientSideSystem.client import ClientSideOrchestrator
from ingestion_system.ingestion_system_orchestrator import IngestionSystemOrchestrator
from utility.message_broker.message_broker import MessageBroker

logger = logging.getLogger()
logger.level = logging.INFO

def run_controller(item):
    controller = IngestionSystemOrchestrator(TEST_DB_FILE_PATH)
    controller.phases = item
    controller.run()


def run_client():
    client = ClientSideOrchestrator("../../")
    client.run(5, True)


def test_ingestion_system_orchestrator():
    # create receiver
    receiver = MessageBroker("preparationSystem")
    label_receiver = MessageBroker("evaluationSystem")

    # Run the controller
    ingestion_system = Process(target=run_controller, args=())
    ingestion_system.start()

    time.sleep(1)

    # Run client
    client_system = Process(target=run_client)
    client_system.start()

    raw_sessions = []
    labels = []
    num_sessions = 28
    num_labels = 8

    # waits for the sessions
    for i in range(num_sessions):
        message = receiver.get_last_message()
        raw_session = json.loads(message["data"])
        raw_sessions.append(raw_session)

    # waits for labels
    for i in range(num_labels):
        message = label_receiver.receive_json()
        label = json.loads(message["data"])
        labels.append(label)

    ingestion_system.terminate()
    client_system.terminate()
    assert len(raw_sessions) == num_sessions
    assert len(labels) == 8
