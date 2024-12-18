"""
Module: raw_session
This module represents a raw session composed of multiple records (3/4).
"""

class RawSession:
    """
    Represents a raw session, which aggregates records and stores session data.

    Attributes:
        uuid (str): Unique identifier for the session.
        environment (str): The environment where the session occurred (e.g, slippery).
        label (str): Label for evaluation purposes.
        eeg_data (list): List of EEG data points.
        activity (str): The activity being recorded (e.g., shopping).
    """

    def __init__(self, uuid, environment, eeg_data, activity, label=None):
        """
        Initialize a raw session instance.

        Args:
            uuid (str): Unique session identifier.
            environment (str): Session environment.
            label (str, optional): Label for evaluation. Defaults to None.
            eeg_data (list): EEG data samples.
            activity(str): Recorded activity.
        """
        self.uuid = uuid
        self.environment = environment
        self.label = label
        self.eeg_data = eeg_data
        self.activity = activity


