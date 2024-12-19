import uuid
from unittest import TestCase
from uuid import uuid4

from segregation_system.prepared_session import PreparedSession
from segregation_system.segregation_system_database_controller import SegregationSystemDatabaseController


class TestSegregationSystemDatabaseController(TestCase):

    def setUp(self):
        """Set up the database controller and mock the database manager."""
        self.db_controller = SegregationSystemDatabaseController()
        self.test_data = {
            "uuid": str(uuid.uuid4()),  # Generate a unique UUID
            "label": "move",  # Valid label
            "psd_alpha_band": 0.25,  # Example numerical value
            "psd_beta_band": 0.30,  # Example numerical value
            "psd_theta_band": 0.45,  # Example numerical value
            "psd_delta_band": 0.60,  # Example numerical value
            "activity": "gaming",  # Valid activity
            "environment": "plain"  # Valid environment
        }

    def test_store_prepared_session(self):
        """Test if the store_prepared_session method stores data correctly."""
        # Prepare the data to store
        session_data = {
            "uuid": str(uuid4()),
            "label": "move",
            "psd_alpha_band": 0.5,
            "psd_beta_band": 0.6,
            "psd_theta_band": 0.7,
            "psd_delta_band": 0.8,
            "activity": "sport",
            "environment": "plain"
        }

        num = self.db_controller.get_number_of_prepared_session_stored()

        # Call the method
        self.db_controller.store_prepared_session(session_data)

        num_next = self.db_controller.get_number_of_prepared_session_stored()

        self.db_controller.remove_prepared_session(session_data["uuid"])

        self.assertEqual(num + 1, num_next)

    def test_initialize_prepared_session_database(self):
        """Test if the initialize_prepared_session_database method creates the table."""
        # Call the method
        self.db_controller.drop_table()
        self.db_controller.initialize_prepared_session_database()

        # Store the prepared session into the database
        self.db_controller.store_prepared_session(self.test_data)

        try:
            result = self.db_controller.get_number_of_prepared_session_stored()
            self.assertEqual(result, 1)
            self.db_controller.remove_prepared_session(self.test_data["uuid"])

        except Exception as e:
            self.fail()

    def test_drop_table(self):
        """Test if the drop_table method drops the table."""
        self.db_controller.initialize_prepared_session_database()
        self.db_controller.drop_table()

        try:
            # Query the sqlite_master table to check if the 'prepared_session' table exists
            query = f"SELECT 1 FROM prepared_session"
            result = self.db_controller.get_db().fetch_query(query)

            # If the result is non-empty, the table still exists.
            self.assertEqual(len(result), 0)

        except Exception as e:
            self.fail()

    from unittest import TestCase

    class TestSegregationSystemDatabaseController(TestCase):
        def setUp(self):
            """Sets up the test environment, initializing necessary data and controllers."""
            # Initialize your database controller (this might be different based on your setup)
            self.db_controller = SegregationSystemDatabaseController()

            # Sample test data for prepared session
            self.test_data = {
                "uuid": str(uuid.uuid4()),  # Generating a unique UUID for the session
                "label": "move",  # Example label
                "psd_alpha_band": 0.2,
                "psd_beta_band": 0.3,
                "psd_theta_band": 0.4,
                "psd_delta_band": 0.5,
                "activity": "shopping",  # Example activity
                "environment": "plain",  # Example environment
            }

        def test_get_all_prepared_sessions(self):
            """Test if the get_all_prepared_sessions method fetches data and converts it correctly."""
            # Drop the table and re-initialize it to start fresh
            self.db_controller.drop_table()
            self.db_controller.initialize_prepared_session_database()

            # Store two prepared sessions into the database
            first_uuid = self.test_data["uuid"]
            second_uuid = str(uuid.uuid4())  # Generate a new UUID for the second session

            # Store the first session
            self.db_controller.store_prepared_session(self.test_data)

            # Change UUID for the second session and store it
            self.test_data["uuid"] = second_uuid
            self.db_controller.store_prepared_session(self.test_data)

            # Retrieve all prepared sessions from the database
            all_prepared_sessions = self.db_controller.get_all_prepared_sessions()

            # Check if we got two sessions
            self.assertEqual(len(all_prepared_sessions), 2, "There should be two sessions in the database.")

            # Check if the session IDs match the UUIDs stored
            self.assertEqual(all_prepared_sessions[0].sessionID, first_uuid, "The first session's UUID does not match.")
            self.assertEqual(all_prepared_sessions[1].sessionID, second_uuid,
                             "The second session's UUID does not match.")

            # Validate the features and labels of the sessions
            for session in all_prepared_sessions:
                self.assertIsInstance(session, PreparedSession,
                                      "The returned object should be an instance of PreparedSession.")
                self.assertEqual(len(session.features), 4, "Each session should have four features (PSD bands).")
                self.assertIn(session.label, ["move", "turn left", "turn right"],
                              "Label should be one of the valid labels.")
                self.assertIn(session.features[4], ["shopping", "sport", "cooking", "gaming", "relax"],
                              "Activity should be one of the valid activities.")
                self.assertIn(session.features[5], ["slippery", "plain", "slope", "house", "track"],
                              "Environment should be one of the valid environments.")

            # Check that all data is correctly stored and converted
            session1 = all_prepared_sessions[0]
            session2 = all_prepared_sessions[1]

            # Check the features of the first session
            self.assertEqual(session1.features, [
                self.test_data["psd_alpha_band"],
                self.test_data["psd_beta_band"],
                self.test_data["psd_theta_band"],
                self.test_data["psd_delta_band"]
            ], "Features of the first session do not match.")

            # Check the features of the second session (which should have the same values)
            self.assertEqual(session2.features, [
                self.test_data["psd_alpha_band"],
                self.test_data["psd_beta_band"],
                self.test_data["psd_theta_band"],
                self.test_data["psd_delta_band"]
            ], "Features of the second session do not match.")


    def test_get_number_of_prepared_session_stored(self):
        """Test if the get_number_of_prepared_session_stored method returns the correct count."""
        self.db_controller.drop_table()
        self.db_controller.initialize_prepared_session_database()

        num_0 = self.db_controller.get_number_of_prepared_session_stored()
        self.assertEqual(num_0, 0)

        # Store the prepared session into the database
        self.test_data["uuid"] = str(uuid.uuid4()) # Change the unique ID.
        self.db_controller.store_prepared_session(self.test_data)
        num_0 = self.db_controller.get_number_of_prepared_session_stored()
        self.assertEqual(num_0, 1)

        # Store the prepared session into the database
        self.test_data["uuid"] = str(uuid.uuid4())  # Change the unique ID.
        self.db_controller.store_prepared_session(self.test_data)
        num_0 = self.db_controller.get_number_of_prepared_session_stored()
        self.assertEqual(num_0, 2)

        self.db_controller.remove_prepared_session(self.test_data["uuid"])
        num_0 = self.db_controller.get_number_of_prepared_session_stored()
        self.assertEqual(num_0, 1)
