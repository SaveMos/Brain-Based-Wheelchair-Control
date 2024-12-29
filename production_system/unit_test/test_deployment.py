import unittest
from unittest.mock import patch, MagicMock
from production_system.deployment import Deployment

class TestDeployment(unittest.TestCase):

    @patch('production_system.deployment.joblib.dump')
    def test_deploy(self, mock_dump):
        # Create a mock classifier
        mock_classifier = MagicMock()

        # Call the deploy method
        Deployment.deploy(mock_classifier)

        # Verify that joblib.dump was called with the correct arguments
        mock_dump.assert_called_once_with(mock_classifier, "model/classifier.sav")

if __name__ == "__main__":
    unittest.main()

