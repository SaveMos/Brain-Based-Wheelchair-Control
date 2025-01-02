import json
from typing import Any
import pandas as pd

from jsonschema import validate, ValidationError, SchemaError
from segregation_system.prepared_session import PreparedSession
from segregation_system.learning_set import LearningSet
from development_system.classifier import Classifier

class JsonValidatorReaderAndWriter:
    """
        A class to read and save file json
    """

    @staticmethod
    def validate_json(json_file: str, schema_file: str) -> bool:
        """
        Validate a JSON file against a JSON schema.

        :param json_file: Path to the JSON file to validate.
        :param schema_file: Path to the JSON schema file.
        :return: True if the JSON is valid, False otherwise.
        """
        try:
            # Load JSON data
            with open(json_file, 'r') as Jf:
                json_data = json.load(Jf)

            # Load JSON schema
            with open(schema_file, 'r') as Sf:
                json_schema = json.load(Sf)

            # Validate JSON against schema
            validate(instance=json_data, schema=json_schema)
            print("JSON is valid.")
            return True

        except ValidationError as ex:
            print(f"Validation Error: {ex.message}")
        except SchemaError as ex:
            print(f"Schema Error: {ex.message}")

        return False

    """"
    @staticmethod
    def json_to_learning_set(json_file_path: str) -> LearningSet:
        
        # Reading of the JSON
        with open(json_file_path, "r") as file:
            current_data = json.load(file)

        # Helper function to create a list of PreparedSession
        def parse_sessions(session_list):
            return [PreparedSession(**session_data) for session_data in session_list]

        # Parsing of the dataset
        training_set = parse_sessions(current_data.get("training_set", []))
        validation_set = parse_sessions(current_data.get("validation_set", []))
        test_set = parse_sessions(current_data.get("test_set", []))

        # Creation of the LearningSet
        learning_set = LearningSet(
            training_set=training_set,
            validation_set=validation_set,
            test_set=test_set
        )

        return learning_set
        """

    """
    @staticmethod
    def print_learning_set(learning_set: LearningSet):
        def print_session(current_session: PreparedSession):
            
            print(f"UUID: {current_session.uuid}")
            print(f"Label: {current_session.label}")
            print(f"Features: {current_session.features}")
            print()

        print("Training Set:")
        for session in learning_set.training_set:
            print_session(session)

        print("Validation Set:")
        for session in learning_set.validation_set:
            print_session(session)

        print("Test Set:")
        for session in learning_set.test_set:
            print_session(session)

    """

    @staticmethod
    def read_configuration_parameters(filepath):
        """
        Read a json file that contains the parameters.

        Returns:
            file_content: content of json file.

        """

        params = {}
        try:
            with open(filepath, "r") as f:
                file_content = json.load(f)

            layers = file_content.get('layers', {})
            neurons = file_content.get('neurons', {})
            tolerance = file_content.get('tolerance', {})

            params["min_layers"] = layers.get('min_layers')
            params["max_layers"] = layers.get('max_layers')
            params["step_layers"] = layers.get('step_layers')
            params["min_neurons"] = neurons.get('min_neurons')
            params["max_neurons"] = neurons.get('max_neurons')
            params["step_neurons"] = neurons.get('step_neurons')
            params["overfitting_tolerance"] = tolerance.get('overfitting_tolerance')
            params["generalization_tolerance"] = tolerance.get('generalization_tolerance')
            params["service_flag"] = file_content.get('service_flag')

            return params

        except Exception as ex:
            print("Error to read file at path " + filepath + str(ex))
            return None

    """
    @staticmethod
    def save_average_hyperparams(avg_neurons, avg_layers, filepath):

        data = {
            "avg_neurons": avg_neurons,
            "avg_layers": avg_layers
        }

        try:
            with open(filepath, "w") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
                return True
        except Exception as e:
            print("Error to save file at path " + filepath + ": " + str(e))
            return False
    """

    @staticmethod
    def read_json_file(filepath):
       
        try:
            with open(filepath, "r") as f:
                file_content = json.load(f)
            return file_content

        except Exception as e:
            print("Error to read file at path " + filepath + ": " + str(e))
            return None


    @staticmethod
    def write_json_file(data, filepath):
        """
            Args:
                data: data to write into json file
                filepath: path where json file will be saved.

            Returns:
                bool: True if the file is written successfully, False otherwise.
        """

        try:
            with open(filepath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                return True
        except Exception as e:
            print("Error to save file at path " + filepath + ": " + str(e))
            return False

    """
    @staticmethod
    def read_winner_network(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)

        classifier = Classifier()
        classifier.set_num_iterations(data.get("num_iterations"))
        classifier.set_validation_error(data.get("validation_error"))
        classifier.set_training_error(data.get("training_error"))
        classifier.set_num_layers(data.get("num_layers"))
        classifier.set_num_neurons(data.get("num_neurons"))

        return classifier
    """

    def get_system_address(self , json_filepath: str, system_name: str) -> Any | None:
        """
        Reads the IP address and port of a specified system from a JSON file.

        Args:
            json_filepath (str): Path to the JSON file containing system configurations.
            system_name (str): Name of the system whose address is to be fetched.

        Returns:
            dict: A dictionary containing the IP address and port of the specified system.
                  Example: {"ip": "192.168.149.66", "port": 8001}
            None: If the system name is not found or an error occurs.
        """
        try:
            # Load the JSON file
            systems_data = self.read_json_file(json_filepath)

            # Fetch the system configuration
            system_info = systems_data.get(system_name)
            if system_info:
                return system_info
            else:
                print(f"System '{system_name}' not found in the configuration file.")
                return None

        except FileNotFoundError:
            print(f"Error: File '{json_filepath}' not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON file.")
            return None
