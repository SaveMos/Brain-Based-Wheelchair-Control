import unittest
from unittest.mock import patch, mock_open
import jsonschema
import json
from evaluation_system.EvaluationSystemParameters import EvaluationSystemParameters

class TestEvaluationSystemParameters(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("evaluation_system.EvaluationSystemParameters.EvaluationSystemParameters._validate_json")
    def test_load_parameters_success(self, mock_validate_json, mock_json_load, mock_file):
        """Test successful loading of parameters."""
        # Mock valid JSON data for local and global parameters
        local_parameters = {
            "minimum_number_labels": 10,
            "total_errors": 5,
            "max_consecutive_errors": 2,
            "testing": True
        }
        global_parameters = {
            "Evaluation System": {"port": 5006},
            "Ingestion System": {"ip": "127.0.0.1"},
            "Production System": {"ip": "127.0.0.2"},
            "Messaging System": {"ip": "127.0.0.3", "port": 5000},
            "Service Class": {"ip": "127.0.0.4", "port": 5001}
        }

        # Setup mock behaviors
        mock_json_load.side_effect = [local_parameters, global_parameters]
        mock_validate_json.return_value = True

        # Call the method
        EvaluationSystemParameters.loadParameters(basedir="..")

        # Assert local parameters
        self.assertEqual(EvaluationSystemParameters.MINIMUM_NUMBER_LABELS, 10)
        self.assertEqual(EvaluationSystemParameters.TOTAL_ERRORS, 5)
        self.assertEqual(EvaluationSystemParameters.MAX_CONSECUTIVE_ERRORS, 2)
        self.assertTrue(EvaluationSystemParameters.TESTING)

        # Assert global parameters
        self.assertEqual(EvaluationSystemParameters.EVALUATION_SYSTEM_PORT, 5006)
        self.assertEqual(EvaluationSystemParameters.INGESTION_SYSTEM_IP, "127.0.0.1")
        self.assertEqual(EvaluationSystemParameters.PRODUCTION_SYSTEM_IP, "127.0.0.2")
        self.assertEqual(EvaluationSystemParameters.MESSAGING_SYSTEM_IP, "127.0.0.3")
        self.assertEqual(EvaluationSystemParameters.MESSAGING_SYSTEM_PORT, 5000)
        self.assertEqual(EvaluationSystemParameters.SERVICE_CLASS_IP, "127.0.0.4")
        self.assertEqual(EvaluationSystemParameters.SERVICE_CLASS_PORT, 5001)

        # Assert file open calls
        self.assertEqual(mock_file.call_count, 2)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("evaluation_system.EvaluationSystemParameters.EvaluationSystemParameters._validate_json")
    def test_load_parameters_invalid_local(self, mock_validate_json, mock_json_load, mock_file):
        """Test loading parameters with invalid local parameters."""
        # Mock invalid local JSON data
        local_parameters = {}
        global_parameters = {
            "Evaluation System": {"port": 5006},
            "Ingestion System": {"ip": "127.0.0.1"},
            "Production System": {"ip": "127.0.0.2"},
            "Messaging System": {"ip": "127.0.0.3", "port": 5000},
            "Service Class": {"ip": "127.0.0.4", "port": 5001}
        }

        # Setup mock behaviors
        mock_json_load.side_effect = [local_parameters, global_parameters]
        mock_validate_json.side_effect = [False, True]

        # Call the method
        EvaluationSystemParameters.loadParameters(basedir="..")

        # Assert local parameters remain None
        self.assertIsNone(EvaluationSystemParameters.MINIMUM_NUMBER_LABELS)
        self.assertIsNone(EvaluationSystemParameters.TOTAL_ERRORS)
        self.assertIsNone(EvaluationSystemParameters.MAX_CONSECUTIVE_ERRORS)
        self.assertIsNone(EvaluationSystemParameters.TESTING)

        # Assert global parameters are loaded
        self.assertEqual(EvaluationSystemParameters.EVALUATION_SYSTEM_PORT, 5006)
        self.assertEqual(EvaluationSystemParameters.INGESTION_SYSTEM_IP, "127.0.0.1")
        self.assertEqual(EvaluationSystemParameters.PRODUCTION_SYSTEM_IP, "127.0.0.2")
        self.assertEqual(EvaluationSystemParameters.MESSAGING_SYSTEM_IP, "127.0.0.3")
        self.assertEqual(EvaluationSystemParameters.MESSAGING_SYSTEM_PORT, 5000)
        self.assertEqual(EvaluationSystemParameters.SERVICE_CLASS_IP, "127.0.0.4")
        self.assertEqual(EvaluationSystemParameters.SERVICE_CLASS_PORT, 5001)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_validate_json_valid(self, mock_json_load, mock_file):
        """Test validation of valid JSON data."""
        schema = {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]}
        valid_json = {"key": "value"}

        mock_file.return_value.read.return_value = json.dumps(schema)
        with patch("jsonschema.validate", return_value=None):
            result = EvaluationSystemParameters._validate_json(valid_json, "local", basedir="..")
            self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_validate_json_invalid(self, mock_json_load, mock_file):
        """Test validation of invalid JSON data."""
        schema = {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]}
        invalid_json = {}

        mock_file.return_value.read.return_value = json.dumps(schema)
        with patch("jsonschema.validate", side_effect=jsonschema.ValidationError("Invalid JSON")):
            result = EvaluationSystemParameters._validate_json(invalid_json, "local", basedir="..")
            self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
