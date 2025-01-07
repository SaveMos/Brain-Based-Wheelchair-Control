"""
Author: Alessandro Ascani
"""

class Deployment:
    """
     Class that execute deployment operation
    """

    @staticmethod
    def deploy(classifier):
        """
        Saves the provided classifier in a .sav file
        Args:
            classifier_json: file json of classifier to save
        """
        try:
            binary_content = classifier.encoded('latin1')
            with  open("model/classifier.sav", "wb") as f:
                f.write(binary_content)

            return True

        except (UnicodeEncodeError, IOError) as e:
            return False
