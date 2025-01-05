"""
Author: Francesco Taverna
"""
import json
import logging

import jsonschema

class JsonHandler:
    """
        A class to read and save file json
    """

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

    def convert_dictionary_to_json(self, dictionary):

        return json.dumps(dictionary)

    # validate Json sent as a python dictionary
    def validate_json(self, json_data: dict, schema_path: str) -> bool:
        """
            Validate a json object against a json schema in a file.
            :param json_data: json object
            :param schema_path: path to the json schema relative to the data folder
            :return: True if json object is valid, False otherwise
            """
        with open(schema_path, "r", encoding="UTF-8") as file:
            json_schema = json.load(file)
        try:
            jsonschema.validate(instance=json_data, schema=json_schema)
        except jsonschema.exceptions.ValidationError as ex:
            logging.error(ex)
            return False
        return True


    def validate_json_from_path(self, json_path: str, schema_path: str) -> bool:
        """
        Validate a json file against a json schema in a file.
        :param json_path: file containing the json object
        :param schema_path: file containing the json schema
        :return: True if json object is valid, False otherwise
        """
        with open(json_path, "r", encoding="UTF-8") as file:
            json_data = json.load(file)
        return self.validate_json(json_data, schema_path)

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





