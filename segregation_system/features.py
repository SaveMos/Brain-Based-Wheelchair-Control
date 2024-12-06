class Features:
    """
    The `Features` class represents a collection of features related to signal processing
    or environmental analysis in a data segregation system.

    Attributes:
        PSD_alpha_band (float): Power spectral density (PSD) for the alpha band.
        PSD_beta_band (float): Power spectral density (PSD) for the beta band.
        PSD_theta_band (float): Power spectral density (PSD) for the theta band.
        activity_plus_small_scatter (float): Activity data combined with small scatter values.
        environment_plus_small_scatter (float): Environmental data combined with small scatter values.
    """

    def __init__(self,
                 PSD_alpha_band: float,
                 PSD_beta_band: float,
                 PSD_theta_band: float,
                 activity_plus_small_scatter: float,
                 environment_plus_small_scatter: float):
        """
        Initializes a new instance of the `Features` class.

        Args:
            PSD_alpha_band (float): Power spectral density for the alpha band.
            PSD_beta_band (float): Power spectral density for the beta band.
            PSD_theta_band (float): Power spectral density for the theta band.
            activity_plus_small_scatter (float): Activity data with small scatter values.
            environment_plus_small_scatter (float): Environmental data with small scatter values.
        """
        self._PSD_alpha_band = PSD_alpha_band
        self._PSD_beta_band = PSD_beta_band
        self._PSD_theta_band = PSD_theta_band
        self._activity_plus_small_scatter = activity_plus_small_scatter
        self._environment_plus_small_scatter = environment_plus_small_scatter

    # Getter and setter for PSD_alpha_band
    @property
    def PSD_alpha_band(self) -> float:
        """Returns the PSD value for the alpha band."""
        return self._PSD_alpha_band

    @PSD_alpha_band.setter
    def PSD_alpha_band(self, value: float):
        """Sets the PSD value for the alpha band."""
        if not isinstance(value, (float, int)):
            raise ValueError("PSD_alpha_band must be a number.")
        self._PSD_alpha_band = float(value)

    # Getter and setter for PSD_beta_band
    @property
    def PSD_beta_band(self) -> float:
        """Returns the PSD value for the beta band."""
        return self._PSD_beta_band

    @PSD_beta_band.setter
    def PSD_beta_band(self, value: float):
        """Sets the PSD value for the beta band."""
        if not isinstance(value, (float, int)):
            raise ValueError("PSD_beta_band must be a number.")
        self._PSD_beta_band = float(value)

    # Getter and setter for PSD_theta_band
    @property
    def PSD_theta_band(self) -> float:
        """Returns the PSD value for the theta band."""
        return self._PSD_theta_band

    @PSD_theta_band.setter
    def PSD_theta_band(self, value: float):
        """Sets the PSD value for the theta band."""
        if not isinstance(value, (float, int)):
            raise ValueError("PSD_theta_band must be a number.")
        self._PSD_theta_band = float(value)

    # Getter and setter for activity_plus_small_scatter
    @property
    def activity_plus_small_scatter(self) -> float:
        """Returns the activity data combined with small scatter values."""
        return self._activity_plus_small_scatter

    @activity_plus_small_scatter.setter
    def activity_plus_small_scatter(self, value: float):
        """Sets the activity data combined with small scatter values."""
        if not isinstance(value, (float, int)):
            raise ValueError("activity_plus_small_scatter must be a number.")
        self._activity_plus_small_scatter = float(value)

    # Getter and setter for environment_plus_small_scatter
    @property
    def environment_plus_small_scatter(self) -> float:
        """Returns the environmental data combined with small scatter values."""
        return self._environment_plus_small_scatter

    @environment_plus_small_scatter.setter
    def environment_plus_small_scatter(self, value: float):
        """Sets the environmental data combined with small scatter values."""
        if not isinstance(value, (float, int)):
            raise ValueError("environment_plus_small_scatter must be a number.")
        self._environment_plus_small_scatter = float(value)
