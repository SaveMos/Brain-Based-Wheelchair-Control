"""
Module: raw_session_preparation
Handles the preparation of raw sessions from records.
"""

from raw_session import RawSession

class RawSessionPreparation:
    """
    Prepares raw sessions and marks missing samples in the records.
    """

    @staticmethod
    def create_raw_session(records):
        """
        Create a raw session from the given records.

        Args:
            records (list): List of records to include in the raw session.

        Returns:
            RawSession: A new raw session instance.
        """
        uuid = "session_" + str(len(records))  # Simulated UUID
        eeg_data = [record["data"] for record in records]
        activity = records[0]["activity"]
        environment = records[0]["environment"]

        return RawSession(uuid, eeg_data, activity, environment)

    @staticmethod
    def mark_missing_samples(raw_session):
        """
        Mark missing samples in the raw session's EEG data.

        Args:
            raw_session (RawSession): The raw session to process.
        """
        for i, sample in enumerate(raw_session.eeg_data):
            if not sample:  # Example: Empty sample
                raw_session.eeg_data[i] = "MISSING"
