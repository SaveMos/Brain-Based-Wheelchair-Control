import os


def _get_data_file_absolute_path(relative_path: str) -> str:
    """
    Returns the absolute path of a file from a path relative to this file.
    :param relative_path: the path of a file relative to this module's file
    :return: the absolute path  resolved from the supplied relative path
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


TIME_START_PATH_PROD = _get_data_file_absolute_path('../nonElasticity/start_time_prod.txt')
TIME_START_PATH_DEV = _get_data_file_absolute_path('../nonElasticity/start_time_dev.txt')
TIME_END_PATH_PROD = _get_data_file_absolute_path("../nonElasticity/end_time_prod.txt")
