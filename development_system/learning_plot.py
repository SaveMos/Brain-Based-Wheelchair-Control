class LearningPlot:
    def __init__(self, error_curve: list):
        self._error_curve = error_curve


    def get_learning_error(self):
        """
            Get the learning error curve.
            Returns:
                list: A list of error values corresponding to each iteration
                or epoch of the learning process.
        """
        return self._error_curve