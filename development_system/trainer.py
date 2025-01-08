import math
import joblib

from sklearn.metrics import log_loss

from development_system.classifier import Classifier
from development_system.configuration_parameters import ConfigurationParameters
from development_system.json_validator_reader_and_writer import JsonValidatorReaderAndWriter
from development_system.learning_set import LearningSet

class Trainer:
    """Class responsible for training a classifier."""

    def __init__(self):
        """Initialize trainer parameters."""
        self.classifier = Classifier()
        self.json_handler = JsonValidatorReaderAndWriter()
        self.learning_set = LearningSet([], [], [])

    def read_number_iterations(self):
        """
            Set the number of iterations.
            This function validates the JSON file containing the iteration details
            using a predefined schema and then reads the data to extract and return
            the number of iterations.

            Returns:
                int: The number of iterations.
        """
        self.json_handler.validate_json("intermediate_results/iterations.json", "schemas/iterations_schema.json")
        data=self.json_handler.read_json_file("intermediate_results/iterations.json")
        iterations =  data["iterations"]
        return iterations


    def set_average_hyperparameters(self):
        """Set the average hyperparameters."""

        avg_neurons = math.ceil((ConfigurationParameters.params['max_neurons'] + ConfigurationParameters.params['min_neurons']) / 2)
        avg_layers = math.ceil((ConfigurationParameters.params['max_layers'] + ConfigurationParameters.params['min_layers']) / 2)

        self.classifier.set_num_neurons(avg_neurons)
        self.classifier.set_num_layers(avg_layers)

    def set_hyperparameters(self, num_layers: int, num_neurons: int):
        """ Set the hyperparameters.
             Args:
                num_layers (int): The number of layers to set.
                num_neurons (int): The number of neurons to set.
        """
        self.classifier.set_num_layers(num_layers)
        self.classifier.set_num_neurons(num_neurons)


    def train(self, iterations, validation: bool = False):
        """
            Train the classifier.
            Args:
                iterations (int): The number of iterations for training.
                validation (bool, optional): Whether to perform validation after training. Defaults to False.

            Returns:
                object: The trained classifier.
        """
        #self.json_handler.validate_json("data/training_set.json","schemas/generic_set_schema.json")
        #training_data = self.json_handler.read_json_file("data/training_set.json")

        #result = self.learning_set.extract_features_and_labels(training_data, "training_set")
        training_data = joblib.load("data/training_set.sav")
        result = self.learning_set.extract_features_and_labels(training_data)

        training_features = result[0]
        training_labels = result[1]

        if not validation:
            self.classifier =  joblib.load("data/classifier_trainer.sav")

        self.classifier.set_num_iterations(iterations)

        # Train the classifier
        self.classifier.fit(x=training_features, y=training_labels)

        if validation:
            self.validate()                     #validation phase

        return self.classifier

    def validate(self):
        """
            Validate the classifier.

            This function loads validation data, extracts features and labels,
            and computes the validation error using log loss. The validation error
            is then set for the classifier.
        """
        #self.json_handler.validate_json("data/validation_set.json", "schemas/generic_set_schema.json")
        #validation_data = self.json_handler.read_json_file("data/validation_set.json")

        #result = self.learning_set.extract_features_and_labels(validation_data, "validation_set")
        validation_data = joblib.load("data/validation_set.sav")
        result = self.learning_set.extract_features_and_labels(validation_data)

        validation_features = result[0]
        validation_labels = result[1]

        validation_error = log_loss(y_true=validation_labels,
                                    y_pred=self.classifier.predict_proba(validation_features))

        self.classifier.set_validation_error(validation_error)