import json
from typing import Any

from segregation_system.prepared_session import PreparedSession
from segregation_system.learning_set import LearningSet
from development_system.classifier import Classifier
class JsonHandler:
    """
        A class to read and save file json
    """

    def create_learning_set_from_json(self, json_file_path: str) -> LearningSet:
        """
        Convert a JSON file in a LearningSet obgect.

        Args:
            json_file_path (str): The path to the JSON file.

        Returns:
            LearningSet: A LearningSet instance created from JSON data.
        """
        # Reading of the JSON
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Helper function to create a list of PreparedSession
        def parse_sessions(session_list):
            return [PreparedSession(**session_data) for session_data in session_list]

        # Parsing of the dataset
        training_set = parse_sessions(data.get("training_set", []))
        validation_set = parse_sessions(data.get("validation_set", []))
        test_set = parse_sessions(data.get("test_set", []))

        # Creation of the LearningSet
        learning_set = LearningSet(
            training_set=training_set,
            validation_set=validation_set,
            test_set=test_set
        )

        return learning_set

    def save_learning_set(self, learning_set: LearningSet, json_file_path: str):
        """
        Save a LearningSet object into a JSON file.

        Args:
            learning_set (LearningSet): The LearningSet instance to save.
            json_file_path (str): The path to the JSON file.
        """

        # Helper function to serialize a list of PreparedSession
        def serialize_sessions(session_list):
            return [
                {
                    "sessionID": session.sessionID,
                    "features": session.features,
                    "label": session.label
                } for session in session_list
            ]

        # Serialization of the dataset
        data = {
            "training_set": serialize_sessions(learning_set.training_set),
            "validation_set": serialize_sessions(learning_set.validation_set),
            "test_set": serialize_sessions(learning_set.test_set)
        }

        # Writing to the JSON file
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)



    def read_configuration_parameters(self, filepath):
        """
        Read a json file.

        Returns:
            filecontent: content of json file.

        """
        """
            dictionary that contains all the values of the configutation parameters
        """
        params = {}
        try:
            with open(filepath, "r") as f:
                filecontent = json.load(f)

            layers = filecontent.get('layers', {})
            neurons = filecontent.get('neurons', {})
            tolerance = filecontent.get('tolerance', {})

            params["min_layers"] = layers.get('min_layers')
            params["max_layers"] = layers.get('max_layers')
            params["step_layers"] = layers.get('step_layers')
            params["min_neurons"] = neurons.get('min_neurons')
            params["max_neurons"] = neurons.get('max_neurons')
            params["step_neurons"] = neurons.get('step_neurons')
            params["overfitting_tolerance"] = tolerance.get('overfitting_tolerance')
            params["generalization_tolerance"] = tolerance.get('generalization_tolerance')

            return params

        except Exception as e:
            print("Error to read file at path " + filepath + ": " + e)
            return None

    def save_average_hyperparams(self, avg_neurons, avg_layers, filepath):
        """
            Args:
                avg_neurons: avg_neurons value to write into json file
                avg_layers: avg_layers value to write into json file
                filepath: path where json file will be saved

            Returns:
                bool: True if the file is written successfully, False otherwise.
        """
        # Struttura dei dati da scrivere nel file JSON
        data = {
            "avg_neurons": avg_neurons,
            "avg_layers": avg_layers
        }

        try:
            # Scrittura nel file JSON
            with open(filepath, "w") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
                return True
        except Exception as e:
            print("Error to save file at path " + filepath + ": " + e)
            return False

    def read_json_file(self, filepath):
        """
        Read a json file.

        Returns:
            filecontent: content of json file.

        """
        try:
            with open(filepath, "r") as f:
                filecontent = json.load(f)
            return filecontent

        except Exception as e:
            print("Error to read file at path " + filepath + ": " + e)
            return None

    def write_json_file(self, data, filepath):
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
            print("Error to save file at path " + filepath + ": " + e)
            return False

    def read_winner_network(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)

        classifier = Classifier()
        classifier.set_num_iterations(data.get("num_iterations"))
        classifier.set_validation_error(data.get("validation_error"))
        classifier.set_training_error(data.get("training_error"))
        classifier.set_num_layers(data.get("num_layers"))
        classifier.set_num_neurons(data.get("num_neurons"))

        return classifier

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
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

# Example to test the class
if __name__ == "__main__":
    handler = JsonHandler()

    # Writing a json file
    data = {"name": "Mario", "age": 30, "hobby": ["sport", "coocking"]}
    handler.write_json_file(data, "esempio.json")

    # Reading a json file
    try:
        content = handler.read_json_file("esempio.json")
        print(content)
    except Exception as e:
        print(f"Errore: {e}")





