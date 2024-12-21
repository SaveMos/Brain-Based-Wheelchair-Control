import uuid
from typing import Any, Dict, List

from segregation_system.prepared_session import PreparedSession
from utility.database.database_manager import DatabaseManager


class SegregationSystemDatabaseController:
    """
    A general-purpose SQLite database manager class.

    This class provides methods to interact with a SQLite database, including
    creating tables, inserting records, updating, deleting, and fetching data
    related to the `prepared_session` table.

    Author: Saverio Mosti

    Creation Date: 2024-12-19

    Attributes:
        __database_name (str): The name of the SQLite database.
        __table_name (str): The name of the table in the database where prepared sessions are stored.
        __db (DatabaseManager): An instance of DatabaseManager for interacting with the database.

    Methods:
        __init__(): Initializes the controller and ensures the database is set up.
        get_db(): Returns the DatabaseManager instance.
        get_table_name(): Returns the name of the table used for prepared sessions.
        store_prepared_session(data: Dict[str, Any]): Stores a prepared session in the database.
        initialize_prepared_session_database(): Ensures the `prepared_session` table exists in the database.
        drop_table(): Drops the `prepared_session` table from the database if it exists.
        get_all_prepared_sessions(): Retrieves all prepared sessions from the database as `PreparedSession` objects.
        get_number_of_prepared_session_stored(): Returns the total number of prepared sessions in the database.
        remove_prepared_session(session_uuid: str): Removes a prepared session from the database based on its UUID.
    """

    def __init__(self):
        """
        Initializes the SegregationSystemDatabaseController, setting up the database and table.

        This constructor ensures that the `prepared_session` table is created in the database
        upon initialization if it does not already exist.
        """
        self.__database_name = "prepared_session_database"  # The name of the SQLite database.
        self.__table_name = "prepared_session"  # PreparedSession table name.
        self.__db = DatabaseManager(self.__database_name) # Instantiate a DatabaseManager object.
        self.initialize_prepared_session_database() # Create if not exists the table.

    def get_db(self) -> DatabaseManager:
        """
        Returns the DatabaseManager instance associated with this controller.

        Returns:
            DatabaseManager: The instance of DatabaseManager for interacting with the database.
        """
        return self.__db

    def get_table_name(self) -> str:
        """
        Returns the name of the table used for storing prepared sessions.

        Returns:
            str: The table name, which is 'prepared_session' in this case.
        """
        return self.__table_name

    def store_prepared_session(self, data: Dict[str, Any]) -> None:
        """
        Stores a prepared session into the `prepared_session` table in the database.

        Args:
            data (Dict[str, Any]): A dictionary containing the session data to be stored.
            This dictionary should match the expected schema for a prepared session.
        """
        self.__db.insert(self.__table_name, data)

    def initialize_prepared_session_database(self):
        """
        Ensures that the `prepared_session` table exists in the database.
        If the table does not exist, this method creates it.

        The table has the following columns:
            - uuid (TEXT, Primary Key)
            - label (TEXT)
            - psd_alpha_band (REAL)
            - psd_beta_band (REAL)
            - psd_theta_band (REAL)
            - psd_delta_band (REAL)
            - activity (TEXT)
            - environment (TEXT)
        """
        create_table_query = f"""
                CREATE TABLE IF NOT EXISTS prepared_session (
                    uuid TEXT PRIMARY KEY,
                    label TEXT CHECK(label IN ('move', 'turn left', 'turn right')) NOT NULL,
                    psd_alpha_band REAL NOT NULL,
                    psd_beta_band REAL NOT NULL,
                    psd_theta_band REAL NOT NULL,
                    psd_delta_band REAL NOT NULL,
                    activity TEXT CHECK(activity IN ('shopping', 'sport', 'cooking', 'gaming', 'relax')) NOT NULL,
                    environment TEXT CHECK(environment IN ('slippery', 'plain', 'slope', 'house', 'track')) NOT NULL
                );
                """
        # Execute the query to create the table if it does not exist
        self.__db.execute_query(create_table_query)

    def drop_table(self):
        """
        Drops the `prepared_session` table from the database if it exists.

        This method ensures that if the table exists, it is removed to reset the database state.

        Returns:
            bool: True if the table was dropped successfully, False otherwise.
        """
        self.__db.drop_table(self.__table_name)

    def get_all_prepared_sessions(self) -> List[PreparedSession]:
        """
        Retrieves all prepared sessions from the database and converts them into `PreparedSession` objects.

        This method fetches all rows from the `prepared_session` table, maps the raw data to dictionaries,
        and then converts them into `PreparedSession` objects with the appropriate attributes.

        Returns:
            List[PreparedSession]: A list of `PreparedSession` objects corresponding to the rows in the database.
        """
        raw_prepared_sessions = self.__db.fetch_all(self.__table_name)

        # Define the column names manually (or dynamically if your database structure is more complex)
        column_names = [
            "uuid",
            "label",
            "psd_alpha_band",
            "psd_beta_band",
            "psd_theta_band",
            "psd_delta_band",
            "activity",
            "environment"
        ]

        # Convert tuples to dictionaries
        converted_sessions = [
            dict(zip(column_names, row)) for row in raw_prepared_sessions
        ]

        if not converted_sessions:  # Handle the case of an empty database
            print("No prepared sessions found in the database.")
            return []

        # Convert dictionaries to PreparedSession objects
        all_prepared_sessions = [
            PreparedSession(
                uuid = session["uuid"],
                features = [session["psd_alpha_band"], session["psd_beta_band"], session["psd_theta_band"],
                          session["psd_delta_band"], session["activity"] , session["environment"]],
                label = session["label"]
            )
            for session in converted_sessions
        ]

        # Assign additional attributes
        for session, raw in zip(all_prepared_sessions, converted_sessions):
            session.activity = raw["activity"]
            session.environment = raw["environment"]

        return all_prepared_sessions

    def get_number_of_prepared_session_stored(self) -> int:
        """
        Returns the number of records stored in the `prepared_session` table.

        Returns:
            int: The total number of prepared sessions in the table.
        """
        query = f"SELECT COUNT(*) FROM {self.__table_name}"

        # Fetch the result of the query and extract the first value from the first row
        result = self.__db.fetch_query(query)

        # Extract and return the first value (COUNT) from the first row (tuple)
        return result[0][0] if result else 0  # Return 0 if no result is found

    def remove_prepared_session(self, session_uuid: str) -> bool:
        """
        Removes a prepared session from the database based on its UUID.

        Args:
            session_uuid (str): The UUID of the session to be removed.

        Returns:
            bool: True if the session was removed successfully, False otherwise.
        """
        # Ensure the UUID is valid (optional validation based on the expected format)
        if not session_uuid:
            raise ValueError("Invalid UUID")

        # Create the query to delete the session from the database
        delete_query = f"DELETE FROM {self.__table_name} WHERE uuid = ?"

        # Execute the query
        self.__db.execute_query(delete_query, (session_uuid,))
        return True

    def reset_session_database(self):
        """
        Drops the `prepared_session` table from the database, and it creates it again.
        Use this function to reset the prepared session database.
        """
        self.drop_table()
        self.initialize_prepared_session_database()


