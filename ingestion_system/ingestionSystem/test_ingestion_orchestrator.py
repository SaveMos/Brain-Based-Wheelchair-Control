import json
import logging
from multiprocessing import Process
import pytest
import time

from src.communicationManager import CommunicationManager
from src.ingestionSystem.ingestionSystemController import IngestionController
from src.clientSideSystem.client import ClientSideController
from src.data import CSV_TEST_DATA_PATH, CLNT_MAN_CONFIG_FILE_PATH, TEST_DB_FILE_PATH

logger = logging.getLogger()
logger.level = logging.INFO

@pytest.fixture
def phases():
    # Returns a CommunicationManager for the evaluationSystem
    return {
        "development_phase": {"max_sessions":  10, "next_phase": "production_phase"},
        "production_phase": {"max_sessions":  10, "next_phase": "evaluation_phase"},
        "evaluation_phase": {"max_sessions":  8, "next_phase": "production_phase"}
    }


def run_controller(item):
    controller = IngestionController(TEST_DB_FILE_PATH)
    controller.phases = item
    controller.run()


def run_client():
    client = ClientSideController(CLNT_MAN_CONFIG_FILE_PATH, CSV_TEST_DATA_PATH)
    client.run(5, True)


def test_ingestion_system_controller(phases):
    # create receiver
    receiver = CommunicationManager("preparationSystem")
    label_receiver = CommunicationManager("evaluationSystem")

    # Run the controller
    ingestion_system = Process(target=run_controller, args=(phases,))
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
        message = receiver.receive_json()
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
