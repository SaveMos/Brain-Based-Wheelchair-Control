import math

import joblib
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
        self.json_handler.validate_json("intermediate_results/iterations.json", "schemas/iterations_schema.json")
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
        self.classifier.set_num_neurons(avg_neurons)
        self.classifier.set_num_layers(avg_layers)
        #save the values in the file so that can be used after the stop
        #self.json_handler.validate_json("intermediate_results/average_hyperparams.json", "schemas/average_hyperparams_schema.json")
        #self.json_handler.save_average_hyperparams(avg_neurons, avg_layers, "intermediate_results/average_hyperparams.json")

    def set_hyperparameters(self, num_layers: int, num_neurons: int):
        """Set the hyperparameters."""
        self.classifier.set_num_layers(num_layers)
        self.classifier.set_num_neurons(num_neurons)

    def train(self, iterations, validation: bool = False):
        """Train the classifier."""
        self.json_handler.validate_json("data/training_set.json","schemas/generic_set_schema.json")
        training_data = self.json_handler.read_json_file("data/training_set.json")

        result = self.json_handler.extract_features_and_labels(training_data, "training_set")
        """
        # Estrazione del training set
        training_set = data["training_set"]

        # Creazione del DataFrame da training_set
        training_data = pd.DataFrame([
            {"psd_alpha_band": record["psd_alpha_band"],
            "psd_beta_band": record["psd_beta_band"],
            "psd_theta_band": record["psd_theta_band"],
            "psd_delta_band": record["psd_delta_band"],
            #"activity": record["activity"],
            #"environment": record["environment"],
            "label": record["label"]}

            for record in training_set
        ])

        # Separazione delle caratteristiche (X) e delle etichette (y)
        #training_features = pd.DataFrame(training_data["features"].to_list())  # Convertiamo le liste in colonne
        training_features = training_data.drop(columns=["label"])
        training_labels = training_data["label"]
         """
        training_features = result[0]
        training_labels = result[1]

        if not validation:
            """
                self.json_handler.validate_json("intermediate_results/average_hyperparams.json","schemas/average_hyperparams_schema.json")
                data = self.json_handler.read_json_file("intermediate_results/average_hyperparams.json")
                self.classifier.set_num_neurons(data["avg_neurons"])
                self.classifier.set_num_layers(data["avg_layers"])
            """
            self.classifier =  joblib.load("data/classifier_trainer.sav")

        self.classifier.set_num_iterations(iterations)
        print("num neurons: ", self.classifier.get_num_neurons())
        print("num layers: ", self.classifier.get_num_layers())

        # Train the classifier
        self.classifier.fit(x=training_features, y=ravel(training_labels))

        if validation:
            self.validate()                     #validation phase

        return self.classifier

    def validate(self):
        self.json_handler.validate_json("data/validation_set.json", "schemas/generic_set_schema.json")
        validation_data = self.json_handler.read_json_file("data/validation_set.json")

        result = self.json_handler.extract_features_and_labels(validation_data, "validation_set")
        """
        # Estrazione del validation set
        validation_set = data["validation_set"]

        # Creazione del DataFrame da validation_set
        validation_data = pd.DataFrame([
            {"psd_alpha_band": record["psd_alpha_band"],
             "psd_beta_band": record["psd_beta_band"],
             "psd_theta_band": record["psd_theta_band"],
             "psd_delta_band": record["psd_delta_band"],
              #"activity": record["activity"],
             # "environment": record["environment"],
             "label": record["label"]}
            for record in validation_set
        ])

        # Separazione delle caratteristiche (X) e delle etichette (y)
        #validation_features = pd.DataFrame(validation_data["features"].to_list())
        validation_features = validation_data.drop(columns=["label"])
        validation_labels = validation_data["label"]
        """
        validation_features = result[0]
        validation_labels = result[1]

        true_labels = []
        for label in validation_labels:
            if label == 1.0:
                true_labels.append([1.0, 0])
            else:
                true_labels.append([0, 1.0])

        validation_error = log_loss(y_true=true_labels,
                                    y_pred=self.classifier.predict_proba(validation_features))

        self.classifier.set_validation_error(validation_error)