"""
Module: ingestion_system_json_io
Handles JSON-based input and output operations for the ingestion system.
"""

class IngestionSystemJSONIO:
    """
    Provides methods for sending and receiving JSON data.
    """

    def send_raw_session(self, raw_session):
        """
        Send the raw session to the preparation system.

        Args:
            raw_session (RawSession): The raw session to send.
        """
        print(f"Raw session sent: {raw_session.uuid}")

    def send_label_to_evaluation_system(self, raw_session):
        """
        Send the label to the evaluation system.

        Args:
            raw_session (RawSession): The raw session with a label.
        """
        print(f"Label sent: {raw_session.label}")

    def receive_record(self):
        """
        Simulate receiving a record.
        Returns:
            dict: Mock record data.
        """
        return {"uuid": "1234", "data": [1, 2, 3], "activity": "running", "environment": "lab"}
