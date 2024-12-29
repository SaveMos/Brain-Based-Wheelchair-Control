"""
Author: Alessandro Ascani
"""
import unittest
from unittest.mock import patch, MagicMock
from production_system.classification import Classification
from production_system.prepared_session import PreparedSession
from production_system.label import Label

class TestClassification(unittest.TestCase):

    @patch('production_system.classification.joblib.load')
    def test_classify(self, mock_load):
        # Mocking the classifier
        mock_classifier = MagicMock()
        mock_classifier.predict.return_value = ['MovementLabel']
        mock_load.return_value = mock_classifier

        # Creating a mock PreparedSession
        mock_prepared_session = PreparedSession("mock_uuid", [0.8, 0.7, 0.9, 0.6])

        # Instance of the Classification class
        classifier = Classification()

        # Call the classify method
        result = classifier.classify(mock_prepared_session)

        # Assertions
        self.assertIsInstance(result, Label)
        self.assertEqual(result.uuid, "mock_uuid")
        self.assertEqual(result.movements, ['MovementLabel'])

        # Verify that the classifier's predict method was called correctly
        mock_classifier.predict.assert_called_once()

if __name__ == "__main__":
    unittest.main()

