import math

from numpy import ravel
import pandas as pd
from sklearn.metrics import log_loss

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.jsonIO import JsonHandler

class Trainer:
    """Class responsible for training a classifier."""

    def __init__(self):
        """Initialize trainer parameters."""
        self.classifier = Classifier()
        self.json_handler = JsonHandler()

    def read_number_iterations(self):
        """Set the number of iterations."""
        data=self.json_handler.read_json_file("intermediate_results/iterations.json")
        iterations =  data["iterations"]
        return iterations

    #def set_num_iterations(self, num_iterations: int):
        #self.classifier.set_num_iterations(num_iterations)

    def set_average_hyperparameters(self):
        """Set the average hyperparameters."""
        avg_neurons = math.ceil((ConfigurationParameters.max_neurons + ConfigurationParameters.min_neurons) / 2)
        avg_layers = math.ceil((ConfigurationParameters.max_layers + ConfigurationParameters.min_layers) / 2)
        print("avg_neurons: ", avg_neurons)

        #save the values in the file so that can be used after the stop
        self.json_handler.save_average_hyperparams(avg_neurons, avg_layers, "intermediate_results/average_hyperparams.json")

    def set_hyperparameters(self, num_layers: int, num_neurons: int):
        """Set the hyperparameters."""
        self.classifier.set_num_layers(num_layers)
        self.classifier.set_num_neurons(num_neurons)

    def train(self, iterations, validation: bool = False):
        """Train the classifier."""
        data = self.json_handler.read_json_file("intermediate_results/dataset_split.json")

        # Estrazione del training set
        training_set = data["training_set"]

        # Creazione del DataFrame da training_set
        training_data = pd.DataFrame([
            {"features": record["features"], "label": record["label"]}
            for record in training_set
        ])

        # Separazione delle caratteristiche (X) e delle etichette (y)
        training_features = pd.DataFrame(training_data["features"].to_list())  # Convertiamo le liste in colonne
        training_labels = training_data["label"]
        data = self.json_handler.read_json_file("intermediate_results/average_hyperparams.json")

        self.classifier.set_num_neurons(data["avg_neurons"])
        self.classifier.set_num_layers(data["avg_layers"])
        self.classifier.set_num_iterations(iterations)

        # Train the classifier
        self.classifier.fit(x=training_features, y=ravel(training_labels))

        if validation:
            self.validate()                     #validation phase

        return self.classifier

    def validate(self):
        data = self.json_handler.read_json_file("intermediate_results/dataset_split.json")

        # Estrazione del validation set
        validation_set = data["validation_set"]

        # Creazione del DataFrame da validation_set
        validation_data = pd.DataFrame([
            {"features": record["features"], "label": record["label"]}
            for record in validation_set
        ])

        # Separazione delle caratteristiche (X) e delle etichette (y)
        validation_features = pd.DataFrame(validation_data["features"].to_list())
        validation_labels = validation_data["label"]

        true_labels = []
        for label in validation_labels:
            if label == 1.0:
                true_labels.append([1.0, 0])
            else:
                true_labels.append([0, 1.0])

        validation_error = log_loss(y_true=true_labels,
                                    y_pred=self.classifier.predict_proba(validation_features))

        self.classifier.set_validation_error(validation_error)