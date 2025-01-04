from development_system.json_validator_reader_and_writer import JsonValidatorReaderAndWriter


class ConfigurationParameters:
    """Class representing configuration parameters of the development system."""

    min_layers = None
    max_layers = None
    step_layers = None
    min_neurons = None
    max_neurons = None
    step_neurons = None
    overfitting_tolerance = None
    generalization_tolerance = None
    service_flag = None

    @staticmethod
    def load_configuration():
        """Load configuration parameters from a JSON file."""
        read_conf = JsonValidatorReaderAndWriter()  # instance of JsonHandler class
        read_conf.validate_json("conf/development_parameters.json", "schemas/development_parameters_schema.json")
        filepath = "conf/development_parameters.json"

        params = read_conf.read_configuration_parameters(filepath)

        ConfigurationParameters.min_layers = params["min_layers"]
        ConfigurationParameters.max_layers = params["max_layers"]
        ConfigurationParameters.step_layers = params['step_layers']
        ConfigurationParameters.min_neurons = params['min_neurons']
        ConfigurationParameters.max_neurons = params['max_neurons']
        ConfigurationParameters.step_neurons = params['step_neurons']
        ConfigurationParameters.overfitting_tolerance = params['overfitting_tolerance']
        ConfigurationParameters.generalization_tolerance = params['generalization_tolerance']
        ConfigurationParameters.service_flag = params['service_flag']
