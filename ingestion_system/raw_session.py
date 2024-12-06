"""
Module: raw_session
This module represents a raw session composed of multiple records.
"""

class RawSession:
    """
    Represents a raw session, which aggregates records and stores session data.

    Attributes:
        uuid (str): Unique identifier for the session.
        eeg_data (list): List of EEG data points.
        activity (str): The activity being recorded (e.g., walking).
        environment (str): The environment where the session occurred.
        label (str): Label for evaluation purposes.
    """

    def __init__(self, uuid, eeg_data, activity, environment, label=None):
        """
        Initialize a raw session instance.

        Args:
            uuid (str): Unique session identifier.
            eeg_data (list): EEG data samples.
            activity (str): Recorded activity.
            environment (str): Session environment.
            label (str, optional): Label for evaluation. Defaults to None.
        """
        self.uuid = uuid
        self.eeg_data = eeg_data
        self.activity = activity
        self.environment = environment
        self.label = label
