from src.data import CLNT_MAN_CONFIG_FILE_PATH, CSV_DATA_PATH, CSV_TEST_DATA_PATH
from .client import ClientSideController

if __name__ == "__main__":
    client_controller = ClientSideController(CLNT_MAN_CONFIG_FILE_PATH, CSV_DATA_PATH)
    client_controller.run(5)
