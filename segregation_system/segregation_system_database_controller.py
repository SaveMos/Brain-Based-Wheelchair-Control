from typing import Any, Dict

from segregation_system.prepared_session import PreparedSession
from utility.database.database_manager import DatabaseManager


class SegregationSystemDatabaseController:
    """
    A general-purpose SQLite database manager class.

    Provides methods to interact with a SQLite database, including
    creating tables, inserting records, updating, deleting, and fetching data.
    """

    def __init__(self):
        """
        Initialize the DatabaseManager with a given database name.
        """
        self.__database_name = "prepared_session_database"  # The database name.
        self.__db = DatabaseManager(self.__database_name)
        self.__table_name = "prepared_session"  # PreparedSession table name.

    def store_prepared_session(self, data: Dict[str, Any]) -> None:
        """
        Store a prepared session into the sessions database.
        """
        self.__db.insert(self.__table_name, data)

    def get_all_prepared_sessions(self):
        """
        Get all the prepared sessions from the database.
        """
        raw_prepared_sessions = self.__db.fetch_all(self.__table_name) # Get all the prepared sessions.

        # Convert them into PreparedSession objects.
        all_prepared_sessions = [
            PreparedSession(
                sessionID = session['sessionID'],
                features = session['features'],
                label = session['label']
            )
            for session in raw_prepared_sessions
        ]
        return all_prepared_sessions

    def get_number_of_prepared_session_stored(self) -> int:
        """
        Returns the number of records in the specified table.


        Returns:
            int: The total number of records in the table.
        """
        query = f"SELECT COUNT(*) FROM {self.__table_name}"

        # Fetch the result of the query and extract the first value from the first row
        result = self.__db.fetch_query(query)

        # Extract and return the first value (COUNT) from the first row (tuple)
        return result[0][0] if result else 0  # Return 0 if no result is found