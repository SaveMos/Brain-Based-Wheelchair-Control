import unittest
from unittest.mock import patch, MagicMock
from production_system.production_orchestrator import ProductionOrchestrator
from production_system.configuration_parameters import ConfigurationParameters
from production_system.production_system_communication import ProductionSystemIO
from production_system.json_validation import JsonHandler
from production_system.classification import Classification
from production_system.deployment import Deployment

class TestProductionOrchestrator(unittest.TestCase):

    @patch('production_system.production_orchestrator.ProductionSystemIO')
    @patch('production_system.production_orchestrator.JsonHandler')
    @patch('production_system.production_orchestrator.Deployment')
    @patch('production_system.production_orchestrator.Classification')
    @patch('production_system.production_orchestrator.ConfigurationParameters')
    def test_develop_session(self, MockConfigurationParameters, MockClassification, MockDeployment, MockJsonHandler, MockProductionSystemIO):
        # Mock Configuration
        mock_config = MockConfigurationParameters.return_value
        mock_config.parameters = {"evaluation_phase": False, "max_session_production": 10, "max_session_evaluation": 5}
        mock_config.global_netconf = {"Ingestion System": {"ip": "151.83.144.119", "port": 5001},
                                      "Preparation System": {"ip": "151.83.144.119", "port": 5002},
                                      "Segregation System": {"ip": "188.217.91.69", "port": 5003},
                                      "Development System": {"ip": "87.19.204.54", "port": 5004},
                                      "Production System": {"ip": "109.116.135.145", "port": 5005},
                                      "Evaluation System": {"ip": "2.38.52.205", "port": 5030},
                                      "Messaging System": {"ip": "2.38.52.205", "port": 5010},
                                      "Service Class": {"ip": "2.38.52.205", "port": 5010}}
        # Mock ProductionSystemIO
        mock_io = MockProductionSystemIO.return_value
        mock_io.get_last_message.return_value = {
            'ip': "87.19.204.54",
            'message': {
                'num_iteration': 100,
                'num_layers': 3,
                'num_neurons': 128,
                'test_error': 0.05,
                'validation_error': 0.04,
                'training_error': 0.03
            }
        }

        # Mock JsonHandler
        mock_handler = MockJsonHandler.return_value
        mock_handler.validate_json.return_value = True

        # Mock Deployment
        mock_deployment = MockDeployment.return_value

        orchestrator = ProductionOrchestrator(service=False, unit_test=True)
        orchestrator.production()

        # Assertions
        mock_handler.validate_json.assert_called_once_with(
            mock_io.get_last_message.return_value['message'],
            "production_schema/ClassifierSchema.json"
        )
        mock_deployment.deploy.assert_called_once_with(mock_io.get_last_message.return_value['message'])

    @patch('production_system.production_orchestrator.ProductionSystemIO')
    @patch('production_system.production_orchestrator.JsonHandler')
    @patch('production_system.production_orchestrator.Classification')
    @patch('production_system.production_orchestrator.ConfigurationParameters')
    def test_classify_session(self, MockConfigurationParameters, MockClassification, MockJsonHandler, MockProductionSystemIO):
        # Mock Configuration
        mock_config = MockConfigurationParameters.return_value
        mock_config.parameters = {"evaluation_phase": True, "max_session_production": 10, "max_session_evaluation": 5}
        mock_config.global_netconf = {"Ingestion System": {"ip": "151.83.144.119", "port": 5001},
                                      "Preparation System": {"ip": "151.83.144.119", "port": 5002},
                                      "Segregation System": {"ip": "188.217.91.69", "port": 5003},
                                      "Development System": {"ip": "87.19.204.54", "port": 5004},
                                      "Production System": {"ip": "109.116.135.145", "port": 5005},
                                      "Evaluation System": {"ip": "2.38.52.205", "port": 5030},
                                      "Messaging System": {"ip": "2.38.52.205", "port": 5010},
                                      "Service Class": {"ip": "2.38.52.205", "port": 5010}}

        # Mock ProductionSystemIO
        mock_io = MockProductionSystemIO.return_value
        mock_io.get_last_message.return_value = {
            'ip': "151.83.144.119",
            'message': {
                'uuid': "001",
                'psd_alpha_band': 0.8,
                'psd_beta_band': 0.7,
                'psd_theta_band': 0.9,
                'psd_delta_band': 0.6,
                'activity': 4,
                'environment': 2
            }
        }

        # Mock JsonHandler
        mock_handler = MockJsonHandler.return_value
        mock_handler.validate_json.return_value = True

        # Mock Classification
        mock_classification = MockClassification.return_value
        mock_label = MagicMock()
        mock_classification.classify.return_value = mock_label

        orchestrator = ProductionOrchestrator(service=False, unit_test=True)
        orchestrator.production()

        # Assertions
        mock_handler.validate_json.assert_called_once_with(
            mock_io.get_last_message.return_value['message'],
            "production_schema/PreparedSessionSchema.json"
        )
        mock_classification.classify.assert_called_once()
        mock_io.send_label.assert_any_call(mock_config.global_netconf['Evaluation System']['ip'],
                                           mock_config.global_netconf['Evaluation System']['port'],
                                           mock_label)
        mock_io.send_label.assert_any_call(mock_config.global_netconf['Service Class']['ip'],
                                           mock_config.global_netconf['Service Class']['ip'],
                                           mock_label)


    @patch('production_system.production_orchestrator.ProductionSystemIO')
    @patch('production_system.production_orchestrator.ConfigurationParameters')
    def test_unknown_sender(self, MockConfigurationParameters, MockProductionSystemIO):
        # Mock Configuration
        mock_config = MockConfigurationParameters.return_value
        mock_config.global_netconf = {"Ingestion System": {"ip": "151.83.144.119", "port": 5001},
                                      "Preparation System": {"ip": "151.83.144.119", "port": 5002},
                                      "Segregation System": {"ip": "188.217.91.69", "port": 5003},
                                      "Development System": {"ip": "87.19.204.54", "port": 5004},
                                      "Production System": {"ip": "109.116.135.145", "port": 5005},
                                      "Evaluation System": {"ip": "2.38.52.205", "port": 5030},
                                      "Messaging System": {"ip": "2.38.52.205", "port": 5010},
                                      "Service Class": {"ip": "2.38.52.205", "port": 5010}}


        # Mock ProductionSystemIO
        mock_io = MockProductionSystemIO.return_value
        mock_io.get_last_message.return_value = {
            'ip': "192.168.0.3",
            'message': {}
        }

        orchestrator = ProductionOrchestrator(service=False, unit_test=True)
        orchestrator.production()

        # Assertions
        mock_io.get_last_message.assert_called_once()

    @patch('production_system.production_orchestrator.ProductionSystemIO')
    @patch('production_system.production_orchestrator.JsonHandler')
    @patch('production_system.production_orchestrator.Deployment')
    @patch('production_system.production_orchestrator.ConfigurationParameters')
    def test_invalid_classifier_schema(self, MockConfigurationParameters, MockDeployment, MockJsonHandler,
                                       MockProductionSystemIO):
        # Mock Configuration
        mock_config = MockConfigurationParameters.return_value
        mock_config.global_netconf = {"Ingestion System": {"ip": "151.83.144.119", "port": 5001},
                                      "Preparation System": {"ip": "151.83.144.119", "port": 5002},
                                      "Segregation System": {"ip": "188.217.91.69", "port": 5003},
                                      "Development System": {"ip": "87.19.204.54", "port": 5004},
                                      "Production System": {"ip": "109.116.135.145", "port": 5005},
                                      "Evaluation System": {"ip": "2.38.52.205", "port": 5030},
                                      "Messaging System": {"ip": "2.38.52.205", "port": 5010},
                                      "Service Class": {"ip": "2.38.52.205", "port": 5010}}

        # Mock ProductionSystemIO
        mock_io = MockProductionSystemIO.return_value
        mock_io.get_last_message.return_value = {
            'ip': "87.19.204.54",
            'message': {
                'num_iteration': 100,
                'num_layers': 3,
                'num_neurons': 128
                # Missing test_error, validation_error, and training_error
            }
        }

        # Mock JsonHandler
        mock_handler = MockJsonHandler.return_value
        mock_handler.validate_json.return_value = False

        orchestrator = ProductionOrchestrator(service=False, unit_test=True)
        orchestrator.production()

        # Assertions
        mock_handler.validate_json.assert_called_once_with(
            mock_io.get_last_message.return_value['message'],
            "production_schema/ClassifierSchema.json"
        )
        MockDeployment.deploy.assert_not_called()

    @patch('production_system.production_orchestrator.ProductionSystemIO')
    @patch('production_system.production_orchestrator.JsonHandler')
    @patch('production_system.production_orchestrator.Classification')
    @patch('production_system.production_orchestrator.ConfigurationParameters')
    def test_invalid_prepared_session_schema(self, MockConfigurationParameters, MockClassification, MockJsonHandler,
                                             MockProductionSystemIO):
        # Mock Configuration
        mock_config = MockConfigurationParameters.return_value
        mock_config.global_netconf = {"Ingestion System": {"ip": "151.83.144.119", "port": 5001},
                                      "Preparation System": {"ip": "151.83.144.119", "port": 5002},
                                      "Segregation System": {"ip": "188.217.91.69", "port": 5003},
                                      "Development System": {"ip": "87.19.204.54", "port": 5004},
                                      "Production System": {"ip": "109.116.135.145", "port": 5005},
                                      "Evaluation System": {"ip": "2.38.52.205", "port": 5030},
                                      "Messaging System": {"ip": "2.38.52.205", "port": 5010},
                                      "Service Class": {"ip": "2.38.52.205", "port": 5010}}


        # Mock ProductionSystemIO
        mock_io = MockProductionSystemIO.return_value
        mock_io.get_last_message.return_value = {
            'ip': "151.83.144.119",
            'message': {
                'uuid': "001",
                'psd_alpha_band': 0.8,
                'psd_beta_band': 0.7
                # Missing psd_tetha_band, psd_delta_band, activity, and environment
            }
        }

        # Mock JsonHandler
        mock_handler = MockJsonHandler.return_value
        mock_handler.validate_json.return_value = False

        orchestrator = ProductionOrchestrator(service=False, unit_test=True)
        orchestrator.production()

        # Assertions
        mock_handler.validate_json.assert_called_once_with(
            mock_io.get_last_message.return_value['message'],
            "production_schema/PreparedSessionSchema.json"
        )
        MockClassification.classify.assert_not_called()

if __name__ == '__main__':
    unittest.main()
