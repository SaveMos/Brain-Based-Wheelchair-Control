"""
Module: raw_session_preparation
Handles the preparation of raw sessions from records.
"""

from .raw_session import RawSession

class RawSessionPreparation:
    """
    Prepares raw sessions and marks missing samples in the records.
    """

    def create_raw_session(self, records: list):
        """
        Create a raw session from the given records.

        Args:
            records (list): List of records to include in the raw session.

        Returns:
            RawSession: A new raw session instance.
        """
        uuid = records[0]
        environment = records[1]
        label = records[2]
        eeg_data = records[3]
        activity = records[4]

        return RawSession(uuid, environment, eeg_data, activity, label)

    def mark_missing_samples(self, raw_session):
        """
        Mark missing samples in the raw session's EEG data.

        Args:
            raw_session (RawSession): The raw session to process.
        """
        for i, sample in enumerate(raw_session.eeg_data):
            if not sample:
                raw_session.eeg_data[i] = "MISSING"
