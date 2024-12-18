from typing import Any, Dict

from segregation_system.prepared_session import PreparedSession
from utility.database.database_manager import DatabaseManager


class SegregationSystemDatabaseController:
    """
    A general-purpose SQLite database manager class.

    Provides methods to interact with a SQLite database, including
    creating tables, inserting records, updating, deleting, and fetching data.
    """

    def __init__(self, db_name: str):
        """
        Initialize the DatabaseManager with a given database name.

        :param db_name: The name of the SQLite database file.
        """
        self.__db = DatabaseManager(db_name)
        self.__table_name = "prepared_session"  # PreparedSession table name.
        self.__database_name = "prepared_session_database"  # The database name.


    def store_prepared_session(self, data: Dict[str, Any]) -> None:
        self.__db.insert(self.__table_name, data)

    def get_all_prepared_sessions(self , table_name : str):
        # Get all the prepared sessions from the database.
        raw_prepared_sessions = self.__db.fetch_all(table_name)

        # Convert them into PreparedSession objects.
        all_prepared_sessions = [
            PreparedSession(
                sessionID=session['sessionID'],  # Assuming 'sessionID' is a key in the dict.
                features=session['features'],  # Assuming 'features' is a list of float values.
                label=session['label']  # Assuming 'label' is a string.
            )
            for session in raw_prepared_sessions
        ]
        return all_prepared_sessions

    def number_of_tuples(self, table_name: str) -> int:
        """
        Returns the number of records in the specified table.

        Args:
            table_name (str): The name of the table to count records from.

        Returns:
            int: The total number of records in the table.
        """
        query = f"SELECT COUNT(*) FROM {table_name}"

        # Fetch the result of the query and extract the first value from the first row
        result = self.__db.fetch_query(query)

        # Extract and return the first value (COUNT) from the first row (tuple)
        return result[0][0] if result else 0  # Return 0 if no result is found