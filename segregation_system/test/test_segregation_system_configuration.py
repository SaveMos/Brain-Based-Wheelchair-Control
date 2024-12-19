import unittest

from segregation_system.segregation_system_configuration import SegregationSystemConfiguration
from utility.json_handler.json_handler import JsonHandler


class TestSegregationSystemConfiguration(unittest.TestCase):

    def test_configure_parameters(self):
        file_path = "../conf/segregation_system_configuration.json"
        json_handler = JsonHandler()
        config_data = json_handler.read_json_file(file_path)

        config = SegregationSystemConfiguration()
        config.configure_parameters(file_path)


        # Assert the values have been set correctly
        self.assertEqual(config.minimum_number_of_collected_sessions, config_data["minimum_number_of_collected_sessions"])
        self.assertEqual(config.tolerance_interval, config_data["tolerance_interval"])
        self.assertEqual(config.training_set_percentage, config_data["training_set_percentage"])
        self.assertEqual(config.validation_set_percentage, config_data["validation_set_percentage"])
        self.assertEqual(config.number_of_training_sessions, config_data["number_of_training_sessions"])


if __name__ == '__main__':
    unittest.main()
