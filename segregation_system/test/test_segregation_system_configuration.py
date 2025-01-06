import unittest

from segregation_system.SegregationSystemJsonHandler import SegregationSystemJsonHandler
from segregation_system.segregation_system_parameters import SegregationSystemConfiguration


class TestSegregationSystemConfiguration(unittest.TestCase):

    def test_configure_parameters(self):
        file_path = "conf/segregation_system_configuration.json"
        json_handler = SegregationSystemJsonHandler()
        config_data = json_handler.read_json_file(file_path)

        SegregationSystemConfiguration.configure_parameters("conf/segregation_system_configuration.json" ,"conf/netconf.json")

        # Assert the values have been set correctly.
        self.assertEqual(SegregationSystemConfiguration.LOCAL_PARAMETERS["minimum_number_of_collected_sessions"],
                         config_data.get("minimum_number_of_collected_sessions"))
        self.assertEqual(SegregationSystemConfiguration.LOCAL_PARAMETERS["tolerance_interval"],
                         config_data["tolerance_interval"])
        self.assertEqual(SegregationSystemConfiguration.LOCAL_PARAMETERS["training_set_percentage"],
                         config_data["training_set_percentage"])
        self.assertEqual(SegregationSystemConfiguration.LOCAL_PARAMETERS["validation_set_percentage"],
                         config_data["validation_set_percentage"])
        self.assertEqual(SegregationSystemConfiguration.LOCAL_PARAMETERS["number_of_training_sessions"],
                         config_data["number_of_training_sessions"])



    def test_validate_json(self):
        valid_json = {
            "minimum_number_of_collected_sessions": 10,
            "tolerance_interval": 5,
            "training_set_percentage": 0.7,
            "validation_set_percentage": 0.2,
            "number_of_training_sessions": 50
        }

        invalid_json = {
            "minimum_number_of_collected_sessions": "ten",  # Invalid type
            "tolerance_interval": 5,
            "training_set_percentage": 0.7,
            "validation_set_percentage": 0.2,
            "number_of_training_sessions": 50
        }


        # Test valid JSON
        self.assertTrue(SegregationSystemConfiguration.validate_json(valid_json, "local"))

        # Test invalid JSON
        self.assertFalse(SegregationSystemConfiguration.validate_json(invalid_json, "local"))


if __name__ == '__main__':
    unittest.main()
