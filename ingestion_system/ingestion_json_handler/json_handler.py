import json

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





