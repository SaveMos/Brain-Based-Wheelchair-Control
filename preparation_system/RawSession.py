class RawSession:
    """
    Represents a raw session, which aggregates records and stores session data.

    Attributes:
        uuid (str): Unique identifier for the session.
        environment (str): The environment where the session occurred (e.g, slippery).
        eeg_data (list): List of EEG data points.
        activity (str): The activity being recorded (e.g., shopping).
        label (str): Label for evaluation purposes.
    """

    def __init__(self, uuid, environment, eeg_data, activity, label=None):
        """
        Initialize a raw session instance.

        Args:
            uuid (str): Unique session identifier.
            environment (str): Session environment.
            eeg_data (list): EEG data samples.
            activity(str): Recorded activity.
            label (str, optional): Label for evaluation. Defaults to None.
        """
        self.uuid = uuid
        self.environment = environment
        self.eeg_data = eeg_data
        self.activity = activity
        self.label = label

    @property
    def uuid(self) -> str:
        """
        Get the uuid of the session.

        Returns:
            str: The uuid of the session.
        """
        return self._uuid

    @uuid.setter
    def uuid(self, value: str):
        """
        Set the uuid of the session.

        Args:
            value (str): The new uuid of the session.
        """
        self._uuid = value

    @property
    def environment(self) -> str:
        """
        Get the environment of the session.

        Returns:
            str: The environment of the session.
        """
        return self._environment

    @environment.setter
    def environment(self, value: str):
        """
        Set the environment of the session.

        Args:
            value (str): The new environment of the session.
        """
        self._environment = value

    @property
    def eeg_data(self) -> list:
        """
        Get the EEG data of the session.

        Returns:
            list: The EEG data of the session.
        """
        return self._eeg_data

    @eeg_data.setter
    def eeg_data(self, value: list):
        """
        Set the EEG data of the session.

        Args:
            value (list): The new EEG data of the session.
        """
        self._eeg_data = value

    @property
    def activity(self) -> str:
        """
        Get the activity of the session.

        Returns:
            str: The activity of the session.
        """
        return self._activity

    @activity.setter
    def activity(self, value: str):
        """
        Set the activity of the session.

        Args:
            value (str): The new activity of the session.
        """
        self._activity = value

    @property
    def label(self) -> str:
        """
        Get the label of the session.

        Returns:
            str: The label of the session.
        """
        return self._label

    @label.setter
    def label(self, value: str):
        """
        Set the label of the session.

        Args:
            value (str): The new label of the session.
        """
        self._label = value
