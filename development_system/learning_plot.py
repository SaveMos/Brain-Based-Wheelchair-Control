class LearningPlot:
    def __init__(self, error_curve: list):
        #self.max_number_iterations = None
        self._error_curve = error_curve


    def get_learning_error(self):
        return self._error_curve