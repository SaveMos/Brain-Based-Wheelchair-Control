import json

class JsonHandler:
    """
        A class to read and save file json
    """

    def read_json_file(self, filepath):
        """
        Read a json file.

        Returns the content of the json file.

        """

        try:
            with open(filepath, "r") as f:
                return json.load(f)

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

    def write_field_to_json(self , file_path: str, field_name: str, value):
        """
        Updates the value of a specific field in a JSON file using `write_json_file`.

        Args:
            file_path (str): Path to the JSON file.
            field_name (str): The field name to update.
            value: The new value to set for the field.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            # Load the existing data
            data = self.read_json_file(file_path)

            # Update the field
            data[field_name] = value

            # Save the updated data using the provided write_json_file helper
            return self.write_json_file(data, file_path)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return False
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
            return False

    def read_field_from_json(self, file_path: str, field_name: str):
        """
        Reads the value of a specific field from a JSON file.

        Args:
            file_path (str): Path to the JSON file.
            field_name (str): The field name to retrieve the value for.

        Returns:
            The value of the specified field or None if the field does not exist.
        """
        return self.read_json_file(file_path).get(field_name, None)

    def get_system_address(self , json_filepath: str, system_name: str) -> dict:
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





