class PreparedSession:
    """
    Represents a raw session, which aggregates records and stores session data.

    Attributes:
        uuid (str): Unique identifier for the session.
        environment (str): The environment where the session occurred (e.g, slippery).
        eeg_data (list): List of EEG data points.
        activity (str): The activity being recorded (e.g., shopping).
        label (str): Label for evaluation purposes.
    """

    def __init__(self, uuid, features, label=None):
        """
        Initialize a raw session instance.

        Args:
            uuid (str): Unique session identifier.
            features(np.ndarray): extracted features
            label (str, optional): Label for evaluation. Defaults to None.
        """
        self.uuid = uuid
        self.features = features
        self.label = label
