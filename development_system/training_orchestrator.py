import math
import random

import joblib

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.json_validator_reader_and_writer import JsonValidatorReaderAndWriter
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
        # Caricare i parametri di configurazione (se non è già stato fatto)
        ConfigurationParameters.load_configuration()
        # Assegnare il valore di service_flag alla proprietà di istanza
        self.service_flag: bool = ConfigurationParameters.service_flag
        self.json_handler = JsonValidatorReaderAndWriter()

    def train_classifier(self, set_average_hyperparams):
        """
            Train the classifier with specified or dynamically determined hyperparameters.

            This function trains the classifier based on whether average hyperparameters
            should be set or iterations should be dynamically adjusted. It handles both
            the service and testing phases, and supports generating and checking learning reports.

            Args:
                set_average_hyperparams (bool):
                    If True, sets average hyperparameters (neurons and layers)
                    and saves the configured classifier. If False, adjusts the number of iterations dynamically.
        """
        if set_average_hyperparams:
            self.trainer.set_average_hyperparameters()
            # both for the test and the service phase, we save the classifier with the layers and neurons setted
            self.classifier.set_num_neurons(self.trainer.classifier.get_num_neurons())
            self.classifier.set_num_layers(self.trainer.classifier.get_num_layers())
            joblib.dump(self.classifier, "data/classifier_trainer.sav")

        else:
            #if testing is true, the iterations are read from the file, otherwise are randomly generated

            if self.service_flag:
                iterations = random.randint(50, 150)

                while True:

                    classifier = self.trainer.train(iterations)
                    # GENERATE LEARNING REPORT
                    learning_error = self.plot_model.generate_learning_report(classifier)
                    # CHECK LEARNING PLOT
                    self.plot_view.show_learning_plot(learning_error)

                    choice = random.randint(0, 4)
                    if choice == 0:  # 20%
                        print("CHECK LEARNING PLOT OK)")
                        # se il numero di iterazioni è corretto, restituisce true, altrimenti false
                        # se il numero di iterazioni è corretto, salva il nuovo classifier
                        self.classifier.set_num_iterations(iterations)
                        joblib.dump(self.classifier, "data/classifier_trainer.sav")
                        break
                    if choice <= 2:  # 40%
                        print("CHECK LEARNING PLOT INCREASE 1/3")
                        iterations = math.ceil(iterations * (1 + 1 / 3))
                    else:  # 40%
                        print("CHECK LEARNING PLOT decrease 1/3")
                        iterations = math.ceil(iterations * (1 - 1 / 3))
            else:
                iterations = self.trainer.read_number_iterations()
                classifier = self.trainer.train(iterations)
                # GENERATE LEARNING REPORT
                learning_error = self.plot_model.generate_learning_report(classifier)
                # CHECK LEARNING PLOT
                self.plot_view.show_learning_plot(learning_error)

            print("number of iterations= ", iterations)

            #classifier.training_error = classifier.get_loss_curve() il training_error è calcolato in automatico da MLPClassifier
            #return classifier non serve nemmeno restituirlo, questo è allenato solo per trovare il numero di iterazioni corretto

