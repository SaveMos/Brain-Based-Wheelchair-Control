import json
import logging
from multiprocessing import Process
import pytest
import time

from src.communicationManager import CommunicationManager
from src.ingestionSystem.ingestionSystemController import IngestionController
from src.clientSideSystem.client import ClientSideController
from src.data import CSV_TEST_DATA_PATH, CLNT_MAN_CONFIG_FILE_PATH, TEST_DB_FILE_PATH
from src.preparationSystem.preparationSystemController import PreparationController


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


def run_ingestion(current_phase):
    controller = IngestionController(TEST_DB_FILE_PATH)
    controller.phases = current_phase
    controller.run()


def run_client():
    client = ClientSideController(CLNT_MAN_CONFIG_FILE_PATH, CSV_TEST_DATA_PATH)
    client.run(5, True)


def run_preparation(current_phase):
    controller = PreparationController()
    controller.phases = current_phase
    controller.run()


def test_preparation_system_controller(phases):
    # create receiver
    receiver_segregation = CommunicationManager("segregationSystem")
    receiver_evaluation = CommunicationManager("evaluationSystem")
    receiver_production = CommunicationManager("productionSystem")

    # Run the controller
    preparation_system = Process(target=run_preparation, args=(phases,))
    preparation_system.start()

    # Run ingestion
    ingestion_system = Process(target=run_ingestion, args=(phases,))
    ingestion_system.start()

    time.sleep(1)

    # Run client
    client_system = Process(target=run_client)
    client_system.start()

    prep_sessions_segregation = []
    prep_sessions_production = []
    labels = []
    num_sessions_segregation = 10
    num_sessions_production = 18
    num_labels = 8

    # waits for the sessions
    for i in range(num_sessions_segregation):
        message = receiver_segregation.receive_json()
        prep_session = json.loads(message["data"])
        prep_sessions_segregation.append(prep_session)

    for i in range(num_sessions_production):
        message = receiver_production.receive_json()
        prep_session = json.loads(message["data"])
        prep_sessions_production.append(prep_session)

    for i in range(num_labels):
        message = receiver_evaluation.receive_json()
        label = json.loads(message["data"])
        labels.append(label)

    # terminates
    preparation_system.terminate()
    ingestion_system.terminate()
    client_system.terminate()
    assert len(prep_sessions_production) == num_sessions_production
    assert len(prep_sessions_segregation) == num_sessions_segregation
    assert len(labels) == num_labels
