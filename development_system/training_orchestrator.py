from development_system.classifier import Classifier
from development_system.learning_plot_model import LearningPlotModel
from development_system.learning_plot_view import LearningPlotView
from development_system.trainer import Trainer


class TrainingOrchestrator:
    """Orchestrator of the training"""

    def __init__(self):
        """ """
        self.trainer = Trainer()
        self.classifier = Classifier()
        self.plot_model = LearningPlotModel()
        self.plot_view = LearningPlotView()

    def train_classifier(self, set_average_hyperparams):
        """ """
        if set_average_hyperparams:
            self.trainer.set_average_hyperparameters()
        else:
            iterations = self.trainer.read_number_iterations()
            print("number of iterations= ", iterations)
            classifier = self.trainer.train(iterations)
            # GENERATE LEARNING REPORT
            learning_error = self.plot_model.generate_learning_report(classifier)
            # CHECK LEARNING PLOT
            self.plot_view.show_learning_plot(learning_error)
            #classifier.training_error = classifier.get_loss_curve() il training_error è calcolato in automatico da MLPClassifier
            #return classifier non serve nemmeno restituirlo, questo è allenato solo per trovare il numero di iterazioni corretto