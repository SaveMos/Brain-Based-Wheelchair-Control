import pytest
import logging
import json

from src.clientSideSystem.recordDispenser import RecordDispenser
from src.data import CSV_TEST_DATA_PATH

logger = logging.getLogger()
logger.level = logging.DEBUG


@pytest.fixture
def csv_list():
    return ["calendar", "helmet", "genre", "labels"]


@pytest.fixture
def max_rows():
    return 6


def test_record_dispenser(csv_list, max_rows):
    # checks the record randomisation on 56 records (4 files * 14 rows)
    rd = RecordDispenser(csv_list, CSV_TEST_DATA_PATH)
    rd.prepare_record_list(max_rows)
    file_path = CSV_TEST_DATA_PATH + 'output.json'

    with open(file_path, 'w') as file:
        json.dump(rd.record_list, file)

    assert len(rd.record_list) == 56


def test_extend(csv_list, max_rows):
    # checks the record randomisation on 56 records (4 files * 14 rows)
    rd = RecordDispenser(csv_list, CSV_TEST_DATA_PATH)
    rd.prepare_record_list(max_rows)
    rd.extend_list()
    file_path = CSV_TEST_DATA_PATH + 'output.json'

    with open(file_path, 'w') as file:
        json.dump(rd.record_list, file)

    assert len(rd.record_list) == 112
