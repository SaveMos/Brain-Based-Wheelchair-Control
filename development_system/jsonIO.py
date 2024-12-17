import json
from segregation_system.prepared_session import PreparedSession
from segregation_system.learning_set import LearningSet

class JsonHandler:
    """
        A class to read and save file json
    """

    def create_learning_set_from_json(self, json_data: str) -> LearningSet:
        """
        Convert a JSON file in a LearningSet obgect.

        Args:
            json_data (str): The content of the JSON file as string.

        Returns:
            LearningSet: A LearningSet instance created from JSON data.
        """
        # Parsing of the JSON
        data = json.loads(json_data)

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

    def read_user_responses(self, filepath):
        """Load the status from the JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)

    def write_json_file(self, data, filepath):
        """
            Args:
                data: data to write into json file
                filepath: path where json file will be save

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





