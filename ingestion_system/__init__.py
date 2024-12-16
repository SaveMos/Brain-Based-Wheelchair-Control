import os


def _get_data_file_absolute_path(relative_path: str) -> str:
    """
    Returns the absolute path of a file from a path relative to this file.
    :param relative_path: the path of a file relative to this module's file
    :return: the absolute path  resolved from the supplied relative path
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# Ingestion system
ING_MAN_CONFIG_FILE_PATH = _get_data_file_absolute_path("Ingestion_Configuration/IngestionSystemConfiguration.json")


# Database Manager
DATABASE_FILE_PATH = _get_data_file_absolute_path("./IngestionDB/IngestionSystem.db")
DATABASE_FOLDER_PATH = _get_data_file_absolute_path("./IngestionDB")




# Communication Manager
COM_MAN_CONFIG_FILE_PATH = _get_data_file_absolute_path("./communicationManager/communicationManagerConfiguration.json")
COM_MAN_CONFIG_SCHEMA_FILE_PATH = _get_data_file_absolute_path("./communicationManager"
                                                               "/communicationManagerConfigurationSchema.json")


# Clientside System
CSV_DATA_PATH = _get_data_file_absolute_path("./clientSideSystem/")
CSV_TEST_DATA_PATH = _get_data_file_absolute_path("./test/clientSideSystem/")




ING_MAN_CONFIG_SCHEMA_FILE_PATH = \
    _get_data_file_absolute_path("./ingestionSystem/ingestionSystemConfigurationSchema.json")
ING_TEST_DATA_PATH = _get_data_file_absolute_path("./test/ingestionSystem/")
TEST_RECORD_EXAMPLE = _get_data_file_absolute_path("./test/ingestionSystem/record0.json")

# Client side system
CLNT_MAN_CONFIG_FILE_PATH = _get_data_file_absolute_path("./clientSideSystem/clientSideSystemConfiguration.json")
RAW_SESS_SCHEMA_FILE_PATH = _get_data_file_absolute_path("./preparationSystem/rawSessionSchema.json")
RECORD_SCHEMA_FILE_PATH = _get_data_file_absolute_path("./ingestionSystem/recordSchema.json")
RECORD_DB_FILE_PATH = _get_data_file_absolute_path("./ingestionSystem/recordDatabase.db")
TEST_DB_FILE_PATH = _get_data_file_absolute_path("./test/ingestionSystem/recordDatabase.db")
