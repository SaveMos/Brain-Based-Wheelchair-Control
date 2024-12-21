import unittest

from segregation_system.prepared_session import PreparedSession
from segregation_system.test.test_utility_lib import generate_random_prepared_sessions_object


class TestPreparedSession(unittest.TestCase):
    def setUp(self):
        """
        This method is called before every test.
        """
        Session = generate_random_prepared_sessions_object(1)
        Session = Session[0]
        self.test_data = Session.to_dictionary()

        # Create a session object using from_dict
        self.session = PreparedSession(
            uuid=self.test_data['uuid'],
            features=[
                self.test_data['psd_alpha_band'],
                self.test_data['psd_beta_band'],
                self.test_data['psd_theta_band'],
                self.test_data['psd_delta_band'],
                self.test_data['activity'],
                self.test_data['environment']
            ],
            label=self.test_data['label']
        )

    def test_from_dict(self):
        """
        Test the from_dict method to ensure it correctly initializes an object from a dictionary.
        """
        new_session = PreparedSession('', [], '')  # Start with empty values
        new_session.from_dict(self.test_data)

        # Check if the session object has been correctly initialized
        self.assertEqual(new_session._uuid, self.test_data['uuid'])
        self.assertEqual(new_session._features, [
            self.test_data['psd_alpha_band'],
            self.test_data['psd_beta_band'],
            self.test_data['psd_theta_band'],
            self.test_data['psd_delta_band'],
            self.test_data['activity'],
            self.test_data['environment']
        ])
        self.assertEqual(new_session._label, self.test_data['label'])

    def test_to_dictionary(self):
        """
        Test the to_dictionary method to ensure it correctly converts an object to a dictionary.
        """
        result = self.session.to_dictionary()

        print(result)
        # Check if the dictionary contains the correct values
        self.assertEqual(result['uuid'], self.test_data['uuid'])
        self.assertEqual(result['label'], self.test_data['label'])
        self.assertEqual(result['psd_alpha_band'], self.test_data['psd_alpha_band'])
        self.assertEqual(result['psd_beta_band'], self.test_data['psd_beta_band'])
        self.assertEqual(result['psd_theta_band'], self.test_data['psd_theta_band'])
        self.assertEqual(result['psd_delta_band'], self.test_data['psd_delta_band'])
        self.assertEqual(result['activity'], self.test_data['activity'])
        self.assertEqual(result['environment'], self.test_data['environment'])


if __name__ == '__main__':
    unittest.main()
