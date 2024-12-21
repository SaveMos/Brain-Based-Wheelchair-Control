import pytest
import logging
import json


from clientSideSystem.recordsender import RecordSender

logger = logging.getLogger()
logger.level = logging.DEBUG


@pytest.fixture #object to support test
def max_rows():
    return 6


def test_record_dispenser(max_rows):
    # checks the record randomisation on 56 records (4 files * 14 rows)
    CSV_TEST_PATH = "dataTest/"
    rd = RecordSender(CSV_TEST_PATH)
    rd.prepare_record_list(max_rows)
    file_path = CSV_TEST_PATH + 'output.json'

    with open(file_path, 'w') as file:
        json.dump(rd.record_list, file)

    assert len(rd.record_list) == 56