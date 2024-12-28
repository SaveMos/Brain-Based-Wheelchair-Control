"""
Author: Alessandro Ascani
"""
import unittest
from unittest.mock import MagicMock, patch
from sklearn.neural_network import MLPClassifier
from production_system.classifier_controller import ClassifierController
from production_system.label import Label
from production_system.prepared_session import PreparedSession


class TestClassifierController(unittest.TestCase):

    @patch("joblib.dump")
    def test_deploy(self, mock_dump):
        """
        Test that the deploy method correctly saves the classifier.
        """
        classifier = MagicMock(spec=MLPClassifier)
        ClassifierController.deploy(classifier)
        mock_dump.assert_called_once_with(classifier, "model/classifier.sav")

    @patch("joblib.load")
    @patch("pandas.DataFrame")
    def test_classify(self, mock_dataframe, mock_load):
        """
        Test the classify method.
        """
        # Mocking a prepared session
        mock_prepared_session = MagicMock(spec=PreparedSession)
        mock_prepared_session.features = [0.8, 0.7, 0.9, 0.6]
        mock_prepared_session.uuid = "001"

        # Mocking the classifier
        mock_classifier = MagicMock(spec=MLPClassifier)
        mock_classifier.predict.return_value = ["movement"]
        mock_load.return_value = mock_classifier

        # Mocking DataFrame
        mock_dataframe.return_value = MagicMock()

        controller = ClassifierController()
        label = controller.classify(mock_prepared_session)

        # Assertions
        mock_load.assert_called_once_with("model/classifier.sav")
        mock_dataframe.assert_called_once_with({
            'PSD_alpha_band': [0.8],
            'PSD_beta_band': [0.7],
            'PSD_theta_band': [0.9],
            'PSD_delta_band': [0.6]
        })
        mock_classifier.predict.assert_called_once()

        self.assertIsInstance(label, Label)
        self.assertEqual(label.uuid, "001")
        self.assertEqual(label.movements, ["movement"])

if __name__ == "__main__":
    unittest.main()