# Example to test the class
if __name__ == "__main__":
    """
    Test the `store_prepared_session` method of the SegregationSystemDatabaseController class.
    """
    # Initialize the database controller
    db_controller = SegregationSystemDatabaseController()

    # Create a test dictionary matching the required schema
    test_data = {
        "uuid": str(uuid.uuid4()),  # Generate a unique UUID
        "label": "move",  # Valid label
        "psd_alpha_band": 0.25,  # Example numerical value
        "psd_beta_band": 0.30,  # Example numerical value
        "psd_theta_band": 0.45,  # Example numerical value
        "psd_delta_band": 0.60,  # Example numerical value
        "activity": "gaming",  # Valid activity
        "environment": "plain"  # Valid environment
    }

    # Store the prepared session into the database
    db_controller.store_prepared_session(test_data)
    print("Prepared session inserted into the database.")

    # Retrieve all records from the database
    all_sessions = db_controller.get_all_prepared_sessions()
    print(f"Total sessions in the database: {len(all_sessions)}")

    # Verify if the last inserted record matches the test data
    last_session = all_sessions[-1]
    assert last_session.uuid is not None, "Session ID should not be None."
    assert last_session.features == [
        test_data["psd_alpha_band"],
        test_data["psd_beta_band"],
        test_data["psd_theta_band"],
        test_data["psd_delta_band"],
        test_data["activity"],
        test_data["environment"]
    ], "Features do not match the test data."
    assert last_session.label == test_data["label"], "Label does not match the test data."

    print("Test passed!")
