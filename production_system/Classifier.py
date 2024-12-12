
class Classifier:
    """
        Data object class to represent a classifier used in Production System
    """
    def __init__(self, num_iteration: int, num_layers: int, num_neurons: int, test_error: int, validation_error: int, training_error: int):
        self._num_iteration = num_iteration
        self._num_layers = num_layers
        self._num_neurons = num_neurons
        self._test_error = test_error
        self._validation_error = validation_error
        self._training_error = training_error

    @property
    def num_iteration(self) -> int:
        """

        """
        return self._num_iteration

    @num_iteration.setter
    def num_iteration(self, value: int):
        self._num_iteration = value

    @property
    def num_layers(self) -> int:
        """

        """
        return self._num_layers

    @num_layers.setter
    def num_layers(self, value: int):
        self._num_layers = value

    @property
    def num_neurons(self) -> int:
        """

        """
        return self._num_neurons

    @num_neurons.setter
    def num_neurons(self, value: int):
        self._num_neurons = value

    @property
    def test_error(self) -> int:
        """

        """
        return self._test_error

    @test_error.setter
    def test_error(self, value: int):
        self._validation_error = value

    @property
    def validation_error(self) -> int:
        """

        """
        return self._validation_error

    @validation_error.setter
    def validation_error(self, value: int):
        self._validation_error = value

    @property
    def training_error(self) -> int:
        """

        """
        return self._training_error

    @training_error.setter
    def training_error(self, value: int):
        self._training_error = value



