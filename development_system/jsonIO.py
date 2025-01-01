import json
import pandas as pd

from typing import Any

from jsonschema import validate, ValidationError, SchemaError
from segregation_system.prepared_session import PreparedSession
from segregation_system.learning_set import LearningSet
from development_system.classifier import Classifier


class JsonHandler:
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
            with open(json_file, 'r') as jf:
                json_data = json.load(jf)

            # Load JSON schema
            with open(schema_file, 'r') as sf:
                json_schema = json.load(sf)

            # Validate JSON against schema
            validate(instance=json_data, schema=json_schema)
            print("JSON is valid.")
            return True

        except ValidationError as ex:
            print(f"Validation Error: {ex.message}")
        except SchemaError as ex:
            print(f"Schema Error: {ex.message}")
        except Exception as ex:
            print(f"Error: {ex}")

        return False
    @staticmethod
    def json_to_learning_set(json_file_path: str) -> LearningSet:
        """
        Convert a JSON file in a LearningSet object.

        Args:
            json_file_path (str): The path to the JSON file.

        Returns:
            LearningSet: A LearningSet instance created from JSON data.
        """
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

    @staticmethod
    def create_learning_set_from_json(json_file_path: str) -> LearningSet:
        """
        Converts a JSON file to a LearningSet object.

        Args:
            json_file_path (str): Path to the JSON file containing the data.

        Returns:
            LearningSet: An instance of the LearningSet class populated with the data from the JSON file.

        Raises:
            FileNotFoundError: If the JSON file does not exist.
            KeyError: If required keys are missing in the JSON data.
            ValueError: If the data types do not match the expected structure.
        """
        try:
            with open(json_file_path, 'r') as file:
                current_data = json.load(file)
        except FileNotFoundError as ex:
            raise FileNotFoundError(f"File not found: {ex}")

        # Helper function to convert a dictionary to a PreparedSession object
        def dict_to_prepared_session(session_dict: dict) -> PreparedSession:
            try:
                uuid = session_dict['uuid']
                label = session_dict['label']
                features = [
                    (
                        session_dict['psd_alpha_band'],
                        session_dict['psd_beta_band'],
                        session_dict['psd_theta_band'],
                        session_dict['psd_delta_band'],
                        session_dict['activity'],
                        session_dict['environment'],
                    )
                ]
                return PreparedSession(uuid=uuid, features=features, label=label)
            except KeyError as er:
                raise KeyError(f"Missing key in session dictionary: {er}")

        # Convert each set in the JSON to a list of PreparedSession objects
        training_set = [dict_to_prepared_session(session) for session in current_data.get('training_set', [])]
        validation_set = [dict_to_prepared_session(session) for session in current_data.get('validation_set', [])]
        test_set = [dict_to_prepared_session(session) for session in current_data.get('test_set', [])]

        # Create and return the LearningSet object
        return LearningSet(training_set=training_set, validation_set=validation_set, test_set=test_set)


    @staticmethod
    def save_learning_set(learning_set: LearningSet):
        """
           Saves the training, validation, and test sets of a LearningSet instance to JSON files.

           Args:
               learning_set (LearningSet): An instance containing training, validation, and test sets.

           Returns:
               None
           """
        def session_to_dict(session: PreparedSession) -> dict:
            """
                Converts a PreparedSession object into a dictionary.

                Args:
                    session (PreparedSession): The session to convert.

                Returns:
                    dict: A dictionary representation of the session.
            """
            return {
                "uuid": session.uuid,
                "label": session.label,
                "psd_alpha_band": session.features[0][0],
                "psd_beta_band": session.features[0][1],
                "psd_theta_band": session.features[0][2],
                "psd_delta_band": session.features[0][3],
                "activity": session.features[0][4],
                "environment": session.features[0][5]
            }

        training_data = [session_to_dict(session) for session in learning_set.training_set]
        validation_data = [session_to_dict(session) for session in learning_set.validation_set]
        test_data = [session_to_dict(session) for session in learning_set.test_set]

        with open('data/training_set.json', 'w') as f:
            json.dump({"training_set": training_data}, f, indent=4)

        with open('data/validation_set.json', 'w') as f:
            json.dump({"validation_set": validation_data}, f, indent=4)

        with open('data/test_set.json', 'w') as f:
            json.dump({"test_set": test_data}, f, indent=4)


    @staticmethod
    def print_learning_set(learning_set: LearningSet):
        """
           Prints the contents of the training, validation, and test sets in a LearningSet instance.

           Args:
               learning_set (LearningSet): An instance containing training, validation, and test sets.

           Returns:
               None
        """
        def print_session(current_session: PreparedSession):
            """
                Prints the details of a single PreparedSession.

                Args:
                    current_session (PreparedSession): The session whose details are to be printed.

                Returns:
                    None
            """
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


    @staticmethod
    def read_configuration_parameters(filepath):
        """
        Read a json file that contains the parameters.

        Returns:
            file_content: content of json file.

        """
        """
            dictionary that contains all the values of the configure parameters
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


    @staticmethod
    def save_average_hyperparams(avg_neurons, avg_layers, filepath):
        """
            Args:
                avg_neurons: avg_neurons value to write into json file
                avg_layers: avg_layers value to write into json file
                filepath: path where json file will be saved

            Returns:
                bool: True if the file is written successfully, False otherwise.
        """

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

    @staticmethod
    def read_json_file(filepath):
        """
        Read a json file.

        Returns:
            file_content: content of json file.

        """
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

    @staticmethod
    def extract_features_and_labels(data_set, set_type):
        """
        Extracts features and labels from a set of data.

        Args:
            data_set (dict): A dictionary which contains a set of data (ex. "test_set").
            set_type (str): Type of dictionary that contains a set.

        Returns:
            list: A list containing two elements:
                  - features (pd.DataFrame): A DataFrame with the characteristics.
                  - labels (pd.Series): Series with the labels.
        """

        activity_mapping = {"shopping": 0, "sport": 1, "cooking": 2, "relax": 3, "gaming": 4}

        environment_mapping = {"slippery": 0, "plain": 1, "slope": 2, "house": 3, "track": 4}

        current_set = data_set[set_type]

        current_data = pd.DataFrame([
            {
                "psd_alpha_band": record["psd_alpha_band"],
                "psd_beta_band": record["psd_beta_band"],
                "psd_theta_band": record["psd_theta_band"],
                "psd_delta_band": record["psd_delta_band"],
                "activity": activity_mapping.get(record["activity"], -1),  # Default value -1 if doesn't find
                "environment": environment_mapping.get(record["environment"], -1),  # Default value -1 if doesn't find
                "label": record["label"]
            }
            for record in current_set
        ])

        # Separation of the features and labels
        #features = pd.DataFrame(data["features"].to_list())
        features = current_data.drop(columns=["label"])
        labels = current_data["label"]

        return [features, labels]