import unittest
from unittest.mock import patch, MagicMock
from production_system.deployment import Deployment
from production_system.classifier import Classifier
import joblib

class TestDeployment(unittest.TestCase):

    @patch('production_system.deployment.joblib.dump')
    @patch('production_system.deployment.Classifier')
    def test_deploy_valid_classifier(self, MockClassifier, mock_joblib_dump):
        # Mock Classifier instance
        mock_classifier_instance = MagicMock()
        MockClassifier.return_value = mock_classifier_instance

        # Input data for the classifier
        classifier_data = {
            'num_iteration': 100,
            'num_layers': 3,
            'num_neurons': 128,
            'test_error': 0.05,
            'validation_error': 0.04,
            'training_error': 0.03
        }

        # Call the deploy method
        Deployment.deploy(classifier_data)

        # Assertions
        MockClassifier.assert_called_once_with(
            classifier_data['num_iteration'],
            classifier_data['num_layers'],
            classifier_data['num_neurons'],
            classifier_data['test_error'],
            classifier_data['validation_error'],
            classifier_data['training_error']
        )
        mock_joblib_dump.assert_called_once_with(mock_classifier_instance, "model/classifier.sav")

if __name__ == '__main__':
    unittest.main()
